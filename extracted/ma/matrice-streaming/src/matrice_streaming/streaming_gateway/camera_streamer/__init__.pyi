"""Stub file for streaming_gateway.camera_streamer directory."""
from typing import Any, Dict, Optional, Set, Tuple

from __future__ import annotations
from abc import ABC, abstractmethod
from collections import OrderedDict
from collections import deque
from contextlib import contextmanager
from dataclasses import dataclass, field
from enum import Enum
from matrice_streaming.url_redact import redact_url
from threading import Lock
import cupy as cp
import glob
import logging
import numpy as np
import os
import subprocess
import threading
import time

# Constants
CODEC_H264: str = ...  # From codec_detect
CODEC_H265: str = ...  # From codec_detect
DEFAULT_CODEC: Any = ...  # From codec_detect
logger: Any = ...  # From codec_detect
logger: Any = ...  # From frame_optimizer
DEFAULT_MAX_ENTRIES: int = ...  # From rtp_correlation
GST_CLOCK_TIME_NONE: int = ...  # From rtp_correlation
SHM_DIR: str = ...  # From shm_liveness
logger: Any = ...  # From shm_liveness

# Functions
# From codec_detect
def detect_codec_ffprobe(url: str, timeout: float = 10.0) -> Optional[str]: ...
    """
    Detect video codec of an RTSP stream or file using ffprobe.
    
        Runs ffprobe as a subprocess to query the first video stream's codec_name.
        Returns the canonical codec string ("h264" or "h265") or None on failure.
    
        This is the most reliable detection method but requires:
        - ffprobe installed (part of ffmpeg package)
        - Network access to the RTSP URL
        - ~2-5 seconds for RTSP streams (connection + probe)
    
        Args:
            url: RTSP URL or file path to probe
            timeout: Maximum seconds to wait for ffprobe (default: 10s)
    
        Returns:
            "h264", "h265", or None if detection failed
    """

# From codec_detect
def detect_codec_rtp_payload(payload: Any) -> Optional[str]: ...
    """
    Detect video codec from a raw RTP payload by inspecting NAL unit headers.
    
        Examines the first bytes of an RTP payload to distinguish H.264 from H.265
        based on the NAL unit type encoding:
    
        - H.264: NAL type is bits [4:0] of byte 0 (5 bits, range 1-23 for single NAL)
        - H.265: NAL type is bits [6:1] of byte 0 (6 bits), and byte 1 has layer_id + tid
    
        Heuristic: H.265 NAL units have the forbidden_zero_bit=0 (bit 7 of byte 0)
        AND the temporal_id in byte 1 bits [2:0] must be >= 1 (never 0 in valid H.265).
        H.264 NAL units don't have this byte 1 constraint.
    
        Args:
            payload: Raw RTP payload bytes (after removing 12-byte RTP header)
    
        Returns:
            "h264", "h265", or None if payload is too short or ambiguous
    """

# From codec_detect
def normalize_codec(codec: Optional[str]) -> str: ...
    """
    Normalize a codec string to canonical form ("h264" or "h265").
    
        Handles case-insensitive matching and common aliases (HEVC, AVC, H.264, etc.).
        Returns DEFAULT_CODEC ("h264") for None, empty, or unrecognized values.
    
        Args:
            codec: Codec string in any case/format, or None
    
        Returns:
            "h264" or "h265"
    """

# From frame_optimizer
def build_frame_optimizer(config: Optional[Dict[str, Any]] = None) -> Any: ...
    """
    Construct a :class:`FrameOptimizer` from a config dict.
    
        Returns :class:`NoOpFrameOptimizer` by default. Set ``config["optimizer"]`` to
        select a skip policy; unknown names log a warning and fall back to no-op.
    """

# From rtp_correlation
def is_valid_pts(pts: Optional[int]) -> bool: ...
    """
    True if ``pts`` can be used as a correlation key.
    
        Rejects ``None``, the GStreamer sentinel, and negatives. A frame without a
        usable PTS is simply not recorded — there is nothing to key it on, and
        guessing is what this module exists to eliminate.
    """

# From shm_liveness
def camera_has_live_shm(camera_id: str, held: Optional[Set[str]] = None) -> bool: ...
    """
    True if any live process holds a databus segment for ``camera_id`` open.
    
        Fails open (returns True) when the scan is unavailable, so an unreadable
        ``/proc`` can never license deleting a segment a producer is writing.
    """

