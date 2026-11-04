"""Check a base64 image before it goes to a model API.

A model API rejects a corrupt image with an error, and some agent harnesses
then loop on that error. A frame can have a valid header and a first part
that decodes, and still be corrupt later in its data. A header, size or
dimension check does not catch such a frame. Only a full decode does.

:func:`check_image_b64` does that decode for every format it accepts:

- strict base64, and the base64 length under the API per-image limit;
- the format from the magic bytes (PNG, JPEG, GIF, WebP), never from the
  declared label, so a wrong ``media_type`` label cannot reach the API;
- width and height in ``1..MAX_DIMENSION``;
- PNG: a decode with the standard library only. It checks each chunk CRC,
  IHDR first, IDAT present, an IEND chunk, and the full zlib stream
  inflated to exactly the size that the IHDR dimensions require, with a
  filter type of 0-4 on each scanline. Bytes after IEND and data after the
  zlib stream end are ignored, as libpng and Pillow do;
- JPEG: SOI, an SOFn marker with the dimensions and EOI at the end;
- GIF and WebP: the header dimensions;
- JPEG, GIF and WebP: then a full Pillow decode. Pillow is a required
  dependency of this SDK. If Pillow cannot be imported (a broken install),
  these formats are rejected as ``unchecked`` and are not sent, because a
  header check alone does not find a corrupt body.

A 1280x720 desktop PNG takes about 1-3 ms.
"""

from __future__ import annotations

import base64
import binascii
import struct
import zlib
from collections.abc import Iterator
from enum import StrEnum

from pydantic import BaseModel

# The Anthropic API limit is 5 MB per image. This limit is on the base64 text,
# which is larger than the decoded bytes, so the check is conservative.
MAX_B64_CHARS = 5 * 1024 * 1024
# The API rejects an image with a side larger than 8000 px.
MAX_DIMENSION = 8000
# The PNG check inflates at most this many bytes at a time.
_INFLATE_BLOCK = 1024 * 1024

_PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
# PNG color type -> (channels, permitted bit depths).
_PNG_COLOR_TYPES: dict[int, tuple[int, frozenset[int]]] = {
    0: (1, frozenset({1, 2, 4, 8, 16})),  # grayscale
    2: (3, frozenset({8, 16})),  # RGB
    3: (1, frozenset({1, 2, 4, 8})),  # palette
    4: (2, frozenset({8, 16})),  # grayscale + alpha
    6: (4, frozenset({8, 16})),  # RGBA
}
# Adam7 passes as (x start, y start, x step, y step).
_ADAM7_PASSES = ((0, 0, 8, 8), (4, 0, 8, 8), (0, 4, 4, 8), (2, 0, 4, 4), (0, 2, 2, 4), (1, 0, 2, 2), (0, 1, 1, 2))
# JPEG SOFn markers: C0-CF, except DHT (C4), JPG (C8) and DAC (CC).
_JPEG_SOF_MARKERS = frozenset(range(0xC0, 0xD0)) - {0xC4, 0xC8, 0xCC}
# JPEG markers that have no length field: TEM, RST0-7, SOI, EOI.
_JPEG_STANDALONE_MARKERS = frozenset({0x01, *range(0xD0, 0xDA)})


class ImageRejectReason(StrEnum):
    """Why :func:`check_image_b64` rejected an image."""

    BAD_BASE64 = "bad_base64"
    TOO_LARGE = "too_large"
    UNKNOWN_FORMAT = "unknown_format"
    BAD_DIMENSIONS = "bad_dimensions"
    CORRUPT = "corrupt"
    UNCHECKED = "unchecked"


class ImageCheck(BaseModel):
    """Result of :func:`check_image_b64`.

    ``media_type`` is the type found in the bytes. Send this type to the API,
    not the declared one.
    """

    ok: bool
    reason: ImageRejectReason | None = None
    detail: str = ""
    media_type: str | None = None
    declared_media_type: str | None = None
    width: int | None = None
    height: int | None = None
    byte_size: int = 0
    b64_size: int = 0


class _Reject(Exception):
    def __init__(self, reason: ImageRejectReason, detail: str) -> None:
        super().__init__(detail)
        self.reason = reason
        self.detail = detail


