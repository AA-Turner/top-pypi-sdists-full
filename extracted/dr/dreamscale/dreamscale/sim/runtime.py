from __future__ import annotations

import importlib
import importlib.metadata
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import time
import warnings
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import yaml

from dreamscale.config import dreamscale_home
from dreamscale.sim.timing import DEFAULT_SIM_MAX_STEPS, LIBERO_ACTION_HZ

HF_LIBERO_VERSION = "0.1.3"
CACHE_ROOT = dreamscale_home() / "sim"
LIBERO_CONFIG_ROOT = CACHE_ROOT / "libero-config"
LIBERO_ASSETS_ROOT = CACHE_ROOT / "libero-assets"
LIBERO_DATASETS_ROOT = CACHE_ROOT / "libero-datasets"

# Copied verbatim from the sandbox rollout.py (the episode loop itself is new
# code in dreamscale.sim.sim_arm — the sandbox loop spoke to a Modal HTTP service).
LIBERO_DUMMY_ACTION = [0.0] * 6 + [-1.0]
SUITE_MAX_STEPS: dict[str, int] = {
    "libero_spatial": DEFAULT_SIM_MAX_STEPS,
    "libero_object": DEFAULT_SIM_MAX_STEPS,
    "libero_goal": DEFAULT_SIM_MAX_STEPS,
    "libero_10": DEFAULT_SIM_MAX_STEPS,
    "libero_90": DEFAULT_SIM_MAX_STEPS,
}


@dataclass(frozen=True)
class LiberoInstallStatus:
    hf_libero_installed: bool
    libero_config_path: Path
    assets_path: Path | None


@dataclass(frozen=True)
class LiberoModules:
    benchmark: Any
    get_libero_path: Any
    offscreen_render_env: Any
    raw_module: Any


@dataclass(frozen=True)
class LiberoTaskHandle:
    task_suite_name: str
    task_id: int
    task: Any
    task_description: str
    env: Any
    init_states: Any


def ensure_hf_libero_installed(*, force_reinstall: bool = False) -> bool:
    if _has_expected_hf_libero_install() and not force_reinstall:
        return False

    uv = shutil.which("uv")
    if uv is None:
        raise RuntimeError(
            "The `uv` command is required to install hf-libero into the current environment."
        )

    command = [
        uv,
        "pip",
        "install",
        "--python",
        sys.executable,
        "--no-deps",
        f"hf-libero=={HF_LIBERO_VERSION}",
    ]
    subprocess.run(command, check=True)
    importlib.invalidate_caches()
    return True


def _has_expected_hf_libero_install() -> bool:
    try:
        if importlib.util.find_spec("libero.libero") is None:
            return False
    except ModuleNotFoundError:
        return False

    for distribution_name in ("hf-libero", "hf_libero"):
        try:
            return importlib.metadata.version(distribution_name) == HF_LIBERO_VERSION
        except importlib.metadata.PackageNotFoundError:
            continue
    return False


def bootstrap_libero_runtime(
    *,
    assets_path: str | None = None,
    download_assets: bool = True,
    force_reinstall: bool = False,
) -> LiberoInstallStatus:
    ensure_hf_libero_installed(force_reinstall=force_reinstall)
    config_root = _write_libero_config()

    resolved_assets = None
    if assets_path is not None:
        candidate = Path(assets_path).expanduser().resolve()
        if not candidate.exists():
            raise FileNotFoundError(f"assets path does not exist: {candidate}")
        resolved_assets = candidate
    elif download_assets:
        resolved_assets = ensure_libero_assets()

    return LiberoInstallStatus(
        hf_libero_installed=True,
        libero_config_path=config_root,
        assets_path=resolved_assets,
    )


def ensure_libero_assets(*, assets_root: Path | None = None) -> Path:
    config_root = _write_libero_config()
    modules = load_libero_modules(config_root=config_root, assets_path=None)
    target = (assets_root or LIBERO_ASSETS_ROOT).expanduser().resolve()
    target.mkdir(parents=True, exist_ok=True)
    download_utils = importlib.import_module("libero.libero.utils.download_utils")
    download_utils.download_assets_from_huggingface(str(target))
    modules.raw_module._assets_path_cache = str(target)
    return target


