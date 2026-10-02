"""Plan 1.5: low disk, a bad HOME, rank dirs and Kubernetes never drop silently.

Live on 0.186.1: with under 2 GiB free and the network fine, 0 of 30 points
arrived and `finish()` said `completed`; a container with no HOME crashed
`Client()`; a read-only HOME or a filesystem without `flock` dropped every
write with a warning apiece; `probe outbox status` saw only the default
directory, never a distributed job's `rank-*` queues.
"""

from __future__ import annotations

import collections
import errno
import json
import os
import tempfile
from pathlib import Path

import httpx
import pytest

from probe._shared import oscompat
from probe.sdk import client as client_mod
from probe.sdk import errors
from probe.sdk import journal as journal_mod
from probe.sdk.client import Client
from probe.sdk.config import Settings
from probe.sdk.journal import Journal, drain
from probe.sdk.transport import Transport

from tests.conftest import make_client, open_run
from tests.test_outbox import seeded_run

_Usage = collections.namedtuple("_Usage", "total used free")
GIB = 1024**3


@pytest.fixture(autouse=True)
def _isolated(monkeypatch, tmp_path):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(tmp_path / "config" / "probe.json"))
    for var in (*journal_mod._GLOBAL_RANK_VARS, "LOCAL_RANK", "PROBE_OUTBOX_DIR",
                "PROBE_OUTBOX_MIN_FREE_BYTES", "KUBERNETES_SERVICE_HOST", "PROBE_ASYNC"):
        monkeypatch.delenv(var, raising=False)
    monkeypatch.setattr(journal_mod, "MIN_FREE_BYTES", None)  # scale with the volume
    monkeypatch.setattr(client_mod, "_FALLBACK_WARNED", set())
    monkeypatch.setattr(client_mod, "_K8S_NOTICE_GIVEN", False)
    monkeypatch.setattr(tempfile, "tempdir", str(tmp_path / "tmp"))
    monkeypatch.setattr(journal_mod, "_private_fallback", None, raising=False)
    (tmp_path / "tmp").mkdir()


def _disk(monkeypatch, *, free: int, total: int = 100 * GIB) -> None:
    monkeypatch.setattr(journal_mod.shutil, "disk_usage", lambda _p: _Usage(total, total - free, free))


def _metrics(client, run_id, step):
    client.write(
        "POST",
        f"/v1/runs/{run_id}/metrics",
        {"points": [{"key": "loss", "kind": "model", "value": float(step), "step_index": step}]},
    )


def _warnings(recwarn) -> list[str]:
    """The SDK's own notices (`safe_warn` emits them as warnings)."""
    return [
        str(w.message)
        for w in recwarn.list
        if str(w.message).startswith("probe:") and "custom transport" not in str(w.message)
    ]


# -- the floor scales with the volume -------------------------------------------


@pytest.mark.parametrize(
    ("total", "floor"),
    [(1000 * GIB, 2 * GIB), (10 * GIB, int(10 * GIB * 0.05)), (1 * GIB, 256 * 1024**2)],
    ids=["large", "medium", "small"],
)
def test_the_free_space_floor_scales_with_the_volume(monkeypatch, tmp_path, total, floor):
    """A fixed 2 GiB floor refused every write on a small pod volume. It is now
    5 % of the volume, between 256 MiB and 2 GiB."""
    _disk(monkeypatch, free=total, total=total)
    assert journal_mod.free_floor(tmp_path) == floor


def test_an_explicit_floor_still_wins(monkeypatch, tmp_path):
    monkeypatch.setattr(journal_mod, "MIN_FREE_BYTES", 12345)
    _disk(monkeypatch, free=1, total=1000 * GIB)
    assert journal_mod.free_floor(tmp_path) == 12345


# -- below the floor: send directly while the run has nothing queued ------------------


def test_below_the_floor_a_healthy_server_gets_every_write(app, tmp_path, monkeypatch):
    """30 logs with 1 MiB free and the network fine: 30 arrive, 0 dropped
    (0.186.1: 0 of 30 arrived). Each is sent directly because the run has
    nothing queued, and the count is reported on the run at finish()."""
    client = make_client(app, tmp_spool=tmp_path / "outbox", async_writes=True)
    run = open_run(client, experiment="lowdisk")
    _disk(monkeypatch, free=1024**2)
    for step in range(30):
        _metrics(client, run.id, step)

    assert len(app.metric_points_posted.get(run.id, [])) == 30
    assert client.dropped_writes == 0 and client.direct_sends == 30
    assert client.journal.pending() == []
    run.finish()
    summary = app.runs[run.id].get("summary") or {}
    assert summary.get("probe_finish", {}).get("direct_sends") == 30
    client.close()


