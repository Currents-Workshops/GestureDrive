import cv2
import mediapipe as mp
import requests  

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

mp_drawing = mp.solutions.drawing_utils

num_fingers = 0
prev_num_fingers = 0
last_gesture = None  


post_url = "http://localhost:5000/gestureDrive" 

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        continue

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(frame_rgb)

    gesture = "None"

    if results.multi_hand_landmarks:
        for landmarks in results.multi_hand_landmarks:
            num_fingers = 0
            thumb_tip = landmarks.landmark[4].y
            thumb_base = landmarks.landmark[2].y
            index_tip = landmarks.landmark[8].y
            middle_tip = landmarks.landmark[12].y
            ring_tip = landmarks.landmark[16].y
            pinky_tip = landmarks.landmark[20].y

            thumb_threshold = 0.8 * thumb_base

            if thumb_tip < thumb_threshold:
                num_fingers += 1

            if index_tip < landmarks.landmark[5].y:
                num_fingers += 1

            if middle_tip < landmarks.landmark[9].y:
                num_fingers += 1

            if ring_tip < landmarks.landmark[13].y:
                num_fingers += 1

            if pinky_tip < landmarks.landmark[17].y:
                num_fingers += 1

            mp_drawing.draw_landmarks(frame, landmarks, mp_hands.HAND_CONNECTIONS)

            if num_fingers == 0:
                gesture = "None"
            elif num_fingers == 1:
                gesture = "Forward"
            elif num_fingers == 2:
                gesture = "Backward"
            elif num_fingers == 3:
                gesture = "Right"
            elif num_fingers == 4:
                gesture = "Left"
            elif num_fingers == 5:
                gesture = "stop"

    if gesture != last_gesture:
        last_gesture = gesture
        data = {"gesture": gesture}
        try:
            response = requests.post(post_url, json=data)
            if response.status_code == 200:
                print("POST request sent successfully.")
            else:
                print(f"Failed to send POST request. Status code: {response.status_code}")
        except Exception as e:
            print(f"Error sending POST request: {e}")

    if num_fingers != prev_num_fingers:
        if num_fingers > prev_num_fingers:
            num_fingers = prev_num_fingers + 1
        else:
            num_fingers = prev_num_fingers - 1
        prev_num_fingers = num_fingers

    cv2.putText(frame, f'Fingers: {num_fingers}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.putText(frame, f'Gesture: {gesture}', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow('Hand Gesture Recognition', frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
