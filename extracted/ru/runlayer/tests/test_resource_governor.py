"""Tests for the cooperative scan resource governor."""

import signal
import threading
import tracemalloc

import pytest

from runlayer_cli.scan import resource_governor as rg
from runlayer_cli.scan.resource_governor import (
    DEFAULT_CPU_CORES,
    DEFAULT_CPU_PERCENT,
    DEFAULT_MEMORY_LIMIT_MB,
    MAX_CPU_CORES,
    MAX_CPU_PERCENT,
    MAX_MEMORY_LIMIT_MB,
    MIN_CPU_CORES,
    MIN_CPU_PERCENT,
    MIN_MEMORY_LIMIT_MB,
    ResourceGovernor,
    ScanResourceLimitExceeded,
    build_governor,
    clamp_cpu_cores,
    clamp_cpu_percent,
    clamp_memory_limit_mb,
    compute_target_core_fraction,
    default_cpu_cores,
    terminate_process,
)

_MB = 1024 * 1024


class FakeProc:
    """Minimal ``subprocess.Popen`` stand-in for kill / registration tests."""

    def __init__(self, pid: int = 999_999, alive: bool = True) -> None:
        self.pid = pid
        self._alive = alive
        self.killed = False

    def poll(self):
        return None if self._alive else 0

    def kill(self) -> None:
        self.killed = True
        self._alive = False


# --- clamp helpers ---------------------------------------------------------


class TestClampCpuCores:
    def test_in_range_passes_through(self):
        assert clamp_cpu_cores(3, cpu_count=8) == 3

    def test_above_max_clamps_to_cpu_count(self):
        assert clamp_cpu_cores(99, cpu_count=8) == 8

    def test_below_one_floors_to_one(self):
        assert clamp_cpu_cores(0, cpu_count=8) == 1
        assert clamp_cpu_cores(-5, cpu_count=8) == 1

    def test_non_int_falls_back_to_half_cores(self):
        assert clamp_cpu_cores(None, cpu_count=8) == 4
        assert clamp_cpu_cores("4", cpu_count=8) == 4

    def test_bool_rejected(self):
        # isinstance(True, int) is True, so bool must be excluded explicitly.
        assert clamp_cpu_cores(True, cpu_count=8) == 4


class TestClampCpuPercent:
    def test_in_range_passes_through(self):
        assert clamp_cpu_percent(42) == 42

    def test_above_max_clamps(self):
        assert clamp_cpu_percent(500) == MAX_CPU_PERCENT

    def test_below_min_clamps(self):
        assert clamp_cpu_percent(1) == MIN_CPU_PERCENT

    def test_non_int_defaults(self):
        assert clamp_cpu_percent(None) == DEFAULT_CPU_PERCENT
        assert clamp_cpu_percent(True) == DEFAULT_CPU_PERCENT


class TestClampMemoryLimitMb:
    def test_floor_covers_scan_retention_budgets(self):
        assert MIN_MEMORY_LIMIT_MB == 512
        assert clamp_memory_limit_mb(256) == 512

    def test_in_range_passes_through(self):
        assert clamp_memory_limit_mb(2048) == 2048

    def test_above_max_clamps(self):
        assert clamp_memory_limit_mb(999_999) == MAX_MEMORY_LIMIT_MB

    def test_below_min_clamps(self):
        assert clamp_memory_limit_mb(1) == MIN_MEMORY_LIMIT_MB

    def test_non_int_defaults(self):
        assert clamp_memory_limit_mb(None) == DEFAULT_MEMORY_LIMIT_MB
        assert clamp_memory_limit_mb(True) == DEFAULT_MEMORY_LIMIT_MB


class TestComputeTargetCoreFraction:
    def test_core_cap_binds(self):
        # min(1 core, 100% * 8 cores) => 1 core
        assert compute_target_core_fraction(1, 100, cpu_count=8) == 1.0

    def test_percent_cap_binds(self):
        # Percent is a single-core-equivalent duty budget, independent of host size.
        assert compute_target_core_fraction(8, 50, cpu_count=8) == 0.5

    def test_floor_prevents_deadlock(self):
        # 1% of a single core would be 0.01; floored to 0.05 so it never stalls.
        assert compute_target_core_fraction(1, 1, cpu_count=1) == pytest.approx(0.05)


