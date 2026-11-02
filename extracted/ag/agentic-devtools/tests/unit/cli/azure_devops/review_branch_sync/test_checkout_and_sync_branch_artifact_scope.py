"""Tests for branch-sync artifact directory selection."""

from unittest.mock import MagicMock, patch

from agentic_devtools.cli.azure_devops import review_branch_sync
from agentic_devtools.cli.git.operations import CheckoutResult, RebaseResult


class TestCheckoutAndSyncBranchArtifactScope:
    def test_missing_commit_hash_falls_back_to_pr_directory(self, tmp_path):
        with (
            patch(
                "agentic_devtools.cli.git.operations.checkout_branch",
                return_value=CheckoutResult(CheckoutResult.SUCCESS),
            ),
            patch("agentic_devtools.cli.git.operations.fetch_branch", return_value=True),
            patch("agentic_devtools.cli.git.operations.reset_branch_to_origin", return_value=True),
            patch("agentic_devtools.cli.git.operations.fetch_main", return_value=True),
            patch(
                "agentic_devtools.cli.git.operations.rebase_onto_main",
                return_value=RebaseResult(RebaseResult.NO_REBASE_NEEDED),
            ),
            patch(
                "agentic_devtools.cli.git.operations.get_branch_change_inventory",
                return_value=(["src/file.ts"], {"src/file.ts": "edit"}, {}, "origin/main...HEAD", True),
            ),
            patch.object(review_branch_sync, "get_value", return_value=None),
            patch.object(review_branch_sync, "get_state_dir", return_value=tmp_path),
            patch.object(
                review_branch_sync,
                "run_safe",
                return_value=MagicMock(returncode=0, stdout="base-commit\n"),
            ),
        ):
            success, _, _, _, _ = review_branch_sync.checkout_and_sync_branch(
                "feature/test",
                pull_request_id=789,
                save_files_on_branch=True,
            )

        assert success is True
        assert (tmp_path / "pull-request-review" / "PR789" / "files-on-branch.json").exists()

    def test_unsafe_commit_hash_falls_back_to_pr_directory(self, tmp_path, capsys):
        with (
            patch(
                "agentic_devtools.cli.git.operations.checkout_branch",
                return_value=CheckoutResult(CheckoutResult.SUCCESS),
            ),
            patch("agentic_devtools.cli.git.operations.fetch_branch", return_value=True),
            patch("agentic_devtools.cli.git.operations.reset_branch_to_origin", return_value=True),
            patch("agentic_devtools.cli.git.operations.fetch_main", return_value=True),
            patch(
                "agentic_devtools.cli.git.operations.rebase_onto_main",
                return_value=RebaseResult(RebaseResult.NO_REBASE_NEEDED),
            ),
            patch(
                "agentic_devtools.cli.git.operations.get_branch_change_inventory",
                return_value=(["src/file.ts"], {"src/file.ts": "edit"}, {}, "origin/main...HEAD", True),
            ),
            patch.object(
                review_branch_sync,
                "get_value",
                side_effect=lambda key, *args, **kwargs: "../evil" if key == "review.commit_hash_short" else None,
            ),
            patch.object(review_branch_sync, "get_state_dir", return_value=tmp_path),
            patch.object(
                review_branch_sync,
                "run_safe",
                return_value=MagicMock(returncode=0, stdout="base-commit\n"),
            ),
        ):
            success, _, _, _, _ = review_branch_sync.checkout_and_sync_branch(
                "feature/test",
                pull_request_id=789,
                save_files_on_branch=True,
            )

        assert success is True
        assert (tmp_path / "pull-request-review" / "PR789" / "files-on-branch.json").exists()
        assert "unsafe" in capsys.readouterr().err
