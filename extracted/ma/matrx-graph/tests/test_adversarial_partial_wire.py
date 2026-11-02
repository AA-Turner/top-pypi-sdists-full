"""Adversarial review (round 2, wire/rendering) — the partial event's
self-description (``matrx_graph/content_ir/partial.py``) — 2026-08-21.

Contract §3.1 (STREAMING_PARTIAL_KINDS.md): a partial's ``value`` "is always
valid JSON, always self-describing (``__kind``)" — the producer stamps the
detection guess so the payload and the announcement agree.

W1 — the stamp LOSES to hostile/echoed model output. ``partial_kind_event``
builds ``payload = {KIND_KEY: kind, **value}``, so a streamed document that
itself contains a ``__kind`` key (a model echoing an example, or naming a
different kind than the fence was detected as) OVERRIDES the stamp: the event
announces ``root.kind = "quiz_set"`` while the value says ``__kind:
"decision_tree"``. The frontend's partial route resolves the component by
``root.kind`` — but every in-band-first reader ("in-band ``__kind`` wins", the
law the workflow-run reducer and ``DelegatedOutput`` follow) routes the SAME
value to a different component. One event, two designated renderers, and which
one the user sees depends on which reader got there first.

Fix: the stamp wins — ``{**value, KIND_KEY: kind}`` — so the announcement and
the payload can never disagree. xfail(strict): an XPASS means it was fixed;
delete the marker so the test guards it.
"""

from __future__ import annotations

import pytest
from matrx_graph.content_ir.partial import partial_kind_event


def _event(value: dict) -> dict:
    return partial_kind_event(
        kind="quiz_set",
        value=value,
        seq=1,
        source_text='{"quiz_title": "x"}',
        discriminator={"format": "fence", "language": "json"},
    )


def test_the_stamp_is_present_when_the_value_carries_no_kind() -> None:
    """ATTACKED AND HELD: the ordinary case is stamped correctly."""
    event = _event({"quiz_title": "x"})
    assert event["root"]["value"]["__kind"] == "quiz_set"
    assert event["root"]["kind"] == "quiz_set"


# FIXED (round-2 triage, 2026-08-21): the finding this test pinned is
# closed; the test now guards the fix.
def test_a_value_carrying_its_own_kind_cannot_override_the_stamp() -> None:
    event = _event({"__kind": "decision_tree", "quiz_title": "x"})
    assert event["root"]["value"]["__kind"] == event["root"]["kind"], (
        "the event announces one kind and its value declares another — "
        "two readers, two renderers, one region"
    )
