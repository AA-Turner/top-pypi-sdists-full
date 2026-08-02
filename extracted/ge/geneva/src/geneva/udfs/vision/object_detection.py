# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""
Open-vocabulary object detection UDF using OWLv2.

Detects objects matching user-provided text queries with bounding boxes.
Returns the highest-confidence detection and its frame coverage percentage.

Model: google/owlv2-base-patch16-ensemble (Apache-2.0)
"""

import io
import logging
from typing import Any

import pyarrow as pa

import geneva

_LOG = logging.getLogger(__name__)

DETECTION_TYPE = pa.struct(
    [
        ("label", pa.string()),
        ("confidence", pa.float32()),
        ("bbox_area_pct", pa.float32()),
    ]
)

_NONE_RESULT = {"label": "none", "confidence": 0.0, "bbox_area_pct": 0.0}


@geneva.udf(
    version="0.1",
    data_type=DETECTION_TYPE,
    num_gpus=1,
    checkpoint_size=32,
)
class ObjectDetector:
    """Open-vocabulary object detection via OWLv2.

    Batched UDF: receives a ``pa.Array`` of image bytes, returns a
    ``pa.Array`` of structs ``{label, confidence, bbox_area_pct}``.

    Parameters
    ----------
        queries
            Text queries describing the objects to detect.
            Each query becomes a candidate label in the output.
    """

    def __init__(self, queries: list[str] | None = None) -> None:
        self.queries = queries or ["object"]
        self.processor: Any = None
        self.model: Any = None
        self.device: str = "cpu"

    def setup(self) -> None:
        """Load OWLv2 model and processor (called lazily on first batch)."""
        import torch
        from transformers import Owlv2ForObjectDetection, Owlv2Processor

        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        _LOG.info("Loading OWLv2 on %s", self.device)
        self.processor = Owlv2Processor.from_pretrained(
            "google/owlv2-base-patch16-ensemble"
        )
        model = Owlv2ForObjectDetection.from_pretrained(
            "google/owlv2-base-patch16-ensemble"
        )
        self.model = model.to(self.device)  # type: ignore[arg-type]
        self.model.eval()

    def __call__(self, image: pa.Array) -> pa.Array:
        import torch
        from PIL import Image

        if self.processor is None:
            self.setup()

        num_rows = len(image)
        output: list[dict[str, Any]] = [dict(_NONE_RESULT) for _ in range(num_rows)]

        pil_images: list[Image.Image] = []
        valid_idx: list[int] = []
        for i, scalar in enumerate(image):
            raw = scalar.as_py()
            if raw is None:
                continue
            pil_images.append(Image.open(io.BytesIO(raw)).convert("RGB"))
            valid_idx.append(i)

        if not pil_images:
            return pa.array(output, type=DETECTION_TYPE)

        texts = [self.queries] * len(pil_images)
        inputs = self.processor(
            text=texts,
            images=pil_images,
            return_tensors="pt",
            padding=True,
        ).to(self.device)

        with torch.no_grad():
            outputs = self.model(**inputs)

        sizes = torch.tensor(
            [[img.height, img.width] for img in pil_images],
            device=self.device,
        )
        detections = self.processor.post_process_object_detection(
            outputs=outputs,
            target_sizes=sizes,
            threshold=0.1,
        )

        for j, idx in enumerate(valid_idx):
            det = detections[j]
            if len(det["scores"]) == 0:
                continue
            best = det["scores"].argmax()
            x1, y1, x2, y2 = det["boxes"][best].tolist()
            img = pil_images[j]
            output[idx] = {
                "label": self.queries[det["labels"][best]],
                "confidence": det["scores"][best].item(),
                "bbox_area_pct": (x2 - x1) * (y2 - y1) / (img.width * img.height),
            }

        return pa.array(output, type=DETECTION_TYPE)
