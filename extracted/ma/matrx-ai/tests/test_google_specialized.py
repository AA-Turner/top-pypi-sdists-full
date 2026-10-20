from __future__ import annotations

from types import SimpleNamespace

import pytest

from matrx_ai.catalog.routes import client_attr_for_wire_format
from matrx_ai.providers.google.specialized import (
    GoogleBackgroundInteractionRuntime,
    GoogleEmbeddingPart,
    GoogleEmbeddingRuntime,
    GoogleLiveOptions,
    GoogleLiveSession,
    WeightedMusicPrompt,
    embedding_contents,
)
from matrx_ai.testing.profile_factory import make_profile


def _profile(wire_format: str):
    return make_profile(
        model_name="test-google-model",
        wire_format=wire_format,
        vendor="google",
        capabilities={
            "input": ["text"],
            "output": ["embedding" if wire_format == "google_embeddings" else "text"],
            "features": [],
            "interaction": "embedding" if wire_format == "google_embeddings" else "turn",
            "multilingual": True,
        },
    )


def test_specialized_catalog_routes_are_not_turn_clients() -> None:
    assert client_attr_for_wire_format("google_live") == "realtime"
    assert client_attr_for_wire_format("google_music_realtime") == "music_realtime"
    assert client_attr_for_wire_format("google_embeddings") == "embedding"
    assert client_attr_for_wire_format("typesafe_systemone") == "decision"


def test_live_defaults_and_lyria_nonzero_weight() -> None:
    # Unset: the offering's cells decide (gemini-3.8-live rejects thinking_level).
    assert GoogleLiveOptions().thinking_level is None
    assert GoogleLiveOptions().context_window_compression is True
    with pytest.raises(ValueError, match="non-zero"):
        WeightedMusicPrompt(text="strings", weight=0)


@pytest.mark.asyncio
async def test_live_runtime_builds_current_sdk_config(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    seen = {}

    class Context:
        async def __aenter__(self):
            return SimpleNamespace()

        async def __aexit__(self, *_args):
            return None

    class Live:
        def connect(self, **kwargs):
            seen.update(kwargs)
            return Context()

    client = SimpleNamespace(aio=SimpleNamespace(live=Live()))
    monkeypatch.setattr("matrx_ai.providers.google.specialized.get_google_client", lambda: client)
    options = GoogleLiveOptions(
        thinking_level="high",
        turn_coverage="TURN_INCLUDES_ALL_INPUT",
        response_modalities=["AUDIO"],
        vad_config={"disabled": False},
    )
    async with GoogleLiveSession(_profile("google_live"), options):
        pass

    config = seen["config"]
    assert config.thinking_config.thinking_level == "HIGH"
    assert config.realtime_input_config.turn_coverage == "TURN_INCLUDES_ALL_INPUT"
    assert config.response_modalities == ["AUDIO"]
    # Session speed defaults: 700 ms silence (a caller's key wins), sliding-window
    # compression, resumption config present.
    assert config.realtime_input_config.automatic_activity_detection.silence_duration_ms == 700
    assert config.realtime_input_config.automatic_activity_detection.disabled is False
    assert config.context_window_compression.sliding_window is not None
    assert config.session_resumption is not None
    assert config.tools is None


@pytest.mark.asyncio
async def test_live_session_declares_non_blocking_tools_and_answers_when_idle(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from google.genai import types

    seen: dict = {}
    sent: dict = {}

    class Session:
        async def send_tool_response(self, **kwargs):
            sent.update(kwargs)

    class Context:
        async def __aenter__(self):
            return Session()

        async def __aexit__(self, *_args):
            return None

    class Live:
        def connect(self, **kwargs):
            seen.update(kwargs)
            return Context()

    client = SimpleNamespace(aio=SimpleNamespace(live=Live()))
    monkeypatch.setattr("matrx_ai.providers.google.specialized.get_google_client", lambda: client)
    options = GoogleLiveOptions(
        tools=[
            {"name": "ask_agent", "description": "Ask the deep agent", "parameters": {"type": "object"}}
        ],
        vad_config={"silence_duration_ms": 500},
    )
    async with GoogleLiveSession(_profile("google_live"), options) as session:
        await session.send(
            {
                "type": "tool_response",
                "responses": [{"id": "c2", "name": "ask_agent", "response": {}, "scheduling": None}],
            }
        )
        with pytest.raises(ValueError, match="at least one"):
            await session.send({"type": "tool_response", "responses": []})

    declaration = seen["config"].tools[0].function_declarations[0]
    assert declaration.name == "ask_agent"
    assert declaration.behavior == types.Behavior.NON_BLOCKING
    assert (
        seen["config"].realtime_input_config.automatic_activity_detection.silence_duration_ms == 500
    )
    assert sent["function_responses"][0].scheduling is None


def test_tool_response_defaults_to_when_idle() -> None:
    from google.genai import types

    from matrx_ai.providers.google.specialized import _tool_responses

    [one] = _tool_responses({"responses": [{"id": "c1", "name": "t", "response": {"a": 1}}]})
    assert one.scheduling == types.FunctionResponseScheduling.WHEN_IDLE
    [two] = _tool_responses({"responses": [{"name": "t", "scheduling": "INTERRUPT"}]})
    assert two.scheduling == types.FunctionResponseScheduling.INTERRUPT


@pytest.mark.asyncio
async def test_embedding_runtime_calls_embed_content(monkeypatch: pytest.MonkeyPatch) -> None:
    seen = {}

    class Models:
        async def embed_content(self, **kwargs):
            seen.update(kwargs)
            return SimpleNamespace(embeddings=[SimpleNamespace(values=[0.1, 0.2])])

    client = SimpleNamespace(aio=SimpleNamespace(models=Models()))
    monkeypatch.setattr("matrx_ai.providers.google.specialized.get_google_client", lambda: client)
    result = await GoogleEmbeddingRuntime(_profile("google_embeddings")).embed(
        "hello", output_dimensionality=128
    )
    assert seen["model"] == "test-google-model"
    assert seen["config"].output_dimensionality == 128
    assert result.vectors == [[0.1, 0.2]]


def test_embedding_content_translation_stays_at_google_provider_boundary() -> None:
    contents = embedding_contents(
        [
            "plain text",
            [GoogleEmbeddingPart(type="inline", data="aGVsbG8=", mime_type="text/plain")],
        ]
    )

    assert contents[0] == "plain text"
    assert contents[1].role == "user"
    assert contents[1].parts[0].inline_data.mime_type == "text/plain"


@pytest.mark.asyncio
async def test_background_interaction_is_stored_and_nonblocking(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    seen = {}

    class Interactions:
        async def create(self, **kwargs):
            seen.update(kwargs)
            return SimpleNamespace(id="i-1", status="in_progress")

    client = SimpleNamespace(aio=SimpleNamespace(interactions=Interactions()))
    monkeypatch.setattr("matrx_ai.providers.google.specialized.get_google_client", lambda: client)
    result = await GoogleBackgroundInteractionRuntime(_profile("google_interactions")).create(
        "research this"
    )
    assert seen["background"] is True
    assert seen["store"] is True
    assert result == {"id": "i-1", "status": "in_progress"}
