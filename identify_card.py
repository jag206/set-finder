import numpy as np
import matplotlib.pyplot as plt
import cv2
from sklearn.cluster import KMeans

def enum(**named_values):
	return type('Enum', (), named_values)

Color = enum(RED='red', GREEN='green', BLUE='blue')
Shape = enum(SQUIGGLE='squiggle', DIAMOND='diamond', PILL='pill')
no_value = 'none'

def doNothing(x):
	pass

def assignShape(contour_area):
	if contour_area > 27000 and contour_area < 30000:
		return Shape.DIAMOND
	if contour_area > 32000 and contour_area < 38000:
		return Shape.SQUIGGLE
	if contour_area > 44000 and contour_area < 50000:
		return Shape.PILL

	return no_value

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
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	blur = cv2.GaussianBlur(gray,(5,5),0)

	thresh = cv2.adaptiveThreshold(blur, 300, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 21,0)

	contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

	contours = sorted(contours, key = cv2.contourArea, reverse=True)

	contours = contours[:10]

	shapes = list()

	for contour in contours:
		print cv2.contourArea(contour)
		shapes.append(assignShape(cv2.contourArea(contour)))

	shapes = filter(lambda a: a != no_value, shapes)
	# get the top 3 shapes
	shapes = shapes[:3]
	print shapes

	cv2.drawContours(img, contours, -1, (255,0,0), 2)

	cv2.imshow('image', img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

	return "Unknown Shape"

# use this function to tune the parameters for the contours on a few cards
def getNumberTest(img):
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	# equ = cv2.equalizeHist(gray)
	blur = cv2.GaussianBlur(gray,(5,5),0)

	cv2.namedWindow('image')

	cv2.createTrackbar('min', 'image', 0, 500, doNothing)
	cv2.createTrackbar('max', 'image', 0, 500, doNothing)

	min = 0
	max = 0

	while(1):
		thresh = cv2.adaptiveThreshold(blur, max, cv2.
			ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 21,min)
		cv2.imshow('image', thresh)

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
# img = cv2.imread('card_10.jpg')
# img = cv2.imread('card_0.jpg')
# img = cv2.imread('card_1.jpg')
# img = cv2.imread('card_2.jpg')
# img = cv2.imread('card_3.jpg')
# img = cv2.imread('card_4.jpg')
img = cv2.imread('card_5.jpg')
# img = cv2.imread('card_6.jpg')
# img = cv2.imread('card_7.jpg')
# img = cv2.imread('card_8.jpg')
# img = cv2.imread('card_9.jpg')
# img = cv2.imread('card_10.jpg')
# img = cv2.imread('card_11.jpg')
# img=cv2.imread('training_pics/3_h_b_s.jpg')

resized = resizeImage(img)

# print "Determined color: " + getColour(resized)
print "Determined number: " + getNumber(resized)

cv2.destroyAllWindows()
