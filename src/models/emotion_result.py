from dataclasses import dataclass
from datetime import datetime

@dataclass
class EmotionResult:

    timestamp: datetime

    user_name: str

    emotion: str

    confidence: float

    fps: float

    detection_time: float

    backend: str