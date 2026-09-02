"""Tests for sync_back() core function."""

import io
import json
from contextlib import contextmanager
from pathlib import Path
from unittest.mock import patch

import pytest

from agentic_devtools.cli.config.sync_back import sync_back

_PC_MOD = "agentic_devtools.cli.config.project_config"
_STATE_MOD = "agentic_devtools.state"


class TestSyncBackHappyPath:
    """Tests for sync_back happy path scenarios."""

    def test_single_key_update(self, tmp_path: Path) -> None:
        """Syncs a single key from state to project.json."""
        config_path = tmp_path / ".agdt" / "config" / "project.json"
        config_path.parent.mkdir(parents=True)
        config_path.write_text(json.dumps({"default_copilot_model": "old-model"}, indent=2))

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
            result = sync_back(keys=["default_copilot_model"], git_root=tmp_path)

        assert len(result["synced_keys"]) == 1
        assert result["synced_keys"][0]["key"] == "default_copilot_model"
        assert result["synced_keys"][0]["new_value"] == "new-model"
        assert not result["errors"]

        # Verify file was written
        written = json.loads(config_path.read_text())
        assert written["default_copilot_model"] == "new-model"

    def test_preserves_existing_keys(self, tmp_path: Path) -> None:
        """Existing keys not being synced are preserved."""
        config_path = tmp_path / ".agdt" / "config" / "project.json"
        config_path.parent.mkdir(parents=True)
        config_path.write_text(json.dumps({"default_copilot_model": "old", "jira_base_url": "http://jira"}, indent=2))

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
            sync_back(keys=["default_copilot_model"], git_root=tmp_path)

        written = json.loads(config_path.read_text())
        assert written["default_copilot_model"] == "new-model"
        assert written["jira_base_url"] == "http://jira"

    def test_deterministic_key_ordering(self, tmp_path: Path) -> None:
        """Written file has sorted keys."""
        config_path = tmp_path / ".agdt" / "config" / "project.json"
        config_path.parent.mkdir(parents=True)
        config_path.write_text(json.dumps({"z_key": "z", "a_key": "a"}, indent=2))

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
            sync_back(keys=["default_copilot_model"], git_root=tmp_path)

        written_text = config_path.read_text()
        keys = list(json.loads(written_text).keys())
        assert keys == sorted(keys)


class TestSyncBackSkipping:
    """Tests for skipping behavior."""

    def test_skips_absent_source_state_key(self, tmp_path: Path) -> None:
        """Skips keys whose source state value is absent."""
        config_path = tmp_path / ".agdt" / "config" / "project.json"
        config_path.parent.mkdir(parents=True)
        config_path.write_text(json.dumps({"default_copilot_model": "old"}, indent=2))

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
            result = sync_back(keys=["default_copilot_model"], git_root=tmp_path)

        assert len(result["skipped_keys"]) == 1
        assert "not set" in result["skipped_keys"][0]["reason"]
        assert not result["errors"]

    def test_all_eligible_no_diff_exits_cleanly(self, tmp_path: Path) -> None:
        """All-eligible with no diff exits cleanly."""
        config_path = tmp_path / ".agdt" / "config" / "project.json"
        config_path.parent.mkdir(parents=True)
        config_path.write_text(json.dumps({"default_copilot_model": "same-model"}, indent=2))

        def mock_get_value(key, required=False):
            assert required is False
            if key == "copilot.model_id":
                return "same-model"
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
            result = sync_back(all_eligible=True, git_root=tmp_path)

        assert not result["errors"]
        assert any("No changes" in w or "No values were synced" in w for w in result["warnings"])

    def test_all_eligible_with_only_missing_state_reports_missing_values_message(
        self,
        tmp_path: Path,
    ) -> None:
        """All-eligible missing-state no-op reports the missing-values summary."""
        config_path = tmp_path / ".agdt" / "config" / "project.json"
        config_path.parent.mkdir(parents=True)
        config_path.write_text("{}", encoding="utf-8")

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
            result = sync_back(all_eligible=True, git_root=tmp_path)

        assert (
            "No values were synced — no sync-eligible source values are set in the current worktree state"
        ) in result["warnings"]

    def test_skips_matching_value_in_specific_keys_mode(self, tmp_path: Path) -> None:
        """When specific keys are given and value already matches, skips it."""
        config_path = tmp_path / ".agdt" / "config" / "project.json"
        config_path.parent.mkdir(parents=True)
        config_path.write_text(json.dumps({"default_copilot_model": "same-model"}, indent=2))

        with (
            patch(
                f"{_PC_MOD}._get_config_path",
                return_value=config_path,
            ),
            patch(
                f"{_STATE_MOD}.get_value",
                return_value="same-model",
            ),
        ):
            result = sync_back(keys=["default_copilot_model"], git_root=tmp_path)

        assert len(result["skipped_keys"]) == 1
        assert "already matches" in result["skipped_keys"][0]["reason"]

    def test_specific_keys_no_diff_reports_requested_values_message(self, tmp_path: Path) -> None:
        """Specific-key no-op message refers only to the requested values."""
        config_path = tmp_path / ".agdt" / "config" / "project.json"
        config_path.parent.mkdir(parents=True)
        config_path.write_text(json.dumps({"default_copilot_model": "same-model"}, indent=2))

        with (
            patch(
                f"{_PC_MOD}._get_config_path",
                return_value=config_path,
            ),
            patch(
                f"{_STATE_MOD}.get_value",
                return_value="same-model",
            ),
        ):
            result = sync_back(keys=["default_copilot_model"], git_root=tmp_path)

        assert "No changes to sync — all requested values already match project.json" in result["warnings"]

    def test_specific_keys_mixed_skips_report_mixed_no_op_message(self, tmp_path: Path) -> None:
        """Mixed matching and missing-state no-op results use a mixed summary message."""
        config_path = tmp_path / ".agdt" / "config" / "project.json"
        config_path.parent.mkdir(parents=True)
        config_path.write_text(json.dumps({"default_copilot_model": "same-model"}, indent=2))

        def mock_get_value(key, **kwargs):
            if key == "copilot.model_id":
                return "same-model"
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
            result = sync_back(
                keys=["default_copilot_model", "jira_base_url"],
                git_root=tmp_path,
            )

        assert (
            "No changes to sync — requested values already match project.json or were "
            "skipped because source values are not set in state"
        ) in result["warnings"]


