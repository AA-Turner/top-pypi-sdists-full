"""Tests for render_issue_md wrapper in agentic_devtools.cli.issue_template.render_issue_md."""

from __future__ import annotations

from unittest.mock import patch

import pytest
import yaml

from agentic_devtools.adapters.types import NormalizedIssue
from agentic_devtools.cli.issue_template.render_issue_md import render_issue_md
from agentic_devtools.cli.issue_template.renderer import PropertyConfig


def _make_issue(**kwargs: object) -> NormalizedIssue:
    """Create a NormalizedIssue with sensible defaults."""
    defaults: dict[str, object] = {
        "issue_id": "PROJECT-42",
        "title": "Add webhook support",
        "url": "https://example.com/issues/42",
        "provider": "jira",
        "description": "Implement webhook handler.",
        "status": "open",
        "labels": ["feature", "backend"],
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-02T00:00:00Z",
        "raw": {"issue_type": "story"},
    }
    defaults.update(kwargs)
    return NormalizedIssue(**defaults)  # type: ignore[arg-type]


class TestRenderIssueMd:
    """Tests for the render_issue_md wrapper function (FR-011)."""

    def test_reads_template_file_and_renders(self, tmp_path: object) -> None:
        """Reads template from path and produces valid output."""
        from pathlib import Path

        tmp = Path(str(tmp_path))
        template_file = tmp / "template.md"
        template_file.write_text("## Description\n\n{{description}}", encoding="utf-8")

        issue = _make_issue()
        with patch(
            "agentic_devtools.cli.issue_template.render_issue_md._find_repo_root",
            return_value=None,
        ):
            result = render_issue_md(str(template_file), issue)

        # Should have frontmatter + body
        parts = result.split("---\n")
        fm = yaml.safe_load(parts[1])
        assert fm["id"] == "PROJECT-42"
        assert fm["type"] == "story"  # FR-005: top-level issue_type returned even without known_types
        assert "Implement webhook handler" in result

    def test_type_resolution_uses_known_types(self, tmp_path: object) -> None:
        """Type resolver uses known_types when preset dir exists."""
        from pathlib import Path

        tmp = Path(str(tmp_path))
        template_file = tmp / "template.md"
        template_file.write_text("{{title}}", encoding="utf-8")

        issue = _make_issue(raw={"issue_type": "story"})

        # Mock discover_templates to return known types including "story"
        with (
            patch(
                "agentic_devtools.cli.issue_template.render_issue_md._find_repo_root",
                return_value=tmp,
            ),
            patch(
                "agentic_devtools.cli.issue_template.render_issue_md.discover_templates",
                return_value=({"story": tmp / "story.md", "task": tmp / "task.md"}, tmp / "default.md"),
            ),
        ):
            # Create a fake preset dir so the exists() check passes
            preset_dir = tmp / ".specify" / "presets" / "agdt-templates"
            preset_dir.mkdir(parents=True)

            result = render_issue_md(str(template_file), issue)

        parts = result.split("---\n")
        fm = yaml.safe_load(parts[1])
        assert fm["type"] == "story"

    def test_timestamp_generated_automatically(self, tmp_path: object) -> None:
        """rendered_at is auto-generated as ISO-8601 UTC."""
        from pathlib import Path

        tmp = Path(str(tmp_path))
        template_file = tmp / "template.md"
        template_file.write_text("{{title}}", encoding="utf-8")

        issue = _make_issue()
        with patch(
            "agentic_devtools.cli.issue_template.render_issue_md._find_repo_root",
            return_value=None,
        ):
            result = render_issue_md(str(template_file), issue)

        parts = result.split("---\n")
        fm = yaml.safe_load(parts[1])
        assert "rendered_at" in fm
        # Should be an ISO-8601 string with timezone
        assert "+" in fm["rendered_at"] or "Z" in fm["rendered_at"]

    def test_resolver_exception_propagates(self, tmp_path: object) -> None:
        """Exception from type resolver propagates unchanged."""
        from pathlib import Path

        tmp = Path(str(tmp_path))
        template_file = tmp / "template.md"
        template_file.write_text("{{title}}", encoding="utf-8")

        issue = _make_issue()
        with (
            patch(
                "agentic_devtools.cli.issue_template.render_issue_md._find_repo_root",
                return_value=None,
            ),
            patch(
                "agentic_devtools.cli.issue_template.render_issue_md.resolve_issue_type",
                side_effect=RuntimeError("resolver broke"),
            ),
            pytest.raises(RuntimeError, match="resolver broke"),
        ):
            render_issue_md(str(template_file), issue)

    def test_property_config_passed_through(self, tmp_path: object) -> None:
        """PropertyConfig is passed to render_issue."""
        from pathlib import Path

        tmp = Path(str(tmp_path))
        template_file = tmp / "template.md"
        template_file.write_text("Priority: {{priority}}\nTitle: {{title}}", encoding="utf-8")

        issue = _make_issue(raw={"priority": "High"})
        config = PropertyConfig(excluded_fields=frozenset({"priority"}))
        with patch(
            "agentic_devtools.cli.issue_template.render_issue_md._find_repo_root",
            return_value=None,
        ):
            result = render_issue_md(str(template_file), issue, property_config=config)

        assert "Priority:" not in result
        assert "Add webhook support" in result

    def test_repo_root_exists_but_no_preset_dir(self, tmp_path: object) -> None:
        """When repo root exists but preset dir doesn't, uses empty known_types."""
        from pathlib import Path

        tmp = Path(str(tmp_path))
        template_file = tmp / "template.md"
        template_file.write_text("{{title}}", encoding="utf-8")

        issue = _make_issue()
        with patch(
            "agentic_devtools.cli.issue_template.render_issue_md._find_repo_root",
            return_value=tmp,
        ):
            # No preset dir created — preset_dir.exists() will be False
            result = render_issue_md(str(template_file), issue)

        parts = result.split("---\n")
        fm = yaml.safe_load(parts[1])
        assert fm["type"] == "story"  # FR-005: top-level issue_type slug returned

    def test_preset_load_error_propagates(self, tmp_path: object) -> None:
        """PresetLoadError from discover_templates propagates unchanged (FR-006/T023)."""
        from pathlib import Path

        from agentic_devtools.cli.issue_template.exceptions import PresetLoadError

        tmp = Path(str(tmp_path))
        template_file = tmp / "template.md"
        template_file.write_text("{{title}}", encoding="utf-8")

        issue = _make_issue()
        preset_dir = tmp / ".specify" / "presets" / "agdt-templates"
        preset_dir.mkdir(parents=True)

        with (
            patch(
                "agentic_devtools.cli.issue_template.render_issue_md._find_repo_root",
                return_value=tmp,
            ),
            patch(
                "agentic_devtools.cli.issue_template.render_issue_md.discover_templates",
                side_effect=PresetLoadError("preset.yml missing"),
            ),
            pytest.raises(PresetLoadError, match="preset.yml missing"),
        ):
            render_issue_md(str(template_file), issue)
