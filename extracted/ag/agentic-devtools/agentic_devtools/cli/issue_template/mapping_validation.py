"""Validation for ``property_section_mapping`` configuration and templates.

Two layers of validation live here (all failures raise
:class:`TemplateValidationError` so CLI/path callers surface a consistent,
actionable error before any rendering step):

1. **Config validation** — shape validation of the ``issueTemplate`` /
   ``issue_template`` block and the ``property_section_mapping`` object, followed
   by key/target validation and ``body:<Section>`` name normalization.
2. **Template-content validation** — guards that run against the raw template
   source *after* mapping resolution, rejecting ambiguous same-line duplicate
   placeholders, mixed-placeholder suppression lines, duplicate matched section
   headings, and mapped canonical placeholders located in table header/delimiter
   rows.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from agentic_devtools.cli.issue_template.exceptions import TemplateValidationError
from agentic_devtools.cli.issue_template.renderer import (
    _ASCII_WS,
    _PLACEHOLDER_ALIASES,
    _PLACEHOLDER_RE,
    CONFIGURABLE_KEYS,
    FRONTMATTER_ONLY_KEYS,
    SECTION_NAME_MAX_LENGTH,
    _compute_fence_flags,
    _find_section_spans,
    _is_commonmark_indented_code,
    _line_has_key_placeholder,
    _mapped_key_lookup,
    _placeholder_names_for_key,
)


def _json_type_name(value: Any) -> str:
    """Return the JSON type name for an actionable error message."""
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, list):
        return "array"
    if isinstance(value, dict):
        return "object"
    if isinstance(value, str):
        return "string"
    if isinstance(value, int) or isinstance(value, float):
        return "number"
    if value is None:
        return "null"
    return type(value).__name__


def _normalize_section_name(key: str, target: str) -> str:
    """Normalize and validate a ``body:<Section>`` target, returning the name."""
    name = target[len("body:") :].strip(_ASCII_WS)
    if not name:
        raise TemplateValidationError(f'mapping target for "{key}" has an empty body section name')
    for ch in name:
        if ch <= "\x1f" or ch == "\x7f":
            raise TemplateValidationError(f'body section name for "{key}" contains a control or DEL character')
    if "#" in name:
        raise TemplateValidationError(f'body section name for "{key}" must not contain "#"')
    if len(name) > SECTION_NAME_MAX_LENGTH:
        raise TemplateValidationError(
            f'body section name for "{key}" exceeds {SECTION_NAME_MAX_LENGTH}-character limit'
        )
    return name


def _validate_target(key: str, target: str, *, configurable: bool) -> str:
    """Validate a mapping target for a key, returning the canonical target."""
    if target == "frontmatter":
        return "frontmatter"
    if not configurable:
        raise TemplateValidationError(f'"{key}" can only be mapped to "frontmatter"; got "{target}"')
    if target == "omit":
        return "omit"
    if target.startswith("body:"):
        return f"body:{_normalize_section_name(key, target)}"
    raise TemplateValidationError(
        f'invalid mapping target "{target}" for "{key}"; must be "frontmatter", "body:<section>", or "omit"'
    )


def validate_property_section_mapping(mapping: Any) -> dict[str, str]:
    """Validate a ``property_section_mapping`` object, returning a canonical dict.

    Aliases (``issue_id`` -> ``id``) are normalized. Raises
    :class:`TemplateValidationError` for any malformed structure, unsupported
    key/target, invalid section name, or conflicting ``id``/``issue_id`` targets.
    """
    if not isinstance(mapping, dict):
        raise TemplateValidationError(f'"property_section_mapping" must be an object, got {_json_type_name(mapping)}')

    # Validate entry shape first so malformed structure is always reported before
    # semantic checks (alias conflict, key/target validation).
    for key, raw_target in mapping.items():
        if not isinstance(raw_target, str):
            raise TemplateValidationError(
                f'mapping target for "{key}" must be a string, got {_json_type_name(raw_target)}'
            )

    # Detect an ``id`` / ``issue_id`` alias conflict (after shape validation)
    # so the ambiguity is reported as a conflict rather than as a constrained-key
    # error on whichever alias is validated second.
    id_raw = mapping.get("id")
    issue_id_raw = mapping.get("issue_id")
    if "id" in mapping and "issue_id" in mapping and id_raw != issue_id_raw:
        raise TemplateValidationError(
            'conflicting targets for the "id" / "issue_id" alias pair; specify only one, or use the same target'
        )

    canonical: dict[str, str] = {}
    for key, raw_target in mapping.items():
        canonical_key = _PLACEHOLDER_ALIASES.get(key, key)
        if canonical_key in FRONTMATTER_ONLY_KEYS:
            target = _validate_target(key, raw_target, configurable=False)
        elif canonical_key in CONFIGURABLE_KEYS:
            target = _validate_target(key, raw_target, configurable=True)
        else:
            raise TemplateValidationError(
                f'"{key}" is not a configurable canonical property; '
                "raw template placeholders cannot be remapped via property_section_mapping"
            )
        canonical[canonical_key] = target

    return canonical


def validate_issue_template_block(block: Any, key_name: str) -> dict[str, str]:
    """Validate an ``issueTemplate`` / ``issue_template`` block's shape.

    Returns the canonical ``property_section_mapping`` (empty when the mapping
    key is absent or ``null``).
    """
    if not isinstance(block, dict):
        raise TemplateValidationError(f'"{key_name}" must be an object, got {_json_type_name(block)}')
    mapping = block.get("property_section_mapping")
    if mapping is None:
        return {}
    return validate_property_section_mapping(mapping)


def _is_table_delimiter_or_header(lines: list[str], idx: int, fence_flags: list[bool]) -> bool:
    """Return True when ``lines[idx]`` is a header or delimiter row of a 2-col table."""
    from agentic_devtools.cli.issue_template.renderer import _is_delimiter_row, _is_table_row, _row_cells

    if (
        fence_flags[idx]
        or _is_commonmark_indented_code(lines[idx])
        or not _is_table_row(lines[idx])
        or len(_row_cells(lines[idx])) != 2
    ):
        return False
    cells = _row_cells(lines[idx])
    # Delimiter row?
    if _is_delimiter_row(cells):
        return True
    if any(_PLACEHOLDER_RE.findall(cell) for cell in cells) and any(
        _is_delimiter_row([cell]) for cell in cells if not _PLACEHOLDER_RE.findall(cell)
    ):
        return True
    # Header row: followed by a delimiter row.
    nxt = idx + 1
    return (
        nxt < len(lines)
        and not fence_flags[nxt]
        and not _is_commonmark_indented_code(lines[nxt])
        and _is_table_row(lines[nxt])
        and _is_delimiter_row(_row_cells(lines[nxt]))
    )


def _is_placeholder_delimiter_candidate(lines: list[str], idx: int, fence_flags: list[bool]) -> bool:
    """Return True when ``lines[idx]`` resembles a malformed delimiter row with a placeholder."""
    from agentic_devtools.cli.issue_template.renderer import _is_delimiter_row, _is_table_row, _row_cells

    if fence_flags[idx] or _is_commonmark_indented_code(lines[idx]) or not _is_table_row(lines[idx]):
        return False
    cells = _row_cells(lines[idx])
    if not any(_PLACEHOLDER_RE.findall(cell) for cell in cells) or not any(
        _is_delimiter_row([cell]) for cell in cells if not _PLACEHOLDER_RE.findall(cell)
    ):
        return False
    if (
        idx == 0
        or fence_flags[idx - 1]
        or _is_commonmark_indented_code(lines[idx - 1])
        or not _is_table_row(lines[idx - 1])
    ):
        return False
    previous_cells = _row_cells(lines[idx - 1])
    if len(previous_cells) != len(cells) or _is_delimiter_row(previous_cells):
        return False
    if idx >= 2 and not fence_flags[idx - 2] and not _is_commonmark_indented_code(lines[idx - 2]):
        if _is_table_row(lines[idx - 2]):
            earlier_cells = _row_cells(lines[idx - 2])
            if len(earlier_cells) == len(cells) and _is_delimiter_row(earlier_cells):
                return False
    return True


def _retained_body_placeholder_lines(
    lines: list[str], fence_flags: list[bool], mapping: Mapping[str, str]
) -> dict[str, int]:
    """Return the single in-template retained line for each ``body:<section>`` key."""
    retained: dict[str, int] = {}
    by_section: dict[str, list[str]] = {}
    for key, target in mapping.items():
        if target.startswith("body:"):
            by_section.setdefault(target[len("body:") :], []).append(key)

    for section in sorted(by_section):
        keys = by_section[section]
        spans = _find_section_spans(lines, fence_flags, section)
        if not spans:
            continue
        heading_idx, end = spans[0]
        if section in {"Metadata", "Properties", "Provenance"}:
            from agentic_devtools.cli.issue_template.renderer import _canonical_retained_index, _find_compatible_table

            table = _find_compatible_table(lines, fence_flags, heading_idx + 1, end)
            for key in keys:
                retained_idx = _canonical_retained_index(lines, key, table, frozenset())
                if retained_idx is not None:
                    retained[key] = retained_idx
        else:
            for key in keys:
                for i in range(heading_idx, end):
                    if (
                        not fence_flags[i]
                        and not _is_commonmark_indented_code(lines[i])
                        and _line_has_key_placeholder(lines[i], key)
                    ):
                        retained[key] = i
                        break
    return retained


def validate_template_content(template_content: str, mapping: Mapping[str, str]) -> None:
    """Validate a template against a non-empty effective mapping (FR-005 guards).

    Raises :class:`TemplateValidationError` for:
      (a) same-line duplicate placeholder for a ``body:<section>``-mapped key;
      (b) a line-removing suppression that would drop a co-located placeholder;
      (c) duplicate matched target section headings;
      (d) a mapped canonical placeholder inside a table header/delimiter row.
    """
    resolved = _mapped_key_lookup(mapping)
    lines = template_content.split("\n")
    fence_flags = _compute_fence_flags(lines)
    retained = _retained_body_placeholder_lines(lines, fence_flags, resolved)

    body_keys = {k for k, t in resolved.items() if t.startswith("body:")}

    for idx, line in enumerate(lines):
        found = _PLACEHOLDER_RE.findall(line)
        if not found:
            continue
        canonical_found = [_PLACEHOLDER_ALIASES.get(p, p) for p in found]

        # (a) same-line duplicate placeholder for a body-mapped key.
        for key in body_keys:
            names = _placeholder_names_for_key(key)
            if sum(1 for p in found if p in names) >= 2:
                raise TemplateValidationError(
                    f'"{key}" placeholder appears multiple times on line {idx + 1}; '
                    "each placeholder may appear at most once per line when mapped to a body section"
                )

        # (b) mixed-placeholder line the suppression pass would remove.
        removing = [
            key
            for key in canonical_found
            if (target := resolved.get(key)) in {"frontmatter", "omit"}
            or (target is not None and target.startswith("body:") and retained.get(key) != idx)
        ]
        distinct = set(canonical_found)
        if removing and len(distinct) >= 2:
            others = sorted(distinct - {removing[0]})
            raise TemplateValidationError(
                f'"{removing[0]}" and "{others[0]}" placeholders share line {idx + 1}; '
                "a line containing a remapped placeholder may not contain another placeholder"
            )

    # (c) duplicate matched target section headings.
    for key, target in resolved.items():
        if not target.startswith("body:"):
            continue
        section = target[len("body:") :]
        spans = _find_section_spans(lines, fence_flags, section)
        if len(spans) > 1:
            raise TemplateValidationError(
                f"Duplicate section '## {section}' in template; each section heading "
                "must be unique when property_section_mapping is configured"
            )
        # (d) mapped canonical placeholder in a table header/delimiter row.
        if spans and section in {"Metadata", "Properties", "Provenance"}:
            heading_idx, end = spans[0]
            selected_header_idx: int | None = None
            selected_delimiter_idx: int | None = None
            from agentic_devtools.cli.issue_template.renderer import _find_compatible_table

            selected_table = _find_compatible_table(lines, fence_flags, heading_idx + 1, end)
            if selected_table is not None:
                selected_header_idx, selected_delimiter_idx, _ = selected_table
            for i in range(heading_idx + 1, end):
                if not _line_has_key_placeholder(lines[i], key):
                    continue
                if selected_table is None and _is_placeholder_delimiter_candidate(lines, i, fence_flags):
                    raise TemplateValidationError(
                        f'"{key}" placeholder appears in a row that also contains a delimiter cell in the '
                        f"canonical {section} table; mapped canonical placeholders must appear only in data rows"
                    )
                if i in {selected_header_idx, selected_delimiter_idx} and _is_table_delimiter_or_header(
                    lines, i, fence_flags
                ):
                    raise TemplateValidationError(
                        f'"{key}" placeholder appears in the header or delimiter row of the '
                        f"canonical {section} table; mapped canonical placeholders must appear only in data rows"
                    )
