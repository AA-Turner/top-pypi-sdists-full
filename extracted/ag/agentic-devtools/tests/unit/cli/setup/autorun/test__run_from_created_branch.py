"""Tests for _run_from_created_branch."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.cli.setup.autorun import _PHASE_NAME, _run_from_created_branch
from agentic_devtools.cli.setup.report import PhaseResult, SetupReport
from agentic_devtools.cli.setup.script_generators.constants import (
    ORCHESTRATOR_MARKER,
    ROOT_ENTRY_POINT_FILENAME,
)

_TARGET_REPO_ROOT = Path("/tmp/user-repo-root")


def _make_report() -> SetupReport:
    return SetupReport(
        schema_version=1,
        timestamp="2026-01-01T00:00:00+00:00",
        exit_code=0,
        exit_code_name="OK",
    )


def _make_fake_run_git(
    *,
    add_returncode: int = 0,
    remove_returncode: int = 0,
    prune_returncode: int = 0,
    write_script: bool = True,
):
    """Return a fake ``run_git`` recording calls on ``.calls``.

    On ``worktree add`` it creates the target directory and (optionally) writes a
    managed script so the subsequent ``_locate_and_run`` finds a valid entry-point.
    """
    calls: list[tuple[str, ...]] = []

    def _fake_run_git(*args: str, check: bool = True) -> MagicMock:
        calls.append(args)
        result = MagicMock()
        result.stderr = "boom" if add_returncode != 0 else ""
        if args[:2] == ("worktree", "add"):
            result.returncode = add_returncode
            if add_returncode == 0:
                worktree_dir = Path(args[3])
                worktree_dir.mkdir(parents=True, exist_ok=True)
                if write_script:
                    worktree_dir_script = worktree_dir / ROOT_ENTRY_POINT_FILENAME
                    worktree_dir_script.write_text(
                        f"{ORCHESTRATOR_MARKER}\n# managed script content\n",
                        encoding="utf-8",
                    )
        elif args[:2] == ("worktree", "remove"):
            result.returncode = remove_returncode
        elif args[:2] == ("worktree", "prune"):
            result.returncode = prune_returncode
        else:
            result.returncode = 0
        return result

    _fake_run_git.calls = calls  # type: ignore[attr-defined]
    return _fake_run_git


class TestRunFromCreatedBranchSuccess:
    """Worktree is created, the script runs, and the worktree is removed."""

    def test_runs_script_and_removes_worktree(self, capsys: pytest.CaptureFixture[str]) -> None:
        report = _make_report()
        fake_run_git = _make_fake_run_git()
        mock_result = MagicMock()
        mock_result.returncode = 0

        with (
            patch("agentic_devtools.cli.setup.autorun.run_safe", return_value=mock_result) as mock_run,
            patch("agentic_devtools.cli.git.core.run_git", side_effect=fake_run_git),
        ):
            _run_from_created_branch("chore/agdt-setup-1.0", _TARGET_REPO_ROOT, report)

        mock_run.assert_called_once()
        assert report.phases[0].status == "success"
        assert fake_run_git.calls[0][:3] == ("worktree", "add", "--detach")
        assert fake_run_git.calls[0][4] == "chore/agdt-setup-1.0"
        assert any(call[:2] == ("worktree", "remove") for call in fake_run_git.calls)
        # A successful removal must not trigger a prune fallback.
        assert all(call[:2] != ("worktree", "prune") for call in fake_run_git.calls)

    def test_worktree_removed_even_when_run_fails(self) -> None:
        """The temporary worktree is torn down even if the child run fails."""
        report = _make_report()
        fake_run_git = _make_fake_run_git()
        mock_result = MagicMock()
        mock_result.returncode = 1

        with (
            patch("agentic_devtools.cli.setup.autorun.run_safe", return_value=mock_result),
            patch("agentic_devtools.cli.git.core.run_git", side_effect=fake_run_git),
        ):
            _run_from_created_branch("chore/agdt-setup-1.0", _TARGET_REPO_ROOT, report)

        assert report.phases[0].status == "failed"
        assert any(call[:2] == ("worktree", "remove") for call in fake_run_git.calls)


class TestRunFromCreatedBranchCheckoutFailure:
    """A failed ``worktree add`` records a failed phase and runs nothing."""

    def test_records_failure_and_does_not_run(self, capsys: pytest.CaptureFixture[str]) -> None:
        report = _make_report()
        fake_run_git = _make_fake_run_git(add_returncode=1)

        with (
            patch("agentic_devtools.cli.setup.autorun.run_safe") as mock_run,
            patch("agentic_devtools.cli.git.core.run_git", side_effect=fake_run_git),
        ):
            _run_from_created_branch("chore/agdt-setup-1.0", _TARGET_REPO_ROOT, report)

        mock_run.assert_not_called()
        assert report.phases[0].status == "failed"
        assert report.phases[0].name == _PHASE_NAME
        assert "chore/agdt-setup-1.0" in (report.phases[0].error or "")
        # No removal is attempted when the add failed.
        assert all(call[:2] != ("worktree", "remove") for call in fake_run_git.calls)
        assert "could not check out branch" in capsys.readouterr().err


class TestRunFromCreatedBranchCleanup:
    """Stale worktree metadata is pruned when removal fails."""

    def test_prunes_when_remove_fails(self) -> None:
        report = _make_report()
        fake_run_git = _make_fake_run_git(remove_returncode=1)
        mock_result = MagicMock()
        mock_result.returncode = 0

        with (
            patch("agentic_devtools.cli.setup.autorun.run_safe", return_value=mock_result),
            patch("agentic_devtools.cli.git.core.run_git", side_effect=fake_run_git),
        ):
            _run_from_created_branch("chore/agdt-setup-1.0", _TARGET_REPO_ROOT, report)

        # The run itself succeeded ...
        assert report.phases[0].status == "success"
        # ... but the failed removal must be followed by a prune.
        remove_index = next(i for i, call in enumerate(fake_run_git.calls) if call[:2] == ("worktree", "remove"))
        prune_index = next(
            i for i, call in enumerate(fake_run_git.calls) if call[:4] == ("worktree", "prune", "--expire", "now")
        )
        assert prune_index > remove_index

    def test_no_prune_when_remove_succeeds(self) -> None:
        report = _make_report()
        fake_run_git = _make_fake_run_git(remove_returncode=0)
        mock_result = MagicMock()
        mock_result.returncode = 0

        with (
            patch("agentic_devtools.cli.setup.autorun.run_safe", return_value=mock_result),
            patch("agentic_devtools.cli.git.core.run_git", side_effect=fake_run_git),
        ):
            _run_from_created_branch("chore/agdt-setup-1.0", _TARGET_REPO_ROOT, report)

        assert all(call[:2] != ("worktree", "prune") for call in fake_run_git.calls)

    def test_records_failure_when_remove_and_prune_fail(self) -> None:
        report = _make_report()
        fake_run_git = _make_fake_run_git(remove_returncode=1, prune_returncode=1)
        mock_result = MagicMock()
        mock_result.returncode = 0

        with (
            patch("agentic_devtools.cli.setup.autorun.run_safe", return_value=mock_result),
            patch("agentic_devtools.cli.git.core.run_git", side_effect=fake_run_git),
        ):
            _run_from_created_branch("chore/agdt-setup-1.0", _TARGET_REPO_ROOT, report)

        assert report.phases[0].status == "failed"
        assert report.phases[0].error is not None
        assert "Worktree cleanup failed after autorun" in report.phases[0].error

    def test_preserves_child_failure_when_cleanup_also_fails(self) -> None:
        report = _make_report()
        fake_run_git = _make_fake_run_git(remove_returncode=1, prune_returncode=1)
        mock_result = MagicMock()
        mock_result.returncode = 1

        with (
            patch("agentic_devtools.cli.setup.autorun.run_safe", return_value=mock_result),
            patch("agentic_devtools.cli.git.core.run_git", side_effect=fake_run_git),
        ):
            _run_from_created_branch("chore/agdt-setup-1.0", _TARGET_REPO_ROOT, report)

        assert report.phases[0].status == "failed"
        assert report.phases[0].error == "Child process exited with code 1"

    def test_records_cleanup_failure_when_no_phase_was_recorded(self) -> None:
        report = _make_report()
        fake_run_git = _make_fake_run_git(remove_returncode=1, prune_returncode=1)

        with (
            patch("agentic_devtools.cli.setup.autorun._locate_and_run") as mock_locate,
            patch("agentic_devtools.cli.git.core.run_git", side_effect=fake_run_git),
        ):
            _run_from_created_branch("chore/agdt-setup-1.0", _TARGET_REPO_ROOT, report)

        locate_call = mock_locate.call_args
        assert locate_call is not None
        assert locate_call.kwargs["target_repo_root"] == _TARGET_REPO_ROOT
        assert report.phases[0].status == "failed"
        assert report.phases[0].error is not None
        assert "Worktree cleanup failed after autorun" in report.phases[0].error

    def test_detects_existing_autorun_after_unrelated_phase(self) -> None:
        report = _make_report()
        report.record(PhaseResult(name="precheck", status="success"))
        fake_run_git = _make_fake_run_git(remove_returncode=1, prune_returncode=1)
        mock_result = MagicMock()
        mock_result.returncode = 0

        with (
            patch("agentic_devtools.cli.setup.autorun.run_safe", return_value=mock_result),
            patch("agentic_devtools.cli.git.core.run_git", side_effect=fake_run_git),
        ):
            _run_from_created_branch("chore/agdt-setup-1.0", _TARGET_REPO_ROOT, report)

        autorun_phase = next(phase for phase in report.phases if phase.name == _PHASE_NAME)
        assert autorun_phase.status == "failed"
        assert autorun_phase.error is not None
        assert "Worktree cleanup failed after autorun" in autorun_phase.error


class TestRunFromCreatedBranchReturnValue:
    """_run_from_created_branch returns False on pre-invocation failure, True otherwise."""

    def test_returns_false_when_worktree_add_fails(self) -> None:
        """Returns False when ``git worktree add`` fails (child never started)."""
        report = _make_report()
        fake_run_git = _make_fake_run_git(add_returncode=1)
        with (
            patch("agentic_devtools.cli.setup.autorun.run_safe"),
            patch("agentic_devtools.cli.git.core.run_git", side_effect=fake_run_git),
        ):
            result = _run_from_created_branch("chore/agdt-setup-1.0", _TARGET_REPO_ROOT, report)
        assert result is False

    def test_returns_true_when_child_invoked_successfully(self) -> None:
        """Returns True when the child process was invoked and succeeded."""
        report = _make_report()
        fake_run_git = _make_fake_run_git()
        mock_result = MagicMock()
        mock_result.returncode = 0
        with (
            patch("agentic_devtools.cli.setup.autorun.run_safe", return_value=mock_result),
            patch("agentic_devtools.cli.git.core.run_git", side_effect=fake_run_git),
        ):
            result = _run_from_created_branch("chore/agdt-setup-1.0", _TARGET_REPO_ROOT, report)
        assert result is True

    def test_returns_true_when_child_fails(self) -> None:
        """Returns True even when the child process fails (it was invoked)."""
        import subprocess

        report = _make_report()
        fake_run_git = _make_fake_run_git()
        with (
            patch(
                "agentic_devtools.cli.setup.autorun.run_safe",
                side_effect=subprocess.CalledProcessError(3, "setup-dev-tools.py"),
            ),
            patch("agentic_devtools.cli.git.core.run_git", side_effect=fake_run_git),
        ):
            result = _run_from_created_branch("chore/agdt-setup-1.0", _TARGET_REPO_ROOT, report)
        assert result is True
