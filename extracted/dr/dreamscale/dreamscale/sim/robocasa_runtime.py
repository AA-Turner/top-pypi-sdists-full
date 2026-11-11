"""Install and run RoboCasa365 independently of the user's LIBERO environment."""

from __future__ import annotations

import json
import shutil
import subprocess
import urllib.request
from collections import deque
from pathlib import Path

import numpy as np
from dreamscale_transport.robocasa import CAMERA_KEYS, ROBOCASA_REVISION, ROBOSUITE_REVISION

from dreamscale.config import dreamscale_home
from dreamscale.sim.native_runtime import NativeSimProcess, _source_checkout, write_native_video

RUNTIME_ROOT = dreamscale_home() / "sim" / "robocasa365" / ROBOCASA_REVISION[:12]
RUNTIME_REQUIREMENTS = (
    "numpy==2.2.5", "mujoco==3.3.1", "numba==0.61.2", "scipy==1.16.3",
    "opencv-python==4.11.0.86", "gymnasium==0.29.1", "h5py>=3.11,<4",
    "Pillow>=10,<12", "pyyaml>=6,<7", "imageio[pyav]>=2.36,<3", "av>=15,<19", "tqdm>=4.66,<5",
    "termcolor>=2,<4", "lxml>=5,<7", "setuptools>=75,<81", "packaging>=24,<26",
    "pygame>=2.6,<3", "pynput>=1.7,<2", "hidapi>=0.14,<1", "cloudpickle>=3,<4",
)
ASSET_PACKS = {
    "textures": "textures", "generative_textures": "generative_textures",
    "fixtures_lightwheel": "fixtures", "objects_lightwheel": "objects/lightwheel",
    "objaverse": "objects/objaverse", "aigen_objs": "objects/aigen_objs",
}



def ensure_robocasa_runtime(*, root: Path = RUNTIME_ROOT, on_line=print) -> Path:
    """Cache an isolated Python 3.12 native stack and assets; never change user packages."""
    uv = shutil.which("uv")
    if uv is None:
        raise RuntimeError("RoboCasa365 needs uv to prepare its runtime. Install uv and retry.")
    root.mkdir(parents=True, exist_ok=True)
    # Lock the cache across concurrent CLI invocations. No GPU session exists during bootstrap.
    import fcntl

    with (root / ".install.lock").open("w") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        python = root / "venv" / "bin" / "python"
        source = root / "robocasa"
        ready = root / ".runtime-ready-v3"
        if not ready.exists():
            on_line("Preparing the RoboCasa365 runtime (first run only)…")
            _source_checkout("ARISE-Initiative/robosuite", ROBOSUITE_REVISION, root / "robosuite")
            _source_checkout("robocasa/robocasa", ROBOCASA_REVISION, source)
            if not python.exists():
                subprocess.run([uv, "venv", "--python", "3.12", str(root / "venv")], check=True)
            subprocess.run([uv, "pip", "install", "--python", str(python),
                            *RUNTIME_REQUIREMENTS, str(root / "robosuite")], check=True)
            # Upstream pins a training-only LeRobot version; native sim doesn't need it.
            subprocess.run([uv, "pip", "install", "--python", str(python), "--no-deps",
                            "--editable", str(source)], check=True)
            for package in (source / "robocasa",
                            root / "venv" / "lib" / "python3.12" / "site-packages" / "robosuite"):
                macros = package / "macros_private.py"
                if not macros.exists():
                    shutil.copyfile(package / "macros.py", macros)
            ready.touch()
        assets = source / "robocasa" / "models" / "assets"
        links = json.loads((assets / "box_links" / "box_links_assets.json").read_text())
        for key, directory in ASSET_PACKS.items():
            marker = root / f".assets-{key}-ready"
            if marker.exists():
                continue
            on_line(f"Downloading RoboCasa365 {key.replace('_', ' ')} (first run only)…")
            shared = links[key]
            base, token = shared.rsplit("/s/", 1)
            destination = assets / directory
            destination.parent.mkdir(parents=True, exist_ok=True)
            archive = root / f"{key}.zip"
            urllib.request.urlretrieve(f"{base}/shared/static/{token}.zip", archive)
            from zipfile import ZipFile

            with ZipFile(archive) as compressed:
                for member in compressed.infolist():
                    resolved = (destination.parent / member.filename).resolve()
                    if not resolved.is_relative_to(destination.parent.resolve()):
                        raise ValueError("unsafe RoboCasa asset archive path")
                compressed.extractall(destination.parent)
            archive.unlink()
            if not destination.is_dir() or not any(destination.iterdir()):
                raise RuntimeError(f"RoboCasa asset pack {key} did not install correctly; retry.")
            marker.touch()
        return python


