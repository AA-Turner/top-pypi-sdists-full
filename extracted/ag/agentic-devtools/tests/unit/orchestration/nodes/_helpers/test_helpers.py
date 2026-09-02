"""Tests for _helpers module shared utilities."""

import subprocess
from pathlib import Path
from unittest.mock import call, patch

from agentic_devtools.models.git_results import SetupResult
from agentic_devtools.orchestration.nodes._helpers import (
    _resolve_git_common_dir,
    _resolve_process_git_common_dir,
    _to_nonneg_int,
    detect_issue_provider,
    detect_test_conventions,
    get_worktree_path,
    normalize_issue_key,
    read_file_content,
    resolve_repo_root,
    run_command,
    scan_directory_structure,
    utc_now,
)


class TestToNonnegInt:
    def test_int_positive_passthrough(self):
        assert _to_nonneg_int(42) == 42

    def test_int_zero_passthrough(self):
        assert _to_nonneg_int(0) == 0

    def test_int_negative_clamps_to_zero(self):
        assert _to_nonneg_int(-5) == 0

    def test_none_returns_zero(self):
        assert _to_nonneg_int(None) == 0

    def test_true_returns_zero(self):
        # bool is subclass of int; True must not be coerced to 1
        assert _to_nonneg_int(True) == 0

    def test_false_returns_zero(self):
        assert _to_nonneg_int(False) == 0

    def test_float_truncates_and_clamps(self):
        assert _to_nonneg_int(3.9) == 3

    def test_float_negative_returns_zero(self):
        assert _to_nonneg_int(-1.5) == 0

    def test_numeric_string_converts(self):
        assert _to_nonneg_int("100") == 100

    def test_numeric_string_negative_clamps(self):
        assert _to_nonneg_int("-10") == 0

    def test_non_numeric_string_returns_zero(self):
        assert _to_nonneg_int("abc") == 0

    def test_list_returns_zero(self):
        assert _to_nonneg_int([1, 2]) == 0

    def test_dict_returns_zero(self):
        assert _to_nonneg_int({"a": 1}) == 0


class TestDetectIssueProvider:
    def test_jira_key_returns_jira(self):
        assert detect_issue_provider("PROJECT-1234") == "jira"

    def test_numeric_returns_github(self):
        assert detect_issue_provider("42") == "github"

    def test_hash_numeric_returns_github(self):
        assert detect_issue_provider("#42") == "github"

    def test_empty_returns_github(self):
        assert detect_issue_provider("") == "github"

    def test_lowercase_project_returns_jira(self):
        assert detect_issue_provider("project-123") == "jira"

    def test_single_letter_project_returns_github(self):
        # Single letter projects require 2+ chars (e.g. AB-1) per Jira convention
        assert detect_issue_provider("A-1") == "github"

    def test_two_letter_project_returns_jira(self):
        assert detect_issue_provider("AB-1") == "jira"

    def test_jira_key_with_surrounding_whitespace_returns_jira(self):
        assert detect_issue_provider("  PROJECT-1234 \n") == "jira"


class TestNormalizeIssueKey:
    def test_strips_hash_prefix(self):
        assert normalize_issue_key("#42") == "42"

    def test_strips_all_leading_hash_prefixes(self):
        assert normalize_issue_key("###42") == "42"

    def test_preserves_jira_key(self):
        assert normalize_issue_key("PROJECT-1234") == "PROJECT-1234"

    def test_preserves_plain_number(self):
        assert normalize_issue_key("42") == "42"

    def test_strips_surrounding_whitespace_before_normalizing(self):
        assert normalize_issue_key("  #42 \n") == "42"

    def test_hash_only_normalizes_to_empty_string(self):
        assert normalize_issue_key("#") == ""


class TestUtcNow:
    def test_returns_string(self):
        result = utc_now()
        assert isinstance(result, str)

    def test_contains_utc_offset(self):
        result = utc_now()
        assert "+00:00" in result


