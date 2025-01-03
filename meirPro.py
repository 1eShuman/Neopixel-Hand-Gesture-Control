import cv2
import mediapipe as mp
import numpy as np
import serial
import time

class HandGestureDetector:
    def __init__(self, port='COM6', baudrate=9600):
        # Initialize MediaPipe hands
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )
        self.mp_draw = mp.solutions.drawing_utils
        
        # Initialize Arduino serial communication
        try:
            self.arduino = serial.Serial(port, baudrate, timeout=1)
            time.sleep(2)  # Wait for Arduino to initialize
            print(f"Connected to Arduino on {port}")
        except:
            print(f"Failed to connect to Arduino on {port}")
            self.arduino = None

    def count_fingers(self, hand_landmarks):
        # Define finger tip IDs and their corresponding base points
        finger_tips = [8, 12, 16, 20]  # Index, Middle, Ring, Pinky
        thumb_tip = 4
        thumb_base = 2
        
        # Get coordinates
        thumb_tip_coord = np.array([hand_landmarks.landmark[thumb_tip].x, hand_landmarks.landmark[thumb_tip].y])
        thumb_base_coord = np.array([hand_landmarks.landmark[thumb_base].x, hand_landmarks.landmark[thumb_base].y])
        
        # Count raised fingers
        raised_fingers = 0
        
        # Check thumb
        if thumb_tip_coord[0] < thumb_base_coord[0]:  # For right hand
            raised_fingers += 1
            
        # Check other fingers
        for tip_idx in finger_tips:
            tip_y = hand_landmarks.landmark[tip_idx].y
            base_y = hand_landmarks.landmark[tip_idx - 2].y
            
            if tip_y < base_y:
                raised_fingers += 1
                
        return min(raised_fingers, 5)  # Limit to maximum of 5

    def send_to_arduino(self, number):
        if self.arduino is not None:
            try:
                # Convert number to string, add newline, and encode to bytes
                data = f"{number}\n".encode()
                self.arduino.write(data)
                print(f"Sent to Arduino: {number}")
            except Exception as e:
                print(f"Error sending to Arduino: {e}")

    def process_frame(self, frame):
        # Convert to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)
        
        number = 0
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw hand landmarks
                self.mp_draw.draw_landmarks(
                    frame,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS
                )
                
                # Count fingers and get number
                number = self.count_fingers(hand_landmarks)
                
                # Send number to Arduino
                self.send_to_arduino(number)
                
                # Display number
                cv2.putText(
                    frame,
                    f"Number: {number}",
                    (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2
                )
                
        return frame, number

    def cleanup(self):
        if self.arduino is not None:
            self.arduino.close()
            print("Arduino connection closed")

def main():
    # Initialize detector (change COM3 to your Arduino port)
    detector = HandGestureDetector(port='COM6', baudrate=9600)
    
    # Start video capture
    cap = cv2.VideoCapture(0)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        # Flip frame horizontally for more intuitive interaction
        frame = cv2.flip(frame, 1)
        
        # Process frame
        processed_frame, number = detector.process_frame(frame)
        
        # Display frame
        cv2.imshow('Hand Gesture Detection', processed_frame)
        
        # Break loop on 'q' press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    # Clean up
    cap.release()
    cv2.destroyAllWindows()
    detector.cleanup()

if __name__ == "__main__":
    main()