def test_a_failing_direct_send_is_tried_once_then_not_for_a_minute(app, tmp_path, monkeypatch):
    """The circuit breaker: a failed direct send costs the training thread one
    attempt (bounded at 5 s), then none for 60 s -- the writes are dropped
    with a capture gap, as below the floor they always were."""
    client = make_client(app, tmp_spool=tmp_path / "outbox", async_writes=True)
    run = open_run(client, experiment="lowdisk")
    _disk(monkeypatch, free=1024**2)
    attempts = []

    def down(method, path, **kw):
        attempts.append(path)
        raise errors.TransportError("down")

    monkeypatch.setattr(client.transport, "request", down)
    clock = [1000.0]
    monkeypatch.setattr(client_mod.time, "monotonic", lambda: clock[0])
    for step in range(10):
        _metrics(client, run.id, step)
    assert len(attempts) == 1 and client.dropped_writes == 10
    clock[0] += 59
    _metrics(client, run.id, 10)
    assert len(attempts) == 1, "still inside the minute"
    clock[0] += 2
    _metrics(client, run.id, 11)
    assert len(attempts) == 2, "tried again after it"
    client.close()


def test_a_run_with_writes_queued_is_not_sent_around_them(app, tmp_path, monkeypatch):
    """First write wins per (series, step), so a direct write may not overtake
    a queued one of the same run (Codex, round 2). A run with nothing queued
    still goes direct."""
    client = make_client(app, tmp_spool=tmp_path / "outbox", async_writes=True)
    busy = open_run(client, experiment="lowdisk", name="busy")
    clear = open_run(client, experiment="lowdisk", name="clear")
    _metrics(client, busy.id, 0)  # queued while there was room
    assert len(client.journal.pending()) == 1
    monkeypatch.setattr(journal_mod, "_STATVFS_EVERY", 1)  # see the drop at once
    _disk(monkeypatch, free=1024**2)

    _metrics(client, busy.id, 1)
    _metrics(client, clear.id, 1)

    assert app.metric_points_posted.get(busy.id, []) == [], "busy's write waited its turn"
    assert len(app.metric_points_posted.get(clear.id, [])) == 1
    assert client.dropped_writes == 1 and client.direct_sends == 1
    client.close()


def test_a_full_disk_mid_append_is_sent_directly_too(app, tmp_path, monkeypatch):
    """ENOSPC from the append itself (the disk filled between samples)."""
    client = make_client(app, tmp_spool=tmp_path / "outbox", async_writes=True)
    run = open_run(client, experiment="lowdisk")

    def full(*a, **kw):
        raise OSError(errno.ENOSPC, "No space left on device")

    monkeypatch.setattr(client.journal, "append_http", full)
    _metrics(client, run.id, 0)
    assert len(app.metric_points_posted.get(run.id, [])) == 1
    assert client.dropped_writes == 0 and client.direct_sends == 1
    client.close()


def _bookkeeping_full(monkeypatch, journal) -> None:
    """The op file lands, then its bookkeeping (status.json) does not: a volume
    that is full but for the few KB a delivered op just freed. Seen on a real
    1 GiB tmpfs in the lane S soak rehearsal (0.195.0): the fake above, which
    fails the WHOLE append, cannot produce it."""

    def full(*a, **kw):
        raise OSError(errno.ENOSPC, "No space left on device")

    monkeypatch.setattr(journal, "_write_status_locked", full)


def _metric_ops(journal) -> list[dict]:
    return [
        op
        for op in (json.loads(p.read_text()) for p in sorted(journal.ops_dir.glob("*.json")))
        if op.get("path", "").endswith("/metrics")
    ]


