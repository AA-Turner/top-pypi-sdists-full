"""Provider-level input/output capability registry — the PROVIDER half of the
capability system (the model-level half is ``resolved_capabilities.py``).

Whether a model can SEE an image or HEAR audio is largely a property of the model
(a text-only model on a vision-capable provider still can't see) — that lives in
``resolved_capabilities`` (per ``ai_model`` row). But whether a PDF, a video file,
or a YouTube URL can be sent at all is a property of the PROVIDER's API / translator
(every Claude model accepts a document; no Groq model does) — that lives HERE.

The truth is the ``.to_<provider>()`` serializers in ``config/media_config.py``: a
container is natively accepted by a serializer style iff that style returns a real
payload (not ``None``) for it. This registry is a faithful, VERIFIED transcription
of those serializers — ``tests/test_provider_io_capabilities.py`` probes the real
content classes so the registry can NEVER silently drift from the translators.

The registry is observation-only; the media-fallback preprocessor consumes its result
to convert unsupported inputs or terminate explicitly before provider dispatch.
"""

from __future__ import annotations

import logging
from enum import Enum
from typing import Any

_log = logging.getLogger(__name__)


class MediaContainer(str, Enum):
    TEXT = "text"
    IMAGE = "image"
    AUDIO = "audio"
    VIDEO = "video"  # a video FILE (mp4 etc.), distinct from a YouTube URL
    YOUTUBE = "youtube"  # a YouTube URL passed through natively (Gemini only)
    DOCUMENT = "document"  # a PDF / document file


# The four distinct serializer styles in media_config.py. Each provider endpoint
# maps to exactly one. (TEXT is implicit for every chat style.)
_STYLE_ANTHROPIC = "anthropic"  # ImageContent/DocumentContent.to_anthropic()
_STYLE_OPENAI_RESPONSES = "openai_responses"  # ...to_openai()  (Responses API)
_STYLE_GOOGLE = "google"  # ...to_google()
_STYLE_OPENAI_CHAT = "openai_chat"  # ...to_openai_chat()  (chat-completions)
_STYLE_MOONSHOT_CHAT = "moonshot_chat"  # ...to_moonshot_chat()


# VERIFIED against config/media_config.py serializers (2026-06-17). A container is
# listed iff its content class returns a non-None payload for that style:
#   • to_anthropic: Image ✓, Document ✓; Audio/Video/YouTube → None
#   • to_openai (Responses): Image ✓, Document ✓; Audio/Video/YouTube → None
#   • to_google: Image ✓, Audio ✓, Video ✓, YouTube ✓, Document ✓
#   • to_openai_chat: ONLY ImageContent defines it → Image ✓; everything else absent
# The self-verifying test asserts this exactly — update both together.
_STYLE_NATIVE_INPUTS: dict[str, frozenset[MediaContainer]] = {
    _STYLE_ANTHROPIC: frozenset(
        {MediaContainer.TEXT, MediaContainer.IMAGE, MediaContainer.DOCUMENT}
    ),
    _STYLE_OPENAI_RESPONSES: frozenset(
        {MediaContainer.TEXT, MediaContainer.IMAGE, MediaContainer.DOCUMENT}
    ),
    _STYLE_GOOGLE: frozenset(
        {
            MediaContainer.TEXT,
            MediaContainer.IMAGE,
            MediaContainer.AUDIO,
            MediaContainer.VIDEO,
            MediaContainer.YOUTUBE,
            MediaContainer.DOCUMENT,
        }
    ),
    _STYLE_OPENAI_CHAT: frozenset({MediaContainer.TEXT, MediaContainer.IMAGE}),
    _STYLE_MOONSHOT_CHAT: frozenset(
        {MediaContainer.TEXT, MediaContainer.IMAGE, MediaContainer.VIDEO}
    ),
}


