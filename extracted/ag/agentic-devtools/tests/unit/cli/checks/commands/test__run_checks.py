"""Tests for _run_checks orchestrator."""

from __future__ import annotations

from unittest.mock import patch

from agentic_devtools.cli.checks.changed_files import DiffUnavailableError
from agentic_devtools.cli.checks.commands import _CheckResult, _run_checks

MODULE = "agentic_devtools.cli.checks.commands"


class TestRunChecksNoChangedFiles:
    """Tests for _run_checks when no files changed."""

    @patch(f"{MODULE}.get_changed_files", return_value=[])
    @patch(f"{MODULE}.validate_test_structure", return_value=[])
    def test_no_files_all_pass(self, mock_struct, mock_gcf, tmp_path, capsys):
        (tmp_path / "tests" / "unit").mkdir(parents=True)
        result = _run_checks(tmp_path)
        assert result == 0
        out = capsys.readouterr().out
        assert "All targeted checks passed!" in out


class TestRunChecksDiffUnavailable:
    """Tests for _run_checks when git diff fails."""

    @patch(f"{MODULE}.get_changed_files", side_effect=DiffUnavailableError("no git"))
    @patch(f"{MODULE}.validate_test_structure", return_value=[])
    def test_diff_unavailable_fails_fast(self, mock_struct, mock_gcf, tmp_path, capsys):
        (tmp_path / "tests" / "unit").mkdir(parents=True)
        result = _run_checks(tmp_path)
        assert result == 1
        mock_struct.assert_not_called()


class TestRunChecksFormatFix:
    """Tests for _run_checks with --format-fix."""

    @patch(f"{MODULE}._find_test_path", return_value=None)
    @patch(f"{MODULE}.run_one_coverage")
    @patch(f"{MODULE}.run_changed_tests")
    @patch(f"{MODULE}.mypy_check_files", return_value=(True, "ok"))
    @patch(f"{MODULE}.lint_files", return_value=(True, "ok"))
    @patch(f"{MODULE}.format_fix_files", return_value=(False, "1 file reformatted"))
    @patch(f"{MODULE}.validate_test_structure", return_value=[])
    @patch(f"{MODULE}.get_changed_files", return_value=["agentic_devtools/foo.py"])
    def test_format_fix_abort(
        self, mock_gcf, mock_struct, mock_fmt, mock_lint, mock_mypy, mock_tests, mock_cov, mock_ftp, tmp_path, capsys
    ):
        (tmp_path / "tests" / "unit").mkdir(parents=True)
        result = _run_checks(tmp_path, format_fix=True)
        assert result == 10  # Distinct exit code for ruff reformatting
        out = capsys.readouterr().out
        assert "reformatted" in out

    @patch(f"{MODULE}._find_test_path", return_value=None)
    @patch(f"{MODULE}.run_changed_tests", return_value=(True, ""))
    @patch(f"{MODULE}.run_one_coverage", return_value=(True, "ok"))
    @patch(f"{MODULE}.mypy_check_files", return_value=(True, "ok"))
    @patch(f"{MODULE}.lint_files", return_value=(True, "ok"))
    @patch(f"{MODULE}.format_fix_files", return_value=(True, "2 files left unchanged"))
    @patch(f"{MODULE}.validate_test_structure", return_value=[])
    @patch(f"{MODULE}.get_changed_files")
    def test_format_fix_pass_continues(
        self, mock_gcf, mock_struct, mock_fmt, mock_lint, mock_mypy, mock_cov, mock_tests, mock_ftp, tmp_path, capsys
    ):
        mock_gcf.return_value = ["agentic_devtools/foo.py"]
        (tmp_path / "tests" / "unit").mkdir(parents=True)
        _run_checks(tmp_path, format_fix=True)
        # The key assertion: we didn't abort at format step
        assert mock_lint.called

    @patch(f"{MODULE}.format_fix_files")
    @patch(f"{MODULE}.validate_test_structure", return_value=[])
    @patch(f"{MODULE}.get_changed_files", return_value=[])
    def test_format_fix_no_files_skips(self, mock_gcf, mock_struct, mock_fmt, tmp_path, capsys):
        (tmp_path / "tests" / "unit").mkdir(parents=True)
        _run_checks(tmp_path, format_fix=True)
        mock_fmt.assert_not_called()

    @patch(f"{MODULE}.format_fix_files", return_value=(False, "ERROR: ruff format failed\nboom"))
    @patch(f"{MODULE}.validate_test_structure", return_value=[])
    @patch(f"{MODULE}.get_changed_files", return_value=["agentic_devtools/foo.py"])
    def test_format_fix_error_returns_failure(self, mock_gcf, mock_struct, mock_fmt, tmp_path, capsys):
        (tmp_path / "tests" / "unit").mkdir(parents=True)
        result = _run_checks(tmp_path, format_fix=True)
        assert result == 1


