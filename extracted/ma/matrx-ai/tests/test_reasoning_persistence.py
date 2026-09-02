"""Reasoning must survive adapter conversion and stream finalization.

The persistent conversation writer consumes ``UnifiedResponse.messages``.  A
provider is therefore not integrated correctly when it only sends reasoning to
the live emitter: its final response must contain a ``ThinkingContent`` whose
storage representation has the ``thinking`` discriminator.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest

from matrx_ai.config import ThinkingContent
from matrx_ai.db.message_parts import validate_message_content
from matrx_ai.providers.generic_openai.generic_openai_api import GenericOpenAIChat
from matrx_ai.providers.generic_openai.translator import GenericOpenAITranslator
from matrx_ai.providers.groq.groq_api import GroqChat
from matrx_ai.providers.groq.translator import GroqTranslator
from matrx_ai.providers.together.together_api import TogetherChat
from matrx_ai.providers.together.translator import TogetherTranslator
from matrx_ai.providers.xai.translator import XAITranslator


class _Emitter:
    def __init__(self) -> None:
        self.chunks: list[str] = []
        self.reasoning_states: list[str] = []

    async def send_chunk(self, text: str) -> None:
        self.chunks.append(text)

    async def send_reasoning_state(self, state: str) -> None:
        self.reasoning_states.append(state)

    async def send_info(self, _payload: Any) -> None:
        pass


class _Stream:
    def __init__(self, chunks: list[Any]) -> None:
        self._chunks = chunks

    def __aiter__(self):
        return self._iterate()

    async def _iterate(self):
        for chunk in self._chunks:
            yield chunk


def _stream() -> _Stream:
    return _Stream(
        [
            SimpleNamespace(
                id="response-1",
                usage=None,
                choices=[
                    SimpleNamespace(
                        delta=SimpleNamespace(
                            content=None,
                            reasoning_content="consider the constraints; ",
                            reasoning=None,
                            tool_calls=None,
                        ),
                        finish_reason=None,
                        usage=None,
                    )
                ],
            ),
            SimpleNamespace(
                id="response-1",
                usage=SimpleNamespace(prompt_tokens=10, completion_tokens=4),
                choices=[
                    SimpleNamespace(
                        delta=SimpleNamespace(
                            content="final answer",
                            reasoning_content=None,
                            reasoning=None,
                            tool_calls=None,
                        ),
                        finish_reason="stop",
                        usage=None,
                    )
                ],
            ),
        ]
    )


def _assert_durable_reasoning(response: Any, provider: str) -> None:
    assert response.messages
    thinking, answer = response.messages[0].content
    assert isinstance(thinking, ThinkingContent)
    assert thinking.text == "consider the constraints; "
    assert thinking.provider == provider
    assert thinking.to_storage_dict()["type"] == "thinking"
    assert answer.text == "final answer"


@pytest.mark.parametrize("provider", ["moonshot", "together", "groq", "xai"])
def test_thinking_provider_is_accepted_by_the_database_content_validator(provider: str) -> None:
    stored = ThinkingContent(text="durable thought", provider=provider).to_storage_dict()
    validated = validate_message_content([stored])

    assert validated == [
        {
            "type": "thinking",
            "id": "",
            "text": "durable thought",
            "provider": provider,
            "metadata": {},
            "summary": [],
        }
    ]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("adapter_class", "provider", "extra_args"),
    [
        (GenericOpenAIChat, "moonshot", ("moonshotai/Kimi-K3", "kimi-k3")),
        (TogetherChat, "together", ("together/model",)),
        (GroqChat, "groq", ("groq/model",)),
    ],
)
async def test_openai_compatible_streaming_reasoning_is_durable(
    adapter_class: type[Any], provider: str, extra_args: tuple[str, ...]
) -> None:
    adapter = object.__new__(adapter_class)
    adapter.debug = False
    adapter.endpoint_name = f"[{provider.upper()} CHAT]"
    if adapter_class is GenericOpenAIChat:
        adapter.provider_name = provider

    async def _create(**_kwargs: Any) -> _Stream:
        return _stream()

    adapter.client = SimpleNamespace(
        chat=SimpleNamespace(completions=SimpleNamespace(create=_create))
    )
    emitter = _Emitter()
    response = await adapter._execute_streaming({"stream": True}, emitter, *extra_args)

    _assert_durable_reasoning(response, provider)
    assert emitter.reasoning_states == ["started", "stopped"]


@pytest.mark.parametrize(
    ("translator", "method_name", "provider"),
    [
        (GenericOpenAITranslator(), "from_generic_openai", "moonshot"),
        (TogetherTranslator(), "from_together", "together"),
        (GroqTranslator(), "from_groq", "groq"),
    ],
)
def test_openai_compatible_non_streaming_reasoning_is_durable(
    translator: Any, method_name: str, provider: str
) -> None:
    response = SimpleNamespace(
        id="response-1",
        model="provider-model",
        usage=None,
        choices=[
            SimpleNamespace(
                finish_reason="stop",
                message=SimpleNamespace(
                    content="final answer",
                    reasoning_content="consider the constraints; ",
                    reasoning=None,
                    tool_calls=None,
                ),
            )
        ],
    )
    method = getattr(translator, method_name)
    unified = (
        method(response, provider)
        if method_name == "from_generic_openai"
        else method(response)
    )

    _assert_durable_reasoning(unified, provider)


def test_xai_reasoning_is_durable() -> None:
    response = SimpleNamespace(
        id="response-1",
        proto=SimpleNamespace(model="grok-4.3"),
        content="final answer",
        reasoning_content="consider the constraints; ",
        tool_calls=[],
        usage=None,
        finish_reason="REASON_STOP",
        citations=[],
    )

    _assert_durable_reasoning(XAITranslator().from_xai(response), "xai")