def _corrupt(detail: str) -> _Reject:
    return _Reject(ImageRejectReason.CORRUPT, detail)


def _check_dimensions(width: int, height: int) -> None:
    if not (1 <= width <= MAX_DIMENSION and 1 <= height <= MAX_DIMENSION):
        raise _Reject(
            ImageRejectReason.BAD_DIMENSIONS,
            f"{width}x{height} is outside 1..{MAX_DIMENSION} px",
        )


def _png_row_bytes(width: int, bits_per_pixel: int) -> int:
    """Bytes in one PNG scanline, including its filter-type byte."""
    return 1 + (width * bits_per_pixel + 7) // 8


def _png_row_layout(width: int, height: int, bits_per_pixel: int, interlaced: bool) -> list[tuple[int, int]]:
    """(bytes in one scanline, scanline count) for each pass that has pixels.

    A plain PNG has one pass. An Adam7 PNG has up to seven.
    """
    if not interlaced:
        return [(_png_row_bytes(width, bits_per_pixel), height)]
    layout = []
    for x0, y0, dx, dy in _ADAM7_PASSES:
        pass_w = (width - x0 + dx - 1) // dx if width > x0 else 0
        pass_h = (height - y0 + dy - 1) // dy if height > y0 else 0
        if pass_w and pass_h:
            layout.append((_png_row_bytes(pass_w, bits_per_pixel), pass_h))
    return layout


def _png_expected_size(layout: list[tuple[int, int]]) -> int:
    return sum(row_bytes * rows for row_bytes, rows in layout)


def _png_filter_offsets(layout: list[tuple[int, int]]) -> Iterator[int]:
    """The offset of each scanline filter-type byte in the inflated data."""
    offset = 0
    for row_bytes, rows in layout:
        for _ in range(rows):
            yield offset
            offset += row_bytes


def _check_png(raw: bytes) -> tuple[int, int]:
    """Fully check a PNG and return its (width, height)."""
    pos = len(_PNG_SIGNATURE)
    end = len(raw)
    width = height = 0
    expected = 0
    inflater: zlib._Decompress | None = None
    inflated = 0
    filter_offsets: Iterator[int] = iter(())
    next_filter: int | None = None
    seen_idat = False
    seen_plte = False
    color_type = -1

    while True:
        if pos + 12 > end:
            raise _corrupt(f"truncated: no IEND chunk (data ends at byte {end})")
        (length,) = struct.unpack_from(">I", raw, pos)
        chunk_type = raw[pos + 4 : pos + 8]
        if length > 0x7FFFFFFF or pos + 12 + length > end:
            raise _corrupt(f"truncated {chunk_type!r} chunk at byte {pos}")
        data_start = pos + 8
        data_end = data_start + length
        (crc,) = struct.unpack_from(">I", raw, data_end)
        if zlib.crc32(raw[pos + 4 : data_end]) != crc:
            raise _corrupt(f"bad CRC in {chunk_type!r} chunk at byte {pos}")

        if pos == len(_PNG_SIGNATURE):
            if chunk_type != b"IHDR" or length != 13:
                raise _corrupt("the first chunk is not a 13-byte IHDR")
            width, height, bit_depth, color_type, compression, filter_method, interlace = struct.unpack_from(
                ">IIBBBBB", raw, data_start
            )
            _check_dimensions(width, height)
            spec = _PNG_COLOR_TYPES.get(color_type)
            if spec is None or bit_depth not in spec[1]:
                raise _corrupt(f"bad IHDR: color type {color_type} with bit depth {bit_depth}")
            if compression != 0 or filter_method != 0 or interlace not in (0, 1):
                raise _corrupt("bad IHDR: unknown compression, filter or interlace method")
            layout = _png_row_layout(width, height, spec[0] * bit_depth, interlace == 1)
            expected = _png_expected_size(layout)
            filter_offsets = _png_filter_offsets(layout)
            next_filter = next(filter_offsets, None)
            inflater = zlib.decompressobj()
        elif chunk_type == b"IHDR":
            raise _corrupt(f"second IHDR chunk at byte {pos}")
        elif chunk_type == b"PLTE":
            seen_plte = True
        elif chunk_type == b"IDAT":
            assert inflater is not None
            if color_type == 3 and not seen_plte:
                raise _corrupt("palette image has no PLTE chunk before IDAT")
            seen_idat = True
            # Data after the end of the zlib stream is ignored, as libpng
            # and Pillow do (libpng gives only a warning).
            if not inflater.eof:
                pending = raw[data_start:data_end]
                while pending and not inflater.eof:
                    # Inflate at most one block at a time, and never more
                    # than the image needs, so peak memory stays near one
                    # block for any image and for a decompression bomb.
                    limit = min(expected - inflated + 1, _INFLATE_BLOCK)
                    try:
                        out = inflater.decompress(pending, limit)
                    except zlib.error as exc:
                        raise _corrupt(f"zlib error in IDAT chunk at byte {pos}: {exc}") from None
                    base = inflated
                    inflated += len(out)
                    if inflated > expected:
                        raise _corrupt(f"pixel data is larger than {expected} bytes")
                    # Each scanline starts with a filter-type byte, and only
                    # types 0-4 exist. libpng rejects any other value.
                    while next_filter is not None and next_filter < inflated:
                        filter_type = out[next_filter - base]
                        if filter_type > 4:
                            raise _corrupt(f"bad filter type {filter_type} at pixel byte {next_filter}")
                        next_filter = next(filter_offsets, None)
                    pending = inflater.unconsumed_tail
        elif chunk_type == b"IEND":
            if not seen_idat:
                raise _corrupt("no IDAT chunk")
            # Bytes after IEND are ignored, as libpng and Pillow do.
            break
        pos = data_end + 4

    assert inflater is not None
    if not inflater.eof:
        raise _corrupt(f"the zlib stream is incomplete ({inflated} of {expected} pixel bytes)")
    if inflated != expected:
        raise _corrupt(f"pixel data is {inflated} bytes, the IHDR needs {expected}")
    return width, height


