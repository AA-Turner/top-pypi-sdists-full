# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

from unittest.mock import patch

import pytest

from geneva.tqdm import (
    Colors,
    TqdmMode,
    fmt,
    fmt_numeric,
    fmt_pending,
    fmt_status_badge,
    supports_color,
)


class TestTqdmMode:
    """Test TqdmMode enum functionality."""

    def test_tqdm_mode_values(self) -> None:
        """Test that TqdmMode enum has expected values."""
        assert TqdmMode.AUTO.value == "auto"
        assert TqdmMode.SLACK.value == "slack"
        assert TqdmMode.RICH.value == "rich"
        assert TqdmMode.STD.value == "std"
        assert TqdmMode.NOTEBOOK.value == "notebook"

    def test_from_str(self) -> None:
        """Test TqdmMode.from_str conversion."""
        assert TqdmMode.from_str("auto") == TqdmMode.AUTO
        assert TqdmMode.from_str("std") == TqdmMode.STD
        assert TqdmMode.from_str("notebook") == TqdmMode.NOTEBOOK
        assert TqdmMode.from_str("rich") == TqdmMode.RICH
        assert TqdmMode.from_str("slack") == TqdmMode.SLACK

    def test_from_str_invalid(self) -> None:
        """Test TqdmMode.from_str with invalid value."""
        with pytest.raises(ValueError, match="'invalid' is not a valid TqdmMode"):
            TqdmMode.from_str("invalid")


class TestSupportsColor:
    """Test supports_color function with different tqdm modules."""

    def test_supports_color_std_module(self) -> None:
        """Test supports_color returns True for std module."""
        with patch("geneva.tqdm.tqdm") as mock_tqdm:
            mock_tqdm.__module__ = "tqdm.std"
            assert supports_color() is True

    def test_supports_color_asyncio_module(self) -> None:
        """Test supports_color returns True for asyncio module."""
        with patch("geneva.tqdm.tqdm") as mock_tqdm:
            mock_tqdm.__module__ = "tqdm.asyncio"
            assert supports_color() is True

    def test_supports_color_notebook_module(self) -> None:
        """Test supports_color returns False for notebook module."""
        with patch("geneva.tqdm.tqdm") as mock_tqdm:
            mock_tqdm.__module__ = "tqdm.notebook"
            assert supports_color() is False

    def test_supports_color_rich_module(self) -> None:
        """Test supports_color returns False for rich module."""
        with patch("geneva.tqdm.tqdm") as mock_tqdm:
            mock_tqdm.__module__ = "tqdm.rich"
            assert supports_color() is True

    def test_supports_color_auto_module(self) -> None:
        """Test supports_color returns False for auto module."""
        with patch("geneva.tqdm.tqdm") as mock_tqdm:
            mock_tqdm.__module__ = "tqdm.auto"
            assert supports_color() is False


