from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from math import isfinite
from numbers import Integral, Real
from typing import Literal

from dreamscale.policy.runtime.contract import RuntimeContract
from dreamscale.policy.types import ActionSmoothingMode, RunStrategy

Action = tuple[float, ...]


@dataclass(frozen=True)
class ResolvedActionSmoothing:
    requested_mode: ActionSmoothingMode
    mode: Literal["output", "motion", "motion_handover", "motion_speed"]
    new_weight: float
    correction_steps: int | None
    normalized_gripper_indices: tuple[int, ...] = ()
    action_hz: float = 30.0
    reference_speed: float = 1.0
    joint_groups: tuple[tuple[int, ...], ...] = ()
    gripper_indices: tuple[int, ...] = ()


@dataclass(frozen=True)
class SmoothingResolution:
    actions: dict[int, Action]
    overlap_steps: int
    max_abs_position_revision: float
    first_executable_source_offset: int | None
    transition_steps: int | None = None
    arm_speed_rad_s: float | None = None
    effective_new_weight: float | None = None
    correction_gain: float | None = None
    correction_rate_ratio: float | None = None


def resolve_action_smoothing(
    strategy: RunStrategy,
    contract: RuntimeContract,
) -> ResolvedActionSmoothing:
    requested_mode = strategy.action_smoothing
    absolute_action_space = contract.action_space in {
        "absolute_joint_position",
        "raw_absolute_joint",
    }
    if requested_mode == "auto":
        mode = "motion" if absolute_action_space else "output"
    else:
        mode = requested_mode
    if mode != "output" and not absolute_action_space:
        raise ValueError(
            "action smoothing mode 'motion' requires "
            "action_space='absolute_joint_position' or 'raw_absolute_joint'; "
            f"resolved action space is {contract.action_space!r}"
        )
    if mode == "output" and strategy.smoothing_correction_steps is not None:
        raise ValueError("smoothing_correction_steps requires action smoothing mode 'motion'")
    adaptive = mode in {"motion_handover", "motion_speed"}
    if adaptive and not (
        contract.joint_groups and contract.joint_unit == "rad" and absolute_action_space
    ):
        raise ValueError(
            "experimental adaptive smoothing requires an absolute joint layout in radians"
        )
    if strategy.smoothing_reference_speed is not None and not adaptive:
        raise ValueError("smoothing_reference_speed requires an adaptive smoothing mode")
    if mode == "motion_handover" and strategy.smoothing_new_weight is not None:
        raise ValueError("motion_handover does not use smoothing_new_weight")
    new_weight = strategy.smoothing_new_weight
    if new_weight is None and contract.action_space == "model_defined":
        # Actions in the model's own space (a π0.5 deployment's end-effector deltas, say)
        # mean nothing this package knows: a newer chunk replaces the overlap, unblended.
        new_weight = 1.0
    if new_weight is None:
        new_weight = 0.7 if mode == "output" else 0.85
    correction_steps = strategy.smoothing_correction_steps
    if mode != "output" and correction_steps is None:
        correction_steps = max(3, (contract.execution_chunk_size + 4) // 5)
    return ResolvedActionSmoothing(
        requested_mode=requested_mode,
        mode=mode,
        new_weight=float(new_weight),
        correction_steps=correction_steps,
        normalized_gripper_indices=contract.normalized_gripper_indices,
        action_hz=contract.action_hz,
        reference_speed=strategy.smoothing_reference_speed or 1.0,
        joint_groups=contract.joint_groups,
        gripper_indices=contract.gripper_indices,
    )


def resolve_motion_smoothing(
    *,
    next_action_step: int,
    action_steps: Sequence[int],
    new_actions: Sequence[Sequence[float]],
    existing_actions: Mapping[int, Sequence[float]],
    executed_history: Sequence[Sequence[float]],
    new_weight: float,
    correction_steps: int,
    normalized_gripper_indices: tuple[int, ...] = (),
    correction_gain_override: float | None = None,
) -> SmoothingResolution:
    resolved_weight = _unit_weight(new_weight)
    if isinstance(correction_steps, bool) or not isinstance(correction_steps, Integral):
        raise ValueError("correction_steps must be an integer")
    if correction_steps < 1:
        raise ValueError("correction_steps must be positive")
    steps, newest, existing, history = _validated_inputs(
        action_steps=action_steps,
        new_actions=new_actions,
        existing_actions=existing_actions,
        executed_history=executed_history,
    )
    for values in (*newest, *existing.values(), *history):
        validate_normalized_grippers(values, normalized_gripper_indices)
    newest_by_step = dict(zip(steps, newest, strict=True))
    executable = [
        (source_offset, step, newest[source_offset])
        for source_offset, step in enumerate(steps)
        if step >= int(next_action_step)
    ]
    if not history and not existing:
        # There is no previous command to reconcile. Preserve the initial
        # trajectory exactly; managed YAM runs explicitly seed measured state.
        return SmoothingResolution(
            actions={step: action for _, step, action in executable},
            overlap_steps=0,
            max_abs_position_revision=0.0,
            first_executable_source_offset=executable[0][0] if executable else None,
        )
    resolved: dict[int, Action] = {}
    max_revision = 0.0
    overlap = 0
    previous_resolved: Action | None = history[-1] if history else None
    old_weight = 1.0 - resolved_weight
    try:
        correction_divisor = float(correction_steps)
    except OverflowError:
        correction_divisor = float("inf")
    correction_gain = 1.0 / correction_divisor
    if correction_gain_override is not None:
        correction_gain = _unit_weight(correction_gain_override)

    for _, step, new_action in executable:
        old_action = existing.get(step)
        if old_action is not None:
            overlap += 1
        new_previous = newest_by_step.get(step - 1)
        if new_previous is None:
            new_previous = history[-1] if history else new_action
        old_previous = existing.get(step - 1)
        if old_previous is None:
            old_previous = (
                history[-1]
                if history and step == int(next_action_step)
                else old_action or new_previous
            )
        # Missing trajectory coverage means no old motion. In particular, do
        # not extrapolate the last two commands or step back to a history pose
        # after the final queued target. Neither is a model prediction.
        if old_action is None:
            old_action = old_previous
        if previous_resolved is None or (step - 1) not in resolved:
            previous_resolved = old_previous

        blended_delta = tuple(
            (old_weight * (old_action[dimension] - old_previous[dimension]))
            + (resolved_weight * (new_action[dimension] - new_previous[dimension]))
            for dimension in range(len(new_action))
        )
        integrated = tuple(
            previous_resolved[dimension] + blended_delta[dimension]
            for dimension in range(len(new_action))
        )
        action = _as_action(
            tuple(
                integrated[dimension]
                + (correction_gain * (new_action[dimension] - integrated[dimension]))
                for dimension in range(len(new_action))
            )
        )
        # Integrating joint deltas can overshoot even when every source target
        # is valid. Bound normalized grippers before caching/integrating the next
        # step, so saturation never becomes hidden momentum in future chunks.
        if normalized_gripper_indices:
            bounded = list(action)
            for index in normalized_gripper_indices:
                bounded[index] = min(1.0, max(0.0, bounded[index]))
            action = tuple(bounded)
        max_revision = max(max_revision, _max_abs_difference(old_action, action))
        resolved[step] = action
        previous_resolved = action

    return SmoothingResolution(
        actions=resolved,
        overlap_steps=overlap,
        max_abs_position_revision=max_revision,
        first_executable_source_offset=(executable[0][0] if executable else None),
    )


def validate_normalized_grippers(action: Sequence[float], indices: tuple[int, ...]) -> None:
    """Reject bad source/history targets; only smoothing-generated overshoot is bounded."""
    for index in indices:
        if type(index) is not int or not 0 <= index < len(action):
            raise ValueError("normalized gripper index is outside the action")
        if not 0.0 <= action[index] <= 1.0:
            raise ValueError("normalized gripper targets must be within [0, 1]")


def _unit_weight(value: float) -> float:
    if isinstance(value, bool) or not isinstance(value, Real):
        raise ValueError("new_weight must be a number")
    try:
        weight = float(value)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError("new_weight must be a number") from exc
    if not isfinite(weight) or not 0.0 <= weight <= 1.0:
        raise ValueError("new_weight must be between 0 and 1")
    return weight


def _validated_inputs(
    *,
    action_steps: Sequence[int],
    new_actions: Sequence[Sequence[float]],
    existing_actions: Mapping[int, Sequence[float]],
    executed_history: Sequence[Sequence[float]],
) -> tuple[list[int], list[Action], dict[int, Action], list[Action]]:
    if len(action_steps) != len(new_actions):
        raise ValueError("action_steps and new_actions must have the same length")
    steps = [int(step) for step in action_steps]
    if any(right <= left for left, right in zip(steps, steps[1:], strict=False)):
        raise ValueError("action_steps must be strictly increasing")
    newest = [_as_action(action) for action in new_actions]
    existing = {int(step): _as_action(action) for step, action in existing_actions.items()}
    history = [_as_action(action) for action in executed_history]
    dimensions = {len(action) for action in [*newest, *existing.values(), *history]}
    if len(dimensions) > 1:
        raise ValueError("all actions must have the same dimension")
    return steps, newest, existing, history


def _as_action(action: Sequence[float]) -> Action:
    if isinstance(action, (str, bytes)):
        raise ValueError("actions must contain only finite values")
    try:
        raw = tuple(action)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError("actions must contain only finite values") from exc
    if not raw:
        raise ValueError("actions must not be empty")
    if any(isinstance(value, bool) for value in raw):
        raise ValueError("actions must contain only finite values")
    try:
        converted = tuple(float(value) for value in raw)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError("actions must contain only finite values") from exc
    if any(not isfinite(value) for value in converted):
        raise ValueError("actions must contain only finite values")
    return converted


def _max_abs_difference(left: Action, right: Action) -> float:
    return max(
        (abs(a - b) for a, b in zip(left, right, strict=True)),
        default=0.0,
    )
