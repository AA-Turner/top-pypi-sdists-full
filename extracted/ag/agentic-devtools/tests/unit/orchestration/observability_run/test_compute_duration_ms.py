"""Tests for _compute_duration_ms helper function."""

from agentic_devtools.orchestration.observability_run import _compute_duration_ms


class TestComputeDurationMs:
    """Tests for _compute_duration_ms."""

    def test_valid_timestamps(self) -> None:
        result = _compute_duration_ms(
            "2024-01-01T00:00:00+00:00",
            "2024-01-01T00:00:01+00:00",
        )
        assert result == 1000

    def test_invalid_start_time_returns_zero(self) -> None:
        result = _compute_duration_ms("not-a-date", "2024-01-01T00:00:01+00:00")
        assert result == 0

    def test_invalid_end_time_returns_zero(self) -> None:
        result = _compute_duration_ms("2024-01-01T00:00:00+00:00", "not-a-date")
        assert result == 0

    def test_end_before_start_returns_zero(self) -> None:
        """Negative duration is clamped to 0."""
        result = _compute_duration_ms(
            "2024-01-01T00:00:02+00:00",
            "2024-01-01T00:00:01+00:00",
        )
        assert result == 0
