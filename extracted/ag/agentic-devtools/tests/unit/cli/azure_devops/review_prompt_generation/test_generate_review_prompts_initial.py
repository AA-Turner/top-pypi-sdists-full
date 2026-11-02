"""Tests for the review_prompt_generation module and helper functions."""


class TestGenerateReviewPrompts:
    """Tests for generate_review_prompts function."""

    def test_generates_prompts_for_files(self, tmp_path):
        """Test generates prompt files for PR files."""
        from unittest.mock import patch

        from agentic_devtools.cli.azure_devops.review_prompt_generation import generate_review_prompts

        pr_details = {
            "files": [
                {"path": "/src/file1.ts", "changeType": "edit"},
                {"path": "/src/file2.ts", "changeType": "add"},
            ],
            "threads": [],
        }

        # Patch the scripts directory location
        with patch("agentic_devtools.cli.azure_devops.review_prompt_generation.Path") as mock_path:
            # Make the path operations work with tmp_path
            mock_path.return_value.parent.parent.parent.parent.parent = tmp_path
            mock_path.return_value.__truediv__ = lambda self, x: tmp_path / x

            # Actually call the function but with simplified setup
            from agentic_devtools.cli.azure_devops.review_prompt_generation import generate_review_prompts

            # Minimal patching to avoid complex path issues
            with patch.object(
                __import__("agentic_devtools.cli.azure_devops.review_prompt_generation", fromlist=["get_state_dir"]),
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

        from agentic_devtools.cli.azure_devops.review_prompt_generation import generate_review_prompts

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
            __import__("agentic_devtools.cli.azure_devops.review_prompt_generation", fromlist=["get_state_dir"]),
            "get_state_dir",
            return_value=tmp_path,
        ):
            prompts_count, skipped_reviewed, skipped_not_on_branch, _, skipped_files = generate_review_prompts(
                pull_request_id=123,
                pr_details=pr_details,
                files_on_branch=None,
            )

        # File is NOT skipped â€” all files are reviewed every run
        assert prompts_count == 1
        assert skipped_reviewed == 0
        assert skipped_files == []

    def test_skips_files_not_on_branch(self, tmp_path):
        """Test skips files not in the branch changes."""
        from unittest.mock import patch

        from agentic_devtools.cli.azure_devops.review_prompt_generation import generate_review_prompts

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
            __import__("agentic_devtools.cli.azure_devops.review_prompt_generation", fromlist=["get_state_dir"]),
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

        from agentic_devtools.cli.azure_devops.review_prompt_generation import generate_review_prompts

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
            __import__("agentic_devtools.cli.azure_devops.review_prompt_generation", fromlist=["get_state_dir"]),
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

        # All 4 files must be generated â€” none silently dropped.
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

        from agentic_devtools.cli.azure_devops.review_prompt_generation import generate_review_prompts

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
            __import__("agentic_devtools.cli.azure_devops.review_prompt_generation", fromlist=["get_state_dir"]),
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

        from agentic_devtools.cli.azure_devops.review_prompt_generation import generate_review_prompts

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
                __import__("agentic_devtools.cli.azure_devops.review_prompt_generation", fromlist=["get_state_dir"]),
                "get_state_dir",
                return_value=tmp_path,
            ),
            patch(
                "agentic_devtools.cli.azure_devops.review_prompt_generation.os.replace",
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

        from agentic_devtools.cli.azure_devops.review_prompt_generation import generate_review_prompts

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
                __import__("agentic_devtools.cli.azure_devops.review_prompt_generation", fromlist=["get_state_dir"]),
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

        from agentic_devtools.cli.azure_devops.review_prompt_generation import generate_review_prompts

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
                __import__("agentic_devtools.cli.azure_devops.review_prompt_generation", fromlist=["get_state_dir"]),
                "get_state_dir",
                return_value=tmp_path,
            ),
            patch(
                "agentic_devtools.cli.azure_devops.review_prompt_generation.os.replace",
                side_effect=OSError("replace fail"),
            ),
            patch(
                "agentic_devtools.cli.azure_devops.review_prompt_generation.Path.unlink",
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

        from agentic_devtools.cli.azure_devops.review_prompt_generation import generate_review_prompts

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
            __import__("agentic_devtools.cli.azure_devops.review_prompt_generation", fromlist=["get_state_dir"]),
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

        from agentic_devtools.cli.azure_devops.review_prompt_generation import generate_review_prompts

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

        from agentic_devtools.cli.azure_devops.review_prompt_generation import generate_review_prompts

        with patch.object(
            __import__("agentic_devtools.cli.azure_devops.review_prompt_generation", fromlist=["get_state_dir"]),
            "get_state_dir",
            return_value=tmp_path,
        ):
            with pytest.raises(FileNotFoundError, match="PR details file not found"):
                generate_review_prompts(
                    pull_request_id=999,
                    pr_details=None,
                    files_on_branch=None,
                )
