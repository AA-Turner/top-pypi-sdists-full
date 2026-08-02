# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors
"""Unit tests for the auto commit_granularity resolver."""

import pytest

from geneva.jobs.config import JobConfig
from geneva.runners.ray.pipeline import resolve_commit_granularity


@pytest.mark.parametrize(
    ("name", "configured", "num_fragments", "expected"),
    [
        # --- auto (configured=None): scales with fragment count -------------
        ("auto floor on tiny table", None, 10, 64),
        ("auto floor at crossover", None, 1_280, 64),
        ("auto scales just past crossover", None, 1_300, 65),
        ("auto on frag100 (11.6k)", None, 11_626, 582),
        ("auto on frag10 (116k)", None, 116_226, 5_812),
        ("auto ceils, never floors fraction", None, 1_281, 65),
        ("auto on zero fragments", None, 0, 64),
        # --- explicit override always wins ----------------------------------
        ("explicit below floor honored", 1, 116_226, 1),
        ("explicit mid honored", 100, 116_226, 100),
        ("explicit above auto honored", 10_000, 116_226, 10_000),
        ("explicit zero clamps to 1", 0, 50, 1),
    ],
)
def test_resolve_commit_granularity(name, configured, num_fragments, expected) -> None:
    assert resolve_commit_granularity(configured, num_fragments) == expected


def test_jobconfig_default_is_auto() -> None:
    assert JobConfig().commit_granularity is None


def test_jobconfig_explicit_value_preserved() -> None:
    assert JobConfig(commit_granularity=128).commit_granularity == 128
    assert JobConfig(commit_granularity="256").commit_granularity == 256
