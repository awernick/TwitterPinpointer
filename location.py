#calculations assume that radius is in meters
#if not, this will screw up the returned location
def getLocation(latitude, longitude, radius):
	geolocations = twitter.api.geo.search(lat=latitude, long=longitude, accuracy=radius)

	listOfPlaces = geolocations['result']['places']

	#Method 1: greatest number of containing locations
	# smallestPlace = listOfPlaces[0]
	# for place in listOfPlaces:
	# 	if(len(smallestPlace['contained_within']) < len(place['contained_within'])):
	# 		smallestPlace = place

	# return smallestPlace['id']

	#Method 2: closest radius
	# estimatedPlace = listOfPlaces[0]
	# closestRadius = sys.maxint
	# radius = convertToLongitudinalDegrees(radius)
	# for place in listOfPlaces:
	# 	r = getApproximateRadius(place)
	# 	if abs(r - radius) < closestRadius:
	# 		closestRadius = r
	# 		estimatedPlace = place

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

#testing
if __name__ == "__main__":
	import sys
	sys.path.insert(0,"twitter")	#add to python's module search path
	import twitter

	# CONSUMER_KEY= 
	# CONSUMER_SECRET= 
	# OAUTH_TOKEN= 
	# OAUTH_TOKEN_SECRET= 

	auth=twitter.oauth.OAuth(OAUTH_TOKEN,OAUTH_TOKEN_SECRET,CONSUMER_KEY,CONSUMER_SECRET)
	twitter.api = twitter.Twitter(auth=auth)

	#college station
	print getLocation('30.628', '-96.3344', '1m')

	#dallas
	print getLocation('32.777', '-96.797', '1m')