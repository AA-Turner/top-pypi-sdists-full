"""Tests for agentic_devtools.cli.setup.platform_detection._jira_adapter_marker_is_authoritative."""

from agentic_devtools.cli.setup.platform_detection import _jira_adapter_marker_is_authoritative


class TestJiraAdapterMarkerIsAuthoritative:
    """Unit tests for the migration-compatible marker authority helper."""

    def test_true_marker_is_authoritative(self):
        """Boolean True → authoritative."""
        assert _jira_adapter_marker_is_authoritative({"issue_adapter_resolved": True}) is True

    def test_false_marker_is_not_authoritative(self):
        """Boolean False → non-authoritative."""
        assert _jira_adapter_marker_is_authoritative({"issue_adapter_resolved": False}) is False

    def test_absent_marker_is_authoritative(self):
        """Absent marker (legacy pre-PR config) → authoritative for migration compatibility."""
        assert _jira_adapter_marker_is_authoritative({}) is True

    def test_absent_marker_with_other_keys_is_authoritative(self):
        """Absent marker alongside other keys is still authoritative."""
        assert _jira_adapter_marker_is_authoritative({"issue_adapter": "jira"}) is True

    def test_null_marker_is_not_authoritative(self):
        """Present-but-null marker (JSON null → Python None) is non-authoritative."""
        assert _jira_adapter_marker_is_authoritative({"issue_adapter_resolved": None}) is False

    def test_string_false_marker_is_not_authoritative(self):
        """Present string "false" marker is non-authoritative (not a valid boolean)."""
        assert _jira_adapter_marker_is_authoritative({"issue_adapter_resolved": "false"}) is False

    def test_string_true_marker_is_not_authoritative(self):
        """Present string "true" marker is non-authoritative (not a valid boolean)."""
        assert _jira_adapter_marker_is_authoritative({"issue_adapter_resolved": "true"}) is False

    def test_integer_one_marker_is_not_authoritative(self):
        """Present integer 1 marker is non-authoritative (isinstance(1, bool) is False)."""
        assert _jira_adapter_marker_is_authoritative({"issue_adapter_resolved": 1}) is False

    def test_integer_zero_marker_is_not_authoritative(self):
        """Present integer 0 marker is non-authoritative."""
        assert _jira_adapter_marker_is_authoritative({"issue_adapter_resolved": 0}) is False
