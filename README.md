# Mood AI Game

This project is an interactive Python application that uses real-time emotion recognition from your webcam to influence the behavior of a Non-Player Character (NPC). The NPC's responses change dynamically based on your detected facial emotion.

## Features

- Real-time emotion detection using FER+ and dlib
- Animated NPC with dynamic facial expressions
- Temporal emotion smoothing for stability
- Speech bubbles and emotional responses
- Face tracking and alignment

## Requirements

- Python 3.7+
- OpenCV (`opencv-python`)
- FER (Facial Expression Recognition)
- dlib
- numpy
- moviepy version 1.0.3 (required by FER)
- Shape predictor file for facial landmarks
- A working webcam

## Installation

1. Clone or download this repository

2. Install dependencies:

   ```bash
   pip install opencv-python numpy dlib fer
   pip install moviepy==1.0.3
   ```

3. Download the shape predictor file:

   ```bash
   # Windows (PowerShell)
   Invoke-WebRequest -Uri "http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2" -OutFile "shape_predictor_68_face_landmarks.dat.bz2"
   # Extract using 7-zip or similar tool

   # Linux/Mac
   wget http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2
   bunzip2 shape_predictor_68_face_landmarks.dat.bz2
   ```

4. Place the extracted `shape_predictor_68_face_landmarks.dat` file in the project root directory

## Usage

Run the main script:

```bash
python main.py
```

- Two windows will open:
  - Live Emotion Camera: Shows your webcam feed with emotion detection
  - NPC: Shows the animated character responding to your emotions
- Press `q` to quit

## Emotions

The NPC responds to these emotional states:

- Happy → Friendly response
- Angry → Defensive response
- Sad → Sympathetic response
- Surprise → Curious response
- Neutral → Neutral response

## Troubleshooting

- If you get TensorFlow/Keras errors, try:

  ```bash
  pip install tf-keras
  ```

- If dlib installation fails, you might need to install C++ build tools:
  - Windows: Install Visual Studio Build Tools
  - Linux: `sudo apt-get install build-essential cmake`
- Make sure your webcam is connected and accessible
- Use good lighting for better emotion detection
- Keep face centered and clearly visible
