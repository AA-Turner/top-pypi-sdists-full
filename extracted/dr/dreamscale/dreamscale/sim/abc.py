"""Bimanual YAM models on ABC's simulator (`dreamscale sim abc`; DSL-425).

The simulator stands in for the robot and nothing else changes: the session is the one
`dreamscale run yam` opens (``dreamscale.connect``), and the episode is the SDK's managed run
loop (``policy.run``), which asks for an observation when it plans and commands one action a
tick, holding the measured joints when none has arrived. The wire is the YAM robot's: the top,
left and right cameras and 14 joint values in, 14 absolute joint targets out.

- Each action is one abc_sim control step (0.034 s of physics), paced by the run loop at the
  model's 30 Hz, so a chunk that arrives late costs the ticks a robot would have held. The
  loop never makes up the time between waking for a tick and sending its action (its rule
  against bursts of overdue commands), so the world runs a little under real time: about 27
  actions a second on a laptop. Each episode reports its rate.
- The cameras are free-running, as a robot's are: the simulator renders them beside the
  physics as fast as the machine can (about 18 frames a second on a laptop), and a plan
  reads the newest frames without stopping the world. A machine that renders slowly gives
  the model old frames, and the run says so.
- An episode ends at the task's first success (upstream's ``ever_success``) or its budget.
- A model trained on abc_sim episodes (ABC-VLA) is told the prompt those episodes carried.
  The others were trained on real footage: they run, and their score says nothing about the
  robot.
"""

from __future__ import annotations

import json
import time
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from dreamscale import errors
from dreamscale.model_names import internal_model, public_model

from .abc_catalog import (
    CONTROL_HZ,
    DEFAULT_TASK,
    HORIZON_STEPS,
    MODELS,
    SEED,
    prompt_for,
    resolve_task,
)

# The viewer and the video take the cameras' newest frames every this many ticks (10 a second).
FRAME_EVERY = 3
# Below this many camera frames a second the model plans on frames a robot would call stale.
SLOW_CAMERA_FPS = 10.0
# Below this share of the model's rate the world ran slow enough to change what the model
# sees of its own latency: the machine is too busy to pace the episode.
SLOW_WORLD = 0.75


@dataclass
class EpisodeResult:
    success: bool
    steps: int
    max_steps: int
    seconds: float
    task: str
    episode: int
    seed: int
    instruction: str
    max_reward: float
    policy_calls: int
    underruns: int
    stop_reason: str
    policy_response_p50_ms: float | None = None
    actions_per_s: float | None = None
    camera_fps: float | None = None
    video: str | None = None

    def as_json(self) -> dict:
        return {key: getattr(self, key) for key in self.__dataclass_fields__}


def yam_observation(observed: dict, *, actions_remaining: int = 0) -> Any:
    """abc_sim's state and cameras as the YAM robot's observation: left six joints and
    gripper, then right; the gripper is 0 closed to 1 open on both sides of the wire."""
    from dreamscale import yam

    state, images = observed["state"], observed["images"]
    return yam.observation(
        top_frame=images["top"], left_frame=images["left"], right_frame=images["right"],
        left_joint_positions=state[0:6], left_gripper=_unit(state[6]),
        right_joint_positions=state[7:13], right_gripper=_unit(state[13]),
        actions_remaining=actions_remaining,
    )


def hold_action(state) -> tuple[float, ...]:
    """The measured joints as an action: what the run loop commands while it has no plan."""
    return (*state[0:6], _unit(state[6]), *state[7:13], _unit(state[13]))


def _unit(value: float) -> float:
    # The simulated finger settles a hair past its limits; the wire takes 0 to 1.
    return min(1.0, max(0.0, float(value)))


def run_episode(env: Any, policy: Any, *, instruction: str, max_steps: int,
                real_time: bool = True, view: bool = False, record: bool = False) -> Any:
    """One episode on a reset env through the managed run loop: its RunResult."""
    from dreamscale.policy.types import ActResult, RunStrategy

    ticks = 0

    def observe(context):
        return yam_observation(env.observe(), actions_remaining=context.actions_remaining)

    def act(action, context):
        nonlocal ticks
        result = env.step(action)
        ticks += 1
        if (view or record) and ticks % FRAME_EVERY == 0:
            env.frame(show=view, record=record)
        return ActResult(done=bool(result["over"]))

    if view or record:
        env.frame(show=view, record=record)
    return policy.run(
        instruction=instruction, observe=observe, act=act,
        read_hold_action=lambda context: hold_action(env.state),
        max_actions=max_steps, strategy=RunStrategy(real_time=real_time),
    )


