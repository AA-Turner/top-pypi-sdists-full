"""Matrice optimization module for frame processing and caching."""

from .frame_optimizer import FrameOptimizer, StreamState
from .result_cache import InferenceResultCache, CachedResult
from .roi_processor import ROIProcessor, ROI, ROIConfig, ROIState

__all__ = [
    "FrameOptimizer",
    "StreamState",
    "InferenceResultCache",
    "CachedResult",
    "ROIProcessor",
    "ROI",
    "ROIConfig",
    "ROIState",
]
