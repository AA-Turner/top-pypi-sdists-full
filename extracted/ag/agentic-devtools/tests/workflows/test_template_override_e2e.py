"""End-to-end integration test for per-issue-type template overrides (#1792).

Exercises the full resolve -> select chain against the *shipped* preset in
``.specify/presets/agdt-templates`` to prove:

* the forward-order filename contract (``issue-template-{slug}.md`` -> base
  ``issue-template.md`` fallback) is honored;
* known types (bug, story, task, feature) resolve to their own overrides;
* an unknown type (spike) falls back to the base default with zero
  ``TemplateNotFoundError``;
* the Jira nested ``issuetype`` normalization path feeds the resolver so a raw
  Jira payload selects the correct type-specific template.

This is a cross-component integration test (discovery + type_resolver +
jira_adapter against real on-disk preset files) and therefore lives under
``tests/workflows/`` rather than ``tests/unit/``.
"""

from __future__ import annotations

from pathlib import Path

from agentic_devtools.adapters.jira_adapter import JiraAdapter
from agentic_devtools.adapters.types import NormalizedIssue
from agentic_devtools.cli.issue_template.discovery import discover_templates, select_template
from agentic_devtools.cli.issue_template.type_resolver import resolve_issue_type
from agentic_devtools.tools.jira import JiraConfig

_PRESET_DIR = Path(__file__).resolve().parents[2] / ".specify" / "presets" / "agdt-templates"


def _make_issue(issue_type: str) -> NormalizedIssue:
    return NormalizedIssue(
        issue_id="PROJ-1",
        title="Title",
        url="https://example.com/PROJ-1",
        provider="jira",
        description="desc",
        status="open",
        labels=[],
        comments=[],
        created_at="",
        updated_at="",
        raw={"issue_type": issue_type},
    )


class TestShippedPresetRegistersForwardOrderTemplates:
    """The shipped preset must register the new forward-order filenames."""

    def test_type_specific_and_default_templates_registered(self) -> None:
        templates, default_template = discover_templates(_PRESET_DIR)

        # Forward-order type-specific overrides are discovered by slug.
        for slug in ("bug", "story", "task", "feature"):
            assert slug in templates, f"expected '{slug}' override to be registered"
            assert templates[slug].name == f"issue-template-{slug}.md"
            assert templates[slug].exists()

        # Base default is registered.
        assert default_template is not None
        assert default_template.name == "issue-template.md"
        assert default_template.exists()


class TestResolveSelectChainAgainstShippedPreset:
    """resolve_issue_type -> select_template end-to-end against real files."""

    def test_known_types_select_their_own_overrides(self) -> None:
        templates, default_template = discover_templates(_PRESET_DIR)
        known = set(templates)

        for slug in ("bug", "story", "task", "feature"):
            resolved = resolve_issue_type(_make_issue(slug), known)
            assert resolved == slug
            selected = select_template(resolved, templates, default_template, preset_dir=_PRESET_DIR)
            assert selected.name == f"issue-template-{slug}.md"

    def test_unknown_type_falls_back_to_default_without_error(self) -> None:
        templates, default_template = discover_templates(_PRESET_DIR)
        known = set(templates)

        resolved = resolve_issue_type(_make_issue("spike"), known)
        # FR-005: the top-level slug is returned even when unknown.
        assert resolved == "spike"
        # FR-002: falls back to the base default, never raising.
        selected = select_template(resolved, templates, default_template, preset_dir=_PRESET_DIR)
        assert selected.name == "issue-template.md"


class TestJiraNestedNormalizationFeedsSelection:
    """A raw Jira payload's nested issuetype drives type-specific selection."""

    def test_nested_jira_issuetype_selects_type_specific_template(self) -> None:
        adapter = JiraAdapter(
            config=JiraConfig(
                base_url="https://jira.example.com",
                headers={"Authorization": "Basic xxx"},
                ssl_verify=False,
            ),
            project_key="PROJ",
        )
        normalized = adapter.normalize(
            {
                "issue_id": "PROJ-9",
                "title": "Nested Bug",
                "description": "desc",
                "status": "Open",
                "labels": [],
                "url": "https://jira.example.com/browse/PROJ-9",
                "comments": [],
                "raw": {"fields": {"issuetype": {"name": "Bug"}}},
            }
        )

        templates, default_template = discover_templates(_PRESET_DIR)
        resolved = resolve_issue_type(normalized, set(templates))
        assert resolved == "bug"
        selected = select_template(resolved, templates, default_template, preset_dir=_PRESET_DIR)
        assert selected.name == "issue-template-bug.md"
