"""Experimental YAM handovers in joint radians; never a driver safety limiter."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import replace
from math import hypot, isfinite, sqrt

from .action_smoothing import (
    ResolvedActionSmoothing,
    SmoothingResolution,
    _as_action,
    _max_abs_difference,
    _validated_inputs,
    resolve_motion_smoothing,
    validate_normalized_grippers,
)


def resolve_adaptive_smoothing(
    *,
    next_action_step: int,
    action_steps: Sequence[int],
    new_actions: Sequence[Sequence[float]],
    existing_actions: Mapping[int, Sequence[float]],
    executed_history: Sequence[Sequence[float]],
    smoothing: ResolvedActionSmoothing,
) -> SmoothingResolution:
    steps, newest, existing, history = _validated_inputs(
        action_steps=action_steps,
        new_actions=new_actions,
        existing_actions=existing_actions,
        executed_history=executed_history,
    )
    groups, grippers = smoothing.joint_groups, smoothing.gripper_indices
    joints = tuple(index for group in groups for index in group)
    dimension = len(joints) + len(grippers)
    if not groups or set((*joints, *grippers)) != set(range(dimension)):
        raise ValueError("adaptive smoothing requires a complete joint layout")
    for action in (*newest, *existing.values(), *history):
        if len(action) != dimension:
            raise ValueError("adaptive smoothing action dimension differs from its joint layout")
        validate_normalized_grippers(action, smoothing.normalized_gripper_indices)
    if any(b != a + 1 for a, b in zip(steps, steps[1:], strict=False)):
        raise ValueError("adaptive smoothing requires contiguous action indices")
    indices = [i for i, step in enumerate(steps) if step >= next_action_step]
    if indices and steps[indices[0]] != next_action_step:
        raise ValueError("adaptive smoothing requires coverage at the next action step")
    hz, reference = smoothing.action_hz, smoothing.reference_speed
    if not all(isfinite(v) and v > 0 for v in (hz, reference)):
        raise ValueError("adaptive smoothing rate and reference speed must be finite and positive")
    limit = smoothing.correction_steps
    if limit is None or limit < 1:
        raise ValueError("adaptive smoothing requires positive correction steps")

    if smoothing.mode == "motion_speed":
        # Use only executable intra-chunk differences. Neither the stale prefix,
        # the inter-chunk offset nor gripper closure represents future arm speed.
        speeds = []
        executable = [newest[i] for i in indices]
        for arm in groups:
            deltas = [
                (right[j] - left[j]) * hz
                for left, right in zip(executable, executable[1:], strict=False)
                for j in arm
            ]
            speeds.append(hypot(*deltas) / sqrt(len(deltas)) if deltas else 0.0)
        speed = max(speeds)
        if not isfinite(speed):
            raise ValueError("derived arm speed must be finite")
        fraction = speed / (speed + reference)
        weight = 1.0 - (1.0 - smoothing.new_weight) * fraction
        gain = 1.0 - (1.0 - 1.0 / limit) * fraction
        result = resolve_motion_smoothing(
            next_action_step=next_action_step,
            action_steps=steps,
            new_actions=newest,
            existing_actions=existing,
            executed_history=history,
            new_weight=weight,
            correction_steps=limit,
            normalized_gripper_indices=smoothing.normalized_gripper_indices,
            correction_gain_override=gain,
        )
        raw = dict(zip(steps, newest, strict=True))
        actions = {
            step: tuple(raw[step][j] if j in grippers else value for j, value in enumerate(action))
            for step, action in result.actions.items()
        }
        return replace(
            result,
            actions=actions,
            max_abs_position_revision=_revision(existing, actions),
            arm_speed_rad_s=speed,
            effective_new_weight=weight,
            correction_gain=gain,
        )

    if smoothing.mode != "motion_handover":
        raise ValueError("unknown adaptive smoothing mode")
    if not indices:
        return SmoothingResolution({}, 0, 0.0, None, transition_steps=0)
    start = indices[0]
    first = newest[start]
    # The incoming predecessor is a model target, not a fabricated extrapolation.
    # Without one, use the first target as a stationary incoming anchor.
    raw_anchor = newest[start - 1] if start else first
    anchor = history[-1] if history else raw_anchor
    old_first = existing.get(next_action_step, anchor)
    offset = _as_action(tuple(anchor[j] - raw_anchor[j] for j in range(dimension)))
    velocity_offset = _as_action(
        tuple(
            ((old_first[j] - anchor[j]) - (first[j] - raw_anchor[j])) * hz for j in range(dimension)
        )
    )
    cap = min(limit, len(indices))
    transition = 1
    ratio = 0.0
    for transition in range(1, cap + 1):
        duration = transition / hz
        # Conservative analytic bounds on the Hermite correction's first and
        # second derivatives. These select a duration, not enforce robot limits.
        ratio = max(
            max(
                (1.5 * abs(offset[j]) / duration + abs(velocity_offset[j])) / reference,
                (6.0 * abs(offset[j]) / duration**2 + 4.0 * abs(velocity_offset[j]) / duration)
                / (reference * hz),
            )
            for j in joints
        )
        if ratio <= 1.0:
            break
    if not isfinite(ratio):
        raise ValueError("derived handover response must be finite")
    actions = {}
    for ordinal, source in enumerate(indices, 1):
        raw = newest[source]
        if ordinal >= transition:
            action = raw  # Exact expiry, including the final available sample.
        else:
            u = ordinal / transition
            h00 = 2 * u**3 - 3 * u**2 + 1
            h10 = u**3 - 2 * u**2 + u
            action = _as_action(
                tuple(
                    raw[j]
                    if j in grippers
                    else raw[j] + offset[j] * h00 + duration * velocity_offset[j] * h10
                    for j in range(dimension)
                )
            )
        actions[steps[source]] = action
    return SmoothingResolution(
        actions=actions,
        overlap_steps=len(actions.keys() & existing.keys()),
        max_abs_position_revision=_revision(existing, actions),
        first_executable_source_offset=start,
        transition_steps=transition,
        correction_rate_ratio=ratio,
    )


def _revision(
    existing: Mapping[int, Sequence[float]], actions: Mapping[int, Sequence[float]]
) -> float:
    return max(
        (
            _max_abs_difference(existing[step], actions[step])
            for step in existing.keys() & actions.keys()
        ),
        default=0.0,
    )
