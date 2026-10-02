"""Outbox telemetry: the two events that make a wedged queue visible.

Three contracts, and every test here is written to fail when the one it names is
removed. The first version of this file did not manage that: its banner test
patched `emit_outbox_stuck` to explode and asserted only that the drainer was
still kicked, so DELETING the call left it green.

  * a swallow site keeps swallowing and a wedged queue still gets kicked --
    observability that breaks delivery is worse than no observability;
  * the volume is bounded ACROSS PROCESSES, because the workload is a training
    loop shelling out to `probe log` per step and every in-memory budget resets
    on each one;
  * the killswitch and the self-host egress gate are checked BEFORE anything is
    written or claimed, and the return value says what actually happened.
"""

from __future__ import annotations

import importlib

import pytest

from probe.cli import telemetry as tm
from probe.sdk import outbox_worker
from probe.sdk.journal import DrainReport, Journal
from probe.sdk.outbox_worker import OutboxOutcome

HOSTED = "https://api.research.prbe.ai"
SELF_HOST = "https://research.internal.example.com"


@pytest.fixture(autouse=True)
def isolate(tmp_path, monkeypatch):
    """State/config into a tmpdir, and a developer's exported creds cleared --
    effective_base_url honors PROBE_BASE_URL, which would flip the hosted gate."""
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(tmp_path / "probe" / "config.json"))
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    for var in ("PROBE_BASE_URL", "PROBE_TOKEN", "PROBE_MCP_TOKEN", "PROBE_OUTBOX_DIR"):
        monkeypatch.delenv(var, raising=False)
    (tmp_path / "probe").mkdir(parents=True, exist_ok=True)
    return tmp_path


@pytest.fixture()
def captured(monkeypatch):
    """Capture emit() records at the queue seam: no thread, no network."""
    records: list[dict] = []
    monkeypatch.setenv("PROBE_TELEMETRY", "on")
    monkeypatch.setattr(tm, "_sender", None)
    monkeypatch.setattr(tm, "_flush_registered", True)  # keep atexit out of tests
    monkeypatch.setattr(tm._Sender, "start", lambda self: None)
    monkeypatch.setattr(tm._Sender, "put", lambda self, rec: records.append(rec))
    return records


def events(records, name):
    return [r["properties"] for r in records if r["event"] == name]


def seeded_journal(tmp_path, base_url: str = HOSTED) -> Journal:
    """A journal holding one real op with a pinned backend.

    Not a convenience: the worker resolves its egress gate from the base_url
    PINNED ON THE OPS, so a journal with no ops proves nothing about the gate.
    """
    journal = Journal(str(tmp_path / "outbox"), context={"name": None, "base_url": base_url})
    journal.append_http("POST", "/v1/runs/r/metrics", {"k": 1})
    return journal


def draining(journal, reports):
    """A fake `drain` that also EMPTIES the journal once it reports remaining=0.

    Without that the worker is right and the test is wrong: the exit-race guard
    re-reads status.json before exiting, still sees the seeded op (nothing
    removed it), and loops forever. A fake that reports "empty" while leaving the
    queue full is not a fake of draining.
    """

    def _drain(j, **kwargs):
        report = reports.pop(0)
        if report.remaining == 0:
            for op in journal.ops_dir.glob("*.json"):
                op.unlink()
            journal.write_status()
        return report

    return _drain


# -- the drainer's own report --------------------------------------------------


def test_clean_drain_reports_the_happy_path(tmp_path, monkeypatch, captured):
    """The baseline is load-bearing: without a `drained` event, a healthy silent
    fleet and a fleet whose workers all died look identical on the dashboard."""
    journal = seeded_journal(tmp_path)
    reports = [
        DrainReport(delivered=2, remaining=1, stopped_transient=True, errors=["net"]),
        DrainReport(delivered=3, dead_lettered=1, remaining=0),
    ]
    monkeypatch.setattr("probe.sdk.journal.drain", draining(journal, reports))
    monkeypatch.setattr(outbox_worker.time, "sleep", lambda s: None)

    assert outbox_worker.run(str(journal.dir)) == 0

    (props,) = events(captured, tm.EVENT_OUTBOX_DRAINED)
    assert props["outcome"] == OutboxOutcome.DRAINED
    # Tallies ACCUMULATE across passes; a per-pass report would undercount.
    assert props["delivered"] == 5
    assert props["dead_lettered"] == 1
    assert props["remaining"] == 0
    assert props["passes"] == 2


def test_auth_block_reports_the_state_a_human_must_fix(tmp_path, monkeypatch, captured):
    journal = seeded_journal(tmp_path)
    monkeypatch.setattr(
        "probe.sdk.journal.drain",
        lambda j, **k: DrainReport(remaining=2, auth_blocked=True, errors=["401"]),
    )
    assert outbox_worker.run(str(journal.dir)) == 3

    (props,) = events(captured, tm.EVENT_OUTBOX_DRAINED)
    assert props["outcome"] == OutboxOutcome.AUTH_BLOCKED
    assert props["remaining"] == 2


