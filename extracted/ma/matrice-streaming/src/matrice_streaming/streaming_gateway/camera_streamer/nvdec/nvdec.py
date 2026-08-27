#!/usr/bin/env python3
"""Streaming Gateway - CUDA IPC Video Producer (NVDEC Hardware Decode).

This module implements the producer side of the zero-copy video pipeline
using NVDEC hardware video decoding for maximum throughput.

Architecture:
=============

    ┌─────────────────────────────────────────────────────────────────────────┐
    │                    STREAMING GATEWAY (Producer)                         │
    ├─────────────────────────────────────────────────────────────────────────┤
    │                                                                         │
    │   ┌─────────────────────────────────────────────────────────────────┐   │
    │   │                   NVDEC Decoder Pool                            │   │
    │   │                                                                 │   │
    │   │  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐     │   │
    │   │  │  Decoder 0     │  │  Decoder 1     │  │  Decoder N     │     │   │
    │   │  │                │  │                │  │                │     │   │
    │   │  │   NVDEC HW     │  │   NVDEC HW     │  │   NVDEC HW     │     │   │
    │   │  │   decode       │  │   decode       │  │   decode       │     │   │
    │   │  │       ↓        │  │       ↓        │  │       ↓        │     │   │
    │   │  │  NV12 Resize   │  │  NV12 Resize   │  │  NV12 Resize   │     │   │
    │   │  │       ↓        │  │       ↓        │  │       ↓        │     │   │
    │   │  │   CUDA IPC     │  │   CUDA IPC     │  │   CUDA IPC     │     │   │
    │   │  │   Ring Buf     │  │   Ring Buf     │  │   Ring Buf     │     │   │
    │   │  │  (NV12 0.6MB)  │  │  (NV12 0.6MB)  │  (NV12 0.6MB)     │     │   │
    │   │  └────────────────┘  └────────────────┘  └────────────────┘     │   │
    │   │                                                                 │   │
    │   └─────────────────────────────────────────────────────────────────┘   │
    │                               │                                         │
    │                    Output: NV12 (H*1.5, W) uint8 = 0.6 MB               │
    │                    50% less IPC bandwidth than RGB                      │
    │                               ↓                                         │
    └───────────────────────────────┼─────────────────────────────────────────┘
                                    │
                         Consumer reads via CUDA IPC
                         → NV12→RGB→CHW→FP16 in one kernel
                         → TensorRT inference

Usage:
======
    python streaming_gateway.py --video videoplayback.mp4 --num-streams 100

Requirements:
=============
    - PyNvVideoCodec for NVDEC hardware decode
    - CuPy with CUDA support
    - cuda_shm_ring_buffer module
"""

from __future__ import annotations

# SCALE-002 RC: resource_tracker semaphore-unlink race fix. Must run BEFORE
# any mp.Queue/Lock is touched. Shared implementation in matrice_streaming._mp_patch.
from matrice_streaming._mp_patch import install_resource_tracker_patch as _matrice_install_rt_patch

_matrice_install_rt_patch()

import argparse
import faulthandler
import glob
import hashlib
import logging
import math
import multiprocessing as mp
import os
import queue as thread_queue
import signal
import tempfile
import threading
import time
import uuid
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Callable, ClassVar, Dict, Generator, List, Optional, Set, Tuple
from urllib.parse import urlparse, urlunparse

import numpy as np

from matrice_streaming.secure_cache import is_safe_cached_file, secure_cache_dir
from matrice_streaming.url_redact import redact_url

# resolve_restart_policy is the single reader of all six MATRICE_SG_* restart /
# stall knobs; the local _env_float/_env_int helpers it replaced are gone.
from .restart_policy import StreamSupervisor, resolve_restart_policy


class _AnyStop:
    """Duck-typed stop flag that is set when ANY of its events is set.

    Lets the decode worker honour both a per-sub SIGTERM (graceful per-camera
    removal / terminate) and the shared orchestrator stop event (full shutdown)
    through the single ``stop_event`` it polls. Only ``is_set()`` is required by
    the worker loop; ``set()`` is provided for completeness.
    """

    def __init__(self, *events: Any) -> None:
        self._events = [e for e in events if e is not None]

    def is_set(self) -> bool:
        return any(e.is_set() for e in self._events)

    def set(self) -> None:  # pragma: no cover - convenience only
        for e in self._events:
            try:
                e.set()
            except Exception:  # nosec B110
                pass


def _unlink_camera_shm(camera_id: str) -> int:
    """Unlink a camera's own DataBus SHM segments (best-effort, idempotent).

    Called from the decode sub-process on teardown so a removed/terminated
    camera does not leave an orphan ``/dev/shm/databus__<cam>__*`` that keeps
    consumers reading stale frames and fools the phantom reconciler (which keys
    on the file's existence). Mirrors the path patterns cleaned by
    ``NVDECWorkerManager._clean_stale_shm_for``. Returns the count removed.
    """
    if not camera_id:
        return 0
    removed = 0
    patterns = [  # nosec B108 - SHM cleanup is intentional
        f"/dev/shm/databus__{camera_id}__*",  # nosec B108
        f"/dev/shm/databus_status__{camera_id}",  # nosec B108
    ]
    for pattern in patterns:
        for path in glob.glob(pattern):
            try:
                os.remove(path)
                removed += 1
            except OSError:
                pass
    return removed


# How often the per-GPU command handler emits a "handler_alive" heartbeat so the
# manager/watchdog can detect a wedged handler (process alive, frames advancing,
# but no commands being consumed). The manager's staleness threshold is a
# multiple of this.
_HANDLER_HEARTBEAT_SEC = 5.0


class DemuxerType(Enum):
    """Demuxer backend selection.

    NVC: PyNvVideoCodec demuxer - fastest for local files
    GSTREAMER: GStreamer demuxer - provides ABSOLUTE RTP timestamps for RTSP
    """

    NVC = "nvc"
    GSTREAMER = "gstreamer"


# Import BenchmarkMetrics for granular timing (lives in py_common for universal access)
try:
    from matrice_common.utils import BenchmarkMetrics
except Exception:
    BenchmarkMetrics = None


try:
    import requests

    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

try:
    import cupy as cp

    CUPY_AVAILABLE = True
except ImportError:
    CUPY_AVAILABLE = False
    cp = None

try:
    import PyNvVideoCodec as nvc

    PYNVCODEC_AVAILABLE = True
except ImportError:
    PYNVCODEC_AVAILABLE = False
    nvc = None

try:
    from matrice_common.stream.cuda_shm_ring_buffer import (
        CudaIpcRingBuffer,
        GlobalFrameCounter,
    )

    RING_BUFFER_AVAILABLE = True
except (ImportError, AttributeError, RuntimeError, TypeError):
    # ImportError: module not found
    # AttributeError: cp.ndarray is None (cupy not available)
    # RuntimeError/TypeError: other initialization errors
    RING_BUFFER_AVAILABLE = False
    CudaIpcRingBuffer = None
    GlobalFrameCounter = None

# GpuCameraMap removed: the inference engine reads the producer GPU from the
# ring-buffer header (consumer_auto), so the SG neither publishes nor needs a
# cam->GPU map. Each camera's decode GPU is config.gpu_id.
GPU_CAMERA_MAP_AVAILABLE = False

try:
    from matrice_common.stream import DataBus
    from matrice_common.stream.databus import DataBusProducer

    DATABUS_AVAILABLE = True
except ImportError:
    DATABUS_AVAILABLE = False
    DataBus = None
    DataBusProducer = None

# CRITICAL: PyNvVideoCodec bundles FFmpeg 6.x, OpenCV bundles FFmpeg 5.x, and
# GStreamer's gst-libav uses system FFmpeg 4.4. Loading all three in the same process
# causes SIGABRT/SIGSEGV when rtspsrc connects. The import-order approach is NOT sufficient
# because the package __init__.py imports OpenCV (via CameraStreamer), loading FFmpeg 5.x
# before GStreamer's rtspsrc needs to load its plugins.
#
# Solution: GStreamerSubprocessDemuxer runs GStreamer in a separate subprocess that never
# imports PyNvVideoCodec or OpenCV, avoiding the FFmpeg symbol conflict entirely.
# H264 bytes + RTP timestamps are streamed through a pipe to the parent process.
GSTREAMER_DEMUXER_AVAILABLE = False
GstRTPDemuxer = None
try:
    from .gstreamer_subprocess_demuxer import (
        GStreamerSubprocessDemuxer as GstRTPDemuxer,
    )

    GSTREAMER_DEMUXER_AVAILABLE = True
except ImportError:
    try:
        from gstreamer_subprocess_demuxer import (
            GStreamerSubprocessDemuxer as GstRTPDemuxer,
        )

        GSTREAMER_DEMUXER_AVAILABLE = True
    except ImportError:
        pass

logger = logging.getLogger(__name__)

# Largest value packable as a little-endian unsigned 64-bit int (struct "<Q").
# Capture timestamps are packed this way into the CUDA shm ring buffer; anything
# >= this is an invalid/sentinel value (e.g. GST_CLOCK_TIME_NONE-derived) and
# must be rejected before packing.
_UINT64_MAX = (1 << 64) - 1

# RTP media clock for H.264/H.265 video, in ticks per second (RFC 3551 §6). Named
# rather than spelled 90000 inline because it appears on both sides of the surface-PTS
# conversion below, and a mismatch there is a silent timestamp scaling error.
RTP_CLOCK_RATE = 90_000

# =============================================================================
# Orin Platform Fallback (opt-in via MATRICE_PLATFORM=orin)
# =============================================================================
_IS_ORIN = os.environ.get("MATRICE_PLATFORM", "").lower() == "orin"
ORIN_NVDEC_AVAILABLE = False

if _IS_ORIN:
    try:
        from .orin_nvdec import OrinNVDECDecoderPool

        ORIN_NVDEC_AVAILABLE = True
        logger.info("MATRICE_PLATFORM=orin: OrinNVDECDecoderPool available")
    except ImportError:
        try:
            from orin_nvdec import OrinNVDECDecoderPool  # type: ignore[no-redef]

            ORIN_NVDEC_AVAILABLE = True
            logger.info("MATRICE_PLATFORM=orin: OrinNVDECDecoderPool available (direct import)")
        except ImportError:
            logger.warning("MATRICE_PLATFORM=orin but OrinNVDECDecoderPool import failed")

# =============================================================================
# Default dimensions for NV12 output
# Per-camera dimensions come from StreamConfig.width/height
# =============================================================================
DEFAULT_FRAME_WIDTH = 0  # 0 = native camera resolution (no SG-side resize, let inference handle preprocess)
DEFAULT_FRAME_HEIGHT = 0  # 0 = native camera resolution
DEFAULT_SOURCE_FPS = 30.0  # When demuxer/RTSP reports 0 or invalid FPS


def _normalize_reported_fps(fps: float) -> float:
    """Clamp reported FPS so timestamp and FPS-limit math never divide by zero."""
    try:
        x = float(fps)
    except (TypeError, ValueError):
        return DEFAULT_SOURCE_FPS
    if x <= 0 or math.isnan(x):  # NaN
        return DEFAULT_SOURCE_FPS
    return x


def _get_h264_nal_type(nal_bytes: bytes, codec: str = "h264") -> int:
    """Extract NAL unit type from H.264/H.265 packet. Returns -1 if invalid.

    Handles both formats:
    - Annex B: starts with 0x00 0x00 0x01 or 0x00 0x00 0x00 0x01
    - Raw NAL: first byte is the NAL header directly (GStreamer output)
    """
    if len(nal_bytes) < 1:
        return -1
    # Find start code or treat as raw NAL
    if len(nal_bytes) >= 4 and nal_bytes[:4] == b"\x00\x00\x00\x01":
        hdr_idx = 4
    elif len(nal_bytes) >= 3 and nal_bytes[:3] == b"\x00\x00\x01":
        hdr_idx = 3
    else:
        hdr_idx = 0  # Raw NAL — no start code (GStreamer format)
    if hdr_idx >= len(nal_bytes):
        return -1
    hdr = nal_bytes[hdr_idx]
    if codec == "h265":
        return (hdr >> 1) & 0x3F
    if hdr & 0x80:  # forbidden_zero_bit must be 0
        return -1
    return hdr & 0x1F


def _validate_h264_nal(nal_bytes: bytes, codec: str = "h264") -> bool:
    """Fast validation of H.264/H.265 NAL unit to prevent NVDEC segfault."""
    if len(nal_bytes) < 2:
        return False
    nal_type = _get_h264_nal_type(nal_bytes, codec)
    if nal_type < 0:
        return False
    if codec == "h265":
        return nal_type <= 47
    return 1 <= nal_type <= 12 or 24 <= nal_type <= 31


def _is_idr_or_sps(nal_bytes: bytes, codec: str = "h264") -> bool:
    """Check if NAL is an IDR keyframe or SPS — safe decoder entry points."""
    nal_type = _get_h264_nal_type(nal_bytes, codec)
    if codec == "h265":
        return nal_type in (
            16,
            17,
            18,
            19,
            20,
            21,
            32,
            33,
            34,
        )  # IDR/BLA/CRA + VPS/SPS/PPS
    return nal_type in (5, 7, 8)  # IDR, SPS, PPS


def create_decoder_pool(pool_size: int, gpu_id: int = 0, demuxer_type: str = "nvc", codec: str = "h264"):
    """Create the appropriate decoder pool for the current platform.

    On Orin (MATRICE_PLATFORM=orin), returns OrinNVDECDecoderPool (gst-launch-1.0).
    On desktop/Thor, returns NVDECDecoderPool (PyNvVideoCodec CUVID).
    """
    if ORIN_NVDEC_AVAILABLE:
        return OrinNVDECDecoderPool(pool_size, gpu_id, demuxer_type, codec)
    return NVDECDecoderPool(pool_size, gpu_id, demuxer_type, codec)


