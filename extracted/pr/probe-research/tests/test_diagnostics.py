"""Crash reports carried as diagnostic spans.

The gap these close: `fluent._excepthook` has always received the dying
process's `(exc_type, exc, tb)` and kept one bit of it -- "canceled" vs
"failed" -- so a run that died inside Probe's own write path recorded THAT it
broke and never why. The tests that matter here are therefore about what
survives into the payload (the chained cause, the Probe frames) and what must
not (the caller's code, credentials, unbounded size).
"""

from __future__ import annotations

import json
import os
import time

import pytest

import probe
from probe.sdk import diagnostics, errors, fluent
from tests.conftest import make_client


@pytest.fixture
def dead_pids(monkeypatch):
    """Every breadcrumb reads as a corpse. Explicit beats relying on the host's
    pid allocator."""
    monkeypatch.setattr(diagnostics, "_pid_alive", lambda _pid: False)


@pytest.fixture(autouse=True)
def _diagnostics_on(monkeypatch):
    """The suite pins PROBE_TELEMETRY=off, which suppresses diagnostics by
    default. Everything here is about the pipeline being ON, so say so
    precisely -- which is also the override the gate exists to offer."""
    monkeypatch.setenv("PROBE_DIAGNOSTICS", "on")


@pytest.fixture(autouse=True)
def _clean_binding():
    fluent._current.set(None)
    fluent._process_default = None
    fluent._exit_status = "completed"
    fluent._exit_exception = None
    yield
    fluent._current.set(None)
    fluent._process_default = None
    fluent._exit_exception = None


@pytest.fixture
def wired(app, tmp_path, monkeypatch):
    built = []

    def factory(*_a, **_kw):
        client = make_client(app, tmp_spool=tmp_path / "spool")
        built.append(client)
        return client

    monkeypatch.setattr(fluent, "Client", factory)
    app.seed_experiment("e1")
    return built


def _real_transport_failure() -> BaseException:
    """Provoke a genuine `TransportError` from inside `transport.py`.

    A helper in THIS file cannot stand in for one: the raise would execute in a
    test frame, so the traceback would carry no Probe frames at all and the
    filter would be graded against a stack it will never see. Going through the
    real transport is also what puts a chained httpx cause underneath, which is
    the shape the outage actually produced. POST, not GET -- POST is the method
    `transport.py` declines to retry, so this returns without burning retries.
    """
    import httpx

    from probe.sdk.config import Settings
    from probe.sdk.transport import Transport

    def boom(request):
        raise httpx.ConnectError("connection refused", request=request)

    settings = Settings(base_url="http://test", token="ros_pat_deadbeef")
    http = httpx.Client(base_url="http://test", transport=httpx.MockTransport(boom))
    try:
        Transport(settings, client=http).post("/v1/runs/abc/metrics", {})
    except errors.TransportError as exc:
        return exc
    raise AssertionError("the transport did not fail")


# -- the gate ------------------------------------------------------------------
@pytest.mark.parametrize(
    ("diag", "telemetry", "expected"),
    [
        (None, None, False),
        (None, "off", True),
        ("off", None, True),
        # The combination that motivates the precedence: the population that
        # turns analytics off is the population whose incidents cannot be
        # reproduced in-house, so they must be able to keep diagnostics.
        ("on", "off", False),
        ("off", "on", True),
    ],
)
def test_gate_precedence(monkeypatch, diag, telemetry, expected):
    monkeypatch.delenv("PROBE_DIAGNOSTICS", raising=False)
    monkeypatch.delenv("PROBE_TELEMETRY", raising=False)
    if diag is not None:
        monkeypatch.setenv("PROBE_DIAGNOSTICS", diag)
    if telemetry is not None:
        monkeypatch.setenv("PROBE_TELEMETRY", telemetry)
    assert diagnostics.disabled() is expected


# -- what the payload keeps ----------------------------------------------------
def test_chained_cause_survives():
    """`transport.py` raises `TransportError(...) from exc`, so the httpx error
    that actually names the failure -- connect refused vs read timeout -- is one
    link down. A report that stops at the head loses the whole diagnosis, which
    is the exact question left open by the outage this module answers."""
    try:
        try:
            raise OSError("Connection refused by 10.0.0.7:443")
        except OSError as cause:
            raise errors.TransportError("POST /v1/runs/abc/metrics: failed") from cause
    except errors.TransportError as exc:
        report = diagnostics.build_report(exc)

    chain = report["exception"]
    assert [link["type"] for link in chain] == ["TransportError", "OSError"]
    assert "Connection refused" in chain[1]["message"]


def test_status_is_promoted_off_the_typed_error():
    """Whether the backend refused us or we never reached it is the first fork
    in triaging this class of failure, and it is one integer."""
    report = diagnostics.build_report(errors.ServerError("boom", status=503))
    assert report["exception"][0]["status"] == 503


