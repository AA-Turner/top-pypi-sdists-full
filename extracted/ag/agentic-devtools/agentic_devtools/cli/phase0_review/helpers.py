"""Pure normalization and structural-comparison helpers."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from agentic_devtools.cli.phase0_review.config import FRONTMATTER_FIELDS

_ASCII_WHITESPACE = " \t\r\n\v\f"
_PLACEHOLDER = re.compile(r"\{\{([A-Za-z_][A-Za-z0-9_]*)\}\}")
_PLACEHOLDER_ONLY = re.compile(r"^\s*\{\{([A-Za-z_][A-Za-z0-9_]*)\}\}\s*$")
_KEY_LINE = re.compile(r"^([A-Za-z_][A-Za-z0-9_-]*):(?:\s|$)")


def normalize_text(value: str) -> str:
    """Normalize line endings and trim only the full value."""
    return value.replace("\r\n", "\n").replace("\r", "\n").strip(_ASCII_WHITESPACE)


def canonical_lines(value: str) -> list[str]:
    """Create the FR-010 canonical body line sequence."""
    normalized = value.replace("\r\n", "\n").replace("\r", "\n")
    result: list[str] = []
    blank = False
    for raw_line in normalized.split("\n"):
        line = raw_line.rstrip(_ASCII_WHITESPACE)
        if not line:
            if result and not blank:
                result.append("")
            blank = True
        else:
            result.append(line)
            blank = False
    while result and not result[-1]:
        result.pop()
    return result


def _canonical_records(value: str) -> list[tuple[str, list[str]]]:
    """Return canonical lines paired with the exact raw lines they represent."""
    normalized = value.replace("\r\n", "\n").replace("\r", "\n")
    records: list[tuple[str, list[str]]] = []
    for raw_line in normalized.split("\n"):
        canonical = raw_line.rstrip(_ASCII_WHITESPACE)
        if not canonical:
            if records:
                if records[-1][0]:
                    records.append(("", [raw_line]))
                else:
                    records[-1][1].append(raw_line)
        else:
            records.append((canonical, [raw_line]))
    while records and not records[-1][0]:
        records.pop()
    return records


def coerce_value(value: Any) -> str:
    """Apply the renderer's frozen scalar/array coercion."""
    if value is None:
        return ""
    if isinstance(value, list):
        return ", ".join(coerce_value(member) for member in value)
    return str(value)


def encode_table_cell(value: str) -> str:
    """Apply canonical two-column table-cell encoding."""
    return value.replace("\\", "\\\\").replace("|", "\\|").replace("\n", "<br>")


def resolve_safe_path(
    value: str,
    repo_root: Path,
    *,
    require_relative: bool,
) -> tuple[Path | None, str | None]:
    """Resolve a path while enforcing repository and .git boundaries."""
    candidate = Path(value)
    if require_relative and candidate.is_absolute():
        return None, "path must be repository-relative"
    candidate = candidate if candidate.is_absolute() else repo_root / candidate
    try:
        resolved = candidate.resolve(strict=False)
        root = repo_root.resolve(strict=True)
        relative = resolved.relative_to(root)
    except (OSError, ValueError):
        return None, "path resolves outside the repository boundary"
    if relative.parts and relative.parts[0] == ".git":
        return None, "path resolves within the .git subtree"
    return resolved, None


def split_frontmatter(document: str) -> tuple[str | None, str, str | None]:
    """Split a Markdown document into YAML frontmatter and body."""
    normalized = document.replace("\r\n", "\n").replace("\r", "\n")
    lines = normalized.split("\n")
    if not lines or lines[0] != "---":
        return None, normalized, "opening YAML frontmatter delimiter is missing"
    try:
        end = lines.index("---", 1)
    except ValueError:
        return None, normalized, "closing YAML frontmatter delimiter is missing"
    return "\n".join(lines[1:end]), "\n".join(lines[end + 1 :]), None


def frontmatter_validate(
    snapshot: str,
    issue_md: str,
) -> tuple[list[tuple[str, str]], dict[str, Any]]:
    """Validate YAML frontmatter delimiters, fields, and ordering."""
    snapshot_frontmatter, _, _ = split_frontmatter(snapshot)
    issue_frontmatter, _, delimiter_error = split_frontmatter(issue_md)
    if delimiter_error:
        return [("valid YAML frontmatter delimiters", delimiter_error)], {}
    if issue_frontmatter is None:
        return [("valid YAML frontmatter delimiters", "frontmatter was not extracted")], {}

    expected_order = list(FRONTMATTER_FIELDS)
    if snapshot_frontmatter is not None:
        snapshot_order = [
            match.group(1) for line in snapshot_frontmatter.split("\n") if (match := _KEY_LINE.match(line))
        ]
        if snapshot_order:
            expected_order = snapshot_order
    actual_order = [match.group(1) for line in issue_frontmatter.split("\n") if (match := _KEY_LINE.match(line))]
    findings: list[tuple[str, str]] = []
    for name in expected_order:
        if name not in actual_order:
            findings.append((f"frontmatter field {name!r} is present", "field is missing"))
    for name in dict.fromkeys(actual_order):
        if name not in expected_order:
            findings.append(("no unexpected frontmatter field", f"found field {name!r}"))
        elif actual_order.count(name) > 1:
            findings.append((f"frontmatter field {name!r} occurs once", "field is duplicated"))
    if actual_order != expected_order:
        findings.append(
            (
                f"frontmatter field order is {expected_order!r}",
                f"observed order is {actual_order!r}",
            )
        )
    try:
        parsed = yaml.safe_load(issue_frontmatter)
    except yaml.YAMLError as exc:
        findings.append(("frontmatter is valid YAML", f"YAML parsing failed: {exc}"))
        return findings, {}
    if not isinstance(parsed, dict):
        findings.append(("frontmatter is a mapping", f"found {type(parsed).__name__}"))
        return findings, {}
    return findings, parsed


