from deepface import DeepFace
import time
import cv2

DEFAULT_BACKEND = "opencv"

RECTANGLE_COLOR = (0, 255, 0)
TEXT_COLOR = (255, 255, 255)
RECTANGLE_THICKNESS = 2

def detect_emotion_from_frame(frame, backend=DEFAULT_BACKEND):
    """
    Detecta la emoción dominante en un frame utilizando DeepFace.
    """

    start_time = time.time()

    result = DeepFace.analyze(
        frame,
        actions=['emotion'],
        detector_backend=backend,

        # Evita errores cuando no se detecta un rostro
        enforce_detection=False
    )

    if isinstance(result, list):
        result = result[0]

    emotion = result['dominant_emotion']

    emotion_scores = result['emotion']

    face_area = result['region']

    detection_time = time.time() - start_time

    return (
        emotion,
        emotion_scores,
        face_area,
        detection_time
    )

def is_valid_face(face_area, frame_shape):
    """
    Valida si el área detectada corresponde a un rostro razonable.
    """

    x = face_area['x']
    y = face_area['y']
    w = face_area['w']
    h = face_area['h']

    frame_height, frame_width = frame_shape[:2]

    if w <= 0 or h <= 0:
        return False

    if w > frame_width * 0.9 or h > frame_height * 0.9:
        return False

    if w < 50 or h < 50:
        return False

    return True

def draw_emotion(frame, emotion, face_area):
    """
    Dibuja la emoción detectada sobre el frame.
    """

    if not is_valid_face(face_area, frame.shape):
        return

    x = face_area['x']
    y = face_area['y']
    w = face_area['w']
    h = face_area['h']

    cv2.rectangle(
        frame,
        (x, y),
        (x + w, y + h),
        RECTANGLE_COLOR,
        RECTANGLE_THICKNESS
    )

    cv2.putText(
        frame,
        emotion,
        (x, y - 15),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        TEXT_COLOR,
        RECTANGLE_THICKNESS
    )