def setup_logging(quiet: bool = True):
    """Configure logging level based on quiet mode."""
    level = logging.WARNING if quiet else logging.INFO
    logging.basicConfig(level=level, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    logging.getLogger("cuda_shm_ring_buffer").setLevel(logging.WARNING if quiet else logging.INFO)


# =============================================================================
# Video Downloader for HTTPS URLs (PyNvVideoCodec's FFmpeg lacks HTTPS support)
# =============================================================================


class VideoDownloader:
    """Downloads and caches video files from HTTPS URLs.

    PyNvVideoCodec uses a bundled FFmpeg that doesn't have HTTPS support.
    This class downloads HTTPS videos to local files before passing them
    to the NVDEC demuxer.

    Features:
    - URL deduplication: same video URL (ignoring query params) is only downloaded once
    - Disk caching: reuses existing files across runs
    - Progress tracking for large files
    - Dynamic timeout based on file size
    """

    # Configuration
    DOWNLOAD_TIMEOUT: ClassVar[int] = 300  # Base timeout in seconds
    DOWNLOAD_TIMEOUT_PER_100MB: ClassVar[int] = 300  # Additional seconds per 100MB
    MAX_DOWNLOAD_TIMEOUT: ClassVar[int] = 6000  # 100 minutes max
    DOWNLOAD_CHUNK_SIZE: ClassVar[int] = 8192

    # Singleton instance for process-wide caching
    _instance: ClassVar[Optional["VideoDownloader"]] = None
    _lock: ClassVar[threading.Lock] = threading.Lock()

    def __new__(cls):
        """Singleton pattern for process-wide cache sharing."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False  # type: ignore[has-type]
        return cls._instance

    def __init__(self):
        """Initialize the video downloader."""
        if self._initialized:  # type: ignore[has-type]
            return

        self._initialized = True
        self.downloaded_files: Dict[str, str] = {}
        self._normalized_url_to_path: Dict[str, str] = {}
        self._download_lock = threading.Lock()
        # Per-user 0700 cache dir (not a world-shared fixed path) so a local
        # attacker cannot pre-create the dir or pre-seed cache files we trust.
        self.temp_dir = secure_cache_dir("nvdec_video_cache")
        logger.info(f"VideoDownloader initialized, cache dir: {self.temp_dir}")

    def prepare_source(self, video_path: str, camera_id: str) -> str:
        """Prepare video source, downloading HTTPS URLs if needed.

        Args:
            video_path: Video file path, RTSP URL, or HTTPS URL
            camera_id: Camera identifier for logging

        Returns:
            Local file path (downloaded if HTTPS) or original path
        """
        if not self._is_https_url(video_path):
            return video_path

        if not REQUESTS_AVAILABLE:
            logger.warning(f"requests module not available, cannot download HTTPS URL for {camera_id}")
            return video_path

        local_path = self._download_video(video_path, camera_id)
        if local_path:
            return local_path

        logger.warning(f"Failed to download {redact_url(video_path)} for {camera_id}, will try URL directly (may fail)")
        return video_path

    def _is_https_url(self, source: str) -> bool:
        """Check if source is an HTTPS URL."""
        return source.startswith("https://")

    def _normalize_url(self, url: str) -> str:
        """Normalize URL by stripping query parameters for deduplication."""
        parsed = urlparse(url)
        return urlunparse(
            (
                parsed.scheme,
                parsed.netloc,
                parsed.path,
                "",
                "",
                "",  # params, query, fragment
            )
        )

    def _get_url_hash(self, normalized_url: str) -> str:
        """Generate a short hash for consistent file naming."""
        # A cache filename, not a security digest; usedforsecurity=False is set.
        # nosemgrep: hashlib-md5-or-sha1
        return hashlib.md5(normalized_url.encode(), usedforsecurity=False).hexdigest()[:12]

    def _download_video(self, url: str, camera_id: str) -> Optional[str]:
        """Download video file from HTTPS URL with caching.

        Thread-safe: uses lock to prevent duplicate downloads.

        Args:
            url: HTTPS video URL
            camera_id: Camera identifier for logging

        Returns:
            Local file path or None if download failed
        """
        normalized_url = self._normalize_url(url)
        file_ext = Path(url.split("?")[0]).suffix or ".mp4"
        url_hash = self._get_url_hash(normalized_url)
        expected_path = self.temp_dir / f"video_{url_hash}{file_ext}"
        expected_path_str = str(expected_path)

        # Quick check: file already on disk — only reuse if it is a regular
        # file owned by us (not a symlink / pre-seeded file from another user).
        if expected_path.exists():
            if not is_safe_cached_file(expected_path):
                logger.warning(
                    f"[{camera_id}] Ignoring untrusted cache file "
                    f"(wrong owner or symlink): {expected_path}; will re-download"
                )
                try:
                    os.unlink(expected_path)
                except OSError:
                    return None
            else:
                existing_size = expected_path.stat().st_size
                logger.info(
                    f"[{camera_id}] Reusing cached video: {expected_path.name} ({existing_size / (1024 * 1024):.1f}MB)"
                )
                with self._download_lock:
                    self.downloaded_files[url] = expected_path_str
                    self._normalized_url_to_path[normalized_url] = expected_path_str
                return expected_path_str

        # Check memory cache
        with self._download_lock:
            if url in self.downloaded_files:
                local_path = self.downloaded_files[url]
                if os.path.exists(local_path):
                    logger.debug(f"[{camera_id}] Using cached path (exact URL match)")
                    return local_path

            if normalized_url in self._normalized_url_to_path:
                local_path = self._normalized_url_to_path[normalized_url]
                if os.path.exists(local_path):
                    logger.info(f"[{camera_id}] Reusing download (same base URL)")
                    self.downloaded_files[url] = local_path
                    return local_path

        # Need to download - acquire lock to prevent duplicate downloads
        with self._download_lock:
            # Double-check after acquiring lock — same trusted-file gate as above.
            if expected_path.exists() and is_safe_cached_file(expected_path):
                self.downloaded_files[url] = expected_path_str
                self._normalized_url_to_path[normalized_url] = expected_path_str
                return expected_path_str

            return self._do_download(url, expected_path, camera_id)

    def _probe_content_length(self, url: str, camera_id: str) -> Tuple[int, float, int]:
        """HEAD request to get content length and compute dynamic timeout.

        Returns:
            (content_length, file_size_mb, timeout)
        """
        content_length = 0
        file_size_mb = 0.0
        timeout = self.DOWNLOAD_TIMEOUT
        try:
            head_response = requests.head(url, timeout=10, allow_redirects=True)
            content_length = int(head_response.headers.get("Content-Length", 0))
            file_size_mb = content_length / (1024 * 1024)
        except Exception as e:
            logger.debug(f"[{camera_id}] HEAD request failed: {e}")

        if content_length > 0:
            timeout = min(
                self.DOWNLOAD_TIMEOUT + int(file_size_mb // 100) * self.DOWNLOAD_TIMEOUT_PER_100MB,
                self.MAX_DOWNLOAD_TIMEOUT,
            )
            logger.info(f"[{camera_id}] Downloading {file_size_mb:.1f}MB (timeout: {timeout}s)")
        else:
            logger.info(f"[{camera_id}] Downloading video (size unknown, timeout: {timeout}s)")
        return content_length, file_size_mb, timeout

    def _do_download(self, url: str, dest_path: Path, camera_id: str) -> Optional[str]:
        """Perform the actual download. Must be called with _download_lock held."""
        bytes_downloaded = 0

        try:
            content_length, file_size_mb, timeout = self._probe_content_length(url, camera_id)

            # Download with progress tracking. Use the streamed Response as a
            # context manager so the pooled HTTP connection is released on every
            # path (success and error) — previously it was never closed, leaking
            # a connection per download.
            with requests.get(url, stream=True, timeout=timeout) as response:
                response.raise_for_status()

                if content_length == 0:
                    content_length = int(response.headers.get("Content-Length", 0))
                    file_size_mb = content_length / (1024 * 1024) if content_length > 0 else 0

                last_progress_log = 0

                # Write to a private temp file in the same (0700) dir, then
                # atomically rename into place so an existing/symlinked path at
                # dest_path can't be trusted or clobbered mid-download.
                tmp_fd, tmp_name = tempfile.mkstemp(dir=str(self.temp_dir), prefix="dl_", suffix=dest_path.suffix)
                try:
                    with os.fdopen(tmp_fd, "wb") as f:
                        for chunk in response.iter_content(chunk_size=self.DOWNLOAD_CHUNK_SIZE):
                            f.write(chunk)
                            bytes_downloaded += len(chunk)

                            # Log progress every 50MB for large files
                            if content_length > 50_000_000:
                                mb_downloaded = bytes_downloaded // (1024 * 1024)
                                if mb_downloaded - last_progress_log >= 50:
                                    progress = (bytes_downloaded / content_length * 100) if content_length else 0
                                    logger.info(
                                        f"[{camera_id}] Download progress: "
                                        f"{mb_downloaded}MB / {file_size_mb:.0f}MB ({progress:.1f}%)"
                                    )
                                    last_progress_log = mb_downloaded
                    os.replace(tmp_name, dest_path)
                except BaseException:
                    try:
                        os.unlink(tmp_name)
                    except OSError:
                        pass
                    raise

            # Update caches
            normalized_url = self._normalize_url(url)
            dest_path_str = str(dest_path)
            self.downloaded_files[url] = dest_path_str
            self._normalized_url_to_path[normalized_url] = dest_path_str

            logger.info(f"[{camera_id}] Downloaded: {dest_path.name} ({bytes_downloaded / (1024 * 1024):.1f}MB)")
            return dest_path_str

        except requests.Timeout:
            logger.error(
                f"[{camera_id}] Download timeout: {file_size_mb:.1f}MB, "
                f"got {bytes_downloaded / (1024 * 1024):.1f}MB in {timeout}s"
            )
        except requests.HTTPError as e:
            logger.exception(f"[{camera_id}] HTTP error: {e.response.status_code} - {e.response.reason}")
        except IOError as e:
            logger.exception(f"[{camera_id}] Disk I/O error: {e}")
        except Exception as e:
            logger.exception(f"[{camera_id}] Download failed: {type(e).__name__}: {e}")

        # Cleanup partial download
        try:
            if dest_path.exists():
                dest_path.unlink()
        except Exception:  # nosec B110
            pass

        return None

    def cleanup(self):
        """Clean up downloaded temporary files."""
        unique_files = set(self.downloaded_files.values())
        unique_files.update(self._normalized_url_to_path.values())

        for filepath in unique_files:
            try:
                if os.path.exists(filepath):
                    os.remove(filepath)
                    logger.debug(f"Removed temp file: {filepath}")
            except Exception as e:
                logger.warning(f"Failed to remove temp file {filepath}: {e}")

        self.downloaded_files.clear()
        self._normalized_url_to_path.clear()


# Global video downloader instance
_video_downloader: Optional[VideoDownloader] = None


def get_video_downloader() -> VideoDownloader:
    """Get or create the global VideoDownloader instance."""
    global _video_downloader
    if _video_downloader is None:
        _video_downloader = VideoDownloader()
    return _video_downloader


@dataclass
class StreamConfig:
    """Configuration for a single video stream."""

    camera_id: str
    video_path: str
    # 0 = native (SG writes camera-native NV12; the inference path / Ultralytics
    # owns preprocess so prod matches local `YOLO(...).predict(image)` behavior).
    width: int = 0
    height: int = 0
    target_fps: int = 10
    gpu_id: int = 0
    stream_type: str = "file"  # "file" or "rtsp"
    _last_rtp_warn: float = 0.0  # throttle for missing-RTP warnings
    demuxer_type: str = "nvc"  # "nvc" or "gstreamer"
    # NOTE: Default codec is h264 — matches the majority of deployed RTSP cameras.
    # Most cameras (Hikvision, Dahua, Axis) use H.264 on primary stream by default.
    # Use detect_codec_ffprobe() from codec_detect.py to auto-detect per-camera codec.
    codec: str = "h264"  # "h264" or "h265"

    def __post_init__(self):
        """Auto-detect stream_type/demuxer_type and normalize codec."""
        # Normalize codec: handle upper/lower case, aliases (HEVC, AVC, H.264, etc.)
        from ..codec_detect import normalize_codec

        self.codec = normalize_codec(self.codec)

        if self.video_path.startswith(("rtsp://", "rtsps://")):
            self.stream_type = "rtsp"
            # Auto-switch to GStreamer for RTSP if available (for ABSOLUTE RTP timestamps)
            if GSTREAMER_DEMUXER_AVAILABLE and self.demuxer_type == "nvc":
                self.demuxer_type = "gstreamer"
        elif self.video_path.split("://", 1)[0] in ("http", "https"):
            self.stream_type = "file"  # Downloaded files
        else:
            self.stream_type = "file"


class _SubprocessCameraRegistry:
    """Track camera ownership for NVDEC GPU subprocesses.

    A boot-time subprocess can own multiple cameras, so removing/updating one
    camera requires detaching the whole owner and respawning unaffected siblings.
    """

    def __init__(self) -> None:
        self._camera_to_sub: Dict[str, Any] = {}
        self._camera_to_config: Dict[str, StreamConfig] = {}
        self._sub_to_cameras: Dict[Any, Set[str]] = {}

    def register(self, owner: Any, configs: List[StreamConfig]) -> None:
        camera_ids = {cfg.camera_id for cfg in configs}
        for cfg in configs:
            previous_owner = self._camera_to_sub.get(cfg.camera_id)
            if previous_owner is not None:
                self._sub_to_cameras.get(previous_owner, set()).discard(cfg.camera_id)
            self._camera_to_sub[cfg.camera_id] = owner
            self._camera_to_config[cfg.camera_id] = cfg
        self._sub_to_cameras[owner] = camera_ids

    def owner_for(self, camera_id: str) -> Optional[Any]:
        return self._camera_to_sub.get(camera_id)

    def active_camera_count(self) -> int:
        """Live count of cameras currently configured on this GPU.

        Used by the progress monitor so per-camera FPS figures track cameras
        hot-added/removed after spawn, instead of the stale spawn-time count.
        """
        return len(self._camera_to_config)

    def config_for(self, camera_id: str) -> Optional[StreamConfig]:
        return self._camera_to_config.get(camera_id)

    def configs_for_owner(self, owner: Any) -> List[StreamConfig]:
        """Every still-configured camera owned by ``owner``.

        Read-only counterpart to :meth:`detach_owner_for_camera`, for the case
        where the owner is already dead and there is nothing to detach — the
        caller only needs to know which cameras went down with it.
        """
        configs = []
        for cid in self._sub_to_cameras.get(owner, set()):
            cfg = self._camera_to_config.get(cid)
            if cfg is not None:
                configs.append(cfg)
        return configs

    def remove_config(self, camera_id: str) -> None:
        self._camera_to_config.pop(camera_id, None)

    def detach_owner_for_camera(self, camera_id: str) -> Tuple[Optional[Any], Dict[str, StreamConfig]]:
        owner = self._camera_to_sub.get(camera_id)
        if owner is None:
            return None, {}

        camera_ids = set(self._sub_to_cameras.pop(owner, set()))
        if not camera_ids:
            camera_ids = {cid for cid, candidate in self._camera_to_sub.items() if candidate is owner}

        owned_configs: Dict[str, StreamConfig] = {}
        for cid in camera_ids:
            self._camera_to_sub.pop(cid, None)
            cfg = self._camera_to_config.get(cid)
            if cfg is not None:
                owned_configs[cid] = cfg
        return owner, owned_configs


def _terminate_subprocess_owner(
    owner: Any,
    logger: Optional[logging.Logger],
    process_id: int,
    cam_id: str,
    terminate_timeout: float = 5.0,
    kill_timeout: float = 3.0,
) -> bool:
    """Terminate a subprocess owner and escalate to kill if it stays alive."""
    try:
        owner.terminate()
        owner.join(timeout=terminate_timeout)
        is_alive = getattr(owner, "is_alive", None)
        if callable(is_alive) and is_alive():
            kill = getattr(owner, "kill", None)
            if callable(kill):
                kill()
                owner.join(timeout=kill_timeout)
    except Exception as e:
        if logger is not None:
            logger.warning(f"Process {process_id}: error terminating sub for camera {cam_id}: {e}")
        return False

    is_alive = getattr(owner, "is_alive", None)
    return not (callable(is_alive) and is_alive())


def _compute_dynamic_burst_size(num_streams: int) -> int:
    """Tiered burst size based on per-decoder stream count.

    FPS limiter (see nvdec_pool_worker) is active for num_streams<=50, and
    committed_idx is published once per decode_round. Smaller burst means
    smoother consumer visibility while the limiter is active; above 50 the
    limiter is off and burst amortizes per-round GPU sync.
    """
    if num_streams <= 10:
        return 1
    if num_streams <= 50:
        return 2
    return 4


def _should_write_frame(
    last_write_ns: Dict[str, int],
    camera_id: str,
    timestamp_ns: int,
    min_interval_ns: int,
    monotonic_ns: Optional[int] = None,
    min_monotonic_interval_ns: Optional[int] = None,
) -> bool:
    """Temporal output-decimation decision for the ring-buffer publish step.

    Caps per-camera publish rate to ~1e9/min_interval_ns FPS, independent of
    camera resolution or how many streams share the decoder. Decode is NOT
    affected — every frame is still decoded for GOP/reference integrity; this
    only gates what gets written downstream.

    Two gates compose (both must pass to write):

    1. **Decode-timestamp gate** (``timestamp_ns`` / ``min_interval_ns``): the
       original PTS/RTP-derived check. ``min_interval_ns <= 0`` disables it.
       A timestamp going backwards (stream restart / new RTP session) is treated
       as a first frame (write + implicit reset).
    2. **Monotonic wall-clock floor** (``monotonic_ns`` /
       ``min_monotonic_interval_ns``): an OPTIONAL hard ceiling. ``monotonic_ns``
       comes from ``time.monotonic_ns()`` so it can never go backwards or alias —
       unlike RTP/PTS it cannot be tricked by RTP wrap, session restarts, or PTS
       aliasing. When both monotonic params are supplied, the gate ALSO requires
       ``(monotonic_ns - prev_mono) >= min_monotonic_interval_ns``.

    The monotonic floor is tracked under a per-camera ``f"{camera_id}:mono"``
    key inside the same ``last_write_ns`` dict to avoid an extra parameter.

    - The first frame for a camera always writes (under both gates).
    - When the monotonic params are omitted (4-arg legacy callers), behaviour is
      identical to the original timestamp-only gate (backward compatible).

    The caller records the accepted timestamp (``last_write_ns[camera_id] = ts``)
    and, when using the monotonic floor, the accepted monotonic time
    (``last_write_ns[f"{camera_id}:mono"] = monotonic_ns``) only when this
    returns True.
    """
    mono_enabled = monotonic_ns is not None and min_monotonic_interval_ns is not None and min_monotonic_interval_ns > 0

    # Gate 1: decode-timestamp (legacy) decision.
    ts_pass = True
    if min_interval_ns > 0:
        prev = last_write_ns.get(camera_id)
        if prev is None:
            ts_pass = True  # first frame
        elif timestamp_ns < prev:  # restart / clock reset
            ts_pass = True
        else:
            ts_pass = (timestamp_ns - prev) >= min_interval_ns

    # Gate 2: monotonic wall-clock floor (hard ceiling, reset-proof).
    mono_pass = True
    if mono_enabled:
        prev_mono = last_write_ns.get(f"{camera_id}:mono")
        if prev_mono is None:
            mono_pass = True  # first frame
        else:
            mono_pass = (monotonic_ns - prev_mono) >= min_monotonic_interval_ns

    return ts_pass and mono_pass


# Float slack so a ratio that sums to a hair under an integer (e.g. 3*(1/3)) still
# crosses the publish threshold on the expected frame.
_ACC_EPS = 1e-9


def _should_publish_frame(
    acc_state: Dict[str, float],
    camera_id: str,
    source_fps: float,
    target_fps: float,
) -> bool:
    """Phase-accumulator publish decimation: keep ``target_fps`` out of ``source_fps``.

    Returns True to publish this decoded frame, False to drop it. The decision is
    frame-count based (a fractional accumulator), NOT wall-clock or RTP/PTS based,
    so the published rate is a stable ``target_fps`` average for ANY source rate
    and is immune to session/RTP resets — unlike a time-interval gate, it never
    jitters between adjacent skip factors on a boundary (e.g. 30->10 is always
    every 3rd frame, 25->10 averages exactly 10 via a 2,3,2,3 pattern).

    Pass-through (returns True for every frame) when:
      * ``target_fps <= 0`` — cap disabled (mirrors MATRICE_OUTPUT_FPS=0), or
      * ``source_fps <= 0`` — unknown source rate, fail open, or
      * ``source_fps <= target_fps`` — cannot upsample a slow source.

    Per-camera accumulator is stored under ``acc_state[camera_id]`` and updated
    only here. Seeded so the first frame for a camera always publishes while
    keeping the long-run average exact.
    """
    if target_fps <= 0 or source_fps <= 0 or source_fps <= target_fps:
        return True

    ratio = target_fps / source_fps  # 0 < ratio < 1: fraction of frames to keep
    acc = acc_state.get(camera_id)
    if acc is None:
        acc = 1.0 - ratio  # so the first frame crosses the threshold immediately
    acc += ratio
    if acc >= 1.0 - _ACC_EPS:
        acc_state[camera_id] = acc - 1.0
        return True
    acc_state[camera_id] = acc
    return False


def _maybe_publish_session_info(
    rb,
    camera_id: str,
    session_id: str,
    session_start_ns: int,
    published_session: Dict[str, str],
) -> bool:
    """Write the RTSP session id into the ring-buffer header ONLY when it changed.

    The session id changes at producer creation and on every RTSP/demuxer
    (re)connect — never per frame. Consumers read it solely to detect an SG
    restart, so writing on change is behaviourally identical to the old
    per-frame write while avoiding ~one mmap write+flush per published frame
    (≈10k/s at 1000 cams × 10 fps).

    Returns True if it published (caller need not act on the return; it's there
    for testability).
    """
    if not session_id or published_session.get(camera_id) == session_id:
        return False
    rb.set_session_info(session_id, session_start_ns)
    published_session[camera_id] = session_id
    return True


# Default per-camera publish (output) cap, in FPS. This is the single knob for
# the cap's default; ``MATRICE_OUTPUT_FPS`` overrides it per deployment (set 0
# to disable). Kept separate from the decode pacer's ``target_fps``.
DEFAULT_OUTPUT_FPS_CAP = 10.0

# The relaxed monotonic flood-guard ceiling is this multiple of the target FPS.
# Above the target so it never rejects on-cadence publishes from the primary
# phase-accumulator decimator; only catches a flood from a mis-detected source.
_OUTPUT_FPS_SAFETY_FACTOR = 1.5


def _resolve_output_interval_ns(default_fps: float = DEFAULT_OUTPUT_FPS_CAP) -> int:
    """Resolve the per-camera output (publish) cap interval in nanoseconds.

    The cap is ON by default at ``DEFAULT_OUTPUT_FPS_CAP`` fps. Reads
    ``MATRICE_OUTPUT_FPS`` as a per-deployment override: a positive value sets a
    different rate, ``0`` (or negative) disables the cap. A missing or malformed
    value falls back to ``default_fps``. Returns 0 when the cap is disabled,
    otherwise ``int(1e9 / fps)``. Emits a WARNING when the cap is active so
    operators are not surprised by silent frame loss. This is the publish cap
    and is intentionally separate from the decode pacer's ``target_fps``.
    """
    raw = os.environ.get("MATRICE_OUTPUT_FPS")
    fps = default_fps
    if raw is not None and raw.strip() != "":
        try:
            fps = float(raw)
        except ValueError:
            fps = default_fps
    if fps <= 0:
        return 0
    logger.warning(
        "Output FPS cap active: %.1f fps — frames exceeding this rate will be "
        "silently dropped. Set MATRICE_OUTPUT_FPS=0 or unset it to disable the cap.",
        fps,
    )
    return int(1e9 / fps)


@dataclass
class GatewayConfig:
    """Configuration for the streaming gateway."""

    video_path: str
    num_streams: int = 100
    target_fps: int = 0  # 0 = unlimited, >0 = FPS limit per stream
    # 0 = native camera resolution; inference owns preprocess (Ultralytics handles letterbox).
    frame_width: int = 0
    frame_height: int = 0
    gpu_id: int = 0
    num_gpus: int = 1
    duration_sec: float = 30.0
    nvdec_pool_size: int = 8
    nvdec_burst_size: int = 4
    num_slots: int = 64
    demuxer_type: str = "nvc"  # "nvc" or "gstreamer"
    benchmark_mode: bool = False  # Enable granular per-stage timing (forces GPU sync, reduces throughput)
    # Frame-skip policy passed to the per-worker optimizer (see camera_streamer/
    # frame_optimizer.py). None = no-op default (publish every frame, subject to
    # the MATRICE_OUTPUT_FPS cap).
    optimizer_config: Optional[Dict[str, Any]] = None


@dataclass
class StreamState:
    """Track state for each logical stream in NVDEC pool."""

    stream_id: int
    camera_id: str
    video_path: str
    demuxer: Any  # NVC demuxer (None if using GStreamer)
    frames_decoded: int = 0
    # 0 = native camera resolution; inference owns preprocess.
    width: int = 0
    height: int = 0
    # The source's OWN resolution, as the demuxer reported it at open. 0 = the
    # demuxer supplied none.
    #
    # Recorded because the ring buffer has to be sized at what the decoder will
    # actually produce, which is min(declared, native) — the decoder clamps a
    # target larger than native down to native and never upsamples. Sizing the
    # ring at the DECLARED value instead meant a stale `customStreamSettings`
    # (1920x1080 against a 1280x720 camera) failed the ring's shape check on
    # every frame and the camera sat at 0 fps until an operator corrected the
    # config by hand. This is knowable at open and used to be logged and then
    # discarded.
    native_width: int = 0
    native_height: int = 0
    empty_packets: int = 0
    decode_errors: int = 0  # Consecutive decode errors
    _empty_start_ns: float = 0.0  # time.monotonic() when current empty-streak started; for wall-clock stall check
    _last_rtp_warn: float = 0.0  # time.time() of last missing-RTP warning (read by _compute_gst_timestamp_ns)
    _last_restart_time: float = 0.0  # time.monotonic() of last real demuxer restart; restart-cooldown anchor
    # NVDEC "Decode Error occurred for picture N" is non-fatal and self-heals at
    # the next IDR; restarting the demuxer here loses several seconds per cycle.
    # Default high; tune down via env MATRICE_SG_MAX_DECODE_ERRORS for strict mode.
    MAX_DECODE_ERRORS: int = int(os.environ.get("MATRICE_SG_MAX_DECODE_ERRORS", "1000"))
    stream_type: str = "file"  # "file" or "rtsp"
    source_fps: float = 30.0  # Source video FPS for timestamp calculation
    demuxer_type: str = "nvc"  # "nvc" or "gstreamer"
    # T0+PTS timestamp tracking for RTSP sync (Mode B)
    session_start_ns: int = 0  # Wall clock (ns) when RTSP connected (T0)
    session_id: str = ""  # Unique 8-char session ID (changes on reconnect)
    # NVDEC PTS tracking - use actual packet PTS instead of frame count calculation
    pts_timebase: int = 0  # Calculated from FPS * packet.duration (e.g., 30000 for 29.97fps)
    first_packet_pts: int = 0  # First PTS in stream (for relative time calculation)
    # GStreamer demuxer fields (for ABSOLUTE RTP timestamps)
    gst_demuxer: Any = None  # GstRTPDemuxer instance
    gst_demux_gen: Optional[Generator] = None  # demux() generator
    last_rtp_timestamp: Optional[int] = None  # Most recent 32-bit RTP timestamp
    first_rtp_timestamp: Optional[int] = None  # First RTP timestamp of session
    awaiting_idr: bool = True  # Skip non-IDR NALs until first keyframe (prevents NVDEC segfault on cold decoder)


# =============================================================================
# CUDA Kernel: NV12 Resize (no color conversion - 50% less bandwidth)
# =============================================================================

_NV12_RESIZE_SOURCE = r"""
// Bilinear NV12 letterbox resize.
// Aspect-ratio preserving fit with gray (Y=114, UV=128) padding, matching
// ultralytics LetterBox preprocessing. Bilinear on both Y and chroma planes
// for training-matched interpolation. Pixel-center sampling: target index i
// maps to source coord (i + 0.5) * src/new - 0.5, identical to OpenCV
// INTER_LINEAR / Pillow BILINEAR.
extern "C" __global__ void nv12_resize(
    const unsigned char* src_y,
    const unsigned char* src_uv,
    unsigned char* dst,
    int src_h, int src_w,
    int dst_h, int dst_w,
    int y_stride, int uv_stride
) {
    int dst_x = blockIdx.x * blockDim.x + threadIdx.x;
    int dst_y = blockIdx.y * blockDim.y + threadIdx.y;

    // Total height in output: dst_h (Y) + dst_h/2 (UV) = dst_h * 1.5
    int total_h = dst_h + dst_h / 2;
    if (dst_x >= dst_w || dst_y >= total_h) return;

    // Letterbox: aspect-ratio preserving resize + gray padding
    float r_h = (float)dst_h / (float)src_h;
    float r_w = (float)dst_w / (float)src_w;
    float r   = fminf(r_h, r_w);

    int new_h = (int)roundf((float)src_h * r);
    int new_w = (int)roundf((float)src_w * r);

    float dh = (float)(dst_h - new_h) * 0.5f;
    float dw = (float)(dst_w - new_w) * 0.5f;
    int pad_top  = (int)roundf(dh - 0.1f);
    int pad_left = (int)roundf(dw - 0.1f);

    if (dst_y < dst_h) {
        // ---------------- Y plane (full resolution) ----------------
        int img_y = dst_y - pad_top;
        int img_x = dst_x - pad_left;
        int dst_idx = dst_y * dst_w + dst_x;

        if (img_y < 0 || img_y >= new_h || img_x < 0 || img_x >= new_w) {
            dst[dst_idx] = 114;  // gray padding
            return;
        }

        // Bilinear: target pixel center -> source coord
        float sx = ((float)img_x + 0.5f) * (float)src_w / (float)new_w - 0.5f;
        float sy = ((float)img_y + 0.5f) * (float)src_h / (float)new_h - 0.5f;

        int x0 = (int)floorf(sx);
        int y0 = (int)floorf(sy);
        float fx = sx - (float)x0;
        float fy = sy - (float)y0;
        int x1 = x0 + 1;
        int y1 = y0 + 1;
        // Clamp source coords to valid range - matches cv2.resize edge behaviour.
        x0 = max(0, min(src_w - 1, x0));
        x1 = max(0, min(src_w - 1, x1));
        y0 = max(0, min(src_h - 1, y0));
        y1 = max(0, min(src_h - 1, y1));

        float v00 = (float)src_y[y0 * y_stride + x0];
        float v01 = (float)src_y[y0 * y_stride + x1];
        float v10 = (float)src_y[y1 * y_stride + x0];
        float v11 = (float)src_y[y1 * y_stride + x1];
        float top = v00 + (v01 - v00) * fx;
        float bot = v10 + (v11 - v10) * fx;
        float val = top + (bot - top) * fy;
        dst[dst_idx] = (unsigned char)__float2uint_rn(fmaxf(0.0f, fminf(255.0f, val)));
    } else {
        // ---------------- UV plane (4:2:0 interleaved) ----------------
        // Output NV12 UV row: U,V,U,V,... at half vertical resolution.
        // dst_x parity selects channel (0=U, 1=V). Within a chroma "cell"
        // (two adjacent output bytes) U and V share the same fractional
        // source coordinate, so we resolve channel late.
        int uv_dst_y = dst_y - dst_h;  // 0 .. dst_h/2 - 1
        int dst_idx = dst_h * dst_w + uv_dst_y * dst_w + dst_x;

        int uv_pad_top = pad_top / 2;
        int uv_new_h   = new_h / 2;
        // Horizontal padding lives in pixel (Y) space and is even-aligned
        // for the standard 16:9 -> NxN letterbox case (pad_left == 0).
        int img_uv_y = uv_dst_y - uv_pad_top;
        int img_x    = dst_x - pad_left;

        if (img_uv_y < 0 || img_uv_y >= uv_new_h || img_x < 0 || img_x >= new_w) {
            dst[dst_idx] = 128;  // neutral chroma for gray padding
            return;
        }

        // Convert to chroma (half) space. img_x is a Y-pixel column; the
        // chroma column it belongs to is img_x >> 1. Adjacent dst_x (U and V
        // for the same cell) round down to the same chroma column.
        float chroma_target_x = (float)(img_x >> 1);
        float chroma_target_y = (float)img_uv_y;

        float src_chroma_w = (float)(src_w >> 1);
        float new_chroma_w = (float)(new_w >> 1);
        float src_chroma_h = (float)(src_h >> 1);
        float new_chroma_h = (float)(new_h >> 1);

        float sx = (chroma_target_x + 0.5f) * src_chroma_w / new_chroma_w - 0.5f;
        float sy = (chroma_target_y + 0.5f) * src_chroma_h / new_chroma_h - 0.5f;

        int cx0 = (int)floorf(sx);
        int cy0 = (int)floorf(sy);
        float fx = sx - (float)cx0;
        float fy = sy - (float)cy0;
        int cx1 = cx0 + 1;
        int cy1 = cy0 + 1;
        int max_cx = (src_w >> 1) - 1;
        int max_cy = (src_h >> 1) - 1;
        cx0 = max(0, min(max_cx, cx0));
        cx1 = max(0, min(max_cx, cx1));
        cy0 = max(0, min(max_cy, cy0));
        cy1 = max(0, min(max_cy, cy1));

        int ch = dst_x & 1;  // 0=U, 1=V - preserves NV12 interleave
        float v00 = (float)src_uv[cy0 * uv_stride + cx0 * 2 + ch];
        float v01 = (float)src_uv[cy0 * uv_stride + cx1 * 2 + ch];
        float v10 = (float)src_uv[cy1 * uv_stride + cx0 * 2 + ch];
        float v11 = (float)src_uv[cy1 * uv_stride + cx1 * 2 + ch];
        float top = v00 + (v01 - v00) * fx;
        float bot = v10 + (v11 - v10) * fx;
        float val = top + (bot - top) * fy;
        dst[dst_idx] = (unsigned char)__float2uint_rn(fmaxf(0.0f, fminf(255.0f, val)));
    }
}
"""


def _compile_nv12_resize_kernel():
    """Compile the NV12 resize CUDA kernel via NVRTC.

    Called once at module import time (single-threaded) to avoid NVRTC
    compilation races when multiple decoder threads start simultaneously.
    The compiled PTX is cached by CuPy in ~/.cupy/kernel_cache/.
    """
    if not CUPY_AVAILABLE:
        return None
    return cp.RawKernel(_NV12_RESIZE_SOURCE, "nv12_resize")


# Pre-compile at import time — single-threaded, before any worker thread starts.
# With mp.get_context("spawn"), each GPU worker re-imports this module, compiling
# the kernel once per process without thread contention.
_nv12_resize_kernel = None

# Capability flag: flipped to False the first time write_frame_fast rejects the
# src_w/src_h kwargs (i.e. running against an older matrice_common). Starts True
# so the fast path is used whenever the installed SDK supports it.
_SUPPORTS_SRC_DIMS = True


def _disable_src_dims_support() -> None:
    """Flip the src_w/src_h capability flag off (older matrice_common).

    Wraps the module-global write so worker code does not reach into
    ``globals()`` directly. Only ever transitions True -> False, so a benign
    race between workers (all writing the same value) is harmless.
    """
    global _SUPPORTS_SRC_DIMS
    _SUPPORTS_SRC_DIMS = False


# Whether this PyNvVideoCodec build lets us carry a per-picture timestamp THROUGH the
# decoder (`PacketData.pts` in, surface timestamp out).
#
# Why this matters: NVDEC is created without `latency=`, so it defaults to NATIVE and
# holds ~2 pictures in its display queue. The decode loop feeds an access unit and then
# iterates the surfaces `Decode()` emits -- but those are EARLIER pictures. Stamping the
# fed-in AU's RTP timestamp onto them labels every frame ~2 source frames ahead of the
# picture it actually contains. Nothing errors: the value is a valid on-grid timestamp,
# so the recorder resolves it to a real stored frame, just the wrong one. That is the
# LPR overlay/alert desync.
#
# Carrying the timestamp through the decoder makes each surface self-describing, which
# is what `orin_nvdec.py` already does on the Jetson path via its PTS->RTP map.
#
# Starts True and flips off permanently the first time the API does not cooperate, so a
# build without `pts`/surface timestamps degrades to the previous behaviour instead of
# raising in the decode path of every camera. `MATRICE_NVDEC_SURFACE_PTS=0` forces the
# old path without a redeploy.
_SUPPORTS_SURFACE_PTS = os.getenv("MATRICE_NVDEC_SURFACE_PTS", "1").strip().lower() not in (
    "0",
    "false",
    "no",
)


def _disable_surface_pts_support(reason: str) -> None:
    """Flip the surface-PTS capability flag off, once, with a reason.

    Same shape as :func:`_disable_src_dims_support`: only ever True -> False, so
    concurrent workers writing the same value is harmless.
    """
    global _SUPPORTS_SURFACE_PTS
    if _SUPPORTS_SURFACE_PTS:
        _SUPPORTS_SURFACE_PTS = False
        logger.warning(
            "[NVDEC] per-picture timestamps unavailable (%s); falling back to stamping "
            "the fed-in access unit's RTP timestamp. Published capture_timestamp_ns will "
            "lead the picture by the decoder's display-queue depth (~2 frames).",
            reason,
        )


def _surface_rtp_timestamp(surface: Any) -> Optional[int]:
    """The RTP timestamp NVDEC carried through for THIS surface, or None.

    The decode loop sets ``PacketData.pts`` to the access unit's true RTP timestamp, so
    whatever comes back out is the emitted picture's own value rather than the one
    currently being fed in. Attribute name varies across PyNvVideoCodec builds, hence the
    probing; None means "could not read it" and the caller keeps the old behaviour.
    """
    for attr in ("timestamp", "pts"):
        value = getattr(surface, attr, None)
        if isinstance(value, int) and value > 0:
            return value
    getter = getattr(surface, "getPTS", None)
    if callable(getter):
        try:
            value = getter()
        except Exception:  # nosec B110 - a probe must never break the decode loop
            return None
        if isinstance(value, int) and value > 0:
            return value
    return None


try:
    _nv12_resize_kernel = _compile_nv12_resize_kernel()
except Exception:  # nosec B110
    pass  # Will retry lazily in _get_nv12_resize_kernel()


def _get_nv12_resize_kernel():
    """Get the pre-compiled NV12 resize kernel, or compile on demand."""
    global _nv12_resize_kernel
    if _nv12_resize_kernel is None and CUPY_AVAILABLE:
        _nv12_resize_kernel = _compile_nv12_resize_kernel()
    return _nv12_resize_kernel


# INVARIANT: one decode worker per process. `_get_nv12_output` returns the SAME
# scratch buffer for every camera that shares a (total_h, dst_w) shape, so it is
# only safe because `_sub_decode_process` runs `nvdec_pool_worker` single-threaded
# per process. The lock below guards the dict, not the buffer contents — do NOT
# call the resize/pack path from multiple threads in one process without keying
# the scratch by thread id.
_NV12_OUTPUT_SCRATCH: Dict[Tuple[int, int], "cp.ndarray"] = {}
_NV12_SCRATCH_LOCK = threading.Lock()


def _get_nv12_output(total_h: int, dst_w: int):
    """Reuse pre-allocated NV12 resize output buffers (N-2, one scratch per shape).

    See the module-level invariant above: the returned buffer is shared across
    all cameras of the same shape and is only safe under the one-worker-thread-
    per-process model.
    """
    if not CUPY_AVAILABLE:
        return None
    key = (total_h, dst_w)
    with _NV12_SCRATCH_LOCK:
        buf = _NV12_OUTPUT_SCRATCH.get(key)
        if buf is None or buf.shape != (total_h, dst_w):
            buf = cp.empty((total_h, dst_w), dtype=cp.uint8)
            _NV12_OUTPUT_SCRATCH[key] = buf
        return buf


def _pack_nv12_native(
    y_plane: "cp.ndarray",
    uv_plane: "cp.ndarray",
    src_h: int,
    src_w: int,
) -> Optional["cp.ndarray"]:
    """Pack NV12 when target == source and strides are tight (REFACTORING_PLAN §20).

    Skips the NV12 resize kernel when no geometry or stride normalization is needed.
    """
    total_h = src_h + src_h // 2
    output = _get_nv12_output(total_h, src_w)
    if output is None:
        return None
    uv_rows = src_h // 2
    output[:src_h, :src_w] = y_plane[:src_h, :src_w]
    output[src_h : src_h + uv_rows, :src_w] = uv_plane[:uv_rows, :src_w]
    return output


def nv12_resize(
    y_plane: cp.ndarray,
    uv_plane: cp.ndarray,
    y_stride: int,
    uv_stride: int,
    src_h: int,
    src_w: int,
    dst_h: int = 0,
    dst_w: int = 0,
) -> cp.ndarray:
    """Resize NV12 without color conversion.

    Output: concatenated Y (H*W) + UV ((H/2)*W) as single buffer.
    Total size: H*W + (H/2)*W = H*W*1.5 bytes (50% of RGB).
    """
    kernel = _get_nv12_resize_kernel()
    if kernel is None:
        return None

    total_h = dst_h + dst_h // 2
    output = _get_nv12_output(total_h, dst_w)
    if output is None:
        return None

    block = (16, 16)
    grid = ((dst_w + 15) // 16, (total_h + 15) // 16)

    kernel(
        grid,
        block,
        (
            y_plane,
            uv_plane,
            output,
            cp.int32(src_h),
            cp.int32(src_w),
            cp.int32(dst_h),
            cp.int32(dst_w),
            cp.int32(y_stride),
            cp.int32(uv_stride),
        ),
    )

    return output


# F08: throttle for per-(src,target) resize warnings — these conditions are a
# static property of a camera's native size vs its configured target, so they
# would otherwise log on every frame.
_RESIZE_WARNED: set = set()


def _warn_resize_fallback(src_w: int, src_h: int, target_w: int, target_h: int, err: Exception) -> None:
    """Warn once per geometry that a resize failed and the frame is being dropped.

    The fallback packs the surface at native size "so one camera's resize error never
    drops its stream" — but the ring is sized for the RESIZED geometry, so a
    native-sized tensor fails its shape check and is dropped anyway. The old wording
    implied the frame had been published. It says what actually happens now: the
    passthrough keeps the stream alive for the frames that do resize, not for this one.
    """
    sig = ("err", src_w, src_h, target_w, target_h)
    if sig in _RESIZE_WARNED:
        return
    _RESIZE_WARNED.add(sig)
    logger.warning(
        "[F08] NV12 resize %dx%d->%dx%d failed (%s); falling back to native passthrough at "
        "%dx%d. NOTE: this camera's ring is sized for the resized geometry, so a native-sized "
        "frame will fail the ring's shape check and be DROPPED — the passthrough keeps the "
        "stream alive for the frames that do resize, it does not publish this one.",
        src_w,
        src_h,
        target_w,
        target_h,
        err,
        src_w,
        src_h,
    )


def surface_to_nv12_with_src_dims(frame, target_h: int = 0, target_w: int = 0) -> Tuple[Optional[cp.ndarray], int, int]:
    """Convert NVDEC surface to NV12 and return the pre-resize source dims.

    Same output format as :func:`surface_to_nv12` but also returns the
    ORIGINAL (pre-resize) source dimensions read off the NVDEC surface.
    Consumers (inference) need these to invert the letterbox geometry so
    bounding boxes in model-input space map back to source pixel space.

    Returns:
        (tensor, src_w, src_h) where tensor is the NV12 frame (or None on
        failure) and (src_w, src_h) are the native camera resolution.
        (None, 0, 0) on any failure path.
    """
    if not CUPY_AVAILABLE or frame is None:
        return None, 0, 0

    try:
        cuda_views = frame.cuda()
        if not cuda_views or len(cuda_views) < 2:
            return None, 0, 0

        # Extract Y plane
        y_view = cuda_views[0]
        y_cai = y_view.__cuda_array_interface__
        y_shape = tuple(y_cai["shape"])
        y_strides = tuple(y_cai["strides"])
        y_ptr = y_cai["data"][0]
        src_h, src_w = y_shape[:2]
        y_stride = y_strides[0]

        y_size = src_h * y_stride
        y_mem = cp.cuda.UnownedMemory(y_ptr, y_size, owner=frame)
        y_memptr = cp.cuda.MemoryPointer(y_mem, 0)
        y_plane = cp.ndarray((src_h, src_w), dtype=cp.uint8, memptr=y_memptr, strides=(y_stride, 1))

        # Extract UV plane
        uv_view = cuda_views[1]
        uv_cai = uv_view.__cuda_array_interface__
        uv_shape = tuple(uv_cai["shape"])
        uv_strides = tuple(uv_cai["strides"])
        uv_ptr = uv_cai["data"][0]
        uv_stride = uv_strides[0]

        uv_h = uv_shape[0]
        # The NV12 chroma plane's byte-width always equals the luma byte-width
        # (src_w): each row holds W/2 interleaved CbCr pairs == W bytes. Do NOT
        # trust uv_shape[1] — depending on the decoder/geometry the surface may
        # report the UV plane as interleaved pairs (H/2, W/2, 2), making
        # uv_shape[1] == W/2. Building the byte view at W/2 then under-counts the
        # width by 2x and the downstream pack/resize broadcast fails (e.g.
        # (160, 288) vs (160, 576) on a 576x320 source), dropping every frame.
        uv_w = src_w
        uv_size = uv_h * uv_stride
        uv_mem = cp.cuda.UnownedMemory(uv_ptr, uv_size, owner=frame)
        uv_memptr = cp.cuda.MemoryPointer(uv_mem, 0)
        uv_plane = cp.ndarray((uv_h, uv_w), dtype=cp.uint8, memptr=uv_memptr, strides=(uv_stride, 1))

        # Use native resolution when target <= 0
        if target_h <= 0:
            target_h = src_h
        if target_w <= 0:
            target_w = src_w

        # F08: never upsample — clamp a target larger than native down to native
        # (the SG floor is max(min_resolution) clamped to the camera capability).
        if target_h > src_h or target_w > src_w:
            _sig = (src_w, src_h, target_w, target_h)
            if _sig not in _RESIZE_WARNED:
                _RESIZE_WARNED.add(_sig)
                logger.warning(
                    "[F08] target %dx%d exceeds native %dx%d; clamping to native (no upsample)",
                    target_w,
                    target_h,
                    src_w,
                    src_h,
                )
            target_h, target_w = min(target_h, src_h), min(target_w, src_w)

        # REFACTORING_PLAN §20: skip resize kernel on native path when strides are tight
        if target_h == src_h and target_w == src_w and y_stride == src_w and uv_stride == src_w:
            nv12_frame = _pack_nv12_native(y_plane, uv_plane, src_h, src_w)
        else:
            # F08: enable the per-camera resize when target < native. On any
            # kernel failure fall back to native passthrough for THIS frame so
            # one camera's resize error never drops its stream (others unaffected).
            try:
                nv12_frame = nv12_resize(y_plane, uv_plane, y_stride, uv_stride, src_h, src_w, target_h, target_w)
            except Exception as resize_err:
                _warn_resize_fallback(src_w, src_h, target_w, target_h, resize_err)
                nv12_frame = _pack_nv12_native(y_plane, uv_plane, src_h, src_w)
        # Synchronize to ensure resize kernel finishes reading from NVDEC surface
        # before next Decode() call can overwrite it (kernel runs on worker stream,
        # Decode uses stream 0 - they can overlap without this sync)
        # cp.cuda.get_current_stream().synchronize()
        # TODO: synchronize() is slower, benchmark both before enabling this
        # Add channel dimension for ring buffer compatibility: (H*1.5, W) -> (H*1.5, W, 1)
        tensor = nv12_frame[:, :, cp.newaxis] if nv12_frame is not None else None
        return tensor, src_w, src_h

    except Exception as e:
        # Safely handle any characters in error message (CUDA errors may contain Unicode like ×)
        try:
            err_msg = str(e).encode("ascii", errors="replace").decode("ascii")
        except Exception:
            try:
                err_msg = repr(str(e))[:200]
            except Exception:
                err_msg = "failed to format error message"
        logger.warning(f"surface_to_nv12 failed: {err_msg}")
        return None, 0, 0


def surface_to_nv12(frame, target_h: int = 0, target_w: int = 0) -> Optional[cp.ndarray]:
    """Convert NVDEC surface to NV12, optionally resized.

    Output: (H + H/2, W, 1) uint8 - concatenated Y + UV planes with channel dim.
    Total size: H*W*1.5 bytes (vs H*W*3 for RGB).

    When target_h/target_w <= 0, uses the native camera resolution (no resize).

    Callers that need the pre-resize source dims should use
    :func:`surface_to_nv12_with_src_dims` instead.
    """
    tensor, _src_w, _src_h = surface_to_nv12_with_src_dims(frame, target_h, target_w)
    return tensor


# =============================================================================
# NVDEC Decoder Pool
# =============================================================================


class NVDECDecoderPool:
    """Pool of NVDEC decoders that time-multiplex streams.

    Each decoder is exclusively owned by one worker thread.
    Outputs NV12: 1.5*H*W bytes (50% smaller than RGB).

    Supports two demuxer backends:
    - NVC (default): PyNvVideoCodec demuxer, fastest for local files
    - GStreamer: Provides ABSOLUTE RTP timestamps for RTSP streams

    KNOWN ISSUE — Resolution Mismatch Crash (SIGABRT):
        NVDEC decoders are created with an implicit max resolution based on the
        first stream they decode. If a camera with a HIGHER resolution than the
        initial streams is later assigned to the same GPU (e.g., a 1280x720 camera
        mixed with 640x360 cameras), PyNvVideoCodec's C++ layer calls
        ReconfigureDecoder which fails with:
            "Error code 801: Reconfigure Not supported when width/height >
             maxwidth/maxheight" (NvDecoder.cpp:462)
        This triggers SIGABRT, killing the entire GPU worker process and all
        cameras on that GPU.

        Root cause: nvc.CreateDecoder() does not accept maxWidth/maxHeight params
        in the current PyNvVideoCodec version. The decoder auto-sizes to the first
        stream's resolution.

    TODO: Fix resolution mismatch by either:
        1. Creating decoders with max expected resolution (e.g., 1920x1080) by
           decoding a dummy frame of that size during initialization
        2. Catching the reconfigure error and recreating the decoder with the
           new resolution (requires decoder-level try/except around Decode())
        3. Grouping cameras by resolution into separate decoder pools
        4. Validating camera resolution against decoder max before assign_stream()
           and rejecting mismatched cameras with a clear error message
    """

    # Codec enum mapping for PyNvVideoCodec
    _CODEC_MAP = {
        "h264": "H264",
        "h265": "HEVC",
        "hevc": "HEVC",
    }

    def __init__(
        self,
        pool_size: int,
        gpu_id: int = 0,
        demuxer_type: str = "nvc",
        codec: str = "h264",
    ):
        from ..codec_detect import normalize_codec

        self.pool_size = pool_size
        self.gpu_id = gpu_id
        self.codec = normalize_codec(codec)
        self.demuxer_type = DemuxerType(demuxer_type)
        self.decoders = []
        self.streams_per_decoder: List[List[StreamState]] = [[] for _ in range(pool_size)]
        self._streams_lock = threading.Lock()  # Protects streams_per_decoder mutations

        # All six operator knobs (MATRICE_SG_RESTART_COOLDOWN / _GIVEUP_COOLDOWN /
        # _MAX_RESTARTS / _RESTART_WINDOW / _STALL_SEC / _BOOTSTRAP_SEC) are
        # resolved here, once, by the single reader in restart_policy. The decode
        # loops read stall_sec/bootstrap_sec off this policy instead of re-parsing
        # os.environ per packet. Resolving once (not per iteration) is deliberate:
        # the values are deployment tuning, not something a running worker retunes.
        self.restart_policy = resolve_restart_policy()
        # Restart policy: cooldown-aware, give-up-capable supervisor shared by
        # every camera on this pool. A permanently-dead source (RTSP "Not
        # found") stops flooding ERROR-level tracebacks — after a burst of
        # failed restarts it enters a quiet slow-probe state (still recovers if
        # the source returns).
        self.stream_supervisor = StreamSupervisor.from_policy(
            self.restart_policy,
            on_give_up=self._on_restart_give_up,
        )

        if not PYNVCODEC_AVAILABLE:
            raise RuntimeError("PyNvVideoCodec not available")

        if CUPY_AVAILABLE:
            cp.cuda.Device(gpu_id).use()

        # Resolve codec enum (self.codec is already normalized to "h264" or "h265")
        codec_name = self._CODEC_MAP.get(self.codec, "H264")
        nvc_codec = getattr(nvc.cudaVideoCodec, codec_name, nvc.cudaVideoCodec.H264)

        for i in range(pool_size):
            try:
                decoder = nvc.CreateDecoder(gpuid=gpu_id, codec=nvc_codec, usedevicememory=True)
                self.decoders.append(decoder)
            except Exception as e:
                logger.warning(f"Failed to create {codec} decoder {i}: {e}")
                break

        self.actual_pool_size = len(self.decoders)
        logger.info(
            f"Created NVDEC pool: {self.actual_pool_size}/{pool_size} {codec} decoders on GPU {gpu_id}, demuxer={demuxer_type}"
        )

    def assign_stream(
        self,
        stream_id: int,
        camera_id: str,
        video_path: str,
        width: int = 0,
        height: int = 0,
        stream_type: str = "file",
        demuxer_type: str = None,
        codec: str = None,
    ) -> bool:
        """Assign a stream to a decoder (round-robin).

        Supports two demuxer backends:
        - NVC: PyNvVideoCodec demuxer (fastest for files)
        - GStreamer: Provides ABSOLUTE RTP timestamps for RTSP

        Args:
            stream_id: Stream identifier
            camera_id: Camera identifier
            video_path: Video file path or RTSP URL
            width: Target width
            height: Target height
            stream_type: Source type ("file" or "rtsp")
            demuxer_type: Override demuxer type ("nvc" or "gstreamer"), uses pool default if None
            codec: Video codec ("h264" or "h265"), uses pool codec if None
        """
        if self.actual_pool_size == 0:
            return False

        decoder_idx = stream_id % self.actual_pool_size
        use_codec = codec or self.codec

        # Use specified demuxer type or pool default
        use_demuxer_type = DemuxerType(demuxer_type) if demuxer_type else self.demuxer_type

        if use_demuxer_type == DemuxerType.GSTREAMER:
            # Use GStreamer demuxer for ABSOLUTE RTP timestamps
            return self._assign_stream_gstreamer(
                decoder_idx,
                stream_id,
                camera_id,
                video_path,
                width,
                height,
                stream_type,
                use_codec,
            )
        # Use NVC demuxer (default, fastest for files)
        return self._assign_stream_nvc(
            decoder_idx,
            stream_id,
            camera_id,
            video_path,
            width,
            height,
            stream_type,
        )

    def _assign_stream_nvc(
        self,
        decoder_idx: int,
        stream_id: int,
        camera_id: str,
        video_path: str,
        width: int,
        height: int,
        stream_type: str,
    ) -> bool:
        """Assign stream using NVC (PyNvVideoCodec) demuxer."""
        # Download HTTPS URLs to local files (PyNvVideoCodec lacks HTTPS support)
        downloader = get_video_downloader()
        local_path = downloader.prepare_source(video_path, camera_id)

        try:
            demuxer = nvc.CreateDemuxer(local_path)
        except Exception as e:
            logger.exception(f"Failed to create NVC demuxer for {camera_id}: {e}")
            return False

        # Extract source FPS from demuxer for video timestamp calculation
        source_fps = 30.0  # Default fallback
        try:
            fps_num = demuxer.FrameRate()[0]
            fps_den = demuxer.FrameRate()[1]
            if fps_den > 0:
                source_fps = fps_num / fps_den
                logger.debug(f"{camera_id}: Detected source FPS = {source_fps:.2f}")
        except Exception as e:
            logger.debug(f"{camera_id}: Could not get FPS from demuxer, using default: {e}")

        source_fps = _normalize_reported_fps(source_fps)

        # T0+PTS sync: For RTSP streams, record wall clock time (T0) and generate session_id
        session_start_ns = 0
        session_id = ""
        if stream_type == "rtsp":
            session_start_ns = time.time_ns()
            session_id = str(uuid.uuid4())[:8]
            logger.info(f"{camera_id}: RTSP session started - session_id={session_id}, T0={session_start_ns}")

        stream_state = StreamState(
            stream_id=stream_id,
            camera_id=camera_id,
            video_path=local_path,
            demuxer=demuxer,
            width=width,
            height=height,
            # The source's own geometry, probed at open. It is knowable here and
            # nowhere later, and the ring is sized from min(declared, native).
            native_width=_demuxer_native_dim(demuxer, "Width", camera_id),
            native_height=_demuxer_native_dim(demuxer, "Height", camera_id),
            stream_type=stream_type,
            source_fps=source_fps,
            demuxer_type="nvc",
            session_start_ns=session_start_ns,
            session_id=session_id,
        )
        with self._streams_lock:
            self.streams_per_decoder[decoder_idx].append(stream_state)
        return True

    def _assign_stream_gstreamer(
        self,
        decoder_idx: int,
        stream_id: int,
        camera_id: str,
        video_path: str,
        width: int,
        height: int,
        stream_type: str,
        codec: str = "h264",
    ) -> bool:
        """Assign stream using GStreamer demuxer (for ABSOLUTE RTP timestamps).

        Single attempt - returns False immediately if source not available.
        Caller handles background retry for failed cameras.
        """
        if not GSTREAMER_DEMUXER_AVAILABLE or GstRTPDemuxer is None:
            logger.error(f"GStreamer demuxer not available for {camera_id}")
            return False

        try:
            gst_demuxer = GstRTPDemuxer(video_path, use_tcp=True, codec=codec)
            gst_demuxer.open(quiet=True)
            source_fps = _normalize_reported_fps(gst_demuxer.fps)
            logger.warning(
                f"{camera_id}: GStreamer demuxer opened, {gst_demuxer.width}x{gst_demuxer.height}@{source_fps:.1f}fps"
            )
        except Exception as e:
            logger.warning(f"{camera_id}: GStreamer demuxer open failed: {e}")
            return False

        # For GStreamer RTSP, session_id tracks reconnections
        session_start_ns = time.time_ns()
        session_id = gst_demuxer.session_id

        stream_state = StreamState(
            stream_id=stream_id,
            camera_id=camera_id,
            video_path=video_path,
            demuxer=None,  # Not used for GStreamer
            width=width,  # Declared target; clamped to native by effective_frame_dims()
            height=height,
            # The resolution the demuxer just reported. It used to be logged on the
            # line above and then discarded, which left the ring sized from config
            # alone — the whole defect this records it for.
            native_width=int(getattr(gst_demuxer, "width", 0) or 0),
            native_height=int(getattr(gst_demuxer, "height", 0) or 0),
            stream_type=stream_type,
            source_fps=source_fps,
            demuxer_type="gstreamer",
            session_start_ns=session_start_ns,
            session_id=session_id,
            gst_demuxer=gst_demuxer,
            gst_demux_gen=gst_demuxer.demux(),
            first_rtp_timestamp=gst_demuxer.first_rtp_timestamp,
        )
        with self._streams_lock:
            self.streams_per_decoder[decoder_idx].append(stream_state)
        return True

    def decode_round(
        self,
        decoder_idx: int,
        frames_per_stream: int = 4,
        target_h: int = 0,
        target_w: int = 0,
        benchmark_metrics=None,
    ) -> Tuple[int, List[Tuple[str, cp.ndarray, int, str, str, int, Optional[int], int, int]]]:
        """Decode frames and convert to NV12.

        Supports two demuxer backends:
        - NVC: PyNvVideoCodec demuxer (fastest for local files)
        - GStreamer: Provides ABSOLUTE RTP timestamps for RTSP streams

        Returns:
            (total_frames, [(camera_id, nv12_tensor, timestamp_ns, stream_type, session_id, session_start_ns, rtp_timestamp), ...])
            where:
            - timestamp_ns: For RTSP = T0 + PTS (absolute wall clock ns), for files = PTS (video-relative ns)
            - stream_type: "rtsp" or "file"
            - session_id: 8-char unique ID for RTSP (changes on reconnect), empty for files
            - session_start_ns: T0 wall clock when RTSP connected (0 for files)
            - rtp_timestamp: ABSOLUTE 32-bit RTP timestamp (GStreamer only, None for NVC)
        """
        if decoder_idx >= self.actual_pool_size:
            return 0, []

        decoder = self.decoders[decoder_idx]
        with self._streams_lock:
            streams = list(self.streams_per_decoder[decoder_idx])  # snapshot
        total_frames = 0
        decoded_frames = []

        if not streams:
            return 0, []

        for stream in streams:
            frames_this_stream = 0

            # Per-stream target dims (match ring buffer); fall back to global
            stream_w = stream.width if stream.width > 0 else target_w
            stream_h = stream.height if stream.height > 0 else target_h

            # Route to appropriate demuxer based on type
            # Skip streams with no demuxer (e.g. duplicates from config rebuild)
            if stream.demuxer is None and stream.gst_demuxer is None:
                continue

            if stream.demuxer_type == "gstreamer" and stream.gst_demuxer is not None:
                # GStreamer demuxer path - ABSOLUTE RTP timestamps
                frames_this_stream, stream_decoded = self._decode_gstreamer_stream(
                    stream,
                    decoder,
                    frames_per_stream,
                    stream_h,
                    stream_w,
                    benchmark_metrics=benchmark_metrics,
                )
                decoded_frames.extend(stream_decoded)
                total_frames += frames_this_stream
            else:
                # NVC demuxer path (default)
                frames_this_stream, stream_decoded = self._decode_nvc_stream(
                    stream,
                    decoder,
                    frames_per_stream,
                    stream_h,
                    stream_w,
                    benchmark_metrics=benchmark_metrics,
                )
                decoded_frames.extend(stream_decoded)
                total_frames += frames_this_stream

        return total_frames, decoded_frames

    @staticmethod
    def _flush_decoder(decoder: Any) -> None:
        """Flush the NVDEC decoder (e.g. on EOF before restart)."""
        try:
            _flush_pkt = nvc.PacketData()
            _flush_pkt.bsl_data = 0
            _flush_pkt.bsl = 0
            for _ in decoder.Decode(_flush_pkt):
                pass
        except Exception:  # nosec B110
            pass

    @staticmethod
    def _compute_gst_timestamp_ns(stream: "StreamState", absolute_ns: int, rtp_ts_ns: int) -> int:
        """Compute decode timestamp from GStreamer RTP data.

        Returns RTP-derived nanoseconds only (rtp_ts * 1e9 / 90kHz), or 0.
        This keeps capture_timestamp_ns purely RTP-based on both platforms
        so the frontend can use it consistently for overlay sync.
        """
        # RTP-derived timestamp only — consistent across nvdec and orin.
        # The value is later packed as an unsigned 64-bit int via
        # struct.pack("<Q", ...) in the CUDA shm ring buffer, so it MUST lie
        # strictly inside the uint64 range. The first frame after a demuxer
        # session restart can carry an invalid/sentinel RTP timestamp that is
        # positive (passes "> 0") but out of range — e.g. derived from
        # GST_CLOCK_TIME_NONE — which would raise struct.error and kill the
        # worker's write loop. Treat any such value as "no timestamp".
        if 0 < rtp_ts_ns < _UINT64_MAX:
            return rtp_ts_ns
        now = time.time()
        # ``getattr``/``setattr`` so a missing throttle field can never turn a
        # bad-timestamp frame into an exception that crashes the decode loop and
        # forces a demuxer restart (the StreamState ``_last_rtp_warn`` drift bug).
        if now - getattr(stream, "_last_rtp_warn", 0.0) > 5.0:
            logger.warning(
                f"[NVDEC] {stream.camera_id}: capture_timestamp_ns=0 "
                f"(no RTP timestamp from camera, frame {stream.frames_decoded})"
            )
            stream._last_rtp_warn = now
        return 0
        # --- Alternative timestamp sources (disabled, kept for reference) ---
        # # RTCP Sender Report: absolute Unix epoch nanoseconds
        # if absolute_ns and absolute_ns > 0:
        #     return absolute_ns
        # # Wall-clock fallback for live RTSP (epoch, ~100ms offset from capture)
        # if stream.stream_type == "rtsp":
        #     return time.time_ns()
        # # Frame-count estimate (file sources)
        # return int(stream.frames_decoded * 1_000_000_000 / stream.source_fps)

    @staticmethod
    def _build_decode_packet(nal_bytes: bytes, rtp_ts: int) -> Tuple[Any, Any]:
        """Wrap one access unit as a ``PacketData``, carrying its RTP timestamp.

        Returns the packet AND the numpy view backing it: the packet holds a raw
        pointer (`bsl_data`) into that buffer, so the caller must keep the array
        alive for as long as the decoder may read the packet.

        The PTS is what lets the surface that eventually comes out describe
        itself. Without it the decode loop stamps the AU being fed in onto a
        picture NVDEC emitted ~2 frames ago (see `_SUPPORTS_SURFACE_PTS`). A
        decoder build whose PacketData has no settable `pts` disables the whole
        surface-PTS path once, rather than raising per packet.
        """
        nal_arr = np.frombuffer(nal_bytes, dtype=np.uint8)
        pkt = nvc.PacketData()
        pkt.bsl_data = nal_arr.ctypes.data
        pkt.bsl = len(nal_bytes)
        if _SUPPORTS_SURFACE_PTS:
            try:
                pkt.pts = rtp_ts
            except Exception as exc:  # nosec B110 - capability probe
                _disable_surface_pts_support(f"PacketData.pts not settable: {exc}")
        return pkt, nal_arr

    def _gst_surface_timestamp_ns(self, stream: "StreamState", absolute_ns: int, rtp_ts_ns: int, surface: Any) -> int:
        """Timestamp one decoded surface, preferring the picture's OWN PTS.

        On the first surface that cannot supply one, drop to the old
        feed-in-timestamp behaviour permanently rather than probing every frame.
        """
        surface_rtp = _surface_rtp_timestamp(surface) if _SUPPORTS_SURFACE_PTS else None
        if surface_rtp is not None:
            return self._compute_gst_timestamp_ns(stream, absolute_ns, surface_rtp * 1_000_000_000 // RTP_CLOCK_RATE)
        if _SUPPORTS_SURFACE_PTS:
            _disable_surface_pts_support("surface exposes no usable timestamp")
        return self._compute_gst_timestamp_ns(stream, absolute_ns, rtp_ts_ns)

    def _to_nv12(self, stream: "StreamState", surface: Any, target_h: int, target_w: int) -> Any:
        """Convert one decoded surface to an NV12 tensor at THIS camera's target.

        ``target_h``/``target_w`` are the worker-global pair and are only the fallback:
        they used to be applied to every camera in the sub-process, so two cameras with
        different declared sizes both got the first one's target while each ring was
        built at its own size — and every camera but the first mismatched. The target
        now comes from the camera's own ``StreamState`` via ``stream_target_dims``.
        """
        eff_h, eff_w = self.stream_target_dims(stream, target_h, target_w)
        return surface_to_nv12_with_src_dims(surface, eff_h, eff_w)

    def _decode_gstreamer_stream(
        self,
        stream: StreamState,
        decoder: Any,
        frames_per_stream: int,
        target_h: int,
        target_w: int,
        benchmark_metrics=None,
    ) -> Tuple[int, List[Tuple[str, cp.ndarray, int, str, str, int, Optional[int], int, int]]]:
        """Decode frames using GStreamer demuxer (for ABSOLUTE RTP timestamps).

        GStreamer extracts H264/H265 NAL units with raw RTP timestamps, then feeds
        them to PyNvVideoCodec for GPU decode. This provides ABSOLUTE RTP timestamps
        that persist across reconnections.

        Returns:
            (frames_decoded, [(camera_id, tensor, timestamp_ns, stream_type, session_id, session_start_ns, rtp_timestamp), ...])
        """
        frames_this_stream = 0
        decoded_frames = []
        _bm = benchmark_metrics

        while frames_this_stream < frames_per_stream:
            try:
                _bm_demux_t = _bm.start() if _bm else 0.0
                nal_result = next(stream.gst_demux_gen)
                if _bm:
                    _bm.record("demux", _bm_demux_t)

                if nal_result is None:
                    self._flush_decoder(decoder)
                    self._quick_restart_demuxer(stream)
                    break

                nal_bytes, rtp_ts, rtp_ts_ns, absolute_ns = nal_result

                if nal_bytes is None or len(nal_bytes) == 0:
                    stream.empty_packets += 1
                    now = time.monotonic()
                    if math.isclose(stream._empty_start_ns, 0.0, abs_tol=1e-9):
                        stream._empty_start_ns = now
                    # MATRICE_SG_STALL_SEC / MATRICE_SG_BOOTSTRAP_SEC, resolved
                    # once in __init__ via restart_policy.resolve_restart_policy.
                    stall_sec = self.restart_policy.stall_sec
                    bootstrap_sec = self.restart_policy.bootstrap_sec
                    limit = bootstrap_sec if stream.frames_decoded == 0 else stall_sec
                    if (now - getattr(stream, "_empty_start_ns", now)) >= limit:
                        logger.warning(
                            "%s: GStreamer stall detected after %.1fs (limit=%.0fs, frames_decoded=%d); restarting",
                            stream.camera_id,
                            now - stream._empty_start_ns,
                            limit,
                            stream.frames_decoded,
                        )
                        self._restart_gstreamer_stream(stream)
                        stream.empty_packets = 0
                        stream._empty_start_ns = 0.0
                    continue

                frames_before = frames_this_stream

                if not _validate_h264_nal(nal_bytes, codec=self.codec):
                    stream.decode_errors += 1
                    if stream.decode_errors == 1:
                        logger.warning(f"{stream.camera_id}: Skipping invalid NAL ({len(nal_bytes)}B)")
                    continue

                try:
                    _pkt, _nal_arr = self._build_decode_packet(nal_bytes, rtp_ts)
                    _bm_decode_t = _bm.start() if _bm else 0.0
                    for surface in decoder.Decode(_pkt):
                        if _bm and _bm_decode_t:
                            _bm.record("gpu_decode", _bm_decode_t)
                            _bm_decode_t = 0.0

                        decode_timestamp_ns = self._gst_surface_timestamp_ns(stream, absolute_ns, rtp_ts_ns, surface)

                        _bm_resize_t = _bm.start() if _bm else 0.0
                        tensor, src_w, src_h = self._to_nv12(stream, surface, target_h, target_w)
                        if _bm:
                            _bm.record("nv12_resize", _bm_resize_t)

                        if tensor is not None:
                            decoded_frames.append(
                                (
                                    stream.camera_id,
                                    tensor,
                                    decode_timestamp_ns,
                                    stream.stream_type,
                                    stream.session_id,
                                    stream.session_start_ns,
                                    rtp_ts,
                                    src_w,
                                    src_h,
                                )
                            )
                            frames_this_stream += 1
                            stream.frames_decoded += 1
                            stream.empty_packets = 0
                            stream.decode_errors = 0
                            stream._empty_start_ns = 0.0

                            if stream.frames_decoded == 1:
                                # First frame since this (re)open: the ONLY proof
                                # of recovery. A demuxer that reopens without
                                # ever delivering a frame is still broken, so the
                                # restart history is cleared here and not in
                                # _restart_gstreamer_stream. keep_anchor=True
                                # preserves the cooldown floor across recovery.
                                self.stream_supervisor.reset(stream.camera_id, keep_anchor=True)

                            stream.last_rtp_timestamp = rtp_ts
                            if stream.first_rtp_timestamp is None:
                                stream.first_rtp_timestamp = rtp_ts

                        if frames_this_stream >= frames_per_stream:
                            break

                except Exception as decode_err:
                    stream.decode_errors += 1
                    if stream.decode_errors == 1:
                        logger.warning(f"{stream.camera_id}: GStreamer decode error: {decode_err}")
                    if stream.decode_errors >= stream.MAX_DECODE_ERRORS:
                        logger.warning(f"{stream.camera_id}: Too many decode errors, restarting GStreamer demuxer")
                        self._restart_gstreamer_stream(stream)
                        break

                if frames_this_stream == frames_before:
                    stream.empty_packets += 1
                    empty_limit = 100 if stream.frames_decoded == 0 else 10
                    if stream.empty_packets >= empty_limit:
                        self._restart_gstreamer_stream(stream)

            except StopIteration:
                logger.debug(f"{stream.camera_id}: GStreamer stream EOF, quick restart")
                self._flush_decoder(decoder)
                self._quick_restart_demuxer(stream)
                break

            except Exception as demux_err:
                logger.warning(f"{stream.camera_id}: GStreamer demux error: {demux_err}")
                stream.decode_errors += 1
                if stream.decode_errors >= stream.MAX_DECODE_ERRORS:
                    self._restart_gstreamer_stream(stream)
                break

            if frames_this_stream >= frames_per_stream:
                break

        return frames_this_stream, decoded_frames

    def _quick_restart_demuxer(self, stream: StreamState) -> None:
        """Lightweight restart for EOF (simulation video loop).

        Restarts the subprocess demuxer and resets the generator without
        the rate-limiting overhead of _restart_gstreamer_stream. Used for
        expected EOFs (video file loops) that happen frequently.
        """
        # A camera already declared dead (slow-probe) must not keep paying the
        # multi-second demuxer.restart() open()-retry on every StopIteration.
        # Defer to the cooldown-gated full restart, which no-ops during its
        # (stretched) cooldown and owns the quiet logging.
        if self.stream_supervisor.should_give_up(stream.camera_id):
            self._restart_gstreamer_stream(stream)
            return
        try:
            if stream.gst_demuxer:
                stream.gst_demuxer.restart()
                stream.gst_demux_gen = stream.gst_demuxer.demux()
                stream.session_id = stream.gst_demuxer.session_id
                stream.first_rtp_timestamp = stream.gst_demuxer.first_rtp_timestamp
                stream.last_rtp_timestamp = None
                stream.empty_packets = 0
                stream._empty_start_ns = 0.0
                stream.frames_decoded = 0
                stream.awaiting_idr = True  # Wait for IDR before decoding
        except Exception as e:
            # Fallback to the supervised full restart, which owns user-facing
            # logging (WARN pre-give-up, one ERROR at give-up, then quiet). Keep
            # this at debug so the frequent file-loop path stays silent.
            logger.debug(f"{stream.camera_id}: quick restart failed, falling back to full restart: {e}")
            self._restart_gstreamer_stream(stream)

    def _restart_gstreamer_stream(self, stream: StreamState) -> None:
        """Restart GStreamer demuxer on EOF or error.

        Note: stream.width/height must NOT be updated here — they must stay
        matched to the ring buffer dimensions set at creation time.
        """
        # Rate-limit + give-up policy is owned by self.stream_supervisor. The
        # cooldown default is high because every restart forces awaiting_idr=True
        # and burns the next IDR-to-IDR window; a too-low floor (was 2s) plus
        # other eager triggers caused 15-30 restarts/min and dropped a 30 FPS
        # source to ~3 FPS on Thor. A permanently-dead source (RTSP "Not found")
        # no longer floods ERROR tracebacks: after a burst of failed restarts
        # the supervisor enters a sticky slow-probe state (stretched cooldown,
        # demoted logging) while still probing so a source that returns recovers.
        cam_id = stream.camera_id
        if not self.stream_supervisor.on_error(cam_id):
            # Inside the cooldown window — suppress this restart. Reset the
            # transient error counters so we don't immediately re-trigger. As
            # before, no clock is anchored on a suppressed poll: the supervisor
            # keys the cooldown off the last REAL restart, so the elapsed time
            # since it keeps growing and a wedged camera can still restart itself
            # once the window elapses (not only on a full gateway restart).
            stream.decode_errors = 0
            stream.empty_packets = 0
            stream._empty_start_ns = 0.0
            logger.debug(f"{cam_id}: restart suppressed (within cooldown)")
            return

        slow_probe = self.stream_supervisor.should_give_up(cam_id)
        try:
            if stream.gst_demuxer:
                stream.gst_demuxer.close()
                stream.gst_demuxer.open(quiet=True)
                stream.gst_demux_gen = stream.gst_demuxer.demux()

                # Generate new session on reconnect
                stream.session_start_ns = time.time_ns()
                stream.session_id = stream.gst_demuxer.session_id
                stream.first_rtp_timestamp = stream.gst_demuxer.first_rtp_timestamp
                stream.last_rtp_timestamp = None
                stream.decode_errors = 0
                stream.empty_packets = 0
                stream._empty_start_ns = 0.0
                stream.frames_decoded = 0
                stream.awaiting_idr = True  # Wait for IDR before decoding
                stream._last_restart_time = time.monotonic()

                # NOT recovered yet — deliberately no supervisor.reset() here.
                # open() succeeding only means the demuxer was rebuilt; a camera
                # whose source is wedged reopens fine and then delivers nothing.
                # Resetting here dropped the cooldown anchor AND the restart
                # count on every such reopen, so a flapping camera restarted once
                # per stall detection (10s) instead of once per cooldown (30s)
                # and could never reach give-up — its restarts kept "succeeding".
                # The decode loop calls reset(keep_anchor=True) on the first frame
                # actually decoded, which is the real recovery signal.
                logger.info(f"{cam_id}: GStreamer demuxer restarted, new session_id={stream.session_id}")
        except Exception as e:
            stream._last_restart_time = time.monotonic()
            # Demote logging once we've given up so a dead camera does not spam
            # ERROR-level tracebacks. The single authoritative ERROR is emitted
            # exactly once by the on_give_up callback (_on_restart_give_up); the
            # RuntimeError message already carries the root cause (e.g. "Not
            # found"), so no full traceback is needed on the hot path.
            if slow_probe:
                logger.debug(f"{cam_id}: demuxer still unreachable (slow-probe): {e}")
            else:
                logger.warning(f"{cam_id}: failed to restart GStreamer demuxer: {e}")
            time.sleep(5)  # Backoff on persistent failures only

    def _on_restart_give_up(self, camera_id: str) -> None:
        """One-shot ERROR when a camera exhausts its fast-restart budget.

        Invoked once by the StreamSupervisor the first time a camera crosses the
        give-up threshold. After this the supervisor slow-probes quietly (see
        _restart_gstreamer_stream); the first frame actually decoded calls reset()
        and re-arms normal-cadence logging.
        """
        logger.error(
            "%s: demuxer restart repeatedly failed — source likely down. "
            "Entering slow-probe mode (cooldown=%.0fs); further failures are "
            "logged at debug. Will auto-recover if the source returns.",
            camera_id,
            self.stream_supervisor.giveup_cooldown_sec,
        )

    def _reset_nvc_demuxer(self, stream: StreamState, reason: str = "") -> bool:
        """Reset NVC demuxer and session state for a stream.

        Recreates the demuxer, resets PTS tracking, and generates a new
        session ID for RTSP streams. Returns True on success, False on error.
        """
        try:
            stream.demuxer = nvc.CreateDemuxer(stream.video_path)
            stream.decode_errors = 0
            stream.empty_packets = 0
            stream.frames_decoded = 0
            stream.pts_timebase = 0
            stream.first_packet_pts = 0
            if stream.stream_type == "rtsp":
                stream.session_start_ns = time.time_ns()
                stream.session_id = str(uuid.uuid4())[:8]
                logger.info(f"{stream.camera_id}: Demuxer reset ({reason}), new session_id={stream.session_id}")
            elif reason:
                logger.info(f"{stream.camera_id}: Demuxer reset ({reason})")
            return True
        except Exception as e:
            logger.exception(f"{stream.camera_id}: Failed to reset demuxer: {e}")
            return False

    def _compute_nvc_timestamp_ns(self, stream: StreamState, packet_pts: int) -> int:
        """Compute decode timestamp from NVC packet PTS.

        For RTSP: T0 (session_start_ns) + PTS = absolute wall clock time.
        For files: PTS only = video-relative timestamp.
        """
        if stream.pts_timebase > 0:
            pts_ns = (packet_pts - stream.first_packet_pts) * 1_000_000_000 // stream.pts_timebase
        else:
            pts_ns = int(stream.frames_decoded * 1_000_000_000 / stream.source_fps)

        if stream.stream_type == "rtsp":
            return stream.session_start_ns + pts_ns
        return pts_ns

    def _decode_nvc_stream(
        self,
        stream: StreamState,
        decoder: Any,
        frames_per_stream: int,
        target_h: int,
        target_w: int,
        benchmark_metrics=None,
    ) -> Tuple[int, List[Tuple[str, cp.ndarray, int, str, str, int, Optional[int], int, int]]]:
        """Decode frames using NVC (PyNvVideoCodec) demuxer.

        Returns:
            (frames_decoded, [(camera_id, tensor, timestamp_ns, stream_type, session_id, session_start_ns, rtp_timestamp), ...])
            Note: rtp_timestamp is always None for NVC demuxer
        """
        frames_this_stream = 0
        decoded_frames = []
        _bm = benchmark_metrics

        while frames_this_stream < frames_per_stream:
            try:
                _bm_demux_t = _bm.start() if _bm else 0.0
                packet = stream.demuxer.Demux()
                if _bm:
                    _bm.record("demux", _bm_demux_t)
                if packet is None:
                    self._reset_nvc_demuxer(stream, "EOF loop")
                    packet = stream.demuxer.Demux()
                    if packet is None:
                        break

                frames_before = frames_this_stream

                # Get packet PTS directly from NVDEC demuxer (more accurate than frame count)
                packet_pts = getattr(packet, "pts", 0) or 0
                packet_duration = getattr(packet, "duration", 0) or 0

                # Calculate timebase on first packet with valid duration
                if stream.pts_timebase == 0 and packet_duration > 0:
                    stream.pts_timebase = int(round(_normalize_reported_fps(stream.source_fps) * packet_duration))
                    stream.first_packet_pts = packet_pts
                    if stream.pts_timebase == 0:
                        stream.pts_timebase = 90000 if stream.stream_type == "rtsp" else 30000

                try:
                    _bm_decode_t = _bm.start() if _bm else 0.0
                    for surface in decoder.Decode(packet):
                        if _bm and _bm_decode_t:
                            _bm.record("gpu_decode", _bm_decode_t)
                            _bm_decode_t = 0.0

                        decode_timestamp_ns = self._compute_nvc_timestamp_ns(stream, packet_pts)

                        _bm_resize_t = _bm.start() if _bm else 0.0
                        tensor, src_w, src_h = self._to_nv12(stream, surface, target_h, target_w)
                        if _bm:
                            _bm.record("nv12_resize", _bm_resize_t)

                        if tensor is not None:
                            decoded_frames.append(
                                (
                                    stream.camera_id,
                                    tensor,
                                    decode_timestamp_ns,
                                    stream.stream_type,
                                    stream.session_id,
                                    stream.session_start_ns,
                                    None,
                                    src_w,
                                    src_h,
                                )
                            )
                            frames_this_stream += 1
                            stream.frames_decoded += 1
                            stream.empty_packets = 0
                            stream.decode_errors = 0

                        if frames_this_stream >= frames_per_stream:
                            break

                except Exception as decode_err:
                    stream.decode_errors += 1
                    if stream.decode_errors == 1:
                        logger.warning(f"{stream.camera_id}: Decode error: {decode_err}")
                    if stream.decode_errors >= stream.MAX_DECODE_ERRORS:
                        logger.warning(
                            f"{stream.camera_id}: {stream.decode_errors} consecutive decode errors, restarting demuxer"
                        )
                        if not self._reset_nvc_demuxer(stream, "decode errors"):
                            break

                if frames_this_stream == frames_before:
                    stream.empty_packets += 1
                    # NAL-count based limit is wrong: NVDEC has internal
                    # pipeline latency, so several consecutive Decode() calls
                    # returning no surface is normal at GOP boundaries and
                    # after every restart. Use a wall-clock check instead.
                    # HEVC + cold decoder bootstrap can chew 10+ NALs (SPS, PPS,
                    # AUD, IDR-config) before the first surface.
                    now = time.monotonic()
                    if stream.empty_packets == 1:
                        stream._empty_start_ns = now
                    # MATRICE_SG_STALL_SEC / MATRICE_SG_BOOTSTRAP_SEC, resolved
                    # once in __init__ via restart_policy.resolve_restart_policy.
                    stall_sec = self.restart_policy.stall_sec
                    bootstrap_sec = self.restart_policy.bootstrap_sec
                    limit = bootstrap_sec if stream.frames_decoded == 0 else stall_sec
                    if (now - getattr(stream, "_empty_start_ns", now)) >= limit:
                        self._reset_nvc_demuxer(stream, "empty packets (stall)")
                        stream._empty_start_ns = now
                else:
                    stream.empty_packets = 0
                    stream._empty_start_ns = 0.0

            except Exception as demux_err:
                logger.warning(f"{stream.camera_id}: Demux error: {demux_err}")
                stream.decode_errors += 1
                if stream.decode_errors >= stream.MAX_DECODE_ERRORS:
                    self._reset_nvc_demuxer(stream, "demux errors")
                break

            if frames_this_stream >= frames_per_stream:
                break

        return frames_this_stream, decoded_frames

    def get_camera_ids_for_decoder(self, decoder_idx: int) -> List[str]:
        """Get camera IDs for a decoder."""
        if decoder_idx >= self.actual_pool_size:
            return []
        return [s.camera_id for s in self.streams_per_decoder[decoder_idx]]

    def get_source_fps_for_decoder(self, decoder_idx: int) -> float:
        """Get average source FPS for streams assigned to a decoder.

        Used when target_fps=0 to cap output to source video rate.
        """
        if decoder_idx >= self.actual_pool_size:
            return DEFAULT_SOURCE_FPS
        streams = self.streams_per_decoder[decoder_idx]
        if not streams:
            return DEFAULT_SOURCE_FPS
        return _normalize_reported_fps(sum(s.source_fps for s in streams) / len(streams))

    @staticmethod
    def stream_target_dims(stream: StreamState, fallback_h: int = 0, fallback_w: int = 0) -> Tuple[int, int]:
        """This stream's decode target as ``(target_h, target_w)``.

        Per-camera, from the camera's own declared size clamped to its own source
        — not the worker-global pair, which is ``camera_configs[0]``'s size applied
        to every camera in the sub-process. That global was the bug behind the
        "F08 per-camera resize" log line: any sub-process holding two cameras with
        different declared sizes resized both to the first one's target while each
        ring was built at its own size, so every camera but the first failed the
        shape check on every frame.

        Derived from the same :func:`effective_frame_dims` the ring is sized with,
        so decode target and ring geometry cannot disagree.

        ``fallback_*`` is used only when this stream declares nothing AND its
        source reported nothing, i.e. there is genuinely no per-camera answer.
        """
        eff_w, eff_h = effective_frame_dims(
            int(stream.width or 0),
            int(stream.height or 0),
            int(stream.native_width or 0),
            int(stream.native_height or 0),
        )
        if eff_w <= 0 and eff_h <= 0:
            return fallback_h, fallback_w
        return eff_h, eff_w

    def get_native_dims_for_camera(self, camera_id: str) -> Optional[Tuple[int, int]]:
        """The source's own ``(width, height)`` as the demuxer reported it, or ``None``.

        Mirrors :meth:`get_source_fps_for_camera`: a per-camera fact learned at
        assignment, recorded on ``StreamState`` and read back here, because it
        cannot be recovered later.

        ``None`` means "the demuxer supplied no usable geometry" (either
        accessor missing, or a non-positive value) — NOT "square" or "default".
        The caller must treat it as unknown and leave the ring's geometry to be
        settled by the first decoded frame instead of inventing a size.
        """
        for streams in self.streams_per_decoder:
            for s in streams:
                if s.camera_id != camera_id:
                    continue
                w, h = int(s.native_width or 0), int(s.native_height or 0)
                return (w, h) if w > 0 and h > 0 else None
        return None

    def get_source_fps_for_camera(self, camera_id: str) -> float:
        """Detected source FPS for one camera (for the publish-rate decimator).

        Falls back to ``DEFAULT_SOURCE_FPS`` when the camera is unknown so the
        decimator fails open at a sane rate rather than dividing by zero.
        """
        for streams in self.streams_per_decoder:
            for s in streams:
                if s.camera_id == camera_id:
                    return _normalize_reported_fps(s.source_fps)
        return DEFAULT_SOURCE_FPS

    def _close_stream_state(self, stream: StreamState) -> None:
        """Explicitly release all resources held by a StreamState."""
        # Close GStreamer subprocess demuxer
        if stream.gst_demuxer is not None:
            try:
                stream.gst_demuxer.close()
            except Exception as e:
                logger.debug(f"Error closing gst_demuxer for {stream.camera_id}: {e}")
            stream.gst_demuxer = None
        # Stop the generator to release its frame
        if stream.gst_demux_gen is not None:
            try:
                stream.gst_demux_gen.close()
            except Exception:  # nosec B110
                pass
            stream.gst_demux_gen = None
        # Close NVC demuxer if present
        if stream.demuxer is not None:
            try:
                if hasattr(stream.demuxer, "close"):
                    stream.demuxer.close()
            except Exception as e:
                logger.debug(f"Error closing NVC demuxer for {stream.camera_id}: {e}")
            stream.demuxer = None

    def remove_stream(self, camera_id: str) -> bool:
        """Remove a specific stream by camera_id, closing its demuxer resources."""
        with self._streams_lock:
            for decoder_idx, streams in enumerate(self.streams_per_decoder):
                for i, stream in enumerate(streams):
                    if stream.camera_id == camera_id:
                        self._close_stream_state(stream)
                        del streams[i]
                        logger.info(f"Removed stream {camera_id} from decoder {decoder_idx}")
                        return True
        return False

    def close(self):
        """Close all decoders and demuxers."""
        self.decoders.clear()
        for streams in self.streams_per_decoder:
            for stream in streams:
                self._close_stream_state(stream)
            streams.clear()


# =============================================================================
# Worker Thread — helpers
# =============================================================================


def _demuxer_native_dim(demuxer: Any, attr: str, camera_id: str) -> int:
    """Read ``Width``/``Height`` off an NVC demuxer, or 0 if it cannot supply one.

    Never raises and never guesses: a build whose demuxer lacks the accessor, or
    reports a non-positive value, yields 0, which the ring sizing reads as
    "unknown" and defers to the first decoded frame. Guessing here would put the
    ring back on a value the source never confirmed, which is the whole defect
    this exists to remove.
    """
    try:
        value = getattr(demuxer, attr, None)
        if callable(value):
            value = value()
        native = int(value or 0)
    except Exception:
        # Capability probe on a C-extension object: no accessor, or an
        # unparseable value, both mean "unknown".
        logger.debug("%s: NVC demuxer exposed no usable %s", camera_id, attr, exc_info=True)
        return 0
    return native if native > 0 else 0


def effective_frame_dims(declared_w: int, declared_h: int, native_w: int, native_h: int) -> Tuple[int, int]:
    """The geometry the decoder will actually emit: ``min(declared, native)``.

    This is the single source of truth for ring-buffer sizing, and it exists
    because the two used to be resolved independently and could disagree
    permanently:

    * the ring was created from the DECLARED per-camera size (the API's
      ``customStreamSettings``), before any source was open, and
    * the decoder clamps a target larger than native down to native and never
      upsamples (``surface_to_nv12_with_src_dims``, the F08 rule).

    So a config declaring 1920x1080 for a camera that really sends 1280x720
    produced a 1920x1080 ring fed 1280x720 tensors — ``_validate_frame_shape``
    rejected every frame, the camera published nothing, and because the frame
    counter only advances AFTER a successful ring write the manager's watchdog
    read the whole GPU as stalled. Deriving both from this function makes that
    disagreement unrepresentable.

    A declared dimension of 0 means "native" and yields the native value. An
    unknown native (0) yields the declared value unchanged: with nothing to
    clamp against, the declared target is still the best available answer, and
    the first-frame reconcile is what settles it.
    """
    w = native_w if declared_w <= 0 else (min(declared_w, native_w) if native_w > 0 else declared_w)
    h = native_h if declared_h <= 0 else (min(declared_h, native_h) if native_h > 0 else declared_h)
    return max(w, 0), max(h, 0)


def nv12_ring_height(frame_h: int) -> int:
    """Ring-buffer row count for an NV12 frame of ``frame_h`` luma rows.

    NV12 packs a full-height Y plane plus a half-height interleaved CbCr plane,
    so the ring is 1.5x the frame height. Named because the ``h + h // 2``
    expression was open-coded at four sites that all had to agree with
    ``_validate_frame_shape``'s inverse (``nv12_h * 2 // 3``).
    """
    return frame_h + frame_h // 2 if frame_h > 0 else 0


def _ack_producer_ready(
    worker_status_queue: Optional[Any],
    cam_id: str,
    gpu_id: int,
    lazy: bool,
) -> None:
    """Emit the ``producer_ready`` ACK the hot-add path waits on.

    Factored out because it is now sent from three places (eager create, the
    pre-flight geometry reconcile, and the lazy first-frame create) and a missed
    ACK is not a cosmetic loss: ``hotadd_policy`` tears the camera down and
    re-adds it in a loop when the ACK misses its deadline.
    """
    if worker_status_queue is None:
        return
    try:
        worker_status_queue.put_nowait({"type": "producer_ready", "camera_id": cam_id, "gpu_id": gpu_id, "lazy": lazy})
    except thread_queue.Full:
        logger.warning(f"GPU {gpu_id}: status queue full, dropping producer_ready ACK for {cam_id}")
    except Exception:
        logger.debug("producer_ready ACK put failed: %s", cam_id, exc_info=True)


def _open_ring_producer(cam_id: str, gpu_id: int, num_slots: int, frame_w: int, nv12_h: int) -> DataBusProducer:
    """Construct one camera's ring-buffer producer.

    Single construction site so every path that creates or re-creates a ring
    agrees on kind, naming and geometry convention (``height`` is the NV12 row
    count, not the luma height). The eager, reconcile and lazy paths previously
    open-coded this call and could drift apart.
    """
    return DataBus.producer(
        cam_id,
        "sg",
        "frames",
        "cupy",
        gpu_id=gpu_id,
        num_slots=num_slots,
        width=frame_w,
        height=nv12_h,
    )


def ring_frame_dims(producer: Any) -> Tuple[int, int]:
    """A producer's ``(frame_w, frame_h)`` in luma pixels, or ``(0, 0)``.

    The ring stores ``height`` as NV12 rows, so the luma height is ``* 2 // 3``
    — the same inverse ``_validate_frame_shape`` applies to a tensor.
    """
    rb = getattr(producer, "rb", None)
    w = int(getattr(rb, "width", 0) or 0)
    nv12_h = int(getattr(rb, "height", 0) or 0)
    if w <= 0 or nv12_h <= 0:
        return 0, 0
    return w, nv12_h * 2 // 3


def _recreate_ring_at(
    cam_id: str,
    ring_buffers: Dict[str, DataBusProducer],
    gpu_id: int,
    num_slots: int,
    frame_w: int,
    frame_h: int,
    reason: str,
    worker_status_queue: Optional[Any] = None,
) -> bool:
    """Re-open ``cam_id``'s ring at ``frame_w x frame_h``. True if it now matches.

    Safe to call while consumers are attached: the producer publishes its
    metadata segment by atomic ``rename`` onto a fresh inode, which is precisely
    what a gateway restart looks like downstream, and the inference connector's
    watchdog already reconnects on an inode change
    (``ring_buffer_connector._watchdog_check_camera``). It is nonetheless only
    called BEFORE a camera's first successful publish — see the caller — because
    a mid-stream re-open costs every attached consumer a reconnect.

    On failure the old producer is left in place: a ring with the wrong geometry
    still drops frames, but it drops them with a live segment the consumer can
    stay attached to, which beats leaving the camera with no producer at all.
    """
    nv12_h = nv12_ring_height(frame_h)
    if frame_w <= 0 or nv12_h <= 0:
        logger.error("%s: refusing to re-open ring at %sx%s (%s)", cam_id, frame_w, frame_h, reason)
        return False

    old = ring_buffers.get(cam_id)
    old_w, old_h = ring_frame_dims(old) if old is not None else (0, 0)
    try:
        producer = _open_ring_producer(cam_id, gpu_id, num_slots, frame_w, nv12_h)
    except Exception as exc:
        # Keep the old ring rather than dropping the camera entirely.
        logger.exception("%s: ring re-open at %sx%s failed (%s): %s", cam_id, frame_w, frame_h, reason, exc)
        return False

    ring_buffers[cam_id] = producer
    if old is not None:
        try:
            old.close()
        except Exception:
            # The replacement is already published.
            logger.debug("%s: closing the superseded ring producer failed", cam_id, exc_info=True)

    logger.warning(
        "%s: ring buffer re-opened %sx%s -> %sx%s (%s). Consumers reconnect on the "
        "new SHM inode; frames flow at the new geometry.",
        cam_id,
        old_w or "?",
        old_h or "?",
        frame_w,
        frame_h,
        reason,
    )
    _ack_producer_ready(worker_status_queue, cam_id, gpu_id, lazy=False)
    return True


def _maybe_create_lazy_ring_buffer(
    cam_id: str,
    tensor: Any,
    ring_buffers: Dict[str, DataBusProducer],
    lazy_rb_cameras: Optional[set],
    pool_gpu_id: int,
    num_slots: int,
    worker_id: int,
    worker_status_queue: Optional[Any] = None,
) -> Optional[str]:
    """Create a ring buffer lazily when first frame arrives for native-res cameras.

    Returns an error message on failure, or None on success/skip.
    """
    if not (lazy_rb_cameras and cam_id not in ring_buffers and cam_id in lazy_rb_cameras):
        return None
    t_nv12_h, t_w, _ = tensor.shape
    t_h = t_nv12_h * 2 // 3
    producer = _open_ring_producer(cam_id, pool_gpu_id, num_slots, t_w, t_nv12_h)
    ring_buffers[cam_id] = producer
    lazy_rb_cameras.discard(cam_id)
    _ack_producer_ready(worker_status_queue, cam_id, pool_gpu_id, lazy=True)
    logger.info(
        f"Worker {worker_id}: Lazy-created ring buffer for {cam_id}: "
        f"{t_w}x{t_h} (NV12: {t_nv12_h}x{t_w}, "
        f"{t_w * t_nv12_h / 1e6:.2f} MB/frame)"
    )
    return None


def _validate_frame_shape(
    tensor: Any,
    producer: Any,
    target_h: int,
    target_w: int,
) -> bool:
    """Validate that tensor shape matches the ring buffer dimensions."""
    rb_w = getattr(producer.rb, "width", 0)
    rb_nv12_h = getattr(producer.rb, "height", 0)
    if rb_w > 0 and rb_nv12_h > 0:
        expected_shape = (rb_nv12_h, rb_w, 1)
    else:
        _nv12_h = target_h + target_h // 2 if target_h > 0 else 0
        expected_shape = (_nv12_h, target_w, 1) if _nv12_h > 0 else tensor.shape
    return tensor.shape == expected_shape


def _reconcile_or_drop_on_shape_mismatch(
    cam_id: str,
    tensor: Any,
    ring_buffers: Dict[str, DataBusProducer],
    published_once: Set[str],
    gpu_id: int,
    num_slots: int,
    worker_id: Any,
    worker_status_queue: Optional[Any],
    log_err_rate_limited: Callable[[str, str], None],
) -> Optional[DataBusProducer]:
    """Last-resort geometry reconcile at the mismatch site.

    ``_preflight_reconcile_geometry`` already sized this ring from the source's own
    geometry, so reaching here means either the source reported nothing at open (a
    demuxer carrying no caps) or the resize kernel fell back to native passthrough.
    Either way the tensor in hand is the authority on what this camera actually
    produces, so the ring is re-opened to match it.

    Only BEFORE the camera's first successful publish. After that the geometry is
    **pinned**: re-opening a ring that consumers have attached to costs every one of
    them a reconnect, and a source whose resolution genuinely changes mid-stream is
    rarer than the config drift this guards against. In that case the frame is
    dropped with one actionable error naming both geometries, rather than the old
    behaviour of dropping every frame forever with nothing that said why.

    Returns the producer to publish through, or ``None`` if this frame must be
    dropped.
    """
    t_nv12_h, t_w, _ = tensor.shape
    frame_h = t_nv12_h * 2 // 3
    if cam_id not in published_once and _recreate_ring_at(
        cam_id,
        ring_buffers,
        gpu_id,
        num_slots,
        t_w,
        frame_h,
        reason="first decoded frame disagreed with the ring geometry",
        worker_status_queue=worker_status_queue,
    ):
        return ring_buffers[cam_id]

    r_w, r_h = ring_frame_dims(ring_buffers[cam_id])
    log_err_rate_limited(
        f"shape:{cam_id}",
        f"Worker {worker_id}: {cam_id} produces {t_w}x{frame_h} but its ring is {r_w}x{r_h} "
        f"and has already published at that geometry — dropping these frames. The source "
        f"resolution changed mid-stream; restart the gateway (or this camera) to resize the ring.",
    )
    return None


def _flush_shared_counters(
    frame_counter: GlobalFrameCounter,
    shared_frame_count: Optional[Any],
    gpu_frame_count: Optional[Any],
    frames_since_counter_update: int,
) -> None:
    """Batch-flush frame counters to avoid per-frame lock overhead."""
    frame_counter.increment()
    if shared_frame_count is not None:
        with shared_frame_count.get_lock():
            shared_frame_count.value += frames_since_counter_update
    if gpu_frame_count is not None:
        with gpu_frame_count.get_lock():
            gpu_frame_count.value += frames_since_counter_update


# =============================================================================
# Worker Thread
# =============================================================================


def nvdec_pool_worker(
    worker_id: int,
    decoder_idx: int,
    pool: NVDECDecoderPool,
    ring_buffers: Dict[str, DataBusProducer],
    frame_counter: GlobalFrameCounter,
    duration_sec: float,
    result_queue: thread_queue.Queue,
    stop_event: threading.Event,
    burst_size: Optional[int] = None,
    target_h: int = 0,
    target_w: int = 0,
    target_fps: int = 0,
    shared_frame_count: Optional[mp.Value] = None,  # type: ignore[valid-type]
    gpu_frame_count: Optional[mp.Value] = None,  # type: ignore[valid-type]
    lazy_rb_cameras: Optional[set] = None,
    num_slots: int = 64,
    benchmark_mode: bool = False,
    worker_status_queue: Optional[Any] = None,
    optimizer_config: Optional[Dict[str, Any]] = None,
    output_fps_cap: float = DEFAULT_OUTPUT_FPS_CAP,
    publish_fps_by_camera: Optional[Dict[str, float]] = None,
):
    """NVDEC worker thread.

    Decodes frames and writes NV12 tensors to ring buffers.
    Uses dedicated CUDA stream per worker for kernel overlap.
    Supports FPS limiting when target_fps > 0.

    F08: ``publish_fps_by_camera`` maps camera_id -> the aggregated per-camera
    publish rate (``max(app min_fps)``). When a camera has a positive entry it
    overrides the worker-global ``output_fps_cap`` for that camera's publish
    decimator; otherwise the global cap (``MATRICE_OUTPUT_FPS``) applies.

    Args:
        shared_frame_count: Global counter (all GPUs)
        gpu_frame_count: Per-GPU counter (this GPU only)
        benchmark_mode: Enable granular per-stage timing
    """
    if CUPY_AVAILABLE:
        cp.cuda.Device(pool.gpu_id).use()
        cuda_stream = cp.cuda.Stream(non_blocking=True)
    else:
        cuda_stream = None

    local_frames = 0
    local_errors = 0
    # Ring geometry is pinned once a camera is in here (see
    # _reconcile_or_drop_on_shape_mismatch).
    published_once: Set[str] = set()
    frames_since_counter_update = 0
    counter_batch_size = 100
    start_time = time.perf_counter()

    # Rate-limited error logging: the old "log the first 3 errors then go silent
    # forever" gating meant a persistently broken ring buffer / shape mismatch
    # produced a worker that discarded frames invisibly for the rest of its
    # life. Instead, log once per interval per (category, camera) with a count
    # of how many were suppressed since the last emission. `local_errors` still
    # accumulates and is reported in the worker result summary.
    _err_log_interval = 60.0
    _err_log_state: Dict[str, Tuple[float, int]] = {}

    def _log_err_rate_limited(key: str, msg: str) -> None:
        now = time.time()
        last_ts, suppressed = _err_log_state.get(key, (0.0, 0))
        if now - last_ts >= _err_log_interval:
            if suppressed:
                logger.error(
                    "%s (+%d similar suppressed in last %.0fs)",
                    msg,
                    suppressed,
                    now - last_ts,
                )
            else:
                logger.error(msg)
            _err_log_state[key] = (now, 0)
        else:
            _err_log_state[key] = (last_ts, suppressed + 1)

    camera_ids = pool.get_camera_ids_for_decoder(decoder_idx)
    num_streams = len(camera_ids)

    # Burst size: explicit override (non-None) wins; otherwise auto-tier by
    # per-decoder stream count. Recomputed only when count changes (cameras
    # added/removed at runtime), not every round.
    explicit_burst = burst_size
    last_stream_count = num_streams
    if explicit_burst is not None:
        active_burst = explicit_burst
    else:
        active_burst = _compute_dynamic_burst_size(num_streams)

    # Benchmark mode: granular per-stage timing
    bm = None
    bm_frames = 0  # frames written in current benchmark interval
    if benchmark_mode and BenchmarkMetrics is not None:
        bm = BenchmarkMetrics(enabled=True)
        bm_log_interval = 5.0  # Log benchmark metrics every 5 seconds
        bm_last_log_time = start_time

    # FPS limiting: cap decode output to real-time camera rate.
    # When target_fps <= 0 (default), uses source video FPS (~30) as the limit.
    # This is INTENTIONAL for production: decoding faster than the camera produces
    # wastes GPU cycles and fills ring buffers with duplicate looped frames.
    # For raw decode throughput benchmarks, pass --fps with a high value (e.g. 999).
    # Each worker handles num_streams cameras at effective_target_fps each.
    if target_fps <= 0:
        # Use source video FPS - get average for this decoder's streams
        source_fps = pool.get_source_fps_for_decoder(decoder_idx)
        effective_target_fps = source_fps
        fps_mode = f", FPS limit=source ({source_fps:.1f})/stream"
    else:
        effective_target_fps = float(target_fps)
        fps_mode = f", FPS limit={target_fps}/stream"

    effective_target_fps = _normalize_reported_fps(effective_target_fps)

    # Disable FPS limiter at scale — with many streams the per-frame sleep
    # dominates and caps throughput far below GPU capacity.
    fps_limit_enabled = num_streams > 0 and num_streams <= 50
    if fps_limit_enabled:
        # Total target frames per second for all streams handled by this worker
        worker_target_fps = effective_target_fps * num_streams
        frame_interval = 1.0 / worker_target_fps
        next_frame_time = start_time
    else:
        frame_interval = 0.0
        next_frame_time = 0.0

    # Output decimation: per-camera PUBLISH cap, separate from the decode pacer
    # above. Config-driven via ``output_fps_cap`` (threaded from the gateway,
    # default DEFAULT_OUTPUT_FPS_CAP = 10 FPS); MATRICE_OUTPUT_FPS overrides it
    # per deployment (0 disables). Decode is unchanged; we only gate writes.
    #
    # The PRIMARY decision is a per-camera phase accumulator
    # (``_should_publish_frame``): frame-count based, so it yields a stable
    # ``output_fps_target`` average out of ANY source rate with no wall-clock
    # jitter (30->every-3rd, 25->2,3,2,3 averaging exactly 10). It needs the
    # per-camera source FPS from the decoder pool.
    output_interval_ns = _resolve_output_interval_ns(output_fps_cap)  # logs WARNING when active
    output_fps_target = (1e9 / output_interval_ns) if output_interval_ns > 0 else 0.0
    # F08: per-camera publish rate (max(app min_fps)) overrides the worker-global
    # target above; the global cap remains the fallback for cameras without a
    # declared demand. The phase accumulator is already keyed per camera_id.
    publish_fps_by_camera = publish_fps_by_camera or {}
    # Relaxed monotonic wall-clock flood-guard: a hard ceiling at
    # SAFETY_FACTOR x the target that only trips if the source FPS is
    # mis-detected LOW (which would make the accumulator pass too many frames).
    # Set well above the target so it never rejects on-cadence publishes.
    safety_interval_ns = int(output_interval_ns / _OUTPUT_FPS_SAFETY_FACTOR) if output_interval_ns > 0 else 0
    # Per-camera phase accumulator for the primary decimator.
    pub_acc: Dict[str, float] = {}
    # last_write_ns holds the per-camera ``f"{cam_id}:mono"`` monotonic time of
    # the last accepted write, used only by the relaxed flood-guard above.
    last_write_ns: Dict[str, int] = {}

    # Per-camera last session_id published into the ring-buffer header. The
    # session id only changes at producer creation and on RTSP/demuxer
    # (re)connect, so publish it on change instead of re-writing + flushing the
    # 16-byte session field on EVERY frame (≈10k mmap flushes/s at 1000 cams ×
    # 10 fps). Consumers read it solely to detect SG restart, so write-on-change
    # is behaviourally identical and far cheaper.
    published_session: Dict[str, str] = {}

    # Pluggable frame-skip seam, shared with the OpenCV flow. Built inside the
    # worker (stateful per camera; never crosses the process boundary). Default
    # is a no-op that publishes every frame — it runs AFTER the output-fps cap
    # above, so future cupy/SSIM gates compose with the existing decimation.
    from ..frame_optimizer import build_frame_optimizer

    optimizer = build_frame_optimizer(optimizer_config)

    # F08: non-native target dims now drive the intentional per-camera SG resize
    # (publish at max(min_resolution), clamped to native). This is the normal
    # path, so log at INFO for visibility rather than WARNING.
    if (target_w or 0) > 0 or (target_h or 0) > 0:
        logger.info(
            "Worker %s decoding to target dims %sx%s (F08 per-camera resize; clamped to native, never upsampled).",
            worker_id,
            target_w,
            target_h,
        )

    logger.debug(f"Worker {worker_id}: decoder={decoder_idx}, cams={num_streams}{fps_mode}")

    while not stop_event.is_set():
        if time.perf_counter() - start_time >= duration_sec:
            break

        # Adapt burst when stream count changes (dynamic add/remove). O(1)
        # len() per round; recompute only fires on actual change.
        if explicit_burst is None:
            current_stream_count = len(pool.streams_per_decoder[decoder_idx])
            if current_stream_count != last_stream_count:
                last_stream_count = current_stream_count
                active_burst = _compute_dynamic_burst_size(current_stream_count)

        # FPS limiting: wait until next scheduled frame time
        _bm_fps_t = bm.start() if bm else 0.0
        if fps_limit_enabled:
            current_time = time.perf_counter()
            if current_time < next_frame_time:
                sleep_time = next_frame_time - current_time
                if sleep_time > 0.0001:  # Only sleep if > 100us
                    time.sleep(sleep_time)
        if bm:
            bm.record("fps_sleep", _bm_fps_t)

        try:
            with cuda_stream:
                # Use per-process target dimensions from StreamConfig
                _bm_decode_t = bm.start() if bm else 0.0
                num_frames, decoded_frames = pool.decode_round(
                    decoder_idx,
                    frames_per_stream=active_burst,
                    target_h=target_h,
                    target_w=target_w,
                    benchmark_metrics=bm,
                )
                if bm:
                    bm.record("decode_round", _bm_decode_t)

                # Cameras that actually published this round (post-decimation);
                # drives the single per-round sync/commit below.
                written_cams: List[str] = []
                for (
                    cam_id,
                    tensor,
                    decode_timestamp_ns,
                    stream_type,
                    session_id,
                    session_start_ns,
                    rtp_timestamp,
                    src_w,
                    src_h,
                ) in decoded_frames:
                    # Lazy ring buffer creation for native-resolution cameras
                    try:
                        _maybe_create_lazy_ring_buffer(
                            cam_id,
                            tensor,
                            ring_buffers,
                            lazy_rb_cameras,
                            pool.gpu_id,
                            num_slots,
                            worker_id,
                            worker_status_queue=worker_status_queue,
                        )
                    except Exception as e:
                        local_errors += 1
                        _log_err_rate_limited(
                            f"lazy_rb:{cam_id}",
                            f"Worker {worker_id} lazy RB error for {cam_id}: {e}",
                        )
                        continue

                    if cam_id not in ring_buffers:
                        continue

                    try:
                        producer = ring_buffers[cam_id]
                        if not _validate_frame_shape(tensor, producer, target_h, target_w):
                            reconciled = _reconcile_or_drop_on_shape_mismatch(
                                cam_id,
                                tensor,
                                ring_buffers,
                                published_once,
                                pool.gpu_id,
                                num_slots,
                                worker_id,
                                worker_status_queue,
                                _log_err_rate_limited,
                            )
                            if reconciled is None:
                                local_errors += 1
                                continue
                            producer = reconciled

                        # Output cap (primary): per-camera phase accumulator keyed
                        # to this camera's source FPS yields a stable target-FPS
                        # average (no wall-clock jitter). Native decode already
                        # happened; this only decimates writes. F08: use the
                        # camera's aggregated max(min_fps) when present, else the
                        # worker-global cap (MATRICE_OUTPUT_FPS / default).
                        #
                        # NOTE: this gate is correct and deliberately unchanged.
                        # It was inert in production only because the value it
                        # was handed — StreamConfig.target_fps, via
                        # publish_fps_by_camera — carried the camera's SOURCE
                        # rate instead of app demand, so `source_fps <=
                        # target_fps` in _should_publish_frame passed every
                        # frame. The rate is now resolved by
                        # streaming_gateway_utils.resolve_publish_fps(); do NOT
                        # clamp to output_fps_target here, that would break the
                        # F08 contract that a declared min_fps above the global
                        # default is honoured.
                        #
                        # This caps PUBLISHES only. Decode still runs at the
                        # source rate by design (see the FPS-limiting comment
                        # above) — a decode-side cap that also saves GPU cycles
                        # is a deliberate follow-up, to be explored once this
                        # publish fix is measured in production.
                        cam_publish_fps = publish_fps_by_camera.get(cam_id) or output_fps_target
                        if not _should_publish_frame(
                            pub_acc,
                            cam_id,
                            pool.get_source_fps_for_camera(cam_id),
                            cam_publish_fps,
                        ):
                            continue
                        # Relaxed monotonic flood-guard (defense-in-depth): only
                        # trips if source FPS was mis-detected low. Set above the
                        # target so it never rejects an on-cadence publish. F08:
                        # derive the ceiling from this camera's publish rate so a
                        # camera whose min_fps exceeds the global cap is not clipped.
                        if safety_interval_ns > 0:
                            cam_safety_ns = (
                                int((1e9 / cam_publish_fps) / _OUTPUT_FPS_SAFETY_FACTOR)
                                if cam_publish_fps > 0
                                else safety_interval_ns
                            )
                            mono_now = time.monotonic_ns()
                            if not _should_write_frame(
                                last_write_ns,
                                cam_id,
                                0,  # timestamp gate disabled; accumulator owns the rate
                                0,
                                monotonic_ns=mono_now,
                                min_monotonic_interval_ns=cam_safety_ns,
                            ):
                                continue
                            last_write_ns[f"{cam_id}:mono"] = mono_now

                        # Pluggable frame-skip seam (default no-op). Runs before
                        # the write so skipped frames never enter `written_cams`
                        # and the per-round batched GPU sync stays intact.
                        if optimizer.optimize(cam_id, tensor) is None:
                            continue

                        _bm_write_t = bm.start() if bm else 0.0
                        # Pass native source dims so consumers can invert the letterbox
                        # geometry when mapping bboxes back to source coordinates.
                        # `_SUPPORTS_SRC_DIMS` caches capability detection so we only
                        # pay the TypeError once on older matrice_common versions.
                        if _SUPPORTS_SRC_DIMS:
                            try:
                                ring_buffers[cam_id].rb.write_frame_fast(
                                    tensor,
                                    sync=False,
                                    timestamp_ns=decode_timestamp_ns,
                                    rtp_timestamp=rtp_timestamp if rtp_timestamp is not None else 0,
                                    src_w=src_w,
                                    src_h=src_h,
                                )
                            except TypeError:
                                _disable_src_dims_support()
                                logger.warning(
                                    "matrice_common does not support src_w/src_h; "
                                    "bbox inverse-letterbox will be disabled downstream"
                                )
                                ring_buffers[cam_id].rb.write_frame_fast(
                                    tensor,
                                    sync=False,
                                    timestamp_ns=decode_timestamp_ns,
                                    rtp_timestamp=rtp_timestamp if rtp_timestamp is not None else 0,
                                )
                        else:
                            ring_buffers[cam_id].rb.write_frame_fast(
                                tensor,
                                sync=False,
                                timestamp_ns=decode_timestamp_ns,
                                rtp_timestamp=rtp_timestamp if rtp_timestamp is not None else 0,
                            )
                        if bm:
                            bm.record("ring_buffer_write", _bm_write_t)
                            bm_frames += 1
                        # Publish session info only when it changes (producer
                        # creation / RTSP reconnect) — not on every frame.
                        _maybe_publish_session_info(
                            ring_buffers[cam_id].rb,
                            cam_id,
                            session_id,
                            session_start_ns,
                            published_session,
                        )
                        local_frames += 1
                        frames_since_counter_update += 1
                        written_cams.append(cam_id)
                        # Pins this camera's ring geometry from here on.
                        published_once.add(cam_id)

                        if fps_limit_enabled:
                            next_frame_time += frame_interval

                    except Exception as e:
                        local_errors += 1
                        _log_err_rate_limited(
                            f"write:{cam_id}",
                            f"Worker {worker_id} write error for {cam_id}: {e}",
                        )

                if written_cams:
                    # Single GPU sync per decode round (not per camera), over the
                    # cameras that actually published this round (decimated frames
                    # excluded). All ring buffers share this worker's CUDA stream,
                    # so one event.record()+synchronize() flushes all pending writes.
                    _bm_sync_t = bm.start() if bm else 0.0
                    first_cam_id = written_cams[0]
                    if first_cam_id in ring_buffers:
                        ring_buffers[first_cam_id].rb.sync_writes()

                    # Update committed_idx for the other cameras that wrote.
                    # GPU sync already done above (shared stream). Just publish
                    # the index so consumers know these frames are safe to read.
                    seen = {first_cam_id}
                    for cam_id in written_cams[1:]:
                        if cam_id not in seen and cam_id in ring_buffers:
                            seen.add(cam_id)
                            ring_buffers[cam_id].rb.update_committed_idx()

                    if bm:
                        bm.record("gpu_sync", _bm_sync_t)

            if num_frames == 0:
                time.sleep(0.0001)
                continue

            if frames_since_counter_update >= counter_batch_size:
                _flush_shared_counters(
                    frame_counter,
                    shared_frame_count,
                    gpu_frame_count,
                    frames_since_counter_update,
                )
                frames_since_counter_update = 0

            # Periodic benchmark metrics logging
            if bm:
                _bm_now = time.perf_counter()
                if _bm_now - bm_last_log_time >= bm_log_interval:
                    _bm_elapsed = _bm_now - bm_last_log_time
                    breakdown = bm.get_breakdown_str(
                        f"SG Worker {worker_id} BENCHMARK METRICS (last {_bm_elapsed:.0f}s, {num_streams} streams)",
                        interval_seconds=_bm_elapsed,
                        total_items=bm_frames,
                        item_label="frames",
                    )
                    if breakdown:
                        logger.info(breakdown)
                    bm.reset()
                    bm_frames = 0
                    bm_last_log_time = _bm_now

        except Exception as e:
            local_errors += 1
            _log_err_rate_limited(
                "round",
                f"Worker {worker_id} error: {e}",
            )

    if frames_since_counter_update > 0:
        _flush_shared_counters(
            frame_counter,
            shared_frame_count,
            gpu_frame_count,
            frames_since_counter_update,
        )

    elapsed = time.perf_counter() - start_time
    result_queue.put(
        {
            "worker_id": worker_id,
            "decoder_idx": decoder_idx,
            "elapsed_sec": elapsed,
            "total_frames": local_frames,
            "total_errors": local_errors,
            "num_streams": len(camera_ids),
            "fps": local_frames / elapsed if elapsed > 0 else 0,
        }
    )


# =============================================================================
# Sub-process worker: one decoder per process for GIL-free parallelism
# =============================================================================


def _open_declared_rings(
    camera_configs: List["StreamConfig"],
    ring_buffers: Dict[str, DataBusProducer],
    num_slots: int,
    sub_id: Any,
    worker_status_queue: Optional[Any],
) -> Set[str]:
    """Eagerly open a ring per camera that declares a resolution.

    Each camera gets its OWN declared size. This deliberately does not fall back to
    ``camera_configs[0]``'s dims: borrowing a sibling's size both sized this camera's
    ring wrongly and denied it the native/lazy path it asked for by declaring nothing.
    ``0`` means native, and native is settled by the pre-flight pass once the source
    has been opened.

    The eager create plus an immediate ``producer_ready`` ACK is load-bearing, not
    incidental: ``_resolve_hotadd_resolution`` records that deferring ring creation to
    the first decoded frame is what made a slow hot-add miss the ACK deadline and get
    torn down and re-added in a loop. So the ACK goes out at the DECLARED size, before
    any source is opened, and the geometry is corrected afterwards.

    Returns the camera ids that declared nothing and so take the lazy path.
    """
    lazy: Set[str] = set()
    for config in camera_configs:
        cfg_w = config.width or 0
        cfg_h = config.height or 0
        if cfg_w <= 0 or cfg_h <= 0:
            lazy.add(config.camera_id)
            continue
        try:
            ring_buffers[config.camera_id] = _open_ring_producer(
                config.camera_id, config.gpu_id, num_slots, cfg_w, nv12_ring_height(cfg_h)
            )
            _ack_producer_ready(worker_status_queue, config.camera_id, config.gpu_id, lazy=False)
        except Exception as exc:
            logger.exception(
                f"Sub-process {sub_id}: producer creation failed for camera {config.camera_id}: {exc}",
            )
            _report_add_failed(worker_status_queue, config, f"producer init: {exc}", sub_id)
            # Skip this camera — don't add to ring_buffers.
    return lazy


def _report_add_failed(
    worker_status_queue: Optional[Any],
    config: "StreamConfig",
    reason: str,
    sub_id: Any,
) -> None:
    """Tell the parent one camera failed, so it acts per camera and not per GPU."""
    if worker_status_queue is None:
        return
    try:
        worker_status_queue.put_nowait(
            {
                "type": "add_failed",
                "camera_id": config.camera_id,
                "gpu_id": config.gpu_id,
                "reason": reason,
            }
        )
    except thread_queue.Full:
        logger.warning(f"Sub-process {sub_id}: status queue full, dropping add_failed for {config.camera_id}")
    except Exception:
        logger.debug("add_failed ACK put failed: %s", config.camera_id, exc_info=True)


def _preflight_reconcile_geometry(
    camera_configs: List["StreamConfig"],
    pool: Any,
    ring_buffers: Dict[str, DataBusProducer],
    num_slots: int,
    worker_status_queue: Optional[Any],
) -> None:
    """Settle every camera's decode target and ring geometry before frame one.

    Opening the source is the moment a camera's real resolution becomes knowable,
    and it is knowable for BOTH demuxers. It used to be logged here and then
    discarded, leaving the ring at whatever the config claimed — so a stale
    declared resolution meant every decoded frame failed its ring's shape check
    and the camera sat at 0 fps forever. Correcting it here, before the first
    decode, means nothing is dropped for a geometry disagreement and the frame
    counter never stalls; a stalled counter is what the manager watchdog reads as
    a dead GPU, and that read is what used to escalate a config typo into a
    restart loop.

    Returns nothing on purpose. The decode target is read back per frame from the
    camera's own ``StreamState`` via ``NVDECDecoderPool.stream_target_dims``; handing
    the decode loop a second copy of it is precisely the divergence that made the
    worker-global ``camera_configs[0]`` target wrong for every other camera.
    """
    for config in camera_configs:
        native = pool.get_native_dims_for_camera(config.camera_id)
        declared_w, declared_h = config.width or 0, config.height or 0
        if native is None:
            # Source reported no geometry: leave the declared target in place and
            # let the first decoded frame settle it.
            continue

        eff_w, eff_h = effective_frame_dims(declared_w, declared_h, native[0], native[1])
        logger.info(
            "%s: source %dx%d, declared %s, decoding and publishing at %dx%d.",
            config.camera_id,
            native[0],
            native[1],
            f"{declared_w}x{declared_h}" if declared_w > 0 and declared_h > 0 else "native",
            eff_w,
            eff_h,
        )
        if (declared_w, declared_h) != (eff_w, eff_h) and declared_w > 0 and declared_h > 0:
            logger.warning(
                "%s: declared %dx%d but the source sends %dx%d; decoding and publishing at "
                "%dx%d (never upsampled). The configured resolution is stale.",
                config.camera_id,
                declared_w,
                declared_h,
                native[0],
                native[1],
                eff_w,
                eff_h,
            )

        existing = ring_buffers.get(config.camera_id)
        if existing is None or ring_frame_dims(existing) == (eff_w, eff_h):
            continue
        _recreate_ring_at(
            config.camera_id,
            ring_buffers,
            config.gpu_id,
            num_slots,
            eff_w,
            eff_h,
            reason="source geometry differs from the configured size",
            worker_status_queue=worker_status_queue,
        )


def _sub_decode_process(
    sub_id: int,
    gpu_id: int,
    camera_configs: List[StreamConfig],
    duration_sec: float,
    result_queue,
    stop_event,
    burst_size: Optional[int] = None,
    num_slots: int = 64,
    target_fps: int = 0,
    shared_frame_count=None,
    gpu_frame_count=None,
    demuxer_type: str = "nvc",
    benchmark_mode: bool = False,
    worker_status_queue=None,
    optimizer_config: Optional[Dict[str, Any]] = None,
    output_fps_cap: float = DEFAULT_OUTPUT_FPS_CAP,
):
    """Single-decoder sub-process for GIL-free parallel decode.

    Each sub-process handles a subset of cameras with 1 NVDEC decoder.
    Having its own GIL means no contention with other decoders —
    PyNvVideoCodec.Decode() holds the GIL, so threads serialize.
    """
    # This is a spawn target: it inherits no faulthandler from the parent, and the
    # code below calls into PyNvVideoCodec/CuPy C extensions that can and do
    # SIGSEGV (e.g. nvc.CreateDemuxer on an rtsp:// URL). Without this a crash
    # leaves no traceback anywhere — the child becomes an unreaped zombie while
    # the manager still reports the GPU alive at 0 fps.
    try:
        faulthandler.enable()
    except Exception:  # a closed/replaced stderr must not kill decode
        logger.debug("faulthandler.enable() failed in decode sub-process %s", sub_id, exc_info=True)

    if not camera_configs:
        result_queue.put({"sub_id": sub_id, "total_frames": 0, "total_errors": 0})
        return

    def _emit_add_failed_for_all(reason: str) -> None:
        if worker_status_queue is None:
            return
        for _cfg in camera_configs:
            try:
                worker_status_queue.put_nowait(
                    {
                        "type": "add_failed",
                        "camera_id": _cfg.camera_id,
                        "gpu_id": _cfg.gpu_id,
                        "reason": reason,
                    }
                )
            except Exception:  # nosec B110
                pass

    if CUPY_AVAILABLE:
        cp.cuda.Device(gpu_id).use()

    # Connect to global frame counter (created by parent/main process)
    frame_counter = GlobalFrameCounter(is_producer=True)
    for _ in range(50):
        try:
            if os.path.exists(GlobalFrameCounter.SHM_PATH):
                frame_counter.connect()
                break
        except Exception:  # nosec B110
            pass
        time.sleep(0.1)

    # Bound before the try so the finally can always close/unlink them even if
    # setup raises early.
    pool = None
    ring_buffers: Dict[str, DataBusProducer] = {}

    # Graceful teardown: a SIGTERM (per-camera REMOVE / orchestrator terminate)
    # sets local_stop so the decode loop exits and the finally below closes AND
    # unlinks this sub's SHM — instead of a hard kill that orphans the segment.
    # The worker also stops when the shared orchestrator stop_event is set (full
    # shutdown), via _AnyStop.
    local_stop = threading.Event()
    _worker_stop = _AnyStop(local_stop, stop_event)
    try:
        signal.signal(signal.SIGTERM, lambda *_a: local_stop.set())
    except (ValueError, OSError):
        # Not the process main thread (shouldn't happen for a spawn target) —
        # rely on the shared stop_event + the manager-side SHM backstop.
        pass

    try:
        target_w = camera_configs[0].width or DEFAULT_FRAME_WIDTH
        target_h = camera_configs[0].height or DEFAULT_FRAME_HEIGHT

        # Detect codec for this subset
        codec = "h265" if camera_configs[0].codec == "h265" else "h264"
        pool = create_decoder_pool(1, gpu_id, demuxer_type, codec=codec)
        if pool.actual_pool_size == 0:
            _emit_add_failed_for_all("no NVDEC decoders available")
            result_queue.put(
                {
                    "sub_id": sub_id,
                    "error": "No decoders",
                    "total_frames": 0,
                    "total_errors": 1,
                }
            )
            return

        # Create ring buffers for this sub-process's cameras
        # (ring_buffers is pre-bound above so the finally can close them.)
        _lazy_rb_cameras: set = set()

        _lazy_rb_cameras |= _open_declared_rings(camera_configs, ring_buffers, num_slots, sub_id, worker_status_queue)

        # Assign streams with stagger
        _stagger_delay = 0.15
        for i, config in enumerate(camera_configs):
            pool.assign_stream(
                stream_id=i,
                camera_id=config.camera_id,
                video_path=config.video_path,
                # Each camera's own declared target; no sibling fallback (see the
                # ring-creation loop above for why).
                width=config.width or 0,
                height=config.height or 0,
                stream_type=config.stream_type,
                # Per-stream demuxer, not the pool default. StreamConfig resolves
                # RTSP to the gstreamer demuxer on purpose ("for ABSOLUTE RTP
                # timestamps"); dropping it here meant an RTSP camera could land on
                # the nvc demuxer, whose CreateDemuxer() segfaults on an rtsp:// URL
                # and takes the decode sub-process with it.
                #
                # `codec` is deliberately NOT forwarded: the decoder pool is created
                # for ONE codec (camera_configs[0]'s), so handing assign_stream a
                # different per-camera codec would mismatch the decoder rather than
                # fix anything. Mixed-codec sub-processes are a separate defect.
                demuxer_type=config.demuxer_type,
            )
            if _stagger_delay > 0 and i < len(camera_configs) - 1:
                time.sleep(_stagger_delay)

        logger.info(f"Sub-process {sub_id}: 1 {codec} decoder, {len(camera_configs)} streams on GPU {gpu_id}")

        _preflight_reconcile_geometry(
            camera_configs,
            pool,
            ring_buffers,
            num_slots,
            worker_status_queue,
        )

        # F08: per-camera publish rate = aggregated max(app min_fps), carried on
        # each StreamConfig.target_fps. Overrides the worker-global cap per camera.
        publish_fps_by_camera = {c.camera_id: float(c.target_fps) for c in camera_configs if (c.target_fps or 0) > 0}

        # Run decode loop directly (single thread, decoder_idx=0)
        sub_result_queue = thread_queue.Queue()

        nvdec_pool_worker(
            worker_id=sub_id,
            decoder_idx=0,
            pool=pool,
            ring_buffers=ring_buffers,
            frame_counter=frame_counter,
            duration_sec=duration_sec,
            result_queue=sub_result_queue,
            stop_event=_worker_stop,  # SIGTERM (per-sub) or shared orchestrator stop
            burst_size=burst_size,
            target_h=target_h,
            target_w=target_w,
            target_fps=target_fps,
            shared_frame_count=shared_frame_count,
            gpu_frame_count=gpu_frame_count,
            lazy_rb_cameras=_lazy_rb_cameras,
            num_slots=num_slots,
            benchmark_mode=benchmark_mode,
            worker_status_queue=worker_status_queue,
            optimizer_config=optimizer_config,
            output_fps_cap=output_fps_cap,
            publish_fps_by_camera=publish_fps_by_camera,
        )

        total_frames = 0
        total_errors = 0
        while not sub_result_queue.empty():
            r = sub_result_queue.get_nowait()
            total_frames += r.get("total_frames", 0)
            total_errors += r.get("total_errors", 0)

        result_queue.put(
            {
                "sub_id": sub_id,
                "total_frames": total_frames,
                "total_errors": total_errors,
            }
        )

    except Exception as e:
        logger.exception("Sub-process %s error: %s", sub_id, e)
        _emit_add_failed_for_all(f"sub-process crashed: {e}")
        result_queue.put({"sub_id": sub_id, "error": str(e), "total_frames": 0, "total_errors": 1})
    finally:
        # Always release GPU/ring-buffer handles — on normal end, on SIGTERM
        # (REMOVE), and on crash.
        try:
            if pool is not None:
                pool.close()
        except Exception:  # nosec B110 - teardown must not raise
            pass
        for _cam, _rb in list(ring_buffers.items()):
            try:
                _rb.close()
            except Exception:  # nosec B110
                pass
        # Unlink the SHM segments ONLY on a per-camera SIGTERM (local_stop) — i.e.
        # a genuine REMOVE where the camera is gone for good. Do NOT unlink when
        # stopping for the shared orchestrator stop_event (full shutdown /
        # watchdog restart) or on a crash: those segments are reused by the
        # replacement sub-processes, and unlinking here would race the new
        # producer and leave consumers with ENOENT. SIGKILL after the terminate
        # grace bypasses this; remove_camera()'s _clean_stale_shm_for backstop
        # reaps that case.
        if local_stop.is_set():
            _unlinked = 0
            for _cfg in camera_configs:
                _unlinked += _unlink_camera_shm(_cfg.camera_id)
            if _unlinked:
                logger.info("Sub-process %s: unlinked %d SHM segment(s) on REMOVE", sub_id, _unlinked)


# =============================================================================
# GPU Process — helpers
# =============================================================================


def _exit_signal_note(exit_code: Optional[int]) -> str:
    """`` (SIGSEGV)``-style suffix for a negative exit code, else empty.

    Mirrors ``NVDECWorkerManager._format_exit_signal``; duplicated rather than
    imported because that lives in the manager module, which imports this one.
    """
    if exit_code is None or exit_code >= 0:
        return ""
    try:
        return f" ({signal.Signals(-exit_code).name})"
    except (ValueError, AttributeError):
        return f" (signal {-exit_code})"


def _reap_dead_subprocesses(
    procs: List[Any],
    sub_registry: "_SubprocessCameraRegistry",
    already_reaped: Set[int],
    process_id: Any,
    worker_status_queue: Optional[Any] = None,
) -> List[str]:
    """Reap decode sub-processes that died after start-up. Returns their cameras.

    The ADD path polls ``exitcode`` once, immediately after spawn, which only
    catches a failure between ``start()`` and that line. A crash a second later —
    a SIGSEGV inside PyNvVideoCodec or CuPy, which does happen — left the child an
    unreaped zombie while this orchestrator stayed alive and reported the GPU
    healthy at 0 fps. Nothing noticed until the manager's frame-stall watchdog
    fired (``FRAME_STALL_THRESHOLD_SEC``, 120s by default) and restarted the WHOLE
    GPU worker, wiping SHM for every camera on it; three of those inside the
    circuit-breaker window used to abandon the GPU permanently.

    So: reap it, name it with its signal, and report each of its cameras as
    ``add_failed`` — the per-camera signal the manager already knows how to act
    on. ``already_reaped`` is updated in place so a corpse that lingers in
    ``procs`` cannot re-report on every call.
    """
    lost: List[str] = []
    for proc in list(procs):
        try:
            if proc.is_alive():
                continue
        except Exception:  # a torn-down handle counts as dead
            logger.debug("Process %s: liveness probe failed on a sub-process", process_id, exc_info=True)
        key = id(proc)
        if key in already_reaped:
            continue
        already_reaped.add(key)
        exit_code = getattr(proc, "exitcode", None)
        signal_note = _exit_signal_note(exit_code)
        owned = sub_registry.configs_for_owner(proc)
        cam_names = ", ".join(c.camera_id for c in owned) or "no registered cameras"
        logger.error(
            "Process %s: decode sub-process died (exitcode=%s%s), cameras: %s. Reaping and "
            "reporting them failed so the manager can act per-camera instead of waiting for "
            "the frame-stall watchdog to restart this GPU.",
            process_id,
            exit_code,
            signal_note,
            cam_names,
        )
        try:
            proc.join(timeout=1.0)  # reap: no zombie left behind
        except Exception:  # already dead; nothing to salvage
            logger.debug("Process %s: join of a dead sub-process failed", process_id, exc_info=True)
        for cfg in owned:
            lost.append(cfg.camera_id)
            if worker_status_queue is None:
                continue
            try:
                worker_status_queue.put_nowait(
                    {
                        "type": "add_failed",
                        "camera_id": cfg.camera_id,
                        "gpu_id": cfg.gpu_id,
                        "reason": f"decode sub-process died (exitcode={exit_code}{signal_note})",
                    }
                )
            except thread_queue.Full:
                logger.warning(
                    "Process %s: status queue full, dropping add_failed for %s",
                    process_id,
                    cfg.camera_id,
                )
            except Exception:
                logger.debug("add_failed put failed: %s", cfg.camera_id, exc_info=True)
    return lost


def _run_report_hook(on_report: Optional[Callable[[], None]], gpu_id: int) -> None:
    """Call the progress-monitor's per-tick hook, never letting it kill the loop.

    The hook is how dead decode sub-processes get reaped on the same cadence the
    orchestrator already reports progress on, so a raising hook must not be able to
    stop progress reporting -- that would silence the very loop that notices a wedge.
    """
    if on_report is None:
        return
    try:
        on_report()
    except Exception:  # never lose the loop to a hook
        logger.debug("GPU %s: progress-report hook raised", gpu_id, exc_info=True)


def _monitor_gpu_progress(
    stop_event: Any,
    duration_sec: float,
    gpu_id: int,
    gpu_frame_count: Any,
    shared_frame_count: Any,
    num_gpu_streams: int,
    total_num_streams: int,
    total_num_gpus: int,
    live_stream_count: Optional[Callable[[], int]] = None,
    on_report: Optional[Callable[[], None]] = None,
) -> None:
    """Progress monitoring loop with current/avg FPS tracking.

    ``num_gpu_streams`` is the spawn-time camera count; when cameras are
    hot-added/removed it goes stale, making the per-camera FPS figures and the
    "(N cams)" label wrong. ``live_stream_count`` (when provided) is polled each
    report to reflect the current count instead.

    ``on_report`` runs once per report interval. This loop is the orchestrator's
    only wait point, so it is also the only place that can notice a decode
    sub-process that died after start-up; the caller uses the hook to reap them.
    Exceptions from it are logged and swallowed — losing the progress log because
    a supervision callback raised would be a poor trade.
    """
    start_time = time.perf_counter()
    last_report_time = start_time
    last_gpu_fc = 0
    last_global_fc = 0
    report_interval = 5.0
    proc_start_time: Optional[float] = None
    gpu_fc_at_start = 0
    global_fc_at_start = 0

    while not stop_event.is_set():  # type: ignore[attr-defined]
        current_time = time.perf_counter()
        if current_time - start_time >= duration_sec:
            break

        if current_time - last_report_time >= report_interval:
            elapsed = current_time - start_time
            remaining = max(0, duration_sec - elapsed)

            # Live per-GPU camera count (falls back to the spawn-time count).
            n_streams = num_gpu_streams
            if live_stream_count is not None:
                try:
                    live = live_stream_count()
                    if live and live > 0:
                        n_streams = live
                except Exception:  # nosec B110 - display metric, never fatal
                    pass

            gpu_frames = gpu_frame_count.value if gpu_frame_count else 0
            gpu_int_frames = gpu_frames - last_gpu_fc
            gpu_int_fps = gpu_int_frames / report_interval
            gpu_ps_fps = gpu_int_fps / n_streams if n_streams > 0 else 0

            global_frames = shared_frame_count.value if shared_frame_count else 0  # type: ignore[union-attr,attr-defined]
            global_int_frames = global_frames - last_global_fc
            global_int_fps = global_int_frames / report_interval
            global_ps_fps = global_int_fps / total_num_streams if total_num_streams > 0 else 0

            if proc_start_time is None and gpu_frames > 0:
                proc_start_time = last_report_time
                gpu_fc_at_start = last_gpu_fc
                global_fc_at_start = last_global_fc

            if proc_start_time is not None:
                proc_elapsed = current_time - proc_start_time
                gpu_avg_fps = (gpu_frames - gpu_fc_at_start) / proc_elapsed if proc_elapsed > 0 else 0
                gpu_avg_ps = gpu_avg_fps / n_streams if n_streams > 0 else 0
                global_avg_fps = (global_frames - global_fc_at_start) / proc_elapsed if proc_elapsed > 0 else 0
                global_avg_ps = global_avg_fps / total_num_streams if total_num_streams > 0 else 0

                logger.info(
                    f"GPU{gpu_id} [{elapsed:5.1f}s] {gpu_frames:,} frames ({n_streams} cams) | "
                    f"cur: {gpu_int_fps:,.0f} FPS ({gpu_ps_fps:.1f}/cam) | "
                    f"avg: {gpu_avg_fps:,.0f} FPS ({gpu_avg_ps:.1f}/cam)"
                )

                if gpu_id == 0:
                    logger.info(
                        f"GLOBAL [{elapsed:5.1f}s] {global_frames:,} frames "
                        f"({total_num_streams} cams, {total_num_gpus} GPUs) | "
                        f"cur: {global_int_fps:,.0f} FPS ({global_ps_fps:.1f}/cam) | "
                        f"avg: {global_avg_fps:,.0f} FPS ({global_avg_ps:.1f}/cam) | "
                        f"{remaining:.0f}s left"
                    )

            last_gpu_fc = gpu_frames
            last_global_fc = global_frames
            last_report_time = current_time

            _run_report_hook(on_report, gpu_id)

        time.sleep(0.1)


# =============================================================================
# GPU Process
# =============================================================================


def nvdec_pool_process(
    process_id: int,
    camera_configs: List[StreamConfig],
    pool_size: int,
    duration_sec: float,
    result_queue: mp.Queue,
    stop_event: mp.Event,  # type: ignore[valid-type]
    burst_size: Optional[int] = None,
    num_slots: int = 64,
    target_fps: int = 0,
    shared_frame_count: Optional[mp.Value] = None,  # type: ignore[valid-type]
    gpu_frame_counts: Optional[Dict[int, mp.Value]] = None,  # type: ignore[valid-type]
    total_num_streams: int = 0,
    total_num_gpus: int = 1,
    demuxer_type: str = "nvc",
    benchmark_mode: bool = False,
    command_queue: Optional[mp.Queue] = None,
    worker_status_queue: Optional[mp.Queue] = None,
    optimizer_config: Optional[Dict[str, Any]] = None,
    output_fps_cap: float = DEFAULT_OUTPUT_FPS_CAP,
):
    """NVDEC process for one GPU.

    Creates NV12 ring buffers: (H*1.5, W) = 0.6 MB/frame.

    Args:
        gpu_frame_counts: Dict mapping gpu_id -> per-GPU frame counter (for per-GPU stats)
        shared_frame_count: Global frame counter (for overall stats)
        total_num_streams: Total streams across ALL GPUs (for global per-stream calc)
        total_num_gpus: Total number of GPUs (for context in logging)
        demuxer_type: Demuxer backend ("nvc" or "gstreamer")
        benchmark_mode: Enable granular per-stage timing
    """
    if not camera_configs:
        return

    gpu_id = camera_configs[0].gpu_id
    target_w = camera_configs[0].width or DEFAULT_FRAME_WIDTH
    target_h = camera_configs[0].height or DEFAULT_FRAME_HEIGHT
    nv12_h = target_h + target_h // 2  # NV12: Y plane (H) + UV plane (H/2)

    # Get per-GPU counter (or fall back to shared if not provided)
    gpu_frame_count: Any = gpu_frame_counts.get(gpu_id) if gpu_frame_counts else None

    if CUPY_AVAILABLE:
        cp.cuda.Device(gpu_id).use()

    # Connect to global frame counter (created by main process)
    frame_counter = GlobalFrameCounter(is_producer=True)
    max_retries = 50
    for retry in range(max_retries):
        try:
            if os.path.exists(GlobalFrameCounter.SHM_PATH):
                frame_counter.connect()
                logger.info(f"Process {process_id}: Connected to GlobalFrameCounter")
                break
        except Exception:
            if retry == max_retries - 1:
                raise
        time.sleep(0.1)
    else:
        raise RuntimeError(f"Process {process_id}: GlobalFrameCounter not found")

    # Use multi-process decode: each decoder runs in its own process with its own GIL.
    # PyNvVideoCodec.Decode() holds the GIL, so threads serialize and are slower.
    # Separate processes bypass GIL contention entirely.
    frame_size_mb = target_w * nv12_h * 1 / 1e6 if target_w > 0 else 0
    total_decoders = min(pool_size, len(camera_configs))

    # Pre-bind so the finally can always signal + terminate sub-processes, even
    # if setup below raises before they are assigned.
    threads: List[Any] = []
    cmd_handler_stop = None
    try:
        logger.warning(
            f"Process {process_id}: spawning {total_decoders} sub-processes, "
            f"{len(camera_configs)} streams, NV12 ({frame_size_mb:.1f} MB/frame)"
        )

        # Split cameras across sub-processes
        chunk_size = len(camera_configs) // total_decoders
        extra = len(camera_configs) % total_decoders

        sub_ctx = mp.get_context("spawn")
        sub_result_queue = sub_ctx.Queue()
        thread_result_queue = sub_result_queue  # alias for result collection below

        threads = []  # actually sub-processes, aliased for monitoring loop compatibility
        # Track which sub-process owns which camera so REMOVE/UPDATE can target it.
        # Mutated by both main thread (boot spawn) and command-handler thread (runtime
        # ADD/REMOVE), so all accesses MUST hold _sub_lock.
        sub_registry = _SubprocessCameraRegistry()
        _sub_lock = threading.Lock()
        # Counter for unique sub_id when hot-spawning new sub-processes at runtime.
        next_sub_idx = total_decoders

        cam_idx = 0
        for sub_idx in range(total_decoders):
            n = chunk_size + (1 if sub_idx < extra else 0)
            sub_configs = camera_configs[cam_idx : cam_idx + n]
            cam_idx += n

            p = sub_ctx.Process(
                target=_sub_decode_process,
                args=(
                    process_id * 100 + sub_idx,
                    gpu_id,
                    sub_configs,
                    duration_sec,
                    sub_result_queue,
                    stop_event,
                    burst_size,
                    num_slots,
                    target_fps,
                    shared_frame_count,
                    gpu_frame_count,
                    demuxer_type,
                    benchmark_mode,
                    worker_status_queue,
                    optimizer_config,
                    output_fps_cap,
                ),
            )
            p.start()
            threads.append(p)
            with _sub_lock:
                sub_registry.register(p, sub_configs)
            time.sleep(0.05)  # Small stagger to avoid SHM creation races

        # ----------------------------------------------------------------------
        # Dynamic ADD/REMOVE/UPDATE handler thread.
        # Polls command_queue (sent by NVDECWorkerManager._send_worker_command)
        # and hot-spawns / terminates per-camera sub-processes without disturbing
        # already-running streams. Daemon thread so it dies with the parent
        # nvdec_pool_process when the gateway stops.
        # ----------------------------------------------------------------------
        cmd_handler_stop = threading.Event()

        def _spawn_for_camera(cfg: StreamConfig) -> Optional[mp.Process]:
            """Spawn a single-camera _sub_decode_process and register it.

            Caller MUST hold _sub_lock so the registry stays consistent.

            Returns the process, or None if it exited before it could be
            registered (in which case an ``add_failed`` status has already been
            emitted for the camera).
            """
            nonlocal next_sub_idx
            new_sub_id = process_id * 100 + next_sub_idx
            next_sub_idx += 1
            new_p = sub_ctx.Process(
                target=_sub_decode_process,
                args=(
                    new_sub_id,
                    gpu_id,
                    [cfg],
                    duration_sec,
                    sub_result_queue,
                    stop_event,
                    burst_size,
                    num_slots,
                    target_fps,
                    shared_frame_count,
                    gpu_frame_count,
                    demuxer_type,
                    benchmark_mode,
                    worker_status_queue,
                    optimizer_config,
                    output_fps_cap,
                ),
            )
            try:
                new_p.start()
            except Exception as _start_exc:
                # start() can raise (e.g. OSError under fd/resource exhaustion)
                # before the exitcode poll below. The REMOVE/UPDATE sibling loops
                # call this unguarded, so a raise here would skip the remaining
                # siblings (and the UPDATE target) and emit no add_failed. Convert
                # it to the same clean failure the immediate-exit path uses.
                logger.exception(
                    f"Process {process_id}: failed to start sub-process for camera {cfg.camera_id}: {_start_exc}"
                )
                if worker_status_queue is not None:
                    try:
                        worker_status_queue.put_nowait(
                            {
                                "type": "add_failed",
                                "camera_id": cfg.camera_id,
                                "gpu_id": gpu_id,
                                "reason": f"spawn start failed: {_start_exc}",
                            }
                        )
                    except Exception:  # nosec B110 - status queue is best-effort
                        pass
                return None

            # A sub-process that is already dead must NOT be registered as the
            # camera's owner: `owner_for(cam) is not None` makes the command
            # handler short-circuit every later ADD with
            # producer_ready(already_running=True), so the manager gets ACKed for
            # a producer that does not exist and the camera can never recover.
            #
            # This is a NON-BLOCKING poll on purpose (`exitcode`, not
            # `join(timeout)`): a healthy sub-process never exits, so any grace
            # period would be paid in full by every spawn and bulk-adding 200
            # cameras would serialize that cost in this handler thread. It
            # therefore only catches a process that died between start() and here
            # (e.g. fork/exec failure). A crash slightly later during CUDA or
            # decoder init is handled by the manager's bounded hot-add retry,
            # which now tears the worker-side camera down before each attempt.
            if new_p.exitcode is not None:
                logger.error(
                    f"Process {process_id}: sub-process {new_sub_id} for camera "
                    f"{cfg.camera_id} exited immediately (exitcode={new_p.exitcode}); "
                    f"not registering it as owner"
                )
                # Report a clean failure so the manager retries instead of
                # waiting out the full producer_ready timeout. The ADD caller's
                # own except-branch does not fire (we do not raise), so this is
                # the only notification — and it must not be skipped.
                if worker_status_queue is not None:
                    try:
                        worker_status_queue.put_nowait(
                            {
                                "type": "add_failed",
                                "camera_id": cfg.camera_id,
                                "gpu_id": gpu_id,
                                "reason": f"sub-process exited immediately (exitcode={new_p.exitcode})",
                            }
                        )
                    except Exception:  # nosec B110 - status queue is best-effort
                        pass
                # Return None rather than raising: the REMOVE/UPDATE paths spawn
                # siblings in a loop, and one bad camera must not skip the rest.
                return None

            threads.append(new_p)
            sub_registry.register(new_p, [cfg])
            logger.warning(
                f"Process {process_id}: hot-spawned sub-process {new_sub_id} for camera {cfg.camera_id} on GPU {gpu_id}"
            )
            return new_p

        def _terminate_subprocess(owner: mp.Process, cam_id: str) -> None:
            """Best-effort termination for a sub-process owner.

            Also prunes the (now-dead) owner from the `threads` list so it
            does not accumulate across many UPDATE/REMOVE cycles. Without
            this, a long-running gateway with frequent reconfigurations
            would keep references to terminated mp.Process objects and
            spend the shutdown grace-period joining them needlessly.
            """
            if not _terminate_subprocess_owner(owner, logger, process_id, cam_id):
                logger.warning(
                    f"Process {process_id}: sub-process for camera {cam_id} remained alive after kill escalation"
                )
            try:
                threads.remove(owner)
            except ValueError:
                # Already pruned (e.g. previous UPDATE detached the same owner).
                pass

        def _emit_removed(cam_id: str, owned: bool) -> None:
            """ACK a REMOVE back to the manager so it need not blind-timeout.

            ``owned=False`` means this GPU never owned the camera (already gone,
            or routed here by mistake); the manager treats both as "stopped here"
            and relies on its SHM backstop to reap any orphan.
            """
            if worker_status_queue is None:
                return
            try:
                worker_status_queue.put_nowait(
                    {
                        "type": "removed",
                        "camera_id": cam_id,
                        "gpu_id": gpu_id,
                        "owned": owned,
                    }
                )
            except Exception:  # nosec B110 - status queue is best-effort
                pass

        def _command_handler():
            """Poll command_queue and dispatch ADD/REMOVE/UPDATE."""
            if command_queue is None:
                return
            _last_hb = 0.0
            _last_qerr_log = 0.0
            while not cmd_handler_stop.is_set() and not stop_event.is_set():
                # Liveness heartbeat: lets the manager/watchdog detect a wedged
                # handler even while the process is alive and cameras decode.
                _now_hb = time.monotonic()
                if worker_status_queue is not None and _now_hb - _last_hb >= _HANDLER_HEARTBEAT_SEC:
                    _last_hb = _now_hb
                    try:
                        worker_status_queue.put_nowait({"type": "handler_alive", "gpu_id": gpu_id})
                    except Exception:  # nosec B110
                        pass
                try:
                    cmd = command_queue.get(timeout=0.5)
                except thread_queue.Empty:
                    continue
                except (EOFError, OSError) as e:
                    if cmd_handler_stop.is_set() or stop_event.is_set():
                        return  # genuine shutdown
                    # Transient/broken read while still running: do NOT exit
                    # permanently — that silently wedges every add/remove/update
                    # for this GPU with no crash and no watchdog restart. Log
                    # rate-limited and keep polling; the heartbeat above lets the
                    # manager detect a handler that is genuinely stuck.
                    if _now_hb - _last_qerr_log >= 30.0:
                        _last_qerr_log = _now_hb
                        logger.warning(f"Process {process_id}: command_queue read error ({e}); continuing")
                    time.sleep(0.5)
                    continue
                except Exception as e:  # pragma: no cover - defensive
                    logger.exception(f"Process {process_id}: command_queue error: {e}")
                    continue

                try:
                    cmd_type = (cmd or {}).get("type")
                    if cmd_type == "add":
                        cfg = cmd.get("config")
                        if cfg is None or getattr(cfg, "camera_id", None) is None:
                            logger.error(f"Process {process_id}: add command missing config")
                            if worker_status_queue is not None and cfg is not None:
                                try:
                                    worker_status_queue.put_nowait(
                                        {
                                            "type": "add_failed",
                                            "camera_id": getattr(cfg, "camera_id", None),
                                            "gpu_id": gpu_id,
                                            "reason": "missing or invalid config",
                                        }
                                    )
                                except Exception:  # nosec B110
                                    pass
                            continue
                        # Split-brain guard: only ACK "already running" when a
                        # LIVE producer actually exists. A registry entry whose
                        # sub-process has died, or whose SHM was reaped, must NOT
                        # short-circuit to producer_ready — that ACKs the manager
                        # for a producer that isn't there and the camera never
                        # recovers. In that case tear the stale owner down and
                        # fall through to a genuine spawn.
                        _shm_frames = f"/dev/shm/databus__{cfg.camera_id}__sg__frames"  # nosec B108
                        stale_owner = None
                        with _sub_lock:
                            existing_owner = sub_registry.owner_for(cfg.camera_id)
                            if existing_owner is not None:
                                _alive = bool(getattr(existing_owner, "is_alive", lambda: False)())
                                _shm_ok = os.path.exists(_shm_frames)
                                if _alive and _shm_ok:
                                    logger.info(
                                        f"Process {process_id}: ADD ignored — camera {cfg.camera_id} already running"
                                    )
                                    if worker_status_queue is not None:
                                        try:
                                            worker_status_queue.put_nowait(
                                                {
                                                    "type": "producer_ready",
                                                    "camera_id": cfg.camera_id,
                                                    "gpu_id": gpu_id,
                                                    "lazy": False,
                                                    "already_running": True,
                                                }
                                            )
                                        except Exception:  # nosec B110
                                            pass
                                    continue
                                # Stale owner: detach now, terminate outside the
                                # lock (terminate can take seconds), then respawn.
                                logger.warning(
                                    f"Process {process_id}: ADD for {cfg.camera_id} found a stale owner "
                                    f"(alive={_alive}, shm={_shm_ok}); respawning instead of false-ACK"
                                )
                                stale_owner, _ = sub_registry.detach_owner_for_camera(cfg.camera_id)
                                sub_registry.remove_config(cfg.camera_id)
                        if stale_owner is not None:
                            _terminate_subprocess(stale_owner, cfg.camera_id)
                        # Genuine spawn (fresh add or post-stale respawn).
                        # _spawn_for_camera no longer raises from start(); the
                        # guard here remains as defense in depth.
                        with _sub_lock:
                            try:
                                _spawn_for_camera(cfg)
                            except Exception as _spawn_exc:
                                logger.exception(
                                    f"Process {process_id}: spawn failed for camera {cfg.camera_id}: {_spawn_exc}",
                                )
                                if worker_status_queue is not None:
                                    try:
                                        worker_status_queue.put_nowait(
                                            {
                                                "type": "add_failed",
                                                "camera_id": cfg.camera_id,
                                                "gpu_id": gpu_id,
                                                "reason": f"spawn: {_spawn_exc}",
                                            }
                                        )
                                    except Exception:  # nosec B110
                                        pass
                    elif cmd_type == "remove":
                        cam_id = cmd.get("camera_id")
                        with _sub_lock:
                            owner, owned_configs = sub_registry.detach_owner_for_camera(cam_id)
                            sub_registry.remove_config(cam_id)
                            sibling_configs = [cfg for cid, cfg in owned_configs.items() if cid != cam_id]
                        if owner is None:
                            logger.info(f"Process {process_id}: REMOVE noop — camera {cam_id} not owned by this GPU")
                            _emit_removed(cam_id, owned=False)
                            continue
                        _terminate_subprocess(owner, cam_id)
                        if sibling_configs:
                            with _sub_lock:
                                for sibling_cfg in sibling_configs:
                                    _spawn_for_camera(sibling_cfg)
                        logger.warning(f"Process {process_id}: stopped sub-process for camera {cam_id}")
                        _emit_removed(cam_id, owned=True)
                    elif cmd_type == "update":
                        cam_id = cmd.get("camera_id")
                        cfg = cmd.get("config")
                        if cfg is None:
                            continue
                        with _sub_lock:
                            owner, owned_configs = sub_registry.detach_owner_for_camera(cam_id)
                            sibling_configs = [
                                existing_cfg for cid, existing_cfg in owned_configs.items() if cid != cam_id
                            ]
                        if owner is not None:
                            _terminate_subprocess(owner, cam_id)
                        with _sub_lock:
                            for sibling_cfg in sibling_configs:
                                _spawn_for_camera(sibling_cfg)
                            _spawn_for_camera(cfg)
                        logger.warning(f"Process {process_id}: re-spawned sub-process for updated camera {cam_id}")
                    elif cmd_type == "stop":
                        return
                    else:
                        logger.warning(f"Process {process_id}: unknown command type {cmd_type!r}")
                except Exception as e:  # pragma: no cover - defensive
                    logger.exception(f"Process {process_id}: command handler error: {e}")

        cmd_thread = threading.Thread(
            target=_command_handler,
            name=f"nvdec-cmd-handler-gpu{gpu_id}",
            daemon=True,
        )
        cmd_thread.start()

        start_time = time.perf_counter()
        # Corpses already reported, keyed by id(proc), so a sub-process that
        # lingers in `threads` is not re-reported on every progress tick.
        _reaped_subs: Set[int] = set()

        def _reap_subs() -> None:
            _reap_dead_subprocesses(threads, sub_registry, _reaped_subs, process_id, worker_status_queue)

        _monitor_gpu_progress(
            stop_event=stop_event,
            duration_sec=duration_sec,
            gpu_id=gpu_id,
            gpu_frame_count=gpu_frame_count,
            shared_frame_count=shared_frame_count,
            num_gpu_streams=len(camera_configs),
            total_num_streams=total_num_streams,
            total_num_gpus=total_num_gpus,
            # Live count so per-camera FPS tracks cameras hot-added/removed after
            # spawn, instead of the stale spawn-time len(camera_configs).
            live_stream_count=sub_registry.active_camera_count,
            # The ADD path only polls exitcode once, right after spawn. This tick
            # is what catches a decode child that segfaults later on.
            on_report=_reap_subs,
        )

        # Signal sub-processes to stop and wait
        stop_event.set()
        cmd_handler_stop.set()
        # Best-effort: nudge the command handler past its blocking get().
        if command_queue is not None:
            try:
                command_queue.put_nowait({"type": "stop"})
            except Exception:  # nosec B110
                pass
        cmd_thread.join(timeout=2.0)

        for t in threads:
            t.join(timeout=30.0)

        total_frames = 0
        total_errors = 0
        elapsed = time.perf_counter() - start_time

        # Collect results from sub-processes
        while not thread_result_queue.empty():
            try:
                r = thread_result_queue.get_nowait()
                total_frames += r.get("total_frames", 0)
                total_errors += r.get("total_errors", 0)
            except Exception:
                break

        # Ring buffers and pools are owned and closed by sub-processes

        result_queue.put(
            {
                "process_id": process_id,
                "elapsed_sec": elapsed,
                "total_frames": total_frames,
                "total_errors": total_errors,
                "num_streams": len(camera_configs),
                "pool_size": total_decoders,
                "fps": total_frames / elapsed if elapsed > 0 else 0,
                "per_stream_fps": total_frames / elapsed / max(len(camera_configs), 1) if elapsed > 0 else 0,
            }
        )

    except Exception as e:
        logger.exception("Process %s error: %s", process_id, e)

        result_queue.put(
            {
                "process_id": process_id,
                "error": str(e),
                "total_frames": 0,
                "total_errors": 1,
            }
        )

    finally:
        # Ensure decode sub-processes are signalled + terminated even on the
        # error path — a crashing orchestrator must not leave orphaned producers
        # writing stale SHM (the "SG logs FPS, IE sees ENOENT" split brain).
        # stop_event is watched by each sub (via _AnyStop) and terminate() sends
        # SIGTERM, both of which trigger the sub's graceful self-clean (close +
        # SHM unlink). Idempotent on the normal path where this already ran.
        try:
            stop_event.set()
        except Exception:  # nosec B110
            pass
        if cmd_handler_stop is not None:
            try:
                cmd_handler_stop.set()
            except Exception:  # nosec B110
                pass
        for _t in list(threads):
            try:
                if hasattr(_t, "terminate") and _t.is_alive():
                    _t.terminate()
            except Exception:  # nosec B110
                pass
        for _t in list(threads):
            try:
                _t.join(timeout=5.0)
            except Exception:  # nosec B110
                pass

        # Drive the canonical CUDA teardown sequence before returning so the
        # GPU driver releases its dmabufs proactively. Without this, on
        # Jetson Thor unified memory the pages stay tied to inode references
        # and only ``drop_caches=2`` reclaims them.
        try:
            from matrice_common.lifecycle import finalize_cuda  # type: ignore

            finalize_cuda(device_id=gpu_id)
        except Exception:  # noqa: BLE001
            # Older py_common builds lack finalize_cuda; fall back to the
            # in-tree warmup pattern so we still flush the default pool.
            try:
                if CUPY_AVAILABLE:
                    cp.cuda.Device(gpu_id).synchronize()
                    cp.get_default_memory_pool().free_all_blocks()
            except Exception:  # nosec B110
                pass


# =============================================================================
# Streaming Gateway
# =============================================================================


class StreamingGateway:
    """Multi-stream video producer outputting NV12 tensors (minimal IPC payload)."""

    def __init__(self, config: GatewayConfig):
        self.config = config
        self._workers: List[mp.Process] = []
        self._stop_event = mp.Event()
        # Pre-existing on this line and deliberately left unbounded HERE: 2.x bounds it
        # as `mp.Queue(maxsize=DEFAULT_IPC_RESULT_QUEUE_MAXSIZE)`, but it did so together
        # with the drain logic and tests that keep a full queue from blocking `put` and
        # wedging a worker. Adding the bound alone would trade an unbounded-growth risk
        # for a deadlock risk. Tracked as a follow-up, not smuggled into a timestamp fix.
        # nosemgrep: py-unbounded-multiprocessing-queue
        self._result_queue = mp.Queue()  # type: ignore[var-annotated]

    def start(self) -> Dict:
        """Start the gateway."""
        if not CUPY_AVAILABLE:
            raise RuntimeError("CuPy is required")
        if not RING_BUFFER_AVAILABLE:
            raise RuntimeError("CUDA IPC ring buffer not available")
        if not PYNVCODEC_AVAILABLE:
            raise RuntimeError("PyNvVideoCodec required")
        return self._start_nvdec_pool()

    def _start_nvdec_pool(self) -> Dict:
        """Start NVDEC pool across GPUs."""
        num_gpus = max(min(self.config.num_gpus, 8), 1)
        streams_per_gpu = self.config.num_streams // num_gpus
        extra_streams = self.config.num_streams % num_gpus

        logger.info(
            f"Starting NVDEC on {num_gpus} GPU(s): {self.config.num_streams} streams, "
            f"pool_size={self.config.nvdec_pool_size}/GPU, output=NV12 (0.6 MB)"
        )

        ctx = mp.get_context("spawn")
        self._stop_event = ctx.Event()
        self._result_queue = ctx.Queue()

        # Shared counter for real-time FPS tracking (use 'L' for large counts)
        shared_frame_count = ctx.Value("L", 0)

        # Per-GPU counters for detailed stats
        gpu_frame_counts = {gpu_id: ctx.Value("L", 0) for gpu_id in range(num_gpus)}

        stream_idx = 0
        for gpu_id in range(num_gpus):
            n_streams = streams_per_gpu + (1 if gpu_id < extra_streams else 0)

            gpu_configs = []
            for _ in range(n_streams):
                config = StreamConfig(
                    camera_id=f"cam_{stream_idx:04d}",
                    video_path=self.config.video_path,
                    width=self.config.frame_width,
                    height=self.config.frame_height,
                    target_fps=self.config.target_fps,
                    gpu_id=gpu_id,
                )
                gpu_configs.append(config)
                stream_idx += 1

            p = ctx.Process(
                target=nvdec_pool_process,
                args=(
                    gpu_id,
                    gpu_configs,
                    self.config.nvdec_pool_size,
                    self.config.duration_sec,
                    self._result_queue,
                    self._stop_event,
                    self.config.nvdec_burst_size,
                    self.config.num_slots,
                    self.config.target_fps,
                    shared_frame_count,
                    gpu_frame_counts,
                    self.config.num_streams,
                    num_gpus,
                    self.config.demuxer_type,
                    self.config.benchmark_mode,
                ),
                kwargs={"optimizer_config": self.config.optimizer_config},
            )
            p.start()
            self._workers.append(p)  # type: ignore[arg-type]
            logger.info(f"GPU {gpu_id}: {n_streams} streams")
            time.sleep(0.1)

        # Progress monitoring loop - print progress every 5 seconds
        start_time = time.perf_counter()
        last_report_time = start_time
        last_frame_count = 0
        report_interval = 5.0  # seconds
        processing_start_time: Optional[float] = None  # Track when actual processing starts
        frames_at_processing_start = 0

        print(f"  [  0.0s] Started {num_gpus} GPU workers...")

        while any(p.is_alive() for p in self._workers):
            time.sleep(0.5)
            current_time = time.perf_counter()

            # Periodic progress report with real-time FPS
            if current_time - last_report_time >= report_interval:
                elapsed = current_time - start_time
                remaining = max(0, self.config.duration_sec - elapsed)

                # Read current frame count
                current_frames = shared_frame_count.value
                interval_frames = current_frames - last_frame_count
                interval_fps = interval_frames / report_interval  # Current throughput
                per_stream_fps = interval_fps / self.config.num_streams if self.config.num_streams > 0 else 0

                # Track when processing actually starts (exclude warmup from avg)
                if processing_start_time is None and current_frames > 0:
                    processing_start_time = last_report_time  # Use previous report time
                    frames_at_processing_start = last_frame_count

                # Calculate average FPS excluding warmup time
                if processing_start_time is not None:
                    processing_elapsed = current_time - processing_start_time
                    processing_frames = current_frames - frames_at_processing_start
                    avg_fps = processing_frames / processing_elapsed if processing_elapsed > 0 else 0
                    print(
                        f"  [{elapsed:5.1f}s] {current_frames:,} frames | cur: {interval_fps:,.0f} FPS ({per_stream_fps:.1f}/stream) | avg: {avg_fps:,.0f} FPS | {remaining:.0f}s left"
                    )
                else:
                    print(f"  [{elapsed:5.1f}s] Warming up... | {remaining:.0f}s left")

                last_report_time = current_time
                last_frame_count = current_frames

        # Wait for all workers to fully complete
        for p in self._workers:  # type: ignore[assignment]
            p.join(timeout=5)

        results = []
        while not self._result_queue.empty():
            results.append(self._result_queue.get())

        for r in results:
            if "error" in r:
                logger.error(f"NVDEC error: {r['error']}")

        total_frames = sum(r.get("total_frames", 0) for r in results)
        total_errors = sum(r.get("total_errors", 0) for r in results)
        total_elapsed = max((r.get("elapsed_sec", 0) for r in results), default=0)

        aggregate_fps = total_frames / total_elapsed if total_elapsed > 0 else 0
        per_stream_fps = aggregate_fps / self.config.num_streams if self.config.num_streams > 0 else 0

        return {
            "num_streams": self.config.num_streams,
            "num_gpus": num_gpus,
            "pool_size": self.config.nvdec_pool_size,
            "duration_sec": total_elapsed,
            "total_frames": total_frames,
            "total_errors": total_errors,
            "aggregate_fps": aggregate_fps,
            "per_stream_fps": per_stream_fps,
            "gpu_results": results,
        }

    def stop(self):
        """Stop all workers."""
        self._stop_event.set()
        for p in self._workers:
            p.join(timeout=5)
            if p.is_alive():
                p.terminate()


# =============================================================================
# CLI
# =============================================================================


def main():
    parser = argparse.ArgumentParser(description="Streaming Gateway - CUDA IPC Producer (NV12)")
    parser.add_argument("--video", "-v", required=True, help="Video file path")
    parser.add_argument("--num-streams", "-n", type=int, default=100, help="Number of streams")
    parser.add_argument(
        "--fps",
        type=int,
        default=0,
        help="Target FPS limit per stream (0=source video FPS)",
    )
    parser.add_argument("--width", type=int, default=640, help="Frame width")
    parser.add_argument("--height", type=int, default=640, help="Frame height")
    parser.add_argument("--duration", "-d", type=float, default=30.0, help="Duration in seconds")
    parser.add_argument("--gpu", type=int, default=0, help="Primary GPU ID")
    parser.add_argument("--num-gpus", "-g", type=int, default=1, help="Number of GPUs (1-8)")
    parser.add_argument("--pool-size", type=int, default=8, help="NVDEC pool size per GPU")
    parser.add_argument("--burst-size", type=int, default=4, help="Frames per stream before rotating")
    parser.add_argument("--slots", type=int, default=32, help="Ring buffer slots per camera")
    parser.add_argument(
        "--demuxer",
        type=str,
        default="nvc",
        choices=["nvc", "gstreamer"],
        help="Demuxer backend: 'nvc' (PyNvVideoCodec, default) or 'gstreamer' (RTP timestamps for RTSP)",
    )
    parser.add_argument(
        "--quiet",
        "-q",
        action="store_true",
        help="Quiet mode - only show final results",
    )
    parser.add_argument(
        "--benchmark-mode",
        action="store_true",
        help="Enable granular per-stage timing with GPU sync points (reduces throughput)",
    )
    args = parser.parse_args()

    # Validate GStreamer availability if requested
    if args.demuxer == "gstreamer" and not GSTREAMER_DEMUXER_AVAILABLE:
        logger.warning("GStreamer demuxer requested but not available, falling back to NVC")
        args.demuxer = "nvc"

    # Setup logging based on quiet mode
    setup_logging(quiet=args.quiet)

    config = GatewayConfig(
        video_path=args.video,
        num_streams=args.num_streams,
        target_fps=args.fps,
        frame_width=args.width,
        frame_height=args.height,
        gpu_id=args.gpu,
        num_gpus=args.num_gpus,
        duration_sec=args.duration,
        nvdec_pool_size=args.pool_size,
        nvdec_burst_size=args.burst_size,
        num_slots=args.slots,
        demuxer_type=args.demuxer,
        benchmark_mode=args.benchmark_mode
        or os.environ.get("MATRICE_BENCHMARK_MODE", "").lower() in ("true", "1", "yes"),
    )

    frame_size = args.width * args.height * 1.5
    demuxer_info = "GStreamer (RTP timestamps)" if args.demuxer == "gstreamer" else "NVC (PyNvVideoCodec)"
    output_fmt = f"NV12 ({args.width}x{args.height}x1.5 = {frame_size / 1e6:.1f} MB/frame)"
    fps_limit_str = f"{args.fps} FPS/stream" if args.fps > 0 else "source FPS"

    if not args.quiet:
        print("\n" + "=" * 60)
        print("      STREAMING GATEWAY - CUDA IPC Producer (NV12)")
        print("=" * 60)
        print(f"  Video:      {args.video}")
        print(f"  Streams:    {args.num_streams}")
        print(f"  GPUs:       {args.num_gpus}")
        print(f"  Pool size:  {args.pool_size} NVDEC decoders/GPU")
        print(f"  Demuxer:    {demuxer_info}")
        print(f"  FPS limit:  {fps_limit_str}")
        print(f"  Output:     {output_fmt}")
        print(f"  Duration:   {args.duration}s")
        if config.benchmark_mode:
            print("  Benchmark:  ENABLED (granular per-stage timing)")
        print("=" * 60)

    gateway = StreamingGateway(config)

    try:
        results = gateway.start()
        # Clean summary output
        print("\n")
        print("=" * 60)
        print("         STREAMING GATEWAY BENCHMARK RESULTS")
        print("=" * 60)
        print(f"  Video:        {args.video}")
        print(f"  Streams:      {args.num_streams}")
        print(f"  GPUs:         {args.num_gpus}")
        print(f"  FPS limit:    {fps_limit_str}")
        print(f"  Duration:     {args.duration}s")
        print("-" * 60)
        print(f"  Total Frames: {results['total_frames']:,}")
        print("-" * 60)
        print(f"  >>> AGGREGATE FPS: {results['aggregate_fps']:,.0f} <<<")
        print(f"  >>> PER-STREAM FPS: {results['per_stream_fps']:.1f} <<<")
        print("=" * 60)
        print()
    except KeyboardInterrupt:
        gateway.stop()
        print("\nStopped")


if __name__ == "__main__":
    main()
