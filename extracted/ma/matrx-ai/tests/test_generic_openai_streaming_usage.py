"""OpenAI-compatible stream usage regressions.

Moonshot returns terminal usage on ``choices[0].usage``. The generic adapter
must normalise that shape just as it does the more common ``chunk.usage`` one,
or successful billed calls are persisted as zero-token requests.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from matrx_ai.config import ThinkingContent
from matrx_ai.providers.generic_openai.generic_openai_api import GenericOpenAIChat


class _Emitter:
    def __init__(self) -> None:
        self.chunks: list[str] = []

    async def send_chunk(self, text: str) -> None:
        self.chunks.append(text)

    async def send_reasoning_state(self, _state: str) -> None:
        pass


class _Stream:
    def __init__(self, chunks: list[object]) -> None:
        self._chunks = chunks

    def __aiter__(self):
        return self._iterate()

    async def _iterate(self):
        for chunk in self._chunks:
            yield chunk


@pytest.mark.asyncio
async def test_choice_level_terminal_usage_is_persisted() -> None:
    chat = object.__new__(GenericOpenAIChat)
    chat.provider_name = "moonshot"
    chat.endpoint_name = "[MOONSHOT CHAT]"
    chat.debug = False

    chunks = [
        SimpleNamespace(
            id="cmpl-kimi",
            usage=None,
            choices=[
                SimpleNamespace(
                    delta=SimpleNamespace(content=None, reasoning_content="First, reason."),
                    finish_reason=None,
                    usage=None,
                )
            ],
        ),
        SimpleNamespace(
            id="cmpl-kimi",
            usage=None,
            choices=[
                SimpleNamespace(
                    delta=SimpleNamespace(content="Hello", reasoning_content=None),
                    finish_reason=None,
                    usage=None,
                )
            ],
        ),
        SimpleNamespace(
            id="cmpl-kimi",
            usage=None,
            choices=[
                SimpleNamespace(
                    delta=SimpleNamespace(content=None, reasoning_content=None),
                    finish_reason="stop",
                    usage=SimpleNamespace(
                        prompt_tokens=100,
                        completion_tokens=20,
                        cached_tokens=40,
                    ),
                )
            ],
        ),
    ]
    stream = _Stream(chunks)

    async def _create(**_kwargs):
        return stream

    chat.client = SimpleNamespace(
        chat=SimpleNamespace(completions=SimpleNamespace(create=_create))
    )
    emitter = _Emitter()

    result = await chat._execute_streaming(
        {"model": "kimi-k3", "stream": True, "stream_options": {"include_usage": True}},
        emitter,
        "moonshotai/Kimi-K3",
        "kimi-k3",
    )

    assert emitter.chunks == ["<reasoning>", "First, reason.", "\n</reasoning>\n", "Hello"]
    assert result.messages
    thinking, answer = result.messages[0].content
    assert isinstance(thinking, ThinkingContent)
    assert thinking.to_storage_dict() == {
        "type": "thinking",
        "id": "",
        "text": "First, reason.",
        "provider": "moonshot",
        "signature": None,
        "signature_encoding": None,
        "metadata": {},
        "summary": [],
    }
    assert answer.text == "Hello"
    assert result.usage is not None
    assert result.usage.input_tokens == 60
    assert result.usage.cached_input_tokens == 40
    assert result.usage.output_tokens == 20
    assert result.usage.response_id == "cmpl-kimi"