def run_abc(*, model: str, task_suite: str = DEFAULT_TASK, task_id: str | int = 0,
            task_seed: int = 0, episodes: int = 1, max_steps: int | None = None,
            max_duration: float | None = None, view: bool = True, real_time: bool = True,
            json_output: bool = False, output_root: str | Path | None = None,
            keep_warm: int = 0, region: str | None = None, transport: str = "auto",
            steady_send: bool | int | None = None,
            env_factory: Callable[..., Any] | None = None,
            connect: Callable[..., Any] | None = None,
            on_line: Callable[[str], None] = print, **_ignored: Any) -> dict:
    """``episodes`` episodes of one abc_sim task, from episode ``task_id``, on one session.

    Episode N's scene is upstream's eval world N (seed 20260511 + N); ``task_seed`` shifts
    it. Returns the summary it prints with ``json_output``.
    """
    model = internal_model(model)
    if model not in MODELS:
        raise ValueError(f"{public_model(model)} doesn't run on abc. {errors.SEE_MODELS}")
    first = resolve_task(task_suite, task_id)
    if type(episodes) is not int or episodes < 1:
        raise ValueError("episodes must be a positive integer")
    horizon = (max(1, int(max_duration * CONTROL_HZ + 0.999999)) if max_duration
               else max_steps or HORIZON_STEPS)
    root = Path(output_root).expanduser().resolve() if output_root is not None else None
    if root is not None:
        root.mkdir(parents=True, exist_ok=True)
    if env_factory is None:
        from dreamscale.config import load_config

        if not load_config().api_key:
            raise errors.catalog("not_configured")
        from .abc_runtime import AbcSimEnv, ensure_abc_assets, ensure_abc_runtime

        # The simulator and its assets before any billable compute opens.
        python = ensure_abc_runtime(on_line=on_line)
        ensure_abc_assets(task_suite, on_line=on_line)
        env_factory = lambda **kwargs: AbcSimEnv(python=python, **kwargs)  # noqa: E731
    if connect is None:
        import dreamscale

        connect = dreamscale.connect
    env = env_factory(task=task_suite, seed=SEED + task_seed + first)
    rows: list[EpisodeResult] = []
    summary: dict[str, Any] = {
        "benchmark": "abc", "model": public_model(model), "task": task_suite,
        "task_seed": task_seed, "success_condition": "upstream_ever_success",
        "scored": bool(env.scored), "results": [],
    }
    policy = None
    try:
        began = time.monotonic()
        policy = connect(model, **_connect_options(
            model, region=region, keep_warm=keep_warm, transport=transport,
            steady_send=steady_send))
        summary["connect_s"] = round(time.monotonic() - began, 1)
        for index in range(first, first + episodes):
            env.reset(SEED + task_seed + index)
            instruction = prompt_for(model, task_suite, env.task_description)
            on_line(f"[local] task: {instruction} (episode {index}, seed {env.seed})")
            frames_before = env.stats()["camera_frames"]
            began = time.monotonic()
            result = run_episode(env, policy, instruction=instruction, max_steps=horizon,
                                 real_time=real_time, view=view, record=root is not None)
            seconds = time.monotonic() - began
            success = bool(env.last["success"])
            row = EpisodeResult(
                success=success, steps=result.actions, max_steps=horizon,
                seconds=round(seconds, 1), task=task_suite, episode=index,
                seed=env.seed, instruction=instruction,
                max_reward=round(float(env.last["max_reward"]), 4),
                policy_calls=result.policy_calls, underruns=result.underruns,
                stop_reason=result.stop_reason,
                policy_response_p50_ms=result.timing.policy_response_ms.p50_ms,
                actions_per_s=_action_rate(result),
                camera_fps=(round((env.stats()["camera_frames"] - frames_before) / seconds, 1)
                            if seconds > 0 else None),
            )
            if root is not None:
                video = root / f"abc_{task_suite}_{index:03d}_{'ok' if success else 'fail'}.mp4"
                try:  # the video is a by-product: a writer that fails costs it, not the run
                    if env.write_video(video, CONTROL_HZ / FRAME_EVERY):
                        row.video = str(video)
                except RuntimeError:
                    pass
            rows.append(row)
            summary["results"].append(row.as_json())
            if root is not None:
                (root / "summary.json").write_text(json.dumps(summary, indent=2))
            rate = "" if row.actions_per_s is None else f" at {row.actions_per_s:g} a second"
            on_line(f"{'✓ Success' if success else '✗ Not done'}: {task_suite} episode {index} "
                    f"({row.steps} actions{rate}, {row.seconds:.0f} s, "
                    f"{row.policy_calls} plans, {row.underruns} held ticks)")
            if real_time and row.camera_fps is not None and row.camera_fps < SLOW_CAMERA_FPS:
                on_line(f"This machine rendered the cameras at {row.camera_fps:g} frames a "
                        f"second (a robot's run at {CONTROL_HZ}): the model planned on old "
                        "frames, so this score is not the model's.")
            elif (real_time and row.actions_per_s is not None
                  and row.actions_per_s < SLOW_WORLD * CONTROL_HZ):
                on_line(f"The world ran at {row.actions_per_s:g} actions a second, well under "
                        f"the model's {CONTROL_HZ}: each plan had more time than a robot gives "
                        "it. Close other work on this machine and run again.")
    finally:
        try:
            if policy is not None:
                policy.close()
        finally:
            env.close()
    summary["episodes"] = len(rows)
    summary["successes"] = sum(row.success for row in rows)
    if root is not None:
        (root / "summary.json").write_text(json.dumps(summary, indent=2))
    if len(rows) > 1:
        on_line(f"ABC {task_suite}: {summary['successes']}/{summary['episodes']} "
                "episodes succeeded")
    if json_output:
        on_line(json.dumps(summary, sort_keys=True))
    return summary


def _action_rate(result: Any) -> float | None:
    """Actions a second once the first plan had arrived: 30 when the world kept real time."""
    moving_s = result.elapsed_s - result.startup_wait_ms / 1000.0
    return round(result.actions / moving_s, 1) if moving_s > 0 else None


def _connect_options(model: str, *, region: str | None, keep_warm: int, transport: str,
                     steady_send: bool | int | None) -> dict:
    """What `dreamscale run yam` asks of its session, for the same model."""
    from dreamscale.policy.deployment import follows_session_contract
    from dreamscale.policy.runtime.contract import runtime_contract_for_model

    options: dict[str, Any] = {
        "region": region or "available", "keep_warm": keep_warm, "transport": transport,
        # A catalog model on its owner's deployments runs at the rate its session says.
        "control_hz": (None if follows_session_contract(model)
                       else int(runtime_contract_for_model(model).action_hz)),
    }
    if steady_send:
        options["steady_send"] = steady_send
    return options
