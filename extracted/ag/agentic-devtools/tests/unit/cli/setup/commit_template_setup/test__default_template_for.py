"""Tests for _default_template_for."""

import pytest

from agentic_devtools.cli.setup.commit_template_setup import (
    _TEMPLATE_GITHUB,
    _TEMPLATE_JIRA,
    _TEMPLATE_MARKDOWN,
    _default_template_for,
)


class TestDefaultTemplateFor:
    """Tests for the per-adapter default-template selector."""

    def test_github_adapter(self):
        assert _default_template_for("github") == _TEMPLATE_GITHUB

    def test_jira_adapter(self):
        assert _default_template_for("jira") == _TEMPLATE_JIRA

    def test_markdown_adapter(self):
        assert _default_template_for("markdown") == _TEMPLATE_MARKDOWN

    @pytest.mark.parametrize("adapter", ["", "unknown", "azure_devops"])
    def test_unknown_adapter_falls_back_to_github(self, adapter):
        """Any unrecognized adapter falls back to the GitHub template."""
        assert _default_template_for(adapter) == _TEMPLATE_GITHUB

    def test_github_template_uses_bare_scope_and_footer(self):
        """GitHub template uses a bare #NNN scope and footer (no markdown link)."""
        assert "(#{{ issueKey }})" in _TEMPLATE_GITHUB
        assert "issueLink" not in _TEMPLATE_GITHUB

    def test_jira_template_uses_bare_scope_and_link_footer(self):
        """Jira template uses a bare-key scope and a markdown link footer."""
        assert "({{ issueKey }})" in _TEMPLATE_JIRA
        assert "[{{ issueKey }}]({{ issueLink }})" in _TEMPLATE_JIRA

    def test_markdown_template_uses_plain_key_footer(self):
        """Markdown template uses a bare-key scope and plain-text footer."""
        assert "({{ issueKey }})" in _TEMPLATE_MARKDOWN
        assert "issueLink" not in _TEMPLATE_MARKDOWN
