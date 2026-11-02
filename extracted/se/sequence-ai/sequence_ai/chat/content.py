"""
Content blocks for chat messages: an image, and a text block marked for the prompt cache.

    messages = [
        {"role": "system", "content": "You plan pick-and-place for a six-axis arm."},
        {"role": "user", "content": [
            sequence_ai.cached(long_manual),            # reused every turn → read from cache
            sequence_ai.image("frame.jpg"),
            {"type": "text", "text": "Where is the red block?"},
        ]},
    ]

Both return plain dicts in the wire shape — nothing here is required; a caller with their own
blocks can keep them.
"""

from __future__ import annotations

import base64
import binascii
import os
from typing import Any

from ..errors import InvalidRequest



_SIGNATURES = (
    (b"\x89PNG\r\n\x1a\n", "image/png"),
    (b"\xff\xd8\xff", "image/jpeg"),
    (b"GIF87a", "image/gif"),
    (b"GIF89a", "image/gif"),
)


def _sniff(raw: bytes) -> str:
    """The image MIME type of `raw` from its magic bytes; refuses anything that is not PNG/JPEG/WebP/GIF."""
    for sig, mime in _SIGNATURES:
        if raw.startswith(sig):
            return mime
    if raw[:4] == b"RIFF" and raw[8:12] == b"WEBP":
        return "image/webp"
    raise InvalidRequest("not a PNG, JPEG, WebP or GIF image — the formats chat models accept")


def image(source: Any, *, detail: str | None = None) -> dict[str, Any]:
    """
    An image content block for chat(): `{"type": "image_url", "image_url": {"url": "data:..."}}`.

    `source` may be:
      - a file path (str or os.PathLike) to a PNG / JPEG / WebP / GIF,
      - the raw bytes of such an image,
      - a PIL image or a numpy array — scaled down to 640 px on its long edge when larger (CHAT_MAX_EDGE: a
        language model has its own size limits), then encoded to JPEG,
      - an existing base64 string or `data:image/...;base64,` URI — passed through.

    Why a data URI and never a URL: the gateway does not fetch URLs, and a model that receives an
    image it cannot read drops it silently — so only an inline image reliably arrives, and the
    gateway refuses anything else up front. `detail` ("low" / "high" / "auto") is forwarded for the
    models that support it.
    """
    url = _data_uri(source)
    block: dict[str, Any] = {"type": "image_url", "image_url": {"url": url}}
    if detail is not None:
        block["image_url"]["detail"] = detail
    return block


def _data_uri(source: Any) -> str:
    if isinstance(source, str) and source.startswith("data:image/"):
        return source
    if isinstance(source, (str, os.PathLike)) and os.path.isfile(source):
        with open(source, "rb") as f:
            raw = f.read()
        return f"data:{_sniff(raw)};base64,{base64.b64encode(raw).decode()}"
    if isinstance(source, (bytes, bytearray, memoryview)):
        raw = bytes(source)
        return f"data:{_sniff(raw)};base64,{base64.b64encode(raw).decode()}"
    if isinstance(source, str):

        try:
            head = base64.b64decode(source[:64] + "=" * (-len(source[:64]) % 4), validate=False)
        except (binascii.Error, ValueError):
            raise InvalidRequest("image(): a string must be a file path, base64, or a data: URI") from None
        return f"data:{_sniff(head)};base64,{source}"


    from .._core.encode import _to_image, encode

    img = _to_image(source)
    if max(img.size) > CHAT_MAX_EDGE:
        from PIL import Image

        scale = CHAT_MAX_EDGE / max(img.size)


        img = img.resize((max(1, round(img.width * scale)), max(1, round(img.height * scale))), Image.LANCZOS)
    return f"data:image/jpeg;base64,{encode(img)}"







CHAT_MAX_EDGE = 640


def cached(text: str, *, ttl: str | None = None) -> dict[str, Any]:
    """
    A text content block marked as a prompt-cache breakpoint: everything up to and including it is
    cached by the models that need an explicit marker (Claude, Qwen, Gemini other than 2.5) and read
    back at a fraction of the input price on the next call with the same prefix. Models that cache on
    their own (GPT, GLM, ...) ignore the marker, so it is safe on any model.

    The gateway already marks the end of your system prompt automatically; use this for a large
    prefix it cannot know is stable — a long document, a manual, few-shot examples. Placing any
    marker yourself turns the automatic one off for that request, so you keep full control (Claude
    allows four per request). `ttl="1h"` keeps the entry an hour instead of five minutes (Claude),
    worth it when turns are minutes apart.
    """
    if ttl not in (None, "5m", "1h"):
        raise InvalidRequest('cached(): ttl must be "5m" or "1h"')
    marker: dict[str, Any] = {"type": "ephemeral"}
    if ttl is not None:
        marker["ttl"] = ttl
    return {"type": "text", "text": text, "cache_control": marker}
