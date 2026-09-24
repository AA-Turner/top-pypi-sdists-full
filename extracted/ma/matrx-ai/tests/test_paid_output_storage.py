"""A storage failure never re-invokes the paid provider — every media output.

Incident (2026-09-22): saving a generated ElevenLabs audio file failed (S3 /
thumbnail step); the failure was classified as a provider error, the executor
retried the whole ``execute()``, and ElevenLabs billed three times for one run.

The contract pinned here, for audio (ElevenLabs, OpenAI) and image/video
(``BaseMediaGeneration``):

* the paid provider call and the storage step are separate phases;
* a storage failure retries STORAGE ONLY, once, with the provider's result held;
* when that retry fails too, the run fails honestly and NON-retryably
  (``media_storage_failed``) — so the executor never calls the provider again;
* the billed usage rides the exception, and the executor records it once.

Each test drives the REAL provider adapter with a stubbed vendor client that
counts invocations and a storage step that fails, then runs the executor's own
retry rule over it (retry while ``error_info.is_retryable``).
"""

from __future__ import annotations

import base64
from typing import Any

import pytest

from matrx_ai.config import TextContent, TokenUsage, UnifiedConfig, UnifiedMessage
from matrx_ai.providers.errors import classify_provider_error, get_billed_usage

EXECUTOR_MAX_RETRIES = 2  # executor default max_retries_per_iteration


class _Emitter:
    def __init__(self) -> None:
        self.data: list[Any] = []
        self.errors: list[dict[str, Any]] = []

    async def send_info(self, payload: Any) -> None:
        return None

    async def send_data(self, payload: Any) -> None:
        self.data.append(payload)

    async def send_error(self, **kwargs: Any) -> None:
        self.errors.append(kwargs)


class _Ctx:
    def __init__(self, emitter: _Emitter) -> None:
        self.emitter = emitter
        self.request_id = "req-paid-output"
        self.user_id = None
        self.is_minor = False


async def _run_like_the_executor(call: Any, provider: str) -> Any:
    """The executor's retry rule: re-invoke the whole provider execute() while
    the attached classification says the failure is retryable."""
    last: BaseException | None = None
    for _attempt in range(EXECUTOR_MAX_RETRIES + 1):
        try:
            return await call()
        except Exception as exc:  # noqa: BLE001 — mirrors executor.py's handler
            last = exc
            info = getattr(exc, "error_info", None) or classify_provider_error(provider, exc)
            if not info.is_retryable:
                raise
    assert last is not None
    raise last


def _usage(model: str, api: str) -> TokenUsage:
    return TokenUsage(input_tokens=42, output_tokens=0, matrx_model_name=model, api=api)


class _StorageStub:
    """save_media_envelope_async stand-in: fails the first ``fail_times`` calls."""

    def __init__(self, fail_times: int) -> None:
        self.calls = 0
        self.fail_times = fail_times

    async def __call__(self, content: Any = None, mime_type: str = "", **kwargs: Any):
        from matrx_ai.media import MediaPersistResult

        self.calls += 1
        if self.calls <= self.fail_times:
            raise OSError("S3 PutObject failed: thumbnail step 503")
        return MediaPersistResult(
            file_id="file-123",
            url="https://cdn.example/file-123",
            cdn_url="https://cdn.example/file-123",
            download_url="https://cdn.example/file-123?download=1",
            storage_uri="s3://bucket/file-123",
            file_path="generations/file-123",
            file_name="file-123",
            mime_type=mime_type or "audio/mpeg",
            size_bytes=3,
            visibility="public",
        )


@pytest.fixture
def ctx(monkeypatch: pytest.MonkeyPatch) -> _Emitter:
    import matrx_ai.context.app_context as app_context

    emitter = _Emitter()
    monkeypatch.setattr(app_context, "get_app_context", lambda: _Ctx(emitter))

    import matrx_ai.config.usage_config as usage_config

    async def _billed(*, characters: int, matrx_model_name: str, api: str, **_: Any):
        return TokenUsage(
            input_tokens=characters, output_tokens=0, matrx_model_name=matrx_model_name, api=api
        )

    monkeypatch.setattr(usage_config, "build_character_billed_usage_async", _billed)
    return emitter


# --------------------------------------------------------------- ElevenLabs


def _eleven_profile():
    from matrx_ai.testing.profile_factory import make_profile

    caps = {"input": ["text"], "output": ["audio"], "features": ["dialogue"], "interaction": "turn"}
    return make_profile(
        model_name="eleven_v3",
        wire_format="elevenlabs_chat",
        capabilities=caps,
        rules={"multi_speaker": {"clamp": {"max": 10}}, "performance_direction": {}},
    ).model_copy(update={"tts_voice_ids": ("kore", "puck"), "tts_default_voice_id": "kore"})


