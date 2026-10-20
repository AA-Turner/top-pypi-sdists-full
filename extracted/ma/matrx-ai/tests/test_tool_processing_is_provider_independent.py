"""PB-03 defect 11: every provider's tool call announces itself the same way.

Live 2026-10-16: the Anthropic run emitted an ``info`` event ``tool_processing``
for its ``agent_call``; the OpenAI and Google runs emitted none. The event was
sent from inside each provider adapter (Anthropic, Groq, Cerebras, xAI, Together,
generic OpenAI-compatible) and simply never written for OpenAI or Google.

Now it is sent from ONE place — the shared tool loop
(``orchestrator.executor.handle_tool_calls`` → ``tool_notices.emit_tool_processing``)
— for every tool call of every provider, and no adapter sends its own.
"""

from __future__ import annotations

import ast
from pathlib import Path
from typing import Any

import pytest

from matrx_ai.config.enums import Role
from matrx_ai.config.message_config import UnifiedMessage
from matrx_ai.config.tools_config import ToolCallContent
from matrx_ai.config.unified_content import TextContent

PKG = Path(__file__).resolve().parent.parent / "matrx_ai"


class _Recorder:
    def __init__(self) -> None:
        self.infos: list[Any] = []

    async def send_info(self, payload: Any) -> None:
        self.infos.append(payload)


def _response(provider: str) -> Any:
    from matrx_ai.config.unified_config import UnifiedResponse

    return UnifiedResponse(
        messages=[
            UnifiedMessage(
                role=Role.ASSISTANT,
                content=[
                    TextContent(text="checking"),
                    ToolCallContent(id="call_1", name="agent_call", arguments={"agent_id": "x"}),
                ],
            )
        ],
        metadata={"provider": provider},
    )


@pytest.mark.parametrize("provider", ["openai", "google", "anthropic", "together"])
async def test_every_provider_announces_its_tool_call(provider: str) -> None:
    from matrx_ai.orchestrator.tool_notices import emit_tool_processing

    recorder = _Recorder()
    await emit_tool_processing(_response(provider), recorder)
    assert [p.code for p in recorder.infos] == ["tool_processing"]
    assert recorder.infos[0].metadata["tool_call"] == "agent_call"
    assert recorder.infos[0].metadata["call_id"] == "call_1"


def test_no_provider_adapter_sends_its_own() -> None:
    offenders = [
        str(path.relative_to(PKG))
        for path in (PKG / "providers").rglob("*.py")
        if '"tool_processing"' in path.read_text()
    ]
    assert offenders == [], f"provider adapters still emit tool_processing: {offenders}"


def test_shared_tool_loop_calls_the_one_emitter() -> None:
    tree = ast.parse((PKG / "orchestrator" / "executor.py").read_text())
    fn = next(
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.AsyncFunctionDef) and node.name == "handle_tool_calls"
    )
    called = {
        getattr(n.func, "id", getattr(n.func, "attr", None))
        for n in ast.walk(fn)
        if isinstance(n, ast.Call)
    }
    assert "emit_tool_processing" in called
