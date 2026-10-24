"""THE CHANGE-CLAIM GATE READS THE WHOLE TURN, not only the resumed request's ledger.

Live 2026-10-22, design-system board d1570962, conversation 8e6dae76: the agent wrote
58 rows with ``records_write`` (requests baf8ecc2 … dcca57d5), then called the
client-run ``board_update_tile``; the client's answer resumed the run as request
7f4118e3 with an EMPTY ``tool_calls_details``. Its reply "Colors: 23 written …" was
judged unbacked and a forced turn told the person "No changes were made in this turn".
The message list below is that turn's shape; the ledger is the resumed request's.
"""

from __future__ import annotations

from matrx_ai.config import TextContent, UnifiedMessage
from matrx_ai.config.message_config import host_authored_user_turn
from matrx_ai.config.tools_config import ToolCallContent, ToolResultContent
from matrx_ai.orchestrator.change_claims import (
    AuthoringPolicy,
    decide_change_claim_action,
    evaluate_change_claims,
)

POLICY = AuthoringPolicy(
    mandate_key="design_system.build",
    write_tools=frozenset({"records", "records_write", "board_item_act", "board_update_tile"}),
)
REPLY = "The Colors table has been updated with 23 rows and the cover was written."


def _opening() -> UnifiedMessage:
    msg = UnifiedMessage(role="user", content=[TextContent(text="Build this board's design system now.")], user_content=[])
    msg.metadata = {"authored_by": "host", "authored_reason": "agent_opening"}
    return msg


def _call(name: str, cid: str) -> UnifiedMessage:
    return UnifiedMessage(role="assistant", content=[ToolCallContent(id=cid, name=name)])


def _result(name: str, cid: str, *, error: bool = False) -> UnifiedMessage:
    return UnifiedMessage(role="tool", content=[ToolResultContent(tool_use_id=cid, call_id=cid, name=name, is_error=error)])


def _resumed_turn(*, write_failed: bool = False) -> list[UnifiedMessage]:
    return [
        _opening(),
        _call("records_read", "r1"),
        _result("records_read", "r1"),
        _call("records_write", "w1"),
        _result("records_write", "w1", error=write_failed),
        _call("board_update_tile", "t1"),
        _result("board_update_tile", "t1", error=write_failed),
    ]


def test_a_resumed_request_counts_the_writes_its_turn_already_made():
    report = evaluate_change_claims(POLICY, [], REPLY, messages=_resumed_turn())
    assert report is not None and report.claims, report
    assert report.wrote, report
    assert set(report.successful_tools) == {"records_write", "board_update_tile"}
    assert decide_change_claim_action(report, corrections_used=0) == "proceed"


def test_control_failed_writes_still_force_the_honest_turn():
    report = evaluate_change_claims(POLICY, [], REPLY, messages=_resumed_turn(write_failed=True))
    assert report is not None and report.unbacked, report
    assert decide_change_claim_action(report, corrections_used=0) == "force"


def test_control_writes_from_an_earlier_turn_never_back_this_one():
    earlier = _resumed_turn()
    person = UnifiedMessage(role="user", content=[TextContent(text="Now make it darker.")], user_content=[TextContent(text="Now make it darker.")])
    report = evaluate_change_claims(POLICY, [], REPLY, messages=[*earlier, person])
    assert report is not None and report.unbacked, report


def test_a_gate_notice_inside_the_turn_is_not_its_boundary():
    turn = [*_resumed_turn(), host_authored_user_turn("SYSTEM NOTICE: …", reason="change_claim_gate")]
    report = evaluate_change_claims(POLICY, [], REPLY, messages=turn)
    assert report is not None and report.wrote, report
