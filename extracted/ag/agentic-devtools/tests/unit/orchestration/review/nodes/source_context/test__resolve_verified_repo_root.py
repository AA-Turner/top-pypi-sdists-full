"""Tests for _resolve_verified_repo_root helper."""

from __future__ import annotations

from pathlib import Path
from subprocess import CompletedProcess
from unittest.mock import patch

from agentic_devtools.orchestration.review.nodes.source_context import _resolve_verified_repo_root


class TestResolveVerifiedRepoRoot:
    """Tests for _resolve_verified_repo_root."""

    def test_blank_repo_root_returns_none(self) -> None:
        """Blank repo-root values are rejected."""
        with patch(
            "agentic_devtools.cli.azure_devops.pr_review_manifest.resolve_repo_root",
            return_value="",
        ):
            assert _resolve_verified_repo_root([{"path": "/src/app.py"}], "abc123") is None

    def test_blank_commit_hash_returns_none(self, tmp_path: Path) -> None:
        """A repo root without the reviewed commit hash is not trusted."""
        with patch(
            "agentic_devtools.cli.azure_devops.pr_review_manifest.resolve_repo_root",
            return_value=str(tmp_path),
        ):
            assert _resolve_verified_repo_root([{"path": "/src/app.py"}], "") is None

    def test_existing_file_path_verifies_repo_root(self, tmp_path: Path) -> None:
        """A changed file present under the reviewed HEAD verifies the checkout."""
        (tmp_path / "src").mkdir()
        (tmp_path / "src" / "app.py").write_text("print('hi')\n")

        with (
            patch(
                "agentic_devtools.cli.azure_devops.pr_review_manifest.resolve_repo_root",
                return_value=str(tmp_path),
            ),
            patch(
                "agentic_devtools.orchestration.review.nodes.source_context.subprocess.run",
                return_value=CompletedProcess(args=[], returncode=0, stdout="abc123\n", stderr=""),
            ),
        ):
            assert _resolve_verified_repo_root([{"path": "/src/app.py"}], "abc123") == tmp_path.as_posix()

    def test_short_reviewed_hash_matching_head_prefix_is_allowed(self, tmp_path: Path) -> None:
        """A 7+ character reviewed short SHA is allowed when it matches the local HEAD prefix."""
        (tmp_path / "src").mkdir()
        (tmp_path / "src" / "app.py").write_text("print('hi')\n")

        with (
            patch(
                "agentic_devtools.cli.azure_devops.pr_review_manifest.resolve_repo_root",
                return_value=str(tmp_path),
            ),
            patch(
                "agentic_devtools.orchestration.review.nodes.source_context.subprocess.run",
                return_value=CompletedProcess(args=[], returncode=0, stdout="abc123def456\n", stderr=""),
            ),
        ):
            assert _resolve_verified_repo_root([{"path": "/src/app.py"}], "abc123d") == tmp_path.as_posix()

    def test_too_short_reviewed_hash_is_rejected(self, tmp_path: Path) -> None:
        """Very short SHAs are rejected even when they match the local HEAD prefix."""
        (tmp_path / "src").mkdir()
        (tmp_path / "src" / "app.py").write_text("print('hi')\n")

        with (
            patch(
                "agentic_devtools.cli.azure_devops.pr_review_manifest.resolve_repo_root",
                return_value=str(tmp_path),
            ),
            patch(
                "agentic_devtools.orchestration.review.nodes.source_context.subprocess.run",
                return_value=CompletedProcess(args=[], returncode=0, stdout="abc123def456\n", stderr=""),
            ),
        ):
            assert _resolve_verified_repo_root([{"path": "/src/app.py"}], "abc") is None

    def test_existing_original_path_verifies_repo_root(self, tmp_path: Path) -> None:
        """A rename's originalPath can verify the checkout."""
        (tmp_path / "src").mkdir()
        (tmp_path / "src" / "old_name.py").write_text("print('hi')\n")

        with (
            patch(
                "agentic_devtools.cli.azure_devops.pr_review_manifest.resolve_repo_root",
                return_value=str(tmp_path),
            ),
            patch(
                "agentic_devtools.orchestration.review.nodes.source_context.subprocess.run",
                return_value=CompletedProcess(args=[], returncode=0, stdout="abc123\n", stderr=""),
            ),
        ):
            assert (
                _resolve_verified_repo_root(
                    [{"path": "/src/new_name.py", "originalPath": "/src/old_name.py"}],
                    "abc123",
                )
                == tmp_path.as_posix()
            )

    def test_mismatched_head_commit_rejects_repo_root(self, tmp_path: Path) -> None:
        """A checkout at the wrong HEAD commit is treated as unverified."""
        (tmp_path / "src").mkdir()
        (tmp_path / "src" / "app.py").write_text("print('hi')\n")

        with (
            patch(
                "agentic_devtools.cli.azure_devops.pr_review_manifest.resolve_repo_root",
                return_value=str(tmp_path),
            ),
            patch(
                "agentic_devtools.orchestration.review.nodes.source_context.subprocess.run",
                return_value=CompletedProcess(args=[], returncode=0, stdout="def456\n", stderr=""),
            ),
        ):
            assert _resolve_verified_repo_root([{"path": "/src/app.py"}], "abc123") is None

    def test_git_head_lookup_failure_rejects_repo_root(self, tmp_path: Path) -> None:
        """A failing git HEAD lookup leaves the repo root unverified."""
        with (
            patch(
                "agentic_devtools.cli.azure_devops.pr_review_manifest.resolve_repo_root",
                return_value=str(tmp_path),
            ),
            patch(
                "agentic_devtools.orchestration.review.nodes.source_context.subprocess.run",
                side_effect=OSError("git missing"),
            ),
        ):
            assert _resolve_verified_repo_root([{"path": "/src/app.py"}], "abc123") is None

    def test_no_matching_paths_returns_none(self, tmp_path: Path) -> None:
        """A matching HEAD without any relevant files does not verify the root."""
        with (
            patch(
                "agentic_devtools.cli.azure_devops.pr_review_manifest.resolve_repo_root",
                return_value=str(tmp_path),
            ),
            patch(
                "agentic_devtools.orchestration.review.nodes.source_context.subprocess.run",
                return_value=CompletedProcess(args=[], returncode=0, stdout="abc123\n", stderr=""),
            ),
        ):
            assert _resolve_verified_repo_root([{"path": "/src/missing.py"}], "abc123") is None
