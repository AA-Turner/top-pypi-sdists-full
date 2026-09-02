"""Tests for decision_log_command in agentic_devtools.cli.setup.decision_log."""

import sys
from pathlib import Path
from unittest.mock import patch

import pytest

from agentic_devtools.cli.setup.decision_log import decision_log_command


class TestDecisionLogCommandAppend:
    """Tests for the 'append' subcommand."""

    def test_valid_args_exit_0(self, tmp_path: Path, capsys) -> None:
        """Valid args → exit 0, stdout contains confirmation."""
        with patch(
            "agentic_devtools.cli.setup.decision_log.get_state_dir",
            return_value=tmp_path,
        ):
            with patch.object(
                sys,
                "argv",
                [
                    "agdt-setup-decision-log",
                    "append",
                    "--step",
                    "install-deps",
                    "--question",
                    "npm unreachable?",
                    "--decision",
                    "Skip optional",
                    "--rationale",
                    "Timeout after 30s",
                    "--auto-resolved",
                    "true",
                ],
            ):
                decision_log_command()
                captured = capsys.readouterr()
                assert "Decision #1 recorded." in captured.out

    def test_missing_required_arg_exits_nonzero(self, capsys) -> None:
        """Missing required arg → exit non-zero with stderr error."""
        with patch.object(
            sys,
            "argv",
            [
                "agdt-setup-decision-log",
                "append",
                "--step",
                "install-deps",
                # missing --question, --decision, --rationale, --auto-resolved
            ],
        ):
            with pytest.raises(SystemExit) as exc_info:
                decision_log_command()
            assert exc_info.value.code != 0

    def test_auto_resolved_invalid_exits_nonzero(self) -> None:
        """--auto-resolved maybe → exit non-zero argparse error."""
        with patch.object(
            sys,
            "argv",
            [
                "agdt-setup-decision-log",
                "append",
                "--step",
                "s",
                "--question",
                "q",
                "--decision",
                "d",
                "--rationale",
                "r",
                "--auto-resolved",
                "maybe",
            ],
        ):
            with pytest.raises(SystemExit) as exc_info:
                decision_log_command()
            assert exc_info.value.code != 0

    def test_auto_resolved_case_insensitive(self, tmp_path: Path, capsys) -> None:
        """--auto-resolved TRUE → exit 0 (case-insensitive)."""
        with patch(
            "agentic_devtools.cli.setup.decision_log.get_state_dir",
            return_value=tmp_path,
        ):
            with patch.object(
                sys,
                "argv",
                [
                    "agdt-setup-decision-log",
                    "append",
                    "--step",
                    "s",
                    "--question",
                    "q",
                    "--decision",
                    "d",
                    "--rationale",
                    "r",
                    "--auto-resolved",
                    "TRUE",
                ],
            ):
                decision_log_command()
                captured = capsys.readouterr()
                assert "Decision #1 recorded." in captured.out

    def test_auto_resolved_false_case_insensitive(self, tmp_path: Path, capsys) -> None:
        """--auto-resolved FALSE → exit 0 (case-insensitive)."""
        with patch(
            "agentic_devtools.cli.setup.decision_log.get_state_dir",
            return_value=tmp_path,
        ):
            with patch.object(
                sys,
                "argv",
                [
                    "agdt-setup-decision-log",
                    "append",
                    "--step",
                    "s",
                    "--question",
                    "q",
                    "--decision",
                    "d",
                    "--rationale",
                    "r",
                    "--auto-resolved",
                    "FALSE",
                ],
            ):
                decision_log_command()
                captured = capsys.readouterr()
                assert "Decision #1 recorded." in captured.out

    def test_validation_error_exits_1(self, tmp_path: Path, capsys) -> None:
        """Validation error prints to stderr and exits 1."""
        with patch(
            "agentic_devtools.cli.setup.decision_log.get_state_dir",
            return_value=tmp_path,
        ):
            with patch.object(
                sys,
                "argv",
                [
                    "agdt-setup-decision-log",
                    "append",
                    "--step",
                    "",
                    "--question",
                    "q",
                    "--decision",
                    "d",
                    "--rationale",
                    "r",
                    "--auto-resolved",
                    "true",
                ],
            ):
                with pytest.raises(SystemExit) as exc_info:
                    decision_log_command()
                assert exc_info.value.code == 1
                captured = capsys.readouterr()
                assert "Error:" in captured.err


class TestDecisionLogCommandShow:
    """Tests for the 'show' subcommand."""

    def test_existing_log_prints_contents(self, tmp_path: Path, capsys) -> None:
        """Existing log → exit 0, stdout matches file content exactly."""
        setup_dir = tmp_path / "setup"
        setup_dir.mkdir(parents=True)
        content = (
            "<!-- agdt-decision-entry:start id:1 -->\n"
            "### Decision #1 (2026-07-08T18:30:00+00:00)\n"
            "- Step: install-deps\n"
            "- Question: npm unreachable?\n"
            "- Decision: Skip optional\n"
            "- Rationale: Timeout\n"
            "- Auto-resolved: true\n"
            "<!-- agdt-decision-entry:end -->\n"
        )
        (setup_dir / "run-setup-decision-log.md").write_text(content, encoding="utf-8")

        with patch(
            "agentic_devtools.cli.setup.decision_log.get_state_dir",
            return_value=tmp_path,
        ):
            with patch.object(sys, "argv", ["agdt-setup-decision-log", "show"]):
                decision_log_command()
                captured = capsys.readouterr()
                assert captured.out == content

    def test_existing_log_without_trailing_newline_no_extra_newline(self, tmp_path: Path, capsys) -> None:
        """Show subcommand does not append an extra trailing newline."""
        setup_dir = tmp_path / "setup"
        setup_dir.mkdir(parents=True)
        content = "Decision block without trailing newline"
        (setup_dir / "run-setup-decision-log.md").write_text(content, encoding="utf-8")

        with patch(
            "agentic_devtools.cli.setup.decision_log.get_state_dir",
            return_value=tmp_path,
        ):
            with patch.object(sys, "argv", ["agdt-setup-decision-log", "show"]):
                decision_log_command()
                captured = capsys.readouterr()
                assert captured.out == content

    def test_missing_log_prints_info_message(self, tmp_path: Path, capsys) -> None:
        """Missing log → exit 0, stdout has informational message."""
        with patch(
            "agentic_devtools.cli.setup.decision_log.get_state_dir",
            return_value=tmp_path,
        ):
            with patch.object(sys, "argv", ["agdt-setup-decision-log", "show"]):
                decision_log_command()
                captured = capsys.readouterr()
                assert "No decisions recorded yet." in captured.out

    def test_no_subcommand_exits_1(self, capsys) -> None:
        """No subcommand → prints help and exits 1."""
        with patch.object(sys, "argv", ["agdt-setup-decision-log"]):
            with pytest.raises(SystemExit) as exc_info:
                decision_log_command()
            assert exc_info.value.code == 1
