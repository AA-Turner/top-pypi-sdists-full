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

from dataclasses import dataclass
from io import BytesIO
from typing import Any

from PIL import Image, ImageOps

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


@dataclass(frozen=True)
class FittedImage:
    """Bytes fitted to a class's bounds, and where the real picture sits in them.

    ``content`` is ``(left, top, right, bottom)`` in pixels of the fitted
    image. It is the whole image unless padding was needed, and it is what maps
    a location answered on the fitted image (a Box) back onto the source.
    """

    data: bytes
    format: str  # "jpg" | "png"
    width: int
    height: int
    content: tuple[int, int, int, int]
    source_width: int
    source_height: int

    def to_source_fractions(self, box: dict[str, float]) -> dict[str, float]:
        """Edges as fractions of the FITTED image → fractions of the source picture."""
        left, top, right, bottom = self.content
        span_x = max(right - left, 1)
        span_y = max(bottom - top, 1)

        def _clamp(value: float) -> float:
            return min(1.0, max(0.0, value))

        return {
            "left": _clamp((box["left"] * self.width - left) / span_x),
            "right": _clamp((box["right"] * self.width - left) / span_x),
            "top": _clamp((box["top"] * self.height - top) / span_y),
            "bottom": _clamp((box["bottom"] * self.height - top) / span_y),
        }


def fit_for_vision_class(master_bytes: bytes, cls: VisionApiClass) -> FittedImage:
    """Fit an arbitrary image INSIDE a class's accepted bounds, upright.

    For routes that reject rather than resize (``cls.min_edge`` set): the
    pixels are rotated upright from EXIF (the route drops EXIF unapplied), an
    animation keeps its first frame, transparency is flattened onto white, the
    long edge is held to ``cls.long_edge``, a short edge under ``cls.min_edge``
    is upscaled — or, when upscaling would break the long edge, padded with
    white and recorded in ``content`` — and the result is a baseline JPEG
    walked down in quality until it fits ``cls.max_bytes``.

    Raises ``ValueError`` with the reason when the bytes are not an image or
    cannot be made to fit.
    """
    try:
        opened = Image.open(BytesIO(master_bytes))
        opened.seek(0)
        img = ImageOps.exif_transpose(opened) or opened
        img.load()
    except Exception as exc:  # noqa: BLE001 — any decode failure is one honest refusal
        raise ValueError(f"the file is not a readable image ({exc.__class__.__name__})") from exc
    if img.mode in ("RGBA", "LA", "P"):
        rgba = img.convert("RGBA")
        flat = Image.new("RGB", rgba.size, (255, 255, 255))
        flat.paste(rgba, mask=rgba.split()[-1])
        img = flat
    elif img.mode != "RGB":
        img = img.convert("RGB")
    source_width, source_height = img.size

    scale = min(1.0, cls.long_edge / max(img.size))
    if cls.min_edge and min(img.size) * scale < cls.min_edge:
        upscale = cls.min_edge / min(img.size)
        scale = upscale if max(img.size) * upscale <= cls.long_edge else scale
    if scale != 1.0:
        new_size = (max(1, round(img.width * scale)), max(1, round(img.height * scale)))
        img = img.resize(new_size, Image.Resampling.LANCZOS)

    content = (0, 0, img.width, img.height)
    if cls.min_edge and min(img.size) < cls.min_edge:
        canvas_size = (max(img.width, cls.min_edge), max(img.height, cls.min_edge))
        canvas = Image.new("RGB", canvas_size, (255, 255, 255))
        left = (canvas_size[0] - img.width) // 2
        top = (canvas_size[1] - img.height) // 2
        canvas.paste(img, (left, top))
        content = (left, top, left + img.width, top + img.height)
        img = canvas

    quality = cls.quality
    while True:
        buf = BytesIO()
        img.save(buf, format="JPEG", quality=quality, optimize=cls.optimize,
                 subsampling=cls.subsampling, progressive=cls.progressive)
        data = buf.getvalue()
        if len(data) <= cls.max_bytes or quality <= cls.min_quality:
            break
        quality -= 5
    if len(data) > cls.max_bytes:
        raise ValueError(
            f"the image is still {len(data)} bytes at the lowest quality, over the "
            f"{cls.max_bytes}-byte limit"
        )
    return FittedImage(
        data=data,
        format="jpg",
        width=img.width,
        height=img.height,
        content=content,
        source_width=source_width,
        source_height=source_height,
    )


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


__all__ = ["FittedImage", "fit_for_vision_class", "reencode_for_vision_class", "should_skip_reencode"]