class TestScanDirectoryStructure:
    def test_returns_empty_for_nonexistent(self, tmp_path):
        nonexistent = tmp_path / "nope"
        result = scan_directory_structure(nonexistent, max_depth=2)
        assert result == []

    def test_returns_files_in_directory(self, tmp_path):
        (tmp_path / "file.py").write_text("hello")
        result = scan_directory_structure(tmp_path, max_depth=1)
        assert "file.py" in result

    def test_excludes_pycache(self, tmp_path):
        (tmp_path / "__pycache__").mkdir()
        (tmp_path / "__pycache__" / "foo.pyc").write_text("")
        result = scan_directory_structure(tmp_path, max_depth=2)
        assert all("__pycache__" not in p for p in result)

    def test_respects_max_depth(self, tmp_path):
        deep = tmp_path / "a" / "b" / "c"
        deep.mkdir(parents=True)
        (deep / "deep.py").write_text("")
        result = scan_directory_structure(tmp_path, max_depth=1)
        assert not any("deep.py" in p for p in result)

    def test_max_depth_zero_returns_empty(self, tmp_path):
        (tmp_path / "file.py").write_text("hello")
        result = scan_directory_structure(tmp_path, max_depth=0)
        assert result == []

    def test_skips_entries_that_are_neither_file_nor_dir(self, tmp_path):
        """Broken symlinks are neither is_file() nor is_dir() — they are skipped."""
        import os

        (tmp_path / "real.py").write_text("hello")
        os.symlink(tmp_path / "nonexistent_target", tmp_path / "broken_link")
        result = scan_directory_structure(tmp_path, max_depth=1)
        assert "real.py" in result
        assert "broken_link" not in result


class TestDetectTestConventions:
    def test_detects_1_1_1_layout(self, tmp_path):
        (tmp_path / "tests" / "unit").mkdir(parents=True)
        result = detect_test_conventions(tmp_path)
        assert result["test_layout"] == "1:1:1"
        assert result["has_tests_unit"] is True

    def test_detects_flat_layout(self, tmp_path):
        (tmp_path / "tests").mkdir()
        result = detect_test_conventions(tmp_path)
        assert result["test_layout"] == "flat"
        assert result["has_tests_unit"] is False

    def test_unknown_when_no_tests(self, tmp_path):
        result = detect_test_conventions(tmp_path)
        assert result["test_layout"] == "unknown"


class TestRunCommand:
    def test_returns_completed_process(self):
        result = run_command(["echo", "hello"])
        assert result.returncode == 0
        assert "hello" in result.stdout

    def test_captures_stderr(self):
        result = run_command(["python3", "-c", "import sys; sys.stderr.write('err')"])
        assert "err" in result.stderr

    def test_nonzero_exit_code(self):
        result = run_command(["python3", "-c", "import sys; sys.exit(1)"])
        assert result.returncode == 1

    def test_timeout_returns_error_result(self):
        with patch(
            "agentic_devtools.orchestration.nodes._helpers.subprocess.run",
            side_effect=subprocess.TimeoutExpired(cmd=["sleep", "10"], timeout=1),
        ):
            result = run_command(["sleep", "10"], timeout=1)
            assert result.returncode == 124
            assert "Command timed out" in result.stderr

    def test_timeout_decodes_byte_stdout(self):
        with patch(
            "agentic_devtools.orchestration.nodes._helpers.subprocess.run",
            side_effect=subprocess.TimeoutExpired(cmd=["sleep", "10"], timeout=1, output=b"partial"),
        ):
            result = run_command(["sleep", "10"], timeout=1)
            assert result.returncode == 124
            assert result.stdout == "partial"

    def test_timeout_preserves_string_stdout(self):
        with patch(
            "agentic_devtools.orchestration.nodes._helpers.subprocess.run",
            side_effect=subprocess.TimeoutExpired(cmd=["sleep", "10"], timeout=1, output="partial"),
        ):
            result = run_command(["sleep", "10"], timeout=1)
            assert result.returncode == 124
            assert result.stdout == "partial"

    def test_timeout_preserves_partial_stderr(self):
        exc = subprocess.TimeoutExpired(cmd=["sleep", "10"], timeout=1)
        exc.stderr = b"partial stderr output"
        with patch(
            "agentic_devtools.orchestration.nodes._helpers.subprocess.run",
            side_effect=exc,
        ):
            result = run_command(["sleep", "10"], timeout=1)
            assert result.returncode == 124
            assert "Command timed out" in result.stderr
            assert "partial stderr output" in result.stderr

    def test_missing_command_returns_error_result(self):
        with patch(
            "agentic_devtools.orchestration.nodes._helpers.subprocess.run",
            side_effect=FileNotFoundError("missing"),
        ):
            result = run_command(["definitely-missing-command"])
            assert result.returncode == 127
            assert "Command not found" in result.stderr


