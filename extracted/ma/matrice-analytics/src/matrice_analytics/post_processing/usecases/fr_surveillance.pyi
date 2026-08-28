"""Auto-generated stub for module: fr_surveillance."""
from typing import Any, Optional

from ..face_reg.face_recognition import FaceRecognitionEmbeddingConfig, FaceRecognitionEmbeddingUseCase

# Classes
class FaceRecognitionSurveillanceConfig:
    # Permissive gates for small, distant faces (≈ legacy face_recognition).

    ...
class FaceRecognitionSurveillanceUseCase:
    # Surveillance FR: multi-face, long tracker buffer, tolerant thresholds.

    def __init__(self: Any, config: Optional[Any] = None) -> None: ...

