# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""
Video embeddings UDF for GPU-accelerated video processing.

This UDF uses torchcodec for efficient video decoding from GCS
and V-JEPA2 (Facebook) for generating video embeddings.
"""

import logging
import os
from typing import Any, cast

import pyarrow as pa

import geneva

_LOG = logging.getLogger(__name__)


@geneva.udf(
    version="0.3",
    memory=8 * 1024**3,  # 8GB memory for video processing
    data_type=pa.list_(pa.list_(pa.float32(), 1024)),  # 2D tensor: [num_tokens, 1024]
)
class VideoEmbedding:
    """
    Generate video embeddings as a 2D tensor using V-JEPA2 model.

    Returns raw frame/token-level embeddings that can be aggregated
    in different ways for flexible search strategies (mean, max, weighted, etc.)

    Decodes videos from GCS, samples frames, and generates embeddings.

    Configuration via environment variables:
    - NUM_FRAMES: Number of frames to sample (default: 64)
    - VJEPA_MODEL: V-JEPA2 model to use (default: "facebook/vjepa2-vitl-fpc64-256")
    - BLOCK_SIZE: fsspec block size for GCS reads (default: 16MB)
    - VIDEO_BASE_PATH: Full GCS path to video directory (default: gs://jon-geneva-demo/demo-data/openvid/videos/video)
    """

    def __init__(self) -> None:
        self.is_loaded = False
        self.processor: Any | None = None
        self.model: Any | None = None
        self.device: str = "cpu"
        self.num_frames = int(os.getenv("NUM_FRAMES", "64"))
        self.model_name = os.getenv("VJEPA_MODEL", "facebook/vjepa2-vitl-fpc64-256")
        self.block_size = int(os.getenv("BLOCK_SIZE", str(16 * 1024 * 1024)))
        # V-JEPA2 ViT-L produces 1024-dimensional embeddings
        self.embedding_dim = 1024
        # Parse VIDEO_BASE_PATH to get bucket and path prefix
        base_path = os.getenv(
            "VIDEO_BASE_PATH", "gs://jon-geneva-demo/demo-data/openvid/videos/video"
        )
        if base_path.startswith("gs://"):
            # Remove gs:// prefix for fsspec
            self.video_base_path = base_path
        else:
            self.video_base_path = f"gs://{base_path}"

    def setup(self) -> None:
        """Initialize V-JEPA2 model and processor."""
        import torch
        from transformers import AutoModel, AutoVideoProcessor

        _LOG.info(f"Loading V-JEPA2 model: {self.model_name}")
        self.processor = AutoVideoProcessor.from_pretrained(self.model_name)
        self.model = AutoModel.from_pretrained(self.model_name)
        model = self.model
        if model is None:  # pragma: no cover
            raise RuntimeError("V-JEPA2 model failed to initialize")

        # Move to GPU if available
        if torch.cuda.is_available():
            self.device = "cuda"
            self.model = model.to(self.device)
            _LOG.info(
                f"V-JEPA2 model loaded on GPU (sampling {self.num_frames} frames)"
            )
        else:
            self.device = "cpu"
            _LOG.warning("GPU not available, V-JEPA2 model will run on CPU (slower)")

        self.is_loaded = True

    def __call__(self, video: str) -> list[list[float]] | None:
        """
        Generate video embedding tensor from GCS video file.

        Parameters
        ----------
            video
                Video filename (e.g., 'video.mp4')

        Returns
        -------
            2D list of embeddings: [[emb1], [emb2], ...], shape [num_tokens, 1024]
            Can be aggregated at search time (mean, max, weighted, etc.)
        """
        if not self.is_loaded:
            self.setup()
        processor = self.processor
        model = self.model
        if processor is None or model is None:  # pragma: no cover
            raise RuntimeError("V-JEPA2 model failed to initialize")
        import fsspec
        import torch
        import torchcodec
        from torchcodec.decoders import VideoDecoder

        decoding_error = getattr(torchcodec, "DecodingError", Exception)

        try:
            # Construct full GCS path
            video_path = f"{self.video_base_path}/{video}"

            # Open video from GCS using fsspec
            of = fsspec.open(
                video_path,
                mode="rb",
                block_size=self.block_size,
                cache_type="block",  # Good for random access
            )

            with of as f:
                # Decode video without downloading entire file
                dec = VideoDecoder(cast("Any", f))

                # Sample frames - V-JEPA2 expects specific number of frames
                total_frames = len(dec)
                if total_frames < self.num_frames:
                    # If video has fewer frames than requested, use all frames
                    frame_indices = list(range(total_frames))
                else:
                    # Sample uniformly across the video
                    frame_indices = list(range(self.num_frames))

                # Get frames: returns tensor of shape [T, C, H, W]
                video_frames = dec.get_frames_at(indices=frame_indices).data

                # Process video with V-JEPA2 processor
                video_input = processor(video_frames, return_tensors="pt").to(
                    self.device
                )

                # Generate embeddings
                with torch.no_grad():
                    video_embeddings = model.get_vision_features(**video_input)

                # Return 2D tensor: [num_tokens, embedding_dim]
                # Remove batch dimension if present
                if video_embeddings.dim() == 3:
                    video_embeddings = video_embeddings.squeeze(0)

                # Convert to 2D list for storage
                return video_embeddings.cpu().numpy().tolist()
        except decoding_error as e:
            _LOG.error(f"Decoding error for video {video}: {e}")
            # Return zero tensor on decoding error
            return None
        except Exception:
            raise
