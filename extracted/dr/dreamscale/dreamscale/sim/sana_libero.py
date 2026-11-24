"""SANA-Robot-AR LIBERO (`dreamscale sim libero --model sana-robot-ar-libero [--mode async]`;
DSL-472).

The authors' LIBERO loop (``NVlabs/Sana`` ``eval/libero``) over a Dreamscale session whose unit
keeps the episode (``dreamscale_core.sana_robot_ar_libero``):

- LIBERO settles for 10 steps with the controller on deltas and the gripper open (the SDK's
  reset), then the controller takes absolute targets (``use_delta = False``), as the authors'
  evaluator switches it;
- the cameras are the agent and wrist views at 256 px, rotated 180 degrees; the state is the
  arm's joints and fingers, the grip site's pose and the arm base's pose in the world;
- a request goes every 16 executed steps through ``predict(observation, past_observations=...)``:
  the observations the robot executed since the last request, whose every 4th step's frames go
  ahead keyed by the step, so the unit composes each window;
- each answer is 32 absolute commands for the grip site. ``sync`` waits for every chunk (the
  simulation pauses) and runs rows 0-15; ``async`` sends the next request when 16 rows are left
  and keeps running them, then runs the new chunk's rows 16-31 (chunk 0: all 32); a chunk still on
  its way when they run out pauses the simulation, so the model's step clock stays the robot's.
"""

from __future__ import annotations

import json
import time
from collections import deque
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
from dreamscale_core.sana_robot_ar_libero import (
    ACTION_HZ,
    CAMERA_KEYS,
    FRAME_STRIDE,
    IMAGE_SIZE,
    MODEL_ID,
    MODES,
    PERIOD,
    executed_rows,
)

MODELS = (MODEL_ID,)
STEP_S = 1.0 / ACTION_HZ
# LIBERO's per-suite step limits (executed steps at 20 Hz, after settling).
MAX_STEPS = {"libero_spatial": 220, "libero_object": 280, "libero_goal": 300, "libero_10": 520}


def is_sana_libero(model: str | None) -> bool:
    return (model or "").removeprefix("dreamscale/") in MODELS


def upright(frame: Any) -> np.ndarray:
    """A LIBERO render rotated 180 degrees, as the model was trained on it."""
    return np.ascontiguousarray(np.asarray(frame, dtype=np.uint8)[::-1, ::-1])


def _raw(env: Any) -> Any:
    raw = getattr(env, "_raw_env", None)
    return raw() if callable(raw) else env


def use_absolute_targets(env: Any, absolute: bool) -> None:
    """LIBERO's OSC_POSE controller reads commands as absolute targets, or as deltas."""
    for robot in _raw(env).robots:
        robot.controller.use_delta = not absolute


def _quaternion_xyzw(matrix: Any) -> list[float]:
    from scipy.spatial.transform import Rotation

    rotation = Rotation.from_matrix(np.asarray(matrix, np.float64).reshape(3, 3))
    return [float(v) for v in rotation.as_quat()]


def state(env: Any, obs: dict) -> list[float]:
    """The model's 23 state values: joints, fingers, the grip site's and the arm base's poses
    in the world (``dreamscale_core.sana_robot_ar_libero.STATE_FIELDS``)."""
    raw = _raw(env)
    robot, sim = raw.robots[0], raw.sim
    sim.forward()  # the poses of the current joints, as the authors' controller_frames reads them
    site = robot.eef_site_id
    base = sim.model.body_name2id(robot.robot_model.naming_prefix + "link0")
    return [
        *map(float, np.asarray(obs["robot0_joint_pos"], np.float64)),
        *map(float, np.asarray(obs["robot0_gripper_qpos"], np.float64)),
        *map(float, sim.data.site_xpos[site]), *_quaternion_xyzw(sim.data.site_xmat[site]),
        *map(float, sim.data.body_xpos[base]), *_quaternion_xyzw(sim.data.body_xmat[base]),
    ]


def cameras(env: Any, obs: dict) -> dict[str, np.ndarray]:
    return {CAMERA_KEYS[0]: upright(env.agent_frame(obs)),
            CAMERA_KEYS[1]: upright(env.wrist_frame(obs))}


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
    mode: str
    connect_s: float
    round_trip_ms_p50: float | None = None
    round_trip_ms_p95: float | None = None
    paused_ms: float = 0.0
    video: str | None = None

    def as_json(self) -> dict:
        return {key: getattr(self, key) for key in self.__dataclass_fields__}


