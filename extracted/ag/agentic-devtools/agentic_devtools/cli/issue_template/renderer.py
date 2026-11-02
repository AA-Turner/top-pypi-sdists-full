"""Pure rendering function for issue.md generation.

Produces YAML frontmatter followed by the resolved template body.
The renderer is pure (no I/O, no side effects, deterministic).
"""

from __future__ import annotations

import dataclasses
import re
from collections.abc import Callable, Mapping
from types import MappingProxyType
from typing import Any

from agentic_devtools.adapters.types import NormalizedIssue
from agentic_devtools.cli.issue_template.template_placeholders import (
    PLACEHOLDER_ALIASES as _PLACEHOLDER_ALIASES,
)
from agentic_devtools.cli.issue_template.template_placeholders import (
    PLACEHOLDER_RE as _PLACEHOLDER_RE,
)

# Backward-compatible module-level aliases: the canonical definitions now live
# in ``template_placeholders`` (single source of truth), but existing callers
# and tests import ``_PLACEHOLDER_RE`` / ``_PLACEHOLDER_ALIASES`` from here.

#: Canonical property keys that may only ever be mapped to ``frontmatter``.
#: ``issue_id`` is accepted as an alias for ``id`` during validation but is
#: normalized to ``id`` in the effective mapping.
FRONTMATTER_ONLY_KEYS: frozenset[str] = frozenset({"id", "title", "status", "provider", "labels"})

#: Canonical property keys that may target ``frontmatter``, ``body:<Section>``
#: or ``omit``.
CONFIGURABLE_KEYS: frozenset[str] = frozenset({"description", "url", "created_at", "updated_at"})

#: Canonical body section names that always render as two-column tables.
CANONICAL_SECTIONS: frozenset[str] = frozenset({"Metadata", "Properties", "Provenance"})

#: Free-text properties rendered as paragraphs (not bullets) in custom sections.
_FREE_TEXT_KEYS: frozenset[str] = frozenset({"description"})

#: Maximum length of a ``body:<Section>`` name after normalization.
SECTION_NAME_MAX_LENGTH = 128


def _display_label(key: str) -> str:
    """Return the deterministic display label for a canonical property key."""
    if key == "created_at":
        return "Created"
    if key == "updated_at":
        return "Updated"
    if key == "url":
        return "URL"
    return key.replace("_", " ").title()


@dataclasses.dataclass(frozen=True)
class PropertyConfig:
    """Configuration declaring which properties are excluded from rendering.

    Fields whose names appear in ``excluded_fields`` are cleanly omitted from
    the rendered body.  An empty ``excluded_fields`` means all properties are
    included.

    ``property_section_mapping`` is an optional constructor input accepting any
    ``Mapping[str, str]`` (canonical property name -> ``frontmatter`` /
    ``body:<Section>`` / ``omit``).  It is canonicalized to a sorted tuple
    snapshot (``_mapping_items``) so the config remains immutable, hashable, and
    value-equal regardless of input insertion order or later caller mutation.
    The read-only view is exposed via the :attr:`mapping` property, which does
    not participate in equality/hashing.
    """

    excluded_fields: frozenset[str] = dataclasses.field(default_factory=frozenset)
    property_section_mapping: dataclasses.InitVar[Mapping[str, str] | None] = None
    _mapping_items: tuple[tuple[str, str], ...] = dataclasses.field(default=(), init=False, repr=False)

    def __post_init__(self, property_section_mapping: Mapping[str, str] | None) -> None:
        object.__setattr__(self, "excluded_fields", frozenset(self.excluded_fields))
        if property_section_mapping is None:
            items: tuple[tuple[str, str], ...] = ()
        else:
            normalized_items: list[tuple[str, str]] = []
            for key, target in property_section_mapping.items():
                if not isinstance(key, str):
                    raise TypeError("property_section_mapping keys must be strings")
                if not isinstance(target, str):
                    raise TypeError(f'mapping target for "{key}" must be a string, got {type(target).__name__}')
                normalized_items.append((key, target))
            items = tuple(sorted(normalized_items))
        object.__setattr__(self, "_mapping_items", items)

    @property
    def mapping(self) -> Mapping[str, str]:
        """Return a read-only view of the canonicalized property-section mapping."""
        return MappingProxyType(dict(self._mapping_items))


