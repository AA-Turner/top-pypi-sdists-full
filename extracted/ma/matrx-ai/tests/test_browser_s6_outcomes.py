"""S6 typed-outcome builders — the additive tool payloads a producer emits."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest

from matrx_ai.browser_handoff import (
    HandoffReason,
    PageFacts,
    PageInventory,
    human_required_output,
    new_error,
    ok_identity,
    page_inventory_payload,
    reopened_for_handoff_output,
)


def test_ok_identity_additive_on_persistent_run():
    out = ok_identity(run_id="run-1", profile_id="prof-1")
    assert out == {"status": "ok", "run_id": "run-1", "profile_id": "prof-1"}


def test_ok_identity_transient_omits_run_and_profile():
    # The backwards-compatibility anchor: a legacy transient call gets no
    # run_id/profile_id keys (S6 §4.1 #3).
    out = ok_identity(run_id=None, profile_id=None)
    assert out == {"status": "ok"}
    assert "run_id" not in out and "profile_id" not in out


def test_human_required_is_a_success_with_embedded_success_true():
    out = human_required_output(
        reason=HandoffReason.MFA_REQUIRED,
        handoff_id="h1",
        run_id="run-1",
        profile_id="prof-1",
        url="https://accounts.example.com/challenge",
        title="Verify",
        message="A person needs to complete a step.",
    )
    assert out["status"] == "human_required"
    assert out["success"] is True  # else the executor flips it to a failure
    assert out["continuation_required"] is True
    assert out["session_id"] == out["run_id"] == "run-1"
    assert out["reason"] == "mfa_required"


def test_human_required_passes_reason_through_untouched():
    # An unknown reason string is passed through, never validated locally (S6 §5.2).
    out = human_required_output(
        reason="some_future_reason", handoff_id="h1", run_id="r", profile_id="p",
        message="x",
    )
    assert out["reason"] == "some_future_reason"


def test_reopened_volatile_state_preserved_is_constant_false():
    out = reopened_for_handoff_output(
        reason=HandoffReason.MFA_REQUIRED, handoff_id="h1", new_run_id="run-2",
        previous_run_id="run-1", profile_id="prof-1", message="Reopened.",
    )
    assert out["volatile_state_preserved"] is False  # always literally False
    assert out["session_id"] == "run-2" and out["previous_run_id"] == "run-1"
    assert "in_page_javascript_state" in out["not_preserved"]


@pytest.mark.parametrize(
    "error_type",
    ["browser_controlled_by_human", "profile_access_denied", "profile_not_found",
     "stale_run", "profile_busy"],
)
def test_new_errors_are_non_retryable(error_type):
    # A retryable conflict is how a tool loop burns a paid turn every second while
    # a human types a password (S6 §5.3).
    err = new_error(error_type, message="nope")
    assert err.is_retryable is False
    assert err.suggested_action


def test_new_error_rejects_uncatalogued_type():
    with pytest.raises(ValueError):
        new_error("made_up_type", message="x")


def _inv(n_pages: int, active="p0") -> PageInventory:
    return PageInventory(
        context_count=1,
        pages=[
            PageFacts(page_id=f"p{i}", origin="https://x.test", url=f"https://x.test/{i}",
                      title=f"Page {i}", is_active=(f"p{i}" == active))
            for i in range(n_pages)
        ],
        active_page_id=active,
        captured_at=datetime(2026, 1, 1, tzinfo=UTC),
    )


def test_page_inventory_self_capped_and_projected():
    payload, self_capped = page_inventory_payload(_inv(2))
    assert self_capped is True
    assert payload["pages_total"] == 2 and payload["pages_truncated"] is False
    # Rows are projected to exactly page_id/url/title/active — no DOM, no text.
    assert set(payload["pages"][0]) == {"page_id", "url", "title", "active"}


def test_page_inventory_truncates_but_keeps_active_page():
    # 40 pages, the active one is the LAST — truncation to 25 must still include it.
    payload, _ = page_inventory_payload(_inv(40, active="p39"))
    assert payload["pages_total"] == 40
    assert payload["pages_shown"] == 25
    assert payload["pages_truncated"] is True
    assert any(row["active"] for row in payload["pages"])
