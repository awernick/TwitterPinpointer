from unicodeFunctions import *

from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
stemmer = PorterStemmer()

stopWords = dict([(word, True) for word in stopwords.words('english')]) #nltk's stopwords
stopWords2 = [".","!","?","rt","@","=","+","-","&amp;","follow","i'm","i'll"]
stopWords2 = dict([(toUnicode(word), True) for word in stopWords2]) #my own set of stopwords
stopWords.update(stopWords2)

#stems the word and lowercases it
def normalize(word):
     return stemmer.stem(word.lower())

#return tuple (features, label)
#for input into NLTK's Naive Bayes Classifier
def feature_tuple(fileName, mode, label):
   features = word_features(fileName, mode)
   return (features, label)

#add each word from the corpus into our dictionary
    #if it's not a stopword
#Note that normalization (word.lower()) is not needed 
    #because the Stanford corpus is already lowercase
#Other corpora might need to be normalized, however
def word_features(fileName, mode):
    corpus = open(fileName, mode)
    features = dict()
    for line in corpus:
        line = toUnicode(line)
        newFeatures = extractFeaturesFrom(line)
        if newFeatures is not None:  #if line is NoneType, skip to next line
            features.update(newFeatures)
    corpus.close()
    return features

#iterate through every word in text, normalize it, and remove stopwords
def extractFeaturesFrom(text):
    if text is not None:
        return dict([(normalize(word), True) for word in text.split() 
                    if word not in stopWords])
    else:
        return None