def _coerce_value(value: Any) -> str:
    """Coerce a placeholder value to a string.

    Rules (per PropertyMapping entity spec):
    - None -> ""
    - list -> ", " joined
    - scalar -> str()
    """
    if value is None:
        return ""
    if isinstance(value, list):
        return ", ".join(str(item) for item in value)
    return str(value)


def _yaml_escape_scalar(value: str) -> str:
    """Escape a string value for YAML frontmatter (FR-005 always-quote).

    Always wraps in double quotes with deterministic escape sequences:
    - Backslash -> \\\\
    - Double-quote -> \\"
    - Newline -> \\n
    - Carriage return -> \\r
    - Tab -> \\t
    - Other control chars (U+0000-U+001F, U+007F) -> \\uXXXX
    """
    if not value:
        return '""'

    escaped_chars: list[str] = []
    for ch in value:
        if ch == "\\":
            escaped_chars.append("\\\\")
        elif ch == '"':
            escaped_chars.append('\\"')
        elif ch == "\n":
            escaped_chars.append("\\n")
        elif ch == "\r":
            escaped_chars.append("\\r")
        elif ch == "\t":
            escaped_chars.append("\\t")
        elif ("\x00" <= ch <= "\x1f") or ch == "\x7f":
            escaped_chars.append(f"\\u{ord(ch):04x}")
        else:
            escaped_chars.append(ch)

    return f'"{"".join(escaped_chars)}"'


# Keep backward-compatible name for existing callers/tests.
_escape_yaml_string = _yaml_escape_scalar


def _serialize_frontmatter(
    issue: NormalizedIssue,
    type_slug: str,
    rendered_at: str,
    extra_keys: list[str] | None = None,
) -> str:
    """Build YAML frontmatter block (FR-002, FR-005, FR-006).

    Emits the 7 required fields in fixed order, properly escaped.  Additional
    configurable properties mapped to ``frontmatter`` (``extra_keys``) are
    emitted after the required block in ascending canonical-name order, using
    the same always-quote/escape rules.
    """
    lines = ["---"]
    lines.append(f"id: {_yaml_escape_scalar(issue.issue_id)}")
    lines.append(f"title: {_yaml_escape_scalar(issue.title)}")
    lines.append(f"type: {_yaml_escape_scalar(type_slug)}")
    lines.append(f"status: {_yaml_escape_scalar(issue.status)}")
    lines.append(f"provider: {_yaml_escape_scalar(issue.provider)}")

    if issue.labels:
        lines.append("labels:")
        for label in issue.labels:
            lines.append(f"  - {_yaml_escape_scalar(label)}")
    else:
        lines.append("labels: []")

    lines.append(f"rendered_at: {_yaml_escape_scalar(rendered_at)}")

    for key in sorted(extra_keys or []):
        lines.append(f"{key}: {_yaml_escape_scalar(_resolve_placeholder(key, issue))}")

    lines.append("---")
    return "\n".join(lines)


def _resolve_placeholder(name: str, issue: NormalizedIssue) -> str:
    """Resolve a single placeholder name to its string value.

    Two-tier lookup (FR-003):
    1. Canonical NormalizedIssue fields (with alias resolution)
    2. Top-level raw dict keys

    Special aliases (via _PLACEHOLDER_ALIASES):
    - {{issue_id}} resolves to the canonical "id" -> issue.issue_id
    """
    # Resolve alias to canonical name
    resolved_name = _PLACEHOLDER_ALIASES.get(name, name)

    canonical_fields: dict[str, Any] = {
        "id": issue.issue_id,
        "title": issue.title,
        "description": issue.description,
        "status": issue.status,
        "url": issue.url,
        "provider": issue.provider,
        "labels": issue.labels,
        "created_at": issue.created_at,
        "updated_at": issue.updated_at,
    }

    if resolved_name in canonical_fields:
        return _coerce_value(canonical_fields[resolved_name])

    if resolved_name in issue.raw:
        return _coerce_value(issue.raw[resolved_name])

    return ""


def _expand_excluded_set(excluded_fields: frozenset[str]) -> frozenset[str]:
    """Expand excluded fields with alias equivalents.

    If 'id' is excluded, 'issue_id' is also excluded and vice versa.
    """
    expanded = set(excluded_fields)
    for alias, canonical in _PLACEHOLDER_ALIASES.items():
        if canonical in excluded_fields:
            expanded.add(alias)
        if alias in excluded_fields:
            expanded.add(canonical)
    return frozenset(expanded)


