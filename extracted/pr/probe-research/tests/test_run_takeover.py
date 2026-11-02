"""SDK reliability 2.3: a requeued job takes over its own silent run.

A preempted pod's replacement relaunches with the same `external_id` while
the old run still reads `running` (the reaper needs 900 s). Before this, every
policy refused a `running` incumbent, so the relaunch died at `init()` with a
ConflictError for ~15 minutes. Now `auto`/`resume`/`Rewind` ask the server to
take the run over once it has been silent long enough to be dead, waiting
within `PROBE_TAKEOVER_WAIT_SEC` when it is not yet.

The server judges a BEATING incumbent by its beats and waits the reaper's own
900 s for one with no beat cadence (review of #2019). The fake mirrors that
with two clocks: `run_beat_silence` (beats) and `run_silence` (anything).

And before ANY resume or takeover the relaunch delivers what the dead attempt
left queued in the (persistent) outbox, minus its queued status writes: the
reopen moves the run to a new write epoch, and every op still carrying the old
one would be fenced.
"""

from __future__ import annotations

import json
import sys
import types

import pytest

from probe import errors
from probe.sdk import client as client_mod
from tests.conftest import make_client

EXTERNAL_ID = "requeue-job"


def _launch(client, **kw):
    return client.run(
        project="takeover-lab",
        name=EXTERNAL_ID,
        external_id=EXTERNAL_ID,
        heartbeat=False,
        **kw,
    )


def _quiet(app, run_id: str, seconds: float, *, beating: bool = True) -> None:
    """The incumbent has been silent `seconds`. `beating` models an owner on
    a beat cadence (a beat after its insert stamp)."""
    app.run_heartbeats[run_id] = max(2, app.run_heartbeats.get(run_id, 0)) if beating else 0
    app.run_beat_silence[run_id] = seconds
    app.run_silence[run_id] = seconds


@pytest.fixture
def lab(client):
    client.create_project("takeover-lab", "Takeover Lab", kind="general")
    return client


@pytest.fixture
def sleeps(app, monkeypatch):
    """Replace the real wait. By default time passes and the incumbent stays
    silent; a test flips `speaks` to model a live incumbent that beats."""

    class Sleeps(list):
        state = {"speaks": False}

    record = Sleeps()

    def fake_sleep(seconds: float) -> None:
        record.append(seconds)
        for clock in (app.run_silence, app.run_beat_silence):
            for rid, silent in list(clock.items()):
                clock[rid] = 10.0 if record.state["speaks"] else silent + seconds

    monkeypatch.setattr(client_mod.resources.runs.reopen.takeover, "_takeover_sleep", fake_sleep, raising=False)
    return record


def _reopens(app) -> list:
    return [r for r in app.requests if r.url.path.endswith("/reopen")]


def test_a_silent_incumbent_is_taken_over_in_place(lab, app, sleeps):
    first = _launch(lab)
    first.log({"loss": 0.5}, step=10)
    first.log({"loss": 0.4}, step=20)
    _quiet(app, first.id, 400.0)

    second = _launch(lab)

    assert second.id == first.id, "the same run, not a -r2 sibling"
    assert app.runs[first.id]["status"] == "running"
    assert app.runs[first.id]["write_epoch"] == 2
    assert second.write_epoch == 2
    assert sleeps == [], "a silent incumbent needs no wait"
    assert second._resume_from_step == 20, "the resume guard is armed at its last step"


def test_a_short_wait_then_the_takeover(lab, app, sleeps, monkeypatch):
    monkeypatch.setenv("PROBE_TAKEOVER_WAIT_SEC", "300")
    first = _launch(lab)
    _quiet(app, first.id, 175.0)  # 5 s short of the 180 s threshold

    with pytest.warns(UserWarning, match="still reads running") as caught:
        second = _launch(lab)

    assert sleeps == [5.0]
    assert len([w for w in caught if "still reads running" in str(w.message)]) == 1
    assert second.id == first.id and second.write_epoch == 2
    sessions = {r.content for r in _reopens(app)}
    assert len(_reopens(app)) == 2 and len(sessions) == 1, "the retry reuses its session"


def test_a_small_budget_still_covers_one_full_threshold(lab, app, sleeps, monkeypatch):
    """Review of #2019: a budget under the threshold failed at the first 409,
    so a relaunch seconds after the death could never take over. Any budget
    that allows a wait covers the threshold plus slack."""
    monkeypatch.setenv("PROBE_TAKEOVER_WAIT_SEC", "60")
    first = _launch(lab)
    _quiet(app, first.id, 0.0)  # died a moment ago

    with pytest.warns(UserWarning, match="still reads running"):
        second = _launch(lab)

    assert sleeps == [180.0]
    assert second.id == first.id and second.write_epoch == 2


def test_a_live_incumbent_waits_out_the_budget_then_conflicts(lab, app, sleeps, monkeypatch):
    """At the first 409 a pod dead for seconds and a live one look alike, so
    the relaunch waits; a live incumbent keeps beating, the server keeps
    refusing, and once the budget cannot cover the next wait it conflicts."""
    monkeypatch.setenv("PROBE_TAKEOVER_WAIT_SEC", "300")
    first = _launch(lab)
    _quiet(app, first.id, 0.0)
    sleeps.state["speaks"] = True

    with pytest.warns(UserWarning, match="still reads running"):
        with pytest.raises(errors.ConflictError) as excinfo:
            _launch(lab)

    assert sleeps == [180.0], "one wait, then the next one no longer fits the budget"
    assert "alive" in str(excinfo.value)
    assert app.runs[first.id]["write_epoch"] == 1


