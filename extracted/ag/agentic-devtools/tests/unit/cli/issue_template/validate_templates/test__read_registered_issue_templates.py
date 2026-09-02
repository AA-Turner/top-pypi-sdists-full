"""Tests for _read_registered_issue_templates()."""

from __future__ import annotations

from pathlib import Path

from agentic_devtools.cli.issue_template.validate_templates import (
    _read_registered_issue_templates,
)


def _write_preset_yml(preset_dir: Path, body: str) -> None:
    preset_dir.mkdir(parents=True, exist_ok=True)
    (preset_dir / "preset.yml").write_text(body, encoding="utf-8")


class TestReadRegisteredIssueTemplates:
    """Tests for enumerating registered issue-template filenames from preset.yml."""

    def test_missing_preset_yml_returns_empty(self, tmp_path: Path) -> None:
        """A directory without preset.yml returns an empty list."""
        assert _read_registered_issue_templates(tmp_path) == []

    def test_non_dict_yaml_returns_empty(self, tmp_path: Path) -> None:
        """A preset.yml whose top-level is not a mapping returns an empty list."""
        _write_preset_yml(tmp_path, "- just\n- a\n- list\n")
        assert _read_registered_issue_templates(tmp_path) == []

    def test_templates_not_list_returns_empty(self, tmp_path: Path) -> None:
        """A preset.yml where 'templates' is not a list returns an empty list."""
        _write_preset_yml(tmp_path, "templates: not-a-list\n")
        assert _read_registered_issue_templates(tmp_path) == []

    def test_malformed_yaml_returns_empty(self, tmp_path: Path) -> None:
        """Malformed YAML returns an empty template list instead of raising."""
        _write_preset_yml(tmp_path, "templates:\n  - issue-template.md\n  - [\n")
        assert _read_registered_issue_templates(tmp_path) == []

    def test_filters_and_keeps_issue_templates(self, tmp_path: Path) -> None:
        """Only default/issue-type templates are kept; others and unsafe entries skipped."""
        _write_preset_yml(
            tmp_path,
            "templates:\n"
            "  - issue-template.md\n"
            "  - issue-template-bug.md\n"
            "  - spec-template.md\n"
            "  - 123\n"
            "  - sub/dir-template.md\n"
            "  - back\\slash.md\n",
        )
        assert _read_registered_issue_templates(tmp_path) == [
            "issue-template.md",
            "issue-template-bug.md",
        ]