class TestFmtFunction:
    """Test fmt function behavior in different modes."""

    def test_fmt_with_color_support(self) -> None:
        """Test fmt applies colors when color is supported."""
        with patch("geneva.tqdm.supports_color", return_value=True):
            result = fmt("test", Colors.RED)
            expected = f"{Colors.RED}test{Colors.RESET}"
            assert result == expected

    def test_fmt_with_bold_and_color_support(self) -> None:
        """Test fmt applies bold and color when supported."""
        with patch("geneva.tqdm.supports_color", return_value=True):
            result = fmt("test", Colors.BLUE, bold=True)
            expected = f"{Colors.BOLD}{Colors.BLUE}test{Colors.RESET}"
            assert result == expected

    def test_fmt_without_color_support(self) -> None:
        """Test fmt returns plain text when color is not supported."""
        with patch("geneva.tqdm.supports_color", return_value=False):
            result = fmt("test", Colors.RED, bold=True)
            assert result == "test"

    def test_fmt_std_mode_has_colors(self) -> None:
        """Test fmt uses colors in STD mode."""
        with patch("geneva.tqdm.tqdm") as mock_tqdm:
            mock_tqdm.__module__ = "tqdm.std"
            result = fmt("test", Colors.GREEN)
            expected = f"{Colors.GREEN}test{Colors.RESET}"
            assert result == expected

    def test_fmt_notebook_mode_no_colors(self) -> None:
        """Test fmt does not use colors in NOTEBOOK mode."""
        with patch("geneva.tqdm.tqdm") as mock_tqdm:
            mock_tqdm.__module__ = "tqdm.notebook"
            result = fmt("test", Colors.GREEN, bold=True)
            assert result == "test"

    def test_fmt_different_colors(self) -> None:
        """Test fmt with different color codes."""
        with patch("geneva.tqdm.supports_color", return_value=True):
            # Test basic colors
            assert fmt("red", Colors.RED) == f"{Colors.RED}red{Colors.RESET}"
            assert fmt("green", Colors.GREEN) == f"{Colors.GREEN}green{Colors.RESET}"
            assert fmt("blue", Colors.BLUE) == f"{Colors.BLUE}blue{Colors.RESET}"

            # Test bright colors
            assert (
                fmt("bright_red", Colors.BRIGHT_RED)
                == f"{Colors.BRIGHT_RED}bright_red{Colors.RESET}"
            )
            assert (
                fmt("bright_green", Colors.BRIGHT_GREEN)
                == f"{Colors.BRIGHT_GREEN}bright_green{Colors.RESET}"
            )
            assert (
                fmt("bright_blue", Colors.BRIGHT_BLUE)
                == f"{Colors.BRIGHT_BLUE}bright_blue{Colors.RESET}"
            )


class TestFmtStatusBadge:
    """Test fmt_status_badge function."""

    def test_fmt_status_badge_running(self) -> None:
        """Test status badge for running state."""
        with patch("geneva.tqdm.supports_color", return_value=True):
            result = fmt_status_badge("RUNNING")
            expected = f"{Colors.BOLD}{Colors.BRIGHT_GREEN}running{Colors.RESET}"
            assert result == expected

    def test_fmt_status_badge_pending(self) -> None:
        """Test status badge for pending state."""
        with patch("geneva.tqdm.supports_color", return_value=True):
            result = fmt_status_badge("PENDING")
            expected = f"{Colors.BOLD}{Colors.BRIGHT_YELLOW}pending{Colors.RESET}"
            assert result == expected

    def test_fmt_status_badge_failed(self) -> None:
        """Test status badge for failed state."""
        with patch("geneva.tqdm.supports_color", return_value=True):
            result = fmt_status_badge("FAILED")
            expected = f"{Colors.BOLD}{Colors.BRIGHT_RED}failed{Colors.RESET}"
            assert result == expected

    def test_fmt_status_badge_unknown_status(self) -> None:
        """Test status badge for unknown status uses default color."""
        with patch("geneva.tqdm.supports_color", return_value=True):
            result = fmt_status_badge("UNKNOWN")
            expected = f"{Colors.BOLD}{Colors.CYAN}unknown{Colors.RESET}"
            assert result == expected

    def test_fmt_status_badge_empty_status(self) -> None:
        """Test status badge for empty status."""
        result = fmt_status_badge("")
        assert result == ""

    def test_fmt_status_badge_without_color_support(self) -> None:
        """Test status badge without color support."""
        with patch("geneva.tqdm.supports_color", return_value=False):
            result = fmt_status_badge("RUNNING")
            assert result == "running"