def test_a_paused_queue_reports_the_depth_it_is_holding(tmp_path, monkeypatch, captured):
    """REGRESSION. The paused branch exits before any drain pass, so `remaining`
    was still its initial 0 -- a `remaining` breakdown showed every paused queue
    as EMPTY, inverting the state a human is meant to act on."""
    journal = seeded_journal(tmp_path)
    journal.pause()

    assert outbox_worker.run(str(journal.dir)) == 4

    (props,) = events(captured, tm.EVENT_OUTBOX_DRAINED)
    assert props["outcome"] == OutboxOutcome.PAUSED
    assert props["passes"] == 0
    assert props["remaining"] == 1, "a paused queue holding one op must not report zero"


def test_a_worker_that_never_exits_still_reports_once(tmp_path, monkeypatch, captured):
    """The loop does not return while it retries, so a wedged server would
    otherwise produce total silence. One STALLED report per worker, at the cap --
    not one per capped pass, which would turn a wedged queue into a beacon."""
    journal = seeded_journal(tmp_path)
    monkeypatch.setattr(
        "probe.sdk.journal.drain",
        lambda j, **k: DrainReport(remaining=4, stopped_transient=True, errors=["503"]),
    )
    slept: list[float] = []

    def fake_sleep(seconds):
        slept.append(seconds)
        if len(slept) > 12:  # the loop is infinite by design; cut it short
            raise KeyboardInterrupt

    monkeypatch.setattr(outbox_worker.time, "sleep", fake_sleep)
    with pytest.raises(KeyboardInterrupt):
        outbox_worker.run(str(journal.dir))

    stalled = events(captured, tm.EVENT_OUTBOX_DRAINED)
    assert [p["outcome"] for p in stalled] == [OutboxOutcome.STALLED]
    assert stalled[0]["remaining"] == 4
    assert max(slept) == outbox_worker._BACKOFF_CAP_SECONDS


def test_broken_telemetry_never_strands_the_queue(tmp_path, monkeypatch, captured):
    """Telemetry is a bystander to delivery, not a step in it. Asserts the report
    was ATTEMPTED as well as absorbed -- otherwise this passes identically when
    the report is never wired at all."""
    journal = seeded_journal(tmp_path)
    tried: list[str] = []

    def explode(**kwargs):
        tried.append(kwargs["outcome"])
        raise RuntimeError("posthog is on fire")

    monkeypatch.setattr(tm, "emit_outbox_drained", explode)
    monkeypatch.setattr("probe.sdk.journal.drain", draining(journal, [DrainReport(remaining=0)]))
    monkeypatch.setattr(outbox_worker.time, "sleep", lambda s: None)

    assert outbox_worker.run(str(journal.dir)) == 0
    assert tried == [OutboxOutcome.DRAINED]


@pytest.mark.parametrize("env", [("PROBE_TELEMETRY", "off"), ("PROBE_DIAGNOSTICS", "off")])
def test_the_drained_report_honors_the_killswitch(tmp_path, monkeypatch, captured, env):
    journal = seeded_journal(tmp_path)
    monkeypatch.setenv(*env)
    monkeypatch.setattr("probe.sdk.journal.drain", draining(journal, [DrainReport(remaining=0)]))
    monkeypatch.setattr(outbox_worker.time, "sleep", lambda s: None)

    outbox_worker.run(str(journal.dir))

    if env[0] == "PROBE_TELEMETRY":
        assert events(captured, tm.EVENT_OUTBOX_DRAINED) == []


def test_the_drained_report_never_leaves_a_self_host_install(tmp_path, monkeypatch, captured):
    """The gate reads the base_url PINNED ON THE OPS, because the worker delivers
    each op to that backend -- gating on the ambient config would let a worker
    draining to a self-host endpoint report to the vendor."""
    journal = seeded_journal(tmp_path, base_url=SELF_HOST)
    monkeypatch.setattr("probe.sdk.journal.drain", draining(journal, [DrainReport(remaining=0)]))
    monkeypatch.setattr(outbox_worker.time, "sleep", lambda s: None)

    outbox_worker.run(str(journal.dir))

    assert events(captured, tm.EVENT_OUTBOX_DRAINED) == []


