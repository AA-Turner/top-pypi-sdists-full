from __future__ import annotations

from collections.abc import Iterable, Sequence
from dataclasses import dataclass, replace
from math import isfinite
from numbers import Integral, Real

from dreamscale.policy.runtime.action_smoothing import (
    ResolvedActionSmoothing,
    resolve_motion_smoothing,
    validate_normalized_grippers,
)
from dreamscale.policy.runtime.adaptive_smoothing import resolve_adaptive_smoothing
from dreamscale.policy.runtime.continuation import continue_motion

Action = tuple[float, ...]


@dataclass
class _BufferedAction:
    action: Action
    rtc_reference_action: Action | None = None
    source_action: Action | None = None


class ActionBuffer:
    def __init__(self, *, next_action_step: int = 0) -> None:
        self._next_action_step = int(next_action_step)
        self._actions: dict[int, _BufferedAction] = {}
        self._last_consumed: tuple[int, Action] | None = None
        # The step last consumed and its RTC reference row: a request whose observation was
        # captured at that step starts its committed rows there (peek_rtc_reference_actions).
        self._last_consumed_reference: tuple[int, Action | None] | None = None
        self._handover_end_step: int | None = None

    @property
    def next_action_step(self) -> int:
        return self._next_action_step

    def consume(self) -> Action | None:
        item = self._actions.pop(self._next_action_step, None)
        if item is None:
            return None
        self._last_consumed = (self._next_action_step, item.action)
        self._last_consumed_reference = (self._next_action_step, item.rtc_reference_action)
        self._next_action_step += 1
        return item.action

    def advance_to(self, action_step: int) -> None:
        target = max(self._next_action_step, int(action_step))
        if target == self._next_action_step:
            return
        self._actions = {step: item for step, item in self._actions.items() if step >= target}
        self._next_action_step = target

    def actions_remaining(self, action_step: int | None = None) -> int:
        step = self._next_action_step if action_step is None else int(action_step)
        remaining = 0
        while step + remaining in self._actions:
            remaining += 1
        return remaining

    def snapshot(self, *, raw: bool = False) -> tuple[tuple[int, Action], ...]:
        """Immutable aligned targets; absent source values remain absent."""
        return tuple(
            (step, item.source_action if raw else item.action)
            for step, item in sorted(self._actions.items())
            if not raw or item.source_action is not None
        )

    def merge_aligned_chunk(
        self,
        *,
        base_action_step: int,
        actions: Sequence[Sequence[float]],
        action_indices: Sequence[int] | None = None,
        new_weight: float = 0.5,
    ) -> dict[str, int | float | str | None]:
        base = int(base_action_step)
        overlap = 0
        resolved_new_weight = _unit_weight(new_weight)
        resolved_old_weight = 1.0 - resolved_new_weight
        action_steps = _resolve_action_steps(
            base_action_step=base,
            action_count=len(actions),
            action_indices=action_indices,
        )
        stale_steps = sum(step < self._next_action_step for step in action_steps)
        first_executable_source_offset = next(
            (offset for offset, step in enumerate(action_steps) if step >= self._next_action_step),
            None,
        )
        if first_executable_source_offset is None:
            return {
                "requested_mode": "output",
                "resolved_mode": "output",
                "new_action_weight": resolved_new_weight,
                "correction_steps": None,
                "stale_steps": stale_steps,
                "overlap_steps": 0,
                "resolved_steps": 0,
                "rebase_offset_steps": 0,
                "first_executable_source_offset": None,
                "max_abs_position_revision": 0.0,
            }
        before = {
            step: item.action
            for step, item in self._actions.items()
            if step >= self._next_action_step
        }
        next_actions = {
            step: item
            for step, item in self._actions.items()
            if self._next_action_step <= step < base
        }
        for offset, raw_action in enumerate(actions):
            step = action_steps[offset]
            if step < self._next_action_step:
                continue
            action = _as_action(raw_action)
            existing = self._actions.get(step)
            if existing is not None:
                overlap += 1
                action = _blend(
                    existing.action,
                    action,
                    resolved_old_weight,
                    resolved_new_weight,
                )
            next_actions[step] = _BufferedAction(
                action=action, source_action=_as_action(raw_action)
            )
        self._actions = next_actions
        after = {
            step: item.action
            for step, item in self._actions.items()
            if step >= self._next_action_step
        }
        return {
            "requested_mode": "output",
            "resolved_mode": "output",
            "new_action_weight": resolved_new_weight,
            "correction_steps": None,
            "stale_steps": stale_steps,
            "overlap_steps": overlap,
            "resolved_steps": len(
                {step for step in action_steps if step >= self._next_action_step}
            ),
            "rebase_offset_steps": 0,
            "first_executable_source_offset": first_executable_source_offset,
            "max_abs_position_revision": _max_buffer_revision(before, after),
        }

    def merge_smoothed_chunk(
        self,
        *,
        base_action_step: int,
        actions: Sequence[Sequence[float]],
        smoothing: ResolvedActionSmoothing,
        executed_history: Sequence[Sequence[float]],
        action_indices: Sequence[int] | None = None,
    ) -> dict[str, int | float | str | None]:
        base = int(base_action_step)
        source_steps = _resolve_action_steps(
            base_action_step=base,
            action_count=len(actions),
            action_indices=action_indices,
        )
        stale_steps = sum(step < self._next_action_step for step in source_steps)
        action_steps = source_steps
        first_executable_source_offset = next(
            (offset for offset, step in enumerate(action_steps) if step >= self._next_action_step),
            None,
        )
        if first_executable_source_offset is None:
            return {
                "requested_mode": smoothing.requested_mode,
                "resolved_mode": smoothing.mode,
                "new_action_weight": (
                    None if smoothing.mode == "motion_handover" else smoothing.new_weight
                ),
                "correction_steps": smoothing.correction_steps,
                "stale_steps": stale_steps,
                "overlap_steps": 0,
                "resolved_steps": 0,
                "rebase_offset_steps": 0,
                "first_executable_source_offset": None,
                "max_abs_position_revision": 0.0,
            }

        if smoothing.mode == "output":
            if smoothing.normalized_gripper_indices:
                for action in actions:
                    validate_normalized_grippers(
                        _as_action(action), smoothing.normalized_gripper_indices
                    )
            diagnostics = self.merge_aligned_chunk(
                base_action_step=base,
                actions=actions,
                action_indices=action_indices,
                new_weight=smoothing.new_weight,
            )
            return {
                **diagnostics,
                "requested_mode": smoothing.requested_mode,
                "resolved_mode": smoothing.mode,
            }

        existing_actions = {
            step: item.action
            for step, item in self._actions.items()
            if step >= self._next_action_step
        }
        if smoothing.mode == "continuation":
            joined = continue_motion(
                next_action_step=self._next_action_step,
                action_steps=action_steps,
                new_actions=actions,
                existing_actions=existing_actions,
                executed_history=executed_history,
                gripper_indices=smoothing.gripper_indices,
                normalized_gripper_indices=smoothing.normalized_gripper_indices,
            )
            next_actions = {
                step: item
                for step, item in self._actions.items()
                if self._next_action_step <= step < base
            }
            sources = dict(zip(action_steps, map(_as_action, actions), strict=True))
            next_actions.update({
                step: _BufferedAction(action=action, source_action=sources[step])
                for step, action in joined.actions.items()
            })
            self._actions = next_actions
            return {
                "requested_mode": smoothing.requested_mode,
                "resolved_mode": smoothing.mode,
                "new_action_weight": None,
                "correction_steps": None,
                "stale_steps": stale_steps,
                "overlap_steps": joined.overlap_steps,
                "resolved_steps": len(joined.actions),
                "rebase_offset_steps": 0,
                "first_executable_source_offset": joined.first_executable_source_offset,
                "max_abs_position_revision": joined.max_abs_position_revision,
                "junction_offset": joined.junction_offset,
            }
        if smoothing.correction_steps is None:
            raise AssertionError("motion smoothing requires correction steps")
        inputs = dict(
            next_action_step=self._next_action_step,
            action_steps=action_steps,
            new_actions=actions,
            existing_actions=existing_actions,
            executed_history=executed_history,
        )
        if smoothing.mode in {"motion_handover", "motion_speed"}:
            resolution = resolve_adaptive_smoothing(**inputs, smoothing=smoothing)
        else:
            resolution = resolve_motion_smoothing(
                **inputs,
                new_weight=smoothing.new_weight,
                correction_steps=smoothing.correction_steps,
                normalized_gripper_indices=smoothing.normalized_gripper_indices,
            )
        sources = dict(zip(action_steps, map(_as_action, actions), strict=True))
        if smoothing.mode == "motion_handover":
            overlap = sources.keys() & existing_actions.keys()
            joints = tuple(index for group in smoothing.joint_groups for index in group)
            # Preserve a finite transition when a replan only repeats/extends
            # the same raw targets. Changed accepted feedback requires reanchoring.
            unchanged = (
                bool(overlap)
                and self._handover_end_step is not None
                and action_steps[-1] >= self._handover_end_step
                and bool(executed_history)
                and self._last_consumed is not None
                and self._last_consumed[0] == self._next_action_step - 1
                and all(self._last_consumed[1][j] == executed_history[-1][j] for j in joints)
                and all(
                    self._actions[step].source_action is not None
                    and all(
                        self._actions[step].source_action[j] == sources[step][j] for j in joints
                    )
                    for step in overlap
                )
            )
            if unchanged:
                continuation = {
                    step: tuple(
                        sources[step][j] if j in smoothing.gripper_indices else value
                        for j, value in enumerate(existing_actions.get(step, sources[step]))
                    )
                    for step in resolution.actions
                }
                resolution = replace(
                    resolution,
                    actions=continuation,
                    max_abs_position_revision=max(
                        (
                            abs(existing_actions[i][j] - continuation[i][j])
                            for i in overlap
                            for j in range(len(continuation[i]))
                        ),
                        default=0.0,
                    ),
                    transition_steps=max(0, self._handover_end_step - self._next_action_step + 1),
                    correction_rate_ratio=None,
                )
            else:
                self._handover_end_step = (
                    self._next_action_step + (resolution.transition_steps or 0) - 1
                )

        next_actions = {
            step: item
            for step, item in self._actions.items()
            if self._next_action_step <= step < base
        }
        next_actions.update(
            {
                step: _BufferedAction(action=action, source_action=sources[step])
                for step, action in resolution.actions.items()
            }
        )
        self._actions = next_actions
        return {
            "requested_mode": smoothing.requested_mode,
            "resolved_mode": smoothing.mode,
            "new_action_weight": (
                None
                if smoothing.mode == "motion_handover"
                else resolution.effective_new_weight
                if resolution.effective_new_weight is not None
                else smoothing.new_weight
            ),
            "correction_steps": smoothing.correction_steps,
            "stale_steps": stale_steps,
            "overlap_steps": resolution.overlap_steps,
            "resolved_steps": len(resolution.actions),
            "rebase_offset_steps": 0,
            "first_executable_source_offset": resolution.first_executable_source_offset,
            "max_abs_position_revision": resolution.max_abs_position_revision,
            "transition_steps": resolution.transition_steps,
            "arm_speed_rad_s": resolution.arm_speed_rad_s,
            "correction_gain": resolution.correction_gain,
            "correction_rate_ratio": resolution.correction_rate_ratio,
        }

    def place_chunk(
        self,
        *,
        actions: Sequence[Sequence[float]],
        action_indices: Sequence[int] | None = None,
    ) -> dict[str, int | float | str | None]:
        """The chunked schedule: the robot held while this chunk was inferred, so its first row
        is the next step's, whatever time went by. Its rows replace the plan as they are."""
        base = self._next_action_step
        steps = _resolve_action_steps(
            base_action_step=base, action_count=len(actions), action_indices=action_indices,
        )
        overlap = sum(1 for step in steps if step in self._actions)
        self._actions = {
            step: _BufferedAction(action=_as_action(row), source_action=_as_action(row))
            for step, row in zip(steps, actions, strict=True)
        }
        return {
            "requested_mode": "sync",
            "resolved_mode": "sync",
            "new_action_weight": None,
            "correction_steps": None,
            "stale_steps": 0,
            "overlap_steps": overlap,
            "resolved_steps": len(steps),
            "rebase_offset_steps": 0,
            "first_executable_source_offset": 0 if steps else None,
            "max_abs_position_revision": 0.0,
        }

    def replace_aligned_chunk(
        self,
        *,
        base_action_step: int,
        actions: Sequence[Sequence[float]],
        action_indices: Sequence[int] | None = None,
        rtc_reference_actions: Sequence[Sequence[float]] | None = None,
    ) -> dict[str, int | str]:
        base = int(base_action_step)
        action_steps = _resolve_action_steps(
            base_action_step=base,
            action_count=len(actions),
            action_indices=action_indices,
        )
        references = (
            [_as_action(action) for action in rtc_reference_actions]
            if rtc_reference_actions is not None
            else [None] * len(actions)
        )
        if len(references) != len(actions):
            raise ValueError("rtc_reference_actions length must match actions")
        if not any(step >= self._next_action_step for step in action_steps):
            return {
                "mode": "rtc_replace",
                "replaced_steps": 0,
                "rebase_offset_steps": 0,
            }
        replaced = 0
        next_actions = {
            step: item
            for step, item in self._actions.items()
            if self._next_action_step <= step < base
        }
        for offset, raw_action in enumerate(actions):
            step = action_steps[offset]
            if step < self._next_action_step:
                continue
            if step in self._actions:
                replaced += 1
            next_actions[step] = _BufferedAction(
                action=_as_action(raw_action),
                rtc_reference_action=references[offset],
                source_action=_as_action(raw_action),
            )
        self._actions = next_actions
        return {
            "mode": "rtc_replace",
            "replaced_steps": replaced,
            "rebase_offset_steps": 0,
        }

    def peek_rtc_reference_actions(
        self, max_steps: int | None = None, from_step: int | None = None
    ) -> list[Action] | None:
        """The planned reference rows from ``from_step`` (default the next step). The step just
        consumed may lead them: a request observed at that step commits it first."""
        refs: list[Action] = []
        if from_step is not None and from_step == self._next_action_step - 1:
            consumed = self._last_consumed_reference
            if consumed is None or consumed[0] != from_step or consumed[1] is None:
                return None
            refs.append(consumed[1])
            max_steps = None if max_steps is None else max_steps - 1
        elif from_step is not None and from_step != self._next_action_step:
            return None
        for step in _contiguous_steps(self._actions, self._next_action_step, max_steps):
            reference = self._actions[step].rtc_reference_action
            if reference is None:
                return None
            refs.append(reference)
        return refs if refs else None


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


