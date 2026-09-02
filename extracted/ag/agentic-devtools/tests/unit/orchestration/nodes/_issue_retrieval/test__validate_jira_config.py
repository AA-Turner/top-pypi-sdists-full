"""Tests for _validate_jira_config."""

from __future__ import annotations

import pytest

from agentic_devtools.orchestration.nodes._issue_retrieval import _validate_jira_config


class TestValidateJiraConfig:
    """Tests for _validate_jira_config attribute checks (raises ValueError, not AttributeError)."""

    def test_missing_base_url_attribute_raises_value_error(self) -> None:
        class NoBaseUrl:
            headers = {"Authorization": "Basic x"}

        with pytest.raises(ValueError, match="missing 'base_url'"):
            _validate_jira_config(NoBaseUrl())

    def test_non_string_base_url_raises_value_error(self) -> None:
        class IntBaseUrl:
            base_url = 123
            headers = {"Authorization": "Basic x"}

        with pytest.raises(ValueError, match="missing 'base_url'"):
            _validate_jira_config(IntBaseUrl())

    def test_missing_headers_attribute_raises_value_error(self) -> None:
        class NoHeaders:
            base_url = "https://jira.example.com"

        with pytest.raises(ValueError, match="missing 'headers'"):
            _validate_jira_config(NoHeaders())
