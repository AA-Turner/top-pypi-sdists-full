# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""
BLIP caption UDF for GPU-accelerated image captioning.

This UDF uses Salesforce's BLIP model to generate image captions.
"""

import io
import logging
from typing import Any

import geneva

_LOG = logging.getLogger(__name__)


@geneva.udf(version="0.1", num_gpus=1.0)
class GenCaption:
    """
    Generate image captions using BLIP model.

    This is a GPU-accelerated stateful UDF.
    """

    def __init__(self) -> None:
        self.is_loaded = False
        self.processor: Any | None = None
        self.model: Any | None = None

    def setup(self) -> None:
        from transformers import BlipForConditionalGeneration, BlipProcessor

        _LOG.info("Loading BLIP model for caption generation")
        self.processor = BlipProcessor.from_pretrained(
            "Salesforce/blip-image-captioning-base"
        )
        self.model = BlipForConditionalGeneration.from_pretrained(
            "Salesforce/blip-image-captioning-base"
        )
        model = self.model
        if model is None:  # pragma: no cover
            raise RuntimeError("BLIP model failed to initialize")

        # Move to GPU if available
        import torch

        if torch.cuda.is_available():
            self.model = model.to("cuda")
            _LOG.info("BLIP model loaded on GPU")
        else:
            _LOG.warning("GPU not available, BLIP model will run on CPU (slower)")

        self.is_loaded = True

    def __call__(self, image: bytes) -> str:
        if not self.is_loaded:
            self.setup()
        processor = self.processor
        model = self.model
        if processor is None or model is None:  # pragma: no cover
            raise RuntimeError("BLIP model failed to initialize")

        import torch
        from PIL import Image

        image_stream = io.BytesIO(image)
        raw_image = Image.open(image_stream).convert("RGB")

        inputs = processor([raw_image], return_tensors="pt")

        # Move inputs to GPU if model is on GPU
        if next(model.parameters()).is_cuda:
            inputs = {k: v.to("cuda") for k, v in inputs.items()}

        with torch.no_grad():
            out = model.generate(**inputs, max_new_tokens=50)

        caption = processor.decode(out[0], skip_special_tokens=True)
        return caption
