import pytest

from pycarlo.common.retries import (
    ExponentialBackoff,
    ExponentialBackoffJitter,
)


class TestExponentialBackoff:
    """Test cases for ExponentialBackoff class."""

    def test_exponential_backoff_with_different_start(self):
        """Test exponential backoff with different start values."""
        backoff = ExponentialBackoff(start=0.5, maximum=5.0)

        assert backoff.backoff(0) == 0.5  # 2^0 * 0.5 = 0.5
        assert backoff.backoff(1) == 1.0  # 2^1 * 0.5 = 1.0
        assert backoff.backoff(2) == 2.0  # 2^2 * 0.5 = 2.0
        assert backoff.backoff(3) == 4.0  # 2^3 * 0.5 = 4.0
        assert backoff.backoff(4) == 5.0  # 2^4 * 0.5 = 8.0, but capped at 5.0

    def test_delays_generator_values(self):
        """Test that delays generator returns expected values."""
        backoff = ExponentialBackoff(start=1.0, maximum=10.0)
        delays = list(backoff.delays())

        # First few values should match exponential backoff
        assert delays[0] == 1.0
        assert delays[1] == 2.0
        assert delays[2] == 4.0
        assert delays[3] == 8.0
        assert delays[4] == 10.0  # Capped at maximum

    def test_delays_generator_with_small_maximum(self):
        """Test delays generator with a small maximum value."""
        backoff = ExponentialBackoff(start=1.0, maximum=1.5)
        delays = list(backoff.delays())

        # Should return the start value first, then the maximum
        assert len(delays) == 2
        assert delays[0] == 1.0
        assert delays[1] == 1.5

    def test_delays_generator_with_zero_start(self):
        """Test delays generator with zero start value."""
        backoff = ExponentialBackoff(start=0.0, maximum=10.0)
        delays = list(backoff.delays())

        # Should return maximum immediately since 2^0 * 0 = 0, but we cap at maximum
        assert len(delays) == 1
        assert delays[0] == 10.0

    def test_negative_start_value(self):
        """Test behavior with negative start value."""
        # Should raise ValueError for negative start values
        with pytest.raises(ValueError, match="start must be >= 0"):
            ExponentialBackoff(start=-1.0, maximum=10.0)

        with pytest.raises(ValueError, match="start must be >= 0"):
            ExponentialBackoffJitter(start=-1.0, maximum=10.0)

    def test_zero_maximum(self):
        """Test behavior with zero maximum value."""
        backoff = ExponentialBackoff(start=1.0, maximum=0.0)
        delays = list(backoff.delays())

        # Should return maximum immediately
        assert len(delays) == 1
        assert delays[0] == 0.0

    def test_very_large_maximum(self):
        """Test behavior with very large maximum value."""
        backoff = ExponentialBackoff(start=1.0, maximum=1000000.0)
        delays = list(backoff.delays())

        assert len(delays) == 21
        assert delays[-1] == 1000000.0
        assert all(0 <= delay <= 1000000.0 for delay in delays)

    def test_very_small_start(self):
        """Test behavior with very small start value."""
        backoff = ExponentialBackoff(start=0.001, maximum=10.0)
        delays = list(backoff.delays())

        assert len(delays) == 15
        assert delays[-1] == 10.0
        assert all(0 <= delay <= 10.0 for delay in delays)


class TestExponentialBackoffJitter:
    """Test cases for ExponentialBackoffJitter class."""

    def test_exponential_backoff_jitter_basic(self):
        """Test basic exponential backoff jitter functionality."""
        backoff = ExponentialBackoffJitter(start=1.0, maximum=10.0)

        # Test that jitter values are within expected range (50% to 100% of base)
        jitter_delay = backoff.backoff(1)

        assert 1.0 <= jitter_delay <= 2.0  # 50% to 100% of 2.0

    def test_exponential_backoff_jitter_monotonic_increasing(self):
        """Test that jitter delays are monotonically increasing."""
        backoff = ExponentialBackoffJitter(start=1.0, maximum=10.0)

        # Test multiple consecutive delays to ensure they're increasing
        delays = []
        for i in range(5):
            delays.append(backoff.backoff(i))

        # Each delay should be greater than or equal to the previous one
        for i in range(1, len(delays)):
            assert delays[i] >= delays[i - 1], (
                f"Delay {i} ({delays[i]}) should be >= delay {i - 1} ({delays[i - 1]})"
            )

    def test_exponential_backoff_jitter_delays_generator_terminates(self):
        """Test that the delays generator terminates for jitter backoff."""
        backoff = ExponentialBackoffJitter(start=1.0, maximum=10.0)
        delays = list(backoff.delays())

        # Should terminate and return finite number of delays
        assert len(delays) <= 6  # worst case is exponential backoff + 1 attempts

        # Last delay should be the maximum
        assert delays[-1] == 10.0

    def test_exponential_backoff_jitter_with_zero_base(self):
        """Test jitter behavior when base delay is zero."""
        backoff = ExponentialBackoffJitter(start=0.0, maximum=10.0)

        # When base delay is 0, jitter should also return 0
        delay = backoff.backoff(0)
        assert delay == 0.0
