"""Tests for MockLLMProvider."""

from __future__ import annotations

import asyncio

from agentic_devtools.orchestration.llm.mock_provider import MockLLMProvider
from agentic_devtools.orchestration.llm.types import LLMMessage, ProviderType


def _user_msg(content: str) -> list[LLMMessage]:
    """Create a single-user-message list."""
    return [LLMMessage(role="user", content=content)]


class TestMockLLMProvider:
    """Tests for MockLLMProvider deterministic responses."""

    def test_complete_returns_configured_response(self) -> None:
        """complete() returns an LLMResponse with the configured text."""
        provider = MockLLMProvider(responses=["Hello world"])
        result = asyncio.run(provider.complete(_user_msg("test")))
        assert result.text == "Hello world"
        assert result.provider_type == ProviderType.LOCAL_MODEL

    def test_complete_cycles_responses(self) -> None:
        """complete() cycles through responses when exhausted."""
        provider = MockLLMProvider(responses=["A", "B"])
        r1 = asyncio.run(provider.complete(_user_msg("1")))
        r2 = asyncio.run(provider.complete(_user_msg("2")))
        r3 = asyncio.run(provider.complete(_user_msg("3")))
        assert r1.text == "A"
        assert r2.text == "B"
        assert r3.text == "A"  # cycles

    def test_complete_structured_returns_response(self) -> None:
        """complete_structured() returns an LLMResponse."""
        provider = MockLLMProvider(responses=['{"status": "ok"}'])
        result = asyncio.run(provider.complete_structured(_user_msg("prompt"), schema={"type": "object"}))
        assert result.text == '{"status": "ok"}'

    def test_stream_yields_chunk(self) -> None:
        """stream() yields StreamChunk(s)."""
        provider = MockLLMProvider(responses=["Full response"])

        async def collect():
            return [chunk async for chunk in provider.stream(_user_msg("prompt"))]

        chunks = asyncio.run(collect())
        assert len(chunks) == 1
        assert chunks[0].text_delta == "Full response"
        assert chunks[0].finish_reason == "stop"

    def test_call_count_and_history(self) -> None:
        """All calls are counted and recorded in call_history."""
        provider = MockLLMProvider(responses=["r"])
        asyncio.run(provider.complete(_user_msg("prompt_1")))
        asyncio.run(provider.complete(_user_msg("prompt_2")))

        assert provider.call_count == 2
        assert len(provider.call_history) == 2
        assert provider.call_history[0]["method"] == "complete"
        assert provider.call_history[1]["messages"][0].content == "prompt_2"

    def test_served_from_fixture_flag(self) -> None:
        """Responses have served_from_fixture=True."""
        provider = MockLLMProvider(responses=["x"])
        result = asyncio.run(provider.complete(_user_msg("test")))
        assert result.served_from_fixture is True

    def test_default_responses(self) -> None:
        """Default response is a JSON mock."""
        provider = MockLLMProvider()
        result = asyncio.run(provider.complete(_user_msg("test")))
        assert "mock response" in result.text
