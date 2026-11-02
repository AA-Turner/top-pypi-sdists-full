import pytest

from agentic_devtools.cli.suggestion_confirm import _positive_int


@pytest.mark.parametrize(("value", "expected"), [(1, 1), ("2", 2)])
def test_accepts_positive_int_inputs(value: object, expected: int) -> None:
    assert _positive_int(value, "field") == expected


@pytest.mark.parametrize("value", [True, [], "not-a-number", 0])
def test_rejects_invalid_positive_int_inputs(value: object) -> None:
    with pytest.raises(ValueError, match="field must be a positive integer"):
        _positive_int(value, "field")
