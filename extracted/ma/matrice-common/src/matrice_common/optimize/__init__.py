"""Matrice optimization module for frame processing and caching."""

from .frame_optimizer import FrameOptimizer, StreamState
from .result_cache import CachedResult, InferenceResultCache
from .roi_processor import ROI, ROIConfig, ROIProcessor, ROIState

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
