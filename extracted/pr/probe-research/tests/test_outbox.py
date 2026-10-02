"""The async outbox: snapshot_file, journal, classifier, drain, worker, CLI.

Covers the eng-review test matrix (2026-07-29): enqueue paths, FIFO drain with
the phase-aware failure policy (permanent -> DLQ + continue; transient ->
stop-and-wait; auth -> halt with items untouched; 409-with-existing_id ->
idempotent success), run-scoped barriers, legacy spool import, and the three
regression guards (sync path unchanged, transient still stops, flush ≡ drain).

Fixtures set BOTH PROBE_CONFIG_PATH and XDG_CONFIG_HOME (recorded pitfall:
the tap and the SDK resolve the config differently; setting only one lets a
test write the developer's real config).
"""

from __future__ import annotations

import json
import os
import stat

import pytest

from probe.sdk import errors
from probe.sdk.durable import snapshot_file
from probe.sdk.journal import Journal, classify, drain, run_ref_for_path
from probe.sdk.spool import Spool

from tests.conftest import make_client


@pytest.fixture(autouse=True)
def _isolated_config(monkeypatch, tmp_path):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(tmp_path / "config" / "probe.json"))
    monkeypatch.delenv("PROBE_TOKEN", raising=False)
    monkeypatch.delenv("PROBE_ASYNC", raising=False)


def journal_at(tmp_path, **kwargs) -> Journal:
    return Journal(tmp_path / "outbox", **kwargs)


# -- snapshot_file -----------------------------------------------------------


def test_snapshot_is_immutable_against_source_mutation(tmp_path):
    source = tmp_path / "ckpt.bin"
    source.write_bytes(b"epoch-1 weights")
    dst = tmp_path / "snap.bin"
    snapshot_file(source, dst)
    source.write_bytes(b"epoch-2 weights overwrite")
    assert dst.read_bytes() == b"epoch-1 weights"
    if os.name == "posix":  # Windows has no permission bits (ACLs)
        assert stat.S_IMODE(dst.stat().st_mode) == 0o600


def test_snapshot_missing_source_raises_and_leaves_no_debris(tmp_path):
    with pytest.raises(FileNotFoundError):
        snapshot_file(tmp_path / "nope.bin", tmp_path / "snap.bin")
    leftovers = [p for p in tmp_path.iterdir()]
    assert leftovers == []


# -- classifier --------------------------------------------------------------


@pytest.mark.parametrize(
    ("exc", "verdict"),
    [
        (errors.TransportError("net down"), "transient"),
        (errors.ServerError("boom", status=503), "transient"),
        # 501 is the one 5xx that means "never", not "not yet": a deployment
        # without artifact storage answers it, and reading that as retryable
        # parked the whole FIFO queue on an op no wait could satisfy.
        (errors.ServerError("not built here", status=501), "permanent"),
        (errors.RosError("slow down", status=429), "transient"),
        (errors.RosError("timeout", status=408), "transient"),
        (errors.ValidationError("bad payload", status=422), "permanent"),
        (errors.NotFoundError("gone", status=404), "permanent"),
        (errors.AuthError("expired", status=401), "auth"),
        (errors.ScopeError("forbidden", status=403), "auth"),
        # "auth" is a promise that logging in fixes it. An op pinned to an
        # endpoint no credential here can ever satisfy -- a test server on a
        # port that died with the test -- breaks that promise, and parking on
        # it stops every op behind it, including the ones bound for the
        # endpoint that IS logged in.
        (errors.UnroutableEndpointError("dead test server"), "permanent"),
        (errors.ConflictError("dup", detail={"existing_id": "abc"}), "idempotent"),
        (errors.ConflictError("lifecycle", detail="run is deleted"), "permanent"),
        (RuntimeError("our own bug"), "transient"),
    ],
)
def test_classify(exc, verdict):
    assert classify(exc) == verdict


def test_run_ref_extraction():
    assert run_ref_for_path("/v1/runs/r-1/metrics") == "r-1"
    assert run_ref_for_path("/v1/runs/r-1") == "r-1"
    assert run_ref_for_path("/v1/experiments/e-1/artifacts") is None


# -- journal mechanics -------------------------------------------------------


def test_append_orders_ops_and_hardens_permissions(tmp_path):
    journal = journal_at(tmp_path, context={"name": "ctx", "base_url": "http://test"})
    first = journal.append_http("POST", "/v1/runs/r-1/metrics", {"n": 1})
    second = journal.append_http("POST", "/v1/runs/r-1/metrics", {"n": 2})
    ops = [op for _, op in journal.pending()]
    assert [op["op_id"] for op in ops] == [first, second]
    assert ops[0]["run_ref"] == "r-1"
    assert ops[0]["context"] == {"name": "ctx", "base_url": "http://test"}
    if os.name == "posix":  # Windows has no permission bits (ACLs)
        assert stat.S_IMODE(journal.ops_dir.stat().st_mode) == 0o700
        path, _ = journal.pending()[0]
        assert stat.S_IMODE(path.stat().st_mode) == 0o600
    status = Journal.read_status(journal.dir)
    assert status["pending"] == 2 and status["failed"] == 0


def test_journal_never_stores_credentials(tmp_path, app):
    client = make_client(app, tmp_spool=tmp_path / "outbox", async_writes=True)
    client.write("POST", "/v1/runs/r-1/metrics", {"points": []})
    everything = "".join(p.read_text() for p in (tmp_path / "outbox").rglob("*") if p.is_file())
    assert "ros_pat_" not in everything and "ros_ing_" not in everything


def test_import_spool_folds_legacy_records_in_order(tmp_path):
    spool = Spool(tmp_path / "legacy")
    spool.append("POST", "/v1/runs/r-1/metrics", {"n": 1})
    spool.append("POST", "/v1/runs/r-1/metrics", {"n": 2})
    journal = journal_at(tmp_path)
    imported = journal.import_spool(spool)
    assert imported == 2
    assert [op["body"]["n"] for _, op in journal.pending()] == [1, 2]
    assert not spool.file.exists() and not spool.inflight_file.exists()


def test_retry_failed_requeues_dead_letters(tmp_path):
    journal = journal_at(tmp_path)
    op_id = journal.append_http("POST", "/v1/nope", {})
    path, op = journal.pending()[0]
    (journal.failed_dir).mkdir(parents=True, exist_ok=True)
    os.replace(path, journal.failed_dir / path.name)
    assert journal.pending() == []
    assert journal.retry_failed(op_id) == 1
    assert [o["op_id"] for _, o in journal.pending()] == [op_id]


def test_gc_blobs_keeps_referenced_bytes(tmp_path):
    journal = journal_at(tmp_path)
    src = tmp_path / "f.bin"
    src.write_bytes(b"bytes")
    queued = journal.append_upload(
        anchor="run",
        anchor_id="r-1",
        name="f.bin",
        src_path=str(src),
        run_ref="r-1",
        inline_hash=True,
    )
    orphan = journal.blobs_dir / ("b" * 64)
    orphan.write_bytes(b"orphan")
    assert journal.gc_blobs() == 1
    assert (journal.blobs_dir / queued["blob"]).exists()
    assert not orphan.exists()


# -- drain -------------------------------------------------------------------


def drain_with(app, journal, **kwargs):
    client = make_client(app)
    try:
        return drain(journal, client_factory=lambda ctx: client, **kwargs)
    finally:
        client.close()


def seeded_run(app, tmp_path):
    from tests.conftest import open_run

    client = make_client(app)
    run = open_run(client, experiment="e", name="r")
    client.close()
    return run.id


def test_drain_delivers_http_ops_in_order(app, tmp_path):
    run_id = seeded_run(app, tmp_path)
    journal = journal_at(tmp_path)
    for n in (1, 2, 3):
        journal.append_http(
            "POST",
            f"/v1/runs/{run_id}/metrics",
            {"points": [{"key": "loss", "kind": "model", "value": float(n), "step_index": n}]},
        )
    report = drain_with(app, journal)
    assert report.delivered == 3 and report.clean
    steps = [p["step_index"] for p in app.metric_points_posted[run_id]]
    assert steps == [1, 2, 3]
    assert journal.pending() == []


def test_permanent_rejection_dead_letters_and_queue_flows(app, tmp_path):
    run_id = seeded_run(app, tmp_path)
    journal = journal_at(tmp_path)
    journal.append_http("POST", "/v1/runs/poisoned/badroute", {})
    journal.append_http(
        "POST",
        f"/v1/runs/{run_id}/metrics",
        {"points": [{"key": "loss", "kind": "model", "value": 1.0, "step_index": 1}]},
    )
    report = drain_with(app, journal)
    assert report.dead_lettered == 1
    assert report.delivered == 1, "the op behind the poison pill must deliver"
    ((failed_path, failed_op),) = journal.failed()
    assert failed_op["attempts"] == 1
    assert "NotFoundError" in failed_op["last_error"]


def test_transient_failure_stops_in_place(app, tmp_path):
    """REGRESSION guard: a 503 must stop the ordered replay, exactly like the
    old spool's stop-on-first-failure, and must not dead-letter anything."""
    run_id = seeded_run(app, tmp_path)
    journal = journal_at(tmp_path)
    journal.append_http(
        "POST",
        f"/v1/runs/{run_id}/metrics",
        {"points": [{"key": "a", "kind": "model", "value": 1.0, "step_index": 1}]},
    )
    journal.append_http(
        "POST",
        f"/v1/runs/{run_id}/metrics",
        {"points": [{"key": "b", "kind": "model", "value": 2.0, "step_index": 2}]},
    )
    app.fail_next_metrics = True  # one 503, then healthy
    report = drain_with(app, journal)
    assert report.stopped_transient and report.delivered == 0
    assert report.remaining == 2 and journal.failed() == []
    report = drain_with(app, journal)
    assert report.delivered == 2 and report.clean


def _upload_op(journal, tmp_path, *, run_id="r-1"):
    src = tmp_path / "ckpt.bin"
    src.write_bytes(b"weights")
    return journal.append_upload(
        anchor="run",
        anchor_id=run_id,
        name="checkpoints/ckpt.bin",
        src_path=str(src),
        run_ref=run_id,
        inline_hash=True,
    )


class _StorageLessClient:
    """A server with no artifact storage: uploads are refused permanently, and
    every other write lands. `calls` records the fallback POSTs."""

    def __init__(self, status=501):
        self.status = status
        self.calls = []
        client = self

        class _T:
            def request(self, method, path, json_body=None, **kw):
                client.calls.append((method, path, json_body))
                return {}

        self.transport = _T()

    def upload_fingerprinted(self, *a, **k):
        raise errors.ServerError("artifact storage is not configured", status=self.status)

    def close(self):
        pass


def test_a_refused_upload_does_not_strand_the_writes_behind_it(tmp_path):
    """THE WEDGE. The queue is strict FIFO and stops at the first failure, so an
    upload that can never succeed used to park every later write forever -- 452
    metric and span points starved behind five checkpoints in production's own
    simulation, and `Run.finish` then refused to close the run at all.

    A permanent refusal must dead-letter and let the queue move."""
    journal = journal_at(tmp_path)
    _upload_op(journal, tmp_path)
    journal.append_http("POST", "/v1/runs/r-1/metrics", {"points": []})
    journal.append_http("POST", "/v1/runs/r-1/spans", {"spans": []})

    client = _StorageLessClient()
    report = drain(journal, client_factory=lambda ctx: client)

    assert report.dead_lettered == 1, "the refused upload should not be retried forever"
    assert report.delivered == 2, "the writes queued behind it must still land"
    assert journal.pending() == []


def test_a_recovered_upload_stops_holding_the_run_open(tmp_path):
    """The synchronous upload path degrades to a reference artifact and leaves no
    failure state; a queued one that reached the same end must not be the reason
    a run cannot close. The dead letter stays as the audit trail -- it just
    stops counting as blocking (`Run._queued_ops` reads `blocking`)."""
    journal = journal_at(tmp_path)
    _upload_op(journal, tmp_path)

    client = _StorageLessClient()
    drain(journal, client_factory=lambda ctx: client)

    posted = [c for c in client.calls if c[1] == "/v1/runs/r-1/artifacts"]
    assert posted, "the file's only record is the reference row; it must be written"
    assert posted[0][2]["is_reference"] is True
    assert posted[0][2]["meta"]["upload"] == "failed"

    failed = [op for _, op in journal.failed()]
    assert len(failed) == 1
    assert failed[0]["blocking"] is False


def test_an_unrecovered_upload_keeps_blocking(tmp_path):
    """The inverse, and the reason the fallback reports success: when the
    reference row could NOT be written the file has no record anywhere, which is
    a real loss and must keep holding the run open."""
    journal = journal_at(tmp_path)
    _upload_op(journal, tmp_path)

    class _NoFallback(_StorageLessClient):
        def __init__(self):
            super().__init__()
            outer = self

            class _T:
                def request(self, *a, **k):
                    raise errors.ServerError("down too", status=500)

            outer.transport = _T()

    drain(journal, client_factory=lambda ctx: _NoFallback())
    failed = [op for _, op in journal.failed()]
    assert len(failed) == 1
    assert failed[0].get("blocking", True) is True


def test_transient_failures_give_up_before_they_wedge_the_queue(tmp_path, monkeypatch):
    """A blip parks the queue, which is right. Parking FOREVER is not: past the
    budget the op takes the permanent path so the writes behind it can move.

    The budget is WALL-CLOCK time since the op first failed (plan 0.6) AND a
    floor of attempts: 60 fast failures inside the day park, one failure after
    it dead-letters (60 >= 50)."""
    from probe.sdk import journal as journal_module

    journal = journal_at(tmp_path)
    _upload_op(journal, tmp_path)
    journal.append_http("POST", "/v1/runs/r-1/metrics", {"points": []})
    client = _StorageLessClient(status=503)  # transient, and permanently so

    clock = {"now": 1_000_000.0}
    monkeypatch.setattr(journal_module.time, "time", lambda: clock["now"])
    for _ in range(60):  # more than the old 50-attempt cap, in no time at all
        drain(journal, client_factory=lambda ctx: client)
    (head,) = [op for _, op in journal.pending() if op["kind"] == "upload"]
    assert head["attempts"] == 60 and head["first_failed_at"] == 1_000_000.0
    assert journal.failed() == [], "polling fast must not spend the budget"

    clock["now"] += journal_module.TRANSIENT_BUDGET_SECONDS  # a day later
    drain(journal, client_factory=lambda ctx: client)

    assert journal.pending() == [], "the queue must drain once patience runs out"
    assert len(journal.failed()) == 1


