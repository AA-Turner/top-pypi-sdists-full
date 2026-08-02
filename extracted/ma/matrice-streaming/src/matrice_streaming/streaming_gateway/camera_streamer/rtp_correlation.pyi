"""Auto-generated stub for module: rtp_correlation."""
from typing import Any, Optional, Tuple

from __future__ import annotations
from collections import OrderedDict
import threading

# Constants
DEFAULT_MAX_ENTRIES: int
GST_CLOCK_TIME_NONE: int

# Functions
def is_valid_pts(pts: Optional[int]) -> bool: ...
    """
    True if ``pts`` can be used as a correlation key.
    
        Rejects ``None``, the GStreamer sentinel, and negatives. A frame without a
        usable PTS is simply not recorded — there is nothing to key it on, and
        guessing is what this module exists to eliminate.
    """

# Classes
class RtpPtsCorrelator:
    """
    Bounded, thread-safe ``PTS -> RTP timestamp`` map for one demuxer session.
    
        Thread-safe because ``record`` runs on the GStreamer streaming thread (inside
        a pad probe) while ``lookup`` runs on the thread driving ``demux()``.
    """

    def __init__(self: Any, max_entries: int = DEFAULT_MAX_ENTRIES) -> None: ...

    def clear(self: Any) -> None: ...
        """
        Drop all pending entries — required on RTSP reconnect.
        
                A new session restarts GStreamer's PTS clock, so a stale key could collide
                with a fresh one and hand a frame the previous session's timestamp.
                Counters are intentionally preserved so the miss rate stays a
                whole-of-life diagnostic across reconnects.
        """

    def lookup(self: Any, pts: Optional[int]) -> int: ...
        """
        Return the true RTP timestamp for ``pts``, or ``0`` if unknown.
        
                Never approximates. ``0`` is the established "no timestamp" signal:
                ``nvdec._compute_gst_timestamp_ns`` treats a non-positive RTP timestamp as
                "no RTP timestamp from the camera", warns rate-limited, and publishes
                ``capture_timestamp_ns=0``. So a miss costs one frame's timestamp and can
                never produce a wrong one.
        
                Consumes the entry on a hit: each appsink sample is pulled exactly once,
                and dropping it keeps the map to genuinely in-flight frames.
        """

    def miss_ratio(self: Any) -> float: ...
        """
        Fraction of lookups that missed, 0.0 when there have been none.
        """

    def pending(self: Any) -> dict: ...
        """
        Snapshot of the in-flight map. Diagnostics/tests only.
        """

    def record(self: Any, pts: Optional[int], rtp_ts: int) -> bool: ...
        """
        Associate a completed frame's PTS with its true RTP timestamp.
        
                Returns True if the entry was stored. A frame with an unusable PTS is
                dropped rather than stored under a placeholder key.
        """

    def stats(self: Any) -> Tuple[int, int]: ...
        """
        ``(hits, misses)``.
        """

