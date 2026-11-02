"""Tests for _as_bool."""

import pytest

from agentic_devtools.cli.pull_request_thread import (
    _as_bool,
)


class TestHelper:
    @pytest.mark.parametrize(
        ("value", "expected"),
        [
            (None, False),
            (True, True),
            (False, False),
            ("true", True),
            ("True", True),
            ("TRUE", True),
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
    def test_boolean_normalization(self, value: object, expected: bool) -> None:
        assert _as_bool(value) is expected

    @pytest.mark.parametrize("value", ["flase", "treu", "maybe", "2", 2, "yes sir"])
    def test_invalid_value_raises(self, value: object) -> None:
        with pytest.raises(ValueError, match="Unrecognised boolean value"):
            _as_bool(value)

    def test_none_with_custom_default(self) -> None:
        assert _as_bool(None, default=True) is True