class TestRunChecksFormatCheck:
    """Tests for _run_checks in CI mode (format --check)."""

    @patch(f"{MODULE}._find_test_path", return_value=None)
    @patch(f"{MODULE}.run_changed_tests", return_value=(True, ""))
    @patch(f"{MODULE}.run_one_coverage", return_value=(True, "ok"))
    @patch(f"{MODULE}.mypy_check_files", return_value=(True, "ok"))
    @patch(f"{MODULE}.format_check_files", return_value=(False, "Would reformat"))
    @patch(f"{MODULE}.lint_files", return_value=(True, "ok"))
    @patch(f"{MODULE}.validate_test_structure", return_value=[])
    @patch(f"{MODULE}.get_changed_files")
    def test_format_check_failure_counts(
        self, mock_gcf, mock_struct, mock_lint, mock_fmt, mock_mypy, mock_cov, mock_tests, mock_ftp, tmp_path
    ):
        mock_gcf.return_value = ["agentic_devtools/foo.py"]
        (tmp_path / "tests" / "unit").mkdir(parents=True)
        result = _run_checks(tmp_path, format_fix=False)
        assert result >= 1


class TestRunChecksWithFailures:
    """Tests for _run_checks counting failures."""

    @patch(f"{MODULE}._find_test_path", return_value=None)
    @patch(f"{MODULE}.run_changed_tests", return_value=(True, ""))
    @patch(f"{MODULE}.run_one_coverage", return_value=(False, "FAIL"))
    @patch(f"{MODULE}.mypy_check_files", return_value=(False, "error"))
    @patch(f"{MODULE}.format_check_files", return_value=(True, "ok"))
    @patch(f"{MODULE}.lint_files", return_value=(False, "lint error"))
    @patch(f"{MODULE}.validate_test_structure")
    @patch(f"{MODULE}.get_changed_files")
    def test_multiple_failures(
        self, mock_gcf, mock_struct, mock_lint, mock_fmt, mock_mypy, mock_cov, mock_tests, mock_ftp, tmp_path, capsys
    ):
        mock_gcf.return_value = ["agentic_devtools/foo.py"]
        mock_struct.return_value = ["violation 1"]
        (tmp_path / "tests" / "unit").mkdir(parents=True)
        result = _run_checks(tmp_path)
        assert result >= 3  # structure + lint + mypy + coverage
        out = capsys.readouterr().out
        assert "failed" in out.lower()


