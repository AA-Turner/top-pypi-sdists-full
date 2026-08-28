"""Face Recognition — Access Control profile (door / gate mounted camera)."""

from dataclasses import dataclass

from ..face_reg.face_recognition import (
    FaceRecognitionEmbeddingConfig,
    FaceRecognitionEmbeddingUseCase,
)


@dataclass
class FaceRecognitionAccessControlConfig(FaceRecognitionEmbeddingConfig):
    """Stricter gates for frontal, large faces at entry points."""

    usecase: str = "fr_access_control"
    category: str = "security"
    confidence_threshold: float = 0.55
    similarity_threshold: float = 0.52
    min_face_w: int = 80
    min_face_h: int = 80
    probation_frames: int = 8
    unknown_patience: int = 3
    switch_patience: int = 8
    tracker_buffer: int = 90
    tracker_max_time_lost: int = 45
    activity_cooldown_sec: float = 45.0
    # Every face that clears confidence_threshold is matched, not just the largest one:
    # tailgating at a door means several people are legitimately in frame at once, and
    # recognizing only the dominant face silently drops the others. Still overridable
    # per-deployment for cameras that really do see one subject at a time.
    single_face_mode: bool = False


class FaceRecognitionAccessControlUseCase(FaceRecognitionEmbeddingUseCase):
    """Access-control FR: all faces above threshold, stricter quality thresholds."""

    def __init__(self, config: FaceRecognitionAccessControlConfig | None = None):
        init_config = config or FaceRecognitionAccessControlConfig()
        super().__init__(config=init_config)
        self.name = "fr_access_control"
        self.category = "security"
        self.CASE_TYPE = "fr_access_control"
        self.CASE_VERSION = "1.0"