def test_the_transient_budget_restarts_on_retry(tmp_path, monkeypatch):
    """`probe outbox retry` is a human asking for another try: the op's
    failure clock restarts, or the budget would dead-letter it again on its
    first failure."""
    from probe.sdk import journal as journal_module

    monkeypatch.setenv("PROBE_OUTBOX_TRANSIENT_BUDGET_SEC", "0")
    monkeypatch.setattr(journal_module, "MIN_TRANSIENT_ATTEMPTS", 1)
    journal = journal_at(tmp_path)
    journal.append_http("POST", "/v1/runs/r-1/metrics", {"points": []})

    class _Down:
        class transport:  # noqa: N801 -- the shape drain uses
            @staticmethod
            def request(*a, **k):
                raise errors.ServerError("down", status=503)

        def close(self):
            pass

    client = _Down()
    drain(journal, client_factory=lambda ctx: client)
    (dead,) = [op for _, op in journal.failed()]
    assert "first_failed_at" in dead

    assert journal.retry_failed() == 1
    (requeued,) = [op for _, op in journal.pending()]
    assert "first_failed_at" not in requeued
    monkeypatch.setenv("PROBE_OUTBOX_TRANSIENT_BUDGET_SEC", str(journal_module.TRANSIENT_BUDGET_SECONDS))
    drain(journal, client_factory=lambda ctx: client)
    assert len(journal.pending()) == 1 and journal.failed() == []


def test_a_deadline_stop_charges_the_op_nothing(tmp_path):
    """`errors.DeadlineExceeded` is the CALLER's clock (finish()'s close
    budget), not the server's answer: the pass stops and the op is untouched."""
    journal = journal_at(tmp_path)
    journal.append_http("POST", "/v1/runs/r-1/metrics", {"points": []})
    before = [op for _, op in journal.pending()]

    class _Late:
        class transport:  # noqa: N801 -- the shape drain uses
            @staticmethod
            def request(*a, **k):
                raise errors.DeadlineExceeded("deadline passed before it was sent")

        def close(self):
            pass

    report = drain(journal, client_factory=lambda ctx: _Late())
    assert report.deadline_reached and not report.stopped_transient
    assert [op for _, op in journal.pending()] == before, "not an attempt, not an error"


def test_a_transient_stop_reports_the_servers_retry_after(tmp_path):
    journal = journal_at(tmp_path)
    journal.append_http("POST", "/v1/runs/r-1/metrics", {"points": []})

    class _Busy:
        class transport:  # noqa: N801
            @staticmethod
            def request(*a, **k):
                exc = errors.ServerError("concurrent telemetry write", status=503)
                exc.retry_after = 3.0
                raise exc

        def close(self):
            pass

    report = drain(journal, client_factory=lambda ctx: _Busy())
    assert report.stopped_transient and report.retry_after == 3.0


def test_a_bounded_lock_wait_gives_up_and_says_so(tmp_path):
    from probe._shared import oscompat
    import time as _time

    journal = journal_at(tmp_path)
    journal.append_http("POST", "/v1/runs/r-1/metrics", {"points": []})
    holder = open(journal.drain_lock, "a+")
    oscompat.flock(holder.fileno(), oscompat.LOCK_EX)
    try:
        started = _time.monotonic()
        report = drain(journal, client_factory=lambda ctx: None, lock_timeout=0.3)
        assert 0.25 <= _time.monotonic() - started < 2
    finally:
        oscompat.flock(holder.fileno(), oscompat.LOCK_UN)
        holder.close()
    assert report.lock_busy and report.remaining == 1 and report.delivered == 0


def test_auth_block_halts_and_keeps_everything(tmp_path):
    journal = journal_at(tmp_path)
    journal.append_http("POST", "/v1/runs/r-1/metrics", {"points": []})
    journal.append_http("POST", "/v1/runs/r-1/metrics", {"points": []})

    class RevokedTransport:
        def request(self, *a, **k):
            raise errors.AuthError("revoked", status=401)

    class RevokedClient:
        transport = RevokedTransport()

        def close(self):
            pass

    report = drain(journal, client_factory=lambda ctx: RevokedClient())
    assert report.auth_blocked
    assert report.remaining == 2 and journal.failed() == []
    status = Journal.read_status(journal.dir)
    assert status["auth_blocked_since"]


def test_an_unroutable_op_dead_letters_and_the_queue_keeps_moving(tmp_path):
    """The failure this box actually hit: 3275 ops pinned to local test
    servers on ports that no longer existed, and one AuthError on the head of
    the queue held back everything behind it for 21 hours while every probe
    command told the researcher to run `probe login` -- which could not have
    helped, because no login writes a credential for a dead ephemeral port."""
    journal = journal_at(tmp_path)
    journal.append_http("POST", "/v1/runs/dead/metrics", {"points": []})
    journal.append_http("POST", "/v1/runs/live/metrics", {"points": []})

    delivered = []

    class _T:
        def request(self, method, path, json_body=None, **kw):
            if "/dead/" in path:
                raise errors.UnroutableEndpointError(
                    "pinned endpoint http://127.0.0.1:54675 is not what "
                    "context default names"
                )
            delivered.append(path)
            return {}

    class _C:
        transport = _T()

        def close(self):
            pass

    report = drain(journal, client_factory=lambda ctx: _C())

    assert not report.auth_blocked, "an unreachable endpoint is not a logged-out user"
    assert delivered == ["/v1/runs/live/metrics"], "the queue behind it must move"
    assert journal.pending() == []
    assert len(journal.failed()) == 1, "kept as a dead letter, not silently dropped"
    status = Journal.read_status(journal.dir)
    assert not status["auth_blocked_since"]
    # The dead letter is only worth anything if the surfaces that offer to
    # retry it can see it: `probe outbox status` reads exactly this count.
    assert status["failed"] == 1


def test_a_logged_out_context_parks_rather_than_dead_letters(tmp_path):
    """The distinction the permanent verdict must NOT swallow: no stored record
    (or a record for THIS endpoint with no credential in it) is a researcher
    who has not logged in, and `probe login` recovers every op. Dead-lettering
    those would throw away real work to fix a problem about dead test servers,
    and a self-hosted user mid-logout is otherwise byte-for-byte
    indistinguishable from a dead ephemeral port."""
    journal = Journal(
        tmp_path / "outbox",
        context={"name": "selfhosted", "base_url": "https://probe.internal"},
    )
    journal.append_http("POST", "/v1/runs/r-1/metrics", {"points": []})
    report = drain(journal)
    assert report.auth_blocked
    assert journal.failed() == [] and report.remaining == 1


def test_an_unroutable_upload_does_not_take_the_drain_down_with_it(tmp_path):
    """Regression, found in review: the permanent path records a fallback
    artifact for a rejected upload, and BUILDING the client for it resolves
    credentials -- which for an unroutable endpoint raises. Evaluated bare as
    an argument, that exception left the `except` block, the loop and drain()
    itself, so the queue behind it never moved: the wedge this change removes,
    reintroduced by removing it."""
    _store_context(tmp_path, "ghost", "http://stored-elsewhere")
    journal = Journal(
        tmp_path / "outbox",
        context={"name": "ghost", "base_url": "http://elsewhere"},
    )
    src = tmp_path / "blob.bin"
    src.write_bytes(b"bytes")
    journal.append_upload(
        anchor="run",
        anchor_id="r-1",
        name="blob.bin",
        src_path=str(src),
        run_ref="r-1",
        inline_hash=True,
    )
    journal.append_http("POST", "/v1/runs/r-1/metrics", {"points": []})

    report = drain(journal)  # must RETURN, not raise

    assert not report.auth_blocked
    assert journal.pending() == [], "the op behind the upload must be reached"
    assert len(journal.failed()) == 2


def test_a_revoked_credential_still_halts_rather_than_dead_letters(tmp_path):
    """The other half of the same distinction: a real 401 IS fixable by
    logging in, so those ops stay queued and the drainer stops. Dead-lettering
    them would throw away work the researcher can still deliver."""
    journal = journal_at(tmp_path)
    journal.append_http("POST", "/v1/runs/r-1/metrics", {"points": []})

    class _T:
        def request(self, *a, **k):
            raise errors.AuthError("revoked", status=401)

    class _C:
        transport = _T()

        def close(self):
            pass

    report = drain(journal, client_factory=lambda ctx: _C())
    assert report.auth_blocked
    assert journal.failed() == [] and report.remaining == 1


def test_conflict_on_retry_counts_as_idempotent_delivery(tmp_path):
    """409-with-existing_id is claimed as our own earlier delivery ONLY when
    the op has a prior attempt (first-attempt policy lives in
    test_first_attempt_conflict_dead_letters_not_swallowed)."""
    journal = journal_at(tmp_path)
    journal.append_http("POST", "/v1/runs/r-1/artifacts", {"name": "n"})
    path, op = journal.pending()[0]
    op["attempts"] = 1  # a previous attempt may have half-delivered
    path.write_text(__import__("json").dumps(op))

    class ReplayedTransport:
        def request(self, *a, **k):
            raise errors.ConflictError("dup", detail={"existing_id": "a-1"})

    class ReplayedClient:
        transport = ReplayedTransport()

        def close(self):
            pass

    report = drain(journal, client_factory=lambda ctx: ReplayedClient())
    assert report.delivered == 1 and report.clean


def test_upload_op_stages_hashes_and_confirms(app, tmp_path):
    run_id = seeded_run(app, tmp_path)
    journal = journal_at(tmp_path)
    src = tmp_path / "model.bin"
    src.write_bytes(b"weights " * 1024)
    # blob=None exercises the 11A big-file path: hashing happens at drain.
    journal.append_upload(
        anchor="run",
        anchor_id=run_id,
        name="model.bin",
        src_path=str(src),
        run_ref=run_id,
        inline_hash=False,
    )
    src.write_bytes(b"mutated after enqueue")  # must not affect the upload
    report = drain_with(app, journal)
    assert report.clean and report.delivered == 1
    (artifact,) = app.artifacts[run_id]
    assert artifact["status"] == "complete"
    assert artifact["size_bytes"] == len(b"weights " * 1024)
    assert list(journal.blobs_dir.iterdir()) == [], "blob must be GC'd after delivery"


def test_run_scoped_drain_leaves_other_runs(app, tmp_path):
    run_a = seeded_run(app, tmp_path)
    journal = journal_at(tmp_path)
    journal.append_http(
        "POST",
        f"/v1/runs/{run_a}/metrics",
        {"points": [{"key": "a", "kind": "model", "value": 1.0, "step_index": 1}]},
    )
    journal.append_http("POST", "/v1/runs/other-run/metrics", {"points": []})
    report = drain_with(app, journal, run_ref=run_a)
    assert report.delivered == 1
    assert [op["run_ref"] for _, op in journal.pending()] == ["other-run"]


def test_paused_journal_does_not_drain(app, tmp_path):
    journal = journal_at(tmp_path)
    journal.append_http("POST", "/v1/runs/r-1/metrics", {"points": []})
    journal.pause()
    report = drain_with(app, journal)
    assert report.delivered == 0 and report.remaining == 1
    journal.resume()


# -- client integration ------------------------------------------------------


def test_async_client_journals_without_touching_the_network(app, tmp_path):
    client = make_client(app, tmp_spool=tmp_path / "outbox", async_writes=True)
    before = len(app.requests)
    client.write("POST", "/v1/runs/r-1/metrics", {"points": []})
    assert len(app.requests) == before, "async write must not touch the network"
    assert len(client.journal.pending()) == 1
    client.close()


def test_flush_delivers_journaled_writes(app, tmp_path):
    run_id = seeded_run(app, tmp_path)
    client = make_client(app, tmp_spool=tmp_path / "outbox", async_writes=True)
    client.write(
        "POST",
        f"/v1/runs/{run_id}/metrics",
        {"points": [{"key": "loss", "kind": "model", "value": 1.0, "step_index": 1}]},
    )
    assert client.flush() == 1
    assert client.journal.pending() == []
    client.close()


# -- worker ------------------------------------------------------------------


def test_maybe_spawn_declines_when_idle_or_paused(tmp_path, monkeypatch):
    from probe.sdk import outbox_worker

    journal = journal_at(tmp_path)
    assert outbox_worker.maybe_spawn(str(journal.dir)) is False  # empty
    journal.append_http("POST", "/v1/x", {})
    journal.pause()
    assert outbox_worker.maybe_spawn(str(journal.dir)) is False  # paused
    journal.resume()
    # A FRESH auth block suppresses; a stale one is a cooldown that has expired
    # and gets one re-probe (test_a_stale_auth_block_allows_one_reprobe).
    from datetime import datetime, timezone

    journal.write_status(auth_blocked_since=datetime.now(timezone.utc).isoformat())
    assert outbox_worker.maybe_spawn(str(journal.dir)) is False  # auth-blocked


def test_worker_loop_backs_off_then_exits_when_empty(tmp_path, monkeypatch):
    from probe.sdk import outbox_worker
    from probe.sdk.journal import DrainReport

    reports = [
        DrainReport(delivered=0, remaining=1, stopped_transient=True, errors=["net"]),
        DrainReport(delivered=1, remaining=0),
    ]
    slept: list[float] = []
    monkeypatch.setattr("probe.sdk.journal.drain", lambda j, **k: reports.pop(0))
    monkeypatch.setattr(outbox_worker.time, "sleep", slept.append)
    assert outbox_worker.run(str(tmp_path / "outbox")) == 0
    # 2.0 = transient backoff; 1.5 = the exit-grace linger for a dying
    # writer's last op (prod smoke 2026-08-06).
    assert slept == [2.0, outbox_worker._EXIT_GRACE_SECONDS]


def test_worker_loop_exits_hard_on_auth_block(tmp_path, monkeypatch):
    from probe.sdk import outbox_worker
    from probe.sdk.journal import DrainReport

    monkeypatch.setattr(
        "probe.sdk.journal.drain",
        lambda j, **k: DrainReport(remaining=2, auth_blocked=True, errors=["401"]),
    )
    assert outbox_worker.run(str(tmp_path / "outbox")) == 3


def test_gc_ignores_staging_dotfiles(tmp_path):
    """Review fix: append_upload stages to a dot-prefixed name and publishes
    it under the append lock, so gc can never reap a mid-enqueue blob."""
    journal = journal_at(tmp_path)
    journal._ensure()
    staging = journal.blobs_dir / ".staging-abc123"
    staging.write_bytes(b"mid-enqueue bytes")
    assert journal.gc_blobs() == 0
    assert staging.exists()


def test_drain_persists_deferred_hash_before_delivery(app, tmp_path):
    """Review fix: the 11A hash+rename must be written back to the op file
    BEFORE the upload attempt -- a crash after the rename must not strand the
    op pointing at a staging name that no longer exists."""
    run_id = seeded_run(app, tmp_path)
    journal = journal_at(tmp_path)
    src = tmp_path / "big.bin"
    src.write_bytes(b"weights " * 2048)
    journal.append_upload(
        anchor="run",
        anchor_id=run_id,
        name="big.bin",
        src_path=str(src),
        run_ref=run_id,
        inline_hash=False,
    )

    class HashesThenDies:
        class transport:  # noqa: N801 -- structural stub
            @staticmethod
            def request(*a, **k):
                raise errors.TransportError("net down")

        @staticmethod
        def upload_fingerprinted(*a, **k):
            raise errors.TransportError("net down mid-upload")

        @staticmethod
        def close():
            pass

    report = drain(journal, client_factory=lambda ctx: HashesThenDies())
    assert report.stopped_transient and report.remaining == 1
    ((_, op),) = journal.pending()
    digest = op["upload"]["blob"]
    assert digest is not None, "hash+rename must be persisted to the op file"
    assert (journal.blobs_dir / digest).exists()
    assert not any(p.name.startswith("incoming-") for p in journal.blobs_dir.iterdir())
    # And the recovered op delivers cleanly on the next drain.
    assert drain_with(app, journal).clean