class TestRunChecksExtraTests:
    """Tests for running additional changed test files."""

    @patch(f"{MODULE}._find_test_path", return_value=None)
    @patch(f"{MODULE}.run_changed_tests", return_value=(True, "3 passed"))
    @patch(f"{MODULE}.run_one_coverage", return_value=(True, "ok"))
    @patch(f"{MODULE}.mypy_check_files", return_value=(True, "ok"))
    @patch(f"{MODULE}.format_check_files", return_value=(True, "ok"))
    @patch(f"{MODULE}.lint_files", return_value=(True, "ok"))
    @patch(f"{MODULE}.validate_test_structure", return_value=[])
    @patch(f"{MODULE}.get_changed_files")
    def test_extra_tests_run(
        self, mock_gcf, mock_struct, mock_lint, mock_fmt, mock_mypy, mock_cov, mock_tests, mock_ftp, tmp_path, capsys
    ):
        def side_effect(*, source_only=False, tests_only=False, cwd=None, **kwargs):
            if source_only:
                return ["agentic_devtools/foo.py"]
            if tests_only:
                return ["tests/unit/other/test_bar.py"]
            return ["agentic_devtools/foo.py", "tests/unit/other/test_bar.py"]

        mock_gcf.side_effect = side_effect
        (tmp_path / "tests" / "unit").mkdir(parents=True)
        _run_checks(tmp_path)
        mock_tests.assert_called_once()

    @patch(f"{MODULE}._find_test_path")
    @patch(f"{MODULE}.run_changed_tests", return_value=(False, "FAIL"))
    @patch(f"{MODULE}.run_one_coverage", return_value=(True, "ok"))
    @patch(f"{MODULE}.mypy_check_files", return_value=(True, "ok"))
    @patch(f"{MODULE}.format_check_files", return_value=(True, "ok"))
    @patch(f"{MODULE}.lint_files", return_value=(True, "ok"))
    @patch(f"{MODULE}.validate_test_structure", return_value=[])
    @patch(f"{MODULE}.get_changed_files")
    def test_extra_tests_failure_counted(
        self, mock_gcf, mock_struct, mock_lint, mock_fmt, mock_mypy, mock_cov, mock_tests, mock_ftp, tmp_path
    ):
        def side_effect(*, source_only=False, tests_only=False, cwd=None, **kwargs):
            if source_only:
                return ["agentic_devtools/foo.py"]
            if tests_only:
                return ["tests/unit/other/test_bar.py"]
            return ["agentic_devtools/foo.py", "tests/unit/other/test_bar.py"]

        mock_gcf.side_effect = side_effect
        mock_ftp.return_value = None
        (tmp_path / "tests" / "unit").mkdir(parents=True)
        result = _run_checks(tmp_path)
        assert result >= 1

    @patch(f"{MODULE}._find_test_path")
    @patch(f"{MODULE}.run_changed_tests", return_value=(True, "ok"))
    @patch(f"{MODULE}.run_one_coverage", return_value=(True, "ok"))
    @patch(f"{MODULE}.mypy_check_files", return_value=(True, "ok"))
    @patch(f"{MODULE}.format_check_files", return_value=(True, "ok"))
    @patch(f"{MODULE}.lint_files", return_value=(True, "ok"))
    @patch(f"{MODULE}.validate_test_structure", return_value=[])
    @patch(f"{MODULE}.get_changed_files")
    def test_covered_tests_deduplicated(
        self, mock_gcf, mock_struct, mock_lint, mock_fmt, mock_mypy, mock_cov, mock_tests, mock_ftp, tmp_path
    ):
        """When _find_test_path returns a test directory, nested changed tests are excluded."""
        covered_test_dir = tmp_path / "tests" / "unit" / "foo"
        mock_ftp.return_value = str(covered_test_dir)

        def side_effect(*, source_only=False, tests_only=False, cwd=None, **kwargs):
            if source_only:
                return ["agentic_devtools/foo.py"]
            if tests_only:
                return ["tests/unit/foo/test_bar.py"]
            return ["agentic_devtools/foo.py", "tests/unit/foo/test_bar.py"]

        mock_gcf.side_effect = side_effect
        (tmp_path / "tests" / "unit").mkdir(parents=True)
        _run_checks(tmp_path)
        # Extra tests should NOT run because the test was already covered
        mock_tests.assert_not_called()

    @patch(f"{MODULE}._find_test_path")
    @patch(f"{MODULE}.run_changed_tests", return_value=(True, "ok"))
    @patch(f"{MODULE}.run_one_coverage", return_value=(True, "ok"))
    @patch(f"{MODULE}.mypy_check_files", return_value=(True, "ok"))
    @patch(f"{MODULE}.format_check_files", return_value=(True, "ok"))
    @patch(f"{MODULE}.lint_files", return_value=(True, "ok"))
    @patch(f"{MODULE}.validate_test_structure", return_value=[])
    @patch(f"{MODULE}.get_changed_files")
    def test_covered_test_file_deduplicated(
        self, mock_gcf, mock_struct, mock_lint, mock_fmt, mock_mypy, mock_cov, mock_tests, mock_ftp, tmp_path
    ):
        """When _find_test_path returns a test file path, the same changed test is excluded."""
        mock_ftp.return_value = "tests/unit/foo/test_bar.py"

        def side_effect(*, source_only=False, tests_only=False, cwd=None, **kwargs):
            if source_only:
                return ["agentic_devtools/foo.py"]
            if tests_only:
                return ["tests/unit/foo/test_bar.py"]
            return ["agentic_devtools/foo.py", "tests/unit/foo/test_bar.py"]

        mock_gcf.side_effect = side_effect
        (tmp_path / "tests" / "unit").mkdir(parents=True)
        _run_checks(tmp_path)
        mock_tests.assert_not_called()


