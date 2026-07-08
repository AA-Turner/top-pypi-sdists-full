"""
Canonical multimodal message parts for AI Red Teaming.

A trial's input (candidate) and output (response) are represented as an ordered list of
``MessagePart`` dicts. Text parts carry their text inline; media parts (image/audio/video)
carry a *content-addressed reference* to bytes stored once on the trial span
(``span.log_artifact`` → ``sha256:`` oid in ``dreadnode.artifacts``), never inline base64.

The shape is a lossless superset of the OpenAI / Anthropic / Gemini content-part models
(discriminated ``source`` union: artifact | url | file_id) so it round-trips faithfully and
the platform can resolve refs to presigned inline URLs for display.
"""

import io
import tempfile
import typing as t
from pathlib import Path

from loguru import logger

if t.TYPE_CHECKING:
    from dreadnode.core.types import Audio, Image, Video
    from dreadnode.tracing.span import TaskSpan

_MIME_BY_EXT = {
    "png": "image/png",
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg",
    "gif": "image/gif",
    "webp": "image/webp",
    "bmp": "image/bmp",
    "mp3": "audio/mpeg",
    "wav": "audio/wav",
    "ogg": "audio/ogg",
    "flac": "audio/flac",
    "m4a": "audio/mp4",
    "mp4": "video/mp4",
    "webm": "video/webm",
    "mov": "video/quicktime",
}


def _mime_for_extension(ext: str | None, default: str) -> str:
    if not ext:
        return default
    return _MIME_BY_EXT.get(ext.lower().lstrip("."), default)


def text_part(
    text: str,
    *,
    transform: str | None = None,
    variant: str | None = None,
) -> dict[str, t.Any]:
    """Build a canonical text message part.

    ``transform``/``variant`` record provenance when a *text* transform was
    applied, so the UI can attribute the transform to the text part (not only
    to image/audio/video parts).
    """
    part: dict[str, t.Any] = {"kind": "text", "text": text}
    if transform:
        part["transform"] = transform
    if variant:
        part["variant"] = variant
    return part


def _store_bytes_as_artifact(
    span: "TaskSpan",
    data: bytes,
    *,
    filename: str,
) -> dict[str, t.Any] | None:
    """Persist bytes as a content-addressed span artifact, return the artifact metadata.

    The artifact's MIME type is inferred from ``filename`` by ``log_artifact``; the
    caller supplies the canonical ``media_type`` on the resulting part separately.
    """
    suffix = Path(filename).suffix or ""
    try:
        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
            tmp.write(data)
            tmp_path = Path(tmp.name)
        try:
            return span.log_artifact(tmp_path, name=filename)
        finally:
            tmp_path.unlink(missing_ok=True)
    except Exception:
        # Storage may be unconfigured (e.g. local unit tests) — degrade to no media ref
        # rather than failing the trial. The text parts still carry the attack content.
        logger.debug("Failed to store media artifact for message part", exc_info=True)
        return None


def _media_part(
    span: "TaskSpan",
    data: bytes,
    *,
    kind: str,
    media_type: str,
    filename: str,
    transform: str | None,
    variant: str | None,
    caption: str | None,
) -> dict[str, t.Any]:
    """Build a media message part, storing bytes as a content-addressed artifact."""
    meta = _store_bytes_as_artifact(span, data, filename=filename)
    source: dict[str, t.Any] = {
        "ref": "artifact",
        "media_type": (meta.get("mime_type") if meta else None) or media_type,
        "byte_size": (meta.get("size") if meta else None) or len(data),
        "filename": (meta.get("name") if meta else None) or filename,
    }
    if meta and meta.get("oid"):
        source["artifact_oid"] = meta["oid"]
    part: dict[str, t.Any] = {"kind": kind, "source": source}
    if transform:
        part["transform"] = transform
    if variant:
        part["variant"] = variant
    if caption:
        part["caption"] = caption
    return part


