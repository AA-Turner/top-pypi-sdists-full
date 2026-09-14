"""THE LOOP GUARD'S REASON TRAVELS — and a stalled loop is never engine_error.

Found live 2026-09-12, workflow run ``6fa6ad90`` ("Newsroom Desk"), node
``n_check`` ("Check it against the live Rulebook"): the check agent called the
``rulebook`` tool 11 times with ``rulebook_id="org-newsroom"`` — a slug where a
UUID belongs — every call failed, the loop guard disabled tools and paused the
turn for a user who does not exist inside a workflow step. What reached the run,
and the person:

    NodeFailureError: Node 'n_check' failed: ai_turn_failed: AI turn ended with
    status 'paused_loop_guard' (paused_loop_guard): no error detail recorded
    → cause engine_error → "Check it against the live Rulebook stopped partway
      through."

Every fact needed to fix it was in the executor's hands. This drives the real
chain — real tool-call history → real health verdict → the real metadata builder
→ the real node normalizer → the real cause ladder — and asserts the tool, the
count, the error and the remedy survive it, with the cause landing on
``tool_loop_stalled``.

Run with:  uv run pytest packages/matrx-ai/tests/test_loop_guard_reason_travels.py -v
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest
from matrx_graph.failure import Cause, failure_from_exception
from matrx_graph.types.result import Failure

from matrx_ai.graph_nodes.shared import (
    AiTurnFailedError,
    normalize_completed,
    normalize_completed_result,
)
from matrx_ai.orchestrator.executor import _loop_guard_meta
from matrx_ai.orchestrator.loop_guard import (
    LOOP_STALL_ERROR_TYPE,
    evaluate_loop_health,
    loop_guard_evidence,
)
from matrx_ai.orchestrator.tracking import ToolCallUsage

RULEBOOK_ERROR = (
    "Invalid arguments: 1 validation error for RulebookArgs\n"
    "rulebook_id\n  invalid input syntax for type uuid: \"org-newsroom\""
)


def _history(*, failures: int = 11, tool: str = "rulebook") -> list[ToolCallUsage]:
    """The live shape: one iteration firing N parallel calls that all fail.

    Matches ``_tool_call_details_from_content`` — name, success, the structured
    error, the agent-facing string, and the arguments a failed call carries.
    """
    return [
        ToolCallUsage(
            iteration=1,
            tool_calls_count=failures,
            tool_calls_details=[
                {
                    "name": tool,
                    "id": f"call_{i}",
                    "call_id": f"call_{i}",
                    "success": False,
                    "arguments": {
                        "action": "read",
                        "rulebook_id": "org-newsroom",
                        "section": "analysis",
                    },
                    "agent_error": RULEBOOK_ERROR,
                    "error": {"message": RULEBOOK_ERROR},
                }
                for i in range(failures)
            ],
        )
    ]


def _completed(metadata: dict) -> SimpleNamespace:
    """Minimal CompletedRequest stand-in — the normalizer is getattr-based."""
    return SimpleNamespace(
        request=None,
        final_response=None,
        total_usage=None,
        timing_stats={},
        tool_call_stats={},
        iterations=3,
        metadata=metadata,
    )


def _stalled_metadata() -> dict:
    """Exactly what the executor now stamps when the guard has intervened."""
    history = _history()
    health = evaluate_loop_health(history)
    assert health.verdict == "stuck", "the fixture must actually trip the guard"
    meta = {"status": "paused_loop_guard"}
    meta.update(
        _loop_guard_meta(
            health={
                "verdict": health.verdict,
                "reason": health.reason,
                "total_calls": health.total_calls,
                "window_size": health.window_size,
                "failures_in_window": health.failures_in_window,
                "successes_in_window": health.successes_in_window,
            },
            evidence=loop_guard_evidence(history),
        )
    )
    return meta


# ---------------------------------------------------------------------------
# The evidence itself
# ---------------------------------------------------------------------------


def test_evidence_names_the_tool_the_count_and_the_error() -> None:
    evidence = loop_guard_evidence(_history())
    assert evidence["failed_calls"] == 11
    assert evidence["total_calls"] == 11
    assert [row["tool"] for row in evidence["tools"]] == ["rulebook"]
    row = evidence["tools"][0]
    assert row["failures"] == 11
    assert row["calls"] == 11
    assert "org-newsroom" in row["last_error"]


def test_evidence_never_carries_the_call_arguments() -> None:
    """A failure record is a diagnosis, not a payload dump."""
    evidence = loop_guard_evidence(_history())
    for row in evidence["tools"]:
        assert "arguments" not in row
        assert "action" not in row


def test_successful_calls_leave_no_failure_row() -> None:
    history = [
        ToolCallUsage(
            iteration=1,
            tool_calls_count=2,
            tool_calls_details=[{"name": "rulebook", "success": True} for _ in range(2)],
        )
    ]
    evidence = loop_guard_evidence(history)
    assert evidence == {"failed_calls": 0, "total_calls": 2, "tools": []}


# ---------------------------------------------------------------------------
# The node failure — the sentence W66 never got
# ---------------------------------------------------------------------------


def test_node_failure_names_the_tool_and_the_error() -> None:
    with pytest.raises(AiTurnFailedError) as exc:
        normalize_completed(_completed(_stalled_metadata()))
    msg = str(exc.value)
    assert "no error detail recorded" not in msg
    assert "rulebook" in msg  # the tool
    assert "11 of its 11" in msg  # how many times
    assert "org-newsroom" in msg  # what it said
    assert "retry the step" in msg  # the remedy
    assert LOOP_STALL_ERROR_TYPE in msg  # the machine word


def test_detail_is_rebuilt_from_evidence_when_the_sentence_is_missing() -> None:
    """An older stored request kept the facts but not the sentence."""
    meta = _stalled_metadata()
    meta.pop("error")
    with pytest.raises(AiTurnFailedError) as exc:
        normalize_completed(_completed(meta))
    assert "rulebook" in str(exc.value)


def test_no_evidence_says_so_and_says_why() -> None:
    """"Nothing recorded" is allowed — mute is not."""
    with pytest.raises(AiTurnFailedError) as exc:
        normalize_completed(_completed({"status": "paused_loop_guard"}))
    msg = str(exc.value)
    assert "no error detail recorded" not in msg
    assert "itself the defect" in msg


def test_failure_result_carries_the_structured_evidence() -> None:
    result = normalize_completed_result(_completed(_stalled_metadata()))
    assert isinstance(result, Failure)
    error = result.error
    assert error is not None
    assert error.code == "ai_turn_failed"
    assert error.details["error_type"] == LOOP_STALL_ERROR_TYPE
    assert error.details["loop_guard_evidence"]["tools"][0]["tool"] == "rulebook"


# ---------------------------------------------------------------------------
# The cause — never engine_error, and never the tool's own words misread
# ---------------------------------------------------------------------------


class _NodeError:
    def __init__(self, code: str, message: str) -> None:
        self.code = code
        self.message = message


class _NodeFailure(Exception):
    """Stand-in for matrx_graph.errors.NodeFailureError's shape."""

    def __init__(self, node_id: str, node_error: _NodeError) -> None:
        super().__init__(f"Node '{node_id}' failed: {node_error.code}: {node_error.message}")
        self.node_id = node_id
        self.node_error = node_error


