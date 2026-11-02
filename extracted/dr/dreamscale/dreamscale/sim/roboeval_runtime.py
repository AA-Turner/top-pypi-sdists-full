"""Install and run RoboEval independently of the user's Python environment."""

from __future__ import annotations

import hashlib
import shutil
import subprocess
import urllib.request
from pathlib import Path

import numpy as np
from dreamscale_transport.messages import BimanualEndEffectorState
from dreamscale_transport.rho_checkpoints import RHO_CHECKPOINTS, RHO_ROBOEVAL_MODEL_ID

from dreamscale.config import dreamscale_home
from dreamscale.sim.native_runtime import NativeSimProcess, write_native_video
from dreamscale.sim.roboeval_catalog import FAMILIES

# Dreamscale-Labs/dreamscale-roboeval: upstream RoboEval packaged as one wheel
# (Panda models included, no git dependencies).
ROBOEVAL_VERSION = "0.1.0.post1"
ROBOEVAL_WHEEL = f"dreamscale_roboeval-{ROBOEVAL_VERSION}-py3-none-any.whl"
ROBOEVAL_WHEEL_URL = (
    "https://github.com/Dreamscale-Labs/dreamscale-roboeval/releases/download/"
    f"v{ROBOEVAL_VERSION}/{ROBOEVAL_WHEEL}"
)
ROBOEVAL_WHEEL_SHA256 = "e74d77aa673e02808e66b8f07995359be4b418d83d0e2c2adfb25a1c7c9fb360"
RUNTIME_ROOT = dreamscale_home() / "sim" / "roboeval" / ROBOEVAL_VERSION
# Viewer window and --output-root video; the wheel pins the simulator stack itself.
RUNTIME_REQUIREMENTS = ("opencv-python==4.11.0.86", "av>=15,<19")
CHECKPOINT = RHO_CHECKPOINTS[RHO_ROBOEVAL_MODEL_ID]


def ensure_roboeval_runtime(*, root: Path = RUNTIME_ROOT, on_line=print) -> Path:
    """Cache an isolated Python 3.12 RoboEval runtime; never change user packages."""
    uv = shutil.which("uv")
    if uv is None:
        raise RuntimeError("RoboEval needs uv to prepare its runtime. Install uv and retry.")
    root.mkdir(parents=True, exist_ok=True)
    import fcntl

    with (root / ".install.lock").open("w") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        python = root / "venv" / "bin" / "python"
        ready = root / ".runtime-ready-v1"
        if not ready.exists():
            on_line("Preparing the RoboEval runtime (first run only)…")
            wheel = root / ROBOEVAL_WHEEL
            if not wheel.exists():
                partial = wheel.with_suffix(".part")
                urllib.request.urlretrieve(ROBOEVAL_WHEEL_URL, partial)
                with partial.open("rb") as source:
                    digest = hashlib.file_digest(source, "sha256").hexdigest()
                if digest != ROBOEVAL_WHEEL_SHA256:
                    partial.unlink()
                    raise RuntimeError("The RoboEval download did not match its pinned checksum; "
                                       "retry, or report this if it persists.")
                partial.rename(wheel)
            if not python.exists():
                subprocess.run([uv, "venv", "--python", "3.12", str(root / "venv")], check=True)
            subprocess.run([uv, "pip", "install", "--python", str(python),
                            str(wheel), *RUNTIME_REQUIREMENTS], check=True)
            ready.touch()
        return python


class RoboEvalSimEnv(NativeSimProcess):
    """Rho-RoboEval contract: 20-d world-frame [xyz, 6D rotation, gripper] per arm."""

    def __init__(self, *, family: str, variant: str, seed: int = 0, python: Path | None = None):
        record = FAMILIES[family]
        self.python = python or ensure_roboeval_runtime()
        super().__init__(python=self.python, script=Path(__file__).with_name("roboeval_process.py"),
            root=RUNTIME_ROOT, label="RoboEval", setup={
                "module": record.module, "variant": variant,
                "instruction": record.instruction, "seed": seed,
            })
        self.task_description = self._initial["instruction"]
        self._grippers = [0.0, 0.0]
        self._steps = 0

    def reset(self):
        # RoboEval resets with closed grippers; demonstrations start by commanding open (0).
        self._grippers = [0.0, 0.0]
        if self._initial is not None:
            result, self._initial = self._initial, None
        else:
            result = self._request({"op": "reset"})
        self.task_description = result["instruction"]
        self._state = result["state"]
        return result

    def step(self, action):
        # Plain floats: the SDK's numpy may be 2.x and the simulator's is 1.26, and
        # numpy 2 pickles do not load under numpy 1.
        obs, done = self._request({"op": "step", "action": [float(value) for value in action]})
        self._grippers = [float(action[9]), float(action[19])]
        self._state = obs["state"]
        self._steps += 1
        return _Observation(obs, self._images, self._steps), done

    def _images(self, step):
        if step != self._steps:
            raise RuntimeError("RoboEval camera frames are only available for the latest step")
        return self._request({"op": "images"})

    def hold_action(self):
        """Hold the measured pose and keep commanding the last gripper targets.

        Measured grippers are openness (1 = open); commands are 1 = close.
        """
        state = list(self._state)
        state[9], state[19] = self._grippers
        return state

    def observation_inputs(self, obs):
        state = obs["state"]
        robot_state = BimanualEndEffectorState(
            coordinate_frame=RHO_ROBOEVAL_MODEL_ID, gripper_unit="checkpoint",
            left_position=state[0:3], left_rotation_6d=state[3:9], left_gripper=state[9],
            right_position=state[10:13], right_rotation_6d=state[13:19], right_gripper=state[19],
        )
        return {"frames": tuple(obs["images"][key] for key in CHECKPOINT.camera_keys),
                "robot_state": robot_state}

    def agent_frame(self, obs):
        return obs["images"][CHECKPOINT.camera_keys[0]]

    def wrist_frame(self, obs):
        return obs["images"][CHECKPOINT.camera_keys[1]]

    def policy_preview_frame(self, obs):
        return np.concatenate([obs["images"][key] for key in CHECKPOINT.camera_keys], axis=1)


class _Observation(dict):
    """Step state, with camera frames rendered by the simulator on first access."""

    def __init__(self, data, fetch, step):
        super().__init__(data)
        self._fetch, self._step = fetch, step

    def __missing__(self, key):
        if key != "images":
            raise KeyError(key)
        self["images"] = images = self._fetch(self._step)
        return images


def write_sim_video(path: Path, frames: np.ndarray, fps: int) -> None:
    write_native_video(RUNTIME_ROOT / "venv" / "bin" / "python", path, frames, fps)
