"""Synchronous CLI entry point for rendering issue.md.

Orchestrates: adapter resolution -> fetch -> normalize -> discover ->
resolve type -> render -> write.
"""

from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

from agentic_devtools.adapters import get_adapter
from agentic_devtools.cli.issue_template._repo_paths import (
    _PRESET_DIR_RELATIVE,
    _find_repo_root,
)
from agentic_devtools.cli.issue_template.discovery import (
    discover_templates,
    select_template,
)
from agentic_devtools.cli.issue_template.exceptions import (
    PresetLoadError,
    TemplateNotFoundError,
    TemplateValidationError,
)
from agentic_devtools.cli.issue_template.renderer import PropertyConfig, render_issue
from agentic_devtools.cli.issue_template.type_resolver import resolve_issue_type, slugify_type
from agentic_devtools.cli.issue_template.validator import validate_required_properties
from agentic_devtools.state import get_state_dir, get_value

_OUTPUT_FILENAME = "issue.md"


def render_issue_command() -> None:
    """Render a NormalizedIssue to issue.md.

    Synchronous orchestration function called by the background task.
    Reads state, fetches issue via adapter, renders template, and writes output.
    """
    template_override = get_value("issue_template.template_path")

    issue_key = get_value("issue_key")
    if not issue_key:
        issue_key = get_value("jira.issue_key")
    if not issue_key:
        print("Error: issue_key is required.", file=sys.stderr)
        sys.exit(1)

    repo_root = _find_repo_root()
    if repo_root is None:
        print("Error: Not in a git repository.", file=sys.stderr)
        sys.exit(1)

    preset_dir = repo_root / _PRESET_DIR_RELATIVE
    try:
        templates_map, default_template = discover_templates(preset_dir)
    except PresetLoadError as exc:
        print(f"Error loading preset: {exc}", file=sys.stderr)
        sys.exit(1)

    try:
        adapter = get_adapter(str(repo_root))
        issue_detail = adapter.get_issue(str(issue_key))
        issue = adapter.normalize(issue_detail)
    except Exception as exc:
        print(f"Error fetching issue: {exc}", file=sys.stderr)
        sys.exit(1)

    type_slug = resolve_issue_type(issue, set(templates_map.keys()))

    # Use the provider-native type name (not the slug) for adapter schema lookup
    # so that multi-word names like "Customer Request" match correctly.
    # Fall back to the slug when no raw type is available (label or default path).
    raw_type_name = issue.raw.get("issue_type")
    properties_type_name = (
        raw_type_name.strip()
        if isinstance(raw_type_name, str) and raw_type_name.strip() and slugify_type(raw_type_name)
        else type_slug
    )

    try:
        properties = adapter.get_type_properties(properties_type_name)
        validate_required_properties(issue, properties)
    except TemplateValidationError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
    except NotImplementedError:
        pass  # Adapter does not implement type properties; skip validation
    except (RuntimeError, ValueError) as exc:
        print(
            f"Error validating type properties for '{properties_type_name}': {exc}.",
            file=sys.stderr,
        )
        sys.exit(1)

    try:
        if isinstance(template_override, str) and template_override.strip():
            template_path = Path(template_override)
            if not template_path.exists():
                print(
                    f"Error: Template override not found: {template_override}",
                    file=sys.stderr,
                )
                sys.exit(1)
            if not template_path.is_file():
                print(
                    f"Error: Template override is not a file: {template_override}",
                    file=sys.stderr,
                )
                sys.exit(1)
        else:
            template_path = select_template(type_slug, templates_map, default_template, preset_dir)
    except TemplateNotFoundError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    try:
        template_content = template_path.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"Error: Could not read template file: {exc}", file=sys.stderr)
        sys.exit(1)
    rendered_at = datetime.now(timezone.utc).isoformat()

    # Resolve the effective property-section mapping so the CLI path cannot
    # bypass project mappings, then thread it into ``render_issue``.
    from agentic_devtools.cli.issue_template.mapping_resolver import resolve_effective_mapping

    try:
        effective_mapping = resolve_effective_mapping()
    except (TemplateValidationError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
    property_config = PropertyConfig(property_section_mapping=effective_mapping or None)

    try:
        output = render_issue(issue, type_slug, template_content, rendered_at, property_config)
    except TemplateValidationError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    output_path = get_state_dir() / _OUTPUT_FILENAME
    try:
        output_path.write_text(output, encoding="utf-8")
    except OSError as exc:
        print(f"Error: Could not write output file: {exc}", file=sys.stderr)
        sys.exit(1)

    print(f"Rendered issue.md written to: {output_path}")
