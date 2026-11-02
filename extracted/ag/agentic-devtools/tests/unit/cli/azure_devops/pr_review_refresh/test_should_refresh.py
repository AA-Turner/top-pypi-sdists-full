"""Tests for should_refresh."""

from agentic_devtools.cli.azure_devops.pr_review_refresh import should_refresh


def _call(accepted, last_count, now, last_ts, *, every_n=1, interval=0.0, force=False, final=False):
    return should_refresh(
        accepted,
        last_count,
        now,
        last_ts,
        every_n=every_n,
        min_interval_seconds=interval,
        force=force,
        final=final,
    )


class TestShouldRefresh:
    def test_force_always_true(self):
        assert _call(0, 5, 0.0, 0.0, force=True) is True

    def test_final_always_true(self):
        assert _call(0, 5, 0.0, 0.0, final=True) is True

    def test_first_refresh_no_last_count(self):
        assert _call(2, None, 100.0, 100.0) is True

    def test_first_refresh_no_last_ts(self):
        assert _call(2, 1, 100.0, None) is True

    def test_count_delta_triggers(self):
        assert _call(5, 2, 100.0, 100.0, every_n=3) is True

    def test_time_interval_triggers(self):
        assert _call(3, 2, 130.0, 100.0, every_n=5, interval=20.0) is True

    def test_throttled_returns_false(self):
        assert _call(3, 2, 105.0, 100.0, every_n=5, interval=20.0) is False

    def test_zero_interval_relies_on_count_threshold(self):
        assert _call(3, 2, 105.0, 100.0, every_n=5, interval=0.0) is False
