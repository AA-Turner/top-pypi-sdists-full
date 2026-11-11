"""Main-thread simulation with nonblocking, ordered stateful policy requests."""

import time
from collections import deque

import numpy as np

from .metrics import SimMetrics
from .timing import RealtimePacer

# Without count_holds: an episode's ticks, holds included, stop at this many times its budget.
TICK_CEILING = 4


def run_stateful_episode(
    *,
    env,
    submit,
    result,
    max_steps,
    action_hz=20,
    real_time=True,
    clock=time.monotonic_ns,
    sleep=time.sleep,
    on_frame=None,
    on_buffer=None,
    metrics=None,
    action_dim=7,
    initial_chunk_size=12,
    chunk_size=16,
    request_input=None,
    hold_action=None,
    hold_description="zero end-effector delta with last gripper command",
    feedback_description=None,
    drain_pending=False,
    pause_for_inference=False,
    count_holds=True,
):
    """Execute every model action; preserve full post-action camera history.

    Inference runs in submit's background future. While waiting, physics keeps
    its native cadence with zero end-effector delta and the last gripper command.
    Holds are reported separately and never mislabeled as policy actions.
    With pause_for_inference, physics instead stops until the reply arrives and
    the real-time cadence resumes afterwards, as in synchronous evaluation.
    Without count_holds, max_steps budgets the policy's actions only, as a synchronous
    evaluation's does; the ticks held while a request is in flight run outside it, up to
    TICK_CEILING times max_steps in all, so a stalled session still ends.
    """
    metrics = metrics or SimMetrics(
        max_steps=max_steps,
        action_hz=action_hz,
        action_dt_s=1 / action_hz,
        real_time_enabled=real_time,
    )
    pacer = RealtimePacer(action_hz=action_hz, clock=clock)
    pending = None
    actions = deque()
    feedback = []
    grip = -1.0
    holds = 0
    executed = 0
    first = True
    max_ticks = max_steps if count_holds else max_steps * TICK_CEILING

    def budget_left():
        return result.steps < max_ticks and (count_holds or executed < max_steps)

    def cameras(obs):
        return np.stack([env.agent_frame(obs), env.wrist_frame(obs)])

    def accept(future):
        nonlocal first
        value = np.asarray(future.result(), dtype=np.float32)
        expected = initial_chunk_size if first else chunk_size
        if value.shape != (expected, action_dim) or not np.isfinite(value).all():
            raise ValueError("Policy returned an invalid complete action chunk")
        actions.extend(value.tolist())
        first = False
        # The next request comes once these actions have run: a window sent ahead starts now.
        expect = getattr(env, "expect_request", None)
        if callable(expect):
            expect(len(actions))
        result.policy_calls += 1
        metrics.policy_calls = result.policy_calls

    try:
        obs = env.reset()
        if on_frame:
            on_frame(obs, 0, False)
        pending = submit(request_input(obs) if request_input else np.stack([cameras(obs)]))
        # Initial readiness precedes the timed episode, as in the ordinary sim.
        accept(pending)
        pending = None
        metrics.start_episode(pacer.start())
        while budget_left():
            if real_time:
                metrics.note_realtime_tick(pacer.wait(result.steps, sleep=sleep))
            if pending is not None and (pending.done() or not real_time or pause_for_inference):
                paused_ns = clock()
                accept(pending)
                pending = None
                if real_time and pause_for_inference:
                    pacer.start(pacer.start_ns + clock() - paused_ns)
            policy_action = bool(actions)
            if policy_action:
                action = actions.popleft()
                grip = action[-1]
                executed += 1
            else:
                if pending is None:
                    raise RuntimeError("Missing stateful inference request")
                action = hold_action() if hold_action else [0.0] * 6 + [grip]
                holds += 1
                metrics.note_action_underrun()
            obs, done = env.step(action)
            result.steps += 1
            if policy_action and request_input is None:
                feedback.append(cameras(obs))
            if on_frame:
                on_frame(obs, result.steps, pending is not None)
            metrics.note_step(steps=result.steps, buffer_remaining=len(actions),
                              **({} if count_holds else {"policy_action_steps": executed}))
            if on_buffer:
                on_buffer(result.steps, len(actions))
            if done:
                result.done = True
                break
            if not actions and pending is None and budget_left():
                pending = submit(request_input(obs) if request_input else np.stack(feedback))
                feedback = []
        if real_time:
            pacer.wait(result.steps, sleep=sleep)
        return result
    finally:
        if pending is not None:
            if drain_pending:
                # Drain the bounded reply before another episode reuses this stream.
                pending.result()
            elif not pending.done():
                pending.cancel()
        now = clock()
        metrics.finish(
            steps=result.steps, policy_calls=result.policy_calls, done=result.done, now_ns=now
        )
        result.metrics = metrics.snapshot(now_ns=now)
        result.metrics["stateful"] = {
            "hold_steps": holds,
            "policy_action_steps": executed,
            "feedback_sampling": feedback_description or (
                "four observations spaced two simulator steps apart"
                if request_input else "one raw camera pair after every policy action"
            ),
            "hold_behavior": hold_description,
            "budget": (
                f"{max_steps} steps, holds included" if count_holds else
                f"{max_steps} policy actions; holds outside it, {max_ticks} steps in all"
            ),
        }