def test_no_budget_conflicts_without_sleeping(lab, app, sleeps):
    """The suite's own default (PROBE_TAKEOVER_WAIT_SEC=0), and a notebook's."""
    first = _launch(lab)

    with pytest.raises(errors.ConflictError) as excinfo:
        _launch(lab)

    assert sleeps == []
    assert "alive" in str(excinfo.value) and "PROBE_TAKEOVER_WAIT_SEC" in str(excinfo.value)
    assert app.runs[first.id]["write_epoch"] == 1


def test_an_incumbent_that_never_beat_waits_the_reapers_window(lab, app, sleeps, monkeypatch):
    """Review of #2019, HIGH-1: heartbeat=False, PROBE_HEARTBEAT_SECONDS=0 or a
    legacy client never beats on a cadence, so a quiet eval looks exactly
    like death. The server asks for the reaper's 900 s, past a 300 s budget."""
    monkeypatch.setenv("PROBE_TAKEOVER_WAIT_SEC", "300")
    first = _launch(lab)
    _quiet(app, first.id, 400.0, beating=False)

    with pytest.raises(errors.ConflictError):
        _launch(lab)

    assert sleeps == []
    assert app.runs[first.id]["write_epoch"] == 1

    _quiet(app, first.id, 1000.0, beating=False)
    assert _launch(lab).write_epoch == 2


def test_a_server_without_takeover_keeps_todays_conflict(lab, app, sleeps):
    app.supports_takeover = False
    first = _launch(lab)
    _quiet(app, first.id, 5000.0)

    with pytest.raises(errors.ConflictError) as excinfo:
        _launch(lab)

    assert "alive" in str(excinfo.value)
    assert _reopens(app) == [], "an older server is never asked (it would refuse anyway)"
    assert sleeps == []


def test_a_notebook_does_not_wait_by_default(lab, app, sleeps, monkeypatch):
    monkeypatch.delenv("PROBE_TAKEOVER_WAIT_SEC", raising=False)
    monkeypatch.setitem(sys.modules, "ipykernel", types.ModuleType("ipykernel"))
    first = _launch(lab)
    _quiet(app, first.id, 175.0)

    with pytest.raises(errors.ConflictError):
        _launch(lab)
    assert sleeps == []


def test_the_default_wait_budget(monkeypatch):
    monkeypatch.delenv("PROBE_TAKEOVER_WAIT_SEC", raising=False)
    monkeypatch.delitem(sys.modules, "ipykernel", raising=False)
    assert client_mod._takeover_wait_budget() == 300.0
    monkeypatch.setenv("PROBE_TAKEOVER_WAIT_SEC", "12")
    assert client_mod._takeover_wait_budget() == 12.0


@pytest.mark.parametrize(
    ("beat", "threshold"),
    [(None, 180), ("0", 180), ("60", 180), ("100", 300), ("5000", 3600)],
)
def test_the_silence_threshold_is_three_beats_within_the_servers_bounds(
    monkeypatch, beat, threshold
):
    if beat is None:
        monkeypatch.delenv("PROBE_HEARTBEAT_SECONDS", raising=False)
    else:
        monkeypatch.setenv("PROBE_HEARTBEAT_SECONDS", beat)
    assert client_mod._takeover_threshold() == threshold


def test_rewind_takes_over_a_silent_running_run(lab, app, sleeps):
    import probe

    first = _launch(lab)
    for step in (10, 20, 30):
        first.log({"loss": 1.0}, step=step)
    _quiet(app, first.id, 400.0)

    second = _launch(lab, on_conflict=probe.Rewind(step=20))

    assert second.id == first.id and second.write_epoch == 2
    kept = {p["step_index"] for p in app.metric_points_posted[first.id]}
    assert kept == {10}, "the rewind still discards from its step"


def test_the_superseded_process_is_told_and_stops_beating(lab, app, sleeps):
    """Review of #2019: after a takeover the old process's beats are refused
    (409, stale epoch). It says so once and stops, instead of beating into a
    wall and having every later write dead-lettered in silence."""
    import threading
    import weakref

    from probe.sdk.run.closing.heartbeat import _beat_forever

    first = _launch(lab)
    _quiet(app, first.id, 400.0)
    _launch(lab)  # the relaunch takes over: epoch 2
    beats_before = app.run_heartbeats.get(first.id, 0)

    stop = threading.Event()
    with pytest.warns(UserWarning, match="taken over by a newer attempt") as caught:
        thread = threading.Thread(
            target=_beat_forever,
            args=(lab, first.id, stop, 0.005, "owner", first.write_epoch, False, weakref.ref(first)),
            daemon=True,
        )
        thread.start()
        thread.join(timeout=5)
    stop.set()

    assert not thread.is_alive(), "the beat thread must end"
    assert len([w for w in caught if "taken over" in str(w.message)]) == 1
    assert app.run_heartbeats.get(first.id, 0) == beats_before
    assert [w["path"] for w in app.fenced_writes][-1].endswith("/heartbeat")


# -- the drain barrier: the dead attempt's queue lands BEFORE the new epoch ----


