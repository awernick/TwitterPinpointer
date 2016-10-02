import twitter
from unicodeFunctions import *
from featureFunctions import *
from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.util import *
from trainClassifier import trainClassifier

CONSUMER_KEY= "eJxO5gRMjIDyUOFIDTHobsoTd"
CONSUMER_SECRET= "w6ew70tpmuPwbqBwdxvRpE35Zg7bniHfk2EkhMe5c35BQwoWNL"
OAUTH_TOKEN= "740720624880881666-OCWQWAN52rD66EHjGrwqti58qta1Dqd"
OAUTH_TOKEN_SECRET= "qWYkEfk9bL26TnMALPl5vuIRFTrHVMgJXsI84XjxciZ54"

auth=twitter.oauth.OAuth(OAUTH_TOKEN,OAUTH_TOKEN_SECRET,CONSUMER_KEY,CONSUMER_SECRET)
twitter_api = twitter.Twitter(auth=auth)

def getHistoricalTweets(locationID):
    classifier = trainClassifier()

    trumpResults = twitterSearch("Trump", locationID, classifier, twitter_api)
    listOfTrumpTweets = trumpResults[0]
    trumpSentimentRatio = trumpResults[1]

    hillaryResults = twitterSearch("Hillary", locationID, classifier, twitter_api)
    listOfHillaryTweets = hillaryResults[0]
    hillarySentimentRatio = hillaryResults[1]

    return {'tweets': {'trump': listOfTrumpTweets, 'hillary': listOfHillaryTweets}, 'sentiment_ratio': {'trump': trumpSentimentRatio, 'hillary': hillarySentimentRatio}}


#returns (listOfTweets, sentimentRatio)
    #where sentiment ratio is (#positive)/(#negative)
def twitterSearch(query, locationID, classifier, twitter_api):
	#get first 100 tweets
    #twitter_api.search.tweets() returns a dictionary
    listOfTweets = twitter_api.search.tweets(q = query, place = locationID, lang = "en", count = 100)["statuses"] 
    
    numPos=0.0
    numNeg=0.0

    listOfFormattedTweets = list()
    for tweet in listOfTweets:
        place=utf8(tweet["user"]["location"])
        person=utf8(tweet["user"]["screen_name"])
        numRetweets=tweet["retweet_count"]
        geocode=tweet["geo"]
        time=tweet["created_at"].split(" +")[0]
        text=utf8(tweet['text'])

        tweetFeatures = extractFeaturesFrom(tweet["text"])
        if tweetFeatures is not None:
            polarity = classifier.classify(tweetFeatures)
            if polarity == "neg":
                numNeg=numNeg+1
            elif polarity == "pos":
                numPos=numPos+1
        
        formattedTweet = {
            'text': text,
             'subject': query,
             'sentiment': polarity,
             'place': place,
             'user': person,
             'geocode': geocode,
             'time': time,
             'retweets': numRetweets
            }
        listOfFormattedTweets.append(formattedTweet)

    return (listOfFormattedTweets, numPos/(numPos+numNeg))

#get from US
if __name__ == "__main__":
    print getHistoricalTweets(1)