class TestRunChecksReconfigure:
    """Tests for stdout/stderr reconfigure handling."""

    @patch(f"{MODULE}.get_changed_files", return_value=[])
    @patch(f"{MODULE}.validate_test_structure", return_value=[])
    def test_skips_reconfigure_when_not_available(self, mock_struct, mock_gcf, tmp_path, monkeypatch):
        """When stdout/stderr lack reconfigure, the function still runs.

        Covers branches 112->114 and 114->117 (hasattr False paths).
        """
        import io

        # Use a simple StringIO that does NOT have a reconfigure method
        fake_out = io.StringIO()
        fake_err = io.StringIO()
        monkeypatch.setattr("sys.stdout", fake_out)
        monkeypatch.setattr("sys.stderr", fake_err)

        (tmp_path / "tests" / "unit").mkdir(parents=True)
        result = _run_checks(tmp_path)
        assert result == 0


class TestRunChecksFailureOutput:
    """Tests for failure output file saving and condensed display."""

    @patch(f"{MODULE}._find_test_path", return_value=None)
    @patch(f"{MODULE}.run_changed_tests", return_value=(True, ""))
    @patch(f"{MODULE}.run_one_coverage", return_value=(False, "FAIL: missing\nline1\nline2"))
    @patch(f"{MODULE}.mypy_check_files", return_value=(True, "ok"))
    @patch(f"{MODULE}.format_check_files", return_value=(True, "ok"))
    @patch(f"{MODULE}.lint_files", return_value=(True, "ok"))
    @patch(f"{MODULE}.validate_test_structure", return_value=[])
    @patch(f"{MODULE}.get_changed_files")
    def test_saves_full_and_condensed_output_files(
        self, mock_gcf, mock_struct, mock_lint, mock_fmt, mock_mypy, mock_cov, mock_tests, mock_ftp, tmp_path, capsys
    ):
        mock_gcf.return_value = ["agentic_devtools/foo.py"]
        (tmp_path / "tests" / "unit").mkdir(parents=True)
        _run_checks(tmp_path)

        full_log = tmp_path / "check-output.txt"
        condensed_log = tmp_path / "check-output-condensed.txt"
        assert full_log.exists()
        assert condensed_log.exists()

        full_content = full_log.read_text(encoding="utf-8")
        assert "FAIL: missing" in full_content

        condensed_content = condensed_log.read_text(encoding="utf-8")
        assert "FAIL: missing" in condensed_content

        out = capsys.readouterr().out
        assert "Full output saved to:" in out
        assert "Condensed output saved to:" in out


