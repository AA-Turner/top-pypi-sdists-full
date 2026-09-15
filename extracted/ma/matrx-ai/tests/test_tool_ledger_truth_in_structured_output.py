"""The model does not get to grade its own tool history.

The break this guards: delete (or weaken to a merge / fill-if-empty) the
``apply_ledger_truth`` call in
``matrx_ai.orchestrator.executor._emit_structured_output_if_schema``, or unhook
``ToolExecutionLogger`` from ``matrx_ai.tools.turn_ledger``, and an agent's
self-reported ``tools_failed: []`` reaches the caller unchallenged — which is
exactly what the Sandbox Specialist agent returned after FOUR errored tool calls
(agent-efficiency-loop, 2026-09-14).

The ledger here is built by calling the REAL ``ToolExecutionLogger`` methods the
tool executor calls, so this also fails if the logger stops feeding the ledger.
Nothing is stubbed inside the system under test: the logger records, the
orchestrator chokepoint parses the model's text and overrides the declared
fields. The only doubles are the emitter (a stream sink) and persistence, which
is switched off with ``store=False`` exactly as an ephemeral run does.
"""

from __future__ import annotations

import json
import time
from types import SimpleNamespace

import pytest

from matrx_ai.tools.logger import ToolExecutionLogger
from matrx_ai.tools.models import ToolContext, ToolDefinition, ToolError, ToolResult
from matrx_ai.tools.turn_ledger import reset_turn_ledger, start_turn_ledger

# A Sandbox-Specialist-shaped report contract: array-of-string tool fields.
STRING_SHAPED_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["summary", "tools_worked", "tools_failed"],
    "properties": {
        "summary": {"type": "string"},
        "tools_worked": {"type": "array", "items": {"type": "string"}},
        "tools_failed": {"type": "array", "items": {"type": "string"}},
    },
}

# The same report, spelled as objects — a schema the string form would violate.
OBJECT_SHAPED_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["summary", "tools_failed"],
    "properties": {
        "summary": {"type": "string"},
        "tools_failed": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["tool_name", "error_message"],
                "properties": {
                    "tool_name": {"type": "string"},
                    "error_message": {"type": "string"},
                },
            },
        },
    },
}

COMMANDS_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["summary", "commands_run"],
    "properties": {
        "summary": {"type": "string"},
        "commands_run": {"type": "array", "items": {"type": "string"}},
    },
}


class _Emitter:
    def __init__(self) -> None:
        self.structured: list[object] = []

    async def send_structured_output(self, payload: object) -> None:
        self.structured.append(payload)

    def __getattr__(self, _name: str):
        async def _noop(*_a, **_k):
            return None

        return _noop


def _completed(final_text: str, schema: dict):
    config = SimpleNamespace(
        response_format={
            "type": "json_schema",
            "json_schema": {"name": "sandbox_report", "strict": True, "schema": schema},
        },
        get_last_output=lambda: final_text,
    )
    return SimpleNamespace(request=SimpleNamespace(config=config))


def _install_ctx(emitter):
    from matrx_connect.context.app_context import AppContext, set_app_context

    set_app_context(
        AppContext(
            emitter=emitter,
            user_id="ledger-truth-test",
            conversation_id="11111111-1111-4111-8111-111111111111",
            request_id="22222222-2222-4222-8222-222222222222",
            # Ephemeral: no chat.tool_call rows are written. The ledger is an
            # in-process mirror and must be just as honest without persistence.
            store=False,
        )
    )


@pytest.fixture
def ledger():
    token = start_turn_ledger()
    yield
    reset_turn_ledger(token)


def _ctx(call_id: str) -> ToolContext:
    return ToolContext(call_id=call_id, tool_name="")


def _ok(tool_name: str, call_id: str) -> ToolResult:
    return ToolResult(
        success=True,
        output={"ok": True},
        started_at=time.time(),
        completed_at=time.time(),
        tool_name=tool_name,
        call_id=call_id,
    )


