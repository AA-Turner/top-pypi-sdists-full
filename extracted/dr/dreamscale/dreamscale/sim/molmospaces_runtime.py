"""Pinned MolmoSpaces native runtimes, independent of LIBERO/RoboCasa packages."""

from __future__ import annotations

import platform
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np

from dreamscale.config import dreamscale_home

from .molmospaces_catalog import BENCHMARKS, REVISION
from .native_runtime import NativeSimProcess, _source_checkout, write_native_video

RUNTIME_ROOT = dreamscale_home() / "sim" / "molmospaces" / REVISION[:12]


def ensure_molmospaces_runtime(*, renderer="classic", root=RUNTIME_ROOT, on_line=print):
    if renderer not in ("classic", "filament"):
        raise ValueError("Unknown MolmoSpaces renderer")
    uv = shutil.which("uv")
    if uv is None:
        raise RuntimeError("MolmoSpaces needs uv to prepare its runtime. Install uv and retry.")
    root.mkdir(parents=True, exist_ok=True)
    import fcntl

    with (root / ".install.lock").open("w") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        source = root / "source"
        _source_checkout("allenai/molmospaces", REVISION, source)
        runtime = root / renderer
        python = runtime / "venv" / "bin" / "python"
        ready = runtime / ".ready-v1"
        if not ready.exists():
            on_line(f"Preparing MolmoSpaces {renderer} runtime (first run only)…")
            if not python.exists():
                subprocess.run([uv, "venv", "--python", "3.11", str(runtime / "venv")], check=True)
            subprocess.run(
                [uv, "pip", "install", "--python", str(python), f"{source}[mujoco]", "av>=15,<19"],
                check=True,
            )
            if renderer == "filament":
                suffix = (
                    "macosx_11_0_arm64"
                    if sys.platform == "darwin" and platform.machine() == "arm64"
                    else "manylinux_2_27_x86_64.manylinux_2_28_x86_64"
                    if sys.platform == "linux" and platform.machine() == "x86_64"
                    else None
                )
                if suffix is None:
                    raise RuntimeError(
                        "MolmoSpaces Filament supports Apple Silicon macOS or "
                        "x86_64 Linux. Select pick-v1.5 for classic MuJoCo."
                    )
                wheel = source / "bin" / "wheels" / f"mujoco-3.7.1-cp311-cp311-{suffix}.whl"
                subprocess.run(
                    [uv, "pip", "install", "--python", str(python), str(wheel)], check=True
                )
            check = (
                "import mujoco; assert getattr(mujoco, 'mjRENDERER', 'classic') == "
                f"{renderer!r}; "
                "from molmo_spaces.evaluation.benchmark_schema import load_all_episodes; "
                "from molmo_spaces.tasks.json_eval_task_sampler "
                "import JsonEvalTaskSampler"
            )
            subprocess.run([str(python), "-c", check], check=True)
            ready.touch()
        return python


class MolmoSpacesSimEnv(NativeSimProcess):
    def __init__(self, *, suite: str, task_id: int, seed=0, python=None):
        benchmark = BENCHMARKS[suite]
        self.python = python or ensure_molmospaces_runtime(renderer=benchmark.renderer)
        super().__init__(
            python=self.python,
            script=Path(__file__).with_name("molmospaces_process.py"),
            root=RUNTIME_ROOT,
            label="MolmoSpaces",
            environment={"MLSPACES_ASSETS_DIR": str(RUNTIME_ROOT / "assets")},
            setup={"suite": suite, "task_id": task_id, "seed": seed},
        )
        self.task_description = self._initial["instruction"]
        self.episode_count = self._initial["episode_count"]
        self.horizon_steps = self._initial["horizon_steps"]
        self.benchmark_info = self._initial["benchmark_info"]
        self._last = self._initial

    def reset(self):
        if self._initial is not None:
            result, self._initial = self._initial, None
        else:
            result = self._request({"op": "reset"}, timeout_s=1800)
        self._last = result
        self.benchmark_info = result["benchmark_info"]
        return result

    def step(self, action):
        result = self._request({"op": "step", "action": list(action)})
        self._last = result[0]
        self.benchmark_info = self._last["benchmark_info"]
        return result

    def hold_action(self):
        return [*self._last["joint_positions"], self._last["gripper"]]

    def observation_inputs(self, obs):
        return {
            "exterior_frame": obs["exterior"],
            "second_exterior_frame": obs["exterior"],
            "wrist_frame": obs["wrist"],
            "joint_positions": obs["joint_positions"],
            "gripper": obs["gripper"],
        }

    def agent_frame(self, obs):
        return obs["exterior"]

    def wrist_frame(self, obs):
        return obs["wrist"]

    def policy_preview_frame(self, obs):
        return np.concatenate([obs["exterior"], obs["wrist"]], axis=1)

    def write_video(self, path, frames, fps):
        write_native_video(self.python, path, frames, fps)


def benchmark_counts(suites, python):
    process = NativeSimProcess(
        python=python,
        script=Path(__file__).with_name("molmospaces_process.py"),
        root=RUNTIME_ROOT,
        label="MolmoSpaces",
        setup={"catalog_only": True, "suites": list(suites)},
        environment={"MLSPACES_ASSETS_DIR": str(RUNTIME_ROOT / "assets")},
    )
    try:
        return process._initial
    finally:
        process.close()
