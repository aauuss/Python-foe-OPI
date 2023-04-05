import numpy as np
import cv2
import time

import telegram_bot as tgb

x1, y1, x2, y2 = 0, 0, 250, 250
kernelB = np.zeros((3, 3), 'uint8')
kernelD = np.zeros((3, 3), 'uint8')
kernelB[1][1] = 1
kernelD[1][1] = 2
videoNum = 0

color = [255,255,0]
def writeVideo(frame, lastFrame):
        cv2.imwrite('img1.png', frame)

        global videoNum
        timeStart = time.time()
        name = 'video{}.avi'.format(str(videoNum))
        videoNum = videoNum + 1
        out = cv2.VideoWriter(name, codec, 25, (640, 480))
        while (time.time() - timeStart < 5):
                if (isMoving(frame, lastFrame, x1, y1, x2, y2)):
                        timeStart = time.time()
                lastFrame = frame
                _, frame = cap.read()                
                out.write(frame)
        out.release()
        
        tgb.bot.sendMessage(tgb.CHAT_ID_GROUP, 'Кто-то грабит холодильник!')
        image = open('img1.png', 'rb')
        tgb.bot.sendPhoto(tgb.CHAT_ID_GROUP, image)
        

        

def mouseClck(event, x, y, flags, params):
        if event == cv2.EVENT_LBUTTONDOWN:
                print("DOWN")                
                global x1
                x1 = x
                global y1
                y1 = y
                print((x1, y1))
        elif event == cv2.EVENT_LBUTTONUP:
                print("UP")                
                global x2
                x2 = x
                global y2
                y2 = y
                print((x2, y2))

def isMoving(img1, img2, x1, y1, x2, y2):
        img1 = img1[y1:y2, x1:x2]
        img2 = img2[y1:y2, x1:x2]
        diff = cv2.absdiff(img1, img2)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 15, 255, cv2.THRESH_BINARY)
        blur = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernelB)
        dilated = cv2.dilate(blur, kernelD, iterations = 3)

        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        
        
        for cont in contours:
                print (len(cont))
                if (len(cont) > 7):
                        rect = cv2.boundingRect(cont)
                        cv2.rectangle(img2, (rect[0], rect[1]), (rect[0]+rect[2], rect[1]+rect[3]),
                                      color, 1, cv2.LINE_AA)
                        return True
        return False                        
        
                
cap = cv2.VideoCapture(0)
codec = cv2.VideoWriter_fourcc(*'MJPG')

_, frame = cap.read()
lastFrame = frame

while(1):       
        
        if isMoving(frame, lastFrame, x1, y1, x2, y2):
                time.sleep(2)
                lastFrame = frame
                _, frame = cap.read()
                if isMoving(frame, lastFrame, x1, y1, x2, y2):
                        writeVideo(frame, lastFrame)        
                
                
        cv2.rectangle(lastFrame, (x1,y1), (x2, y2), color, 1, cv2.LINE_AA)
        cv2.imshow('frame', lastFrame)
        cv2.setMouseCallback('frame', mouseClck)

        lastFrame = frame
        _, frame = cap.read()
        
        k = cv2.waitKey(1) & 0xff
        if k == 27:
                break
        if k == 32:
                print((x1, y1), (x2, y2))
        
cap.release()
cv2.destroyAllWindows()
