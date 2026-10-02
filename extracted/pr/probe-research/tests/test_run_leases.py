"""SDK reliability 2.8: a process writes its run under its own lease.

Against a server that declares `run_writer_leases` the SDK opens a `leases`
run with its lease in the create, beats that lease (jittered, carrying the
progress counter) instead of the run-level heartbeat, and ends it with a
RELEASE carrying its verdict -- the server closes the run once its leases say
the work ended. Every request is marked `X-Probe-Leases: 1`, so the server
never mistakes this client for one that does not speak leases. Against any
other server nothing changes (the rest of the suite runs there).
"""

from __future__ import annotations

import threading
import time
import weakref

import pytest

from probe.sdk import run as run_mod
from probe.sdk.run import _beat_forever, _Progress
from probe.sdk.transport import LEASES_HEADER
from tests.conftest import make_client, open_run


@pytest.fixture
def app(app):
    app.supports_leases = True
    return app


def _lease_requests(app, run_id: str, verb: str) -> list:
    return [
        r
        for r in app.requests
        if r.url.path.startswith(f"/v1/runs/{run_id}/writers/") and r.url.path.endswith(f"/{verb}")
    ]


def _bodies(requests) -> list[dict]:
    import json

    return [json.loads(r.content) if r.content else {} for r in requests]


def _open(client, **kw):
    run = open_run(client, experiment="e", name="r", **kw)
    return run


# -- the mark and the create ------------------------------------------------------


def test_every_request_says_it_speaks_leases(client, app):
    run = _open(client)
    run.log({"loss": 1.0})
    assert app.requests, "the fake saw nothing"
    assert all(r.headers.get(LEASES_HEADER) == "1" for r in app.requests)


def test_a_run_opens_with_its_owners_lease(client, app):
    run = _open(client)
    create = [r for r in app.requests if r.method == "POST" and r.url.path.endswith("/runs")][-1]
    (body,) = _bodies([create])

    assert body["liveness_protocol"] == "leases"
    lease = body["writer"]
    assert lease["session_id"] == run.session_id and lease["role"] == "owner"
    assert lease["pid"] > 0 and lease["host"]
    assert app.runs[run.id]["liveness_protocol"] == "leases"
    assert list(app.leases[run.id]) == [run.session_id]
    run.stop_heartbeat()


def test_a_launcher_opens_as_launcher(client, app):
    run = _open(client, launcher=True)
    assert app.leases[run.id][run.session_id]["role"] == "launcher"
    run.stop_heartbeat()


def test_an_older_server_gets_the_run_level_heartbeat(client, app):
    app.supports_leases = False
    run = _open(client)
    create = [r for r in app.requests if r.method == "POST" and r.url.path.endswith("/runs")][-1]
    (body,) = _bodies([create])
    assert "liveness_protocol" not in body and "writer" not in body
    assert run._lease is None
    run.stop_heartbeat()


def test_a_detached_run_takes_no_lease(client, app):
    run = _open(client, heartbeat=False)
    assert run._lease is None and app.leases.get(run.id) is None


# -- the beat ----------------------------------------------------------------------


def _beat_a_few(client, run, *, n: int = 3):
    stop = threading.Event()
    thread = threading.Thread(
        target=_beat_forever,
        args=(
            client,
            run.id,
            stop,
            0.01,
            "owner",
            run.write_epoch,
            False,
            weakref.ref(run),
            run._lease,
        ),
        daemon=True,
    )
    thread.start()
    deadline = time.monotonic() + 5
    while time.monotonic() < deadline and len(_lease_requests(client._fake, run.id, "beat")) < n:
        time.sleep(0.01)
    stop.set()
    thread.join(timeout=5)


def test_the_beat_is_the_leases_and_carries_progress(client, app):
    client._fake = app
    run = _open(client)
    run.stop_heartbeat()
    for step in range(5):
        run.log({"loss": 1.0 / (step + 1)}, step=step)

    _beat_a_few(client, run)

    beats = _bodies(_lease_requests(app, run.id, "beat"))
    assert beats, "no lease beat"
    last = beats[-1]
    assert last["write_epoch"] == 1 and last["role"] == "owner"
    assert last["progress"] == 5 and last["progress_idle_seconds"] >= 0
    assert "session_id" not in last, "the session is the path"
    assert not [r for r in app.requests if r.url.path.endswith("/heartbeat")]
    assert app.leases[run.id][run.session_id]["progress"] == 5


