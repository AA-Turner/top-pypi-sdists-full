"""Designated-member enforcement (C-26, D-38) — predicate, decision table, and
the executor seams.

The guard's whole point is that the RUNTIME decides from durable facts —
tool_call_history ∩ the projection map — never the prompt. These tests hand the
predicate real composed shapes (projection maps keyed by prompt_id, per-call
{name, success} details) so a wrong join, a dropped success flag, or a swapped
member produces a different, failing answer.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from matrx_ai.orchestrator.required_members import (
    REQUIRED_MEMBER_SKIPPED_STATUS,
    REQUIRED_ORCHESTRA_MEMBERS_KEY,
    decide_required_member_action,
    evaluate_required_members,
)
from matrx_ai.orchestrator.tracking import ToolCallUsage
from matrx_ai.tools.agent_projection import PROJECTED_AGENT_TOOLS_KEY

VALIDATOR_ID = "11111111-1111-1111-1111-111111111111"
RESEARCHER_ID = "22222222-2222-2222-2222-222222222222"


def _metadata(required_ids: list[tuple[str, str | None]]) -> dict:
    """Metadata as the host stamps it: declaration + projection map, with the
    projection keyed custom_tool_N -> {prompt_id: agent_id}."""
    projections = {
        "custom_tool_1": {"prompt_id": RESEARCHER_ID, "tool_type": "agent"},
        "custom_tool_2": {"prompt_id": VALIDATOR_ID, "tool_type": "agent"},
    }
    return {
        REQUIRED_ORCHESTRA_MEMBERS_KEY: [
            {"agent_id": agent_id, "role_title": title} for agent_id, title in required_ids
        ],
        PROJECTED_AGENT_TOOLS_KEY: projections,
    }


def _history(calls: list[tuple[str, bool]]) -> list[ToolCallUsage]:
    return [
        ToolCallUsage(
            iteration=i,
            tool_calls_count=1,
            tool_calls_details=[{"name": name, "id": f"c{i}", "success": success}],
        )
        for i, (name, success) in enumerate(calls)
    ]


ACTIVE = ["web_search", "custom_tool_1", "custom_tool_2"]


def test_satisfied_only_when_the_required_member_itself_succeeded() -> None:
    metadata = _metadata([(VALIDATOR_ID, "Validator")])

    # The OTHER member succeeding must not satisfy the requirement — this is
    # the member-swap forcing function: a predicate that checks "any agent
    # tool succeeded" instead of joining prompt_id -> projected name passes
    # the wrong case and fails here.
    report = evaluate_required_members(
        metadata,
        _history([("custom_tool_1", True)]),
        active_tool_names=ACTIVE,
    )
    assert [m.agent_id for m in report.missing] == [VALIDATOR_ID]
    assert report.missing[0].projected_name == "custom_tool_2"

    report = evaluate_required_members(
        metadata,
        _history([("custom_tool_1", True), ("custom_tool_2", True)]),
        active_tool_names=ACTIVE,
    )
    assert report.satisfied


def test_failed_call_does_not_satisfy_but_later_success_does() -> None:
    metadata = _metadata([(VALIDATOR_ID, "Validator")])

    report = evaluate_required_members(
        metadata,
        _history([("custom_tool_2", False)]),
        active_tool_names=ACTIVE,
    )
    assert not report.satisfied

    report = evaluate_required_members(
        metadata,
        _history([("custom_tool_2", False), ("custom_tool_2", True)]),
        active_tool_names=ACTIVE,
    )
    assert report.satisfied


def test_inherited_declaration_in_child_loop_is_unenforceable_not_missing() -> None:
    """fork_for_child_agent copies metadata into member loops. A loop whose
    active toolset does not offer the projected name must never fire."""
    metadata = _metadata([(VALIDATOR_ID, "Validator")])
    report = evaluate_required_members(
        metadata,
        _history([]),
        active_tool_names=["web_search"],  # a member's own toolset
    )
    assert report.satisfied
    assert [m.agent_id for m in report.unenforceable] == [VALIDATOR_ID]


def test_unprojected_required_member_is_unenforceable() -> None:
    metadata = _metadata([(VALIDATOR_ID, "Validator")])
    del metadata[PROJECTED_AGENT_TOOLS_KEY]["custom_tool_2"]
    report = evaluate_required_members(metadata, _history([]), active_tool_names=ACTIVE)
    assert report.satisfied
    assert len(report.unenforceable) == 1


def test_no_declaration_means_no_requirement() -> None:
    report = evaluate_required_members(
        {PROJECTED_AGENT_TOOLS_KEY: {"custom_tool_1": {"prompt_id": RESEARCHER_ID}}},
        _history([]),
        active_tool_names=ACTIVE,
    )
    assert report.satisfied
    assert report.required == []


# ── decision table ─────────────────────────────────────────────────────────


def _missing_report():
    metadata = _metadata([(VALIDATOR_ID, "Validator")])
    return evaluate_required_members(metadata, _history([]), active_tool_names=ACTIVE)


@pytest.mark.parametrize(
    ("already_intervened", "loop_guard", "is_workflow", "expected"),
    [
        (False, False, False, "force"),  # first miss, chat → forced turn
        (False, False, True, "force"),  # first miss, workflow → forced turn too (D-38)
        (True, False, False, "pause"),  # still skipped, chat → distinct pause
        (True, False, True, "fail"),  # still skipped, workflow → loud failure
        (False, True, False, "proceed"),  # loop guard owns the turn (already non-clean)
        (True, True, True, "proceed"),
    ],
)
def test_decision_table(already_intervened, loop_guard, is_workflow, expected) -> None:
    action = decide_required_member_action(
        _missing_report(),
        already_intervened=already_intervened,
        loop_guard_intervened=loop_guard,
        is_workflow_step=is_workflow,
    )
    assert action == expected


def test_nothing_forceable_goes_terminal_immediately() -> None:
    """Declared required but not offered as a tool anywhere it could be forced
    → 'force' would restrict the toolset to NOTHING; the decision must skip
    straight to the terminal posture."""
    metadata = _metadata([(VALIDATOR_ID, "Validator")])
    # Enforceable (active) but... this case needs projected present; simulate a
    # missing member whose projection vanished mid-run by evaluating, then
    # stripping forceable names via a report with no projection.
    del metadata[PROJECTED_AGENT_TOOLS_KEY]["custom_tool_2"]
    report = evaluate_required_members(metadata, _history([]), active_tool_names=ACTIVE)
    # Unenforceable → satisfied → proceed; the terminal-shortcut branch is only
    # reachable for enforceable-but-unforceable, which cannot occur by
    # construction (enforceable requires a projected name). Pin the invariant:
    assert report.satisfied
    assert decide_required_member_action(
        report, already_intervened=False, loop_guard_intervened=False, is_workflow_step=False
    ) == "proceed"


def test_satisfied_always_proceeds() -> None:
    metadata = _metadata([(VALIDATOR_ID, "Validator")])
    report = evaluate_required_members(
        metadata, _history([("custom_tool_2", True)]), active_tool_names=ACTIVE
    )
    assert decide_required_member_action(
        report, already_intervened=True, loop_guard_intervened=False, is_workflow_step=True
    ) == "proceed"


# ── executor seams (structural pins) ───────────────────────────────────────
# The gate is worthless if a finishing exit stops consulting it. These pins
# fail the build when the seam is removed or reordered past the finalize.

EXECUTOR_SRC = (
    Path(__file__).resolve().parents[1] / "matrx_ai" / "orchestrator" / "executor.py"
).read_text()


def test_no_tool_calls_exit_consults_the_gate_before_finalizing() -> None:
    # Inside the `if tool_results is None:` block: gate call, then the force /
    # fail branches, then the pause status stamp — all BEFORE the block's
    # _finalize_and_persist.
    block_start = EXECUTOR_SRC.index("if tool_results is None:")
    finalize_at = EXECUTOR_SRC.index("_finalize_and_persist(", block_start)
    gate_at = EXECUTOR_SRC.index("_required_member_gate(", block_start)
    assert gate_at < finalize_at
    assert REQUIRED_MEMBER_SKIPPED_STATUS == "paused_required_member_skipped"
    assert 'REQUIRED_MEMBER_SKIPPED_STATUS' in EXECUTOR_SRC


def test_handoff_exit_cannot_bypass_the_guard() -> None:
    handoff_fn = EXECUTOR_SRC.index("async def _finalize_handoff(")
    next_fn = EXECUTOR_SRC.index("\nasync def ", handoff_fn + 10)
    handoff_body = EXECUTOR_SRC[handoff_fn:next_fn]
    assert "evaluate_required_members(" in handoff_body
    assert "REQUIRED_MEMBER_SKIPPED_STATUS" in handoff_body
    # workflow posture at the handoff exit is a hard failure
    assert '"failed"' in handoff_body


def test_forced_turn_restores_the_full_toolset_before_dispatch() -> None:
    restore_at = EXECUTOR_SRC.index("required_member_forced_pending:")
    dispatch_at = EXECUTOR_SRC.index("await handle_tool_calls(", restore_at)
    # restore happens in the loop body before this iteration's dispatch
    assert restore_at < dispatch_at
    # and the restriction really sets tool_choice='required'
    assert re.search(r"tool_choice = \"required\"", EXECUTOR_SRC)