def test_an_op_that_landed_is_queued_once_even_when_its_bookkeeping_cannot_be(tmp_path, monkeypatch):
    """0.195.0 raised ENOSPC for an op that was already on disk, then retried
    the append and wrote a SECOND op file for the same write. The op is queued
    (the drain rebuilds status.json, per `_append_locked`), so the append must
    say so, once."""
    journal = Journal(tmp_path / "outbox")
    journal.append_http("POST", "/v1/runs/r1/metrics", {"points": []}, run_ref="r1")
    _bookkeeping_full(monkeypatch, journal)

    op_id = journal.append_http("POST", "/v1/runs/r1/metrics", {"points": []}, run_ref="r1")

    ops = _metric_ops(journal)
    assert len(ops) == 2, "one op file per append, not a duplicate from a retry"
    assert ops[-1]["op_id"] == op_id


def test_a_write_whose_op_landed_on_a_full_disk_is_not_dropped(app, tmp_path, monkeypatch):
    """The Client side of the same disk: the write is queued, so it is not a
    drop -- 0.195.0 counted it dropped (while delivering it later), and the op
    it had in fact queued made the run's lane non-empty, so every later write
    of the run in the full window was dropped instead of sent directly (soak
    rehearsal: 118 of 119 writes over 120 s)."""
    client = make_client(app, tmp_spool=tmp_path / "outbox", async_writes=True)
    run = open_run(client, experiment="lowdisk")
    _bookkeeping_full(monkeypatch, client.journal)

    _metrics(client, run.id, 0)

    assert client.dropped_writes == 0
    assert len(_metric_ops(client.journal)) + len(app.metric_points_posted.get(run.id, [])) == 1
    client.close()


def test_a_landed_op_whose_status_write_failed_still_wakes_a_worker(tmp_path, monkeypatch):
    """The op landed but status.json could not be rewritten (a full disk), so
    it still says nothing is queued. 0.200.2's `maybe_spawn` read only that
    count and started no worker: the op stayed on disk, the run's lane stayed
    non-empty, and every later write of the window was dropped instead of sent
    directly (7-day soak, condensed run: 891 of 901 steps over a 15-min full
    window, every drop with the same one op queued)."""
    from probe.sdk import outbox_worker

    journal = Journal(tmp_path / "outbox")
    _bookkeeping_full(monkeypatch, journal)
    journal.append_http("POST", "/v1/runs/r1/metrics", {"points": []}, run_ref="r1")
    assert not (Journal.read_status(str(journal.dir), include_receipts=False) or {}).get("pending")
    assert len(_metric_ops(journal)) == 1
    spawned: list = []
    monkeypatch.setattr(outbox_worker.subprocess, "Popen", lambda argv, **kw: spawned.append(argv))

    assert outbox_worker.maybe_spawn(str(journal.dir)) is True
    assert spawned and spawned[0][1:3] == ["-m", "probe.sdk.outbox_worker"]


def test_a_worker_does_not_exit_past_an_op_its_status_count_missed(tmp_path, monkeypatch):
    """The live worker's exit guard read status.json alone: with the count left
    at zero by a full disk it exited `drained` while the landed op waited."""
    from probe.sdk import outbox_worker

    journal = Journal(tmp_path / "outbox")
    _bookkeeping_full(monkeypatch, journal)
    journal.append_http("POST", "/v1/runs/r1/metrics", {"points": []}, run_ref="r1")
    fresh = Journal.read_status(str(journal.dir), include_receipts=False) or {}
    assert not fresh.get("pending")

    assert outbox_worker._work_arrived(Journal(journal.dir), fresh) is True


def test_a_write_held_back_by_its_queued_run_wakes_the_drainer(app, tmp_path, monkeypatch):
    """Below the floor a write waits behind its run's queued ops -- and on a full
    disk it is then dropped without ever being queued, so no enqueue kicks the
    drainer. The hold itself must, or a stranded op is never delivered."""
    from probe.sdk import outbox_worker

    client = make_client(app, tmp_spool=tmp_path / "outbox", async_writes=True)
    run = open_run(client, experiment="lowdisk")
    _metrics(client, run.id, 0)  # queued while there was room
    monkeypatch.setattr(journal_mod, "_STATVFS_EVERY", 1)
    _disk(monkeypatch, free=1024**2)
    client._default_transport, client._auto_drain = True, True
    client._drainer_kicked_at = float("-inf")
    kicks: list = []
    monkeypatch.setattr(outbox_worker, "maybe_spawn", lambda d=None: kicks.append(d) or False)

    _metrics(client, run.id, 1)

    assert client.dropped_writes == 1
    assert kicks, "the held-back write woke the drainer"
    client.close()


