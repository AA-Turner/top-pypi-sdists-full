"""Tests for implementation_review_node."""

from pathlib import Path
from unittest.mock import call, patch

from agentic_devtools.models.git_results import SetupResult
from agentic_devtools.orchestration.nodes.implementation_review import (
    _scan_file,
    implementation_review_node,
)


class TestImplementationReviewNode:
    def test_no_affected_paths_returns_clean(self):
        with patch(
            "agentic_devtools.orchestration.nodes.implementation_review.resolve_repo_root",
            return_value=Path("/tmp/repo"),
        ):
            result = implementation_review_node({"affected_paths": []})
            assert result["step"] == "implementation_review"
            assert result["verification_ready"] is True

    def test_detects_issues_in_files(self, tmp_path):
        test_file = tmp_path / "bad.py"
        test_file.write_text("x = 1\nbreakpoint()\ny = 2")
        with patch(
            "agentic_devtools.orchestration.nodes.implementation_review.resolve_repo_root",
            return_value=tmp_path.resolve(),
        ):
            result = implementation_review_node({"affected_paths": ["bad.py"]})
            assert result["error"] is not None
            assert "Debug" in result["error"] or "breakpoint" in result["error"]

    def test_skips_missing_files(self, tmp_path):
        with patch(
            "agentic_devtools.orchestration.nodes.implementation_review.resolve_repo_root",
            return_value=tmp_path.resolve(),
        ):
            result = implementation_review_node({"affected_paths": ["nonexistent.py"]})
            assert result["verification_ready"] is True

    def test_rejects_path_traversal_outside_repo(self, tmp_path):
        """Paths that escape repo_root via '..' must be silently skipped."""
        # Create a sentinel file one level above tmp_path that must never be scanned.
        outside = tmp_path.parent / "outside_secret.py"
        try:
            outside.write_text("breakpoint()  # should not be scanned")
            traversal_path = "../outside_secret.py"
            with patch(
                "agentic_devtools.orchestration.nodes.implementation_review.resolve_repo_root",
                return_value=tmp_path.resolve(),
            ):
                result = implementation_review_node({"affected_paths": [traversal_path]})
                # The traversal path is skipped; no issues surfaced
                assert result["verification_ready"] is True
                assert result.get("error") is None
                # Confirm sentinel content is absent from every event/error field
                result_str = str(result)
                assert "breakpoint" not in result_str
        finally:
            outside.unlink(missing_ok=True)

    def test_skips_non_python_files(self, tmp_path):
        (tmp_path / "readme.md").write_text("# TODO: write docs")
        with patch(
            "agentic_devtools.orchestration.nodes.implementation_review.resolve_repo_root",
            return_value=tmp_path.resolve(),
        ):
            result = implementation_review_node({"affected_paths": ["readme.md"]})
            assert result["verification_ready"] is True

    def test_returns_clean_when_no_repo_root(self):
        with patch(
            "agentic_devtools.orchestration.nodes.implementation_review.resolve_repo_root",
            return_value=None,
        ):
            result = implementation_review_node({"affected_paths": ["file.py"], "error": "stale error"})
            assert result["verification_ready"] is True
            assert result["error"] is None
            assert result["events"][0]["signals"].get("skipped") == "no_repo_root"

    def test_stale_explicit_worktree_blocks_review(self):
        """When setup_result checkpoints a worktree that resolve_repo_root can no longer
        validate, implementation review must return verification_ready=False so the caller
        can trigger a fresh setup rather than advancing to verification silently."""
        with patch(
            "agentic_devtools.orchestration.nodes.implementation_review.resolve_repo_root",
            return_value=None,
        ):
            result = implementation_review_node(
                {
                    "affected_paths": ["file.py"],
                    "setup_result": SetupResult(worktree_path="/tmp/gone-wt", branch_name="feature/42/x"),
                }
            )
        assert result["verification_ready"] is False
        assert result["error"] is not None
        assert "no longer accessible" in result["error"]
        assert result["events"][0]["event"] == "implementation_review_blocked"
        assert result["events"][0]["signals"]["reason"] == "worktree_unavailable"

    def test_dry_run_with_simulated_worktree_skips_to_clean_path(self):
        """Dry runs record a simulated worktree path that never exists on disk.
        The stale-worktree guard must not fire for dry runs so verification_ready
        is returned as True via the repo_root is None clean-skip path."""
        with patch(
            "agentic_devtools.orchestration.nodes.implementation_review.resolve_repo_root",
            return_value=None,
        ):
            result = implementation_review_node(
                {
                    "affected_paths": [],
                    "dry_run": True,
                    "setup_result": SetupResult(
                        worktree_path="/tmp/dry-run-simulated-wt",
                        branch_name="feature/42/dry",
                    ),
                }
            )
        assert result["verification_ready"] is True
        assert result["error"] is None

    def test_emits_completed_event_when_clean(self, tmp_path):
        with patch(
            "agentic_devtools.orchestration.nodes.implementation_review.resolve_repo_root",
            return_value=tmp_path.resolve(),
        ):
            result = implementation_review_node({"affected_paths": []})
            assert result["events"][0]["event"] == "implementation_review_completed"

    def test_emits_issues_found_event(self, tmp_path):
        test_file = tmp_path / "x.py"
        test_file.write_text("# FIXME: broken")
        with patch(
            "agentic_devtools.orchestration.nodes.implementation_review.resolve_repo_root",
            return_value=tmp_path.resolve(),
        ):
            result = implementation_review_node({"affected_paths": ["x.py"]})
            assert result["events"][0]["event"] == "implementation_review_issues_found"

    def test_handles_none_affected_paths(self):
        with patch(
            "agentic_devtools.orchestration.nodes.implementation_review.resolve_repo_root",
            return_value=Path("/tmp"),
        ):
            result = implementation_review_node({"affected_paths": None})
            assert result["verification_ready"] is True

    def test_handles_string_affected_paths_without_char_iteration(self):
        """A corrupted string value must not be iterated character-by-character."""
        with patch(
            "agentic_devtools.orchestration.nodes.implementation_review.resolve_repo_root",
            return_value=Path("/tmp"),
        ):
            # If string were iterated as chars, individual chars "s","r","c",…
            # would be treated as file paths and the loop would scan dozens of
            # spurious paths — here we simply assert no exception is raised and
            # no false issues are reported for non-existent single-char paths.
            result = implementation_review_node({"affected_paths": "src/corrupted.py"})
            assert result["verification_ready"] is True

    def test_skips_file_on_read_error(self, tmp_path):
        """Verify OSError/UnicodeDecodeError when reading a file is gracefully skipped."""
        test_file = tmp_path / "bad_encoding.py"
        test_file.write_text("clean code", encoding="utf-8")
        with (
            patch(
                "agentic_devtools.orchestration.nodes.implementation_review.resolve_repo_root",
                return_value=tmp_path.resolve(),
            ),
            patch("pathlib.Path.read_text", side_effect=UnicodeDecodeError("utf-8", b"", 0, 1, "bad")),
        ):
            result = implementation_review_node({"affected_paths": ["bad_encoding.py"]})
            assert result["verification_ready"] is True

    def test_uses_setup_result_worktree_path_after_git_validation(self, tmp_path):
        test_file = tmp_path / "bad.py"
        test_file.write_text("breakpoint()")
        git_common_dir_result = type("Result", (), {"returncode": 0, "stdout": f"{tmp_path}\n", "stderr": ""})()
        symbolic_ref_result = type(
            "Result", (), {"returncode": 0, "stdout": "refs/heads/feature/42/x\n", "stderr": ""}
        )()
        show_toplevel_result = type("Result", (), {"returncode": 0, "stdout": f"{tmp_path}\n", "stderr": ""})()

        def _side_effect(cmd, **_kwargs):
            if cmd[1:] == ["symbolic-ref", "HEAD"]:
                return symbolic_ref_result
            if cmd[1:] == ["rev-parse", "--show-toplevel"]:
                return show_toplevel_result
            return git_common_dir_result

        with patch(
            "agentic_devtools.orchestration.nodes._helpers.run_command",
            side_effect=_side_effect,
        ) as mock_run_command:
            result = implementation_review_node(
                {
                    "affected_paths": ["bad.py"],
                    "setup_result": SetupResult(worktree_path=str(tmp_path), branch_name="feature/42/x"),
                }
            )
        assert result["error"] is not None
        assert mock_run_command.call_args_list == [
            call(["git", "rev-parse", "--show-toplevel"], cwd=str(tmp_path.resolve())),
            call(["git", "rev-parse", "--git-common-dir"], cwd=str(tmp_path.resolve())),
            call(["git", "rev-parse", "--git-common-dir"], cwd=str(Path.cwd().resolve())),
            call(["git", "symbolic-ref", "HEAD"], cwd=str(tmp_path.resolve())),
        ]


class TestScanFileExtended:
    def test_detects_print_debug(self):
        issues = _scan_file("x.py", 'print("DEBUG: value =", x)')
        assert len(issues) >= 1

    def test_ignores_regular_print(self):
        issues = _scan_file("x.py", 'print("Hello, world!")')
        assert issues == []

    def test_detects_import_ipdb(self):
        issues = _scan_file("x.py", "import ipdb\nipdb.set_trace()")
        assert len(issues) >= 1

    def test_detects_hack_marker(self):
        issues = _scan_file("x.py", "# HACK: temporary workaround")
        assert len(issues) == 1

    def test_detects_xxx_marker(self):
        issues = _scan_file("x.py", "# XXX: needs attention")
        assert len(issues) == 1

    def test_skips_non_python_non_js_markers(self):
        issues = _scan_file("x.py", "# regular comment\nx = 42")
        assert issues == []