def load_libero_modules(
    *,
    config_root: Path | None = None,
    assets_path: str | Path | None,
) -> LiberoModules:
    root = config_root or _write_libero_config()
    os.environ["LIBERO_CONFIG_PATH"] = str(root)

    _import_robosuite()
    importlib.invalidate_caches()
    raw_module = importlib.import_module("libero.libero")

    if assets_path is not None:
        raw_module._assets_path_cache = str(Path(assets_path).expanduser().resolve())

    benchmark = importlib.import_module("libero.libero.benchmark")
    envs = importlib.import_module("libero.libero.envs")
    return LiberoModules(
        benchmark=benchmark,
        get_libero_path=raw_module.get_libero_path,
        offscreen_render_env=envs.OffScreenRenderEnv,
        raw_module=raw_module,
    )


def create_task_handle(
    *,
    task_suite_name: str,
    task_id: int,
    seed: int,
    env_resolution: int,
    assets_path: str | Path | None,
    control_freq: int = LIBERO_ACTION_HZ,
) -> LiberoTaskHandle:
    config_root = _write_libero_config()
    modules = load_libero_modules(config_root=config_root, assets_path=assets_path)
    task_suite = modules.benchmark.get_benchmark_dict()[task_suite_name]()
    task = task_suite.get_task(task_id)
    task_description = str(task.language)
    task_bddl_file = (
        Path(modules.get_libero_path("bddl_files"))
        / task.problem_folder
        / task.bddl_file
    )
    env = modules.offscreen_render_env(
        bddl_file_name=str(task_bddl_file),
        camera_heights=env_resolution,
        camera_widths=env_resolution,
        control_freq=control_freq,
    )
    env.seed(seed)
    init_states = task_suite.get_task_init_states(task_id)
    return LiberoTaskHandle(
        task_suite_name=task_suite_name,
        task_id=task_id,
        task=task,
        task_description=task_description,
        env=env,
        init_states=init_states,
    )


def build_server_state_from_raw_obs(obs: dict[str, Any]) -> np.ndarray:
    position = np.asarray(obs["robot0_eef_pos"], dtype=np.float32)
    quat = np.asarray(obs["robot0_eef_quat"], dtype=np.float32)
    gripper_qpos = np.asarray(obs["robot0_gripper_qpos"], dtype=np.float32)
    if position.shape != (3,):
        raise ValueError(f"robot0_eef_pos must be shape (3,), got {position.shape}")
    if quat.shape != (4,):
        raise ValueError(f"robot0_eef_quat must be shape (4,), got {quat.shape}")
    if gripper_qpos.shape != (2,):
        raise ValueError(f"robot0_gripper_qpos must be shape (2,), got {gripper_qpos.shape}")
    return np.ascontiguousarray(
        np.concatenate((position, quat_to_axis_angle(quat), gripper_qpos), axis=0),
        dtype=np.float32,
    )


def quat_to_axis_angle(quat_xyzw: np.ndarray) -> np.ndarray:
    quat = np.asarray(quat_xyzw, dtype=np.float32).copy()
    if quat.shape != (4,):
        raise ValueError(f"expected quaternion shape (4,), got {quat.shape}")
    quat[3] = float(np.clip(quat[3], -1.0, 1.0))
    den = float(np.sqrt(max(0.0, 1.0 - float(quat[3] * quat[3]))))
    if den <= 1e-10:
        return np.zeros(3, dtype=np.float32)
    angle = 2.0 * float(np.arccos(quat[3]))
    return np.ascontiguousarray((quat[:3] * angle) / den, dtype=np.float32)


def default_assets_cache_path() -> Path:
    return LIBERO_ASSETS_ROOT


def default_runs_root(project_root: Path) -> Path:
    return project_root / "runs"


