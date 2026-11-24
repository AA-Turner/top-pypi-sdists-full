"""Every TTS send records the request kwargs it sends on the active ExecutionState.

Real: the openai / groq / xai ``_execute_tts`` bodies. Double: the provider client (it raises after the send so
nothing past the paid call runs). The probe snapshots stored ``request_payload {}`` because the speech branch
returned from ``execute()`` before ``capture_request_payload`` (the chat seam) ever ran.
"""

from __future__ import annotations

from types import SimpleNamespace
from collections.abc import Iterator
from typing import Any

import pytest

from matrx_ai.orchestrator.execution_state import (
    ExecutionState,
    clear_execution_state,
    set_execution_state,
    try_get_execution_state,
)


class _Sent(Exception):
    pass


def _config() -> Any:
    part = SimpleNamespace(text="Hello there")
    return SimpleNamespace(
        tts_voice_config=None,
        messages=[SimpleNamespace(role="user", content=[part])],
        audio_format="wav",
        dictionary=None,
        performance_direction=None,
        speech_speed=None,
        model="tts-model",
        stream=False,
    )


def _profile() -> Any:
    return SimpleNamespace(
        provider_model_id="provider-tts-1",
        model_name="tts-model",
        vendor="x",
        tts_voice_ids=["alloy"],
        capabilities=SimpleNamespace(produces_audio=True, produces_text=False),
    )


@pytest.fixture
def state(monkeypatch: pytest.MonkeyPatch) -> Iterator[ExecutionState]:
    st = ExecutionState()
    # Reset on teardown: the ContextVar is set in the shared test context, so an unreset
    # state leaks into every later test (test_outbound_capture then read iteration=0).
    token = set_execution_state(st)
    monkeypatch.setattr("matrx_ai.catalog.resolve.resolve_tts_voice", lambda profile, requested: "alloy")
    monkeypatch.setattr("matrx_ai.speech.compile.direction_supported", lambda profile: False)
    yield st
    clear_execution_state(token)


class _FakeSpeech:
    def __init__(self, calls: list[dict[str, Any]]) -> None:
        self._calls = calls

    async def create(self, **kwargs: Any) -> Any:
        self._calls.append(kwargs)
        raise _Sent


def _fake_client(calls: list[dict[str, Any]]) -> Any:
    return SimpleNamespace(audio=SimpleNamespace(speech=_FakeSpeech(calls)))


@pytest.mark.parametrize("vendor", ["openai", "groq"])
async def test_sdk_speech_send_records_the_kwargs_it_sends(vendor: str, state: ExecutionState, monkeypatch: pytest.MonkeyPatch) -> None:
    if vendor == "openai":
        from matrx_ai.providers.openai.openai_api import OpenAIChat as Chat
    else:
        from matrx_ai.providers.groq.groq_api import GroqChat as Chat

    calls: list[dict[str, Any]] = []
    monkeypatch.setattr(Chat, "client", _fake_client(calls), raising=False)
    chat = Chat()
    with pytest.raises(_Sent):
        await chat._execute_tts(_config(), _profile(), SimpleNamespace(), "tts-model")

    assert calls, "the fake client was never called"
    snap = state.snapshot_payload
    assert snap, "TTS send left the request snapshot empty"
    assert snap["model"] == "provider-tts-1"
    assert snap["voice"] == "alloy"
    assert snap["input"] == "Hello there"
    assert snap["response_format"] == "wav"
    assert state.snapshot_provider == vendor
    assert {k: calls[0][k] for k in snap} == snap  # what was recorded IS what was sent


async def test_xai_speech_send_records_the_payload_it_posts(state: ExecutionState, monkeypatch: pytest.MonkeyPatch) -> None:
    from matrx_ai.providers.xai import xai_api

    posted: list[dict[str, Any]] = []

    class _Http:
        async def __aenter__(self) -> _Http:
            return self

        async def __aexit__(self, *exc: object) -> None:
            return None

        async def post(self, url: str, **kw: Any) -> Any:
            posted.append(kw["json"])
            raise _Sent

    monkeypatch.setattr(xai_api, "make_capture_http_client", lambda **kw: _Http())
    monkeypatch.setattr(xai_api, "resolve_api_key", lambda name: "k")
    with pytest.raises(_Sent):
        await xai_api.XAIChat()._execute_tts(_config(), _profile(), SimpleNamespace(), "tts-model")

    snap = state.snapshot_payload
    assert snap and snap["voice_id"] == "alloy" and snap["text"] == "Hello there"
    assert snap == posted[0]
    assert state.snapshot_provider == "xai"
    assert try_get_execution_state() is state