class TestDefaults:
    def test_default_cpu_cores_is_half(self):
        assert default_cpu_cores() == DEFAULT_CPU_CORES
        assert DEFAULT_CPU_CORES == max(MIN_CPU_CORES, MAX_CPU_CORES // 2)


# --- build_governor factory ------------------------------------------------


class TestBuildGovernor:
    def test_none_uses_defaults(self):
        gov = build_governor()
        assert gov.cpu_cores == DEFAULT_CPU_CORES
        assert gov.max_cpu_percent == DEFAULT_CPU_PERCENT
        assert gov.memory_limit_mb == DEFAULT_MEMORY_LIMIT_MB

    def test_out_of_range_values_are_clamped(self):
        gov = build_governor(
            cpu_cores=99_999,
            max_cpu_percent=999,
            memory_limit_mb=1,
            cpu_count=4,
        )
        assert gov.cpu_cores == 4
        assert gov.max_cpu_percent == MAX_CPU_PERCENT
        assert gov.memory_limit_mb == MIN_MEMORY_LIMIT_MB


# --- CPU throttle ----------------------------------------------------------


def _governor_with_clock(*, cpu_cores, max_cpu_percent, cpu_count, clock, sleeps):
    """Governor wired to a mutable ``clock`` dict + recording ``sleeps`` list.

    Skips ``__enter__`` (no monitor thread / tracemalloc); ``_start_wall`` /
    ``_start_cpu`` default to 0.0, so the clock values are the elapsed totals.
    """
    return ResourceGovernor(
        cpu_cores=cpu_cores,
        max_cpu_percent=max_cpu_percent,
        memory_limit_mb=DEFAULT_MEMORY_LIMIT_MB,
        cpu_count=cpu_count,
        monotonic=lambda: clock["wall"],
        process_time=lambda: clock["cpu"],
        sleep=sleeps.append,
        memory_sampler=lambda: 0,
    )


class TestCpuThrottle:
    def test_parent_budget_shrinks_for_each_registered_child(self):
        gov = ResourceGovernor(
            cpu_cores=8,
            max_cpu_percent=50,
            memory_limit_mb=DEFAULT_MEMORY_LIMIT_MB,
            cpu_count=8,
            memory_sampler=lambda: 0,
        )
        first = FakeProc()
        second = FakeProc()

        assert gov.effective_parent_core_fraction == pytest.approx(0.5)
        gov.register_child(first)
        assert gov.effective_parent_core_fraction == pytest.approx(0.25)
        gov.register_child(second)
        assert gov.effective_parent_core_fraction == pytest.approx(0.5 / 3)
        gov.unregister_child(first)
        assert gov.effective_parent_core_fraction == pytest.approx(0.25)

    def test_sleeps_when_over_duty_cycle(self):
        clock = {"wall": 1.0, "cpu": 1.0}
        sleeps: list[float] = []
        # 50 means 0.5 core on every host; 1 cpu-sec over 1 wall-sec is 2x the
        # budget, so it must sleep to 2.0s wall total => 1.0s.
        gov = _governor_with_clock(
            cpu_cores=10, max_cpu_percent=50, cpu_count=10, clock=clock, sleeps=sleeps
        )
        assert gov.target_core_fraction == pytest.approx(0.5)
        gov.checkpoint()
        assert sleeps == [pytest.approx(1.0)]

    def test_no_sleep_under_generous_caps(self):
        clock = {"wall": 1.0, "cpu": 1.0}
        sleeps: list[float] = []
        gov = _governor_with_clock(
            cpu_cores=10, max_cpu_percent=100, cpu_count=10, clock=clock, sleeps=sleeps
        )
        gov.checkpoint()
        assert sleeps == []

    def test_single_sleep_is_clamped(self):
        clock = {"wall": 1.0, "cpu": 1.0}
        sleeps: list[float] = []
        # target floored at 0.05 => required wall 20s => 19s owed, clamped to 1.0.
        gov = _governor_with_clock(
            cpu_cores=1, max_cpu_percent=5, cpu_count=1, clock=clock, sleeps=sleeps
        )
        assert gov.target_core_fraction == pytest.approx(0.05)
        gov.checkpoint()
        assert sleeps == [pytest.approx(1.0)]

    def test_no_sleep_before_any_time_elapses(self):
        clock = {"wall": 0.0, "cpu": 0.0}
        sleeps: list[float] = []
        gov = _governor_with_clock(
            cpu_cores=1, max_cpu_percent=5, cpu_count=1, clock=clock, sleeps=sleeps
        )
        gov.checkpoint()
        assert sleeps == []

    def test_concurrent_checkpoints_do_not_serialize_throttle_sleep(self):
        clock = {"wall": 1.0, "cpu": 1.0}
        first_sleeping = threading.Event()
        both_sleeping = threading.Event()
        release_sleep = threading.Event()
        sleep_count = 0
        sleep_count_lock = threading.Lock()

        def blocking_sleep(_seconds: float) -> None:
            nonlocal sleep_count
            with sleep_count_lock:
                sleep_count += 1
                if sleep_count == 1:
                    first_sleeping.set()
                if sleep_count == 2:
                    both_sleeping.set()
            release_sleep.wait(timeout=2.0)

        gov = ResourceGovernor(
            cpu_cores=1,
            max_cpu_percent=5,
            memory_limit_mb=DEFAULT_MEMORY_LIMIT_MB,
            cpu_count=1,
            monotonic=lambda: clock["wall"],
            process_time=lambda: clock["cpu"],
            sleep=blocking_sleep,
            memory_sampler=lambda: 0,
        )
        first = threading.Thread(target=gov.checkpoint)
        second = threading.Thread(target=gov.checkpoint)

        first.start()
        assert first_sleeping.wait(timeout=1.0)
        second.start()
        try:
            assert both_sleeping.wait(timeout=1.0)
        finally:
            release_sleep.set()
            first.join(timeout=1.0)
            second.join(timeout=1.0)
        assert not first.is_alive()
        assert not second.is_alive()


# --- memory abort ----------------------------------------------------------


class TestMemoryAbort:
    def test_sample_over_budget_sets_abort_and_checkpoint_raises(self):
        gov = ResourceGovernor(
            cpu_cores=1,
            max_cpu_percent=100,
            memory_limit_mb=MIN_MEMORY_LIMIT_MB,
            memory_sampler=lambda: (MIN_MEMORY_LIMIT_MB + 1) * _MB,
        )
        assert gov._sample_memory_once() is True
        assert gov._abort.is_set()
        with pytest.raises(ScanResourceLimitExceeded):
            gov.checkpoint()

    def test_sample_under_budget_is_noop(self):
        gov = ResourceGovernor(
            cpu_cores=1,
            max_cpu_percent=100,
            memory_limit_mb=1024,
            memory_sampler=lambda: 10 * _MB,
        )
        assert gov._sample_memory_once() is False
        assert not gov._abort.is_set()
        gov.checkpoint()  # does not raise

    def test_monitor_thread_trips_abort(self):
        gov = ResourceGovernor(
            cpu_cores=1,
            max_cpu_percent=100,
            memory_limit_mb=MIN_MEMORY_LIMIT_MB,
            monitor_interval_s=0.01,
            memory_sampler=lambda: (MIN_MEMORY_LIMIT_MB + 1) * _MB,
            sleep=lambda _s: None,
        )
        with gov:
            assert gov._abort.wait(2.0)
            with pytest.raises(ScanResourceLimitExceeded):
                gov.checkpoint()
        # monitor joined + cleared on exit
        assert gov._monitor is None

    def test_no_op_at_generous_caps_does_not_abort(self):
        gov = ResourceGovernor(
            cpu_cores=MAX_CPU_CORES,
            max_cpu_percent=100,
            memory_limit_mb=MAX_MEMORY_LIMIT_MB,
            monitor_interval_s=0.01,
            memory_sampler=lambda: 5 * _MB,
            sleep=lambda _s: None,
        )
        with gov:
            for _ in range(3):
                gov.checkpoint()
        assert not gov._abort.is_set()


# --- child registration + kill-on-abort ------------------------------------


class TestChildKill:
    @pytest.mark.skipif(not hasattr(signal, "SIGSTOP"), reason="POSIX only")
    def test_posix_controller_duty_cycles_child_group(self):
        proc = FakeProc()
        signals: list[tuple[object, int]] = []
        gov = ResourceGovernor(
            cpu_cores=8,
            max_cpu_percent=50,
            memory_limit_mb=DEFAULT_MEMORY_LIMIT_MB,
            cpu_count=8,
            memory_sampler=lambda: 0,
            posix_child_control=True,
            child_duty_period_s=0.2,
            process_group_signaler=lambda child, sig: (
                signals.append((child, sig)) or True
            ),
        )
        gov.register_child(proc)
        waits: list[float] = []

        def wait(duration: float) -> bool:
            waits.append(duration)
            if len(waits) == 2:
                gov._stop.set()
            return False

        gov._duty_wake.wait = wait
        gov._child_cpu_loop()

        assert waits == [pytest.approx(0.05), pytest.approx(0.15)]
        assert signals == [(proc, signal.SIGSTOP), (proc, signal.SIGCONT)]

    @pytest.mark.skipif(not hasattr(signal, "SIGSTOP"), reason="POSIX only")
    def test_register_during_pause_stops_and_unregister_resumes(self):
        proc = FakeProc()
        signals: list[tuple[object, int]] = []
        gov = ResourceGovernor(
            cpu_cores=8,
            max_cpu_percent=50,
            memory_limit_mb=DEFAULT_MEMORY_LIMIT_MB,
            memory_sampler=lambda: 0,
            posix_child_control=True,
            process_group_signaler=lambda child, sig: (
                signals.append((child, sig)) or True
            ),
        )
        gov._pause_phase = True

        gov.register_child(proc)
        gov.unregister_child(proc)

        assert signals == [(proc, signal.SIGSTOP), (proc, signal.SIGCONT)]
        assert gov._children == set()
        assert gov._paused_children == set()

    @pytest.mark.skipif(not hasattr(signal, "SIGSTOP"), reason="POSIX only")
    def test_failed_unregister_resume_is_retried_on_context_exit(self):
        proc = FakeProc()
        signals: list[tuple[object, int]] = []
        resume_attempts = 0

        def signal_process_group(child: object, sig: int) -> bool:
            nonlocal resume_attempts
            signals.append((child, sig))
            if sig == signal.SIGCONT:
                resume_attempts += 1
                return resume_attempts > 1
            return True

        gov = ResourceGovernor(
            cpu_cores=8,
            max_cpu_percent=50,
            memory_limit_mb=DEFAULT_MEMORY_LIMIT_MB,
            memory_sampler=lambda: 0,
            posix_child_control=True,
            process_group_signaler=signal_process_group,
        )
        gov._pause_phase = True

        gov.register_child(proc)
        gov.unregister_child(proc)
        gov.__exit__(None, None, None)

        assert signals == [
            (proc, signal.SIGSTOP),
            (proc, signal.SIGCONT),
            (proc, signal.SIGCONT),
        ]
        assert gov._paused_children == set()

    @pytest.mark.skipif(not hasattr(signal, "SIGSTOP"), reason="POSIX only")
    def test_context_exit_resumes_paused_child(self):
        proc = FakeProc()
        signals: list[tuple[object, int]] = []
        gov = ResourceGovernor(
            cpu_cores=8,
            max_cpu_percent=50,
            memory_limit_mb=DEFAULT_MEMORY_LIMIT_MB,
            memory_sampler=lambda: 0,
            posix_child_control=True,
            process_group_signaler=lambda child, sig: (
                signals.append((child, sig)) or True
            ),
        )
        gov._pause_phase = True
        gov.register_child(proc)

        gov.__exit__(None, None, None)

        assert signals == [(proc, signal.SIGSTOP), (proc, signal.SIGCONT)]
        assert gov._paused_children == set()

    def test_abort_kills_all_registered_children(self, monkeypatch):
        killed: list[object] = []
        monkeypatch.setattr(rg, "terminate_process", killed.append)
        gov = ResourceGovernor(
            cpu_cores=1,
            max_cpu_percent=100,
            memory_limit_mb=MIN_MEMORY_LIMIT_MB,
            memory_sampler=lambda: (MIN_MEMORY_LIMIT_MB + 1) * _MB,
        )
        first = FakeProc()
        second = FakeProc()
        gov.register_child(first)
        gov.register_child(second)
        gov._sample_memory_once()
        assert set(killed) == {first, second}

    def test_register_after_abort_kills_immediately(self, monkeypatch):
        killed: list[object] = []
        monkeypatch.setattr(rg, "terminate_process", killed.append)
        gov = ResourceGovernor(
            cpu_cores=1,
            max_cpu_percent=100,
            memory_limit_mb=MIN_MEMORY_LIMIT_MB,
            memory_sampler=lambda: 0,
        )
        gov._abort.set()  # abort already fired before the child registered
        proc = FakeProc()
        gov.register_child(proc)
        assert killed == [proc]

    def test_unregister_clears_child(self):
        gov = ResourceGovernor(
            cpu_cores=1,
            max_cpu_percent=100,
            memory_limit_mb=MIN_MEMORY_LIMIT_MB,
            memory_sampler=lambda: 0,
        )
        proc = FakeProc()
        gov.register_child(proc)
        gov.unregister_child(proc)
        assert gov._children == set()


# --- terminate_process -----------------------------------------------------


class TestTerminateProcess:
    def test_already_exited_is_not_killed(self):
        proc = FakeProc(alive=False)
        terminate_process(proc)
        assert proc.killed is False

    def test_alive_child_is_killed_via_fallback(self, monkeypatch):
        # Force the POSIX killpg path to miss so the proc.kill() fallback runs
        # (deterministic across platforms).
        monkeypatch.setattr(
            rg.os,
            "getpgid",
            lambda _pid: (_ for _ in ()).throw(ProcessLookupError()),
            raising=False,
        )
        proc = FakeProc(alive=True)
        terminate_process(proc)
        assert proc.killed is True

    def test_never_raises_when_kill_fails(self, monkeypatch):
        monkeypatch.setattr(
            rg.os,
            "getpgid",
            lambda _pid: (_ for _ in ()).throw(ProcessLookupError()),
            raising=False,
        )

        class BadProc(FakeProc):
            def kill(self):
                raise OSError("boom")

        # Must swallow the kill error — a cleanup failure can't crash the scan.
        terminate_process(BadProc())


# --- context manager / tracemalloc lifecycle -------------------------------


class TestContextManager:
    def test_context_starts_and_stops_daemon_child_controller(self):
        gov = ResourceGovernor(
            cpu_cores=1,
            max_cpu_percent=50,
            memory_limit_mb=MAX_MEMORY_LIMIT_MB,
            monitor_interval_s=10.0,
            memory_sampler=lambda: 0,
            posix_child_control=True,
        )

        with gov:
            controller = gov._child_controller
            assert controller is not None
            assert controller.daemon is True
            assert controller.is_alive()

        assert gov._child_controller is None
        assert not controller.is_alive()

    def test_default_rss_sampler_is_growth_without_tracemalloc(self, monkeypatch):
        current = {"rss": 100 * _MB}
        monkeypatch.setattr(rg, "_default_rss_peak_bytes", lambda: current["rss"])
        was_tracing = tracemalloc.is_tracing()
        gov = ResourceGovernor(
            cpu_cores=1,
            max_cpu_percent=100,
            memory_limit_mb=MAX_MEMORY_LIMIT_MB,
            monitor_interval_s=10.0,
            sleep=lambda _s: None,
        )
        with gov:
            assert tracemalloc.is_tracing() == was_tracing
            current["rss"] = 160 * _MB
            assert gov._rss_sampler() == 60 * _MB
            current["rss"] = 50 * _MB  # can't happen for a real high-water mark
            assert gov._rss_sampler() == 0
            if not was_tracing:
                # Heap signal stays wired but inert when RSS covers the cap.
                assert gov._memory_sampler() == 0

    def test_starts_and_stops_tracemalloc_when_rss_unavailable(self, monkeypatch):
        monkeypatch.setattr(rg, "_default_rss_peak_bytes", lambda: 0)
        was_tracing = tracemalloc.is_tracing()
        gov = ResourceGovernor(
            cpu_cores=1,
            max_cpu_percent=100,
            memory_limit_mb=MAX_MEMORY_LIMIT_MB,
            monitor_interval_s=0.01,
            sleep=lambda _s: None,
        )
        with gov:
            assert tracemalloc.is_tracing()
        # Only stops it if the governor is the one that started it.
        if not was_tracing:
            assert not tracemalloc.is_tracing()

    def test_does_not_suppress_exceptions(self):
        gov = ResourceGovernor(
            cpu_cores=1,
            max_cpu_percent=100,
            memory_limit_mb=MAX_MEMORY_LIMIT_MB,
            monitor_interval_s=0.01,
            memory_sampler=lambda: 0,
            sleep=lambda _s: None,
        )
        with pytest.raises(ValueError):
            with gov:
                raise ValueError("scan blew up")
        assert gov._monitor is None
