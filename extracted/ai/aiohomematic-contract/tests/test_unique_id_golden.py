# SPDX-License-Identifier: MIT
# Copyright (c) 2021-2026
"""
Validate the reference ``generate_unique_id`` against the golden fixture.

This proves the packaged fixture is internally consistent with the
algorithm-of-record. aiohomematic and py-openccu-loom-client run the same
fixture against their own implementations, so the routing-key format cannot
silently drift across repos.
"""

from typing import Any

from aiohomematic_contract import generate_unique_id, load_golden_cases
import pytest

_CASES: list[dict[str, Any]] = load_golden_cases("unique_id")


def test_fixture_not_empty() -> None:
    """Guard against a fixture that silently lost all its cases."""
    assert len(_CASES) >= 10


@pytest.mark.parametrize("case", _CASES)
def test_reference_matches_golden(case: dict[str, Any]) -> None:
    """Verify the reference implementation reproduces the golden output exactly."""
    result = generate_unique_id(
        central_id=case["central_id"],
        address=case["address"],
        parameter=case["parameter"],
        prefix=case["prefix"],
    )
    assert result == case["expected"]