def test_every_wait_is_jittered_the_first_included(monkeypatch, client, app):
    """608 ranks started together must not beat together."""
    run = _open(client)
    run.stop_heartbeat()
    draws: list[tuple[float, float]] = []

    def uniform(a, b):
        draws.append((a, b))
        return b if a == 0.0 else 1.0

    monkeypatch.setattr(run_mod.random, "uniform", uniform)
    stop = threading.Event()
    waits: list[float] = []
    real_wait = stop.wait

    def recording_wait(timeout=None):
        waits.append(timeout)
        if len(waits) >= 3:
            stop.set()
        return real_wait(0)

    monkeypatch.setattr(stop, "wait", recording_wait)
    _beat_forever(client, run.id, stop, 60.0, "owner", 1, False, weakref.ref(run), run._lease)

    assert draws[0] == (0.0, 60.0), "the first beat waits a uniform [0, interval)"
    assert (0.8, 1.2) in draws, "later waits are +-20%"
    assert waits[0] == 60.0 and waits[1] == 60.0


def test_a_superseded_writer_stops_beating_its_lease(client, app):
    run = _open(client)
    run.stop_heartbeat()
    app.runs[run.id]["write_epoch"] = 2
    stop = threading.Event()
    with pytest.warns(UserWarning, match="taken over by a newer attempt"):
        _beat_forever(client, run.id, stop, 0.01, "owner", 1, False, weakref.ref(run), run._lease)


def test_a_beat_learns_the_run_fell_back_to_legacy(client, app):
    run = _open(client)
    run.stop_heartbeat()
    app.runs[run.id]["liveness_protocol"] = "legacy"
    client._fake = app
    _beat_a_few(client, run, n=1)
    assert run._lease_protocol == "legacy"


# -- the close -----------------------------------------------------------------------


def test_finish_releases_the_lease_and_the_server_closes_the_run(client, app):
    run = _open(client)
    run.log({"loss": 0.5})

    row = run.finish(summary_metrics={"loss": 0.5})

    (release,) = _bodies(_lease_requests(app, run.id, "release"))
    assert (release["write_epoch"], release["exit_status"]) == (1, "completed")
    assert release["writer"]["role"] == "owner" and "session_id" not in release["writer"], (
        "a release names its writer; the session is the path"
    )
    patches = _bodies(
        [r for r in app.requests if r.method == "PATCH" and r.url.path == f"/v1/runs/{run.id}"]
    )
    assert patches and all("status" not in p for p in patches), "status is the server's now"
    assert any("ended_at" in p for p in patches)
    assert app.runs[run.id]["status"] == "completed"
    assert row["status"] == "completed"


def test_a_failure_is_released_as_failed(client, app):
    run = _open(client)
    run.finish("failed")
    (release,) = _bodies(_lease_requests(app, run.id, "release"))
    assert release["exit_status"] == "failed"
    assert app.runs[run.id]["status"] == "failed"


def test_a_run_flipped_just_before_the_close_is_closed_by_the_owners_release(client, app):
    """Flipped between the last beat and the close: on a run that is not
    `leases` the server closes it on an owner's release, with its verdict."""
    run = _open(client)
    run.stop_heartbeat()
    app.runs[run.id]["liveness_protocol"] = "legacy"

    run.finish("failed")

    assert _lease_requests(app, run.id, "release")
    assert app.runs[run.id]["status"] == "failed"


