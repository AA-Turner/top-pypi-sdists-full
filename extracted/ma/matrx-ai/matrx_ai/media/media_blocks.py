"""THE ONE media-block builder — a durable media reference → the runtime's block.

Every place in the platform that needs an agent to SEE or HEAR media it holds
only a reference to (a ``file_id``, one of our durable URLs, an external
``https://``) builds the block HERE. Before 2026-08-22 three private copies of
this function existed (the workflow image-pipeline node and two flashcard call
sites); the Provision media channel (``aidream/services/mandates/provisions.py``)
needed a fourth, so the copies collapsed into this one.

🚨 **THE BLOCK TYPE COMES FROM THE MIME TYPE.** This builder emitted a hardcoded
``"type": "image"`` until 2026-08-22, which was invisible while every caller
passed a picture — and silently wrong the moment one passed a recording (the
spoken graders' answer clips). ``UnifiedMessage.parse_content`` deserializes
``image`` / ``audio`` / ``video`` into three different content classes, and a
provider translator hands each to a different part of the request. Resolved
``audio/*`` bytes labeled ``image`` reach the model as a broken picture, never
as something it can listen to. So the mime decides, and the fallback stays
``image/png`` ONLY when nothing told us otherwise.

The block is the shape ``UnifiedMessage.parse_content`` already understands
(``ImageContent`` / ``AudioContent`` / ``VideoContent``): ``{"type": <kind>,
"base64_data", "mime_type", "is_resolved", "file_id" | "url", "metadata"}``.
Resolution goes through the host-injected
``FileManager.resolve_media_async`` (idempotent, cache-first — external URLs are
byte-cached by URL hash), exactly as the provider boundary resolves every other
image item. Identity travels beside the bytes: a ``file_id`` or the DURABLE url
the caller supplied — never ``resolved_url`` (a signed handoff, never an
identity; ``common-docs/systems/files/media-durability/FEATURE.md``).
"""

from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)


#: mime prefix → the block ``type`` ``UnifiedMessage.parse_content`` deserializes.
_BLOCK_TYPE_BY_MIME_PREFIX: dict[str, str] = {
    "audio/": "audio",
    "video/": "video",
    "image/": "image",
    # A text file (plain, markdown, csv, html) is a ``document``: ``DocumentContent`` decodes it to text for every
    # provider (``to_openai`` / ``to_anthropic``; Google takes the text mime inline). Labelled ``image`` it reached
    # the model as a broken picture (review of 1f0b51a3c0b, finding 4).
    "text/": "document",
}


#: exact mime → block ``type``. A PDF is a ``document`` (``DocumentContent``): labelled ``image`` it reached the
#: provider as a broken picture (Matrx Scan helpers, 2026-11-19: every saved scan is a PDF and the counter answered
#: "the attached photo could not be read").
_BLOCK_TYPE_BY_EXACT_MIME: dict[str, str] = {"application/pdf": "document"}


def block_type_for_mime(mime_type: str | None, *, unknown: str = "image") -> str:
    """The runtime block ``type`` for a mime — THE one mime → media-kind table (``agent_testing.input_parts.kind_for``
    in aidream asks here too).

    ``audio/*`` / ``video/*`` / ``image/*`` by prefix; PDF, Office (docx/pptx/xlsx and legacy doc/ppt/xls), HTML and
    text formats → ``document``, exactly the families the media fallback's extractor reads
    (``processing/media_fallback/resolvers.document_format``): a provider that takes the format natively gets it
    natively, any other gets the extracted text (``content_needs_fallback`` per item). Labelled ``image`` a docx
    reached the model as a broken picture. Anything else → ``unknown``, which stays ``image`` for this builder because
    that is what it always emitted and every picture call site relies on.
    """
    lowered = (mime_type or "").strip().lower()
    bare = lowered.split(";", 1)[0].strip()
    exact = _BLOCK_TYPE_BY_EXACT_MIME.get(bare)
    if exact:
        return exact
    for prefix, block_type in _BLOCK_TYPE_BY_MIME_PREFIX.items():
        if lowered.startswith(prefix):
            return block_type
    if bare:
        from matrx_ai.processing.media_fallback.resolvers import document_format

        if document_format(bare, ""):
            return "document"
    return unknown


#: A mime that names no type at all: the media kind cannot be decided from it.
_NO_TYPE_MIMES = frozenset({"", "application/octet-stream", "binary/octet-stream"})


