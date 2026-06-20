import pandas as pd

def export_results_to_excel(results, file_name="emotion_results.xlsx"):
    """
    Exporta los resultados emocionales a un archivo Excel.
    """

    data = []

    for result in results:

        data.append({
            "Timestamp": result.timestamp,
            "Identifier": result.identifier,
            "Emotion": result.emotion,
            "Confidence": result.confidence,
            "FPS": result.fps,
            "Detection Time": result.detection_time,
            "Backend": result.backend
        })

    dataframe = pd.DataFrame(data)

    dataframe.to_excel(
        file_name,
        index=False
    )

    print(f"Resultados exportados a {file_name}")