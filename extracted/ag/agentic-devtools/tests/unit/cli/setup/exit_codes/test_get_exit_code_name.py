"""Tests for get_exit_code_name backward-compat wrapper."""

from agentic_devtools.cli.setup.exit_codes import ALL_EXIT_CODES, get_exit_code_name


class TestGetExitCodeName:
    """get_exit_code_name delegates to name_for."""

    def test_known_codes_return_name(self) -> None:
        for name, code in ALL_EXIT_CODES.items():
            assert get_exit_code_name(code) == name

    def test_unknown_code_returns_unknown_with_value(self) -> None:
        assert get_exit_code_name(999) == "UNKNOWN_999"

    def test_negative_code_returns_unknown_with_sign(self) -> None:
        assert get_exit_code_name(-1) == "UNKNOWN_-1"
