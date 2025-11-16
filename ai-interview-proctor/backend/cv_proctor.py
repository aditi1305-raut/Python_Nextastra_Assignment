import cv2
import numpy as np
import base64
from io import BytesIO
from PIL import Image
import mediapipe as mp

mp_face_mesh = mp.solutions.face_mesh

def decode_base64_image(data_url: str):
    header, encoded = data_url.split(",", 1) if ',' in data_url else (None, data_url)
    data = base64.b64decode(encoded)
    img = Image.open(BytesIO(data)).convert("RGB")
    arr = np.array(img)[:, :, ::-1].copy()
    return arr

# Simple face detection using Haar Cascade (works offline, no dlib needed)
def detect_faces_simple(frame_bgr):
    gray = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)
    cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = cascade.detectMultiScale(gray, 1.1, 4)
    return len(faces)

# Blink detection using MediaPipe landmarks
def estimate_blink(frame_bgr):
    with mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1, refine_landmarks=True) as fm:
        rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        res = fm.process(rgb)

        if not res.multi_face_landmarks:
            return {"face_found": False, "blink": False, "ear": 0.0}

        lm = res.multi_face_landmarks[0]
        h, w, _ = frame_bgr.shape

        left_eye = [33, 160, 158, 133, 153, 144]
        right_eye = [362, 385, 387, 263, 373, 380]

        def EAR(indices):
            pts = [(int(lm.landmark[i].x * w), int(lm.landmark[i].y * h)) for i in indices]
            A = np.linalg.norm(np.array(pts[1]) - np.array(pts[5]))
            B = np.linalg.norm(np.array(pts[2]) - np.array(pts[4]))
            C = np.linalg.norm(np.array(pts[0]) - np.array(pts[3]))

            return (A + B) / (2.0 * C) if C != 0 else 0

        ear_left = EAR(left_eye)
        ear_right = EAR(right_eye)
        ear = (ear_left + ear_right) / 2.0

        blink = ear < 0.18

        return {"face_found": True, "blink": blink, "ear": float(ear)}