def _failed(tool_name: str, call_id: str, message: str) -> ToolResult:
    return ToolResult(
        success=False,
        error=ToolError(error_type="execution_error", message=message),
        started_at=time.time(),
        completed_at=time.time(),
        tool_name=tool_name,
        call_id=call_id,
    )


async def _run_tool(logger: ToolExecutionLogger, result: ToolResult, arguments: dict) -> None:
    """Drive one tool call through the real logger, start → terminal."""
    tool_def = ToolDefinition(
        name=result.tool_name,
        parameters={k: {"type": "string"} for k in arguments},
    )
    row_id = await logger.log_started(_ctx(result.call_id), tool_def, arguments)
    if result.success:
        await logger.log_completed(row_id, result, [])
    else:
        await logger.log_error(row_id, result, [])


# Two INDEPENDENT runs with different truths — a hard-coded return cannot
# satisfy both, and neither can the model's own (identical, false) claim.
LEDGER_CASES = [
    pytest.param(
        [
            (_ok("shell_execute", "c1"), {"command": "uv run pytest -q"}),
            (
                _failed("vfs_write", "c2", "Permission denied: /etc/hosts"),
                {"path": "/etc/hosts"},
            ),
        ],
        ["shell_execute"],
        ["vfs_write: Permission denied: /etc/hosts"],
        id="one_write_refused",
    ),
    pytest.param(
        [
            (
                _failed("rag_search", "c3", "invalid input for query argument $5"),
                {"query": "recycling"},
            ),
            (_ok("skill_read", "c4"), {"skill": "sandbox"}),
            (_failed("browser_click", "c5", "no such element: #submit"), {"selector": "#submit"}),
        ],
        ["skill_read"],
        [
            "rag_search: invalid input for query argument $5",
            "browser_click: no such element: #submit",
        ],
        id="two_of_three_failed",
    ),
]


@pytest.mark.asyncio
@pytest.mark.parametrize("calls,expected_worked,expected_failed", LEDGER_CASES)
async def test_declared_tool_fields_carry_ledger_truth_not_the_models_claim(
    ledger, calls, expected_worked, expected_failed
) -> None:
    from matrx_ai.orchestrator.executor import _emit_structured_output_if_schema

    emitter = _Emitter()
    _install_ctx(emitter)
    logger = ToolExecutionLogger()
    for result, arguments in calls:
        await _run_tool(logger, result, arguments)

    # What the model says: everything worked, nothing failed. A lie in both
    # directions — it also claims a tool that errored among the successes.
    model_text = json.dumps(
        {
            "summary": "All clean.",
            "tools_worked": [result.tool_name for result, _ in calls],
            "tools_failed": [],
        }
    )

    parsed = await _emit_structured_output_if_schema(_completed(model_text, STRING_SHAPED_SCHEMA))

    assert parsed is not None, "the structured output must still reach the caller"
    assert parsed["tools_failed"] == expected_failed, (
        "every tool call that errored this turn must appear with its tool name AND "
        "its error text, whatever the model wrote"
    )
    assert parsed["tools_worked"] == expected_worked, (
        "only the calls that actually succeeded may be reported as working"
    )
    assert parsed["summary"] == "All clean.", "fields the platform does not own are untouched"
    # The same corrected object is what the frontend receives.
    assert emitter.structured[0].data["tools_failed"] == expected_failed


@pytest.mark.asyncio
async def test_object_shaped_failures_use_the_schemas_own_property_names(ledger) -> None:
    from matrx_ai.orchestrator.executor import _emit_structured_output_if_schema

    emitter = _Emitter()
    _install_ctx(emitter)
    logger = ToolExecutionLogger()
    await _run_tool(
        logger, _failed("vfs_write", "o1", "Permission denied: /etc/hosts"), {"path": "/etc/hosts"}
    )

    model_text = json.dumps({"summary": "All clean.", "tools_failed": []})
    parsed = await _emit_structured_output_if_schema(_completed(model_text, OBJECT_SHAPED_SCHEMA))

    assert parsed["tools_failed"] == [
        {"tool_name": "vfs_write", "error_message": "Permission denied: /etc/hosts"}
    ], "an array-of-object field must be filled with objects spelled the schema's way"


