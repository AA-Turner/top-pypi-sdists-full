"""probe.hw.monitor: the collector — one daemon thread per elected node
leader, fail-open everywhere.

Testability is by injection: sources, emit, clock, env, and lock dir are all
parameters; tick() is a plain method the thread calls in a loop, so every
behavior below runs without sleeping. Contracts under test, each traceable
to a locked review decision:
- per-node election (LOCAL_RANK heuristics, file-lock fallback) — 8 DDP
  ranks must not run 8 collectors;
- identity captured at start() and stamped on every point — contextvars are
  thread-local and never reach a daemon thread;
- higher-tier family claims suppress lower tiers; a tripped breaker
  re-delegates the family back down (first-write-wins makes handoff safe);
- circuit breaker: N consecutive failures disables a source, ONE warning;
- series governor: 2500/node runaway guard, family-priority admission;
- emit failures buffer bounded, drop-oldest (the SDK's emit queues in the
  run's journal, so an emit failure means the journal itself is broken).
"""

from __future__ import annotations

import threading
import time

from probe.hw.grid import HW_STEP_SECONDS
from probe.hw.monitor import HwMonitor, elect_leader
from probe.hw.types import HwSample


class FakeClock:
    def __init__(self, t=1_782_000_000.0):
        self.t = t

    def __call__(self):
        return self.t


class FakeSource:
    def __init__(self, samples=(), families=frozenset(), fail=False):
        self.samples = list(samples)
        self.families = frozenset(families)
        self.fail = fail
        self.sample_calls = 0

    def sample(self, ts):
        self.sample_calls += 1
        if self.fail:
            raise RuntimeError("sensor exploded")
        return list(self.samples)

    def probe(self):
        return {}


def _collect_emits():
    emitted = []

    def emit(points):
        emitted.extend(points)

    return emitted, emit


# -- election ---------------------------------------------------------------


def test_local_rank_nonzero_is_never_leader(tmp_path):
    assert not elect_leader("run1", env={"LOCAL_RANK": "3"}, lock_dir=str(tmp_path))


def test_local_rank_zero_is_leader(tmp_path):
    assert elect_leader("run1", env={"LOCAL_RANK": "0"}, lock_dir=str(tmp_path))


def test_no_rank_env_falls_back_to_file_lock_single_winner(tmp_path):
    first = elect_leader("run1", env={}, lock_dir=str(tmp_path))
    second = elect_leader("run1", env={}, lock_dir=str(tmp_path))
    assert first is True and second is False
    # A different run elects its own leader.
    assert elect_leader("run2", env={}, lock_dir=str(tmp_path)) is True


# -- sampling / identity ----------------------------------------------------


def _monitor(sources, emit, clock, **kw):
    return HwMonitor(
        sources=sources,
        emit=emit,
        clock=clock,
        identity={"host": "node1"},
        interval=15.0,
        **kw,
    )


def test_identity_coords_stamped_on_every_point():
    clock = FakeClock()
    emitted, emit = _collect_emits()
    src = FakeSource([HwSample("hw/cpu/utilization", 50.0, {}, "mean")], {"system"})
    mon = _monitor([src], emit, clock)

    mon.tick()
    clock.t += HW_STEP_SECONDS
    mon.tick()

    assert emitted, "completed window should have flushed"
    assert all(p.coords["host"] == "node1" for p in emitted)


def test_device_coords_survive_identity_merge():
    clock = FakeClock()
    emitted, emit = _collect_emits()
    src = FakeSource([HwSample("hw/gpu/utilization", 9.0, {"gpu": 3}, "mean")], {"gpu"})
    mon = _monitor([src], emit, clock)

    mon.tick()
    clock.t += HW_STEP_SECONDS
    mon.tick()

    (point,) = [p for p in emitted if p.key == "hw/gpu/utilization"]
    assert point.coords == {"gpu": 3, "host": "node1"}


# -- tiering / breaker ------------------------------------------------------


def test_higher_tier_claim_suppresses_lower_tier_source():
    clock = FakeClock()
    emitted, emit = _collect_emits()
    scraper = FakeSource([HwSample("hw/gpu/utilization", 1.0, {"gpu": 0}, "mean")], {"gpu"})
    nvml = FakeSource([HwSample("hw/gpu/utilization", 2.0, {"gpu": 0}, "mean")], {"gpu"})
    mon = _monitor([scraper, nvml], emit, clock)  # tier order = list order

    mon.tick()
    assert scraper.sample_calls == 1
    assert nvml.sample_calls == 0


