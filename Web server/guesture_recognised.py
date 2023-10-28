import cv2
import numpy as np
import math
import requests


last_gesture1 = None
last_gesture2 = None


def send_gesture_request(gesture):
    
    url = "http://localhost:5000/gestureDrive"
       
    data = {'gesture': gesture}

    response = requests.post(url, json=data)

    if response.status_code == 200:
        print(f"Gesture '{gesture}' sent to the server successfully.")
    else:
        print(f"Failed to send gesture '{gesture}' to the server.")

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    kernel = np.ones((3, 3), np.uint8)

    roi1 = frame[100:300, 100:300]
    cv2.rectangle(frame, (100, 100), (300, 300), (0, 255, 0), 0)
    roi2 = frame[100:300, 400:600]
    cv2.rectangle(frame, (400, 100), (600, 300), (0, 255, 0), 0)

    hsv1 = cv2.cvtColor(roi1, cv2.COLOR_BGR2HSV)
    hsv2 = cv2.cvtColor(roi2, cv2.COLOR_BGR2HSV)

    lower_skin = np.array([0, 20, 70], dtype=np.uint8)
    upper_skin = np.array([20, 255, 255], dtype=np.uint8)

    mask1 = cv2.inRange(hsv1, lower_skin, upper_skin)
    mask2 = cv2.inRange(hsv2, lower_skin, upper_skin)

    mask1 = cv2.dilate(mask1, kernel, iterations=4)
    mask2 = cv2.dilate(mask2, kernel, iterations=4)

    mask1 = cv2.GaussianBlur(mask1, (5, 5), 100)
    mask2 = cv2.GaussianBlur(mask2, (5, 5), 100)

    contours1, _ = cv2.findContours(mask1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours2, _ = cv2.findContours(mask2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if contours1:
        cnt1 = max(contours1, key=lambda x: cv2.contourArea(x))

        epsilon1 = 0.0005 * cv2.arcLength(cnt1, True)
        approx1 = cv2.approxPolyDP(cnt1, epsilon1, True)

        hull1 = cv2.convexHull(cnt1)
        areahull1 = cv2.contourArea(hull1)
        areacnt1 = cv2.contourArea(cnt1)
        arearatio1 = ((areahull1 - areacnt1) / areacnt1) * 100
        hull1 = cv2.convexHull(approx1, returnPoints=False)
        defects1 = cv2.convexityDefects(approx1, hull1)

        if defects1 is not None:
            l1 = 0
            for i in range(defects1.shape[0]):
                s1, e1, f1, d1 = defects1[i, 0]
                start1 = tuple(approx1[s1][0])
                end1 = tuple(approx1[e1][0])
                far1 = tuple(approx1[f1][0])
                a1 = math.sqrt((end1[0] - start1[0]) ** 2 + (end1[1] - start1[1]) ** 2)
                b1 = math.sqrt((far1[0] - start1[0]) ** 2 + (far1[1] - start1[1]) ** 2)
                c1 = math.sqrt((end1[0] - far1[0]) ** 2 + (end1[1] - far1[1]) ** 2)
                s1 = (a1 + b1 + c1) / 2
                ar1 = math.sqrt(s1 * (s1 - a1) * (s1 - b1) * (s1 - c1))
                d1 = (2 * ar1) / a1
                angle1 = math.acos((b1 ** 2 + c1 ** 2 - a1 ** 2) / (2 * b1 * c1)) * 57
                if angle1 <= 90 and d1 > 30:
                    l1 += 1
                    cv2.circle(roi1, far1, 3, [255, 0, 0], -1)

                cv2.line(roi1, start1, end1, [0, 255, 0], 2)

        l1 += 1
        font = cv2.FONT_HERSHEY_SIMPLEX
        if l1 == 1:
            if areacnt1 < 2000:
                cv2.putText(frame, 'Put hand in the box 1', (0, 50), font, 2, (0, 0, 255), 3, cv2.LINE_AA)
            else:
                cv2.putText(frame, 'reposition 1', (0, 50), font, 2, (0, 0, 255), 3, cv2.LINE_AA)

        elif l1 == 2:
            cv2.putText(frame, 'Forward 1', (0, 50), font, 2, (0, 0, 255), 3, cv2.LINE_AA)
        elif l1 == 3:
            cv2.putText(frame, 'Backward 1', (0, 50), font, 2, (0, 0, 255), 3, cv2.LINE_AA)
        elif l1 == 5:
            cv2.putText(frame, 'Stop 1', (0, 50), font, 2, (0, 0, 255), 3, cv2.LINE_AA)
        else:
            cv2.putText(frame, 'reposition 1', (10, 50), font, 2, (0, 0, 255), 3, cv2.LINE_AA)

        # Check if the current gesture is different from the last recognized gesture
        if l1 is not None and l1 != last_gesture1:
            if l1 == 2:
                send_gesture_request('Forward')
            elif l1 == 3:
                send_gesture_request('Backward')
            elif l1 == 5:
                send_gesture_request('Stop')
            else:
                send_gesture_request('Reposition 1')
            
            
            last_gesture1 = l1

    if contours2:
        cnt2 = max(contours2, key=lambda x: cv2.contourArea(x))

        epsilon2 = 0.0005 * cv2.arcLength(cnt2, True)
        approx2 = cv2.approxPolyDP(cnt2, epsilon2, True)

        hull2 = cv2.convexHull(cnt2)
        areahull2 = cv2.contourArea(hull2)
        areacnt2 = cv2.contourArea(cnt2)
        arearatio2 = ((areahull2 - areacnt2) / areacnt2) * 100
        hull2 = cv2.convexHull(approx2, returnPoints=False)
        defects2 = cv2.convexityDefects(approx2, hull2)

        if defects2 is not None:
            l2 = 0
            for i in range(defects2.shape[0]):
                s2, e2, f2, d2 = defects2[i, 0]
                start2 = tuple(approx2[s2][0])
                end2 = tuple(approx2[e2][0])
                far2 = tuple(approx2[f2][0])
                a2 = math.sqrt((end2[0] - start2[0]) ** 2 + (end2[1] - start2[1]) ** 2)
                b2 = math.sqrt((far2[0] - start2[0]) ** 2 + (far2[1] - start2[1]) ** 2)
                c2 = math.sqrt((end2[0] - far2[0]) ** 2 + (end2[1] - far2[1]) ** 2)
                s2 = (a2 + b2 + c2) / 2
                ar2 = math.sqrt(s2 * (s2 - a2) * (s2 - b2) * (s2 - c2))
                d2 = (2 * ar2) / a2
                angle2 = math.acos((b2 ** 2 + c2 ** 2 - a2 ** 2) / (2 * b2 * c2)) * 57
                if angle2 <= 90 and d2 > 30:
                    l2 += 1
                    cv2.circle(roi2, far2, 3, [255, 0, 0], -1)

                cv2.line(roi2, start2, end2, [0, 255, 0], 2)

        l2 += 1
        font = cv2.FONT_HERSHEY_SIMPLEX
        if l2 == 1:
            if areacnt2 < 2000:
                cv2.putText(frame, 'Put hand in the box 2', (0, 150), font, 2, (0, 0, 255), 3, cv2.LINE_AA)
            else:
                cv2.putText(frame, 'reposition 2', (0, 150), font, 2, (0, 0, 255), 3, cv2.LINE_AA)
        elif l2 == 2:
            cv2.putText(frame, 'Left 2', (0, 150), font, 2, (0, 0, 255), 3, cv2.LINE_AA)
        elif l2 == 3:
            cv2.putText(frame, 'Right 2', (0, 150), font, 2, (0, 0, 255), 3, cv2.LINE_AA)
    
        elif l2 == 5:
            cv2.putText(frame, 'Stop 2', (0, 150), font, 2, (0, 0, 255), 3, cv2.LINE_AA)
        else:
            cv2.putText(frame, 'Reposition 2', (10, 150), font, 2, (0, 0, 255), 3, cv2.LINE_AA)

        # Check if the current gesture is different from the last recognized gesture
        if l2 is not None and l2 != last_gesture2:
            if l2 == 2:
                send_gesture_request('Left')
            elif l2 == 3:
                send_gesture_request('Right')
            elif l2 == 5:
                send_gesture_request('Stop')
            else:
                send_gesture_request('Reposition 2')

            last_gesture2 = l2

    cv2.imshow('frame', frame)
    cv2.imshow('mask1', mask1)
    cv2.imshow('mask2', mask2)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
cap.release()
