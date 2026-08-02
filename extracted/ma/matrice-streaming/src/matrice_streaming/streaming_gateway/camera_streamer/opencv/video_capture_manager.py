"""Video capture management with robust retry logic."""

import hashlib
import logging
import os
import tempfile
import time
from pathlib import Path
from typing import Any, ClassVar, Dict, Optional, Tuple, Union
from urllib.parse import urlparse, urlunparse

import cv2
import requests

from matrice_streaming.secure_cache import is_safe_cached_file, secure_cache_dir
from matrice_streaming.url_redact import redact_url


class VideoSourceConfig:
    """Configuration for video source handling."""

    MAX_CAPTURE_RETRIES: ClassVar[int] = 6
    CAPTURE_RETRY_DELAYS: ClassVar[list] = [
        2,
        2,
        4,
        6,
        8,
        8,
    ]  # exponential backoff (~30s total)
    MAX_CONSECUTIVE_FAILURES: ClassVar[int] = 10
    DOWNLOAD_TIMEOUT: ClassVar[int] = 30  # Base timeout in seconds
    DOWNLOAD_TIMEOUT_PER_100MB: ClassVar[int] = 30  # Additional seconds per 100MB
    MAX_DOWNLOAD_TIMEOUT: ClassVar[int] = 600  # 10 minutes max
    DOWNLOAD_CHUNK_SIZE: ClassVar[int] = 8192
    DEFAULT_BUFFER_SIZE: ClassVar[int] = 5  # Increased from 1 to 5 for better throughput
    DEFAULT_FPS: ClassVar[int] = 30


