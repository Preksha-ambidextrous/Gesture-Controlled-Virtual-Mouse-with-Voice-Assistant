import cv2
import mediapipe as mp
import pyautogui
import numpy as np

# Initialize MediaPipe Hand model
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Get screen dimensions
screen_width, screen_height = pyautogui.size()

# OpenCV video capture
cap = cv2.VideoCapture(0)

# Initialize smoothing variables
prev_x, prev_y = 0, 0
smoothing_factor = 0.2
dragging = False

def smooth_coordinates(new_x, new_y, prev_x, prev_y, factor):
    smoothed_x = prev_x + (new_x - prev_x) * factor
    smoothed_y = prev_y + (new_y - prev_y) * factor
    return smoothed_x, smoothed_y

def map_coordinates(x, y, frame_width, frame_height):
    """
    Map coordinates from frame to screen.
    """
    screen_x = np.interp(x, (0, frame_width), (0, screen_width))
    screen_y = np.interp(y, (0, frame_height), (0, screen_height))
    return screen_x, screen_y

while True:
    success, frame = cap.read()
    if not success:
        break
    
    frame = cv2.flip(frame, 1)  # Flip the frame horizontally for natural interaction
    frame_height, frame_width, _ = frame.shape
    
    # Convert the frame color from BGR to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            # Get coordinates for index finger tip (landmark 8)
            index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            x, y = int(index_finger_tip.x * frame_width), int(index_finger_tip.y * frame_height)
            
            # Map coordinates to screen
            screen_x, screen_y = map_coordinates(x, y, frame_width, frame_height)
            
            # Smooth coordinates
            smoothed_x, smoothed_y = smooth_coordinates(screen_x, screen_y, prev_x, prev_y, smoothing_factor)
            pyautogui.moveTo(smoothed_x, smoothed_y)
            prev_x, prev_y = smoothed_x, smoothed_y

            # Draw hand landmarks on the frame
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            # Detect left click gesture (thumb tip and index finger tip close together)
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            thumb_x, thumb_y = int(thumb_tip.x * frame_width), int(thumb_tip.y * frame_height)
            distance_thumb_index_tip = np.sqrt((thumb_x - x)*2 + (thumb_y - y)*2)

            if distance_thumb_index_tip < 40:
                pyautogui.click()

            # Detect right click gesture (middle finger tip and thumb tip close together)
            middle_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
            middle_x, middle_y = int(middle_finger_tip.x * frame_width), int(middle_finger_tip.y * frame_height)
            distance_middle_thumb = np.sqrt((middle_x - thumb_x)*2 + (middle_y - thumb_y)*2)

            if distance_middle_thumb < 40:
                pyautogui.rightClick()

            # Detect increase volume gesture (thumb tip and ring finger tip close together)
            ring_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
            ring_x, ring_y = int(ring_finger_tip.x * frame_width), int(ring_finger_tip.y * frame_height)
            distance_thumb_ring_tip = np.sqrt((thumb_x - ring_x)*2 + (thumb_y - ring_y)*2)

            if distance_thumb_ring_tip < 40:
                pyautogui.press('volumeup')

            # Detect decrease volume gesture (thumb tip and pinky finger tip close together)
            pinky_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]
            pinky_x, pinky_y = int(pinky_finger_tip.x * frame_width), int(pinky_finger_tip.y * frame_height)
            distance_thumb_pinky_tip = np.sqrt((thumb_x - pinky_x)*2 + (thumb_y - pinky_y)*2)

            if distance_thumb_pinky_tip < 40:
                pyautogui.press('volumedown')

            # Detect drag and drop gesture (index finger and middle finger extended together)
            index_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP]
            middle_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP]
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
            
            distance_index_middle_mcp = np.sqrt((index_mcp.x - middle_mcp.x)*2 + (index_mcp.y - middle_mcp.y)*2)
            distance_index_middle_tip = np.sqrt((index_tip.x - middle_tip.x)*2 + (index_tip.y - middle_tip.y)*2)

            if distance_index_middle_mcp < 0.05 and distance_index_middle_tip < 0.05:
                if not dragging:
                    pyautogui.mouseDown()
                    dragging = True
            else:
                if dragging:
                    pyautogui.mouseUp()
                    dragging = False

            # New gesture to close the window (thumb tip touching the index finger's middle joint)
            index_finger_middle = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP]
            index_middle_x, index_middle_y = int(index_finger_middle.x * frame_width), int(index_finger_middle.y * frame_height)
            distance_thumb_index_middle = np.sqrt((thumb_x - index_middle_x)*2 + (thumb_y - index_middle_y)*2)

            if distance_thumb_index_middle < 40:
                cv2.destroyWindow('Gesture Controlled Virtual Mouse')

    # Display the resulting frame
    cv2.imshow('Gesture Controlled Virtual Mouse', frame)
    
    # Exit the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
hands.close()
