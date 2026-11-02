"""Tests for validate_commit_template (adapter-aware)."""

import json
from pathlib import Path
from unittest.mock import patch

from agentic_devtools.cli.git.commit_template import TEMPLATE_PATH
from agentic_devtools.cli.setup.commit_template_setup import (
    _TEMPLATE_GITHUB,
    _TEMPLATE_JIRA,
    validate_commit_template,
)


def _write_config(tmp_path: Path, issue_adapter: str) -> None:
    """Write a .github/agdt-config.json selecting the given issue adapter."""
    config_dir = tmp_path / ".github"
    config_dir.mkdir(parents=True, exist_ok=True)
    (config_dir / "agdt-config.json").write_text(
        json.dumps({"platform": {"issue_adapter": issue_adapter}}), encoding="utf-8"
    )


def _write_template(tmp_path: Path, content: str) -> Path:
    template_file = tmp_path / TEMPLATE_PATH
    template_file.parent.mkdir(parents=True, exist_ok=True)
    template_file.write_text(content, encoding="utf-8")
    return template_file


class TestValidateCommitTemplate:
    """Tests for validate_commit_template."""

    def test_github_default_template_no_warnings(self, tmp_path):
        """GitHub default template (no issueLink) produces no warnings under github adapter."""
        _write_config(tmp_path, "github")
        _write_template(tmp_path, _TEMPLATE_GITHUB)
        assert validate_commit_template(tmp_path) == []

    def test_jira_default_template_no_warnings(self, tmp_path):
        """Jira default template (with issueLink) produces no warnings under jira adapter."""
        _write_config(tmp_path, "jira")
        _write_template(tmp_path, _TEMPLATE_JIRA)
        assert validate_commit_template(tmp_path) == []

    def test_github_adapter_does_not_require_issue_link(self, tmp_path):
        """issueLink is not required for the github adapter (it legitimately omits it)."""
        _write_config(tmp_path, "github")
        _write_template(tmp_path, _TEMPLATE_GITHUB)
        warnings = validate_commit_template(tmp_path)
        assert all("issueLink" not in w for w in warnings)

    def test_jira_adapter_warns_about_missing_issue_link(self, tmp_path):
        """Jira adapter requires issueLink; a template omitting it warns."""
        _write_config(tmp_path, "jira")
        # GitHub-style template (no issueLink) used under the jira adapter.
        _write_template(tmp_path, _TEMPLATE_GITHUB)
        warnings = validate_commit_template(tmp_path)
        assert len(warnings) == 1
        assert "issueLink" in warnings[0]

    def test_extra_variables_no_error(self, tmp_path):
        """Extra custom variables do not produce errors (FR-006)."""
        _write_config(tmp_path, "github")
        _write_template(tmp_path, _TEMPLATE_GITHUB + "\n{{ customVar }}")
        assert validate_commit_template(tmp_path) == []

    def test_returns_empty_when_no_file(self, tmp_path):
        """Returns empty list when template file does not exist."""
        assert validate_commit_template(tmp_path) == []

    def test_empty_file_warns(self, tmp_path):
        """Warns when template file is empty."""
        _write_template(tmp_path, "")
        warnings = validate_commit_template(tmp_path)
        assert len(warnings) == 1
        assert "empty" in warnings[0]

    def test_syntax_error_warns(self, tmp_path):
        """Warns when template has Jinja2 syntax error."""
        _write_template(tmp_path, "{% if x %}")
        warnings = validate_commit_template(tmp_path)
        assert len(warnings) == 1
        assert "syntax error" in warnings[0]

    def test_multiple_missing_variables_github(self, tmp_path):
        """Reports all missing required variables for the github adapter (no issueLink)."""
        _write_config(tmp_path, "github")
        _write_template(tmp_path, "{{ issueKey }}")
        warnings = validate_commit_template(tmp_path)
        # Missing: issueType, commitMessageTitle, commitMessageBody (NOT issueLink)
        assert len(warnings) == 3
        assert all("issueLink" not in w for w in warnings)

    def test_multiple_missing_variables_jira(self, tmp_path):
        """Reports all missing required variables for the jira adapter (incl. issueLink)."""
        _write_config(tmp_path, "jira")
        _write_template(tmp_path, "{{ issueKey }}")
        warnings = validate_commit_template(tmp_path)
        # Missing: issueType, issueLink, commitMessageTitle, commitMessageBody
        assert len(warnings) == 4

    def test_read_error_warns(self, tmp_path):
        """Returns warning when file cannot be read."""
        _write_template(tmp_path, "content")
        # Mock the read to raise OSError (cross-platform; chmod(0o000) does not
        # prevent reads for the owner on Windows).
        with patch("pathlib.Path.read_text", side_effect=OSError("permission denied")):
            warnings = validate_commit_template(tmp_path)
        assert len(warnings) == 1
        assert "Cannot read" in warnings[0]
