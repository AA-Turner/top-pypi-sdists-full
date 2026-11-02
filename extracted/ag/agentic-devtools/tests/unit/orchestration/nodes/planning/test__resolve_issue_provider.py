"""Tests for _resolve_issue_provider."""

from __future__ import annotations

from typing import Any, cast

from agentic_devtools.orchestration.nodes.planning import _resolve_issue_provider
from agentic_devtools.orchestration.state_schema import WorkOnIssueState


class TestResolveIssueProvider:
    """Tests for issue provider resolution from state or key format."""

    def _state(self, **kwargs: Any) -> WorkOnIssueState:
        return cast(WorkOnIssueState, kwargs)

    def test_returns_jira_from_state(self) -> None:
        state = self._state(issue_provider="jira")
        assert _resolve_issue_provider(state, "42") == "jira"

    def test_returns_github_from_state(self) -> None:
        state = self._state(issue_provider="github")
        assert _resolve_issue_provider(state, "PROJECT-1") == "github"

    def test_ignores_invalid_provider_in_state(self) -> None:
        state = self._state(issue_provider="unknown_provider")
        # Falls back to key-based detection
        result = _resolve_issue_provider(state, "PROJECT-123")
        assert result == "jira"

    def test_falls_back_to_key_detection_for_jira_key(self) -> None:
        state = self._state()
        assert _resolve_issue_provider(state, "PROJ-42") == "jira"

    def test_falls_back_to_key_detection_for_github_number(self) -> None:
        state = self._state()
        assert _resolve_issue_provider(state, "42") == "github"

    def test_falls_back_to_key_detection_for_hash_prefixed_github(self) -> None:
        state = self._state()
        assert _resolve_issue_provider(state, "#7") == "github"

    def test_non_string_provider_in_state_falls_back_to_detection(self) -> None:
        state = self._state(issue_provider=123)
        result = _resolve_issue_provider(state, "PROJ-1")
        assert result == "jira"
