"""Tests for _restore_stashed_changes."""

from subprocess import CompletedProcess
from unittest.mock import patch

from agentic_devtools.cli.setup.pr_workflow import _restore_stashed_changes


def _ok(stdout: str = "") -> CompletedProcess:
    return CompletedProcess(args=[], returncode=0, stdout=stdout, stderr="")


def _fail(stderr: str = "") -> CompletedProcess:
    return CompletedProcess(args=[], returncode=1, stdout="", stderr=stderr)


class TestRestoreStashedChanges:
    """Tests for _restore_stashed_changes."""

    def test_warns_when_rollback_cannot_be_verified_without_snapshots(self, capsys):
        """Missing status/untracked snapshots force the helper down the manual-recovery path."""
        with patch("agentic_devtools.cli.setup.pr_workflow.run_git") as mock_git:
            mock_git.side_effect = [
                _fail("status failed"),  # status snapshot before pop
                _fail("untracked failed"),  # untracked paths before pop
                _fail("conflict"),  # stash pop fails
                _ok("restored.txt\0"),  # untracked paths after failed pop
                _ok(),  # reset --merge
                _ok(),  # checkout --merge -- .
                _ok("?? restored.txt\0"),  # status after rollback
            ]
            result = _restore_stashed_changes("stash@{0}")

        assert result is False
        err = capsys.readouterr().err
        assert "rollback could not be verified" in err

    def test_warns_when_rollback_fails(self, capsys):
        """When rollback itself fails, the helper warns and returns False."""
        with patch("agentic_devtools.cli.setup.pr_workflow.run_git") as mock_git:
            mock_git.side_effect = [
                _ok(""),  # status snapshot before pop
                _ok(""),  # untracked paths before pop
                _fail("conflict"),  # stash pop fails
                _ok("restored.txt\0"),  # untracked paths after failed pop
                _fail("reset failed"),  # rollback reset fails
                _ok(),  # rollback checkout still attempted
                _ok("?? restored.txt\0"),  # status after rollback
            ]
            result = _restore_stashed_changes("stash@{0}")

        assert result is False
        err = capsys.readouterr().err
        assert "rollback could not be verified" in err

    def test_removes_untracked_directories_restored_by_failed_pop(self, capsys, monkeypatch, tmp_path):
        """Rollback removes introduced untracked directories as well as files."""
        monkeypatch.chdir(tmp_path)
        restored_dir = tmp_path / "restored-dir"
        restored_dir.mkdir()
        (restored_dir / "nested.txt").write_text("remove")

        with patch("agentic_devtools.cli.setup.pr_workflow.run_git") as mock_git:
            mock_git.side_effect = [
                _ok(""),  # status snapshot before pop
                _ok(""),  # untracked paths before pop
                _fail("conflict"),  # stash pop fails
                _ok("restored-dir\0"),  # untracked after failed pop
                _ok(),  # reset --merge
                _ok(),  # checkout --merge -- .
                _ok(""),  # status after rollback
            ]
            result = _restore_stashed_changes("stash@{0}")

        assert result is False
        assert not restored_dir.exists()
        err = capsys.readouterr().err
        assert "rollback succeeded" in err

    def test_removes_untracked_paths_restored_by_failed_pop(self, capsys, monkeypatch, tmp_path):
        """Rollback removes untracked files introduced by a failed stash pop before reporting success."""
        monkeypatch.chdir(tmp_path)
        existing = tmp_path / "existing.txt"
        existing.write_text("keep")
        restored_file = tmp_path / "restored.txt"
        restored_file.write_text("remove")
        restored_dir = tmp_path / "restored-dir"
        restored_dir.mkdir()
        restored_nested = restored_dir / "nested.txt"
        restored_nested.write_text("remove")

        with patch("agentic_devtools.cli.setup.pr_workflow.run_git") as mock_git:
            mock_git.side_effect = [
                _ok("?? existing.txt\0"),  # status snapshot before pop
                _ok("existing.txt\0"),  # untracked paths before pop
                _fail("conflict"),  # stash pop fails
                _ok("existing.txt\0restored.txt\0restored-dir/nested.txt\0"),  # untracked after failed pop
                _ok(),  # reset --merge
                _ok(),  # checkout --merge -- .
                _ok("?? existing.txt\0"),  # status after rollback
            ]
            result = _restore_stashed_changes("stash@{0}")

        assert result is False
        assert existing.exists()
        assert not restored_file.exists()
        assert not restored_nested.exists()
        err = capsys.readouterr().err
        assert "rollback succeeded" in err

    def test_warns_when_cleanup_of_restored_untracked_file_fails(self, capsys, monkeypatch, tmp_path):
        """Cleanup failure falls back to manual recovery instructions."""
        monkeypatch.chdir(tmp_path)
        restored_file = tmp_path / "restored.txt"
        restored_file.write_text("remove")

        with patch("agentic_devtools.cli.setup.pr_workflow.Path.unlink", side_effect=OSError("boom")):
            with patch("agentic_devtools.cli.setup.pr_workflow.run_git") as mock_git:
                mock_git.side_effect = [
                    _ok(""),  # status snapshot before pop
                    _ok(""),  # untracked paths before pop
                    _fail("conflict"),  # stash pop fails
                    _ok("restored.txt\0"),  # untracked after failed pop
                    _ok(),  # reset --merge
                    _ok(),  # checkout --merge -- .
                    _ok("?? restored.txt\0"),  # status after rollback
                ]
                result = _restore_stashed_changes("stash@{0}")

        assert result is False
        err = capsys.readouterr().err
        assert "rollback could not be verified" in err

    def test_returns_false_when_status_snapshot_mismatch_after_rollback(self) -> None:
        """A rollback status mismatch is treated as unverified recovery."""
        with patch("agentic_devtools.cli.setup.pr_workflow.run_git") as mock_git:
            mock_git.side_effect = [
                _ok("before"),  # status snapshot before pop
                _ok(""),  # untracked paths before pop
                _fail(),  # stash pop
                _ok(""),  # untracked paths after failed pop
                _ok(),  # reset --merge
                _ok(),  # checkout --merge
                _ok("different"),  # status after rollback mismatch
            ]
            assert _restore_stashed_changes("stash@{0}") is False
