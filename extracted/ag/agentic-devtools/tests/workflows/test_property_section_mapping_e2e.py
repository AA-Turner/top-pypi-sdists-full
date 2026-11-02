"""End-to-end integration test for property-section mapping (#1793).

Exercises both public entry points — ``render_issue_md`` (path-based API) and
``render_issue_command`` (CLI) — against the property-section mapping resolver
to prove:

* a project-config-only mapping (``.agdt/config/project.json``) is honored by
  both entry points; and
* an explicit ``PropertyConfig`` mapping merges over the project layer
  (explicit wins per key) through ``render_issue_md``.

This is a cross-component integration test (mapping resolver + project config
+ renderer + CLI orchestration) and therefore lives under ``tests/workflows/``
rather than ``tests/unit/``.
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

import yaml

from agentic_devtools.adapters.types import NormalizedIssue
from agentic_devtools.cli.issue_template.render_issue_md import render_issue_md
from agentic_devtools.cli.issue_template.renderer import PropertyConfig


def _make_issue() -> NormalizedIssue:
    return NormalizedIssue(
        issue_id="PROJ-1",
        title="Title",
        url="https://example.com/PROJ-1",
        provider="jira",
        description="Body description.",
        status="open",
        labels=["story"],
        comments=[],
        created_at="2024-01-01T00:00:00Z",
        updated_at="2024-01-02T00:00:00Z",
        raw={"issue_type": "story"},
    )


def _frontmatter(rendered: str) -> dict:
    return yaml.safe_load(rendered.split("---\n")[1])


class TestRenderIssueMdProjectMapping:
    """render_issue_md honors project-config mappings and explicit merges."""

    def test_project_mapping_only(self, tmp_path: Path) -> None:
        template = tmp_path / "tmpl.md"
        template.write_text("## Links\n\n{{url}}\n", encoding="utf-8")

        project_config = {"issueTemplate": {"property_section_mapping": {"url": "frontmatter"}}}
        with (
            patch(
                "agentic_devtools.cli.config.project_config.load_effective_project_config",
                lambda *, git_root=None: project_config,
            ),
            patch(
                "agentic_devtools.cli.issue_template.render_issue_md._find_repo_root",
                return_value=None,
            ),
        ):
            rendered = render_issue_md(str(template), _make_issue())

        fm = _frontmatter(rendered)
        assert fm["url"] == "https://example.com/PROJ-1"
        # The body occurrence was routed away.
        assert "https://example.com/PROJ-1" not in rendered.split("---\n")[2]

    def test_explicit_mapping_merges_over_project(self, tmp_path: Path) -> None:
        template = tmp_path / "tmpl.md"
        template.write_text("## Links\n\n- URL: {{url}}\n", encoding="utf-8")

        project_config = {"issueTemplate": {"property_section_mapping": {"url": "frontmatter", "created_at": "omit"}}}
        explicit = PropertyConfig(property_section_mapping={"url": "body:Links"})
        with (
            patch(
                "agentic_devtools.cli.config.project_config.load_effective_project_config",
                lambda *, git_root=None: project_config,
            ),
            patch(
                "agentic_devtools.cli.issue_template.render_issue_md._find_repo_root",
                return_value=None,
            ),
        ):
            rendered = render_issue_md(str(template), _make_issue(), explicit)

        # Explicit url->body:Links wins over the project's url->frontmatter.
        assert "url" not in _frontmatter(rendered)
        assert "- URL: https://example.com/PROJ-1" in rendered


class TestRenderIssueCommandProjectMapping:
    """render_issue_command (CLI) cannot bypass the project mapping."""

    def _setup_preset(self, tmp_path: Path) -> Path:
        preset_dir = tmp_path / ".specify" / "presets" / "agdt-templates"
        templates_dir = preset_dir / "templates"
        templates_dir.mkdir(parents=True)
        (preset_dir / "preset.yml").write_text(
            "name: test\ntemplates:\n  - issue-template.md\n  - issue-template-story.md\n",
            encoding="utf-8",
        )
        (templates_dir / "issue-template.md").write_text("## Links\n\n{{url}}\n", encoding="utf-8")
        (templates_dir / "issue-template-story.md").write_text("## Links\n\n{{url}}\n", encoding="utf-8")
        return tmp_path

    def test_cli_applies_project_mapping(self, tmp_path: Path) -> None:
        from agentic_devtools.cli.issue_template.commands import render_issue_command

        repo_root = self._setup_preset(tmp_path)
        state_dir = tmp_path / "state"
        state_dir.mkdir()

        issue = _make_issue()
        mock_adapter = MagicMock()
        mock_adapter.get_issue.return_value = {}
        mock_adapter.normalize.return_value = issue

        project_config = {"issueTemplate": {"property_section_mapping": {"url": "frontmatter"}}}
        with (
            patch(
                "agentic_devtools.cli.issue_template.commands.get_value",
                side_effect=lambda k: {
                    "issue_template.template_path": None,
                    "issue_key": "PROJ-1",
                    "jira.issue_key": None,
                }.get(k),
            ),
            patch(
                "agentic_devtools.cli.issue_template.commands._find_repo_root",
                return_value=repo_root,
            ),
            patch(
                "agentic_devtools.cli.issue_template.commands.get_adapter",
                return_value=mock_adapter,
            ),
            patch(
                "agentic_devtools.cli.issue_template.commands.get_state_dir",
                return_value=state_dir,
            ),
            patch(
                "agentic_devtools.cli.config.project_config.load_effective_project_config",
                lambda *, git_root=None: project_config,
            ),
        ):
            render_issue_command()

        content = (state_dir / "issue.md").read_text(encoding="utf-8")
        fm = _frontmatter(content)
        assert fm["url"] == "https://example.com/PROJ-1"
        assert "https://example.com/PROJ-1" not in content.split("---\n")[2]
