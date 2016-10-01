from flask import Flask, abort, request, jsonify
app = Flask(__name__)

@app.route('/tweets', methods=['GET', 'POST'])
def get_tweets():
    pass

@app.route('/tweets/<int:tweet_id>', methods=['GET'])
def get_tweet(tweet_id):
    pass


if __name__ == '__main__':
    app.run(debug=True)

