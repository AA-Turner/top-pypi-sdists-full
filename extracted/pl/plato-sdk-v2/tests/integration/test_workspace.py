"""Integration tests for Workspace — verifies DVC init/commit/restore cycle."""

import asyncio
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

# Ensure venv bin is on PATH so subprocess can find dvc
_venv_bin = str(Path(sys.executable).parent)
if _venv_bin not in os.environ.get("PATH", ""):
    os.environ["PATH"] = _venv_bin + os.pathsep + os.environ.get("PATH", "")

from plato.worlds.workspace import Workspace  # noqa: E402


def _dvc_works() -> bool:
    """Check if dvc is installed and functional (can actually init)."""
    dvc_bin = shutil.which("dvc")
    if not dvc_bin:
        return False
    try:
        import tempfile

        with tempfile.TemporaryDirectory() as tmpdir:
            subprocess.run(["git", "init"], cwd=tmpdir, capture_output=True, check=True, timeout=10)
            result = subprocess.run([dvc_bin, "init"], cwd=tmpdir, capture_output=True, timeout=10)
            return result.returncode == 0
    except Exception:
        return False


pytestmark = pytest.mark.skipif(not _dvc_works(), reason="dvc not installed or broken")


@pytest.fixture
def workspace_dir(tmp_path):
    ws_path = tmp_path / "workspace"
    ws_path.mkdir()
    return ws_path


def run(coro):
    return asyncio.get_event_loop().run_until_complete(coro)


class TestWorkspaceInit:
    def test_init_creates_git_and_dvc(self, workspace_dir):
        ws = Workspace("test", workspace_dir, tracked=True)
        run(ws.init())
        assert (workspace_dir / ".git").is_dir()
        assert (workspace_dir / ".dvc").exists()

    def test_init_idempotent(self, workspace_dir):
        ws = Workspace("test", workspace_dir, tracked=True)
        run(ws.init())
        run(ws.init())
        assert (workspace_dir / ".git").is_dir()
        assert (workspace_dir / ".dvc").exists()

    def test_init_untracked_skips_git(self, workspace_dir):
        ws = Workspace("test", workspace_dir, tracked=False)
        run(ws.init())
        assert not (workspace_dir / ".git").exists()
        assert not (workspace_dir / ".dvc").exists()


class TestWorkspaceCommit:
    def test_commit_with_data_dir(self, workspace_dir):
        ws = Workspace("test", workspace_dir, tracked=True)
        run(ws.init())

        data_dir = workspace_dir / "data"
        data_dir.mkdir()
        (data_dir / "file1.txt").write_text("hello")
        (data_dir / "file2.txt").write_text("world")

        result = run(ws.commit("step_1"))
        assert result
        assert (workspace_dir / "data.dvc").exists()

    def test_commit_with_multiple_dirs(self, workspace_dir):
        ws = Workspace("test", workspace_dir, tracked=True)
        run(ws.init())

        for name in ["recordings", "outputs"]:
            d = workspace_dir / name
            d.mkdir()
            (d / "file.txt").write_text(f"data in {name}")

        result = run(ws.commit("step_1"))
        assert result
        assert (workspace_dir / "recordings.dvc").exists()
        assert (workspace_dir / "outputs.dvc").exists()

    def test_commit_empty_workspace(self, workspace_dir):
        ws = Workspace("test", workspace_dir, tracked=True)
        run(ws.init())
        result = run(ws.commit("step_1"))
        assert result

    def test_commit_twice(self, workspace_dir):
        ws = Workspace("test", workspace_dir, tracked=True)
        run(ws.init())

        data_dir = workspace_dir / "data"
        data_dir.mkdir()
        (data_dir / "file.txt").write_text("v1")

        run(ws.commit("step_1"))
        assert (workspace_dir / "data.dvc").exists()

        (data_dir / "file2.txt").write_text("v2")
        run(ws.commit("step_2"))


class TestWorkspaceCommitReturnsValidDvcInfo:
    def test_commit_returns_dvc_file_info(self, workspace_dir):
        ws = Workspace("test", workspace_dir, tracked=True)
        run(ws.init())

        data_dir = workspace_dir / "data"
        data_dir.mkdir()
        (data_dir / "file.txt").write_text("hello")

        import json

        result = run(ws.commit("step_1"))
        info = json.loads(result)
        assert "step" in info
        assert info["step"] == "step_1"
        assert "dvc_files" in info
        assert "data" in info["dvc_files"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
