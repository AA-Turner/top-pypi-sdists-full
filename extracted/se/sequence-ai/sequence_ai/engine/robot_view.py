# SPDX-FileCopyrightText: Copyright (c) 2026 General Sequences Company
# SPDX-License-Identifier: Apache-2.0
"""
What a policy's @seq.plan is handed: `robot`, one robot as its server holds it the moment the plan is called - a
deployment's worker and a policy server of your own alike, this one module in both.

In one sentence: its clock comes due (engine.plan_clock) → its plan is called, off the act's thread, with a read-only
view of its episode's state (view): the keys the policy keeps there as they are, and the server's three
(record.OBSERVATIONS, ACTIONS, PLANS) as tuples, oldest first, the newest observation decoded as its act function gets
it → what the plan returns goes to its episode's plans, where its act function reads it.

WHY a view and not the live Episode: its act writes that state on another thread while the plan reads it, and an act
function's `seq.observations` is {step: observation} - `[-1]` there is a KeyError. The older observations stay as they
came (a video's frames are decoded in order, on the act's path); a key a robot said is readable in them all.
"""
from __future__ import annotations

from types import MappingProxyType
from typing import Any

from . import record

__all__ = ["Robot", "view"]


class Robot:
    """One robot, as its @seq.plan reads it: `id`, its episode's; `state`, what its episode's state holds (view)."""

    __slots__ = ("id", "state")

    def __init__(self, robot_id: str, state: Any) -> None:
        self.id = robot_id
        self.state = state

    def __repr__(self) -> str:
        return f"Robot({self.id!r})"


def _oldest_first(kept: Any) -> list:
    """A {step: value} record's values, oldest first (list(): the act's thread writes it as this reads)."""
    return [value for _, value in sorted(list(kept.items()), key=lambda item: item[0])] if kept else []


def view(episode: Any, latest: Any = None) -> Robot:
    """The robot of `episode` now: `latest`, its newest observation as its act function gets it, in place of that
    observation as it came."""
    state = dict(list(episode.state.items()))
    seen = _oldest_first(state.get(record.OBSERVATIONS))
    if latest is not None:
        seen[-1:] = [latest]
    state[record.OBSERVATIONS] = tuple(seen)
    state[record.ACTIONS] = tuple(_oldest_first(state.get(record.ACTIONS)))
    state[record.PLANS] = tuple(state.get(record.PLANS) or ())
    return Robot(episode.id, MappingProxyType(state))