class TestFmtNumeric:
    """Test fmt_numeric function."""

    def test_fmt_numeric_with_total_complete(self) -> None:
        """Test fmt_numeric when value equals total (complete)."""
        with patch("geneva.tqdm.supports_color", return_value=True):
            result = fmt_numeric(5, 5)
            expected = f"{Colors.BRIGHT_GREEN}5{Colors.RESET}"
            assert result == expected

    def test_fmt_numeric_with_total_incomplete(self) -> None:
        """Test fmt_numeric when value is less than total (incomplete)."""
        with patch("geneva.tqdm.supports_color", return_value=True):
            result = fmt_numeric(3, 5)
            expected = f"{Colors.BRIGHT_RED}3{Colors.RESET}"
            assert result == expected

    def test_fmt_numeric_without_total_nonzero(self) -> None:
        """Test fmt_numeric without total and non-zero value."""
        with patch("geneva.tqdm.supports_color", return_value=True):
            result = fmt_numeric(5)
            expected = f"{Colors.BRIGHT_GREEN}5{Colors.RESET}"
            assert result == expected

    def test_fmt_numeric_without_total_zero(self) -> None:
        """Test fmt_numeric without total and zero value."""
        with patch("geneva.tqdm.supports_color", return_value=True):
            result = fmt_numeric(0)
            expected = f"{Colors.BRIGHT_RED}0{Colors.RESET}"
            assert result == expected

    def test_fmt_numeric_none_values(self) -> None:
        """Test fmt_numeric with None values."""
        with patch("geneva.tqdm.supports_color", return_value=True):
            result = fmt_numeric(None, None)
            expected = f"{Colors.BRIGHT_RED}0{Colors.RESET}"
            assert result == expected

    def test_fmt_numeric_without_color_support(self) -> None:
        """Test fmt_numeric without color support."""
        with patch("geneva.tqdm.supports_color", return_value=False):
            result = fmt_numeric(5, 10)
            assert result == "5"

    def test_fmt_numeric_exception_handling(self) -> None:
        """Test fmt_numeric handles exceptions gracefully."""
        with patch("geneva.tqdm.supports_color", side_effect=Exception("test error")):
            result = fmt_numeric(5, 10)
            assert result == Colors.BRIGHT_GREEN


class TestFmtPending:
    """Test fmt_pending function."""

    def test_fmt_pending_zero(self) -> None:
        """Test fmt_pending with zero pending items."""
        with patch("geneva.tqdm.supports_color", return_value=True):
            result = fmt_pending(0)
            expected = f"{Colors.BRIGHT_GREEN}0{Colors.RESET}"
            assert result == expected

    def test_fmt_pending_nonzero(self) -> None:
        """Test fmt_pending with non-zero pending items."""
        with patch("geneva.tqdm.supports_color", return_value=True):
            result = fmt_pending(5)
            expected = f"{Colors.BRIGHT_YELLOW}5{Colors.RESET}"
            assert result == expected

    def test_fmt_pending_none(self) -> None:
        """Test fmt_pending with None value."""
        with patch("geneva.tqdm.supports_color", return_value=True):
            result = fmt_pending(None)
            expected = f"{Colors.BRIGHT_GREEN}0{Colors.RESET}"
            assert result == expected

    def test_fmt_pending_without_color_support(self) -> None:
        """Test fmt_pending without color support."""
        with patch("geneva.tqdm.supports_color", return_value=False):
            result = fmt_pending(5)
            assert result == "5"


