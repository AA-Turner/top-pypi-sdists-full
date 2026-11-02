"""Tests for check_workflow_files."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

from agentic_devtools.cli.checks.workflow_lint import check_workflow_files

MODULE = "agentic_devtools.cli.checks.workflow_lint"


def _install_fake_actionlint(tmp_path: Path, monkeypatch) -> Path:
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    fixture = bin_dir / "fake_actionlint.py"
    fixture.write_text(
        """\
import json
import os
import sys
from pathlib import Path

Path(os.environ["ACTIONLINT_RECORD"]).write_text(
    json.dumps({"args": sys.argv[1:], "cwd": os.getcwd()}), encoding="utf-8"
)
sys.stdout.write(os.environ.get("ACTIONLINT_STDOUT", ""))
sys.stderr.write(os.environ.get("ACTIONLINT_STDERR", ""))
raise SystemExit(int(os.environ.get("ACTIONLINT_RETURN_CODE", "0")))
""",
        encoding="utf-8",
    )
    if os.name == "nt":
        executable = bin_dir / "actionlint.cmd"
        executable.write_text(
            f'@echo off\r\n"{sys.executable}" "{fixture}" %*\r\nexit /b %ERRORLEVEL%\r\n',
            encoding="utf-8",
        )
    else:
        executable = bin_dir / "actionlint"
        executable.write_text(f"#!{sys.executable}\n" + fixture.read_text(encoding="utf-8"), encoding="utf-8")
        executable.chmod(0o755)
    monkeypatch.setenv("PATH", str(bin_dir) + os.pathsep + os.environ.get("PATH", ""))
    monkeypatch.setenv("ACTIONLINT_RECORD", str(tmp_path / "actionlint-record.json"))
    return executable


class TestCheckWorkflowFiles:
    def test_empty_selection_passes_without_tool_lookup(self, tmp_path):
        with (
            patch(f"{MODULE}.select_changed_workflow_files", return_value=[]),
            patch(f"{MODULE}.shutil.which") as mock_which,
            patch(f"{MODULE}.subprocess.run") as mock_run,
        ):
            result = check_workflow_files(tmp_path)

        assert result.label == "Lint changed workflows"
        assert result.passed is True
        assert result.output == "OK - no changed workflow files."
        mock_which.assert_not_called()
        mock_run.assert_not_called()

    def test_missing_actionlint_fails_with_setup_guidance(self, tmp_path):
        selected = [".github/workflows/build.yml"]
        with (
            patch(f"{MODULE}.select_changed_workflow_files", return_value=selected),
            patch(f"{MODULE}.shutil.which", return_value=None) as mock_which,
            patch(f"{MODULE}.subprocess.run") as mock_run,
        ):
            result = check_workflow_files(tmp_path)

        assert result.passed is False
        assert "bash scripts/install-actionlint.sh" in result.output
        assert "scripts/actionlint-version.txt" in result.output
        mock_which.assert_called_once_with("actionlint")
        mock_run.assert_not_called()

    def test_fake_actionlint_success_receives_only_selected_paths_and_cwd(self, tmp_path, monkeypatch):
        selected = [".github/workflows/one.yml", ".github/workflows/two.yaml"]
        _install_fake_actionlint(tmp_path, monkeypatch)
        monkeypatch.setenv("ACTIONLINT_STDOUT", "ok\n")
        with patch(f"{MODULE}.select_changed_workflow_files", return_value=selected):
            result = check_workflow_files(tmp_path)

        record = json.loads((tmp_path / "actionlint-record.json").read_text(encoding="utf-8"))
        assert result.label == "Lint changed workflows"
        assert result.passed is True
        assert result.output == "ok"
        assert record == {"args": selected, "cwd": str(tmp_path)}

    def test_fake_actionlint_failure_preserves_diagnostic(self, tmp_path, monkeypatch):
        selected = [".github/workflows/broken.yml"]
        _install_fake_actionlint(tmp_path, monkeypatch)
        monkeypatch.setenv("ACTIONLINT_RETURN_CODE", "1")
        monkeypatch.setenv("ACTIONLINT_STDERR", "broken.yml:12:3: invalid expression context\n")
        with patch(f"{MODULE}.select_changed_workflow_files", return_value=selected):
            result = check_workflow_files(tmp_path)

        assert result.passed is False
        assert "broken.yml:12:3" in result.output
        assert "invalid expression context" in result.output

    def test_process_start_error_fails_actionably(self, tmp_path):
        selected = [".github/workflows/build.yml"]
        with (
            patch(f"{MODULE}.select_changed_workflow_files", return_value=selected),
            patch(f"{MODULE}.shutil.which", return_value="/unavailable/actionlint"),
            patch(f"{MODULE}.subprocess.run", side_effect=OSError("permission denied")) as mock_run,
        ):
            result = check_workflow_files(tmp_path)

        assert result.passed is False
        assert "could not run actionlint" in result.output
        assert "permission denied" in result.output
        assert mock_run.call_args.args[0] == ["/unavailable/actionlint", *selected]
        assert mock_run.call_args.kwargs["cwd"] == tmp_path
        assert mock_run.call_args.kwargs["shell"] is False

    def test_selector_errors_are_not_converted_to_empty_selection(self, tmp_path):
        with (
            patch(f"{MODULE}.select_changed_workflow_files", side_effect=RuntimeError("diff unavailable")),
            patch(f"{MODULE}.shutil.which") as mock_which,
        ):
            with pytest.raises(RuntimeError, match="diff unavailable"):
                check_workflow_files(tmp_path)
        mock_which.assert_not_called()
