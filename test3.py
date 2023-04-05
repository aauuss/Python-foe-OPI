import numpy as np
import cv2

def nothing(*arg):
        pass

def createPath(img):
        h, w = img.shape[:2]
        return np.zeros((h, w, 3), np.uint8)

color = (255, 255, 255)
cv2.namedWindow('Result')
##cv2.namedWindow('Settings')

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_EXPOSURE, 200)
cap.set(cv2.CAP_PROP_FPS, 30)


ret, img = cap.read()

path = createPath(img)
#contours = createPath(img)

img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
lastImg = cv2.GaussianBlur(img, (7, 7), 0)
delta = cv2.subtract(lastImg, img)
thresh = 27

while True:
        ret, img = cap.read()
        img = cv2.GaussianBlur(img, (7, 7), 0)
        imgg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        delta = cv2.absdiff(lastImg, imgg)
        
        lastImg = imgg
        
        ret, thr = cv2.threshold(delta, thresh, 255, cv2.THRESH_BINARY)
        
        contours, hierarchy = cv2.findContours(thr,
                                               cv2.RETR_LIST,
                                               cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(img, contours, -1,  color, 2, 3)
        
        
        cv2.imshow('Result', img)
##        cv2.imshow('Cont', thr)

        ch = cv2.waitKey(5)
        if ch == 27:
                break
        if ch == 32:
                path = createPath(img)
cap.release()
cv2.destroyAllWindows()