class TestRunChecksProgressLabels:
    """Tests for progress counter output."""

    @patch(f"{MODULE}._find_test_path", return_value=None)
    @patch(f"{MODULE}.run_changed_tests", return_value=(True, ""))
    @patch(f"{MODULE}.run_one_coverage", return_value=(True, "ok"))
    @patch(f"{MODULE}.mypy_check_files", return_value=(True, "ok"))
    @patch(f"{MODULE}.format_check_files", return_value=(True, "ok"))
    @patch(f"{MODULE}.lint_files", return_value=(True, "ok"))
    @patch(f"{MODULE}.validate_test_structure", return_value=[])
    @patch(f"{MODULE}.get_changed_files")
    def test_progress_counter_shown(
        self, mock_gcf, mock_struct, mock_lint, mock_fmt, mock_mypy, mock_cov, mock_tests, mock_ftp, tmp_path, capsys
    ):
        mock_gcf.return_value = ["agentic_devtools/foo.py"]
        (tmp_path / "tests" / "unit").mkdir(parents=True)
        _run_checks(tmp_path)
        out = capsys.readouterr().out
        assert "Progress:" in out
        assert "Starting coverage: agentic_devtools/foo.py" in out

    @patch(f"{MODULE}._find_test_path", return_value=None)
    @patch(f"{MODULE}.run_changed_tests", return_value=(True, ""))
    @patch(f"{MODULE}.run_one_coverage", return_value=(True, "ok"))
    @patch(f"{MODULE}.mypy_check_files", return_value=(True, "ok"))
    @patch(f"{MODULE}.format_check_files", return_value=(True, "ok"))
    @patch(f"{MODULE}.lint_files", return_value=(True, "ok"))
    @patch(f"{MODULE}.validate_test_structure", return_value=[])
    @patch(f"{MODULE}.get_changed_files")
    def test_progress_message_mentions_sequential_coverage(
        self, mock_gcf, mock_struct, mock_lint, mock_fmt, mock_mypy, mock_cov, mock_tests, mock_ftp, tmp_path, capsys
    ):
        """Progress text explains that coverage runs after the parallel phase."""
        mock_gcf.return_value = ["agentic_devtools/foo.py"]
        (tmp_path / "tests" / "unit").mkdir(parents=True)
        _run_checks(tmp_path)
        out = capsys.readouterr().out
        assert "sequential coverage" in out


class TestRunChecksUnexpectedException:
    """Tests for handling unexpected exceptions from check futures."""

    @patch(f"{MODULE}.validate_test_structure", side_effect=RuntimeError("boom"))
    @patch(f"{MODULE}.get_changed_files", return_value=[])
    def test_unexpected_exception_recorded_as_failure(self, mock_gcf, mock_struct, tmp_path, capsys):
        (tmp_path / "tests" / "unit").mkdir(parents=True)
        result = _run_checks(tmp_path)
        assert result >= 1
        out = capsys.readouterr().out
        assert "unexpected error" in out

    @patch(f"{MODULE}._find_test_path", return_value=None)
    @patch(f"{MODULE}.run_changed_tests", return_value=(True, ""))
    @patch(f"{MODULE}.run_one_coverage", side_effect=RuntimeError("coverage exploded"))
    @patch(f"{MODULE}.mypy_check_files", return_value=(True, "ok"))
    @patch(f"{MODULE}.format_check_files", return_value=(True, "ok"))
    @patch(f"{MODULE}.lint_files", return_value=(True, "ok"))
    @patch(f"{MODULE}.validate_test_structure", return_value=[])
    @patch(f"{MODULE}.get_changed_files", return_value=["agentic_devtools/foo.py"])
    def test_sequential_coverage_exception_recorded_as_failure(
        self, mock_gcf, mock_struct, mock_lint, mock_fmt, mock_mypy, mock_cov, mock_ct, mock_ftp, tmp_path, capsys
    ):
        """An unexpected exception from a sequential coverage call is recorded as a
        failed check result rather than crashing the whole _run_checks invocation."""
        (tmp_path / "tests" / "unit").mkdir(parents=True)
        result = _run_checks(tmp_path)
        assert result >= 1
        out = capsys.readouterr().out
        assert "Unexpected exception" in out


