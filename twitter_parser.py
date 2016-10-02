import geocoder

from twitter import *
from unicode_funcs import *
from difflib import SequenceMatcher

from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.classify import NaiveBayesClassifier

class TwitterParser(object):
    stopWords = dict([(word, True) for word in stopwords.words('english')]) #nltk's stopwords
    stopWords2 = [".","!","?","rt","@","=","+","-","&amp;","follow","i'm","i'll"]
    stopWords2 = dict([(to_unicode(word), True) for word in stopWords2]) #my own set of stopwords
    stopWords.update(stopWords2)

    def __init__(self, auth):
        self.api = Twitter(auth=auth)
        self.stemmer = PorterStemmer()
        self.__create_classifier()

    def search(self, query, place):
        #get first 100 tweets
        #twitter_api.search.tweets() returns a dictionary
        tweets = self.api.search.tweets(q = query,
                                        place = place,
                                        lang = "en",
                                        count = 100)["statuses"]

        numPos=0.0
        numNeg=0.0

        formatted_tweets = list()
        for tweet in tweets:
            ftweet = self.parse(tweet, query)
            formatted_tweets.append(ftweet)
            if ftweet['sentiment'] == "neg":
                numNeg=numNeg+1
            else:
                numPos=numPos+1

        return (formatted_tweets, numPos/(numPos+numNeg))

    def parse(self, tweet, query):
        if tweet["coordinates"]:
            coordinates = tweet["coordinates"]
        elif tweet["user"]["location"]:
            location = tweet["user"]["location"]
            coordinates = self.geocode(location)
            if coordinates == False:
                lat = ""
                lng = ""
            else:
                lat = coordinates[0]
                lng = coordinates[1]
        else:
            lat = ""
            lng = ""

        person = tweet["user"]["screen_name"]
        numRetweets=tweet["retweet_count"]
        geocode=tweet["geo"]
        time=tweet["created_at"].split(" +")[0]
        text = tweet['text']

        tweetFeatures = self.extract_features_from(tweet["text"])
        if tweetFeatures is not None:
            polarity = self.classifier.classify(tweetFeatures)

        return {
            'text': text,
            'subject': query,
            'sentiment': polarity,
            'user': person,
            'geocode': geocode,
            'time': time,
            'lat': lat,
            'lng': lng,
            'retweets': numRetweets
        }


    def geocode(self, location):
        if location:
            g = geocoder.google(location)
            if(len(g.latlng) != 2):
                return False
            return g.latlng
        else:
            return False

    def __similar(self, a, b):
        return SequenceMatcher(None, a, b).ratio()


    #stems the word and lowercases it
    def __normalize(self, word):
        return self.stemmer.stem(word.lower())

    #return tuple (features, label)
    #for input into NLTK's Naive Bayes Classifier
    def __feature_tuple(self, fileName, mode, label):
        features = self.__word_features(fileName, mode)
        return (features, label)

    #add each word from the corpus into our dictionary
    #if it's not a stopword
    def __word_features(self, fileName, mode):
        corpus = open(fileName, mode)
        features = dict()
        for line in corpus:
            line = to_unicode(line)
            newFeatures = self.extract_features_from(line)
            if newFeatures is not None:  #if line is NoneType, skip to next line
                features.update(newFeatures)
        corpus.close()
        return features

    def __create_classifier(self):
        print "Determining polarity of features..."

        #NLTK classifiers work on "featstructs", simple dictionaries
        #mapping a feature name to a feature value
        #We use booleans to indicate that the set (a tweet) does (or doesn't) contain a feature
        #For more information: http://www.nltk.org/howto/featstruct.html

        #pos/negfeats are tuples (dict, label)
        #Where dict is a dictionary of (word, boolean) key-val pairs
        #label indicates positive or negative
        posfeats = self.__feature_tuple("corpora/finalPositiveCorpus.txt", "r", "pos")
        negfeats = self.__feature_tuple("corpora/finalNegativeCorpus.txt", "r", "neg")

        #a list of (dict, label) tuples, one for each label
        trainfeats=[posfeats,negfeats]

        print "Training the classifier..."

        #input: list of (dict, label) tuples, one for each label (pos, neg)
        #output: trained classifier that can identify each label
        self.classifier = NaiveBayesClassifier.train(trainfeats)

    # iterate through every word in text, normalize it, and remove stopwords
    # Note that normalization (word.lower()) is not needed
    # because the Stanford corpus is already lowercase
    # Other corpora might need to be normalized, however
    def extract_features_from(self, text):
        if text is not None:
            return dict([(self.__normalize(word), True) for word in text.split()
                        if word not in TwitterParser.stopWords])
        else:
            return None
