from deepface import DeepFace
import cv2

WINDOW_NAME = "Emotion Detection"
TEXT_POSITION = (50, 50)
DETECTOR_BACKEND = "opencv"


def detect_emotion_from_frame(frame):
    """
    Detecta la emoción dominante en un frame capturado desde la webcam.
    """

    result = DeepFace.analyze(
        frame,
        actions=['emotion'],
        detector_backend=DETECTOR_BACKEND,

        # Evita errores cuando no se detecta un rostro
        enforce_detection=False
    )

    if isinstance(result, list):
        return result[0]['dominant_emotion']

    return result['dominant_emotion']

def draw_emotion(frame, emotion):
    """
    Dibuja la emoción detectada sobre el frame.
    """

    cv2.putText(
        frame,
        emotion,
        TEXT_POSITION,
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
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

            emotion = detect_emotion_from_frame(frame)

            draw_emotion(frame, emotion)

        except Exception as e:
            print(f"Error de detección: {e}")

        cv2.imshow(WINDOW_NAME, frame)

        key = cv2.waitKey(1)

        # Presionar 'q' para cerrar la ventana
        if key & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    start_camera()