def test_a_resumed_pre_lease_run_closes_the_old_way(client, app):
    """Review of #2060, HIGH-1 (probes A-A3): a run opened before 0271 (or by
    an older client) has NO protocol. The new SDK resumes it under a lease;
    its finish must still close it -- the pre-2.8 way, with a status PATCH --
    or it stays `running` until the reaper calls it `crashed` and mails."""
    app.supports_leases = False
    first = _open(client, external_id="job-null")
    first.finish("failed")
    assert app.runs[first.id].get("liveness_protocol") is None
    app.supports_leases = True
    client = make_client(app)  # a new process: a fresh features preflight

    second = client.run(
        project="project-e", experiment="e", name="r", external_id="job-null", on_conflict="resume"
    )
    second.stop_heartbeat()
    assert second._lease is not None and second._lease_protocol == "legacy"

    second.finish()

    assert "completed" in _status_patches(app, second.id)
    assert app.runs[second.id]["status"] == "completed"
    released = app.leases[second.id][second.session_id]
    assert released["exit_status"] == "completed", "the lease reads released, not expired"


def test_a_deferred_close_of_a_legacy_run_keeps_its_status(app, tmp_path):
    """HIGH-1: the deferred finish stripped `status` from the queued close; on
    a run that is not `leases` that verdict is what closes it."""
    client = make_client(app, tmp_spool=tmp_path / "outbox", async_writes=True)
    run = _open(client)
    run.stop_heartbeat()
    run._lease_protocol = "legacy"
    app.fail_paths = {f"/v1/runs/{run.id}/metrics"}
    run.log({"loss": 1.0}, step=1)

    report = run.finish("failed", flush_timeout=0.2)

    assert report["finish_queued"] is True
    queued = [op for _, op in client.journal.pending() if op.get("run_ref") == run.id]
    kinds = [(op["method"], op["path"].rsplit("/", 1)[-1]) for op in queued]
    assert kinds[-2:] == [("PATCH", run.id), ("POST", "release")], kinds
    assert queued[-2]["body"]["status"] == "failed"


def _attach_rank(client, run_id, monkeypatch, rank: int = 1):
    """A non-zero rank of a distributed job joining through PROBE_RUN_ID
    (what fluent.init does for it: the env names the rank, and it sends no
    terminal status of its own)."""
    monkeypatch.setenv("RANK", str(rank))
    monkeypatch.setenv("WORLD_SIZE", "4")
    handle = client.attach_run(run_id, heartbeat=True, attached=True)
    handle._sends_terminal_status = False
    monkeypatch.delenv("RANK")
    monkeypatch.delenv("WORLD_SIZE")
    return handle


def test_an_attached_rank_registers_its_lease_and_only_releases(client, app, monkeypatch):
    owner = _open(client)
    rank = _attach_rank(client, owner.id, monkeypatch)
    (register,) = _bodies(_lease_requests(app, owner.id, "beat"))
    assert register["role"] == "rank"
    assert app.leases[owner.id][rank.session_id]["role"] == "rank"

    before = len([r for r in app.requests if r.method == "PATCH"])
    rank.finish()
    after = len([r for r in app.requests if r.method == "PATCH"])

    assert after == before, "a non-zero rank sends no run fields"
    assert _bodies(_lease_requests(app, owner.id, "release"))[-1]["exit_status"] == "completed"
    assert app.runs[owner.id]["status"] == "running", "the owner's lease is still live"
    owner.finish()
    assert app.runs[owner.id]["status"] == "completed"


def test_a_ranks_failure_is_the_runs_failure(client, app, monkeypatch):
    """The worst verdict wins: the owner finishing `completed` does not hide
    a rank that failed."""
    owner = _open(client)
    rank = _attach_rank(client, owner.id, monkeypatch)
    rank.finish("failed")
    owner.finish()
    assert app.runs[owner.id]["status"] == "failed"


def test_a_deferred_finish_drains_its_lease_and_queues_the_release_behind_the_data(app, tmp_path):
    client = make_client(app, tmp_spool=tmp_path / "outbox", async_writes=True)
    run = _open(client)
    app.fail_paths = {f"/v1/runs/{run.id}/metrics"}
    run.log({"loss": 1.0}, step=1)

    report = run.finish(flush_timeout=0.2)

    assert report["finish_queued"] is True
    (drain,) = [
        b for b in _bodies(_lease_requests(app, run.id, "beat")) if "draining_for_seconds" in b
    ]
    assert drain["draining_for_seconds"] == run_mod._LEASE_DRAIN_SECONDS
    queued = [op for _, op in client.journal.pending() if op.get("run_ref") == run.id]
    kinds = [(op["method"], op["path"].rsplit("/", 1)[-1]) for op in queued]
    assert kinds[-2:] == [("PATCH", run.id), ("POST", "release")], kinds
    assert "status" not in queued[-2]["body"]
    assert app.runs[run.id]["status"] == "running"

    app.fail_paths = set()
    client.flush()
    assert app.runs[run.id]["status"] == "completed"


