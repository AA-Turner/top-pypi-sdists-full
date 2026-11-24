"""Unified ControlArbiter for cold-start teleop demos and live clutch takeover.

State machine:
- ``IDLE``: holding pose before start / after stop.
- ``TELEOP_ONLY``: cold-start human demo collection (``dreamscale record``; ``policy=None``).
  Records every frame with ``action_source="human"`` and ``intervention=False`` with zero
  cloud inference sessions opened.
- ``AUTONOMOUS``: cloud policy driving; records ``action_source="policy"``, ``intervention=False``.
- ``HUMAN_TAKEOVER``: human clutch engaged; immediately preempts policy, pauses remote inference,
  smoothly blends from the follower's measured pose over ``blend_steps``, and stamps every frame
  with ``action_source="human"`` and ``intervention=True``.
- ``HANDBACK_RESET``: clutch released; commands a safe hold at the post-takeover measured pose,
  calls ``await policy.reset_episode()`` to flush stale chunks and reset client + server history,
  and blends smoothly back into ``AUTONOMOUS`` with zero motion jump.
"""

from __future__ import annotations

import asyncio
import enum
import inspect
import time
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from typing import Any

from dreamscale.policy.types import RunContext, RunResult

from .devices import TeleopDevice


class ArbiterState(enum.StrEnum):
    IDLE = "idle"
    TELEOP_ONLY = "teleop_only"
    AUTONOMOUS = "autonomous"
    HUMAN_TAKEOVER = "human_takeover"
    HANDBACK_RESET = "handback_reset"


@dataclass(frozen=True)
class ArbiterTransition:
    step: int
    from_state: ArbiterState
    to_state: ArbiterState
    timestamp_s: float


@dataclass(frozen=True)
class ArbiterSummary:
    run_result: RunResult
    total_frames: int
    policy_frames: int
    takeover_frames: int
    teleop_frames: int
    takeover_count: int
    policy_resets: int
    max_command_step: float
    transitions: tuple[ArbiterTransition, ...]


def _blend_target(
    start: Sequence[float],
    goal: Sequence[float],
    *,
    alpha: float,
    max_delta: float | None = None,
) -> tuple[float, ...]:
    a = min(1.0, max(0.0, float(alpha)))
    out: list[float] = []
    for s, g in zip(start, goal, strict=True):
        val = float(s) + (float(g) - float(s)) * a
        if max_delta is not None and max_delta > 0:
            diff = val - float(s)
            if abs(diff) > max_delta:
                val = float(s) + (max_delta if diff > 0 else -max_delta)
        out.append(val)
    return tuple(out)


def _max_abs_delta(a: Sequence[float], b: Sequence[float]) -> float:
    return max((abs(float(x) - float(y)) for x, y in zip(a, b, strict=True)), default=0.0)