def test_probe_frames_are_kept_and_caller_frames_are_placeholders():
    """Caller frames hold the position -- where our code and theirs meet, the one
    thing a crash report has to answer -- without holding their module paths."""
    report = diagnostics.build_report(_real_transport_failure())

    frames = report["exception"][0]["frames"]
    ours = [f for f in frames if f.get("probe")]
    theirs = [f for f in frames if not f.get("probe")]

    assert ours, "the Probe frame that raised must be reported"
    assert theirs, "the test's own frame must appear, as a placeholder"
    assert all(set(f) == {"probe"} for f in theirs), "a caller frame leaked detail"
    assert all("diagnostics.py" not in f["file"] for f in ours)
    # Package-relative, never absolute: an absolute path carries the customer's
    # usernames and cluster mount points and tells us nothing extra.
    assert all(not f["file"].startswith("/") for f in ours)


def test_environment_is_stamped():
    report = diagnostics.build_report(ValueError("x"))
    assert report["environment"]["sdk_version"]
    assert report["environment"]["python"]


def test_client_state_records_the_delivery_mode(app, tmp_path):
    """Once async_writes defaults on, a failed write journals instead of raising,
    so the run quietly stops receiving metrics while training continues. A report
    that does not say which mode was in force cannot tell that apart from a
    transport failure."""
    client = make_client(app, tmp_spool=tmp_path / "spool", async_writes=True)
    report = diagnostics.build_report(ValueError("x"), client=client)
    assert report["client"]["async_writes"] is True


# -- what the payload must not keep --------------------------------------------
#: Assembled rather than written literally. The pre-push secret scanner matches
#: `scheme://user:pass@host` on sight, and a test fixture that trips it on every
#: push trains people to bypass the guard -- which costs more than the fixture
#: reading slightly awkwardly. No single literal here carries both `://` and `@`.
_CREDENTIALED_URL = "https://user:" + "hunter2" + "@" + "api.example.com/v1/runs"


def test_credentials_are_scrubbed():
    exc = errors.TransportError(f"GET {_CREDENTIALED_URL} failed")
    report = diagnostics.build_report(exc)
    blob = json.dumps(report)
    assert "hunter2" not in blob
    assert "<redacted>" in blob


def test_report_is_bounded_and_stays_valid_json():
    """A span write that 413s or stalls because a diagnostic was large would be
    this module causing the class of outage it reports on."""

    def deep(n):
        if n:
            return deep(n - 1)
        raise errors.TransportError("x" * 40_000)

    try:
        deep(60)
    except errors.TransportError as exc:
        report = diagnostics.build_report(exc)

    encoded = json.dumps(report).encode()
    assert len(encoded) <= diagnostics.MAX_REPORT_BYTES
    assert json.loads(encoded)["schema"] == 1


def test_deep_stack_keeps_both_ends():
    """The boundary is at the ends; the middle of a deep recursion is noise."""

    def deep(n):
        if n:
            return deep(n - 1)
        raise ValueError("bottom")

    try:
        deep(80)
    except ValueError as exc:
        report = diagnostics.build_report(exc)

    link = report["exception"][0]
    assert len(link["frames"]) <= diagnostics.MAX_FRAMES
    assert link["frames_elided"] > 0


# -- it must never be the thing that breaks ------------------------------------
def test_nothing_raises_on_a_poisoned_run():
    """A diagnostic that breaks a teardown repeats the original sin in a more
    embarrassing place."""

    class Poisoned:
        def __getattr__(self, _name):
            raise RuntimeError("interpreter teardown")

    diagnostics.report_exception(Poisoned(), ValueError("x"))
    diagnostics.emit(Poisoned(), {"schema": 1})


def test_build_report_survives_an_unprintable_exception():
    class Hostile(Exception):
        def __str__(self):
            raise RuntimeError("nope")

    report = diagnostics.build_report(Hostile())
    assert report["schema"] == 1


# -- end to end through the exit hook ------------------------------------------
def test_crash_writes_a_diagnostic_span_before_the_run_closes(app, wired):
    """Ordering is load-bearing: finish() flips the run terminal and owns the
    delivery barrier, so a span written behind it races a closed run."""
    run = probe.init(experiment="e1", name="r1")
    try:
        raise errors.TransportError("POST /v1/runs/x/metrics: connect timeout")
    except errors.TransportError as exc:
        fluent._exit_status = "failed"
        fluent._exit_exception = exc

    fluent._finish_at_exit()

    (span,) = [s for s in app.spans[run.id] if s["span_type"] == diagnostics.SPAN_TYPE]
    assert span["status"] == "failed"
    assert span["attributes"]["exception"][0]["type"] == "TransportError"
    assert app.runs[run.id]["status"] == "failed"

    paths = [f"{r.method} {r.url.path}" for r in app.requests]
    assert paths.index(f"POST /v1/runs/{run.id}/spans") < len(paths) - 1


def test_a_crash_inside_probe_context_names_the_batch_in_the_diagnostic_span(app, wired):
    """`probe.context` exists so the crash email can say which batch died: the
    ids must survive the real exit path (excepthook -> atexit -> span)."""
    run = probe.init(experiment="e1", name="r1")
    try:
        with probe.context(batch_id="b7", epoch=3):
            raise ValueError("NaN in the loss")
    except ValueError as exc:
        fluent._excepthook(type(exc), exc, exc.__traceback__)

    fluent._finish_at_exit()

    (span,) = [s for s in app.spans[run.id] if s["span_type"] == diagnostics.SPAN_TYPE]
    assert span["attributes"]["context"] == {"run_id": run.id, "batch_id": "b7", "epoch": "3"}
    assert app.runs[run.id]["status"] == "failed"


