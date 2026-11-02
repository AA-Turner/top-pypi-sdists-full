"""VideoHandler — frame extraction and cloud upload for video files.

Requires ``opencv-python`` (or ``opencv-python-headless``) for frame extraction.
The dependency is imported lazily inside the methods so that the handler can be
imported without cv2 installed (it will raise only when frame methods are called).

Typical usage in a FastAPI route
---------------------------------
    from matrx_files import FileManager, PODCAST_VARIANTS

    fm = FileManager.get_instance("my_app")

    # Upload a video and get its public URL
    video_url = await fm.video_handler.upload_video_async(
        video_bytes,
        "s3://bucket/{user_id}/{uuid}/video.mp4",
        content_type="video/mp4",
    )

    # Extract a thumbnail frame and generate image variants from it
    frame_bytes = await fm.video_handler.extract_frame_at_async(video_bytes)
    urls = await fm.image_handler.process_variants_async(
        frame_bytes, PODCAST_VARIANTS, "s3://bucket/{user_id}/{uuid}"
    )
"""

from __future__ import annotations

import asyncio
import os
import tempfile
from io import BytesIO

from matrx_files.file_handler import FileHandler
from matrx_files.specific_handlers.video_compose import (
    SlideSegment,
    compose_slideshow,
    compose_slideshow_async,
)


