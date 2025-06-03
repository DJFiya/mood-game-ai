import cv2
import numpy as np
import time
import random

class NPC:
    def __init__(self, emotion="neutral"):
        self.state = emotion
        self.last_blink = time.time()
        self.blinking = False
        self.blink_duration = 0.15
        self.next_blink = random.uniform(2, 4)
        self.smile_anim = 0
        self.smile_dir = 1
        self.last_smile_update = time.time()
        self.head_tilt = 0

    def update_behavior(self, emotion):
        if emotion == "happy":
            self.state = "friendly"
        elif emotion == "angry":
            self.state = "defensive"
        elif emotion == "sad":
            self.state = "sympathetic"
        elif emotion == "surprise":
            self.state = "curious"
        else:
            self.state = "neutral"

    def _update_blink(self):
        now = time.time()
        if self.blinking:
            if now - self.last_blink > self.blink_duration:
                self.blinking = False
                self.last_blink = now
                self.next_blink = random.uniform(2, 4)
        else:
            if now - self.last_blink > self.next_blink:
                self.blinking = True
                self.last_blink = now

    def _update_smile(self):
        if self.state == "friendly":
            now = time.time()
            if now - self.last_smile_update > 0.07:
                self.smile_anim += self.smile_dir
                if self.smile_anim > 8 or self.smile_anim < -8:
                    self.smile_dir *= -1
                self.last_smile_update = now
        else:
            self.smile_anim = 0
            self.smile_dir = 1

    def _update_head_tilt(self):
        if self.state == "curious":
            self.head_tilt = int(8 * np.sin(time.time() * 2))
        else:
            self.head_tilt = 0

    def draw(self):
        self._update_blink()
        self._update_smile()
        self._update_head_tilt()

        face_colors = {
            "friendly": (180, 255, 255),    # light yellow
            "defensive": (255, 230, 220),   # light blue
            "sympathetic": (255, 240, 220), # light blue
            "curious": (220, 245, 255),     # light orange
            "neutral": (245, 245, 245)      # light gray
        }
        face_color = face_colors.get(self.state, (180, 255, 255))

        img = np.ones((400, 400, 3), dtype=np.uint8) * 255
        
        face_layer = img.copy()

        cv2.circle(face_layer, (200, 200), 120, face_color, -1) 
        cv2.circle(face_layer, (200, 200), 120, (0, 0, 0), 2) 


        # Eyes
        left_eye = (150, 170)
        right_eye = (250, 170)
        eye_radius = 20
        if self.blinking:
            cv2.ellipse(face_layer, left_eye, (eye_radius, 5), 0, 0, 360, (0, 0, 0), -1)
            cv2.ellipse(face_layer, right_eye, (eye_radius, 5), 0, 0, 360, (0, 0, 0), -1)
        else:
            cv2.circle(face_layer, left_eye, eye_radius, (255, 255, 255), -1)
            cv2.circle(face_layer, right_eye, eye_radius, (255, 255, 255), -1)
            cv2.circle(face_layer, left_eye, 8, (0, 0, 0), -1)
            cv2.circle(face_layer, right_eye, 8, (0, 0, 0), -1)
            cv2.circle(face_layer, (left_eye[0] - 5, left_eye[1] - 5), 3, (255, 255, 255), -1)
            cv2.circle(face_layer, (right_eye[0] - 5, right_eye[1] - 5), 3, (255, 255, 255), -1)

        # Tears
        if self.state == "sympathetic" and not self.blinking:
            cv2.ellipse(face_layer, (left_eye[0], left_eye[1] + 22), (5, 10), 0, 0, 360, (255, 200, 150), -1)
            cv2.ellipse(face_layer, (right_eye[0], right_eye[1] + 22), (5, 10), 0, 0, 360, (255, 200, 150), -1)
            cv2.ellipse(face_layer, (left_eye[0], left_eye[1] + 32), (3, 6), 0, 0, 360, (200, 180, 255), -1)
            cv2.ellipse(face_layer, (right_eye[0], right_eye[1] + 32), (3, 6), 0, 0, 360, (200, 180, 255), -1)

        # Eyebrows and mouth
        if self.state == "friendly":
            cv2.ellipse(face_layer, (200, 240), (50, 25 + self.smile_anim), 0, 0, 180, (0, 0, 0), 4)
            cv2.line(face_layer, (130, 140), (170, 150), (0, 0, 0), 4)
            cv2.line(face_layer, (230, 150), (270, 140), (0, 0, 0), 4)
        elif self.state == "defensive":
            cv2.ellipse(face_layer, (200, 260), (50, 20), 0, 0, -180, (0, 0, 0), 4)
            cv2.line(face_layer, (130, 140), (170, 130), (0, 0, 0), 4)
            cv2.line(face_layer, (230, 130), (270, 140), (0, 0, 0), 4)
        elif self.state == "sympathetic":
            cv2.ellipse(face_layer, (200, 260), (40, 15), 0, 0, 180, (0, 0, 0), 2)
            cv2.line(face_layer, (130, 150), (170, 140), (0, 0, 0), 3)
            cv2.line(face_layer, (230, 140), (270, 150), (0, 0, 0), 3)
        elif self.state == "curious":
            cv2.circle(face_layer, (200, 250), 20, (0, 0, 0), 3)
            cv2.line(face_layer, (130, 130), (170, 120), (0, 0, 0), 3)
            cv2.line(face_layer, (230, 120), (270, 130), (0, 0, 0), 3)
        else:
            cv2.line(face_layer, (170, 250), (230, 250), (0, 0, 0), 3)
            cv2.line(face_layer, (130, 140), (170, 140), (0, 0, 0), 3)
            cv2.line(face_layer, (230, 140), (270, 140), (0, 0, 0), 3)

        face_mask = np.zeros((400, 400), dtype=np.uint8)
        cv2.circle(face_mask, (200, 200), 120, 255, -1)
        
        M = cv2.getRotationMatrix2D((200, 200), self.head_tilt, 1.0)
        face_layer = cv2.warpAffine(face_layer, M, (400, 400), borderValue=(255, 255, 255))
        face_mask = cv2.warpAffine(face_mask, M, (400, 400), borderValue=0)

        face_mask = cv2.cvtColor(face_mask, cv2.COLOR_GRAY2BGR) / 255.0
        img = img * (1 - face_mask) + face_layer * face_mask

        messages = {
            "friendly": "Hi there! 😊",
            "defensive": "Please keep your distance!",
            "sympathetic": "Are you okay?",
            "curious": "Wow! That's surprising!",
            "neutral": "Hello."
        }
        msg = messages.get(self.state, "")

        # Draw speech bubble
        if msg:
            cv2.rectangle(img, (20, 40), (380, 90), (255, 255, 255), -1)
            cv2.rectangle(img, (20, 40), (380, 90), (180, 180, 180), 2)
            pts = np.array([[80, 90], [100, 110], [120, 90]], np.int32)
            cv2.fillPoly(img, [pts], (255, 255, 255))
            cv2.polylines(img, [pts], isClosed=True, color=(180, 180, 180), thickness=2)
            cv2.putText(img, msg, (30, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (50, 50, 50), 2, cv2.LINE_AA)

        cv2.putText(img, f"NPC: {self.state}", (10, 390), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (50, 50, 50), 2)
        return img.astype(np.uint8)

    def interact(self):
        img = self.draw()
        cv2.imshow("NPC", img)