def test_an_empty_queue_with_a_zero_count_still_spawns_nothing(tmp_path, monkeypatch):
    """The negative control: the extra look only finds an op that is there."""
    from probe.sdk import outbox_worker

    journal = Journal(tmp_path / "outbox")
    journal.append_http("POST", "/v1/runs/r1/metrics", {"points": []}, run_ref="r1")
    for path in journal.ops_dir.glob("*.json"):
        path.unlink()
    journal.write_status(pending=0)
    spawned: list = []
    monkeypatch.setattr(outbox_worker.subprocess, "Popen", lambda argv, **kw: spawned.append(argv))

    assert outbox_worker.maybe_spawn(str(journal.dir)) is False
    assert spawned == []


def test_a_refused_ops_queue_still_spawns_nothing_despite_corrupt_bookkeeping(
    app, tmp_path, monkeypatch
):
    """The exit guard's new look in ``ops/`` (`_has_queued_op`) must not turn an
    op the drain already tried and set aside -- refused for its credential
    (#2041) -- into "work arrived". Once started, a REAL worker backs a
    permanently refused credential off forever (`LaneBackoff` never reaches its
    STALLED exit for it -- confirmed empirically with a real subprocess in
    review of this fix; that loop is untouched by this diff and identical on
    main). The only thing this diff may change is whether `maybe_spawn` STARTS
    that worker in the first place when status.json's `pending`/`held` are
    corrupted to 0 (this op's own full-disk bookkeeping failure) while the
    op -- already attempted once, per its own `attempts` field -- sits in
    `ops/`. It must not, exactly as main does not (main trusts the corrupted
    `pending: 0` outright, for the wrong reason but the same outcome)."""
    from tests.served_fake_app import serve

    from probe.sdk import outbox_worker

    token = "probe_pat_refused_0123456789abcdef"
    run_id = seeded_run(app, tmp_path)
    with serve(app) as url:
        monkeypatch.setenv("PROBE_TOKEN", token)
        monkeypatch.setenv("PROBE_BASE_URL", url)
        app.rejected_tokens.add(token)  # refused from the start: no direct send can succeed
        client = Client(spool_dir=tmp_path / "outbox", async_writes=True, auto_drain=False)
        try:
            client.write(
                "POST",
                f"/v1/runs/{run_id}/metrics",
                {"points": [{"key": "loss", "kind": "model", "value": 1.0, "step_index": 1}]},
            )
        finally:
            client.close()
        root = Journal(tmp_path / "outbox")
        report = drain(root)
        assert report.credential_refused == 1

        # A refused credential's op sits in ITS OWN queue (#2035), not the
        # root's -- `maybe_spawn` finds and probes it too (see
        # `_own_credential_queue`, called from the root's own `maybe_spawn`).
        cred_dir = root.dir / journal_mod.CREDENTIAL_NAMESPACE / journal_mod.credential_fingerprint(
            token, None
        )
        cred_journal = Journal(cred_dir)
        ((_op_path, op),) = cred_journal.pending()
        assert op.get("attempts", 0) >= 1, "the one real drain pass must have recorded its attempt"

        # The exact corruption this fix is about (a full-disk bookkeeping
        # write that never landed), worst-cased: `held` lost along with
        # `pending`, so neither cached field alone tells `maybe_spawn` this
        # op is already accounted for.
        status_path = cred_dir / "status.json"
        status = json.loads(status_path.read_text())
        status["pending"] = 0
        status["held"] = 0
        status_path.write_text(json.dumps(status))

        spawned: list = []
        monkeypatch.setattr(
            outbox_worker.subprocess, "Popen", lambda argv, **kw: spawned.append(argv)
        )

        assert outbox_worker.maybe_spawn(str(root.dir)) is False, (
            "an already-attempted, undeliverable-by-design op must not be read as new work"
        )
        assert spawned == []
        assert len(cred_journal.pending()) == 1, "the refused op must still be there"


# -- a HOME the queue cannot use -------------------------------------------------------


