"""Vision input — let sage CLI users attach images to messages.

The cloud:llava-next-7b model (Cloud Run GPU vLLM) accepts the OpenAI
vision-API payload shape: messages with content as a LIST of typed parts
(text + image_url). This module bridges sage's CLI/agent layer (which
takes plain prompt strings and file paths) to that shape.

Typical flow:
    msg = build_vision_message("what's in this?", [Path("screenshot.png")])
    response = sage_agent.send(messages=[msg])  # → routes to cloud:llava-next-7b
"""

from __future__ import annotations

import base64
from dataclasses import dataclass
from pathlib import Path
from typing import Union

# Max image size we'll send to the cloud model. ~10 MB is plenty for a
# typical screenshot; bigger and we blow the model's context window with
# image tokens. Users can resize first if they hit this.
_MAX_IMAGE_BYTES = 10 * 1024 * 1024


# Map imghdr's identifiers to canonical MIME types.
_IMGHDR_TO_MIME = {
    "png": "image/png",
    "jpeg": "image/jpeg",
    "jpg": "image/jpeg",
    "gif": "image/gif",
    "webp": "image/webp",
    "bmp": "image/bmp",
}


def _guess_image_type(h: bytes) -> str | None:
    if h.startswith(b"\x89PNG\r\n\x1a\n"):
        return "png"
    if h.startswith(b"\xff\xd8"):
        return "jpeg"
    if h.startswith(b"GIF87a") or h.startswith(b"GIF89a"):
        return "gif"
    if h.startswith(b"RIFF") and len(h) >= 12 and h[8:12] == b"WEBP":
        return "webp"
    if h.startswith(b"BM"):
        return "bmp"
    return None


@dataclass(frozen=True)
class VisionAttachment:
    """An image ready to send to a vision model. ``data_url`` is the
    `data:image/<type>;base64,<payload>` form the OpenAI API expects."""
    source_path: Path
    mime_type: str
    data_url: str


def encode_image_for_vision(path: Path | str) -> VisionAttachment:
    """Load an image and encode it as a data URL suitable for the
    OpenAI/LLaVA-NeXT vision API.

    Raises:
        FileNotFoundError: if `path` doesn't exist
        ValueError: if the file isn't a recognized image or is too large
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Image file not found: {path}")

    raw = path.read_bytes()
    if len(raw) > _MAX_IMAGE_BYTES:
        size_mb = len(raw) / 1024 / 1024
        raise ValueError(
            f"Image too large ({size_mb:.1f} MB). "
            f"Max {_MAX_IMAGE_BYTES // 1024 // 1024} MB to fit the model context. "
            "Resize before attaching."
        )

    # Use helper to identify by content (more reliable than file extension).
    # If content check fails, fall back to extension as a last resort.
    fmt = _guess_image_type(raw)
    mime = _IMGHDR_TO_MIME.get(fmt) if fmt else None
    if mime is None:
        # Last-ditch: trust the extension if it's a known image type
        ext = path.suffix.lower().lstrip(".")
        mime = _IMGHDR_TO_MIME.get(ext)
    if mime is None:
        raise ValueError(
            f"File {path.name!r} is not an image (or format not recognized). "
            "Supported: PNG, JPEG, GIF, WebP, BMP."
        )

    encoded = base64.b64encode(raw).decode("ascii")
    return VisionAttachment(
        source_path=path,
        mime_type=mime,
        data_url=f"data:{mime};base64,{encoded}",
    )


def build_vision_message(
    prompt: str,
    image_paths: list[Path | str],
) -> dict:
    """Build an OpenAI-shaped chat message with vision input.

    When ``image_paths`` is empty, returns the simple string-content form
    (``{"role": "user", "content": "<prompt>"}``) so plain-text calls
    don't accidentally get sent as malformed multimodal payloads.

    When images are attached, the content becomes a list of typed parts:
        [{"type": "text", "text": prompt},
         {"type": "image_url", "image_url": {"url": "data:..."}}]

    Per OpenAI guidance, text comes first to anchor the model's attention.
    """
    if not image_paths:
        return {"role": "user", "content": prompt}

    parts: list[dict] = [{"type": "text", "text": prompt}]
    for img_path in image_paths:
        attachment = encode_image_for_vision(img_path)
        parts.append({
            "type": "image_url",
            "image_url": {"url": attachment.data_url},
        })

    return {"role": "user", "content": parts}


__all__ = [
    "VisionAttachment",
    "encode_image_for_vision",
    "build_vision_message",
]
