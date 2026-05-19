from deepface import DeepFace
import cv2
import time

WINDOW_NAME = "Detección de Emociones"
TEXT_POSITION = (50, 50)
DETECTOR_BACKEND = "opencv"
INFO_TEXT_COLOR = (255, 255, 255)
INFO_FONT_SCALE = 0.7


def detect_emotion_from_frame(frame):
    """
    Detecta la emoción dominante en un frame capturado desde la webcam.
    """

    start_time = time.time()

    result = DeepFace.analyze(
        frame,
        actions=['emotion'],
        detector_backend=DETECTOR_BACKEND,

        # Evita errores cuando no se detecta un rostro
        enforce_detection=False
    )

    if isinstance(result, list):
        result = result[0]

    emotion = result['dominant_emotion']
    face_area = result['region']

    detection_time = time.time() - start_time

    return emotion, face_area, detection_time

def draw_emotion(frame, emotion, face_area):
    """
    Dibuja la emoción detectada sobre el frame.
    """

    x = face_area['x']
    y = face_area['y']
    w = face_area['w']
    h = face_area['h']

    frame_height, frame_width = frame.shape[:2]

    if w <= 0 or h <= 0:
        return

    if w > frame_width * 0.9 or h > frame_height * 0.9:
        return

    if w < 50 or h < 50:
        return

    cv2.rectangle(
        frame,
        (x, y),
        (x + w, y + h),
        (0, 255, 0),
        2
    )

    cv2.putText(
        frame,
        emotion,
        (x, y - 15),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 255, 255),
        2
    )

def start_camera():
    """
    Inicia la captura de video en tiempo real utilizando la webcam.
    """

    # Inicializa la webcam principal del sistema
    cap = cv2.VideoCapture(0)

    while True:

        ret, frame = cap.read()

        # Si no se pudo capturar el frame, termina el programa
        if not ret:
            break

        try:

            emotion, face_area, detection_time = detect_emotion_from_frame(frame)

            fps = 1 / detection_time if detection_time > 0 else 0

            draw_emotion(frame, emotion, face_area)

            cv2.putText(
                frame,
                f"Backend: {DETECTOR_BACKEND}",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                INFO_FONT_SCALE,
                INFO_TEXT_COLOR,
                2
            )

            cv2.putText(
                frame,
                f"Detection: {detection_time:.2f}s",
                (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX,
                INFO_FONT_SCALE,
                INFO_TEXT_COLOR,
                2
            )

            cv2.putText(
                frame,
                f"FPS: {fps:.2f}",
                (10, 90),
                cv2.FONT_HERSHEY_SIMPLEX,
                INFO_FONT_SCALE,
                INFO_TEXT_COLOR,
                2
            )

        except Exception as e:
            print(f"Error de detección: {e}")

        cv2.imshow(WINDOW_NAME, frame)

        key = cv2.waitKey(1)

        if cv2.getWindowProperty(WINDOW_NAME, cv2.WND_PROP_VISIBLE) < 1:
            break

        # Presionar 'q' para cerrar la ventana
        if key & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    start_camera()