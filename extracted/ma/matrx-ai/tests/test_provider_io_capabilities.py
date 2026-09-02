"""The provider I/O registry must match the ACTUAL serializers — drift-proof.

`provider_io_capabilities._STYLE_NATIVE_INPUTS` is a transcription of the
`.to_<provider>()` methods in config/media_config.py. This probes the real content
classes (does each serializer return a payload or None/absent?) and asserts the
registry equals reality, so the two can never silently diverge.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from matrx_ai.config.media_config import (
    AudioContent,
    DocumentContent,
    ImageContent,
    VideoContent,
    YouTubeVideoContent,
)
from matrx_ai.providers import provider_io_capabilities as pio
from matrx_ai.providers.provider_io_capabilities import (
    MediaContainer,
    endpoint_native_inputs,
    scan_message_media,
    unsupported_inputs,
)

_B64 = "aGVsbG8="  # "hello"


def _samples() -> dict[MediaContainer, object]:
    return {
        MediaContainer.IMAGE: ImageContent(base64_data=_B64, mime_type="image/png"),
        MediaContainer.AUDIO: AudioContent(base64_data=_B64, mime_type="audio/mp3"),
        MediaContainer.VIDEO: VideoContent(base64_data=_B64, mime_type="video/mp4"),
        MediaContainer.YOUTUBE: YouTubeVideoContent(
            url="https://www.youtube.com/watch?v=abc123"
        ),
        MediaContainer.DOCUMENT: DocumentContent(base64_data=_B64, mime_type="application/pdf"),
    }


_STYLE_METHOD = {
    pio._STYLE_ANTHROPIC: "to_anthropic",
    pio._STYLE_OPENAI_RESPONSES: "to_openai",
    pio._STYLE_GOOGLE: "to_google",
    pio._STYLE_OPENAI_CHAT: "to_openai_chat",
    pio._STYLE_MOONSHOT_CHAT: "to_moonshot_chat",
}


def _probe_supported(style: str) -> frozenset[MediaContainer]:
    method = _STYLE_METHOD[style]
    supported = {MediaContainer.TEXT}  # text is always accepted
    for container, obj in _samples().items():
        fn = getattr(obj, method, None)
        if fn is None:
            continue  # no serializer for this style → not natively supported
        try:
            out = fn()
        except Exception:  # noqa: BLE001 — treat a raise as "unsupported"
            out = None
        if out is not None:
            supported.add(container)
    return frozenset(supported)


@pytest.mark.parametrize("style", list(_STYLE_METHOD))
def test_registry_matches_actual_serializers(style):
    assert _probe_supported(style) == pio._STYLE_NATIVE_INPUTS[style], (
        f"registry for style {style!r} disagrees with the real .{_STYLE_METHOD[style]}() "
        f"serializers — update _STYLE_NATIVE_INPUTS to match media_config.py"
    )


def test_endpoint_native_inputs_known_and_unknown():
    # Google chat = everything; chat-completions = text+image; unknown = None.
    assert MediaContainer.YOUTUBE in endpoint_native_inputs("google_chat")
    assert MediaContainer.DOCUMENT in endpoint_native_inputs("anthropic_chat")
    assert MediaContainer.DOCUMENT not in endpoint_native_inputs("groq_chat")
    assert endpoint_native_inputs("openai_image") is None  # media-gen, not chat
    assert endpoint_native_inputs(None) is None


def test_unsupported_inputs_flags_documents_on_chat_completions():
    present = {MediaContainer.DOCUMENT, MediaContainer.IMAGE}
    # groq (chat-completions) drops documents, keeps images.
    assert unsupported_inputs(present, "groq_chat") == {MediaContainer.DOCUMENT}
    # anthropic accepts documents → nothing unsupported.
    assert unsupported_inputs(present, "anthropic_chat") == set()


def test_unsupported_inputs_video_and_youtube_only_google():
    present = {MediaContainer.VIDEO, MediaContainer.YOUTUBE}
    assert unsupported_inputs(present, "openai_chat") == present  # OpenAI drops both
    assert unsupported_inputs(present, "google_chat") == set()  # Gemini takes both


def test_image_is_unsupported_when_model_is_not_vision_capable():
    present = {MediaContainer.IMAGE}
    assert unsupported_inputs(
        present,
        "openai_chat",
        model_supports_vision=False,
    ) == {MediaContainer.IMAGE}
    assert unsupported_inputs(
        present,
        "openai_chat",
        model_supports_vision=True,
    ) == set()


def test_moonshot_chat_accepts_video_but_not_youtube():
    present = {MediaContainer.VIDEO, MediaContainer.YOUTUBE}
    assert unsupported_inputs(present, "moonshot_chat") == {MediaContainer.YOUTUBE}


def test_audio_excluded_when_transcribe_fallback_on():
    present = {MediaContainer.AUDIO}
    # Audio has a transcribe fallback → not "dropped" even on a non-audio provider.
    assert unsupported_inputs(present, "openai_chat") == set()
    # ...but if a caller asks to ignore the fallback, it's flagged.
    assert unsupported_inputs(present, "openai_chat", audio_has_transcribe_fallback=False) == {
        MediaContainer.AUDIO
    }


def test_unknown_endpoint_flags_nothing():
    # We don't guess for unknown/non-chat endpoints.
    assert unsupported_inputs({MediaContainer.DOCUMENT}, "some_future_endpoint") == set()


def test_known_non_vision_model_still_flags_image_on_unknown_endpoint():
    assert unsupported_inputs(
        {MediaContainer.IMAGE},
        "some_future_endpoint",
        model_supports_vision=False,
    ) == {MediaContainer.IMAGE}


def test_scan_message_media_classifies_content():
    msgs = SimpleNamespace(
        to_list=lambda: [
            SimpleNamespace(
                content=[
                    DocumentContent(base64_data=_B64, mime_type="application/pdf"),
                    ImageContent(base64_data=_B64, mime_type="image/png"),
                ]
            )
        ]
    )
    assert scan_message_media(msgs) == {MediaContainer.DOCUMENT, MediaContainer.IMAGE}
    assert scan_message_media(None) == set()  # tolerant


def test_find_unsupported_media_end_to_end():
    from matrx_ai.providers.provider_io_capabilities import find_unsupported_media

    msgs = SimpleNamespace(
        to_list=lambda: [
            SimpleNamespace(
                content=[DocumentContent(base64_data=_B64, mime_type="application/pdf")]
            )
        ]
    )
    # A PDF heading to Groq (chat-completions) is silently dropped.
    assert find_unsupported_media(msgs, "groq_chat") == {MediaContainer.DOCUMENT}
    # The same PDF to Anthropic is fine.
    assert find_unsupported_media(msgs, "anthropic_chat") == set()
