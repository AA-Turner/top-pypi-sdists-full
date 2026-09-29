"""
Advanced tracker module for post-processing operations.

This module provides advanced tracking capabilities similar to BYTETracker from Ultralytics,
with support for various input formats and output formats.
"""

from .base import BaseTrack, TrackState
from .config import TrackerConfig
from .rtp_clock import RTP_CLOCK_HZ, RtpClock
from .tracker import AdvancedTracker

__all__ = [
    "AdvancedTracker",
    "TrackerConfig",
    "BaseTrack",
    "TrackState",
    "RtpClock",
    "RTP_CLOCK_HZ",
]
