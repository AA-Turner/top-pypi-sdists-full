"""Tests for detect_parent_cli._positive_int."""

from __future__ import annotations

import argparse

import pytest

from agentic_devtools.cli.speckit.detect_parent_cli import _positive_int


class TestPositiveInt:
    """Tests for the _positive_int argparse type validator."""

    def test_valid_positive_integer(self):
        """Returns the integer for a valid positive value."""
        assert _positive_int("10") == 10
        assert _positive_int("1") == 1
        assert _positive_int("999") == 999

    def test_zero_raises(self):
        """Raises ArgumentTypeError for zero."""
        with pytest.raises(argparse.ArgumentTypeError, match="positive integer"):
            _positive_int("0")

    def test_negative_raises(self):
        """Raises ArgumentTypeError for negative values."""
        with pytest.raises(argparse.ArgumentTypeError, match="positive integer"):
            _positive_int("-1")
        with pytest.raises(argparse.ArgumentTypeError, match="positive integer"):
            _positive_int("-100")

    def test_non_integer_string_raises(self):
        """Raises ArgumentTypeError for non-integer strings."""
        with pytest.raises(argparse.ArgumentTypeError, match="not an integer"):
            _positive_int("abc")

    def test_float_string_raises(self):
        """Raises ArgumentTypeError for float strings."""
        with pytest.raises(argparse.ArgumentTypeError, match="not an integer"):
            _positive_int("1.5")
