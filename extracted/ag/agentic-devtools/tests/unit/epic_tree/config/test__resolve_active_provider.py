"""Tests for _resolve_active_provider function."""

from agentic_devtools.config import DEFAULT_ISSUE_ADAPTER
from agentic_devtools.epic_tree.config import _resolve_active_provider


class TestResolveActiveProvider:
    """Tests for _resolve_active_provider."""

    def test_returns_default_when_no_platform(self):
        """Returns DEFAULT_ISSUE_ADAPTER when platform key absent."""
        assert _resolve_active_provider({}) == DEFAULT_ISSUE_ADAPTER

    def test_returns_default_when_platform_not_dict(self):
        """Returns DEFAULT_ISSUE_ADAPTER when platform is not a dict."""
        assert _resolve_active_provider({"platform": "string"}) == DEFAULT_ISSUE_ADAPTER
        assert _resolve_active_provider({"platform": 42}) == DEFAULT_ISSUE_ADAPTER
        assert _resolve_active_provider({"platform": None}) == DEFAULT_ISSUE_ADAPTER

    def test_returns_default_when_issue_adapter_missing(self):
        """Returns DEFAULT_ISSUE_ADAPTER when issue_adapter not in platform."""
        assert _resolve_active_provider({"platform": {}}) == DEFAULT_ISSUE_ADAPTER

    def test_returns_default_when_issue_adapter_invalid(self):
        """Returns DEFAULT_ISSUE_ADAPTER when issue_adapter is not a valid value."""
        assert _resolve_active_provider({"platform": {"issue_adapter": "invalid"}}) == DEFAULT_ISSUE_ADAPTER
        assert _resolve_active_provider({"platform": {"issue_adapter": 123}}) == DEFAULT_ISSUE_ADAPTER

    def test_returns_github(self):
        """Returns 'github' when issue_adapter is 'github'."""
        assert _resolve_active_provider({"platform": {"issue_adapter": "github"}}) == "github"

    def test_returns_jira(self):
        """Returns 'jira' when issue_adapter is 'jira'."""
        assert _resolve_active_provider({"platform": {"issue_adapter": "jira"}}) == "jira"

    def test_returns_markdown(self):
        """Returns 'markdown' when issue_adapter is 'markdown'."""
        assert _resolve_active_provider({"platform": {"issue_adapter": "markdown"}}) == "markdown"
