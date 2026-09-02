"""Tests for agentic_devtools.cli.pr_template.ensure_pr_title_template."""

import json
from pathlib import Path

from agentic_devtools.cli.pr_template import (
    _PR_TITLE_GITHUB,
    _PR_TITLE_JIRA,
    _PR_TITLE_MARKDOWN,
    PR_TITLE_TEMPLATE_PATH,
    ensure_pr_title_template,
)


def _write_config(tmp_path: Path, issue_adapter: str) -> None:
    """Write a .github/agdt-config.json selecting the given issue adapter."""
    config_dir = tmp_path / ".github"
    config_dir.mkdir(parents=True, exist_ok=True)
    (config_dir / "agdt-config.json").write_text(
        json.dumps({"platform": {"issue_adapter": issue_adapter}}), encoding="utf-8"
    )


class TestEnsurePrTitleTemplate:
    """Tests for ensure_pr_title_template()."""

    def test_creates_template_when_missing(self, tmp_path):
        """Creates default PR title template when it does not exist."""
        result = ensure_pr_title_template(tmp_path)

        assert result is True
        template_path = tmp_path / PR_TITLE_TEMPLATE_PATH
        assert template_path.exists()
        content = template_path.read_text(encoding="utf-8")
        assert "{{ issueType }}" in content
        assert "{{ issueKey }}" in content
        assert "{{ commitMessageTitle }}" in content

    def test_creates_github_template_under_github_adapter(self, tmp_path):
        """Writes the GitHub `#NNN` PR title template under the github adapter."""
        _write_config(tmp_path, "github")
        assert ensure_pr_title_template(tmp_path) is True
        content = (tmp_path / PR_TITLE_TEMPLATE_PATH).read_text(encoding="utf-8")
        assert content == _PR_TITLE_GITHUB
        assert "(#{{ issueKey }})" in content

    def test_creates_jira_template_under_jira_adapter(self, tmp_path):
        """Writes the Jira bare-key PR title template under the jira adapter."""
        _write_config(tmp_path, "jira")
        assert ensure_pr_title_template(tmp_path) is True
        content = (tmp_path / PR_TITLE_TEMPLATE_PATH).read_text(encoding="utf-8")
        assert content == _PR_TITLE_JIRA
        assert "({{ issueKey }})" in content

    def test_creates_markdown_template_under_markdown_adapter(self, tmp_path):
        """Writes the markdown bare-key PR title template under the markdown adapter."""
        _write_config(tmp_path, "markdown")
        assert ensure_pr_title_template(tmp_path) is True
        content = (tmp_path / PR_TITLE_TEMPLATE_PATH).read_text(encoding="utf-8")
        assert content == _PR_TITLE_MARKDOWN

    def test_does_not_overwrite_existing(self, tmp_path):
        """Does not overwrite an existing template."""
        template_path = tmp_path / PR_TITLE_TEMPLATE_PATH
        template_path.parent.mkdir(parents=True, exist_ok=True)
        template_path.write_text("custom template", encoding="utf-8")

        result = ensure_pr_title_template(tmp_path)

        assert result is False
        assert template_path.read_text(encoding="utf-8") == "custom template"

    def test_creates_parent_directories(self, tmp_path):
        """Creates parent directories if they don't exist."""
        result = ensure_pr_title_template(tmp_path)

        assert result is True
        template_path = tmp_path / PR_TITLE_TEMPLATE_PATH
        assert template_path.parent.is_dir()