def _node_failure() -> _NodeFailure:
    result = normalize_completed_result(_completed(_stalled_metadata()))
    error = result.error
    assert error is not None
    return _NodeFailure("n_check", _NodeError(error.code, error.message))


def test_cause_is_tool_loop_stalled_not_engine_error() -> None:
    failure = failure_from_exception(
        _node_failure(),
        step_id="n_check",
        step_label="Check it against the live Rulebook",
    )
    assert failure.cause == Cause.TOOL_LOOP_STALLED
    assert failure.cause != Cause.ENGINE_ERROR
    assert "stopped partway through" not in failure.message
    assert "rulebook" in failure.message


def test_a_tools_own_words_never_outrank_the_machine_word() -> None:
    """The bounded tool error is arbitrary English and must not classify the run.

    A ``rulebook`` loop whose tool says "that Rulebook does not exist" would
    classify NOT_FOUND off the prose ladder and tell a person something was
    deleted.
    """
    history = [
        ToolCallUsage(
            iteration=1,
            tool_calls_count=11,
            tool_calls_details=[
                {
                    "name": "rulebook",
                    "success": False,
                    "error": {"message": "That Rulebook does not exist (or was deleted)."},
                }
                for _ in range(11)
            ],
        )
    ]
    meta = {"status": "paused_loop_guard"}
    meta.update(_loop_guard_meta(health=None, evidence=loop_guard_evidence(history)))
    result = normalize_completed_result(_completed(meta))
    error = result.error
    assert error is not None
    failure = failure_from_exception(
        _NodeFailure("n_check", _NodeError(error.code, error.message)),
        step_id="n_check",
    )
    assert failure.cause == Cause.TOOL_LOOP_STALLED


def test_max_iterations_without_tool_failures_still_explains_itself() -> None:
    meta = {"status": "max_iterations_exceeded"}
    meta.update(
        _loop_guard_meta(
            status="max_iterations_exceeded",
            health={"reason": "hit the iteration ceiling (40)"},
            evidence={"failed_calls": 0, "total_calls": 12, "tools": []},
        )
    )
    with pytest.raises(AiTurnFailedError) as exc:
        normalize_completed(_completed(meta))
    msg = str(exc.value)
    assert "no error detail recorded" not in msg
    assert "iteration ceiling" in msg
    assert "Raise the ceiling" in msg