class TestTqdmModeIntegration:
    """Test integration between TqdmMode and formatting functions."""

    @patch("geneva.tqdm._tqdm_config")
    def test_std_mode_integration(self, mock_config) -> None:
        """Test that STD mode enables color formatting."""
        mock_config.mode = TqdmMode.STD

        with patch("geneva.tqdm.tqdm") as mock_tqdm:
            mock_tqdm.__module__ = "tqdm.std"

            # Test that colors are applied in STD mode
            result = fmt("test", Colors.RED)
            expected = f"{Colors.RED}test{Colors.RESET}"
            assert result == expected

            # Test status badge
            status_result = fmt_status_badge("running")
            assert Colors.BRIGHT_GREEN in status_result
            assert "running" in status_result

    @patch("geneva.tqdm._tqdm_config")
    def test_notebook_mode_integration(self, mock_config) -> None:
        """Test that NOTEBOOK mode disables color formatting."""
        mock_config.mode = TqdmMode.NOTEBOOK

        with patch("geneva.tqdm.tqdm") as mock_tqdm:
            mock_tqdm.__module__ = "tqdm.notebook"

            # Test that colors are NOT applied in NOTEBOOK mode
            result = fmt("test", Colors.RED)
            assert result == "test"

            # Test status badge
            status_result = fmt_status_badge("running")
            assert status_result == "running"
            assert Colors.BRIGHT_GREEN not in status_result

    def test_mode_switching_affects_formatting(self) -> None:
        """Test that switching modes affects formatting behavior."""
        # Test STD mode
        with patch("geneva.tqdm.tqdm") as mock_tqdm:
            mock_tqdm.__module__ = "tqdm.std"
            std_result = fmt("test", Colors.BLUE, bold=True)
            assert Colors.BLUE in std_result
            assert Colors.BOLD in std_result
            assert Colors.RESET in std_result

        # Test NOTEBOOK mode
        with patch("geneva.tqdm.tqdm") as mock_tqdm:
            mock_tqdm.__module__ = "tqdm.notebook"
            notebook_result = fmt("test", Colors.BLUE, bold=True)
            assert notebook_result == "test"

    def test_all_formatting_functions_respect_mode(self) -> None:
        """Test that all formatting functions respect the current mode."""
        test_cases = [
            ("tqdm.std", True),
            ("tqdm.asyncio", True),
            ("tqdm.notebook", False),
            ("tqdm.rich", True),
            ("tqdm.auto", False),
        ]

        for module_name, should_have_colors in test_cases:
            with patch("geneva.tqdm.tqdm") as mock_tqdm:
                mock_tqdm.__module__ = module_name

                # Test fmt
                fmt_result = fmt("test", Colors.RED)
                if should_have_colors:
                    assert Colors.RED in fmt_result
                    assert Colors.RESET in fmt_result
                else:
                    assert fmt_result == "test"

                # Test fmt_status_badge
                badge_result = fmt_status_badge("running")
                if should_have_colors:
                    assert Colors.BRIGHT_GREEN in badge_result
                else:
                    assert badge_result == "running"

                # Test fmt_numeric
                numeric_result = fmt_numeric(5, 10)
                if should_have_colors:
                    assert Colors.BRIGHT_RED in numeric_result
                else:
                    assert numeric_result == "5"

                # Test fmt_pending
                pending_result = fmt_pending(3)
                if should_have_colors:
                    assert Colors.BRIGHT_YELLOW in pending_result
                else:
                    assert pending_result == "3"


class TestColors:
    """Test Colors class constants."""

    def test_color_constants_exist(self) -> None:
        """Test that all expected color constants exist."""
        # Test basic colors
        assert hasattr(Colors, "RED")
        assert hasattr(Colors, "GREEN")
        assert hasattr(Colors, "BLUE")
        assert hasattr(Colors, "YELLOW")
        assert hasattr(Colors, "MAGENTA")
        assert hasattr(Colors, "CYAN")
        assert hasattr(Colors, "WHITE")
        assert hasattr(Colors, "BLACK")

        # Test bright colors
        assert hasattr(Colors, "BRIGHT_RED")
        assert hasattr(Colors, "BRIGHT_GREEN")
        assert hasattr(Colors, "BRIGHT_BLUE")
        assert hasattr(Colors, "BRIGHT_YELLOW")
        assert hasattr(Colors, "BRIGHT_MAGENTA")
        assert hasattr(Colors, "BRIGHT_CYAN")
        assert hasattr(Colors, "BRIGHT_WHITE")
        assert hasattr(Colors, "BRIGHT_BLACK")

        # Test formatting
        assert hasattr(Colors, "RESET")
        assert hasattr(Colors, "BOLD")
        assert hasattr(Colors, "DIM")

    def test_color_values_are_ansi_codes(self) -> None:
        """Test that color values are proper ANSI escape codes."""
        assert Colors.RESET == "\033[0m"
        assert Colors.BOLD == "\033[1m"
        assert Colors.DIM == "\033[2m"

        # Test some basic colors
        assert Colors.RED == "\033[31m"
        assert Colors.GREEN == "\033[32m"
        assert Colors.BLUE == "\033[34m"

        # Test some bright colors
        assert Colors.BRIGHT_RED == "\033[91m"
        assert Colors.BRIGHT_GREEN == "\033[92m"
        assert Colors.BRIGHT_BLUE == "\033[94m"
