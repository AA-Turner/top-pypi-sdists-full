"""Path-based wrapper for issue.md rendering (FR-011).

Handles file I/O, type resolution, and timestamp generation, then delegates
to the pure ``render_issue`` core function.
"""

from __future__ import annotations

from datetime import datetime, timezone

from agentic_devtools.adapters.types import NormalizedIssue
from agentic_devtools.cli.issue_template._repo_paths import (
    _PRESET_DIR_RELATIVE,
    _find_repo_root,
)
from agentic_devtools.cli.issue_template.discovery import discover_templates
from agentic_devtools.cli.issue_template.renderer import PropertyConfig, render_issue
from agentic_devtools.cli.issue_template.type_resolver import resolve_issue_type


def render_issue_md(
    template_path: str,
    normalized_issue: NormalizedIssue,
    property_config: PropertyConfig | None = None,
) -> str:
    """Render an issue.md from a template file path and a NormalizedIssue.

    This is the public path-based API required by issue #1791. It reads the
    template file, resolves the issue type, generates a timestamp, and
    delegates to the pure ``render_issue`` core.

    Args:
        template_path: Path to the template file to read.
        normalized_issue: The normalized issue to render.
        property_config: Optional exclusion / mapping overrides. Its
            ``excluded_fields`` are applied directly and any
            ``property_section_mapping`` entries override the effective
            project-config mapping per key.

    Returns:
        The complete rendered issue.md content.

    Raises:
        OSError: If the template file cannot be read.
        PresetLoadError: If ``preset.yml`` is missing or cannot be parsed while
            discovering known types (propagated unchanged from
            ``discover_templates``).
        TemplateValidationError: If the effective project/explicit
            ``property_section_mapping`` is invalid, or if the resolved mapping
            conflicts with the template content.
        ValueError: If the project configuration contains an unrecognised
            ``config_mode`` value (propagated from
            ``resolve_effective_mapping``).
        Any exception raised by the type resolver propagates unchanged.
    """
    from pathlib import Path

    template_content = Path(template_path).read_text(encoding="utf-8")

    # Resolve the effective property-section mapping (project config + any
    # explicit override carried on ``property_config``) and thread it into a
    # populated ``PropertyConfig`` so the pure core honors project mappings.
    from agentic_devtools.cli.issue_template.mapping_resolver import resolve_effective_mapping

    explicit_mapping = dict(property_config.mapping) if property_config else None
    effective_mapping = resolve_effective_mapping(explicit_mapping)
    excluded_fields = property_config.excluded_fields if property_config else frozenset()
    resolved_config = PropertyConfig(
        excluded_fields=excluded_fields,
        property_section_mapping=effective_mapping or None,
    )

    # Resolve known types from preset directory
    repo_root = _find_repo_root()
    known_types: set[str] = set()
    if repo_root is not None:
        preset_dir = repo_root / _PRESET_DIR_RELATIVE
        if preset_dir.exists():
            templates_map, _ = discover_templates(preset_dir)
            known_types = set(templates_map.keys())

    # Resolve type — let exceptions propagate per FR-011
    type_slug = resolve_issue_type(normalized_issue, known_types)
    rendered_at = datetime.now(timezone.utc).isoformat()

    return render_issue(
        issue=normalized_issue,
        type_slug=type_slug,
        template_content=template_content,
        rendered_at=rendered_at,
        property_config=resolved_config,
    )
