"""Tests for thread-safe scan phase timing."""

from concurrent.futures import ThreadPoolExecutor

from runlayer_cli.scan.timing import PhaseTimer


def test_phase_timer_records_context_duration():
    ticks = iter([10.0, 10.125])
    timer = PhaseTimer(clock=lambda: next(ticks))

    with timer.phase("crawl"):
        pass

    assert timer.durations_ms() == {"crawl": 125}


def test_phase_timer_records_concurrent_updates_in_stable_order():
    timer = PhaseTimer()

    with ThreadPoolExecutor(max_workers=4) as pool:
        list(
            pool.map(lambda index: timer.record(f"phase_{index:02}", index), range(20))
        )

    assert timer.durations_ms() == {f"phase_{index:02}": index for index in range(20)}
