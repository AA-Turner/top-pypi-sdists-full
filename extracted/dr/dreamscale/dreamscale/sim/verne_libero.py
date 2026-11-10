"""Verne V0.5 on LIBERO (`dreamscale sim libero --model verne-v0.5-libero`; DSL-400 C4).

Verne's own LIBERO loop (vernerobotics/v0.5 ``examples/libero/main.py`` @ 91ed7ed) over a
Dreamscale session. Verne plans 30 Hz absolute end-effector poses; LIBERO's controller takes
20 Hz OSC_POSE deltas:

- the robot is the right arm: its wrist view is camera_1 and the agent view camera_2, both
  flipped upright (the renderer draws them upside down);
- its state is the OSC controller's goal in force, not the measured hand, at the model's tool
  axes (``TOOL_AXES``), and a jaw that is open or shut, because LIBERO's training data holds
  the goal;
- each 20 Hz env step drives toward the plan at the next env tick, ``t + 0.05`` s: 1.5 model
  steps per env step, so ``next_action`` runs once or twice per env step and the target is
  interpolated between the two actions around that time (position linear, rotation slerp, jaw
  linear), as upstream's ``chunk.at(t + STEP_S)``;
- the target becomes the OSC_POSE action that moves the goal there from the measured pose
  (``Controller.action``, upstream's).
"""

from __future__ import annotations

import json
import math
import time
from collections.abc import Callable, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import numpy as np
from dreamscale_transport import verne_v05_deploy as C

# The catalog models this runner serves: Verne V0.5 LIBERO, by its public name or its id.
MODELS = ("verne-v0.5-libero", "verne-v05-libero")
# The LIBERO controller runs at 20 Hz; Verne plans at 30 Hz.
ENV_HZ = 20
STEP_S = 1.0 / ENV_HZ
MODEL_HZ = float(C.ACTION_HZ)
# The model's tool axes in the LIBERO hand frame: R_model = R_hand @ TOOL_AXES.
TOOL_AXES = np.diag([-1.0, -1.0, 1.0])
# robosuite OSC_POSE: an action of 1 moves the goal 0.05 m or 0.5 rad.
OSC_POS_SCALE_M = 0.05
OSC_ROT_SCALE_RAD = 0.5
# The two finger joints of an open Panda gripper sum to this width, m.
JAW_FULL_OPEN_M = 0.08
# Upstream's per-suite step limits (env steps at 20 Hz).
MAX_STEPS = {"libero_spatial": 220, "libero_object": 280, "libero_goal": 300, "libero_10": 520}


def is_verne_libero(model: str | None) -> bool:
    return (model or "").removeprefix("dreamscale/") in MODELS


def instruction_text(text: str) -> str:
    """One sentence with a capital first letter and one final period, as in training."""
    text = " ".join(str(text).split()).rstrip(" .,;")
    return text[:1].upper() + text[1:] + "."


def _rotation():
    from scipy.spatial.transform import Rotation

    return Rotation


