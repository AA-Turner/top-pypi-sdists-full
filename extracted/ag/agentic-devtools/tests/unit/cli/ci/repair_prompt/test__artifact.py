"""Tests for _artifact()."""

from __future__ import annotations

import pytest

from agentic_devtools.cli.ci.repair_prompt import _artifact


def test_returns_string_value() -> None:
    assert _artifact("value", "artifact") == "value"


def test_optional_none_returns_none() -> None:
    assert _artifact(None, "artifact", optional=True) is None


@pytest.mark.parametrize("value", [1, False, object(), None])
def test_rejects_non_string_values(value: object) -> None:
    with pytest.raises(ValueError, match="artifact must be a string"):
        _artifact(value, "artifact")