def test_an_unprovable_backend_reports_nothing(tmp_path):
    """Empty queue, an unpinned op, or two ops disagreeing all mean "cannot prove
    which backend this is", and the egress contract makes that a no-send."""
    empty = Journal(str(tmp_path / "empty"))
    empty._ensure()
    assert outbox_worker._pinned_base_url(empty) is None

    mixed = Journal(str(tmp_path / "mixed"), context={"name": None, "base_url": HOSTED})
    mixed.append_http("POST", "/v1/runs/r/metrics", {"k": 1})
    mixed.context = {"name": None, "base_url": SELF_HOST}
    mixed.append_http("POST", "/v1/runs/r/metrics", {"k": 2})
    assert outbox_worker._pinned_base_url(mixed) is None


# -- the foreground stuck report -----------------------------------------------


def test_last_error_is_reduced_to_its_type():
    """`last_error` is `_redact(f"{type(exc).__name__}: {exc}")` -- redacted, but
    still free text. Only the leading class name is metadata."""
    assert tm._error_kind("AuthError: token 'sk-live-abc' rejected by /v1/runs") == "AuthError"
    assert tm._error_kind("no colon here") is None
    assert tm._error_kind("not an identifier!: boom") is None
    assert tm._error_kind(None) is None


def test_age_hours_handles_the_stamps_a_journal_actually_writes():
    """A broken `_age_hours` makes the field VANISH from the payload rather than
    fail anything, because emit drops None-valued props. Silent-failure shaped."""
    from datetime import datetime, timedelta, timezone

    assert tm._age_hours(None) is None
    assert tm._age_hours("not a timestamp") is None
    naive = (datetime.now(timezone.utc) - timedelta(hours=2)).replace(tzinfo=None).isoformat()
    assert 1.9 < tm._age_hours(naive) < 2.1  # a naive stamp reads as UTC
    future = (datetime.now(timezone.utc) + timedelta(hours=3)).isoformat()
    assert tm._age_hours(future) == 0.0  # clock skew clamps, never goes negative


def test_a_drained_queue_with_old_scars_is_not_stuck():
    """REGRESSION. `outbox.stuck` used to fire on the BANNER's condition, which
    includes a dead-letter count. Dead letters are permanent, so a fully drained
    queue kept emitting "stuck" every six hours forever over one op that died
    last month -- a false positive with an unbounded tail."""
    assert tm.stuck_status({"pending": 0, "failed": 7, "paused": False}) is False
    assert tm.stuck_status({"pending": 3, "failed": 0, "paused": True}) is True
    assert tm.stuck_status({"pending": 0, "auth_blocked_since": "2026-08-20T00:00:00+00:00"}) is True


def test_a_refused_credential_is_stuck_too(tmp_path):
    """Since #2041 a revoked token's writes are set aside by fingerprint and the
    queue-wide `auth_blocked_since` stays empty for every stamped write: the
    banner, `probe doctor` and this report read only that field, so a revoked
    per-credential token showed nowhere. `journal.auth_blocked_since` reads
    both, and the root's status carries its credential queues' refusals."""
    import json

    from probe.sdk.journal import CREDENTIAL_NAMESPACE, Journal, auth_blocked_since

    refused = {"pending": 3, "refused_fingerprints": {"fp1": "2026-09-27T10:00:00+00:00"}}
    assert tm.stuck_status(refused) is True
    assert auth_blocked_since(refused) == "2026-09-27T10:00:00+00:00"
    assert auth_blocked_since(refused, {"someone-else"}) is None
    root = Journal(str(tmp_path / "outbox"))
    root.append_http("POST", "/v1/runs/r/metrics", {"k": 1})
    queue = Journal(str(tmp_path / "outbox" / CREDENTIAL_NAMESPACE / "0123456789abcdef"))
    queue.append_http("POST", "/v1/runs/r/metrics", {"k": 2})
    status = json.loads(queue.status_file.read_text())
    status["refused_fingerprints"] = {"fp1": "2026-09-27T10:00:00+00:00"}
    queue.status_file.write_text(json.dumps(status))
    assert auth_blocked_since(Journal.read_status(str(root.dir))) == "2026-09-27T10:00:00+00:00"


def test_the_throttle_is_shared_across_processes(tmp_path):
    """The whole point. An in-memory budget is defeated by a training loop
    shelling out to `probe log` per step: each invocation is a fresh interpreter
    with a fresh counter, so N commands would mean N reports."""
    spool = tmp_path / "outbox"
    spool.mkdir()
    assert tm.report_due(str(spool), "stuck", interval_s=3600) is True
    assert tm.report_due(str(spool), "stuck", interval_s=3600) is False
    assert tm.report_due(str(spool), "stuck", interval_s=0) is True
    # A different key has its own window.
    assert tm.report_due(str(spool), "swallow-client.lease_renew", interval_s=3600) is True


