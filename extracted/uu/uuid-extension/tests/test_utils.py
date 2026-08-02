"""
Tests for utility functions in the uuid-extension package.

This module contains tests for the utility functions provided by
the uuid-extension package, focusing on timestamp manipulation utilities.
"""

import time
from datetime import datetime, timedelta
from unittest import mock

import pytest

from uuid_extension.utils import generate_unix_ts_in_ms


class TestGenerateUnixTsInMs:
    """Tests for the generate_unix_ts_in_ms function."""

    def test_with_none_timestamp(self):
        """Test generating timestamp with None input (current time)."""
        # Mock time.time() to return a known value
        with mock.patch(
            "uuid_extension.utils.time",
            return_value=1621234567.89,
        ):
            result = generate_unix_ts_in_ms()
            # Expected: 1621234567.89 * 1000 = 1621234567890
            assert result == 1621234567890
            # Verify 48-bit constraint
            assert result <= 0xFFFFFFFFFFFF

    def test_with_float_timestamp(self):
        """Test generating timestamp from float seconds."""
        result = generate_unix_ts_in_ms(1621234567.89)
        assert result == 1621234567890
        assert result <= 0xFFFFFFFFFFFF

    def test_with_int_timestamp(self):
        """Test generating timestamp from integer seconds."""
        result = generate_unix_ts_in_ms(1621234567)
        assert result == 1621234567000
        assert result <= 0xFFFFFFFFFFFF

    def test_with_datetime_timestamp(self):
        """Test generating timestamp from datetime object."""
        dt = datetime(2021, 5, 17, 12, 34, 56)
        result = generate_unix_ts_in_ms(dt)
        # Convert datetime to expected timestamp
        expected = int(dt.timestamp() * 1000)
        assert result == expected
        assert result <= 0xFFFFFFFFFFFF

    def test_48bit_masking(self):
        """Test that timestamps are properly masked to 48 bits."""
        # Use a value just above the 48-bit limit to test masking
        # 0x1000000000000 = 2^48 = first 49-bit value
        ms_above_limit = 0x1000000000000  # 1 bit larger than 48 bits
        result = generate_unix_ts_in_ms(ms_above_limit / 1000)

        # Should be masked to zero (all bits beyond 48 are removed)
        assert result == 0

        # Test with value at exactly 48 bits (all 1's)
        max_48bit = 0xFFFFFFFFFFFF  # Max 48-bit value
        result_max = generate_unix_ts_in_ms(max_48bit / 1000)

        # Should remain unchanged after masking
        assert result_max == max_48bit
        assert hex(result_max) == "0xffffffffffff"

    def test_realtime_timestamp_range(self):
        """Test that current time is within expected range."""
        # Get timestamp slightly before our function call
        before = int(time.time() * 1000)

        result = generate_unix_ts_in_ms()

        # Get timestamp slightly after our function call
        after = int(time.time() * 1000)

        # Result should be between before and after
        assert before <= result <= after or before - 1 <= result <= after

    def test_invalid_timestamp_type(self):
        """Test handling of invalid timestamp types."""
        with pytest.raises(TypeError) as excinfo:
            generate_unix_ts_in_ms("invalid")

        assert "Unsupported timestamp type: str" in str(excinfo.value)

    def test_future_datetime(self):
        """Test with a future datetime."""
        future = datetime.now() + timedelta(days=30)
        result = generate_unix_ts_in_ms(future)
        expected = int(future.timestamp() * 1000) & 0xFFFFFFFFFFFF
        assert result == expected

    def test_past_datetime(self):
        """Test with a past datetime."""
        past = datetime(1970, 1, 2)  # One day after epoch
        result = generate_unix_ts_in_ms(past)
        expected = int(past.timestamp() * 1000) & 0xFFFFFFFFFFFF
        assert result == expected