def test_a_deferred_finish_beats_even_when_its_budget_is_spent(app, tmp_path, monkeypatch):
    """A close defers BECAUSE its budget ran out, and the draining beat went
    out under that same spent deadline (a nested `deadline_scope` keeps the
    earlier one): `DeadlineExceeded` before the send, swallowed, so the lease
    expired while the worker was still delivering and `writer_lost` fired
    falsely. The flaky test above lost it 2 of 20 times beside the full suite.
    Here the budget is spent on purpose before the beat. The beat gets a budget
    of its own: at least `_DRAINING_BEAT_MIN_SECONDS`, at most
    `_CLOSE_BEAT_SECONDS`."""
    from probe.sdk import transport
    from probe.sdk.client import Client

    client = make_client(app, tmp_spool=tmp_path / "outbox", async_writes=True)
    run = _open(client)
    app.fail_paths = {f"/v1/runs/{run.id}/metrics"}
    run.log({"loss": 1.0}, step=1)
    real_hand_off = Client.hand_off_delivery

    def slow_hand_off(self, *a, **k):
        time.sleep(0.4)  # past the close's 0.2 s: the beat comes after its deadline
        return real_hand_off(self, *a, **k)

    budgets = []
    real_beat = Client.beat_writer

    def beat(self, run_id, session_id, body):
        if "draining_for_seconds" in body:
            budgets.append(transport._request_deadline.get() - time.monotonic())
        return real_beat(self, run_id, session_id, body)

    monkeypatch.setattr(Client, "hand_off_delivery", slow_hand_off)
    monkeypatch.setattr(Client, "beat_writer", beat)
    report = run.finish(flush_timeout=0.2)

    assert report["finish_queued"] is True
    drains = [b for b in _bodies(_lease_requests(app, run.id, "beat")) if "draining_for_seconds" in b]
    assert len(drains) == 1, "the draining beat was not sent"
    (budget,) = budgets
    assert run_mod._DRAINING_BEAT_MIN_SECONDS - 0.1 <= budget <= run_mod._CLOSE_BEAT_SECONDS


# -- resume and takeover ----------------------------------------------------------------


def test_a_resume_reopens_with_the_relaunchs_lease(client, app):
    first = _open(client, external_id="job-1")
    first.finish("failed")

    second = client.run(
        project="project-e", experiment="e", name="r", external_id="job-1", on_conflict="resume"
    )

    reopen = [r for r in app.requests if r.url.path.endswith("/reopen")][-1]
    (body,) = _bodies([reopen])
    assert body["writer"]["session_id"] == body["session_id"] == second.session_id
    lease = app.leases[second.id][second.session_id]
    assert lease["write_epoch"] == 2 and second._lease is not None
    second.stop_heartbeat()


def test_the_barrier_holds_the_incumbents_queued_release_too(app, tmp_path):
    """2.3's barrier retires the dead attempt's verdict only once the
    takeover succeeds -- on a leases run that verdict is its queued release."""
    outbox = tmp_path / "pv"
    pod1 = make_client(app, tmp_spool=outbox, async_writes=True)
    old = _open(pod1, external_id="job-2")
    app.fail_paths = {f"/v1/runs/{old.id}/metrics"}
    old.log({"loss": 1.0}, step=1)
    # A verdict that did not finish the work (a `completed` release is
    # delivered instead, like a `completed` close: #2069).
    old.finish("failed", flush_timeout=0.1)  # queues PATCH + release behind the data
    app.fail_paths = set()
    pod2 = make_client(app, tmp_spool=outbox, async_writes=True)
    held = pod2._hold_status_writes(
        app.runs[old.id], {p.name: op for p, op in pod2.journal.pending()}
    )
    methods = sorted(op["method"] for p, op in pod2.journal.failed() if p.name in held)
    assert "POST" in methods, "the release was not held"


# -- the progress counter -------------------------------------------------------------


