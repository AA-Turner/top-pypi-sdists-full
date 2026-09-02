"""Tests for get_hierarchy_detector factory function."""

import pytest

from agentic_devtools.cli.speckit.hierarchy_detector import (
    GitHubHierarchyDetector,
    JiraHierarchyDetector,
    get_hierarchy_detector,
)


class TestGetHierarchyDetector:
    """Test suite for get_hierarchy_detector factory."""

    def test_returns_github_detector(self) -> None:
        """Verify factory returns GitHubHierarchyDetector for 'github'."""
        detector = get_hierarchy_detector("github", owner="test-org", repo="test-repo")
        assert isinstance(detector, GitHubHierarchyDetector)

    def test_returns_jira_detector(self) -> None:
        """Verify factory returns JiraHierarchyDetector for 'jira'."""
        detector = get_hierarchy_detector("jira")
        assert isinstance(detector, JiraHierarchyDetector)

    def test_rejects_unknown_provider(self) -> None:
        """Verify factory raises ValueError for unknown provider."""
        with pytest.raises(ValueError, match="Unsupported hierarchy provider: 'azure_devops'"):
            get_hierarchy_detector("azure_devops")

    def test_rejects_empty_string(self) -> None:
        """Verify factory raises ValueError for empty string."""
        with pytest.raises(ValueError, match="Unsupported hierarchy provider: ''"):
            get_hierarchy_detector("")

    def test_rejects_none(self) -> None:
        """Verify factory raises ValueError for None."""
        with pytest.raises(ValueError, match="Unsupported hierarchy provider: None"):
            get_hierarchy_detector(None)

    def test_rejects_uppercase_github(self) -> None:
        """Verify factory is case-sensitive and rejects 'GitHub'."""
        with pytest.raises(ValueError, match="Unsupported hierarchy provider: 'GitHub'"):
            get_hierarchy_detector("GitHub")

    def test_rejects_uppercase_jira(self) -> None:
        """Verify factory is case-sensitive and rejects 'Jira'."""
        with pytest.raises(ValueError, match="Unsupported hierarchy provider: 'Jira'"):
            get_hierarchy_detector("Jira")

    def test_rejects_unhashable_provider(self) -> None:
        """Verify factory raises ValueError (not TypeError) for unhashable types."""
        with pytest.raises(ValueError, match="Unsupported hierarchy provider"):
            get_hierarchy_detector([])

    def test_jira_rejects_unexpected_kwargs(self) -> None:
        """Verify jira provider fails fast on unexpected kwargs."""
        with pytest.raises(TypeError):
            get_hierarchy_detector("jira", owner="org", repo="repo")

    def test_module_all_exports(self) -> None:
        """Verify __all__ contains the expected exports."""
        import agentic_devtools.cli.speckit.hierarchy_detector as mod

        assert mod.__all__ == [
            "GitHubHierarchyDetector",
            "JiraHierarchyDetector",
            "get_hierarchy_detector",
            "parse_issue_reference",
        ]
