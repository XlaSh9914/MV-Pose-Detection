import cv2
import mediapipe as mp
import json
from datetime import datetime


class PoseLandmarkCapture:
    LANDMARK_INDICES = {
        'Nose': 0,
        'Left_Eye': 1,
        'Right_Eye': 2,
        'Left_Ear': 3,
        'Right_Ear': 4,
        'Left_Shoulder': 5,
        'Right_Shoulder': 2,
        'Left_Elbow': 6,
        'Right_Elbow': 8,
        'Left_Wrist': 7,
        'Right_Wrist': 9,
        'Left_Hip': 11,
        'Right_Hip': 12,
        'Left_Knee': 13,
        'Right_Knee': 14,
        'Left_Ankle': 15,
        'Right_Ankle': 16
    }

    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            static_image_mode=False,
            model_complexity=1,
            enable_segmentation=False,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.pose_data = []
        self.frame_count = 0

    def capture_landmarks(self):
        cap = cv2.VideoCapture(r"D:\Projects\MV-Pose-Detection\WhatsApp Video 2024-10-25 at 12.13.33 AM.mp4")

        if not cap.isOpened():
            raise RuntimeError("Could not open video capture device")

        try:
            while True:
                success, image = cap.read()
                if not success:
                    print("Failed to capture frame")
                    break  # Use break instead of continue to exit the loop

                image = cv2.flip(image, 1)
                image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                results = self.pose.process(image_rgb)

                if results.pose_landmarks:
                    self.process_landmarks(image, results.pose_landmarks)

                cv2.imshow('Pose Landmark Capture', image)

                if cv2.waitKey(5) & 0xFF == ord('q'):
                    break

                self.frame_count += 1

        finally:
            cap.release()
            cv2.destroyAllWindows()
            self.save_pose_data()

    def process_landmarks(self, image, pose_landmarks):
        height, width, _ = image.shape
        current_frame = {
            'frame': self.frame_count,
            'landmarks': {}
        }

        for feature, idx in self.LANDMARK_INDICES.items():
            landmark = pose_landmarks.landmark[idx]
            current_frame['landmarks'][feature] = {
                'x': landmark.x,
                'y': landmark.y,
                'z': landmark.z,
                'pixel_x': int(landmark.x * width),
                'pixel_y': int(landmark.y * height)
            }
            cv2.circle(image,
                       (int(landmark.x * width), int(landmark.y * height)),
                       5, (0, 255, 0), -1)

        self.pose_data.append(current_frame)

    def save_pose_data(self):
        filename = f'pose_data.json'
        with open(filename, 'w') as f:
            json.dump({
                'metadata': {
                    'frame_count': self.frame_count,
                    'landmark_indices': self.LANDMARK_INDICES
                },
                'frames': self.pose_data
            }, f, indent=2)
        print(f"Pose data saved to {filename}")


if __name__ == "__main__":
    capturer = PoseLandmarkCapture()
    capturer.capture_landmarks()