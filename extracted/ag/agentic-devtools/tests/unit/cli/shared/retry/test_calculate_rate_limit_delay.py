"""Tests for calculate_rate_limit_delay()."""

import pytest

from agentic_devtools.cli.shared.retry import calculate_rate_limit_delay


class TestCalculateRateLimitDelay:
    """calculate_rate_limit_delay() selects bounded cooldown timing safely."""

    def test_prefers_retry_after_and_adds_margin(self) -> None:
        result = calculate_rate_limit_delay(
            retry_after_seconds=120,
            reset_timestamp=500,
            now=100,
            safety_margin=10,
        )
        assert result.source == "retry-after"
        assert result.delay_seconds == 130
        assert result.resume_at == 230

    def test_uses_reset_then_fallback(self) -> None:
        reset = calculate_rate_limit_delay(reset_timestamp=500, now=400, safety_margin=10)
        fallback = calculate_rate_limit_delay(
            reset_timestamp="bad",  # type: ignore[arg-type]
            now=400,
            fallback_delay=20,
            safety_margin=10,
        )
        assert reset.source == "x-ratelimit-reset"
        assert reset.resume_at == 510
        assert fallback.source == "fallback"
        assert fallback.delay_seconds == 30

    def test_rejects_invalid_clock_and_configuration(self) -> None:
        with pytest.raises(ValueError, match="now"):
            calculate_rate_limit_delay(now=float("nan"))
        with pytest.raises(ValueError, match="configuration"):
            calculate_rate_limit_delay(fallback_delay=-1)
        with pytest.raises(ValueError, match="configuration"):
            calculate_rate_limit_delay(max_delay=float("inf"))
        with pytest.raises(ValueError, match="configuration"):
            calculate_rate_limit_delay(fallback_delay=float("nan"))
        with pytest.raises(ValueError, match="configuration"):
            calculate_rate_limit_delay(safety_margin=float("inf"))

    def test_ignores_non_numeric_metadata(self) -> None:
        result = calculate_rate_limit_delay(
            retry_after_seconds="bad",  # type: ignore[arg-type]
            reset_timestamp="bad",  # type: ignore[arg-type]
            now=100,
            fallback_delay=20,
            safety_margin=10,
        )
        assert result.source == "fallback"