def test_progress_counts_and_measures_idle_on_the_monotonic_clock(monkeypatch):
    clock = {"t": 1000.0}
    monkeypatch.setattr(run_mod.time, "monotonic", lambda: clock["t"])
    progress = _Progress()
    assert progress.snapshot() == {}
    for gap in (1.0, 1.0, 1.0, 50.0, 1.0):
        progress.bump()
        clock["t"] += gap
    snap = progress.snapshot()
    assert snap["progress"] == 5 and snap["progress_idle_seconds"] == 1.0
    assert snap["progress_longest_gap_seconds"] == 50.0
    assert 1.0 <= snap["progress_gap_p99_seconds"] <= 50.0 * 1.25


def test_the_longest_gap_is_remembered_for_the_whole_run(monkeypatch):
    """A nightly 30-minute checkpoint, learned once, stays learned: a 24 h
    window forgot it just before the next one (review of #2062, MED-2)."""
    clock = {"t": 0.0}
    monkeypatch.setattr(run_mod.time, "monotonic", lambda: clock["t"])
    progress = _Progress()
    progress.bump()
    clock["t"] += 1800.0  # the first nightly checkpoint
    progress.bump()
    for _ in range(int(26 * 3600 / 10)):  # a day and more of steady 10 s steps
        clock["t"] += 10.0
        progress.bump()
    snap = progress.snapshot()
    assert snap["progress_longest_gap_seconds"] == 1800.0
    assert snap["progress_gap_p99_seconds"] <= 15.0, "the p99 still follows the last 24 h"


def test_run_progress_and_step_count_and_hardware_does_not(client, app):
    run = _open(client)
    run.stop_heartbeat()
    run.progress()
    run.step(1, name="s")
    run.log({"gpu/util": 0.9}, kind="hardware")
    assert run._progress.count == 2


def test_an_upload_and_a_span_are_progress(client, app, tmp_path):
    """A checkpoint save that uploads is work, not a stall (review of #2062)."""
    run = _open(client)
    run.stop_heartbeat()
    ckpt = tmp_path / "ckpt.pt"
    ckpt.write_bytes(b"weights")
    before = run._progress.count
    run.log_artifact("ckpt.pt", path=str(ckpt))
    run.span("rollout", name="episode-1")
    assert run._progress.count == before + 2


def test_list_writers_reads_the_leases(client, app):
    run = _open(client)
    run.stop_heartbeat()
    (lease,) = client.list_writers(run.id)
    assert lease["session_id"] == run.session_id and lease["role"] == "owner"


def test_a_lease_the_server_never_saw_is_registered_before_its_release(client, app):
    """The attach's own beat failed and the job ended before its first loop
    beat: releasing a lease the server never held would close nothing."""
    owner = _open(client)
    session = "11111111-1111-4111-8111-111111111111"
    app.fail_paths = {f"/v1/runs/{owner.id}/writers/{session}/beat"}
    rank = client.attach_run(owner.id, heartbeat=True, attached=True, session_id=session)
    rank.stop_heartbeat()
    assert rank._lease_registered is False and session not in app.leases[owner.id]
    app.fail_paths = set()

    rank.finish("failed")

    assert app.leases[owner.id][session]["exit_status"] == "failed"


def _status_patches(app, run_id) -> list:
    return [
        p.get("status")
        for p in _bodies(
            [r for r in app.requests if r.method == "PATCH" and r.url.path == f"/v1/runs/{run_id}"]
        )
        if p.get("status") is not None
    ]


def test_an_attached_job_that_owns_the_verdict_holds_an_owner_lease(client, app):
    """No finalizing launcher will close this run (a PROBE_RUN_ID forwarded
    to another machine, a scheduler hand-off): the job's lease is an OWNER's.
    A hand-off run was opened without a lease, so it is not on leases: the
    job closes it exactly as before 2.8 (its status) and releases its lease."""
    handoff = _open(client, awaiting_attach=True)
    app.runs[handoff.id]["status"] = "running"
    job = client.attach_run(handoff.id, heartbeat=True, attached=True)
    job.stop_heartbeat()
    assert app.leases[handoff.id][job.session_id]["role"] == "owner"
    assert job._lease_protocol == "legacy", "the attach beat said so"

    job.finish()

    assert _status_patches(app, handoff.id) == ["completed"]
    assert _bodies(_lease_requests(app, handoff.id, "release"))[-1]["exit_status"] == "completed"
    assert app.runs[handoff.id]["status"] == "completed"


