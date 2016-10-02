from nltk.classify import NaiveBayesClassifier
from featureFunctions import *

def trainClassifier():
	print "Determining polarity of features..."

	#NLTK classifiers work on "featstructs", simple dictionaries
	    #mapping a feature name to a feature value
	    #We use booleans to indicate that the set (a tweet) does (or doesn't) contain a feature
	#For more information: http://www.nltk.org/howto/featstruct.html

	#pos/negfeats are tuples (dict, label)
	    #Where dict is a dictionary of (word, boolean) key-val pairs
	    #label indicates positive or negative
	posfeats = feature_tuple("corpora/finalPositiveCorpus.txt", "r", "pos")
	negfeats = feature_tuple("corpora/finalNegativeCorpus.txt", "r", "neg")

	#a list of (dict, label) tuples, one for each label
	trainfeats=[posfeats,negfeats]

	print "Training the classifier..."

	#input: list of (dict, label) tuples, one for each label (pos, neg)
	#output: trained classifier that can identify each label
	classifier = NaiveBayesClassifier.train(trainfeats)

	return classifier