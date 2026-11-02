"""Tests branch inventory behavior in review_branch_sync."""


class TestCheckoutAndSyncBranch:
    def test_save_files_on_branch_writes_json(self, tmp_path):
        """Test save_files_on_branch=True writes files-on-branch.json.

        Covers lines 264-272.
        """
        import json
        from unittest.mock import MagicMock, patch

        from agentic_devtools.cli.azure_devops.review_branch_sync import checkout_and_sync_branch
        from agentic_devtools.cli.git.operations import CheckoutResult, RebaseResult

        with patch("agentic_devtools.cli.git.operations.checkout_branch") as mock_checkout:
            with patch("agentic_devtools.cli.git.operations.fetch_branch") as mock_fetch_branch:
                with patch("agentic_devtools.cli.git.operations.reset_branch_to_origin") as mock_reset:
                    with patch("agentic_devtools.cli.git.operations.fetch_main") as mock_fetch:
                        with patch("agentic_devtools.cli.git.operations.rebase_onto_main") as mock_rebase:
                            with patch("agentic_devtools.cli.git.operations.get_files_changed_on_branch") as mock_files:
                                with patch(
                                    "agentic_devtools.cli.git.operations.get_branch_change_inventory"
                                ) as mock_inventory:
                                    with patch(
                                        "agentic_devtools.cli.azure_devops.review_branch_sync.get_value",
                                        return_value="abc123def456",
                                    ):
                                        with patch(
                                            "agentic_devtools.cli.azure_devops.review_branch_sync.get_state_dir",
                                            return_value=tmp_path,
                                        ):
                                            with patch(
                                                "agentic_devtools.cli.azure_devops.review_branch_sync.run_safe"
                                            ) as mock_run_safe:
                                                mock_checkout.return_value = CheckoutResult(CheckoutResult.SUCCESS)
                                                mock_fetch_branch.return_value = True
                                                mock_reset.return_value = True
                                                mock_fetch.return_value = True
                                                mock_rebase.return_value = RebaseResult(RebaseResult.NO_REBASE_NEEDED)
                                                mock_files.side_effect = AssertionError(
                                                    "Fallback file listing should not be used "
                                                    "on successful inventory lookup"
                                                )
                                                mock_inventory.return_value = (
                                                    ["src/a.ts", "src/b.ts"],
                                                    {"src/a.ts": "edit", "src/b.ts": "add"},
                                                    {},
                                                    "main...HEAD",
                                                    True,
                                                )
                                                mock_run_safe.return_value = MagicMock(
                                                    returncode=0,
                                                    stdout="abc1234\n",
                                                    stderr="",
                                                )

                                                success, _error, files, _conflicts, _push = checkout_and_sync_branch(
                                                    "feature/test",
                                                    pull_request_id=123,
                                                    save_files_on_branch=True,
                                                )

                                            assert success is True
                                            assert files == {"src/a.ts", "src/b.ts"}

                                            files_json = (
                                                tmp_path
                                                / "pull-request-review"
                                                / "abc123def456"
                                                / "files-on-branch.json"
                                            )
                                            assert files_json.exists()
                                            with open(files_json) as f:
                                                data = json.load(f)
                                            assert set(data["files"]) == {"src/a.ts", "src/b.ts"}
                                            assert data["change_types"] == {
                                                "src/a.ts": "edit",
                                                "src/b.ts": "add",
                                            }
                                            assert data["rename_sources"] == {}
                                            assert data["diff_base_ref"] == "abc1234"
                                            mock_run_safe.assert_called_once_with(
                                                ["git", "merge-base", "main", "HEAD"],
                                                capture_output=True,
                                                text=True,
                                                shell=False,
                                            )

    def test_save_files_on_branch_uses_branch_ref_when_merge_base_fails(self, tmp_path, capsys):
        """Persist branch ref when merge-base resolution fails."""
        import json
        from unittest.mock import MagicMock, patch

        from agentic_devtools.cli.azure_devops.review_branch_sync import checkout_and_sync_branch
        from agentic_devtools.cli.git.operations import CheckoutResult, RebaseResult

        with patch("agentic_devtools.cli.git.operations.checkout_branch") as mock_checkout:
            with patch("agentic_devtools.cli.git.operations.fetch_branch") as mock_fetch_branch:
                with patch("agentic_devtools.cli.git.operations.reset_branch_to_origin") as mock_reset:
                    with patch("agentic_devtools.cli.git.operations.fetch_main") as mock_fetch:
                        with patch("agentic_devtools.cli.git.operations.rebase_onto_main") as mock_rebase:
                            with patch("agentic_devtools.cli.git.operations.get_files_changed_on_branch") as mock_files:
                                with patch(
                                    "agentic_devtools.cli.git.operations.get_branch_change_inventory"
                                ) as mock_inventory:
                                    with patch(
                                        "agentic_devtools.cli.azure_devops.review_branch_sync.get_value",
                                        return_value="abc123def456",
                                    ):
                                        with patch(
                                            "agentic_devtools.cli.azure_devops.review_branch_sync.get_state_dir",
                                            return_value=tmp_path,
                                        ):
                                            with patch(
                                                "agentic_devtools.cli.azure_devops.review_branch_sync.run_safe",
                                            ) as mock_run_safe:
                                                mock_checkout.return_value = CheckoutResult(CheckoutResult.SUCCESS)
                                                mock_fetch_branch.return_value = True
                                                mock_reset.return_value = True
                                                mock_fetch.return_value = True
                                                mock_rebase.return_value = RebaseResult(RebaseResult.NO_REBASE_NEEDED)
                                                mock_files.side_effect = AssertionError(
                                                    "Fallback file listing should not be used "
                                                    "on successful inventory lookup"
                                                )
                                                mock_inventory.return_value = (
                                                    ["src/a.ts"],
                                                    {"src/a.ts": "edit"},
                                                    {},
                                                    "main...HEAD",
                                                    True,
                                                )
                                                mock_run_safe.return_value = MagicMock(
                                                    returncode=128,
                                                    stdout="",
                                                    stderr="error",
                                                )

                                                success, _error, files, _conflicts, _push = checkout_and_sync_branch(
                                                    "feature/test",
                                                    pull_request_id=123,
                                                    save_files_on_branch=True,
                                                )

                                                assert success is True
                                                assert files == {"src/a.ts"}

                                                files_json = (
                                                    tmp_path
                                                    / "pull-request-review"
                                                    / "abc123def456"
                                                    / "files-on-branch.json"
                                                )
                                                with open(files_json) as f:
                                                    data = json.load(f)
                                                assert data["diff_base_ref"] == "main"
                                                assert (
                                                    "Warning: Could not resolve merge-base for 'main...HEAD'"
                                                    in capsys.readouterr().err
                                                )

    def test_save_files_on_branch_sets_null_diff_base_ref_when_diff_ref_unavailable(self, tmp_path):
        """Persist null diff_base_ref when no diff ref can be resolved."""
        import json
        from unittest.mock import patch

        from agentic_devtools.cli.azure_devops.review_branch_sync import checkout_and_sync_branch
        from agentic_devtools.cli.git.operations import CheckoutResult, RebaseResult

        with patch("agentic_devtools.cli.git.operations.checkout_branch") as mock_checkout:
            with patch("agentic_devtools.cli.git.operations.fetch_branch") as mock_fetch_branch:
                with patch("agentic_devtools.cli.git.operations.reset_branch_to_origin") as mock_reset:
                    with patch("agentic_devtools.cli.git.operations.fetch_main") as mock_fetch:
                        with patch("agentic_devtools.cli.git.operations.rebase_onto_main") as mock_rebase:
                            with patch("agentic_devtools.cli.git.operations.get_files_changed_on_branch") as mock_files:
                                with patch(
                                    "agentic_devtools.cli.git.operations.get_branch_change_inventory"
                                ) as mock_inventory:
                                    with patch(
                                        "agentic_devtools.cli.azure_devops.review_branch_sync.get_value",
                                        return_value="abc123def456",
                                    ):
                                        with patch(
                                            "agentic_devtools.cli.azure_devops.review_branch_sync.get_state_dir",
                                            return_value=tmp_path,
                                        ):
                                            with patch(
                                                "agentic_devtools.cli.azure_devops.review_branch_sync.run_safe",
                                                side_effect=AssertionError(
                                                    "run_safe should not be called when diff ref is unavailable"
                                                ),
                                            ):
                                                mock_checkout.return_value = CheckoutResult(CheckoutResult.SUCCESS)
                                                mock_fetch_branch.return_value = True
                                                mock_reset.return_value = True
                                                mock_fetch.return_value = True
                                                mock_rebase.return_value = RebaseResult(RebaseResult.NO_REBASE_NEEDED)
                                                mock_files.return_value = ["src/a.ts"]
                                                mock_inventory.return_value = (
                                                    [],
                                                    {},
                                                    {},
                                                    None,
                                                    False,
                                                )

                                                success, _error, files, _conflicts, _push = checkout_and_sync_branch(
                                                    "feature/test",
                                                    pull_request_id=123,
                                                    save_files_on_branch=True,
                                                )

                                                assert success is True
                                                assert files == {"src/a.ts"}

                                                files_json = (
                                                    tmp_path
                                                    / "pull-request-review"
                                                    / "abc123def456"
                                                    / "files-on-branch.json"
                                                )
                                                with open(files_json) as f:
                                                    data = json.load(f)
                                                assert data["diff_base_ref"] is None

    def test_save_files_on_branch_falls_back_to_name_only_when_inventory_parse_fails(self, tmp_path):
        """Use name-only changed-file fallback when name-status inventory fails to load."""
        import json
        from unittest.mock import MagicMock, patch

        from agentic_devtools.cli.azure_devops.review_branch_sync import checkout_and_sync_branch
        from agentic_devtools.cli.git.operations import CheckoutResult, RebaseResult

        with patch("agentic_devtools.cli.git.operations.checkout_branch") as mock_checkout:
            with patch("agentic_devtools.cli.git.operations.fetch_branch") as mock_fetch_branch:
                with patch("agentic_devtools.cli.git.operations.reset_branch_to_origin") as mock_reset:
                    with patch("agentic_devtools.cli.git.operations.fetch_main") as mock_fetch:
                        with patch("agentic_devtools.cli.git.operations.rebase_onto_main") as mock_rebase:
                            with patch("agentic_devtools.cli.git.operations.get_files_changed_on_branch") as mock_files:
                                with patch(
                                    "agentic_devtools.cli.git.operations.get_branch_change_inventory"
                                ) as mock_inventory:
                                    with patch(
                                        "agentic_devtools.cli.azure_devops.review_branch_sync.get_value",
                                        return_value="abc123def456",
                                    ):
                                        with patch(
                                            "agentic_devtools.cli.azure_devops.review_branch_sync.get_state_dir",
                                            return_value=tmp_path,
                                        ):
                                            with patch(
                                                "agentic_devtools.cli.azure_devops.review_branch_sync.run_safe"
                                            ) as mock_run_safe:
                                                mock_checkout.return_value = CheckoutResult(CheckoutResult.SUCCESS)
                                                mock_fetch_branch.return_value = True
                                                mock_reset.return_value = True
                                                mock_fetch.return_value = True
                                                mock_rebase.return_value = RebaseResult(RebaseResult.NO_REBASE_NEEDED)
                                                mock_inventory.return_value = ([], {}, {}, "main...HEAD", False)
                                                mock_files.return_value = ["src/fallback.ts"]
                                                mock_run_safe.return_value = MagicMock(
                                                    returncode=0,
                                                    stdout="abc1234\n",
                                                    stderr="",
                                                )

                                                success, _error, files, _conflicts, _push = checkout_and_sync_branch(
                                                    "feature/test",
                                                    pull_request_id=123,
                                                    save_files_on_branch=True,
                                                )

                                                assert success is True
                                                assert files == {"src/fallback.ts"}
                                                assert mock_files.call_count == 1

                                                files_json = (
                                                    tmp_path
                                                    / "pull-request-review"
                                                    / "abc123def456"
                                                    / "files-on-branch.json"
                                                )
                                                with open(files_json) as f:
                                                    data = json.load(f)
                                                assert data["files"] == ["src/fallback.ts"]
                                                assert data["change_types"] == {}
                                                assert data["rename_sources"] == {}
                                                assert data["diff_base_ref"] == "abc1234"
