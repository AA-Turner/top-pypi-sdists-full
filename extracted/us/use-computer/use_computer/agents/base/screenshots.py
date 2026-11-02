"""Screenshot resizing helpers for vision models."""

from __future__ import annotations

import io

from PIL import Image


def screenshot_cap_for_model(model: str) -> int:
    """Long-edge cap for the resize that precedes vision input."""
    m = (model or "").lower()
    if "opus-4-7" in m or "opus-4-8" in m or "opus-5" in m:
        return 2576  # Anthropic Opus 4.7+ caps at 2576px
    if "claude" in m or "anthropic/" in m:
        return 1568  # Other Anthropic models cap at 1568px
    if "kimi" in m or "fireworks" in m:
        # Kimi: y-coord accuracy degrades at >1024
        return 896
        # TODO: probe Qwen 3.6 Plus separately — it inherits Kimi's cap for now
    return 1280  # OpenAI/Gemini fallback


def scale_screenshot_for_model(
    image_bytes: bytes, model: str
) -> tuple[bytes, int, int, float, float]:
    """Aspect-preserving resize of a screenshot to the model's vision cap.

    Returns `(resized_bytes, api_w, api_h, sx, sy)`:
        - `resized_bytes` — encoded image to send to the model
        - `api_w`, `api_h` — the resized image's dimensions
        - `sx`, `sy` — multiply model-returned coords by these to recover
          native display points
    """
    img = Image.open(io.BytesIO(image_bytes))
    native_w, native_h = img.size
    target = screenshot_cap_for_model(model)
    scale = min(target / native_w, target / native_h, 1.0)
    api_w = int(native_w * scale)
    api_h = int(native_h * scale)
    sx = native_w / api_w
    sy = native_h / api_h
    if scale == 1.0:
        return image_bytes, api_w, api_h, sx, sy
    resized = img.resize((api_w, api_h), Image.Resampling.LANCZOS)
    buf = io.BytesIO()
    fmt = (img.format or "PNG").upper()
    if fmt == "JPEG":
        resized.convert("RGB").save(buf, format="JPEG", quality=85)
    else:
        resized.save(buf, format="PNG")
    return buf.getvalue(), api_w, api_h, sx, sy
