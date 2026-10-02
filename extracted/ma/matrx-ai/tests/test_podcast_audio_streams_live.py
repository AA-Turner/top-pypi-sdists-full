"""A podcast episode's audio reaches the person WHILE it renders.

Live regression (2026-09-09 → 2026-10-01): the nested-stream-leak fix muted
every podcast stage, the two TTS stages included, so ``audio_stream_chunk`` /
``audio_stream_end`` were swallowed and the studio stayed silent until the
whole run — images and videos too — ended (~45 min on long runs).

SUTs: ``run_agent`` + ``SilentEmitter`` (a muted child forwards ONLY the named
data events to its parent's emitter) and ``_create_audio`` (both TTS paths ask
for exactly the live audio events). Doubles: ``execute_ai_request`` (emits what
a TTS provider emits, then returns a completed request) and, for the stage
contract, ``_run_mandated`` (the paid agent call).

Breaks named:
* a muted child drops the audio events → nothing plays live;
* the forward list leaks text, phases or other data → the stream-leak class
  is back;
* either audio path (1–2 hosts Gemini, 3+ hosts ElevenLabs) stops asking for
  the live audio events.
"""

from __future__ import annotations

import asyncio
from typing import Any

import pytest
from matrx_connect.context.app_context import (
    AppContext,
    clear_app_context,
    get_app_context,
    set_app_context,
)
from matrx_connect.context.data_types import (
    LIVE_MEDIA_DATA_TYPES,
    AudioStreamChunkData,
    AudioStreamEndData,
    ConversationIdData,
)

import matrx_ai.agent_runners.podcast_generator as podcast
from matrx_ai.agents.executor import AgentRunResult


class _ParentWire:
    def __init__(self) -> None:
        self.data: list[str] = []
        self.chunks: list[str] = []

    async def send_data(self, payload: Any) -> None:
        self.data.append(getattr(payload, "type", None) or payload.get("type"))

    async def send_chunk(self, text: str) -> None:
        self.chunks.append(text)

    def __getattr__(self, name: str) -> Any:
        async def _noop(*a: Any, **k: Any) -> None:
            return None

        return _noop


def _completed_request() -> Any:
    from matrx_ai.config import MessageList, UnifiedConfig
    from matrx_ai.config.unified_config import UnifiedResponse
    from matrx_ai.orchestrator.requests import AIMatrixRequest, CompletedRequest

    return CompletedRequest(
        request=AIMatrixRequest(
            conversation_id="5a0b3c9e-6a51-4c55-9c39-6f1e0f2d7a11",
            config=UnifiedConfig(model="gemini-2.5-pro-preview-tts", messages=MessageList()),
        ),
        iterations=1,
        final_response=UnifiedResponse(messages=[]),
        metadata={"status": "complete"},
    )


async def _tts_like_execute(config: Any, **kwargs: Any) -> Any:
    emitter = get_app_context().emitter
    await emitter.send_chunk('{"leaked": "stage json"}')
    await emitter.send_data(
        AudioStreamChunkData(stream_id="ep-114", seq=0, audio_base64="AAAA")
    )
    await emitter.send_data(
        # A non-media data event: a muted child's bookkeeping must stay muted.
        ConversationIdData(conversation_id="5a0b3c9e-6a51-4c55-9c39-6f1e0f2d7a11")
    )
    await emitter.send_data(
        AudioStreamEndData(stream_id="ep-114", total_chunks=1, url="https://cdn.aimatrx.com/a/ep-114.wav")
    )
    return _completed_request()


def _run(monkeypatch: pytest.MonkeyPatch, stream_data_types: frozenset[str] | None) -> _ParentWire:
    import matrx_ai.agents.definition as definition
    from matrx_ai.agents.definition import Agent
    from matrx_ai.agents.executor import run_agent
    from matrx_ai.config import MessageList, UnifiedConfig

    monkeypatch.setattr(definition, "execute_ai_request", _tts_like_execute)
    parent = _ParentWire()
    agent = Agent(UnifiedConfig(model="gemini-2.5-pro-preview-tts", messages=MessageList()), name="Podcast Audio")
    token = set_app_context(AppContext(emitter=parent, user_id="e4687a9c-acf7-469f-aa12-860eb4d948d0", store=False))  # type: ignore[arg-type]
    try:
        asyncio.run(
            run_agent(
                agent,
                label="Podcast Audio",
                source_feature="podcast",
                suppress_stream=True,
                stream_data_types=stream_data_types,
            )
        )
    finally:
        clear_app_context(token)
    return parent


def test_a_muted_audio_stage_delivers_its_audio_live(monkeypatch) -> None:
    parent = _run(monkeypatch, podcast.LIVE_MEDIA_DATA_TYPES)
    assert parent.data == ["audio_stream_chunk", "audio_stream_end"]
    assert parent.chunks == []


def test_a_muted_stage_without_a_forward_list_stays_silent(monkeypatch) -> None:
    parent = _run(monkeypatch, None)
    assert parent.data == []
    assert parent.chunks == []


def _script(names: list[str]) -> str:
    lines = [
        f"{name}: Today's pickup route covers {stop} — the cardboard bales go out first."
        for name, stop in zip(names * 2, ["Ventura Ave", "Blackstone", "Shaw", "Herndon", "Cedar", "Kings Canyon"])
    ]
    return "<podcast_dialogue>\n" + "\n".join(lines) + "\n</podcast_dialogue>"


@pytest.mark.parametrize(
    ("host_count", "names"),
    [(2, ["Maya", "Daniel"]), (3, ["Maya", "Daniel", "Priya"])],
    ids=["gemini-2-hosts", "elevenlabs-3-hosts"],
)
def test_both_audio_paths_ask_for_live_audio(monkeypatch, host_count: int, names: list[str]) -> None:
    calls: list[dict[str, Any]] = []

    async def paid_call(agent_cls: type, **kwargs: Any) -> AgentRunResult:
        calls.append(kwargs)
        return AgentRunResult(success=False, error="stopped before the paid call")

    monkeypatch.setattr(podcast, "_run_mandated", paid_call)
    request = podcast.PodcastRequest(
        show_id="route-report",
        input_data_type=list(podcast.InputDataType)[0],
        podcast_type=list(podcast.PodcastType)[0],
        host_count=host_count,
    )
    asyncio.run(podcast._create_audio(request, _script(names)))

    assert len(calls) == 1
    assert calls[0]["suppress_stream"] is True
    # The platform's one live-media list, and it must carry the audio events.
    assert calls[0]["stream_data_types"] is LIVE_MEDIA_DATA_TYPES
    assert {"audio_stream_chunk", "audio_stream_end"} <= calls[0]["stream_data_types"]