class TestRunChecksFileCountBreakdown:
    """Tests for changed file count showing source vs test split."""

    @patch(f"{MODULE}._find_test_path", return_value=None)
    @patch(f"{MODULE}.run_changed_tests", return_value=(True, ""))
    @patch(f"{MODULE}.run_one_coverage", return_value=(True, "ok"))
    @patch(f"{MODULE}.mypy_check_files", return_value=(True, "ok"))
    @patch(f"{MODULE}.format_check_files", return_value=(True, "ok"))
    @patch(f"{MODULE}.lint_files", return_value=(True, "ok"))
    @patch(f"{MODULE}.validate_test_structure", return_value=[])
    @patch(f"{MODULE}.get_changed_files")
    def test_shows_source_and_test_counts(
        self, mock_gcf, mock_struct, mock_lint, mock_fmt, mock_mypy, mock_cov, mock_tests, mock_ftp, tmp_path, capsys
    ):
        def side_effect(*, source_only=False, tests_only=False, cwd=None, **kwargs):
            if source_only:
                return ["agentic_devtools/foo.py"]
            if tests_only:
                return ["tests/unit/foo/test_bar.py", "tests/unit/foo/test_baz.py"]
            return ["agentic_devtools/foo.py", "tests/unit/foo/test_bar.py", "tests/unit/foo/test_baz.py"]

        mock_gcf.side_effect = side_effect
        (tmp_path / "tests" / "unit").mkdir(parents=True)
        _run_checks(tmp_path)
        out = capsys.readouterr().out
        assert "3 (1 source, 2 test)" in out

    @patch(f"{MODULE}._find_test_path", return_value=None)
    @patch(f"{MODULE}.run_changed_tests", return_value=(True, ""))
    @patch(f"{MODULE}.run_one_coverage", return_value=(True, "ok"))
    @patch(f"{MODULE}.mypy_check_files", return_value=(True, "ok"))
    @patch(f"{MODULE}.format_check_files", return_value=(True, "ok"))
    @patch(f"{MODULE}.lint_files", return_value=(True, "ok"))
    @patch(f"{MODULE}.validate_test_structure", return_value=[])
    @patch(f"{MODULE}.get_changed_files")
    def test_source_and_test_breakdown_falls_back_to_empty_on_diff_error(
        self, mock_gcf, mock_struct, mock_lint, mock_fmt, mock_mypy, mock_cov, mock_tests, mock_ftp, tmp_path, capsys
    ):
        mock_gcf.side_effect = [
            ["agentic_devtools/foo.py"],
            DiffUnavailableError("no source diff"),
            DiffUnavailableError("no tests diff"),
            [],
            DiffUnavailableError("no support diff"),
        ]
        (tmp_path / "tests" / "unit").mkdir(parents=True)
        _run_checks(tmp_path)
        out = capsys.readouterr().out
        assert "1 (0 source, 0 test)" in out

    @patch(f"{MODULE}.get_changed_files")
    def test_markdown_diff_unavailable_is_fatal(self, mock_gcf, tmp_path, capsys):
        """A DiffUnavailableError on markdown file detection must fail fast, not silently skip."""
        mock_gcf.side_effect = [
            ["agentic_devtools/foo.py"],
            [],
            [],
            DiffUnavailableError("no markdown diff"),
        ]
        (tmp_path / "tests" / "unit").mkdir(parents=True)
        result = _run_checks(tmp_path)
        assert result == 1


class TestRunChecksMarkdownlint:
    """Tests for wiring markdownlint into the parallel check pool."""

    @staticmethod
    def _side_effect(md_files):
        def side_effect(*, pattern="*.py", source_only=False, tests_only=False, cwd=None, **kwargs):
            if source_only or tests_only:
                return []
            if pattern == "*.md":
                return md_files
            return []

        return side_effect

    @patch(f"{MODULE}.markdownlint_files", return_value=(True, "Summary: 0 error(s)"))
    @patch(f"{MODULE}.validate_test_structure", return_value=[])
    @patch(f"{MODULE}.get_changed_files")
    def test_changed_markdown_is_linted(self, mock_gcf, mock_struct, mock_md, tmp_path, capsys):
        mock_gcf.side_effect = self._side_effect(["docs/guide.md"])
        (tmp_path / "tests" / "unit").mkdir(parents=True)
        result = _run_checks(tmp_path)
        assert result == 0
        mock_md.assert_called_once_with(["docs/guide.md"], cwd=str(tmp_path))
        out = capsys.readouterr().out
        assert "Changed markdown files: 1" in out
        assert "markdownlint changed files" in out

    @patch(f"{MODULE}.markdownlint_files", return_value=(False, "docs/guide.md:1 MD041"))
    @patch(f"{MODULE}.validate_test_structure", return_value=[])
    @patch(f"{MODULE}.get_changed_files")
    def test_markdownlint_failure_is_counted(self, mock_gcf, mock_struct, mock_md, tmp_path, capsys):
        mock_gcf.side_effect = self._side_effect(["docs/guide.md"])
        (tmp_path / "tests" / "unit").mkdir(parents=True)
        result = _run_checks(tmp_path)
        assert result == 1
        out = capsys.readouterr().out
        assert "MD041" in out

    @patch(f"{MODULE}.markdownlint_files")
    @patch(f"{MODULE}.validate_test_structure", return_value=[])
    @patch(f"{MODULE}.get_changed_files")
    def test_no_markdown_changes_skips_markdownlint(self, mock_gcf, mock_struct, mock_md, tmp_path, capsys):
        mock_gcf.side_effect = self._side_effect([])
        (tmp_path / "tests" / "unit").mkdir(parents=True)
        result = _run_checks(tmp_path)
        assert result == 0
        mock_md.assert_not_called()
        out = capsys.readouterr().out
        assert "Changed markdown files: 0" in out