class RoboCasaSimEnv(NativeSimProcess):
    """Same episode interface as LIBERO; native MuJoCo stays on the child main thread.

    ``control="droid_joint"`` drives the PandaOmron's Franka arm with absolute joint
    targets at 15 Hz from DROID's home pose and reports DROID's three camera views,
    seven joints and normalized gripper; the default keeps RoboCasa's delta-EEF API.

    ``camera_history`` (the ticks back of each window frame, oldest first) makes each policy
    observation that window of every camera, with the current state: before the episode has
    reached a tick, its first frame stands in, as upstream's training windows clamp to the
    episode's start. Without it, each observation is the four-frame, two-tick window and the
    states that go with it (Xiaomi's and RLDX-1's).
    """

    control = "eef_delta"
    camera_history: tuple[int, ...] | None = None

    def __init__(self, *, task: str, seed: int = 0, python: Path | None = None,
                 control: str = "eef_delta", camera_history: tuple[int, ...] | None = None):
        if control not in ("eef_delta", "droid_joint"):
            raise ValueError("RoboCasa365 control must be eef_delta or droid_joint")
        if camera_history is not None and (
                control != "eef_delta" or not camera_history
                or any(not isinstance(tick, int) or tick < 0 for tick in camera_history)
                or list(camera_history) != sorted(camera_history, reverse=True)):
            raise ValueError("a RoboCasa365 camera history is its ticks back, oldest first")
        self.camera_history = None if camera_history is None else tuple(camera_history)
        self.python = python or ensure_robocasa_runtime()
        self.control = control
        super().__init__(python=self.python, script=Path(__file__).with_name("robocasa_process.py"),
            root=RUNTIME_ROOT, label="RoboCasa365",
            setup={"task": task, "seed": seed, "control": control})
        self.task_description = self._initial["instruction"]
        self._last_gripper = -1.0
        self._history = deque(maxlen=7 if self.camera_history is None
                              else self.camera_history[0] + 1)
        self._last = self._initial

    def reset(self):
        self._last_gripper = -1.0
        self._history.clear()
        if self._initial is not None:
            result, self._initial = self._initial, None
        else:
            result = self._request({"op": "reset"})
        self.task_description = result["instruction"]
        self._history.append(result)
        self._last = result
        return result

    def step(self, action):
        result = self._request({"op": "step", "action": list(action)})
        if self.control == "eef_delta":
            self._last_gripper = float(action[6])
        self._history.append(result[0])
        self._last = result[0]
        return result

    def hold_action(self):
        if self.control == "droid_joint":
            return [*self._last["joint_positions"], self._last["gripper"]]
        return [0.0] * 6 + [self._last_gripper] + [0.0] * 4 + [-1.0]

    def observation_inputs(self, obs):
        if self.control == "droid_joint":
            return {
                "exterior_frame": obs["images"][CAMERA_KEYS[0]],
                "second_exterior_frame": obs["images"][CAMERA_KEYS[1]],
                "wrist_frame": obs["images"][CAMERA_KEYS[2]],
                "joint_positions": obs["joint_positions"],
                "gripper": obs["gripper"],
            }
        history = list(self._history)
        if not history:
            raise RuntimeError("Reset the simulator before requesting a policy observation")
        if self.camera_history is not None:
            window = [history[max(0, len(history) - 1 - tick)] for tick in self.camera_history]
            return {"images": {key: np.stack([item["images"][key] for item in window])
                               for key in CAMERA_KEYS},
                    "robot_state": obs["state"]}
        sampled = [history[max(0, len(history) - 1 - (3 - index) * 2)] for index in range(4)]
        return {"images": {key: np.stack([item["images"][key] for item in sampled])
                           for key in CAMERA_KEYS},
                "robot_state": obs["state"],
                "robot_state_history": [item["state"] for item in sampled]}

    def agent_frame(self, obs):
        return obs["images"][CAMERA_KEYS[0]]

    def wrist_frame(self, obs):
        return obs["images"][CAMERA_KEYS[2]]

    def policy_preview_frame(self, obs):
        return np.concatenate([obs["images"][key] for key in CAMERA_KEYS], axis=1)


def write_sim_video(path: Path, frames: np.ndarray, fps: int) -> None:
    """Use the isolated native runtime's encoder without parent SDK media imports."""
    write_native_video(RUNTIME_ROOT / "venv" / "bin" / "python", path, frames, fps)