def _remove_excluded_lines(template_lines: list[str], excluded: frozenset[str]) -> list[str]:
    """Remove lines containing placeholders that belong to excluded fields (FR-010).

    A line is removed if it contains any {{field}} where field (or its alias-
    equivalent) is in the excluded set.
    """
    if not excluded:
        return list(template_lines)

    expanded = _expand_excluded_set(excluded)
    result: list[str] = []
    for line in template_lines:
        placeholders = _PLACEHOLDER_RE.findall(line)
        if placeholders:
            # Check if any placeholder on this line is excluded
            should_exclude = any(_PLACEHOLDER_ALIASES.get(p, p) in expanded or p in expanded for p in placeholders)
            if should_exclude:
                continue
        result.append(line)
    return result


def _cleanup_empty_tables(lines: list[str]) -> list[str]:
    """Remove markdown tables that have only header+separator and no data rows (FR-010 micro-pass 1).

    A table is: header row (contains |), separator row (matches |---...|),
    followed by zero or more data rows (contain |). If no data rows remain,
    the entire table (header+separator) is removed.
    """
    result: list[str] = []
    i = 0
    while i < len(lines):
        # Detect potential table start: line with |
        if "|" in lines[i]:
            # Check if next line is a separator
            if i + 1 < len(lines) and re.match(r"^\|[\s\-:|]+\|$", lines[i + 1].strip()):
                # We have header + separator. Count data rows.
                table_start = i
                i += 2  # skip header and separator
                has_data_rows = False
                while i < len(lines) and "|" in lines[i] and not lines[i].strip() == "":
                    has_data_rows = True
                    i += 1
                if has_data_rows:
                    # Keep entire table
                    result.extend(lines[table_start:i])
                # else: skip the table entirely (no data rows)
                continue
        result.append(lines[i])
        i += 1
    return result


def _get_heading_level_simple(line: str) -> int:
    """Return heading level (1-6) or 0 if not a heading (pre-CommonMark legacy variant).

    Strips all leading whitespace before checking for ``#`` markers.  This
    mirrors the behavior of the original ``_get_heading_level`` implementation
    that existed before CommonMark indented-code-block awareness was added.
    It is used exclusively by ``_cleanup_orphaned_headings`` so that the FR-010
    cleanup pass retains its pre-PR behavior and satisfies the SC-003 guarantee
    (no-mapping output is byte-identical to pre-PR output).
    """
    stripped = line.lstrip()
    if stripped.startswith("#"):
        level = 0
        for ch in stripped:
            if ch == "#":
                level += 1
            else:
                break
        if level <= 6 and (len(stripped) == level or stripped[level] == " "):
            return level
    return 0


def _cleanup_orphaned_headings(
    lines: list[str], *, heading_level_fn: Callable[[str], int] = _get_heading_level_simple
) -> list[str]:
    """Remove orphaned headings and bold-labels (FR-010 micro-pass 2).

    A heading (# ... ######) or bold-label (**Name**:) is orphaned if no data
    lines exist between it and the next heading of equal/higher level (or
    end-of-document). "Data lines" are non-blank lines that are not themselves
    headings/bold-labels.

    Uses ``heading_level_fn`` to classify heading lines. The default keeps the
    legacy SC-003 no-mapping behavior; mapping-aware callers can pass
    :func:`_get_heading_level` so CommonMark indented-code lines are treated as
    content rather than heading boundaries.
    """
    result: list[str] = []
    i = 0
    while i < len(lines):
        heading_level = heading_level_fn(lines[i])
        if heading_level > 0 or _is_bold_label(lines[i]):
            # Look ahead to determine if orphaned
            level = heading_level if heading_level > 0 else 7  # bold-labels treated as lowest level
            has_data = False
            j = i + 1
            while j < len(lines):
                next_level = heading_level_fn(lines[j])
                if next_level > 0 and next_level <= level:
                    break  # reached boundary
                if _is_bold_label(lines[j]):
                    break  # another label is also a boundary
                if lines[j].strip() and not (next_level > 0 or _is_bold_label(lines[j])):
                    has_data = True
                    break
                j += 1
            if has_data:
                result.append(lines[i])
            # else: orphaned, skip
        else:
            result.append(lines[i])
        i += 1
    return result