def known_mime(mime_type: str | None, name: str | None = None) -> str | None:
    """The media's real mime, or ``None`` when nothing says what it is.

    A stated mime wins unless it names no type (absent / ``application/octet-stream``); then the file name's or the
    url path's extension decides, through matrx-files' upload sniff (``media_sniff.sniff_mime_type`` — the same
    extension table every upload is stamped with; no bytes are fetched). ``None`` means the kind CANNOT be known:
    a caller that saves a reference refuses it in plain words then, never labels it a guess that fails at replay
    (re-verify of 2c1bef229b6: a mime-less photo url was saved as a ``document``).
    """
    stated = (mime_type or "").strip().lower().split(";", 1)[0].strip()
    if stated not in _NO_TYPE_MIMES:
        return stated
    if not name or not str(name).strip():
        return None
    from urllib.parse import urlsplit

    from matrx_files.media_sniff import sniff_mime_type

    raw = str(name).strip()
    path = urlsplit(raw).path if "://" in raw else raw
    guessed = sniff_mime_type(claimed=None, head_bytes=b"", filename=path.rsplit("/", 1)[-1])
    return None if guessed in _NO_TYPE_MIMES else guessed


async def resolve_media_block(
    ref: Any,
    *,
    access_label: str,
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any] | None:
    """Resolve ``ref`` (a ``MediaRef`` / wire dict / file id / url) to a media block.

    Returns ``None`` when the bytes cannot be produced: no host FileManager is
    registered (standalone install — the caller may fall back to a url block the
    provider boundary resolves), the reference carries no identifier, or the
    resolver failed. Never raises.
    """
    from matrx_files.cloud_sync.media_ref import MediaRef, coerce_to_media_ref

    from matrx_ai._ext import get_ext, has_ext

    try:
        media_ref = coerce_to_media_ref(ref)
    except (TypeError, ValueError) as exc:
        logger.warning("[media_blocks] unusable media reference %r: %s", ref, exc)
        return None
    if media_ref is None:
        return None
    if not has_ext("get_cloud_file_manager"):
        return None
    try:
        fm = get_ext("get_cloud_file_manager")()
    except Exception as exc:  # noqa: BLE001 — standalone/misconfigured host: caller falls back
        logger.warning("[media_blocks] get_cloud_file_manager() raised: %s", exc)
        return None

    from matrx_utils.ctx import system_file_access

    # A fresh MediaRef so an already-resolved input is never mutated in place.
    working: MediaRef = (
        media_ref if not media_ref.is_resolved else MediaRef(**_identity_fields(media_ref))
    )
    try:
        with system_file_access(access_label):
            await fm.resolve_media_async(working, needs_bytes=True)
    except Exception as exc:  # noqa: BLE001 — the caller decides; an image that won't resolve is not fatal here
        logger.warning(
            "[media_blocks] media reference did not resolve (%s): %s",
            _describe(media_ref),
            exc,
        )
        return None
    base64_data = getattr(working, "base64_data", None)
    if not base64_data:
        logger.warning(
            "[media_blocks] media reference resolved without bytes (%s): %s",
            _describe(media_ref),
            getattr(working, "resolver_error", None) or "no base64_data",
        )
        return None
    mime_type = getattr(working, "mime_type", None) or "image/png"
    block: dict[str, Any] = {
        "type": block_type_for_mime(mime_type),
        "base64_data": base64_data,
        "mime_type": mime_type,
        "is_resolved": True,
    }
    # Identity beside the bytes — a file id when the file is ours, else the
    # durable url the caller handed us. Never the minted ``resolved_url``.
    file_id = getattr(working, "file_id", None) or media_ref.file_id
    if file_id:
        block["file_id"] = str(file_id)
    elif media_ref.url:
        block["url"] = media_ref.url
    if metadata:
        block["metadata"] = dict(metadata)
    return block


def _identity_fields(ref: Any) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for name in ("file_id", "url", "file_uri"):
        value = getattr(ref, name, None)
        if value:
            out[name] = value
            break
    mime = getattr(ref, "mime_type", None)
    if mime:
        out["mime_type"] = mime
    return out


def _describe(ref: Any) -> str:
    for name in ("file_id", "url", "file_uri"):
        value = getattr(ref, name, None)
        if value:
            return f"{name}={str(value)[:120]}"
    return "no identifier"


__all__ = ["block_type_for_mime", "known_mime", "resolve_media_block"]