def _requeue_scenario(app, tmp_path, *, close: str | None = None):
    """Pod 1 opens the run on a persistent outbox, logs 50 steps through an
    outage (all queued, none delivered) and is deleted -- optionally after
    queueing its own close. Pod 2 relaunches with the same outbox."""
    outbox = tmp_path / "pv-outbox"
    pod1 = make_client(app, tmp_spool=outbox, async_writes=True)
    pod1.create_project("takeover-lab", "Takeover Lab", kind="general")
    old = _launch(pod1)
    for step in range(50):
        old.log({"loss": 1.0 / (step + 1)}, step=step)
    if close is not None:
        old.set_status(close)
    _quiet(app, old.id, 1000.0)  # the pod is gone; nothing reaped it yet
    pod2 = make_client(app, tmp_spool=outbox, async_writes=True)
    return old, pod2


def test_a_requeue_delivers_the_dead_attempts_backlog_first(app, tmp_path, monkeypatch, sleeps):
    monkeypatch.setenv("PROBE_TAKEOVER_WAIT_SEC", "300")
    old, pod2 = _requeue_scenario(app, tmp_path)

    new = _launch(pod2)
    for step in range(50, 60):
        new.log({"loss": 0.01}, step=step)
    pod2.flush()

    assert new.id == old.id and new.write_epoch == 2
    assert pod2.journal.failed() == [], "the dead attempt's queue was fenced"
    assert app.fenced_writes == []
    steps = {p["step_index"] for p in app.metric_points_posted[old.id]}
    assert steps == set(range(60))
    assert sleeps == [], "delivered data is not a beat: the incumbent stays silent"


@pytest.mark.parametrize("close", ["failed", "canceled"])
def test_the_dead_attempts_queued_close_is_retired_not_delivered(
    app, tmp_path, monkeypatch, sleeps, close
):
    """Review of #2019: the barrier delivered the old attempt's queued close
    first -- a `failed` mailed a crash notice. The relaunch owns the verdict
    of an attempt that did not finish: the close is dead-lettered, the data
    lands. (A `completed` close is the next test's.)"""
    old, pod2 = _requeue_scenario(app, tmp_path, close=close)

    new = _launch(pod2)

    assert new.write_epoch == 2 and app.runs[old.id]["status"] == "running"
    (dead,) = pod2.journal.failed()
    assert dead[1]["method"] == "PATCH" and dead[1]["body"]["status"] == close
    assert "takeover" in dead[1]["last_error"]
    assert len({p["step_index"] for p in app.metric_points_posted[old.id]}) == 50


def test_a_finished_incumbents_completed_close_is_delivered_not_taken_over(
    app, tmp_path, monkeypatch, sleeps
):
    """Follow-up to #2019: the incumbent FINISHED -- its `completed` close was
    still queued when it exited. Retiring that close let the relaunch continue
    a finished run. The barrier now delivers it with the data, and the
    relaunch refuses like any resume of a completed run."""
    old, pod2 = _requeue_scenario(app, tmp_path, close="completed")

    with pytest.raises(errors.ConflictError, match="already completed"):
        _launch(pod2)

    assert app.runs[old.id]["status"] == "completed"
    assert app.runs[old.id]["write_epoch"] == 1, "nothing took the run over"
    assert pod2.journal.failed() == [] and _queued_status(pod2.journal) == []
    assert len({p["step_index"] for p in app.metric_points_posted[old.id]}) == 50


def test_a_rewind_of_a_finished_incumbent_is_a_plain_reopen(app, tmp_path, sleeps):
    """A rewind may reopen a completed run on purpose, so a delivered
    `completed` close turns the takeover into the plain rewind reopen."""
    from probe.sdk.client.resources.runs.reopen.conflict import Rewind

    old, pod2 = _requeue_scenario(app, tmp_path, close="completed")

    new = _launch(pod2, on_conflict=Rewind(step=10))

    assert new.id == old.id and new.write_epoch == 2
    (reopen,) = _reopens(app)
    assert b"takeover_stale_after_seconds" not in reopen.content


def test_without_the_barrier_the_backlog_is_fenced(app, tmp_path, monkeypatch, sleeps):
    """Negative control for the tests above: skip the drain and the reopen's
    new epoch refuses all 50 queued steps. They are set aside in discarded/,
    not dead-lettered: no retry can ever land them (T24)."""
    old, pod2 = _requeue_scenario(app, tmp_path)
    monkeypatch.setattr(
        client_mod.Client, "_drain_before_takeover", lambda self, old: None, raising=False
    )

    _launch(pod2)
    pod2.flush()

    assert pod2.journal.failed() == []
    assert len(list((pod2.journal.dir / "discarded").glob("*.json"))) == 50
    # The drain merges a run's queued metric writes into one POST (plan 1.2),
    # so the fence refuses them in one request: count the writes, not requests.
    assert app.fenced_writes and not app.metric_points_posted.get(old.id)


def test_a_backlog_that_cannot_land_is_reported_not_silently_fenced(
    app, tmp_path, monkeypatch, sleeps
):
    monkeypatch.setenv("PROBE_TAKEOVER_DRAIN_SEC", "0")
    old, pod2 = _requeue_scenario(app, tmp_path)
    app.fail_paths = {f"/v1/runs/{old.id}/metrics"}

    with pytest.warns(UserWarning, match="50 op\\(s\\) the previous attempt"):
        _launch(pod2)