def _get_heading_level(line: str) -> int:
    """Return heading level (1-6) or 0 if not a heading.

    Lines with four or more leading spaces, or any tab in the indentation prefix,
    are indented-code blocks in CommonMark and are not recognized as headings.
    A single space or tab after the marker is accepted as heading whitespace.
    """
    if _is_commonmark_indented_code(line):
        return 0
    indent = 0
    while indent < len(line) and indent < 4 and line[indent] == " ":
        indent += 1
    stripped = line[indent:]
    if stripped.startswith("#"):
        level = 0
        for ch in stripped:
            if ch == "#":
                level += 1
            else:
                break
        if level <= 6 and (len(stripped) == level or stripped[level] in {" ", "\t"}):
            return level
    return 0


def _is_bold_label(line: str) -> bool:
    """Check if a line is an empty bold-label pattern like **Name**:."""
    stripped = line.strip()
    return bool(re.match(r"^\*\*[^*]+\*\*\s*:\s*$", stripped))


_FENCE_RE = re.compile(r"^ {0,3}(?P<marker>`{3,}|~{3,})")
_ASCII_WS = " \t\n\r\f\v"


def _is_commonmark_indented_code(line: str) -> bool:
    """Return True when ``line`` is an indented code-block line in CommonMark."""
    indent = 0
    while indent < len(line) and indent < 4 and line[indent] == " ":
        indent += 1
    return indent == 4 or (indent < len(line) and line[indent] == "\t")


def _compute_fence_flags(lines: list[str]) -> list[bool]:
    """Return flags identifying lines inside fenced code blocks."""
    flags: list[bool] = []
    fence_char: str | None = None
    fence_length = 0
    for line in lines:
        if fence_char is None:
            match = _FENCE_RE.match(line)
            is_fence = False
            if match is not None:
                marker = match.group("marker")
                # CommonMark §4.5: backtick fence info strings must not contain backticks.
                if marker[0] != "`" or "`" not in line[match.end() :]:
                    is_fence = True
                    fence_char = marker[0]
                    fence_length = len(marker)
            flags.append(is_fence)
            continue

        flags.append(True)
        stripped = line.lstrip(" ")
        candidate = stripped.rstrip(" \t\r")
        indent = len(line) - len(stripped)
        if indent <= 3 and len(candidate) >= fence_length and set(candidate) == {fence_char}:
            fence_char = None
            fence_length = 0
    return flags


def _heading_text(line: str) -> str:
    """Return the trimmed text of a markdown heading line.

    Strips an optional CommonMark closing hash sequence so that
    ``## Links ##`` and ``## Links`` both resolve to ``Links``.

    CommonMark closing sequence rules (applied to the already-stripped text):
    - ``Links ##``  → the hashes are preceded by whitespace → strip them → ``Links``
    - ``##``        → the entire text is only hashes (e.g. ``## ##``) → strip → ``""``
    """
    stripped = line.lstrip()
    level = _get_heading_level(line)
    if not level:
        return ""
    text = stripped[level:].strip()
    # Case 1: closing hashes preceded by whitespace, e.g. "Links ##" → "Links"
    text = re.sub(r"\s+#+\s*$", "", text)
    # Case 2: entire text is only hashes (e.g. "## ##" strips level+space, leaving "##")
    text = re.sub(r"^#+\s*$", "", text)
    return text


def _placeholder_names_for_key(key: str) -> set[str]:
    """Return every placeholder name (canonical + aliases) resolving to ``key``."""
    names = {key}
    for alias, canonical in _PLACEHOLDER_ALIASES.items():
        if canonical == key:
            names.add(alias)
        if alias == key:
            names.add(canonical)
    return names


def _line_has_key_placeholder(line: str, key: str) -> bool:
    """Return True when ``line`` contains a ``{{placeholder}}`` resolving to ``key``."""
    names = _placeholder_names_for_key(key)
    return any(p in names for p in _PLACEHOLDER_RE.findall(line))


def _find_section_spans(lines: list[str], fence_flags: list[bool], name: str) -> list[tuple[int, int]]:
    """Return ``(heading_idx, end_idx)`` spans for level-2 headings matching ``name``.

    Matching is exact and case-sensitive; fenced-code headings are ignored.
    ``end_idx`` is exclusive and stops at the next level-1/level-2 heading.
    """
    spans: list[tuple[int, int]] = []
    for i, line in enumerate(lines):
        if fence_flags[i] or _get_heading_level(line) != 2 or _heading_text(line) != name:
            continue
        end = len(lines)
        for j in range(i + 1, len(lines)):
            if fence_flags[j]:
                continue
            level = _get_heading_level(lines[j])
            if 0 < level <= 2:
                end = j
                break
        spans.append((i, end))
    return spans