def _default_client() -> Client:
    settings = Settings(base_url="http://test", token="ros_pat_deadbeef", ingest_token=None,
                        hmac_secret=None)
    transport = Transport(
        settings, client=httpx.Client(base_url="http://test", transport=httpx.MockTransport(
            lambda request: httpx.Response(200, json={})
        ))
    )
    return Client(settings=settings, transport=transport, async_writes=True, auto_drain=False)


@pytest.mark.skipif(os.name != "posix", reason="POSIX permission bits; Windows uses ACLs")
def test_a_read_only_home_falls_back_with_one_warning(tmp_path, monkeypatch, recwarn):
    home = tmp_path / "home"
    home.mkdir()
    monkeypatch.setenv("HOME", str(home))
    monkeypatch.delenv("XDG_STATE_HOME", raising=False)
    home.chmod(0o500)
    try:
        client = _default_client()
        for step in range(20):
            client.write("POST", "/v1/runs/r-1/metrics", {"points": [{"i": step}]})
        fallback = journal_mod.fallback_dir()
        # The fallback outbox; a token passed in code queues in its own
        # credential queue inside it (#2035).
        assert client.journal.outbox_root == fallback
        assert sum(len(q.pending()) for q in Journal(fallback).namespaces()) == 20
        assert client.dropped_writes == 0
        warned = _warnings(recwarn)
        assert len(warned) == 1 and "does NOT survive" in warned[0], warned
        client.close()
    finally:
        home.chmod(0o700)


def test_no_home_at_all_does_not_crash_the_client(tmp_path, monkeypatch, recwarn):
    """A container running an arbitrary uid has no HOME and no passwd entry:
    `Path.home()` raises, and it crashed `Client()`. (HOME itself stays set:
    the suite's isolation of other tools' config reads it.)"""
    monkeypatch.delenv("XDG_STATE_HOME", raising=False)

    def no_home():
        raise RuntimeError("Could not determine home directory.")

    with monkeypatch.context() as patch:
        patch.setattr(Path, "home", staticmethod(no_home))
        client = _default_client()
        client.write("POST", "/v1/runs/r-1/metrics", {"points": [{"i": 0}]})
    assert client.journal.outbox_root == journal_mod.fallback_dir()
    assert len(client.journal.pending()) == 1
    warned = _warnings(recwarn)
    assert len(warned) == 1 and "no home directory" in warned[0], warned
    client.close()


def test_a_busy_queue_is_not_mistaken_for_an_unusable_one(tmp_path, monkeypatch):
    """The control (Codex, round 2): another process holding the queue's
    append lock is normal and must never redirect a healthy queue."""
    journal = Journal(tmp_path / "outbox")
    journal._ensure()
    with open(journal.append_lock, "a+") as held:
        oscompat.flock(held.fileno(), oscompat.LOCK_EX)
        assert journal.usable() is None


def test_a_filesystem_without_locks_is_unusable(tmp_path, monkeypatch):
    journal = Journal(tmp_path / "outbox")

    def no_locks(fd, op):
        raise OSError(errno.ENOSYS, "Function not implemented")

    monkeypatch.setattr(oscompat, "flock", no_locks)
    assert "file locks" in (journal.usable() or "")


# -- Kubernetes -------------------------------------------------------------------------


def test_on_kubernetes_the_default_outbox_says_so_once(tmp_path, monkeypatch, recwarn):
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    monkeypatch.setenv("KUBERNETES_SERVICE_HOST", "10.0.0.1")
    monkeypatch.setattr(client_mod, "_on_container_root_disk", lambda path: True)
    _default_client().close()
    _default_client().close()
    warned = _warnings(recwarn)
    assert len(warned) == 1 and "PROBE_OUTBOX_DIR" in warned[0], warned


def test_on_kubernetes_a_configured_outbox_is_quiet(tmp_path, monkeypatch, recwarn):
    monkeypatch.setenv("KUBERNETES_SERVICE_HOST", "10.0.0.1")
    monkeypatch.setenv("PROBE_OUTBOX_DIR", str(tmp_path / "pv" / "outbox"))
    _default_client().close()
    assert _warnings(recwarn) == []