def test_a_live_writer_sharing_the_outbox_stops_the_barrier(app, tmp_path, monkeypatch, sleeps):
    """A duplicate launch on the same box shares the outbox with a LIVE
    writer: its queue keeps growing, so the barrier must not chase it for 120 s
    and then warn about a 'previous attempt'. It stops, and the takeover
    conflicts because the incumbent is not silent."""
    import warnings

    from probe.sdk.delivery import journal as journal_mod

    old, pod2 = _requeue_scenario(app, tmp_path)
    _quiet(app, old.id, 0.0)  # it is alive
    real_drain = journal_mod.drain
    appended = {"n": 0}

    def drain_while_the_live_writer_logs(journal, **kw):
        report = real_drain(journal, **kw)
        appended["n"] += 1
        old.log({"loss": 0.5}, step=1000 + appended["n"])  # the live writer, meanwhile
        return report

    monkeypatch.setattr("probe.sdk.delivery.outbox.drain.drain.drain", drain_while_the_live_writer_logs)
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        with pytest.raises(errors.ConflictError):
            _launch(pod2)

    assert appended["n"] <= 2, "the barrier chased a live queue"
    assert not [w for w in caught if "previous attempt" in str(w.message)]


def test_a_dead_run_resume_also_drains_first(app, tmp_path, monkeypatch, sleeps):
    """The same barrier guards the plain crashed-run resume: its reopen bumps
    the epoch just the same."""
    old, pod2 = _requeue_scenario(app, tmp_path)
    app.runs[old.id]["status"] = "crashed"

    new = _launch(pod2)
    pod2.flush()

    assert new.write_epoch == 2
    assert pod2.journal.failed() == []
    assert {p["step_index"] for p in app.metric_points_posted[old.id]} == set(range(50))


# -- review of #2019, MED-A: a relaunch that does NOT take over never costs the
# incumbent its close. The barrier holds the queued status writes aside and
# retires them only once the reopen succeeds; any refusal puts them back.


def _queued_status(journal) -> list[str]:
    return [
        op["body"]["status"]
        for _, op in journal.pending()
        if op.get("method") == "PATCH" and "status" in (op.get("body") or {})
    ]


@pytest.mark.parametrize("close", ["failed", "canceled"])
def test_a_refused_takeover_puts_the_incumbents_close_back(app, tmp_path, sleeps, close):
    """Pod 1 finished (its close still queued) and exited moments ago; a
    relaunch with no wait budget (a notebook re-run, the suite default) is
    refused. The close is delivered afterwards, as it was before 2.3."""
    old, pod2 = _requeue_scenario(app, tmp_path, close=close)
    _quiet(app, old.id, 5.0)  # beat 5 s ago: not silent enough

    with pytest.raises(errors.ConflictError):
        _launch(pod2)

    assert pod2.journal.failed() == [], "the refused relaunch dead-lettered the close"
    assert _queued_status(pod2.journal) == [close]
    pod2.flush()
    assert app.runs[old.id]["status"] == close


@pytest.mark.parametrize("close", ["failed", "canceled"])
def test_a_reopen_that_errors_puts_the_close_back(app, tmp_path, sleeps, monkeypatch, close):
    old, pod2 = _requeue_scenario(app, tmp_path, close=close)

    def broken(*a, **kw):
        raise errors.TransportError("connection reset")

    monkeypatch.setattr(pod2, "reopen_run", broken)
    with pytest.raises(errors.TransportError):
        _launch(pod2)

    assert pod2.journal.failed() == []
    assert _queued_status(pod2.journal) == [close]


def test_a_no_cadence_incumbent_refused_keeps_its_close(app, tmp_path, sleeps, monkeypatch):
    """The 900 s case: an incumbent that never beat on a cadence, quiet for
    less than the reaper's window, is refused -- and keeps its close."""
    monkeypatch.setenv("PROBE_TAKEOVER_WAIT_SEC", "300")
    old, pod2 = _requeue_scenario(app, tmp_path, close="failed")
    _quiet(app, old.id, 200.0, beating=False)

    with pytest.raises(errors.ConflictError):
        _launch(pod2)

    assert pod2.journal.failed() == []
    assert _queued_status(pod2.journal) == ["failed"]


def test_a_live_duplicates_queued_status_goes_back_when_the_barrier_stops(
    app, tmp_path, monkeypatch, sleeps
):
    """A LIVE writer shares the outbox: its queued status write is its own,
    and goes back the moment the barrier sees it appending."""
    from probe.sdk.delivery import journal as journal_mod

    old, pod2 = _requeue_scenario(app, tmp_path, close="failed")
    _quiet(app, old.id, 0.0)  # it is alive
    real_drain = journal_mod.drain

    def drain_while_the_live_writer_logs(journal, **kw):
        report = real_drain(journal, **kw)
        old.log({"loss": 0.5}, step=2000)
        return report

    monkeypatch.setattr("probe.sdk.delivery.outbox.drain.drain.drain", drain_while_the_live_writer_logs)
    with pytest.raises(errors.ConflictError):
        _launch(pod2)

    assert pod2.journal.failed() == []
    assert _queued_status(pod2.journal) == ["failed"]


