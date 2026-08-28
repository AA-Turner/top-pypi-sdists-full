"""Auto-generated stub for module: fr_access_control."""
from typing import Any

from ..face_reg.face_recognition import FaceRecognitionEmbeddingConfig, FaceRecognitionEmbeddingUseCase

# Classes
class FaceRecognitionAccessControlConfig:
    # Stricter gates for frontal, large faces at entry points.

    ...
class FaceRecognitionAccessControlUseCase:
    # Access-control FR: all faces above threshold, stricter quality thresholds.

    def __init__(self: Any, config: Any | None = None) -> None: ...

