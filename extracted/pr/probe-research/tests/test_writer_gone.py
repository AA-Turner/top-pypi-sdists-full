"""SDK reliability 2.2: a sole writer's death reaches the server in seconds.

The output helper outlives the training process; the moment it is reparented
it starts `python -m probe.sdk.outputs --writer-gone ENTRY` (the logcapture
tests cover that trigger). This file covers what that reporter sends, what the
capture record carries so it can, the node agent's report, and the repair when
a report was wrong: a live owner whose beat lands on a `crashed` row reopens
it under its own epoch (1.1).
"""

from __future__ import annotations

import json
import threading
import time
import weakref

import pytest

from probe.sdk import outputs
from probe.sdk.run import _beat_forever
from tests.conftest import make_client, open_run


@pytest.fixture
def reporter(app, monkeypatch, tmp_path):
    """Point the reporter's client at the fake. `_recovery_client` resolves the
    run's recorded context from config; here it hands back a fake-backed client
    of the same shape (client, journal)."""
    client = make_client(app, tmp_spool=tmp_path / "outbox")
    monkeypatch.setattr(outputs, "_recovery_client", lambda record: (client, client.journal))
    return client


def _record(tmp_path, run, **writer_overrides) -> str:
    capture = outputs.OutputCapture(
        run._client, run.id, str(tmp_path), tee=False, launcher=False,
        writer={**run._writer_record(), **writer_overrides},
    )
    entry = tmp_path / "rec.json"
    entry.write_text(json.dumps(capture._record(shared_with=[])))
    return str(entry)


def _owner(client):
    # heartbeat=True at create is what makes the server call it in-process.
    run = open_run(client, experiment="e", name="r", heartbeat=True)
    run.stop_heartbeat()
    return run


def test_the_capture_record_names_its_writer(client, app, tmp_path):
    run = _owner(client)
    record = json.loads(open(_record(tmp_path, run)).read())
    assert record["writer"] == {
        "session_id": run.session_id,
        "write_epoch": 1,
        "role": "owner",
        "sole_writer": True,
    }

    rank = client.attach_run(run.id, heartbeat=False, attached=True)
    assert rank._writer_record()["sole_writer"] is False
    assert rank._writer_record()["role"] == "attached"


def test_a_sole_owners_death_crashes_its_run(client, app, tmp_path, reporter):
    run = _owner(client)
    entry = _record(tmp_path, run)

    outcome = outputs.writer_gone(entry)

    assert outcome["sent"] is True and outcome["applied"] is True
    assert app.runs[run.id]["status"] == "crashed"
    (report,) = app.writer_gone_reports
    assert report == {
        "session_id": run.session_id,
        "write_epoch": 1,
        "observed_by": "output_helper",
        "host": report["host"],
        "pid": report["pid"],
        "sole_writer": True,
    }
    assert json.loads((tmp_path / "rec.json.gone").read_text())["sent"] is True


def test_one_report_per_record(client, app, tmp_path, reporter):
    run = _owner(client)
    entry = _record(tmp_path, run)
    outputs.writer_gone(entry)

    assert outputs.writer_gone(entry) is None
    assert len(app.writer_gone_reports) == 1


def test_an_attached_rank_reports_but_the_server_keeps_the_run(client, app, tmp_path, reporter):
    run = _owner(client)
    entry = _record(tmp_path, run, sole_writer=False, role="attached")

    outcome = outputs.writer_gone(entry)

    assert outcome["sent"] is True and outcome["applied"] is False
    assert app.runs[run.id]["status"] == "running"


def test_an_older_server_is_never_sent_the_report(client, app, tmp_path, reporter):
    app.supports_writer_gone = False
    run = _owner(client)
    entry = _record(tmp_path, run)

    outcome = outputs.writer_gone(entry)

    assert outcome == {"sent": False, "reason": "unsupported"}
    assert app.writer_gone_reports == []
    assert not [r for r in app.requests if r.url.path.endswith("/writer-gone")]


def test_a_record_without_a_writer_sends_nothing(client, app, tmp_path, reporter):
    entry = tmp_path / "old.json"
    entry.write_text(json.dumps({"run_id": "r", "pid": 1}))  # an older SDK's record
    assert outputs.writer_gone(str(entry))["reason"] == "no_writer"
    assert app.writer_gone_reports == []


