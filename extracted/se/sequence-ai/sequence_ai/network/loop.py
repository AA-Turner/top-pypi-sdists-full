# SPDX-FileCopyrightText: Copyright (c) 2026 General Sequences Company
# SPDX-License-Identifier: Apache-2.0
"""
A robot's control loop that plays each answer's steps while it asks for the next one, for any policy it reaches with
observe() and act(): a Link (sequence_ai.network.connect) or a policy sequence_ai.connect returns.

    from sequence_ai.network import connect, play

    with connect("http://your-gpu:8000") as policy:
        play(policy, read=read_observation, step=robot.step, hz=15, replan_at=8)

`read()` returns the robot's observation now; `step(action)` moves the robot by one of an answer's steps; `hz` is how
many steps it plays a second; `replan_at` is how many steps after an act was sent the next act is sent. Optional:
`valid_steps`, how many of an answer's steps may be played (all of them when not given); `done()`, checked after each
step, to stop; `steps_of(answer)`, the answer's steps (by default the answer itself when it is a list or an array, or the
only array or list in a dict, or its "actions"). It returns how many steps it played.

In one sentence: an act is sent on a thread of its own (a connection takes one act at a time) → its answer's steps play
at `hz`, counted from when that act was sent → `replan_at` steps after it was sent the next act is sent, and the steps
go on playing while it comes → the next answer is switched to as soon as it is in, at the step the robot has reached
since its act was sent, so no step plays twice → when the valid steps run out first, the robot waits for it.

WHY counted from the send: an answer's steps are what the policy wants from the moment it read the observation; by the
time the answer arrives the robot has moved on, and its first steps are behind it.
WHY sleep until each step's tick, not for 1 / hz: a fixed sleep adds what each step's own work takes, and the robot
plays slower and slower.
WHY the policy's wait_until_ready() first, where it has one: the first act of a server that compiles its model on its
first inference takes tens of seconds, which the robot waits out before it moves, not in the middle of a motion.
"""
from __future__ import annotations

import time
from concurrent.futures import Future, ThreadPoolExecutor
from typing import Any, Callable, Optional, Sequence

__all__ = ["play", "steps"]


def steps(answer: Any) -> Sequence:
    """An answer's steps: the answer itself when it is a list, a tuple or an array of them; in a dict, the only list or
    array it holds, else its "actions". ValueError for anything else: say which with play()'s `steps_of`."""
    if isinstance(answer, (list, tuple)) or hasattr(answer, "__array_interface__"):
        return answer
    if isinstance(answer, dict):
        held = [v for v in answer.values() if isinstance(v, (list, tuple)) or hasattr(v, "__array_interface__")]
        if len(held) == 1:
            return held[0]
        if "actions" in answer:
            return answer["actions"]
    raise ValueError("cannot tell which of the answer's values are its steps: pass steps_of=, a function that returns "
                     "them from an answer")


def play(policy: Any, *, read: Callable[[], Any], step: Callable[[Any], Any], hz: float, replan_at: int,
         valid_steps: Optional[int] = None, done: Optional[Callable[[], bool]] = None,
         steps_of: Callable[[Any], Sequence] = steps, ready: bool = True,
         clock: Callable[[], float] = time.monotonic, sleep: Callable[[float], Any] = time.sleep) -> int:
    """Play the policy's answers on the robot, asking for each next one while the last plays (the module's docstring).
    Returns how many steps were played. An error of an act - or of `read` on its thread - is raised here, once the act
    that met it is waited for; so is one of `step` or `done`. Before it returns, an act still in flight is waited for, so
    the caller may close the connection next. `ready`: call the policy's wait_until_ready() first, where it has one."""
    if hz <= 0:
        raise ValueError(f"hz must be positive, got {hz}")
    if replan_at < 0:
        raise ValueError(f"replan_at must be 0 or more, got {replan_at}")
    if ready and callable(getattr(policy, "wait_until_ready", None)):
        policy.wait_until_ready()

    def ask() -> Sequence:
        policy.observe(read())
        rows = steps_of(policy.act())
        return rows[:valid_steps] if valid_steps is not None else rows

    played = 0
    with ThreadPoolExecutor(max_workers=1, thread_name_prefix="sequence-ai-play") as pool:
        ahead: Optional[Future] = pool.submit(ask)
        since = 0                                       # steps played since the act `ahead` was sent
        while True:
            if done is not None and done():
                return played
            rows, i = ahead.result(), since             # the robot is at step `since` of this answer
            ahead, t0 = None, clock() - i / hz
            while i < len(rows):
                if ahead is None and i >= replan_at:    # `replan_at` steps since its act was sent: ask again
                    ahead, since = pool.submit(ask), 0
                step(rows[i])
                played, i, since = played + 1, i + 1, since + 1
                if done is not None and done():
                    return played                       # the pool's exit waits for an act in flight
                sleep(max(0.0, t0 + i / hz - clock()))  # to the next step's tick
                if ahead is not None and ahead.done():  # the next answer is in: switch to it
                    break
            if ahead is None:                           # its steps ran out by the replan step: ask now, the robot waits
                ahead, since = pool.submit(ask), 0
