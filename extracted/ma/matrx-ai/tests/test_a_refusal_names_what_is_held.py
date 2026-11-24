"""A refusal names WHAT is held, never "this agent" for something that is not one (L12b, 2026-11-03).

Live on chat.aimatrx.com: the walker's own $2.18 Deep Research run held its whole sign-in session (subject
``coding_session``, the login's JWT session id), and every later run in that login was refused — a one-word Test
Reply included — with "This agent's first run cost more than its approval limit". The Test Reply agent never ran over
anything. The sentence was keyed on the hold's REASON only. Red proof: before this, every subject kind read "This
agent…".
"""

from __future__ import annotations

import pytest

from matrx_ai.providers.run_approval_gate import REFUSAL_SENTENCES, RunApprovalRequiredError


def _refusal(kind: str, reason: str, status: str = "waiting") -> RunApprovalRequiredError:
    return RunApprovalRequiredError(
        approval_id="a1", subject_kind=kind, subject_id="s1", status=status, approval_url="https://x/a1", reason=reason
    )


@pytest.mark.parametrize("reason", ["volume", "over_threshold", "expired", "declined", "waiting"])
def test_a_held_sign_in_session_says_so_and_never_blames_an_agent(reason: str) -> None:
    message = _refusal("coding_session", reason, "rejected" if reason == "declined" else "waiting").message
    assert "sign-in session" in message
    assert "agent" not in message.lower()


@pytest.mark.parametrize(
    ("kind", "noun"),
    [("workflow", "automation"), ("workflow_trigger", "automation"), ("sch_task", "scheduled task"), ("agent_schedule", "scheduled task")],
)
def test_an_automation_or_schedule_is_named_as_itself(kind: str, noun: str) -> None:
    message = _refusal(kind, "over_threshold").message
    assert noun in message
    assert "This agent" not in message


@pytest.mark.parametrize("kind", ["agent", "mandate", "agent_factory", "unknown_kind"])
def test_an_agent_keeps_its_sentence(kind: str) -> None:
    for reason, sentence in REFUSAL_SENTENCES.items():
        status = "rejected" if reason == "declined" else "waiting"
        assert _refusal(kind, reason, status).message == sentence