class TestRunChecksCustomizationQuality:
    """Tests for wiring _check_customization_quality into the parallel check pool."""

    @staticmethod
    def _side_effect(md_files):
        def side_effect(*, pattern="*.py", source_only=False, tests_only=False, cwd=None, **kwargs):
            if source_only or tests_only:
                return []
            if pattern == "*.md":
                return md_files
            return []

        return side_effect

    @patch(f"{MODULE}._check_customization_quality")
    @patch(f"{MODULE}.validate_test_structure", return_value=[])
    @patch(f"{MODULE}.get_changed_files")
    def test_called_with_changed_md_and_cwd(self, mock_gcf, mock_struct, mock_cq, tmp_path):
        """_check_customization_quality is submitted with the changed-Markdown list and cwd."""
        mock_gcf.side_effect = self._side_effect([".github/instructions/python.instructions.md"])
        mock_cq.return_value = _CheckResult(
            "Customization quality", True, "OK — 1 customization file(s) validated.", 0.0
        )
        (tmp_path / "tests" / "unit").mkdir(parents=True)
        result = _run_checks(tmp_path)
        assert result == 0
        mock_cq.assert_called_once_with([".github/instructions/python.instructions.md"], tmp_path)

    @patch(f"{MODULE}._check_customization_quality")
    @patch(f"{MODULE}.validate_test_structure", return_value=[])
    @patch(f"{MODULE}.get_changed_files")
    def test_failed_result_makes_runner_fail(self, mock_gcf, mock_struct, mock_cq, tmp_path, capsys):
        """A failing _check_customization_quality result increments the failure count."""
        mock_gcf.side_effect = self._side_effect([".github/instructions/python.instructions.md"])
        mock_cq.return_value = _CheckResult(
            "Customization quality",
            False,
            "  Q10: .github/instructions/python.instructions.md: file too large\nFAIL: 1 violation(s)",
            0.0,
        )
        (tmp_path / "tests" / "unit").mkdir(parents=True)
        result = _run_checks(tmp_path)
        assert result == 1
        out = capsys.readouterr().out
        assert "Customization quality" in out

    @patch(f"{MODULE}._check_customization_quality")
    @patch(f"{MODULE}.validate_test_structure", return_value=[])
    @patch(f"{MODULE}.get_changed_files")
    def test_no_markdown_still_submits_check(self, mock_gcf, mock_struct, mock_cq, tmp_path):
        """_check_customization_quality is always submitted, even with no changed Markdown."""
        mock_gcf.side_effect = self._side_effect([])
        mock_cq.return_value = _CheckResult(
            "Customization quality",
            True,
            "Customization quality check skipped: no customization files changed.",
            0.0,
        )
        (tmp_path / "tests" / "unit").mkdir(parents=True)
        result = _run_checks(tmp_path)
        assert result == 0
        mock_cq.assert_called_once_with([], tmp_path)
