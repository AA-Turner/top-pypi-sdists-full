"""Auto-generated stubs for package: matrice_streaming."""
from typing import Any, Optional

from __future__ import annotations
from matrice_streaming.streaming_gateway.camera_streamer.codec_detect import normalize_codec
from matrice_streaming.streaming_gateway.camera_streamer.nvdec.nvdec import VideoDownloader, surface_to_nv12
from pathlib import Path
from urllib.parse import urlparse, urlunparse
import PyNvVideoCodec as nvc
import cupy as cp
import cv2
import multiprocessing.resource_tracker as _rt
import numpy as np
import os
import stat
import tempfile

# Functions
# From _mp_patch
def install_resource_tracker_patch() -> None: ...
    """
    Install the semaphore-unlink no-op patch on this interpreter.
    
        Must run BEFORE any ``mp.Queue``/``mp.Lock`` is created. Safe to call
        repeatedly and from any process.
    """

# From secure_cache
def is_safe_cached_file(path: Any) -> bool: ...
    """
    True if ``path`` is a regular file owned by the current uid.
    
        Rejects symlinks and files owned by other users so a pre-seeded cache entry
        is never trusted for reuse.
    """

# From secure_cache
def secure_cache_dir(name: str) -> Any: ...
    """
    Return a per-user cache dir under the temp root, created mode 0700.
    
        The directory name is suffixed with the current uid so distinct users never
        share a cache path. Raises RuntimeError if an existing path at that location
        is a symlink, not a directory, or owned by another user (hijack attempt).
    """

# From url_redact
def redact_url(url: Any) -> str: ...
    """
    Return a log-safe form of ``url`` with credentials stripped.
    
        Removes both the ``user:pass@`` userinfo and the ``?...`` query string /
        fragment (which frequently carry presigned tokens), while preserving the
        scheme, host, port and path so the value is still useful for debugging.
    
        Non-URL / non-string inputs and unparseable values are returned as a plain
        ``str`` (with any embedded ``user:pass@`` masked) so callers can use this
        unconditionally.
    """

# Classes
# From local_decoder
class LocalDecoder:
    """
    Simple NVDEC decoder for local testing. No SHM, no multiprocessing.
    """

    def __init__(self: Any, source: str, gpu_id: int = 0, codec: str = 'h264', width: int = 0, height: int = 0) -> None: ...
        """
        Args:
            source: Video file path, RTSP URL, or HTTPS URL.
            gpu_id: GPU device index.
            codec: "h264" or "h265" (also accepts aliases like "hevc").
            width: Output width. 0 = native camera resolution.
            height: Output height. 0 = native camera resolution.
        """

    def close(self: Any) -> Any: ...
        """
        Release resources.
        """

    def fps(self: Any) -> float: ...

    def frame_count(self: Any) -> int: ...

    def frames(self: Any, limit: int = 0) -> Any: ...
        """
        Yield NV12 frames. limit=0 means all frames until EOF.
        """

    def height(self: Any) -> int: ...
        """
        Frame height (resolved after first decode if using native resolution).
        """

    def preprocessed_frames(self: Any, model_w: int = 640, model_h: int = 640, limit: int = 0) -> Any: ...
        """
        Yield preprocessed frames. limit=0 means all.
        """

    def read_bgr(self: Any, width: int = 0, height: int = 0) -> Optional[np.ndarray]: ...
        """
        Decode and convert to BGR uint8 HWC for OpenCV / matplotlib.
        
                Args:
                    width: Output width. 0 = use decoder's target resolution.
                    height: Output height. 0 = use decoder's target resolution.
        
                Returns numpy (H, W, 3) uint8 BGR, or None at EOF.
        """

    def read_frame(self: Any) -> Optional[cp.ndarray]: ...
        """
        Decode next frame as NV12 CuPy array.
        
                Returns (H*1.5, W, 1) uint8 on GPU, or None at EOF.
                This is the exact format written to the CUDA SHM ring buffer in production.
        """

    def read_preprocessed_frame(self: Any, model_w: int = 640, model_h: int = 640) -> Optional[np.ndarray]: ...
        """
        Decode and preprocess: NV12 -> RGB (BT.601) -> resize -> CHW -> [0,1].
        
                Returns numpy (3, model_h, model_w) float32, matching the production
                CUDA kernel output in gpu_kernels.py. Returns None at EOF.
        """

    def reset(self: Any) -> Any: ...
        """
        Reset to beginning of video (recreates demuxer).
        """

    def width(self: Any) -> int: ...
        """
        Frame width (resolved after first decode if using native resolution).
        """


from . import _mp_patch, local_decoder, secure_cache, url_redact

def __getattr__(name: str) -> Any: ...