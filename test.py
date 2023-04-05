import cv2
import numpy as np


def nothing(*arg):
        pass

def createPath(img):
        h, w = img.shape[:2]
        return np.zeros((h, w, 3), np.uint8)

cv2.namedWindow('Result')
cv2.namedWindow('Settings')

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_EXPOSURE, 400)
cap.set(cv2.CAP_PROP_ZOOM, 0)
cap.set(cv2.CAP_PROP_FPS, 1)
print (cap.get(cv2.CAP_PROP_FOURCC))

cv2.createTrackbar('hue_1', 'Settings', 0, 255, nothing)
cv2.createTrackbar('satur_1', 'Settings', 0, 255, nothing)
cv2.createTrackbar('value_1', 'Settings', 0, 255, nothing)
cv2.createTrackbar('hue_2', 'Settings', 255, 255, nothing)
cv2.createTrackbar('satur_2', 'Settings', 255, 255, nothing)
cv2.createTrackbar('value_2', 'Settings', 255, 255, nothing)
cv2.setTrackbarPos('hue_1', 'Settings', 0)
cv2.setTrackbarPos('satur_1', 'Settings', 240)
cv2.setTrackbarPos('value_1', 'Settings', 240)
cv2.setTrackbarPos('hue_2', 'Settings', 20)
cv2.setTrackbarPos('satur_2', 'Settings', 255)
cv2.setTrackbarPos('value_2', 'Settings', 255)

ret, img = cap.read()
#path = createPath(img)
lastx , lasty, x, y = 0, 0, 0, 0
green = (0, 255, 0)
while True:
        ret, img = cap.read()
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        h1 = cv2.getTrackbarPos('hue_1', 'Settings')
        s1 = cv2.getTrackbarPos('satur_1', 'Settings')
        v1 = cv2.getTrackbarPos('value_1', 'Settings')
        h2 = cv2.getTrackbarPos('hue_2', 'Settings')
        s2 = cv2.getTrackbarPos('satur_2', 'Settings')
        v2 = cv2.getTrackbarPos('value_2', 'Settings')

        h_min = np.array((h1, s1, v1), np.uint8)
        h_max = np.array((h2, s2, v2), np.uint8)

        thresh = cv2.inRange(hsv, h_min, h_max)
        contours, hierarchy = cv2.findContours(thresh.copy(),
                                               cv2.RETR_TREE,
                                               cv2.CHAIN_APPROX_SIMPLE)
#        cv2.drawContours(img, contours, -1, green, 2, cv2.LINE_AA, hierarchy, 2)
        

        for cnt in contours:
                if len(cnt) > 5:
                        ellipse = cv2.fitEllipse(cnt)
                        cv2.ellipse(img, ellipse, green, 2)
                
        cv2.imshow('Result', img)
        
        ch = cv2.waitKey(5)
        if ch == 27:
                break
        if ch == 32:
                path = createPath(img)
cap.release()
cv2.destroyAllWindows()
