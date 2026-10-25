"""A spend-guard stop reads as its own plain reason, never "AI turn ended with status 'failed' (...)".

Live run 246ffb53 (2026-10-24): the build page said "AI turn ended with status 'failed' (automation_guardrail):
Stopped: limit — this run ...". The prefix is built once, in ``normalize_completed``, for every AI graph node, so
the fix is there: a CALLER REFUSAL (``providers/caller_refusal``: the spend guardrail, a spend approval, a usage
limit) gives the person the gate's own sentence, on both doors a node can take (the returned ``Failure`` and the
raised error the scheduler reads). The technical text keeps the prefix and the code: the database repeat counter
(``scheduler.automation_repeat_runs_24h``) finds ``(run_approval_required)`` in the stored error.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from matrx_ai.graph_nodes.shared import (
    AiTurnFailedError,
    normalize_completed,
    normalize_completed_result,
)

GUARD = "Stopped: limit — this run reached its budget. The output so far is kept; raise Max cost per run if the task needs more."
APPROVAL = "This agent is waiting for an administrator to approve its spending, so it was not run."


def _completed(error_type: str, error: str) -> SimpleNamespace:
    return SimpleNamespace(
        metadata={"status": "failed", "error_type": error_type, "error": error},
        total_usage=None,
        request=SimpleNamespace(conversation_id="c", request_id="r"),
    )


@pytest.mark.parametrize(("error_type", "reason"), [("automation_guardrail", GUARD), ("run_approval_required", APPROVAL)])
def test_a_spend_stop_is_its_own_plain_reason(error_type: str, reason: str) -> None:
    result = normalize_completed_result(_completed(error_type, reason))
    error = result.error
    assert error.message == reason
    assert "AI turn ended" not in error.message
    assert error.technical is not None and f"({error_type})" in error.technical and reason in error.technical


def test_the_raised_door_carries_the_same_plain_reason() -> None:
    from matrx_graph.failure import failure_from_exception

    with pytest.raises(AiTurnFailedError) as caught:
        normalize_completed(_completed("automation_guardrail", GUARD))
    built = failure_from_exception(caught.value)
    assert built.message == GUARD
    assert "(automation_guardrail)" in (built.technical or "")


def test_an_engine_failure_keeps_its_full_text() -> None:
    result = normalize_completed_result(_completed("engine_error", "boom"))
    assert result.error.message == "AI turn ended with status 'failed' (engine_error): boom"
