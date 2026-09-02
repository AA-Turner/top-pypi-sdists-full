"""Tests for backoff_seconds function."""

from __future__ import annotations

import pytest

from agentic_devtools.cli.setup.fixloop import backoff_seconds


class TestBackoffSeconds:
    """FR-008: Exponential backoff capped at 30 seconds."""

    def test_n_zero(self) -> None:
        assert backoff_seconds(0) == 1

    def test_n_one(self) -> None:
        assert backoff_seconds(1) == 2

    def test_n_two(self) -> None:
        assert backoff_seconds(2) == 4

    def test_n_three(self) -> None:
        assert backoff_seconds(3) == 8

    def test_n_four(self) -> None:
        assert backoff_seconds(4) == 16

    def test_n_five(self) -> None:
        assert backoff_seconds(5) == 30

    def test_n_six(self) -> None:
        assert backoff_seconds(6) == 30

    def test_large_n(self) -> None:
        assert backoff_seconds(100) == 30

    def test_negative_raises_value_error(self) -> None:
        with pytest.raises(ValueError, match="n >= 0"):
            backoff_seconds(-1)

    def test_negative_large_raises_value_error(self) -> None:
        with pytest.raises(ValueError, match="n >= 0"):
            backoff_seconds(-100)
