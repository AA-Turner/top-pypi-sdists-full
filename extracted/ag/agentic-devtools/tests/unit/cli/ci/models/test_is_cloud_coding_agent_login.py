"""Tests for the is_cloud_coding_agent_login helper."""

import pytest

from agentic_devtools.cli.ci.models import is_cloud_coding_agent_login


class TestIsCloudCodingAgentLogin:
    """Tests for exact Cloud Coding Agent identity matching."""

    @pytest.mark.parametrize(
        "login",
        [
            "copilot-swe-agent[bot]",
            "copilot-swe-agent",
            "app/copilot-swe-agent",
        ],
    )
    def test_recognizes_cloud_coding_agent_aliases(self, login: str) -> None:
        assert is_cloud_coding_agent_login(login) is True

    def test_matching_is_case_insensitive(self) -> None:
        assert is_cloud_coding_agent_login("APP/COPILOT-SWE-AGENT") is True

    def test_reviewer_bot_is_not_cloud_coding_agent(self) -> None:
        assert is_cloud_coding_agent_login("copilot-pull-request-reviewer[bot]") is False

    @pytest.mark.parametrize("login", ["", "octocat", "copilot[bot]", None, 123])
    def test_rejects_other_or_non_string_values(self, login: object) -> None:
        assert is_cloud_coding_agent_login(login) is False  # type: ignore[arg-type]