def _row_cells(line: str) -> list[str]:
    """Return the stripped cells of a pipe-delimited table row.

    Only unescaped ``|`` characters are treated as cell delimiters; ``\\|``
    inside a cell is preserved as a literal pipe.

    Assumes a well-formed row whose stripped form starts and ends with ``|``
    (as produced by :func:`_is_table_row`).  The content between the outer
    pipes is scanned character-by-character; the trailing accumulator after
    the last real ``|`` delimiter contains the last cell (typically empty
    for a well-formed closing ``|``).
    """
    stripped = line.strip()
    inner = stripped[1:-1]
    cells: list[str] = []
    current: list[str] = []
    saw_internal_delimiter = False
    i = 0
    while i < len(inner):
        ch = inner[i]
        if ch == "|":
            bs = 0
            j = i - 1
            while j >= 0 and inner[j] == "\\":
                bs += 1
                j -= 1
            if bs % 2 == 0:
                cells.append("".join(current).strip())
                current = []
                saw_internal_delimiter = True
            else:
                current.append(ch)
            i += 1
            continue
        current.append(ch)
        i += 1
    trailing = "".join(current).strip()
    if trailing or saw_internal_delimiter:
        cells.append(trailing)
    return cells


def _is_table_row(line: str) -> bool:
    """Return True when a line is a pipe-delimited markdown table row."""
    stripped = line.strip()
    return len(stripped) >= 2 and stripped.startswith("|") and stripped.endswith("|")


def _is_delimiter_row(cells: list[str]) -> bool:
    """Return True when all cells are markdown table delimiter cells (``---``)."""
    return all(re.fullmatch(r":?-{3,}:?", c) is not None for c in cells) and len(cells) > 0


def _find_compatible_table(
    lines: list[str], fence_flags: list[bool], start: int, end: int
) -> tuple[int, int, int] | None:
    """Locate the first structurally compatible two-column table in ``[start, end)``.

    Returns ``(header_idx, delimiter_idx, last_data_idx)`` or ``None``. A
    compatible table is a two-column header row immediately followed by a
    ``| --- | --- |`` delimiter row.
    """
    i = start
    while i < end - 1:
        if not fence_flags[i] and not _is_commonmark_indented_code(lines[i]) and _is_table_row(lines[i]):
            if (
                not fence_flags[i + 1]
                and not _is_commonmark_indented_code(lines[i + 1])
                and len(_row_cells(lines[i])) == 2
                and _is_table_row(lines[i + 1])
            ):
                delim = _row_cells(lines[i + 1])
                if len(delim) == 2 and _is_delimiter_row(delim):
                    last = i + 1
                    k = i + 2
                    while (
                        k < end
                        and not fence_flags[k]
                        and not _is_commonmark_indented_code(lines[k])
                        and _is_table_row(lines[k])
                    ):
                        last = k
                        k += 1
                    return (i, i + 1, last)
        i += 1
    return None


def _encode_table_cell(value: str) -> str:
    """Encode a value for insertion into a markdown table cell (deterministic)."""
    value = value.replace("\\", "\\\\")
    value = value.replace("|", "\\|")
    value = value.replace("\r\n", "<br>").replace("\r", "<br>").replace("\n", "<br>")
    return value


def _last_content_index(lines: list[str], fence_flags: list[bool], start: int, end: int) -> int:
    """Return the index of the last non-blank content line in ``[start, end)``.

    Falls back to ``start`` (the heading) when the section is heading-only.
    """
    last = start
    for j in range(start + 1, end):
        if lines[j].strip():
            last = j
    return last


def _mapped_key_lookup(mapping: Mapping[str, str]) -> dict[str, str]:
    """Return a canonicalized ``{key: target}`` dict (aliases resolved to ``id``)."""
    resolved: dict[str, str] = {}
    for key, target in mapping.items():
        resolved[_PLACEHOLDER_ALIASES.get(key, key)] = target
    return resolved


