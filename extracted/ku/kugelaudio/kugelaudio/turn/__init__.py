"""Local, CPU-native semantic turn detection."""

from ._bundle import DEFAULT_REPO_ID, DEFAULT_REVISION, download_bundle, verify_bundle
from .errors import (
    TurnAudioError,
    TurnBundleError,
    TurnDependencyError,
    TurnDetectionError,
    TurnModelDownloadError,
    TurnStateError,
    UnsupportedTurnLanguageError,
)
from ._runtime import TurnPredictor, TurnProbabilities
from ._detector import (
    TurnDecision,
    TurnDecisionReason,
    TurnDetector,
    TurnLanguage,
    TurnSession,
)

__all__ = [
    "DEFAULT_REPO_ID",
    "DEFAULT_REVISION",
    "download_bundle",
    "verify_bundle",
    "TurnAudioError",
    "TurnBundleError",
    "TurnDependencyError",
    "TurnDetectionError",
    "TurnModelDownloadError",
    "TurnStateError",
    "TurnPredictor",
    "TurnProbabilities",
    "TurnDecision",
    "TurnDecisionReason",
    "TurnDetector",
    "TurnLanguage",
    "TurnSession",
    "UnsupportedTurnLanguageError",
]