def _write_libero_config() -> Path:
    LIBERO_CONFIG_ROOT.mkdir(parents=True, exist_ok=True)
    package_root = _resolve_hf_libero_package_root()
    config_path = LIBERO_CONFIG_ROOT / "config.yaml"
    config = {
        "benchmark_root": str(package_root),
        "bddl_files": str(package_root / "bddl_files"),
        "init_states": str(package_root / "init_files"),
        "datasets": str(LIBERO_DATASETS_ROOT),
        "assets": str(default_assets_cache_path()),
    }
    config_path.write_text(yaml.safe_dump(config), encoding="utf-8")
    return LIBERO_CONFIG_ROOT


def _resolve_hf_libero_package_root() -> Path:
    try:
        spec = importlib.util.find_spec("libero.libero")
    except ModuleNotFoundError:
        spec = None
    if spec is None or spec.origin is None:
        raise RuntimeError(
            "hf-libero is not installed in the current environment. "
            "Run `libero-local-rollout bootstrap-sim` first."
        )
    return Path(spec.origin).resolve().parent


def describe_bootstrap_status(status: LiberoInstallStatus) -> str:
    payload = {
        "hf_libero_installed": status.hf_libero_installed,
        "libero_config_path": str(status.libero_config_path),
        "assets_path": None if status.assets_path is None else str(status.assets_path),
    }
    return json.dumps(payload, indent=2, sort_keys=True)


# ── Dreamscale additions (not in the sandbox source) ──────────────────────────

from dreamscale import errors  # noqa: E402

DEFAULT_TASK_SUITE = "libero_spatial"
DEFAULT_TASK_ID = 0
NUM_STEPS_WAIT = 10  # settle physics before driving (sandbox rollout pattern)


def _import_robosuite() -> Any:
    # robosuite 1.4.1's ASCII logo contains an unescaped backslash-space.
    # Python emits this during source compilation, using the filename as the
    # warning module (DeprecationWarning on 3.11, SyntaxWarning on 3.12+).
    # Keep the filter local to this import and this exact logo.
    with warnings.catch_warnings():
        for category in (DeprecationWarning, SyntaxWarning):
            warnings.filterwarnings(
                "ignore",
                message=(r"invalid escape sequence '\\ '$"
                         r'|"\\ " is an invalid escape sequence\.'),
                category=category,
                module=r".*[/\\]robosuite[/\\]__init__$",
            )
        return importlib.import_module("robosuite")


def ensure_sim_ready() -> None:
    """Prepare Dreamscale's built-in local LIBERO sim runtime.

    This is for the curated `dreamscale sim` path only. Downstream user projects
    that own their own simulator environment should not rely on this helper or
    on `dreamscale[sim]` transitively.
    """
    try:
        import mujoco  # noqa: F401
        _import_robosuite()
    except ImportError as exc:
        raise errors.catalog("sim_not_installed") from exc
    ensure_hf_libero_installed()


