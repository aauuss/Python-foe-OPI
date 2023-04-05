import numpy as np
import cv2

cap = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
cap.set(cv2.CAP_PROP_FOURCC, fourcc)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cap.set(cv2.CAP_PROP_FPS, 30)

width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

ret, frame1 = cap.read()
ret, frame2 = cap.read()

while True:
        diff = cv2.absdiff(frame1, frame2)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
        dilated = cv2.dilate(thresh, None, iterations = 3)
        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
                if len(contour) > 7:
                        ellipse = cv2.fitEllipse(contour)
                        cv2.ellipse(frame1, ellipse, (0,0,255), 2)
                (x, y, h, w) = cv2.boundingRect(contour)

                print(cv2.contourArea(contour))
                if cv2.contourArea(contour) < 1000:
                        continue
                cv2.rectangle(frame1, (x, y), (x+h, y+w), (0, 255, 0), 2)
        cv2.imshow('frame1', frame1)
        frame1 = frame2
        ret, frame2 = cap.read()
        k = cv2.waitKey(5) & 0xff
        if k == 27:
                break
        prvs = next
cap.release()
cv2.destroyAllWindows()
