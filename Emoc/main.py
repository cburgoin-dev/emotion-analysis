import os
from deepface import DeepFace
import matplotlib.pyplot as plt
from collections import Counter

dataset_path = "C:/Users/Emili/Downloads/Emoc/personas"

for persona in os.listdir(dataset_path):

    persona_path = os.path.join(dataset_path, persona)

    if os.path.isdir(persona_path):

        emociones = []

        print("\nAnalizando persona:", persona)

        for foto in os.listdir(persona_path):

            foto_path = os.path.join(persona_path, foto)

            try:
                resultados = DeepFace.analyze(
                    img_path=foto_path,
                    actions=['emotion'],
                    detector_backend='retinaface',
                    enforce_detection=False
                )

                emocion = resultados[0]['dominant_emotion']
                emociones.append(emocion)

                print(foto, "->", emocion)

            except Exception as e:
                print("Error:", foto)

        conteo = Counter(emociones)

        etiquetas = list(conteo.keys())
        valores = list(conteo.values())

        plt.figure()
        plt.bar(etiquetas, valores)
        plt.title(f"Emociones detectadas - {persona}")
        plt.xlabel("Emocion")
        plt.ylabel("Cantidad")

        plt.show()