def test_keyboard_interrupt_files_no_diagnostic(app, wired):
    """Ctrl-C is a decision, not a defect. Reporting it would file a crash on
    every interactive session anyone ever interrupts."""
    run = probe.init(experiment="e1", name="r1")
    fluent._excepthook(KeyboardInterrupt, KeyboardInterrupt(), None)
    fluent._finish_at_exit()

    assert fluent._exit_status == "canceled"
    assert not [s for s in app.spans.get(run.id, []) if s["span_type"] == diagnostics.SPAN_TYPE]


def test_killswitch_suppresses_the_span(app, wired, monkeypatch):
    monkeypatch.setenv("PROBE_DIAGNOSTICS", "off")
    run = probe.init(experiment="e1", name="r1")
    fluent._exit_status = "failed"
    fluent._exit_exception = errors.TransportError("boom")

    fluent._finish_at_exit()

    assert not [s for s in app.spans.get(run.id, []) if s["span_type"] == diagnostics.SPAN_TYPE]
    assert app.runs[run.id]["status"] == "failed"


# -- hard kills: the breadcrumb sweep ------------------------------------------
#: A syntactically valid run id. Anything else is rejected before it can reach a
#: filename or a request path.
_RID = "11111111-2222-4333-8444-555555555555"


#: A pid that is not this process. Liveness is decided by monkeypatching
#: `_pid_alive` rather than by spawning and reaping a real process: the OS
#: releases that pid the instant wait() reaps it, so a recycled pid made the
#: sweep tests fail unreproducibly (macOS PID_MAX is 99999), and it cost three
#: interpreter spawns per module.
_DEAD_PID = 424242


def _dead_pid() -> int:
    return _DEAD_PID


def test_init_arms_a_breadcrumb_and_finish_clears_it(app, wired, tmp_path):
    run = probe.init(experiment="e1", name="r1")
    crumbs = list((tmp_path / "spool").glob("*.crash.json"))
    assert len(crumbs) == 1
    assert json.loads(crumbs[0].read_text())["run_id"] == run.id

    probe.finish()
    assert not list((tmp_path / "spool").glob("*.crash.json"))


def test_sweep_files_a_hard_exit_for_a_dead_process(app, tmp_path, dead_pids):
    """SIGKILL, the OOM killer and a collective timeout all skip atexit, so the
    exit hook never sees them. The breadcrumb is the only evidence that a run
    was open when its process stopped existing.

    The span is JOURNALED, never POSTed: sweep runs inside probe.init(), and a
    synchronous write there would add a 30s timeout per orphan to the startup of
    exactly the population whose backend is unreachable."""
    client = make_client(app, tmp_spool=tmp_path / "spool")
    app.seed_experiment("e1")
    run = client.run(experiment="e1", name="r1")
    before = len(app.spans.get(run.id, []))

    diagnostics.arm(client, run.id)
    crumb = tmp_path / "spool" / f"{run.id}.crash.json"
    payload = json.loads(crumb.read_text())
    payload["pid"] = _dead_pid()
    crumb.write_text(json.dumps(payload))

    filed = diagnostics.sweep(client)

    assert len(filed) == 1
    assert filed[0]["kind"] == "hard_exit"
    assert len(app.spans.get(run.id, [])) == before, "sweep must not touch the network"
    queued = [op for op in client.journal.pending() if "/spans" in str(op)]
    assert queued, "the orphan span must be queued for the drainer"
    assert not crumb.exists(), "a swept breadcrumb must not be reported twice"


def test_sweep_leaves_a_live_process_alone(app, tmp_path):
    """Two runs sharing a journal is the normal case, not a crash."""
    client = make_client(app, tmp_spool=tmp_path / "spool")
    app.seed_experiment("e1")
    run = client.run(experiment="e1", name="r1")

    diagnostics.arm(client, run.id)  # this process, still very much alive
    assert diagnostics.sweep(client) == []
    assert (tmp_path / "spool" / f"{run.id}.crash.json").exists()


def test_sweep_is_bounded(app, tmp_path, monkeypatch, dead_pids):
    """It runs on the init path, and a crash-looping job leaves thousands."""
    client = make_client(app, tmp_spool=tmp_path / "spool")
    dead = _dead_pid()
    spool = tmp_path / "spool"
    spool.mkdir(parents=True, exist_ok=True)
    for i in range(diagnostics.MAX_SWEEP + 5):
        # Real UUIDs: a run id is interpolated into a filename and a request
        # path, so anything that is not one is rejected before it reaches either.
        rid = f"{i:08d}-0000-4000-8000-000000000000"
        (spool / f"{rid}.crash.json").write_text(json.dumps({"run_id": rid, "pid": dead}))

    assert len(diagnostics.sweep(client)) == diagnostics.MAX_SWEEP


