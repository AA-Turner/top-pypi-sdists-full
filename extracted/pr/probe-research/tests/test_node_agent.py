"""The node agent: the one observer that outlives the job.

Two properties carry everything here. It must never mistake a live process for
a dead one, because that puts a crash email in front of somebody whose job is
running. And it must never mistake a recycled process id for the original,
because that does the opposite and quietly hides a death forever.
"""

from __future__ import annotations

import json
import os
import sys

import pytest

from probe.box import registry, watch

RUN = "11111111-1111-4111-8111-111111111111"


@pytest.fixture
def box(tmp_path):
    return tmp_path / "runs"


# -- the registry ---------------------------------------------------------------


def test_a_registered_run_records_this_process(box) -> None:
    registry.register(RUN, directory=box, context="default", base_url="https://api.example")

    (entry,) = registry.entries(box)
    assert entry["run_id"] == RUN
    assert entry["pid"] == os.getpid()
    assert entry["context"] == "default"
    assert entry["base_url"] == "https://api.example"
    assert entry["create_time"] is not None, "identity needs more than a pid"


def test_a_closed_run_leaves_nothing_to_explain(box) -> None:
    registry.register(RUN, directory=box)
    registry.deregister(RUN, directory=box)
    assert registry.entries(box) == []


def test_a_run_id_cannot_escape_the_directory(box) -> None:
    """The id is a server-minted UUID, but it arrives from a caller and becomes
    a filename."""
    registry.register("../../etc/passwd", directory=box)
    written = list(box.glob("**/*"))
    assert all(p.parent == box for p in written)
    assert not (box.parent.parent / "etc").exists()


def test_a_corrupt_entry_does_not_blind_the_watcher(box) -> None:
    registry.register(RUN, directory=box)
    (box / "garbage.json").write_text("{not json")
    (box / "future.json").write_text(json.dumps({"schema": 99, "run_id": "x", "pid": 1}))

    assert [e["run_id"] for e in registry.entries(box)] == [RUN]


def test_entries_on_a_missing_directory_is_empty_not_an_error(tmp_path) -> None:
    assert registry.entries(tmp_path / "never-created") == []


# -- liveness, where both mistakes live ------------------------------------------


def test_this_process_reads_as_alive(box) -> None:
    registry.register(RUN, directory=box)
    (entry,) = registry.entries(box)
    assert registry.process_is_alive(entry) is True


def test_a_pid_that_is_gone_reads_as_gone(box) -> None:
    registry.register(RUN, directory=box)
    (entry,) = registry.entries(box)
    entry["pid"] = 999_999  # above the default pid_max on every platform we run
    assert registry.process_is_alive(entry) is False


def test_a_recycled_pid_is_not_the_original_process(box) -> None:
    """The quiet failure this guards: a new process takes the dead one's id,
    the watcher reads the run as healthy, and the death is never reported."""
    registry.register(RUN, directory=box)
    (entry,) = registry.entries(box)
    entry["create_time"] = float(entry["create_time"]) - 500.0
    assert registry.process_is_alive(entry) is False


def test_an_unreadable_process_is_not_evidence_of_death(box, monkeypatch) -> None:
    """Returning False on a permission error would invent a death. Silence is
    not evidence."""
    registry.register(RUN, directory=box)
    (entry,) = registry.entries(box)
    entry["create_time"] = None  # nothing to compare against
    assert registry.process_is_alive(entry) is True


# -- the sweep --------------------------------------------------------------------


@pytest.fixture
def reported(monkeypatch):
    calls: list[dict] = []
    monkeypatch.setattr(watch, "report_vanished", lambda entry, **kw: calls.append(entry) or True)
    return calls


def test_a_live_run_is_left_alone(box, reported) -> None:
    registry.register(RUN, directory=box)

    tally = watch.sweep(box)

    assert tally == {"alive": 1, "gone": 0, "reported": 0}
    assert reported == []
    assert len(registry.entries(box)) == 1, "a live run stays registered"


def test_a_vanished_process_is_reported_once_and_forgotten(box, reported) -> None:
    registry.register(RUN, directory=box)
    entry_path = next(box.glob("*.json"))
    entry = json.loads(entry_path.read_text())
    entry["pid"] = 999_999
    entry_path.write_text(json.dumps(entry))

    tally = watch.sweep(box)

    assert tally == {"alive": 0, "gone": 1, "reported": 1}
    assert [e["run_id"] for e in reported] == [RUN]
    assert registry.entries(box) == [], "nothing left to watch"
    assert watch.sweep(box)["gone"] == 0, "and never reported twice"


def test_an_unreportable_death_still_stops_being_watched(box, monkeypatch) -> None:
    """The server's reaper is still behind this. Retrying forever would turn
    one unreachable API into a permanent spin."""
    monkeypatch.setattr(watch, "report_vanished", lambda entry, **kw: False)
    registry.register(RUN, directory=box)
    path = next(box.glob("*.json"))
    entry = json.loads(path.read_text())
    entry["pid"] = 999_999
    path.write_text(json.dumps(entry))

    tally = watch.sweep(box)

    assert tally == {"alive": 0, "gone": 1, "reported": 0}
    assert registry.entries(box) == []


# -- the loop ---------------------------------------------------------------------