# -- review-pass additions (testing + performance + security specialists) -----


def _store_context(tmp_path, name, base_url, token="tok"):
    """Write one context into the isolated config `_isolated_config` points at."""
    cfg = tmp_path / "config" / "probe.json"
    cfg.parent.mkdir(parents=True, exist_ok=True)
    cfg.write_text(
        json.dumps(
            {
                "version": 2,
                "current_context": name,
                "contexts": {name: {"base_url": base_url, "token": token}},
            }
        )
    )


def test_drain_without_factory_dead_letters_an_unmatched_pin(tmp_path):
    """Production credential path (no client_factory): an op pinned to an
    endpoint no stored context matches must never borrow an ambient token
    issued for a different host (security review) -- that property is
    unchanged and is what makes the op undeliverable here.

    What changed is the disposition. It used to auth-block, which reads as
    "log in and this will go", and no login can produce a credential for an
    endpoint the config does not name -- so the queue parked on it forever.
    A dead letter says the same thing honestly, stays visible in `probe
    outbox status`, and can still be retried if that endpoint ever becomes
    reachable."""
    _store_context(tmp_path, "ghost", "http://stored-elsewhere")
    journal = Journal(
        tmp_path / "outbox",
        context={"name": "ghost", "base_url": "http://elsewhere"},
    )
    journal.append_http("POST", "/v1/runs/r-1/metrics", {"points": []})
    report = drain(journal)
    assert not report.auth_blocked
    assert journal.pending() == []
    failed = journal.failed()
    assert len(failed) == 1
    # The refusal happens while RESOLVING the credential, before any request:
    # the security property this test was written for. Assert the refusal
    # itself -- the pinned URL alone also appears in the op's own context, so
    # matching on it proved nothing about which branch ran.
    assert "is not what context" in failed[0][1]["last_error"]
    assert "no stored credential matches it" in failed[0][1]["last_error"]


def test_missing_staged_bytes_dead_letter_not_livelock(app, tmp_path):
    """ValidationError without an HTTP status must classify permanent: a
    forever-transient local error would park the drainer at the backoff cap
    for eternity (performance review)."""
    run_id = seeded_run(app, tmp_path)
    journal = journal_at(tmp_path)
    src = tmp_path / "gone.bin"
    src.write_bytes(b"bytes")
    queued = journal.append_upload(
        anchor="run",
        anchor_id=run_id,
        name="gone.bin",
        src_path=str(src),
        run_ref=run_id,
        inline_hash=True,
    )
    (journal.blobs_dir / queued["blob"]).unlink()
    src.unlink()
    report = drain_with(app, journal)
    assert report.dead_lettered == 1 and not report.stopped_transient
    ((_, op),) = journal.failed()
    assert "gone" in op["last_error"]


def test_an_unknown_op_kind_is_held_not_dead_lettered(app, tmp_path):
    """Plan 1.11: an op of a kind this release cannot deliver was queued by a
    newer SDK sharing the outbox (or survives a rollback). It used to be
    dead-lettered as permanent -- data a newer worker could have delivered.
    It now waits, unattempted, with nothing charged to its failure budget."""
    journal = journal_at(tmp_path)
    journal.append_http("POST", "/v1/x", {})
    path, op = journal.pending()[0]
    op["kind"] = "from-the-future"
    path.write_text(__import__("json").dumps(op))
    report = drain_with(app, journal)
    assert report.dead_lettered == 0 and report.remaining == 1 and journal.failed() == []
    assert report.unknown_kinds == 1
    (_, held), = journal.pending()
    assert held["attempts"] == 0 and "first_failed_at" not in held


def test_last_error_redacts_presigned_urls(tmp_path):
    journal = journal_at(tmp_path)
    journal.append_http("POST", "/v1/x", {})

    class LeakyTransport:
        def request(self, *a, **k):
            raise errors.ValidationError(
                "PUT https://r2.example/put/abc?X-Amz-Signature=SECRET123: rejected",
                status=422,
            )

    class LeakyClient:
        transport = LeakyTransport()

        def close(self):
            pass

    drain(journal, client_factory=lambda ctx: LeakyClient())
    ((_, op),) = journal.failed()
    assert "SECRET123" not in op["last_error"]
    assert "<redacted>" in op["last_error"]
    status = Journal.read_status(journal.dir)
    assert "SECRET123" not in (status.get("last_error") or "")


def test_drain_lock_contention_reports_without_touching_queue(tmp_path):
    from probe._shared import oscompat

    journal = journal_at(tmp_path)
    journal.append_http("POST", "/v1/x", {})
    journal._ensure()
    holder = open(journal.drain_lock, "a+")
    oscompat.flock(holder.fileno(), oscompat.LOCK_EX)
    try:
        report = drain(journal, wait_for_lock=False)
        assert report.remaining == 1 and report.delivered == 0
        assert any("another drain holds the lock" in e for e in report.errors)
    finally:
        oscompat.flock(holder.fileno(), oscompat.LOCK_UN)
        holder.close()


def test_maybe_spawn_spawns_detached_worker(tmp_path, monkeypatch):
    from probe.sdk import outbox_worker

    journal = journal_at(tmp_path)
    journal.append_http("POST", "/v1/x", {})
    calls: list = []
    monkeypatch.setattr(
        outbox_worker.subprocess, "Popen", lambda argv, **kw: calls.append((argv, kw))
    )
    assert outbox_worker.maybe_spawn(str(journal.dir)) is True
    argv, kw = calls[0]
    assert argv[1:3] == ["-m", "probe.sdk.outbox_worker"]
    if os.name == "posix":
        assert kw["start_new_session"] is True
        import stat as stat_module

        mode = stat_module.S_IMODE((journal.dir / "drainer.log").stat().st_mode)
        assert mode == 0o600
    else:  # start_new_session is ignored on Windows: a detached process group instead
        import subprocess

        assert kw["creationflags"] == subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP


def test_worker_run_exits_4_when_paused(tmp_path):
    from probe.sdk import outbox_worker

    journal = journal_at(tmp_path)
    journal.append_http("POST", "/v1/x", {})
    journal.pause()
    assert outbox_worker.run(str(journal.dir)) == 4


def test_harbor_clone_branch_retries_then_raises_on_mutation(tmp_path, monkeypatch):
    """The clone-first branch's mutation guard is testable on ANY filesystem by
    faking try_clone (testing review: the logic had never executed anywhere)."""
    import shutil as shutil_module

    from probe.connectors import harbor

    def fake_clone(src, dst):
        shutil_module.copyfile(src, dst)
        return True

    monkeypatch.setattr(harbor, "try_clone", fake_clone)
    source = tmp_path / "src.bin"
    source.write_bytes(b"stable contents")
    digest, size = harbor._copy_and_hash(source, tmp_path / "out.bin")
    assert size == len(b"stable contents")

    real_stat = harbor.Path.stat
    calls = {"n": 0}

    def mutating_stat(self, **kw):
        result = real_stat(self, **kw)
        if self == source:
            calls["n"] += 1
            if calls["n"] % 2 == 0:  # every after-stat sees a "new" file
                # Advance deterministically rather than relying on two adjacent
                # wall-clock reads landing in different filesystem timestamp
                # ticks (tmpfs can legitimately return the same mtime here).
                os.utime(
                    source,
                    ns=(result.st_atime_ns, result.st_mtime_ns + 1_000_000_000),
                )
                return real_stat(self, **kw)
        return result

    # A private MonkeyPatch: calling the FIXTURE's undo() would also revert
    # the autouse env isolation and trip the conftest teardown guard.
    stat_patch = pytest.MonkeyPatch()
    stat_patch.setattr(harbor.Path, "stat", mutating_stat, raising=False)
    try:
        with pytest.raises(RuntimeError, match="source changed while staging"):
            harbor._copy_and_hash(source, tmp_path / "out2.bin")
    finally:
        stat_patch.undo()


# -- codex adversarial-pass regressions ---------------------------------------


def test_first_attempt_conflict_dead_letters_not_swallowed(tmp_path):
    """A 409-with-existing_id on a FIRST attempt is a genuine natural-key
    conflict -- treating it as idempotent success would silently discard the
    queued write (codex). Only a RETRY may claim its own earlier delivery."""
    journal = journal_at(tmp_path)
    journal.append_http("POST", "/v1/runs/r-1/artifacts", {"name": "n"})

    class Conflicted:
        class transport:  # noqa: N801
            @staticmethod
            def request(*a, **k):
                raise errors.ConflictError("dup", detail={"existing_id": "a-1"})

        @staticmethod
        def close():
            pass

    report = drain(journal, client_factory=lambda ctx: Conflicted())
    assert report.dead_lettered == 1 and report.delivered == 0
    # The same conflict on an op that has already been attempted counts as
    # our own half-delivered retry.
    journal.retry_failed()
    report = drain(journal, client_factory=lambda ctx: Conflicted())
    assert report.delivered == 1 and report.dead_lettered == 0


@pytest.mark.parametrize("message, delivered", [
    ("lineage edge already exists", True),  # that exact edge is recorded: the write is done
    ("this run already has a genealogy parent — a run descends from at most one predecessor", False),
])
def test_an_edge_that_already_exists_is_delivered_on_the_first_attempt(tmp_path, message, delivered):
    """A queued `probe edge add` of an edge that was already recorded dead-lettered
    on its first attempt (a 409 with existing_id). The conflict key is the whole
    edge, so nothing is lost by counting it done; the genealogy-parent 409 names a
    DIFFERENT edge and stays a dead letter."""
    journal = journal_at(tmp_path)
    journal.append_http("POST", "/v1/edges", {"source_type": "run", "source_id": "r-1", "relation": "derived_from",
                                              "target_type": "run", "target_id": "r-0"})

    class Conflicted:
        class transport:  # noqa: N801
            @staticmethod
            def request(*a, **k):
                raise errors.error_for(409, {"message": message, "existing_id": "e-1"})

        @staticmethod
        def close():
            pass

    report = drain(journal, client_factory=lambda ctx: Conflicted())
    assert (report.delivered, report.dead_lettered) == ((1, 0) if delivered else (0, 1))
    assert journal.pending() == []


def test_corrupt_op_files_are_quarantined_visibly(app, tmp_path):
    journal = journal_at(tmp_path)
    journal.append_http("POST", "/v1/runs/r-1/metrics", {"points": []})
    journal._ensure()
    bad = journal.ops_dir / "00000000000000000000-corrupt.json"
    bad.write_text("{not json")
    journal.write_status()
    report = drain_with(app, journal)
    assert report.dead_lettered == 0  # quarantine is not a dead-letter event
    assert not bad.exists(), "corrupt op must leave ops/"
    assert (journal.failed_dir / bad.name).exists(), "…and stay visible in failed/"
    status = Journal.read_status(journal.dir)
    assert status["pending"] == 0, "status must agree with what drain can see"
    assert status["failed"] >= 1


def test_custom_journal_dir_never_steals_the_global_spool(tmp_path, monkeypatch):
    """Only the DEFAULT journal auto-imports the legacy spool: a Client with a
    custom spool_dir must not migrate (and delete) the machine's global
    pending writes into its private directory (codex)."""
    state = tmp_path / "state"
    monkeypatch.setenv("XDG_STATE_HOME", str(state))
    monkeypatch.delenv("PROBE_OUTBOX_DIR", raising=False)
    monkeypatch.delenv("PROBE_SPOOL_DIR", raising=False)
    legacy = Spool()  # resolves under the isolated XDG_STATE_HOME
    legacy.append("POST", "/v1/x", {"n": 1})
    custom = Journal(tmp_path / "custom")
    custom.append_http("POST", "/v1/y", {})
    assert legacy.file.exists(), "custom journal must not consume the global spool"
    assert len(custom.pending()) == 1
    default = Journal()  # the default dir DOES fold the legacy spool in
    default.append_http("POST", "/v1/z", {})
    assert not legacy.file.exists()
    assert [op["path"] for _, op in default.pending()] == ["/v1/x", "/v1/z"]


def _fresh_auth_block() -> str:
    from datetime import datetime, timezone

    return datetime.now(timezone.utc).isoformat()


def test_a_fresh_auth_block_still_suppresses_spawning(tmp_path):
    """The zombie-uploader guard: no hot retry against rejected credentials."""
    from probe.sdk import outbox_worker

    journal = journal_at(tmp_path)
    journal.append_http("POST", "/v1/x", {})
    journal.write_status(auth_blocked_since=_fresh_auth_block())
    assert outbox_worker.maybe_spawn(str(journal.dir)) is False


def test_a_stale_auth_block_allows_one_reprobe(tmp_path):
    """...but suppression is a COOLDOWN, not a permanent stop. A token that
    expired or rotated mid-run used to leave the queue undelivered forever,
    recoverable only if someone noticed and ran `probe outbox retry`. After the
    cooldown one worker is allowed, so a re-issued credential resumes on its own.
    """
    from datetime import datetime, timedelta, timezone

    from probe.sdk import outbox_worker

    journal = journal_at(tmp_path)
    journal.append_http("POST", "/v1/x", {})
    stale = datetime.now(timezone.utc) - timedelta(
        seconds=outbox_worker._AUTH_RETRY_COOLDOWN_SECONDS + 60
    )
    journal.write_status(auth_blocked_since=stale.isoformat())

    calls: list = []
    mp = pytest.MonkeyPatch()
    mp.setattr(outbox_worker.subprocess, "Popen", lambda *a, **k: calls.append(a))
    try:
        assert outbox_worker.maybe_spawn(str(journal.dir)) is True
    finally:
        mp.undo()


def test_clear_auth_block_reopens_spawning(tmp_path):
    from probe.sdk import outbox_worker

    journal = journal_at(tmp_path)
    journal.append_http("POST", "/v1/x", {})
    journal.write_status(auth_blocked_since=_fresh_auth_block())
    assert outbox_worker.maybe_spawn(str(journal.dir)) is False
    journal.clear_auth_block()
    calls: list = []
    mp = pytest.MonkeyPatch()
    mp.setattr(outbox_worker.subprocess, "Popen", lambda *a, **k: calls.append(a))
    try:
        assert outbox_worker.maybe_spawn(str(journal.dir)) is True
    finally:
        mp.undo()