def _pillow_decode(raw: bytes, media_type: str) -> None:
    """Fully decode ``raw`` with Pillow, or raise :class:`_Reject`.

    Pillow is a required dependency of this SDK. If it cannot be imported
    (a broken install), the image is rejected as unchecked, because only a
    full decode finds a corrupt body.
    """
    try:
        from io import BytesIO

        from PIL import Image
    except ImportError:
        raise _Reject(
            ImageRejectReason.UNCHECKED,
            f"Pillow is not installed, so the {media_type} body cannot be decoded",
        ) from None
    try:
        with Image.open(BytesIO(raw)) as img:
            img.load()
    except Exception as exc:
        raise _corrupt(f"Pillow cannot decode the image: {exc}") from None


def _check_jpeg(raw: bytes) -> tuple[int, int]:
    end = len(raw)
    if raw[-2:] != b"\xff\xd9":
        raise _corrupt("no EOI marker at the end")
    pos = 2
    dims: tuple[int, int] | None = None
    while True:
        if pos + 2 > end or raw[pos] != 0xFF:
            raise _corrupt(f"bad marker at byte {pos}")
        while pos < end and raw[pos] == 0xFF:  # fill bytes
            pos += 1
        if pos >= end:
            raise _corrupt("truncated marker")
        marker = raw[pos]
        pos += 1
        if marker in _JPEG_STANDALONE_MARKERS:
            if marker == 0xD9:
                raise _corrupt("EOI before the image data")
            continue
        if pos + 2 > end:
            raise _corrupt(f"truncated segment 0x{marker:02X}")
        (seg_len,) = struct.unpack_from(">H", raw, pos)
        if seg_len < 2 or pos + seg_len > end:
            raise _corrupt(f"bad length in segment 0x{marker:02X} at byte {pos}")
        if marker in _JPEG_SOF_MARKERS:
            if seg_len < 7:
                raise _corrupt("SOF segment is too short")
            height, width = struct.unpack_from(">HH", raw, pos + 3)
            dims = (width, height)
        if marker == 0xDA:  # SOS: entropy-coded data follows
            break
        pos += seg_len
    if dims is None:
        raise _corrupt("no SOF marker before the image data")
    _check_dimensions(*dims)
    _pillow_decode(raw, "image/jpeg")
    return dims