def test_sweep_discards_a_torn_breadcrumb(app, tmp_path):
    """Rather than re-reading it on every init forever."""
    client = make_client(app, tmp_spool=tmp_path / "spool")
    spool = tmp_path / "spool"
    spool.mkdir(parents=True, exist_ok=True)
    torn = spool / "half-written.crash.json"
    torn.write_text('{"run_id": "x", "pi')

    assert diagnostics.sweep(client) == []
    assert not torn.exists()


def test_killswitch_arms_nothing(app, wired, tmp_path, monkeypatch):
    monkeypatch.setenv("PROBE_DIAGNOSTICS", "off")
    probe.init(experiment="e1", name="r1")
    assert not list((tmp_path / "spool").glob("*.crash.json"))


# -- the transport ring buffer -------------------------------------------------
# NB: the ring buffer / breadcrumb / throttle globals are reset by the
# suite-wide `_reset_diagnostics_state` fixture in conftest.py.


def test_a_successful_request_is_recorded(app, tmp_path):
    client = make_client(app, tmp_spool=tmp_path / "spool")
    app.seed_experiment("e1")
    client.run(experiment="e1", name="r1")

    log = diagnostics.recent_transport()
    assert log, "the transport recorded nothing"
    assert all("ms" in e for e in log)
    assert any(e.get("status") == 200 or e.get("status") == 201 for e in log)


def test_a_stall_is_flagged_without_any_exception(monkeypatch):
    """The whole point. A stalled endpoint raises nothing -- it just takes the
    caller's wall clock -- so duration is the only signal that exists."""
    diagnostics.record_transport("POST", "/v1/runs/x/metrics", seconds=12.0, status=200)
    (entry,) = diagnostics.recent_transport()
    assert entry["stalled"] is True
    assert entry["ms"] == 12_000


def test_a_fast_request_is_not_flagged():
    diagnostics.record_transport("POST", "/v1/runs/x/metrics", seconds=0.02, status=200)
    assert "stalled" not in diagnostics.recent_transport()[0]


def test_the_buffer_is_bounded():
    for i in range(diagnostics.TRANSPORT_LOG_SIZE + 20):
        diagnostics.record_transport("GET", f"/v1/x/{i}", seconds=0.01, status=200)
    assert len(diagnostics.recent_transport()) == diagnostics.TRANSPORT_LOG_SIZE


def test_a_transport_failure_reaches_the_report():
    report = diagnostics.build_report(_real_transport_failure())
    assert report["transport"], "the failed request must be in the buffer"
    assert report["transport"][-1]["error"]


def test_an_incident_refreshes_the_breadcrumb(app, tmp_path):
    """This is what makes an in-memory buffer survive a SIGKILL: the file on
    disk is the only thing that outlives the process."""
    client = make_client(app, tmp_spool=tmp_path / "spool")
    diagnostics.arm(client, _RID)
    crumb = tmp_path / "spool" / f"{_RID}.crash.json"
    assert "transport" not in json.loads(crumb.read_text())

    diagnostics.record_transport("POST", "/v1/runs/x/metrics", seconds=30.0, error="timeout")

    persisted = json.loads(crumb.read_text())
    assert persisted["transport"][-1]["stalled"] is True
    assert persisted["transport"][-1]["error"] == "timeout"


def test_breadcrumb_refresh_is_throttled(app, tmp_path):
    """A hard failure loop can produce thousands of incidents a second, and this
    runs on the write path."""
    client = make_client(app, tmp_spool=tmp_path / "spool")
    diagnostics.arm(client, _RID)
    crumb = tmp_path / "spool" / f"{_RID}.crash.json"

    diagnostics.record_transport("POST", "/a", seconds=30.0, error="one")
    first = json.loads(crumb.read_text())["transport"]
    diagnostics.record_transport("POST", "/b", seconds=30.0, error="two")
    second = json.loads(crumb.read_text())["transport"]

    assert first == second, "the second incident rewrote the file inside the floor"


def test_a_hard_exit_report_carries_the_last_transport_state(app, tmp_path, dead_pids):
    """For a kill with no traceback, this is the only evidence there is."""
    client = make_client(app, tmp_spool=tmp_path / "spool")
    app.seed_experiment("e1")
    run = client.run(experiment="e1", name="r1")
    diagnostics.arm(client, run.id)
    diagnostics.record_transport("POST", "/v1/runs/x/metrics", seconds=30.0, error="stalled")

    crumb = tmp_path / "spool" / f"{run.id}.crash.json"
    payload = json.loads(crumb.read_text())
    payload["pid"] = _dead_pid()
    crumb.write_text(json.dumps(payload))

    (filed,) = diagnostics.sweep(client)
    assert filed["transport"][-1]["error"] == "stalled"


def test_disarm_stops_refreshing(app, tmp_path):
    client = make_client(app, tmp_spool=tmp_path / "spool")
    diagnostics.arm(client, _RID)
    diagnostics.disarm(client, _RID)
    diagnostics.record_transport("POST", "/a", seconds=30.0, error="boom")  # must not recreate
    assert not (tmp_path / "spool" / f"{_RID}.crash.json").exists()


