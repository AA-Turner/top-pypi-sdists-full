"""Deterministic source-to-rendered factual comparison."""

from __future__ import annotations

from collections import Counter
from typing import Any

from agentic_devtools.cli.phase0_review.config import RENDERER_METADATA_FIELDS, UNORDERED_FIELDS
from agentic_devtools.cli.phase0_review.helpers import (
    StructuralResult,
    coerce_value,
    encode_table_cell,
    normalize_text,
)
from agentic_devtools.cli.phase0_review.report import Finding, ambiguity, discrepancy, json_literal

_ALIASES = {"id": "issue_id", "description": "body"}
_NAMED_ARRAYS = {"labels", "dependencies", "constraints", "assignees"}


def _resolve_source(name: str, source: dict[str, Any]) -> tuple[Any, bool]:
    source_name = _ALIASES.get(name, name)
    if source_name in source:
        return source[source_name], True
    properties = source.get("properties")
    if isinstance(properties, dict) and source_name in properties:
        return properties[source_name], True
    return None, False


def _coerced_members(value: Any) -> list[str] | None:
    if not isinstance(value, list):
        return None
    return [coerce_value(member) for member in value]


def _expected_string(name: str, value: Any, *, table_cell: bool, source: dict[str, Any]) -> str:
    source_name = _ALIASES.get(name, name)
    if source_name == "constraints" and isinstance(value, list):
        rendered = ", ".join(normalize_text(member) for member in value)
    else:
        rendered = coerce_value(value)
    original_size = source.get("original_size")
    if (
        source_name == "body"
        and source.get("truncated") is True
        and isinstance(original_size, int)
        and not isinstance(original_size, bool)
    ):
        body_size = len(rendered.encode("utf-8"))
        annotation = f"[CONTENT_TRUNCATED: original_size={original_size} bytes, included={body_size} bytes]"
        rendered = f"{rendered}\n{annotation}"
    return encode_table_cell(rendered) if table_cell else rendered


def _is_ambiguous(value: Any) -> bool:
    members = _coerced_members(value)
    return members is not None and any(", " in member for member in members)


def _compare_one(
    name: str,
    actual: str,
    source: dict[str, Any],
    *,
    table_cell: bool,
    joined_placeholder: bool,
) -> Finding:
    value, present = _resolve_source(name, source)
    expected = _expected_string(name, value if present else None, table_cell=table_cell, source=source)
    source_name = _ALIASES.get(name, name)
    compared_actual = normalize_text(actual) if source_name == "constraints" else actual
    if joined_placeholder and _is_ambiguous(value):
        return ambiguity(
            name,
            'array member contains the non-injective joined-placeholder delimiter ", "',
        )
    if source_name in UNORDERED_FIELDS and isinstance(value, list) and not table_cell:
        actual_members = [] if not compared_actual else compared_actual.split(", ")
        passed = Counter(actual_members) == Counter(_coerced_members(value) or [])
    else:
        passed = compared_actual == expected
    if passed:
        return Finding("content", f"Field {json_literal(name)} matches", passed=True)
    return discrepancy(name, expected, compared_actual)


def compare_content(
    source: dict[str, Any],
    frontmatter: dict[str, Any],
    structure: StructuralResult,
) -> list[Finding]:
    """Compare fixed frontmatter and every snapshot-rendered source field."""
    findings: list[Finding] = []
    fixed = {
        "id": source.get("issue_id"),
        "title": source.get("title"),
        "type": source.get("type"),
        "status": source.get("status"),
        "provider": source.get("provider"),
        "labels": source.get("labels"),
    }
    for name, expected_value in fixed.items():
        if name not in frontmatter:
            continue
        observed_value = frontmatter[name]
        if name == "labels" and isinstance(observed_value, list) and isinstance(expected_value, list):
            passed = Counter(str(item) for item in observed_value) == Counter(expected_value)
            expected = ", ".join(expected_value)
            observed = ", ".join(str(item) for item in observed_value)
        else:
            expected = coerce_value(expected_value)
            observed = coerce_value(observed_value)
            passed = expected == observed
        findings.append(
            Finding("content", f"Field {json_literal(name)} matches", passed=True)
            if passed
            else discrepancy(name, expected, observed)
        )

    for name, captures in structure.captures.items():
        if name in RENDERER_METADATA_FIELDS:
            continue
        for actual in captures:
            findings.append(
                _compare_one(
                    name,
                    actual,
                    source,
                    table_cell=name in structure.table_fields,
                    joined_placeholder=name in _NAMED_ARRAYS
                    or (
                        isinstance(source.get("properties"), dict)
                        and name in source["properties"]
                        and isinstance(source["properties"][name], list)
                    ),
                )
            )
    return findings
