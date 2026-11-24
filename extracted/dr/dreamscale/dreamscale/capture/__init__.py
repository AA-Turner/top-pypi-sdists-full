"""Off-hot-path robot episode capture and latency-aware background upload."""

from dreamscale.capture.spool import EpisodeSummary, SpoolEpisode
from dreamscale.capture.uploader import (
    DEFAULT_ACTIVE_BYTES_PER_SEC,
    CaptureManager,
    SpoolUploader,
    UploadOutcome,
    default_spool_root,
)

__all__ = [
    "CaptureManager",
    "DEFAULT_ACTIVE_BYTES_PER_SEC",
    "EpisodeSummary",
    "SpoolEpisode",
    "SpoolUploader",
    "UploadOutcome",
    "default_spool_root",
]
