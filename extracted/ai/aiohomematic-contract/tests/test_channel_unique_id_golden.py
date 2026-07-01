# SPDX-License-Identifier: MIT
# Copyright (c) 2021-2026
"""
Golden test for ``generate_channel_unique_id`` — the channel-level routing key.

aiohomematic's second routing key (``Channel._unique_id``); the client rebuilds
it independently, so it must stay bit-identical. See ``docs/contract-gaps.md`` (P1).
"""

from typing import Any

from aiohomematic_contract import generate_channel_unique_id, load_golden_cases
import pytest

_CASES: list[dict[str, Any]] = load_golden_cases("channel_unique_id")


def test_fixture_not_empty() -> None:
    """Guard against the fixture silently losing all its cases."""
    assert len(_CASES) >= 5


@pytest.mark.parametrize("case", _CASES)
def test_channel_unique_id_matches_golden(case: dict[str, Any]) -> None:
    """Verify generate_channel_unique_id reproduces the golden output exactly."""
    result = generate_channel_unique_id(central_id=case["central_id"], address=case["address"])
    assert result == case["expected"]