def test_a_hold_left_by_a_relaunch_that_died_is_put_back_by_the_next(
    app, tmp_path, monkeypatch, sleeps
):
    """The hold lives in the dead-letter folder, visible, with a deadline. A
    relaunch killed mid-barrier cannot release it; the next one does, once it
    has expired -- and leaves an unexpired one alone."""
    old, pod2 = _requeue_scenario(app, tmp_path, close="failed")
    (name, op), *_ = [
        (p.name, op) for p, op in pod2.journal.pending() if "status" in (op.get("body") or {})
    ]
    held = pod2._hold_status_writes(old=app.runs[old.id], ops={name: op})
    assert held == [name] and _queued_status(pod2.journal) == []
    (_, dead), = pod2.journal.failed()
    assert "held by a relaunch" in dead["last_error"] and dead["blocking"] is False

    pod2._restore_expired_holds()
    assert _queued_status(pod2.journal) == [], "an unexpired hold is someone's barrier"

    path = pod2.journal.failed_dir / name
    raw = client_mod.json.loads(path.read_text())
    raw["takeover_hold"]["until"] = 0
    path.write_text(client_mod.json.dumps(raw))
    pod2._restore_expired_holds()
    assert pod2.journal.failed() == []
    assert _queued_status(pod2.journal) == ["failed"]
    (_, back), = [(p, o) for p, o in pod2.journal.pending() if "status" in (o.get("body") or {})]
    assert "takeover_hold" not in back and "blocking" not in back


def test_a_takeover_drops_the_incumbents_draining_tag(app, tmp_path, sleeps):
    """Review of #2019, LOW-D: the retired close was what would have taken the
    deferred finish's "draining" tag back off."""
    old, pod2 = _requeue_scenario(app, tmp_path, close="failed")
    app.runs[old.id]["tags"] = ["ablation", "draining"]

    new = _launch(pod2)

    assert new.write_epoch == 2
    assert app.runs[old.id]["tags"] == ["ablation"]


def test_an_interrupted_barrier_releases_its_hold(app, tmp_path, monkeypatch, sleeps):
    """Ctrl-C (or a bug) inside the delivery loop must not leave the close
    stranded in the hold until some later relaunch."""

    old, pod2 = _requeue_scenario(app, tmp_path, close="failed")

    def interrupted(journal, **kw):
        raise KeyboardInterrupt

    monkeypatch.setattr("probe.sdk.delivery.outbox.drain.drain.drain", interrupted)
    with pytest.raises(KeyboardInterrupt):
        _launch(pod2)

    assert pod2.journal.failed() == []
    assert _queued_status(pod2.journal) == ["failed"]


def test_the_barrier_is_bounded_inside_a_pass(app, tmp_path, monkeypatch, sleeps):
    """Review of #2019, MED-2: the drain budget bounded only the time BETWEEN
    passes, and one pass delivers a whole backlog. With every delivery slow,
    the barrier now stops at its budget, mid-pass, and says what is left."""
    import time as _time


    monkeypatch.setenv("PROBE_TAKEOVER_DRAIN_SEC", "1")
    monkeypatch.setenv("PROBE_TAKEOVER_WAIT_SEC", "300")
    # One write per request: a coalesced pass (plan 1.2) sends this whole
    # backlog in one POST, well inside the budget this test is about.
    monkeypatch.setattr("probe.sdk.delivery.outbox.drain.coalesce.MERGE_MAX_POINTS", 1)
    real = app.handler
    slow_now = {"on": False}

    def slow(request):
        if slow_now["on"] and request.url.path.endswith("/metrics"):
            _time.sleep(0.2)
        return real(request)

    monkeypatch.setattr(app, "handler", slow)  # bound by every client made from here
    old, pod2 = _requeue_scenario(app, tmp_path)
    slow_now["on"] = True
    started = _time.monotonic()
    with pytest.warns(UserWarning, match="PROBE_TAKEOVER_DRAIN_SEC"):
        _launch(pod2)
    took = _time.monotonic() - started

    delivered = len({p["step_index"] for p in app.metric_points_posted.get(old.id, [])})
    assert took < 4, f"the barrier held init() for {took:.1f}s past a 1 s budget"
    assert 0 < delivered < 50


# -- follow-ups to #2019 -----------------------------------------------------------


def _dead_pid() -> int:
    """A pid that WAS a process on this host and is not any more."""
    import subprocess

    proc = subprocess.Popen([sys.executable, "-c", "pass"])
    proc.wait()
    return proc.pid


def _hold_the_close(app, tmp_path, *, pid: int | None = None, until: float | None = None):
    old, pod2 = _requeue_scenario(app, tmp_path, close="failed")
    (name, op), *_ = [
        (p.name, op) for p, op in pod2.journal.pending() if "status" in (op.get("body") or {})
    ]
    assert pod2._hold_status_writes(old=app.runs[old.id], ops={name: op}) == [name]
    path = pod2.journal.failed_dir / name
    raw = client_mod.json.loads(path.read_text())
    if pid is not None:
        raw["takeover_hold"]["pid"] = pid
    if until is not None:
        raw["takeover_hold"]["until"] = until
    path.write_text(client_mod.json.dumps(raw))
    return old, pod2


def test_a_hold_whose_relaunch_died_on_this_host_goes_back_at_the_next_drain(
    app, tmp_path, sleeps
):
    """A relaunch killed hard mid-barrier left the incumbent's close aside
    for ~17 min, until another barrier ran on this box -- past the reaper's
    900 s, so the run read `crashed` and mailed. Its pid is gone: the very
    next drain pass puts the close back and delivers it."""
    old, pod2 = _hold_the_close(app, tmp_path, pid=_dead_pid())

    pod2.flush()

    assert pod2.journal.failed() == []
    assert app.runs[old.id]["status"] == "failed"
    assert not pod2.journal.holds_marker.exists(), "nothing is held any more"


