import cv2
import numpy as np

def callback (*arg):
        print(arg)
def nothing(*arg):
        pass
        
faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')


cv2.namedWindow('Result')
cv2.namedWindow('Zoom')

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_EXPOSURE, 400)
cap.set(cv2.CAP_PROP_FPS, 30)

cv2.createTrackbar('zoom', 'Zoom', 0, 17, nothing)
cv2.setTrackbarPos('zoom', 'Zoom', 0)


ret, img = cap.read()

lastx , lasty, x, y = 0, 0, 0, 0
green = (0, 255, 0)
while True:
        z = cv2.getTrackbarPos('zoom', 'Zoom')
        cap.set(cv2.CAP_PROP_ZOOM, z)
        
        ret, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(gray, 1.2, 5)

        for (x, y, w, h) in faces:
                cv2.rectangle(img, (x,y), (x + w, y + h), green, 2)
        cv2.imshow('Result', img)
        
        ch = cv2.waitKey(5)
        if ch == 27:
                break

cap.release()
cv2.destroyAllWindows()