def test_breaker_trips_and_redelegates_family_down_tier():
    clock = FakeClock()
    emitted, emit = _collect_emits()
    scraper = FakeSource(fail=True, families={"gpu"})
    nvml = FakeSource([HwSample("hw/gpu/utilization", 2.0, {"gpu": 0}, "mean")], {"gpu"})
    mon = _monitor([scraper, nvml], emit, clock, breaker_threshold=3)

    for _ in range(3):
        mon.tick()
        clock.t += 1
    assert nvml.sample_calls == 0  # still suppressed while scraper is alive

    mon.tick()  # breaker now open: family re-delegated
    assert nvml.sample_calls == 1
    assert scraper.sample_calls == 3  # disabled source is not called again


def test_source_failure_never_propagates():
    clock = FakeClock()
    _, emit = _collect_emits()
    mon = _monitor([FakeSource(fail=True, families={"gpu"})], emit, clock)
    mon.tick()  # must not raise


# -- governor ---------------------------------------------------------------


def test_governor_refuses_new_series_past_cap_with_family_priority():
    """At the cap, remaining slots go to higher-priority families first:
    hw/proc/* is the first family degraded, core gpu/system metrics last."""
    clock = FakeClock()
    emitted, emit = _collect_emits()
    samples = [HwSample("hw/proc/rss_bytes", 1.0, {"i": i}, "max") for i in range(3)] + [
        HwSample("hw/gpu/utilization", 1.0, {"gpu": i}, "mean") for i in range(3)
    ]
    src = FakeSource(samples, {"gpu", "system"})
    mon = _monitor([src], emit, clock, governor_max_series=4)

    mon.tick()
    clock.t += HW_STEP_SECONDS
    mon.tick()

    keys = sorted({(p.key, tuple(sorted(p.coords.items()))) for p in emitted})
    gpu_series = [k for k in keys if k[0] == "hw/gpu/utilization"]
    proc_series = [k for k in keys if k[0] == "hw/proc/rss_bytes"]
    assert len(gpu_series) == 3  # high priority: all admitted
    assert len(proc_series) == 1  # low priority: only the leftover slot


# -- backpressure -----------------------------------------------------------