def test_only_one_concurrent_caller_claims_the_window(tmp_path):
    """The journal dir is shared across ranks, so N processes can stat before any
    of them writes. O_CREAT|O_EXCL decides a single winner."""
    from concurrent.futures import ThreadPoolExecutor

    spool = tmp_path / "outbox"
    spool.mkdir()
    with ThreadPoolExecutor(max_workers=16) as pool:
        results = list(pool.map(lambda _: tm.report_due(str(spool), "stuck", interval_s=3600), range(16)))

    assert results.count(True) == 1


def test_stuck_payload_carries_ages_and_no_free_text(tmp_path, captured):
    from datetime import datetime, timedelta, timezone

    spool = tmp_path / "outbox"
    spool.mkdir()
    blocked = (datetime.now(timezone.utc) - timedelta(hours=5)).isoformat()
    status = {
        "pending": 7,
        "failed": 2,
        "paused": False,
        "auth_blocked_since": blocked,
        "oldest_pending": blocked,
        "last_error": "AuthError: token 'sk-live-abc' rejected",
    }

    assert tm.emit_outbox_stuck(status, spool_dir=str(spool), base_url=HOSTED) is True

    (props,) = events(captured, tm.EVENT_OUTBOX_STUCK)
    assert props["pending"] == 7
    assert props["dead_lettered"] == 2
    assert props["auth_blocked"] is True
    assert props["paused"] is False
    assert 4.9 < props["auth_blocked_age_hours"] < 5.1
    assert 4.9 < props["oldest_pending_age_hours"] < 5.1
    assert props["last_error_kind"] == "AuthError"
    assert "sk-live-abc" not in repr(props)


@pytest.mark.parametrize(
    "kwargs,env",
    [
        ({"base_url": HOSTED}, ("PROBE_TELEMETRY", "off")),
        ({"base_url": SELF_HOST}, None),
        ({"base_url": None}, None),
    ],
    ids=["killswitch", "self-host", "unknown-backend"],
)
def test_a_suppressed_stuck_report_says_so_and_stamps_nothing(
    tmp_path, monkeypatch, captured, kwargs, env
):
    """REGRESSION, two bugs in one place. It returned True whenever the STAMP was
    written -- including when the context was disabled and `emit` was a silent
    no-op -- so it claimed to have sent an event it never sent. And it stamped
    before checking the gates, so `PROBE_TELEMETRY=off` burned the six-hour
    window: turning telemetry back on left the fleet blind to that queue for six
    more hours."""
    if env:
        monkeypatch.setenv(*env)
    spool = tmp_path / "outbox"
    spool.mkdir()
    status = {"pending": 3, "paused": True}

    assert tm.emit_outbox_stuck(status, spool_dir=str(spool), **kwargs) is False

    assert events(captured, tm.EVENT_OUTBOX_STUCK) == []
    assert list(spool.iterdir()) == [], "a suppressed reporter must not claim the window"


# -- the banner wiring ---------------------------------------------------------


@pytest.mark.parametrize(
    "status",
    [
        {"pending": 1, "failed": 0, "paused": False, "auth_blocked_since": "2026-08-20T00:00:00+00:00"},
        {"pending": 1, "failed": 0, "paused": True, "auth_blocked_since": None},
    ],
    ids=["auth-blocked", "paused"],
)
def test_the_banner_reports_the_states_no_drainer_ever_sees(monkeypatch, status):
    """POSITIVE wiring test. The predecessor patched emit_outbox_stuck to explode
    and asserted only that the drainer was still kicked -- which passes
    identically when the call it guards no longer exists. These two states are
    the event's entire reason to exist: `maybe_spawn` will not fork a worker in
    either, so no drainer ever reports the standing condition."""
    main = importlib.import_module("probe.cli.main")
    seen: list[dict] = []
    monkeypatch.setattr("probe.sdk.journal.Journal.read_status", staticmethod(lambda d=None: status))
    monkeypatch.setattr(tm, "emit_outbox_stuck", lambda s, **kw: seen.append(s))
    monkeypatch.setattr(main, "_kick_drainer", lambda: None)

    main._outbox_notice()

    assert seen == [status]


def test_a_broken_report_still_kicks_the_drainer(monkeypatch, capsys):
    """The banner reports a stuck queue AND re-kicks the worker. If a telemetry
    failure could skip that kick, reporting a stuck outbox would cause one."""
    main = importlib.import_module("probe.cli.main")
    kicked: list[bool] = []
    monkeypatch.setattr(
        "probe.sdk.journal.Journal.read_status",
        staticmethod(
            lambda d=None: {"pending": 3, "failed": 2, "paused": False, "auth_blocked_since": None}
        ),
    )
    monkeypatch.setattr(main, "_kick_drainer", lambda: kicked.append(True))

    def explode(*a, **kw):
        raise RuntimeError("telemetry is on fire")

    monkeypatch.setattr(tm, "emit_outbox_stuck", explode)

    main._outbox_notice()

    assert kicked == [True]
    assert "2 dead-lettered" in capsys.readouterr().err