def _resolve_action_steps(
    *,
    base_action_step: int,
    action_count: int,
    action_indices: Sequence[int] | None,
) -> list[int]:
    base = int(base_action_step)
    if action_indices is None:
        steps = [base + offset for offset in range(action_count)]
    else:
        if len(action_indices) != action_count:
            raise ValueError("action_indices length must match actions")
        if any(
            isinstance(action_index, bool)
            or not isinstance(action_index, Integral)
            or action_index < 0
            for action_index in action_indices
        ):
            raise ValueError("action_indices must contain nonnegative integers")
        steps = [base + int(action_index) for action_index in action_indices]
    if any(right <= left for left, right in zip(steps, steps[1:], strict=False)):
        raise ValueError("resolved action steps must be strictly increasing")
    return steps


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


def _blend(old: Action, new: Action, old_weight: float, new_weight: float) -> Action:
    if len(old) != len(new):
        raise ValueError("cannot blend actions with different dimensions")
    return tuple(old[i] * old_weight + new[i] * new_weight for i in range(len(old)))


def _max_buffer_revision(
    before: dict[int, Action],
    after: dict[int, Action],
) -> float:
    maximum = 0.0
    for step in before.keys() & after.keys():
        maximum = max(
            maximum,
            max(
                (abs(old - new) for old, new in zip(before[step], after[step], strict=True)),
                default=0.0,
            ),
        )
    return maximum


def _contiguous_steps(
    actions: dict[int, _BufferedAction],
    start: int,
    max_steps: int | None,
) -> Iterable[int]:
    count = 0
    while start + count in actions:
        if max_steps is not None and count >= max_steps:
            return
        yield start + count
        count += 1
