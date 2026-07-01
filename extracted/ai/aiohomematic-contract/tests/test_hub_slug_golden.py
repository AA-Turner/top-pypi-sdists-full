# SPDX-License-Identifier: MIT
# Copyright (c) 2021-2026
"""
Golden test for ``hub_slug`` — the hub data-point name slug rule.

aiohomematic slugifies hub data-point names with python-slugify before building
their ``unique_id``. A consumer using a naive cleaner diverges on non-ASCII
names, so this pins the rule. See ``docs/contract-gaps.md`` (P0b).
"""

from typing import Any

from aiohomematic_contract import hub_slug, load_golden_cases
import pytest

_CASES: list[dict[str, Any]] = load_golden_cases("hub_slug")


def test_fixture_not_empty() -> None:
    """Guard against the fixture silently losing all its cases."""
    assert len(_CASES) >= 5


@pytest.mark.parametrize("case", _CASES)
def test_hub_slug_matches_golden(case: dict[str, Any]) -> None:
    """Verify hub_slug reproduces the golden slug exactly (incl. transliteration)."""
    assert hub_slug(case["name"]) == case["slug"]
