"""Tests checkout scope and artifact behavior in review_branch_sync."""


class TestCheckoutAndSyncBranch:
    def test_refresh_review_commit_scope_uses_current_head(self):
        """Review setup can refresh its artifact scope after branch synchronization."""
        from unittest.mock import patch

        from agentic_devtools.cli.azure_devops.review_branch_sync import checkout_and_sync_branch
        from agentic_devtools.cli.git.operations import CheckoutResult, RebaseResult

        current_head = "1234567890abcdef1234567890abcdef12345678"
        with patch("agentic_devtools.cli.git.operations.checkout_branch") as mock_checkout:
            with patch("agentic_devtools.cli.git.operations.fetch_branch", return_value=True):
                with patch("agentic_devtools.cli.git.operations.reset_branch_to_origin", return_value=True):
                    with patch("agentic_devtools.cli.git.operations.fetch_main", return_value=True):
                        with patch(
                            "agentic_devtools.cli.git.operations.rebase_onto_main",
                            return_value=RebaseResult(RebaseResult.SUCCESS),
                        ):
                            with patch(
                                "agentic_devtools.cli.git.operations.get_files_changed_on_branch",
                                return_value=["file.ts"],
                            ):
                                with patch("agentic_devtools.cli.git.operations.force_push"):
                                    with patch(
                                        "agentic_devtools.cli.azure_devops.review_branch_sync._get_current_commit_hash",
                                        return_value=current_head,
                                    ):
                                        with patch(
                                            "agentic_devtools.cli.azure_devops.review_branch_sync.get_value",
                                            return_value="oldcommit12",
                                        ):
                                            with patch(
                                                "agentic_devtools.cli.azure_devops.review_branch_sync.set_value"
                                            ) as mock_set_value:
                                                mock_checkout.return_value = CheckoutResult(CheckoutResult.SUCCESS)

                                                success, _error, files, _conflicts, _push = checkout_and_sync_branch(
                                                    "feature/test",
                                                    pull_request_id=123,
                                                    refresh_review_commit_scope=True,
                                                )

        assert success is True
        assert files == {"file.ts"}
        mock_set_value.assert_called_once_with("review.commit_hash_short", current_head[:12])

    def test_save_files_on_branch_rescopes_inventory_when_head_advances_without_push(self, tmp_path):
        """Persist files-on-branch under post-sync HEAD scope when no push occurs."""
        import json
        from unittest.mock import MagicMock, patch

        from agentic_devtools.cli.azure_devops.review_branch_sync import checkout_and_sync_branch
        from agentic_devtools.cli.git.operations import CheckoutResult, RebaseResult

        old_scope = "oldcommit1234"
        new_head = "1234567890abcdef1234567890abcdef12345678"
        with patch("agentic_devtools.cli.git.operations.checkout_branch") as mock_checkout:
            with patch("agentic_devtools.cli.git.operations.fetch_branch", return_value=True):
                with patch("agentic_devtools.cli.git.operations.reset_branch_to_origin", return_value=True):
                    with patch("agentic_devtools.cli.git.operations.fetch_main", return_value=True):
                        with patch(
                            "agentic_devtools.cli.git.operations.rebase_onto_main",
                            return_value=RebaseResult(RebaseResult.NO_REBASE_NEEDED),
                        ):
                            with patch(
                                "agentic_devtools.cli.git.operations.get_files_changed_on_branch",
                                side_effect=AssertionError("Inventory fallback should not run"),
                            ):
                                with patch(
                                    "agentic_devtools.cli.git.operations.get_branch_change_inventory",
                                    return_value=(
                                        ["src/new.ts"],
                                        {"src/new.ts": "edit"},
                                        {},
                                        "main...HEAD",
                                        True,
                                    ),
                                ):
                                    with patch(
                                        "agentic_devtools.cli.azure_devops.review_branch_sync.get_value",
                                        return_value=old_scope,
                                    ):
                                        with patch(
                                            "agentic_devtools.cli.azure_devops.review_branch_sync.get_state_dir",
                                            return_value=tmp_path,
                                        ):
                                            with patch(
                                                "agentic_devtools.cli.azure_devops.review_branch_sync._get_current_commit_hash",
                                                return_value=new_head,
                                            ):
                                                with patch(
                                                    "agentic_devtools.cli.azure_devops.review_branch_sync.set_value"
                                                ) as mock_set_value:
                                                    with patch(
                                                        "agentic_devtools.cli.azure_devops.review_branch_sync.run_safe",
                                                        return_value=MagicMock(
                                                            returncode=0,
                                                            stdout="abc1234\n",
                                                            stderr="",
                                                        ),
                                                    ):
                                                        mock_checkout.return_value = CheckoutResult(
                                                            CheckoutResult.SUCCESS
                                                        )

                                                        success, _error, files, _conflicts, push_succeeded = (
                                                            checkout_and_sync_branch(
                                                                "feature/test",
                                                                pull_request_id=123,
                                                                save_files_on_branch=True,
                                                                refresh_review_commit_scope=True,
                                                            )
                                                        )

        assert success is True
        assert files == {"src/new.ts"}
        assert push_succeeded is None
        mock_set_value.assert_called_once_with("review.commit_hash_short", new_head[:12])

        old_files_json = tmp_path / "pull-request-review" / old_scope / "files-on-branch.json"
        assert not old_files_json.exists()

        new_files_json = tmp_path / "pull-request-review" / new_head[:12] / "files-on-branch.json"
        with open(new_files_json) as f:
            data = json.load(f)
        assert data["files"] == ["src/new.ts"]
        assert data["change_types"] == {"src/new.ts": "edit"}
        assert data["diff_base_ref"] == "abc1234"

    def test_refresh_review_commit_scope_leaves_scope_when_head_unavailable(self):
        """A successful push with an unreadable HEAD leaves the existing review scope unchanged."""
        from unittest.mock import patch

        from agentic_devtools.cli.azure_devops.review_branch_sync import checkout_and_sync_branch
        from agentic_devtools.cli.git.operations import CheckoutResult, RebaseResult

        with patch("agentic_devtools.cli.git.operations.checkout_branch") as mock_checkout:
            with patch("agentic_devtools.cli.git.operations.fetch_branch", return_value=True):
                with patch("agentic_devtools.cli.git.operations.reset_branch_to_origin", return_value=True):
                    with patch("agentic_devtools.cli.git.operations.fetch_main", return_value=True):
                        with patch(
                            "agentic_devtools.cli.git.operations.rebase_onto_main",
                            return_value=RebaseResult(RebaseResult.SUCCESS),
                        ):
                            with patch(
                                "agentic_devtools.cli.git.operations.get_files_changed_on_branch",
                                return_value=["file.ts"],
                            ):
                                with patch("agentic_devtools.cli.git.operations.force_push"):
                                    with patch(
                                        "agentic_devtools.cli.azure_devops.review_branch_sync._get_current_commit_hash",
                                        return_value=None,
                                    ):
                                        with patch(
                                            "agentic_devtools.cli.azure_devops.review_branch_sync.set_value"
                                        ) as mock_set_value:
                                            mock_checkout.return_value = CheckoutResult(CheckoutResult.SUCCESS)

                                            success, _error, files, _conflicts, push_succeeded = (
                                                checkout_and_sync_branch(
                                                    "feature/test",
                                                    refresh_review_commit_scope=True,
                                                )
                                            )

        assert success is True
        assert files == {"file.ts"}
        assert push_succeeded is True
        mock_set_value.assert_not_called()

    def test_does_not_refresh_scope_when_force_push_fails(self):
        """A local-only rebase does not move review scope away from the PR head."""
        from unittest.mock import patch

        from agentic_devtools.cli.azure_devops.review_branch_sync import checkout_and_sync_branch
        from agentic_devtools.cli.git.operations import CheckoutResult, RebaseResult

        with patch("agentic_devtools.cli.git.operations.checkout_branch") as mock_checkout:
            with patch("agentic_devtools.cli.git.operations.fetch_branch", return_value=True):
                with patch("agentic_devtools.cli.git.operations.reset_branch_to_origin", return_value=True):
                    with patch("agentic_devtools.cli.git.operations.fetch_main", return_value=True):
                        with patch(
                            "agentic_devtools.cli.git.operations.rebase_onto_main",
                            return_value=RebaseResult(RebaseResult.SUCCESS),
                        ):
                            with patch(
                                "agentic_devtools.cli.git.operations.get_files_changed_on_branch",
                                return_value=["file.ts"],
                            ):
                                with patch(
                                    "agentic_devtools.cli.git.operations.force_push",
                                    side_effect=SystemExit(1),
                                ):
                                    with patch(
                                        "agentic_devtools.cli.azure_devops.review_branch_sync._get_current_commit_hash"
                                    ) as mock_current_head:
                                        with patch(
                                            "agentic_devtools.cli.azure_devops.review_branch_sync.get_value",
                                            return_value="oldcommit12",
                                        ):
                                            with patch(
                                                "agentic_devtools.cli.azure_devops.review_branch_sync.set_value"
                                            ) as mock_set_value:
                                                mock_checkout.return_value = CheckoutResult(CheckoutResult.SUCCESS)

                                                success, _error, files, _conflicts, push_succeeded = (
                                                    checkout_and_sync_branch(
                                                        "feature/test",
                                                        pull_request_id=123,
                                                        refresh_review_commit_scope=True,
                                                    )
                                                )

        assert success is True
        assert files == {"file.ts"}
        assert push_succeeded is False
        mock_current_head.assert_not_called()
        mock_set_value.assert_not_called()