def _source_value(name: str, source: dict[str, Any]) -> str:
    mapped = {"description": "body", "id": "issue_id"}.get(name, name)
    if mapped in source:
        return coerce_value(source[mapped])
    properties = source.get("properties")
    if isinstance(properties, dict) and mapped in properties:
        return coerce_value(properties[mapped])
    return ""


def _line_pattern(line: str) -> tuple[re.Pattern[str], list[str]]:
    names: list[str] = []
    pieces: list[str] = []
    cursor = 0
    for match in _PLACEHOLDER.finditer(line):
        pieces.append(re.escape(line[cursor : match.start()]))
        pieces.append("(.*?)")
        names.append(match.group(1))
        cursor = match.end()
    pieces.append(re.escape(line[cursor:]))
    return re.compile("^" + "".join(pieces) + "$"), names


def _is_table_route(line: str) -> bool:
    stripped = line.strip()
    return stripped.startswith("|") and stripped.endswith("|") and stripped.count("|") == 3


@dataclass
class StructuralResult:
    """Results of deterministic snapshot alignment."""

    findings: list[tuple[str, str]] = field(default_factory=list)
    malformed: list[tuple[str, str]] = field(default_factory=list)
    captures: dict[str, list[str]] = field(default_factory=dict)
    table_fields: set[str] = field(default_factory=set)


def structural_compare(
    snapshot: str,
    issue_md: str,
    source: dict[str, Any],
) -> StructuralResult:
    """Align snapshot and rendered body using FR-010 placeholder boundaries."""
    _, snapshot_body, _ = split_frontmatter(snapshot)
    _, issue_body, issue_error = split_frontmatter(issue_md)
    if issue_error:
        issue_body = issue_md.replace("\r\n", "\n").replace("\r", "\n")
    expected = canonical_lines(snapshot_body)
    observed_records = _canonical_records(issue_body)
    observed = [line for line, _ in observed_records]
    result = StructuralResult()
    si = 0
    oi = 0

    while si < len(expected):
        placeholder = _PLACEHOLDER_ONLY.match(expected[si])
        if placeholder:
            name = placeholder.group(1)
            if si + 1 < len(expected) and _PLACEHOLDER_ONLY.match(expected[si + 1]):
                result.malformed.append(
                    (
                        "structural snapshot has no adjacent placeholder-only lines",
                        f"adjacent placeholder-only lines begin with {expected[si]!r}",
                    )
                )
                si += 1
                continue
            if si + 1 == len(expected):
                boundary = len(observed)
            else:
                successor = expected[si + 1]
                pattern, _ = _line_pattern(successor)
                source_lines = canonical_lines(_source_value(name, source))
                source_count = sum(line == successor for line in source_lines)
                seen = 0
                boundary = len(observed)
                for index in range(oi, len(observed)):
                    if pattern.fullmatch(observed[index]):
                        seen += 1
                        if seen == source_count + 1:
                            boundary = index
                            break
                if boundary == len(observed):
                    result.findings.append(
                        (
                            f"structural line {successor!r} follows placeholder {name!r}",
                            "successor structural line is missing",
                        )
                    )
            raw_capture = [raw_line for _, raw_lines in observed_records[oi:boundary] for raw_line in raw_lines]
            result.captures.setdefault(name, []).append("\n".join(raw_capture))
            oi = boundary
            si += 1
            continue

        pattern, names = _line_pattern(expected[si])
        if oi >= len(observed):
            result.findings.append((f"structural line {expected[si]!r} is present", "line is missing"))
            si += 1
            continue
        match = pattern.fullmatch(observed[oi])
        if match:
            table_route = _is_table_route(expected[si])
            for index, name in enumerate(names, start=1):
                result.captures.setdefault(name, []).append(match.group(index))
                if table_route:
                    result.table_fields.add(name)
                elif "\n" in _source_value(name, source).replace("\r\n", "\n").replace("\r", "\n"):
                    result.malformed.append(
                        (
                            f"inline placeholder {name!r} resolves to single-line content",
                            "source field is multiline-capable",
                        )
                    )
            si += 1
            oi += 1
            continue
        result.findings.append(
            (
                f"structural line {expected[si]!r}",
                f"found {observed[oi]!r}",
            )
        )
        si += 1
        oi += 1

    for line in observed[oi:]:
        result.findings.append(("no extra structural line", f"found {line!r}"))
    return result
