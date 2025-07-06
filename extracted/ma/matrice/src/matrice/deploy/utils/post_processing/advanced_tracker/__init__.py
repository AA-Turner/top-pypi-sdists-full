"""
Advanced tracker module for post-processing operations.

This module provides advanced tracking capabilities similar to BYTETracker from Ultralytics,
with support for various input formats and output formats.
"""

from .tracker import AdvancedTracker
from .config import TrackerConfig
from .base import BaseTrack, TrackState

__all__ = [
    "AdvancedTracker",
    "TrackerConfig", 
    "BaseTrack",
    "TrackState"
] 