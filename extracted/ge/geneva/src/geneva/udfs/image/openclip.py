# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""
OpenCLIP embedding UDF for generating 512-dimensional image embeddings.

This UDF uses OpenAI's CLIP ViT-B/32 model to generate embeddings.
"""

import io
import logging
from typing import Any

import pyarrow as pa

import geneva

_LOG = logging.getLogger(__name__)


@geneva.udf(version="0.1", data_type=pa.list_(pa.float32(), 512))
class GenEmbeddings:
    """
    Generate 512-dimensional embeddings using OpenCLIP.

    This is a stateful UDF that loads the model once and reuses it.
    """

    def __init__(self) -> None:
        self.is_loaded = False
        self.model: Any | None = None
        self.preprocess: Any | None = None

    def setup(self) -> None:
        import open_clip

        _LOG.info("Loading OpenCLIP model for embeddings")
        self.model, _, self.preprocess = open_clip.create_model_and_transforms(
            "ViT-B-32", pretrained="openai"
        )
        model = self.model
        if model is None:  # pragma: no cover
            raise RuntimeError("OpenCLIP model failed to initialize")
        model.eval()
        self.is_loaded = True

    def __call__(self, image: bytes) -> list[float]:
        if not self.is_loaded:
            self.setup()
        model = self.model
        preprocess = self.preprocess
        if model is None or preprocess is None:  # pragma: no cover
            raise RuntimeError("OpenCLIP model failed to initialize")

        import torch
        from PIL import Image

        image_stream = io.BytesIO(image)
        pil_image = Image.open(image_stream).convert("RGB")
        image_tensor = preprocess(pil_image).unsqueeze(0)

        with torch.no_grad():
            embedding = model.encode_image(image_tensor)
            embedding = embedding.squeeze().cpu().numpy()

        return embedding.tolist()
