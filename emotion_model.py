import cv2
from deepface import DeepFace

def stream_emotion():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    emotion = "neutral"

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break

        try:
            results = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)

            for face in results:
                x, y, w, h = face['region']['x'], face['region']['y'], face['region']['w'], face['region']['h']
                emotion = face['dominant_emotion']

                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, emotion, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        except Exception as e:
            print("DeepFace error:", e)

        cv2.imshow("Live Emotion Camera", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        yield emotion  

    cap.release()
    cv2.destroyAllWindows()
