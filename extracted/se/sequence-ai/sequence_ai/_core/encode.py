"""
Encode one camera frame to the base64 JPEG the wire carries; fit one to a camera, and read a frame's size.

Nothing here changes a frame behind the caller's back (0.34.12, contract 0.5.2): `encode` sends the frame it is given,
at its own size; `resize_image` is the tool a robot calls to fit a frame the way its policy was trained; `image_size`
reads a frame's width and height from its header.



WHY this is in `_core`: both a robot's frames (what it hands policy.observe) and the chat path (`chat.content`)
turn images into wire strings, and they must do it the same way. A second copy is a second place
for the JPEG quality or the upload cap to drift.

Pillow is imported lazily, never at module scope, so `import sequence_ai` stays quick and a caller who only ever
passes pre-encoded strings never loads it. It is a dependency since 0.34.19 - the robot fits its own frames - so the
ImportErrors below are for a broken install, and say how to repair it.
"""

from __future__ import annotations

import base64
import binascii
import io
import struct
from typing import Any


















DEFAULT_JPEG_QUALITY = 95

def encode(frame: Any, *, quality: int = DEFAULT_JPEG_QUALITY) -> str:
    """
    One camera frame to a base64 JPEG, for an input that carries its frames as text.

    `frame` may be a numpy array, a PIL image, raw `bytes` already encoded, or a `str` already base64
    — the last two pass through untouched, so a caller with their own pipeline is not forced through
    this one. Codec is JPEG at `quality`, unconditionally, at the frame's own size.

    Before 0.34.12 a frame over 640 px on its long edge was scaled down to 640 here, and the policy
    resized it again on the worker. Now the robot fits its frames itself, with `resize_image`, the way its
    policy was trained.
    """
    if isinstance(frame, str):
        return frame
    if isinstance(frame, (bytes, bytearray)):
        return base64.b64encode(bytes(frame)).decode()

    try:
        from PIL import Image
    except ImportError as e:
        raise ImportError(
            "encoding an array or PIL image needs Pillow, which sequence-ai installs; it is missing or broken here: "
            "pip install -U sequence-ai. Pass an already-encoded base64 str or bytes to avoid it."
        ) from e

    img = frame if hasattr(frame, "save") else Image.fromarray(frame)
    if img.mode != "RGB":
        img = img.convert("RGB")
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=quality)
    return base64.b64encode(buf.getvalue()).decode()








MODES = ("pad", "stretch")
FILTERS = ("nearest", "box", "bilinear", "hamming", "bicubic", "lanczos")


def _to_image(frame: Any) -> Any:
    """A frame as an RGB PIL image: a PIL image, encoded bytes (JPEG / PNG), base64 text (a data: URI too), or an
    HxWx3 uint8 array (anything Image.fromarray takes)."""
    try:
        from PIL import Image
    except ImportError as e:
        raise ImportError("fitting a frame needs Pillow, which sequence-ai installs; it is missing or broken here: "
                          "pip install -U sequence-ai") from e

    if isinstance(frame, str):
        frame = base64.b64decode(frame.split(",", 1)[1] if frame.startswith("data:") else frame, validate=False)
    if isinstance(frame, (bytes, bytearray)):
        img = Image.open(io.BytesIO(bytes(frame)))
    elif hasattr(frame, "save"):
        img = frame
    else:
        img = Image.fromarray(frame)
    return img if img.mode == "RGB" else img.convert("RGB")


def resize_image(frame: Any, width: int, height: int, *, mode: str, filter: str) -> Any:
    """
    One camera frame fitted to `width` x `height`, the way a policy was trained to see it: an RGB PIL image, for
    `encode` next. Runs on the robot; nothing is sent.

        frame = sequence_ai.resize_image(camera.read(), 224, 224, mode="pad", filter="bilinear")
        data = sequence_ai.encode(frame)

    `mode` "pad" scales the frame into the box keeping its aspect ratio and pads the rest black, centred - openpi's
    resize_with_pad exactly, what the templates' client.py ran; "stretch" scales it to the box. `filter` is the
    resampling filter, one of FILTERS (Pillow's names). Neither has a default: they are how the policy was trained,
    which its author knows. A frame already that size comes back as it is. `frame` is a PIL image, encoded JPEG /
    PNG bytes, base64 text, or an HxWx3 uint8 array.
    """
    if mode not in MODES:
        raise ValueError(f"mode must be one of {MODES}, got {mode!r}")
    if filter not in FILTERS:
        raise ValueError(f"filter must be one of {FILTERS}, got {filter!r}")
    if int(width) <= 0 or int(height) <= 0:
        raise ValueError(f"the size must be positive, got {width}x{height}")
    from PIL import Image

    img = _to_image(frame)
    if img.size == (width, height):
        return img
    resample = Image.Resampling[filter.upper()]
    if mode == "stretch":
        return img.resize((width, height), resample=resample)
    cur_width, cur_height = img.size
    ratio = max(cur_width / width, cur_height / height)
    resized_width, resized_height = int(cur_width / ratio), int(cur_height / ratio)
    resized = img.resize((resized_width, resized_height), resample=resample)
    canvas = Image.new(resized.mode, (width, height), 0)
    canvas.paste(resized, (max(0, int((width - resized_width) / 2)), max(0, int((height - resized_height) / 2))))
    return canvas


def _header_size(raw: bytes) -> tuple[int, int]:
    """(width, height) from a PNG's IHDR or a JPEG's first start-of-frame segment; ValueError otherwise."""
    if raw[:8] == b"\x89PNG\r\n\x1a\n" and raw[12:16] == b"IHDR" and len(raw) >= 24:
        return struct.unpack(">II", raw[16:24])
    if raw[:2] != b"\xff\xd8":
        raise ValueError("not a JPEG or PNG image")
    i = 2
    while i + 4 <= len(raw):
        if raw[i] != 0xFF:
            raise ValueError("a JPEG whose segments do not line up")
        marker = raw[i + 1]
        if marker == 0xFF:
            i += 1
            continue
        if marker == 0x01 or 0xD0 <= marker <= 0xD8:
            i += 2
            continue
        if marker in (0xD9, 0xDA):
            break
        if 0xC0 <= marker <= 0xCF and marker not in (0xC4, 0xC8, 0xCC) and i + 9 <= len(raw):
            height, width = struct.unpack(">HH", raw[i + 5:i + 9])
            return width, height
        i += 2 + int.from_bytes(raw[i + 2:i + 4], "big")
    raise ValueError("a JPEG with no frame header")


def image_size(data: str) -> tuple[int, int]:
    """
    (width, height) of a base64 JPEG or PNG frame - a data: URI's prefix taken off - read from its header, without
    Pillow. ValueError for anything else.
    """
    text = data.split(",", 1)[1] if isinstance(data, str) and data.startswith("data:") else data
    if not isinstance(text, str):
        raise ValueError("not base64 text")


    for part in (text[:8192], text):
        try:
            return _header_size(base64.b64decode(part, validate=False))
        except (binascii.Error, ValueError):
            if part is text:
                raise ValueError("not a JPEG or PNG image") from None
    raise ValueError("not a JPEG or PNG image")
