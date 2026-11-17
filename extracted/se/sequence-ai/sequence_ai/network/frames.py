# SPDX-FileCopyrightText: Copyright (c) 2026 General Sequences Company
# SPDX-License-Identifier: Apache-2.0
"""
A camera frame resized on the robot to the size its policy takes, before upload, and encoded as JPEG; and on the
server, turned back into the array its policy reads.

    from sequence_ai.network import frames

    frame = frames.resize_image(camera.read(), 224, 224, mode="pad", filter="bilinear")
    data = frames.encode(frame)        # a base64 JPEG, for an input that carries its frames as text

    image = frames.decode(data)        # on the server: the HxWx3 uint8 array

No function here changes a frame implicitly: `encode` sends the frame it is given, at its own size; `resize_image`
resizes a frame the way a policy was trained to see it, with the mode and the filter passed explicitly and no default;
`decode` returns the picture it is given at its own size; `image_size` reads a frame's width and height from its
header, without Pillow.

WHY on the robot: a frame resized before upload is a smaller upload, and the robot's code knows how its policy was
trained.

"pad" is adapted from openpi's resize_with_pad (Apache-2.0): see THIRD_PARTY_NOTICES.md.

Pillow is imported where it is used, so importing this module costs nothing on a robot that sends no frames.
"""

from __future__ import annotations

import base64
import binascii
import io
import struct
from typing import Any

# Quality 95: the value was measured, not chosen by convention.
#
# On 50 real DROID observations (an exterior and a wrist camera, each fitted to 224 x 224), with a pi0.5 policy's
# sampling noise fixed (required: the policy draws new noise on each call), JPEG encoding changes the resulting
# action chunk - its mean |change| divided by its mean |action| - by, on average (median in brackets):
#     q100   3.1%  (1.9%)
#     q95    5.9%  (3.5%)
#     q85   10.2%  (5.8%)
#     q75   15.5%  (7.9%)
# The change grows as the quality drops. New sampling noise alone, with no JPEG, changes the chunk by 64.5%: at
# quality 95 JPEG moves the actions by about a tenth of what the policy's own sampling does.
#
# 95 and not 100: a little over half the bytes, for a change still about a tenth of the noise's. Not lower: below 95
# the change keeps growing while the bytes saved shrink - the two cameras' JPEGs are 42.3 KB together at q100,
# 23.6 KB at q95, 14.5 KB at q85 and 11.5 KB at q75, against 301 KB as arrays.
DEFAULT_JPEG_QUALITY = 95


def encode(frame: Any, *, quality: int = DEFAULT_JPEG_QUALITY) -> str:
    """
    One camera frame as a base64 JPEG, for an input that carries its frames as text.

    `frame` may be a numpy array, a PIL image, `bytes` that are already encoded, or a `str` that is already base64. A
    `str` is returned unchanged and `bytes` are only base64-encoded, so a caller with their own encoding pipeline can
    keep it. An array or a PIL image is always encoded as JPEG at `quality`, at the frame's own size.

    The frame is not resized here: the robot resizes it first with `resize_image`, the way its policy was trained.
    """
    if isinstance(frame, str):
        return frame
    if isinstance(frame, (bytes, bytearray)):
        return base64.b64encode(bytes(frame)).decode()

    try:
        from PIL import Image
    except ImportError as e:  # pragma: no cover - depends on the install
        raise ImportError(
            'encoding an array or PIL image requires Pillow, which is missing or broken: '
            'pip install pillow. Pass a base64 str or encoded bytes to avoid it.'
        ) from e

    img = frame if hasattr(frame, "save") else Image.fromarray(frame)
    if img.mode != "RGB":
        img = img.convert("RGB")
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=quality)
    return base64.b64encode(buf.getvalue()).decode()


# What decode() opens. A picture comes over the network, so Pillow is not left to choose among all the formats it can
# open: some of them hand the file to other programs.
DECODED_FORMATS = ("JPEG", "PNG")