class TestSyncBackNoKeysOrAllEligible:
    """Tests for when neither keys nor all_eligible is provided."""

    def test_returns_error_when_neither_specified(self, tmp_path: Path) -> None:
        """Returns error when neither keys nor all_eligible is set."""
        result = sync_back(keys=None, all_eligible=False, git_root=tmp_path)

        assert result["errors"]
        assert "Must specify" in result["errors"][0]


class TestSyncBackConfigPathNone:
    """Tests for when _get_config_path returns None."""

    def test_raises_runtime_error_when_git_root_unresolvable(self, tmp_path: Path) -> None:
        """Raises RuntimeError when git root cannot be determined."""
        with (
            patch(
                f"{_PC_MOD}._get_config_path",
                return_value=None,
            ),
            pytest.raises(RuntimeError, match="Cannot determine git repository root"),
        ):
            sync_back(keys=["default_copilot_model"], git_root=tmp_path)


class TestSyncBackValidationFailure:
    """Tests for value validation failure."""

    def test_returns_error_on_validation_failure(self, tmp_path: Path) -> None:
        """Validation failure on a value produces an error."""
        config_path = tmp_path / ".agdt" / "config" / "project.json"
        config_path.parent.mkdir(parents=True)
        config_path.write_text(json.dumps({"default_copilot_model": "old"}, indent=2))

        with (
            patch(
                f"{_PC_MOD}._get_config_path",
                return_value=config_path,
            ),
            patch(
                f"{_STATE_MOD}.get_value",
                return_value="",  # Empty string fails _validate_string
            ),
        ):
            result = sync_back(keys=["default_copilot_model"], git_root=tmp_path)

        assert result["errors"]
        assert "Validation failed" in result["errors"][0]


class TestSyncBackErrorsAfterChanges:
    """Tests for errors accumulated after some changes have been staged."""

    def test_returns_errors_when_cross_field_validation_fails(self, tmp_path: Path) -> None:
        """Cross-field validation errors prevent writing."""
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
                return "chore"  # Not in availableCommitIssueTypes
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
            result = sync_back(keys=["defaultCommitIssueType"], git_root=tmp_path)

        assert result["errors"]
        assert "Cross-field" in result["errors"][0]


class TestSyncBackIneligibleKey:
    """Tests for ineligible key rejection."""

    def test_rejects_ineligible_key(self, tmp_path: Path) -> None:
        """Rejects keys not in SYNC_ELIGIBLE_KEYS."""
        config_path = tmp_path / ".agdt" / "config" / "project.json"
        config_path.parent.mkdir(parents=True)
        config_path.write_text("{}")

        with patch(
            f"{_PC_MOD}._get_config_path",
            return_value=config_path,
        ):
            result = sync_back(keys=["not_a_real_key"], git_root=tmp_path)

        assert result["errors"]
        assert "not sync-eligible" in result["errors"][0]


