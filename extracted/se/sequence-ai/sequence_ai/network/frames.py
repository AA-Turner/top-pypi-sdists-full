# SPDX-FileCopyrightText: Copyright (c) 2026 General Sequences Company
# SPDX-License-Identifier: Apache-2.0
"""
A camera frame resized on the robot to the size its policy takes, before upload, and encoded as JPEG; and on the
server, turned back into the array its policy reads.

    from sequence_ai.network import frames

    frame = frames.resize_image(camera.read(), 224, 224, mode="pad", filter="bilinear")
    data = frames.encode(frame)        # a base64 JPEG, for an input that carries its frames as text

    image = frames.decode(data)        # on the server: the HxWx3 uint8 array

    observation, n = frames.pack_pictures(observation)   # each HxWx3 uint8 array in it as JPEG, under any key
    observation = frames.unpack_pictures(observation)    # on the server: each back as its array

connect() packs an observation's pictures this way when its server says it reads JPEG; serve() unpacks them.

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
import sys
from typing import Any, Optional

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
    return base64.b64encode(_jpeg(frame, quality)).decode()


def _jpeg(frame: Any, quality: int) -> bytes:
    """One frame - an array or a PIL image - as the bytes of a JPEG at `quality`, at its own size."""
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
    return buf.getvalue()


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


# ── pictures sent as JPEG, found by what they are ─────────────────────────────────────────────────────────────────────
# What a robot's connection sends in place of each picture when its server says it reads JPEG (link.py: the server's
# X-Seq-Reads names "jpeg"), and what the server restores: a map under the same reserved key as compressed.py's, so a
# reader of either format leaves the other's maps as they are.
#     {"__seq__": "jpeg", "v": 1, "data": <the picture as a JPEG, at its own size>}
# A picture is a numpy array of shape HxWx3 and dtype uint8 with both sides at least PICTURE_MIN_SIDE - what a camera
# gives and an image policy reads - or an RGB PIL image of that size, as resize_image returns it, under any key, at any
# depth of the observation. Any other array (CxHxW, HxW, HxWx4, float, smaller) is sent as it is: JPEG changes a
# picture's values a little (DEFAULT_JPEG_QUALITY has how much), which a policy that reads an image tolerates and another
# array may not.
PICTURE_KIND = "jpeg"
PICTURE_VERSION = 1
PICTURE_MIN_SIDE = 32
_MARK = "__seq__"            # compressed.MARK
_MAX_DEPTH = 64              # msgpack_io.MAX_DEPTH: nothing deeper is sent


def is_picture(value: Any) -> bool:
    """Whether `value` is a picture pack_pictures sends as JPEG: a numpy array of shape HxWx3 and dtype uint8, or an RGB
    PIL image (resize_image's), both sides at least PICTURE_MIN_SIDE."""
    if is_pil_image(value):
        width, height = value.size
        return value.mode == "RGB" and width >= PICTURE_MIN_SIDE and height >= PICTURE_MIN_SIDE
    shape = getattr(value, "shape", None)
    if getattr(getattr(value, "dtype", None), "name", None) != "uint8" or not hasattr(value, "__array_interface__"):
        return False
    return (isinstance(shape, tuple) and len(shape) == 3 and shape[2] == 3
            and shape[0] >= PICTURE_MIN_SIDE and shape[1] >= PICTURE_MIN_SIDE)


def is_pil_image(value: Any) -> bool:
    """Whether `value` is a PIL image. Pillow is not imported for it: a process that made one has it loaded. A module
    still being imported - warm() loads it on a thread of its own while the robot's first act packs - has no Image
    class yet, and nothing made from one."""
    cls = getattr(sys.modules.get("PIL.Image"), "Image", None)
    return isinstance(cls, type) and isinstance(value, cls)


def warm() -> None:
    """Load what encoding a picture as JPEG loads on its first call - Pillow and its JPEG encoder, tens of milliseconds
    - now, so the first picture sent does not wait for it. Nothing where Pillow is not installed."""
    try:
        from PIL import Image
    except ImportError:
        return
    Image.new("RGB", (8, 8)).save(io.BytesIO(), format="JPEG")


def is_packed_picture(value: Any) -> bool:
    """Whether `value` is the map pack_pictures writes for one picture."""
    return isinstance(value, dict) and value.get(_MARK) == PICTURE_KIND


def pack_pictures(value: Any, *, quality: int = DEFAULT_JPEG_QUALITY) -> "tuple[Any, int]":
    """
    `value` - an observation - with each picture in it (is_picture), in any of its dicts, lists and tuples, replaced by
    the map unpack_pictures restores: (the new value, how many pictures it holds as JPEG). The containers are new ones and
    `value` is not changed. Every other value is kept as it is. Needs Pillow, which sequence-ai installs.

        observation, pictures = frames.pack_pictures({"image": frame, "state": joints})
    """
    count = [0]

    def walk(item: Any, depth: int) -> Any:
        if depth > _MAX_DEPTH:
            return item                         # left to msgpack_io, which refuses it
        if is_picture(item):
            count[0] += 1
            return {_MARK: PICTURE_KIND, "v": PICTURE_VERSION, "data": _jpeg(item, quality)}
        if isinstance(item, dict):
            return {key: walk(inner, depth + 1) for key, inner in item.items()}
        if type(item) in (list, tuple):
            return type(item)(walk(inner, depth + 1) for inner in item)
        return item

    packed = walk(value, 0)
    return packed, count[0]


def unpack_pictures(value: Any, *, limit: Optional[int] = None) -> Any:
    """
    `value` - an observation as msgpack_io.unpack read it - with each map pack_pictures wrote turned back into its
    picture: the HxWx3 uint8 array its JPEG decodes to (decode: read-only, its values close to the robot's, not equal),
    in new containers. Every other value is returned as it is, a map of another kind under the reserved key among them
    (compressed.expand restores compressed.py's). `limit`: the most bytes one picture may decode to, read from its
    JPEG's header (width x height x 3) before anything is decoded, as compressed.expand's limit - a JPEG of a few
    kilobytes can name a picture of hundreds of megabytes. Raises ValueError, naming where it is, for a map of this kind
    of another version, whose data is not a JPEG, or whose picture is past `limit`.

        observation = frames.unpack_pictures(compressed.expand(msgpack_io.unpack(body), limit=64 << 20)[0],
                                             limit=64 << 20)
    """

    def walk(item: Any, path: str, depth: int) -> Any:
        if depth > _MAX_DEPTH:
            return item
        if is_packed_picture(item):
            where = path or "the observation"
            if item.get("v") != PICTURE_VERSION or not isinstance(item.get("data"), (bytes, bytearray)):
                raise ValueError(f"{where}: a picture of version {item.get('v')!r}, or without its JPEG bytes: this "
                                 f"reads version {PICTURE_VERSION}")
            raw = bytes(item["data"])
            if limit is not None:
                try:
                    width, height = _header_size(raw)
                except ValueError as e:
                    raise ValueError(f"{where}: {e}") from e
                if width * height * 3 > limit:
                    raise ValueError(f"{where}: a picture of {width} x {height} decodes to {width * height * 3:,} "
                                     f"bytes, past the limit of {limit:,}")
            try:
                return decode(raw)
            except ValueError as e:
                raise ValueError(f"{where}: {e}") from e
        if isinstance(item, dict):
            if _MARK in item:
                return item                     # another format's map: never looked inside
            return {key: walk(inner, f"{path}/{key}" if path else str(key), depth + 1) for key, inner in item.items()}
        if type(item) in (list, tuple):
            return type(item)(walk(inner, f"{path}[{i}]", depth + 1) for i, inner in enumerate(item))
        return item

    return walk(value, "", 0)


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
