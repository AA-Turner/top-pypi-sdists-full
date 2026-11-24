"""CGU-10 finding 3: the non-streaming provider paths sent a bare ``<reasoning>``.

When a settled response carries answer text BEFORE its thought, the fence landed
mid-line and the one block splitter (its inline rule, mirrored by the web and the
Android Kit) kept ``prose <reasoning>…</reasoning>`` as literal answer text. Every
non-streaming adapter now emits settled content through ONE funnel
(``emit_settled_content``) whose opener is ``reasoning_opener`` — the streaming rule.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest

from matrx_ai.config.message_config import UnifiedMessage
from matrx_ai.config.unified_config import UnifiedResponse
from matrx_ai.config.unified_content import TextContent, ThinkingContent
from matrx_ai.processing.blocks.block_detector import split_content_into_blocks

BEFORE = "Sure."
THOUGHT = "The user wants an estimate; eight to nine hours fits."
AFTER = "About eight to nine hours."


class _Emitter:
    def __init__(self) -> None:
        self.chunks: list[str] = []
        self.states: list[str] = []

    async def send_chunk(self, text: str) -> None:
        self.chunks.append(text)

    async def send_reasoning_state(self, state: str) -> None:
        self.states.append(state)

    async def send_data(self, *_a: Any, **_k: Any) -> None:  # citations, none here
        return None


def _openers_start_a_line(stream: str) -> bool:
    """The client splitters (web ``splitContentIntoBlocksV2``, the Android Kit) fence only an
    opener that starts a line; the Python splitter is more lenient, so assert the wire rule."""
    at = stream.find("<reasoning>")
    while at != -1:
        if at and stream[at - 1] != "\n":
            return False
        at = stream.find("<reasoning>", at + 1)
    return True


def _mixed() -> UnifiedResponse:
    return UnifiedResponse(
        messages=[
            UnifiedMessage(
                role="assistant",
                content=[TextContent(text=BEFORE), ThinkingContent(text=THOUGHT), TextContent(text=AFTER)],
            )
        ]
    )


def _bare(cls_path: str, **attrs: Any) -> Any:
    module, name = cls_path.rsplit(".", 1)
    chat = object.__new__(getattr(__import__(module, fromlist=[name]), name))
    chat.debug = False
    for key, value in attrs.items():
        setattr(chat, key, value)
    return chat


async def _create(**_kwargs: Any) -> Any:
    return SimpleNamespace()


def _chat_completions(cls_path: str, **attrs: Any):
    def build():
        chat = _bare(cls_path, **attrs)
        chat.client = SimpleNamespace(chat=SimpleNamespace(completions=SimpleNamespace(create=_create)))
        chat.to_unified_response = lambda *_a, **_k: _mixed()
        return chat, ({"model": "m", "messages": []},)

    return build


def _xai():
    chat = _bare("matrx_ai.providers.xai.xai_api.XAIChat")
    chat.translator = SimpleNamespace(from_xai=lambda _r: _mixed())

    async def sample() -> Any:
        return SimpleNamespace(content="")

    return chat, (SimpleNamespace(sample=sample),)


PATHS = {
    "together": _chat_completions("matrx_ai.providers.together.together_api.TogetherChat"),
    "groq": _chat_completions("matrx_ai.providers.groq.groq_api.GroqChat"),
    "cerebras": _chat_completions("matrx_ai.providers.cerebras.cerebras_api.CerebrasChat"),
    "generic_openai": _chat_completions(
        "matrx_ai.providers.generic_openai.generic_openai_api.GenericOpenAIChat",
        provider_name="generic_openai",
        endpoint_name="[GENERIC]",
    ),
    "xai": _xai,
}


@pytest.mark.asyncio
@pytest.mark.parametrize("provider", sorted(PATHS))
async def test_a_thought_after_answer_text_is_fenced_on_its_own_line(provider: str) -> None:
    chat, args = PATHS[provider]()
    emitter = _Emitter()
    await chat._execute_non_streaming(*args, emitter, "m")

    stream = "".join(emitter.chunks)
    assert _openers_start_a_line(stream), stream
    blocks = split_content_into_blocks(stream)
    assert [b.type for b in blocks] == ["text", "reasoning", "text"], stream
    assert all("<reasoning>" not in b.content and "</reasoning>" not in b.content for b in blocks), stream
    assert THOUGHT in blocks[1].content
    assert emitter.states == ["started", "stopped"]


@pytest.mark.asyncio
async def test_a_leading_thought_gets_no_leading_newline() -> None:
    from matrx_ai.providers.reasoning import emit_settled_content

    emitter = _Emitter()
    response = UnifiedResponse(
        messages=[UnifiedMessage(role="assistant", content=[ThinkingContent(text=THOUGHT), TextContent(text=AFTER)])]
    )
    await emit_settled_content(emitter, response)
    assert emitter.chunks[0] == "<reasoning>"
    assert [b.type for b in split_content_into_blocks("".join(emitter.chunks))] == ["reasoning", "text"]


def test_no_provider_sends_a_bare_opener_by_hand() -> None:
    """Sibling guard: a provider chunk that STARTS with ``<reasoning>`` can land mid-line.
    Openers come from ``reasoning_opener`` / ``emit_settled_content`` or start with a newline."""
    import re
    from pathlib import Path

    import matrx_ai.providers as providers

    root = Path(providers.__file__).parent
    bare = re.compile(r"""send_chunk\(\s*f?["']<reasoning>""")
    offenders = [
        f"{path.relative_to(root)}:{n}"
        for path in root.rglob("*.py")
        for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1)
        if bare.search(line)
    ]
    assert offenders == [], offenders
