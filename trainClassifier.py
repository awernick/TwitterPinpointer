from nltk.classify import NaiveBayesClassifier
from featureFunctions import *
from nltk.corpus import sentence_polarity
from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.util import *

def trainClassifier():
	pos_docs = [(sent, 'pos') for sent in subjectivity.sents(categories='pos')]
	neg_docs = [(sent, 'neg') for sent in subjectivity.sents(categories='neg')]

	sentim_analyzer = SentimentAnalyzer()
	all_words_negate = sentim_analyzer.all_words([mark_negation(doc) for doc in training_docs])

	unigram_feats = sentim_analyzer.unigram_word_feats(all_words_negate, min_freq=4)
	sentim_analyzer.add_feat_extractor(extract_unigram_feats, unigrams=unigram_feats)
	training_set = sentim_analyzer.apply_features(training_docs)
	trainer = NaiveBayesClassifier.train
	classifier = sentim_analyzer.train(trainer, training_set)

	for key,value in sorted(sentim_analyzer.evaluate(test_set).items()):
		print('{0}: {1}'.format(key, value))

	return classifier