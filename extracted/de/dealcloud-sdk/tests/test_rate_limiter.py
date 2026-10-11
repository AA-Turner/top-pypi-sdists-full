"""Tests for dealcloud_sdk.utils.rate_limiter."""

import asyncio
import pytest
from unittest.mock import patch, MagicMock

from dealcloud_sdk.utils.rate_limiter import RateLimiter, AsyncRateLimiter


class TestRateLimiter:
    """Tests for RateLimiter."""

    def test_init_valid(self):
        r = RateLimiter(max_calls_per_second=4.0)
        assert r.max_calls_per_second == 4.0
        assert r.min_interval == 0.25

    def test_init_zero_raises(self):
        with pytest.raises(ValueError, match="must be positive"):
            RateLimiter(max_calls_per_second=0)

    def test_init_negative_raises(self):
        with pytest.raises(ValueError, match="must be positive"):
            RateLimiter(max_calls_per_second=-1)

    def test_init_above_five_warns(self):
        with pytest.warns(UserWarning, match="5/second"):
            RateLimiter(max_calls_per_second=10.0)

    def test_wait_if_needed_first_call_no_wait(self):
        r = RateLimiter(max_calls_per_second=4.0)
        r.wait_if_needed()
        assert r.last_call_time > 0

    @pytest.mark.filterwarnings("ignore:Rate limiter set to 1000")
    def test_wait_if_needed_second_call_waits(self):
        r = RateLimiter(max_calls_per_second=1000.0)
        r.reset()
        mock_time = MagicMock()
        call_times = [0.0, 0.001, 0.0001, 0.001, 0.002]
        mock_time.time.side_effect = call_times
        mock_time.sleep = MagicMock()
        with patch("dealcloud_sdk.utils.rate_limiter.time", mock_time):
            r.wait_if_needed()
            r.wait_if_needed()
        assert mock_time.sleep.call_count >= 1
        assert mock_time.sleep.call_args[0][0] > 0

    def test_reset(self):
        r = RateLimiter(max_calls_per_second=4.0)
        r.wait_if_needed()
        r.reset()
        assert r.last_call_time == 0.0

    def test_repr(self):
        r = RateLimiter(max_calls_per_second=4.0)
        assert "RateLimiter" in repr(r)
        assert "4.0" in repr(r)


class TestAsyncRateLimiter:
    """Tests for AsyncRateLimiter."""

    def test_init_valid(self):
        r = AsyncRateLimiter(max_calls_per_second=4.0)
        assert r.max_calls_per_second == 4.0
        assert r.min_interval == 0.25

    def test_init_zero_raises(self):
        with pytest.raises(ValueError, match="must be positive"):
            AsyncRateLimiter(max_calls_per_second=0)

    def test_init_above_five_warns(self):
        with pytest.warns(UserWarning, match="5/second"):
            AsyncRateLimiter(max_calls_per_second=6.0)

    @pytest.mark.asyncio
    async def test_wait_if_needed_first_call_no_wait(self):
        r = AsyncRateLimiter(max_calls_per_second=4.0)
        await r.wait_if_needed()
        assert r.last_call_time > 0

    @pytest.mark.asyncio
    @pytest.mark.filterwarnings("ignore:Rate limiter set to 1000")
    async def test_wait_if_needed_second_call_waits(self):
        r = AsyncRateLimiter(max_calls_per_second=1000.0)
        await r.wait_if_needed()
        with patch("time.time", return_value=0.0):
            with patch("asyncio.sleep", return_value=None) as mock_sleep:
                with patch("dealcloud_sdk.utils.rate_limiter.time") as t:
                    t.time.return_value = 0.0001
                    await r.wait_if_needed()
                    mock_sleep.assert_called_once()

    def test_reset(self):
        r = AsyncRateLimiter(max_calls_per_second=4.0)
        r.reset()
        assert r.last_call_time == 0.0

    def test_repr(self):
        r = AsyncRateLimiter(max_calls_per_second=4.0)
        assert "AsyncRateLimiter" in repr(r)
        assert "4.0" in repr(r)
