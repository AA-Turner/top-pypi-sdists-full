"""Tests for _build_jira_config."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.orchestration.nodes._issue_retrieval import _build_jira_config


class TestBuildJiraConfig:
    """Tests for _build_jira_config helper."""

    def test_raises_on_import_error(self) -> None:
        with patch(
            "agentic_devtools.cli.jira.config.get_jira_base_url",
            side_effect=ImportError("no requests module"),
        ):
            with pytest.raises(ValueError, match="Failed to construct Jira configuration"):
                _build_jira_config()

    def test_raises_on_value_error(self) -> None:
        with patch(
            "agentic_devtools.cli.jira.config.get_jira_base_url",
            side_effect=ValueError("JIRA_BASE_URL not set"),
        ):
            with pytest.raises(ValueError, match="Failed to construct Jira configuration"):
                _build_jira_config()

    def test_success(self) -> None:
        with (
            patch("agentic_devtools.cli.jira.config.get_jira_base_url", return_value="https://jira.example.com"),
            patch("agentic_devtools.cli.jira.config.get_jira_headers", return_value={"Authorization": "Basic x"}),
            patch("agentic_devtools.cli.jira.helpers._get_ssl_verify", return_value=True),
            patch("agentic_devtools.cli.jira.helpers._get_requests", return_value=MagicMock()),
        ):
            config = _build_jira_config()
            assert config.base_url == "https://jira.example.com"