def test_inline_hash_is_taken_from_the_snapshot(tmp_path):
    """TOCTOU guard: the recorded digest must describe the STAGED bytes, so a
    source rewrite between enqueue steps can never poison the content
    address (codex)."""
    import hashlib

    journal = journal_at(tmp_path)
    src = tmp_path / "f.bin"
    src.write_bytes(b"original contents")
    queued = journal.append_upload(
        anchor="run",
        anchor_id="r-1",
        name="f.bin",
        src_path=str(src),
        run_ref="r-1",
        inline_hash=True,
    )
    src.write_bytes(b"rewritten after enqueue")
    staged = (journal.blobs_dir / queued["blob"]).read_bytes()
    assert staged == b"original contents"
    assert queued["blob"] == hashlib.sha256(b"original contents").hexdigest()


# -- a queued petname reaches a UUID-typed route -----------------------------
#
# Enqueue does not read the run on purpose: `--async` exists so a write can be
# queued with no network. Every route the drainer replays EXCEPT
# `GET /v1/runs/{ref}` types its path param as a UUID, so
# `probe --async log tunneling-sambar-254 ...` queued cleanly, reported
# `failed: 0`, and dead-lettered on a 422 minutes later where nobody saw it.


class _PetnameBackend:
    """Accepts the UUID and 422s the petname, like the real routes."""

    RUN_ID = "0f8e1c26-1c2f-4d2f-9c1f-2b6d5a1e9c00"

    def __init__(self, *, resolvable=True):
        self.resolvable = resolvable
        self.paths: list[str] = []
        self.lookups: list[str] = []

    # -- transport
    @property
    def transport(self):
        return self

    def request(self, method, path, json_body=None):
        self.paths.append(path)
        if run_ref_for_path(path) not in (None, self.RUN_ID):
            raise errors.ValidationError(f"badly formed uuid in {path}", status=422)
        return {}

    # -- client
    def get_run(self, ref):
        self.lookups.append(ref)
        if not self.resolvable:
            raise errors.NotFoundError(f"no run {ref}")
        return {"id": self.RUN_ID, "slug": ref}

    def close(self):
        pass


def test_a_queued_petname_is_resolved_and_delivered(tmp_path):
    journal = journal_at(tmp_path)
    journal.append_http("POST", "/v1/runs/tunneling-sambar-254/metrics", {"points": []})

    backend = _PetnameBackend()
    report = drain(journal, client_factory=lambda ctx: backend)

    assert report.delivered == 1
    assert report.dead_lettered == 0
    assert backend.paths[-1] == f"/v1/runs/{_PetnameBackend.RUN_ID}/metrics"


def test_the_lookup_happens_only_after_the_422(tmp_path):
    """Not before it: the happy path must not pay a round trip, and a genuine
    body-validation 422 must not be hidden behind a lookup of our own."""
    journal = journal_at(tmp_path)
    journal.append_http("POST", f"/v1/runs/{_PetnameBackend.RUN_ID}/metrics", {"points": []})

    backend = _PetnameBackend()
    report = drain(journal, client_factory=lambda ctx: backend)

    assert report.delivered == 1
    assert backend.lookups == [], "a UUID path resolved something it already had"


def test_one_lookup_serves_every_op_for_the_same_run(tmp_path):
    journal = journal_at(tmp_path)
    for _ in range(4):
        journal.append_http("POST", "/v1/runs/tunneling-sambar-254/metrics", {"points": []})

    backend = _PetnameBackend()
    report = drain(journal, client_factory=lambda ctx: backend)

    assert report.delivered == 4
    assert backend.lookups == ["tunneling-sambar-254"], backend.lookups


def test_an_unresolvable_ref_dead_letters_on_the_servers_error(tmp_path):
    """Not on ours. The 422 the server gave is the better diagnosis, and a
    swallowed lookup failure would replace it with a 404 about a lookup the
    caller never asked for."""
    journal = journal_at(tmp_path)
    journal.append_http("POST", "/v1/runs/no-such-petname/metrics", {"points": []})

    backend = _PetnameBackend(resolvable=False)
    report = drain(journal, client_factory=lambda ctx: backend)

    assert report.dead_lettered == 1
    assert "badly formed uuid" in report.errors[-1]


def test_the_queued_ref_survives_in_the_op_file(tmp_path):
    """The substitution is per-attempt. `run_ref` is the barrier-drain scoping
    key, so a queued petname has to keep matching a barrier armed on it."""
    journal = journal_at(tmp_path)
    journal.append_http("POST", "/v1/runs/tunneling-sambar-254/metrics", {"points": []})

    backend = _PetnameBackend()
    # A barrier scoped to the petname must still select the op.
    report = drain(journal, run_ref="tunneling-sambar-254", client_factory=lambda ctx: backend)

    assert report.delivered == 1


def test_one_blip_after_a_day_asleep_does_not_dead_letter(tmp_path, monkeypatch):
    """Time alone is not enough (review of #2011, LOW 3): a laptop that slept
    through a day after one failure must not dead-letter on its next blip.
    The op needs the day AND `MIN_TRANSIENT_ATTEMPTS` attempts."""
    from probe.sdk import journal as journal_module

    journal = journal_at(tmp_path)
    journal.append_http("POST", "/v1/runs/r-1/metrics", {"points": []})

    class _Down:
        class transport:  # noqa: N801 -- the shape drain uses
            @staticmethod
            def request(*a, **k):
                raise errors.ServerError("down", status=503)

        def close(self):
            pass

    clock = {"now": 1_000_000.0}
    monkeypatch.setattr(journal_module.time, "time", lambda: clock["now"])
    drain(journal, client_factory=lambda ctx: _Down())
    clock["now"] += 2 * journal_module.TRANSIENT_BUDGET_SECONDS  # asleep for two days
    drain(journal, client_factory=lambda ctx: _Down())

    (op,) = [op for _, op in journal.pending()]
    assert op["attempts"] == 2 and journal.failed() == [], "a day is not enough on its own"
    for _ in range(journal_module.MIN_TRANSIENT_ATTEMPTS - 2):
        drain(journal, client_factory=lambda ctx: _Down())
    assert journal.pending() == [] and len(journal.failed()) == 1, "the day AND the floor"


def test_a_deadline_cut_after_the_request_left_counts_as_an_attempt(app, tmp_path):
    """A close whose deadline cut a request mid-RESPONSE (the server may have
    applied it) records the attempt (review of #2011, LOW 2), so the replayed
    create's 409-with-existing_id reads as its own earlier delivery, not a
    first-attempt conflict to dead-letter."""
    journal = journal_at(tmp_path)
    journal.append_http("POST", "/v1/runs/r-1/metrics", {"points": []})
    journal.append_http("POST", "/v1/runs/r-1/metrics", {"points": []})
    answers = iter(
        [
            errors.DeadlineExceeded("cut while reading the response", sent=True),
            errors.ConflictError("already exists", detail={"existing_id": "x-1"}),
            None,
        ]
    )

    class _Once:
        class transport:  # noqa: N801
            @staticmethod
            def request(*a, **k):
                answer = next(answers)
                if answer is not None:
                    raise answer
                return None

        def close(self):
            pass

    first = drain(journal, client_factory=lambda ctx: _Once())
    assert first.deadline_reached
    head = [op for _, op in journal.pending()][0]
    assert head["attempts"] == 1 and "first_failed_at" not in head and not head.get("last_error")
    second = drain(journal, client_factory=lambda ctx: _Once())
    assert second.delivered == 2 and journal.failed() == [], "the replay's 409 is our own delivery"


def test_a_malformed_transient_budget_does_not_raise_under_W_error(tmp_path, monkeypatch):
    import warnings

    from probe.sdk import journal as journal_module

    monkeypatch.setenv("PROBE_OUTBOX_TRANSIENT_BUDGET_SEC", "soon")
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        assert journal_module._transient_budget_seconds() == journal_module.TRANSIENT_BUDGET_SECONDS


# -- plan 0.1: the pending estimate tracks the real queue ----------------------


def test_a_refusal_rereads_the_queue_before_dropping(tmp_path, monkeypatch):
    """The estimate only ever grows between refreshes, and another process's
    drain never reaches it. At the ceiling, re-read what the drain recounted
    before dropping anything."""
    from probe.sdk import journal as journal_module
    from probe.sdk.journal import OutboxFull

    monkeypatch.setattr(journal_module, "MAX_PENDING_OPS", 5)
    writer = journal_at(tmp_path)
    for _ in range(5):
        writer.append_http("POST", "/v1/runs/r-1/metrics", {"points": []})
    with pytest.raises(OutboxFull):
        writer.append_http("POST", "/v1/runs/r-1/metrics", {"points": []})

    # Another process (its own Journal object) drains everything.
    drainer = Journal(writer.dir, context=writer.context)

    class _Ok:
        class transport:  # noqa: N801 -- the shape drain uses
            @staticmethod
            def request(*a, **k):
                return None

        def close(self):
            pass

    assert drain(drainer, client_factory=lambda ctx: _Ok()).delivered == 5

    writer.append_http("POST", "/v1/runs/r-1/metrics", {"points": []})  # no longer refused
    assert len(writer.pending()) == 1


def test_the_estimate_follows_the_queue_that_another_process_drains(tmp_path):
    """Invariant (eng review, Code quality 4): with deliveries happening in
    ANOTHER process, this process's count never runs ahead of the real queue:
    every append takes its count from the status write it already makes."""
    writer = journal_at(tmp_path)
    drainer = Journal(writer.dir, context=writer.context)

    class _Ok:
        class transport:  # noqa: N801
            @staticmethod
            def request(*a, **k):
                return None

        def close(self):
            pass

    worst = 0
    for i in range(900):
        writer.append_http("POST", "/v1/runs/r-1/metrics", {"points": []})
        # Right after an append, which is when the cap is consulted.
        real = len(os.listdir(writer.ops_dir))
        worst = max(worst, writer._pending_estimate - real)
        if i % 50 == 49:
            drain(drainer, client_factory=lambda ctx: _Ok())
    assert worst == 0, worst


def test_a_writer_is_not_refused_in_the_middle_of_a_long_drain_pass(tmp_path, monkeypatch):
    """A drain pass rewrites status.json only when it ENDS, so mid-pass the
    file still says "full" although most of the queue has landed (review of
    #2014: 94 queued, status.json 200, 20 of 20 writes refused). Before
    refusing, the writer counts the queue directory itself."""
    import threading
    import time as _time

    from probe.sdk import journal as journal_module

    cap = 60
    monkeypatch.setattr(journal_module, "MAX_PENDING_OPS", cap)
    writer = journal_at(tmp_path)
    for _ in range(cap):
        writer.append_http("POST", "/v1/runs/r-1/metrics", {"points": []})
    drainer = Journal(writer.dir, context=writer.context)
    release = threading.Event()
    delivered = {"n": 0}

    class _Slow:
        class transport:  # noqa: N801
            @staticmethod
            def request(*a, **k):
                delivered["n"] += 1
                if delivered["n"] >= 50:
                    release.wait(10)  # hold the pass open with 10 ops left
                return None

        def close(self):
            pass

    thread = threading.Thread(target=lambda: drain(drainer, client_factory=lambda c: _Slow()))
    thread.start()
    try:
        deadline = _time.monotonic() + 10
        while delivered["n"] < 50 and _time.monotonic() < deadline:
            _time.sleep(0.01)
        assert Journal.read_status(writer.dir, include_receipts=False)["pending"] == cap
        refused = 0
        for _ in range(20):
            try:
                writer.append_http("POST", "/v1/runs/r-1/metrics", {"points": []})
            except journal_module.OutboxFull:
                refused += 1
        assert refused == 0, f"{refused} of 20 refused while the real queue was ~10"
    finally:
        release.set()
        thread.join(15)


def test_each_drop_is_one_gap_and_the_record_stays_small(app, tmp_path, monkeypatch):
    """Review of #2014: every refused write appended to an unbounded `gaps`
    list, recorded twice (journal and client), rewriting the whole producer
    file each time -- 6,000 drops took a refused log() from 16 ms to 107 ms."""
    from probe.sdk import journal as journal_module

    monkeypatch.setattr(journal_module, "MAX_PENDING_OPS", 3)
    client = make_client(app, tmp_spool=tmp_path / "outbox", async_writes=True, auto_drain=False)
    for i in range(3 + 200):
        client.write("POST", "/v1/runs/r-1/metrics", {"points": [{"i": i}]})
    assert client.dropped_writes == 200
    (record,) = client.journal.producer_report()
    assert record["gap_count"] == 200, "one gap per drop, not two"
    assert len(record["gaps"]) == journal_module._GAPS_KEPT
    assert record["gaps"][-1]["sequence"] == record["last_sequence"]
    (path,) = list(client.journal.producers_dir.iterdir())
    assert path.stat().st_size < 16_000, path.stat().st_size
    client.close()


# -- plan 1.9: a drain pass does not re-parse the queue under the append lock --


def _count_reads_under_the_append_lock(monkeypatch, journal):
    """Count op-file reads made while THIS journal's append lock is held."""
    import contextlib
    import pathlib

    from probe.sdk import journal as journal_module

    state = {"held": 0, "reads": []}
    real_lock = journal_module.file_lock

    @contextlib.contextmanager
    def tracking_lock(path):
        with real_lock(path):
            mine = pathlib.Path(path) == journal.append_lock
            state["held"] += mine
            try:
                yield
            finally:
                state["held"] -= mine

    real_read = pathlib.Path.read_text

    def counting_read(self, *a, **k):
        if state["held"] and self.parent in (journal.ops_dir, journal.failed_dir):
            state["reads"].append(self.name)
        return real_read(self, *a, **k)

    monkeypatch.setattr(journal_module, "file_lock", tracking_lock)
    monkeypatch.setattr(pathlib.Path, "read_text", counting_read)
    return state


def test_a_drain_pass_opens_only_the_tail_and_the_corrupt_under_the_lock(tmp_path, monkeypatch):
    """Plan 1.9: every pass parsed the whole queue TWICE while holding the
    append lock (quarantine, then the status recount), so a training loop's
    append waited behind it: 3.3 s at 20k ops. Now the queue is parsed once,
    outside the lock; under it, only the corrupt files are re-checked and only
    the ops appended during the pass are parsed."""
    journal = journal_at(tmp_path)
    for n in range(200):
        journal.append_http("POST", "/v1/runs/r-1/metrics", {"points": [{"i": n}]})
    for bad in ("00000000000000000000-bad1.json", "00000000000000000001-bad2.json"):
        (journal.ops_dir / bad).write_text("{not json")
    appended = {"n": 0}
    writer = Journal(journal.dir, context=journal.context)

    class _AppendsMidPass:
        class transport:  # noqa: N801 -- the shape drain uses
            @staticmethod
            def request(*a, **k):
                if appended["n"] < 3:  # a live training loop, mid-pass
                    appended["n"] += 1
                    writer.append_http("POST", "/v1/runs/r-2/metrics", {"points": []})
                raise errors.TransportError("down")  # park: the pass ends here

        def close(self):
            pass

    state = _count_reads_under_the_append_lock(monkeypatch, journal)
    report = drain(journal, client_factory=lambda ctx: _AppendsMidPass())

    assert report.stopped_transient
    assert len(state["reads"]) <= 3 + 2 * 2, state["reads"]  # tail + corrupt (checked, then gone)
    assert not (journal.ops_dir / "00000000000000000000-bad1.json").exists(), "still quarantined"
    status = Journal.read_status(journal.dir)
    real = len([n for n in os.listdir(journal.ops_dir) if n.endswith(".json")])
    assert status["pending"] == real == 200 + 1 == report.remaining, (status, real)
    assert status["failed"] == 2