@pytest.mark.asyncio
async def test_commands_run_is_derived_from_the_tools_free_form_command_argument(
    ledger,
) -> None:
    from matrx_ai.orchestrator.executor import _emit_structured_output_if_schema

    _install_ctx(_Emitter())
    logger = ToolExecutionLogger()
    await _run_tool(logger, _ok("shell_execute", "k1"), {"command": "uv run pytest -q"})
    await _run_tool(logger, _ok("shell_execute", "k2"), {"command": "git status --short"})

    model_text = json.dumps({"summary": "ran nothing", "commands_run": []})
    parsed = await _emit_structured_output_if_schema(_completed(model_text, COMMANDS_SCHEMA))

    assert parsed["commands_run"] == ["uv run pytest -q", "git status --short"], (
        "the commands the run actually executed, in order"
    )


@pytest.mark.asyncio
async def test_commands_run_is_left_alone_when_nothing_in_the_ledger_ran_a_command(
    ledger,
) -> None:
    """Honesty cuts both ways: with nothing to derive from, the platform must not
    blank the field — an invented ``[]`` is a lie of a different shape."""
    from matrx_ai.orchestrator.executor import _emit_structured_output_if_schema

    _install_ctx(_Emitter())
    logger = ToolExecutionLogger()
    await _run_tool(logger, _ok("rag_search", "n1"), {"query": "recycling"})

    model_text = json.dumps({"summary": "ok", "commands_run": ["ls -la"]})
    parsed = await _emit_structured_output_if_schema(_completed(model_text, COMMANDS_SCHEMA))

    assert parsed["commands_run"] == ["ls -la"]


@pytest.mark.asyncio
async def test_a_failure_routed_through_log_completed_is_still_a_failure(ledger) -> None:
    """``handle_tool_calls`` logs its blocked-handoff audit row by calling
    ``log_completed`` with a FAILED ToolResult. The ledger reads the result, not
    the method name — a failure recorded as a success is the exact lie this
    exists to stop."""
    from matrx_ai.orchestrator.executor import _emit_structured_output_if_schema

    _install_ctx(_Emitter())
    logger = ToolExecutionLogger()
    blocked = _failed("handoff_to_researcher", "b1", "Call one handoff, alone, in its own turn.")
    tool_def = ToolDefinition(name=blocked.tool_name)
    row_id = await logger.log_started(_ctx(blocked.call_id), tool_def, {})
    await logger.log_completed(row_id, blocked, [])

    model_text = json.dumps(
        {"summary": "fine", "tools_worked": ["handoff_to_researcher"], "tools_failed": []}
    )
    parsed = await _emit_structured_output_if_schema(_completed(model_text, STRING_SHAPED_SCHEMA))

    assert parsed["tools_worked"] == []
    assert parsed["tools_failed"] == [
        "handoff_to_researcher: Call one handoff, alone, in its own turn."
    ]


@pytest.mark.asyncio
async def test_a_schema_that_declares_none_of_the_fields_is_untouched(ledger) -> None:
    from matrx_ai.orchestrator.executor import _emit_structured_output_if_schema

    _install_ctx(_Emitter())
    logger = ToolExecutionLogger()
    await _run_tool(logger, _failed("vfs_write", "u1", "Permission denied"), {"path": "/etc"})

    schema = {
        "type": "object",
        "additionalProperties": False,
        "required": ["summary"],
        "properties": {"summary": {"type": "string"}},
    }
    parsed = await _emit_structured_output_if_schema(
        _completed(json.dumps({"summary": "ordinary agent"}), schema)
    )
    assert parsed == {"summary": "ordinary agent"}
