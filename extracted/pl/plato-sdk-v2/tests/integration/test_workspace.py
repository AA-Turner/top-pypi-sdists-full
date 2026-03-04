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

from plato.markers import WorkspaceMarker  # noqa: E402
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

        # ws.path is now the content dir (workspace_dir / "data")
        (ws.path / "file1.txt").write_text("hello")
        (ws.path / "file2.txt").write_text("world")

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

        (ws.path / "file.txt").write_text("v1")

        run(ws.commit("step_1"))
        assert (workspace_dir / "data.dvc").exists()

        (ws.path / "file2.txt").write_text("v2")
        run(ws.commit("step_2"))


class TestWorkspaceCommitReturnsValidDvcInfo:
    def test_commit_returns_dvc_file_info(self, workspace_dir):
        ws = Workspace("test", workspace_dir, tracked=True)
        run(ws.init())

        (ws.path / "file.txt").write_text("hello")

        import json

        result = run(ws.commit("step_1"))
        info = json.loads(result)
        assert "step" in info
        assert info["step"] == "step_1"
        assert "dvc_files" in info
        assert "data" in info["dvc_files"]


class TestWorkspacePathIsContentDir:
    """workspace.path should point to the content directory, not the DVC repo root."""

    def test_tracked_path_is_content_dir(self, workspace_dir):
        ws = Workspace("test", workspace_dir, tracked=True)
        assert ws.path == workspace_dir / "data"
        assert ws.path != workspace_dir  # NOT the repo root

    def test_untracked_path_is_root(self, workspace_dir):
        ws = Workspace("test", workspace_dir, tracked=False)
        assert ws.path == workspace_dir

    def test_no_data_path_attribute(self, workspace_dir):
        ws = Workspace("test", workspace_dir, tracked=True)
        assert not hasattr(ws, "data_path")  # deleted from API


class TestWorkspaceDvcIgnore:
    def test_init_creates_default_dvcignore(self, workspace_dir):
        ws = Workspace("test", workspace_dir, tracked=True)
        run(ws.init())
        dvcignore = workspace_dir / ".dvcignore"  # at repo root, not content dir
        assert dvcignore.exists()
        content = dvcignore.read_text()
        for pattern in WorkspaceMarker.DEFAULT_DVCIGNORE:
            assert pattern in content

    def test_custom_dvcignore_merged_with_defaults(self, workspace_dir):
        ws = Workspace("test", workspace_dir, tracked=True, dvcignore=["dist", "build"])
        run(ws.init())
        content = (workspace_dir / ".dvcignore").read_text()
        assert "node_modules" in content  # default
        assert "dist" in content  # custom
        assert "build" in content  # custom

    def test_dvcignore_idempotent_on_reinit(self, workspace_dir):
        ws = Workspace("test", workspace_dir, tracked=True)
        run(ws.init())
        run(ws.init())  # second init
        content = (workspace_dir / ".dvcignore").read_text()
        assert content.count("node_modules") == 1

    def test_untracked_no_dvcignore(self, workspace_dir):
        ws = Workspace("test", workspace_dir, tracked=False)
        run(ws.init())
        assert not (workspace_dir / ".dvcignore").exists()


class TestWorkspaceRepoRootHidden:
    """DVC repo root (_repo_root) is private; only path is public."""

    def test_repo_root_is_private(self, workspace_dir):
        ws = Workspace("test", workspace_dir, tracked=True)
        assert ws._repo_root == workspace_dir
        assert ws.path == workspace_dir / "data"

    def test_init_creates_git_dvc_at_repo_root(self, workspace_dir):
        ws = Workspace("test", workspace_dir, tracked=True)
        run(ws.init())
        assert (ws._repo_root / ".git").is_dir()
        assert (ws._repo_root / ".dvc").exists()
        # NOT at content dir
        assert not (ws.path / ".git").exists()
        assert not (ws.path / ".dvc").exists()

    def test_content_dir_created_on_init(self, workspace_dir):
        ws = Workspace("test", workspace_dir, tracked=True)
        run(ws.init())
        assert ws.path.is_dir()  # data/ dir created


class TestWorkspaceCommitUpdated:
    """Commit should work with the new path layout."""

    def test_commit_creates_dvc_file_at_repo_root(self, workspace_dir):
        ws = Workspace("test", workspace_dir, tracked=True)
        run(ws.init())
        # Write to content dir (ws.path)
        (ws.path / "file.txt").write_text("hello")
        result = run(ws.commit("step_1"))
        assert result
        # .dvc file at repo root, not content dir
        assert (ws._repo_root / "data.dvc").exists()
        assert not (ws.path / "data.dvc").exists()

    def test_commit_multiple_content_subdirs(self, workspace_dir):
        ws = Workspace("test", workspace_dir, tracked=True)
        run(ws.init())
        (ws.path / "src").mkdir()
        (ws.path / "src" / "app.py").write_text("print('hi')")
        (ws.path / "config").mkdir()
        (ws.path / "config" / "settings.json").write_text("{}")
        run(ws.commit("step_1"))
        # data.dvc should exist (data/ is the tracked dir)
        assert (ws._repo_root / "data.dvc").exists()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
