"""ONE classifier-aware transient retry, at the shared dispatch seam.

Context (2026-10-01): ea1bb5d8ab turned the Stainless SDKs' silent
``max_retries=2`` off beneath our retry loops. A request/response path that
has NO loop of its own — Gemini embeddings (google-genai never retried by
default), speech-to-text for every ``execute_stt`` caller — must still survive
a network blip, but must never re-buy work the provider may already have done.
``UnifiedAIClient._dispatch_with_billing_net(..., transient_retries=N)`` is the
one opt-in primitive.

Breaks named:
* a dropped connection on an embedding batch fails the whole ingestion (no retry);
* an out-of-credit refusal is retried (it never recovers, and it re-alarms);
* a provider TIMEOUT on a paid transcription is retried — the provider may have
  finished (and billed) the work we stopped waiting for.

Real code: ``GoogleEmbeddingRuntime.embed`` / ``execute_stt`` → the real
dispatch seam, the real admission gate and the shared classifier. Doubles: the
vendor wire (raising the SDK's own exception types), ``capture_error`` and
``sleep``.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import groq
import httpx
import pytest
from google.genai.errors import ClientError

from matrx_ai.testing.profile_factory import make_profile

_PROPERTY_MANAGER_CHUNKS = [
    "Unit 4B reports a slow drain in the kitchen sink; tenant available weekdays after 3pm.",
    "Annual HVAC inspection for 1180 Harbor View completed; filter replaced, no faults found.",
]
_GROQ_REQ = httpx.Request("POST", "https://api.groq.com/openai/v1/audio/transcriptions")


@pytest.fixture(autouse=True)
def quiet(monkeypatch: pytest.MonkeyPatch) -> list[float]:
    sleeps: list[float] = []

    async def capture_error(_exc: BaseException, **_kwargs: Any) -> None:
        return None

    async def _sleep(seconds: float) -> None:
        sleeps.append(seconds)

    monkeypatch.setattr("matrx_connect.streaming.error_capture.capture_error", capture_error)
    monkeypatch.setattr("matrx_ai.providers.unified_client._transient_retry_sleep", _sleep, raising=False)
    return sleeps


def _wire_google(monkeypatch: pytest.MonkeyPatch, *outcomes: Any) -> list[dict[str, Any]]:
    import matrx_ai.providers.google.specialized as specialized

    calls: list[dict[str, Any]] = []
    script = list(outcomes)

    class _Models:
        async def embed_content(self, **kwargs: Any) -> Any:
            calls.append(kwargs)
            outcome = script.pop(0)
            if isinstance(outcome, BaseException):
                raise outcome
            return outcome

    class _Client:
        class aio:  # noqa: N801 — mirrors the SDK attribute
            models = _Models()

    monkeypatch.setattr(specialized, "get_google_client", lambda: _Client())
    return calls


def _embedding_runtime() -> Any:
    from matrx_ai.providers.google import GoogleEmbeddingRuntime

    return GoogleEmbeddingRuntime(
        make_profile(
            model_name="gemini-embedding-2",
            provider_model_id="gemini-embedding-2",
            wire_format="google_embeddings",
            vendor="google",
        )
    )


def _vectors(n: int, value: float) -> Any:
    return SimpleNamespace(embeddings=[SimpleNamespace(values=[value] * 1536) for _ in range(n)])


async def test_a_dropped_connection_on_an_embedding_batch_is_retried_once_and_succeeds(monkeypatch, quiet) -> None:
    calls = _wire_google(
        monkeypatch,
        httpx.ConnectError("[Errno 54] Connection reset by peer"),
        _vectors(2, 0.25),
    )
    result = await _embedding_runtime().embed(_PROPERTY_MANAGER_CHUNKS, output_dimensionality=1536)

    assert len(calls) == 2
    assert result.vectors[0][:2] == [0.25, 0.25]
    assert len(quiet) == 1


async def test_an_out_of_credit_embedding_refusal_is_never_retried(monkeypatch, quiet) -> None:
    exc = ClientError(
        429,
        {"error": {"code": 429, "status": "RESOURCE_EXHAUSTED",
                   "message": "Your prepayment credits are depleted. Please go to AI Studio to manage your project and billing."}},
    )
    calls = _wire_google(monkeypatch, exc, _vectors(2, 0.5))
    with pytest.raises(ClientError) as raised:
        await _embedding_runtime().embed(_PROPERTY_MANAGER_CHUNKS, output_dimensionality=1536)
    assert raised.value is exc
    assert len(calls) == 1
    assert quiet == []


def _wire_groq(monkeypatch: pytest.MonkeyPatch, *outcomes: Any) -> list[dict[str, Any]]:
    import matrx_ai.catalog.resolve as resolve_module
    import matrx_ai.providers.groq.stt as groq_stt

    calls: list[dict[str, Any]] = []
    script = list(outcomes)

    class _Transcriptions:
        async def create(self, **kwargs: Any) -> Any:
            calls.append(kwargs)
            outcome = script.pop(0)
            if isinstance(outcome, BaseException):
                raise outcome
            return outcome

    class _Client:
        class audio:  # noqa: N801 — mirrors the SDK attribute
            transcriptions = _Transcriptions()
            translations = _Transcriptions()

    profile = make_profile(
        model_name="whisper-large-v3-turbo",
        provider_model_id="whisper-large-v3-turbo",
        wire_format="groq_stt",
        vendor="groq",
        rules={"language": {}, "response_format": {}, "timestamp_granularities": {}},
    ).model_copy(update={"client_attr": "stt", "offering_metadata": {"stt": {"max_file_size_mb": 25}}})

    async def _resolve(*_args: Any, **_kwargs: Any) -> Any:
        return profile

    monkeypatch.setattr(resolve_module, "resolve_call_profile", _resolve)
    from matrx_ai.providers.unified_client import UnifiedAIClient

    adapter = getattr(UnifiedAIClient(), "groq_stt")
    monkeypatch.setitem(type(adapter).execute.__globals__, "_client", lambda: _Client())
    monkeypatch.setattr(groq_stt, "_client", lambda: _Client())
    return calls


def _stt_request() -> Any:
    from matrx_ai.processing.audio.stt import STTRequest

    return STTRequest(
        audio_source=b"RIFF....WAVEfmt voice-memo",
        model="whisper-large-v3-turbo",
        language="en",
        response_format="verbose_json",
        timestamp_granularities=["segment"],
    )


async def test_a_timed_out_paid_transcription_is_never_bought_again(monkeypatch, quiet) -> None:
    from matrx_ai.processing.audio.stt import execute_stt

    exc = groq.APITimeoutError(request=_GROQ_REQ)
    calls = _wire_groq(monkeypatch, exc, {"text": "never reached", "duration": 3.0})
    with pytest.raises(groq.APITimeoutError):
        await execute_stt(_stt_request())
    assert len(calls) == 1
    assert quiet == []


async def test_a_refused_overloaded_transcription_is_retried_and_counts_its_attempts(monkeypatch, quiet) -> None:
    from matrx_ai.processing.audio.stt import execute_stt

    body = {"error": {"message": "Service Unavailable", "type": "service_unavailable"}}
    overloaded = groq.APIStatusError(
        "Error code: 503", response=httpx.Response(503, request=_GROQ_REQ, json=body), body=body
    )
    calls = _wire_groq(
        monkeypatch,
        overloaded,
        {"text": "Caller asked to move the Thursday pickup to Friday.", "duration": 4.2},
    )
    result = await execute_stt(_stt_request())

    assert len(calls) == 2
    assert result.text == "Caller asked to move the Thursday pickup to Friday."
    assert result.attempts == 2