def test_a_new_client_puts_an_abandoned_hold_back(app, tmp_path, sleeps):
    old, pod2 = _hold_the_close(app, tmp_path, pid=_dead_pid())

    pod3 = make_client(app, tmp_spool=tmp_path / "pv-outbox", async_writes=True)

    assert pod3.journal.failed() == []
    assert _queued_status(pod3.journal) == ["failed"]


def test_a_live_barriers_hold_is_left_alone(app, tmp_path, sleeps):
    """Control: this process holds it (its pid lives) and it has not expired."""
    old, pod2 = _hold_the_close(app, tmp_path)

    pod2.flush()

    (_, held), = pod2.journal.failed()
    assert "takeover_hold" in held
    assert app.runs[old.id]["status"] == "running"


def test_a_hold_is_short_enough_to_beat_the_reaper(monkeypatch):
    """The deadline covers the barrier's two bounded phases plus a short
    margin -- under the reaper's 900 s with the default budgets."""
    monkeypatch.delenv("PROBE_TAKEOVER_DRAIN_SEC", raising=False)
    monkeypatch.delenv("PROBE_TAKEOVER_WAIT_SEC", raising=False)
    total = (
        client_mod._TAKEOVER_DRAIN_SECONDS
        + max(
            client_mod._takeover_wait_budget(),
            client_mod._takeover_threshold() + client_mod._TAKEOVER_BUDGET_SLACK_SECONDS,
        )
        + client_mod._TAKEOVER_HOLD_MARGIN_SECONDS
    )
    assert total < 900


def test_an_outage_stops_the_barrier_at_once(app, tmp_path, monkeypatch, sleeps):
    """In an outage the barrier looped its whole budget outside init's own
    (review of #2019). A server that cannot be reached ends it at the first
    pass, and says why."""
    import time as _time

    import httpx

    monkeypatch.setenv("PROBE_TAKEOVER_DRAIN_SEC", "5")
    real = app.handler
    down = {"on": False}

    def unreachable(request):
        if down["on"] and request.url.path.endswith("/metrics"):
            raise httpx.ConnectError("connection refused", request=request)
        return real(request)

    monkeypatch.setattr(app, "handler", unreachable)
    old, pod2 = _requeue_scenario(app, tmp_path)
    down["on"] = True
    started = _time.monotonic()
    with pytest.warns(UserWarning, match="could not be reached"):
        _launch(pod2)
    assert _time.monotonic() - started < 2.5


def _queue_open_archive(pod, run_id: str, tmp_path) -> None:
    """The open's code-bytes archive, as `CodeUploadMixin` queues it: staged, non-blocking, on
    its own lane."""
    archive = tmp_path / "code.tar.gz"
    archive.write_bytes(b"\x1f\x8b" + b"x" * 64)
    queued = pod.journal.append_upload(
        anchor="run", anchor_id=run_id, name="code-bytes.gz", src_path=str(archive),
        content_type="application/gzip", kind="code_bytes", run_ref=run_id,
        require_staged=True, blocking=False, lane=f"code-bytes:{run_id}",
    )
    assert queued.get("staged"), queued


def _hung_store(app, monkeypatch, *, metrics_busy=lambda: False) -> None:
    import httpx

    real = app.handler

    def handler(request):
        if request.method == "PUT":
            raise httpx.ReadTimeout("the store took the bytes and never answered", request=request)
        if request.method == "POST" and request.url.path.endswith("/metrics") and metrics_busy():
            return httpx.Response(503, json={"detail": "busy"})
        return real(request)

    monkeypatch.setattr(app, "handler", handler)


def test_a_store_that_never_answers_the_archive_never_holds_the_barrier(app, tmp_path, monkeypatch, sleeps):
    """The open's code-bytes archive rides its own lane, so its stall never read as an outage,
    and the barrier waited the whole budget for it (native adversarial, pass 1). It is not waited
    for at all: non-blocking on a lane of its own, it is no write the new epoch refuses."""
    import time as _time
    import warnings

    monkeypatch.setenv("PROBE_TAKEOVER_DRAIN_SEC", "5")
    _hung_store(app, monkeypatch)
    old, pod2 = _requeue_scenario(app, tmp_path)
    _queue_open_archive(pod2, old.id, tmp_path)
    started = _time.monotonic()
    with warnings.catch_warnings(record=True) as said:
        warnings.simplefilter("always")
        _launch(pod2)
    assert _time.monotonic() - started < 2.5
    assert not [w for w in said if "not delivered" in str(w.message) or "could not be reached" in str(w.message)]
    assert {p["step_index"] for p in app.metric_points_posted[old.id]} == set(range(50))
    assert [op.get("lane") for _, op in pod2.journal.pending() if op.get("kind") == "upload"] == [f"code-bytes:{old.id}"]