def test_emit_failure_buffers_and_retries_then_drops_oldest():
    clock = FakeClock()
    delivered = []
    failing = {"on": True}

    def emit(points):
        if failing["on"]:
            raise ConnectionError("outage")
        delivered.extend(points)

    src = FakeSource([HwSample("hw/cpu/utilization", 5.0, {}, "mean")], {"system"})
    mon = _monitor([src], emit, clock, buffer_max_points=2)

    for _ in range(4):  # four completed windows during the outage; buffer holds 2
        clock.t += HW_STEP_SECONDS
        mon.tick()

    failing["on"] = False
    clock.t += HW_STEP_SECONDS
    mon.tick()

    steps = sorted({p.step for p in delivered})
    # Bounded buffer: the oldest windows were dropped, the newest survived.
    assert len(steps) <= 3
    assert steps[-1] == (int(clock.t) // HW_STEP_SECONDS) - 1


# -- lifecycle --------------------------------------------------------------


def test_start_and_finish_run_and_join_the_daemon_thread():
    emitted, emit = _collect_emits()
    src = FakeSource([HwSample("hw/cpu/utilization", 5.0, {}, "mean")], {"system"})
    mon = HwMonitor(sources=[src], emit=emit, identity={"host": "n1"}, interval=0.01)

    mon.start()
    assert mon._thread is not None and mon._thread.daemon
    deadline = threading.Event()
    deadline.wait(0.1)  # let a few ticks happen
    mon.finish()
    assert src.sample_calls >= 1
    assert not mon._thread.is_alive()


def test_finish_abandons_a_hung_collector_within_its_timeout_and_it_emits_nothing_late():
    """A source hung in a driver call (NVML on a failing GPU). finish() joined
    the collector for 5 s, then sampled AGAIN on the caller's thread -- which
    hung too, with no limit. Now it gives up within ``timeout``, never calls a
    source itself, and the stuck tick emits nothing into the closed run when
    it finally returns."""
    clock = FakeClock()
    emitted, emit = _collect_emits()
    release = threading.Event()
    in_hung_call = threading.Event()
    callers: list[str] = []

    class HungSource:
        families = frozenset({"gpu"})

        def sample(self, ts):
            callers.append(threading.current_thread().name)
            if len(callers) > 1:
                in_hung_call.set()
                release.wait(10)
            return [HwSample("hw/gpu/utilization", 50.0, {"gpu": "0"}, "mean")]

    mon = HwMonitor([HungSource()], emit=emit, clock=clock, interval=0.01)
    mon.tick()  # a window's sample, as the collector took it
    clock.t += HW_STEP_SECONDS  # that window is complete now
    mon.start()
    try:
        assert in_hung_call.wait(5)
        started = time.monotonic()
        mon.finish(timeout=0.3)
        took = time.monotonic() - started
    finally:
        release.set()
    mon._thread.join(5)
    assert took < 1.0, f"finish(timeout=0.3) took {took:.1f}s"
    assert callers.count(threading.current_thread().name) == 1, "finish() sampled"
    assert not mon._thread.is_alive()
    assert emitted == [], "the stuck tick emitted into a closed run"


def test_a_clean_finish_never_samples_on_the_callers_thread():
    """Stopping a healthy collector: its windows are flushed, but every source
    call is the collector thread's. The last pass used to tick -- a sample on
    the CALLER's thread, which a hung driver call then held with no limit."""
    emitted, emit = _collect_emits()
    callers: list[int] = []

    class Source:
        families = frozenset({"system"})

        def sample(self, ts):
            callers.append(threading.get_ident())
            return [HwSample("hw/cpu/utilization", 5.0, {}, "mean")]

    clock = FakeClock()
    mon = HwMonitor([Source()], emit=emit, clock=clock, interval=0.01)
    mon.start()
    deadline = time.monotonic() + 5
    while len(callers) < 3 and time.monotonic() < deadline:
        time.sleep(0.01)  # the collector has sampled the open window
    clock.t += HW_STEP_SECONDS  # that window is complete now
    mon.finish(timeout=2.0)
    assert callers, "the collector never sampled"
    assert threading.get_ident() not in callers, "finish() sampled on the caller's thread"
    first = int(clock.t) // HW_STEP_SECONDS - 1
    # The completed window, then the open one the collector's last pass sampled.
    assert [(p.key, p.step) for p in emitted] == [
        ("hw/cpu/utilization", first),
        ("hw/cpu/utilization", first + 1),
    ]


# -- the last, partial window (environment suite, lane E3) ---------------------


class _Readings:
    """A source whose reading is the clock's second within its minute, so a
    window's mean says which samples it holds."""

    families = frozenset({"system"})

    def __init__(self, clock):
        self.clock = clock
        self.thread_names: list[str] = []

    def sample(self, ts):
        self.thread_names.append(threading.current_thread().name)
        return [HwSample("hw/cpu/utilization", float(ts % HW_STEP_SECONDS), {}, "mean")]


def _aligned(offset: float) -> float:
    """An instant ``offset`` seconds into a hardware window."""
    return (1_782_000_000 // HW_STEP_SECONDS) * HW_STEP_SECONDS + offset


def test_a_run_under_a_minute_records_its_one_window():
    """A 10 s run. Windows are 60 s and were sent only once closed, and the
    collector first samples after one interval (15 s): the run recorded no
    hardware at all. The close now takes one last sample on the collector
    thread and sends the open window."""
    clock = FakeClock(_aligned(20.0))
    emitted, emit = _collect_emits()
    source = _Readings(clock)
    mon = HwMonitor([source], emit=emit, clock=clock, interval=3600)  # never ticks by itself
    mon.start()
    clock.t += 10.0  # the run's whole life
    mon.finish(timeout=2.0)
    assert [(p.key, p.step, p.value) for p in emitted] == [
        ("hw/cpu/utilization", int(clock.t) // HW_STEP_SECONDS, 30.0)
    ]
    assert source.thread_names == ["probe-hw-monitor"], "sampled once, on the collector thread"


def test_a_70s_run_records_its_second_partial_window():
    """Samples at +15/+30/+45 fill window 0; the +60 sample opens window 1,
    which the run's close at +70 left unsent -- every run lost its last
    partial minute. Now window 1 is sent at the close, holding the +60 sample
    and the last pass's +70 one, and window 0 exactly once."""
    t0 = _aligned(0.0)
    clock = FakeClock(t0)
    emitted, emit = _collect_emits()
    mon = HwMonitor([_Readings(clock)], emit=emit, clock=clock, interval=3600)
    for at in (15.0, 30.0, 45.0, 60.0):
        clock.t = t0 + at
        mon.tick()  # the collector's own ticks, driven by hand
    mon.start()
    clock.t = t0 + 70.0
    mon.finish(timeout=2.0)
    first = int(t0) // HW_STEP_SECONDS
    assert [(p.step, p.value) for p in emitted] == [
        (first, 30.0),  # mean of 15, 30, 45: sent when the +60 tick closed it
        (first + 1, 5.0),  # mean of 0 (+60) and 10 (+70): the partial window
    ]


def test_a_stuck_last_pass_is_abandoned_within_the_close_budget():
    """The last sample hangs (a driver call on a failing GPU): finish()
    returns within its timeout, never samples itself, and nothing is emitted
    into the closed run when the sample finally returns."""
    clock = FakeClock(_aligned(20.0))
    emitted, emit = _collect_emits()
    release = threading.Event()
    entered = threading.Event()

    class Hangs:
        families = frozenset({"gpu"})

        def sample(self, ts):
            entered.set()
            release.wait(10)
            return [HwSample("hw/gpu/utilization", 50.0, {"gpu": "0"}, "mean")]

    mon = HwMonitor([Hangs()], emit=emit, clock=clock, interval=3600)
    mon.start()
    started = time.monotonic()
    try:
        mon.finish(timeout=0.3)
        took = time.monotonic() - started
        assert entered.is_set(), "the last pass never sampled"
    finally:
        release.set()
    mon._thread.join(5)
    assert took < 1.0, f"finish(timeout=0.3) took {took:.1f}s"
    assert emitted == [], "the abandoned last pass emitted into a closed run"


def test_a_stop_without_finish_takes_no_last_sample():
    """`request_stop` (an abandoned run's finalizer, a Ctrl-C in the close)
    ends the collector without the last pass: nothing more is sampled or sent
    for a run that is not closing normally."""
    clock = FakeClock(_aligned(20.0))
    emitted, emit = _collect_emits()
    source = _Readings(clock)
    mon = HwMonitor([source], emit=emit, clock=clock, interval=3600)
    mon.start()
    mon.request_stop()
    mon._thread.join(5)
    assert not mon._thread.is_alive()
    assert source.thread_names == [] and emitted == []


# -- start hook (plan 0.3) ----------------------------------------------------


def test_on_start_runs_off_the_callers_thread_and_finish_waits_for_it_briefly():
    """The inventory publication: off the run() path (probe() can block on
    NVML init or an exporter round trip), and finish() waits for it -- so in
    the common case its env_ref PATCH is queued before the close drains."""
    ran: list[str] = []
    started = threading.Event()
    release = threading.Event()

    def on_start():
        started.set()
        release.wait(2.0)
        ran.append(threading.current_thread().name)

    _, emit = _collect_emits()
    mon = HwMonitor(sources=[], emit=emit, interval=3600.0, on_start=on_start)
    mon.start()
    assert started.wait(2.0)
    assert ran == []  # start() returned while the hook was still working
    threading.Timer(0.1, release.set).start()
    mon.finish()  # the hook is still blocked when this is called
    assert ran == ["probe-hw-inventory"]


def test_a_slow_on_start_never_holds_finish():
    """A hook stuck on a slow API (the transport allows 30 s) must not hold
    the run's close: finish() waits `on_start_wait` and moves on."""
    release = threading.Event()
    _, emit = _collect_emits()
    mon = HwMonitor(
        sources=[], emit=emit, interval=3600.0, on_start=lambda: release.wait(10.0),
        on_start_wait=0.2,
    )
    mon.start()
    try:
        started = time.monotonic()
        mon.finish()
        assert time.monotonic() - started < 1.0
        assert mon._hook_thread.is_alive()  # abandoned, not joined
    finally:
        release.set()
        mon._hook_thread.join(2.0)


def test_a_raising_on_start_never_stops_the_collector():
    emitted, emit = _collect_emits()
    src = FakeSource([HwSample("hw/cpu/utilization", 5.0, {}, "mean")], {"system"})

    def on_start():
        raise RuntimeError("inventory exploded")

    mon = HwMonitor(sources=[src], emit=emit, interval=0.01, on_start=on_start)
    mon.start()
    threading.Event().wait(0.1)
    mon.finish()
    assert src.sample_calls >= 1
