import time

from emotion_model import stream_emotion
from npc import NPC

DELAY = 0.05  # seconds

def main():
    npc = NPC()

    for emotion in stream_emotion():
        print(f"\nDetected Emotion: {emotion}")
        npc.update_behavior(emotion)
        npc.interact()
        time.sleep(DELAY)

if __name__ == "__main__":
    main()
