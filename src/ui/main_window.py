import tkinter as tk
import cv2
import sys
import os

from tkinter import ttk
from PIL import Image, ImageTk
from datetime import datetime

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..")
    )
)

from src.utils.emotion_detector import (
    detect_emotion_from_frame,
    draw_emotion,
    is_valid_face
)
from src.utils.exporter import export_results_to_excel

from src.models.emotion_result import EmotionResult

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 600

VIDEO_WIDTH = 700
VIDEO_HEIGHT = 600

BACKGROUND_COLOR = "#1e1e1e"
TEXT_COLOR = "white"
BUTTON_COLOR = "#2d2d2d"

TITLE_FONT = ("Arial", 16, "bold")
LABEL_FONT = ("Arial", 11)
BUTTON_FONT = ("Arial", 10, "bold")
STATUS_FONT = ("Arial", 11, "bold")

class EmotionApp:

    def __init__(self):

        self.root = tk.Tk()

        self.root.title("Sistema de Detección de Emociones")

        self.root.geometry(
            f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}"
        )

        self.create_layout()

        self.cap = None
        self.camera_running = False

        self.session_results = []

        # Manejo correcto al cerrar ventana
        self.root.protocol(
            "WM_DELETE_WINDOW",
            self.on_close
        )

    def create_layout(self):
        """
        Crea la estructura principal de la interfaz.
        """

        # Frame izquierdo (video)
        self.video_frame = tk.Frame(
            self.root,
            bg="black",
            width=VIDEO_WIDTH,
            height=VIDEO_HEIGHT
        )

        self.video_frame.pack(side="left", fill="both")
        self.video_frame.pack_propagate(False)

        self.video_label = tk.Label(
            self.video_frame,
            bg="black"
        )

        self.video_label.pack(fill="both", expand=True)

        # Frame derecho (panel información)
        self.info_frame = tk.Frame(
            self.root,
            bg=BACKGROUND_COLOR,
            width=300
        )

        self.info_frame.pack(side="right", fill="y")
        self.info_frame.pack_propagate(False)

        self.create_controls()

    def create_controls(self):
        """
        Crea los controles y métricas del sistema.
        """

        title_label = tk.Label(
            self.info_frame,
            text="Detección de Emociones",
            font=TITLE_FONT,
            fg=TEXT_COLOR,
            bg=BACKGROUND_COLOR
        )

        title_label.pack(pady=20)

        user_label = tk.Label(
            self.info_frame,
            text="Nombre Usuario",
            font=STATUS_FONT,
            fg=TEXT_COLOR,
            bg=BACKGROUND_COLOR
        )

        user_label.pack()

        self.user_entry = tk.Entry(
            self.info_frame,
            width=25
        )

        self.user_entry.pack(pady=10)

        # Selector backend
        backend_label = tk.Label(
            self.info_frame,
            text="Detector Facial",
            font=STATUS_FONT,
            fg=TEXT_COLOR,
            bg=BACKGROUND_COLOR
        )

        backend_label.pack()

        self.backend_selector = ttk.Combobox(
            self.info_frame,
            values=["opencv", "mtcnn", "retinaface"]
        )

        self.backend_selector.set("opencv")

        self.backend_selector.pack(pady=10)

        ttk.Separator(self.info_frame, orient="horizontal").pack(
            fill="x",
            pady=15
        )

        # Labels métricas
        self.emotion_label = tk.Label(
            self.info_frame,
            text="Emoción: -",
            fg=TEXT_COLOR,
            bg=BACKGROUND_COLOR,
            font=LABEL_FONT
        )

        self.emotion_label.pack(pady=10)

        self.confidence_label = tk.Label(
            self.info_frame,
            text="Confianza: -",
            fg=TEXT_COLOR,
            bg=BACKGROUND_COLOR,
            font=LABEL_FONT
        )

        self.confidence_label.pack(pady=10)

        self.fps_label = tk.Label(
            self.info_frame,
            text="FPS: -",
            fg=TEXT_COLOR,
            bg=BACKGROUND_COLOR,
            font=LABEL_FONT
        )

        self.fps_label.pack(pady=10)

        self.detection_label = tk.Label(
            self.info_frame,
            text="Detección: -",
            fg=TEXT_COLOR,
            bg=BACKGROUND_COLOR,
            font=LABEL_FONT
        )

        self.detection_label.pack(pady=10)

        self.status_label = tk.Label(
            self.info_frame,
            text="Estado: Cámara detenida",
            fg=TEXT_COLOR,
            bg=BACKGROUND_COLOR,
            font=STATUS_FONT
        )

        self.status_label.pack(pady=20)

        # Botones
        self.start_button = tk.Button(
            self.info_frame,
            text="Iniciar Cámara",
            font=BUTTON_FONT,
            width=20,
            fg=TEXT_COLOR,
            bg=BUTTON_COLOR,
            command=self.start_camera
        )

        self.start_button.pack(pady=20)

        self.stop_button = tk.Button(
            self.info_frame,
            text="Detener Cámara",
            font=BUTTON_FONT,
            width=20,
            fg=TEXT_COLOR,
            bg=BUTTON_COLOR,
            command=self.stop_camera
        )

        self.stop_button.pack()

        self.export_button = tk.Button(
            self.info_frame,
            text="Exportar Excel",
            font=BUTTON_FONT,
            width=20,
            fg=TEXT_COLOR,
            bg=BUTTON_COLOR,
            command=self.export_results
        )

        self.export_button.pack(pady=20)

        self.stop_button.config(state="disabled")

    def start_camera(self):
        """
        Inicia la cámara y comienza la actualización de frames.
        """

        if self.camera_running:
            return

        self.cap = cv2.VideoCapture(0)

        self.camera_running = True

        self.start_button.config(state="disabled")

        self.stop_button.config(state="normal")

        self.status_label.config(
            text="Estado: Cámara activa"
        )

        self.update_frame()

    def stop_camera(self):
        """
        Detiene la cámara.
        """

        self.camera_running = False

        self.start_button.config(state="normal")

        self.stop_button.config(state="disabled")

        self.status_label.config(
            text="Estado: Cámara detenida"
        )

        self.emotion_label.config(
            text="Emoción: -"
        )

        self.fps_label.config(
            text="FPS: -"
        )

        self.detection_label.config(
            text="Detección: -"
        )

        if self.cap:

            self.cap.release()

            self.cap = None

        # Limpiar imagen del video
        self.video_label.configure(
            image="",
            bg="black"
        )

        self.video_label.imgtk = None

    def export_results(self):
        """
        Exporta los resultados emocionales a Excel.
        """

        if not self.session_results:

            self.status_label.config(
                text="Estado: No hay datos para exportar"
            )

            return
        export_results_to_excel(
            self.session_results
        )

        self.status_label.config(
            text="Estado: Datos exportados"
        )

    def update_frame(self):
        """
        Captura y actualiza frames en la interfaz.
        """

        if not self.camera_running:
            return

        ret, frame = self.cap.read()

        if not ret:
            return

        backend = self.backend_selector.get()

        try:

            emotion, emotion_scores, face_area, detection_time = detect_emotion_from_frame(
                frame,
                backend
            )

        except Exception as e:

            print(f"Error de detección: {e}")

            self.status_label.config(
                text="Estado: Error de detección"
            )

            self.root.after(10, self.update_frame)

            return

        fps = 1 / detection_time if detection_time > 0 else 0

        face_detected = is_valid_face(
            face_area,
            frame.shape
        )

        if face_detected:

            draw_emotion(frame, emotion, face_area)

            confidence = emotion_scores[emotion]

            result = EmotionResult(
                timestamp=datetime.now(),
                user_name=self.user_entry.get(),
                emotion=emotion,
                confidence=confidence,
                fps=fps,
                detection_time=detection_time,
                backend=backend
            )

            self.session_results.append(result)

            self.emotion_label.config(
                text=f"Emoción: {emotion}"
            )

            self.confidence_label.config(
                text=f"Confianza: {confidence:.2f}%"
            )

            self.fps_label.config(
                text=f"FPS: {fps:.2f}"
            )

            self.detection_label.config(
                text=f"Detección: {detection_time:.2f}s"
            )

            self.status_label.config(
                text="Estado: Rostro detectado"
            )

        else:

            self.emotion_label.config(
                text="Emoción: -"
            )

            self.confidence_label.config(
                text="Confianza: -"
            )

            self.fps_label.config(
                text=f"FPS: {fps:.2f}"
            )

            self.detection_label.config(
                text=f"Detección: {detection_time:.2f}s"
            )

            self.status_label.config(
                text="Estado: Sin rostro detectado"
            )

        # Convertir BGR -> RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        frame = cv2.resize(
            frame,
            (VIDEO_WIDTH, VIDEO_HEIGHT)
        )

        # Convertir frame a imagen PIL
        image = Image.fromarray(frame)

        # Convertir PIL -> Tkinter
        image_tk = ImageTk.PhotoImage(image=image)

        # Mostrar imagen
        self.video_label.imgtk = image_tk

        self.video_label.configure(image=image_tk)

        # Actualizar nuevamente
        self.root.after(10, self.update_frame)

    def on_close(self):
        """
        Cierra correctamente la aplicación.
        """

        self.stop_camera()

        self.root.destroy()

    def run(self):

        self.root.mainloop()

if __name__ == "__main__":

    app = EmotionApp()

    app.run()