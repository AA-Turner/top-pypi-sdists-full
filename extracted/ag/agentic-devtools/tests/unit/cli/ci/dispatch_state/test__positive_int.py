import pytest

from agentic_devtools.cli.ci import dispatch_state as dispatch_state_module


def test_accepts_positive_integer_values() -> None:
    assert dispatch_state_module._positive_int(7, "value") == 7


def test_rejects_non_positive_or_non_integer_values() -> None:
    for value in (True, 0, -1, "7"):
        with pytest.raises(ValueError, match="value must be a positive integer"):
            dispatch_state_module._positive_int(value, "value")