# -- regressions from the pre-merge security + red-team review -----------------
@pytest.mark.parametrize(
    ("build", "secrets"),
    [
        (lambda: KeyError("OPENAI_API_KEY"), ["OPENAI_API_KEY"]),
        (
            lambda: FileNotFoundError(2, "No such file", "/Users/alice/unreleased-thing/train.py"),
            ["alice", "unreleased-thing"],
        ),
        (
            lambda: AssertionError("config={'api_key': 'sk-live-abc123', 'host': 'gpu-17.acme'}"),
            ["sk-live-abc123"],
        ),
        (
            lambda: errors.TransportError("GET https://api.acme.com/v1/x?token=SECRET123 failed"),
            ["SECRET123"],
        ),
    ],
)
def test_exception_messages_are_scrubbed(build, secrets):
    """The frame filter keeps caller CODE out of a report and the message channel
    walked straight around it. KeyError names its key, FileNotFoundError names
    its path, an assertion prints whatever the author interpolated -- all of it
    shipped verbatim before this. Verified leaking; this is the regression."""
    try:
        raise build()
    except Exception as exc:
        blob = json.dumps(diagnostics.build_report(exc))
    for secret in secrets:
        assert secret not in blob, f"{secret!r} leaked into the report"


def test_transport_error_strings_are_scrubbed():
    diagnostics.record_transport(
        "POST", "/v1/runs/x/metrics", seconds=0.1, error="open('/home/bob/secret.pt') failed"
    )
    entry = diagnostics.recent_transport()[-1]
    assert "bob" not in entry["error"]
    assert "<path>" in entry["error"]


def test_content_hashes_survive_scrubbing():
    """A long hex run is a sha in this codebase, not a secret, and it joins a
    report to an artifact. Over-redacting it would cost real diagnostic value."""
    sha = "a" * 64
    diagnostics.record_transport("GET", f"/v1/artifacts/{sha}", seconds=0.1, status=200)
    assert sha in diagnostics.recent_transport()[-1]["p"]


def test_breadcrumb_is_private(app, tmp_path):
    """journal.py enforces 0700/0600 because "queue contents are research data".
    A breadcrumb sits in that directory carrying the same class of thing."""
    import stat

    client = make_client(app, tmp_spool=tmp_path / "spool")
    diagnostics.arm(client, _RID)
    crumb = tmp_path / "spool" / f"{_RID}.crash.json"
    assert stat.S_IMODE(crumb.stat().st_mode) == 0o600


@pytest.mark.parametrize("hostile", ["../../etc/passwd", "x/../../y", "not-a-uuid", ""])
def test_hostile_run_ids_are_refused(app, tmp_path, hostile):
    """run_id reaches both a filename and a request path, and in the sweep case
    it arrives from a JSON file on disk."""
    client = make_client(app, tmp_spool=tmp_path / "spool")
    diagnostics.arm(client, hostile)
    assert not list((tmp_path / "spool").glob("*.crash.json"))


def test_sweep_discards_a_breadcrumb_with_a_hostile_run_id(app, tmp_path, dead_pids):
    client = make_client(app, tmp_spool=tmp_path / "spool")
    spool = tmp_path / "spool"
    spool.mkdir(parents=True, exist_ok=True)
    bad = spool / "evil.crash.json"
    bad.write_text(json.dumps({"run_id": "../../v1/elsewhere", "pid": _dead_pid()}))

    assert diagnostics.sweep(client) == []
    assert not bad.exists()


def test_another_hosts_breadcrumb_is_left_alone(app, tmp_path):
    """The journal defaults to a home directory, which is shared NFS on any
    ordinary cluster. A pid from node A means nothing on node B -- sweeping it
    would file a crash against a LIVE run and then delete the evidence."""
    client = make_client(app, tmp_spool=tmp_path / "spool")
    diagnostics.arm(client, _RID)
    crumb = tmp_path / "spool" / f"{_RID}.crash.json"
    payload = json.loads(crumb.read_text())
    payload["host"] = "some-other-node:deadbeef"
    payload["pid"] = _dead_pid()
    crumb.write_text(json.dumps(payload))

    assert diagnostics.sweep(client) == []
    assert crumb.exists(), "a foreign host's evidence must survive"


def test_an_undeliverable_orphan_keeps_its_breadcrumb(app, tmp_path, monkeypatch, dead_pids):
    """Unlinking regardless destroyed the evidence with nothing recorded and no
    retry -- and a full disk is both why the append failed and why the next
    attempt is worth having."""
    client = make_client(app, tmp_spool=tmp_path / "spool")
    diagnostics.arm(client, _RID)
    crumb = tmp_path / "spool" / f"{_RID}.crash.json"
    payload = json.loads(crumb.read_text())
    payload["pid"] = _dead_pid()
    crumb.write_text(json.dumps(payload))

    def boom(*_a, **_kw):
        raise OSError("no space left on device")

    monkeypatch.setattr(client.journal, "append_http", boom)
    assert diagnostics.sweep(client) == []
    assert crumb.exists(), "evidence destroyed with nothing recorded"
    assert json.loads(crumb.read_text())["attempts"] == 1


