"""A paced For each stops sending once one item's spend approval is pending (2026-11-12).

The code path stops launching new paid work after the first hold. The workflow kept admitting the next
waves, and each item became another held hole waiting on the same approval. Now a settled ``held`` item
stops the dispatch: every item not yet admitted gets ``UNTIL`` and settles as not sent, naming why;
items already admitted finish.

Red before: after item 0 settled ``held``, item 1 was admitted into the next wave.
"""

from __future__ import annotations

import asyncio

from matrx_graph.executor.paced_dispatch import ADMIT, UNTIL, PacedDispatch


async def _never_stop(_waited: bool) -> bool:
    return False


async def test_a_held_item_stops_every_item_not_yet_admitted() -> None:
    pace = PacedDispatch("call", {"wave_size": "1", "total": 3})
    for i in range(3):
        pace.register(i)
    assert await pace.admit(0, _never_stop) == ADMIT
    pace.start(0)
    pace.settle(0, "held", None)
    assert await asyncio.wait_for(pace.admit(1, _never_stop), timeout=2) == UNTIL
    assert await asyncio.wait_for(pace.admit(2, _never_stop), timeout=2) == UNTIL
    assert pace.reason == "not sent: a spend approval is pending after 1 item(s)"


async def test_an_admitted_item_still_finishes_after_a_hold() -> None:
    pace = PacedDispatch("call", {"wave_size": "2", "total": 3})
    for i in range(3):
        pace.register(i)
    assert await pace.admit(0, _never_stop) == ADMIT
    assert await pace.admit(1, _never_stop) == ADMIT
    pace.settle(0, "held", None)
    pace.settle(1, "succeeded", {"v": 1})  # already admitted: it finishes and its result is kept
    assert pace._inputs()["results"] == [{"v": 1}]
    assert await asyncio.wait_for(pace.admit(2, _never_stop), timeout=2) == UNTIL


async def test_a_plain_success_does_not_stop_the_dispatch() -> None:
    pace = PacedDispatch("call", {"wave_size": "1", "total": 2})
    for i in range(2):
        pace.register(i)
    assert await pace.admit(0, _never_stop) == ADMIT
    pace.settle(0, "succeeded", {"v": 1})
    assert await asyncio.wait_for(pace.admit(1, _never_stop), timeout=2) == ADMIT