def _eleven_chat(monkeypatch: pytest.MonkeyPatch, counter: dict[str, int]):
    from matrx_ai.providers.eleven_labs import elevenlabs_api
    from matrx_ai.providers.eleven_labs.elevenlabs_api import ElevenLabsChat

    text = "Hi there. Hello."
    starts = [i * 0.1 for i in range(len(text))]

    class _Dialogue:
        def convert_with_timestamps(self, **kwargs: Any):
            from elevenlabs.types.audio_with_timestamps_and_voice_segments_response_model import (
                AudioWithTimestampsAndVoiceSegmentsResponseModel,
            )

            counter["provider"] += 1
            return AudioWithTimestampsAndVoiceSegmentsResponseModel.model_validate(
                {
                    "audio_base64": base64.b64encode(b"ID3").decode(),
                    "alignment": {
                        "characters": list(text),
                        "character_start_times_seconds": starts,
                        "character_end_times_seconds": [s + 0.1 for s in starts],
                    },
                    "normalized_alignment": None,
                    "voice_segments": [],
                }
            )

    class _Client:
        text_to_dialogue = _Dialogue()

    async def _no_capture(**_: Any) -> None:
        return None

    monkeypatch.setattr(elevenlabs_api, "stamp_call_meta", lambda **_: None)
    monkeypatch.setattr(elevenlabs_api, "emit_explicit_context_analysis", _no_capture)
    chat = ElevenLabsChat.__new__(ElevenLabsChat)
    chat.client = _Client()
    return chat


def _script_config() -> UnifiedConfig:
    from matrx_ai.config.speech_script_config import SpeechScriptContent

    content = SpeechScriptContent(
        turns=[
            {"speaker": "Maya", "voice": "kore", "text": "Hi there."},
            {"speaker": "Sam", "voice": "puck", "text": "Hello."},
        ]
    )
    return UnifiedConfig(model="eleven_v3", messages=[UnifiedMessage(role="user", content=[content])])


@pytest.mark.asyncio
async def test_elevenlabs_storage_failure_calls_the_provider_once(monkeypatch, ctx):
    import matrx_ai.media as media

    counter = {"provider": 0}
    storage = _StorageStub(fail_times=99)
    monkeypatch.setattr(media, "save_media_envelope_async", storage)
    chat = _eleven_chat(monkeypatch, counter)

    with pytest.raises(Exception) as caught:
        await _run_like_the_executor(
            lambda: chat.execute(_script_config(), _eleven_profile()), "elevenlabs"
        )

    assert counter["provider"] == 1, "a storage failure re-invoked the paid provider"
    assert storage.calls == 2, "storage must be retried exactly once, alone"
    info = caught.value.error_info
    assert info.is_retryable is False
    assert info.error_type == "media_storage_failed"
    assert "saving" in info.user_message.lower()
    billed = get_billed_usage(caught.value)
    assert billed is not None and billed.input_tokens > 0, "billed usage lost on storage failure"


@pytest.mark.asyncio
async def test_elevenlabs_storage_retry_succeeds_without_a_second_provider_call(monkeypatch, ctx):
    import matrx_ai.media as media

    counter = {"provider": 0}
    storage = _StorageStub(fail_times=1)
    monkeypatch.setattr(media, "save_media_envelope_async", storage)
    chat = _eleven_chat(monkeypatch, counter)

    response = await _run_like_the_executor(
        lambda: chat.execute(_script_config(), _eleven_profile()), "elevenlabs"
    )

    assert counter["provider"] == 1
    assert storage.calls == 2
    assert response.messages[0].content[0].file_id == "file-123"
    assert response.usage is not None


# ------------------------------------------------------------------- OpenAI


@pytest.mark.asyncio
async def test_openai_tts_storage_failure_calls_the_provider_once(monkeypatch, ctx):
    import matrx_ai.media as media
    from matrx_ai.providers.openai import openai_api
    from matrx_ai.testing.profile_factory import make_profile

    counter = {"provider": 0}

    class _Speech:
        async def create(self, **kwargs: Any):
            counter["provider"] += 1

            class _Resp:
                content = b"ID3"

            return _Resp()

    class _Audio:
        speech = _Speech()

    class _Client:
        audio = _Audio()

    storage = _StorageStub(fail_times=99)
    monkeypatch.setattr(media, "save_media_envelope_async", storage)
    monkeypatch.setattr(openai_api, "stamp_call_meta", lambda **_: None)
    chat = openai_api.OpenAIChat.__new__(openai_api.OpenAIChat)
    chat.client = _Client()
    chat.debug = False
    profile = make_profile(
        model_name="tts-1",
        wire_format="openai_chat",
        capabilities={"input": ["text"], "output": ["audio"], "features": [], "interaction": "turn"},
        rules={},
    ).model_copy(update={"tts_voice_ids": ("coral",), "tts_default_voice_id": "coral"})
    config = UnifiedConfig(
        model="tts-1", messages=[UnifiedMessage(role="user", content=[TextContent(text="Hi")])]
    )

    with pytest.raises(Exception) as caught:
        await _run_like_the_executor(
            lambda: chat._execute_tts(config, profile, ctx, "tts-1"), "openai"
        )

    assert counter["provider"] == 1
    assert storage.calls == 2
    assert caught.value.error_info.is_retryable is False
    assert get_billed_usage(caught.value) is not None


