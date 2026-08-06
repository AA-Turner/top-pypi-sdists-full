"""Auto-generated stub for module: video_source."""
from typing import Any, Dict, Optional, Tuple

from __future__ import annotations
from matrice_streaming.secure_cache import is_safe_cached_file, secure_cache_dir
from matrice_streaming.url_redact import redact_url
from pathlib import Path, PurePosixPath
from urllib.parse import urlparse, urlunparse
import hashlib
import logging
import os
import requests as _requests_module
import tempfile
import threading

# Constants
log: Any

# Functions
def get_video_downloader(cache_dir: Optional[Path] = None, http_session: Any = None) -> Any: ...
    """
    Get or create the process-wide VideoDownloader instance.
    """
def validate_source_url(url: str) -> str: ...
    """
    Validate a video source before passing to GStreamer or subprocess.
    
        Allows:
        - Network streams: rtsp://, rtsps://, http://, https://
        - Local file URIs: file:///path/to/video.mp4
        - Bare/relative paths: /data/clip.mp4, videoplayback.mp4
    
        Raises ValueError for:
        - empty or non-string input
        - disallowed URL schemes (data://, ftp://, etc.)
        - path traversal (..) in any component
    
        Returns the URL unchanged on success.
    """

# Classes
class VideoDownloader:
    """
    Downloads and caches video files from HTTPS URLs.
    
        PyNvVideoCodec uses a bundled FFmpeg that doesn't have HTTPS support.
        This class downloads HTTPS videos to local files before passing them
        to the NVDEC demuxer.
    
        Features:
        - URL deduplication: same video URL (ignoring query params) is only downloaded once
        - Disk caching: reuses existing files across runs
        - Progress tracking for large files
        - Dynamic timeout based on file size
    """

    def __init__(self: Any, cache_dir: Optional[Path] = None, http_session: Any = None) -> None: ...
        """
        Initialize the video downloader.
        
                Args:
                    cache_dir: Override the cache directory. Test-injection seam only —
                        when omitted (the production path) the per-user 0700 directory
                        from ``secure_cache_dir`` is used.
                    http_session: Optional ``requests.Session``-like object. When None,
                        the module-level ``requests`` functions are used.
        """

    def cleanup(self: Any) -> None: ...
        """
        Clean up downloaded temporary files.
        """

    def prepare_source(self: Any, video_path: str, camera_id: str) -> str: ...
        """
        Prepare video source, downloading HTTPS URLs if needed.
        
                Args:
                    video_path: Video file path, RTSP URL, or HTTPS URL
                    camera_id: Camera identifier for logging
        
                Returns:
                    Local file path (downloaded if HTTPS) or original path
        """

