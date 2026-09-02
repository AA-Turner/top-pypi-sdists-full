"""Tests for show_log in agentic_devtools.cli.setup.decision_log."""

from pathlib import Path
from unittest.mock import patch

from agentic_devtools.cli.setup.decision_log import show_log


class TestShowLog:
    """Tests for show_log() read-only behavior."""

    def test_missing_file_returns_empty(self, tmp_path: Path) -> None:
        """File does not exist → returns empty string."""
        with patch(
            "agentic_devtools.cli.setup.decision_log.get_state_dir",
            return_value=tmp_path,
        ):
            result = show_log()
            assert result == ""

    def test_empty_file_returns_empty(self, tmp_path: Path) -> None:
        """File exists but is empty → returns empty string."""
        setup_dir = tmp_path / "setup"
        setup_dir.mkdir(parents=True)
        (setup_dir / "run-setup-decision-log.md").write_text("", encoding="utf-8")

        with patch(
            "agentic_devtools.cli.setup.decision_log.get_state_dir",
            return_value=tmp_path,
        ):
            result = show_log()
            assert result == ""

    def test_whitespace_only_file_returns_unchanged(self, tmp_path: Path) -> None:
        """File with only whitespace → returns contents unchanged."""
        setup_dir = tmp_path / "setup"
        setup_dir.mkdir(parents=True)
        content = "   \n\n  "
        (setup_dir / "run-setup-decision-log.md").write_text(content, encoding="utf-8")

        with patch(
            "agentic_devtools.cli.setup.decision_log.get_state_dir",
            return_value=tmp_path,
        ):
            result = show_log()
            assert result == content

    def test_file_with_entries_returns_full_contents(self, tmp_path: Path) -> None:
        """File with valid entries → returns full raw contents."""
        setup_dir = tmp_path / "setup"
        setup_dir.mkdir(parents=True)
        content = (
            "<!-- agdt-decision-entry:start id:1 -->\n"
            "### Decision #1 (2026-07-08T18:30:00+00:00)\n"
            "- Step: install-dependencies\n"
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
            result = show_log()
            assert result == content

    def test_freeform_text_returns_unchanged(self, tmp_path: Path) -> None:
        """File with freeform text (no markers) → returns contents unchanged."""
        setup_dir = tmp_path / "setup"
        setup_dir.mkdir(parents=True)
        content = "Some random text\nAnother line\n"
        (setup_dir / "run-setup-decision-log.md").write_text(content, encoding="utf-8")

        with patch(
            "agentic_devtools.cli.setup.decision_log.get_state_dir",
            return_value=tmp_path,
        ):
            result = show_log()
            assert result == content

    def test_does_not_create_file(self, tmp_path: Path) -> None:
        """show_log never creates the log file."""
        with patch(
            "agentic_devtools.cli.setup.decision_log.get_state_dir",
            return_value=tmp_path,
        ):
            show_log()
            assert not (tmp_path / "setup" / "run-setup-decision-log.md").exists()

    def test_read_race_deleted_file_returns_empty(self, tmp_path: Path) -> None:
        """File disappearing right before read is treated as missing log."""
        setup_dir = tmp_path / "setup"
        setup_dir.mkdir(parents=True)
        log_path = setup_dir / "run-setup-decision-log.md"
        log_path.write_text("content", encoding="utf-8")

        with (
            patch("agentic_devtools.cli.setup.decision_log.get_state_dir", return_value=tmp_path),
            patch.object(Path, "read_text", side_effect=FileNotFoundError),
        ):
            assert show_log() == ""

    def test_permission_error_returns_empty(self, tmp_path: Path) -> None:
        """Permission errors are treated as unreadable/missing log."""
        with (
            patch("agentic_devtools.cli.setup.decision_log.get_state_dir", return_value=tmp_path),
            patch.object(Path, "read_text", side_effect=PermissionError),
        ):
            assert show_log() == ""

    def test_unicode_decode_error_returns_empty(self, tmp_path: Path) -> None:
        """Unicode decode errors are treated as unreadable/missing log."""
        with (
            patch("agentic_devtools.cli.setup.decision_log.get_state_dir", return_value=tmp_path),
            patch.object(Path, "read_text", side_effect=UnicodeDecodeError("utf-8", b"\x80", 0, 1, "boom")),
        ):
            assert show_log() == ""

    def test_is_a_directory_error_returns_empty(self, tmp_path: Path) -> None:
        """Directory path at log location is treated as unreadable/missing log."""
        with (
            patch("agentic_devtools.cli.setup.decision_log.get_state_dir", return_value=tmp_path),
            patch.object(Path, "read_text", side_effect=IsADirectoryError),
        ):
            assert show_log() == ""

    def test_generic_oserror_returns_empty(self, tmp_path: Path) -> None:
        """Any generic OSError (e.g. I/O failure) is treated as unreadable/missing log."""
        with (
            patch("agentic_devtools.cli.setup.decision_log.get_state_dir", return_value=tmp_path),
            patch.object(Path, "read_text", side_effect=OSError("I/O error")),
        ):
            assert show_log() == ""
