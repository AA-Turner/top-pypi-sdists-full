"""Integration test for ``aroom docs start/stop/status``.

Launches a real docs background server, polls the port, then exercises
``docs status`` (auto-discovering the port) and ``docs stop``.

Requires mkdocs to be installed in the test runner's environment; skips
otherwise. Mark: integration.
"""

from __future__ import annotations

import os
import socket
import subprocess
import time
import urllib.error
import urllib.request
from pathlib import Path

import pytest

pytest.importorskip("mkdocs")


def _free_port() -> int:
    """Return an available TCP port by letting the kernel pick."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def _venv_aroom() -> Path:
    """Locate the worktree's ``.venv/bin/aroom`` entry point."""
    # Walk up from this file to find the worktree root (has pyproject.toml).
    here = Path(__file__).resolve()
    for parent in [here.parent, *here.parents]:
        candidate = parent / ".venv" / "bin" / "aroom"
        if candidate.is_file():
            return candidate
    pytest.skip("Worktree .venv/bin/aroom not found; skipping integration test")


@pytest.mark.integration
def test_aroom_docs_server_lifecycle(tmp_path: Path) -> None:
    aroom = _venv_aroom()
    port = _free_port()

    # Force the subprocess to use an isolated HOME so ~/.anteroom resolves
    # inside tmp_path. Also clear any config-override env vars.
    env = os.environ.copy()
    env["HOME"] = str(tmp_path)
    env["USERPROFILE"] = str(tmp_path)  # Windows fallback
    # Data dir is ~/.anteroom when HOME is set; create a minimal config so
    # _load_config_or_exit does not complain.
    data_dir = tmp_path / ".anteroom"
    data_dir.mkdir(exist_ok=True)
    (data_dir / "config.yaml").write_text('ai:\n  base_url: "http://127.0.0.1:9"\n  api_key: "test"\n  model: "test"\n')

    start_proc: subprocess.Popen[bytes] | None = None
    try:
        # Kick off `aroom docs start` — the start helper detaches a child and
        # this command itself exits quickly.
        start_proc = subprocess.Popen(
            [str(aroom), "docs", "start", "--port", str(port)],
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        start_proc.wait(timeout=20)

        # Poll until the docs server responds on the picked port.
        deadline = time.monotonic() + 20.0
        responded = False
        while time.monotonic() < deadline:
            try:
                with urllib.request.urlopen(f"http://127.0.0.1:{port}/", timeout=1.0) as resp:
                    if resp.status == 200:
                        responded = True
                        break
            except (urllib.error.URLError, TimeoutError, OSError):
                pass
            time.sleep(0.5)
        assert responded, "docs server did not respond on port within 20s"

        # `aroom docs status` with no --port: auto-discovers the single PID.
        status = subprocess.run(
            [str(aroom), "docs", "status"],
            env=env,
            capture_output=True,
            text=True,
            timeout=10,
        )
        assert status.returncode == 0, status.stderr
        assert "running" in status.stdout.lower() or "running" in status.stderr.lower()

        # `aroom docs stop --port <port>` should succeed.
        stop = subprocess.run(
            [str(aroom), "docs", "stop", "--port", str(port)],
            env=env,
            capture_output=True,
            text=True,
            timeout=15,
        )
        assert stop.returncode == 0, stop.stderr

        # PID file must be removed.
        pid_path = data_dir / f"anteroom-docs-{port}.pid"
        assert not pid_path.exists(), f"PID file still present: {pid_path}"

        # `aroom docs status` should now report no server.
        status2 = subprocess.run(
            [str(aroom), "docs", "status"],
            env=env,
            capture_output=True,
            text=True,
            timeout=10,
        )
        # Exit 1 when no server is running (via _resolve_docs_port).
        assert status2.returncode == 1
        assert "no docs server" in (status2.stderr + status2.stdout).lower()
    finally:
        # Best-effort cleanup: if something went wrong, kill the background
        # mkdocs process by scanning the data_dir for a PID file.
        pid_path = data_dir / f"anteroom-docs-{port}.pid"
        if pid_path.exists():
            try:
                import json as _json

                info = _json.loads(pid_path.read_text())
                bg_pid = int(info.get("pid", 0))
                if bg_pid > 0:
                    try:
                        os.kill(bg_pid, 15)  # SIGTERM
                    except ProcessLookupError:
                        pass
            except (OSError, ValueError, _json.JSONDecodeError):
                pass
        if start_proc is not None and start_proc.poll() is None:
            start_proc.terminate()
            try:
                start_proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                start_proc.kill()
