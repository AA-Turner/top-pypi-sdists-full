"""Tests for agentic_devtools.cli.jira.discovery._schema_has_required_keys."""

from agentic_devtools.cli.jira.discovery import _schema_has_required_keys


class TestSchemaHasRequiredKeys:
    """Tests for _schema_has_required_keys."""

    def test_all_keys_present_returns_true(self) -> None:
        """Returns True when all 6 required keys are present."""
        data = {
            "version": "9.12.0",
            "versionNumbers": [9, 12, 0],
            "deploymentType": "Server",
            "buildNumber": "912000",
            "baseUrl": "https://jira.example.com",
            "discoveredUtc": "2024-01-01T00:00:00+00:00",
        }
        assert _schema_has_required_keys(data) is True

    def test_missing_key_returns_false(self) -> None:
        """Returns False when a required key is missing."""
        data = {
            "version": "9.12.0",
            "versionNumbers": [9, 12, 0],
            "deploymentType": "Server",
            "baseUrl": "https://jira.example.com",
            "discoveredUtc": "2024-01-01T00:00:00+00:00",
            # buildNumber missing
        }
        assert _schema_has_required_keys(data) is False

    def test_none_valued_build_number_is_valid(self) -> None:
        """A key present with None value is valid (buildNumber can be None)."""
        data = {
            "version": "9.12.0",
            "versionNumbers": [9, 12, 0],
            "deploymentType": "Server",
            "buildNumber": None,
            "baseUrl": "https://jira.example.com",
            "discoveredUtc": "2024-01-01T00:00:00+00:00",
        }
        assert _schema_has_required_keys(data) is True

    def test_empty_dict_returns_false(self) -> None:
        """Returns False for an empty dict."""
        assert _schema_has_required_keys({}) is False
