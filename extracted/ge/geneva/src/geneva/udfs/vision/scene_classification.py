# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""
Zero-shot image classification UDF using SigLIP2.

Scores each image against user-provided text labels using zero-shot
classification and returns structured tags for downstream filtering.

Model: google/siglip2-so400m-patch14-224 (Apache-2.0)
"""

import io
import logging
from typing import Any

import pyarrow as pa

import geneva

_LOG = logging.getLogger(__name__)

CLASSIFICATION_TYPE = pa.struct(
    [
        ("top_label", pa.string()),
        ("top_score", pa.float32()),
    ]
)


@geneva.udf(
    version="0.1",
    data_type=CLASSIFICATION_TYPE,
    num_gpus=1,
    checkpoint_size=64,
)
class ZeroShotClassifier:
    """Zero-shot image classification via SigLIP2.

    Batched UDF: receives a ``pa.Array`` of image bytes, returns a
    ``pa.Array`` of structs ``{top_label, top_score}``.

    Parameters
    ----------
        labels
            Text labels to classify against.
    """

    def __init__(self, labels: list[str] | None = None) -> None:
        self.labels = labels or ["object"]
        self.processor: Any = None
        self.model: Any = None
        self.text_embeds: Any = None
        self.device: str = "cpu"

    def setup(self) -> None:
        """Load SigLIP2 and pre-encode labels (called lazily)."""
        import torch
        from transformers import AutoModel, AutoProcessor

        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        _LOG.info("Loading SigLIP2 on %s", self.device)
        self.processor = AutoProcessor.from_pretrained(
            "google/siglip2-so400m-patch14-224"
        )
        self.model = AutoModel.from_pretrained("google/siglip2-so400m-patch14-224").to(
            self.device
        )
        self.model.eval()

        text_inputs = self.processor(
            text=self.labels,
            padding="max_length",
            return_tensors="pt",
        ).to(self.device)
        with torch.no_grad():
            self.text_embeds = self.model.get_text_features(**text_inputs)
            self.text_embeds = self.text_embeds / self.text_embeds.norm(
                dim=-1, keepdim=True
            )

    def __call__(self, image: pa.Array) -> pa.Array:
        import torch
        from PIL import Image

        if self.processor is None:
            self.setup()

        num_rows = len(image)
        none_result: dict[str, Any] = {
            "top_label": "unknown",
            "top_score": 0.0,
        }
        output: list[dict[str, Any]] = [none_result] * num_rows

        pil_images: list[Image.Image] = []
        valid_idx: list[int] = []
        for i, scalar in enumerate(image):
            raw = scalar.as_py()
            if raw is None:
                continue
            pil_images.append(Image.open(io.BytesIO(raw)).convert("RGB"))
            valid_idx.append(i)

        if not pil_images:
            return pa.array(output, type=CLASSIFICATION_TYPE)

        img_inputs = self.processor(
            images=pil_images,
            return_tensors="pt",
        ).to(self.device)
        with torch.no_grad():
            img_embeds = self.model.get_image_features(**img_inputs)
            img_embeds = img_embeds / img_embeds.norm(dim=-1, keepdim=True)

        # SigLIP uses sigmoid -- each label scored independently.
        probs = torch.sigmoid(img_embeds @ self.text_embeds.T)

        for j, idx in enumerate(valid_idx):
            scores = probs[j]
            top_idx = int(scores.argmax().item())
            output[idx] = {
                "top_label": self.labels[top_idx],
                "top_score": scores[top_idx].item(),
            }

        return pa.array(output, type=CLASSIFICATION_TYPE)