# From shm_liveness
def camera_shm_prefixes(camera_id: str) -> tuple: ...
    """
    The ``/dev/shm`` name prefixes owned by ``camera_id``.
    
        Mirrors the patterns the worker managers clean:
        ``databus__<cam>__*`` (ring buffers, e.g. ``__sg__frames``) and
        ``databus_status__<cam>`` (the status segment, which has no trailing ``__``).
    """

# From shm_liveness
def held_shm_paths() -> Optional[Set[str]]: ...
    """
    Return every ``/dev/shm`` path currently held open by any live process.
    
        Returns ``None`` when the scan could not be performed, which callers must
        treat as "unknown — assume everything is live" (fail open). An empty set is a
        positive result meaning "scanned successfully, nothing is held".
    """

# From shm_liveness
def is_shm_path_live(path: str, held: Optional[Set[str]] = None) -> bool: ...
    """
    True if ``path`` is held open by a live process, or if that is unknown.
    
        Pass ``held`` from a single :func:`held_shm_paths` call when checking many
        paths, so the ``/proc`` walk happens once instead of per path.
    """

# Classes
# From databus_backpressure
class BackpressurePolicy(Enum):
    BLOCK: str
    DROP_OLDEST: str
    DROP_TO_KEYFRAME: str

    pass

# From databus_backpressure
class BackpressurePublisher:
    """
    Wraps ``DataBusProducer.publish`` with lag-aware backpressure.
    """

    def __init__(self: Any, producer: Any, camera_id: str, maxsize: Optional[int] = None, policy: Optional[BackpressurePolicy] = None) -> None: ...

    def depth(self: Any) -> int: ...

    def is_full(self: Any) -> bool: ...

    def publish(self: Any, data: Any, metadata: Optional[Dict] = None) -> bool: ...


# From databus_backpressure
class QueueMetrics:
    def drop_rate(self: Any) -> float: ...

    def p99_depth(self: Any) -> float: ...


# From frame_optimizer
class FrameOptimizer(ABC):
    """
    Decide, per camera, whether a decoded frame should be published.
    
        Implementations are stateful per ``camera_id`` (the same instance is shared
        across all cameras a worker owns). Subclass this to add a skip policy.
    """

    def optimize(self: Any, camera_id: str, frame: Any) -> Optional[Any]: ...
        """
        Return the frame to publish, or ``None`` to drop it.
        """

    def reset(self: Any, camera_id: str) -> None: ...
        """
        Drop per-camera state (called on stream reconnect/remove). Default no-op.
        """


# From frame_optimizer
class MotionFrameOptimizer(FrameOptimizer):
    """
    GPU motion gate for NVDEC NV12 frames using downsampled Y-plane SSIM.
    
        Compares each frame to the last *published* reference for ``camera_id``. Frames
        whose motion score ``1 - SSIM`` falls below ``threshold`` are dropped. The metric
        runs entirely on-GPU (downsampled luma thumbnails only); non-CuPy frames (OpenCV
        BGR) pass through unchanged.
    """

    def __init__(self: Any, threshold: float = 0.02, thumb_height: int = 64, thumb_width: int = 64) -> None: ...

    def optimize(self: Any, camera_id: str, frame: Any) -> Optional[Any]: ...

    def reset(self: Any, camera_id: str) -> None: ...


# From frame_optimizer
class NoOpFrameOptimizer(FrameOptimizer):
    """
    Default optimizer: never drops a frame — every frame passes through.
    """

    def optimize(self: Any, camera_id: str, frame: Any) -> Optional[Any]: ...


# From frame_pool
class GatewayFramePool:
    """
    Per-shape ring of reusable frame buffers.
    
        Eliminates per-frame ``np.empty`` / ``np.full`` allocation on the hot path.
    """

    def __init__(self: Any, resolution: Tuple[int, ...], pool_size: int = 4, dtype: Any = np.uint8) -> None: ...

    def free_count(self: Any) -> int: ...

    def lease(self: Any) -> Any: ...
        """
        Yield a buffer from the pool; return it on context exit.
        """


# From frame_pool
class PoolExhaustedError(RuntimeError):
    """
    Raised when no buffer is free in the pool.
    """

    pass

# From rtp_correlation
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


from . import codec_detect, databus_backpressure, frame_optimizer, frame_pool, rtp_correlation, shm_liveness