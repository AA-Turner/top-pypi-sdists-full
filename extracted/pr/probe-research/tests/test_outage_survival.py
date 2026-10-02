"""What the outbox must do while the server is down.

Async-by-default made the local journal the thing standing between a training
run and lost telemetry. A five-lens audit of 0.99.1 found it degraded during
exactly the outage it exists to survive: the enqueue got slower as the backlog
grew, one 401 stopped delivery forever, a dead worker reported success, a clean
close threw away whatever had not drained yet, and nothing capped the queue
before it filled the disk.

Each test here pins one of those. All were verified to FAIL against the
pre-fix code.
"""

from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone

import pytest

from probe.sdk import journal as journal_mod
from probe.sdk import outbox_worker
from probe.sdk.journal import Journal, OutboxFull


@pytest.fixture(autouse=True)
def _isolated_config(monkeypatch, tmp_path):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(tmp_path / "config" / "probe.json"))
    monkeypatch.delenv("PROBE_ASYNC", raising=False)
    for var in (*journal_mod._GLOBAL_RANK_VARS, "LOCAL_RANK", "PROBE_OUTBOX_DIR"):
        monkeypatch.delenv(var, raising=False)


# -- the enqueue must not slow down as the outage lengthens -------------------


def test_an_append_never_lists_the_queue(tmp_path, monkeypatch):
    """The O(N^2): `_write_status_locked` recounted the queue with `os.listdir`
    on EVERY append, so a training loop writing through an outage got steadily
    slower — measured 1.19ms/append at depth 1 rising to 6.50ms at 8k.

    Asserted as an ALGORITHM, not a duration. A timing assertion needs a deep
    queue to separate the curves and is still at the mercy of a loaded CI box;
    "the enqueue does not scan the directory it is appending to" is the actual
    invariant, and it is instant and deterministic.
    """
    journal = Journal(tmp_path / "outbox")
    journal.register_producer("bench:1", role="sdk")
    for _ in range(20):
        journal.append_http("POST", "/v1/runs/r1/metrics", {"n": 1})

    listings: list[str] = []
    real_listdir = os.listdir
    monkeypatch.setattr(
        os, "listdir", lambda p=".": (listings.append(str(p)), real_listdir(p))[1]
    )
    journal.append_http("POST", "/v1/runs/r1/metrics", {"n": 2})

    queue_scans = [p for p in listings if "ops" in p or "failed" in p]
    assert queue_scans == [], (
        f"append scanned the queue {len(queue_scans)}x — that is the O(N^2): {queue_scans}"
    )


def test_the_drain_still_writes_authoritative_counts(tmp_path, app):
    """The delta counter is an optimisation, not a new source of truth. The
    drain walks both directories anyway, so it must correct any drift."""
    from tests.test_outbox import drain_with

    journal = Journal(tmp_path / "outbox")
    journal.append_http("POST", "/v1/x", {})
    journal.write_status(pending=999)  # pretend the delta drifted
    drain_with(app, journal)

    assert (Journal.read_status(journal.dir) or {})["pending"] == 0


# -- a queue may not grow until it fills the disk ------------------------------


def test_the_queue_has_a_ceiling(tmp_path, monkeypatch):
    """`append_http` had no cap of any kind — no free-space floor, no count
    limit, no backpressure. The upload path's own comment says it best: a
    producer that outruns delivery makes filling the disk the STEADY STATE."""
    monkeypatch.setattr(journal_mod, "MAX_PENDING_OPS", 5)
    journal = Journal(tmp_path / "outbox")
    for _ in range(5):
        journal.append_http("POST", "/v1/x", {})

    with pytest.raises(OutboxFull):
        journal.append_http("POST", "/v1/x", {})


def test_a_refused_write_is_recorded_as_a_gap_not_silence(tmp_path, monkeypatch):
    monkeypatch.setattr(journal_mod, "MAX_PENDING_OPS", 3)
    journal = Journal(tmp_path / "outbox")
    journal.register_producer("sdk:test", role="sdk")
    for _ in range(3):
        journal.append_http("POST", "/v1/x", {})
    with pytest.raises(OutboxFull):
        journal.append_http("POST", "/v1/x", {})

    record = journal.producer_report()[0]
    gaps = record.get("gaps") or []
    assert gaps, "a dropped write must leave a numbered hole in the record"
    assert "outbox full" in gaps[0]["reason"]