def _beat_for(client, run, *, until, seconds: float = 5.0) -> None:
    stop = threading.Event()
    beat = threading.Thread(
        target=_beat_forever,
        args=(client, run.id, stop, 0.005, "owner", run.write_epoch, False, weakref.ref(run)),
        daemon=True,
    )
    beat.start()
    try:
        deadline = time.monotonic() + seconds
        while time.monotonic() < deadline and not until():
            time.sleep(0.01)
    finally:
        stop.set()
        beat.join(timeout=5)


def _status_event(app, run_id: str, **payload) -> None:
    app.run_events.setdefault(run_id, []).insert(
        0, {"event_type": "run.status_changed", "payload": {"status": "crashed", **payload}}
    )


def test_a_live_owner_repairs_a_wrong_report_on_its_next_beat(client, app, tmp_path, reporter):
    """A report can be wrong (a helper misreading its parent). The owner is
    alive, so its next beat lands on the `crashed` row, and that alone now
    triggers the keep-epoch reopen: no failed beat needed."""
    run = _owner(client)
    assert outputs.writer_gone(_record(tmp_path, run))["applied"] is True
    assert app.runs[run.id]["status"] == "crashed"

    _beat_for(client, run, until=lambda: app.runs[run.id]["status"] == "running")

    assert app.runs[run.id]["status"] == "running"
    assert app.runs[run.id]["write_epoch"] == 1 and run.write_epoch == 1


def test_a_live_owner_repairs_a_reaper_verdict_it_never_saw_coming(client, app):
    """No failed beat, yet the reaper crashed the run (the process was
    suspended past the stale window): same repair."""
    run = _owner(client)
    app.runs[run.id]["status"] = "crashed"
    _status_event(app, run.id, reason="stale")

    _beat_for(client, run, until=lambda: app.runs[run.id]["status"] == "running")

    assert app.runs[run.id]["status"] == "running"


def test_a_person_s_crashed_is_never_undone_by_a_live_beat(client, app):
    """`probe run end --status crashed` on a hung job whose beat thread still
    runs: the person meant it. A status PATCH's event carries no reason, so
    the beat leaves the row alone -- and reads the events once, not per beat."""
    run = _owner(client)
    app.runs[run.id]["status"] = "crashed"
    _status_event(app, run.id)  # what a status PATCH records: no reason
    reads = lambda: len(  # noqa: E731
        [r for r in app.requests if r.url.path == f"/v1/runs/{run.id}/events"]
    )
    beats = lambda: len(  # noqa: E731
        [r for r in app.requests if r.url.path == f"/v1/runs/{run.id}/heartbeat"]
    )

    _beat_for(client, run, until=lambda: beats() >= 20)

    assert beats() >= 20
    assert app.runs[run.id]["status"] == "crashed"
    assert reads() == 1
    assert not [r for r in app.requests if r.url.path.endswith("/reopen")]


def test_an_older_server_costs_a_crashed_beat_no_extra_reads(client, app):
    """Without keep_epoch the recovery is skipped (1.1), and the feature check
    comes first and is cached: beating on a crashed row stays one request."""
    app.supports_keep_epoch = False
    run = _owner(client)
    app.runs[run.id]["status"] = "crashed"
    stop = threading.Event()
    stop.set()  # one pass
    before = len([r for r in app.requests if r.method == "GET" and r.url.path == f"/v1/runs/{run.id}"])
    _beat_forever(client, run.id, stop, 0.01, "owner", run.write_epoch, False, weakref.ref(run))
    after = len([r for r in app.requests if r.method == "GET" and r.url.path == f"/v1/runs/{run.id}"])
    assert after == before
    assert app.runs[run.id]["status"] == "crashed"


def test_the_node_agent_reports_a_vanished_writer(app, tmp_path, monkeypatch):
    from probe.box import registry, watch

    client = make_client(app)
    run = _owner(client)
    monkeypatch.setattr(watch, "_client_for", lambda entry: client)
    path = registry.register(
        run.id, pid=999_999, directory=tmp_path, writer=run._writer_record()
    )
    entry = json.loads(path.read_text())

    assert watch.report_vanished(entry) is True

    (report,) = app.writer_gone_reports
    assert report["observed_by"] == "node_agent" and report["sole_writer"] is True
    assert app.runs[run.id]["status"] == "crashed"


