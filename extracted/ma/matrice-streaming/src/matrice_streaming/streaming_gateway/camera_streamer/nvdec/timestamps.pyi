"""Auto-generated stub for module: timestamps."""
from typing import Any, Optional

from __future__ import annotations
import logging
import time

# Constants
RTP_CLOCK_RATE: int
log: Any

# Functions
def compute_ntp_timestamp_ns(ntp_ts: int) -> int: ...
    """
    Convert a 64-bit NTP timestamp (from RTCP SR) to nanoseconds since Unix epoch.
    """
def compute_pts_timestamp_ns(packet_pts: int, first_packet_pts: int, pts_timebase: int, source_fps: float, frames_decoded: int, session_start_ns: int = 0, is_rtsp: bool = False) -> int: ...
    """
    Convert a decoder packet PTS to nanoseconds.
    
        For RTSP streams, adds session_start_ns to produce an absolute wall-clock time.
        For file streams, returns a video-relative timestamp.
    
        Output is clamped to [0, 2^64-1].
    """
def compute_rtp_timestamp_ns(rtp_ts_ns: int, absolute_ns: int = 0, rtp_clock_rate: int = RTP_CLOCK_RATE) -> int: ...
    """
    Validate an RTP-derived nanosecond timestamp for SHM safety.
    
        Priority:
          1. rtp_ts_ns if it is in (0, 2^64-1) — accepted as-is
          2. absolute_ns if it is in (0, 2^64-1) — fallback (RTCP-derived)
          3. 0 — sentinel "no valid timestamp"
    
        The result is always in [0, 2^64-1] so callers can safely call
        struct.pack('<Q', result) without catching struct.error.
    """
def monotonic_ns() -> int: ...
    """
    Current monotonic time in nanoseconds.
    """
