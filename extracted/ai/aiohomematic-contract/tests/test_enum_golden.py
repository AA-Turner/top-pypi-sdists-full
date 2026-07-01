# SPDX-License-Identifier: MIT
# Copyright (c) 2021-2026
"""
Golden tests pinning the enum name→value maps.

aiohomematic imports these enums from this package; an alternative client keeps
its own copy. Both sides assert against these fixtures so the value sets cannot
silently drift. See ``docs/contract-gaps.md`` (P2).
"""

import json
from typing import Any, cast

from aiohomematic_contract import CommandPriority, DataPointCategory, DataPointType, golden_fixture_path


def _load(name: str) -> dict[str, Any]:
    """Load a name→value golden fixture (not the ``cases`` shape)."""
    return cast("dict[str, Any]", json.loads(golden_fixture_path(name).read_text(encoding="utf-8")))


def test_category_enums_match_golden() -> None:
    """Verify DataPointCategory/DataPointType values match the golden fixture."""
    data = _load("category")
    assert {m.name: m.value for m in DataPointCategory} == data["DataPointCategory"]
    assert {m.name: m.value for m in DataPointType} == data["DataPointType"]


def test_command_priority_matches_golden() -> None:
    """Verify CommandPriority values match the golden fixture."""
    data = _load("command")
    assert {m.name: m.value for m in CommandPriority} == data["CommandPriority"]