def image_part(
    span: "TaskSpan",
    image: "Image",
    *,
    transform: str | None = None,
    variant: str | None = None,
    filename: str = "image.png",
) -> dict[str, t.Any]:
    """Build an image message part from an ``Image``, storing its bytes as an artifact."""
    try:
        data, metadata = image.to_serializable()
        media_type = _mime_for_extension(metadata.get("extension"), "image/png")
        caption = metadata.get("caption")
    except Exception:
        buffer = io.BytesIO()
        image.to_pil().save(buffer, format="PNG")
        data, media_type, caption = buffer.getvalue(), "image/png", None
    return _media_part(
        span,
        data,
        kind="image",
        media_type=media_type,
        filename=filename,
        transform=transform,
        variant=variant,
        caption=caption,
    )


def audio_part(
    span: "TaskSpan",
    audio: "Audio",
    *,
    transform: str | None = None,
    variant: str | None = None,
    filename: str = "audio",
) -> dict[str, t.Any]:
    """Build an audio message part from an ``Audio``, storing its bytes as an artifact."""
    data, metadata = audio.to_serializable()
    ext = metadata.get("extension", "mp3")
    media_type = _mime_for_extension(ext, "audio/mpeg")
    name = filename if Path(filename).suffix else f"{filename}.{ext}"
    return _media_part(
        span,
        data,
        kind="audio",
        media_type=media_type,
        filename=name,
        transform=transform,
        variant=variant,
        caption=metadata.get("transcript"),
    )


def video_part(
    span: "TaskSpan",
    video: "Video",
    *,
    transform: str | None = None,
    variant: str | None = None,
    filename: str = "video",
) -> dict[str, t.Any]:
    """Build a video message part from a ``Video``, storing its bytes as an artifact."""
    data, metadata = video.to_serializable()
    ext = metadata.get("extension", "mp4")
    media_type = _mime_for_extension(ext, "video/mp4")
    name = filename if Path(filename).suffix else f"{filename}.{ext}"
    return _media_part(
        span,
        data,
        kind="video",
        media_type=media_type,
        filename=name,
        transform=transform,
        variant=variant,
        caption=None,
    )


def modality_from_parts(parts: list[dict[str, t.Any]]) -> str:
    """Derive input_modality from the kinds present in a part list."""
    kinds = {str(p.get("kind")) for p in parts if p.get("kind")}
    media = kinds - {"text"}
    if not media:
        return "text"
    if len(media) == 1:
        return next(iter(media))  # "image" | "audio" | "video"
    return "multimodal"


def response_to_parts(
    span: "TaskSpan",
    response: t.Any,
) -> list[dict[str, t.Any]]:
    """
    Build response message parts from a target's output.

    Handles text-out targets (str), media-out targets (Image/Audio/Video), and mixed
    outputs (a Message, or a list/dict containing media). Media bytes are stored as
    content-addressed artifacts; text is inlined.
    """
    from dreadnode.core.types import Audio, Image, Video

    parts: list[dict[str, t.Any]] = []

    def _walk(value: t.Any) -> None:
        if value is None:
            return
        if isinstance(value, str):
            if value:
                parts.append(text_part(value))
        elif isinstance(value, Image):
            parts.append(image_part(span, value, variant="output", filename="response.png"))
        elif isinstance(value, Audio):
            parts.append(audio_part(span, value, variant="output", filename="response"))
        elif isinstance(value, Video):
            parts.append(video_part(span, value, variant="output", filename="response"))
        elif isinstance(value, dict):
            # A Message-like dict or provider payload — walk content/parts if present.
            for key in ("content", "content_parts", "parts", "text"):
                if key in value:
                    _walk(value[key])
                    return
            parts.append(text_part(str(value)))
        elif isinstance(value, (list, tuple)):
            for item in value:
                _walk(item)
        else:
            # Message object or unknown — try content_parts, else stringify.
            content = getattr(value, "content_parts", None) or getattr(value, "content", None)
            if content is not None and not isinstance(content, str):
                _walk(content)
            else:
                parts.append(text_part(str(value)))

    _walk(response)
    return parts or [text_part("")]