# What an ASSISTANT turn may carry, where it is narrower than the style's inputs. Only Gemini
# replays media on its ``model`` turn. The Claude API refuses an ``image`` block in an assistant
# message ("'image' blocks are not permitted within assistant turns", live 2026-11-10: every
# Claude reply after a made picture) and a ``document`` one (version 2026-10-21); the Responses
# API takes ``output_text`` / ``refusal`` only; Chat Completions takes ``image_url`` on a user
# message only. Such media is CARRIED to a host-written user turn by the send boundary
# (``config/assistant_turn_media.py``), so the model still sees what it made; a translator names
# whatever slips past. A document still there at the fallback seam is converted to text.
_STYLE_ASSISTANT_NATIVE_INPUTS: dict[str, frozenset[MediaContainer]] = {
    _STYLE_ANTHROPIC: frozenset({MediaContainer.TEXT}),
    _STYLE_OPENAI_RESPONSES: frozenset({MediaContainer.TEXT}),
    _STYLE_OPENAI_CHAT: frozenset({MediaContainer.TEXT}),
    _STYLE_MOONSHOT_CHAT: frozenset({MediaContainer.TEXT}),
}


def assistant_turn_refuses(content: Any, endpoint: str | None) -> bool:
    """Whether THIS media part may not ride an assistant turn on ``endpoint``'s wire style.

    Text and non-media parts (tool calls, thinking) are never refused. An unknown or non-chat
    endpoint refuses nothing (the caller does not guess)."""
    container = container_for_content(content)
    if container is None or container is MediaContainer.TEXT:
        return False
    carried = _STYLE_ASSISTANT_NATIVE_INPUTS.get(endpoint_serializer_style(endpoint) or "")
    return carried is not None and container not in carried


# Chat wire_format (ai.api.translator_key == the UnifiedAIClient dispatch attr) → serializer style.
# Only chat endpoints take user-message media; media-generation endpoints
# (openai_image, google_video, *_tts, …) are output-side and return None here.
_ENDPOINT_STYLE: dict[str, str] = {
    "anthropic_chat": _STYLE_ANTHROPIC,
    "openai_chat": _STYLE_OPENAI_RESPONSES,
    "google_chat": _STYLE_GOOGLE,
    "groq_chat": _STYLE_OPENAI_CHAT,
    "xai_chat": _STYLE_OPENAI_CHAT,
    "cerebras_chat": _STYLE_OPENAI_CHAT,
    "together_chat": _STYLE_OPENAI_CHAT,
    "generic_openai_chat": _STYLE_OPENAI_CHAT,
    "huggingface_chat": _STYLE_OPENAI_CHAT,
    "moonshot_chat": _STYLE_MOONSHOT_CHAT,
    # llama-server on a person's device speaks chat-completions (images only).
    "device_chat": _STYLE_OPENAI_CHAT,
}


# Audio is handled by its dedicated software fallback: when a provider
# can't accept audio natively, `processing/audio` transcribes it to text before
# dispatch (degraded but never dropped). So audio is "handled" on every chat
# endpoint even where it isn't native. Other media routes through the registered
# media-fallback resolver seam.
_CONTAINERS_WITH_TRANSCODE_FALLBACK: frozenset[MediaContainer] = frozenset(
    {MediaContainer.AUDIO}
)


def endpoint_serializer_style(endpoint: str | None) -> str | None:
    return _ENDPOINT_STYLE.get(endpoint or "")


def endpoint_native_inputs(endpoint: str | None) -> frozenset[MediaContainer] | None:
    """Containers the endpoint's provider API accepts NATIVELY. ``None`` for a
    non-chat / unknown endpoint (caller should treat unknown as 'don't assume')."""
    style = endpoint_serializer_style(endpoint)
    if style is None:
        return None
    return _STYLE_NATIVE_INPUTS[style]


