# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors
"""Render small valid images and pad them to a deterministic target byte size.

Fidelity is byte-size only: we render a valid (decodable) PNG/JPEG from the
derived summary text, then append deterministic padding past the image EOF
(decoders ignore trailing bytes) to reach the target size. For small targets the
text render is replaced by a minimal image so the target can still be hit.
"""

from __future__ import annotations

import functools
import io
import logging
import os
from typing import TYPE_CHECKING, NamedTuple

from loadtest.azure_scale_bench import constants, image_distribution

if TYPE_CHECKING:
    from PIL import ImageFont

_LOG = logging.getLogger(__name__)


class PayloadResult(NamedTuple):
    """A generated image payload plus the metadata describing it."""

    image_bytes: bytes
    actual_bytes: int
    target_bytes: int
    bucket: str
    image_format: str
    font: str
    background_color: str
    summary_in_image: str


@functools.lru_cache(maxsize=64)
def _load_font(
    font_name: str, size: int, font_dir: str | None
) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    """Load a TrueType font, falling back to Pillow's default font."""
    from PIL import ImageFont

    file_name = constants.FONT_FILE_MAP.get(font_name)
    search_dir = font_dir or constants.DEFAULT_FONT_DIR
    if file_name and search_dir:
        path = os.path.join(search_dir, file_name)
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except OSError as exc:  # pragma: no cover - font load edge
                _LOG.debug("truetype load failed for %s: %s", path, exc)
    try:
        return ImageFont.load_default(size)
    except TypeError:  # pragma: no cover - older Pillow without size arg
        return ImageFont.load_default()


def _normalize_format(image_format: str) -> tuple[str, str]:
    """Return (pil_format, normalized_name) for ``png``/``jpeg``."""
    fmt = image_format.lower()
    if fmt in ("jpg", "jpeg"):
        return "JPEG", "jpeg"
    return "PNG", "png"


def normalize_format_name(image_format: str) -> str:
    """The normalized format name (``png``/``jpeg``) for a requested format."""
    return _normalize_format(image_format)[1]


def render_text_image(
    text: str,
    font_name: str,
    background_rgb: tuple[int, int, int],
    *,
    width: int,
    height: int,
    image_format: str,
    font_dir: str | None = None,
) -> bytes:
    """Render centered, word-wrapped text on a colored background (mmlb-style)."""
    from PIL import Image, ImageDraw

    pil_format, _ = _normalize_format(image_format)
    img = Image.new("RGB", (width, height), background_rgb)
    draw = ImageDraw.Draw(img)

    scale = min(width, height) / constants.DEFAULT_IMAGE_SIZE
    font_size = max(1, int(constants.BASE_FONT_SIZE * scale))
    line_height = max(1, int(constants.BASE_LINE_HEIGHT * scale))
    font = _load_font(font_name, font_size, font_dir)

    words = text.split()
    lines = [
        " ".join(words[i : i + constants.WORDS_PER_LINE])
        for i in range(0, len(words), constants.WORDS_PER_LINE)
    ] or [""]

    total_height = line_height * len(lines)
    y = max(0, (height - total_height) // 2)
    for line in lines:
        line_width = draw.textlength(line, font=font)
        x = max(0, int((width - line_width) // 2))
        draw.text((x, y), line, fill=constants.TEXT_COLOR, font=font)
        y += line_height

    buffer = io.BytesIO()
    if pil_format == "JPEG":
        img.save(buffer, format="JPEG", quality=85)
    else:
        img.save(buffer, format="PNG", optimize=True)
    return buffer.getvalue()


def render_minimal_image(
    background_rgb: tuple[int, int, int], image_format: str
) -> bytes:
    """Smallest valid image, used when the target is below the text render."""
    from PIL import Image

    pil_format, _ = _normalize_format(image_format)
    img = Image.new("RGB", (1, 1), background_rgb)
    buffer = io.BytesIO()
    img.save(buffer, format=pil_format)
    return buffer.getvalue()


def render_base_under_target(
    text: str,
    font_name: str,
    background_rgb: tuple[int, int, int],
    target: int,
    *,
    width: int,
    height: int,
    image_format: str,
    font_dir: str | None = None,
) -> bytes:
    """Largest renderable base image not exceeding ``target`` where possible.

    Uses the full text render when it fits the target; otherwise a minimal image
    so padding can reach small targets. For targets below the minimal image the
    minimal image is returned (actual will then exceed target).
    """
    full = render_text_image(
        text,
        font_name,
        background_rgb,
        width=width,
        height=height,
        image_format=image_format,
        font_dir=font_dir,
    )
    if len(full) <= target:
        return full
    return render_minimal_image(background_rgb, image_format)


def pad_to_target(image_bytes: bytes, target: int, pad_byte: int) -> bytes:
    """Append deterministic padding past the image EOF to reach ``target``.

    Returns the input unchanged when it already meets or exceeds the target.
    """
    if len(image_bytes) >= target:
        return image_bytes
    pad_len = target - len(image_bytes)
    return image_bytes + bytes([pad_byte & 0xFF]) * pad_len


def build_payload(
    row_index: int,
    summary: str | None,
    *,
    width: int = constants.DEFAULT_IMAGE_SIZE,
    height: int = constants.DEFAULT_IMAGE_SIZE,
    image_format: str = "png",
    include_large_tail: bool = False,
    max_bytes: int | None = None,
    font_dir: str | None = None,
) -> PayloadResult:
    """Generate the full deterministic image payload for one row.

    Combines the deterministic attribute/bucket/target derivation with the
    render-and-pad step. Pure with respect to ``(row_index, summary)`` and the
    knobs, so it is fully testable without Ray or Azure.
    """
    _, normalized_format = _normalize_format(image_format)
    attrs = image_distribution.derive_attrs(row_index, summary)
    assignment = image_distribution.assign(
        row_index, include_large_tail=include_large_tail, max_bytes=max_bytes
    )
    base = render_base_under_target(
        attrs.summary_in_image,
        attrs.font,
        attrs.background_rgb,
        assignment.target,
        width=width,
        height=height,
        image_format=normalized_format,
        font_dir=font_dir,
    )
    payload = pad_to_target(
        base, assignment.target, image_distribution.pad_byte(row_index)
    )
    return PayloadResult(
        image_bytes=payload,
        actual_bytes=len(payload),
        target_bytes=assignment.target,
        bucket=assignment.bucket,
        image_format=normalized_format,
        font=attrs.font,
        background_color=attrs.background_color,
        summary_in_image=attrs.summary_in_image,
    )


def decode_size(image_bytes: bytes) -> tuple[int, int]:
    """Decode an image with Pillow and return ``(width, height)``."""
    from PIL import Image

    with Image.open(io.BytesIO(image_bytes)) as img:
        img.load()
        return img.size