def test_a_client_drops_the_datapoint_instead_of_the_run(tmp_path, monkeypatch, app):
    """The enqueue was unguarded on the DEFAULT path, so ENOSPC or a flock-less
    filesystem raised a raw OSError out of run.log() — the original bug with the
    substrate swapped from network to disk."""
    from tests.conftest import make_client

    client = make_client(app, tmp_spool=tmp_path / "outbox", async_writes=True)

    def boom(*a, **kw):
        raise OSError(28, "No space left on device")

    monkeypatch.setattr(client.journal, "append_http", boom)
    # Must not raise.
    assert client.write("POST", "/v1/runs/r1/metrics", {"points": []}) is None
    client.close()


# -- delivery must resume on its own ------------------------------------------


def test_a_stale_auth_block_stops_suppressing_new_workers(tmp_path):
    """One 401 used to disable delivery machine-wide, forever. A token rotating
    mid-run left hours of metrics queued with no retry and no signal."""
    journal = Journal(tmp_path / "outbox")
    journal.append_http("POST", "/v1/x", {})
    stale = datetime.now(timezone.utc) - timedelta(
        seconds=outbox_worker._AUTH_RETRY_COOLDOWN_SECONDS + 60
    )
    journal.write_status(auth_blocked_since=stale.isoformat())

    mp = pytest.MonkeyPatch()
    mp.setattr(outbox_worker.subprocess, "Popen", lambda *a, **k: _LiveChild())
    try:
        assert outbox_worker.maybe_spawn(str(journal.dir)) is True
    finally:
        mp.undo()


class _LiveChild:
    returncode = None

    def poll(self):
        return None


class _DeadChild:
    returncode = 1

    def poll(self):
        return 1


def test_a_worker_that_dies_on_startup_is_not_reported_as_spawned(tmp_path):
    """`Popen` succeeding says the fork worked, not that a worker is running.
    A child that cannot `import probe` still armed the caller's kick throttle,
    so the journal grew while nothing drained."""
    journal = Journal(tmp_path / "outbox")
    journal.append_http("POST", "/v1/x", {})

    mp = pytest.MonkeyPatch()
    mp.setattr(outbox_worker.subprocess, "Popen", lambda *a, **k: _DeadChild())
    try:
        assert outbox_worker.maybe_spawn(str(journal.dir)) is False
    finally:
        mp.undo()


# -- ranks must not serialise on one lock --------------------------------------


def test_each_rank_gets_its_own_journal(monkeypatch, tmp_path):
    """On SLURM with a shared $HOME every rank shared ONE append lock, which
    made metric logging a cluster-wide mutex."""
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    monkeypatch.setenv("SLURM_PROCID", "7")
    assert journal_mod.default_dir().name == "rank-7"


def test_an_explicit_outbox_dir_is_split_per_rank_too(monkeypatch, tmp_path):
    """PROBE_OUTBOX_DIR is the setting the reliability plan's rollout note gives a
    cluster ("a writable PROBE_OUTBOX_DIR on a large disk"), exported once for the
    whole job. It skipped the rank split, so every rank on every node appended
    under ONE `.append.lock`. On an NFS home that lock is cross-client, and the
    Linux NFS client polls a contended lock with backoff: in the two-node Slurm
    environment test each `log()` waited up to ~30 s (10 DDP steps in 5 minutes,
    agent/tests/environments/nfs_home). The explicit directory is the ROOT, like
    the default one: each rank queues in its own `rank-<N>/` under it."""
    root = tmp_path / "shared" / "outbox"
    monkeypatch.setenv("PROBE_OUTBOX_DIR", str(root))
    monkeypatch.setenv("SLURM_PROCID", "7")
    assert journal_mod.default_root() == root
    assert journal_mod.default_dir() == root / "rank-7"
    # A process with no rank (the login node's `probe outbox status`) still
    # finds that rank's queue from the root.
    Journal().append_http("POST", "/v1/runs/r-1/metrics", {"n": 1})
    monkeypatch.delenv("SLURM_PROCID")
    assert journal_mod.default_dir() == root
    assert root / "rank-7" in Journal.discover()


def test_a_single_process_run_keeps_the_historic_path(monkeypatch, tmp_path):
    """No suffix without a rank: the default path stays byte-identical, so
    nothing needs migrating for the overwhelmingly common case."""
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    assert journal_mod.default_dir() == tmp_path / "state" / "probe" / "outbox"


def test_local_rank_alone_is_qualified_by_host(monkeypatch, tmp_path):
    """LOCAL_RANK repeats per node, so on shared storage two nodes' rank 0
    would collide back into a single queue."""
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    monkeypatch.setenv("LOCAL_RANK", "0")
    import socket

    assert socket.gethostname().split(".")[0][:4] in journal_mod.default_dir().name


