"""A helper's relayed answer is its final prose — never a fragment of it.

Live 2026-10-21 (tracker 258f17f4): a parent agent was handed, as a helper's
"result", (a) the raw JSON of the helper's last tool call, (b) the literal
``['active_sandbox']`` and (c) a dict whose keys were sentence fragments
(``"changed": "", "pass)": ""``). Causes: the lenient JSON extractor ran over
prose from agents that declared no output schema, and ``get_output()``
serialised a trailing tool call as if it were answer text.
"""

from __future__ import annotations

from types import SimpleNamespace

from matrx_ai.agents.executor import unanswered_tool_calls
from matrx_ai.config.enums import Role
from matrx_ai.config.message_config import UnifiedMessage
from matrx_ai.config.tools_config import ToolCallContent
from matrx_ai.config.unified_content import TextContent
from matrx_ai.tools.implementations.agent_call import relayable_answer

PLAIN_AGENT = SimpleNamespace(name="helper", output_schema=None, config=None)

TOOL_CALL_JSON = (
    '{"type":"tool_call","call_id":"toolu_01","name":"shell_execute",'
    '"arguments":{"command":"git log -1"}}'
)

REPORT_QUOTING_A_TOOL_CALL = (
    "Root cause found.\n\n"
    f"- The parent was handed `{TOOL_CALL_JSON}` instead of the report.\n"
    "- Fixed in `agent_call.py`.\n"
)
REPORT_WITH_A_LIST_SPAN = (
    "Root cause: `missing_tools: ['active_sandbox']` after the resume, so the "
    "helper lost its shell.\n\n- Fixed in `children.py`.\n- Tests pass.\n"
)
REPORT_WITH_FRAGMENTS = (
    "Files changed (tests pass):\n\n- `children.py` {changed, pass), tests: "
    "12 passed, 0 failed}\n- Commit abc123 pushed.\n"
)


def test_shape_a_a_quoted_tool_call_stays_inside_the_report() -> None:
    assert relayable_answer(REPORT_QUOTING_A_TOOL_CALL, PLAIN_AGENT) == REPORT_QUOTING_A_TOOL_CALL


def test_shape_b_a_list_in_a_code_span_is_not_the_answer() -> None:
    assert relayable_answer(REPORT_WITH_A_LIST_SPAN, PLAIN_AGENT) == REPORT_WITH_A_LIST_SPAN


def test_the_three_live_reports_did_garble_under_the_old_extractor() -> None:
    """Guard the fixtures: each one is a shape the lenient extractor mangles."""
    from matrx_ai.agents.output import parse_agent_output

    for report in (REPORT_QUOTING_A_TOOL_CALL, REPORT_WITH_A_LIST_SPAN, REPORT_WITH_FRAGMENTS):
        extraction = parse_agent_output(report, PLAIN_AGENT)
        assert extraction.success and isinstance(extraction.data, dict | list), report


def test_shape_c_prose_is_never_repaired_into_a_dict() -> None:
    assert relayable_answer(REPORT_WITH_FRAGMENTS, PLAIN_AGENT) == REPORT_WITH_FRAGMENTS


def test_an_answer_that_is_wholly_json_still_comes_back_as_data() -> None:
    assert relayable_answer('{"ok": true, "n": 2}', PLAIN_AGENT) == {"ok": True, "n": 2}


def test_a_declared_schema_still_gets_its_json_parsed() -> None:
    agent = SimpleNamespace(
        name="structured",
        output_schema={"type": "object", "properties": {"n": {"type": "integer"}}},
        config=None,
    )
    assert relayable_answer('Here you go:\n```json\n{"n": 3}\n```', agent) == {"n": 3}


def _assistant(*content: object) -> UnifiedMessage:
    return UnifiedMessage(role=Role.ASSISTANT, content=list(content))


def test_shape_a_a_trailing_tool_call_is_not_serialised_as_the_answer() -> None:
    call = ToolCallContent(id="toolu_01", name="shell_execute", arguments={"command": "git log -1"})
    assert _assistant(call).get_output() == ""
    assert _assistant(TextContent(text="Checking."), call).get_output() == "Checking."


def test_a_run_cut_off_mid_tool_call_says_so_plainly() -> None:
    call = ToolCallContent(id="toolu_01", name="shell_execute", arguments={"command": "git log -1"})
    stopped = unanswered_tool_calls(_assistant(call))
    assert stopped == [{"name": "shell_execute", "arguments": {"command": "git log -1"}}]
    answer = relayable_answer("", PLAIN_AGENT, stopped_on_tool_calls=stopped)
    assert answer.startswith("The helper stopped before writing an answer")
    assert "last action: shell_execute(command='git log -1')" in answer
    assert "tool_call" not in answer


def test_a_turn_with_answer_text_is_not_reported_as_stopped() -> None:
    call = ToolCallContent(id="toolu_01", name="shell_execute", arguments={})
    assert unanswered_tool_calls(_assistant(TextContent(text="All done."), call)) == []
    assert unanswered_tool_calls(None) == []
