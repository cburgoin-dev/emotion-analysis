import cv2

from src.utils.emotion_detector import (
    detect_emotion_from_frame,
    draw_emotion
)

WINDOW_NAME = "Detección de Emociones"

DETECTOR_BACKEND = "opencv"

INFO_TEXT_COLOR = (255, 255, 255)
INFO_FONT_SCALE = 0.7

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

            emotion, face_area, detection_time = detect_emotion_from_frame(
                frame,
                DETECTOR_BACKEND
            )

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

        # Permite cerrar la ventana presionando la tecla 'q'
        if key & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    start_camera()