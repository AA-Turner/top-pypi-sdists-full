"""Install and run ABC's simulator independently of the user's Python environment."""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import tarfile
import threading
import urllib.request
from pathlib import Path

from dreamscale.config import dreamscale_home

from .abc_catalog import (
    ASSETS_MANIFEST,
    ASSETS_MIRROR,
    CAMERAS,
    IMAGE_SIZE,
    REPOSITORY,
    REVISION,
    packages_for,
)
from .native_runtime import NativeSimProcess, _source_checkout

RUNTIME_ROOT = dreamscale_home() / "sim" / "abc" / REVISION[:12]
# abc_sim alone needs MuJoCo, Gymnasium and NumPy (no torch, no warp): upstream's own MuJoCo
# pin. The rest is the viewer window and the --output-root video.
RUNTIME_REQUIREMENTS = ("mujoco~=3.8.0", "gymnasium>=1.1,<2", "numpy>=2,<3",
                        "opencv-python==4.11.0.86", "av>=15,<19", "imageio>=2.34,<3")
# The mirror refuses Python's default agent (403); it accepts any other.
_USER_AGENT = "dreamscale-sdk sim-assets"


def ensure_abc_runtime(*, root: Path = RUNTIME_ROOT, on_line=print) -> Path:
    """Cache the pinned abc_sim source and an isolated Python for it; never change user
    packages."""
    uv = shutil.which("uv")
    if uv is None:
        raise RuntimeError("ABC needs uv to prepare its runtime. Install uv and retry.")
    root.mkdir(parents=True, exist_ok=True)
    import fcntl

    with (root / ".install.lock").open("w") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        source = root / "source"
        _source_checkout(REPOSITORY, REVISION, source)
        python = root / "venv" / "bin" / "python"
        ready = root / ".runtime-ready-v1"
        if not ready.exists():
            on_line("Preparing the ABC simulator runtime (first run only)…")
            if not python.exists():
                subprocess.run([uv, "venv", "--python", "3.12", str(root / "venv")], check=True)
            subprocess.run([uv, "pip", "install", "--python", str(python),
                            *RUNTIME_REQUIREMENTS], check=True)
            subprocess.run(
                [str(python), "-c",
                 f"import sys; sys.path.insert(0, {str(source)!r}); "
                 "import mujoco, abc_sim; abc_sim.get_task_spec('put_plastic_bottles_in_bin')"],
                check=True,
            )
            ready.touch()
        return python


def ensure_abc_assets(task: str, *, root: Path = RUNTIME_ROOT, on_line=print,
                      fetch=None) -> None:
    """Install the asset packages ``task``'s scene loads, each checked against the sha256 the
    pinned source's manifest gives it. ``fetch(url, path)`` downloads one archive."""
    source = root / "source"
    manifest = json.loads((source / ASSETS_MANIFEST).read_text())
    packages = {package["name"]: package for package in manifest["packages"]}
    fetch = fetch or _fetch
    import fcntl

    with (root / ".assets.lock").open("w") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        for name in packages_for(task):
            package = packages[name]
            archive_name = Path(package["archive"]).name
            url = ASSETS_MIRROR + archive_name
            if package["uri"] != url or package["extract_dir"] != "abc_sim/models/assets":
                raise RuntimeError(f"ABC asset package {name} is not where its manifest says")
            installed = root / "assets-installed" / f"{name}-{package['sha256'][:16]}"
            if installed.exists():
                continue
            on_line(f"Downloading ABC assets: {name} "
                    f"({package['size_bytes'] / 1e6:.1f} MB, first run only)…")
            archive = root / "archives" / archive_name
            archive.parent.mkdir(parents=True, exist_ok=True)
            partial = archive.with_suffix(".part")
            fetch(url, partial)
            with partial.open("rb") as handle:
                digest = hashlib.file_digest(handle, "sha256").hexdigest()
            if digest != package["sha256"]:
                partial.unlink()
                raise RuntimeError(f"The ABC asset download {name} did not match its pinned "
                                   "checksum; retry, or report this if it persists.")
            partial.rename(archive)
            target = source / package["extract_dir"]
            target.mkdir(parents=True, exist_ok=True)
            with tarfile.open(archive) as bundle:
                bundle.extractall(target, filter="data")
            archive.unlink()
            installed.parent.mkdir(parents=True, exist_ok=True)
            installed.touch()


def _fetch(url: str, path: Path) -> None:
    request = urllib.request.Request(url, headers={"User-Agent": _USER_AGENT})
    with urllib.request.urlopen(request, timeout=120) as response, path.open("wb") as sink:
        shutil.copyfileobj(response, sink, 1 << 20)


class AbcSimEnv(NativeSimProcess):
    """One abc_sim world: the YAM wire's 14 joint values in and out, and the top, left and
    right cameras free-running beside the physics, as a robot's are."""

    def __init__(self, *, task: str, seed: int, python: Path | None = None,
                 root: Path = RUNTIME_ROOT):
        self.python = python or ensure_abc_runtime(root=root)
        self._lock = threading.Lock()
        self._initial_seed = int(seed)
        super().__init__(
            python=self.python,
            script=Path(__file__).with_name("abc_process.py"),
            root=root,
            label="ABC",
            setup={"source": str(root / "source"), "task": task, "seed": int(seed),
                   "cameras": CAMERAS, "image_size": IMAGE_SIZE},
        )
        self._start(self._initial)

    def _start(self, initial: dict) -> None:
        self.task_description = initial["instruction"]
        self.seed = initial["seed"]
        self.scored = initial["scored"]
        self.state = tuple(initial["state"])
        self.last = {"over": False, "success": False, "reward": 0.0, "max_reward": 0.0,
                     "eval": {}}

    def _call(self, message, **kwargs):
        # The run loop's callbacks and the caller's thread share one pipe.
        with self._lock:
            return self._request(message, **kwargs)

    def reset(self, seed: int | None = None) -> dict:
        """The episode's first observation; ``seed`` starts another scene."""
        if self._initial is not None and seed in (None, self._initial_seed):
            # The process starts on its first scene: that reset is already done.
            result, self._initial = self._initial, None
        else:
            self._initial = None
            result = self._call({"op": "reset", "seed": self.seed if seed is None else seed},
                                timeout_s=600)
        self._start(result)
        return result

    def observe(self, *, fresh: bool = False) -> dict:
        """The measured joints and the cameras' newest frames; ``fresh`` waits for the frames
        of the current state instead."""
        result = self._call({"op": "observe", "fresh": fresh})
        self.state = tuple(result["state"])
        return result

    def step(self, action) -> dict:
        result = self._call({"op": "step", "action": [float(value) for value in action]})
        self.state = tuple(result["state"])
        self.last = result
        return result

    def frame(self, *, show: bool, record: bool) -> None:
        self._call({"op": "frame", "show": show, "record": record})

    def stats(self) -> dict:
        """How many camera frames the process has rendered and what one took, ms."""
        return self._call({"op": "stats"})

    def write_video(self, path: Path, fps: float) -> int:
        return self._call({"op": "video", "path": str(path), "fps": fps}, timeout_s=300)
