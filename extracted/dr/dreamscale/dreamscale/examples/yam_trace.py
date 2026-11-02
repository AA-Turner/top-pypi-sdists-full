"""Generate a synthetic async recording: no robot, cameras, credentials or cloud."""

from __future__ import annotations

import argparse
import asyncio
import math
import time
from types import SimpleNamespace

import numpy as np

from dreamscale import ActResult, RunStrategy
from dreamscale.policy.run_loop import run_policy_loop
from dreamscale.policy.types import ActionChunkResult, ActionTiming, RuntimeStats
from dreamscale.trace import TraceRecorder


class _SyntheticPolicy:
    model = "molmoact2-bimanual-yam"
    region = "synthetic"
    transport_mode = None
    control = "ultra_aggressive"
    resolved_optimization_config = None

    def __init__(self):
        self.calls = 0
        self.runtime_stats = RuntimeStats()

    async def predict(self, observation, **kwargs):
        self.calls += 1
        call = self.calls
        # Deliberately outlast the queue once to visualize a real managed hold.
        latency = 1.1 if call == 2 else 0.12
        await asyncio.sleep(latency)
        actions = []
        for offset in range(30):
            step = observation.context.action_index + offset
            target = 0.12 * math.sin(step / 20) + 0.015 * (call % 2)
            gripper = 0.2 if step > 45 else 0.8
            actions.append((target,) * 6 + (gripper,) + (-target,) * 6 + (gripper,))
        return ActionChunkResult(
            observation_id=call, chunk_id=call, actions=tuple(actions),
            timing=ActionTiming(obs_to_action_ms=latency * 1000),
        )


async def _run(output, mode):
    policy = _SyntheticPolicy()
    strategy = RunStrategy(action_smoothing=mode)
    state = np.array([0.0] * 6 + [0.8] + [0.0] * 6 + [0.8])
    with TraceRecorder(output, strategy=strategy, model=policy.model) as trace:
        def observe(context):
            return SimpleNamespace(
                context=context, hold_action=tuple(state),
                camera_capture_times_ns=(time.time_ns(),) * 3,
            )

        def act(action, context):
            # Synthetic lagged proprio and a clipped accepted command are
            # separate signals. This is diagnostic data, not a robot simulator.
            trace.measured(state, capture_unix_s=time.time())
            accepted = state + np.clip(np.asarray(action) - state, -0.04, 0.04)
            state[:] += 0.65 * (accepted - state)
            return ActResult(accepted_action=tuple(accepted))

        result = await run_policy_loop(
            policy=policy, instruction="synthetic recording fixture",
            observe=observe, act=act, read_hold_action=lambda _: tuple(state),
            max_actions=90, strategy=strategy, hooks=trace.hooks(),
        )
    print(f"Synthetic only: {result.actions} callbacks, {result.execution_underruns} hold ticks.")
    print(trace.path)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, help="New directory; never overwrites.")
    parser.add_argument(
        "--smoothing", choices=("motion", "motion_handover", "motion_speed"), default="motion",
    )
    args = parser.parse_args()
    asyncio.run(_run(args.output, args.smoothing))


if __name__ == "__main__":
    main()
