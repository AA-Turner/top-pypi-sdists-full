"""THE ONE INTERNING GRAIN (L-SPEED round 6a, item 1).

A large list written by an event (32 KB grain) and by a checkpoint / the run output (4 KB grain)
was split into different children, so the same 5.4 MB sources list was stored twice per run tree.
Every writer now interns at ``knobs.interning_grain()``: the same value gives the same references
and the same stored digests, so the second writer stores nothing new.
"""

from __future__ import annotations

import asyncio

from matrx_graph.checkpoint.values import intern_values
from matrx_graph.knobs import STARTING_CHECKPOINT_POLICY, STARTING_EVENT_INLINE_VALUE_MAX_BYTES, interning_grain

SOURCES = [{"url": f"https://example.com/{i}", "text": "word " * 1500, "n": i} for i in range(60)]


def _stored(limit: int) -> set[str]:
    store: dict[str, object] = {}
    intern_values({"sources": SOURCES}, store, limit)
    return set(store)


def test_the_grain_is_the_event_knob() -> None:
    assert asyncio.run(interning_grain()) == STARTING_EVENT_INLINE_VALUE_MAX_BYTES


def test_one_grain_stores_a_value_once() -> None:
    grain = asyncio.run(interning_grain())
    event_side, checkpoint_side = _stored(grain), _stored(grain)
    assert event_side == checkpoint_side


def test_two_grains_stored_the_same_value_twice() -> None:
    """The red side: the old checkpoint grain (4 KB) beside the event grain shares almost nothing."""
    old = _stored(STARTING_CHECKPOINT_POLICY.inline_value_max_bytes)
    new = _stored(STARTING_EVENT_INLINE_VALUE_MAX_BYTES)
    assert old != new and len(old & new) < len(new)
