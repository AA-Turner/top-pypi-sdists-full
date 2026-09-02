"""Tests for positive_int in nest/async_commands.py."""

from __future__ import annotations

import argparse

import pytest

from agentic_devtools.cli.speckit.nest.async_commands import positive_int


class TestPositiveInt:
    """Tests for the positive_int argument type validator."""

    def test_valid_positive_integer_returns_int(self) -> None:
        """Test that a valid positive integer string returns the parsed int."""
        assert positive_int("1") == 1
        assert positive_int("42") == 42
        assert positive_int("9999") == 9999

    def test_non_integer_string_raises_argument_type_error(self) -> None:
        """Test that a non-integer string raises ArgumentTypeError."""
        with pytest.raises(argparse.ArgumentTypeError, match="expected a positive integer"):
            positive_int("abc")

    def test_float_string_raises_argument_type_error(self) -> None:
        """Test that a float string raises ArgumentTypeError."""
        with pytest.raises(argparse.ArgumentTypeError, match="expected a positive integer"):
            positive_int("1.5")

    def test_zero_raises_argument_type_error(self) -> None:
        """Test that zero raises ArgumentTypeError."""
        with pytest.raises(argparse.ArgumentTypeError, match="expected a positive integer"):
            positive_int("0")

    def test_negative_integer_raises_argument_type_error(self) -> None:
        """Test that a negative integer string raises ArgumentTypeError."""
        with pytest.raises(argparse.ArgumentTypeError, match="expected a positive integer"):
            positive_int("-5")