def _check_gif(raw: bytes) -> tuple[int, int]:
    if len(raw) < 10:
        raise _corrupt("truncated GIF header")
    width, height = struct.unpack_from("<HH", raw, 6)
    _check_dimensions(width, height)
    _pillow_decode(raw, "image/gif")
    return width, height


def _check_webp(raw: bytes) -> tuple[int, int]:
    if len(raw) < 30:
        raise _corrupt("truncated WebP header")
    (riff_size,) = struct.unpack_from("<I", raw, 4)
    if riff_size + 8 > len(raw):
        raise _corrupt(f"truncated: the RIFF header says {riff_size + 8} bytes, the data has {len(raw)}")
    chunk = raw[12:16]
    data = raw[20:]
    if chunk == b"VP8 ":
        if data[3:6] != b"\x9d\x01\x2a":
            raise _corrupt("bad VP8 start code")
        width, height = (v & 0x3FFF for v in struct.unpack_from("<HH", data, 6))
    elif chunk == b"VP8L":
        if data[0] != 0x2F:
            raise _corrupt("bad VP8L signature")
        (bits,) = struct.unpack_from("<I", data, 1)
        width, height = 1 + (bits & 0x3FFF), 1 + ((bits >> 14) & 0x3FFF)
    elif chunk == b"VP8X":
        width = 1 + int.from_bytes(data[4:7], "little")
        height = 1 + int.from_bytes(data[7:10], "little")
    else:
        raise _corrupt(f"unknown WebP chunk {chunk!r}")
    _check_dimensions(width, height)
    _pillow_decode(raw, "image/webp")
    return width, height


def _detect(raw: bytes) -> str | None:
    if raw.startswith(_PNG_SIGNATURE):
        return "image/png"
    if raw.startswith(b"\xff\xd8\xff"):
        return "image/jpeg"
    if raw[:6] in (b"GIF87a", b"GIF89a"):
        return "image/gif"
    if raw[:4] == b"RIFF" and raw[8:12] == b"WEBP":
        return "image/webp"
    return None


_CHECKERS = {
    "image/png": _check_png,
    "image/jpeg": _check_jpeg,
    "image/gif": _check_gif,
    "image/webp": _check_webp,
}


def check_image_b64(data: str, declared_media_type: str | None = None) -> ImageCheck:
    """Check that ``data`` is a base64 image that a model API accepts.

    The result never raises: a bad image gives ``ok=False`` with a reason
    and a short detail. On success, ``media_type`` is the detected type.
    """
    b64_size = len(data) if isinstance(data, str) else 0
    result = ImageCheck(ok=False, declared_media_type=declared_media_type, b64_size=b64_size)
    if not isinstance(data, str) or not data:
        result.reason = ImageRejectReason.BAD_BASE64
        result.detail = "empty or not a string"
        return result
    if b64_size > MAX_B64_CHARS:
        result.reason = ImageRejectReason.TOO_LARGE
        result.detail = f"{b64_size} base64 chars, the limit is {MAX_B64_CHARS}"
        return result
    try:
        raw = base64.b64decode(data, validate=True)
    except (binascii.Error, ValueError) as exc:
        result.reason = ImageRejectReason.BAD_BASE64
        result.detail = str(exc)
        return result
    result.byte_size = len(raw)

    media_type = _detect(raw)
    if media_type is None:
        result.reason = ImageRejectReason.UNKNOWN_FORMAT
        result.detail = f"unknown magic bytes {raw[:8].hex()}"
        return result
    result.media_type = media_type
    try:
        result.width, result.height = _CHECKERS[media_type](raw)
    except _Reject as rej:
        result.reason = rej.reason
        result.detail = rej.detail
        return result
    except (struct.error, IndexError, ValueError) as exc:
        result.reason = ImageRejectReason.CORRUPT
        result.detail = f"truncated or malformed {media_type}: {exc}"
        return result
    result.ok = True
    return result