def test_the_recount_still_totals_bytes_and_the_oldest_op(tmp_path):
    """The cheap recount keeps status.json's other facts true: pending_bytes
    (from the scan's cache plus the tail) and oldest_pending."""
    journal = journal_at(tmp_path)
    src = tmp_path / "blob.bin"
    src.write_bytes(b"x" * 1000)
    journal.append_upload(
        anchor="run", anchor_id="r-1", name="blob.bin", src_path=str(src), run_ref="r-1"
    )
    journal.append_http("POST", "/v1/runs/r-1/metrics", {"points": []})
    first = sorted(journal.ops_dir.iterdir())[0]
    enqueued = json.loads(first.read_text())["enqueued_at"]

    class _Down:
        class transport:  # noqa: N801
            @staticmethod
            def request(*a, **k):
                raise errors.TransportError("down")

        def upload_fingerprinted(self, *a, **k):
            raise errors.TransportError("down")

        def close(self):
            pass

    drain(journal, client_factory=lambda ctx: _Down())
    status = Journal.read_status(journal.dir)
    assert status["pending"] == 2
    assert status["pending_bytes"] == 1000
    assert status["oldest_pending"] == enqueued


def test_a_drain_sweeps_temp_files_a_killed_writer_left(tmp_path):
    """`write_text_atomic` writes `.<name>.<uuid>.tmp` then renames; a writer
    SIGKILLed in between leaves the temp forever. A pass removes ones older
    than an hour and leaves a live write's alone."""
    import time as _time

    journal = journal_at(tmp_path)
    journal.append_http("POST", "/v1/runs/r-1/metrics", {"points": []})
    stale = journal.ops_dir / ".0001-x.json.deadbeef.tmp"
    fresh = journal.ops_dir / ".0002-y.json.cafef00d.tmp"
    stale_status = journal.dir / ".status.json.0badc0de.tmp"
    for path in (stale, fresh, stale_status):
        path.write_text("{")
    old = _time.time() - 2 * 3600
    os.utime(stale, (old, old))
    os.utime(stale_status, (old, old))

    class _Down:
        class transport:  # noqa: N801
            @staticmethod
            def request(*a, **k):
                raise errors.TransportError("down")

        def close(self):
            pass

    drain(journal, client_factory=lambda ctx: _Down())
    assert not stale.exists() and not stale_status.exists()
    assert fresh.exists(), "a live write's temp is not touched"


def test_an_upload_stuck_at_the_head_does_not_rescan_the_queue_every_pass(
    tmp_path, monkeypatch
):
    """Review of #2038 (MED): a pass that merely TRIED an upload ran
    `gc_blobs`, which re-reads the whole queue under the append lock. An
    upload at the head of the queue during an outage is tried every pass, so
    `log()` froze behind it again (20k ops: ~1 s per pass). gc now runs only
    when an upload left the queue -- delivered or dead-lettered."""
    journal = journal_at(tmp_path)
    src = tmp_path / "ckpt.bin"
    src.write_bytes(b"w" * 1000)
    journal.append_upload(
        anchor="run", anchor_id="r-1", name="ckpt.bin", src_path=str(src), run_ref="r-1"
    )
    for n in range(20):
        journal.append_http("POST", "/v1/runs/r-1/metrics", {"points": [{"i": n}]})
    calls = []
    real_gc = Journal.gc_blobs
    monkeypatch.setattr(
        Journal, "gc_blobs", lambda self, **kw: (calls.append(1), real_gc(self, **kw))[1]
    )

    class _Down:
        class transport:  # noqa: N801
            @staticmethod
            def request(*a, **k):
                raise errors.TransportError("down")

        def upload_fingerprinted(self, *a, **k):
            raise errors.TransportError("down")

        def close(self):
            pass

    for _ in range(3):
        report = drain(journal, client_factory=lambda ctx: _Down())
        assert report.stopped_transient
    assert calls == [], "an upload that is still queued frees no blob"


def test_an_upload_that_leaves_the_queue_still_collects_blobs(app, tmp_path, monkeypatch):
    """The control: a delivered upload may leave its blob unreferenced, so the
    pass still collects."""
    run_id = seeded_run(app, tmp_path)
    journal = journal_at(tmp_path)
    _upload_op(journal, tmp_path, run_id=run_id)
    calls = []
    real_gc = Journal.gc_blobs
    monkeypatch.setattr(
        Journal, "gc_blobs", lambda self, **kw: (calls.append(1), real_gc(self, **kw))[1]
    )
    report = drain_with(app, journal)
    assert report.delivered == 1 and calls, "gc ran after the upload landed"


@pytest.mark.parametrize("failure", ["auth", "deadline"])
def test_the_status_counts_bytes_right_after_an_in_place_rewrite(tmp_path, failure):
    """Review of #2038 (LOW): the drain hashes an upload (it now has a size),
    then an auth block or a deadline after the request left rewrites the op in
    place; the recount reused the pass's stale cache and status.json read
    pending_bytes 0 for 5,000 queued bytes."""
    journal = journal_at(tmp_path)
    src = tmp_path / "big.bin"
    src.write_bytes(b"y" * 5000)
    journal.append_upload(
        anchor="run", anchor_id="r-1", name="big.bin", src_path=str(src), run_ref="r-1",
        inline_hash=False,
    )
    journal.append_http("POST", "/v1/runs/r-1/metrics", {"points": []})

    def boom(*a, **k):
        if failure == "auth":
            raise errors.AuthError("401", status=401)
        exc = errors.DeadlineExceeded("budget", sent=True)
        raise exc

    class _Refusing:
        class transport:  # noqa: N801
            request = staticmethod(boom)

        upload_fingerprinted = staticmethod(boom)

        def close(self):
            pass

    drain(journal, client_factory=lambda ctx: _Refusing())
    real = sum(
        int((op.get("upload") or {}).get("size_bytes") or 0) for _, op in journal.pending()
    )
    assert real == 5000
    assert Journal.read_status(journal.dir)["pending_bytes"] == real


# -- plan 1.3: a cheaper append ------------------------------------------------


def _metrics_body(i: int, *, label: str = "plain") -> dict:
    return {
        "points": [
            {
                "key": f"train/m{k}",
                "kind": "model",
                "labels": {"note": label},
                "step_index": i,
                "value": float(i),
                "wall_clock": "2026-09-27T12:00:00.000001+00:00",
            }
            for k in range(5)
        ]
    }


def _count_fsyncs(monkeypatch) -> list[int]:
    calls = [0]
    real = os.fsync

    def counting(fd):
        calls[0] += 1
        return real(fd)

    monkeypatch.setattr(os, "fsync", counting)
    return calls


def test_a_logged_write_fsyncs_once(app, tmp_path, monkeypatch):
    """Plan 1.3: each `log()` did 8 fsyncs -- the op file, `.seq`, status.json
    and the producer record, each file AND directory. Now only the op file is
    fsynced (before its rename), and the bookkeeping beside it is rebuilt by
    the drain (status) or recovered from the op names (`.seq`)."""
    client = make_client(app, tmp_spool=tmp_path / "outbox", async_writes=True)
    client.write("POST", "/v1/runs/r-1/metrics", _metrics_body(0))  # layout, producer file
    fsyncs = _count_fsyncs(monkeypatch)
    for i in range(1, 11):
        client.write("POST", "/v1/runs/r-1/metrics", _metrics_body(i))
    assert fsyncs[0] == 10, f"{fsyncs[0]} fsyncs for 10 writes"
    assert len(client.journal.pending()) == 11


def test_a_runs_terminal_status_keeps_every_fsync(tmp_path, monkeypatch):
    """The control: the one op a run cannot lose (its close, queued `admitted`)
    still takes the full path -- file and directory, for the op and its
    bookkeeping -- so the counter above is measuring a real difference."""
    journal = journal_at(tmp_path)
    journal.register_producer("sdk:test")
    journal.append_http("POST", "/v1/runs/r-1/metrics", _metrics_body(0))
    fsyncs = _count_fsyncs(monkeypatch)
    journal.append_http("PATCH", "/v1/runs/r-1", {"status": "completed"}, admitted=True)
    # File and directory for each of the three; Windows cannot fsync a
    # directory (`fsync_directory` is a no-op there), so the files only.
    floor = 6 if os.name == "posix" else 3
    assert fsyncs[0] >= floor, f"{fsyncs[0]} fsyncs for the terminal PATCH"


def test_a_logged_body_is_scrubbed_once(app, tmp_path, monkeypatch):
    """Plan 1.3: a metrics body crossed the full scrubber three times on the
    way to disk (`Client.write`, `append_http`, then the whole op in
    `_append`), plus status.json once more. `Client.write` scrubs it; the
    journal takes that body as prepared and scrubs only the envelope."""
    from probe.sdk import journal as journal_mod
    from probe.sdk import redaction, stamp_scrub

    client = make_client(app, tmp_spool=tmp_path / "outbox", async_writes=True)
    client.write("POST", "/v1/runs/r-1/metrics", _metrics_body(0))
    real = redaction.default_scrub
    seen: list[bool] = []
    depth = [0]

    def counting(value, *a, **kw):
        if depth[0] == 0:
            seen.append("points" in json.dumps(value, default=str))
        depth[0] += 1
        try:
            return real(value, *a, **kw)
        finally:
            depth[0] -= 1

    for module in (redaction, journal_mod, stamp_scrub):
        monkeypatch.setattr(module, "default_scrub", counting)
    client.write("POST", "/v1/runs/r-1/metrics", _metrics_body(1))
    assert seen.count(True) == 1, f"the body was scrubbed {seen.count(True)}x"
    assert seen.count(False) <= 1, "at most the op envelope besides"


def test_a_credential_is_still_redacted_on_disk(app, tmp_path):
    """Scrubbing once is still scrubbing: a token in a point's labels and one
    in the request path (the envelope) are both `<redacted>` in the op file."""
    client = make_client(app, tmp_spool=tmp_path / "outbox", async_writes=True)
    token = "probe_pat_" + "a1b2c3d4" * 4
    client.write(
        "POST", f"/v1/runs/r-1/metrics?api_key={token}", _metrics_body(1, label=token)
    )
    (path, op), = client.journal.pending()
    on_disk = path.read_text()
    assert token not in on_disk
    assert op["body"]["points"][0]["labels"]["note"].startswith("<redacted")
    assert "<redacted" in op["path"]


def test_a_raw_body_handed_to_the_queue_is_still_scrubbed(app, tmp_path):
    """The control for "prepared": only `Client.write` hands the journal a
    scrubbed body. The CLI's reference door calls `Client._enqueue` with a
    raw one, and the journal must still scrub it."""
    client = make_client(app, tmp_spool=tmp_path / "outbox", async_writes=True)
    token = "probe_pat_" + "a1b2c3d4" * 4
    assert client._enqueue(
        "POST", "/v1/runs/r-1/artifacts", {"name": token, "is_reference": True}
    )
    (path, op), = client.journal.pending()
    assert token not in path.read_text()
    assert op["body"]["name"].startswith("<redacted")


def test_a_regressed_sequence_never_sorts_a_new_write_ahead_of_a_queued_one(tmp_path):
    """`.seq` is no longer fsynced on the `log()` path, so a power loss can
    leave it behind op files that survived (Codex, round 2). The next append
    must still sort AFTER them: a terminal PATCH ahead of its run's data is a
    run closed before its data arrived."""
    journal = journal_at(tmp_path)
    for i in range(5):
        journal.append_http("POST", "/v1/runs/r-1/metrics", _metrics_body(i))
    (journal.dir / ".seq").write_text("1\n")  # the power loss: .seq went back

    restarted = journal_at(tmp_path)  # the next process
    restarted.append_http("PATCH", "/v1/runs/r-1", {"status": "completed"})
    methods = [op["method"] for _, op in restarted.pending()]
    assert methods == ["POST"] * 5 + ["PATCH"], methods


def test_the_high_water_mark_counts_dead_letters_and_waiting_uploads(tmp_path):
    """A dead letter goes back in line on `probe outbox retry`, and a waiting
    upload reserved its place when it was queued: both hold sequences a new
    write must sort after."""
    journal = journal_at(tmp_path)
    journal._ensure()
    (journal.failed_dir / "000000000040-1-dead.json").write_text("{}")
    reserved = "000000000070-1-waiting.json"
    record = journal.waiting_dir / "w1.json"
    op = {"op_id": "w1", "queue_filename": reserved, "run_ref": "r-1"}
    record.write_text(json.dumps({"op": op}))
    (journal.dir / ".seq").write_text("3\n")
    assert journal._queued_seq_high_water() == 70
    name = journal._op_filename("new")
    assert int(name.split("-", 1)[0]) == 71


def test_a_sequence_ahead_of_the_queue_is_kept(tmp_path):
    """The control: recovery only ever RAISES the sequence. An empty queue
    (everything delivered) behind `.seq` = 100 keeps counting from 100."""
    journal = journal_at(tmp_path)
    journal._ensure()
    (journal.dir / ".seq").write_text("100\n")
    journal.append_http("POST", "/v1/runs/r-1/metrics", _metrics_body(0))
    (path, _), = journal.pending()
    assert path.name.startswith("000000000101-")


def test_the_other_namespace_is_not_read_on_every_append(tmp_path, monkeypatch):
    """Plan 1.3: the op ceiling counts the sibling namespace (`delivery-v1`)
    too, and read its status.json on every append. It is re-read with the
    free-space sample and before any refusal, so a stale cached count can
    never refuse a write on its own."""
    from probe.sdk import journal as journal_mod

    journal = journal_at(tmp_path)
    sibling = journal.dir / journal_mod.DELIVERY_NAMESPACE
    sibling.mkdir(parents=True)
    (sibling / "status.json").write_text(json.dumps({"pending": 0}))
    reads: list[str] = []
    real = Journal.read_status

    def counting(directory=None, **kw):
        reads.append(str(directory))
        return real(directory, **kw)

    monkeypatch.setattr(Journal, "read_status", staticmethod(counting))
    for i in range(100):
        journal.append_http("POST", "/v1/runs/r-1/metrics", _metrics_body(i))
    sibling_reads = [r for r in reads if r == str(sibling)]
    assert len(sibling_reads) <= 1, f"{len(sibling_reads)} sibling reads for 100 appends"

    # The cached count said the sibling was full; it has since drained.
    monkeypatch.setattr(journal_mod, "MAX_PENDING_OPS", 150)
    journal._sibling_pending = 1_000
    journal.append_http("POST", "/v1/runs/r-1/metrics", _metrics_body(100))
    assert len(journal.pending()) == 101, "re-read before refusing, then admitted"


# -- plan 1.6: per-run lanes ---------------------------------------------------