def test_a_store_timeout_on_the_archive_never_strands_the_runs_data(app, tmp_path, monkeypatch, sleeps):
    """Pass 1 read any unanswered stall of the barrier's pass as the server being down: one storage
    timeout on the open's archive ended the barrier while the run's own lane only backed off a
    503, the reopen moved the epoch, and the dead attempt's metrics were refused as stale
    (native adversarial, pass 2). Only the run's own lane says the API is down."""
    from probe.sdk.delivery.outbox.drain import drain as drain_module
    from probe.sdk.delivery.outbox.drain.report import LaneStall

    monkeypatch.setenv("PROBE_TAKEOVER_DRAIN_SEC", "30")
    real_drain = drain_module.drain
    passes = {"n": 0}

    def counting_drain(*args, **kwargs):
        barrier = kwargs.get("wait_for_lock") is False  # the barrier's passes
        if barrier:
            passes["n"] += 1
        report = real_drain(*args, **kwargs)
        if barrier and passes["n"] == 1:
            # What a storage timeout on the archive's lane reports (no answer at all). The barrier
            # no longer sends the archive (`only_ops`), so it is put there by hand: the guard that
            # reads only the run's own lane stays the thing under test.
            report.stalled_runs[f"code-bytes:{old.id}"] = LaneStall("ReadTimeout: no answer")
        return report

    monkeypatch.setattr(drain_module, "drain", counting_drain)
    _hung_store(app, monkeypatch, metrics_busy=lambda: passes["n"] <= 1)
    old, pod2 = _requeue_scenario(app, tmp_path)
    _queue_open_archive(pod2, old.id, tmp_path)
    _launch(pod2)
    assert passes["n"] >= 2, "the barrier stopped after its first pass"
    assert {p["step_index"] for p in app.metric_points_posted[old.id]} == set(range(50))
    assert app.fenced_writes == []


def test_a_hung_store_on_the_archive_queued_at_open_never_spends_the_barrier(app, tmp_path, monkeypatch, sleeps):
    """The open queues its archive before any metric, and the barrier's pass, which no longer
    waited for the archive, still sent it first: a store that takes the bytes and never answers
    spent the barrier's budget there, and the dead attempt's metrics were left to the new epoch
    (red team, native and Codex adversarial, pass 3). The barrier sends only what it waits for."""
    import threading
    import time as _time

    import httpx

    monkeypatch.setenv("PROBE_TAKEOVER_DRAIN_SEC", "4")
    real = app.handler

    def handler(request):
        if request.method == "PUT":
            threading.Event().wait(1.5)
            raise httpx.ReadTimeout("the store took the bytes and never answered", request=request)
        return real(request)

    monkeypatch.setattr(app, "handler", handler)
    outbox = tmp_path / "pv-outbox"
    pod1 = make_client(app, tmp_spool=outbox, async_writes=True)
    pod1.create_project("takeover-lab", "Takeover Lab", kind="general")
    old = _launch(pod1)
    _queue_open_archive(pod1, old.id, tmp_path)  # at open: ahead of every metric
    for step in range(50):
        old.log({"loss": 1.0 / (step + 1)}, step=step)
    _quiet(app, old.id, 1000.0)
    pod2 = make_client(app, tmp_spool=outbox, async_writes=True)
    started = _time.monotonic()
    _launch(pod2)
    assert _time.monotonic() - started < 3.0, "the barrier waited on the archive's store"
    assert {p["step_index"] for p in app.metric_points_posted[old.id]} == set(range(50))
    assert app.fenced_writes == []


@pytest.mark.parametrize("worker_alive", [True, False], ids=["delivered-elsewhere", "stranded-elsewhere"])
def test_the_open_archive_under_another_credential_is_neither_waited_for_nor_stranded(
    app, tmp_path, monkeypatch, sleeps, worker_alive
):
    """`_is_waited_for` at the barrier's two other sites (testing specialist, pass 3): the open's
    archive in another credential's queue is not waited for while that queue's worker runs, and
    not reported stranded when none does."""
    import time as _time
    import types
    import warnings

    monkeypatch.setenv("PROBE_TAKEOVER_DRAIN_SEC", "3")
    old, pod2 = _requeue_scenario(app, tmp_path)
    archive = {
        "op_id": "c0de", "kind": "upload", "run_ref": old.id, "blocking": False,
        "lane": f"code-bytes:{old.id}", "upload": {"name": "code-bytes.gz"},
    }
    elsewhere = types.SimpleNamespace(
        receipt_enabled=False, dir=tmp_path / "elsewhere", worker_alive=lambda: worker_alive,
        pending=lambda: [(tmp_path / "elsewhere" / "op.json", archive)],
    )
    monkeypatch.setattr(pod2.journal, "other_queues", lambda: [elsewhere])
    started = _time.monotonic()
    with warnings.catch_warnings(record=True) as said:
        warnings.simplefilter("always")
        _launch(pod2)
    assert _time.monotonic() - started < 2.0
    assert not [w for w in said if "not delivered" in str(w.message)], [str(w.message) for w in said]


def _queue_waiting_upload(pod, run_id: str, tmp_path) -> None:
    """A file the dead attempt logged right before it died, still in the waiting room: copied,
    its credential scan not run yet (`defer_scan`, as `Run.log_artifact` queues one)."""
    src = tmp_path / "notes.txt"
    src.write_text("checkpoint notes\n")
    queued = pod.journal.append_upload(
        anchor="run", anchor_id=run_id, name="notes.txt", src_path=str(src),
        content_type="text/plain", run_ref=run_id, require_staged=True, defer_scan=True,
    )
    assert queued.get("waiting"), queued