class VideoHandler(FileHandler):
    """Handles video upload and frame extraction for media processing pipelines."""

    SUPPORTED_CONTENT_TYPES: frozenset[str] = frozenset({
        "video/mp4",
        "video/quicktime",   # MOV
        "video/webm",
        "video/x-msvideo",   # AVI
        "video/x-matroska",  # MKV
    })

    # ------------------------------------------------------------------
    # Format validation
    # ------------------------------------------------------------------

    @classmethod
    def is_supported_format(cls, content_type: str) -> bool:
        """Return True if *content_type* is a supported video MIME type."""
        return content_type in cls.SUPPORTED_CONTENT_TYPES

    # ------------------------------------------------------------------
    # Frame extraction — pure CPU, runs in executor for async callers
    # ------------------------------------------------------------------

    @staticmethod
    def extract_frame_at_path(video_path: str, position: float = 0.10) -> bytes:
        """Extract a single frame from a video FILE PATH at *position* (0.0–1.0).

        This is the bounded-memory primitive: OpenCV reads the file from disk
        directly, so the whole video is never materialized in Python memory.
        Prefer this for large media (see
        ``cloud_sync.processing.thumbnails.LARGE_MEDIA_THRESHOLD_BYTES``).
        The caller owns the file at *video_path* — nothing is deleted here.

        Returns JPEG bytes at quality 90.

        Raises
        ------
        RuntimeError
            If the video cannot be opened or the frame cannot be read.
        ImportError
            If ``opencv-python`` (cv2) is not installed.
        """
        from matrx_files._extras import require

        cv2 = require("cv2", "media", "VideoHandler.extract_frame_at_path")

        from PIL import Image

        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise RuntimeError("Could not open video file — unsupported format or corrupt data")

        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        target_frame = max(0, int(total_frames * position))
        cap.set(cv2.CAP_PROP_POS_FRAMES, target_frame)

        ret, frame = cap.read()
        cap.release()

        if not ret or frame is None:
            raise RuntimeError(
                f"Could not read frame at position {position:.0%} "
                f"(frame {target_frame}/{total_frames})"
            )

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)
        buf = BytesIO()
        img.save(buf, format="JPEG", quality=90, optimize=True)
        return buf.getvalue()

    @staticmethod
    def extract_frame_at(video_bytes: bytes, position: float = 0.10) -> bytes:
        """Extract a single frame from in-memory video bytes at *position*.

        Writes *video_bytes* to a named temp file (OpenCV requires a filesystem
        path) and delegates to :meth:`extract_frame_at_path`. The temp file is
        always cleaned up. For LARGE videos, prefer streaming the object to
        disk yourself and calling :meth:`extract_frame_at_path` — this method
        requires the whole video in memory first.

        Parameters
        ----------
        video_bytes:
            Raw bytes of the video file (MP4, MOV, WebM, etc.).
        position:
            Fractional position within the video (0.0 = first frame,
            0.10 = 10% through, 0.5 = midpoint, 1.0 = last frame).
            Defaults to 0.10 (10%) which typically avoids black intro frames.

        Returns
        -------
        bytes
            JPEG-encoded bytes of the extracted frame.

        Raises
        ------
        RuntimeError
            If the video cannot be opened or the frame cannot be read.
        ImportError
            If ``opencv-python`` (cv2) is not installed.
        """
        tmp_path: str | None = None
        try:
            with tempfile.NamedTemporaryFile(suffix=".tmp", delete=False) as tmp:
                tmp.write(video_bytes)
                tmp_path = tmp.name
            return VideoHandler.extract_frame_at_path(tmp_path, position)
        finally:
            if tmp_path:
                try:
                    os.unlink(tmp_path)
                except OSError:
                    pass

    async def extract_frame_at_async(
        self, video_bytes: bytes, position: float = 0.10
    ) -> bytes:
        """Async wrapper around extract_frame_at() — offloads to a thread executor.

        Use this in FastAPI routes. The event loop is never blocked.

        Parameters
        ----------
        video_bytes:
            Raw bytes of the video file.
        position:
            Fractional position (0.0–1.0). Defaults to 0.10 (10%).

        Returns
        -------
        bytes
            JPEG-encoded bytes of the extracted frame.
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None, self.extract_frame_at, video_bytes, position
        )

    # ------------------------------------------------------------------
    # Cloud upload
    # ------------------------------------------------------------------

    # ------------------------------------------------------------------
    # Composition — stitch images + videos into one crossfaded slideshow
    # ------------------------------------------------------------------

    @staticmethod
    def compose_slideshow(segments: list[SlideSegment], **kwargs) -> bytes:
        """Stitch an ordered list of image/video segments into a single
        crossfaded MP4 (blurred-fill background, smooth transitions).

        Thin pass-through to
        :func:`matrx_files.specific_handlers.video_compose.compose_slideshow`.
        Returns the MP4 bytes; upload them with :meth:`upload_video_async`.
        """
        return compose_slideshow(segments, **kwargs)

    @staticmethod
    async def compose_slideshow_async(segments: list[SlideSegment], **kwargs) -> bytes:
        """Async (thread-offloaded) variant of :meth:`compose_slideshow`.

        Use this in FastAPI routes / async pipelines so the event loop is
        never blocked by ffmpeg.
        """
        return await compose_slideshow_async(segments, **kwargs)

    async def upload_video_async(
        self,
        video_bytes: bytes,
        dest_uri: str,
        content_type: str = "video/mp4",
    ) -> str:
        """Upload video bytes to cloud storage and return the permanent public URL.

        The upload uses the BackendRouter's retry policy and the S3 backend's
        600-second timeout, so large files (up to 500MB) are handled safely.

        Parameters
        ----------
        video_bytes:
            Raw bytes of the video file.
        dest_uri:
            Full cloud storage URI including filename.
            e.g. ``"s3://bucket/{user_id}/{uuid}/video.mp4"``
        content_type:
            MIME type of the video. Defaults to ``"video/mp4"``.

        Returns
        -------
        str
            Permanent public URL of the uploaded video.
        """
        await self.cloud_write_async(dest_uri, video_bytes, content_type=content_type)
        return await self.cloud_get_public_url_async(dest_uri)

    def upload_video(
        self,
        video_bytes: bytes,
        dest_uri: str,
        content_type: str = "video/mp4",
    ) -> str:
        """Synchronous version of upload_video_async(). Use in scripts/tests."""
        self.cloud_write(dest_uri, video_bytes, content_type=content_type)
        return self.cloud_get_public_url(dest_uri)
