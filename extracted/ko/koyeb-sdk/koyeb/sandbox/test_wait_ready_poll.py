import asyncio
import unittest
from unittest.mock import patch

from koyeb.sandbox.sandbox import (
    FAST_POLL_INTERVAL,
    FAST_POLL_WINDOW,
    AsyncSandbox,
    Sandbox,
)


class FakeClock:
    """time.time()/sleep() stand-in: sleeping advances the clock."""

    def __init__(self):
        self.now = 0.0
        self.sleeps = []  # (time the sleep started, duration)

    def time(self):
        return self.now

    def sleep(self, seconds):
        self.sleeps.append((self.now, seconds))
        self.now += seconds

    async def async_sleep(self, seconds):
        self.sleep(seconds)


class WaitReadyPollSchedule:
    """wait_ready() polls every FAST_POLL_INTERVAL during the first
    FAST_POLL_WINDOW seconds, when most sandboxes turn HEALTHY, then backs
    off up to poll_interval."""

    healthy_at = FAST_POLL_WINDOW + 3

    def run_wait_ready(self, clock, poll_interval):
        raise NotImplementedError

    def assert_schedule(self, clock, poll_interval):
        previous = None
        for started, duration in clock.sleeps:
            if abs(started - FAST_POLL_WINDOW) < 1e-6:
                pass  # float sums land on either side of the window's end
            elif started < FAST_POLL_WINDOW:
                self.assertEqual(duration, min(FAST_POLL_INTERVAL, poll_interval))
            else:
                self.assertEqual(duration, min(previous * 2, poll_interval))
            previous = duration
        self.assertGreaterEqual(clock.now, self.healthy_at)
        self.assertLess(clock.now, self.healthy_at + poll_interval + 1e-6)

    def test_fast_then_backoff_to_default(self):
        clock = FakeClock()
        self.assertTrue(self.run_wait_ready(clock, 0.5))
        self.assert_schedule(clock, 0.5)
        self.assertEqual(clock.sleeps[-1][1], 0.5)

    def test_explicit_poll_interval_caps_the_backoff(self):
        clock = FakeClock()
        self.assertTrue(self.run_wait_ready(clock, 2.0))
        self.assert_schedule(clock, 2.0)
        after_window = [d for t, d in clock.sleeps if t > FAST_POLL_WINDOW + 1e-6]
        self.assertEqual(after_window[:4], [0.2, 0.4, 0.8, 1.6])

    def test_poll_interval_below_fast_interval_is_kept(self):
        clock = FakeClock()
        self.assertTrue(self.run_wait_ready(clock, 0.05))
        self.assertEqual({d for _, d in clock.sleeps}, {0.05})


class TestSyncWaitReadyPoll(WaitReadyPollSchedule, unittest.TestCase):
    def run_wait_ready(self, clock, poll_interval):
        sb = Sandbox.__new__(Sandbox)
        sb.poll_interval = 0.5
        deployment_healthy = patch.object(
            Sandbox,
            "_is_deployment_healthy",
            side_effect=lambda: clock.now >= self.healthy_at,
        )
        executor_healthy = patch.object(
            Sandbox, "_check_executor_health", return_value=True
        )
        with deployment_healthy, executor_healthy:
            with patch("koyeb.sandbox.sandbox.time.time", clock.time):
                with patch("koyeb.sandbox.sandbox.time.sleep", clock.sleep):
                    return sb.wait_ready(timeout=60, poll_interval=poll_interval)


class TestAsyncWaitReadyPoll(WaitReadyPollSchedule, unittest.TestCase):
    def run_wait_ready(self, clock, poll_interval):
        sb = AsyncSandbox.__new__(AsyncSandbox)
        sb.poll_interval = 0.5

        async def is_deployment_healthy():
            return clock.now >= self.healthy_at

        async def check_executor_health():
            return True

        deployment_healthy = patch.object(
            AsyncSandbox,
            "_async_is_deployment_healthy",
            side_effect=is_deployment_healthy,
        )
        executor_healthy = patch.object(
            AsyncSandbox,
            "_async_check_executor_health",
            side_effect=check_executor_health,
        )
        with deployment_healthy, executor_healthy:
            with patch("koyeb.sandbox.sandbox.time.time", clock.time):
                with patch("koyeb.sandbox.sandbox.asyncio.sleep", clock.async_sleep):
                    return asyncio.run(
                        sb.wait_ready(timeout=60, poll_interval=poll_interval)
                    )


if __name__ == "__main__":
    unittest.main()
