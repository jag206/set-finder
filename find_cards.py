import numpy as np
import cv2

num_cards = 12

# here we make sure we have the axes correct before we do the affine transformation otherwise we will horribly stretch one of the cards that we have selected
def correct(rect):
	row0 = rect[0]
	row1 = rect[1]
	row2 = rect[2]

	len1 = np.linalg.norm(row1 - row0)
	len2 = np.linalg.norm(row2 - row1)

	if (len1 > len2):
		return np.concatenate((rect[-1:], rect[:-1]))

	return rect

def saveCard(filename, card):
	cv2.imwrite(filename, card)

def getCard(card_idx):

	card = contours[card_idx]

	peri = cv2.arcLength(card,True)

	# aprox may be a weird way round

	approx = cv2.approxPolyDP(card,.02*peri,True)
	approx = approx.reshape((4,2))

	approx = correct(approx)

	for idx in range(0,4):
		idx_2 = (idx + 1) % 4

		if idx == 0:
			color = (255,0,0)
		if idx == 1:
			color = (0,255,0)
		if idx == 2:
			color = (0,0,255)
		if idx == 3:
			color = (255,255,255)

		# if idx==0 is a short edge then we need to swap these elements to make sure the mapping is correct

		# cv2.line(img, (approx[idx][0],approx[idx][1]), (approx[idx_2][0],approx[idx_2][1]), color, 2)

	approx = np.float32(approx)

	h = np.array([ [0,0],[499,0],[499,699],[0,699] ],np.float32)
	transform = cv2.getPerspectiveTransform(approx,h)

	warp = cv2.warpPerspective(orig_img,transform,(500,700))

	return warp


img = cv2.imread("SetCards1.jpg")

orig_img = img.copy()

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray,(3,3),1000)
flag, thresh = cv2.threshold(blur, 120, 250, cv2.THRESH_BINARY)

contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

contours = sorted(contours, key = cv2.contourArea, reverse=True)

contours = contours[:num_cards]

cv2.drawContours(img, contours, -1, (255,0,0), 2)

# for x in range(0, num_cards):
# 	# identify each card
# 	detected_card = getCard(x)
# 	saveCard("card_" + str(x) +".jpg", detected_card)

img = cv2.resize(img, (600, 540))
cv2.imshow('image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
