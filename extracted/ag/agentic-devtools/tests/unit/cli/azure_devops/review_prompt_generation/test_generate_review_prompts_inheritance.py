"""Tests for the review_prompt_generation module and helper functions."""


class TestGenerateReviewPrompts:
    def test_inherited_path_uses_unchanged_file_prompt(self, tmp_path):
        """Test that files with PROCESSING_PATH_INHERITED use the simplified prompt.

        Covers line 506 — the _write_unchanged_file_prompt branch.
        """
        from unittest.mock import MagicMock, patch

        from agentic_devtools.cli.azure_devops.review_prompt_generation import generate_review_prompts
        from agentic_devtools.cli.azure_devops.review_state import (
            FileEntry,
            ReviewStatus,
        )

        pr_details = {
            "files": [
                {"path": "/src/app.ts", "changeType": "edit"},
            ],
            "threads": [],
        }

        # Create a mock prior review state with a completed entry for the file
        prior_entry = FileEntry(
            threadId=100,
            commentId=200,
            folder="src",
            fileName="app.ts",
            status=ReviewStatus.APPROVED.value,
            summary="Looks good.",
        )
        prior_state = MagicMock()
        prior_state.commitHash = "abc1234def5678"
        prior_state.files = {"/src/app.ts": prior_entry}

        with (
            patch.object(
                __import__("agentic_devtools.cli.azure_devops.review_prompt_generation", fromlist=["get_state_dir"]),
                "get_state_dir",
                return_value=tmp_path,
            ),
            patch(
                "agentic_devtools.cli.azure_devops.review_state.load_review_state",
                return_value=prior_state,
            ),
        ):
            prompts_count, _, _, prompts_dir, _ = generate_review_prompts(
                pull_request_id=123,
                pr_details=pr_details,
                files_on_branch=None,
                unchanged_files={"/src/app.ts"},
            )

        assert prompts_count == 1
        # Verify the prompt uses the simplified unchanged content
        prompt_files = list(prompts_dir.glob("*.md"))
        assert len(prompt_files) == 1
        content = prompt_files[0].read_text()
        assert "no changes since last review" in content

    def test_recovered_files_use_change_type_from_files_on_branch_json(self, tmp_path):
        """Test that recovered files get their changeType from files-on-branch.json, not "edit".

        Regression test for: recovered entries must carry the git-derived change type
        (add/delete/rename) so that deleted files are not labelled "edit" and the v2
        manifest can classify them correctly.
        """
        import json
        from unittest.mock import patch

        from agentic_devtools.cli.azure_devops.review_prompt_generation import generate_review_prompts

        pr_details = {
            "files": [
                {"path": "/src/file1.ts", "changeType": "edit"},
            ],
            "threads": [],
        }

        # files-on-branch.json reports two files: file1.ts (edit) and deleted.ts
        # (delete).  deleted.ts is absent from the PR API listing and must be
        # recovered with changeType "delete", not the default "edit".
        prompts_dir = tmp_path / "pull-request-review" / "PR123"
        prompts_dir.mkdir(parents=True, exist_ok=True)
        files_json = prompts_dir / "files-on-branch.json"
        with open(files_json, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "files": ["/src/file1.ts", "/src/deleted.ts"],
                    "change_types": {
                        "/src/file1.ts": "edit",
                        "/src/deleted.ts": "delete",
                    },
                },
                f,
            )

        with (
            patch.object(
                __import__("agentic_devtools.cli.azure_devops.review_prompt_generation", fromlist=["get_state_dir"]),
                "get_state_dir",
                return_value=tmp_path,
            ),
            patch(
                "agentic_devtools.cli.azure_devops.review_prompt_generation.get_value",
                return_value=None,
            ),
        ):
            prompts_count, _, skipped_not_on_branch, prompts_dir_out, _ = generate_review_prompts(
                pull_request_id=123,
                pr_details=pr_details,
                files_on_branch=None,  # Force loading from JSON
            )

        # Both files must be queued.
        assert prompts_count == 2
        assert skipped_not_on_branch == 0

        # The recovered deleted.ts entry in pr_details must have changeType "delete".
        recovered = {fd["path"]: fd["changeType"] for fd in pr_details["files"]}
        assert recovered["/src/deleted.ts"] == "delete"
        assert recovered["/src/file1.ts"] == "edit"

    def test_recovered_files_use_change_type_from_json_when_files_on_branch_provided(self, tmp_path):
        """Test that saved change types are still used when files_on_branch is passed explicitly."""
        import json
        from unittest.mock import patch

        from agentic_devtools.cli.azure_devops.review_prompt_generation import generate_review_prompts

        pr_details = {
            "files": [
                {"path": "/src/file1.ts", "changeType": "edit"},
            ],
            "threads": [],
        }
        files_on_branch = {"/src/file1.ts", "/src/deleted.ts"}

        prompts_dir = tmp_path / "pull-request-review" / "PR123"
        prompts_dir.mkdir(parents=True, exist_ok=True)
        files_json = prompts_dir / "files-on-branch.json"
        with open(files_json, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "files": ["/src/file1.ts", "/src/deleted.ts"],
                    "change_types": {"/src/file1.ts": "edit", "/src/deleted.ts": "delete"},
                },
                f,
            )

        with (
            patch.object(
                __import__("agentic_devtools.cli.azure_devops.review_prompt_generation", fromlist=["get_state_dir"]),
                "get_state_dir",
                return_value=tmp_path,
            ),
            patch("agentic_devtools.cli.azure_devops.review_prompt_generation.get_value", return_value=None),
            patch("agentic_devtools.cli.azure_devops.review_prompt_generation.set_value"),
            patch("agentic_devtools.cli.azure_devops.review_prompt_generation.get_diff_lines_info"),
            patch("agentic_devtools.cli.azure_devops.review_prompt_generation.get_diff_patch"),
        ):
            generate_review_prompts(
                pull_request_id=123,
                pr_details=pr_details,
                files_on_branch=files_on_branch,
            )

        recovered = {fd["path"]: fd["changeType"] for fd in pr_details["files"]}
        assert recovered["/src/deleted.ts"] == "delete"

    def test_non_string_pr_file_paths_are_ignored_during_recovery(self, tmp_path, capsys):
        """Non-string PR file paths must not abort recovery reconciliation."""
        from unittest.mock import patch

        from agentic_devtools.cli.azure_devops.review_prompt_generation import generate_review_prompts

        pr_details = {
            "files": [
                {"path": "", "changeType": "edit"},
                {"path": 123, "changeType": "edit"},
            ],
            "threads": [],
        }
        files_on_branch = {"/src/file1.ts"}

        with (
            patch.object(
                __import__("agentic_devtools.cli.azure_devops.review_prompt_generation", fromlist=["get_state_dir"]),
                "get_state_dir",
                return_value=tmp_path,
            ),
            patch("agentic_devtools.cli.azure_devops.review_prompt_generation.get_diff_lines_info"),
            patch("agentic_devtools.cli.azure_devops.review_prompt_generation.get_diff_patch"),
        ):
            prompts_count, _, skipped_not_on_branch, _, _ = generate_review_prompts(
                pull_request_id=123,
                pr_details=pr_details,
                files_on_branch=files_on_branch,
            )

        assert prompts_count == 1
        assert skipped_not_on_branch == 2
        assert [file_detail["path"] for file_detail in pr_details["files"]] == ["/src/file1.ts"]
        assert "non-string path: 123" in capsys.readouterr().err
