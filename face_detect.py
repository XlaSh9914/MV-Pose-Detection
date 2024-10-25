# face_capture.py
import cv2
import mediapipe as mp
import json
from datetime import datetime

class FacialLandmarkCapture:
    LANDMARK_INDICES = {
        'Left_Eye': {
            'outer': 33,
            'inner': 133,
            'top': 160,
            'bottom': 144
        },
        'Right_Eye': {
            'outer': 362,
            'inner': 263,
            'top': 386,
            'bottom': 374
        },
        'Nose': {
            'tip': 5,
            'bridge': 168
        },
        'Mouth': {
            'left_corner': 61,
            'right_corner': 291,
            'top': 13,
            'bottom': 14,
            'top_inner': 84,
            'bottom_inner': 314
        }
    }

    def __init__(self):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.face_data = []
        self.frame_count = 0

    def capture_landmarks(self):
        cap = cv2.VideoCapture(r".\test_data\face_detection_test.mp4")
        
        if not cap.isOpened():
            raise RuntimeError("Could not open video capture device")

        try:
            while True:
                success, image = cap.read()
                if not success:
                    print("Failed to capture frame")
                    continue

                image = cv2.flip(image, 1)
                image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                results = self.face_mesh.process(image_rgb)

                if results.multi_face_landmarks:
                    self.process_landmarks(image, results.multi_face_landmarks[0])
                
                cv2.imshow('Facial Landmark Capture', image)
                
                if cv2.waitKey(5) & 0xFF == ord('q'):
                    break

                self.frame_count += 1

        finally:
            cap.release()
            cv2.destroyAllWindows()
            self.save_face_data()

    def process_landmarks(self, image, face_landmarks):
        height, width, _ = image.shape
        current_frame = {
            'frame': self.frame_count,
            'landmarks': {}
        }

        for feature, indices in self.LANDMARK_INDICES.items():
            current_frame['landmarks'][feature] = {}
            for position, idx in indices.items():
                landmark = face_landmarks.landmark[idx]
                current_frame['landmarks'][feature][position] = {
                    'x': landmark.x,
                    'y': landmark.y,
                    'z': landmark.z,
                    'pixel_x': int(landmark.x * width),
                    'pixel_y': int(landmark.y * height)
                }
                cv2.circle(image, 
                          (int(landmark.x * width), int(landmark.y * height)),
                          2, (0, 255, 0), -1)

        self.face_data.append(current_frame)

    def save_face_data(self):
        filename = r'.\generated_data\face_data.json'
        with open(filename, 'w') as f:
            json.dump({
                'metadata': {
                    'frame_count': self.frame_count,
                    'landmark_indices': self.LANDMARK_INDICES
                },
                'frames': self.face_data
            }, f, indent=2)
        print(f"Face data saved to {filename}")

if __name__ == "__main__":
    capturer = FacialLandmarkCapture()
    capturer.capture_landmarks()