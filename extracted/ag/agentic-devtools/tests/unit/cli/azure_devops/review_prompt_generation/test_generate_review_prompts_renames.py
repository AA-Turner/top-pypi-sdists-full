"""Tests for the review_prompt_generation module and helper functions."""


class TestGenerateReviewPrompts:
    def test_recovered_rename_includes_original_path_from_branch_json(self, tmp_path):
        """Regression: recovered renames must include originalPath from files-on-branch.json.

        Without originalPath, source_context.py queries the destination path at the
        base commit (where the file does not yet exist) and produces an empty base-side
        context, so the pre-rename content is unavailable during the review.
        """
        import json
        from unittest.mock import patch

        from agentic_devtools.cli.azure_devops.review_prompt_generation import generate_review_prompts

        pr_details = {
            "files": [{"path": "/src/file1.ts", "changeType": "edit"}],
            "threads": [],
        }

        prompts_dir = tmp_path / "pull-request-review" / "PR123"
        prompts_dir.mkdir(parents=True, exist_ok=True)
        (prompts_dir / "files-on-branch.json").write_text(
            json.dumps(
                {
                    "files": ["/src/file1.ts", "/src/renamed-new.ts"],
                    "change_types": {
                        "/src/file1.ts": "edit",
                        "/src/renamed-new.ts": "rename",
                    },
                    "rename_sources": {"/src/renamed-new.ts": "/src/renamed-old.ts"},
                    "diff_base_ref": "abc123",
                }
            ),
            encoding="utf-8",
        )

        with (
            patch.object(
                __import__("agentic_devtools.cli.azure_devops.review_prompt_generation", fromlist=["get_state_dir"]),
                "get_state_dir",
                return_value=tmp_path,
            ),
            patch("agentic_devtools.cli.azure_devops.review_prompt_generation.get_value", return_value=None),
            patch("agentic_devtools.cli.azure_devops.review_prompt_generation.get_diff_lines_info"),
            patch("agentic_devtools.cli.azure_devops.review_prompt_generation.get_diff_patch"),
        ):
            generate_review_prompts(
                pull_request_id=123,
                pr_details=pr_details,
                files_on_branch=None,
            )

        recovered = {fd["path"]: fd for fd in pr_details["files"]}
        assert "/src/renamed-new.ts" in recovered
        rename_entry = recovered["/src/renamed-new.ts"]
        assert rename_entry["changeType"] == "rename"
        assert rename_entry["originalPath"] == "/src/renamed-old.ts"

    def test_recovered_rename_without_source_in_json_omits_original_path(self, tmp_path):
        """A recovered rename with no matching rename_sources entry must not include originalPath.

        Callers that pass files_on_branch directly without a rename_sources dict
        (e.g. in tests) must not cause a KeyError or inject an empty/None originalPath.
        """
        import json
        from unittest.mock import patch

        from agentic_devtools.cli.azure_devops.review_prompt_generation import generate_review_prompts

        pr_details = {
            "files": [{"path": "/src/file1.ts", "changeType": "edit"}],
            "threads": [],
        }

        prompts_dir = tmp_path / "pull-request-review" / "PR123"
        prompts_dir.mkdir(parents=True, exist_ok=True)
        (prompts_dir / "files-on-branch.json").write_text(
            json.dumps(
                {
                    "files": ["/src/file1.ts", "/src/renamed-new.ts"],
                    "change_types": {
                        "/src/file1.ts": "edit",
                        "/src/renamed-new.ts": "rename",
                    },
                    # rename_sources intentionally absent
                    "diff_base_ref": "abc123",
                }
            ),
            encoding="utf-8",
        )

        with (
            patch.object(
                __import__("agentic_devtools.cli.azure_devops.review_prompt_generation", fromlist=["get_state_dir"]),
                "get_state_dir",
                return_value=tmp_path,
            ),
            patch("agentic_devtools.cli.azure_devops.review_prompt_generation.get_value", return_value=None),
            patch("agentic_devtools.cli.azure_devops.review_prompt_generation.get_diff_lines_info"),
            patch("agentic_devtools.cli.azure_devops.review_prompt_generation.get_diff_patch"),
        ):
            generate_review_prompts(
                pull_request_id=123,
                pr_details=pr_details,
                files_on_branch=None,
            )

        recovered = {fd["path"]: fd for fd in pr_details["files"]}
        assert "/src/renamed-new.ts" in recovered
        rename_entry = recovered["/src/renamed-new.ts"]
        assert rename_entry["changeType"] == "rename"
        assert "originalPath" not in rename_entry

    def test_non_dict_rename_sources_in_json_is_ignored(self, tmp_path):
        """A non-dict rename_sources value in files-on-branch.json must be ignored safely.

        This covers the isinstance(raw_rename_sources, dict) False branch: when the
        JSON carries an unexpected type for rename_sources, branch_rename_sources
        stays empty and no originalPath is injected.
        """
        import json
        from unittest.mock import patch

        from agentic_devtools.cli.azure_devops.review_prompt_generation import generate_review_prompts

        pr_details = {
            "files": [{"path": "/src/file1.ts", "changeType": "edit"}],
            "threads": [],
        }

        prompts_dir = tmp_path / "pull-request-review" / "PR123"
        prompts_dir.mkdir(parents=True, exist_ok=True)
        (prompts_dir / "files-on-branch.json").write_text(
            json.dumps(
                {
                    "files": ["/src/file1.ts", "/src/renamed-new.ts"],
                    "change_types": {
                        "/src/file1.ts": "edit",
                        "/src/renamed-new.ts": "rename",
                    },
                    "rename_sources": "invalid-not-a-dict",
                    "diff_base_ref": "abc123",
                }
            ),
            encoding="utf-8",
        )

        with (
            patch.object(
                __import__("agentic_devtools.cli.azure_devops.review_prompt_generation", fromlist=["get_state_dir"]),
                "get_state_dir",
                return_value=tmp_path,
            ),
            patch("agentic_devtools.cli.azure_devops.review_prompt_generation.get_value", return_value=None),
            patch("agentic_devtools.cli.azure_devops.review_prompt_generation.get_diff_lines_info"),
            patch("agentic_devtools.cli.azure_devops.review_prompt_generation.get_diff_patch"),
        ):
            generate_review_prompts(
                pull_request_id=123,
                pr_details=pr_details,
                files_on_branch=None,
            )

        recovered = {fd["path"]: fd for fd in pr_details["files"]}
        assert "/src/renamed-new.ts" in recovered
        rename_entry = recovered["/src/renamed-new.ts"]
        assert rename_entry["changeType"] == "rename"
        # Non-dict rename_sources must be ignored; no originalPath injected.
        assert "originalPath" not in rename_entry

    def test_non_string_rename_sources_in_json_are_ignored(self, tmp_path):
        """Non-string rename_sources entries must be ignored without coercion."""
        import json
        from unittest.mock import patch

        from agentic_devtools.cli.azure_devops.review_prompt_generation import generate_review_prompts

        pr_details = {
            "files": [{"path": "/src/file1.ts", "changeType": "edit"}],
            "threads": [],
        }

        prompts_dir = tmp_path / "pull-request-review" / "PR123"
        prompts_dir.mkdir(parents=True, exist_ok=True)
        (prompts_dir / "files-on-branch.json").write_text(
            json.dumps(
                {
                    "files": ["/src/file1.ts", "/src/renamed-new.ts"],
                    "change_types": {
                        "/src/file1.ts": "edit",
                        "/src/renamed-new.ts": "rename",
                    },
                    "rename_sources": {"/src/renamed-new.ts": None},
                    "diff_base_ref": "abc123",
                }
            ),
            encoding="utf-8",
        )

        with (
            patch.object(
                __import__("agentic_devtools.cli.azure_devops.review_prompt_generation", fromlist=["get_state_dir"]),
                "get_state_dir",
                return_value=tmp_path,
            ),
            patch("agentic_devtools.cli.azure_devops.review_prompt_generation.get_value", return_value=None),
            patch("agentic_devtools.cli.azure_devops.review_prompt_generation.get_diff_lines_info"),
            patch("agentic_devtools.cli.azure_devops.review_prompt_generation.get_diff_patch"),
        ):
            generate_review_prompts(
                pull_request_id=123,
                pr_details=pr_details,
                files_on_branch=None,
            )

        recovered = {fd["path"]: fd for fd in pr_details["files"]}
        rename_entry = recovered["/src/renamed-new.ts"]
        assert rename_entry["changeType"] == "rename"
        assert "originalPath" not in rename_entry

    def test_recovered_rename_diff_lookup_includes_original_and_destination_paths(self, tmp_path):
        """Recovered rename diff lookups must include old and new path for rename detection."""
        import json
        from types import SimpleNamespace
        from unittest.mock import patch

        from agentic_devtools.cli.azure_devops.review_prompt_generation import generate_review_prompts

        pr_details = {
            "files": [{"path": "/src/file1.ts", "changeType": "edit"}],
            "threads": [],
        }
        diff_info = SimpleNamespace(
            added=SimpleNamespace(is_binary=False, lines=[]),
            removed=SimpleNamespace(is_binary=False, lines=[]),
        )

        prompts_dir = tmp_path / "pull-request-review" / "PR123"
        prompts_dir.mkdir(parents=True, exist_ok=True)
        (prompts_dir / "files-on-branch.json").write_text(
            json.dumps(
                {
                    "files": ["/src/file1.ts", "/src/renamed-new.ts"],
                    "change_types": {
                        "/src/file1.ts": "edit",
                        "/src/renamed-new.ts": "rename",
                    },
                    "rename_sources": {"/src/renamed-new.ts": "/src/renamed-old.ts"},
                    "diff_base_ref": "abc123",
                }
            ),
            encoding="utf-8",
        )

        with (
            patch.object(
                __import__("agentic_devtools.cli.azure_devops.review_prompt_generation", fromlist=["get_state_dir"]),
                "get_state_dir",
                return_value=tmp_path,
            ),
            patch("agentic_devtools.cli.azure_devops.review_prompt_generation.get_value", return_value=None),
            patch(
                "agentic_devtools.cli.azure_devops.review_prompt_generation.get_diff_lines_info",
                return_value=diff_info,
            ) as mock_diff_lines,
            patch(
                "agentic_devtools.cli.azure_devops.review_prompt_generation.get_diff_patch", return_value=None
            ) as mock_patch,
        ):
            generate_review_prompts(
                pull_request_id=123,
                pr_details=pr_details,
                files_on_branch=None,
            )

        expected_paths = ["src/renamed-old.ts", "src/renamed-new.ts"]
        mock_diff_lines.assert_called_with("abc123", "HEAD", expected_paths)
        mock_patch.assert_called_with("abc123", "HEAD", expected_paths)

    def test_recovered_rename_same_source_and_destination_uses_single_lookup_path(self, tmp_path):
        """Rename metadata with identical source/destination keeps single-path lookup."""
        import json
        from types import SimpleNamespace
        from unittest.mock import patch

        from agentic_devtools.cli.azure_devops.review_prompt_generation import generate_review_prompts

        pr_details = {
            "files": [{"path": "/src/file1.ts", "changeType": "edit"}],
            "threads": [],
        }
        diff_info = SimpleNamespace(
            added=SimpleNamespace(is_binary=False, lines=[]),
            removed=SimpleNamespace(is_binary=False, lines=[]),
        )

        prompts_dir = tmp_path / "pull-request-review" / "PR123"
        prompts_dir.mkdir(parents=True, exist_ok=True)
        (prompts_dir / "files-on-branch.json").write_text(
            json.dumps(
                {
                    "files": ["/src/file1.ts", "/src/renamed-new.ts"],
                    "change_types": {
                        "/src/file1.ts": "edit",
                        "/src/renamed-new.ts": "rename",
                    },
                    "rename_sources": {"/src/renamed-new.ts": "/src/renamed-new.ts"},
                    "diff_base_ref": "abc123",
                }
            ),
            encoding="utf-8",
        )

        with (
            patch.object(
                __import__("agentic_devtools.cli.azure_devops.review_prompt_generation", fromlist=["get_state_dir"]),
                "get_state_dir",
                return_value=tmp_path,
            ),
            patch("agentic_devtools.cli.azure_devops.review_prompt_generation.get_value", return_value=None),
            patch(
                "agentic_devtools.cli.azure_devops.review_prompt_generation.get_diff_lines_info",
                return_value=diff_info,
            ) as mock_diff_lines,
            patch("agentic_devtools.cli.azure_devops.review_prompt_generation.get_diff_patch", return_value=None),
        ):
            generate_review_prompts(
                pull_request_id=123,
                pr_details=pr_details,
                files_on_branch=None,
            )

        mock_diff_lines.assert_called_with("abc123", "HEAD", "src/renamed-new.ts")

    def test_recovered_rename_with_root_source_path_skips_original_path(self, tmp_path):
        """Root-like source paths that normalize empty should be skipped safely."""
        import json
        from unittest.mock import patch

        from agentic_devtools.cli.azure_devops.review_prompt_generation import generate_review_prompts

        pr_details = {
            "files": [{"path": "/src/file1.ts", "changeType": "edit"}],
            "threads": [],
        }

        prompts_dir = tmp_path / "pull-request-review" / "PR123"
        prompts_dir.mkdir(parents=True, exist_ok=True)
        (prompts_dir / "files-on-branch.json").write_text(
            json.dumps(
                {
                    "files": ["/src/file1.ts", "/src/renamed-new.ts"],
                    "change_types": {
                        "/src/file1.ts": "edit",
                        "/src/renamed-new.ts": "rename",
                    },
                    "rename_sources": {"/src/renamed-new.ts": "/"},
                    "diff_base_ref": "abc123",
                }
            ),
            encoding="utf-8",
        )

        with (
            patch.object(
                __import__("agentic_devtools.cli.azure_devops.review_prompt_generation", fromlist=["get_state_dir"]),
                "get_state_dir",
                return_value=tmp_path,
            ),
            patch("agentic_devtools.cli.azure_devops.review_prompt_generation.get_value", return_value=None),
            patch("agentic_devtools.cli.azure_devops.review_prompt_generation.get_diff_lines_info"),
            patch("agentic_devtools.cli.azure_devops.review_prompt_generation.get_diff_patch"),
        ):
            generate_review_prompts(
                pull_request_id=123,
                pr_details=pr_details,
                files_on_branch=None,
            )

        recovered = {fd["path"]: fd for fd in pr_details["files"]}
        rename_entry = recovered["/src/renamed-new.ts"]
        assert "originalPath" not in rename_entry

    def test_blank_rename_source_entries_are_ignored(self, tmp_path):
        """Blank path pairs in rename_sources must be ignored."""
        import json
        from unittest.mock import patch

        from agentic_devtools.cli.azure_devops.review_prompt_generation import generate_review_prompts

        pr_details = {
            "files": [{"path": "/src/file1.ts", "changeType": "edit"}],
            "threads": [],
        }

        prompts_dir = tmp_path / "pull-request-review" / "PR123"
        prompts_dir.mkdir(parents=True, exist_ok=True)
        (prompts_dir / "files-on-branch.json").write_text(
            json.dumps(
                {
                    "files": ["/src/file1.ts", "/src/renamed-new.ts"],
                    "change_types": {
                        "/src/file1.ts": "edit",
                        "/src/renamed-new.ts": "rename",
                    },
                    "rename_sources": {
                        "/src/renamed-new.ts": "   ",
                        "   ": "/src/renamed-old.ts",
                    },
                    "diff_base_ref": "abc123",
                }
            ),
            encoding="utf-8",
        )

        with (
            patch.object(
                __import__("agentic_devtools.cli.azure_devops.review_prompt_generation", fromlist=["get_state_dir"]),
                "get_state_dir",
                return_value=tmp_path,
            ),
            patch("agentic_devtools.cli.azure_devops.review_prompt_generation.get_value", return_value=None),
            patch("agentic_devtools.cli.azure_devops.review_prompt_generation.get_diff_lines_info"),
            patch("agentic_devtools.cli.azure_devops.review_prompt_generation.get_diff_patch"),
        ):
            generate_review_prompts(
                pull_request_id=123,
                pr_details=pr_details,
                files_on_branch=None,
            )

        recovered = {fd["path"]: fd for fd in pr_details["files"]}
        rename_entry = recovered["/src/renamed-new.ts"]
        assert "originalPath" not in rename_entry