def test_a_waiting_queue_is_kicked_when_a_client_starts(tmp_path, monkeypatch):
    """A pod recreated on the same persistent volume: its backlog starts
    draining when the new process starts, not at its first write."""
    from probe.sdk import outbox_worker

    monkeypatch.setenv("PROBE_OUTBOX_DIR", str(tmp_path / "pv" / "outbox"))
    Journal().append_http("POST", "/v1/runs/r-1/metrics", {"points": [{"i": 0}]})
    kicked = []
    monkeypatch.setattr(outbox_worker, "maybe_spawn", lambda d=None: kicked.append(d) or False)
    settings = Settings(base_url="http://test", token="ros_pat_deadbeef", ingest_token=None,
                        hmac_secret=None)
    Client(settings=settings, async_writes=True).close()
    assert kicked == [str(tmp_path / "pv" / "outbox")]


# -- every queue on the machine ---------------------------------------------------------


def test_outbox_status_shows_every_rank_dir(tmp_path, monkeypatch, capsys):
    from probe import cli

    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    root = journal_mod.default_root()
    for rank, count in (("rank-0", 2), ("rank-1", 3)):
        journal = Journal(root / rank)
        for n in range(count):
            journal.append_http("POST", "/v1/runs/r-1/metrics", {"points": [{"i": n}]})

    assert cli.main(["outbox", "status"]) == 2
    summary = json.loads(capsys.readouterr().out)
    dirs = {Path(entry["dir"]).name: entry["pending"] for entry in summary["dirs"]}
    assert dirs.get("rank-0") == 2 and dirs.get("rank-1") == 3
    assert summary["total"]["pending"] == 5


def test_an_offline_queue_is_never_found_by_drain_all(tmp_path, monkeypatch):
    """Plan 2.12 (lane G) queues an offline run at `<root>/offline/`, beside the
    `rank-*` dirs. Only `probe sync` may deliver it: discovery (and so `probe
    outbox status`, `drain --all`, `retry --all`) sees rank dirs only."""
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    root = journal_mod.default_root()
    Journal(root / "rank-0").append_http("POST", "/v1/runs/r-1/metrics", {"points": []})
    Journal(root / "offline" / "local-1").append_http("POST", "/v1/runs/r-2/metrics", {"points": []})
    Journal(root / "offline").append_http("POST", "/v1/runs/r-3/metrics", {"points": []})

    found = {path.relative_to(root).as_posix() for path in Journal.discover()}
    assert found == {"rank-0"}, found


def test_a_dir_holding_only_credential_queues_is_found(tmp_path, monkeypatch):
    """#2041 queues a stamped write at `<dir>/credential-v1/<fingerprint>/`,
    so a directory whose every write was stamped holds no `ops/` of its own:
    discovery must still list it (its `namespaces()` then reach the queues)."""
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    root = journal_mod.default_root()
    for where in (root, root / "rank-2"):
        Journal(where / journal_mod.CREDENTIAL_NAMESPACE / "fp-1").append_http(
            "POST", "/v1/runs/r-1/metrics", {"points": []}
        )
    assert not (root / "ops").exists()

    found = {path.relative_to(root).as_posix() for path in Journal.discover()}
    assert found == {".", "rank-2"}, found


def test_drain_all_carries_every_report_field():
    """`drain --all` rebuilt its report from six fields, so any other one --
    #2041's credential_held and held_reasons -- never reached the output. Every
    field folds now; one journal's report is printed as it came."""
    from dataclasses import dataclass, field

    from probe.cli.main import _fold_drain_reports
    from probe.sdk.journal import DrainReport, LaneStall

    @dataclass
    class WithHolds(DrainReport):
        credential_held: int = 0
        held_reasons: list = field(default_factory=list)

    only = WithHolds(credential_held=1)
    assert _fold_drain_reports([only]) is only

    first = WithHolds(
        delivered=1,
        credential_held=2,
        held_reasons=["another job's PROBE_TOKEN"],
        auth_blocked=True,
        auth_status=401,
        auth_context={"name": "a"},
        errors=["e1"],
        stalled_runs={"r-1": LaneStall("busy")},
    )
    second = WithHolds(
        delivered=2,
        dead_lettered=1,
        credential_held=3,
        held_reasons=["another job's PROBE_TOKEN", "refused at 12:00"],
        auth_status=403,
        auth_context={"name": "b", "base_url": "https://b"},
        errors=["e2"],
        queued_runs={"r-2"},
        progressed_runs={"r-2"},
    )

    folded = _fold_drain_reports([first, second])

    assert (folded.delivered, folded.dead_lettered, folded.credential_held) == (3, 1, 5)
    assert folded.held_reasons == ["another job's PROBE_TOKEN", "refused at 12:00"]
    assert folded.auth_blocked and folded.auth_status == 401
    assert folded.auth_context == {"name": "a"} == first.auth_context, "one refusal's, unmixed"
    assert folded.errors == ["e1", "e2"] and set(folded.stalled_runs) == {"r-1"}
    assert folded.queued_runs == {"r-2"} and folded.progressed_runs == {"r-2"}
    assert first.delivered == 1, "the parts are not mutated"


