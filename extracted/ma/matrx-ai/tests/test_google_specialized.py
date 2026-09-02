from __future__ import annotations

from types import SimpleNamespace

import pytest

from matrx_ai.catalog.routes import client_attr_for_wire_format
from matrx_ai.providers.google.specialized import (
    GoogleBackgroundInteractionRuntime,
    GoogleEmbeddingRuntime,
    GoogleLiveOptions,
    GoogleLiveSession,
    WeightedMusicPrompt,
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


def test_live_defaults_and_lyria_nonzero_weight() -> None:
    assert GoogleLiveOptions().thinking_level == "minimal"
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