async def model_media_inputs(model_id: str | None) -> frozenset[str]:
    """THE media kinds (``image`` · ``audio`` · ``video`` · ``document`` · ``youtube``) a model
    takes natively — the one capability check every Source delivery uses (aidream's
    ``resolve_source_set`` when it resolves, matrx-ai's replay gate when a stored turn is sent
    again). Two halves, never a name list: the model row's declared input modalities
    (``resolve_model_capabilities``) AND what its provider route's serializer accepts
    (:func:`endpoint_native_inputs` for the route ``ai_catalog_manager.wire_format_for`` picks).
    A document needs vision too, exactly as ``UnifiedAIClient`` decides native PDF input.
    Unknown model → empty: text, never a guess."""
    if not model_id:
        return frozenset()
    try:
        from matrx_ai.catalog.manager import ai_catalog_manager
        from matrx_ai.db.ai_models.ai_model_manager import ai_model_manager_instance
        from matrx_ai.providers.resolved_capabilities import resolve_model_capabilities

        row = await ai_model_manager_instance.load_model(model_id)
        if row is None:
            return frozenset()
        await ai_catalog_manager.ensure_loaded()
        native = endpoint_native_inputs(ai_catalog_manager.wire_format_for(model_id)) or frozenset()
        caps = resolve_model_capabilities(row)
        declared = getattr(row, "capabilities", None)
        declared_input = {
            str(token).strip().lower()
            for token in ((declared or {}).get("input") or [] if isinstance(declared, dict) else [])
        }
    except Exception as exc:  # noqa: BLE001 — an unknown capability is text, never a guess
        _log.warning("media capability unavailable for %r: %s", model_id, exc)
        return frozenset()
    kinds: set[str] = set()
    if caps.supports_vision and MediaContainer.IMAGE in native:
        kinds.add("image")
    if caps.supports_audio_input and MediaContainer.AUDIO in native:
        kinds.add("audio")
    if "video" in declared_input and MediaContainer.VIDEO in native:
        kinds.add("video")
    if caps.supports_vision and MediaContainer.DOCUMENT in native:
        kinds.add("document")
    if MediaContainer.YOUTUBE in native:
        kinds.add("youtube")
    return frozenset(kinds)


def is_input_natively_supported(container: MediaContainer, endpoint: str | None) -> bool:
    native = endpoint_native_inputs(endpoint)
    return native is not None and container in native


def unsupported_inputs(
    containers_present: set[MediaContainer],
    endpoint: str | None,
    *,
    audio_has_transcribe_fallback: bool = True,
    model_supports_vision: bool | None = None,
) -> set[MediaContainer]:
    """Return inputs requiring conversion before provider dispatch."""
    native = endpoint_native_inputs(endpoint)
    if native is None:
        unsupported: set[MediaContainer] = set()
    else:
        handled = set(native)
        if audio_has_transcribe_fallback:
            handled |= _CONTAINERS_WITH_TRANSCODE_FALLBACK
        unsupported = {c for c in containers_present if c not in handled}
    if model_supports_vision is False and MediaContainer.IMAGE in containers_present:
        unsupported.add(MediaContainer.IMAGE)
    return unsupported


# ── classifying the media in a request ───────────────────────────────────────
# Maps the media content classes (config/media_config.py) to a MediaContainer by
# class name, so this module needs no import of the content classes (keeps it a
# leaf). The boundary already constructs the right class per media kind.
_CONTENT_CLASS_CONTAINER: dict[str, MediaContainer] = {
    "ImageContent": MediaContainer.IMAGE,
    "AudioContent": MediaContainer.AUDIO,
    "VideoContent": MediaContainer.VIDEO,
    "YouTubeVideoContent": MediaContainer.YOUTUBE,
    "DocumentContent": MediaContainer.DOCUMENT,
}


def container_for_content(content: Any) -> MediaContainer | None:
    return _CONTENT_CLASS_CONTAINER.get(type(content).__name__)