# -------------------------------------------------------------- image/video


class _ImageStub:
    """A BaseMediaGeneration subclass whose SDK call is a counter."""

    @staticmethod
    def build(counter: dict[str, int]):
        from matrx_ai.providers.base_media import BaseMediaGeneration, GeneratedAsset

        class _Image(BaseMediaGeneration):
            provider = "openai"
            modality = "image"

            def _build_kwargs(self, unified_config: Any, profile: Any) -> dict[str, Any]:
                return {"prompt": "a lighthouse"}

            def _call_provider(self, kwargs: dict[str, Any]) -> Any:
                counter["provider"] += 1
                return object()

            def _extract_assets(self, raw: Any) -> list[GeneratedAsset]:
                return [GeneratedAsset(data=b"\x89PNG", mime_type="image/png")]

            def _classify_error(self, exc: Exception) -> Any:
                from matrx_ai.providers.errors import classify_openai_error

                return classify_openai_error(exc)

            def _build_usage(self, *args: Any, **kwargs: Any) -> TokenUsage:
                return _usage("gpt-image-1", "openai")

        return _Image()


@pytest.mark.asyncio
async def test_image_storage_failure_calls_the_provider_once(monkeypatch, ctx):
    import matrx_ai.media as media
    from matrx_ai.testing.profile_factory import make_profile

    counter = {"provider": 0}
    storage = _StorageStub(fail_times=99)
    monkeypatch.setattr(media, "save_media_envelope_async", storage)
    generator = _ImageStub.build(counter)
    profile = make_profile(
        model_name="gpt-image-1",
        wire_format="openai_image",
        capabilities={"input": ["text"], "output": ["image"], "features": [], "interaction": "turn"},
        rules={},
    )
    config = UnifiedConfig(
        model="gpt-image-1",
        messages=[UnifiedMessage(role="user", content=[TextContent(text="a lighthouse")])],
    )

    with pytest.raises(Exception) as caught:
        await _run_like_the_executor(lambda: generator.execute(config, profile), "openai")

    assert counter["provider"] == 1
    assert storage.calls == 2
    assert caught.value.error_info.is_retryable is False
    assert caught.value.error_info.error_type == "media_storage_failed"
    assert get_billed_usage(caught.value) is not None, "the paid image's usage was dropped"


# --------------------------------------------------------- recorded once


def test_billed_usage_from_a_storage_failure_is_recorded_once():
    from matrx_ai.orchestrator.executor import _record_billed_usage_on_failure
    from matrx_ai.providers.paid_output import PaidOutputStorageError

    class _Request:
        request_id = "req-1"
        conversation_id = "conv-1"

        def __init__(self) -> None:
            self.added: list[TokenUsage] = []

        def add_usage(self, usage: TokenUsage) -> None:
            self.added.append(usage)

    err = PaidOutputStorageError(
        provider="elevenlabs",
        modality="audio",
        cause=OSError("S3 down"),
        usage=_usage("eleven_v3", "elevenlabs"),
    )
    request = _Request()
    _record_billed_usage_on_failure(request, err, iteration=1, provider_attempt=1)
    _record_billed_usage_on_failure(request, err, iteration=1, provider_attempt=1)
    assert len(request.added) == 1


# ------------------------------------------------------------------- Gemini


@pytest.mark.asyncio
async def test_gemini_audio_storage_retries_once_then_fails_honestly(monkeypatch):
    """Gemini TTS/image/video/document bytes used to be DROPPED on a save
    failure (a paid output silently missing); now storage retries once and the
    run fails non-retryably — the Google adapter never re-calls Gemini for it."""
    import matrx_ai.media as media
    from matrx_ai.config.media_config import AudioContent
    from matrx_ai.providers.paid_output import PaidOutputStorageError

    storage = _StorageStub(fail_times=99)
    monkeypatch.setattr(media, "save_media_envelope_async", storage)
    with pytest.raises(PaidOutputStorageError) as caught:
        await AudioContent.from_raw_audio_async(b"\x00\x01" * 8, "audio/L16;rate=24000")
    assert storage.calls == 2
    assert caught.value.error_info.is_retryable is False


@pytest.mark.asyncio
async def test_gemini_image_is_never_silently_dropped(monkeypatch):
    from google.genai.types import Blob, Part

    import matrx_ai.media as media
    from matrx_ai.config.media_config import ImageContent
    from matrx_ai.providers.paid_output import PaidOutputStorageError

    storage = _StorageStub(fail_times=1)
    monkeypatch.setattr(media, "save_media_envelope_async", storage)
    part = Part(inline_data=Blob(data=b"\x89PNG", mime_type="image/png"))
    image = await ImageContent.from_google_async(part)
    assert image is not None and image.file_id == "file-123"
    assert storage.calls == 2

    storage.calls, storage.fail_times = 0, 99
    with pytest.raises(PaidOutputStorageError):
        await ImageContent.from_google_async(part)
