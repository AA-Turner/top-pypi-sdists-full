"""Tests for sync_back_cmd() CLI entry point."""

import json
from pathlib import Path
from unittest.mock import patch

import pytest

from agentic_devtools.cli.config.sync_back import sync_back_cmd

_PC_MOD = "agentic_devtools.cli.config.project_config"
_STATE_MOD = "agentic_devtools.state"


class TestSyncBackCmd:
    """Tests for sync_back_cmd CLI argument parsing."""

    def test_defaults_to_all_eligible_without_flags(self, monkeypatch) -> None:
        """No key-selection flags defaults to syncing all eligible keys."""
        monkeypatch.setattr("sys.argv", ["agdt-sync-back"])
        with patch(
            "agentic_devtools.cli.config.sync_back.sync_back",
            return_value={"synced_keys": [], "skipped_keys": [], "warnings": [], "errors": []},
        ) as mock_sync_back:
            sync_back_cmd()

        mock_sync_back.assert_called_once_with(
            keys=None,
            all_eligible=True,
            dry_run=False,
        )

    def test_keys_with_only_empty_segments_errors(self, monkeypatch, capsys) -> None:
        """--keys must include at least one non-empty key after comma expansion."""
        monkeypatch.setattr("sys.argv", ["agdt-sync-back", "--keys", ","])

        with pytest.raises(SystemExit) as exc_info:
            sync_back_cmd()
        assert exc_info.value.code == 2  # argparse error
        captured = capsys.readouterr()
        assert "must include at least one non-empty key" in captured.err

    def test_keys_deduplicate_after_comma_expansion(self, monkeypatch) -> None:
        """Expanded --keys values are deduplicated while preserving order."""
        monkeypatch.setattr(
            "sys.argv",
            ["agdt-sync-back", "--keys", "vpn_url,vpn_url", "jira_base_url", "vpn_url"],
        )
        with patch(
            "agentic_devtools.cli.config.sync_back.sync_back",
            return_value={"synced_keys": [], "skipped_keys": [], "warnings": [], "errors": []},
        ) as mock_sync_back:
            sync_back_cmd()

        mock_sync_back.assert_called_once_with(
            keys=["vpn_url", "jira_base_url"],
            all_eligible=False,
            dry_run=False,
        )

    def test_keys_and_all_eligible_mutually_exclusive(self, monkeypatch) -> None:
        """--keys and --all-eligible cannot both be specified."""
        monkeypatch.setattr(
            "sys.argv",
            ["agdt-sync-back", "--keys", "default_copilot_model", "--all-eligible"],
        )
        with pytest.raises(SystemExit) as exc_info:
            sync_back_cmd()
        assert exc_info.value.code == 2

    def test_dry_run_flag(self, monkeypatch, tmp_path: Path) -> None:
        """--dry-run prevents file modification."""
        config_path = tmp_path / ".agdt" / "config" / "project.json"
        config_path.parent.mkdir(parents=True)
        config_path.write_text(json.dumps({"default_copilot_model": "old"}, indent=2))

        monkeypatch.setattr(
            "sys.argv",
            ["agdt-sync-back", "--keys", "default_copilot_model", "--dry-run"],
        )

        with (
            patch(
                f"{_PC_MOD}._get_config_path",
                return_value=config_path,
            ),
            patch(
                f"{_STATE_MOD}.get_value",
                return_value="new-model",
            ),
        ):
            sync_back_cmd()

        # File should NOT be modified
        written = json.loads(config_path.read_text())
        assert written["default_copilot_model"] == "old"

    def test_dry_run_no_changes(self, monkeypatch, tmp_path: Path, capsys) -> None:
        """Dry-run when no changes shows appropriate message."""
        config_path = tmp_path / ".agdt" / "config" / "project.json"
        config_path.parent.mkdir(parents=True)
        config_path.write_text(json.dumps({"default_copilot_model": "same"}, indent=2))

        monkeypatch.setattr(
            "sys.argv",
            ["agdt-sync-back", "--keys", "default_copilot_model", "--dry-run"],
        )

        with (
            patch(
                f"{_PC_MOD}._get_config_path",
                return_value=config_path,
            ),
            patch(
                f"{_STATE_MOD}.get_value",
                return_value="same",
            ),
        ):
            sync_back_cmd()

        captured = capsys.readouterr()
        assert "No changes" in captured.out

    def test_no_changes_not_duplicated_on_stderr(self, monkeypatch, tmp_path: Path, capsys) -> None:
        """'No changes' appears only on stdout, not also as a stderr warning."""
        config_path = tmp_path / ".agdt" / "config" / "project.json"
        config_path.parent.mkdir(parents=True)
        config_path.write_text(json.dumps({"default_copilot_model": "same"}, indent=2))

        monkeypatch.setattr(
            "sys.argv",
            ["agdt-sync-back", "--keys", "default_copilot_model"],
        )

        with (
            patch(
                f"{_PC_MOD}._get_config_path",
                return_value=config_path,
            ),
            patch(
                f"{_STATE_MOD}.get_value",
                return_value="same",
            ),
        ):
            sync_back_cmd()

        captured = capsys.readouterr()
        assert "No changes" in captured.out
        assert "No changes" not in captured.err
        assert "all requested values already match project.json" in captured.out

    def test_dry_run_reports_cross_field_errors(self, monkeypatch, tmp_path: Path) -> None:
        """--dry-run reports cross-field validation errors."""
        config_path = tmp_path / ".agdt" / "config" / "project.json"
        config_path.parent.mkdir(parents=True)
        config_path.write_text(
            json.dumps(
                {"availableCommitIssueTypes": ["feat", "fix"], "defaultCommitIssueType": "feat"},
                indent=2,
            )
        )

        def mock_get_value(key, **kwargs):
            if key == "versionControl.commitMessageType":
                return "chore"
            return None

        monkeypatch.setattr(
            "sys.argv",
            ["agdt-sync-back", "--keys", "defaultCommitIssueType", "--dry-run"],
        )

        with (
            patch(
                f"{_PC_MOD}._get_config_path",
                return_value=config_path,
            ),
            patch(
                f"{_STATE_MOD}.get_value",
                side_effect=mock_get_value,
            ),
            pytest.raises(SystemExit) as exc_info,
        ):
            sync_back_cmd()

        assert exc_info.value.code == 1

    def test_handles_value_error(self, monkeypatch, tmp_path: Path, capsys) -> None:
        """Exits with error when sync_back raises ValueError."""
        monkeypatch.setattr(
            "sys.argv",
            ["agdt-sync-back", "--keys", "default_copilot_model"],
        )

        with (
            patch(
                "agentic_devtools.cli.config.sync_back.sync_back",
                side_effect=ValueError("Malformed JSON in project.json"),
            ),
            pytest.raises(SystemExit) as exc_info,
        ):
            sync_back_cmd()

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "Malformed JSON" in captured.err

    def test_handles_runtime_error(self, monkeypatch, tmp_path: Path, capsys) -> None:
        """Exits with error when sync_back raises RuntimeError."""
        monkeypatch.setattr(
            "sys.argv",
            ["agdt-sync-back", "--keys", "default_copilot_model"],
        )

        with (
            patch(
                "agentic_devtools.cli.config.sync_back.sync_back",
                side_effect=RuntimeError("Cannot determine git repository root"),
            ),
            pytest.raises(SystemExit) as exc_info,
        ):
            sync_back_cmd()

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "Cannot determine" in captured.err

    def test_dry_run_with_changes_shows_rerun_message(self, monkeypatch, tmp_path: Path, capsys) -> None:
        """Dry-run with changes shows re-run message."""
        config_path = tmp_path / ".agdt" / "config" / "project.json"
        config_path.parent.mkdir(parents=True)
        config_path.write_text(json.dumps({"default_copilot_model": "old"}, indent=2))

        monkeypatch.setattr(
            "sys.argv",
            ["agdt-sync-back", "--keys", "default_copilot_model", "--dry-run"],
        )

        with (
            patch(
                f"{_PC_MOD}._get_config_path",
                return_value=config_path,
            ),
            patch(
                f"{_STATE_MOD}.get_value",
                return_value="new-model",
            ),
        ):
            sync_back_cmd()

        captured = capsys.readouterr()
        assert "Dry run" in captured.out
        assert "Re-run without --dry-run" in captured.out

    def test_keys_comma_separated_input(self, monkeypatch, tmp_path: Path, capsys) -> None:
        """--keys accepts comma-separated values like --keys vpn_url,vpn_hostnames."""
        config_path = tmp_path / ".agdt" / "config" / "project.json"
        config_path.parent.mkdir(parents=True)
        config_path.write_text(
            json.dumps(
                {"vpn_url": "https://old.vpn.example.com", "vpn_hostnames": "old.host"},
                indent=2,
            )
        )

        monkeypatch.setattr(
            "sys.argv",
            ["agdt-sync-back", "--keys", "vpn_url,vpn_hostnames"],
        )

        def mock_get_value(key, **kwargs):
            if key == "vpn_url":
                return "https://new.vpn.example.com"
            if key == "vpn_hostnames":
                return "new.host"
            return None

        with (
            patch(
                f"{_PC_MOD}._get_config_path",
                return_value=config_path,
            ),
            patch(
                f"{_STATE_MOD}.get_value",
                side_effect=mock_get_value,
            ),
        ):
            sync_back_cmd()

        captured = capsys.readouterr()
        assert "vpn_url" in captured.out
        assert "vpn_hostnames" in captured.out

    def test_successful_sync_prints_changes(self, monkeypatch, tmp_path: Path, capsys) -> None:
        """Successful sync prints the changes made."""
        config_path = tmp_path / ".agdt" / "config" / "project.json"
        config_path.parent.mkdir(parents=True)
        config_path.write_text(json.dumps({"default_copilot_model": "old"}, indent=2))

        monkeypatch.setattr(
            "sys.argv",
            ["agdt-sync-back", "--keys", "default_copilot_model"],
        )

        with (
            patch(
                f"{_PC_MOD}._get_config_path",
                return_value=config_path,
            ),
            patch(
                f"{_STATE_MOD}.get_value",
                return_value="new-model",
            ),
        ):
            sync_back_cmd()

        captured = capsys.readouterr()
        assert "Synced the following keys" in captured.out
        assert "default_copilot_model" in captured.out

    def test_all_eligible_flag_passes_none_keys(self, monkeypatch, tmp_path: Path, capsys) -> None:
        """--all-eligible uses the args.keys=None branch (273->278)."""
        config_path = tmp_path / ".agdt" / "config" / "project.json"
        config_path.parent.mkdir(parents=True)
        config_path.write_text(json.dumps({"default_copilot_model": "old"}, indent=2))

        monkeypatch.setattr(
            "sys.argv",
            ["agdt-sync-back", "--all-eligible"],
        )

        def mock_get_value(key, **kwargs):
            # Only provide a value for default_copilot_model; all others return None (skipped).
            if key == "copilot.model_id":
                return "new-model"
            return None

        with (
            patch(
                f"{_PC_MOD}._get_config_path",
                return_value=config_path,
            ),
            patch(
                f"{_STATE_MOD}.get_value",
                side_effect=mock_get_value,
            ),
        ):
            sync_back_cmd()

        captured = capsys.readouterr()
        assert "Synced the following keys" in captured.out

    def test_no_changes_skipped_state_missing_prints_neutral_message(self, monkeypatch, tmp_path: Path, capsys) -> None:
        """When all keys are skipped due to missing state, prints a neutral message."""
        config_path = tmp_path / ".agdt" / "config" / "project.json"
        config_path.parent.mkdir(parents=True)
        config_path.write_text("{}\n")

        monkeypatch.setattr(
            "sys.argv",
            ["agdt-sync-back", "--keys", "default_copilot_model"],
        )

        with (
            patch(
                f"{_PC_MOD}._get_config_path",
                return_value=config_path,
            ),
            patch(
                f"{_STATE_MOD}.get_value",
                return_value=None,
            ),
        ):
            sync_back_cmd()

        captured = capsys.readouterr()
        assert "No values were synced" in captured.out
        assert "not set in state" in captured.out