def test_a_dead_attempts_waiting_upload_is_its_backlog_not_a_live_writer(app, tmp_path, monkeypatch, sleeps):
    """The barrier sends only the op ids it listed (`only_ops`), and its own pass promoted the
    dead attempt's waiting upload into an op it had not listed: unsent, it read as a live
    writer's append, and the barrier gave the dead attempt's close back instead of retiring it
    (review of #3804's last five commits). Promoted before the list is taken, it is backlog."""
    old, pod2 = _requeue_scenario(app, tmp_path, close="failed")
    _queue_waiting_upload(pod2, old.id, tmp_path)

    _launch(pod2)

    assert _queued_status(pod2.journal) == [], "the dead attempt's close went back in the queue"
    (dead,) = pod2.journal.failed()
    assert dead[1]["body"]["status"] == "failed" and "takeover" in dead[1]["last_error"]
    assert [op for _, op in pod2.journal.pending() if op.get("kind") == "upload"] == []
    assert len({p["step_index"] for p in app.metric_points_posted[old.id]}) == 50


def test_a_first_pass_503_beside_a_waiting_upload_still_lands_before_the_reopen(app, tmp_path, monkeypatch, sleeps):
    """The same misreading after a first pass that could not land everything (one 503, its
    lane backed off with the promoted upload behind it): the barrier stopped there, the reopen
    moved the epoch, and the dead attempt's metrics were fenced, with no warning."""
    import httpx

    real = app.handler
    seen = {"metrics": 0}

    def handler(request):
        if request.method == "POST" and request.url.path.endswith("/metrics"):
            seen["metrics"] += 1
            if seen["metrics"] == 1:
                return httpx.Response(503, json={"detail": "busy"})
        return real(request)

    monkeypatch.setattr(app, "handler", handler)
    old, pod2 = _requeue_scenario(app, tmp_path)
    _queue_waiting_upload(pod2, old.id, tmp_path)

    _launch(pod2)

    assert {p["step_index"] for p in app.metric_points_posted.get(old.id, [])} == set(range(50))
    assert app.fenced_writes == []


def test_a_dead_attempts_completed_close_lands_behind_its_waiting_upload(app, tmp_path, monkeypatch, sleeps):
    """A fail-open close queued while the run's last upload still waited for its scan: the
    barrier sent the `completed` close and left the upload it had promoted, unlisted, behind it
    (state-machines specialist). The upload goes first, in queue order."""
    outbox = tmp_path / "pv-outbox"
    pod1 = make_client(app, tmp_spool=outbox, async_writes=True)
    pod1.create_project("takeover-lab", "Takeover Lab", kind="general")
    old = _launch(pod1)
    old.log({"loss": 1.0}, step=0)
    _queue_waiting_upload(pod1, old.id, tmp_path)
    waiting = pod1.journal.waiting(run_ref=old.id)
    monkeypatch.setattr(pod1.journal, "promote_for_close", lambda run_ref, timeout: waiting)
    old.set_status("completed")
    _quiet(app, old.id, 1000.0)
    pod2 = make_client(app, tmp_spool=outbox, async_writes=True)
    start = len(app.requests)

    with pytest.raises(errors.ConflictError, match="already completed"):
        _launch(pod2)

    sent = app.requests[start:]
    close = next(i for i, r in enumerate(sent) if r.method == "PATCH" and b'"status"' in (r.content or b""))
    assert any("upload" in r.url.path or r.method == "PUT" for r in sent[:close]), [
        (r.method, r.url.path) for r in sent
    ]


def test_a_waiting_upload_a_worker_promotes_mid_barrier_is_still_backlog(app, tmp_path, monkeypatch, sleeps):
    """The detached worker a relaunch starts can hold the dead attempt's waiting upload while the
    barrier lists its backlog, then promote it between two passes (red team). The op it writes
    keeps the name the waiting room reserved for it: the same backlog, not a live writer's."""
    from probe.sdk.delivery.journal.journal import Journal
    from probe.sdk.delivery.outbox.drain import drain as drain_module

    old, pod2 = _requeue_scenario(app, tmp_path, close="failed")
    _queue_waiting_upload(pod2, old.id, tmp_path)
    real_drain, real_promote = drain_module.drain, Journal.promote_waiting
    passes = {"n": 0}

    def drain_beside_a_worker(*args, **kwargs):
        if kwargs.get("wait_for_lock") is not False or passes["n"]:
            return real_drain(*args, **kwargs)
        passes["n"] += 1
        monkeypatch.setattr(Journal, "promote_waiting", lambda self, **kw: 0)  # the worker holds it
        try:
            report = real_drain(*args, **kwargs)
        finally:
            monkeypatch.setattr(Journal, "promote_waiting", real_promote)
        real_promote(pod2.journal, run_ref=old.id)  # ... and promotes it once that pass is over
        return report

    monkeypatch.setattr(drain_module, "drain", drain_beside_a_worker)

    _launch(pod2)

    assert _queued_status(pod2.journal) == [], "the dead attempt's close went back in the queue"
    assert [op for _, op in pod2.journal.pending() if op.get("kind") == "upload"] == []
    assert len({p["step_index"] for p in app.metric_points_posted[old.id]}) == 50


def test_a_takeover_says_how_the_new_attempt_will_be_alive(lab, app, sleeps):
    """Review of #2049: the takeover resets the run's liveness mode; the new
    attempt's own signals let the server re-derive it (2.2's writer-gone
    needs `in-process`)."""
    old = _launch(lab)
    _quiet(app, old.id, 200.0)

    _launch(lab)

    (reopen,) = _reopens(app)
    body = json.loads(reopen.content)
    # `_launch` opens with heartbeat=False: the signal is the handle's own.
    assert (body["heartbeat"], body["launcher"]) == (False, False)
