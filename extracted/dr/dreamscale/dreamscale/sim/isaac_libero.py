"""Isaac 0.5 on LIBERO (`dreamscale sim libero --model isaac-0.5-libero`; DSL-457).

Perceptron's own LIBERO protocol for ``PerceptronAI/Isaac-0.5-LIBERO`` (LeRobot ``lerobot_eval``
at 7c129e with its ``LiberoProcessorStep``) over a Dreamscale session:

- the cameras are LIBERO's agent view and wrist view at 256 px, each rotated 180 degrees as
  LeRobot's processor rotates them, sent under the deployment's own camera keys (matched by
  view: ``primary`` the agent view, ``wrist`` the wrist);
- the state is LeRobot's 8 values: end-effector position, its axis-angle and the two finger
  joints;
- after LIBERO's reset the arm settles for 50 no-op steps, then the model plans a chunk of 10
  of which the episode plays 8, synchronously (``predict``, then 8 env steps), at LIBERO's
  20 Hz;
- each observation is stamped with the episode's sim time (env step / 20 Hz), so the prompt's
  timestamp is the frame clock Perceptron's policy keeps, whatever the round trip took; the
  clock's origin is set back by the episode's whole budget, so no stamp is in the future.

The server picks the suite's normalization from the instruction (LIBERO's own task text).
"""

from __future__ import annotations

import json
import time
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np

# The catalog models this runner serves: Isaac 0.5 LIBERO, by its public name or its id.
MODELS = ("isaac-0.5-libero", "isaac05-libero")
ENV_HZ = 20
STEP_NS = 1_000_000_000 // ENV_HZ
IMAGE_SIZE = 256
# Perceptron's eval settles 50 steps after LIBERO's reset (num_steps_wait); the SDK's env
# settles NUM_STEPS_WAIT of them itself.
SETTLE_STEPS = 50
DUMMY_ACTION = [0.0] * 6 + [-1.0]
# LIBERO's per-suite step limits (env steps at 20 Hz, after settling).
MAX_STEPS = {"libero_spatial": 220, "libero_object": 280, "libero_goal": 300, "libero_10": 520}


def is_isaac_libero(model: str | None) -> bool:
    return (model or "").removeprefix("dreamscale/") in MODELS


def upright(frame: Any) -> np.ndarray:
    """LeRobot's LIBERO frame: the render rotated 180 degrees."""
    return np.ascontiguousarray(np.asarray(frame, dtype=np.uint8)[::-1, ::-1])


def camera_frames(env: Any, obs: dict, cameras: Any) -> dict[str, np.ndarray]:
    """Each deployment camera's frame, by its view (agent view: ``primary``; wrist: ``wrist``)."""
    frames = {"primary": env.agent_frame(obs), "wrist": env.wrist_frame(obs)}
    out = {}
    for camera in cameras:
        if camera.view not in frames:
            raise ValueError(f"the deployment's camera {camera.key!r} is view {camera.view!r}; "
                             "LIBERO has the primary (agent) and wrist views")
        out[camera.key] = upright(frames[camera.view])
    return out


def settle(env: Any) -> dict:
    """Reset, then the no-op steps Perceptron's eval takes before the policy drives."""
    from dreamscale.sim.runtime import NUM_STEPS_WAIT

    obs = env.reset()
    for _ in range(max(0, SETTLE_STEPS - NUM_STEPS_WAIT)):
        obs, _ = env.step(DUMMY_ACTION)
    return obs


@dataclass
class EpisodeResult:
    success: bool
    steps: int
    chunks: int
    seconds: float
    task: str
    suite: str
    task_id: int
    seed: int
    connect_s: float
    round_trip_ms_p50: float | None = None
    round_trip_ms_p95: float | None = None
    video: str | None = None

    def as_json(self) -> dict:
        return {key: getattr(self, key) for key in self.__dataclass_fields__}


