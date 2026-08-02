# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

from __future__ import annotations

import base64
import io
import logging
from typing import Any

import pyarrow as pa

import geneva

_LOG = logging.getLogger(__name__)

MODEL_ID = "google/vit-base-patch16-224"
IMAGE_SIZE = 224
_PIXEL_VALUES_LEN = 3 * IMAGE_SIZE * IMAGE_SIZE
_CPU_UDF_MEMORY_BYTES = 20 * 1024**3

_DECODED_STRUCT = pa.struct(
    [
        pa.field("image_bytes", pa.large_binary()),
        pa.field("width", pa.int32()),
        pa.field("height", pa.int32()),
    ]
)

_PREPROCESSED_TYPE = pa.list_(pa.float32(), _PIXEL_VALUES_LEN)

_PROCESSOR = None


def _get_processor():  # noqa: ANN202
    global _PROCESSOR  # noqa: PLW0603
    if _PROCESSOR is None:
        from PIL import Image
        from transformers import ViTImageProcessor

        _PROCESSOR = ViTImageProcessor(
            do_convert_rgb=None,
            do_normalize=True,
            do_rescale=True,
            do_resize=True,
            image_mean=[0.5, 0.5, 0.5],
            image_std=[0.5, 0.5, 0.5],
            resample=Image.Resampling.BILINEAR,
            rescale_factor=0.00392156862745098,
            size={"height": IMAGE_SIZE, "width": IMAGE_SIZE},
        )
    return _PROCESSOR


def _decode_base64(image: bytes) -> bytes:
    try:
        import pybase64

        return pybase64.b64decode(image, None, True)
    except ModuleNotFoundError:
        return base64.b64decode(image, validate=True)


def _preprocess_image_bytes(image_bytes: bytes) -> Any:
    import numpy as np
    from PIL import Image

    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    outputs = _get_processor()(images=img)["pixel_values"]
    if len(outputs) != 1:  # pragma: no cover
        raise ValueError(f"Expected 1 image output, got {len(outputs)}")

    return np.asarray(outputs[0], dtype=np.float32).reshape(-1)


@geneva.udf(version="0.1", data_type=_DECODED_STRUCT, memory=_CPU_UDF_MEMORY_BYTES)
def decode(image: bytes | None) -> dict[str, Any] | None:
    """
    Decode base64 image bytes and extract width/height.

    Geneva maps returned dicts to pa.struct fields.
    """
    if not image:
        return None
    try:
        decoded = _decode_base64(image)
        from PIL import Image

        img = Image.open(io.BytesIO(decoded))
        width, height = img.size
        return {
            "image_bytes": decoded,
            "width": int(width),
            "height": int(height),
        }
    except Exception as exc:  # pragma: no cover
        _LOG.warning("Failed to decode image payload: %s", exc)
        return None


@geneva.udf(version="0.1", data_type=_PREPROCESSED_TYPE, memory=_CPU_UDF_MEMORY_BYTES)
def preprocess(decoded: dict[str, Any] | None) -> Any | None:
    if not decoded:
        return None

    image_bytes = decoded.get("image_bytes")
    if not image_bytes:
        return None

    try:
        return _preprocess_image_bytes(image_bytes)
    except Exception as exc:  # pragma: no cover
        _LOG.warning("Failed to preprocess image payload: %s", exc)
        return None


@geneva.udf(version="0.1", data_type=_PREPROCESSED_TYPE, memory=_CPU_UDF_MEMORY_BYTES)
def decode_and_preprocess(image: bytes | None) -> Any | None:
    if not image:
        return None

    try:
        return _preprocess_image_bytes(_decode_base64(image))
    except Exception as exc:  # pragma: no cover
        _LOG.warning("Failed to decode and preprocess image payload: %s", exc)
        return None


@geneva.udf(version="0.1", data_type=pa.list_(pa.float32(), 1000), num_gpus=1.0)
class Infer:
    def __init__(self) -> None:
        self._model: Any | None = None
        self._device: str | None = None

    def setup(self) -> None:
        import torch
        from transformers import ViTForImageClassification

        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self._device = device.type
        model_any: Any = ViTForImageClassification.from_pretrained(
            MODEL_ID
        )  # avoid Pyright issue
        self._model = model_any.to(device)
        model = self._model
        if model is None:  # pragma: no cover
            raise RuntimeError("ViT model failed to initialize")
        model.eval()

    def __call__(self, preprocessed: Any | None) -> list[float] | None:
        if preprocessed is None:
            return None

        if self._model is None or self._device is None:
            self.setup()
        model = self._model
        device = self._device
        if model is None or device is None:  # pragma: no cover
            raise RuntimeError("ViT model failed to initialize")

        import numpy as np
        import torch

        pixel_values = np.asarray(preprocessed, dtype=np.float32).reshape(
            (1, 3, IMAGE_SIZE, IMAGE_SIZE)
        )
        pixel_values = torch.from_numpy(pixel_values).to(
            dtype=torch.float32, device=device, non_blocking=True
        )

        with torch.inference_mode():
            logits = model(pixel_values=pixel_values).logits
        return logits.squeeze(0).cpu().tolist()


__all__ = ["Infer", "decode", "decode_and_preprocess", "preprocess"]