class _PerRunServer:
    """A drain client whose server refuses chosen runs: a 503 (a sick run), or
    a connect failure (nobody can reach it). Records what reached it."""

    def __init__(self, *, busy=(), fail_once=(), unreachable=False):
        self.busy = set(busy)
        self.fail_once = set(fail_once)
        self.unreachable = unreachable
        self.sent: list[tuple[str, str]] = []
        outer = self

        class transport:  # noqa: N801 -- the shape drain uses
            @staticmethod
            def request(method, path, **kwargs):
                if outer.unreachable:
                    failure = errors.TransportError(f"{method} {path}: connection refused")
                    failure.unreachable = True
                    raise failure
                run = path.split("/")[3]
                label = ((kwargs.get("json_body") or {}).get("label")) or method
                if run in outer.busy or (run, label) in outer.fail_once:
                    outer.fail_once.discard((run, label))
                    raise errors.ServerError("concurrent telemetry write", status=503)
                outer.sent.append((run, label))

                class _Resp:
                    content = b""

                return _Resp()

        self.transport = transport

    def close(self):
        pass


def _queue(journal, run, label, *, method="POST"):
    path = f"/v1/runs/{run}/metrics" if method == "POST" else f"/v1/runs/{run}"
    journal.append_http(method, path, {"label": label})


def test_one_runs_503_does_not_hold_another_runs_ops(tmp_path):
    """Plan 1.6: the first transient failure of ANY op ended the pass, and the
    worker then slept and restarted from the global head, so one run's stuck op
    held every run on the machine -- for the 24 h it takes to dead-letter.
    Now A's head parks, A waits, and B's three ops land in the same pass."""
    journal = journal_at(tmp_path)
    for label in ("a1", "a2"):
        _queue(journal, "run-a", label)
    for label in ("b1", "b2", "b3"):
        _queue(journal, "run-b", label)
    server = _PerRunServer(busy={"run-a"})

    report = drain(journal, client_factory=lambda ctx: server)

    assert server.sent == [("run-b", "b1"), ("run-b", "b2"), ("run-b", "b3")]
    assert report.delivered == 3 and report.stopped_transient
    assert set(report.stalled_runs) == {"run-a"}
    assert "concurrent telemetry write" in report.stalled_runs["run-a"].error
    assert [op["body"]["label"] for _, op in journal.pending()] == ["a1", "a2"], "parked, in order"
    assert journal.failed() == []


def test_a_runs_own_order_holds_through_a_retry(tmp_path):
    """A run's ops still arrive in the order they were queued, its close last:
    m1 failing once parks m1 AND everything behind it in that run."""
    journal = journal_at(tmp_path)
    _queue(journal, "run-a", "m1")
    _queue(journal, "run-a", "m2")
    _queue(journal, "run-a", "PATCH", method="PATCH")
    server = _PerRunServer(fail_once={("run-a", "m1")})

    first = drain(journal, client_factory=lambda ctx: server)
    assert first.delivered == 0 and set(first.stalled_runs) == {"run-a"}
    second = drain(journal, client_factory=lambda ctx: server)
    assert second.delivered == 3 and second.clean
    assert server.sent == [("run-a", "m1"), ("run-a", "m2"), ("run-a", "PATCH")]


def test_a_deep_backlog_does_not_starve_a_new_run(tmp_path):
    """The lanes take turns: B's one op, queued behind A's 100, is among the
    first two delivered rather than the 101st."""
    journal = journal_at(tmp_path)
    for n in range(100):
        _queue(journal, "run-a", f"a{n}")
    _queue(journal, "run-b", "b0")
    server = _PerRunServer()

    report = drain(journal, client_factory=lambda ctx: server)

    assert report.delivered == 101
    assert ("run-b", "b0") in server.sent[:2], server.sent[:3]
    assert [label for run, label in server.sent if run == "run-a"] == [f"a{n}" for n in range(100)]


def test_an_unreachable_server_ends_the_pass_for_every_run(tmp_path):
    """The control for lanes: a connect failure says the SERVER is down, not
    one run. Trying every run's head op would wait one connect timeout per
    run, so the pass still stops at the first."""
    journal = journal_at(tmp_path)
    for run in ("run-a", "run-b", "run-c"):
        _queue(journal, run, "x")
    attempts = []
    server = _PerRunServer(unreachable=True)
    real = server.transport.request

    def counting(*a, **k):
        attempts.append(a)
        return real(*a, **k)

    server.transport.request = staticmethod(counting)
    report = drain(journal, client_factory=lambda ctx: server)

    assert len(attempts) == 1
    assert report.unreachable and report.stopped_transient and report.stalled_runs == {}
    assert report.remaining == 3


def test_runs_being_backed_off_are_not_attempted(tmp_path):
    """`skip_runs`: the worker's per-run backoff. A skipped run's ops are left
    alone this pass; nobody else's are."""
    journal = journal_at(tmp_path)
    _queue(journal, "run-a", "a1")
    _queue(journal, "run-b", "b1")
    server = _PerRunServer()

    report = drain(journal, client_factory=lambda ctx: server, skip_runs={"run-a"})

    assert server.sent == [("run-b", "b1")]
    assert report.remaining == 1 and not report.stopped_transient


def test_a_barrier_drain_still_stops_on_its_runs_failure(tmp_path):
    """`run_ref=` (finish()'s barrier) is one lane: a transient failure stops
    it in place, as before, and never touches another run."""
    journal = journal_at(tmp_path)
    _queue(journal, "run-a", "a1")
    _queue(journal, "run-a", "a2")
    _queue(journal, "run-b", "b1")
    server = _PerRunServer(fail_once={("run-a", "a1")})

    report = drain(journal, client_factory=lambda ctx: server, run_ref="run-a")

    assert report.stopped_transient and report.delivered == 0 and server.sent == []


def test_a_stalled_run_backs_off_on_its_own(tmp_path):
    """`LaneBackoff`: a stalled run waits (at least its Retry-After), doubling
    while it keeps failing; a run that delivers starts over; other runs are
    never skipped on its account."""
    from probe.sdk.journal import DrainReport, LaneBackoff, LaneStall

    lanes = LaneBackoff(ceiling=300.0)
    stalled = DrainReport(stalled_runs={"run-a": LaneStall("503", retry_after=None)})
    lanes.record(stalled, now=0.0)
    assert lanes.skip(now=1.0) == {"run-a"} and lanes.skip(now=2.5) == set()
    lanes.record(stalled, now=3.0)
    assert lanes.skip(now=6.5) == {"run-a"} and lanes.skip(now=7.5) == set(), "doubled"
    lanes.record(DrainReport(stalled_runs={"run-a": LaneStall("503", retry_after=30.0)}), now=8.0)
    assert lanes.skip(now=37.0) == {"run-a"}, "Retry-After lengthens the wait"
    lanes.record(DrainReport(progressed_runs={"run-a"}), now=40.0)
    assert lanes.skip(now=40.0) == set() and lanes.next_wake(now=40.0) is None


def test_the_worker_wakes_early_for_another_runs_new_op(tmp_path):
    """A worker whose queue holds only a backing-off run sleeps until that run
    may be tried again, but an op queued meanwhile by ANOTHER run ends the
    sleep; one from the backing-off run does not."""
    import threading
    import time as _time

    from probe.sdk import outbox_worker
    from probe.sdk.journal import DrainReport, LaneBackoff, LaneStall

    journal = journal_at(tmp_path)
    _queue(journal, "run-a", "a1")
    lanes = LaneBackoff(ceiling=300.0)
    lanes.record(DrainReport(stalled_runs={"run-a": LaneStall("503", retry_after=60.0)}))
    seen = outbox_worker._queued_names(journal)

    def later(run):
        _time.sleep(0.3)
        _queue(journal, run, "late")

    writer = threading.Thread(target=later, args=("run-a",))
    writer.start()
    started = _time.monotonic()
    outbox_worker._sleep_until_new_work(journal, seen, lanes, 2.5)
    writer.join()
    assert _time.monotonic() - started >= 2.4, "the backing-off run's own op does not wake it"

    writer = threading.Thread(target=later, args=("run-b",))
    writer.start()
    started = _time.monotonic()
    outbox_worker._sleep_until_new_work(journal, seen, lanes, 30.0)
    writer.join()
    assert _time.monotonic() - started < 10.0, "another run's op ends the sleep"


# -- plan 1.6, review of #2051 -------------------------------------------------


def test_an_expired_backoff_says_nothing_about_when_to_look_next():
    """MED-HIGH: `next_wake` took the minimum over every entry, expired ones
    included, so a run whose wait was over kept it at 0 and the worker spun."""
    from probe.sdk.journal import DrainReport, LaneBackoff, LaneStall

    lanes = LaneBackoff(ceiling=300.0)
    lanes.record(DrainReport(stalled_runs={"A": LaneStall("503", retry_after=5.0)}), now=0.0)
    lanes.record(DrainReport(stalled_runs={"C": LaneStall("503", retry_after=120.0)}), now=10.0)
    assert lanes.next_wake(now=10.0) == pytest.approx(120.0)
    assert lanes.skip(now=10.0) == {"C"}


def test_a_run_with_nothing_queued_is_forgotten():
    """Its ops left through another drainer (its own `finish()`): the entry
    must not linger."""
    from probe.sdk.journal import DrainReport, LaneBackoff, LaneStall

    lanes = LaneBackoff(ceiling=300.0)
    lanes.record(DrainReport(stalled_runs={"A": LaneStall("503", retry_after=60.0)}), now=0.0)
    lanes.record(DrainReport(queued_runs={"B"}), now=1.0)
    assert lanes.skip(now=1.0) == set() and lanes.next_wake(now=1.0) is None


def test_a_run_that_delivers_and_stalls_in_one_pass_does_not_climb():
    """LOW-MED: a busy run answering `Retry-After: 1` to every other write
    climbed 2, 4, ... 300 s while it was delivering."""
    from probe.sdk.journal import DrainReport, LaneBackoff, LaneStall

    lanes = LaneBackoff(ceiling=300.0)
    for t in range(0, 50, 5):
        lanes.record(
            DrainReport(
                progressed_runs={"A"}, stalled_runs={"A": LaneStall("503", retry_after=1.0)}
            ),
            now=float(t),
        )
        assert lanes.next_wake(now=float(t)) == pytest.approx(2.0), t


def test_a_parked_runs_ops_are_not_parsed_again_every_pass(tmp_path, monkeypatch):
    """MED: a worker delivering one run while another backs off re-parsed the
    parked run's whole backlog every pass. Unchanged, unattempted op files
    come from the pass cache."""
    journal = journal_at(tmp_path)
    for n in range(50):
        _queue(journal, "run-c", f"c{n}")
    _queue(journal, "run-b", "b0")
    server = _PerRunServer()
    drain(journal, client_factory=lambda ctx: server, skip_runs={"run-c"})
    _queue(journal, "run-b", "b1")
    parsed = []
    real_loads = json.loads
    monkeypatch.setattr(json, "loads", lambda text, *a, **k: (parsed.append(1), real_loads(text, *a, **k))[1])

    drain(journal, client_factory=lambda ctx: server, skip_runs={"run-c"})

    assert server.sent[-1] == ("run-b", "b1")
    assert len(parsed) <= 5, f"{len(parsed)} op files parsed for one new op"


def test_the_pass_cache_keeps_a_bounded_number_of_bytes(tmp_path, monkeypatch):
    """The parse cache outlives the pass, so on a training node the exporter
    held every parked op parsed: 58 MB at 20k one-point ops. It keeps only the
    first `SCAN_CACHE_MAX_BYTES` of op files; the rest are parsed again each
    pass, and every op is still queued."""
    from probe.sdk import journal as journal_mod

    journal = journal_at(tmp_path)
    for n in range(50):
        _queue(journal, "run-c", f"c{n}")
    files = sorted(journal.ops_dir.glob("*.json"))
    cap = sum(path.stat().st_size for path in files[:10])
    monkeypatch.setattr(journal_mod, "SCAN_CACHE_MAX_BYTES", cap)
    server = _PerRunServer()

    drain(journal, client_factory=lambda ctx: server, skip_runs={"run-c"})

    kept = journal._scan_cache
    assert sorted(kept) == [path.name for path in files[:10]], "the oldest, up to the cap"
    assert sum((journal.ops_dir / name).stat().st_size for name in kept) <= cap
    parsed = []
    real_loads = json.loads
    monkeypatch.setattr(json, "loads", lambda text, *a, **k: (parsed.append(1), real_loads(text, *a, **k))[1])

    drain(journal, client_factory=lambda ctx: server, skip_runs={"run-c"})

    # The 40 op files past the cap, plus the pass's own status/producer reads.
    assert 40 <= len(parsed) <= 44, f"{len(parsed)} parsed; only the ops past the cap should be"
    assert len(journal.pending()) == 50 and server.sent == []


def test_a_server_that_accepts_and_hangs_ends_the_pass_at_the_second_timeout(tmp_path):
    """LOW: a response lost after sending is per run (it may be that op), so a
    hung-after-accept server cost one read timeout per run per pass, holding
    the drain lock. The second in one pass stops it."""
    journal = journal_at(tmp_path)
    for run in ("run-a", "run-b", "run-c", "run-d"):
        _queue(journal, run, "x")
    attempts = []

    class _Hung:
        class transport:  # noqa: N801
            @staticmethod
            def request(method, path, **kw):
                attempts.append(path)
                raise errors.TransportError(f"{method} {path}: ReadTimeout")

        def close(self):
            pass

    report = drain(journal, client_factory=lambda ctx: _Hung())

    assert len(attempts) == 2 and report.unreachable and report.remaining == 4


def test_a_closed_port_is_unreachable_through_the_real_transport(tmp_path):
    """The `unreachable` flag, set by the real transport on a connect failure
    (not by a test double): the pass stops for every run."""
    import socket

    from probe.sdk.config import Settings
    from probe.sdk.transport import Transport

    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        port = sock.getsockname()[1]  # closed again once the block ends
    url = f"http://127.0.0.1:{port}"
    settings = Settings(base_url=url, token="probe_pat_test", ingest_token=None, hmac_secret=None)
    transport = Transport(settings, max_retries=0)
    with pytest.raises(errors.TransportError) as caught:
        transport.request("POST", "/v1/runs/r-1/metrics", json_body={"points": []})
    assert caught.value.unreachable is True

    class _Real:
        def __init__(self):
            self.transport = transport

        def close(self):
            pass

    journal = Journal(tmp_path / "outbox", context={"name": None, "base_url": url})
    for run in ("run-a", "run-b", "run-c"):
        _queue(journal, run, "x")
    report = drain(journal, client_factory=lambda ctx: _Real())
    assert report.unreachable and report.stalled_runs == {} and report.remaining == 3
    transport.close()


