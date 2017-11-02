import numpy as np
import matplotlib.pyplot as plt
import cv2
from sklearn.cluster import KMeans

def enum(**named_values):
	return type('Enum', (), named_values)

Color = enum(RED='red', GREEN='green', BLUE='blue')

def doNothing(x):
	pass

def getColour(img):
	# reshape into a linear array
	hs = img.reshape((img.shape[0] * img.shape[1], 3))

	kmeans = KMeans(n_clusters=2)
	kmeans.fit(hs)

	mean_second_dominant_colour = np.uint8([[kmeans.cluster_centers_[1]]])

	# convert the colour to HSV space
	mean_second_dominant_colour = cv2.cvtColor(mean_second_dominant_colour, cv2.COLOR_BGR2HSV)

	hue = mean_second_dominant_colour[0][0][0] * 2

	# alter hue so that red does not straddle 360

	hue = (hue + 60) % 360

	print "Second most dominant hue: " + str(hue)

	if hue < 120:
		return Color.RED
	if hue < 240:
		return Color.GREEN
	if hue < 360:
		return Color.BLUE


	return "Unknown Color"

def getNumber(img):
	img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	edges = cv2.Canny(img, 80, 180)
	cv2.imshow('image', edges)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

	return "Unknown Shape"

# use this function to tune the parameters for the canny edge detection on a few cards
def getNumberTest(img):
	img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	cv2.namedWindow('image')

	cv2.createTrackbar('min', 'image', 0, 500, doNothing)
	cv2.createTrackbar('max', 'image', 0, 500, doNothing)

	min = 0
	max = 0

	while(1):
		edges = cv2.Canny(img, min, max)
		cv2.imshow('image', edges)

		k = cv2.waitKey(1) & 0xFF
		if k == 27:
			break
		min = cv2.getTrackbarPos('min','image')
		max = cv2.getTrackbarPos('max', 'image')

		print min, max

	return "Unknown Shape"

def resizeImage(img):
	resize = cv2.resize(img, (600, 540))
	return resize

# let us assume we have the picture and now we want to classify what it actually is

# read in the file
# img = cv2.imread('card_1.jpg')
# img = cv2.imread('card_0.jpg')
# img = cv2.imread('card_4.jpg')
img = cv2.imread('card_8.jpg')
# img=cv2.imread('training_pics/3_h_b_s.jpg')

resized = resizeImage(img)

# print "Determined color: " + getColour(resized)
print "Determined number: " + getNumber(resized)

cv2.destroyAllWindows()