def test_an_undeliverable_orphan_is_eventually_dropped(app, tmp_path, monkeypatch, dead_pids):
    client = make_client(app, tmp_spool=tmp_path / "spool")
    diagnostics.arm(client, _RID)
    crumb = tmp_path / "spool" / f"{_RID}.crash.json"
    payload = json.loads(crumb.read_text())
    payload["pid"] = _dead_pid()
    payload["attempts"] = diagnostics.MAX_ORPHAN_ATTEMPTS - 1
    crumb.write_text(json.dumps(payload))

    monkeypatch.setattr(
        client.journal, "append_http", lambda *a, **k: (_ for _ in ()).throw(OSError())
    )
    diagnostics.sweep(client)
    assert not crumb.exists(), "a permanently-undeliverable crumb must not be swept forever"


def test_the_with_form_disarms(app, wired, tmp_path):
    """`with probe.init(...) as run:` goes through Run.__exit__ -> Run.finish and
    never touches fluent.finish, so a breadcrumb disarmed only there stayed
    armed for the ergonomic the docs advertise."""
    with probe.init(experiment="e1", name="r1"):
        assert list((tmp_path / "spool").glob("*.crash.json"))
    assert not list((tmp_path / "spool").glob("*.crash.json"))


def test_fork_reset_clears_inherited_state(app, tmp_path):
    """A child forked while _REFRESH_LOCK was held inherits it LOCKED with no
    thread alive to release it. A deadlock is not an exception, so the module's
    swallow-everything discipline would not have caught it."""
    client = make_client(app, tmp_spool=tmp_path / "spool")
    diagnostics.arm(client, _RID)
    diagnostics._REFRESH_LOCK.acquire()
    try:
        diagnostics._reset_after_fork()
        assert diagnostics._REFRESH_LOCK.acquire(blocking=False), "child inherited a locked lock"
        diagnostics._REFRESH_LOCK.release()
        assert diagnostics._ACTIVE_BREADCRUMB is None, "child must not rewrite the parent's crumb"
    finally:
        pass


# -- the size-shedding ladder (mutation testing proved every tier untested) ----
def _chained(depth: int = 3) -> BaseException:
    exc: BaseException = ValueError("root cause with some text to occupy bytes")
    for i in range(depth):
        try:
            raise errors.TransportError(f"link {i} " + "x" * 60) from exc
        except errors.TransportError as e:
            exc = e
    return exc


def _bulky_report() -> dict:
    """A report with something at every rung: Probe frames carrying source
    lines, caller placeholders, and a multi-link chain."""
    link = {
        "type": "TransportError",
        "module": "probe.sdk.errors",
        "message": "m" * 120,
        "frames": (
            [
                {
                    "probe": True,
                    "file": "sdk/transport.py",
                    "line": 221,
                    "func": "request",
                    "code": "c" * 80,
                }
                for _ in range(6)
            ]
            + [{"probe": False} for _ in range(6)]
        ),
    }
    return {
        "schema": 1,
        "environment": {"sdk_version": "0.0.0"},
        "exception": [dict(link) for _ in range(4)],
    }


@pytest.mark.parametrize("marker", ["frame source", "caller frames", "chain"])
def test_fit_sheds_in_order(monkeypatch, marker):
    """Each tier drops the largest thing that is NOT the diagnosis. Replacing
    _fit's body with `return report` left every test green, because the only
    bounded-report test built 1180 bytes against a 16KB cap.

    Driven through _fit directly with a fixed report: building one from a live
    exception made the input grow between iterations (the transport ring buffer
    accumulates), so the ladder could not be pinned."""
    seen = {}
    full = len(json.dumps(_bulky_report()).encode())
    for budget in range(full, 60, -25):
        monkeypatch.setattr(diagnostics, "MAX_REPORT_BYTES", budget)
        out = diagnostics._fit(_bulky_report())
        assert len(json.dumps(out).encode()) <= budget or out.get("degraded"), (
            f"budget={budget} produced an over-budget report with no degraded marker"
        )
        seen.setdefault(out.get("truncated"), budget)
    assert marker in seen, f"tier {marker!r} never entered; saw {sorted(k for k in seen if k)}"


def test_fit_sheds_unbounded_fields_before_the_diagnosis(monkeypatch):
    """`extra` and `transport` are the only unbounded fields; frames and
    messages are already capped. Shedding the capped ones first spent the budget
    in the wrong place and discarded the exception chain."""
    monkeypatch.setattr(diagnostics, "MAX_REPORT_BYTES", 2000)
    report = diagnostics.build_report(_chained(), extra={"blob": "y" * 50_000})
    assert report["truncated"] == "extra"
    assert report["exception"], "the chain is the diagnosis and must survive"


def test_fit_degrades_honestly_when_nothing_can_be_shed(monkeypatch):
    monkeypatch.setattr(diagnostics, "MAX_REPORT_BYTES", 40)
    report = diagnostics.build_report(_chained())
    assert report["degraded"] == "report exceeded size budget"
    assert report["schema"] == 1


def test_fit_does_not_claim_a_truncation_it_did_not_make(monkeypatch):
    """A hard-exit report carries no exception, so the chain tier popped nothing
    and stamped "chain" anyway — a marker naming a field the report never had."""
    monkeypatch.setattr(diagnostics, "MAX_REPORT_BYTES", 50)
    fitted = diagnostics._fit({"schema": 1, "kind": "hard_exit", "environment": {"x": "z" * 400}})
    assert fitted.get("truncated") != "chain"


