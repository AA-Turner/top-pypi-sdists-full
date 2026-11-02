"""Tests for ensure_commit_template (provider-aware)."""

import json
from pathlib import Path

from agentic_devtools.cli.git.commit_template import TEMPLATE_PATH
from agentic_devtools.cli.setup.commit_template_setup import (
    _TEMPLATE_GITHUB,
    _TEMPLATE_JIRA,
    _TEMPLATE_MARKDOWN,
    ensure_commit_template,
)


def _write_config(tmp_path: Path, issue_adapter: str) -> None:
    """Write a .github/agdt-config.json selecting the given issue adapter."""
    config_dir = tmp_path / ".github"
    config_dir.mkdir(parents=True, exist_ok=True)
    (config_dir / "agdt-config.json").write_text(
        json.dumps({"platform": {"issue_adapter": issue_adapter}}), encoding="utf-8"
    )


class TestEnsureCommitTemplate:
    """Tests for ensure_commit_template."""

    def test_creates_github_template_under_github_adapter(self, tmp_path):
        """Writes the GitHub default template when issue_adapter is github."""
        _write_config(tmp_path, "github")
        result = ensure_commit_template(tmp_path)
        assert result is True
        template_file = tmp_path / TEMPLATE_PATH
        assert template_file.read_text(encoding="utf-8") == _TEMPLATE_GITHUB

    def test_creates_jira_template_under_jira_adapter(self, tmp_path):
        """Writes the Jira default template when issue_adapter is jira."""
        _write_config(tmp_path, "jira")
        result = ensure_commit_template(tmp_path)
        assert result is True
        template_file = tmp_path / TEMPLATE_PATH
        assert template_file.read_text(encoding="utf-8") == _TEMPLATE_JIRA

    def test_creates_markdown_template_under_markdown_adapter(self, tmp_path):
        """Writes the markdown default template when issue_adapter is markdown."""
        _write_config(tmp_path, "markdown")
        result = ensure_commit_template(tmp_path)
        assert result is True
        template_file = tmp_path / TEMPLATE_PATH
        assert template_file.read_text(encoding="utf-8") == _TEMPLATE_MARKDOWN

    def test_no_config_uses_default_adapter(self, tmp_path):
        """With no config the platform default adapter (jira) template is written."""
        result = ensure_commit_template(tmp_path)
        assert result is True
        template_file = tmp_path / TEMPLATE_PATH
        assert template_file.read_text(encoding="utf-8") == _TEMPLATE_JIRA

    def test_does_not_overwrite_existing(self, tmp_path):
        """Does not overwrite an existing template (FR-002)."""
        template_file = tmp_path / TEMPLATE_PATH
        template_file.parent.mkdir(parents=True)
        template_file.write_text("custom template", encoding="utf-8")
        result = ensure_commit_template(tmp_path)
        assert result is False
        assert template_file.read_text(encoding="utf-8") == "custom template"

    def test_creates_directory_structure(self, tmp_path):
        """Creates .agdt/config/ directory when missing (FR-008)."""
        _write_config(tmp_path, "github")
        config_dir = tmp_path / ".agdt" / "config"
        assert not config_dir.exists()
        ensure_commit_template(tmp_path)
        assert config_dir.is_dir()

    def test_returns_false_when_exists(self, tmp_path):
        """Returns False when template already exists."""
        template_file = tmp_path / TEMPLATE_PATH
        template_file.parent.mkdir(parents=True)
        template_file.write_text("existing", encoding="utf-8")
        assert ensure_commit_template(tmp_path) is False

    def test_default_templates_are_valid_jinja2(self):
        """Each provider default template is syntactically valid Jinja2."""
        import jinja2

        env = jinja2.Environment(loader=jinja2.BaseLoader())
        for template in (_TEMPLATE_GITHUB, _TEMPLATE_JIRA, _TEMPLATE_MARKDOWN):
            # Should not raise
            env.parse(template)