class TestGetWorktreePath:
    def test_returns_setup_result_worktree_path(self, tmp_path):
        top_level_result = type("Result", (), {"returncode": 0, "stdout": f"{tmp_path}\n", "stderr": ""})()
        candidate_common_dir_result = type("Result", (), {"returncode": 0, "stdout": "/shared/.git\n", "stderr": ""})()
        process_common_dir_result = type("Result", (), {"returncode": 0, "stdout": "/shared/.git\n", "stderr": ""})()
        symbolic_ref_result = type(
            "Result", (), {"returncode": 0, "stdout": "refs/heads/feature/42/x\n", "stderr": ""}
        )()
        with patch(
            "agentic_devtools.orchestration.nodes._helpers.run_command",
            side_effect=[top_level_result, candidate_common_dir_result, process_common_dir_result, symbolic_ref_result],
        ):
            result = get_worktree_path(
                {"setup_result": SetupResult(worktree_path=str(tmp_path), branch_name="feature/42/x")}
            )
        assert result == tmp_path.resolve()

    def test_returns_none_for_blank_or_missing_path(self):
        assert get_worktree_path({"setup_result": SetupResult(worktree_path="   ", branch_name="feature/42/x")}) is None
        assert get_worktree_path({}) is None

    def test_returns_none_for_missing_worktree_path(self):
        missing = Path("/definitely/missing/worktree/path")
        with patch("agentic_devtools.orchestration.nodes._helpers.run_command") as mock_run_command:
            result = get_worktree_path(
                {"setup_result": SetupResult(worktree_path=str(missing), branch_name="feature/42/x")}
            )
        assert result is None
        mock_run_command.assert_not_called()

    def test_returns_none_when_git_toplevel_does_not_match_worktree(self, tmp_path):
        mock_result = type("Result", (), {"returncode": 0, "stdout": "/other/repo\n", "stderr": ""})()
        with patch("agentic_devtools.orchestration.nodes._helpers.run_command", return_value=mock_result):
            result = get_worktree_path(
                {"setup_result": SetupResult(worktree_path=str(tmp_path), branch_name="feature/42/x")}
            )
        assert result is None

    def test_returns_none_when_git_toplevel_command_fails(self, tmp_path):
        mock_result = type("Result", (), {"returncode": 128, "stdout": "", "stderr": "fatal"})()
        with patch("agentic_devtools.orchestration.nodes._helpers.run_command", return_value=mock_result):
            result = get_worktree_path(
                {"setup_result": SetupResult(worktree_path=str(tmp_path), branch_name="feature/42/x")}
            )
        assert result is None

    def test_returns_none_when_git_toplevel_output_is_blank(self, tmp_path):
        mock_result = type("Result", (), {"returncode": 0, "stdout": "\n", "stderr": ""})()
        with patch("agentic_devtools.orchestration.nodes._helpers.run_command", return_value=mock_result):
            result = get_worktree_path(
                {"setup_result": SetupResult(worktree_path=str(tmp_path), branch_name="feature/42/x")}
            )
        assert result is None

    def test_returns_none_when_git_common_dir_differs_from_process_repo(self, tmp_path):
        top_level_result = type("Result", (), {"returncode": 0, "stdout": f"{tmp_path}\n", "stderr": ""})()
        candidate_common_dir_result = type(
            "Result", (), {"returncode": 0, "stdout": "/candidate/.git\n", "stderr": ""}
        )()
        process_common_dir_result = type("Result", (), {"returncode": 0, "stdout": "/process/.git\n", "stderr": ""})()
        with patch(
            "agentic_devtools.orchestration.nodes._helpers.run_command",
            side_effect=[top_level_result, candidate_common_dir_result, process_common_dir_result],
        ):
            result = get_worktree_path(
                {"setup_result": SetupResult(worktree_path=str(tmp_path), branch_name="feature/42/x")}
            )
        assert result is None

    def test_returns_none_when_candidate_git_common_dir_command_fails(self, tmp_path):
        top_level_result = type("Result", (), {"returncode": 0, "stdout": f"{tmp_path}\n", "stderr": ""})()
        candidate_common_dir_result = type("Result", (), {"returncode": 128, "stdout": "", "stderr": "fatal"})()
        with patch(
            "agentic_devtools.orchestration.nodes._helpers.run_command",
            side_effect=[top_level_result, candidate_common_dir_result],
        ):
            result = get_worktree_path(
                {"setup_result": SetupResult(worktree_path=str(tmp_path), branch_name="feature/42/x")}
            )
        assert result is None

    def test_returns_none_when_process_git_common_dir_command_fails(self, tmp_path):
        top_level_result = type("Result", (), {"returncode": 0, "stdout": f"{tmp_path}\n", "stderr": ""})()
        candidate_common_dir_result = type("Result", (), {"returncode": 0, "stdout": "/shared/.git\n", "stderr": ""})()
        process_common_dir_result = type("Result", (), {"returncode": 128, "stdout": "", "stderr": "fatal"})()
        with patch(
            "agentic_devtools.orchestration.nodes._helpers.run_command",
            side_effect=[top_level_result, candidate_common_dir_result, process_common_dir_result],
        ):
            result = get_worktree_path(
                {"setup_result": SetupResult(worktree_path=str(tmp_path), branch_name="feature/42/x")}
            )
        assert result is None

    def test_returns_none_when_git_common_dir_output_is_blank(self, tmp_path):
        top_level_result = type("Result", (), {"returncode": 0, "stdout": f"{tmp_path}\n", "stderr": ""})()
        candidate_common_dir_result = type("Result", (), {"returncode": 0, "stdout": "\n", "stderr": ""})()
        with patch(
            "agentic_devtools.orchestration.nodes._helpers.run_command",
            side_effect=[top_level_result, candidate_common_dir_result],
        ):
            result = get_worktree_path(
                {"setup_result": SetupResult(worktree_path=str(tmp_path), branch_name="feature/42/x")}
            )
        assert result is None

    def test_returns_none_when_branch_has_been_switched(self, tmp_path):
        top_level_result = type("Result", (), {"returncode": 0, "stdout": f"{tmp_path}\n", "stderr": ""})()
        candidate_common_dir_result = type("Result", (), {"returncode": 0, "stdout": "/shared/.git\n", "stderr": ""})()
        process_common_dir_result = type("Result", (), {"returncode": 0, "stdout": "/shared/.git\n", "stderr": ""})()
        symbolic_ref_result = type("Result", (), {"returncode": 0, "stdout": "refs/heads/main\n", "stderr": ""})()
        with patch(
            "agentic_devtools.orchestration.nodes._helpers.run_command",
            side_effect=[top_level_result, candidate_common_dir_result, process_common_dir_result, symbolic_ref_result],
        ):
            result = get_worktree_path(
                {"setup_result": SetupResult(worktree_path=str(tmp_path), branch_name="feature/42/x")}
            )
        assert result is None

    def test_returns_none_when_symbolic_ref_command_fails(self, tmp_path):
        top_level_result = type("Result", (), {"returncode": 0, "stdout": f"{tmp_path}\n", "stderr": ""})()
        candidate_common_dir_result = type("Result", (), {"returncode": 0, "stdout": "/shared/.git\n", "stderr": ""})()
        process_common_dir_result = type("Result", (), {"returncode": 0, "stdout": "/shared/.git\n", "stderr": ""})()
        symbolic_ref_result = type(
            "Result", (), {"returncode": 128, "stdout": "", "stderr": "fatal: ref HEAD is not a symbolic ref"}
        )()
        with patch(
            "agentic_devtools.orchestration.nodes._helpers.run_command",
            side_effect=[top_level_result, candidate_common_dir_result, process_common_dir_result, symbolic_ref_result],
        ):
            result = get_worktree_path(
                {"setup_result": SetupResult(worktree_path=str(tmp_path), branch_name="feature/42/x")}
            )
        assert result is None

    def test_skips_branch_check_when_branch_name_is_none(self, tmp_path):
        top_level_result = type("Result", (), {"returncode": 0, "stdout": f"{tmp_path}\n", "stderr": ""})()
        candidate_common_dir_result = type("Result", (), {"returncode": 0, "stdout": "/shared/.git\n", "stderr": ""})()
        process_common_dir_result = type("Result", (), {"returncode": 0, "stdout": "/shared/.git\n", "stderr": ""})()
        with patch(
            "agentic_devtools.orchestration.nodes._helpers.run_command",
            side_effect=[top_level_result, candidate_common_dir_result, process_common_dir_result],
        ) as mock_run_command:
            result = get_worktree_path({"setup_result": SetupResult(worktree_path=str(tmp_path), branch_name=None)})
        assert result == tmp_path.resolve()
        assert mock_run_command.call_count == 3


