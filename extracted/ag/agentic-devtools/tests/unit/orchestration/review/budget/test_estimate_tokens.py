"""Tests for estimate_tokens function."""

from __future__ import annotations

import pytest

from agentic_devtools.orchestration.review.budget import estimate_tokens


class TestEstimateTokens:
    """Tests for character-based token estimation."""

    def test_empty_string_returns_zero(self) -> None:
        assert estimate_tokens("") == 0

    def test_basic_estimation(self) -> None:
        """1 token per 3.5 chars, ceiling."""
        # 7 chars / 3.5 = 2 tokens
        assert estimate_tokens("abcdefg") == 2

    def test_ceiling_rounding(self) -> None:
        """Non-integer results are rounded up."""
        # 1 char / 3.5 = 0.286 → ceil = 1
        assert estimate_tokens("a") == 1

    def test_custom_ratio(self) -> None:
        """Custom chars_per_token ratio."""
        # 10 chars / 5.0 = 2.0
        assert estimate_tokens("0123456789", chars_per_token=5.0) == 2

    def test_invalid_ratio_raises(self) -> None:
        with pytest.raises(ValueError):
            estimate_tokens("hello", chars_per_token=0)
        with pytest.raises(ValueError):
            estimate_tokens("hello", chars_per_token=-1)
