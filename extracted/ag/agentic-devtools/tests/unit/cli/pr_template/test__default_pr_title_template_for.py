"""Tests for _default_pr_title_template_for."""

import pytest

from agentic_devtools.cli.pr_template import (
    _PR_TITLE_GITHUB,
    _PR_TITLE_JIRA,
    _PR_TITLE_MARKDOWN,
    _default_pr_title_template_for,
)


class TestDefaultPrTitleTemplateFor:
    """Tests for the per-adapter PR title template selector."""

    def test_github_adapter(self):
        assert _default_pr_title_template_for("github") == _PR_TITLE_GITHUB

    def test_jira_adapter(self):
        assert _default_pr_title_template_for("jira") == _PR_TITLE_JIRA

    def test_markdown_adapter(self):
        assert _default_pr_title_template_for("markdown") == _PR_TITLE_MARKDOWN

    @pytest.mark.parametrize("adapter", ["", "unknown", "azure_devops"])
    def test_unknown_adapter_falls_back_to_github(self, adapter):
        assert _default_pr_title_template_for(adapter) == _PR_TITLE_GITHUB

    def test_github_uses_hash_scope(self):
        """GitHub PR title uses a bare #NNN scope."""
        assert "(#{{ issueKey }})" in _PR_TITLE_GITHUB

    def test_jira_uses_bare_key_scope(self):
        """Jira PR title uses a bare-key scope (no #)."""
        assert "({{ issueKey }})" in _PR_TITLE_JIRA
        assert "(#{{ issueKey }})" not in _PR_TITLE_JIRA
