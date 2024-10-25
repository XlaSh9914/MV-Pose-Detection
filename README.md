# Machine Vision Human Pose Detection

## Table of Contents
1. [Project Description](#project-description)
2. [Project Domain](#project-domain)
3. [Features](#features)
4. [Installation](#installation)
5. [Usage](#usage)
6. [Contributing](#contributing)
7. [License](#license)
8. [Contact](#contact)

---

## Project Description

This project provides a human pose detection system that interfaces with Blender to create a fully-rigged armature for animation. By capturing human posture from either video input or a live camera, the system generates detailed skeletal data for a realistic rig, enabling animations to mirror real-time or recorded movements.
---

## Project Domain

**`Computer Vision`**, **`3D Animation`**, **`Augmented Reality (AR)`**, **`Virtual Reality (VR)`**, **`Human-Computer Interaction (HCI)`**

---

## Features

- **Real-time Pose Detection**: Tracks human pose live from a camera.
- **Video-based Animation**: Uses video inputs to generate animatable rigs.
- **Detailed Skeletal Mapping**:
  - **Hand with Fingers**: Captures precise hand and finger movements.
  - **Face with Eyes and Mouth**: Detects facial points for expressions.
  - **Main Body Joints**: Tracks core joints for full-body animation.
- **Blender Armature Integration**: Converts pose data into Blender rigs.
- **JSON Output**: Exports pose data in JSON for easy integration.

---

## Highlights

- **Realistic Animation**: Creates precise animations by capturing detailed joint data.
- **Wide Applications**: Ideal for VR/AR, gaming, and film for realistic movement.
- **Blender Compatibility**: Directly integrates with Blender for seamless rigging.
- **Flexible and Modular**: Use individual or combined modules for custom setups.

---

## Installation

To get a local copy up and running, follow these simple steps:

1. Clone the repository:
    ```bash
    git clone https://github.com/XlaSh9914/MV-Pose-Detection.git
    ```

2. Navigate into the project directory:
    ```bash
    cd MV-Pose-Detection
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
    install blender
    (to se errors while execution open blender through cmd)

---

## Usage

## 1. Recording Data

To generate JSON output files, run each of the following scripts once to generate the required data:

```bash
python body_detect.py
python face_detect.py
python static_pose_detect.py
```

-**Instructions**: 
  -Press "Q" to stop recording and store json file

-**Warning**:
  - Running script again after successful execution will override the json file

## 2. Setting up Blender files

To set up blender files for running:

- **Set file locations**: Do the following changes to set the location of input file (json):
  - **For face_rig.py**: 
  ```bash
78 json_path = r"D:\Projects\MV-Pose-Detection\face_data.json"  # Update this path to where your json file is stored
```
  - **For pose_rig.py**:
  ```bash
80 json_path = r"D:\Projects\MV-Pose-Detection\pose_data.json"  # Update this path to where your json file is stored
```

  - **For static_pose_rig.py**:
  ```bash
12 with open(r"D:\Projects\MV-Pose-Detection\generated_data\static_pose_data.json") as f: # Update this path to where your json file is stored
```

## 3. Run the Blender scripts

To run the scripts to import the json data

- **Run Scripts on Blender**: After setting up blender files, open these scripts in Blender
  - blender_code\face_rig.py (to render face_data.json)
  - blender_code\pose_rig.py (to render pose_data.json)
  - blender_code\static_pose_rig.py (to render static_pose_data.json)

## 4. Viewing Animation

To view your animation, press **'space'** in **3D Viewport**.