def _placeholder_token(key: str) -> str:
    """Return the ``{{key}}`` placeholder token for an injected property.

    Injected lines carry the placeholder token rather than the resolved value so
    the value is substituted exactly once by the final resolution pass (like a
    retained in-place placeholder). This prevents literal ``{{...}}`` sequences
    inside user data from being re-scanned and wrongly re-resolved.
    """
    return "{{" + key + "}}"


def _canonical_table_row(key: str) -> str:
    """Build a ``| Label | {{key}} |`` canonical table row for ``key``.

    The value cell holds the placeholder token; the final resolution pass
    substitutes and table-cell-encodes it.
    """
    return f"| {_display_label(key)} | {_placeholder_token(key)} |"


def _synthesized_section_lines(section: str, keys: list[str]) -> list[str]:
    """Build the lines for a synthesized (absent) target section."""
    is_canonical = section in CANONICAL_SECTIONS
    lines = ["", f"## {section}"]
    if is_canonical:
        lines.append("| Property | Value |")
        lines.append("| --- | --- |")
        for key in _order_injection_keys(keys):
            lines.append(_canonical_table_row(key))
    else:
        lines.extend(_custom_injection_lines(keys, heading_only=True))
    return lines


def _order_injection_keys(keys: list[str]) -> list[str]:
    """Order keys: free-text properties first, then label/value ascending by name."""
    free = sorted(k for k in keys if k in _FREE_TEXT_KEYS)
    labelled = sorted(k for k in keys if k not in _FREE_TEXT_KEYS)
    return free + labelled


def _custom_injection_lines(keys: list[str], *, heading_only: bool) -> list[str]:
    """Build paragraph/bullet lines for a custom-section injection.

    Free-text properties render first as paragraphs, then label/value properties
    as a contiguous bullet list. Blank lines separate blocks; when the section is
    heading-only the first block sits directly under the heading. Each value is a
    ``{{key}}`` placeholder token resolved once by the final resolution pass.
    """
    free = sorted(k for k in keys if k in _FREE_TEXT_KEYS)
    labelled = sorted(k for k in keys if k not in _FREE_TEXT_KEYS)
    out: list[str] = []
    first = heading_only
    for key in free:
        if not first:
            out.append("")
        first = False
        out.append(_placeholder_token(key))
    if labelled:
        if not first:
            out.append("")
        for key in labelled:
            out.append(f"- {_display_label(key)}: {_placeholder_token(key)}")
    return out


def _line_blocks_retention(line: str, key: str, excluded_fields: frozenset[str]) -> bool:
    """Return True when ``line`` also carries an independently excluded placeholder."""
    if not excluded_fields:
        return False
    expanded = _expand_excluded_set(excluded_fields)
    key_names = _placeholder_names_for_key(key)
    for placeholder in _PLACEHOLDER_RE.findall(line):
        canonical = _PLACEHOLDER_ALIASES.get(placeholder, placeholder)
        if placeholder in key_names or canonical in key_names:
            continue
        if placeholder in expanded or canonical in expanded:
            return True
    return False


def _canonical_retained_index(
    lines: list[str], key: str, table: tuple[int, int, int] | None, excluded_fields: frozenset[str]
) -> int | None:
    """Return the data-row index retaining ``key``'s placeholder, or ``None``.

    Only a row with exactly two cells qualifies: a malformed three-or-more-cell
    row is skipped so that the injection path creates a canonical two-column
    row instead of updating an incompatible one.
    """
    if table is None:
        return None
    _, delim_idx, last_data_idx = table
    for i in range(delim_idx + 1, last_data_idx + 1):
        if (
            _line_has_key_placeholder(lines[i], key)
            and not _line_blocks_retention(lines[i], key, excluded_fields)
            and len(_row_cells(lines[i])) == 2
        ):
            return i
    return None


def _first_placeholder_in_span(
    lines: list[str],
    fence_flags: list[bool],
    key: str,
    start: int,
    end: int,
    excluded_fields: frozenset[str],
) -> int | None:
    """Return the first in-span line index with ``key``'s placeholder, or ``None``."""
    for i in range(start, end):
        if (
            not fence_flags[i]
            and not _is_commonmark_indented_code(lines[i])
            and _line_has_key_placeholder(lines[i], key)
            and not _line_blocks_retention(lines[i], key, excluded_fields)
        ):
            return i
    return None