class TestResolveRepoRoot:
    def test_prefers_setup_result_worktree_path(self, tmp_path):
        top_level_result = type("Result", (), {"returncode": 0, "stdout": f"{tmp_path}\n", "stderr": ""})()
        candidate_common_dir_result = type("Result", (), {"returncode": 0, "stdout": "/shared/.git\n", "stderr": ""})()
        process_common_dir_result = type("Result", (), {"returncode": 0, "stdout": "/shared/.git\n", "stderr": ""})()
        symbolic_ref_result = type(
            "Result", (), {"returncode": 0, "stdout": "refs/heads/feature/42/x\n", "stderr": ""}
        )()
        with patch(
            "agentic_devtools.orchestration.nodes._helpers.run_command",
            side_effect=[top_level_result, candidate_common_dir_result, process_common_dir_result, symbolic_ref_result],
        ) as mock_run_command:
            result = resolve_repo_root(
                {"setup_result": SetupResult(worktree_path=str(tmp_path), branch_name="feature/42/x")}
            )
        assert result == tmp_path.resolve()
        mock_run_command.assert_has_calls(
            [
                call(["git", "rev-parse", "--show-toplevel"], cwd=str(tmp_path.resolve())),
                call(["git", "rev-parse", "--git-common-dir"], cwd=str(tmp_path.resolve())),
                call(["git", "rev-parse", "--git-common-dir"], cwd=str(Path.cwd())),
                call(["git", "symbolic-ref", "HEAD"], cwd=str(tmp_path.resolve())),
            ]
        )

    def test_falls_back_to_git_toplevel(self):
        mock_result = type("Result", (), {"returncode": 0, "stdout": "/repo/root\n", "stderr": ""})()
        with patch("agentic_devtools.orchestration.nodes._helpers.run_command", return_value=mock_result):
            result = resolve_repo_root()
        assert result == Path("/repo/root")

    def test_returns_none_when_git_lookup_fails(self):
        mock_result = type("Result", (), {"returncode": 128, "stdout": "", "stderr": "not a git repo"})()
        with patch("agentic_devtools.orchestration.nodes._helpers.run_command", return_value=mock_result):
            result = resolve_repo_root()
        assert result is None

    def test_returns_none_when_worktree_branch_switched(self, tmp_path):
        top_level_result = type("Result", (), {"returncode": 0, "stdout": f"{tmp_path}\n", "stderr": ""})()
        candidate_common_dir_result = type("Result", (), {"returncode": 0, "stdout": "/shared/.git\n", "stderr": ""})()
        process_common_dir_result = type("Result", (), {"returncode": 0, "stdout": "/shared/.git\n", "stderr": ""})()
        symbolic_ref_result = type(
            "Result", (), {"returncode": 0, "stdout": "refs/heads/other-branch\n", "stderr": ""}
        )()
        with patch(
            "agentic_devtools.orchestration.nodes._helpers.run_command",
            side_effect=[top_level_result, candidate_common_dir_result, process_common_dir_result, symbolic_ref_result],
        ):
            result = resolve_repo_root(
                {"setup_result": SetupResult(worktree_path=str(tmp_path), branch_name="feature/42/x")}
            )
        assert result is None

    def test_explicit_invalid_worktree_path_returns_none_without_process_fallback(self, tmp_path):
        validation_result = type("Result", (), {"returncode": 0, "stdout": "/other/repo\n", "stderr": ""})()
        fallback_result = type("Result", (), {"returncode": 0, "stdout": "/process/repo\n", "stderr": ""})()
        with patch(
            "agentic_devtools.orchestration.nodes._helpers.run_command",
            side_effect=[validation_result, fallback_result],
        ) as mock_run_command:
            result = resolve_repo_root(
                {"setup_result": SetupResult(worktree_path=str(tmp_path), branch_name="feature/42/x")}
            )
        assert result is None
        mock_run_command.assert_called_once_with(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=str(tmp_path.resolve()),
        )