def test_a_crashed_row_it_cannot_recover_is_not_hammered(client, app, monkeypatch):
    """A beat landing on a crashed row tries the repair once; when that is
    refused (a sibling rank or a newer attempt), later beats on the SAME row
    do not keep calling the reopen route."""
    from probe import errors

    run = _owner(client)
    app.runs[run.id]["status"] = "crashed"
    _status_event(app, run.id, reason="writer_gone")
    calls = {"n": 0}

    def refused(*a, **kw):
        calls["n"] += 1
        raise errors.ConflictError("keep_epoch refused", detail={"message": "x"})

    monkeypatch.setattr(client, "reopen_run", refused)
    beats = {"n": 0}
    real = client.heartbeat_run

    def counted(*a, **kw):
        beats["n"] += 1
        return real(*a, **kw)

    monkeypatch.setattr(client, "heartbeat_run", counted)
    stop = threading.Event()
    beat = threading.Thread(
        target=_beat_forever,
        args=(client, run.id, stop, 0.005, "owner", run.write_epoch, False, weakref.ref(run)),
        daemon=True,
    )
    beat.start()
    try:
        deadline = time.monotonic() + 5
        while time.monotonic() < deadline and beats["n"] < 20:
            time.sleep(0.01)
    finally:
        stop.set()
        beat.join(timeout=5)

    assert beats["n"] >= 20
    assert calls["n"] == 1


def test_a_report_during_a_partition_is_queued_not_dropped(client, app, tmp_path, reporter):
    """Review of #2049: the feature check itself failed in a partition, and
    the report was dropped there. It is queued (non-blocking) and lands when
    the drain can reach the server."""
    run = _owner(client)
    entry = _record(tmp_path, run)
    app.fail_paths = {"/v1/server/features"}
    reporter._server_features_cache = None  # a fresh reporter process: nothing cached

    outcome = outputs.writer_gone(entry)

    assert (outcome["reason"], outcome.get("queued")) == ("unreachable", True)
    (queued,) = [
        op for _, op in reporter.journal.pending() if op["path"].endswith("/writer-gone")
    ]
    assert queued["blocking"] is False
    app.fail_paths = set()
    reporter.flush()
    assert app.runs[run.id]["status"] == "crashed"


def test_a_daemonizing_script_is_not_reported_dead(client, app, tmp_path, reporter):
    """Review of #2049: `fork()` then `os._exit()` in the parent is how a
    script daemonizes; its child carries the run on. A write from the child
    leaves a marker, and while that child lives the reporter stands down."""
    import subprocess
    import sys

    run = _owner(client)
    entry = _record(tmp_path, run)
    child = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(30)"])
    try:
        outputs.mark_forked_writer(entry, child.pid)

        outcome = outputs.writer_gone(entry)

        assert (outcome["reason"], outcome["pid"]) == ("writer_continues", child.pid)
        assert app.writer_gone_reports == []
        assert app.runs[run.id]["status"] == "running"
    finally:
        child.kill()
        child.wait()


def test_a_reused_pid_is_not_the_forked_writer(client, app, tmp_path, reporter):
    """Follow-up to #2049: the marker named a pid, and ANY living process
    under it stood the report down -- a pid the kernel had reused for
    something else turned fast crash detection off for the run. The marker
    now holds the child's start time; another start time is another process."""
    import subprocess
    import sys

    run = _owner(client)
    entry = _record(tmp_path, run)
    other = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(30)"])
    try:
        outputs.mark_forked_writer(entry, other.pid)
        marker = next(tmp_path.glob("rec.json.writer-*"))
        marker.write_text("1")  # the child that wrote it started at another time

        outcome = outputs.writer_gone(entry)

        assert outcome["applied"] is True, "another process under that pid is not the writer"
        assert not marker.exists()
    finally:
        other.kill()
        other.wait()


def test_a_marker_whose_child_exited_does_not_stand_the_report_down(
    client, app, tmp_path, reporter
):
    run = _owner(client)
    entry = _record(tmp_path, run)
    outputs.mark_forked_writer(entry, 999_999)

    outcome = outputs.writer_gone(entry)

    assert outcome["applied"] is True
    assert not list(tmp_path.glob("rec.json.writer-*")), "the stale marker is cleared"


def test_a_write_from_a_forked_child_leaves_the_marker(client, app, tmp_path, monkeypatch):
    from probe.sdk import run as run_mod

    run = _owner(client)

    class _Capture:
        _entry = tmp_path / "rec.json"

    run._capture = _Capture()
    run.log({"loss": 1.0}, step=1)
    assert not list(tmp_path.glob("rec.json.writer-*")), "the opener leaves none"
    monkeypatch.setattr(run_mod.os, "getpid", lambda: 424242)
    run.log({"loss": 0.5}, step=2)
    run.log({"loss": 0.4}, step=3)
    assert [p.name for p in tmp_path.glob("rec.json.writer-*")] == ["rec.json.writer-424242"]
