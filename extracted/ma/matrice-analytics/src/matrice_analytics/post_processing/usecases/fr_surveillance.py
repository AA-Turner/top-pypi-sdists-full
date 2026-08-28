"""Face Recognition — Surveillance profile (CCTV / in-the-wild)."""

from dataclasses import dataclass
from typing import Optional

from ..face_reg.face_recognition import (
    FaceRecognitionEmbeddingConfig,
    FaceRecognitionEmbeddingUseCase,
)


@dataclass
class FaceRecognitionSurveillanceConfig(FaceRecognitionEmbeddingConfig):
    """Permissive gates for small, distant faces (≈ legacy face_recognition)."""

    usecase: str = "fr_surveillance"
    category: str = "security"
    confidence_threshold: float = 0.25
    similarity_threshold: float = 0.42
    min_face_w: int = 30
    min_face_h: int = 40
    probation_frames: int = 45
    unknown_patience: int = 10
    switch_patience: int = 5
    tracker_buffer: int = 600
    tracker_max_time_lost: int = 300
    activity_cooldown_sec: float = 10.0
    single_face_mode: bool = False


class FaceRecognitionSurveillanceUseCase(FaceRecognitionEmbeddingUseCase):
    """Surveillance FR: multi-face, long tracker buffer, tolerant thresholds."""

    def __init__(self, config: Optional[FaceRecognitionSurveillanceConfig] = None):
        init_config = config or FaceRecognitionSurveillanceConfig()
        super().__init__(config=init_config)
        self.name = "fr_surveillance"
        self.category = "security"
        self.CASE_TYPE = "fr_surveillance"
        self.CASE_VERSION = "1.0"
