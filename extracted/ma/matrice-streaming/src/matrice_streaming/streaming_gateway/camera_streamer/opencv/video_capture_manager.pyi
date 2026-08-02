"""Auto-generated stub for module: video_capture_manager."""
from typing import Any, Dict, Optional, Tuple, Union

from matrice_streaming.secure_cache import is_safe_cached_file, secure_cache_dir
from matrice_streaming.url_redact import redact_url
from pathlib import Path
from urllib.parse import urlparse, urlunparse
import cv2
import hashlib
import logging
import os
import requests
import tempfile
import time

# Classes
class VideoCaptureManager:
    """
    Manages video capture from various sources with retry logic and caching.
    
        Features URL deduplication: if multiple cameras use the same video URL
        (ignoring query parameters like AWS signed URL tokens), the video is only
        downloaded once and the local path is shared between cameras.
    """

    def __init__(self: Any) -> None: ...
        """
        Initialize video capture manager.
        """

    def cleanup(self: Any) -> None: ...
        """
        Clean up downloaded temporary files.
        """

    def get_video_properties(self: Any, cap: Any) -> Dict[str, Any]: ...
        """
        Extract video properties from capture.
        
                Args:
                    cap: VideoCapture object
        
                Returns:
                    Dictionary with video properties
        """

    def open_capture(self: Any, source: Union[str, int], width: Optional[int] = None, height: Optional[int] = None) -> Tuple[cv2.VideoCapture, str]: ...
        """
        Open video capture with retry logic.
        
                Args:
                    source: Video source
                    width: Target width for camera
                    height: Target height for camera
        
                Returns:
                    Tuple of (VideoCapture object, source_type)
        
                Raises:
                    RuntimeError: If unable to open capture after retries
        """

    def prepare_source(self: Any, source: Union[str, int], stream_key: str) -> Union[str, int]: ...
        """
        Prepare video source, downloading if it's a URL.
        
                Args:
                    source: Video source (camera index, file path, or URL)
                    stream_key: Stream identifier for caching
        
                Returns:
                    Prepared source (downloaded file path or original source)
        """

class VideoSourceConfig:
    """
    Configuration for video source handling.
    """

    pass