class LiberoSimEnv:
    """SimEnvProtocol implementation over a LIBERO offscreen env."""

    _CAMERA_OBSERVABLES = ("agentview_image", "robot0_eye_in_hand_image")

    def __init__(self, task_handle, *, fast_camera_obs: bool = True) -> None:
        self._handle = task_handle
        self.task_description = task_handle.task_description
        self._fast_camera_obs = fast_camera_obs
        self._camera_obs_cache_source_id: int | None = None
        self._camera_obs_cache: dict[str, Any] | None = None
        self._set_camera_observables_enabled(False)

    @classmethod
    def create_default(
        cls,
        *,
        task_suite_name: str = DEFAULT_TASK_SUITE,
        task_id: int = DEFAULT_TASK_ID,
        seed: int = 0,
        control_freq: int = LIBERO_ACTION_HZ,
        env_resolution: int = 256,
    ) -> LiberoSimEnv:
        handle = create_task_handle(
            task_suite_name=task_suite_name, task_id=task_id,
            seed=seed, env_resolution=env_resolution, assets_path=ensure_libero_assets(),
            control_freq=control_freq,
        )
        return cls(handle)

    def reset(self) -> dict:
        self._camera_obs_cache_source_id = None
        self._camera_obs_cache = None
        self._set_camera_observables_enabled(False)
        self._handle.env.reset()
        obs = self._handle.env.set_init_state(self._handle.init_states[0])
        for _ in range(NUM_STEPS_WAIT):
            obs, _, _, _ = self._handle.env.step(LIBERO_DUMMY_ACTION)
        return self._ensure_camera_obs(obs)

    def step(self, action) -> tuple[dict, bool]:
        self._camera_obs_cache_source_id = None
        self._camera_obs_cache = None
        self._set_camera_observables_enabled(False)
        obs, _reward, done, _info = self._handle.env.step(list(action))
        return obs, bool(done)

    def agent_frame(self, obs):
        return self._ensure_camera_obs(obs)["agentview_image"]

    def wrist_frame(self, obs):
        return self._ensure_camera_obs(obs)["robot0_eye_in_hand_image"]

    def proprio(self, obs) -> list[float]:
        return [float(value) for value in build_server_state_from_raw_obs(obs)]

    def close(self) -> None:
        self._handle.env.close()

    def _ensure_camera_obs(self, obs: dict[str, Any]) -> dict[str, Any]:
        if all(name in obs for name in self._CAMERA_OBSERVABLES):
            return obs
        source_id = id(obs)
        if (
            self._camera_obs_cache_source_id == source_id
            and self._camera_obs_cache is not None
        ):
            return self._camera_obs_cache
        if not self._fast_camera_obs:
            return obs

        raw_env = self._raw_env()
        update_observables = getattr(raw_env, "_update_observables", None)
        get_observations = getattr(raw_env, "_get_observations", None)
        if update_observables is None or get_observations is None:
            return obs

        self._set_camera_observables_enabled(True)
        try:
            update_observables(force=True)
            camera_obs = dict(get_observations())
        finally:
            self._set_camera_observables_enabled(False)

        self._camera_obs_cache_source_id = source_id
        self._camera_obs_cache = camera_obs
        return camera_obs

    def _raw_env(self) -> Any:
        return getattr(self._handle.env, "env", self._handle.env)

    def _set_camera_observables_enabled(self, enabled: bool) -> None:
        if not self._fast_camera_obs:
            return
        observables = getattr(self._raw_env(), "_observables", None)
        if not isinstance(observables, dict):
            return
        for name in self._CAMERA_OBSERVABLES:
            observable = observables.get(name)
            if observable is None:
                continue
            is_enabled = getattr(observable, "is_enabled", None)
            set_enabled = getattr(observable, "set_enabled", None)
            if is_enabled is None or set_enabled is None:
                continue
            if bool(is_enabled()) != enabled:
                set_enabled(enabled)


