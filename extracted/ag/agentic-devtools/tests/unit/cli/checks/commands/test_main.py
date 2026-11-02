"""Tests for main entry point."""

from __future__ import annotations

from unittest.mock import patch

from agentic_devtools.cli.checks.commands import main

MODULE = "agentic_devtools.cli.checks.commands"


class TestMain:
    """Tests for main."""

    @patch(f"{MODULE}._run_checks", return_value=0)
    def test_returns_zero_on_success(self, mock_run):
        result = main()
        assert result == 0

    @patch(f"{MODULE}._run_checks", return_value=3)
    def test_returns_failure_count(self, mock_run):
        result = main()
        assert result == 3

    @patch(f"{MODULE}.sys.argv", ["checks", "--format-fix"])
    @patch(f"{MODULE}._run_checks", return_value=0)
    def test_passes_format_fix_flag(self, mock_run):
        main()
        _, kwargs = mock_run.call_args
        assert kwargs["format_fix"] is True

    @patch(f"{MODULE}.sys.argv", ["checks"])
    @patch(f"{MODULE}._run_checks", return_value=0)
    def test_no_format_fix_by_default(self, mock_run):
        main()
        _, kwargs = mock_run.call_args
        assert kwargs["format_fix"] is False

    @patch(f"{MODULE}._run_checks")
    def test_fails_before_running_checks_on_older_python(self, mock_run, capsys):
        with patch(f"{MODULE}._is_supported_python_version", return_value=False):
            assert main() == 1
        mock_run.assert_not_called()
        assert "Python 3.14 or newer is required" in capsys.readouterr().err

    @patch(f"{MODULE}._run_checks", return_value=0)
    def test_runs_checks_on_python_314_or_newer(self, mock_run):
        with patch(f"{MODULE}._is_supported_python_version", return_value=True):
            assert main() == 0
        mock_run.assert_called_once()
