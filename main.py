import cv2
import mediapipe as mp
import pyautogui
import json
import numpy as np
import subprocess
import time

gesture_file = "gestures.json"
default_gestures = {
    "C": "chrome",
    ">": "volume_up",
    "<": "volume_down",
    "O": "desktop",
    "L": "delete",
    "2": "rename",
    "S": "screenshot",
    "T": "notepad",
    "X": "lock_screen",
    "U": "undo"
}

try:
    with open(gesture_file, "r") as file:
        gesture_actions = json.load(file)
except (FileNotFoundError, json.JSONDecodeError):
    gesture_actions = default_gestures
    with open(gesture_file, "w") as file:
        json.dump(default_gestures, file, indent=4)


mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.8, max_num_hands=1)

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

if not cap.isOpened():
    print("❌ Error: Could not access webcam!")
    exit()

gesture_path = []
last_action_time = time.time()
ACTION_DELAY = 2.0  
CLICK_THRESHOLD = 50

def recognize_shape(path_points):
    if len(path_points) < 30:
        return None
    x_coords, y_coords = zip(*path_points)
    x_coords = np.array(x_coords) - min(x_coords)
    y_coords = np.array(y_coords) - min(y_coords)
    dx = np.diff(x_coords)
    dy = np.diff(y_coords)
    shape = ""
    if np.mean(dy) < -2 and np.mean(dx) > 2:
        shape = "M"
    elif np.mean(dy) > 2 and np.mean(dx) < -2:
        shape = "C"
    elif np.all(dx > 0) and np.abs(np.mean(dy)) < 2:
        shape = ">"
    elif np.all(dx < 0) and np.abs(np.mean(dy)) < 2:
        shape = "<"
    elif np.all(dy < 0):
        shape = "O"
    elif np.all(dy > 0):
        shape = "L"
    elif np.count_nonzero(np.diff(np.sign(dx))) > 2:
        shape = "2"
    elif np.mean(dy) > 2 and np.mean(dx) > 2:
        shape = "U"
    return shape


def execute_action(gesture):
    action = gesture_actions.get(gesture)
    if action == "chrome":
        pyautogui.hotkey("win", "r")
        pyautogui.typewrite("chrome\n")
    elif action == "volume_up":
        pyautogui.press("volumeup")
    elif action == "volume_down":
        pyautogui.press("volumedown")
    elif action == "desktop":
        pyautogui.hotkey("win", "d")
    elif action == "delete":
        pyautogui.hotkey("shift", "delete")
    elif action == "rename":
        pyautogui.press("f2")
    elif action == "screenshot":
        pyautogui.hotkey("win", "shift", "s")
    elif action == "notepad":
        pyautogui.hotkey("win", "r")
        pyautogui.typewrite("notepad\n")
    elif action == "lock_screen":
        pyautogui.hotkey("win", "l")
    elif action == "undo":
        pyautogui.hotkey("ctrl", "z")

def process_frame():
    global gesture_path, last_action_time
    screen_w, screen_h = pyautogui.size()
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)
        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            index_finger = hand_landmarks.landmark[8]
            h, w, _ = frame.shape
            index_x, index_y = int(index_finger.x * w), int(index_finger.y * h)
            pyautogui.moveTo((index_x / w) * screen_w, (index_y / h) * screen_h, duration=0.1)
            cv2.circle(frame, (index_x, index_y), 10, (0, 255, 0), -1)
            if len(gesture_path) == 0 or abs(gesture_path[-1][0] - index_x) > 4 or abs(gesture_path[-1][1] - index_y) > 4:
                gesture_path.append((index_x, index_y))
            thumb_tip = hand_landmarks.landmark[4]
            thumb_x, thumb_y = int(thumb_tip.x * w), int(thumb_tip.y * h)
            distance = np.linalg.norm(np.array([index_x, index_y]) - np.array([thumb_x, thumb_y]))
            if distance < CLICK_THRESHOLD:
                pyautogui.click()
                print("🖱 Click detected!")
        else:
            if len(gesture_path) > 30:
                recognized_gesture = recognize_shape(gesture_path)
                if recognized_gesture and (time.time() - last_action_time > ACTION_DELAY):
                    last_action_time = time.time()
                    execute_action(recognized_gesture)
                gesture_path.clear()
        cv2.imshow("Hand Gesture Recognition", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
    print("📷 Camera turned off.")

process_frame()