class TestSyncBackMalformedJson:
    """Tests for malformed project.json handling."""

    def test_raises_on_malformed_json(self, tmp_path: Path) -> None:
        """Raises ValueError on malformed JSON."""
        config_path = tmp_path / ".agdt" / "config" / "project.json"
        config_path.parent.mkdir(parents=True)
        config_path.write_text("{ invalid json }")

        with (
            patch(
                f"{_PC_MOD}._get_config_path",
                return_value=config_path,
            ),
            pytest.raises(ValueError, match="Malformed JSON"),
        ):
            sync_back(keys=["default_copilot_model"], git_root=tmp_path)

    def test_raises_on_non_object_json(self, tmp_path: Path) -> None:
        """Raises ValueError when JSON is not an object."""
        config_path = tmp_path / ".agdt" / "config" / "project.json"
        config_path.parent.mkdir(parents=True)
        config_path.write_text('"just a string"')

        with (
            patch(
                f"{_PC_MOD}._get_config_path",
                return_value=config_path,
            ),
            pytest.raises(ValueError, match="Expected JSON object"),
        ):
            sync_back(keys=["default_copilot_model"], git_root=tmp_path)

    def test_raises_on_unreadable_json_file(self, tmp_path: Path) -> None:
        """Raises ValueError when project.json cannot be read."""
        config_path = tmp_path / ".agdt" / "config" / "project.json"
        config_path.parent.mkdir(parents=True)
        config_path.write_text("{}")

        with (
            patch(
                f"{_PC_MOD}._get_config_path",
                return_value=config_path,
            ),
            patch.object(
                Path,
                "read_text",
                side_effect=OSError("permission denied"),
            ),
            pytest.raises(ValueError, match="Could not read"),
        ):
            sync_back(keys=["default_copilot_model"], git_root=tmp_path)

    def test_raises_on_non_utf8_json_file(self, tmp_path: Path) -> None:
        """Raises ValueError when project.json is not valid UTF-8."""
        config_path = tmp_path / ".agdt" / "config" / "project.json"
        config_path.parent.mkdir(parents=True)
        config_path.write_bytes(b"\x80\x81")

        with (
            patch(
                f"{_PC_MOD}._get_config_path",
                return_value=config_path,
            ),
            pytest.raises(ValueError, match="Could not read"),
        ):
            sync_back(keys=["default_copilot_model"], git_root=tmp_path)


