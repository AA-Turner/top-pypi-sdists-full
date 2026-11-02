"""Tests for cross-field validation in sync_back."""

import json
from pathlib import Path
from unittest.mock import patch

from agentic_devtools.cli.config.sync_back import sync_back

_PC_MOD = "agentic_devtools.cli.config.project_config"
_STATE_MOD = "agentic_devtools.state"


class TestCrossFieldValidation:
    """Tests for cross-field validation in sync_back."""

    def test_rejects_default_type_not_in_available(self, tmp_path: Path) -> None:
        """Rejects when defaultCommitIssueType is not in availableCommitIssueTypes."""
        config_path = tmp_path / ".agdt" / "config" / "project.json"
        config_path.parent.mkdir(parents=True)
        config_path.write_text(
            json.dumps(
                {
                    "availableCommitIssueTypes": ["feat", "fix"],
                    "defaultCommitIssueType": "feat",
                },
                indent=2,
            )
        )

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
        ):
            result = sync_back(keys=["defaultCommitIssueType"], git_root=tmp_path)

        assert result["errors"]
        assert "must appear in" in result["errors"][0]

    def test_unrelated_key_not_blocked_by_preexisting_violation(self, tmp_path: Path) -> None:
        """Syncing an unrelated key is not blocked by a pre-existing cross-field violation."""
        config_path = tmp_path / ".agdt" / "config" / "project.json"
        config_path.parent.mkdir(parents=True, exist_ok=True)
        # project.json already has an invalid commit-type config, but we are syncing vpn_url.
        config_path.write_text(
            json.dumps(
                {
                    "availableCommitIssueTypes": ["feat", "fix"],
                    "defaultCommitIssueType": "chore",  # violates invariant
                    "vpn_url": "https://old.vpn.example.com",
                },
                indent=2,
            )
        )

        def mock_get_value(key, **kwargs):
            if key == "vpn_url":
                return "https://new.vpn.example.com"
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
            result = sync_back(keys=["vpn_url"], git_root=tmp_path, dry_run=True)

        # The pre-existing commit-type violation must NOT block the unrelated vpn_url sync.
        assert not result["errors"]
        assert len(result["synced_keys"]) == 1
        assert result["synced_keys"][0]["key"] == "vpn_url"

    def test_accepts_valid_cross_field(self, tmp_path: Path) -> None:
        """Accepts when defaultCommitIssueType is in availableCommitIssueTypes."""
        config_path = tmp_path / ".agdt" / "config" / "project.json"
        config_path.parent.mkdir(parents=True, exist_ok=True)
        config_path.write_text(
            json.dumps(
                {
                    "availableCommitIssueTypes": ["feat", "fix", "chore"],
                    "defaultCommitIssueType": "feat",
                },
                indent=2,
            )
        )

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
        ):
            result = sync_back(keys=["defaultCommitIssueType"], git_root=tmp_path)

        assert not result["errors"]
        assert len(result["synced_keys"]) == 1

    def test_accepts_default_type_matching_stripped_available_entry(self, tmp_path: Path) -> None:
        """Accepts when defaultCommitIssueType matches an available entry after stripping."""
        config_path = tmp_path / ".agdt" / "config" / "project.json"
        config_path.parent.mkdir(parents=True, exist_ok=True)
        # " fix" has a leading space — the runtime consumer strips it, so "fix" is valid.
        config_path.write_text(
            json.dumps(
                {
                    "availableCommitIssueTypes": ["feat", " fix"],
                    "defaultCommitIssueType": "feat",
                },
                indent=2,
            )
        )

        def mock_get_value(key, **kwargs):
            if key == "versionControl.commitMessageType":
                return "fix"
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

        # "fix" matches " fix" after normalization — must not raise a cross-field error.
        assert not result["errors"]

    def test_accepts_default_type_with_surrounding_whitespace(self, tmp_path: Path) -> None:
        """Accepts when defaultCommitIssueType itself has surrounding whitespace."""
        config_path = tmp_path / ".agdt" / "config" / "project.json"
        config_path.parent.mkdir(parents=True, exist_ok=True)
        config_path.write_text(
            json.dumps(
                {
                    "availableCommitIssueTypes": ["feat", "fix"],
                    "defaultCommitIssueType": "feat",
                },
                indent=2,
            )
        )

        def mock_get_value(key, **kwargs):
            if key == "versionControl.commitMessageType":
                return " fix "
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

        # " fix " strips to "fix", which is in the list — no cross-field error.
        assert not result["errors"]

    def test_ignores_non_string_elements_in_available_types(self, tmp_path: Path) -> None:
        """Non-string elements already in project.json availableCommitIssueTypes are ignored."""
        config_path = tmp_path / ".agdt" / "config" / "project.json"
        config_path.parent.mkdir(parents=True, exist_ok=True)
        # project.json has a pre-existing malformed list (non-string element at index 1).
        # The runtime consumer ignores non-strings, so "fix" is still a valid default.
        config_path.write_text(
            json.dumps(
                {
                    "availableCommitIssueTypes": ["feat", 42, "fix"],
                    "defaultCommitIssueType": "feat",
                },
                indent=2,
            )
        )

        def mock_get_value(key, **kwargs):
            if key == "versionControl.commitMessageType":
                return "fix"
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
            # Sync only defaultCommitIssueType; the merged availableCommitIssueTypes
            # comes from the existing (malformed) project.json.
            result = sync_back(keys=["defaultCommitIssueType"], git_root=tmp_path)

        # "fix" is in the list (ignoring the non-string 42) — no cross-field error.
        assert not result["errors"]

    def test_skips_type_check_when_default_type_is_non_string(self, tmp_path: Path) -> None:
        """No cross-field error when defaultCommitIssueType is a non-string in project.json.

        Covers the False branch of ``isinstance(default_type, str) and isinstance(available_types, list)``
        (line 38) — when both keys are present but one has an unexpected type the validator
        silently skips the cross-field check rather than crashing.
        """
        config_path = tmp_path / ".agdt" / "config" / "project.json"
        config_path.parent.mkdir(parents=True, exist_ok=True)
        # project.json has a malformed defaultCommitIssueType (integer, not string).
        # Syncing availableCommitIssueTypes still merges both keys, but the isinstance
        # guard at line 38 evaluates to False and the check is skipped safely.
        config_path.write_text(
            json.dumps(
                {
                    "availableCommitIssueTypes": ["feat", "fix"],
                    "defaultCommitIssueType": 99,  # non-string — triggers 38->55
                },
                indent=2,
            )
        )

        def mock_get_value(key, **kwargs):
            if key == "versionControl.availableCommitIssueTypes":
                return ["feat", "fix", "chore"]
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
            result = sync_back(keys=["availableCommitIssueTypes"], git_root=tmp_path, dry_run=True)

        # Type mismatch in existing project.json must not raise — sync proceeds.
        assert not result["errors"]
        assert len(result["synced_keys"]) == 1

    def test_skips_cross_field_check_when_only_one_commit_key_in_merged(self, tmp_path: Path) -> None:
        """No cross-field error when only one commit-type key exists in merged config."""
        config_path = tmp_path / ".agdt" / "config" / "project.json"
        config_path.parent.mkdir(parents=True, exist_ok=True)
        # Only availableCommitIssueTypes is present — defaultCommitIssueType is absent,
        # so the inner "both keys present" guard evaluates to False (branch 35->45).
        config_path.write_text(
            json.dumps(
                {"availableCommitIssueTypes": ["feat", "fix"]},
                indent=2,
            )
        )

        def mock_get_value(key, **kwargs):
            if key == "versionControl.availableCommitIssueTypes":
                return ["feat", "fix", "chore"]
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
            result = sync_back(keys=["availableCommitIssueTypes"], git_root=tmp_path, dry_run=True)

        assert not result["errors"]
        assert len(result["synced_keys"]) == 1
