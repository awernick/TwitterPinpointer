from twitter_parser import TwitterParser
from twitter        import TwitterStream
import pprint

class TwitterStreamParser(TwitterParser):
    def __init__(self, auth):
        super(TwitterStreamParser, self).__init__(auth)
        self.stream_api = TwitterStream(auth=auth)

    def search(self, query, place=None):
        tweets = self.stream_api.statuses.filter(track=query, place=place)
        return FormattedTweetIterator(tweets, self.parse, query)

class FormattedTweetIterator:
    def __init__(self, stream, func, query):
        self.stream = stream
        self.func = func
        self.query = query

    def __iter__(self):
        return self

    def next(self):
        tweet = self.stream.next()
        return self.func(tweet, self.query)


