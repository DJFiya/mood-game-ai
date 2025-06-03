import time
import cv2

from emotion_model import stream_emotion
from npc import NPC

DELAY = 0.05  # seconds

def main():
    npc = NPC()
    print("NPC initialized - starting main loop")

    for emotion in stream_emotion():
        print(f"\nDetected Emotion: {emotion}")
        npc.update_behavior(emotion)
        
        face_img = npc.draw()
        if face_img is not None:
            print(f"Face image shape: {face_img.shape}")
            npc.interact()
            
        key = cv2.waitKey(1)
        if key & 0xFF == ord('q'):
            break
        time.sleep(DELAY)

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
