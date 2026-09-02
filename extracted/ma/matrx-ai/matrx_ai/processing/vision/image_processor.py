"""Pillow-based image re-encoding for a given ``VisionApiClass``.

Implements the algorithm from
``packages/matrx-ai/matrx_ai/config/tool_config_image_processing_spec.md``:

  1. Decode source bytes with Pillow, convert to RGB.
  2. Downscale (LANCZOS) so long edge equals ``cls.long_edge`` — never upscale.
  3. Encode as JPEG with the class's ``quality`` / ``subsampling`` /
     ``progressive`` / ``optimize`` flags.
  4. If output exceeds ``cls.max_bytes``, drop quality by 5 and re-encode
     until the cap is satisfied or ``min_quality`` is hit.

The functions here are pure — no I/O, no DB, no cloud. They take bytes in
and return bytes out. Wire them up at the variant render layer.
"""

from __future__ import annotations

from io import BytesIO
from typing import Any

from PIL import Image

from .vision_classes import VisionApiClass


def reencode_for_vision_class(
    master_bytes: bytes,
    cls: VisionApiClass,
    *,
    ocr_mode: bool = False,
) -> bytes:
    """Re-encode ``master_bytes`` for the given ``VisionApiClass``.

    ``ocr_mode=True`` swaps to 4:4:4 chroma subsampling and bumps quality
    to at least 90, matching the spec's OCR override.
    """
    img = Image.open(BytesIO(master_bytes))
    if img.mode != "RGB":
        img = img.convert("RGB")

    long_edge = max(img.size)
    if long_edge > cls.long_edge:
        scale = cls.long_edge / long_edge
        new_size = (round(img.width * scale), round(img.height * scale))
        img = img.resize(new_size, Image.Resampling.LANCZOS)

    quality = max(cls.quality, 90) if ocr_mode else cls.quality
    subsampling = 0 if ocr_mode else cls.subsampling
    fmt = cls.format.upper()

    save_kwargs: dict[str, Any] = {
        "format": fmt,
        "optimize": cls.optimize,
    }
    if fmt in ("JPEG", "WEBP"):
        save_kwargs["quality"] = quality
    if fmt == "JPEG":
        save_kwargs["subsampling"] = subsampling
        save_kwargs["progressive"] = cls.progressive

    buf = BytesIO()
    img.save(buf, **save_kwargs)
    out = buf.getvalue()

    while len(out) > cls.max_bytes and quality > cls.min_quality and fmt in ("JPEG", "WEBP"):
        quality -= 5
        save_kwargs["quality"] = quality
        buf = BytesIO()
        img.save(buf, **save_kwargs)
        out = buf.getvalue()

    return out


def should_skip_reencode(master_meta: dict[str, Any] | None, cls: VisionApiClass) -> bool:
    """Pass-through guard from gotcha #5 of the spec.

    Returns True when the master is already JPEG at smaller-or-equal long
    edge AND equal-or-higher quality than the target class — re-encoding
    would only lose detail. Caller should hand the master bytes through
    unchanged when this returns True.

    ``master_meta`` is the dict the screenshot tool emits (see spec § 1):
    keys ``media_type`` / ``format`` / ``width`` / ``height`` / ``profile``.
    Conservative: when any required hint is missing, return False so we
    do the safe thing and re-encode.
    """
    if not master_meta:
        return False
    media_type = (master_meta.get("media_type") or "").lower()
    fmt = (master_meta.get("format") or "").lower()
    if not (media_type.startswith("image/jpeg") or fmt == "jpeg"):
        return False
    if cls.format.upper() != "JPEG":
        return False
    width = master_meta.get("width")
    height = master_meta.get("height")
    if not isinstance(width, int) or not isinstance(height, int):
        return False
    if max(width, height) > cls.long_edge:
        return False
    # We don't have the exact JPEG quality on the wire — the spec's
    # default master is q=88. Trust that figure when the master profile
    # is the documented "auto" master; otherwise be conservative.
    profile = (master_meta.get("profile") or "").lower()
    if profile not in ("auto", "lossless"):
        return False
    if cls.quality > 88:
        return False
    return True


__all__ = ["reencode_for_vision_class", "should_skip_reencode"]
