"""Tests for the delete_review_comments_command CLI entry point."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.cli.ci.delete_review_comments_command import (
    _resolve_repo_path,
    delete_review_comments_command,
)
from agentic_devtools.cli.ci.models import ReviewCommentDeletionResult, ReviewCommentTarget

_MODULE = "agentic_devtools.cli.ci.delete_review_comments_command"


def _target(**overrides: object) -> ReviewCommentTarget:
    base: dict[str, object] = {
        "thread_id": 1,
        "comment_id": 2,
        "comment_type": "text",
        "marker_type": "file-summary",
        "snippet": "summary",
    }
    base.update(overrides)
    return ReviewCommentTarget(**base)  # type: ignore[arg-type]


class TestDeleteReviewCommentsCommand:
    """Tests for the command return codes and error handling."""

    def test_build_provider_value_error_returns_2(self, capsys) -> None:
        with patch(f"{_MODULE}._build_provider", side_effect=ValueError("bad config")):
            exit_code = delete_review_comments_command(["--pr", "42"])
        assert exit_code == 2
        assert "bad config" in capsys.readouterr().err

    def test_not_implemented_returns_1(self, capsys) -> None:
        provider = MagicMock()
        provider.delete_review_comments.side_effect = NotImplementedError("ADO only")
        with patch(f"{_MODULE}._build_provider", return_value=provider):
            exit_code = delete_review_comments_command(["--pr", "42"])
        assert exit_code == 1
        assert "ADO only" in capsys.readouterr().err

    def test_runtime_error_returns_1(self, capsys) -> None:
        provider = MagicMock()
        provider.delete_review_comments.side_effect = RuntimeError("repo lookup failed")
        with patch(f"{_MODULE}._build_provider", return_value=provider):
            exit_code = delete_review_comments_command(["--pr", "7"])
        assert exit_code == 1
        assert "repo lookup failed" in capsys.readouterr().err

    def test_os_error_returns_1(self, capsys) -> None:
        provider = MagicMock()
        provider.delete_review_comments.side_effect = OSError("no PAT")
        with patch(f"{_MODULE}._build_provider", return_value=provider):
            exit_code = delete_review_comments_command(["--pr", "7"])
        assert exit_code == 1
        assert "no PAT" in capsys.readouterr().err

    def test_dry_run_success_returns_0(self, capsys) -> None:
        provider = MagicMock()
        provider.delete_review_comments.return_value = ReviewCommentDeletionResult(executed=False, targets=(_target(),))
        with patch(f"{_MODULE}._build_provider", return_value=provider):
            exit_code = delete_review_comments_command(["--pr", "42"])
        assert exit_code == 0
        out = capsys.readouterr().out
        assert "[DRY-RUN]" in out
        provider.delete_review_comments.assert_called_once_with(42, execute=False, author_substring=None)

    def test_execute_with_failures_returns_1(self) -> None:
        provider = MagicMock()
        provider.delete_review_comments.return_value = ReviewCommentDeletionResult(
            executed=True, targets=(_target(error="HTTP 500", deleted=False),)
        )
        with patch(f"{_MODULE}._build_provider", return_value=provider):
            exit_code = delete_review_comments_command(["--pr", "42", "--execute"])
        assert exit_code == 1

    def test_execute_clean_returns_0(self) -> None:
        provider = MagicMock()
        provider.delete_review_comments.return_value = ReviewCommentDeletionResult(
            executed=True, targets=(_target(deleted=True),)
        )
        with patch(f"{_MODULE}._build_provider", return_value=provider):
            exit_code = delete_review_comments_command(["--pr", "42", "--execute"])
        assert exit_code == 0

    def test_passes_author_and_execute_flags(self) -> None:
        provider = MagicMock()
        provider.delete_review_comments.return_value = ReviewCommentDeletionResult(executed=True, targets=())
        with patch(f"{_MODULE}._build_provider", return_value=provider):
            delete_review_comments_command(["-p", "9", "--author", "Marsnik", "--execute"])
        provider.delete_review_comments.assert_called_once_with(9, execute=True, author_substring="Marsnik")

    def test_missing_pr_raises_systemexit(self) -> None:
        with pytest.raises(SystemExit):
            delete_review_comments_command([])

    def test_uses_resolved_repo_root_for_provider_dispatch(self) -> None:
        provider = MagicMock()
        provider.delete_review_comments.return_value = ReviewCommentDeletionResult(executed=False, targets=())
        with (
            patch(f"{_MODULE}._resolve_repo_path", return_value="/repo/root"),
            patch(f"{_MODULE}._build_provider", return_value=provider) as build_provider,
        ):
            delete_review_comments_command(["--pr", "42"])
        build_provider.assert_called_once()
        assert build_provider.call_args.args[1] == "/repo/root"


class TestResolveRepoPath:
    """Tests for repository root resolution."""

    def test_uses_git_toplevel_when_available(self) -> None:
        result = MagicMock(returncode=0, stdout="/repo/root\n")
        with patch(f"{_MODULE}.run_safe", return_value=result):
            assert _resolve_repo_path() == "/repo/root"

    def test_falls_back_to_cwd_when_git_command_fails(self) -> None:
        with (
            patch(f"{_MODULE}.run_safe", side_effect=OSError("git missing")),
            patch(f"{_MODULE}.os.getcwd", return_value="/cwd"),
        ):
            assert _resolve_repo_path() == "/cwd"

    def test_falls_back_to_cwd_when_git_returns_nonzero(self) -> None:
        result = MagicMock(returncode=1, stdout="")
        with (
            patch(f"{_MODULE}.run_safe", return_value=result),
            patch(f"{_MODULE}.os.getcwd", return_value="/cwd"),
        ):
            assert _resolve_repo_path() == "/cwd"

    def test_falls_back_to_cwd_when_git_returns_empty_repo_root(self) -> None:
        result = MagicMock(returncode=0, stdout="")
        with (
            patch(f"{_MODULE}.run_safe", return_value=result),
            patch(f"{_MODULE}.os.getcwd", return_value="/cwd"),
        ):
            assert _resolve_repo_path() == "/cwd"