class Controller:
    """Turns the policy's absolute targets into LIBERO's OSC_POSE delta actions (upstream's).

    The model reads the controller goal in force, not the measured hand pose."""

    def __init__(self, obs: dict) -> None:
        rotation = _rotation()
        self.goal_pos = np.asarray(obs["robot0_eef_pos"], dtype=np.float64)
        self.goal_rot = rotation.from_quat(obs["robot0_eef_quat"])
        fingers = obs["robot0_gripper_qpos"]
        opening = np.clip((fingers[0] - fingers[1]) / JAW_FULL_OPEN_M, 0.0, 1.0)
        self.jaw = 1.0 if opening >= 0.5 else 0.0

    def pose(self) -> np.ndarray:
        pose = np.eye(4)
        pose[:3, :3] = self.goal_rot.as_matrix() @ TOOL_AXES
        pose[:3, 3] = self.goal_pos
        return pose

    def state(self) -> list[float]:
        """Verne's 10 values for the right arm: xyz, rotation rows 0-1, jaw."""
        return [*C.row_from_pose(self.pose()).tolist(), float(self.jaw)]

    def action(self, obs: dict, target_pose: np.ndarray, target_jaw: float) -> np.ndarray:
        """The OSC_POSE action that moves the goal to the target, from the measured pose."""
        rotation = _rotation()
        pos = np.asarray(obs["robot0_eef_pos"], dtype=np.float64)
        hand = rotation.from_quat(obs["robot0_eef_quat"])
        target_rot = rotation.from_matrix(target_pose[:3, :3] @ TOOL_AXES)
        arm = np.concatenate([
            (target_pose[:3, 3] - pos) / OSC_POS_SCALE_M,
            (target_rot * hand.inv()).as_rotvec() / OSC_ROT_SCALE_RAD,
        ])
        arm = np.clip(arm, -1.0, 1.0)
        grip = 1.0 if target_jaw < 0.5 else -1.0
        # The goal the controller sets from this action; a zero rotation keeps the old one.
        self.goal_pos = pos + OSC_POS_SCALE_M * arm[:3]
        if np.any(arm[3:]):
            self.goal_rot = rotation.from_rotvec(OSC_ROT_SCALE_RAD * arm[3:]) * hand
        self.jaw = 1.0 if grip < 0 else 0.0
        return np.concatenate([arm, [grip]])


def target_index(env_step: int) -> float:
    """The model step (30 Hz, from the episode's first action) at env step ``env_step``'s next
    tick, ``(k + 1) * 0.05`` s: 1.5, 3.0, 4.5, ..."""
    return (env_step + 1) * MODEL_HZ * STEP_S


def interpolate(a: Sequence[float], b: Sequence[float], weight: float) -> tuple[np.ndarray, float]:
    """The pose and jaw ``weight`` of the way from action ``a`` to ``b`` (Verne's 11 values:
    xyz, rotation rows 0-1, jaw, progress): position linear, rotation slerp, jaw linear."""
    pa, pb = C.pose_from_row(a[:9]), C.pose_from_row(b[:9])
    if weight <= 0.0:
        return pa, float(a[9])
    if weight >= 1.0:
        return pb, float(b[9])
    from scipy.spatial.transform import Slerp

    rotation = _rotation()
    slerp = Slerp([0.0, 1.0], rotation.from_matrix(np.stack([pa[:3, :3], pb[:3, :3]])))
    pose = np.eye(4)
    pose[:3, :3] = slerp([weight]).as_matrix()[0]
    pose[:3, 3] = (1.0 - weight) * pa[:3, 3] + weight * pb[:3, 3]
    return pose, (1.0 - weight) * float(a[9]) + weight * float(b[9])


@dataclass
class ModelClock:
    """The session's 30 Hz clock under a 20 Hz env: ``next_action`` once per model step (each
    with the env's latest observation), keeping every action by its model step."""

    next_action: Callable[[Any], Sequence[float]]
    actions: list[tuple[float, ...]] = field(default_factory=list)

    def target(self, env_step: int, observation: Any) -> tuple[np.ndarray, float]:
        index = target_index(env_step)
        while len(self.actions) <= math.ceil(index):
            self.actions.append(tuple(float(v) for v in self.next_action(observation)))
        low = math.floor(index)
        return interpolate(self.actions[low], self.actions[min(low + 1, len(self.actions) - 1)],
                           index - low)


def observation(env: Any, obs: dict, controller: Controller, cameras: Sequence[Any]) -> Any:
    """The robot's observation: each camera its frame upright, the controller's goal as state.
    The frames come through the env (``wrist_frame``/``agent_frame``): the sim renders its
    cameras only when asked, so a step's raw observation holds none."""
    from dreamscale import robot

    frames = {"camera_1": env.wrist_frame(obs), "camera_2": env.agent_frame(obs)}
    images = {camera.key: np.ascontiguousarray(np.asarray(frames[camera.feature])[::-1])
              for camera in cameras}
    return robot.observe(cameras=images, state=controller.state())


@dataclass
class EpisodeResult:
    success: bool
    steps: int
    model_steps: int
    seconds: float
    task: str
    suite: str
    task_id: int
    seed: int
    connect_s: float
    video: str | None = None
    underruns: int | None = None

    def as_json(self) -> dict:
        return {key: getattr(self, key) for key in self.__dataclass_fields__}