def test_a_job_under_a_finalizing_launcher_is_a_rank(client, app, monkeypatch):
    from probe.sdk.run import EXEC_FINALIZES_ENV

    launcher = _open(client, launcher=True)
    monkeypatch.setenv(EXEC_FINALIZES_ENV, launcher.id)
    job = client.attach_run(launcher.id, heartbeat=True, attached=True)
    job.stop_heartbeat()
    assert app.leases[launcher.id][job.session_id]["role"] == "rank"


def test_a_ranks_failure_survives_the_verdict_owning_jobs_close(client, app, monkeypatch):
    """Review of #2060: the process that opened the run finishes, rank 3
    fails, then job 0 (which owns the verdict) finishes `completed`. Before,
    job 0's own status PATCH turned the leases' `failed` back into
    `completed`. Now the run ends `failed` and nobody overwrites it."""
    opener = _open(client)
    job0 = client.attach_run(opener.id, heartbeat=True, attached=True)
    job3 = _attach_rank(client, opener.id, monkeypatch, rank=3)
    for handle in (job0, job3):
        handle.stop_heartbeat()
    assert app.leases[opener.id][job0.session_id]["role"] == "owner"

    opener.finish()
    assert app.runs[opener.id]["status"] == "running", "job 0 still owns work"
    job3.finish("failed")
    job0.finish()

    assert app.runs[opener.id]["status"] == "failed"
    assert _status_patches(app, opener.id) == []


def test_a_wrong_death_report_heals_under_the_writers_own_lease(client, app, tmp_path, monkeypatch):
    """2.2's report was wrong: the owner's beat lands on the crashed row, its
    keep-epoch recovery reopens the run under its own lease (reviving it), and
    its finish then closes the run `completed`, not `crashed`."""
    from probe.sdk import outputs

    monkeypatch.setattr(outputs, "_recovery_client", lambda record: (client, client.journal))
    run = _open(client)
    run.stop_heartbeat()
    capture = outputs.OutputCapture(
        client, run.id, str(tmp_path), tee=False, launcher=False, writer=run._writer_record()
    )
    entry = tmp_path / "rec.json"
    import json as _json

    entry.write_text(_json.dumps(capture._record(shared_with=[])))
    assert outputs.writer_gone(str(entry))["applied"] is True
    assert app.runs[run.id]["status"] == "crashed"

    client._fake = app
    _beat_a_few(client, run, n=2)
    reopen = [r for r in app.requests if r.url.path.endswith("/reopen")][-1]
    (body,) = _bodies([reopen])
    assert body["session_id"] == run.session_id and body["writer"]["session_id"] == run.session_id
    assert app.runs[run.id]["status"] == "running"

    run.finish()
    assert app.runs[run.id]["status"] == "completed"


def test_a_release_names_its_writer_when_no_beat_ever_landed(client, app, monkeypatch):
    """Every beat of this rank failed, the one at its close included: its
    release still registers it, so its `failed` is in the run's verdict
    instead of vanishing (review of #2058)."""
    owner = _open(client)
    owner.stop_heartbeat()
    session = "22222222-2222-4222-8222-222222222222"
    app.fail_paths = {f"/v1/runs/{owner.id}/writers/{session}/beat"}
    monkeypatch.setenv("RANK", "1")
    monkeypatch.setenv("WORLD_SIZE", "4")
    rank = client.attach_run(owner.id, heartbeat=True, attached=True, session_id=session)
    rank._sends_terminal_status = False
    rank.stop_heartbeat()

    rank.finish("failed")

    lease = app.leases[owner.id][session]
    assert (lease["role"], lease["exit_status"]) == ("rank", "failed")
    owner.finish()
    assert app.runs[owner.id]["status"] == "failed"


