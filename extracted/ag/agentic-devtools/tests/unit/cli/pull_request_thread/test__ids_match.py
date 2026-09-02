"""Tests for _ids_match."""

import pytest

from agentic_devtools.cli.pull_request_thread import _ids_match


class TestIdsMatch:
    """Validate int/str tolerant comparison for discussion-ID reconciliation."""

    @pytest.mark.parametrize(
        "api_value,request_value",
        [
            (34, 34),
            (34, "34"),
            ("34", 34),
            ("34", "34"),
        ],
    )
    def test_matches_when_values_are_equal(self, api_value: object, request_value: int | str) -> None:
        assert _ids_match(api_value, request_value) is True

    @pytest.mark.parametrize(
        "api_value,request_value",
        [
            (34, 35),
            (34, "35"),
            ("34", 35),
        ],
    )
    def test_does_not_match_when_values_differ(self, api_value: object, request_value: int | str) -> None:
        assert _ids_match(api_value, request_value) is False

    @pytest.mark.parametrize(
        "api_value,request_value",
        [
            (True, 1),
            (True, "1"),
            (False, 0),
            (False, "0"),
            (1, True),
        ],
    )
    def test_returns_false_for_boolean_values(self, api_value: object, request_value: int | str) -> None:
        assert _ids_match(api_value, request_value) is False

    @pytest.mark.parametrize(
        "api_value,request_value",
        [
            (None, 34),
            ("not-a-number", 34),
            (34, "not-a-number"),
        ],
    )
    def test_returns_false_for_non_numeric_values(self, api_value: object, request_value: int | str) -> None:
        assert _ids_match(api_value, request_value) is False
