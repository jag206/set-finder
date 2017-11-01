import numpy as np
import matplotlib.pyplot as plt
import cv2
from sklearn.cluster import KMeans

def enum(**named_values):
	return type('Enum', (), named_values)

Color = enum(RED='red', GREEN='green', BLUE='blue')

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

def preprocess(img):
	resize = cv2.resize(img, (600, 540))
	return resize

# let us assume we have the picture and now we want to classify what it actually is

# read in the file
img = cv2.imread('card_1.jpg')
# img = cv2.imread('card_0.jpg')
# img = cv2.imread('card_4.jpg')
# img = cv2.imread('card_8.jpg')
# img=cv2.imread('training_pics/3_h_b_s.jpg')

processed = preprocess(img)

print "Determined color: " + getColour(processed)
