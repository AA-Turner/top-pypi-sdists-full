"""Tests for ``_parse_hierarchy_lock_metadata``."""

import pytest

from agentic_devtools.cli.speckit.scaffold_new_feature import _parse_hierarchy_lock_metadata


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ('{"pid": 123, "created_at": 1.5}', (123, 1.5)),
        ("not-json", (None, None)),
        ("[]", (None, None)),
        ('{"pid": true, "created_at": 1}', (None, 1.0)),
        ('{"pid": 123, "created_at": true}', (123, None)),
        ('{"pid": "123", "created_at": "1.5"}', (None, None)),
        ('{"pid": [], "created_at": []}', (None, None)),
    ],
)
def test_parses_only_numeric_owner_metadata(raw: str, expected: tuple[int | None, float | None]) -> None:
    assert _parse_hierarchy_lock_metadata(raw) == expected
