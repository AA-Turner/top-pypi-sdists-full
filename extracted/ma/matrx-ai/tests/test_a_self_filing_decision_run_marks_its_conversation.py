"""A run whose lane files its own decision items marks its conversation row.

``metadata.decision_items_owner`` on the run's context is copied onto its conversation row, where
``platform.capture_message_decision_items`` reads it and skips the conversation — so Search Decide
(any mandate on its provision) and decision-review reference runs are never filed twice.
"""

from __future__ import annotations

from types import SimpleNamespace

from matrx_ai.db.conversation_gate import DECISION_ITEMS_OWNER_KEY, _with_mandate_attribution


def test_the_marker_rides_onto_the_conversation_with_or_without_a_mandate() -> None:
    with_key = SimpleNamespace(metadata={"mandate_key": "acme.custom_result", DECISION_ITEMS_OWNER_KEY: "search_decide"})
    assert _with_mandate_attribution({}, with_key)[DECISION_ITEMS_OWNER_KEY] == "search_decide"
    no_key = SimpleNamespace(metadata={DECISION_ITEMS_OWNER_KEY: "decision_review.reference_run"})
    assert _with_mandate_attribution({}, no_key) == {DECISION_ITEMS_OWNER_KEY: "decision_review.reference_run"}


def test_an_ordinary_run_carries_no_marker() -> None:
    assert DECISION_ITEMS_OWNER_KEY not in _with_mandate_attribution({}, SimpleNamespace(metadata={"mandate_key": "x.y"}))