def _document_natively_serializable(content: Any, style: str) -> bool:
    """Whether THIS document's format has a representation in the style's serializer.

    The container answer ("Anthropic accepts documents") is not enough: the
    serializers represent a document only as a PDF or as decoded UTF-8 text
    (``DocumentContent.to_anthropic`` / ``to_openai``), and Gemini's inline
    document slot takes PDF and ``text/*`` only. A .docx/.xlsx/.pptx/.doc or any
    other binary therefore must be CONVERTED before dispatch — before PB-05
    (2026-10-18) it passed the container check and the serializer returned
    ``None``, dropping the file with a console line only. Mirrors the
    serializers exactly; ``tests/test_attachment_every_kind_arrives.py`` asserts
    this predicate and the real serializers never disagree.
    """
    from matrx_ai.config.media_config import decode_document_text, is_pdf_mime

    mime = getattr(content, "mime_type", None)
    if is_pdf_mime(mime):
        return True
    b64 = getattr(content, "base64_data", None)
    if style == _STYLE_GOOGLE:
        if getattr(content, "file_uri", None) and str(content.file_uri).startswith("gs://"):
            return True
        return bool(b64) and (mime or "").split(";")[0].strip().lower().startswith("text/")
    if style in (_STYLE_ANTHROPIC, _STYLE_OPENAI_RESPONSES):
        if b64:
            return decode_document_text(b64) is not None
        # No bytes: the url-source path. Only a PDF url is representable in fact,
        # but an unresolved url is the boundary's to fetch; leave it native.
        return bool(getattr(content, "resolved_url", None) or getattr(content, "url", None))
    return False


def content_needs_fallback(
    content: Any,
    endpoint: str | None,
    *,
    model_supports_vision: bool | None = None,
    role: Any = None,
) -> bool:
    """Whether this ONE media item must go through the fallback seam before dispatch.

    Per item, never per container: a PDF beside a .docx stays a native PDF while
    the .docx is converted. ``role`` narrows by the turn the item rides on
    (``_STYLE_ASSISTANT_NATIVE_INPUTS``).
    """
    container = container_for_content(content)
    if container is None or container is MediaContainer.TEXT:
        return False
    if container is MediaContainer.IMAGE and model_supports_vision is False:
        return True
    native = endpoint_native_inputs(endpoint)
    if native is None:
        return False
    if str(getattr(role, "value", role)) == "assistant" and container is not MediaContainer.IMAGE:
        # A picture on an assistant turn is carried (send boundary) or named (translator),
        # never turned into OCR text: the model made it and should keep seeing it.
        if assistant_turn_refuses(content, endpoint):
            return True
    if container in _CONTAINERS_WITH_TRANSCODE_FALLBACK:
        return False
    if container not in native:
        return True
    if container is MediaContainer.DOCUMENT:
        style = endpoint_serializer_style(endpoint)
        return not _document_natively_serializable(content, style or "")
    return False


def scan_message_media(messages: Any) -> set[MediaContainer]:
    """Best-effort set of non-text media containers present in a MessageList /
    list of messages. Never raises — a shape it doesn't understand contributes
    nothing."""
    present: set[MediaContainer] = set()
    try:
        msgs = messages.to_list() if hasattr(messages, "to_list") else messages
        for message in msgs or []:
            for content in getattr(message, "content", None) or []:
                c = container_for_content(content)
                if c is not None and c is not MediaContainer.TEXT:
                    present.add(c)
    except Exception:  # noqa: BLE001 — classification must never break a caller
        return present
    return present


def find_unsupported_media(
    messages: Any,
    endpoint: str | None,
    *,
    model_supports_vision: bool | None = None,
) -> set[MediaContainer]:
    """Return the containers of every request media item that needs the fallback seam."""
    found = unsupported_inputs(
        scan_message_media(messages),
        endpoint,
        model_supports_vision=model_supports_vision,
    )
    try:
        msgs = messages.to_list() if hasattr(messages, "to_list") else messages
        for message in msgs or []:
            for content in getattr(message, "content", None) or []:
                if content_needs_fallback(
                    content,
                    endpoint,
                    model_supports_vision=model_supports_vision,
                    role=getattr(message, "role", None),
                ):
                    container = container_for_content(content)
                    if container is not None:
                        found.add(container)
    except Exception:  # noqa: BLE001 — classification must never break a caller
        return found
    return found


__all__ = [
    "MediaContainer",
    "endpoint_serializer_style",
    "endpoint_native_inputs",
    "model_media_inputs",
    "is_input_natively_supported",
    "unsupported_inputs",
    "container_for_content",
    "content_needs_fallback",
    "scan_message_media",
    "find_unsupported_media",
]