def test_fit_does_not_mutate_its_input(monkeypatch):
    monkeypatch.setattr(diagnostics, "MAX_REPORT_BYTES", 600)
    original = diagnostics.build_report(_chained())
    snapshot = json.dumps(original, sort_keys=True)
    diagnostics._fit(original)
    assert json.dumps(original, sort_keys=True) == snapshot


# -- chain bounds --------------------------------------------------------------
def test_chain_is_capped():
    report = diagnostics.build_report(_chained(diagnostics.MAX_CHAIN + 6))
    assert len(report["exception"]) == diagnostics.MAX_CHAIN


def test_a_self_referential_context_terminates():
    exc = ValueError("loop")
    exc.__context__ = exc
    assert diagnostics.build_report(exc)["exception"]


# -- liveness ------------------------------------------------------------------
def test_pid_alive_treats_permission_denied_as_alive(monkeypatch):
    """Another user's pid on a shared node. A false 'dead' files a crash report
    against a healthy run, so this direction is the safe one."""
    monkeypatch.setattr(diagnostics, "_IS_WINDOWS", False)
    monkeypatch.setattr(
        diagnostics.os, "kill", lambda *_a: (_ for _ in ()).throw(PermissionError())
    )
    assert diagnostics._pid_alive(1) is True


def test_pid_alive_reports_a_missing_process(monkeypatch):
    monkeypatch.setattr(diagnostics, "_IS_WINDOWS", False)
    monkeypatch.setattr(
        diagnostics.os, "kill", lambda *_a: (_ for _ in ()).throw(ProcessLookupError())
    )
    assert diagnostics._pid_alive(1) is False


def test_pid_alive_never_calls_os_kill_on_windows(monkeypatch):
    """CPython routes any sig other than CTRL_C/CTRL_BREAK to TerminateProcess,
    so os.kill(pid, 0) KILLS the process. sweep() runs on every probe.init(),
    so a second training run would have terminated its live siblings."""
    called = []
    # `_IS_WINDOWS`, not `os.name`: setting the latter makes pathlib return
    # WindowsPath and takes the rest of the suite down with it.
    monkeypatch.setattr(diagnostics, "_IS_WINDOWS", True)
    monkeypatch.setattr(diagnostics.os, "kill", lambda *a: called.append(a))
    assert diagnostics._pid_alive(4242) is True
    assert called == [], "os.kill must never be reached on Windows"


def test_a_stale_breadcrumb_is_swept_even_while_the_pid_looks_alive(app, tmp_path, monkeypatch):
    """Otherwise 'alive' is permanent for a pid we can never resolve, and the
    evidence is stranded forever."""
    client = make_client(app, tmp_spool=tmp_path / "spool")
    diagnostics.arm(client, _RID)
    crumb = tmp_path / "spool" / f"{_RID}.crash.json"
    old = time.time() - (diagnostics.STALE_AFTER_SECONDS + 60)
    os.utime(crumb, (old, old))
    monkeypatch.setattr(diagnostics, "_pid_alive", lambda _pid: True)

    (filed,) = diagnostics.sweep(client)
    assert filed["kind"] == "hard_exit"


# -- the hang that never returns -----------------------------------------------
def test_an_in_flight_request_is_visible(app, tmp_path):
    """A request that hangs until SIGKILL never reaches either recording site,
    so without the in-flight mark the breadcrumb preserved the last COMPLETED
    request instead of the hanging one — the exact case this exists for."""
    client = make_client(app, tmp_spool=tmp_path / "spool")
    diagnostics.arm(client, _RID)
    diagnostics.begin_transport("POST", "/v1/runs/x/metrics")

    assert diagnostics.recent_transport()[-1] == {
        "m": "POST",
        "p": "/v1/runs/x/metrics",
        "inflight": True,
    }
    persisted = json.loads((tmp_path / "spool" / f"{_RID}.crash.json").read_text())
    assert persisted["transport"][-1]["inflight"] is True

    diagnostics.end_transport()
    assert not [e for e in diagnostics.recent_transport() if e.get("inflight")]


# -- degraded paths ------------------------------------------------------------
def test_build_report_degrades_rather_than_raising(monkeypatch):
    monkeypatch.setattr(
        diagnostics, "default_scrub", lambda *_a, **_k: (_ for _ in ()).throw(RuntimeError())
    )
    assert diagnostics.build_report(ValueError("x"))["degraded"] == "report construction failed"


def test_environment_survives_a_broken_platform(monkeypatch):
    monkeypatch.setattr(
        diagnostics.platform, "python_version", lambda: (_ for _ in ()).throw(RuntimeError())
    )
    assert diagnostics.build_report(ValueError("x"))["environment"]["sdk_version"]


def test_sweep_survives_an_unreadable_directory(app, tmp_path, monkeypatch):
    client = make_client(app, tmp_spool=tmp_path / "spool")
    monkeypatch.setattr(
        diagnostics.os, "listdir", lambda *_a: (_ for _ in ()).throw(PermissionError())
    )
    assert diagnostics.sweep(client) == []


