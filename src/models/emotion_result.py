from dataclasses import dataclass
from datetime import datetime

@dataclass
class EmotionResult:

    timestamp: datetime

    identifier: str

    emotion: str

    confidence: float

    fps: float

    detection_time: float

    backend: str