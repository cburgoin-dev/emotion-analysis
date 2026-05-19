import tkinter as tk
import cv2
import sys
import os

from tkinter import ttk
from PIL import Image, ImageTk

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..")
    )
)

from src.utils.emotion_detector import (
    detect_emotion_from_frame,
    draw_emotion
)

class EmotionApp:

    def __init__(self):

        self.root = tk.Tk()

        self.root.title("Sistema de Detección de Emociones")

        self.root.geometry("1000x600")

        self.create_layout()

        self.cap = None
        self.camera_running = False

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
            width=700,
            height=600
        )

        self.video_frame.pack(side="left", fill="both")
        self.video_frame.pack_propagate(False)

        self.video_label = tk.Label(self.video_frame)

        self.video_label.pack(fill="both", expand=True)

        # Frame derecho (panel información)
        self.info_frame = tk.Frame(
            self.root,
            bg="#1e1e1e",
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
            font=("Arial", 16, "bold"),
            fg="white",
            bg="#1e1e1e"
        )

        title_label.pack(pady=20)

        # Selector backend
        backend_label = tk.Label(
            self.info_frame,
            text="Detector Facial",
            font=("Arial", 11, "bold"),
            fg="white",
            bg="#1e1e1e"
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
            fg="white",
            bg="#1e1e1e",
            font=("Arial", 11)
        )

        self.emotion_label.pack(pady=10)

        self.fps_label = tk.Label(
            self.info_frame,
            text="FPS: -",
            fg="white",
            bg="#1e1e1e",
            font=("Arial", 11)
        )

        self.fps_label.pack(pady=10)

        self.detection_label = tk.Label(
            self.info_frame,
            text="Detección: -",
            fg="white",
            bg="#1e1e1e",
            font=("Arial", 11)
        )

        self.detection_label.pack(pady=10)

        # Botones
        start_button = tk.Button(
            self.info_frame,
            text="Iniciar Cámara",
            font=("Arial", 10, "bold"),
            width=20,
            fg="white",
            bg="#2d2d2d",
            command=self.start_camera
        )

        start_button.pack(pady=20)

        stop_button = tk.Button(
            self.info_frame,
            text="Detener Cámara",
            font=("Arial", 10, "bold"),
            width=20,
            fg="white",
            bg="#2d2d2d",
            command=self.stop_camera
        )

        stop_button.pack()

    def start_camera(self):
        """
        Inicia la cámara y comienza la actualización de frames.
        """

        if self.camera_running:
            return

        self.cap = cv2.VideoCapture(0)

        self.camera_running = True

        self.update_frame()

    def stop_camera(self):
        """
        Detiene la cámara.
        """

        self.camera_running = False

        if self.cap:

            self.cap.release()

            self.cap = None

        # Limpiar imagen del video
        self.video_label.configure(image="")

        self.video_label.imgtk = None

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

            emotion, face_area, detection_time = detect_emotion_from_frame(
                frame,
                backend
            )

            fps = 1 / detection_time if detection_time > 0 else 0

            draw_emotion(frame, emotion, face_area)

            self.emotion_label.config(
                text=f"Emoción: {emotion}"
            )

            self.fps_label.config(
                text=f"FPS: {fps:.2f}"
            )

            self.detection_label.config(
                text=f"Detección: {detection_time:.2f}s"
            )

        except Exception as e:

            print(f"Error de detección: {e}")

        # Convertir BGR -> RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

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