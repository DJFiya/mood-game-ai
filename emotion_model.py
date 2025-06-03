import cv2
import numpy as np
from collections import deque
from fer import FER
import dlib

class EmotionDetector:
    def __init__(self):
        self.detector = FER(mtcnn=True)
        
        self.face_detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
        
        self.emotion_history = deque(maxlen=10)
        self.confidence_threshold = 0.3
        
        self.emotion_map = {
            'angry': 'angry',
            'disgust': 'angry',
            'fear': 'defensive',
            'happy': 'happy',
            'sad': 'sad',
            'surprise': 'surprise',
            'neutral': 'neutral'
        }

    def align_face(self, image, face):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        landmarks = self.predictor(gray, face)
        return image  

    def smooth_emotions(self, emotion):
        self.emotion_history.append(emotion)
        if len(self.emotion_history) < self.emotion_history.maxlen:
            return emotion

        emotion_counts = {}
        for e in self.emotion_history:
            emotion_counts[e] = emotion_counts.get(e, 0) + 1

        return max(emotion_counts.items(), key=lambda x: x[1])[0]

    def detect_emotion(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_detector(gray, 1)
        
        if not faces:
            return "neutral", None

        face = max(faces, key=lambda rect: rect.width() * rect.height())
        
        aligned_face = self.align_face(frame, face)
        
        emotions = self.detector.detect_emotions(aligned_face)
        
        if not emotions:
            return "neutral", None

        emotion_data = emotions[0]['emotions']
        dominant_emotion = max(emotion_data.items(), key=lambda x: x[1])
        
        if dominant_emotion[1] < self.confidence_threshold:
            return "neutral", None

        mapped_emotion = self.emotion_map.get(dominant_emotion[0], "neutral")
        
        smoothed_emotion = self.smooth_emotions(mapped_emotion)
        
        return smoothed_emotion, face

def stream_emotion():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    emotion_detector = EmotionDetector()
    print("Initializing emotion detector...")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break

        emotion, face = emotion_detector.detect_emotion(frame)

        if face:
            x, y = face.left(), face.top()
            w, h = face.width(), face.height()
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, emotion, (x, y - 10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        cv2.imshow("Live Emotion Camera", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        yield emotion

    cap.release()
    cv2.destroyAllWindows()
