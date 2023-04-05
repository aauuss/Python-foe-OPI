import numpy as np
import cv2
import math

class Struct:
        pass

def createPath(img):
        h, w = img.shape[:2]
        return np.zeros((h, w, 3), np.uint8)

def getCentr(contour):
        (x, y, h, w) = cv2.boundingRect(contour)
        return [int(x+h/2), int(y+w/2)]

def isMoving(point1, point2, delta):
        dx = point1[0] - point2[0]
        dy = point1[1] - point2[1]
        if (math.sqrt(dx*dx + dy*dy)) < delta:
                return True
        return False

cap = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
cap.set(cv2.CAP_PROP_FOURCC, fourcc)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 3840)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 2160)
cap.set(cv2.CAP_PROP_FPS, 30)

width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

ret, img = cap.read();
ret, frame1 = cap.read()
ret, frame2 = cap.read()
ret, frame3 = cap.read()

path = createPath(frame1)
lpx , lpy, px, py = 0, 0, 0, 0


s = list()

kernel1 = np.ones((7, 7), 'float32')/49
kernel2 = np.ones((7, 7), 'uint8')

while True:
        diff1 = cv2.absdiff(frame1, frame2)
        diff2 = cv2.absdiff(frame2, frame3)
        diff = cv2.add(diff1, diff2)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)        
        
        _, thresh = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)
        blur = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel1)
        dilated = cv2.dilate(blur, kernel1, iterations = 5)

        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for newCont in contours:
                if len(newCont) > 9:
                        centr = getCentr(newCont)

                        point = Struct()
                        point.contour = newCont
                        point.track = []
                        point.track.append(centr)
                        
                        s.append(point)
                        
                        for i in range(len(s) - 1):                                
                                if isMoving(point.track[0], s[i].track[0], 20):
                                        print('asdf')
                                        s[len(s)-1].track.extend(s[i].track)
                                        s.pop(i)
                                        break

                        cv2.circle(img, centr, 10, (0,255,0), 2)                        
                        ##cv2.rectangle(img, (x, y), (x+h, y+w), (0, 255, 0), 2)

        
        for point in s:                
                for i in range(len(point.track)-2):
                        cv2.line(path, point.track[i], point.track[i+1], (255,0,0), 5)
                        
                        
        img = cv2.add(img, path)
        cv2.imshow('frame1', img)

        ret, img = cap.read();
        frame1 = frame2
        frame2 = frame3
        frame3 = cv2.filter2D(img, -1, kernel1)
        
        k = cv2.waitKey(5) & 0xff
        if k == 27:
                break
        if k == 32:
                path = createPath(img)
                s.clear()

cap.release()
cv2.destroyAllWindows()
