"""Tests for the review_commands module and helper functions."""


class TestGenerateReviewPrompts:
    """Tests for generate_review_prompts function."""

    def test_generates_prompts_for_files(self, tmp_path):
        """Test generates prompt files for PR files."""
        from unittest.mock import patch

        from agentic_devtools.cli.azure_devops.review_commands import generate_review_prompts

        pr_details = {
            "files": [
                {"path": "/src/file1.ts", "changeType": "edit"},
                {"path": "/src/file2.ts", "changeType": "add"},
            ],
            "threads": [],
        }

        # Patch the scripts directory location
        with patch("agentic_devtools.cli.azure_devops.review_commands.Path") as mock_path:
            # Make the path operations work with tmp_path
            mock_path.return_value.parent.parent.parent.parent.parent = tmp_path
            mock_path.return_value.__truediv__ = lambda self, x: tmp_path / x

            # Actually call the function but with simplified setup
            from agentic_devtools.cli.azure_devops.review_commands import generate_review_prompts

            # Minimal patching to avoid complex path issues
            with patch.object(
                __import__("agentic_devtools.cli.azure_devops.review_commands", fromlist=["get_state_dir"]),
                "get_state_dir",
                return_value=tmp_path,
            ):
                prompts_count, skipped_reviewed, skipped_not_on_branch, prompts_dir, skipped_files = (
                    generate_review_prompts(
                        pull_request_id=123,
                        pr_details=pr_details,
                        files_on_branch=None,
                    )
                )

        assert prompts_count == 2
        assert skipped_reviewed == 0
        assert skipped_not_on_branch == 0
        assert skipped_files == []

    def test_no_longer_skips_reviewed_files(self, tmp_path):
        """Test that previously-reviewed files are no longer skipped.

        All in-scope files are now reviewed every run regardless of prior review status.
        """
        from unittest.mock import patch

        from agentic_devtools.cli.azure_devops.review_commands import generate_review_prompts

        pr_details = {
            "files": [
                {"path": "/src/file1.ts", "changeType": "edit"},
            ],
            "threads": [],
            "reviewer": {
                "reviewedFiles": ["/src/file1.ts"],
            },
        }

        with patch.object(
            __import__("agentic_devtools.cli.azure_devops.review_commands", fromlist=["get_state_dir"]),
            "get_state_dir",
            return_value=tmp_path,
        ):
            prompts_count, skipped_reviewed, skipped_not_on_branch, _, skipped_files = generate_review_prompts(
                pull_request_id=123,
                pr_details=pr_details,
                files_on_branch=None,
            )

        # File is NOT skipped — all files are reviewed every run
        assert prompts_count == 1
        assert skipped_reviewed == 0
        assert skipped_files == []

    def test_skips_files_not_on_branch(self, tmp_path):
        """Test skips files not in the branch changes."""
        from unittest.mock import patch

        from agentic_devtools.cli.azure_devops.review_commands import generate_review_prompts

        pr_details = {
            "files": [
                {"path": "/src/file1.ts", "changeType": "edit"},
                {"path": "/src/file2.ts", "changeType": "edit"},
            ],
            "threads": [],
        }

        # Only file1.ts is actually on the branch
        files_on_branch = {"/src/file1.ts"}

        with patch.object(
            __import__("agentic_devtools.cli.azure_devops.review_commands", fromlist=["get_state_dir"]),
            "get_state_dir",
            return_value=tmp_path,
        ):
            prompts_count, skipped_reviewed, skipped_not_on_branch, _, skipped_files = generate_review_prompts(
                pull_request_id=123,
                pr_details=pr_details,
                files_on_branch=files_on_branch,
            )

        assert prompts_count == 1
        assert skipped_not_on_branch == 1
        assert len(skipped_files) == 1
        assert skipped_files[0].path == "/src/file2.ts"
        assert skipped_files[0].reason == "not_on_branch"
        assert pr_details["files"] == [{"path": "/src/file1.ts", "changeType": "edit"}]

    def test_recovers_files_missing_from_pr_details_but_present_on_branch(self, tmp_path):
        """Test files present in files_on_branch but absent from pr_details["files"]
        are recovered into the queue instead of being silently dropped.

        The PR API reports 2 files; git reports 4 (2 overlapping, 2 new). All 4
        must appear in queue.json, have prompt files on disk, and be reflected in
        pr_details["files"].

        Regression test for: "PR file review queue silently drops files that
        are present in files-on-branch.json".
        """
        import json
        from unittest.mock import patch

        from agentic_devtools.cli.azure_devops.review_commands import generate_review_prompts

        pr_details = {
            "files": [
                {"path": "/src/file1.ts", "changeType": "edit"},
                {"path": "/src/file2.ts", "changeType": "add"},
            ],
            "threads": [],
        }

        # git reports 4 files: the 2 above plus 2 absent from the PR API listing.
        files_on_branch = {"/src/file1.ts", "/src/file2.ts", "/src/file3.ts", "/src/file4.ts"}

        with patch.object(
            __import__("agentic_devtools.cli.azure_devops.review_commands", fromlist=["get_state_dir"]),
            "get_state_dir",
            return_value=tmp_path,
        ):
            prompts_count, skipped_reviewed, skipped_not_on_branch, prompts_dir, skipped_files = (
                generate_review_prompts(
                    pull_request_id=123,
                    pr_details=pr_details,
                    files_on_branch=files_on_branch,
                )
            )

        # All 4 files must be generated — none silently dropped.
        assert prompts_count == 4
        assert skipped_not_on_branch == 0
        assert skipped_files == []

        # All 4 files must have a corresponding entry in queue.json.
        queue_path = prompts_dir / "queue.json"
        with open(queue_path, encoding="utf-8") as f:
            queue = json.load(f)
        queued_paths = {entry["path"] for entry in queue["pending"]}
        assert queued_paths == {"/src/file1.ts", "/src/file2.ts", "/src/file3.ts", "/src/file4.ts"}

        # All 4 files must also get a prompt file on disk.
        prompt_files = list(prompts_dir.glob("*.md"))
        assert len(prompt_files) == 4

        # pr_details is mutated so downstream consumers (e.g. the v2 manifest
        # builder) also see the recovered files.
        assert len(pr_details["files"]) == 4
        recovered_paths = {fd["path"] for fd in pr_details["files"]}
        assert recovered_paths == {"/src/file1.ts", "/src/file2.ts", "/src/file3.ts", "/src/file4.ts"}

        # Synthetic entries must include all required fields so that downstream
        # consumers (manifest builder, prompt writer) receive well-formed records.
        synthetic = {fd["path"]: fd for fd in pr_details["files"] if fd["path"] in {"/src/file3.ts", "/src/file4.ts"}}
        for path, record in synthetic.items():
            assert "changeType" in record, f"changeType missing for {path}"
            assert record["isBinary"] is False
            assert record["addedLineCount"] == 0
            assert record["addedLines"] == []
            assert record["removedLineCount"] == 0
            assert record["removedLines"] == []
            assert record["patch"] is None

    def test_recovers_files_persist_back_to_pr_details_artifact(self, tmp_path):
        """Test recovered files are written back to the canonical PR details artifact."""
        import json
        from unittest.mock import patch

        from agentic_devtools.cli.azure_devops.review_commands import generate_review_prompts

        pr_details = {
            "files": [
                {"path": "/src/file1.ts", "changeType": "edit"},
            ],
            "threads": [],
        }
        files_on_branch = {"/src/file1.ts", "/src/file2.ts"}
        details_path = tmp_path / "temp-get-pull-request-details-response.json"
        details_path.write_text(json.dumps(pr_details), encoding="utf-8")

        with patch.object(
            __import__("agentic_devtools.cli.azure_devops.review_commands", fromlist=["get_state_dir"]),
            "get_state_dir",
            return_value=tmp_path,
        ):
            generate_review_prompts(
                pull_request_id=123,
                pr_details=pr_details,
                files_on_branch=files_on_branch,
            )

        persisted = json.loads(details_path.read_text(encoding="utf-8"))
        assert {fd["path"] for fd in persisted["files"]} == {"/src/file1.ts", "/src/file2.ts"}

    def test_warns_when_reconciled_pr_details_cannot_be_persisted(self, tmp_path, capsys):
        """Test persistence failures for reconciled PR details emit a warning only."""
        import json
        from unittest.mock import patch

        from agentic_devtools.cli.azure_devops.review_commands import generate_review_prompts

        pr_details = {
            "files": [{"path": "/src/file1.ts", "changeType": "edit"}],
            "threads": [],
        }
        files_on_branch = {"/src/file1.ts", "/src/file2.ts"}
        details_path = tmp_path / "temp-get-pull-request-details-response.json"
        original_payload = json.dumps(pr_details)
        details_path.write_text(original_payload, encoding="utf-8")

        with (
            patch.object(
                __import__("agentic_devtools.cli.azure_devops.review_commands", fromlist=["get_state_dir"]),
                "get_state_dir",
                return_value=tmp_path,
            ),
            patch(
                "agentic_devtools.cli.azure_devops.review_commands.os.replace",
                side_effect=OSError("disk full"),
            ),
        ):
            generate_review_prompts(
                pull_request_id=123,
                pr_details=pr_details,
                files_on_branch=files_on_branch,
            )

        assert "Could not persist filtered PR details artifact" in capsys.readouterr().err
        assert details_path.read_text(encoding="utf-8") == original_payload

    def test_warns_when_temp_file_cannot_be_created_for_reconciled_details(self, tmp_path, capsys):
        """Open/write failures should warn without attempting temp-file cleanup."""
        import builtins
        import json
        from unittest.mock import patch

        from agentic_devtools.cli.azure_devops.review_commands import generate_review_prompts

        pr_details = {
            "files": [{"path": "/src/file1.ts", "changeType": "edit"}],
            "threads": [],
        }
        files_on_branch = {"/src/file1.ts", "/src/file2.ts"}
        details_path = tmp_path / "temp-get-pull-request-details-response.json"
        original_payload = json.dumps(pr_details)
        details_path.write_text(original_payload, encoding="utf-8")
        temp_details_path = details_path.with_name(f"{details_path.name}.tmp")
        real_open = builtins.open

        def failing_open(path, mode="r", *args, **kwargs):
            if path == temp_details_path and "w" in mode:
                raise OSError("disk full")
            return real_open(path, mode, *args, **kwargs)

        with (
            patch.object(
                __import__("agentic_devtools.cli.azure_devops.review_commands", fromlist=["get_state_dir"]),
                "get_state_dir",
                return_value=tmp_path,
            ),
            patch("builtins.open", side_effect=failing_open),
        ):
            generate_review_prompts(
                pull_request_id=123,
                pr_details=pr_details,
                files_on_branch=files_on_branch,
            )

        assert "Could not persist filtered PR details artifact" in capsys.readouterr().err
        assert details_path.read_text(encoding="utf-8") == original_payload

    def test_warns_when_temp_file_cleanup_fails_after_persist_error(self, tmp_path, capsys):
        """Temp-file cleanup failures should not abort prompt generation."""
        import json
        from unittest.mock import patch

        from agentic_devtools.cli.azure_devops.review_commands import generate_review_prompts

        pr_details = {
            "files": [{"path": "/src/file1.ts", "changeType": "edit"}],
            "threads": [],
        }
        files_on_branch = {"/src/file1.ts", "/src/file2.ts"}
        details_path = tmp_path / "temp-get-pull-request-details-response.json"
        original_payload = json.dumps(pr_details)
        details_path.write_text(original_payload, encoding="utf-8")

        with (
            patch.object(
                __import__("agentic_devtools.cli.azure_devops.review_commands", fromlist=["get_state_dir"]),
                "get_state_dir",
                return_value=tmp_path,
            ),
            patch(
                "agentic_devtools.cli.azure_devops.review_commands.os.replace",
                side_effect=OSError("replace fail"),
            ),
            patch(
                "agentic_devtools.cli.azure_devops.review_commands.Path.unlink",
                side_effect=OSError("unlink fail"),
            ),
        ):
            prompts_count, _, _, _, _ = generate_review_prompts(
                pull_request_id=123,
                pr_details=pr_details,
                files_on_branch=files_on_branch,
            )

        captured = capsys.readouterr()
        assert prompts_count == 2
        assert "Could not persist filtered PR details artifact: replace fail" in captured.err
        assert "Could not remove temporary PR details artifact: unlink fail" in captured.err

    def test_loads_pr_details_from_temp_file_when_none(self, tmp_path):
        """Test loads pr_details from temp file when None is passed.

        Covers lines 419-423.
        """
        import json
        from unittest.mock import patch

        from agentic_devtools.cli.azure_devops.review_commands import generate_review_prompts

        pr_details = {
            "files": [
                {"path": "/src/file1.ts", "changeType": "edit"},
            ],
            "threads": [],
        }

        # Write the temp file
        details_path = tmp_path / "temp-get-pull-request-details-response.json"
        with open(details_path, "w", encoding="utf-8") as f:
            json.dump(pr_details, f)

        with patch.object(
            __import__("agentic_devtools.cli.azure_devops.review_commands", fromlist=["get_state_dir"]),
            "get_state_dir",
            return_value=tmp_path,
        ):
            prompts_count, _, _, _, _ = generate_review_prompts(
                pull_request_id=123,
                pr_details=None,  # Force loading from file
                files_on_branch=None,
            )

        assert prompts_count == 1

    def test_loads_files_on_branch_from_json_when_none(self, tmp_path):
        """Test loads files_on_branch from files-on-branch.json when None.

        Covers lines 429-432.
        """
        import json
        from unittest.mock import patch

        from agentic_devtools.cli.azure_devops.review_commands import generate_review_prompts

        pr_details = {
            "files": [
                {"path": "/src/file1.ts", "changeType": "edit"},
                {"path": "/src/file2.ts", "changeType": "edit"},
            ],
            "threads": [],
        }

        # The function uses resolve_review_artifact_dir_name which, with
        # commit_hash_short=None, falls back to "PR{id}" (e.g. "PR123").
        prompts_dir = tmp_path / "pull-request-review" / "PR123"
        prompts_dir.mkdir(parents=True, exist_ok=True)
        files_json = prompts_dir / "files-on-branch.json"
        with open(files_json, "w", encoding="utf-8") as f:
            json.dump({"files": ["/src/file1.ts"]}, f)

        with patch.object(
            __import__("agentic_devtools.cli.azure_devops.review_commands", fromlist=["get_state_dir"]),
            "get_state_dir",
            return_value=tmp_path,
        ):
            with patch(
                "agentic_devtools.cli.azure_devops.review_commands.get_value",
                return_value=None,
            ):
                with patch(
                    "agentic_devtools.cli.azure_devops.review_commands.resolve_review_artifact_dir_name",
                    return_value="PR123",
                ) as resolver:
                    prompts_count, _, skipped_not_on_branch, _, _ = generate_review_prompts(
                        pull_request_id=123,
                        pr_details=pr_details,
                        files_on_branch=None,  # Force loading from file
                    )

        assert prompts_count == 1
        assert skipped_not_on_branch == 1
        resolver.assert_called_once_with(123, None, allow_discovery=False)

    def test_raises_when_pr_details_none_and_temp_file_missing(self, tmp_path):
        """Test raises FileNotFoundError when pr_details is None and temp file doesn't exist.

        Covers line 421.
        """
        from unittest.mock import patch

        import pytest

        from agentic_devtools.cli.azure_devops.review_commands import generate_review_prompts

        with patch.object(
            __import__("agentic_devtools.cli.azure_devops.review_commands", fromlist=["get_state_dir"]),
            "get_state_dir",
            return_value=tmp_path,
        ):
            with pytest.raises(FileNotFoundError, match="PR details file not found"):
                generate_review_prompts(
                    pull_request_id=999,
                    pr_details=None,
                    files_on_branch=None,
                )

    def test_inherited_path_uses_unchanged_file_prompt(self, tmp_path):
        """Test that files with PROCESSING_PATH_INHERITED use the simplified prompt.

        Covers line 506 — the _write_unchanged_file_prompt branch.
        """
        from unittest.mock import MagicMock, patch

        from agentic_devtools.cli.azure_devops.review_commands import generate_review_prompts
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
                __import__("agentic_devtools.cli.azure_devops.review_commands", fromlist=["get_state_dir"]),
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

        from agentic_devtools.cli.azure_devops.review_commands import generate_review_prompts

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
                __import__("agentic_devtools.cli.azure_devops.review_commands", fromlist=["get_state_dir"]),
                "get_state_dir",
                return_value=tmp_path,
            ),
            patch(
                "agentic_devtools.cli.azure_devops.review_commands.get_value",
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

        from agentic_devtools.cli.azure_devops.review_commands import generate_review_prompts

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
                __import__("agentic_devtools.cli.azure_devops.review_commands", fromlist=["get_state_dir"]),
                "get_state_dir",
                return_value=tmp_path,
            ),
            patch("agentic_devtools.cli.azure_devops.review_commands.get_diff_lines_info"),
            patch("agentic_devtools.cli.azure_devops.review_commands.get_diff_patch"),
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

        from agentic_devtools.cli.azure_devops.review_commands import generate_review_prompts

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
                __import__("agentic_devtools.cli.azure_devops.review_commands", fromlist=["get_state_dir"]),
                "get_state_dir",
                return_value=tmp_path,
            ),
            patch("agentic_devtools.cli.azure_devops.review_commands.get_diff_lines_info"),
            patch("agentic_devtools.cli.azure_devops.review_commands.get_diff_patch"),
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

    def test_recovered_files_prefer_saved_diff_base_ref(self, tmp_path):
        """Test recovered-file metadata reuses the persisted diff base ref when available."""
        import json
        from types import SimpleNamespace
        from unittest.mock import patch

        from agentic_devtools.cli.azure_devops.review_commands import generate_review_prompts

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
                __import__("agentic_devtools.cli.azure_devops.review_commands", fromlist=["get_state_dir"]),
                "get_state_dir",
                return_value=tmp_path,
            ),
            patch(
                "agentic_devtools.cli.azure_devops.review_commands.get_diff_lines_info",
                return_value=diff_info,
            ) as mock_diff_lines,
            patch("agentic_devtools.cli.azure_devops.review_commands.get_diff_patch", return_value=None),
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

        from agentic_devtools.cli.azure_devops.review_commands import generate_review_prompts

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
                __import__("agentic_devtools.cli.azure_devops.review_commands", fromlist=["get_state_dir"]),
                "get_state_dir",
                return_value=tmp_path,
            ),
            patch(
                "agentic_devtools.cli.azure_devops.review_commands.get_diff_lines_info",
                return_value=diff_info,
            ) as mock_diff_lines,
            patch(
                "agentic_devtools.cli.azure_devops.review_commands.get_diff_patch",
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

        from agentic_devtools.cli.azure_devops.review_commands import generate_review_prompts

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
                __import__("agentic_devtools.cli.azure_devops.review_commands", fromlist=["get_state_dir"]),
                "get_state_dir",
                return_value=tmp_path,
            ),
            patch(
                "agentic_devtools.cli.azure_devops.review_commands.get_diff_lines_info",
                return_value=diff_info,
            ) as mock_diff_lines,
            patch(
                "agentic_devtools.cli.azure_devops.review_commands.get_diff_patch",
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

        from agentic_devtools.cli.azure_devops.review_commands import generate_review_prompts

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
                __import__("agentic_devtools.cli.azure_devops.review_commands", fromlist=["get_state_dir"]),
                "get_state_dir",
                return_value=tmp_path,
            ),
            patch(
                "agentic_devtools.cli.azure_devops.review_commands.get_diff_lines_info",
                return_value=diff_info,
            ) as mock_diff_lines,
            patch(
                "agentic_devtools.cli.azure_devops.review_commands.get_diff_patch",
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

        from agentic_devtools.cli.azure_devops.review_commands import generate_review_prompts

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
                __import__("agentic_devtools.cli.azure_devops.review_commands", fromlist=["get_state_dir"]),
                "get_state_dir",
                return_value=tmp_path,
            ),
            patch(
                "agentic_devtools.cli.azure_devops.review_commands.get_diff_lines_info",
                return_value=diff_info,
            ) as mock_diff_lines,
            patch(
                "agentic_devtools.cli.azure_devops.review_commands.get_diff_patch",
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

        from agentic_devtools.cli.azure_devops.review_commands import generate_review_prompts

        pr_details = {
            "files": [{"path": "/src/file1.ts", "changeType": "edit"}],
            "threads": [],
        }
        files_on_branch = {"/src/file1.ts", "/src/file3.ts"}

        with (
            patch.object(
                __import__("agentic_devtools.cli.azure_devops.review_commands", fromlist=["get_state_dir"]),
                "get_state_dir",
                return_value=tmp_path,
            ),
            patch(
                "agentic_devtools.cli.azure_devops.review_commands.get_diff_lines_info",
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

        from agentic_devtools.cli.azure_devops.review_commands import generate_review_prompts

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
                __import__("agentic_devtools.cli.azure_devops.review_commands", fromlist=["get_state_dir"]),
                "get_state_dir",
                return_value=tmp_path,
            ),
            patch(
                "agentic_devtools.cli.azure_devops.review_commands.get_diff_lines_info",
                return_value=diff_info,
            ),
            patch(
                "agentic_devtools.cli.azure_devops.review_commands.get_diff_patch",
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

        from agentic_devtools.cli.azure_devops.review_commands import generate_review_prompts

        pr_details = {
            "files": [{"path": "/src/file1.ts", "changeType": "edit"}],
            "threads": [],
        }
        files_on_branch = {"/src/file1.ts", "/src/file3.ts"}
        prompts_dir = tmp_path / "pull-request-review" / "PR123"
        prompts_dir.mkdir(parents=True, exist_ok=True)
        with open(prompts_dir / "files-on-branch.json", "w", encoding="utf-8") as f:
            json.dump({"files": ["/src/file1.ts", "/src/file3.ts"], "change_types": ["not-a-dict"]}, f)

        with patch.object(
            __import__("agentic_devtools.cli.azure_devops.review_commands", fromlist=["get_state_dir"]),
            "get_state_dir",
            return_value=tmp_path,
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

        from agentic_devtools.cli.azure_devops.review_commands import generate_review_prompts

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
            __import__("agentic_devtools.cli.azure_devops.review_commands", fromlist=["get_state_dir"]),
            "get_state_dir",
            return_value=tmp_path,
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

        from agentic_devtools.cli.azure_devops.review_commands import generate_review_prompts

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
            __import__("agentic_devtools.cli.azure_devops.review_commands", fromlist=["get_state_dir"]),
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

    def test_recovered_rename_includes_original_path_from_branch_json(self, tmp_path):
        """Regression: recovered renames must include originalPath from files-on-branch.json.

        Without originalPath, source_context.py queries the destination path at the
        base commit (where the file does not yet exist) and produces an empty base-side
        context, so the pre-rename content is unavailable during the review.
        """
        import json
        from unittest.mock import patch

        from agentic_devtools.cli.azure_devops.review_commands import generate_review_prompts

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
                __import__("agentic_devtools.cli.azure_devops.review_commands", fromlist=["get_state_dir"]),
                "get_state_dir",
                return_value=tmp_path,
            ),
            patch("agentic_devtools.cli.azure_devops.review_commands.get_value", return_value=None),
            patch("agentic_devtools.cli.azure_devops.review_commands.get_diff_lines_info"),
            patch("agentic_devtools.cli.azure_devops.review_commands.get_diff_patch"),
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

        from agentic_devtools.cli.azure_devops.review_commands import generate_review_prompts

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
                __import__("agentic_devtools.cli.azure_devops.review_commands", fromlist=["get_state_dir"]),
                "get_state_dir",
                return_value=tmp_path,
            ),
            patch("agentic_devtools.cli.azure_devops.review_commands.get_value", return_value=None),
            patch("agentic_devtools.cli.azure_devops.review_commands.get_diff_lines_info"),
            patch("agentic_devtools.cli.azure_devops.review_commands.get_diff_patch"),
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

        from agentic_devtools.cli.azure_devops.review_commands import generate_review_prompts

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
                __import__("agentic_devtools.cli.azure_devops.review_commands", fromlist=["get_state_dir"]),
                "get_state_dir",
                return_value=tmp_path,
            ),
            patch("agentic_devtools.cli.azure_devops.review_commands.get_value", return_value=None),
            patch("agentic_devtools.cli.azure_devops.review_commands.get_diff_lines_info"),
            patch("agentic_devtools.cli.azure_devops.review_commands.get_diff_patch"),
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

        from agentic_devtools.cli.azure_devops.review_commands import generate_review_prompts

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
                __import__("agentic_devtools.cli.azure_devops.review_commands", fromlist=["get_state_dir"]),
                "get_state_dir",
                return_value=tmp_path,
            ),
            patch("agentic_devtools.cli.azure_devops.review_commands.get_value", return_value=None),
            patch("agentic_devtools.cli.azure_devops.review_commands.get_diff_lines_info"),
            patch("agentic_devtools.cli.azure_devops.review_commands.get_diff_patch"),
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

        from agentic_devtools.cli.azure_devops.review_commands import generate_review_prompts

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
                __import__("agentic_devtools.cli.azure_devops.review_commands", fromlist=["get_state_dir"]),
                "get_state_dir",
                return_value=tmp_path,
            ),
            patch("agentic_devtools.cli.azure_devops.review_commands.get_value", return_value=None),
            patch(
                "agentic_devtools.cli.azure_devops.review_commands.get_diff_lines_info",
                return_value=diff_info,
            ) as mock_diff_lines,
            patch("agentic_devtools.cli.azure_devops.review_commands.get_diff_patch", return_value=None) as mock_patch,
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

        from agentic_devtools.cli.azure_devops.review_commands import generate_review_prompts

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
                __import__("agentic_devtools.cli.azure_devops.review_commands", fromlist=["get_state_dir"]),
                "get_state_dir",
                return_value=tmp_path,
            ),
            patch("agentic_devtools.cli.azure_devops.review_commands.get_value", return_value=None),
            patch(
                "agentic_devtools.cli.azure_devops.review_commands.get_diff_lines_info",
                return_value=diff_info,
            ) as mock_diff_lines,
            patch("agentic_devtools.cli.azure_devops.review_commands.get_diff_patch", return_value=None),
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

        from agentic_devtools.cli.azure_devops.review_commands import generate_review_prompts

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
                __import__("agentic_devtools.cli.azure_devops.review_commands", fromlist=["get_state_dir"]),
                "get_state_dir",
                return_value=tmp_path,
            ),
            patch("agentic_devtools.cli.azure_devops.review_commands.get_value", return_value=None),
            patch("agentic_devtools.cli.azure_devops.review_commands.get_diff_lines_info"),
            patch("agentic_devtools.cli.azure_devops.review_commands.get_diff_patch"),
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

        from agentic_devtools.cli.azure_devops.review_commands import generate_review_prompts

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
                __import__("agentic_devtools.cli.azure_devops.review_commands", fromlist=["get_state_dir"]),
                "get_state_dir",
                return_value=tmp_path,
            ),
            patch("agentic_devtools.cli.azure_devops.review_commands.get_value", return_value=None),
            patch("agentic_devtools.cli.azure_devops.review_commands.get_diff_lines_info"),
            patch("agentic_devtools.cli.azure_devops.review_commands.get_diff_patch"),
        ):
            generate_review_prompts(
                pull_request_id=123,
                pr_details=pr_details,
                files_on_branch=None,
            )

        recovered = {fd["path"]: fd for fd in pr_details["files"]}
        rename_entry = recovered["/src/renamed-new.ts"]
        assert "originalPath" not in rename_entry

    def test_recovered_files_tolerate_null_comparison(self, tmp_path):
        """comparison=None in pr_details must not raise AttributeError.

        When the PR API returns a null comparison object and no diff_base_ref is
        available, the code must fall back to origin/main rather than crashing.
        """
        from types import SimpleNamespace
        from unittest.mock import patch

        from agentic_devtools.cli.azure_devops.review_commands import generate_review_prompts

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
                __import__("agentic_devtools.cli.azure_devops.review_commands", fromlist=["get_state_dir"]),
                "get_state_dir",
                return_value=tmp_path,
            ),
            patch(
                "agentic_devtools.cli.azure_devops.review_commands.get_diff_lines_info",
                return_value=diff_info,
            ) as mock_diff_lines,
            patch("agentic_devtools.cli.azure_devops.review_commands.get_diff_patch", return_value=None),
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

        from agentic_devtools.cli.azure_devops.review_commands import generate_review_prompts

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
                __import__("agentic_devtools.cli.azure_devops.review_commands", fromlist=["get_state_dir"]),
                "get_state_dir",
                return_value=tmp_path,
            ),
            patch(
                "agentic_devtools.cli.azure_devops.review_commands.get_diff_lines_info",
                return_value=diff_info,
            ) as mock_diff_lines,
            patch("agentic_devtools.cli.azure_devops.review_commands.get_diff_patch", return_value=None),
        ):
            generate_review_prompts(
                pull_request_id=123,
                pr_details=pr_details,
                files_on_branch=files_on_branch,
            )

        mock_diff_lines.assert_called_with("origin/main", "HEAD", "src/file2.ts")
