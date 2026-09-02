"""Tests for agentic_devtools.cli.setup.phase_0._parse_yes_no."""

import pytest

from agentic_devtools.cli.setup.phase_0 import _parse_yes_no


class TestParseYesNo:
    """Tests for _parse_yes_no helper."""

    def test_empty_string_returns_default_true(self) -> None:
        """Empty string returns default (True)."""
        assert _parse_yes_no("", True) is True

    def test_empty_string_returns_default_false(self) -> None:
        """Empty string returns default (False)."""
        assert _parse_yes_no("", False) is False

    def test_y_returns_true(self) -> None:
        """'y' returns True."""
        assert _parse_yes_no("y", False) is True

    def test_yes_returns_true(self) -> None:
        """'yes' returns True."""
        assert _parse_yes_no("yes", False) is True

    def test_Y_uppercase_returns_true(self) -> None:
        """'Y' (uppercase) returns True."""
        assert _parse_yes_no("Y", False) is True

    def test_YES_uppercase_returns_true(self) -> None:
        """'YES' (uppercase) returns True."""
        assert _parse_yes_no("YES", False) is True

    def test_n_returns_false(self) -> None:
        """'n' returns False."""
        assert _parse_yes_no("n", True) is False

    def test_no_returns_false(self) -> None:
        """'no' returns False."""
        assert _parse_yes_no("no", True) is False

    def test_N_uppercase_returns_false(self) -> None:
        """'N' (uppercase) returns False."""
        assert _parse_yes_no("N", True) is False

    def test_NO_uppercase_returns_false(self) -> None:
        """'NO' (uppercase) returns False."""
        assert _parse_yes_no("NO", True) is False

    def test_unrecognised_input_returns_default_true(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Unrecognised input returns default (True) and prints warning."""
        result = _parse_yes_no("maybe", True)
        assert result is True
        err = capsys.readouterr().err
        assert "Unrecognised input" in err
        assert "maybe" in err

    def test_unrecognised_input_returns_default_false(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Unrecognised input returns default (False) and prints warning."""
        result = _parse_yes_no("dunno", False)
        assert result is False
        err = capsys.readouterr().err
        assert "Unrecognised input" in err

    def test_whitespace_only_returns_default(self) -> None:
        """Whitespace-only input returns default."""
        assert _parse_yes_no("   ", False) is False

    def test_y_with_whitespace_returns_true(self) -> None:
        """'y' with surrounding whitespace returns True."""
        assert _parse_yes_no("  y  ", False) is True