def decode(picture: Any) -> Any:
    """
    A picture sent as JPEG or PNG, as the HxWx3 uint8 array its policy reads: the server's half of `encode`.

        image = frames.decode(observation["image"])

    `picture` is base64 text, as `encode` writes it (a data: URI is accepted), or the encoded bytes. Anything else, an
    array included, is returned unchanged, so a server can pass every picture through this whether or not its robot
    encoded it. The array holds the picture's RGB values at its own size, read-only (as msgpack_io reads an array); a
    JPEG's values are close to those of the frame it was made from, not equal to them (DEFAULT_JPEG_QUALITY has how
    close). Raises ValueError for text or bytes that are not a JPEG or PNG image.
    """
    if isinstance(picture, str):
        text = picture.partition(",")[2] if picture.startswith("data:") else picture
        try:
            raw = base64.b64decode(text, validate=False)
        except (binascii.Error, ValueError):
            raise ValueError("not a JPEG or PNG image: text that is not base64") from None
    elif isinstance(picture, (bytes, bytearray)):
        raw = bytes(picture)
    else:
        return picture
    try:
        import numpy as np
        from PIL import Image
    except ImportError as e:  # pragma: no cover - depends on the install
        raise ImportError("decoding a picture requires numpy and Pillow, one of which is missing or broken: "
                          "pip install numpy pillow") from e

    try:
        with Image.open(io.BytesIO(raw), formats=DECODED_FORMATS) as img:
            array = np.asarray(img if img.mode == "RGB" else img.convert("RGB"))
    except (OSError, ValueError, Image.DecompressionBombError) as e:
        raise ValueError("not a JPEG or PNG image that Pillow can read") from e
    array.flags.writeable = False
    return array


# ── resizing a frame, and reading its size ────────────────────────────────────────────────────────────────────────────
# The resize modes, and the resampling filters under Pillow's names: the caller always passes both. With a default
# filter, frames resampled with LANCZOS once reached a policy trained on BILINEAR ones: the filter is part of what
# a policy was trained on.
MODES = ("pad", "stretch")
FILTERS = ("nearest", "box", "bilinear", "hamming", "bicubic", "lanczos")


def _to_image(frame: Any) -> Any:
    """A frame as an RGB PIL image. `frame` is a PIL image, encoded bytes (JPEG or PNG), base64 text (a data: URI is
    accepted), or an HxWx3 uint8 array (anything Image.fromarray takes)."""
    try:
        from PIL import Image
    except ImportError as e:  # pragma: no cover - depends on the install
        raise ImportError('resizing a frame requires Pillow, which is missing or broken: '
                          'pip install pillow') from e

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
    One camera frame resized to `width` x `height`, the way a policy was trained to see it: an RGB PIL image, ready for
    `encode`. Runs on the robot; nothing is sent.

        frame = frames.resize_image(camera.read(), 224, 224, mode="pad", filter="bilinear")
        data = frames.encode(frame)

    `mode` "pad" scales the frame to fit inside the box, keeping its aspect ratio, and pads the rest with black,
    centered, exactly as openpi's resize_with_pad does; "stretch" scales it to the box. `filter` is the resampling
    filter, one of FILTERS (Pillow's names). Neither has a default: they are how the policy was trained, which its
    author knows. A frame that already has that size is not resampled. `frame` is a PIL image, encoded JPEG or PNG
    bytes, base64 text, or an HxWx3 uint8 array.
    """
    if mode not in MODES:
        raise ValueError(f"mode must be one of {MODES}, got {mode!r}")
    if filter not in FILTERS:
        raise ValueError(f"filter must be one of {FILTERS}, got {filter!r}")
    if int(width) <= 0 or int(height) <= 0:
        raise ValueError(f"the size must be positive, got {width}x{height}")
    try:
        from PIL import Image
    except ImportError as e:  # pragma: no cover - depends on the install
        raise ImportError('resizing a frame requires Pillow, which is not installed: '
                          'pip install pillow') from e

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
            raise ValueError("a JPEG with a malformed segment")
        marker = raw[i + 1]
        if marker == 0xFF:                                   # a fill byte before the marker
            i += 1
            continue
        if marker == 0x01 or 0xD0 <= marker <= 0xD8:         # markers that carry no length
            i += 2
            continue
        if marker in (0xD9, 0xDA):                           # the image's end, or its data, before any frame header
            break
        if 0xC0 <= marker <= 0xCF and marker not in (0xC4, 0xC8, 0xCC) and i + 9 <= len(raw):
            height, width = struct.unpack(">HH", raw[i + 5:i + 9])
            return width, height
        i += 2 + int.from_bytes(raw[i + 2:i + 4], "big")
    raise ValueError("a JPEG with no frame header")


def image_size(data: str) -> tuple[int, int]:
    """
    (width, height) of a base64 JPEG or PNG frame (a data: URI's prefix is removed first), read from its header without
    Pillow. Raises ValueError for anything else.
    """
    text = data.split(",", 1)[1] if isinstance(data, str) and data.startswith("data:") else data
    if not isinstance(text, str):
        raise ValueError("not base64 text")
    # The header is near the start: decode a prefix first, and the whole frame only when the prefix does not contain
    # it (a large metadata segment before a JPEG's frame header). This can run on every request.
    for part in (text[:8192], text):
        try:
            return _header_size(base64.b64decode(part, validate=False))
        except (binascii.Error, ValueError):
            if part is text:
                raise ValueError("not a JPEG or PNG image") from None
    raise ValueError("not a JPEG or PNG image")  # pragma: no cover - the loop returns or raises