def test_disarm_is_idempotent(app, tmp_path):
    client = make_client(app, tmp_spool=tmp_path / "spool")
    diagnostics.arm(client, _RID)
    diagnostics.disarm(client, _RID)
    diagnostics.disarm(client, _RID)  # must not raise: finish() calls it in a finally
    assert diagnostics._ACTIVE_BREADCRUMB is None


# -- the diagnostic must not change the outcome it reports on ------------------
def test_a_diagnostic_span_cannot_block_a_runs_close(app, tmp_path):
    """finish() refuses to mark a run terminal while any of its ops are
    undelivered or dead-lettered -- right for data, wrong for a best-effort
    write. A diagnostic the server rejects would otherwise leave the run
    `running` for the reaper instead of `failed`."""
    client = make_client(app, tmp_spool=tmp_path / "spool")
    app.seed_experiment("e1")
    run = client.run(experiment="e1", name="r1")

    # journal a diagnostic op the way emit() does when delivery fails
    client.journal.append_http("POST", f"/v1/runs/{run.id}/spans", {"spans": []}, blocking=False)
    assert client.journal.pending(), "the op must really be queued"
    assert run._queued_ops(client.journal.pending()) == [], "it must not gate the close"


def test_an_ordinary_op_still_blocks(app, tmp_path):
    """The carve-out is opt-in, not a hole in the barrier."""
    client = make_client(app, tmp_spool=tmp_path / "spool")
    app.seed_experiment("e1")
    run = client.run(experiment="e1", name="r1")

    client.journal.append_http("POST", f"/v1/runs/{run.id}/metrics", {"points": []})
    assert run._queued_ops(client.journal.pending()), "a data op must still gate"


# -- the originating stall must outlive the rolling window ---------------------
def test_the_first_incident_is_sticky(app, tmp_path):
    """The window is 32 entries -- under a second of a training loop -- and the
    refresh is last-writer-wins, so by SIGKILL time it holds the tail of the
    cascade and has evicted the stall that started it."""
    client = make_client(app, tmp_spool=tmp_path / "spool")
    diagnostics.arm(client, _RID)
    diagnostics.record_transport("POST", "/first", seconds=30.0, error="THE ORIGINAL STALL")
    for i in range(diagnostics.TRANSPORT_LOG_SIZE + 10):
        diagnostics.record_transport("POST", f"/noise/{i}", seconds=0.01, status=200)

    assert not [e for e in diagnostics.recent_transport() if "/first" in e["p"]], (
        "precondition: the window must have evicted it"
    )
    crumb = json.loads((tmp_path / "spool" / f"{_RID}.crash.json").read_text())
    assert crumb["first_incident"]["error"] == "THE ORIGINAL STALL"


def test_a_new_run_starts_a_new_incident_history(app, tmp_path):
    client = make_client(app, tmp_spool=tmp_path / "spool")
    diagnostics.arm(client, _RID)
    diagnostics.record_transport("POST", "/a", seconds=30.0, error="run one")
    other = "22222222-3333-4444-8555-666666666666"
    diagnostics.arm(client, other)
    assert diagnostics._FIRST_INCIDENT is None


# -- one report must not carry another backend's history -----------------------
def test_a_report_carries_only_its_own_backends_requests(app, tmp_path):
    """One process can hold clients for two backends. The buffer is shared, so
    without partitioning a report delivered to one carried the other's paths."""
    client = make_client(app, tmp_spool=tmp_path / "spool")
    mine = client.settings.base_url
    diagnostics.record_transport("GET", "/v1/mine", seconds=0.1, status=200, base=mine)
    diagnostics.record_transport(
        "GET", "/v1/theirs", seconds=0.1, status=200, base="https://other.example"
    )

    report = diagnostics.build_report(ValueError("x"), client=client)
    paths = [e["p"] for e in report["transport"]]
    assert "/v1/mine" in paths
    assert "/v1/theirs" not in paths


# -- the disk floor the outbox reserves ---------------------------------------
def test_a_breadcrumb_respects_the_outbox_disk_floor(app, tmp_path, monkeypatch):
    """journal.py gates blob staging on the same floor because this directory
    sits next to training checkpoints."""
    client = make_client(app, tmp_spool=tmp_path / "spool")
    monkeypatch.setattr(diagnostics, "_has_disk_headroom", lambda _d: False)
    diagnostics.arm(client, _RID)
    assert not list((tmp_path / "spool").glob("*.crash.json"))


# -- blob transfers are the likeliest stalls and were invisible ----------------
def test_artifact_transfers_are_recorded(app, tmp_path):
    """Only request() was instrumented, so the stall detector was blind to the
    longest-running traffic the SDK has."""
    client = make_client(app, tmp_spool=tmp_path / "spool")
    try:
        client.transport.get_url("https://blobs.example.com/bucket/obj?X-Signature=SECRET")
    except Exception:
        pass
    entry = diagnostics.recent_transport()[-1]
    assert entry["p"] == "blobs.example.com/bucket/obj"
    assert "SECRET" not in json.dumps(entry), "the presigned signature must not be recorded"
