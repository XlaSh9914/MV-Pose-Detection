import cv2
import mediapipe as mp
import json

# Initialize Mediapipe Pose detection
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# Start capturing from the webcam
cap = cv2.VideoCapture(0)

# Function to map Mediapipe landmarks to bones with descriptive names for the full body
def landmarks_to_bones(landmarks):
    bone_data = {
        "bones": {}
    }

    # Define connections with descriptive names for bones
    connections = [
        # Head and torso
        ("head_to_neck", 0, 1),
        ("neck_to_left_shoulder", 1, 11),
        ("neck_to_right_shoulder", 1, 12),
        ("left_shoulder_to_left_elbow", 11, 13),
        ("left_elbow_to_left_wrist", 13, 15),
        ("right_shoulder_to_right_elbow", 12, 14),
        ("right_elbow_to_right_wrist", 14, 16),
        ("neck_to_spine", 1, 23),
        ("spine_to_left_hip", 23, 25),
        ("spine_to_right_hip", 23, 24),
        ("left_hip_to_left_knee", 25, 27),
        ("left_knee_to_left_ankle", 27, 29),
        ("right_hip_to_right_knee", 24, 26),
        ("right_knee_to_right_ankle", 26, 28)
    ]
    
    # Add the bones using the specified connections and names
    for bone_name, start_idx, end_idx in connections:
        head = [landmarks[start_idx].x, landmarks[start_idx].y, landmarks[start_idx].z]
        tail = [landmarks[end_idx].x, landmarks[end_idx].y, landmarks[end_idx].z]
        
        bone_data["bones"][bone_name] = {
            "head": head,
            "tail": tail
        }

    return bone_data

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the image to RGB (Mediapipe expects RGB)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the image and detect body pose
    result = pose.process(rgb_frame)

    if result.pose_landmarks:
        # Draw the landmarks on the original frame (optional)
        mp_drawing.draw_landmarks(frame, result.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # Convert the landmarks into bones format with descriptive names
        landmarks = result.pose_landmarks.landmark
        bone_data = landmarks_to_bones(landmarks)

        # Print bone data as JSON (you can write it to a file if needed)
        json_data = json.dumps(bone_data, indent=4)
        print(json_data)

        # Optionally, write the JSON data to a file
        with open(".\generated_data\static_pose_data.json", "w") as f:
            f.write(json_data)

    # Display the frame
    cv2.imshow('Body Pose Tracking', frame)

    # Exit with the 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()