def test_waiting_on_a_scan_while_a_run_backs_off_does_not_end_the_worker(tmp_path, monkeypatch):
    """LOW (review of #2051): passes that skipped a backing-off run and found
    the rest held behind an upload being scanned counted toward the worker's
    20 idle looks, so it exited and threw the backoff away."""
    from probe.sdk import outbox_worker
    from probe.sdk.journal import DrainReport, LaneStall

    journal = journal_at(tmp_path)
    journal._ensure()
    passes = []

    def fake_drain(j, **kw):
        passes.append(kw.get("skip_runs"))
        if len(passes) <= 25:
            return DrainReport(
                held_back=1,
                remaining=2,
                stalled_runs={"run-a": LaneStall("503", retry_after=60.0)} if len(passes) == 1 else {},
                queued_runs={"run-a", "run-b"},
            )
        return DrainReport(remaining=0, queued_runs=set())

    monkeypatch.setattr("probe.sdk.journal.drain", fake_drain)
    monkeypatch.setattr(outbox_worker.time, "sleep", lambda s: None)
    assert outbox_worker.run(str(journal.dir)) == 0
    assert len(passes) >= 26, f"the worker gave up after {len(passes)} passes"
    assert passes[1] == {"run-a"}, "run-a stayed in its backoff"


# -- plan 1.11: queue format versioning ----------------------------------------


def _queue_kind(journal, run, kind, **extra):
    journal.append_http("POST", f"/v1/runs/{run}/metrics", {"label": kind})
    path, op = sorted(journal.pending(), key=lambda item: item[0].name)[-1]
    op["kind"] = kind
    op.update(extra)
    path.write_text(json.dumps(op))


def test_a_held_kind_holds_only_its_own_run(tmp_path):
    """Held in its run's lane, in order: the run's later ops wait behind it
    (its close must not overtake it), other runs deliver -- and a day past the
    transient budget it is still queued, not dead-lettered."""
    journal = journal_at(tmp_path)
    # A kind no release knows yet (`multipart_upload` was the example until plan
    # (g) made it real).
    _queue_kind(journal, "run-a", "tensor_stream", first_failed_at=0.0, attempts=99)
    _queue(journal, "run-a", "PATCH", method="PATCH")
    _queue(journal, "run-b", "b1")
    server = _PerRunServer()

    report = drain(journal, client_factory=lambda ctx: server)

    assert server.sent == [("run-b", "b1")]
    assert set(report.stalled_runs) == {"run-a"} and "newer" in report.stalled_runs["run-a"].error
    assert journal.failed() == [] and len(journal.pending()) == 2


def _hold_lease(journal):
    """Stand in for a live worker: hold its lease from this process."""
    from probe._shared import oscompat

    from probe.sdk import outbox_worker

    journal._ensure()
    handle = open(outbox_worker._lease_path(journal), "a+")
    oscompat.flock(handle.fileno(), oscompat.LOCK_EX | oscompat.LOCK_NB)
    return handle


def test_what_the_live_worker_delivers(tmp_path):
    """No worker: anything goes (the next kick spawns one of this version).
    A worker with no caps file predates them: only the kinds every release
    knows. A caps file from a live process: what it says. A caps file whose
    process is gone was left by a killed worker: the legacy set again."""
    from probe.sdk import outbox_worker
    from probe.sdk.journal import OP_KINDS

    journal = journal_at(tmp_path)
    journal._ensure()
    assert outbox_worker.live_worker_kinds(str(journal.dir)) is None
    lease = _hold_lease(journal)
    try:
        assert outbox_worker.live_worker_kinds(str(journal.dir)) == outbox_worker._LEGACY_KINDS
        caps = outbox_worker._caps_path(journal)
        caps.write_text(json.dumps({"kinds": ["http", "multipart_upload"], "pid": os.getpid()}))
        assert outbox_worker.live_worker_kinds(str(journal.dir)) == {"http", "multipart_upload"}
        caps.write_text(json.dumps({"kinds": ["multipart_upload"], "pid": 2**22 + 12345}))
        assert outbox_worker.live_worker_kinds(str(journal.dir)) == outbox_worker._LEGACY_KINDS
    finally:
        lease.close()
    # `create_run` (plan 2.12) lives only in offline queues, which only `probe
    # sync` drains: no worker, old or new, ever meets it there.
    # `multipart_upload` (plan (g)) is the first kind an older worker can
    # meet: its producer asks `ready_for` and parks it until one can deliver it.
    assert OP_KINDS == outbox_worker._LEGACY_KINDS | {"create_run", "multipart_upload"}, (
        "a new kind must be added to OP_KINDS only"
    )


def test_a_new_kind_waits_for_a_worker_that_knows_it(tmp_path):
    """`ready_for`: with a live worker that does not know the kind, the answer
    is no and a stop file asks that worker to step aside; a kind it knows
    (and no worker at all) is yes, and leaves no stop file."""
    from probe.sdk import outbox_worker

    journal = journal_at(tmp_path)
    journal._ensure()
    assert outbox_worker.ready_for("multipart_upload", str(journal.dir)) is True
    lease = _hold_lease(journal)
    try:
        assert outbox_worker.ready_for("http", str(journal.dir)) is True
        assert not outbox_worker._stop_path(journal).exists()
        assert outbox_worker.ready_for("multipart_upload", str(journal.dir)) is False
        assert outbox_worker.ready_for("tensor_stream", str(journal.dir)) is False
        stop = json.loads(outbox_worker._stop_path(journal).read_text())
        assert stop == {"kinds": ["multipart_upload", "tensor_stream"]}
    finally:
        lease.close()


def test_a_worker_steps_aside_only_for_a_kind_it_lacks(tmp_path):
    """The stop file is consumed either way, so the worker that replaces an old
    one does not exit on the same request."""
    from probe.sdk import outbox_worker

    journal = journal_at(tmp_path)
    journal._ensure()
    stop = outbox_worker._stop_path(journal)
    stop.write_text(json.dumps({"kinds": ["http"]}))
    assert outbox_worker._asked_to_stop(journal) is False and not stop.exists()
    stop.write_text(json.dumps({"kinds": ["tensor_stream"]}))
    assert outbox_worker._asked_to_stop(journal) is True and not stop.exists()
    # Plan (g): a kind this release knows is not a reason to step aside.
    stop.write_text(json.dumps({"kinds": ["multipart_upload"]}))
    assert outbox_worker._asked_to_stop(journal) is False and not stop.exists()
    assert outbox_worker._asked_to_stop(journal) is False, "nothing asked"


def test_a_kind_that_is_not_a_string_is_dead_lettered_not_a_crash(tmp_path):
    """Review of #2052: `kind not in OP_KINDS` with a list kind raised
    TypeError out of drain(), so every pass on the machine failed. A malformed
    kind is refused by `_execute` like before (a dead letter)."""
    journal = journal_at(tmp_path)
    _queue(journal, "run-a", "a1")
    _queue(journal, "run-b", "b1")
    path, op = sorted(journal.pending(), key=lambda item: item[0].name)[0]
    op["kind"] = ["multipart_upload"]
    path.write_text(json.dumps(op))
    server = _PerRunServer()

    report = drain(journal, client_factory=lambda ctx: server)

    assert report.dead_lettered == 1 and server.sent == [("run-b", "b1")]


def test_a_held_kind_says_why_and_a_runless_one_holds_only_itself(tmp_path):
    """Review of #2052: a held op recorded no reason (drainer.log said '?'),
    and one naming no run stalled the run-less lane: every other run-less
    write on the machine waited behind it."""
    journal = journal_at(tmp_path)
    journal.append_http("POST", "/v1/projects/p-1/notes", {"text": "first"})
    journal.append_http("POST", "/v1/projects/p-1/notes", {"text": "second"})
    path, op = sorted(journal.pending(), key=lambda item: item[0].name)[0]
    op["kind"] = "tensor_stream"
    path.write_text(json.dumps(op))
    sent = []

    class _Recording:
        class transport:  # noqa: N801
            @staticmethod
            def request(method, path, json_body=None, **kw):
                sent.append(json_body)

                class _Resp:
                    content = b""

                return _Resp()

        def close(self):
            pass

    report = drain(journal, client_factory=lambda ctx: _Recording())

    assert sent == [{"text": "second"}], "the run-less lane kept moving"
    assert report.unknown_kinds == 1 and any("tensor_stream" in e for e in report.errors)
    assert report.stalled_runs == {}


def test_the_refusal_recount_lists_the_queue_outside_the_append_lock(tmp_path, monkeypatch):
    """Follow-up to #2014: a write about to be refused at the cap counts the
    queue for real, and that SORTED listing ran under the cross-process append
    lock -- at 500k queued names, every other writer's `log()` waited on it.
    It is counted outside the lock now, unsorted."""
    import contextlib

    from probe.sdk import journal as journal_mod

    journal = journal_at(tmp_path)
    for n in range(5):
        journal.append_http("POST", "/v1/runs/r-1/metrics", {"points": [{"i": n}]})
    held = {"now": False}
    real_lock = journal_mod.file_lock

    @contextlib.contextmanager
    def watched(path):
        with real_lock(path):
            held["now"] = True
            try:
                yield
            finally:
                held["now"] = False

    listed_under_lock = []
    real_listdir = os.listdir

    def listing(path="."):
        if str(path) == str(journal.ops_dir):
            listed_under_lock.append(held["now"])
        return real_listdir(path)

    monkeypatch.setattr(journal_mod, "file_lock", watched)
    monkeypatch.setattr(os, "listdir", listing)
    assert journal._recount_pending() == 5
    assert listed_under_lock == [False]


# -- plan 1.2: coalesced drain -------------------------------------------------

RUN_A = "0b6f7a4e-1c2d-4e5f-8a9b-0c1d2e3f4a5b"
RUN_B = "1c7a8b5f-2d3e-4f60-9bac-1d2e3f4a5b6c"


class _MetricsServer:
    """Records each POST's points; refuses the ops named in ``bad`` (422) or
    everything while ``busy`` (503)."""

    def __init__(self, *, bad=(), busy=False):
        self.bad = set(bad)
        self.busy = busy
        self.posts: list[tuple[str, list]] = []
        outer = self

        class transport:  # noqa: N801
            @staticmethod
            def request(method, path, json_body=None, **kwargs):
                points = (json_body or {}).get("points") or []
                if outer.busy:
                    raise errors.ServerError("busy", status=503)
                if any(p.get("value") in outer.bad for p in points):
                    raise errors.ValidationError("bad point", status=422)
                outer.posts.append((path, [p.get("value") for p in points]))

                class _Resp:
                    content = b""

                return _Resp()

        self.transport = transport

    def close(self):
        pass


def _metric(journal, run, value, *, step=True, stamp=True, **body_extra):
    point = {"key": "loss", "kind": "model", "value": float(value)}
    if step:
        point["step_index"] = int(value)
    if stamp:
        point["wall_clock"] = "2026-09-27T12:00:00.000001+00:00"
    journal.append_http(
        "POST", f"/v1/runs/{run}/metrics", {"points": [point], **body_extra}
    )


def test_consecutive_metric_ops_go_in_one_post(tmp_path):
    """Plan 1.2: one POST per `log()` capped delivery at ~12-14 calls/s; a
    2,000-step run took 143 s to drain. A run's consecutive metric ops now
    ride in one POST, in order, and each op is still removed and tallied."""
    journal = journal_at(tmp_path)
    journal.register_producer("sdk:test")
    for value in range(10):
        _metric(journal, RUN_A, value)
    server = _MetricsServer()

    report = drain(journal, client_factory=lambda ctx: server)

    assert server.posts == [(f"/v1/runs/{RUN_A}/metrics", [float(v) for v in range(10)])]
    assert report.delivered == 10 and report.coalesced == 10 and report.clean
    assert journal.pending() == []
    (producer,) = journal.producer_report()
    assert producer["delivered"] == 10


def test_ops_that_differ_in_anything_but_points_are_not_merged(tmp_path):
    """The merge key is everything but the points: another epoch (a relaunch),
    another session, another run are separate POSTs; a terminal PATCH is not a
    metrics op and keeps its place behind them."""
    journal = journal_at(tmp_path)
    _metric(journal, RUN_A, 0, write_epoch=1)
    _metric(journal, RUN_A, 1, write_epoch=1)
    _metric(journal, RUN_A, 2, write_epoch=2)
    _metric(journal, RUN_A, 3, write_epoch=2)
    journal.append_http("PATCH", f"/v1/runs/{RUN_A}", {"status": "completed"})
    server = _MetricsServer()

    report = drain(journal, client_factory=lambda ctx: server)

    assert [values for _, values in server.posts] == [[0.0, 1.0], [2.0, 3.0], []]
    assert server.posts[-1][0] == f"/v1/runs/{RUN_A}"
    assert report.delivered == 5


def test_points_without_a_step_or_a_clock_drain_one_by_one(tmp_path):
    """The control for the merge rule: an unstepped point with no client clock
    takes the server's transaction time, and two of them in one transaction
    would collapse under the wall-clock dedupe index. Ops queued by releases
    before 1.4 look like that, so they keep one POST each."""
    journal = journal_at(tmp_path)
    for value in range(3):
        _metric(journal, RUN_A, value, step=False, stamp=False)
    server = _MetricsServer()

    report = drain(journal, client_factory=lambda ctx: server)

    assert [values for _, values in server.posts] == [[0.0], [1.0], [2.0]]
    assert report.delivered == 3 and report.coalesced == 0


def test_one_invalid_op_does_not_dead_letter_its_neighbours(tmp_path):
    """A 422 on a merged POST is bisected down to the op that caused it: that
    one is dead-lettered, the rest land, in order, in a handful of requests."""
    journal = journal_at(tmp_path)
    for value in range(16):
        _metric(journal, RUN_A, value)
    server = _MetricsServer(bad={11.0})
    calls = []
    real = server.transport.request

    def counting(*a, **k):
        calls.append(1)
        return real(*a, **k)

    server.transport.request = staticmethod(counting)

    report = drain(journal, client_factory=lambda ctx: server)

    delivered = [v for _, values in server.posts for v in values]
    assert delivered == [float(v) for v in range(16) if v != 11]
    assert report.dead_lettered == 1 and report.delivered == 15
    (_, dead), = journal.failed()
    assert dead["body"]["points"][0]["value"] == 11.0
    assert len(calls) <= 10, f"{len(calls)} requests to isolate one bad op among 16"


def test_a_503_on_a_merged_post_parks_the_run_in_place(tmp_path):
    """A transient failure of the merged POST is the head op's, as it would be
    alone: nothing is removed, the head is charged one attempt, its run waits,
    and the ops behind it are untouched."""
    journal = journal_at(tmp_path)
    for value in range(5):
        _metric(journal, RUN_A, value)
    _metric(journal, RUN_B, 100)
    server = _MetricsServer(busy=True)

    report = drain(journal, client_factory=lambda ctx: server)

    assert report.delivered == 0 and set(report.stalled_runs) >= {RUN_A}
    ops = [op for _, op in journal.pending()]
    assert len(ops) == 6
    attempts = [op["attempts"] for op in ops if op["run_ref"] == RUN_A]
    assert attempts == [1, 0, 0, 0, 0]


