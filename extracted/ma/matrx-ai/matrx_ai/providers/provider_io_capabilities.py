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

from enum import Enum
from typing import Any


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
    """Return request media that needs the fallback conversion seam."""
    return unsupported_inputs(
        scan_message_media(messages),
        endpoint,
        model_supports_vision=model_supports_vision,
    )


__all__ = [
    "MediaContainer",
    "endpoint_serializer_style",
    "endpoint_native_inputs",
    "is_input_natively_supported",
    "unsupported_inputs",
    "container_for_content",
    "scan_message_media",
    "find_unsupported_media",
]
