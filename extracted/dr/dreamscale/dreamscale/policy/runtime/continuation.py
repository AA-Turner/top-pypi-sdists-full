"""Joining a new chunk to the motion a robot is executing, on the robot (DSL-424).

A chunk that arrives while the robot runs the previous one starts with rows that are already
due: the robot executed the old plan for them. Runway's real-time server joins the two by a rule
(``praxis/serve/rtc.py`` at the pinned commit: rebase into the prefix, fade the velocity, carry
the grip over), but it must guess on the server how many rows the robot will run before the
answer lands (the longest of its last five call times). The robot knows: the join is done here,
at the row actually due when the chunk is merged, with the same rule in joint space:

- **Offset.** The new chunk's row for the last executed step is compared with the command the
  robot actually executed there; the difference is added to the new rows from the first due
  row on and handed back to zero over ``decay`` rows (cosine ramp). The robot continues from
  where it is commanded, and ends up on the new plan.
- **Velocity.** Over the first ``vel_fade`` rows the step size fades from the robot's last
  executed step to the new plan's, so the seam turns instead of switching direction; the
  position this builds goes back to zero over the rest of ``decay``.
- **Grippers.** They fade from the old plan's own grip at the same steps (its last grip once it
  ran out) to the new plan's over ``grip_rows`` rows, so a grasp is not let go of or snapped
  shut by a seam.

The rule never changes a row of the plan the robot already executed, puts no measured pose into
the output (the joins don't feed back into an oscillation), and the very first chunk of a run
plays exactly as the model answered. Its defaults are Runway's own for their robot runs.
"""

from __future__ import annotations

import math
from collections.abc import Mapping, Sequence
from dataclasses import dataclass

Action = tuple[float, ...]

DECAY_ROWS = 24
VEL_FADE_ROWS = 6
GRIP_ROWS = 16


def ramp(i: int, steps: int) -> float:
    """``(1 - cos(pi (i + 1) / (steps + 1))) / 2``: rises from near 0 to near 1 over ``steps``."""
    return 0.5 * (1.0 - math.cos(math.pi * (i + 1) / (steps + 1)))


@dataclass(frozen=True)
class Continuation:
    actions: dict[int, Action]
    overlap_steps: int
    max_abs_position_revision: float
    first_executable_source_offset: int | None
    # The largest joint offset the rule handed back at the seam (the jump a plain switch makes).
    junction_offset: float = 0.0


def continue_motion(
    *,
    next_action_step: int,
    action_steps: Sequence[int],
    new_actions: Sequence[Sequence[float]],
    existing_actions: Mapping[int, Sequence[float]],
    executed_history: Sequence[Sequence[float]],
    gripper_indices: Sequence[int],
    normalized_gripper_indices: Sequence[int] = (),
    decay: int = DECAY_ROWS,
    vel_fade: int = VEL_FADE_ROWS,
    grip_rows: int = GRIP_ROWS,
) -> Continuation:
    """The rows of ``new_actions`` from the first due step (``next_action_step``) on, joined to
    the executed commands ``executed_history`` (oldest first; its last at the step before)."""
    first = int(next_action_step)
    steps = [int(step) for step in action_steps]
    new = [tuple(float(v) for v in row) for row in new_actions]
    if len(steps) != len(new):
        raise ValueError("action_steps and new_actions must have the same length")
    executable = [offset for offset, step in enumerate(steps) if step >= first]
    if not executable:
        return Continuation({}, 0, 0.0, None)
    p = executable[0]
    old = {int(step): tuple(float(v) for v in row) for step, row in existing_actions.items()}
    overlap = sum(1 for offset in executable if steps[offset] in old)
    history = [tuple(float(v) for v in row) for row in executed_history]
    if not history:
        # Nothing executed yet: the first chunk plays as the model answered.
        return Continuation({steps[o]: new[o] for o in executable}, overlap, 0.0, p)
    width = len(new[0])
    grips = set(int(i) for i in gripper_indices)
    joints = [i for i in range(width) if i not in grips]
    last = history[-1]
    if p >= 1:
        reference = new[p - 1]
    elif len(new) >= 2:
        # The chunk starts at the due step: its row before is extrapolated back one step.
        reference = tuple(2.0 * a - b for a, b in zip(new[0], new[1], strict=True))
    else:
        reference = new[0]
    offset = [last[j] - reference[j] for j in range(width)]
    v_end = ([history[-1][j] - history[-2][j] for j in range(width)]
             if len(history) >= 2 else [0.0] * width)
    rows = [new[o] for o in executable]
    out = [list(row) for row in rows]
    # Offset rebase on the joints, handed back over `decay` rows.
    for i in range(len(rows)):
        w = 1.0 if decay <= 0 else (1.0 - ramp(i, decay) if i < decay else 0.0)
        for j in joints:
            out[i][j] = rows[i][j] + w * offset[j]
    # Velocity fade from the last executed step to the rebased plan's, then back to the plan.
    if vel_fade > 0 and len(history) >= 2:
        base = [list(row) for row in out]
        back = max(decay - vel_fade, 1)
        acc = [0.0] * width
        for i in range(len(base)):
            if i < vel_fade:
                fade = 1.0 - ramp(i, vel_fade)
                for j in joints:
                    step = base[i][j] - (base[i - 1][j] if i else last[j])
                    acc[j] += fade * (v_end[j] - step)
                    out[i][j] = base[i][j] + acc[j]
                continue
            k = i - vel_fade
            w = 1.0 if decay <= 0 else (1.0 - ramp(k, back) if k < back else 0.0)
            for j in joints:
                out[i][j] = base[i][j] + w * acc[j]
    # Grippers: from the old plan's grip at each step (its last executed one when it ran out).
    for i, offset_index in enumerate(executable):
        if i >= grip_rows:
            break
        old_row = old.get(steps[offset_index])
        for g in grips:
            held = (old_row if old_row is not None else last)[g]
            out[i][g] = held + ramp(i, grip_rows) * (rows[i][g] - held)
    for row in out:
        for g in normalized_gripper_indices:
            row[g] = min(1.0, max(0.0, row[g]))
    actions = {steps[o]: tuple(row) for o, row in zip(executable, out, strict=True)}
    revision = max(
        (abs(old[step][j] - actions[step][j]) for step in actions if step in old
         for j in range(width)),
        default=0.0,
    )
    junction = max((abs(offset[j]) for j in joints), default=0.0)
    return Continuation(actions, overlap, revision, p, junction)
