"""Tests for the _json_type_name helper (actionable error type names)."""

from __future__ import annotations

import pytest

from agentic_devtools.cli.issue_template.mapping_validation import _json_type_name


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (True, "boolean"),
        ([1], "array"),
        ({"a": 1}, "object"),
        ("s", "string"),
        (42, "number"),
        (3.14, "number"),
        (None, "null"),
    ],
)
def test_json_type_name(value: object, expected: str) -> None:
    assert _json_type_name(value) == expected


def test_json_type_name_fallback() -> None:
    """An exotic type falls back to the Python type name."""

    class Weird:
        pass

    assert _json_type_name(Weird()) == "Weird"
