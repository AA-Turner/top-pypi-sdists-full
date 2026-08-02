# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""
Frame extraction UDF for blob column testing in materialized views.

This UDF extracts a single frame (thumbnail) from video files as a PNG blob.
Uses torchcodec for efficient GPU-accelerated video decoding.
"""

import io
import logging
import os
from typing import Any, cast

import pyarrow as pa

import geneva

_LOG = logging.getLogger(__name__)


@geneva.udf(
    version="0.1",
    memory=4 * 1024**3,  # 4GB memory for video processing
    data_type=pa.large_binary(),
    field_metadata={"lance-encoding:blob": "true"},  # Critical: enables blob storage
)
class ExtractFirstFrame:
    """
    Extract first frame from video as PNG blob.

    Returns ~10-100KB per frame (practical blob size for testing).

    Configuration via environment variables:
    - VIDEO_BASE_PATH: Full GCS path to video directory
      (default: gs://jon-geneva-demo/demo-data/openvid/videos/video)
    - FRAME_INDEX: Frame index to extract (default: 0)
    - FRAME_SIZE: Target frame size in pixels (default: 256)
    """

    def __init__(self) -> None:
        self.is_loaded = False
        self.Image: Any | None = None
        self.frame_index = int(os.getenv("FRAME_INDEX", "0"))
        self.frame_size = int(os.getenv("FRAME_SIZE", "256"))
        base_path = os.getenv(
            "VIDEO_BASE_PATH",
            "gs://jon-geneva-demo/demo-data/openvid/videos/video",
        )
        self.video_base_path = (
            base_path if base_path.startswith("gs://") else f"gs://{base_path}"
        )

    def setup(self) -> None:
        """Initialize dependencies on first call."""
        from PIL import Image

        self.Image = Image
        self.is_loaded = True
        _LOG.info(
            f"ExtractFirstFrame initialized (frame={self.frame_index}, "
            f"size={self.frame_size})"
        )

    def __call__(self, video: str) -> bytes | None:
        """
        Extract first frame from video file as PNG blob.

        Parameters
        ----------
            video
                Video filename (e.g., 'video.mp4')

        Returns
        -------
            PNG image bytes or None on failure
        """
        if not self.is_loaded:
            self.setup()
        image_mod = self.Image
        if image_mod is None:  # pragma: no cover
            raise RuntimeError("PIL.Image failed to initialize")
        import fsspec
        from torchcodec.decoders import VideoDecoder

        try:
            video_path = f"{self.video_base_path}/{video}"

            # Open video from GCS using fsspec with block caching
            of = fsspec.open(
                video_path,
                mode="rb",
                block_size=16 * 1024 * 1024,  # 16MB blocks
                cache_type="block",
            )

            with of as f:
                # Decode video without downloading entire file
                dec = VideoDecoder(cast("Any", f))

                # Get single frame at specified index
                frame_tensor = dec.get_frames_at(indices=[self.frame_index]).data[0]

                # Convert to PIL Image (CHW -> HWC)
                frame_np = frame_tensor.permute(1, 2, 0).cpu().numpy()
                img = image_mod.fromarray(frame_np.astype("uint8"))

                # Resize to target size
                img = img.resize((self.frame_size, self.frame_size))

                # Encode as PNG
                buffer = io.BytesIO()
                img.save(buffer, format="PNG")
                return buffer.getvalue()

        except Exception as e:
            _LOG.error(f"Failed to extract frame from {video}: {e}")
            return None
