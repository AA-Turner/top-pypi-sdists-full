"""Experimental: test-time smoothing as Flash ALOHA describes it, a sigmoid crossfade of two plans.

"Flash ALOHA: Learning Fast and Precise Manipulation" (Yao, Wu, Gao, Finn, Fu; section IV,
Fig. 5): over the ``H`` steps an earlier chunk ``q1`` and a later chunk ``q2`` both cover, the
command is

    a(t') = (1 - w(t')) q1(t') + w(t') q2(t'),    w(t') = sigmoid((t' - t0 - H / 2) / sigma)

where ``t0`` is the first step of the overlap. Outside it, each chunk plays as predicted. ``H``
(the window) and ``sigma`` (the time scale, in action steps) set how late and how sharply the
robot turns to the newer chunk. The paper publishes neither value.

How it sits in this runtime:

- **The earlier chunk is the plan in the buffer.** Under frequent replanning that plan is itself
  a crossfade of older chunks, and the rows a robot executes are the early rows of each window,
  where the weight is still low: a change of plan takes most of a window to reach the robot.
- **The window starts at the first step still due** when the chunk is merged. It is at most
  ``window`` steps and at most the steps both plans cover. Where the old plan runs further than
  the window, the new chunk plays as answered after it.
- **The paper's action lookahead** (skip the first n actions of a chunk) is the buffer's own
  alignment: rows whose step has passed are dropped before the crossfade.
- **With no window given, it is 0.4 s of actions** at the run's rate (12 steps at 30 Hz), the
  setting that did best where this mode helped (below).
- **With no time scale given, sigma is an eighth of the window used**, so the weight starts at
  about 2% new and a crossfade over a short overlap still completes. A given time scale is used
  as it is.

Every command lies between the two plans' targets for its step, so the crossfade never overshoots
either of them and normalized grippers stay in range. It does not look at the executed commands:
a chunk that arrives with no plan left to cross from (the first of a run, or after an underrun)
plays as the model answered.

What it measured against the stock ``output`` blend (dev, 2026-11-13, paired starts): better on
absolute joint targets replanned every few steps (ABC-VLA on ABC's simulator, RTC off: 54 of 60
worlds against 41 with a 12-step window, 47 with a 4-step one), worse on relative end-effector
actions replanned once per half chunk (five LIBERO models: 88.2% against 90.8% with a 3-4 step
window, 83.8% with the whole overlap). It is opt-in for that reason: ``auto`` never picks it.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from math import exp, isfinite
from numbers import Integral, Real

from .action_smoothing import (
    Action,
    SmoothingResolution,
    _max_abs_difference,
    _validated_inputs,
    validate_normalized_grippers,
)

# sigma = window / SIGMA_PER_WINDOW when none is given: sigmoid(-4) = 1.8% new on the first step.
SIGMA_PER_WINDOW = 8.0


def crossfade_weight(position: int, window: int, time_scale: float) -> float:
    """The newer chunk's weight ``position`` steps into a ``window``-step overlap."""
    x = (position - window / 2.0) / time_scale
    # exp(-x) overflows for a very small time scale; the weight there is 0 or 1.
    if x <= -700.0:
        return 0.0
    return 1.0 / (1.0 + exp(-x))


def resolve_crossfade(
    *,
    next_action_step: int,
    action_steps: Sequence[int],
    new_actions: Sequence[Sequence[float]],
    existing_actions: Mapping[int, Sequence[float]],
    window: int,
    time_scale: float | None = None,
    normalized_gripper_indices: tuple[int, ...] = (),
) -> SmoothingResolution:
    """The rows of ``new_actions`` from ``next_action_step`` on, crossed over from the plan in
    ``existing_actions`` during the first ``window`` steps both cover."""
    if isinstance(window, bool) or not isinstance(window, Integral) or window < 1:
        raise ValueError("crossfade window must be a positive integer")
    if time_scale is not None and (
        isinstance(time_scale, bool)
        or not isinstance(time_scale, Real)
        or not isfinite(time_scale)
        or time_scale <= 0
    ):
        raise ValueError("crossfade time scale must be finite and positive")
    steps, newest, existing, _ = _validated_inputs(
        action_steps=action_steps,
        new_actions=new_actions,
        existing_actions=existing_actions,
        executed_history=(),
    )
    for values in (*newest, *existing.values()):
        validate_normalized_grippers(values, normalized_gripper_indices)
    first = int(next_action_step)
    executable = [
        (offset, step, newest[offset]) for offset, step in enumerate(steps) if step >= first
    ]
    shared = [step for _, step, _ in executable if step in existing]
    if not shared:
        return SmoothingResolution(
            actions={step: action for _, step, action in executable},
            overlap_steps=0,
            max_abs_position_revision=0.0,
            first_executable_source_offset=executable[0][0] if executable else None,
            transition_steps=0,
        )
    start = shared[0]
    used = min(int(window), shared[-1] - start + 1)
    sigma = float(time_scale) if time_scale is not None else used / SIGMA_PER_WINDOW
    resolved: dict[int, Action] = {}
    revision = 0.0
    for _, step, new_action in executable:
        old_action = existing.get(step)
        if old_action is None or step - start >= used:
            action = new_action
        else:
            weight = crossfade_weight(step - start, used, sigma)
            action = tuple(
                (1.0 - weight) * old + weight * new
                for old, new in zip(old_action, new_action, strict=True)
            )
        if old_action is not None:
            revision = max(revision, _max_abs_difference(old_action, action))
        resolved[step] = action
    return SmoothingResolution(
        actions=resolved,
        overlap_steps=len(shared),
        max_abs_position_revision=revision,
        first_executable_source_offset=executable[0][0],
        transition_steps=used,
        time_scale=sigma,
    )
