import sys
import json
import thread
import eventlet
eventlet.monkey_patch()

from os             import environ
from twitter        import *
from flask          import Flask, abort, request, jsonify, \
                           copy_current_request_context
from flask_socketio import SocketIO


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

def process_stream(event, query):
    stream = twitter_stream.statuses.filter(track=query)
    for tweet in stream:
        socketio.emit(event, "ID: %s\nText: %s\nTweet ID: %s\n" %
                        (tweet['user']['id_str'], tweet['text'], tweet['id_str']))
        eventlet.sleep(5)

eventlet.spawn(process_stream, 'clinton_tweet', 'Hillary Clinton')
# eventlet.spawn(process_stream, 'trump_tweet', 'Donald Trump')

# RESTful
@app.route('/tweets', methods=['GET'])
def get_tweets():
    if 'lat' in request.args \
        and 'lng' in request.args and 'radius' in request.args:
        lat    = request.args['lat']
        lng    = request.args['lng']
        radius = request.args['radius']

        placeID = getLocation(lat, lng, radius)
    else:
        placeID = None

    hillary_tweets = twitter.search.tweets(q='Hilary Clinton', place=placeID)
    trump_tweets = twitter.search.tweets(q='Donald Trump', place=placeID)
    tweets = hillary_tweets['statuses'] + trump_tweets['statuses']

    return jsonify(tweets)


@app.route('/tweets/<int:tweet_id>', methods=['GET'])
def get_tweet(tweet_id):
    if(len(str(tweet_id)) == 0):
        abort(404)
    try:
        tweet = twitter.statuses.show(id=tweet_id)
        return jsonify(tweet)
    except TwitterHTTPError as error:
        abort(404)

# WebSocket
@socketio.on('connect')
def client_connected():
    print "Client connected"

def getLocation(latitude, longitude, radius):
    geolocations = twitter.geo.search(lat=latitude, long=longitude, accuracy=radius)

    listOfPlaces = geolocations['result']['places']

    #Method 3: closest centroid
    estimatedPlace = listOfPlaces[0]
    closestCentroidDistance = sys.maxint

    for place in listOfPlaces:
        centroidDistance = distance(place['centroid'], [float(latitude), float(longitude)])
        if centroidDistance < closestCentroidDistance:
            closestCentroidDistance = centroidDistance
            estimatedPlace = place

    return estimatedPlace['id']

def convertToLongitudinalDegrees(meters):
    return float(meters[:-1]) / 111044.46

def getApproximateRadius(place):
    center = place['centroid']
    sumOfRadi = 0
    for vertex in place['bounding_box']['coordinates'][0]:
        sumOfRadi = sumOfRadi + distance(center, vertex)
    return sumOfRadi / len(place['bounding_box']['coordinates'][0])

def distance(x, y):
    return ((x[0]-y[0]) + (x[1]-y[1])) ** 2


if __name__ == '__main__':
    socketio.run(app, debug=True)