class ControlArbiter:
    """Shared control-loop arbiter for ``dreamscale record`` and ``dreamscale run --teleop``."""

    def __init__(
        self,
        *,
        rig: Any,
        teleop: TeleopDevice,
        policy: Any | None = None,
        observe: Callable[[RunContext], Any] | None = None,
        act: Callable[[Sequence[float], RunContext | None], Any] | None = None,
        read_hold_action: Callable[[RunContext | None], Sequence[float]] | None = None,
        fps: float = 30.0,
        blend_steps: int = 5,
        max_transition_delta: float | None = None,
        spool_episode: Any | None = None,
        on_inference_active: Callable[[bool], None] | None = None,
        print_fn: Callable[[str], None] | None = None,
        pace: bool = True,
    ) -> None:
        self.rig = rig
        self.teleop = teleop
        self.policy = policy
        self._observe = observe or rig.observe
        self._act = act or rig.act
        self._read_hold_action = read_hold_action or rig.read_hold_action
        self.fps = float(fps) if fps and fps > 0 else 30.0
        self.period_s = 1.0 / self.fps
        self.blend_steps = max(1, int(blend_steps))
        self.max_transition_delta = max_transition_delta
        self.spool_episode = spool_episode
        self._on_inference_active = on_inference_active
        self._print = print_fn
        self._pace = bool(pace)

        self.state = ArbiterState.IDLE
        self._stop_requested = False
        self._transitions: list[ArbiterTransition] = []

    def request_stop(self) -> None:
        self._stop_requested = True

    def _set_state(self, new_state: ArbiterState, step: int) -> None:
        if new_state == self.state:
            return
        prev = self.state
        self.state = new_state
        self._transitions.append(
            ArbiterTransition(
                step=step,
                from_state=prev,
                to_state=new_state,
                timestamp_s=time.monotonic(),
            )
        )

    def _set_inference_active(self, active: bool) -> None:
        if self._on_inference_active is not None:
            self._on_inference_active(active)

    def _safe_frames(self) -> dict[str, Any] | None:
        if hasattr(self.rig, "latest_frames"):
            try:
                return self.rig.latest_frames()
            except Exception:  # noqa: BLE001
                return None
        return None

    async def _next_policy_action(
        self,
        obs: Any,
        *,
        instruction: str,
        cached_chunk: list[tuple[float, ...]],
    ) -> tuple[float, ...]:
        assert self.policy is not None
        next_fn = getattr(self.policy, "next_action", None)
        if callable(next_fn):
            res = next_fn(obs, instruction, pace=False)
            if inspect.isawaitable(res):
                res = await res
            return tuple(float(v) for v in res)
        if not cached_chunk:
            chunk = self.policy.predict(obs, instruction=instruction)
            if inspect.isawaitable(chunk):
                chunk = await chunk
            cached_chunk.extend(tuple(float(v) for v in row) for row in chunk.actions)
        if not cached_chunk:
            return tuple(float(v) for v in self._read_hold_action(None))
        return cached_chunk.pop(0)

    async def _reset_policy_episode(self, cached_chunk: list[tuple[float, ...]]) -> int:
        cached_chunk.clear()
        if self.policy is None:
            return 0
        reset_fn = getattr(self.policy, "reset_episode", None)
        if callable(reset_fn):
            res = reset_fn()
            if inspect.isawaitable(res):
                await res
            return 1
        return 0

    async def run_episode(
        self,
        *,
        instruction: str = "",
        max_actions: int | None = None,
    ) -> ArbiterSummary:
        """Run one episode under unified arbitration until ``max_actions`` or ``request_stop``."""
        self._stop_requested = False
        self._transitions.clear()
        self.teleop.open()

        started_s = time.monotonic()
        total_frames = 0
        policy_frames = 0
        takeover_frames = 0
        teleop_frames = 0
        takeover_count = 0
        policy_resets = 0
        policy_calls = 0
        max_command_step = 0.0

        cached_chunk: list[tuple[float, ...]] = []
        blend_remaining = 0
        last_command: tuple[float, ...] = tuple(float(v) for v in self._read_hold_action(None))

        if self.policy is None:
            self._set_state(ArbiterState.TELEOP_ONLY, step=0)
            self._set_inference_active(False)
            self.teleop.sync_pose(last_command)
        else:
            self._set_state(ArbiterState.AUTONOMOUS, step=0)
            self._set_inference_active(True)

        step = 0
        try:
            while not self._stop_requested:
                if max_actions is not None and step >= max_actions:
                    break
                tick_start = time.monotonic()
                ctx = RunContext(
                    action_index=step,
                    observation_id=step,
                    actions_remaining=len(cached_chunk),
                    stalled=False,
                    elapsed_s=tick_start - started_s,
                )
                measured = tuple(float(v) for v in self._read_hold_action(ctx))
                sample = self.teleop.read()

                if self.policy is None:
                    # Cold-start teleop demo collection (dreamscale record)
                    if sample.clutch:
                        raw_target = sample.target
                        if blend_remaining > 0:
                            alpha = (self.blend_steps - blend_remaining + 1) / self.blend_steps
                            command = _blend_target(
                                last_command,
                                raw_target,
                                alpha=alpha,
                                max_delta=self.max_transition_delta,
                            )
                            blend_remaining -= 1
                        else:
                            command = _blend_target(
                                last_command,
                                raw_target,
                                alpha=1.0,
                                max_delta=self.max_transition_delta,
                            )
                    else:
                        command = measured
                        blend_remaining = self.blend_steps

                    self._act(command, ctx)
                    max_command_step = max(max_command_step, _max_abs_delta(last_command, command))
                    last_command = command
                    teleop_frames += 1
                    total_frames += 1
                    if self.spool_episode is not None:
                        self.spool_episode.record_step(
                            measured,
                            command,
                            frames=self._safe_frames(),
                            action_source="human",
                            intervention=False,
                        )
                else:
                    # Autonomous + live clutch takeover (dreamscale run --teleop)
                    if sample.clutch:
                        if self.state != ArbiterState.HUMAN_TAKEOVER:
                            self._set_state(ArbiterState.HUMAN_TAKEOVER, step=step)
                            self._set_inference_active(False)
                            takeover_count += 1
                            self.teleop.sync_pose(measured)
                            blend_remaining = self.blend_steps
                            # Re-read once after sync_pose so Quest 3S starts at zero delta.
                            sample = self.teleop.read()
                            if self._print is not None:
                                self._print(
                                    f"Human takeover #{takeover_count} engaged — policy paused."
                                )

                        if blend_remaining > 0:
                            alpha = (self.blend_steps - blend_remaining + 1) / self.blend_steps
                            command = _blend_target(
                                last_command,
                                sample.target,
                                alpha=alpha,
                                max_delta=self.max_transition_delta,
                            )
                            blend_remaining -= 1
                        else:
                            command = _blend_target(
                                last_command,
                                sample.target,
                                alpha=1.0,
                                max_delta=self.max_transition_delta,
                            )
                        self._act(command, ctx)
                        max_command_step = max(
                            max_command_step, _max_abs_delta(last_command, command)
                        )
                        last_command = command
                        takeover_frames += 1
                        total_frames += 1
                        if self.spool_episode is not None:
                            self.spool_episode.record_step(
                                measured,
                                command,
                                frames=self._safe_frames(),
                                action_source="human",
                                intervention=True,
                            )
                    else:
                        if self.state == ArbiterState.HUMAN_TAKEOVER:
                            # Safe handback: hold pose, reset policy history, then blend in.
                            self._set_state(ArbiterState.HANDBACK_RESET, step=step)
                            self._act(measured, ctx)
                            last_command = measured
                            policy_resets += await self._reset_policy_episode(cached_chunk)
                            blend_remaining = self.blend_steps
                            self._set_state(ArbiterState.AUTONOMOUS, step=step)
                            self._set_inference_active(True)
                            if self._print is not None:
                                self._print("Handback complete — policy reset and resumed.")

                        obs = self._observe(ctx)
                        if inspect.isawaitable(obs):
                            obs = await obs
                        policy_calls += 1
                        raw_policy_action = await self._next_policy_action(
                            obs, instruction=instruction, cached_chunk=cached_chunk
                        )
                        if blend_remaining > 0:
                            alpha = (self.blend_steps - blend_remaining + 1) / self.blend_steps
                            command = _blend_target(
                                last_command,
                                raw_policy_action,
                                alpha=alpha,
                                max_delta=self.max_transition_delta,
                            )
                            blend_remaining -= 1
                        else:
                            command = raw_policy_action
                        self._act(command, ctx)
                        max_command_step = max(
                            max_command_step, _max_abs_delta(last_command, command)
                        )
                        last_command = command
                        policy_frames += 1
                        total_frames += 1
                        if self.spool_episode is not None:
                            self.spool_episode.record_step(
                                measured,
                                command,
                                frames=self._safe_frames(),
                                action_source="policy",
                                intervention=False,
                            )

                step += 1
                if self._pace:
                    remaining = self.period_s - (time.monotonic() - tick_start)
                    if remaining > 0:
                        await asyncio.sleep(remaining)
        finally:
            self._set_inference_active(False)
            self._set_state(ArbiterState.IDLE, step=step)

        elapsed_s = time.monotonic() - started_s
        return ArbiterSummary(
            run_result=RunResult(
                actions=total_frames,
                policy_calls=policy_calls,
                underruns=0,
                done=not self._stop_requested,
                elapsed_s=elapsed_s,
            ),
            total_frames=total_frames,
            policy_frames=policy_frames,
            takeover_frames=takeover_frames,
            teleop_frames=teleop_frames,
            takeover_count=takeover_count,
            policy_resets=policy_resets,
            max_command_step=max_command_step,
            transitions=tuple(self._transitions),
        )
