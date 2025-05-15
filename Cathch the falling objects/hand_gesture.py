import cv2
import mediapipe as mp
import numpy as np
import pygame
import threading
import time

class HandGestureDetector:
    def __init__(self, mirror=True):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        
        # Initialize webcam
        self.cap = cv2.VideoCapture(0)
        self.mirror = mirror
        
        # Control variables
        self.is_running = False
        self.current_gesture = "none"  # none, left, right, up
        self.thread = None
        
        # Debug window
        self.show_debug_window = True
        self.debug_surface = None
        
        # Gesture thresholds
        self.horizontal_threshold = 0.2  # For left/right detection
        self.vertical_threshold = 0.15   # For up detection
        
    def start(self):
        """Start the hand gesture detection in a separate thread"""
        if not self.is_running:
            self.is_running = True
            self.thread = threading.Thread(target=self._process_frames)
            self.thread.daemon = True
            self.thread.start()
            print("Hand gesture detection started")
            
    def stop(self):
        """Stop the hand gesture detection"""
        self.is_running = False
        if self.thread:
            self.thread.join(timeout=1.0)
        self.cap.release()
        cv2.destroyAllWindows()
        print("Hand gesture detection stopped")
        
    def get_gesture(self):
        """Return the current detected gesture"""
        return self.current_gesture
    
    def _process_frames(self):
        """Process video frames to detect hand gestures"""
        while self.is_running:
            success, image = self.cap.read()
            if not success:
                print("Failed to capture frame from webcam")
                continue
                
            # Mirror the image if needed
            if self.mirror:
                image = cv2.flip(image, 1)
                
            # Convert to RGB for MediaPipe
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = self.hands.process(image_rgb)
            
            # Default gesture is none
            self.current_gesture = "none"
            
            # Draw hand landmarks and detect gestures
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # Draw hand landmarks
                    self.mp_drawing.draw_landmarks(
                        image,
                        hand_landmarks,
                        self.mp_hands.HAND_CONNECTIONS,
                        self.mp_drawing_styles.get_default_hand_landmarks_style(),
                        self.mp_drawing_styles.get_default_hand_connections_style()
                    )
                    
                    # Get wrist and index finger tip positions
                    wrist = hand_landmarks.landmark[self.mp_hands.HandLandmark.WRIST]
                    index_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
                    
                    # Calculate horizontal movement (left/right)
                    horizontal_diff = index_tip.x - wrist.x
                    
                    if horizontal_diff < -self.horizontal_threshold:
                        self.current_gesture = "left"
                    elif horizontal_diff > self.horizontal_threshold:
                        self.current_gesture = "right"
                    
                    # Calculate vertical movement (up)
                    vertical_diff = wrist.y - index_tip.y
                    if vertical_diff > self.vertical_threshold:
                        self.current_gesture = "up"
                    
                    # Add gesture text to image
                    cv2.putText(
                        image, 
                        f"Gesture: {self.current_gesture}", 
                        (10, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 
                        1, 
                        (0, 255, 0), 
                        2
                    )
            
            # Show debug window if enabled
            if self.show_debug_window:
                cv2.imshow("Hand Gesture Detection", image)
                
                # Convert to pygame surface for in-game display
                image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                image_rgb = cv2.resize(image_rgb, (320, 240))
                self.debug_surface = pygame.surfarray.make_surface(np.rot90(image_rgb))
                
            # Break loop if 'q' is pressed
            if cv2.waitKey(5) & 0xFF == ord('q'):
                break
                
            # Small delay to reduce CPU usage
            time.sleep(0.01)
    
    def get_debug_surface(self):
        """Return the debug surface for display in pygame"""
        return self.debug_surface

# Test the hand gesture detector if run directly
if __name__ == "__main__":
    detector = HandGestureDetector()
    detector.start()
    
    try:
        while True:
            gesture = detector.get_gesture()
            print(f"Current gesture: {gesture}")
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("Stopping...")
    finally:
        detector.stop()