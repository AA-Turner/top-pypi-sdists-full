"""Tests for _as_bool."""

import pytest

from agentic_devtools.cli.suggestion_confirm import _as_bool


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (True, True),
        (False, False),
        ("true", True),
        ("True", True),
        ("yes", True),
        ("1", True),
        ("on", True),
        ("false", False),
        ("False", False),
        ("no", False),
        ("0", False),
        ("off", False),
    ],
)
def test_normalizes_boolean_inputs(value: object, expected: bool) -> None:
    assert _as_bool(value) is expected


@pytest.mark.parametrize(("default", "expected"), [(False, False), (True, True)])
def test_returns_default_for_none(default: bool, expected: bool) -> None:
    assert _as_bool(None, default=default) is expected


@pytest.mark.parametrize("value", ["maybe", "2", 2, [], object()])
def test_rejects_unrecognised_boolean_values(value: object) -> None:
    with pytest.raises(ValueError, match="Unrecognised boolean value"):
        _as_bool(value)