class HistoryLiberoSimEnv(LiberoSimEnv):
    """LIBERO with a camera history: by default RLDX-1's frames at env steps -6, -4, -2 and 0,
    or the steps back a model's ``history_ticks`` names (oldest first).

    Every step renders both 256px cameras, rotated 180 degrees as upstream's LIBERO
    wrapper does. Before an episode has enough steps, the oldest frame repeats, matching
    upstream's padding with copies of the first observation.
    """

    RLDX_TICKS = (6, 4, 2, 0)

    def __init__(self, task_handle, *, history_ticks=RLDX_TICKS, **kwargs) -> None:
        super().__init__(task_handle, **kwargs)
        self.set_history_ticks(history_ticks)
        self._last_gripper = -1.0

    def set_history_ticks(self, history_ticks) -> None:
        """The steps back of each window frame, oldest first, ending at the current step."""
        from collections import deque

        ticks = tuple(int(tick) for tick in history_ticks)
        descending = all(a > b for a, b in zip(ticks, ticks[1:], strict=False))
        if not ticks or ticks[-1] != 0 or not descending:
            raise ValueError("history_ticks must count down to 0, oldest first")
        self._ticks = ticks
        self._history: deque = deque(maxlen=ticks[0] + 1)
        self._sent: deque = deque(maxlen=2 * (ticks[0] + 1))
        self._step = -1  # the newest rendered frame's step in the episode
        self._wanted: set[int] = set()

    def send_frames_ahead(self, send, *, kept: int | None = None) -> None:
        """Hand frames to ``send(key, agent, wrist)`` (a model that sends its window ahead); a
        request then names the frames ``send`` accepted.

        By default every frame goes as it is rendered. With ``kept`` (how many ticks of frames
        the server keeps a session, the oldest sent evicted first), only the frames a window
        will name go: those of the next request announced by ``expect_request``, and any of a
        request's own still missing; a window names only frames among the last ``kept`` sent.
        """
        from collections import deque

        self._send = send
        self._targeted = kept is not None
        if kept is not None:
            self._sent = deque(maxlen=kept)

    def expect_request(self, after_steps: int) -> None:
        """The next request comes ``after_steps`` steps from now: send its window's older
        frames already rendered, and the others as they are (with ``send_frames_ahead(kept=)``).
        """
        if not getattr(self, "_targeted", False):
            return
        target = self._step + after_steps
        if target < self._ticks[0]:
            self._wanted = set()  # an early window repeats its first frame: a strip
            return
        steps = {target - tick for tick in self._ticks[:-1]}
        self._wanted = {step for step in steps if step > self._step}
        for step in sorted(steps - self._wanted):
            self._send_step(step)

    def _send_step(self, step: int) -> None:
        back = self._step - step
        if not 0 <= back < len(self._history):
            return
        agent, wrist, key = self._history[len(self._history) - 1 - back]
        if key not in self._sent and self._send(key, agent, wrist):
            self._sent.append(key)

    def reset(self) -> dict:
        obs = super().reset()
        self._history.clear()
        self._step = -1
        self._wanted = set()
        self._last_gripper = -1.0
        self._remember(obs)
        return obs

    def step(self, action) -> tuple[dict, bool]:
        obs, done = super().step(action)
        self._last_gripper = float(action[-1])
        self._remember(obs)
        return obs, done

    def _remember(self, obs) -> None:
        agent = np.ascontiguousarray(self.agent_frame(obs)[::-1, ::-1])
        wrist = np.ascontiguousarray(self.wrist_frame(obs)[::-1, ::-1])
        key = time.time_ns()
        if self._history and key <= self._history[-1][2]:
            key = self._history[-1][2] + 1  # capture keys only ever increase
        self._history.append((agent, wrist, key))
        self._step += 1
        send = getattr(self, "_send", None)
        if send is None:
            return
        if not getattr(self, "_targeted", False):
            if send(key, agent, wrist):
                self._sent.append(key)
        elif self._step in self._wanted:
            self._wanted.discard(self._step)
            self._send_step(self._step)

    def hold_action(self) -> list[float]:
        return [0.0] * 6 + [self._last_gripper]

    def observation_inputs(self, obs) -> dict:
        history = list(self._history)
        if not history:
            raise RuntimeError("Reset the simulator before requesting a policy observation")
        sampled = [history[max(0, len(history) - 1 - tick)] for tick in self._ticks]
        inputs = {"agent_frames": np.stack([agent for agent, _, _ in sampled]),
                  "wrist_frames": np.stack([wrist for _, wrist, _ in sampled]),
                  "libero_state": self.proprio(obs)}
        keys = tuple(key for _, _, key in sampled)
        # Name the older frames only when each was sent ahead and the window is full (before an
        # episode has enough steps its oldest frame repeats, and repeats travel in a strip).
        if getattr(self, "_send", None) is not None and len(set(keys)) == len(keys):
            if getattr(self, "_targeted", False):
                for tick in self._ticks[:-1]:  # any the announcement missed go now, in order
                    self._send_step(self._step - tick)
            if set(keys[:-1]) <= set(self._sent):
                inputs["frame_keys"] = keys
        return inputs

    def policy_preview_frame(self, obs) -> np.ndarray:
        agent, wrist, _ = self._history[-1]
        return np.concatenate((agent, wrist), axis=1)