def _apply_property_mapping(
    template_lines: list[str],
    mapping: Mapping[str, str],
    excluded_fields: frozenset[str],
) -> tuple[list[str], frozenset[str], list[str], list[str]]:
    """Apply the property-section mapping to the template lines (pure).

    Returns ``(new_lines, extra_removal_keys, frontmatter_extra_keys, synthesized_lines)`` where
    ``extra_removal_keys`` are keys whose remaining placeholder lines must be
    removed by the clean-exclusion pass (frontmatter/omit/stale-exclusion), and
    ``frontmatter_extra_keys`` are configurable keys to add to the YAML block.
    ``synthesized_lines`` are deferred absent-section lines that must be appended
    after cleanup and placeholder resolution so they cannot affect template-body
    cleanup decisions.
    """
    resolved = _mapped_key_lookup(mapping)
    mapped_keys = set(resolved)
    retention_exclusions = frozenset(
        _expand_excluded_set(frozenset(excluded_fields)) - _expand_excluded_set(frozenset(mapped_keys))
    )

    frontmatter_keys = {k for k, t in resolved.items() if t == "frontmatter"}
    omit_keys = {k for k, t in resolved.items() if t == "omit"}

    # Group body-mapped keys by their target section so multiple properties in
    # the same section are inserted together in deterministic order.
    sections_to_keys: dict[str, list[str]] = {}
    for key, target in resolved.items():
        if target.startswith("body:"):
            sections_to_keys.setdefault(target[len("body:") :], []).append(key)

    fence_flags = _compute_fence_flags(template_lines)

    # Lines removed for section-scoped body suppression (all occurrences except a
    # single retained in-place occurrence per body-mapped key).
    remove_indices: set[int] = set()
    insert_after: dict[int, list[str]] = {}
    synth_sections: dict[str, list[str]] = {}

    for section in sorted(sections_to_keys):
        keys = sections_to_keys[section]
        spans = _find_section_spans(template_lines, fence_flags, section)
        retained: dict[str, int] = {}

        if spans:
            heading_idx, end = spans[0]
            if section in CANONICAL_SECTIONS:
                table = _find_compatible_table(template_lines, fence_flags, heading_idx + 1, end)
                inject_keys: list[str] = []
                for key in _order_injection_keys(keys):
                    retained_idx = _canonical_retained_index(template_lines, key, table, retention_exclusions)
                    if retained_idx is not None:
                        retained[key] = retained_idx
                    else:
                        inject_keys.append(key)
                if inject_keys:
                    rows = [_canonical_table_row(k) for k in inject_keys]
                    if table is not None:
                        insert_after.setdefault(table[2], []).extend(rows)
                    else:
                        insert_after.setdefault(heading_idx, []).extend(
                            ["| Property | Value |", "| --- | --- |", *rows]
                        )
            else:
                append_keys = []
                for key in keys:
                    in_section = _first_placeholder_in_span(
                        template_lines, fence_flags, key, heading_idx, end, retention_exclusions
                    )
                    if in_section is not None:
                        retained[key] = in_section
                    else:
                        append_keys.append(key)
                if append_keys:
                    anchor = _last_content_index(template_lines, fence_flags, heading_idx, end)
                    insert_after.setdefault(anchor, []).extend(
                        _custom_injection_lines(append_keys, heading_only=(anchor == heading_idx))
                    )
        else:
            synth_sections[section] = list(keys)

        for key in keys:
            for i in range(len(template_lines)):
                if _line_has_key_placeholder(template_lines[i], key) and retained.get(key) != i:
                    remove_indices.add(i)

    # Keys whose *every* placeholder line is removed by the ordinary exclusion pass.
    stale_excluded = frozenset(excluded_fields) - _expand_excluded_set(frozenset(mapped_keys))
    extra_removal_keys = frozenset(frontmatter_keys | omit_keys | set(stale_excluded))

    # Rebuild lines: drop section-scoped removals, apply in-place injections.
    rebuilt: list[str] = []
    for i, line in enumerate(template_lines):
        if i not in remove_indices:
            rebuilt.append(line)
        for extra in insert_after.get(i, []):
            rebuilt.append(extra)

    synthesized_lines: list[str] = []
    for section in sorted(synth_sections, key=lambda s: (s.casefold(), s)):
        synthesized_lines.extend(_synthesized_section_lines(section, synth_sections[section]))

    frontmatter_extra = sorted(k for k in frontmatter_keys if k in CONFIGURABLE_KEYS)
    return rebuilt, extra_removal_keys, frontmatter_extra, synthesized_lines


