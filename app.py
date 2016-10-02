import json
import thread
import eventlet
eventlet.monkey_patch()

from os             import environ
from twitter        import *
from flask          import Flask, abort, request, jsonify, \
                           copy_current_request_context
from flask_socketio import SocketIO, send, emit


app = Flask(__name__)
app.config['SECRET_KEY'] = environ.get('SECRET_KEY') or \
                           'supercalifragilisticexpiralidocious'

# SocketIO
socketio = SocketIO(app)

# Twitter
consumer_key    = environ['TWITTER_CONSUMER_KEY']
consumer_secret = environ['TWITTER_CONSUMER_SECRET']
auth_token      = environ['TWITTER_AUTH_KEY']
auth_secret     = environ['TWITTER_AUTH_SECRET']

auth           = OAuth(auth_token, auth_secret, consumer_key, consumer_secret)
twitter        = Twitter(auth=auth)
twitter_stream = TwitterStream(auth=auth)

# hilary_stream  = twitter_stream.statuses.filter(track='Hilary Clinton')
#trump_stream   = twitter_stream.statuses.filter(track='Donald Trump')

# RESTful
@app.route('/tweets', methods=['GET', 'POST'])
def get_tweets():
    pass

@app.route('/tweets/<int:tweet_id>', methods=['GET'])
def get_tweet(tweet_id):
    pass

# WebSocket
@socketio.on('connect')
def client_connected():
    print "Client connected"

    # Start stream processing
    @copy_current_request_context
    def process_stream(event, strm):
        stream = strm.statuses.filter(track='Hilary Clinton')
        for tweet in stream:
            emit(event, tweet)

    eventlet.spawn(process_stream, 'clinton_tweet', twitter_stream)


if __name__ == '__main__':
    socketio.run(app, debug=True)

