"""Tests for the JiraProvider dry run capability."""

from __future__ import annotations

from agentic_devtools.adapters.jira_provider import JiraProvider
from tests.unit.adapters.jira_provider._fixtures import _make_mock_session


class TestJiraProviderDryRunManifest:
    """Tests for dry-run manifest accumulation."""

    def test_dry_run_accumulates_issues(self):
        session = _make_mock_session()
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        provider.create_issue("Title 1", "Body", "epic", dry_run=True)
        provider.create_issue("Title 2", "Body", "feature", dry_run=True)
        manifest = provider.get_dry_run_manifest()
        assert len(manifest["issues"]) == 2

    def test_dry_run_accumulates_dependencies(self):
        session = _make_mock_session()
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)
        provider.link_subissue("PROJ-1", "PROJ-2", dry_run=True)
        provider.add_blocked_by("PROJ-3", "PROJ-4", dry_run=True)
        manifest = provider.get_dry_run_manifest()
        assert len(manifest["dependencies"]) == 2

    def test_dry_run_manifest_full_flow(self):
        """10 issues + 8 dependencies all marked dry-run."""
        session = _make_mock_session()
        provider = JiraProvider(project_key="PROJ", base_url="https://jira.example.com", session=session)

        for i in range(10):
            result = provider.create_issue(f"Issue {i}", f"Body {i}", "task", dry_run=True)
            assert result.status == "dry-run"

        for i in range(8):
            result = provider.add_blocked_by(f"PROJ-{i + 1}", f"PROJ-{i}", dry_run=True)
            assert result.status == "dry-run"

        manifest = provider.get_dry_run_manifest()
        assert len(manifest["issues"]) == 10
        assert len(manifest["dependencies"]) == 8
        session.request.assert_not_called()
