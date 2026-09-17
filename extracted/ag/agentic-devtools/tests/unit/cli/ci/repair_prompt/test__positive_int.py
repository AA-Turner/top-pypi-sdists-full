"""Tests for _positive_int()."""

from __future__ import annotations

import pytest

from agentic_devtools.cli.ci.repair_prompt import _positive_int


def test_returns_positive_integer() -> None:
    assert _positive_int(1, "value") == 1


@pytest.mark.parametrize("value", [0, -1, False, "1"])
def test_rejects_non_positive_integer_values(value: object) -> None:
    with pytest.raises(ValueError, match="value must be a positive integer"):
        _positive_int(value, "value")