def test_a_queue_only_sync_drains_is_never_sent_around(app, tmp_path, monkeypatch):
    """An offline client (`_drains_by_hand`, plan 2.12) must not touch the
    network, even below the free-space floor."""
    client = make_client(app, tmp_spool=tmp_path / "outbox", async_writes=True)
    run = open_run(client, experiment="lowdisk")
    client._drains_by_hand = True
    _disk(monkeypatch, free=1024**2)
    posted_before = len(app.metric_points_posted.get(run.id, []))
    _metrics(client, run.id, 0)
    assert len(app.metric_points_posted.get(run.id, [])) == posted_before
    assert client.direct_sends == 0
    client.close()


# -- review of #2054: the $TMPDIR fallback must be this user's alone --------------


def _hostile_fallback(tmp_path, *, mode=0o777, symlink=False):
    """What another user can leave in a shared /tmp: the fallback's name, with
    one op of theirs queued in it."""
    name = journal_mod.fallback_root()
    if symlink:
        target = tmp_path / "elsewhere"
        target.mkdir(mode=0o700)
        name.symlink_to(target)
        where = target
    else:
        name.mkdir()
        name.chmod(mode)
        where = name
    planted = Journal(where / "q")  # built off to the side, then moved in
    planted.append_http("POST", "/v1/runs/theirs/metrics", {"points": [{"i": 1}]})
    for part in ("ops", "status.json"):
        os.replace(where / "q" / part, where / part)
    return name


@pytest.mark.parametrize("shape", ["world-writable", "symlink", "group-writable"])
@pytest.mark.skipif(os.name != "posix", reason="POSIX permission bits; Windows uses ACLs")
def test_a_planted_fallback_is_never_drained(tmp_path, monkeypatch, shape):
    """P1 (review of #2054): `discover()` always listed $TMPDIR/probe-outbox-<uid>,
    and `probe outbox drain --all` sent a planted op with the caller's bearer
    token. A fallback that is not a private, real directory of this user is
    skipped, and never used to queue."""
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    planted = _hostile_fallback(
        tmp_path, mode=0o770 if shape == "group-writable" else 0o777, symlink=shape == "symlink"
    )
    assert planted not in Journal.discover()
    assert journal_mod.fallback_dir() != planted
    assert journal_mod.trusted_dir(journal_mod.fallback_dir())


@pytest.mark.skipif(os.name != "posix", reason="POSIX permission bits; Windows uses ACLs")
def test_a_fallback_owned_by_someone_else_is_skipped(tmp_path, monkeypatch):
    """The third hostile shape, by owner: a fake uid makes the real dir read
    as another user's."""
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    name = journal_mod.fallback_root()
    Journal(name).append_http("POST", "/v1/runs/r-1/metrics", {"points": []})
    name.chmod(0o700)
    assert name in Journal.discover(), "control: our own private fallback is listed"
    real_uid = os.getuid()
    monkeypatch.setattr(journal_mod.os, "getuid", lambda: real_uid + 1)
    assert not journal_mod.trusted_dir(name)


@pytest.mark.skipif(os.name != "posix", reason="POSIX permission bits; Windows uses ACLs")
def test_drain_all_does_not_send_a_planted_op(tmp_path, monkeypatch, capsys):
    from probe import cli

    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    _hostile_fallback(tmp_path)
    sent = []
    monkeypatch.setattr(
        journal_mod, "drain", lambda j, **kw: sent.append(str(j.dir)) or journal_mod.DrainReport()
    )
    cli.main(["outbox", "drain", "--all"])
    assert not any("probe-outbox" in d for d in sent), sent