class VideoCaptureManager:
    """Manages video capture from various sources with retry logic and caching.

    Features URL deduplication: if multiple cameras use the same video URL
    (ignoring query parameters like AWS signed URL tokens), the video is only
    downloaded once and the local path is shared between cameras.
    """

    def __init__(self):
        """Initialize video capture manager."""
        # Maps normalized URL (without query params) -> local file path. A single
        # cache keyed on the normalized URL deduplicates downloads across cameras
        # whose URLs differ only by query params (e.g. AWS signed-URL tokens).
        self._url_to_path: Dict[str, str] = {}
        # Per-user 0700 cache dir (not a world-shared fixed path) so a local
        # attacker cannot pre-create the dir or pre-seed cache files we trust.
        self.temp_dir = secure_cache_dir("matrice_streaming_cache")
        self.logger = logging.getLogger(__name__)

    def prepare_source(self, source: Union[str, int], stream_key: str) -> Union[str, int]:
        """Prepare video source, downloading if it's a URL.

        Args:
            source: Video source (camera index, file path, or URL)
            stream_key: Stream identifier for caching

        Returns:
            Prepared source (downloaded file path or original source)
        """
        if isinstance(source, str) and self._is_downloadable_url(source):
            local_path = self._download_video_file(source, stream_key)
            if local_path:
                self.logger.debug(f"Using downloaded file: {local_path}")
                return local_path
            self.logger.warning(f"Failed to download {redact_url(source)}, will try to use URL directly")
        return source

    def open_capture(  # type: ignore[return]
        self,
        source: Union[str, int],
        width: Optional[int] = None,
        height: Optional[int] = None,
    ) -> Tuple[cv2.VideoCapture, str]:
        """Open video capture with retry logic.

        Args:
            source: Video source
            width: Target width for camera
            height: Target height for camera

        Returns:
            Tuple of (VideoCapture object, source_type)

        Raises:
            RuntimeError: If unable to open capture after retries
        """
        for attempt in range(VideoSourceConfig.MAX_CAPTURE_RETRIES):
            try:
                source_type = self._detect_source_type(source)
                cap = cv2.VideoCapture(self._get_capture_source(source))

                if not cap.isOpened():
                    raise RuntimeError(f"Failed to open source: {redact_url(source)}")

                self._configure_capture(cap, source_type, width, height)

                self.logger.info(f"Opened {source_type} source: {redact_url(source)}")
                return cap, source_type

            except Exception as e:
                # Gather detailed source info for error logging
                source_info = ""
                if isinstance(source, str):
                    if os.path.exists(source):
                        file_size = os.path.getsize(source)
                        source_info = f" | File exists: {file_size / (1024 * 1024):.1f}MB"
                    elif source.split("://", 1)[0] in ("rtsp", "http", "https"):
                        source_info = " | Network source"
                    else:
                        source_info = " | File does not exist"

                self.logger.error(
                    f"Attempt {attempt + 1}/{VideoSourceConfig.MAX_CAPTURE_RETRIES} failed to open "
                    f"{source_type} source: {type(e).__name__}: {e}{source_info}"
                )
                if attempt < VideoSourceConfig.MAX_CAPTURE_RETRIES - 1:
                    delay = VideoSourceConfig.CAPTURE_RETRY_DELAYS[
                        min(attempt, len(VideoSourceConfig.CAPTURE_RETRY_DELAYS) - 1)
                    ]
                    time.sleep(delay)
                else:
                    raise RuntimeError(
                        f"Failed to open source after {VideoSourceConfig.MAX_CAPTURE_RETRIES} attempts: "
                        f"{type(e).__name__}: {e}{source_info}"
                    ) from e

    def get_video_properties(self, cap: cv2.VideoCapture) -> Dict[str, Any]:
        """Extract video properties from capture.

        Args:
            cap: VideoCapture object

        Returns:
            Dictionary with video properties
        """
        return {
            "original_fps": float(cap.get(cv2.CAP_PROP_FPS) or VideoSourceConfig.DEFAULT_FPS),
            "frame_count": cap.get(cv2.CAP_PROP_FRAME_COUNT),
            "width": int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            "height": int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
        }

    def cleanup(self):
        """Clean up downloaded temporary files."""
        for filepath in set(self._url_to_path.values()):
            try:
                if os.path.exists(filepath):
                    os.remove(filepath)
                    self.logger.debug(f"Removed temp file: {filepath}")
            except Exception as e:
                self.logger.warning(f"Failed to remove temp file {filepath}: {e}")

        self._url_to_path.clear()

    # Private methods

    def _is_downloadable_url(self, source: str) -> bool:
        """Check if source is a downloadable URL (not RTSP).

        Only ``https://`` is accepted by default — plain ``http://`` downloads
        are unencrypted and subject to MITM tampering of the video content.
        Set ``MATRICE_STREAMING_ALLOW_HTTP_DOWNLOAD=1`` to opt back into
        cleartext http downloads for legacy/on-prem sources.
        """
        if source.startswith("rtsp"):
            return False
        if source.startswith("https://"):
            return True
        if source.split("://", 1)[0] == "http":
            if os.environ.get("MATRICE_STREAMING_ALLOW_HTTP_DOWNLOAD") == "1":
                return True
            self.logger.warning(
                "Refusing cleartext http:// video download for %s "
                "(set MATRICE_STREAMING_ALLOW_HTTP_DOWNLOAD=1 to allow)",
                redact_url(source),
            )
            return False
        return False

    def _normalize_url(self, url: str) -> str:
        """Normalize URL by stripping query parameters.

        This allows URLs that point to the same file but have different
        query parameters (e.g., AWS signed URLs with different tokens)
        to be recognized as the same resource.

        Args:
            url: Full URL with potential query parameters

        Returns:
            Normalized URL without query parameters
        """
        parsed = urlparse(url)
        # Rebuild URL without query string and fragment
        normalized = urlunparse(
            (
                parsed.scheme,
                parsed.netloc,
                parsed.path,
                "",  # params
                "",  # query
                "",  # fragment
            )
        )
        return normalized

    def _get_url_hash(self, normalized_url: str) -> str:
        """Generate a short hash for the normalized URL.

        This is used for creating unique but consistent file names.

        Args:
            normalized_url: URL without query parameters

        Returns:
            Short hash string
        """
        return hashlib.md5(normalized_url.encode(), usedforsecurity=False).hexdigest()[:12]

    def _download_video_file(self, url: str, stream_key: str) -> Optional[str]:
        """Download video file from URL and cache it locally.

        Uses URL deduplication: if the same video (by normalized URL without
        query parameters) has already been downloaded, returns the existing
        local path instead of downloading again.

        Features dynamic timeout calculation based on file size and progress
        tracking for large files.

        Args:
            url: Video file URL (may include query parameters like AWS signatures)
            stream_key: Stream identifier

        Returns:
            Local file path or None if download failed
        """
        # Initialize tracking variables for error reporting
        content_length = 0
        file_size_mb = 0.0
        bytes_downloaded = 0
        timeout = VideoSourceConfig.DOWNLOAD_TIMEOUT
        expected_path = None

        try:
            # Normalize URL to check for duplicate downloads
            # (same file but different query params, e.g., different AWS signatures)
            normalized_url = self._normalize_url(url)

            # Generate a consistent filename using URL hash
            file_ext = Path(url.split("?")[0]).suffix or ".mp4"
            url_hash = self._get_url_hash(normalized_url)
            expected_path = self.temp_dir / f"video_{url_hash}{file_ext}"
            expected_path_str = str(expected_path)

            # Quick check: if file already exists on disk, use it — but only if
            # it is a regular file owned by us (not a symlink or a pre-seeded
            # file planted by another user).
            if os.path.exists(expected_path):
                if is_safe_cached_file(expected_path):
                    existing_size = os.path.getsize(expected_path)
                    self.logger.debug(
                        f"Reusing existing video file for {stream_key}: {expected_path} "
                        f"({existing_size / (1024 * 1024):.1f}MB, already downloaded)"
                    )
                    self._url_to_path[normalized_url] = expected_path_str
                    return expected_path_str
                self.logger.warning(
                    "Ignoring untrusted cache file (wrong owner or symlink) for "
                    f"{stream_key}: {expected_path}; will re-download"
                )
                try:
                    os.unlink(expected_path)
                except OSError:
                    return None

            # Memory cache keyed on the normalized URL (dedups across cameras whose
            # URLs differ only by query params, e.g. AWS signed-URL tokens)
            cached = self._url_to_path.get(normalized_url)
            if cached and os.path.exists(cached):
                self.logger.debug(f"Reusing previously downloaded file for {stream_key}: {cached}")
                return cached

            # HEAD request to get file size for dynamic timeout calculation
            try:
                head_response = requests.head(url, timeout=10, allow_redirects=True)
                content_length = int(head_response.headers.get("Content-Length", 0))
                file_size_mb = content_length / (1024 * 1024)
            except Exception as head_err:
                self.logger.debug(f"HEAD request failed for {stream_key}: {head_err}")
                content_length = 0
                file_size_mb = 0.0

            # Calculate dynamic timeout based on file size
            if content_length > 0:
                # Base timeout + additional time per 100MB
                timeout = min(
                    VideoSourceConfig.DOWNLOAD_TIMEOUT
                    + int(file_size_mb // 100) * VideoSourceConfig.DOWNLOAD_TIMEOUT_PER_100MB,
                    VideoSourceConfig.MAX_DOWNLOAD_TIMEOUT,
                )
                self.logger.info(f"Downloading video file for {stream_key}: {file_size_mb:.1f}MB (timeout: {timeout}s)")
            else:
                timeout = VideoSourceConfig.DOWNLOAD_TIMEOUT
                self.logger.info(f"Downloading video file for {stream_key} (size unknown, timeout: {timeout}s)")

            # Download the file with progress tracking
            response = requests.get(url, stream=True, timeout=timeout)
            response.raise_for_status()

            # Update content_length from response if HEAD failed
            if content_length == 0:
                content_length = int(response.headers.get("Content-Length", 0))
                file_size_mb = content_length / (1024 * 1024) if content_length > 0 else 0

            last_progress_log = 0

            # Write to a private temp file in the same (0700) dir, then
            # atomically rename into place. This avoids trusting/clobbering an
            # existing or symlinked path at expected_path during the download.
            tmp_fd, tmp_name = tempfile.mkstemp(dir=str(self.temp_dir), prefix="dl_", suffix=file_ext)
            try:
                with os.fdopen(tmp_fd, "wb") as f:
                    for chunk in response.iter_content(chunk_size=VideoSourceConfig.DOWNLOAD_CHUNK_SIZE):
                        f.write(chunk)
                        bytes_downloaded += len(chunk)

                        # Log progress every 50MB for large files (>50MB)
                        if content_length > 50_000_000:
                            mb_downloaded = bytes_downloaded // (1024 * 1024)
                            if mb_downloaded - last_progress_log >= 50:
                                progress = (bytes_downloaded / content_length * 100) if content_length else 0
                                self.logger.info(
                                    f"Download progress for {stream_key}: "
                                    f"{mb_downloaded}MB / {file_size_mb:.0f}MB ({progress:.1f}%)"
                                )
                                last_progress_log = mb_downloaded
                os.replace(tmp_name, expected_path)
            except BaseException:
                try:
                    os.unlink(tmp_name)
                except OSError:
                    pass
                raise

            self._url_to_path[normalized_url] = expected_path_str

            self.logger.info(
                f"Downloaded video file for {stream_key}: {expected_path} ({bytes_downloaded / (1024 * 1024):.1f}MB)"
            )
            return expected_path_str

        except requests.Timeout as e:
            self.logger.error(
                f"Download timeout for {stream_key}: {e} | "
                f"File size: {file_size_mb:.1f}MB, Downloaded: {bytes_downloaded / (1024 * 1024):.1f}MB, "
                f"Timeout: {timeout}s"
            )
            return None
        except requests.HTTPError as e:
            self.logger.error(
                f"HTTP error downloading {stream_key}: {e.response.status_code} - {e.response.reason} | "
                f"URL: {redact_url(url)}"
            )
            return None
        except IOError as e:
            self.logger.error(
                f"Disk I/O error downloading {stream_key}: {e} | "
                f"Downloaded: {bytes_downloaded / (1024 * 1024):.1f}MB, Path: {expected_path}"
            )
            return None
        except Exception as e:
            size_info = f"{file_size_mb:.1f}MB" if content_length > 0 else "unknown"
            self.logger.error(
                f"Failed to download video file for {stream_key}: {type(e).__name__}: {e} | "
                f"File size: {size_info}, Downloaded: {bytes_downloaded / (1024 * 1024):.1f}MB"
            )
            return None

    def _detect_source_type(self, source: Union[str, int]) -> str:
        """Detect the type of video source."""
        if isinstance(source, int) or (isinstance(source, str) and source.isdigit()):
            return "camera"
        if isinstance(source, str) and source.startswith("rtsp"):
            return "rtsp"
        if isinstance(source, str) and source.startswith("http"):
            return "http"
        return "video_file"

    def _get_capture_source(self, source: Union[str, int]) -> Union[str, int]:
        """Get the actual source to pass to cv2.VideoCapture."""
        if isinstance(source, str) and source.isdigit():
            return int(source)
        return source

    def _configure_capture(
        self,
        cap: cv2.VideoCapture,
        source_type: str,
        width: Optional[int],
        height: Optional[int],
    ):
        """Configure capture settings based on source type."""
        if source_type in ["camera", "rtsp"]:
            cap.set(cv2.CAP_PROP_BUFFERSIZE, VideoSourceConfig.DEFAULT_BUFFER_SIZE)

        if source_type == "camera":
            if width:
                cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
            if height:
                cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