def test_a_deferred_close_queues_its_verdict_before_the_draining_beat(app, tmp_path, monkeypatch):
    """A pre-empted job may be killed at any moment of its close: the verdict
    is on disk before the draining beat goes out, and that beat is bounded
    (review of #2060)."""
    from probe.sdk.transport import deadline_remaining

    client = make_client(app, tmp_spool=tmp_path / "outbox", async_writes=True)
    run = _open(client)
    run.stop_heartbeat()
    app.fail_paths = {f"/v1/runs/{run.id}/metrics"}
    run.log({"loss": 1.0}, step=1)
    seen: list[tuple[bool, float]] = []
    real = client.beat_writer

    def beat(run_id, session_id, body):
        if "draining_for_seconds" in body:
            queued = [op for _, op in client.journal.pending() if op.get("run_ref") == run_id]
            has_release = any(str(op.get("path", "")).endswith("/release") for op in queued)
            seen.append((has_release, deadline_remaining(999.0)))
        return real(run_id, session_id, body)

    monkeypatch.setattr(client, "beat_writer", beat)
    run.finish(flush_timeout=0.2)

    ((queued_first, budget),) = seen
    assert queued_first, "the release was queued before the draining beat"
    assert budget <= run_mod._CLOSE_BEAT_SECONDS


def test_ranks_attaching_together_spread_their_first_beat(client, app, monkeypatch):
    """608 ranks attaching at once: each waits up to 2 s before its attach
    beat. A single process waits nothing."""
    from probe.sdk import client as client_mod

    owner = _open(client)
    owner.stop_heartbeat()
    sleeps: list[float] = []
    monkeypatch.setattr(client_mod.time, "sleep", lambda s: sleeps.append(s))
    monkeypatch.setattr(client_mod.random, "uniform", lambda a, b: b)
    monkeypatch.setenv("RANK", "5")
    monkeypatch.setenv("WORLD_SIZE", "608")
    client.attach_run(owner.id, heartbeat=True, attached=True).stop_heartbeat()
    monkeypatch.delenv("RANK")
    monkeypatch.delenv("WORLD_SIZE")
    client.attach_run(owner.id, heartbeat=True, attached=True).stop_heartbeat()
    assert sleeps == [2.0]


def test_a_beat_that_says_the_lease_is_gone_warns_once(client, app):
    run = _open(client)
    run.stop_heartbeat()
    app.leases[run.id][run.session_id]["gone_at"] = "2026-09-27T00:00:00Z"
    with pytest.warns(UserWarning, match="reported dead"):
        run_mod._lease_beat(client, run.id, run._lease, 1, weakref.ref(run))
    import warnings as _warnings

    with _warnings.catch_warnings():
        _warnings.simplefilter("error")
        run_mod._lease_beat(client, run.id, run._lease, 1, weakref.ref(run))


def test_a_launcher_resumes_under_a_launchers_lease(client, app):
    first = _open(client, external_id="job-l", launcher=True)
    first.finish("failed")
    second = client.run(
        project="project-e",
        experiment="e",
        name="r",
        external_id="job-l",
        on_conflict="resume",
        launcher=True,
    )
    second.stop_heartbeat()
    assert second._lease["role"] == "launcher"
    assert app.leases[second.id][second.session_id]["role"] == "launcher"


def test_a_finished_leased_incumbents_completed_release_is_not_held(app, tmp_path):
    """#2069's rule on a leases run: a queued `completed` release is the
    incumbent having FINISHED, so the barrier delivers it instead of holding
    it, and the relaunch knows the run completed."""
    outbox = tmp_path / "pv"
    pod1 = make_client(app, tmp_spool=outbox, async_writes=True)
    old = _open(pod1, external_id="job-3")
    app.fail_paths = {f"/v1/runs/{old.id}/metrics"}
    old.log({"loss": 1.0}, step=1)
    old.finish(flush_timeout=0.1)
    app.fail_paths = set()
    pod2 = make_client(app, tmp_spool=outbox, async_writes=True)
    ops = {p.name: op for p, op in pod2.journal.pending()}
    assert pod2._queued_completed_close(app.runs[old.id]) is True
    held = pod2._hold_status_writes(app.runs[old.id], ops)
    assert not [n for n in held if ops[n]["method"] == "POST"], "the completed release is delivered"