def run_episode(env: Any, policy: Any, *, instruction: str, max_steps: int,
                real_time: bool = True, frames: list | None = None,
                sleep: Callable[[float], None] = time.sleep) -> tuple[bool, int, int]:
    """One episode on a reset env: (success, env steps, model steps)."""
    obs = env.reset()
    controller = Controller(obs)
    cameras = policy.deployment.cameras
    clock = ModelClock(lambda o: policy.next_action(o, instruction=instruction))
    started = time.monotonic()
    for step in range(max_steps):
        model_obs = observation(env, obs, controller, cameras)
        if frames is not None:
            frames.append(np.asarray(env.agent_frame(obs))[::-1])
        pose, jaw = clock.target(step, model_obs)
        action = controller.action(obs, pose, jaw)
        obs, done = env.step(action.tolist())
        if done:
            return True, step + 1, len(clock.actions)
        if real_time:  # the controller's rate, so the session sees a robot's timing
            sleep(max(0.0, started + (step + 1) * STEP_S - time.monotonic()))
    return False, max_steps, len(clock.actions)


def run_verne_libero(*, model: str, task_suite: str, task_id: int, task_seed: int = 0,
                     max_steps: int | None = None, region: str | None = None,
                     real_time: bool = True, json_output: bool = False,
                     output_root: str | None = None, env_factory: Callable[..., Any] | None = None,
                     connect: Callable[..., Any] | None = None,
                     print_fn: Callable[[str], None] = print, **_ignored: Any) -> EpisodeResult:
    """One LIBERO episode of the Verne V0.5 LIBERO catalog model, upstream's protocol."""
    if env_factory is None:
        from dreamscale.sim.sim_arm import _default_env_factory as env_factory
    if connect is None:
        import dreamscale

        connect = dreamscale.connect
    env = env_factory(task_suite=task_suite, task_id=int(task_id), task_seed=int(task_seed),
                      control_freq=ENV_HZ, env_resolution=C.IMAGE_SIZE)
    instruction = instruction_text(getattr(env, "task_description", ""))
    steps_limit = max_steps or MAX_STEPS.get(task_suite, 300)
    began = time.monotonic()
    policy = connect(model.removeprefix("dreamscale/"),
                     **({"region": region} if region else {"region": "available"}))
    connect_s = time.monotonic() - began
    frames: list | None = [] if output_root else None
    try:
        began = time.monotonic()
        success, steps, model_steps = run_episode(env, policy, instruction=instruction,
                                                  max_steps=steps_limit, real_time=real_time,
                                                  frames=frames)
        seconds = time.monotonic() - began
        stats = getattr(policy, "runtime_stats", None)
    finally:
        try:
            policy.close()
        finally:
            env.close()
    video = None
    if frames:
        video = _write_video(Path(output_root), task_suite, int(task_id), success, frames)
    result = EpisodeResult(success, steps, model_steps, round(seconds, 1), instruction,
                           task_suite, int(task_id), int(task_seed), round(connect_s, 1), video,
                           getattr(stats, "underruns", None))
    if json_output:
        print_fn(json.dumps(result.as_json()))
    else:
        print_fn(f"{'✓ Success' if success else '✗ Not done'}: {instruction} "
                 f"({steps} steps at {ENV_HZ} Hz, {model_steps} Verne actions at 30 Hz, "
                 f"{seconds:.0f} s)")
    return result


def _write_video(root: Path, suite: str, task_id: int, success: bool, frames: list) -> str | None:
    try:
        import imageio
    except ImportError:
        return None
    root.mkdir(parents=True, exist_ok=True)
    path = root / f"verne_{suite}_{task_id}_{'ok' if success else 'fail'}.mp4"
    try:  # the episode's video is a by-product: a writer that fails costs it, not the run
        imageio.mimwrite(path, frames, fps=ENV_HZ, codec="libx264")
    except Exception:  # noqa: BLE001
        return None
    return str(path)
