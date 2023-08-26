import cv2
import RPi.GPIO as rg
import mediapipe as mp
import time


rg.setmode(rg.BCM)
rg.setwarnings(False)
LED_PINS = [12,13]
for pin in LED_PINS:
    rg.setup(pin, rg.OUT)

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands



def led_dimming(led, duration, pwm_frequency=100):
    pwm = rg.PWM(led, pwm_frequency)

    try:
        pwm.start(0)
        for _ in range(int(duration * pwm_frequency)):
            for duty_cycle in range(0, 101, 5):
                pwm.ChangeDutyCycle(duty_cycle)
                time.sleep(1 / (pwm_frequency * 2))

            for duty_cycle in range(100, -1, -5):
                pwm.ChangeDutyCycle(duty_cycle)
                time.sleep(1 / (pwm_frequency * 2))
    finally:
        pwm.stop()



def count_fingers(hand_landmarks):
    finger_tips = [mp_hands.HandLandmark.INDEX_FINGER_TIP, mp_hands.HandLandmark.MIDDLE_FINGER_TIP, mp_hands.HandLandmark.RING_FINGER_TIP, mp_hands.HandLandmark.PINKY_TIP]
    count = 0
    for finger_tip in finger_tips:
        if hand_landmarks.landmark[finger_tip].y < hand_landmarks.landmark[finger_tip-1].y:
            count += 1
    return count

hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

try:
    while cap.isOpened():
        ret, frame = cap.read()
        
        if not ret:
            break

        result = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        if result.multi_hand_landmarks:
            hand_landmarks = result.multi_hand_landmarks[0]
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            
            # 화살표 모양 손가락
            if (hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y < hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y) and \
                (hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_DIP].y > hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_DIP].y) and \
                (hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_DIP].y < hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_DIP].y) and \
                (hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_DIP].y < hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_DIP].y) and \
                (abs(hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_DIP].x) < abs(hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x)) and \
                (abs(hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_DIP].x) < abs(hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].x)) and \
                (abs(hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_DIP].x) < abs(hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].x)): 


                led_dimming(13, 5)
            
            # Okay 모양 손가락
            elif (hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y > hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].y) and (hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x > hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP].x):

                led_dimming(12, 5)

        frame.flags.writeable = True
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        results = hands.process(frame)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())
        cv2.imshow('MediaPipe Hands', frame)
        if cv2.waitKey(5) & 0xFF == 27:
            break

finally:
    cap.release()
    cv2.destroyAllWindows()
