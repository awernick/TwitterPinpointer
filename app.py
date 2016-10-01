from os             import environ
from twitter        import *
from flask          import Flask, abort, request, jsonify
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

twitter = Twitter(auth=OAuth(auth_token, auth_secret,
                             consumer_key, consumer_secret))

# RESTful
@app.route('/tweets', methods=['GET', 'POST'])
def get_tweets():
    pass

@app.route('/tweets/<int:tweet_id>', methods=['GET'])
def get_tweet(tweet_id):
    pass

@app.route('/tweets/live', methods=['POST'])
def get_tweet_stream():
    pass


if __name__ == '__main__':
    socketio.run(app, debug=True)