def run_episode(env: Any, policy: Any, *, instruction: str, max_steps: int,
                frames: list | None = None, show: Callable[[dict], None] | None = None,
                clock: Callable[[], int] = time.time_ns) -> tuple[bool, int, list[float]]:
    """One episode: (success, env steps, each chunk's round trip in ms). ``show`` gets each
    observation the episode reaches (the viewer's frame)."""
    from dreamscale import robot

    obs = settle(env)
    if show is not None:
        show(obs)
    cameras = policy.deployment.cameras
    # The episode's sim clock, its origin early enough that no step's stamp is in the future.
    t0 = clock() - max_steps * STEP_NS
    trips: list[float] = []
    step = 0
    while step < max_steps:
        observation = robot.observe(cameras=camera_frames(env, obs, cameras),
                                    state=env.proprio(obs), capture_time_ns=t0 + step * STEP_NS)
        began = time.perf_counter()
        chunk = policy.predict(observation, instruction)
        trips.append((time.perf_counter() - began) * 1e3)
        for action in chunk.actions:
            if frames is not None:
                frames.append(upright(env.agent_frame(obs)))
            obs, done = env.step([float(v) for v in action])
            step += 1
            if show is not None:
                show(obs)
            if done:
                return True, step, trips
            if step >= max_steps:
                break
    return False, step, trips


def run_isaac_libero(*, model: str, task_suite: str, task_id: int, task_seed: int = 0,
                     max_steps: int | None = None, region: str | None = None,
                     json_output: bool = False, output_root: str | None = None,
                     view: bool = False, env_factory: Callable[..., Any] | None = None,
                     connect: Callable[..., Any] | None = None,
                     preview: Callable[[Any], tuple[Callable, Callable]] | None = None,
                     print_fn: Callable[[str], None] = print, **_ignored: Any) -> EpisodeResult:
    """One LIBERO episode of the Isaac 0.5 LIBERO catalog model, Perceptron's protocol.
    ``view`` shows it in the local LIBERO viewer window (``preview(env)``: its show and close;
    by default run_sim's window)."""
    if env_factory is None:
        from dreamscale.sim.sim_arm import _default_env_factory as env_factory
    if connect is None:
        import dreamscale

        connect = dreamscale.connect
    env = env_factory(task_suite=task_suite, task_id=int(task_id), task_seed=int(task_seed),
                      control_freq=ENV_HZ, env_resolution=IMAGE_SIZE)
    instruction = str(getattr(env, "task_description", "")).strip()
    steps_limit = max_steps or MAX_STEPS.get(task_suite, 300)
    began = time.monotonic()
    policy = connect(model.removeprefix("dreamscale/"),
                     **({"region": region} if region else {"region": "available"}))
    connect_s = time.monotonic() - began
    frames: list | None = [] if output_root else None
    from dreamscale.sim.sim_arm import libero_viewer

    show, close_view = libero_viewer(env, view and not json_output, preview, print_fn)
    try:
        began = time.monotonic()
        success, steps, trips = run_episode(env, policy, instruction=instruction,
                                            max_steps=steps_limit, frames=frames, show=show)
        seconds = time.monotonic() - began
    finally:
        try:
            policy.close()
        finally:
            try:
                env.close()
            finally:
                close_view()
    video = None
    if frames:
        video = _write_video(Path(output_root), task_suite, int(task_id), success, frames)
    # The first chunk prepares the instruction on the server; the rest are steady.
    steady = trips[1:] or trips
    p50 = round(float(np.percentile(steady, 50)), 1) if steady else None
    p95 = round(float(np.percentile(steady, 95)), 1) if steady else None
    result = EpisodeResult(success, steps, len(trips), round(seconds, 1), instruction,
                           task_suite, int(task_id), int(task_seed), round(connect_s, 1),
                           p50, p95, video)
    if json_output:
        print_fn(json.dumps(result.as_json()))
    else:
        print_fn(f"{'✓ Success' if success else '✗ Not done'}: {instruction} "
                 f"({steps} steps at {ENV_HZ} Hz, {len(trips)} chunks, round trip p50 "
                 f"{p50} ms, {seconds:.0f} s)")
    return result


def _write_video(root: Path, suite: str, task_id: int, success: bool, frames: list) -> str | None:
    try:
        import imageio
    except ImportError:
        return None
    root.mkdir(parents=True, exist_ok=True)
    path = root / f"isaac_{suite}_{task_id}_{'ok' if success else 'fail'}.mp4"
    try:  # the episode's video is a by-product: a writer that fails costs it, not the run
        imageio.mimwrite(path, frames, fps=ENV_HZ, codec="libx264")
    except Exception:  # noqa: BLE001
        return None
    return str(path)