class TestReadFileContent:
    def test_reads_file(self, tmp_path):
        f = tmp_path / "test.txt"
        f.write_text("hello world", encoding="utf-8")
        assert read_file_content(f) == "hello world"

    def test_truncates_long_content(self, tmp_path):
        f = tmp_path / "big.txt"
        f.write_text("x" * 200, encoding="utf-8")
        result = read_file_content(f, max_chars=50)
        assert len(result) <= 50  # must not exceed the max_chars budget
        assert "[truncated]" in result

    def test_truncated_length_equals_max_chars(self, tmp_path):
        f = tmp_path / "big.txt"
        f.write_text("x" * 200, encoding="utf-8")
        result = read_file_content(f, max_chars=50)
        assert len(result) == 50  # exactly max_chars, not max_chars + len(suffix)

    def test_max_chars_smaller_than_suffix_does_not_exceed_budget(self, tmp_path):
        # When max_chars <= len("\n... [truncated]") the suffix itself would exceed
        # the budget; the function must fall back to a plain slice without appending it.
        f = tmp_path / "big.txt"
        f.write_text("x" * 200, encoding="utf-8")
        result = read_file_content(f, max_chars=5)
        assert len(result) <= 5

    def test_returns_empty_on_missing_file(self, tmp_path):
        f = tmp_path / "nope.txt"
        assert read_file_content(f) == ""

    def test_returns_empty_on_decode_error(self, tmp_path):
        f = tmp_path / "binary.bin"
        f.write_bytes(b"\xff\xfe\x00\x01" * 100)
        with patch.object(type(f), "read_text", side_effect=UnicodeDecodeError("utf-8", b"", 0, 1, "bad")):
            assert read_file_content(f) == ""