# -- async must never be on without something to deliver it --------------------


def _delivery_mechanism(client) -> str:
    """Which of the two drainers (parity F1/F2) this client actually has."""
    if client._drain_interval is not None:
        return "exporter"
    if client._auto_drain and client._default_transport:
        return "worker"
    return "none"


def _client(tmp_path, **kw):
    from probe.sdk.client import Client
    from probe.sdk.config import Settings

    kw.setdefault("settings", Settings(base_url="https://example.invalid", token="probe_pat_x"))
    kw.setdefault("journal", Journal(tmp_path / "outbox"))
    return Client(**kw)


def test_no_configuration_queues_without_a_drainer(tmp_path):
    """THE invariant. Async writes are gated on `async_writes`; delivery needs
    either the detached worker (default transport + auto_drain) or the
    in-process exporter (drain_interval). Nothing used to require that one of
    them exists, so three reachable configurations wrote to disk into a void —
    silently, because a queued write returns None exactly like a delivered one.

    Enumerated rather than spot-checked: the bug survived because each case
    looked fine on its own.
    """
    from probe.sdk.transport import Transport
    from probe.sdk.config import Settings

    settings = Settings(base_url="https://example.invalid", token="probe_pat_x")
    cases = [
        ("default", {}),
        ("explicit async", {"async_writes": True}),
        ("injected transport", {"transport": Transport(settings), "settings": settings}),
        (
            "injected transport + explicit async",
            {"transport": Transport(settings), "settings": settings, "async_writes": True},
        ),
        ("auto_drain off", {"auto_drain": False}),
        ("auto_drain off + interval", {"auto_drain": False, "drain_interval": 1.0}),
    ]
    for label, kw in cases:
        import warnings as _w

        with _w.catch_warnings():
            _w.simplefilter("ignore")
            client = _client(tmp_path, **kw)
        try:
            if client.async_writes and client._default_transport:
                # A default-transport client has no manual-drain story: nobody
                # is going to call flush() for a training loop. It MUST have a
                # background drainer, and never falls back to sync to get one.
                assert _delivery_mechanism(client) != "none", (
                    f"{label}: queues writes with no drainer"
                )
        finally:
            client.close()


def test_an_injected_transport_without_a_drainer_says_so(tmp_path):
    """A custom transport disqualifies the detached worker and does not
    activate the exporter, so nothing delivers in the BACKGROUND — but
    `flush()`/`finish()` still does, and draining by hand is exactly what the
    CLI barrier and the fake-transport tests do deliberately.

    So this warns rather than forcing an exporter thread: silence was the bug,
    not the configuration. Forcing one would start a background drain in every
    test using a fake transport and race their assertions.
    """
    from probe.sdk.transport import Transport
    from probe.sdk.config import Settings

    settings = Settings(base_url="https://example.invalid", token="probe_pat_x")
    with pytest.warns(UserWarning, match="no background drainer"):
        client = _client(
            tmp_path, settings=settings, transport=Transport(settings), async_writes=True
        )
    try:
        assert client.async_writes is True
    finally:
        client.close()


def test_auto_drain_off_keeps_async_and_uses_the_exporter(tmp_path):
    """auto_drain=False rules out the detached worker, not delivery: on a
    default transport the in-process exporter is still available.

    Taking it beats degrading to sync. Sync puts the network back on the
    training loop's critical path — the exact failure this change exists to
    remove — and would do it silently, on a flag whose meaning shifted
    underneath its users: before async became the default, auto_drain=False
    only meant "do not auto-drain the fail-open spool" and writes still went
    over the network.
    """
    client = _client(tmp_path, auto_drain=False)
    try:
        assert client.async_writes is True
        assert _delivery_mechanism(client) == "exporter"
    finally:
        client.close()


def test_asking_for_async_with_no_background_drainer_says_so(tmp_path):
    """Explicitly async AND explicitly no background drainer is a real
    configuration — writers that drain by hand use it, and so do tests that
    want a journal to inspect without a thread racing their assertions. It
    warns rather than refusing: the defect was never the shape, it was that a
    write into a queue nothing would drain looked identical to a delivered one.
    """
    with pytest.warns(UserWarning, match="no background drainer"):
        client = _client(tmp_path, auto_drain=False, async_writes=True)
    assert client.async_writes is True
    client.close()
