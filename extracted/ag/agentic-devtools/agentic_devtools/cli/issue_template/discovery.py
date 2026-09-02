"""Template discovery from preset.yml.

Discovers registered issue templates from the preset directory and
provides type-specific template selection with fallback.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

import yaml

from agentic_devtools.cli.issue_template.exceptions import (
    PresetLoadError,
    TemplateNotFoundError,
)

_ISSUE_TYPE_PATTERN = re.compile(r"^issue-template-(.+)\.md$")
_DEFAULT_TEMPLATE_NAME = "issue-template.md"


def discover_templates(
    preset_dir: Path,
) -> tuple[dict[str, Path], Path | None]:
    """Discover registered issue templates from a preset directory.

    Reads ``preset.yml`` in the given directory and builds a slug-to-path
    map from entries matching ``issue-template-{type_slug}.md``. The default
    template ``issue-template.md`` is returned separately.

    Args:
        preset_dir: Path to the preset directory containing ``preset.yml``
            and a ``templates/`` subdirectory.

    Returns:
        A tuple of (type_slug -> template_path mapping, default_template_path or None).
        The default template is not included in the dict.

    Raises:
        PresetLoadError: If ``preset.yml`` is missing or cannot be parsed as
            valid YAML.
    """
    preset_file = preset_dir / "preset.yml"
    if not preset_file.exists():
        raise PresetLoadError(f"preset.yml not found in preset directory: {preset_dir}")

    try:
        with preset_file.open(encoding="utf-8") as file_handle:
            preset_data = yaml.safe_load(file_handle)
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        raise PresetLoadError(f"Could not parse preset.yml at {preset_file}: {exc}") from exc

    if not isinstance(preset_data, dict):
        return {}, None

    templates_value: Any = preset_data.get("templates")
    if not isinstance(templates_value, list):
        return {}, None

    templates_dir = preset_dir / "templates"
    templates_root = templates_dir.resolve()
    type_map: dict[str, Path] = {}
    default_template: Path | None = None
    seen_types: set[str] = set()

    for entry in templates_value:
        if not isinstance(entry, str):
            continue

        # Reject entries with path separators or dot-segments, and any entry
        # whose resolved path escapes the templates/ directory, to prevent
        # reading files outside templates/ (path traversal, FR-007).
        # Use explicit character checks rather than pathlib for the separator
        # guard so it is consistent across platforms (pathlib treats '\\' as a
        # separator on Windows but not on POSIX).
        if "/" in entry or "\\" in entry:
            print(
                f"Warning: Ignoring unsafe template path '{entry}' in preset.yml (path separators are not allowed).",
                file=sys.stderr,
            )
            continue

        if entry == ".":
            print(
                f"Warning: Ignoring unsafe template path '{entry}' in preset.yml (dot-segments are not allowed).",
                file=sys.stderr,
            )
            continue

        resolved_entry = (templates_dir / entry).resolve()
        if resolved_entry != templates_root and templates_root not in resolved_entry.parents:
            print(
                f"Warning: Ignoring unsafe template path '{entry}' in preset.yml "
                f"(path escapes the templates directory).",
                file=sys.stderr,
            )
            continue

        file_path = templates_dir / entry

        if entry == _DEFAULT_TEMPLATE_NAME:
            if file_path.exists() and file_path.is_file():
                default_template = file_path
            continue

        match = _ISSUE_TYPE_PATTERN.match(entry)
        if not match:
            continue

        type_slug = match.group(1)
        if type_slug in seen_types:
            print(
                f"Warning: Duplicate issue template type '{type_slug}' "
                f"in preset.yml; using first match, ignoring '{entry}'.",
                file=sys.stderr,
            )
            continue

        seen_types.add(type_slug)
        if file_path.exists() and file_path.is_file():
            type_map[type_slug] = file_path

    return type_map, default_template


def select_template(
    type_slug: str,
    templates: dict[str, Path],
    default_template: Path | None,
    preset_dir: Path | None = None,
) -> Path:
    """Select the appropriate template for the given type slug.

    Returns the type-specific template if available, otherwise the
    default template. Raises TemplateNotFoundError when neither is
    available.

    Args:
        type_slug: The resolved issue type slug.
        templates: The type-specific template map from discover_templates.
        default_template: The default template path (or None).
        preset_dir: Optional preset directory; used to produce a more helpful
            error message when no template is found.

    Returns:
        The path to the selected template file.

    Raises:
        TemplateNotFoundError: When no matching template is found.
    """
    if type_slug in templates:
        return templates[type_slug]

    if default_template is not None:
        return default_template

    preset_hint = f"'{preset_dir / 'preset.yml'}'" if preset_dir is not None else "preset.yml"
    raise TemplateNotFoundError(
        f"No template found for issue type '{type_slug}' and no default template "
        f"'issue-template.md' is registered. Ensure {preset_hint} lists "
        f"'issue-template.md' under the 'templates' key and the file exists "
        f"in the templates directory."
    )
