import numpy as np
import cv2
import math
import time

class Struct:
        pass

def createPath(img):
        h, w = img.shape[:2]
        return np.zeros((h, w, 3), np.uint8)

def getCentr(contour):
        (x, y, h, w) = cv2.boundingRect(contour)
        return [int(x+h/2), int(y+w/2)]

##point2 - старая точка
def isMoving(point1, point2, deltaL, deltaT, deltaAng):
        dx = point1[0][0] - point2[0][0]
        dy = point1[0][1] - point2[0][1]        
        dt = abs(point1[1] - point2[1])
        length = (math.sqrt(dx*dx + dy*dy))
        ang1 = math.atan2(dy, dx)        
        ang2 = point2[2]
        da = abs(ang1 - ang2)
        if (da > math.pi):
                da = 2*math.pi - da        
        if (length < deltaL) and (dt < deltaT) and (da < deltaAng) :
                return True
        return False

def getImage(cap):
        _ret, _img = cap.read()
        x = 1640
        y = 830
        return _img#[y : y + 640, x : x + 800]
                
##3840x2160 1920x1080 640x480 800x480 800x600 640x360 1280x720

cap = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
cap.set(cv2.CAP_PROP_FOURCC, fourcc)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
cap.set(cv2.CAP_PROP_FPS, 30)
cap.set(cv2.CAP_PROP_EXPOSURE, 350)

width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

img = getImage(cap);
frame1 = getImage(cap)
frame2 = getImage(cap)
frame3 = getImage(cap)

path = createPath(frame1)
lpx , lpy, px, py = 0, 0, 0, 0
lastTime = time.time()
curTime = time.time()
color = [0,255,0]
trackCounter = 0

s = list()

kernelB = np.ones((3, 3), 'uint8')/9
kernelF = np.ones((3, 3), 'uint8')/20
kernelD = np.ones((3, 3), 'uint8')/10

while True:
        diff = cv2.absdiff(frame3, frame2)
        #diff2 = cv2.absdiff(frame3, frame1)
        #diff = cv2.add(diff1, diff2)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)        
        
        _, thresh = cv2.threshold(gray, 15, 255, cv2.THRESH_BINARY)
        blur = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernelB)
        dilated = cv2.dilate(blur, kernelD, iterations = 4)

        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for newCont in contours:
                
                if len(newCont) > 4:
                        centr = getCentr(newCont)
                        
                        #if centr[1] < 60 :
                        #        continue

                        point = Struct()
                        point.contour = newCont
                        point.track = []
                        st = [centr, time.time(), 0]
                        point.track.append(st)                        
                        point.number = trackCounter
                        trackCounter += 1
                        
                        s.append(point)
                        print (len(s))
                        if len(s) < 2 :
                                continue
                        for i in range(len(s) - 2):                                 
                                if isMoving(s[len(s) - 1].track[0], s[i].track[0], 100, 1, math.pi/2):                                        
                                        s[len(s)-1].track.extend(s[i].track)
                                        dx = point.track[0][0][0] - s[i].track[0][0][0]
                                        dy = point.track[0][0][1] - s[i].track[0][0][1]
                                        #угол
                                        s[len(s)-1].track[0][2] =  math.atan2(dy, dx)
                                        
                                        s.pop(i)
                                        break

                        cv2.circle(img, s[len(s)-1].track[0][0], 10, (255,255,0), 1)
                        cv2.putText(img, str(len(s[len(s)-1].track)), s[len(s)-1].track[0][0], cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 1, cv2.LINE_AA)
                       
        
        for i in range(len(s) - 1):
                cv2.putText(path, str(s[i].number), s[i].track[len(s[i].track) - 1][0], cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 1, cv2.LINE_AA)
                
                if (len(s[i].track) > 2):
                        for j in range(len(s[i].track)-2):
                                cv2.line(path, s[i].track[j][0], s[i].track[j+1][0], color, 3)
                        color[0] = color[0] + 25
                        if color[0] > 255 :
                                color[0] = color[0] - 255
                        color[1] = color[1] + 50
                        if color[1] > 255 :
                                color[1] = color[1] - 255
                        color[2] = color[2] + 75
                        if color[2] > 255 :
                                color[2] = color[2] - 255


        for point in s:
                if time.time() - point.track[0][1] > 5:
                        s.remove(point)
                        
        img = cv2.add(img, path)
        cv2.imshow('frame1', img)
        

        lastTime = curTime
        curTime = time.time()


        img = getImage(cap);
        frame1 = frame2
        frame2 = frame3
        frame3 = cv2.filter2D(img, -1, kernelF)
        
        k = cv2.waitKey(1) & 0xff
        if k == 27:
                break
        if k == 32:
                path = createPath(img)
                s.clear()

cap.release()
cv2.destroyAllWindows()
