"""Tests for agentic_devtools.cli.jira.sdk.is_cloud."""

from __future__ import annotations

from agentic_devtools.cli.jira.sdk import is_cloud


class TestIsCloud:
    """is_cloud() deployment type detection."""

    def test_cloud_returns_true(self) -> None:
        """Returns True for deploymentType 'Cloud'."""
        assert is_cloud({"deploymentType": "Cloud"}) is True

    def test_server_returns_false(self) -> None:
        """Returns False for deploymentType 'Server'."""
        assert is_cloud({"deploymentType": "Server"}) is False

    def test_data_center_returns_false(self) -> None:
        """Returns False for deploymentType 'DataCenter'."""
        assert is_cloud({"deploymentType": "DataCenter"}) is False

    def test_missing_key_returns_false(self) -> None:
        """Returns False when deploymentType key is missing."""
        assert is_cloud({}) is False

    def test_wrong_case_returns_false(self) -> None:
        """Returns False for lowercase 'cloud' (case-sensitive)."""
        assert is_cloud({"deploymentType": "cloud"}) is False
