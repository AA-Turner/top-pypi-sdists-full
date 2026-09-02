"""Tests for SYNC_ELIGIBLE_KEYS constant structure."""

from agentic_devtools.cli.config.project_config import SYNC_ELIGIBLE_KEYS


class TestSyncEligibleKeys:
    """Tests for the SYNC_ELIGIBLE_KEYS constant."""

    def test_is_dict(self) -> None:
        """SYNC_ELIGIBLE_KEYS is a dictionary."""
        assert isinstance(SYNC_ELIGIBLE_KEYS, dict)

    def test_has_expected_keys(self) -> None:
        """Contains all expected project.json keys."""
        expected = {
            "default_copilot_model",
            "defaultCommitIssueType",
            "availableCommitIssueTypes",
            "jira_project_keys",
            "jira_base_url",
            "corporate_network_test_host",
            "vpn_hostnames",
            "vpn_url",
        }
        assert set(SYNC_ELIGIBLE_KEYS.keys()) == expected

    def test_each_entry_has_state_key(self) -> None:
        """Every entry has a 'state_key' string."""
        for key, entry in SYNC_ELIGIBLE_KEYS.items():
            assert "state_key" in entry, f"Missing state_key in {key}"
            assert isinstance(entry["state_key"], str), f"state_key not str in {key}"

    def test_each_entry_has_validator(self) -> None:
        """Every entry has a 'validator' callable."""
        for key, entry in SYNC_ELIGIBLE_KEYS.items():
            assert "validator" in entry, f"Missing validator in {key}"
            assert callable(entry["validator"]), f"validator not callable in {key}"

    def test_string_validator_accepts_valid(self) -> None:
        """String validator accepts non-empty string."""
        validator = SYNC_ELIGIBLE_KEYS["default_copilot_model"]["validator"]
        assert validator("gpt-4o") is None

    def test_string_validator_rejects_empty(self) -> None:
        """String validator rejects empty string."""
        validator = SYNC_ELIGIBLE_KEYS["default_copilot_model"]["validator"]
        assert validator("") is not None

    def test_string_validator_rejects_non_string(self) -> None:
        """String validator rejects non-string."""
        validator = SYNC_ELIGIBLE_KEYS["default_copilot_model"]["validator"]
        assert validator(123) is not None

    def test_list_validator_accepts_valid(self) -> None:
        """List validator accepts non-empty list of strings."""
        validator = SYNC_ELIGIBLE_KEYS["availableCommitIssueTypes"]["validator"]
        assert validator(["feat", "fix", "chore"]) is None

    def test_list_validator_rejects_empty_list(self) -> None:
        """List validator rejects empty list."""
        validator = SYNC_ELIGIBLE_KEYS["availableCommitIssueTypes"]["validator"]
        assert validator([]) is not None

    def test_list_validator_rejects_non_list(self) -> None:
        """List validator rejects non-list."""
        validator = SYNC_ELIGIBLE_KEYS["availableCommitIssueTypes"]["validator"]
        assert validator("feat,fix") is not None

    def test_list_validator_rejects_empty_string_element(self) -> None:
        """List validator rejects list with empty string element."""
        validator = SYNC_ELIGIBLE_KEYS["availableCommitIssueTypes"]["validator"]
        result = validator(["feat", "", "chore"])
        assert result is not None
        assert "index 1" in result

    def test_list_validator_rejects_non_string_element(self) -> None:
        """List validator rejects list with non-string element."""
        validator = SYNC_ELIGIBLE_KEYS["availableCommitIssueTypes"]["validator"]
        result = validator(["feat", 123, "chore"])
        assert result is not None
        assert "index 1" in result

    def test_comma_string_validator_accepts_valid(self) -> None:
        """Comma-string validator accepts non-empty comma-separated string."""
        validator = SYNC_ELIGIBLE_KEYS["jira_project_keys"]["validator"]
        assert validator("PROJ1,PROJ2") is None

    def test_comma_string_validator_rejects_empty(self) -> None:
        """Comma-string validator rejects empty string."""
        validator = SYNC_ELIGIBLE_KEYS["jira_project_keys"]["validator"]
        assert validator("") is not None

    def test_comma_string_validator_rejects_whitespace(self) -> None:
        """Comma-string validator rejects whitespace-only string."""
        validator = SYNC_ELIGIBLE_KEYS["jira_project_keys"]["validator"]
        assert validator("   ") is not None

    def test_comma_string_validator_rejects_non_string(self) -> None:
        """Comma-string validator rejects non-string."""
        validator = SYNC_ELIGIBLE_KEYS["jira_project_keys"]["validator"]
        assert validator(123) is not None

    def test_comma_string_validator_rejects_only_commas(self) -> None:
        """Comma-string validator rejects strings with no actual items."""
        validator = SYNC_ELIGIBLE_KEYS["jira_project_keys"]["validator"]
        assert validator(",,,") is not None

    def test_comma_string_validator_rejects_only_whitespace_items(self) -> None:
        """Comma-string validator rejects comma lists with only whitespace items."""
        validator = SYNC_ELIGIBLE_KEYS["jira_project_keys"]["validator"]
        assert validator(" , ") is not None

    def test_vpn_url_uses_string_validator(self) -> None:
        """vpn_url entry uses the string validator."""
        validator = SYNC_ELIGIBLE_KEYS["vpn_url"]["validator"]
        assert validator("https://vpn.example.com") is None
        assert validator("") is not None
