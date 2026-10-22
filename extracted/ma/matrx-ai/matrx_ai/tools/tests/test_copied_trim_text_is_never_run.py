"""A tool call carrying text copied from a trimmed call is refused, never run.

Conversation 9b224bf5 (2026-10-21): the context trimmer replaced old tool-call
arguments with ``{"result": "[tool arguments cleared] …", "keys": […], "chars": N}``
and the model sent that object as the arguments of three NEW calls. The trimmer
now keeps each call's real shape and cuts long values with a note
(``config/context_trim.py``); this guard is the second layer: a new call whose
arguments carry the note — or the retired stub — is refused with a message the
model can act on, and the tool body never runs.

What each test is FOR (the production change that turns it red): delete the
``arguments_carry_trim_marker`` block in ``ToolExecutor.execute`` and both
refusal tests reach the tool body.
"""

from __future__ import annotations

from typing import Any

import pytest

from matrx_ai.config.context_trim import (
    _DEFAULT_ARGUMENTS_SUBSTITUTE,
    TRIMMED_ARGUMENT_MARKER,
)
from matrx_ai.tools.executor import ToolExecutor
from matrx_ai.tools.guardrails import GuardrailEngine
from matrx_ai.tools.lifecycle import ToolLifecycleManager
from matrx_ai.tools.logger import ToolExecutionLogger
from matrx_ai.tools.models import ToolDefinition, ToolType
from matrx_ai.tools.registry import ToolRegistry
from matrx_ai.tools.tests.test_dispatch_validation import _make_ctx, _NullEmitter


@pytest.fixture
def registry():
    reg = ToolRegistry.get_instance()
    saved = dict(reg._tools)
    yield reg
    reg._tools = saved


@pytest.fixture
def app_ctx():
    from matrx_connect import AppContext
    from matrx_connect.context.app_context import clear_app_context, set_app_context

    token = set_app_context(AppContext(emitter=_NullEmitter(), metadata={}, is_authenticated=True))
    yield
    clear_app_context(token)


def _executor_with_probe(registry: ToolRegistry, ran: list[dict[str, Any]]) -> ToolExecutor:
    definition = ToolDefinition(
        name="trim_copy_probe",
        description="probe",
        parameters={},
        tool_type=ToolType.LOCAL,
        function_path="tests.trim_copy_probe",
    )

    async def probe(args: dict[str, Any], _ctx: Any) -> dict[str, Any]:
        ran.append(args)
        return {"ok": True}

    definition._callable = probe
    registry._tools["trim_copy_probe"] = definition
    return ToolExecutor(
        registry=registry,
        guardrails=GuardrailEngine(),
        execution_logger=ToolExecutionLogger(),
        lifecycle=ToolLifecycleManager.get_instance(),
    )


@pytest.mark.parametrize(
    "arguments",
    [
        # What a model copies from a trimmed call today.
        {"prompt": "Fix the bug" + _DEFAULT_ARGUMENTS_SUBSTITUTE.format(n=3200, unit="characters")},
        # The retired stub, verbatim from conversation 9b224bf5.
        {
            "keys": ["prompt", "agent_id", "description", "run_in_background"],
            "chars": 3735,
            "result": "[tool arguments cleared] Large arguments removed from context",
        },
    ],
    ids=["trim-note", "retired-stub"],
)
async def test_a_call_carrying_copied_trim_text_is_refused(registry, app_ctx, arguments) -> None:
    ran: list[dict[str, Any]] = []
    executor = _executor_with_probe(registry, ran)

    content, result = await executor.execute("trim_copy_probe", arguments, _make_ctx())

    assert ran == [], "a call carrying copied trim text reached the tool body"
    assert result.success is False and result.error is not None
    assert result.error.error_type == "invalid_arguments"
    assert "trimmed from your context" in result.error.message
    assert "in full" in (result.error.suggested_action or "")
    assert content


async def test_a_clean_call_still_runs(registry, app_ctx) -> None:
    ran: list[dict[str, Any]] = []
    executor = _executor_with_probe(registry, ran)

    _content, result = await executor.execute(
        "trim_copy_probe", {"prompt": "Fix the bug in the parser"}, _make_ctx()
    )

    assert result.success is True
    assert ran == [{"prompt": "Fix the bug in the parser"}]


def test_the_note_carries_the_marker_the_executor_looks_for() -> None:
    assert TRIMMED_ARGUMENT_MARKER in _DEFAULT_ARGUMENTS_SUBSTITUTE.format(n=1, unit="items")