class TestResolveGitCommonDir:
    def test_returns_none_for_blank_output(self, tmp_path):
        assert _resolve_git_common_dir(" \n", tmp_path) is None

    def test_resolves_relative_path_against_cwd(self, tmp_path):
        resolved = _resolve_git_common_dir(".git", tmp_path)
        assert resolved == (tmp_path / ".git").resolve()

    def test_resolves_absolute_path(self):
        resolved = _resolve_git_common_dir("/shared/.git", Path("/tmp"))
        assert resolved == Path("/shared/.git").resolve()


class TestResolveProcessGitCommonDir:
    def test_returns_common_dir_from_current_working_directory(self):
        process_common_dir_result = type("Result", (), {"returncode": 0, "stdout": "/shared/.git\n", "stderr": ""})()
        with patch(
            "agentic_devtools.orchestration.nodes._helpers.run_command",
            side_effect=[process_common_dir_result],
        ):
            resolved = _resolve_process_git_common_dir()
        assert resolved == Path("/shared/.git").resolve()

    def test_returns_none_when_current_working_directory_is_not_git(self):
        cwd_result = type("Result", (), {"returncode": 128, "stdout": "", "stderr": "fatal"})()
        with patch(
            "agentic_devtools.orchestration.nodes._helpers.run_command",
            side_effect=[cwd_result],
        ):
            resolved = _resolve_process_git_common_dir()
        assert resolved is None

    def test_returns_none_for_blank_common_dir_output(self):
        cwd_result = type("Result", (), {"returncode": 0, "stdout": "\n", "stderr": ""})()
        with patch(
            "agentic_devtools.orchestration.nodes._helpers.run_command",
            side_effect=[cwd_result],
        ):
            resolved = _resolve_process_git_common_dir()
        assert resolved is None
