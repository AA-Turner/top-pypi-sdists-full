"""Tests for the private timeout validator."""

import pytest

from agentic_devtools.cli.github.single_finding_dispatch_host import _validate_timeout


@pytest.mark.parametrize("timeout_seconds", [True, 0, -1, "1"])
def test_rejects_nonpositive_or_noninteger_values(timeout_seconds: object) -> None:
    with pytest.raises(ValueError, match="timeout_seconds"):
        _validate_timeout(timeout_seconds)  # type: ignore[arg-type]


def test_accepts_positive_integer() -> None:
    _validate_timeout(1)