def run_episode(env: Any, policy: Any, *, instruction: str, max_steps: int, mode: str,
                real_time: bool = True, frames: list | None = None,
                show: Callable[[dict], None] | None = None,
                sleep: Callable[[float], None] = time.sleep,
                clock: Callable[[], float] = time.monotonic) -> dict:
    """One episode on a fresh env: success, executed steps, each request's round trip and the
    time the simulation paused for a chunk."""
    from dreamscale import robot

    if mode not in MODES:
        raise ValueError(f"mode is one of {', '.join(MODES)}")
    obs = env.reset()
    use_absolute_targets(env, True)
    if show is not None:
        show(obs)
    trips: list[float] = []
    executor = ThreadPoolExecutor(max_workers=1, thread_name_prefix="sana-request")
    rendered: dict[str, np.ndarray] = {}

    def observe(step: int) -> Any:
        # Frames only matter on the steps the unit reads (every 4th); the state on every one.
        if step % FRAME_STRIDE == 0 or not rendered:
            rendered.update(cameras(env, obs))
        return robot.observation(cameras=dict(rendered), state=state(env, obs))

    def ask(observation: Any, past: list) -> np.ndarray:
        began = time.perf_counter()
        chunk = policy.predict(observation, instruction, past_observations=past)
        trips.append((time.perf_counter() - began) * 1e3)
        return np.asarray([[float(v) for v in row] for row in chunk.actions], dtype=np.float64)

    def rows_of(answer: np.ndarray, chunk: int) -> list:
        return [answer[i] for i in executed_rows(chunk, mode)]

    queue: deque = deque()
    executed: list = []  # the observations the robot executed from since the last request
    pending: deque = deque()  # async: the chunks requested and not yet running
    chunk = 0
    step = 0
    paused = 0.0
    success = False
    seconds = 0.0

    def wait(future_or_call):
        nonlocal paused, origin
        waited = clock()
        answer = future_or_call()
        stalled = clock() - waited
        paused += stalled
        origin += stalled  # the simulation paused: real time resumes from here
        return answer

    try:
        first = observe(0)
        queue.extend(rows_of(ask(first, []), 0))
        started = origin = clock()
        while step < max_steps:
            current = first if step == 0 else observe(step)
            if step and step % PERIOD == 0:
                past, executed = executed, []
                if mode == "async":
                    # Planned while the robot runs the rows it has left.
                    pending.append(executor.submit(ask, current, past))
                else:
                    answer = wait(lambda current=current, past=past: ask(current, past))
                    chunk += 1
                    queue.extend(rows_of(answer, chunk))
            if not queue:
                answer = wait(pending.popleft().result)
                chunk += 1
                queue.extend(rows_of(answer, chunk))
            executed.append(current)
            if frames is not None:
                frames.append(upright(env.agent_frame(obs)))
            obs, done = env.step([float(v) for v in queue.popleft()])
            step += 1
            if show is not None:
                show(obs)
            if done:
                success = True
                break
            if real_time:
                sleep(max(0.0, origin + step * STEP_S - clock()))
        seconds = clock() - started
    finally:
        for future in pending:
            future.cancel()
        executor.shutdown(wait=True, cancel_futures=True)
    return {"success": success, "steps": step, "chunks": len(trips), "trips": trips,
            "paused_ms": paused * 1e3, "seconds": seconds}


def run_sana_libero(*, model: str, task_suite: str, task_id: int, task_seed: int = 0,
                    mode: str = "sync", max_steps: int | None = None, region: str | None = None,
                    json_output: bool = False, output_root: str | None = None,
                    view: bool = False, env_factory: Callable[..., Any] | None = None,
                    connect: Callable[..., Any] | None = None,
                    preview: Callable[[Any], tuple[Callable, Callable]] | None = None,
                    print_fn: Callable[[str], None] = print, **_ignored: Any) -> EpisodeResult:
    """One LIBERO episode of SANA-Robot-AR LIBERO, the authors' loop, sync or async. ``view``
    shows it in the local LIBERO viewer window."""
    if mode not in MODES:
        raise ValueError(f"--mode is one of {', '.join(MODES)}")
    if env_factory is None:
        from dreamscale.sim.sim_arm import _default_env_factory as env_factory
    if connect is None:
        import dreamscale

        connect = dreamscale.connect
    env = env_factory(task_suite=task_suite, task_id=int(task_id), task_seed=int(task_seed),
                      control_freq=ACTION_HZ, env_resolution=IMAGE_SIZE)
    instruction = str(getattr(env, "task_description", "")).strip()
    steps_limit = max_steps or MAX_STEPS.get(task_suite, 300)
    began = time.monotonic()
    policy = connect(model.removeprefix("dreamscale/"),
                     **({"region": region} if region else {}))
    connect_s = time.monotonic() - began
    frames: list | None = [] if output_root else None
    from dreamscale.sim.sim_arm import libero_viewer

    show, close_view = libero_viewer(env, view and not json_output, preview, print_fn)
    try:
        episode = run_episode(env, policy, instruction=instruction, max_steps=steps_limit,
                              mode=mode, frames=frames, show=show)
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
        video = _write_video(Path(output_root), task_suite, int(task_id), episode["success"],
                             frames)
    # The first request opens the episode on the unit; the rest are steady.
    steady = episode["trips"][1:] or episode["trips"]
    p50 = round(float(np.percentile(steady, 50)), 1) if steady else None
    p95 = round(float(np.percentile(steady, 95)), 1) if steady else None
    result = EpisodeResult(episode["success"], episode["steps"], episode["chunks"],
                           round(episode["seconds"], 1), instruction, task_suite, int(task_id),
                           int(task_seed), mode, round(connect_s, 1), p50, p95,
                           round(episode["paused_ms"], 1), video)
    if json_output:
        print_fn(json.dumps(result.as_json()))
    else:
        print_fn(f"{'✓ Success' if result.success else '✗ Not done'}: {instruction} "
                 f"({result.steps} steps at {ACTION_HZ} Hz, {mode}, {result.chunks} chunks, "
                 f"round trip p50 {p50} ms, paused {result.paused_ms / 1e3:.1f} s, "
                 f"{result.seconds:.0f} s)")
    return result


def _write_video(root: Path, suite: str, task_id: int, success: bool, frames: list) -> str | None:
    try:
        import imageio
    except ImportError:
        return None
    root.mkdir(parents=True, exist_ok=True)
    path = root / f"sana_{suite}_{task_id}_{'ok' if success else 'fail'}.mp4"
    try:  # the episode's video is a by-product: a writer that fails costs it, not the run
        imageio.mimwrite(path, frames, fps=ACTION_HZ, codec="libx264")
    except Exception:  # noqa: BLE001
        return None
    return str(path)
