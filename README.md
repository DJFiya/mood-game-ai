# Mood AI Game

This project is an interactive Python application that uses real-time emotion recognition from your webcam to influence the behavior of a Non-Player Character (NPC). The NPC's responses change dynamically based on your detected facial emotion.

## Features

- Real-time emotion detection using your webcam and DeepFace.
- NPC behavior adapts to your mood (happy, angry, sad, surprise, neutral).
- Simple command-line interface.

## Requirements

- Python 3.7+
- OpenCV (`opencv-python`)
- DeepFace
- A working webcam

## Installation

1. Clone or download this repository.
2. Install dependencies:
   ```bash
   pip install opencv-python deepface
   ```

## Usage

Run the main script:

```bash
python main.py
```

- A window will open showing your webcam feed.
- Detected emotion will be displayed, and the NPC will react accordingly in the terminal.
- Press `q` to quit.

## Notes

- Make sure your webcam is connected and accessible.
- For best results, use in a well-lit environments.
- Depending on your current pip version you might have to run this command:
```bash
pip install tf-keras
```