@pytest.mark.skipif(not hasattr(os, "O_NOFOLLOW"), reason="no O_NOFOLLOW on Windows (a symlink there needs privilege to plant)")
def test_a_symlinked_drainer_log_starts_no_worker(tmp_path, monkeypatch):
    from probe.sdk import outbox_worker

    journal = Journal(tmp_path / "outbox")
    journal.append_http("POST", "/v1/runs/r-1/metrics", {"points": []})
    (tmp_path / "loot").write_text("")
    (journal.dir / "drainer.log").symlink_to(tmp_path / "loot")
    spawned = []
    monkeypatch.setattr(outbox_worker.subprocess, "Popen", lambda *a, **k: spawned.append(a))
    assert outbox_worker.maybe_spawn(str(journal.dir)) is False
    assert spawned == []


def test_a_small_volume_floor_is_at_most_a_quarter_of_it(monkeypatch, tmp_path):
    _disk(monkeypatch, free=50 * 1024**2, total=100 * 1024**2)
    assert journal_mod.free_floor(tmp_path) == 25 * 1024**2


# -- review of #2054: the direct-send breaker ----------------------------------------


def test_a_refused_direct_send_does_not_close_the_breaker(app, tmp_path, monkeypatch):
    """P3: any failed direct send opened the breaker, so one 422 stopped direct
    sends for every run for a minute. Only a server-wide failure opens it."""
    client = make_client(app, tmp_spool=tmp_path / "outbox", async_writes=True)
    run = open_run(client, experiment="lowdisk")
    _disk(monkeypatch, free=1024**2)
    real = client.transport.request
    calls = []

    def refuse_one(method, path, **kw):
        calls.append(path)
        if len(calls) == 1:
            raise errors.ValidationError("bad point", status=422)
        return real(method, path, **kw)

    monkeypatch.setattr(client.transport, "request", refuse_one)
    _metrics(client, run.id, 0)  # refused: dropped, the breaker stays shut
    _metrics(client, run.id, 1)
    assert len(calls) == 2 and client.direct_sends == 1
    client.close()


def test_a_deep_queue_is_not_scanned_on_the_training_thread(app, tmp_path, monkeypatch):
    """P3: proving a run clear parsed every queued op file the first time; over
    `DIRECT_SEND_MAX_QUEUED` queued ops no direct send is tried at all."""
    client = make_client(app, tmp_spool=tmp_path / "outbox", async_writes=True)
    run = open_run(client, experiment="lowdisk")
    monkeypatch.setattr(client, "DIRECT_SEND_MAX_QUEUED", 3)
    for n in range(4):
        client.journal.append_http("POST", "/v1/runs/other/metrics", {"points": [{"i": n}]})
    _disk(monkeypatch, free=1024**2)
    parsed = []
    real_scan = journal_mod.RunOps._scan
    monkeypatch.setattr(
        journal_mod.RunOps, "_scan", lambda self, d: parsed.append(d) or real_scan(self, d)
    )
    _metrics(client, run.id, 0)
    assert parsed == [] and client.direct_sends == 0
    client.close()


def test_the_kubernetes_notice_is_quiet_for_a_home_on_its_own_volume(
    tmp_path, monkeypatch, recwarn
):
    """P3: a HOME that is a mounted volume (JupyterHub's per-user PV) is not the
    container's disk; and an explicit spool_dir is the caller's choice."""
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    monkeypatch.setenv("KUBERNETES_SERVICE_HOST", "10.0.0.1")
    monkeypatch.setattr(client_mod, "_on_container_root_disk", lambda path: False)
    _default_client().close()
    assert _warnings(recwarn) == []
    monkeypatch.setattr(client_mod, "_on_container_root_disk", lambda path: True)
    settings = Settings(base_url="http://test", token="ros_pat_deadbeef", ingest_token=None,
                        hmac_secret=None)
    transport = Transport(settings, client=httpx.Client(base_url="http://test"))
    Client(settings=settings, transport=transport, spool_dir=str(tmp_path / "mine"),
           async_writes=True, auto_drain=False).close()
    assert _warnings(recwarn) == [], "an explicit spool_dir gets no notice"
