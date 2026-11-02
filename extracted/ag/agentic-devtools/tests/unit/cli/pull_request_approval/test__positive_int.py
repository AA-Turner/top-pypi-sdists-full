from __future__ import annotations

import pytest

from agentic_devtools.cli import pull_request_approval as commands


@pytest.mark.parametrize("value", [True, [], "bad", 0, -1])
def test_rejects_invalid_values(value: object) -> None:
    with pytest.raises(ValueError, match="positive integer"):
        commands._positive_int(value, "number")


def test_accepts_string_integer() -> None:
    assert commands._positive_int("3", "number") == 3
