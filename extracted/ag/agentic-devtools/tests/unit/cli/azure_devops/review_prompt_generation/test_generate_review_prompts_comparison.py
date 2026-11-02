"""Tests for the review_prompt_generation module and helper functions."""


class TestGenerateReviewPrompts:
    def test_recovered_files_tolerate_null_comparison(self, tmp_path):
        """comparison=None in pr_details must not raise AttributeError.

        When the PR API returns a null comparison object and no diff_base_ref is
        available, the code must fall back to origin/main rather than crashing.
        """
        from types import SimpleNamespace
        from unittest.mock import patch

        from agentic_devtools.cli.azure_devops.review_prompt_generation import generate_review_prompts

        pr_details = {
            "comparison": None,
            "files": [{"path": "/src/file1.ts", "changeType": "edit"}],
            "threads": [],
        }
        files_on_branch = {"/src/file1.ts", "/src/file2.ts"}
        diff_info = SimpleNamespace(
            added=SimpleNamespace(is_binary=False, lines=[]),
            removed=SimpleNamespace(is_binary=False, lines=[]),
        )

        with (
            patch.object(
                __import__("agentic_devtools.cli.azure_devops.review_prompt_generation", fromlist=["get_state_dir"]),
                "get_state_dir",
                return_value=tmp_path,
            ),
            patch(
                "agentic_devtools.cli.azure_devops.review_prompt_generation.get_diff_lines_info",
                return_value=diff_info,
            ) as mock_diff_lines,
            patch("agentic_devtools.cli.azure_devops.review_prompt_generation.get_diff_patch", return_value=None),
        ):
            generate_review_prompts(
                pull_request_id=123,
                pr_details=pr_details,
                files_on_branch=files_on_branch,
            )

        # Must fall back to origin/main when comparison is None.
        mock_diff_lines.assert_called_with("origin/main", "HEAD", "src/file2.ts")

    def test_recovered_files_tolerate_malformed_comparison_object(self, tmp_path):
        """Truthy non-dict ``comparison`` values must not raise ``AttributeError``."""
        from types import SimpleNamespace
        from unittest.mock import patch

        from agentic_devtools.cli.azure_devops.review_prompt_generation import generate_review_prompts

        pr_details = {
            "comparison": [1],  # malformed payload from external JSON
            "files": [{"path": "/src/file1.ts", "changeType": "edit"}],
            "threads": [],
        }
        files_on_branch = {"/src/file1.ts", "/src/file2.ts"}
        diff_info = SimpleNamespace(
            added=SimpleNamespace(is_binary=False, lines=[]),
            removed=SimpleNamespace(is_binary=False, lines=[]),
        )

        with (
            patch.object(
                __import__("agentic_devtools.cli.azure_devops.review_prompt_generation", fromlist=["get_state_dir"]),
                "get_state_dir",
                return_value=tmp_path,
            ),
            patch(
                "agentic_devtools.cli.azure_devops.review_prompt_generation.get_diff_lines_info",
                return_value=diff_info,
            ) as mock_diff_lines,
            patch("agentic_devtools.cli.azure_devops.review_prompt_generation.get_diff_patch", return_value=None),
        ):
            generate_review_prompts(
                pull_request_id=123,
                pr_details=pr_details,
                files_on_branch=files_on_branch,
            )

        mock_diff_lines.assert_called_with("origin/main", "HEAD", "src/file2.ts")