def test_a_merged_post_respects_the_point_cap(tmp_path, monkeypatch):
    from probe.sdk import journal as journal_mod

    monkeypatch.setattr(journal_mod, "MERGE_MAX_POINTS", 4)
    journal = journal_at(tmp_path)
    for value in range(10):
        _metric(journal, RUN_A, value)
    server = _MetricsServer()

    drain(journal, client_factory=lambda ctx: server)

    assert [len(values) for _, values in server.posts] == [4, 4, 2]


def test_two_runs_coalesce_in_their_own_lanes(tmp_path):
    """Batches never cross runs, and the lanes still take turns."""
    journal = journal_at(tmp_path)
    for value in range(3):
        _metric(journal, RUN_A, value)
    for value in range(100, 103):
        _metric(journal, RUN_B, value)
    for value in range(3, 6):
        _metric(journal, RUN_A, value)
    server = _MetricsServer()

    drain(journal, client_factory=lambda ctx: server)

    assert server.posts == [
        (f"/v1/runs/{RUN_A}/metrics", [float(v) for v in range(6)]),
        (f"/v1/runs/{RUN_B}/metrics", [100.0, 101.0, 102.0]),
    ]


class _PoisonServer:
    """Answers 500 to any POST carrying the poison value (a step past int64 or
    a key past the index row size does that on the real server), and
    ``refuse_all`` for everything, recording each request."""

    def __init__(self, *, poison=None, refuse_all=None):
        self.poison = poison
        self.refuse_all = refuse_all
        self.requests = 0
        self.landed: list[float] = []
        outer = self

        class transport:  # noqa: N801
            @staticmethod
            def request(method, path, json_body=None, **kwargs):
                outer.requests += 1
                if outer.refuse_all is not None:
                    raise outer.refuse_all
                values = [p.get("value") for p in (json_body or {}).get("points") or []]
                if outer.poison in values:
                    raise errors.ServerError("internal error", status=500)
                outer.landed.extend(values)

                class _Resp:
                    content = b""

                return _Resp()

        self.transport = transport

    def close(self):
        pass


def test_a_500_on_a_merged_post_is_split_to_find_the_op(tmp_path, monkeypatch):
    """Review of #2053 (HIGH): a 500 on a merged POST was pinned on the head
    and the batch stopped, so ops before the poison were dead-lettered in
    turn, 24 h each (~11 days to reach it at op 10 of 20). Now the batch is
    split: 0-9 land, the poison alone is charged and holds its run as it would
    unmerged, and once its budget runs out 11-19 land."""
    journal = journal_at(tmp_path)
    for value in range(20):
        _metric(journal, RUN_A, value)
    server = _PoisonServer(poison=10.0)

    drain(journal, client_factory=lambda ctx: server)

    assert server.landed == [float(v) for v in range(10)]
    pending = sorted(journal.pending(), key=lambda item: item[0].name)
    assert [op["body"]["points"][0]["value"] for _, op in pending] == [float(v) for v in range(10, 20)]
    assert [op["attempts"] for _, op in pending] == [1] + [0] * 9, "only the poison is charged"

    # A day of failures later the poison is dead-lettered, alone.
    path, op = pending[0]
    op.update(attempts=60, first_failed_at=0.0)
    path.write_text(json.dumps(op))
    drain(journal, client_factory=lambda ctx: server)

    assert [dead["body"]["points"][0]["value"] for _, dead in journal.failed()] == [10.0]
    assert server.landed == [float(v) for v in range(20) if v != 10]


def test_a_refusal_true_of_the_whole_batch_costs_one_request(tmp_path):
    """Review of #2053 (MED): a 409 fence (or a deleted run) refuses every op of
    a batch -- one run, one epoch by the merge key -- and bisecting it cost
    2n-1 requests (400 ops: 799). The batch is dead-lettered at once."""
    journal = journal_at(tmp_path)
    for value in range(400):
        _metric(journal, RUN_A, value)
    server = _PoisonServer(refuse_all=errors.ConflictError("write_epoch 1 is older"))

    report = drain(journal, client_factory=lambda ctx: server)

    assert server.requests == 1 and report.dead_lettered == 400 and journal.pending() == []


def test_a_merged_post_the_server_is_too_busy_for_stops_at_its_head(tmp_path):
    """The control: a 503 is not the batch's fault -- split it and every half
    503s too. The head is charged, as it would be alone, and nothing is split."""
    journal = journal_at(tmp_path)
    for value in range(8):
        _metric(journal, RUN_A, value)
    server = _PoisonServer(refuse_all=errors.ServerError("busy", status=503))

    drain(journal, client_factory=lambda ctx: server)

    assert server.requests == 1
    assert [op["attempts"] for _, op in sorted(journal.pending(), key=lambda i: i[0].name)] == [1] + [0] * 7


def test_coalesced_counts_only_ops_inside_multi_op_posts(tmp_path):
    journal = journal_at(tmp_path)
    for value in range(4):
        _metric(journal, RUN_A, value)
    server = _PoisonServer(poison=3.0)

    report = drain(journal, client_factory=lambda ctx: server)

    # [0,1] merged; [2] and [3] went alone while the batch was split.
    assert report.coalesced == 2 and server.landed == [0.0, 1.0, 2.0]


def test_what_the_server_cannot_store_is_dropped_before_it_is_queued(app, tmp_path):
    """Review of #2053: a step past int64 and a key past the index row size are
    500s on the server, retried for a day and holding the run's later writes.
    `log()` now drops them, warns once, and never raises."""
    import warnings

    from tests.conftest import open_run

    client = make_client(app, tmp_spool=tmp_path / "outbox", async_writes=True)
    run = open_run(client, experiment="guards")
    long_key = "k" * 3000  # over the 2,048-byte limit
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        run.log({"loss": 1.0}, step=2**63)
        run.log({"loss": 1.0}, step=2**63 + 1)
        run.log({"loss": 2.0, long_key: 3.0}, step=1)
        run.log({long_key: 4.0}, step=2)
    queued = [op["body"]["points"] for _, op in client.journal.pending() if "points" in op["body"]]
    keys = [point["key"] for points in queued for point in points]
    assert keys == ["loss"], keys
    messages = [str(w.message) for w in caught if str(w.message).startswith("probe: dropped")]
    assert len(messages) == 2, messages
    client.close()


# -- review of #2053, verify round -------------------------------------------------


def test_a_lost_answer_on_a_merged_post_is_not_split(tmp_path):
    """(a): an answer lost after sending was split, and each half waited out a
    read timeout (2 runs x 64 ops against a hung server: 14 requests). It now
    stops at the head, counting toward the pass's lost-answer limit: two runs,
    two requests, and the pass ends."""
    journal = journal_at(tmp_path)
    for value in range(64):
        _metric(journal, RUN_A, value)
        _metric(journal, RUN_B, 100 + value)
    server = _PoisonServer(refuse_all=errors.TransportError("POST /x: ReadTimeout"))

    report = drain(journal, client_factory=lambda ctx: server)

    assert server.requests == 2 and report.unreachable
    heads = [op for _, op in journal.pending() if op["attempts"]]
    assert len(heads) == 2, "each run's head charged once, and it goes alone next pass"


def test_a_failure_while_settling_a_batch_holds_the_run(tmp_path, monkeypatch):
    """(b): an error while settling a batch was swallowed and the run went on:
    its close went out while one of its writes was still queued."""
    import pathlib

    from probe.sdk import journal as journal_mod

    journal = journal_at(tmp_path)
    for value in range(4):
        _metric(journal, RUN_A, value)
    journal.append_http("PATCH", f"/v1/runs/{RUN_A}", {"status": "completed"})
    server = _PoisonServer(poison=2.0)
    real = journal_mod.write_text_atomic
    fired = []

    def flaky(path, text, **kw):
        if not fired and "ops" in pathlib.Path(path).parts and '"last_error"' in text:
            fired.append(path)
            raise OSError(28, "No space left on device")
        return real(path, text, **kw)

    monkeypatch.setattr(journal_mod, "write_text_atomic", flaky)
    patched = []
    real_request = server.transport.request

    def recording(method, path, **kw):
        patched.append(method)
        return real_request(method, path, **kw)

    server.transport.request = staticmethod(recording)
    drain(journal, client_factory=lambda ctx: server)

    assert fired and "PATCH" not in patched, "the close waited behind the unsettled write"


RUN_C = "2d8b9c60-3e4f-4a71-8cbd-2e3f4a5b6c7d"


def test_a_held_batch_stays_queued_whole_and_parks_its_run(tmp_path):
    """The seam #2041's `CredentialNotHere` lands in: a batch whose client
    this drainer must not build is held whole -- no attempt counted, nothing
    dead-lettered -- and its run's close waits behind it while other runs
    deliver. A lone op is held the same way. A hold is not a stall: no
    back-off follows it."""
    from probe.sdk.journal import OpHeldHere

    journal = journal_at(tmp_path)
    base = dict(journal.context or {})
    elsewhere = {**base, "name": "other-login", "principal": {"fingerprint": "fp-other"}}
    journal.context = elsewhere
    for value in range(3):
        _metric(journal, RUN_A, value)
    journal.append_http("PATCH", f"/v1/runs/{RUN_A}", {"status": "completed"})
    journal.append_http("PATCH", f"/v1/runs/{RUN_C}", {"status": "completed"})
    journal.context = base
    _metric(journal, RUN_B, 100)
    _metric(journal, RUN_B, 101)
    server = _MetricsServer()

    def factory(ctx):
        if (ctx or {}).get("principal"):
            raise OpHeldHere("its credential is not here")
        return server

    report = drain(journal, client_factory=factory)

    assert server.posts == [(f"/v1/runs/{RUN_B}/metrics", [100.0, 101.0])]
    held = [op for _, op in journal.pending()]
    assert sorted(op["run_ref"] for op in held) == sorted([RUN_A] * 4 + [RUN_C])
    assert all(op["attempts"] == 0 and not op.get("last_error") for op in held)
    assert journal.failed() == [] and report.dead_lettered == 0
    assert report.stalled_runs == {} and report.delivered == 2


def test_two_credentials_never_ride_in_one_post(tmp_path):
    """#2041 stamps the credential that queued a write into its context, and
    the context is in `_merge_key`: writes of one run queued under two
    credentials never share a POST, which would deliver one credential's
    points as the other's."""
    journal = journal_at(tmp_path)
    base = dict(journal.context or {})
    for value, fingerprint in [(0, "fp-a"), (1, "fp-a"), (2, "fp-b"), (3, "fp-b"), (4, "fp-a")]:
        journal.context = {**base, "principal": {"fingerprint": fingerprint}}
        _metric(journal, RUN_A, value)
    server = _MetricsServer()

    report = drain(journal, client_factory=lambda ctx: server)

    assert [values for _, values in server.posts] == [[0.0, 1.0], [2.0, 3.0], [4.0]]
    assert report.delivered == 5


@pytest.mark.parametrize("attempts", ["x", [1], {"n": 1}, True])
def test_a_malformed_attempt_count_does_not_break_the_drain(tmp_path, attempts):
    """(c): `int(op["attempts"])` on "x" raised ValueError out of drain(), so
    the worker crashed on every kick, machine-wide."""
    journal = journal_at(tmp_path)
    _metric(journal, RUN_A, 1)
    _metric(journal, RUN_B, 2)
    _metric(journal, RUN_A, 3)
    path, op = sorted(journal.pending(), key=lambda item: item[0].name)[0]
    op["attempts"] = attempts
    path.write_text(json.dumps(op))
    server = _PoisonServer()

    report = drain(journal, client_factory=lambda ctx: server)

    assert report.delivered == 3 and sorted(server.landed) == [1.0, 2.0, 3.0]


def test_a_run_ref_that_is_not_a_string_does_not_break_the_drain(tmp_path):
    """Pre-existing, same class: a list `run_ref` raised TypeError (unhashable)."""
    journal = journal_at(tmp_path)
    _queue(journal, "run-a", "a1")
    _queue(journal, "run-b", "b1")
    path, op = sorted(journal.pending(), key=lambda item: item[0].name)[0]
    op["run_ref"] = ["run-a"]
    path.write_text(json.dumps(op))
    server = _PerRunServer()

    report = drain(journal, client_factory=lambda ctx: server)

    assert ("run-b", "b1") in server.sent and report.delivered == 2


def test_every_metric_door_drops_what_the_server_cannot_store(app, tmp_path):
    """(d): the step and key guard was in `Run.log` only. `Client.write` (which
    `log_derived*` and the W&B import use) and the journal's own door (the
    hardware rail's) apply it too, and the key limit is 2,048 bytes."""
    import warnings

    from probe.sdk import client as client_mod

    client_mod._UNSTORABLE_WARNED.clear()
    client = make_client(app, tmp_spool=tmp_path / "outbox", async_writes=True)
    fits = "k" * 2048
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        client.write(
            "POST",
            f"/v1/runs/{RUN_A}/metrics",
            {"points": [
                {"key": "ok", "value": 1.0, "step_index": 1},
                {"key": "big", "value": 1.0, "step_index": 2**63},
                {"key": fits, "value": 1.0, "step_index": 2},
                {"key": fits + "k", "value": 1.0, "step_index": 3},
            ]},
        )
        client.journal.append_http(
            "POST",
            f"/v1/runs/{RUN_B}/metrics",
            {"points": [{"key": "hw", "value": 1.0, "step_index": -(2**63) - 1}]},
        )
    queued = [op for _, op in client.journal.pending()]
    assert len(queued) == 1, "the all-unstorable direct append queued nothing"
    assert [p["key"] for p in queued[0]["body"]["points"]] == ["ok", fits]
    messages = [str(w.message) for w in caught if "cannot store" in str(w.message)]
    assert len(messages) == 2, messages
    client.close()


def test_the_worker_scrubs_with_the_cache_on(tmp_path, monkeypatch):
    """The detached worker re-scrubs every op it sends and ran with the scrub
    cache off, so a fresh worker scanned each point's constant keys again for
    every point: 7.1 s for 2,002 coalesced one-step writes, all of it inside
    the drain lock `finish()` waits on (0.9 s with the cache)."""
    from probe.sdk import outbox_worker, redaction
    from probe.sdk.journal import DrainReport

    monkeypatch.setattr(redaction, "_CACHE_ENABLED", False)
    monkeypatch.setenv("PROBE_TELEMETRY", "off")
    journal = Journal(
        str(tmp_path / "outbox"), context={"name": None, "base_url": "https://api.research.prbe.ai"}
    )
    journal.append_http("POST", "/v1/runs/r/metrics", {"k": 1})
    during = []

    def fake_drain(j, **kwargs):
        during.append(redaction._CACHE_ENABLED)
        for op in j.ops_dir.glob("*.json"):
            op.unlink()
        j.write_status()
        return DrainReport(delivered=1, remaining=0)

    monkeypatch.setattr("probe.sdk.journal.drain", fake_drain)
    monkeypatch.setattr(outbox_worker.time, "sleep", lambda s: None)
    assert outbox_worker.run(str(journal.dir)) == 0
    assert during and all(during)