class TestSyncBackFileLocking:
    """Tests for file locking during sync-back."""

    def test_uses_locked_file(self, tmp_path: Path) -> None:
        """sync_back uses locked_file for writing."""
        config_path = tmp_path / ".agdt" / "config" / "project.json"
        config_path.parent.mkdir(parents=True)
        config_path.write_text(json.dumps({"default_copilot_model": "old"}, indent=2))

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
            result = sync_back(keys=["default_copilot_model"], git_root=tmp_path)

        assert not result["errors"]
        written = json.loads(config_path.read_text())
        assert written["default_copilot_model"] == "new-model"

    def test_handles_empty_file_under_lock(self, tmp_path: Path) -> None:
        """Empty file under lock falls back to pre-lock snapshot, preserving existing keys."""
        config_path = tmp_path / ".agdt" / "config" / "project.json"
        config_path.parent.mkdir(parents=True)
        config_path.write_text(json.dumps({"default_copilot_model": "old", "jira_base_url": "http://jira"}, indent=2))

        captured_buffers: list[io.StringIO] = []

        @contextmanager
        def fake_locked_file(path, mode="r+", exclusive=True):
            """Simulate a locked file that returns empty content on read."""
            buf = io.StringIO()
            yield buf
            captured_buffers.append(buf)

        with (
            patch(
                f"{_PC_MOD}._get_config_path",
                return_value=config_path,
            ),
            patch(
                f"{_STATE_MOD}.get_value",
                return_value="new-model",
            ),
            patch(
                "agentic_devtools.file_locking.locked_file",
                side_effect=fake_locked_file,
            ),
        ):
            result = sync_back(keys=["default_copilot_model"], git_root=tmp_path)

        assert not result["errors"]
        assert len(result["synced_keys"]) == 1
        # Verify pre-lock snapshot keys are preserved (no data loss)
        written = json.loads(captured_buffers[0].getvalue())
        assert written["jira_base_url"] == "http://jira"
        assert written["default_copilot_model"] == "new-model"

    def test_falls_back_to_existing_config_on_corrupted_json_under_lock(self, tmp_path: Path) -> None:
        """Falls back to pre-lock snapshot when JSON under lock is corrupted."""
        config_path = tmp_path / ".agdt" / "config" / "project.json"
        config_path.parent.mkdir(parents=True)
        config_path.write_text(json.dumps({"default_copilot_model": "old", "jira_base_url": "http://jira"}, indent=2))

        @contextmanager
        def fake_locked_file_corrupted(path, mode="r+", exclusive=True):
            """Simulate a locked file that returns corrupted JSON."""
            buf = io.StringIO()
            buf.write("{ bad json !!!")
            buf.seek(0)
            yield buf

        with (
            patch(
                f"{_PC_MOD}._get_config_path",
                return_value=config_path,
            ),
            patch(
                f"{_STATE_MOD}.get_value",
                return_value="new-model",
            ),
            patch(
                "agentic_devtools.file_locking.locked_file",
                side_effect=fake_locked_file_corrupted,
            ),
        ):
            result = sync_back(keys=["default_copilot_model"], git_root=tmp_path)

        # Should succeed using the pre-lock parsed existing_config as fallback
        assert not result["errors"]
        assert len(result["synced_keys"]) == 1

    def test_falls_back_to_existing_config_on_non_object_json_under_lock(self, tmp_path: Path) -> None:
        """Falls back to pre-lock snapshot when JSON under lock is not an object."""
        config_path = tmp_path / ".agdt" / "config" / "project.json"
        config_path.parent.mkdir(parents=True)
        config_path.write_text(json.dumps({"default_copilot_model": "old"}, indent=2))

        @contextmanager
        def fake_locked_file_array(path, mode="r+", exclusive=True):
            """Simulate a locked file that returns a JSON array (non-object)."""
            buf = io.StringIO()
            buf.write("[1, 2, 3]")
            buf.seek(0)
            yield buf

        with (
            patch(
                f"{_PC_MOD}._get_config_path",
                return_value=config_path,
            ),
            patch(
                f"{_STATE_MOD}.get_value",
                return_value="new-model",
            ),
            patch(
                "agentic_devtools.file_locking.locked_file",
                side_effect=fake_locked_file_array,
            ),
        ):
            result = sync_back(keys=["default_copilot_model"], git_root=tmp_path)

        # Should succeed using the pre-lock parsed existing_config as fallback
        assert not result["errors"]
        assert len(result["synced_keys"]) == 1

    def test_revalidates_cross_field_invariants_after_locked_read(self, tmp_path: Path) -> None:
        """Re-validates cross-field invariants on locked snapshot before writing."""
        config_path = tmp_path / ".agdt" / "config" / "project.json"
        config_path.parent.mkdir(parents=True)
        config_path.write_text(
            json.dumps(
                {
                    "availableCommitIssueTypes": ["feat", "fix", "chore"],
                    "defaultCommitIssueType": "feat",
                },
                indent=2,
            )
        )

        captured_buffers: list[io.StringIO] = []

        @contextmanager
        def fake_locked_file_changed(path, mode="r+", exclusive=True):
            """Simulate concurrent change that removes the soon-to-be default from available list."""
            buf = io.StringIO()
            buf.write(
                json.dumps(
                    {
                        "availableCommitIssueTypes": ["feat", "fix"],
                        "defaultCommitIssueType": "feat",
                    }
                )
            )
            buf.seek(0)
            yield buf
            captured_buffers.append(buf)

        def mock_get_value(key, **kwargs):
            if key == "versionControl.commitMessageType":
                return "chore"
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
            patch(
                "agentic_devtools.file_locking.locked_file",
                side_effect=fake_locked_file_changed,
            ),
        ):
            result = sync_back(keys=["defaultCommitIssueType"], git_root=tmp_path)

        assert result["errors"]
        assert "Cross-field validation error" in result["errors"][0]
        # No write should occur when lock-time validation fails.
        assert json.loads(captured_buffers[0].getvalue()) == {
            "availableCommitIssueTypes": ["feat", "fix"],
            "defaultCommitIssueType": "feat",
        }
        assert json.loads(config_path.read_text()) == {
            "availableCommitIssueTypes": ["feat", "fix", "chore"],
            "defaultCommitIssueType": "feat",
        }


