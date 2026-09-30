"""Arguments the executor strips are TOLD to the model, never dropped quietly.

The flattened dispatcher schema offers every action's fields, so a model can send
a field another action owns (``web`` action=search with ``url``). The executor
removes it and re-validates — correct — but only logged it, so the model got an
answer to a different question than it asked and never learned. The result the
model reads now carries a notice, and a rebuilt turn replays the same notice.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest

import matrx_ai.tools._generated_declarations  # noqa: F401 — registers WebArgs
from matrx_ai.tools.executor import ToolExecutor
from matrx_ai.tools.logger import ToolExecutionLogger
from matrx_ai.tools.models import ToolContext, ToolDefinition, ToolType
from matrx_ai.tools.registry import ToolRegistry


#: The persisted tool_step name that carries a model notice (executor.MODEL_NOTICE_STEP).
MODEL_NOTICE_STEP = "model_notice"


class _NullEmitter:
    async def send_chunk(self, *_a: Any, **_kw: Any) -> None: ...
    async def send_reasoning_chunk(self, *_a: Any, **_kw: Any) -> None: ...
    async def send_data(self, *_a: Any, **_kw: Any) -> None: ...
    async def send_phase(self, *_a: Any, **_kw: Any) -> None: ...
    async def send_warning(self, *_a: Any, **_kw: Any) -> None: ...
    async def send_error(self, *_a: Any, **_kw: Any) -> None: ...
    async def send_tool_event(self, *_a: Any, **_kw: Any) -> None: ...
    async def fatal_error(self, *_a: Any, **_kw: Any) -> None: ...
    async def send_end(self, *_a: Any, **_kw: Any) -> None: ...


@pytest.fixture
def web_dispatch(monkeypatch):
    from matrx_connect import AppContext
    from matrx_connect.context.app_context import clear_app_context, set_app_context

    token = set_app_context(AppContext(emitter=_NullEmitter(), metadata={}, is_authenticated=True))
    registry = ToolRegistry.get_instance()
    saved = dict(registry._tools)
    persisted: list[list[dict[str, Any]]] = []

    async def body(*_a: Any, **_kw: Any) -> str:
        return "3 search results"  # a plain-string output: no dict to hang a key on

    async def capture(self, row_id, result, execution_events=None, **_kw):
        persisted.append(execution_events or [])

    monkeypatch.setattr(ToolExecutionLogger, "log_completed", capture)
    definition = ToolDefinition(
        name="web",
        description="Web dispatcher",
        parameters={},
        tool_type=ToolType.LOCAL,
        function_path="matrx_ai.tools.implementations.web.web",
    )
    definition._callable = body
    registry._tools["web"] = definition
    yield ToolExecutor(registry=registry), persisted
    registry._tools = saved
    clear_app_context(token)


def _ctx() -> ToolContext:
    return ToolContext(call_id="call-ignored", tool_name="web", emitter=_NullEmitter())


async def test_a_stray_argument_is_named_in_the_result_the_model_reads(web_dispatch) -> None:
    executor, persisted = web_dispatch
    content, result = await executor.execute(
        "web", {"action": "search", "queries": ["plumbers"], "url": "https://a.example"}, _ctx()
    )
    assert result.success is True, result.error
    text = content["content"]
    assert text.startswith("3 search results")
    assert "ignored argument(s) for action='search': url" in text
    assert "not accepted by this action" in text

    # A rebuilt turn replays the persisted row: the same notice must come back.
    from matrx_ai.db._conversation_rebuild_impl import _rebuild_tool_result_content

    events = persisted[-1]
    assert any((e.get("data") or {}).get("step") == MODEL_NOTICE_STEP for e in events)
    row = SimpleNamespace(
        call_id="call-ignored",
        tool_name="web",
        output="3 search results",
        is_error=False,
        output_chars=16,
        output_preview=None,
        model_stub_at=None,
        execution_events=events,
    )
    replayed = _rebuild_tool_result_content([row])[0]["content"]
    assert "ignored argument(s) for action='search': url" in replayed


async def test_a_clean_call_carries_no_notice(web_dispatch) -> None:
    executor, _persisted = web_dispatch
    content, result = await executor.execute(
        "web", {"action": "search", "queries": ["plumbers"]}, _ctx()
    )
    assert result.success is True and content["content"] == "3 search results"
