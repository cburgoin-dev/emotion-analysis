import os
from collections import Counter

from deepface import DeepFace
import matplotlib.pyplot as plt

DATASET_PATH = "dataset/personas"
DETECTOR_BACKEND = "retinaface"


def detect_emotion_from_image(image_path):
    """
    Detecta la emoción dominante en una imagen utilizando DeepFace.
    """

    result = DeepFace.analyze(
        img_path=image_path,
        actions=['emotion'],
        detector_backend=DETECTOR_BACKEND,

        # Evita errores cuando no se detecta un rostro
        enforce_detection=False
    )

    if isinstance(result, list):
        return result[0]['dominant_emotion']

    return result['dominant_emotion']

def generate_chart(person_name, emotions):
    """
    Genera una gráfica de barras con las emociones detectadas.
    """

    emotion_count = Counter(emotions)

    labels = list(emotion_count.keys())
    values = list(emotion_count.values())

    plt.figure()

    plt.bar(labels, values)

    plt.title(f"Emociones detectadas - {person_name}")
    plt.xlabel("Emoción")
    plt.ylabel("Cantidad")

    plt.show()

def analyze_person(person_name, person_path):
    """
    Analiza todas las imágenes pertenecientes a una persona.
    """

    emotions = []

    print(f"\nAnalizando persona: {person_name}")

    for photo in os.listdir(person_path):

        photo_path = os.path.join(person_path, photo)

        try:

            emotion = detect_emotion_from_image(photo_path)

            emotions.append(emotion)

            print(photo, "->", emotion)

        except Exception as e:

            print(f"Error analizando: {photo}")
            print(f"Detalles del error: {e}")

    generate_chart(person_name, emotions)

def analyze_dataset():
    """
    Recorre todas las carpetas del dataset y analiza cada persona.
    """

    for person in os.listdir(DATASET_PATH):

        person_path = os.path.join(DATASET_PATH, person)

        if os.path.isdir(person_path):

            analyze_person(person, person_path)

if __name__ == "__main__":
    analyze_dataset()