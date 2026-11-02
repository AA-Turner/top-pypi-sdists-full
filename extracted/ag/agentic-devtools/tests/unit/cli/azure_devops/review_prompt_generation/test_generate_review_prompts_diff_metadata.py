"""Tests for the review_prompt_generation module and helper functions."""


class TestGenerateReviewPrompts:
    def test_recovered_files_prefer_saved_diff_base_ref(self, tmp_path):
        """Test recovered-file metadata reuses the persisted diff base ref when available."""
        import json
        from types import SimpleNamespace
        from unittest.mock import patch

        from agentic_devtools.cli.azure_devops.review_prompt_generation import generate_review_prompts

        pr_details = {
            "comparison": {"baseBranch": "release", "baseRef": "origin/release"},
            "files": [{"path": "/src/file1.ts", "changeType": "edit"}],
            "threads": [],
        }
        prompts_dir = tmp_path / "pull-request-review" / "PR123"
        prompts_dir.mkdir(parents=True, exist_ok=True)
        (prompts_dir / "files-on-branch.json").write_text(
            json.dumps(
                {
                    "files": ["/src/file1.ts", "/src/file3.ts"],
                    "change_types": {"/src/file1.ts": "edit", "/src/file3.ts": "edit"},
                    "diff_base_ref": "main",
                }
            ),
            encoding="utf-8",
        )
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
            patch("agentic_devtools.cli.azure_devops.review_prompt_generation.get_value", return_value=None),
            patch("agentic_devtools.cli.azure_devops.review_prompt_generation.set_value"),
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

        mock_diff_lines.assert_called_with("main", "HEAD", "src/file3.ts")

    def test_recovered_files_include_git_diff_metadata_when_available(self, tmp_path):
        """Test recovered entries carry git-derived diff metadata when available."""
        from types import SimpleNamespace
        from unittest.mock import patch

        from agentic_devtools.cli.azure_devops.review_prompt_generation import generate_review_prompts

        pr_details = {
            "comparison": {"baseRef": "base-commit", "compareRef": "compare-commit", "baseBranch": "trunk"},
            "files": [
                {"path": "/src/file1.ts", "changeType": "edit"},
            ],
            "threads": [],
        }
        files_on_branch = {"/src/file1.ts", "/src/file3.ts"}
        diff_info = SimpleNamespace(
            added=SimpleNamespace(is_binary=False, lines=[SimpleNamespace(line_number=11, content="added line")]),
            removed=SimpleNamespace(is_binary=False, lines=[SimpleNamespace(line_number=4, content="removed line")]),
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
            patch(
                "agentic_devtools.cli.azure_devops.review_prompt_generation.get_diff_patch",
                return_value="@@ -4 +11 @@",
            ) as mock_patch,
        ):
            generate_review_prompts(
                pull_request_id=123,
                pr_details=pr_details,
                files_on_branch=files_on_branch,
            )

        recovered = {fd["path"]: fd for fd in pr_details["files"]}
        recovered_entry = recovered["/src/file3.ts"]
        assert recovered_entry["isBinary"] is False
        assert recovered_entry["addedLineCount"] == 1
        assert recovered_entry["addedLines"] == [{"line": 11, "content": "added line"}]
        assert recovered_entry["removedLineCount"] == 1
        assert recovered_entry["removedLines"] == [{"line": 4, "content": "removed line"}]
        assert recovered_entry["patch"] == "@@ -4 +11 @@"
        # Recovered-file metadata is always derived from the current post-sync
        # branch range (origin/<baseBranch>...HEAD). compareRef and baseRef from
        # pr_details are snapshots taken before sync/rebase and may be stale.
        mock_diff_lines.assert_called_with("origin/trunk", "HEAD", "src/file3.ts")
        mock_patch.assert_called_with("origin/trunk", "HEAD", "src/file3.ts")

    def test_recovered_files_use_origin_base_ref_hint_when_base_branch_missing(self, tmp_path):
        """Test metadata lookup derives base branch from origin/<branch> baseRef hints."""
        from types import SimpleNamespace
        from unittest.mock import patch

        from agentic_devtools.cli.azure_devops.review_prompt_generation import generate_review_prompts

        pr_details = {
            "comparison": {"baseRef": "origin/release"},
            "files": [{"path": "/src/file1.ts", "changeType": "edit"}],
            "threads": [],
        }
        files_on_branch = {"/src/file1.ts", "/src/file3.ts"}
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
            patch(
                "agentic_devtools.cli.azure_devops.review_prompt_generation.get_diff_patch",
                return_value=None,
            ),
        ):
            generate_review_prompts(
                pull_request_id=123,
                pr_details=pr_details,
                files_on_branch=files_on_branch,
            )

        mock_diff_lines.assert_called_with("origin/release", "HEAD", "src/file3.ts")

    def test_recovered_files_use_refs_heads_base_ref_hint_when_base_branch_missing(self, tmp_path):
        """Test metadata lookup derives base branch from refs/heads/<branch> baseRef hints."""
        from types import SimpleNamespace
        from unittest.mock import patch

        from agentic_devtools.cli.azure_devops.review_prompt_generation import generate_review_prompts

        pr_details = {
            "comparison": {"baseRef": "refs/heads/release"},
            "files": [{"path": "/src/file1.ts", "changeType": "edit"}],
            "threads": [],
        }
        files_on_branch = {"/src/file1.ts", "/src/file3.ts"}
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
            patch(
                "agentic_devtools.cli.azure_devops.review_prompt_generation.get_diff_patch",
                return_value=None,
            ),
        ):
            generate_review_prompts(
                pull_request_id=123,
                pr_details=pr_details,
                files_on_branch=files_on_branch,
            )

        mock_diff_lines.assert_called_with("origin/release", "HEAD", "src/file3.ts")

    def test_recovered_files_fall_back_to_main_when_base_ref_is_commit_sha(self, tmp_path, capsys):
        """Test unrecognized baseRef values fall back to origin/main with a warning."""
        from types import SimpleNamespace
        from unittest.mock import patch

        from agentic_devtools.cli.azure_devops.review_prompt_generation import generate_review_prompts

        pr_details = {
            "comparison": {"baseRef": "abc123def456"},
            "files": [{"path": "/src/file1.ts", "changeType": "edit"}],
            "threads": [],
        }
        files_on_branch = {"/src/file1.ts", "/src/file3.ts"}
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
            patch(
                "agentic_devtools.cli.azure_devops.review_prompt_generation.get_diff_patch",
                return_value=None,
            ),
        ):
            generate_review_prompts(
                pull_request_id=123,
                pr_details=pr_details,
                files_on_branch=files_on_branch,
            )

        mock_diff_lines.assert_called_with("origin/main", "HEAD", "src/file3.ts")
        assert "Could not derive base branch from PR details" in capsys.readouterr().err

    def test_recovered_files_fall_back_to_default_metadata_when_diff_lookup_fails(self, tmp_path):
        """Test recovered entries keep safe defaults when git diff metadata lookup fails."""
        from unittest.mock import patch

        from agentic_devtools.cli.azure_devops.review_prompt_generation import generate_review_prompts

        pr_details = {
            "files": [{"path": "/src/file1.ts", "changeType": "edit"}],
            "threads": [],
        }
        files_on_branch = {"/src/file1.ts", "/src/file3.ts"}

        with (
            patch.object(
                __import__("agentic_devtools.cli.azure_devops.review_prompt_generation", fromlist=["get_state_dir"]),
                "get_state_dir",
                return_value=tmp_path,
            ),
            patch(
                "agentic_devtools.cli.azure_devops.review_prompt_generation.get_diff_lines_info",
                side_effect=RuntimeError("boom"),
            ),
        ):
            generate_review_prompts(
                pull_request_id=123,
                pr_details=pr_details,
                files_on_branch=files_on_branch,
            )

        recovered = {fd["path"]: fd for fd in pr_details["files"]}
        recovered_entry = recovered["/src/file3.ts"]
        assert recovered_entry["isBinary"] is False
        assert recovered_entry["addedLineCount"] == 0
        assert recovered_entry["addedLines"] == []
        assert recovered_entry["removedLineCount"] == 0
        assert recovered_entry["removedLines"] == []
        assert recovered_entry["patch"] is None

    def test_recovered_files_keep_line_metadata_when_patch_lookup_fails(self, tmp_path):
        """Test patch failures do not discard recovered line metadata."""
        from types import SimpleNamespace
        from unittest.mock import patch

        from agentic_devtools.cli.azure_devops.review_prompt_generation import generate_review_prompts

        pr_details = {
            "files": [{"path": "/src/file1.ts", "changeType": "edit"}],
            "threads": [],
        }
        files_on_branch = {"/src/file1.ts", "/src/file3.ts"}
        diff_info = SimpleNamespace(
            added=SimpleNamespace(is_binary=False, lines=[SimpleNamespace(line_number=8, content="line +")]),
            removed=SimpleNamespace(is_binary=False, lines=[SimpleNamespace(line_number=2, content="line -")]),
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
            ),
            patch(
                "agentic_devtools.cli.azure_devops.review_prompt_generation.get_diff_patch",
                side_effect=RuntimeError("patch fail"),
            ),
        ):
            generate_review_prompts(
                pull_request_id=123,
                pr_details=pr_details,
                files_on_branch=files_on_branch,
            )

        recovered = {fd["path"]: fd for fd in pr_details["files"]}
        recovered_entry = recovered["/src/file3.ts"]
        assert recovered_entry["addedLineCount"] == 1
        assert recovered_entry["addedLines"] == [{"line": 8, "content": "line +"}]
        assert recovered_entry["removedLineCount"] == 1
        assert recovered_entry["removedLines"] == [{"line": 2, "content": "line -"}]
        assert recovered_entry["patch"] is None

    def test_invalid_change_types_payload_uses_edit_fallback(self, tmp_path):
        """Test non-dict change_types payload does not crash and falls back to edit."""
        import json
        from unittest.mock import patch

        from agentic_devtools.cli.azure_devops.review_prompt_generation import generate_review_prompts

        pr_details = {
            "files": [{"path": "/src/file1.ts", "changeType": "edit"}],
            "threads": [],
        }
        files_on_branch = {"/src/file1.ts", "/src/file3.ts"}
        prompts_dir = tmp_path / "pull-request-review" / "PR123"
        prompts_dir.mkdir(parents=True, exist_ok=True)
        with open(prompts_dir / "files-on-branch.json", "w", encoding="utf-8") as f:
            json.dump({"files": ["/src/file1.ts", "/src/file3.ts"], "change_types": ["not-a-dict"]}, f)

        with (
            patch.object(
                __import__("agentic_devtools.cli.azure_devops.review_prompt_generation", fromlist=["get_state_dir"]),
                "get_state_dir",
                return_value=tmp_path,
            ),
            patch("agentic_devtools.cli.azure_devops.review_prompt_generation.get_value", return_value=None),
            patch("agentic_devtools.cli.azure_devops.review_prompt_generation.set_value"),
        ):
            generate_review_prompts(
                pull_request_id=123,
                pr_details=pr_details,
                files_on_branch=files_on_branch,
            )

        recovered = {fd["path"]: fd["changeType"] for fd in pr_details["files"]}
        assert recovered["/src/file3.ts"] == "edit"

    def test_non_string_or_unknown_change_types_are_ignored(self, tmp_path):
        """Only recognized string change types should be loaded from JSON metadata."""
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
                    "files": ["/src/file1.ts", "/src/deleted.ts", "/src/added.ts"],
                    "change_types": {
                        "/src/deleted.ts": None,
                        "/src/file1.ts": "unknown-token",
                        "   ": "add",
                        "/src/added.ts": "A",
                    },
                }
            ),
            encoding="utf-8",
        )

        with patch.object(
            __import__("agentic_devtools.cli.azure_devops.review_prompt_generation", fromlist=["get_state_dir"]),
            "get_state_dir",
            return_value=tmp_path,
        ):
            with patch(
                "agentic_devtools.cli.azure_devops.review_prompt_generation.get_value",
                return_value=None,
            ):
                with patch(
                    "agentic_devtools.cli.azure_devops.review_prompt_generation.resolve_review_artifact_dir_name",
                    return_value="PR123",
                ):
                    generate_review_prompts(
                        pull_request_id=123,
                        pr_details=pr_details,
                        files_on_branch=None,
                    )

        recovered = {fd["path"]: fd["changeType"] for fd in pr_details["files"]}
        assert recovered["/src/deleted.ts"] == "edit"
        assert recovered["/src/added.ts"] == "add"

    def test_branch_files_reconciliation_matches_with_different_slash_conventions(self, tmp_path):
        """Test path normalization: Windows backslash paths match Unix slash paths and
        don't create duplicate entries.

        A file present in files_on_branch as '\\path\\to\\file.ts' must match
        '/path/to/file.ts' in pr_details["files"] and must NOT produce a recovered
        entry (it's already represented).
        """
        from unittest.mock import patch

        from agentic_devtools.cli.azure_devops.review_prompt_generation import generate_review_prompts

        pr_details = {
            "files": [
                {"path": "/src/app.ts", "changeType": "edit"},
            ],
            "threads": [],
        }

        # files_on_branch uses Windows-style backslashes for app.ts.
        # This must match the forward-slash form in pr_details and must NOT
        # be treated as a separate missing file.
        files_on_branch = {"\\src\\app.ts"}

        with patch.object(
            __import__("agentic_devtools.cli.azure_devops.review_prompt_generation", fromlist=["get_state_dir"]),
            "get_state_dir",
            return_value=tmp_path,
        ):
            prompts_count, _, skipped_not_on_branch, prompts_dir, _ = generate_review_prompts(
                pull_request_id=123,
                pr_details=pr_details,
                files_on_branch=files_on_branch,
            )

        # Exactly 1 prompt — no duplicate from the slash mismatch.
        assert prompts_count == 1
        assert skipped_not_on_branch == 0

        # pr_details["files"] must still contain exactly 1 entry (no synthetic
        # duplicate was appended).
        assert len(pr_details["files"]) == 1
