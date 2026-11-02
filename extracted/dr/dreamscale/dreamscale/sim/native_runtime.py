"""Shared lifecycle for isolated local simulator processes."""

from __future__ import annotations

import contextlib
import os
import subprocess
import sys
import tarfile
import tempfile
import urllib.request
from pathlib import Path

from .native_process import read_message, write_message


class NativeSimProcess:
    def __init__(
        self,
        *,
        python: Path,
        script: Path,
        root: Path,
        setup: dict,
        label: str,
        environment: dict | None = None,
    ):
        self.label = label
        child_env = dict(os.environ)
        child_env.pop("PYTHONPATH", None)
        if sys.platform == "linux":
            child_env.setdefault("MUJOCO_GL", "egl")
        child_env.update(environment or {})
        logs = root / "logs"
        logs.mkdir(parents=True, exist_ok=True)
        self._log = tempfile.NamedTemporaryFile(
            prefix="native-", suffix=".log", dir=logs, delete=False
        )
        self._process = subprocess.Popen(
            [str(python), "-u", str(script)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=self._log,
            env=child_env,
            bufsize=0,
        )
        try:
            self._initial = self._request(setup, timeout_s=1800)
        except BaseException:
            self.close()
            raise

    def _request(self, message, *, timeout_s=120):
        try:
            write_message(self._process.stdin, message)
            response = read_message(self._process.stdout, timeout_s=timeout_s)
        except (EOFError, BrokenPipeError, TimeoutError, ValueError) as exc:
            raise RuntimeError(
                f"{self.label} simulator stopped responding. Details: {self._log.name}"
            ) from exc
        if "error" in response:
            raise RuntimeError(f"{self.label}: {response['error']}\nDetails: {self._log.name}")
        return response["ok"]

    def render_frame(self, frame):
        self._request({"op": "render"})

    def close(self):
        process = self._process
        try:
            if process.poll() is None:
                with contextlib.suppress(BrokenPipeError, OSError):
                    write_message(process.stdin, {"op": "close"})
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.terminate()
                    try:
                        process.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        process.kill()
                        process.wait()
        finally:
            for stream in (process.stdin, process.stdout):
                if stream is not None:
                    stream.close()
            self._log.close()


def write_native_video(python: Path, path: Path, frames, fps: int) -> None:
    import numpy as np

    with tempfile.TemporaryDirectory(prefix="dreamscale-sim-recording-") as temporary:
        array_path = Path(temporary) / "frames.npy"
        np.save(array_path, frames, allow_pickle=False)
        subprocess.run(
            [
                str(python),
                "-c",
                "import imageio.v3 as i, numpy as n, sys; "
                "i.imwrite(sys.argv[2], n.load(sys.argv[1], allow_pickle=False), "
                "plugin='pyav', codec='libx264', fps=float(sys.argv[3]))",
                str(array_path),
                str(path),
                str(fps),
            ],
            check=True,
            timeout=120,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
        )


def _source_checkout(repository: str, revision: str, destination: Path) -> None:
    if destination.exists():
        return
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=destination.parent) as temporary:
        archive = Path(temporary) / "source.tar.gz"
        urllib.request.urlretrieve(
            f"https://codeload.github.com/{repository}/tar.gz/{revision}", archive
        )
        with tarfile.open(archive) as source:
            source.extractall(Path(temporary) / "source", filter="data")
        (root,) = (Path(temporary) / "source").iterdir()
        root.rename(destination)