def render_issue(
    issue: NormalizedIssue,
    type_slug: str,
    template_content: str,
    rendered_at: str,
    property_config: PropertyConfig | None = None,
) -> str:
    """Render a NormalizedIssue into an issue.md string.

    Produces YAML frontmatter followed by the resolved template body.
    The type_slug is used directly in the frontmatter type field —
    it is NOT re-derived from the issue (preserving purity and determinism).

    Args:
        issue: The normalized issue to render.
        type_slug: The resolved type slug (from resolve_issue_type).
        template_content: The raw template body content (no frontmatter).
        rendered_at: ISO-8601 timestamp for the rendered_at field.
        property_config: Optional exclusion / mapping configuration. When None,
            all properties are included and no mapping-derived transforms apply.

    Returns:
        The complete issue.md content with frontmatter and resolved body.

    Raises:
        TemplateValidationError: When a non-empty ``property_section_mapping``
            conflicts with the supplied template (see mapping validation guards).
    """
    excluded = property_config.excluded_fields if property_config else frozenset()
    mapping = dict(property_config.mapping) if property_config else {}

    template_lines = template_content.split("\n")
    frontmatter_extra: list[str] = []
    synthesized_lines: list[str] = []

    if mapping:
        # Deferred import to avoid a module-level import cycle.
        from agentic_devtools.cli.issue_template.mapping_validation import (
            validate_property_section_mapping,
            validate_template_content,
        )

        mapping = validate_property_section_mapping(mapping)
        validate_template_content(template_content, mapping)
        template_lines, extra_removal_keys, frontmatter_extra, synthesized_lines = _apply_property_mapping(
            template_lines, mapping, excluded
        )
        # Recompute the effective exclusion set: (excluded − mapped) ∪ omit.
        resolved = _mapped_key_lookup(mapping)
        mapped_keys = _expand_excluded_set(frozenset(resolved))
        omit_keys = frozenset(k for k, t in resolved.items() if t == "omit")
        excluded = (frozenset(excluded) - mapped_keys) | omit_keys | extra_removal_keys
    frontmatter = _serialize_frontmatter(issue, type_slug, rendered_at, frontmatter_extra)

    # Step 1: Remove lines containing excluded placeholders
    template_lines = _remove_excluded_lines(template_lines, excluded)

    # Step 2: Empty-table cleanup micro-pass
    template_lines = _cleanup_empty_tables(template_lines)

    # Step 3: Orphaned-heading cleanup micro-pass
    template_lines = _cleanup_orphaned_headings(
        template_lines,
        heading_level_fn=_get_heading_level if mapping else _get_heading_level_simple,
    )

    # Step 4: Resolve remaining placeholders
    encoded_rows = set()
    if mapping:
        encoded_keys = {
            key
            for key, target in _mapped_key_lookup(mapping).items()
            if target.startswith("body:") and target[len("body:") :] in CANONICAL_SECTIONS
        }
        encoded_rows = {
            idx
            for idx, line in enumerate(template_lines)
            if any(_line_has_key_placeholder(line, key) for key in encoded_keys)
        }

    resolved_lines: list[str] = []
    for idx, line in enumerate(template_lines):
        encode = idx in encoded_rows

        def replace_match(match: re.Match[str], _encode: bool = encode) -> str:
            name = match.group(1)
            value = _coerce_value(type_slug) if name == "type" else _resolve_placeholder(name, issue)
            return _encode_table_cell(value) if _encode else value

        resolved_lines.append(_PLACEHOLDER_RE.sub(replace_match, line))

    if synthesized_lines:
        for line in synthesized_lines:
            # Preserve synthesized heading lines verbatim; substitute only content rows.
            if line.startswith("## "):
                resolved_lines.append(line)
                continue
            encode = any(_line_has_key_placeholder(line, key) for key in encoded_keys)

            def replace_synth_match(match: re.Match[str], _encode: bool = encode) -> str:
                name = match.group(1)
                value = _coerce_value(type_slug) if name == "type" else _resolve_placeholder(name, issue)
                return _encode_table_cell(value) if _encode else value

            resolved_lines.append(_PLACEHOLDER_RE.sub(replace_synth_match, line))

    resolved_body = "\n".join(resolved_lines)

    return frontmatter + "\n" + resolved_body