def test_the_watcher_exits_when_the_box_goes_quiet(box) -> None:
    """Otherwise it idles forever on a laptop. A later run spawns a new one."""
    clock = [0.0]

    def now():
        return clock[0]

    def sleep(seconds):
        clock[0] += seconds

    totals = watch.watch_forever(
        interval=10.0, idle_exit_seconds=30.0, directory=box, now=now, sleep=sleep
    )

    assert totals["sweeps"] >= 3
    assert totals["gone"] == 0


def test_a_live_run_keeps_the_watcher_awake(box, reported) -> None:
    registry.register(RUN, directory=box)
    clock = [0.0]
    sweeps = {"n": 0}

    def now():
        return clock[0]

    def sleep(seconds):
        clock[0] += seconds
        sweeps["n"] += 1
        if sweeps["n"] > 5:
            # The run outlives the idle window; end the test by removing it.
            registry.deregister(RUN, directory=box)

    totals = watch.watch_forever(
        interval=10.0, idle_exit_seconds=20.0, directory=box, now=now, sleep=sleep
    )

    assert totals["sweeps"] > 5, "a live run must not let it time out"


def test_a_zero_interval_is_a_kill_switch(box) -> None:
    assert watch.watch_forever(interval=0, directory=box)["sweeps"] == 0


# -- the switch --------------------------------------------------------------------


@pytest.mark.parametrize("value", ["1", "true", "on", "TRUE"])
def test_the_agent_is_opt_in(value: str) -> None:
    assert watch.enabled({"PROBE_BOX": value}) is True


@pytest.mark.parametrize("env", [{}, {"PROBE_BOX": "0"}, {"PROBE_BOX": ""}])
def test_and_off_by_default(env: dict) -> None:
    assert watch.enabled(env) is False


# -- the lease ---------------------------------------------------------------------


def test_the_lease_admits_exactly_one_watcher(box) -> None:
    """Sixty-four ranks start together and all of them try. Only one wins."""
    from probe.box import spawn

    assert spawn.already_running(box) is False
    held = spawn.hold_lease(box)
    assert held is not None
    assert spawn.already_running(box) is True
    assert spawn.hold_lease(box) is None, "a second watcher must not start"
    held.close()
    assert spawn.already_running(box) is False, "and the lease dies with its holder"


def test_spawning_is_a_no_op_while_a_watcher_holds_the_lease(box, monkeypatch) -> None:
    from probe.box import spawn

    monkeypatch.setenv("PROBE_BOX", "1")
    started: list[object] = []
    monkeypatch.setattr(spawn.subprocess, "Popen", lambda *a, **k: started.append(a) or object())

    held = spawn.hold_lease(box)
    assert spawn.maybe_spawn(box) is False
    assert started == []
    held.close()

    assert spawn.maybe_spawn(box) is True
    assert len(started) == 1


def test_nothing_spawns_when_the_agent_is_off(box, monkeypatch) -> None:
    from probe.box import spawn

    monkeypatch.delenv("PROBE_BOX", raising=False)
    monkeypatch.setattr(
        spawn.subprocess, "Popen", lambda *a, **k: pytest.fail("spawned while disabled")
    )
    assert spawn.maybe_spawn(box) is False


def test_the_watcher_leaves_the_training_process_group(box, monkeypatch) -> None:
    """A watcher inside the job's process group would take the same Ctrl-C the
    job takes, and a Ctrl-C is one of the deaths it exists to observe."""
    from probe.box import spawn

    monkeypatch.setenv("PROBE_BOX", "1")
    seen: dict = {}
    monkeypatch.setattr(
        spawn.subprocess, "Popen", lambda *a, **k: seen.update(argv=a[0], **k) or object()
    )

    spawn.maybe_spawn(box)

    assert seen["start_new_session"] is True
    assert seen["argv"][1:] == ["-m", "probe.box"]
    assert seen["argv"][0] == sys.executable, "the watcher runs on the job's interpreter"


def _rewrite(box, **fields) -> None:
    entry_path = next(box.glob("*.json"))
    entry = json.loads(entry_path.read_text())
    entry.update(fields)
    entry_path.write_text(json.dumps(entry))


@pytest.mark.parametrize(
    "fields",
    [
        {"host": "gpu-node-17"},  # a shared HOME across an HPC cluster
        {"pidns": "pid:[4026532999]"},  # a container sharing HOME with its host
    ],
    ids=["another-host", "another-pid-namespace"],
)
def test_another_machines_run_is_not_judged_here(box, reported, fields) -> None:
    """Review of #2049: with PROBE_BOX=1 and a HOME shared across machines,
    this watcher read node A's live run as dead (its pid does not exist HERE)
    and reported writer-gone, crashing a run that was training."""
    registry.register(RUN, directory=box)
    _rewrite(box, pid=999_999, **fields)

    tally = watch.sweep(box)

    assert tally == {"alive": 0, "gone": 0, "reported": 0}
    assert reported == []
    assert len(registry.entries(box)) == 1, "left for the watcher on its own host"


def test_an_entry_records_its_pid_namespace(box) -> None:
    registry.register(RUN, directory=box)
    entry = json.loads(next(box.glob("*.json")).read_text())
    assert entry["pidns"] == registry.pid_namespace()
    assert registry.is_local(entry)