class TestSyncBackGitignoreNegations:
    """Tests for gitignore negation invocation."""

    def test_calls_ensure_negations_when_file_absent(self, tmp_path: Path) -> None:
        """ensure_root_gitignore_negations is called when project.json is new."""
        config_path = tmp_path / ".agdt" / "config" / "project.json"
        # Do NOT create config_path — simulate absent project.json
        config_path.parent.mkdir(parents=True, exist_ok=True)

        with (
            patch(
                f"{_PC_MOD}._get_config_path",
                return_value=config_path,
            ),
            patch(
                f"{_STATE_MOD}.get_value",
                return_value="new-model",
            ),
            patch(
                "agentic_devtools.cli.setup.gitignore_negations.ensure_root_gitignore_negations",
            ) as mock_negations,
            patch(
                "agentic_devtools.state._get_git_repo_root",
                return_value=tmp_path,
            ),
        ):
            result = sync_back(keys=["default_copilot_model"], git_root=tmp_path)

        assert not result["errors"]
        mock_negations.assert_called_once_with(tmp_path)

    def test_does_not_write_placeholder_before_lock_when_file_absent(self, tmp_path: Path) -> None:
        """Avoids an unlocked placeholder write before the locked update path."""
        config_path = tmp_path / ".agdt" / "config" / "project.json"
        config_path.parent.mkdir(parents=True, exist_ok=True)

        @contextmanager
        def fake_locked_file(path, mode="r+", exclusive=True):
            """Simulate concurrent creation of project.json before lock acquisition."""
            assert path == config_path
            assert not path.exists()
            with open(path, "w", encoding="utf-8") as seed:
                json.dump(
                    {
                        "default_copilot_model": "concurrent-model",
                        "jira_base_url": "http://jira.example",
                    },
                    seed,
                )
            with open(path, mode, encoding="utf-8") as handle:
                yield handle

        with (
            patch(
                f"{_PC_MOD}._get_config_path",
                return_value=config_path,
            ),
            patch(
                f"{_STATE_MOD}.get_value",
                return_value="new-model",
            ),
            patch.object(Path, "write_text", autospec=True) as mock_write_text,
            patch(
                "agentic_devtools.file_locking.locked_file",
                side_effect=fake_locked_file,
            ),
            patch(
                "agentic_devtools.cli.setup.gitignore_negations.ensure_root_gitignore_negations",
            ),
            patch(
                "agentic_devtools.state._get_git_repo_root",
                return_value=tmp_path,
            ),
        ):
            result = sync_back(keys=["default_copilot_model"], git_root=tmp_path)

        assert not result["errors"]
        mock_write_text.assert_not_called()
        assert config_path.exists()
        written = json.loads(config_path.read_text())
        assert written == {
            "default_copilot_model": "new-model",
            "jira_base_url": "http://jira.example",
        }

    def test_warns_on_gitignore_negation_failure(self, tmp_path: Path) -> None:
        """Warns when ensure_root_gitignore_negations raises."""
        config_path = tmp_path / ".agdt" / "config" / "project.json"
        config_path.parent.mkdir(parents=True, exist_ok=True)

        with (
            patch(
                f"{_PC_MOD}._get_config_path",
                return_value=config_path,
            ),
            patch(
                f"{_STATE_MOD}.get_value",
                return_value="new-model",
            ),
            patch(
                "agentic_devtools.cli.setup.gitignore_negations.ensure_root_gitignore_negations",
                side_effect=OSError("permission denied"),
            ),
            patch(
                "agentic_devtools.state._get_git_repo_root",
                return_value=tmp_path,
            ),
        ):
            result = sync_back(keys=["default_copilot_model"], git_root=tmp_path)

        assert not result["errors"]
        assert any("Could not update .gitignore" in w for w in result["warnings"])

    def test_skips_gitignore_negation_when_root_unresolvable(self, tmp_path: Path) -> None:
        """Skips gitignore negations silently when git root cannot be resolved."""
        config_path = tmp_path / ".agdt" / "config" / "project.json"
        config_path.parent.mkdir(parents=True, exist_ok=True)

        with (
            patch(
                f"{_PC_MOD}._get_config_path",
                return_value=config_path,
            ),
            patch(
                f"{_STATE_MOD}.get_value",
                return_value="new-model",
            ),
            patch(
                "agentic_devtools.cli.setup.gitignore_negations.ensure_root_gitignore_negations",
            ) as mock_negations,
            patch(
                "agentic_devtools.state._get_git_repo_root",
                return_value=None,
            ),
        ):
            result = sync_back(keys=["default_copilot_model"])

        assert not result["errors"]
        mock_negations.assert_not_called()
