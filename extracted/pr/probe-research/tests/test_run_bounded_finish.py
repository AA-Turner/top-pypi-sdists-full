"""`Run.finish()`: one deadline, and it never raises over delivery (plan 0.2/0.6).

Parity F3/F3a (docs/2026-08-04-outbox-miles-parity.md) introduced the bounded
close: a run that cannot drain in time queues its terminal status BEHIND its
pending ops -- FIFO is the correctness guarantee: the run can never read
terminal ahead of its data -- stamped with the F3a accounting (real end time,
pending count, writing session), plus a best-effort "draining" beacon so the
dashboard shows intent instead of a phantom "running".

The SDK reliability plan (docs/2026-09-26-sdk-reliability-plan.md, 0.2 + 0.6)
makes that the DEFAULT: every close retries to one deadline (600 s,
`PROBE_FINISH_TIMEOUT_SEC` / ``flush_timeout=`` override), then defers; dead
letters warn and close the run marked ``probe_finish.dead_lettered``. Only
``strict=True`` still raises. It lands PR #1679's retry loop (Mahit) and
extends it.

REGRESSION CONTRACT (plan, eng review round 1, Section 3), asserted below:
  1. the terminal status is still queued behind the run's own data (FIFO);
  2. a run with undelivered or dead-lettered data never reads ``completed``
     without ``probe_finish.deferred`` or ``probe_finish.dead_lettered`` set;
  3. ``strict=True`` still raises.
"""

from __future__ import annotations

import fcntl
import http.server
import json
import re
import threading
import time
import uuid

import pytest

from probe.sdk import errors
from probe.sdk import run as run_module
from probe.sdk.run import Run
from probe.sdk.session_marker import WIZARD_HINT

from tests.conftest import make_client
from tests.test_outbox import seeded_run

BUSY = "concurrent telemetry write; retry this ingest batch"


@pytest.fixture(autouse=True)
def _isolated_config(monkeypatch, tmp_path):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(tmp_path / "config" / "probe.json"))
    monkeypatch.delenv("PROBE_TOKEN", raising=False)
    monkeypatch.delenv("PROBE_ASYNC", raising=False)
    monkeypatch.delenv("PROBE_FINISH_TIMEOUT_SEC", raising=False)


def _setup(app, tmp_path, **client_kwargs):
    run_id = seeded_run(app, tmp_path)
    client = make_client(app, tmp_spool=tmp_path / "outbox", async_writes=True, **client_kwargs)
    return run_id, client, Run(client, {"id": run_id})


def _fail_metrics(client, mp, exc=None):
    """Metrics POSTs fail; reads and PATCHes still reach the fake app -- the
    slow-drain shape, where the beacon CAN land."""
    original = client.transport.request
    exc = exc or errors.TransportError("net down")

    def selective(method, path, *a, **kw):
        if method == "POST" and path.endswith("/metrics"):
            raise exc
        return original(method, path, *a, **kw)

    mp.setattr(client.transport, "request", selective)


def _log(client, run_id, step=1):
    client.write(
        "POST",
        f"/v1/runs/{run_id}/metrics",
        {"points": [{"key": "loss", "kind": "model", "value": 1.0, "step_index": step}]},
    )


def _finish_block(row) -> dict:
    return (row.get("summary") or {}).get("probe_finish") or {}


# --------------------------------------------------------------------------
# The live bug (plan root cause 2): one 503 from a colliding write.
# --------------------------------------------------------------------------


def test_a_503_concurrent_telemetry_write_during_the_close_no_longer_raises(app, tmp_path):
    """Live: the hardware rail's write collided with the finish drain, the
    metric insert answered 503 `concurrent telemetry write`, and `finish()`
    raised on 4 of 6 ten-step runs. The same answer, through the real transport
    and the fake's production-shaped 503: the close retries and lands."""
    run_id, client, run = _setup(app, tmp_path)
    app.metrics_busy_next = 1  # the FIRST metric POST of the finish drain
    _log(client, run_id)

    result = run.finish()

    assert app.metrics_busy_next == 0, "the 503 was served"
    assert app.runs[run_id]["status"] == "completed"
    assert app.metric_points_posted[run_id], "the point landed on the retry"
    assert "probe_finish" not in (app.runs[run_id].get("summary") or {})
    assert result["status"] == "completed", "a clean close still returns the run row"
    assert client.journal.pending() == []
    client.close()


def test_a_503_that_outlasts_the_deadline_defers_and_lands_after_recovery(app, tmp_path):
    """The same 503 for longer than the close may wait: finish() RETURNS, the
    terminal status waits behind the data, and the run lands `completed` once
    the server recovers -- marked as a late close."""
    run_id, client, run = _setup(app, tmp_path)
    app.metrics_busy_next = 10_000
    _log(client, run_id)

    report = run.finish(flush_timeout=1.0)

    assert report["finish_queued"] is True
    assert app.runs[run_id]["status"] != "completed"
    app.metrics_busy_next = 0  # the server recovers
    assert client.flush() == 2
    row = app.runs[run_id]
    assert row["status"] == "completed"
    assert _finish_block(row)["deferred"] is True
    assert app.metric_points_posted[run_id]
    client.close()


def test_the_close_waits_at_least_what_retry_after_asks(app, tmp_path, monkeypatch):
    """A 503 carrying `Retry-After` (plan 0.4 adds one server-side) is retried
    no sooner than it asks, even though the loop's own first wait is 0.5 s."""
    run_id, client, run = _setup(app, tmp_path)
    app.metrics_busy_next = 1
    app.metrics_busy_retry_after = "1.5"
    _log(client, run_id)
    slept: list[float] = []
    real_sleep = time.sleep
    monkeypatch.setattr(run_module.time, "sleep", lambda s: (slept.append(s), real_sleep(0))[1])

    run.finish(flush_timeout=10.0)

    assert app.runs[run_id]["status"] == "completed"
    assert slept and max(slept) >= 1.5, slept
    client.close()


def test_retry_after_is_parsed_onto_the_error(app):
    """Delta-seconds and HTTP-date forms both reach `RosError.retry_after`."""
    from email.utils import formatdate

    client = make_client(app)
    run_id = seeded_run(app, None)
    app.metrics_busy_next = 2
    app.metrics_busy_retry_after = "7"
    with pytest.raises(errors.ServerError) as seconds:
        client.transport.request("POST", f"/v1/runs/{run_id}/metrics", json_body={"points": []})
    assert seconds.value.status == 503 and seconds.value.retry_after == 7.0
    app.metrics_busy_retry_after = formatdate(time.time() + 30, usegmt=True)
    with pytest.raises(errors.ServerError) as date:
        client.transport.request("POST", f"/v1/runs/{run_id}/metrics", json_body={"points": []})
    assert 25 <= date.value.retry_after <= 31
    app.metrics_busy_retry_after = None
    app.metrics_busy_next = 1
    with pytest.raises(errors.ServerError) as bare:
        client.transport.request("POST", f"/v1/runs/{run_id}/metrics", json_body={"points": []})
    assert bare.value.retry_after is None
    client.close()


# --------------------------------------------------------------------------
# The regression contract.
# --------------------------------------------------------------------------


def test_contract_terminal_status_is_queued_behind_the_runs_own_data(app, tmp_path, monkeypatch):
    run_id, client, run = _setup(app, tmp_path)
    _fail_metrics(client, monkeypatch)
    for step in (1, 2, 3):
        _log(client, run_id, step=step)

    report = run.finish(summary={"acc": 0.9}, flush_timeout=1.0)

    assert report["finish_queued"] is True and report["remaining"] == 4
    ops = [op for _, op in client.journal.pending()]
    assert [op["method"] for op in ops] == ["POST", "POST", "POST", "PATCH"], (
        "the close must sit BEHIND the run's data -- the ordering IS the barrier"
    )
    close = ops[-1]
    assert close["run_ref"] == run_id and close["body"]["status"] == "completed"
    accounting = close["body"]["summary"]["probe_finish"]
    assert accounting["deferred"] is True
    assert accounting["pending_at_exit"] == 3
    assert accounting["session_id"] == run.session_id
    assert close["body"]["summary"]["acc"] == 0.9
    assert app.runs[run_id]["status"] != "completed"
    client.close()


@pytest.mark.parametrize("shape", ["undelivered", "dead_lettered", "both"])
def test_contract_undelivered_or_dead_data_never_reads_completed_unmarked(
    app, tmp_path, monkeypatch, shape
):
    """Whatever the close could not deliver, a `completed` run carries the
    marker that says so -- on the RECORD, after the late drain lands it."""
    run_id, client, run = _setup(app, tmp_path)
    mp = pytest.MonkeyPatch()
    original = client.transport.request

    def selective(method, path, *a, **kw):
        body = kw.get("json_body") or {}
        # ANY point: the drain merges a run's consecutive metric writes into
        # one POST (plan 1.2), and a server refuses the whole request.
        steps = {point.get("step_index") for point in body.get("points") or []}
        if method == "POST" and path.endswith("/metrics") and steps:
            if 1 in steps and shape in ("dead_lettered", "both"):
                raise errors.ValidationError("bad point", status=422)
            if 2 in steps and shape in ("undelivered", "both"):
                raise errors.TransportError("net down")
        return original(method, path, *a, **kw)

    mp.setattr(client.transport, "request", selective)
    _log(client, run_id, step=1)
    _log(client, run_id, step=2)

    run.finish(flush_timeout=1.0)
    mp.undo()  # the network comes back; the 422 stays a 422 (it is dead-lettered)
    client.flush()

    row = app.runs[run_id]
    assert row["status"] == "completed"
    block = _finish_block(row)
    if shape in ("undelivered", "both"):
        assert block.get("deferred") is True
    if shape in ("dead_lettered", "both"):
        assert block.get("dead_lettered") == 1
    assert block.get("deferred") or block.get("dead_lettered"), block
    client.close()


def test_contract_strict_true_still_raises_on_undelivered_data(app, tmp_path, monkeypatch):
    run_id, client, run = _setup(app, tmp_path)
    _fail_metrics(client, monkeypatch)
    _log(client, run_id)

    with pytest.raises(errors.RosError, match="not closed"):
        run.finish(strict=True, flush_timeout=0.5)

    assert app.runs[run_id]["status"] != "completed"
    assert [op["method"] for _, op in client.journal.pending()] == ["POST"], (
        "a strict refusal queues no close"
    )
    client.close()


def test_contract_strict_true_still_raises_on_dead_letters_at_once(app, tmp_path, monkeypatch):
    """A dead letter refuses a strict close IMMEDIATELY, without waiting out
    the budget: retrying bets on "not yet", and a dead letter is the drain
    having concluded "not ever" (PR #1679's rule)."""
    run_id, client, run = _setup(app, tmp_path)
    _fail_metrics(client, monkeypatch, exc=errors.ValidationError("bad", status=422))
    _log(client, run_id)

    started = time.monotonic()
    with pytest.raises(errors.RosError, match="dead-lettered"):
        run.finish(strict=True, flush_timeout=30)
    assert time.monotonic() - started < 5
    assert app.runs[run_id]["status"] != "completed"
    client.close()


def test_a_strict_client_makes_a_strict_close(app, tmp_path, monkeypatch):
    """`strict=None` resolves the way every other write resolves it: from the
    client's `fail_open`."""
    run_id, client, run = _setup(app, tmp_path, fail_open=False)
    _fail_metrics(client, monkeypatch)
    # A strict client's own writes go out synchronously and raise, so queue the
    # undeliverable write the way a crashed predecessor would have left it.
    client.journal.append_http(
        "POST",
        f"/v1/runs/{run_id}/metrics",
        {"points": [{"key": "loss", "kind": "model", "value": 1.0, "step_index": 1}]},
        run_ref=run_id,
    )
    with pytest.raises(errors.RosError, match="not closed"):
        run.finish(flush_timeout=0.3)
    client.close()


# --------------------------------------------------------------------------
# Dead letters close the run, marked.
# --------------------------------------------------------------------------


def test_a_close_with_nowhere_to_record_it_warns_instead_of_raising(
    app, tmp_path, monkeypatch
):
    """The server does not take the data in time AND the outbox cannot take
    the close (a read-only mount): nothing can record the verdict. The close
    says so and returns; it does not turn a finished script into a crash."""
    import errno

    from probe.sdk import journal as journal_module

    run_id, client, run = _setup(app, tmp_path)
    _log(client, run_id)
    _fail_metrics(client, monkeypatch)
    root = str(client.journal.dir)
    real_write = journal_module.write_text_atomic

    def read_only(path, *a, **k):
        if str(path).startswith(root):
            raise OSError(errno.EROFS, "Read-only file system", str(path))
        return real_write(path, *a, **k)

    monkeypatch.setattr(journal_module, "write_text_atomic", read_only)

    with pytest.warns(UserWarning, match="could not be closed"):
        report = run.finish(flush_timeout=0.5)

    assert report["finish_queued"] is False and report["close_unrecorded"] is True
    assert app.runs[run_id]["status"] != "completed", "no false claim of a close"
    client.close()


def test_dead_letters_warn_and_close_the_run_marked(app, tmp_path, monkeypatch):
    run_id, client, run = _setup(app, tmp_path)
    _fail_metrics(client, monkeypatch, exc=errors.ValidationError("bad", status=422))
    _log(client, run_id)

    with pytest.warns(UserWarning, match="dead-lettered"):
        result = run.finish(flush_timeout=30)

    row = app.runs[run_id]
    assert row["status"] == "completed"
    assert _finish_block(row)["dead_lettered"] == 1
    assert result["status"] == "completed"
    assert len(client.journal.failed()) == 1, "the dead letter stays for `probe outbox retry`"
    client.close()


def test_default_finish_defers_and_warns_instead_of_raising(app, tmp_path, monkeypatch):
    run_id, client, run = _setup(app, tmp_path)
    _fail_metrics(client, monkeypatch)
    _log(client, run_id)

    with pytest.warns(UserWarning, match="still queued on disk"):
        report = run.finish()  # the suite's default deadline (conftest), not 600 s

    assert report["finish_queued"] is True
    assert app.runs[run_id]["status"] != "completed"
    assert [op["method"] for _, op in client.journal.pending()] == ["POST", "PATCH"]
    client.close()


def test_the_default_deadline_is_600_seconds(monkeypatch):
    import inspect

    # The suite shortens it (conftest); the shipped value is the source's.
    assert "\nFINISH_TIMEOUT_DEFAULT_SECONDS = 600.0\n" in inspect.getsource(run_module)
    monkeypatch.setattr(run_module, "FINISH_TIMEOUT_DEFAULT_SECONDS", 600.0)
    assert Run._resolve_finish_timeout(None) == 600.0
    monkeypatch.setenv("PROBE_FINISH_TIMEOUT_SEC", "42")
    assert Run._resolve_finish_timeout(None) == 42.0
    assert Run._resolve_finish_timeout(7) == 7.0
    assert Run._resolve_finish_timeout(-1) == 0.0


def test_a_malformed_timeout_warns_and_uses_the_default(monkeypatch):
    monkeypatch.setattr(run_module, "FINISH_TIMEOUT_DEFAULT_SECONDS", 600.0)
    monkeypatch.setenv("PROBE_FINISH_TIMEOUT_SEC", "soon")
    with pytest.warns(UserWarning, match="PROBE_FINISH_TIMEOUT_SEC"):
        assert Run._resolve_finish_timeout(None) == pytest.approx(600.0)


# --------------------------------------------------------------------------
# The bounded close (F3/F3a), now the only close.
# --------------------------------------------------------------------------


def test_deferred_finish_lands_in_order_after_recovery(app, tmp_path):
    run_id, client, run = _setup(app, tmp_path)
    mp = pytest.MonkeyPatch()
    _fail_metrics(client, mp)
    _log(client, run_id)
    report = run.finish(flush_timeout=1.0)
    assert "draining" in app.runs[run_id]["tags"], "the beacon marked intent"
    assert report["finish_queued"] is True

    mp.undo()  # the network comes back
    assert client.flush() == 2
    assert client.journal.pending() == []
    row = app.runs[run_id]
    assert row["status"] == "completed"
    assert row["summary"]["probe_finish"]["deferred"] is True
    assert "draining" not in row["tags"], "the queued close restores the tags"
    assert app.metric_points_posted[run_id], "data landed BEFORE the flip"
    client.close()


def test_bounded_finish_that_drains_in_time_closes_normally(app, tmp_path):
    run_id, client, run = _setup(app, tmp_path)
    _log(client, run_id)

    run.finish(flush_timeout=5.0)

    # The metric drained inside the deadline, so finish() closes the run
    # SYNCHRONOUSLY and hands back the row (ProSeCo, 2026-08-19: the close used
    # to be journaled like any other async write, which left finish() returning
    # None and the run reading "running" until some later drain).
    #
    # FIFO still holds, which is what makes the sync close correct here rather
    # than a shortcut: the run's own data is already delivered, so a close that
    # goes straight to the network cannot overtake it.
    assert client.journal.pending() == []
    assert app.runs[run_id]["status"] == "completed"
    assert "probe_finish" not in (app.runs[run_id].get("summary") or {})
    client.close()


def test_beacon_failure_is_silent_when_the_network_is_fully_down(app, tmp_path, monkeypatch):
    run_id, client, run = _setup(app, tmp_path)
    _log(client, run_id)

    def down(*a, **kw):
        raise errors.TransportError("network unreachable")

    monkeypatch.setattr(client.transport, "request", down)
    report = run.finish(flush_timeout=0.5)

    assert report["finish_queued"] is True
    close = [op for _, op in client.journal.pending()][-1]
    assert "tags" not in close["body"], "no beacon -> nothing to restore"
    assert "draining" not in (app.runs[run_id].get("tags") or [])
    client.close()


def test_env_timeout_bounds_the_close(app, tmp_path, monkeypatch):
    run_id, client, run = _setup(app, tmp_path)
    _fail_metrics(client, monkeypatch)
    _log(client, run_id)
    monkeypatch.setenv("PROBE_FINISH_TIMEOUT_SEC", "0.3")

    started = time.monotonic()
    report = run.finish()

    assert time.monotonic() - started < 2.0
    assert report["finish_queued"] is True
    assert app.runs[run_id]["status"] != "completed"
    client.close()


def test_zero_waits_for_nothing(app, tmp_path, monkeypatch):
    """`flush_timeout=0`: no request is attempted and nothing is charged to
    the op; the close is queued behind the data for the detached worker."""
    run_id, client, run = _setup(app, tmp_path)
    _log(client, run_id)
    before = len(app.requests)

    report = run.finish(flush_timeout=0)

    assert report["finish_queued"] is True
    assert len(app.requests) == before, "a zero deadline sends nothing"
    ops = [op for _, op in client.journal.pending()]
    assert [op["method"] for op in ops] == ["POST", "PATCH"]
    assert ops[0]["attempts"] == 0 and "first_failed_at" not in ops[0], (
        "our own deadline is not the op's failure"
    )
    client.close()


# --------------------------------------------------------------------------
# PR #1679 (Mahit): the close retries a blip, with backoff, bounded.
# --------------------------------------------------------------------------


def _fail_metrics_n_times(client, mp, run_id, times):
    """The blip shape: the first `times` metric POSTs for `run_id` fail, then
    the network comes back on its own."""
    original = client.transport.request
    state = {"left": times}

    def selective(method, path, *a, **kw):
        if method == "POST" and path == f"/v1/runs/{run_id}/metrics" and state["left"] > 0:
            state["left"] -= 1
            raise errors.TransportError("blip")
        return original(method, path, *a, **kw)

    mp.setattr(client.transport, "request", selective)
    return state


def test_a_transient_blip_no_longer_permanently_fails_a_run(app, tmp_path, monkeypatch):
    """The whole point of #1679. One `flush()` and a count meant a two-second
    blip was indistinguishable from data loss: the close was refused, and a run
    whose work had finished never closed -- over a write that was durable on
    disk and would have landed on the next attempt."""
    monkeypatch.setattr(run_module, "FINISH_TIMEOUT_DEFAULT_SECONDS", 30.0)
    run_id, client, run = _setup(app, tmp_path)
    _fail_metrics_n_times(client, monkeypatch, run_id, times=2)
    _log(client, run_id)

    run.finish()

    assert app.runs[run_id]["status"] == "completed"
    assert app.metric_points_posted[run_id], "the data landed on a retry"
    assert client.journal.pending() == []
    client.close()


def test_the_retry_is_bounded_and_then_it_defers(app, tmp_path, monkeypatch):
    """Retrying must not become hanging. A permanently unreachable endpoint
    ends the close inside the budget -- deferred, not raised."""
    run_id, client, run = _setup(app, tmp_path)
    _fail_metrics(client, monkeypatch)
    _log(client, run_id)

    started = time.monotonic()
    report = run.finish(flush_timeout=1.0)
    elapsed = time.monotonic() - started

    assert elapsed < 3, f"the budget did not bound the close ({elapsed:.1f}s)"
    assert report["finish_queued"] is True
    assert app.runs[run_id]["status"] != "completed"
    client.close()


def test_the_retry_backs_off_instead_of_polling(app, tmp_path, monkeypatch):
    """Waits come from `durable.backoff_delays`: 0.5 s doubling to a 4 s
    ceiling -- not the old fixed 0.25 s poll that spent 50 transient attempts
    (and so dead-lettered the data) in ~13 s."""
    run_id, client, run = _setup(app, tmp_path)
    _fail_metrics(client, monkeypatch)
    _log(client, run_id)
    slept: list[float] = []
    clock = {"now": time.monotonic()}
    monkeypatch.setattr(run_module.time, "monotonic", lambda: clock["now"])

    def advance(s):
        slept.append(s)
        clock["now"] += s

    monkeypatch.setattr(run_module.time, "sleep", advance)
    run.finish(flush_timeout=30)

    assert slept[:5] == [0.5, 1.0, 2.0, 4.0, 4.0], slept
    client.close()


def test_the_retry_does_not_drain_a_neighbour(app, tmp_path, monkeypatch):
    """The retry loop inherits the barrier's scoping: spinning to a deadline
    would otherwise spend this run's whole budget on someone else's op."""
    neighbour_id = seeded_run(app, tmp_path)
    mine_id = seeded_run(app, tmp_path)
    client = make_client(app, tmp_spool=tmp_path / "outbox", async_writes=True)
    mine = Run(client, {"id": mine_id})

    _fail_one_runs_metrics(client, monkeypatch, neighbour_id)
    _log(client, neighbour_id)
    _log(client, mine_id)

    mine.finish(flush_timeout=2.0)

    assert app.runs[mine_id]["status"] == "completed"
    assert [op["run_ref"] for _, op in client.journal.pending()] == [neighbour_id]
    client.close()


# --------------------------------------------------------------------------
# Run-scoped drain (#1678).
# --------------------------------------------------------------------------


def _fail_one_runs_metrics(client, mp, poisoned_run):
    """Only POSTs to `poisoned_run`'s metrics fail. Every other write lands."""
    original = client.transport.request

    def selective(method, path, *a, **kw):
        if method == "POST" and path == f"/v1/runs/{poisoned_run}/metrics":
            raise errors.TransportError("net down for this run only")
        return original(method, path, *a, **kw)

    mp.setattr(client.transport, "request", selective)


def test_close_ignores_another_runs_stuck_op(app, tmp_path, monkeypatch):
    """A neighbour's undeliverable op must not decide MY close.

    The journal is shared per directory across runs and `drain` is strict FIFO,
    so before the barrier was scoped one run's parked op held every op behind
    it -- and the NEXT run's finish() raised on a queue it had no stake in.
    Measured in production: a run whose own work recorded exit_code 0 was
    closed `failed` over two ops that were not its own.
    """
    neighbour_id = seeded_run(app, tmp_path)
    mine_id = seeded_run(app, tmp_path)
    client = make_client(app, tmp_spool=tmp_path / "outbox", async_writes=True)
    neighbour = Run(client, {"id": neighbour_id})
    mine = Run(client, {"id": mine_id})

    _fail_one_runs_metrics(client, monkeypatch, neighbour_id)
    # The neighbour's op is enqueued FIRST, so strict FIFO puts it in front of
    # mine -- the ordering that made this a cross-run block.
    _log(client, neighbour_id)
    _log(client, mine_id)

    result = mine.finish(flush_timeout=5.0)

    assert result.get("finish_queued") is not True, "my close must not be deferred"
    assert app.runs[mine_id]["status"] == "completed"
    assert app.metric_points_posted[mine_id], "my data had to land before the flip"
    assert [op["run_ref"] for _, op in client.journal.pending()] == [neighbour_id]
    assert app.runs[neighbour_id]["status"] != "completed"
    # And the neighbour's own strict close still refuses: its op really is stuck.
    with pytest.raises(errors.RosError, match="not closed"):
        neighbour.finish(strict=True, flush_timeout=0.5)
    client.close()


def test_machine_wide_flush_is_still_the_default(app, tmp_path):
    """`client.flush()` with no run_ref must keep draining EVERYTHING -- it is
    what `probe outbox drain` and post-outage recovery rely on. The barrier
    scoping is a new keyword, never a changed default."""
    run_a = seeded_run(app, tmp_path)
    run_b = seeded_run(app, tmp_path)
    client = make_client(app, tmp_spool=tmp_path / "outbox", async_writes=True)
    _log(client, run_a)
    _log(client, run_b)

    assert client.flush() == 2, "an unscoped flush delivers both runs' ops"
    assert client.journal.pending() == []

    # ...and the scoped form delivers only its own.
    _log(client, run_a)
    _log(client, run_b)
    assert client.flush(run_ref=run_a) == 1
    assert [op["run_ref"] for _, op in client.journal.pending()] == [run_b]
    client.close()


# --------------------------------------------------------------------------
# ONE deadline, propagated (plan 0.6).
# --------------------------------------------------------------------------


def test_the_drain_lock_wait_is_bounded_by_the_deadline(app, tmp_path):
    """A detached worker mid-pass holds the drain lock. The close used to BLOCK
    on it with no timeout; now it polls, and gives up at its deadline."""
    run_id, client, run = _setup(app, tmp_path)
    _log(client, run_id)
    holder = open(client.journal.drain_lock, "a+")
    fcntl.flock(holder.fileno(), fcntl.LOCK_EX)  # another open file: a real conflict
    try:
        started = time.monotonic()
        report = run.finish(flush_timeout=1.0)
        elapsed = time.monotonic() - started
    finally:
        fcntl.flock(holder.fileno(), fcntl.LOCK_UN)
        holder.close()

    assert elapsed < 3, f"the lock held the close past its deadline ({elapsed:.1f}s)"
    assert report["finish_queued"] is True
    assert [op["method"] for _, op in client.journal.pending()] == ["POST", "PATCH"]
    client.close()


def test_upload_promotion_is_inside_the_deadline(app, tmp_path, monkeypatch):
    run_id, client, run = _setup(app, tmp_path)
    seen: list[float] = []

    def promote(run_ref, *, timeout):
        seen.append(timeout)
        return []

    monkeypatch.setattr(client.journal, "promote_for_close", promote)
    run.finish(flush_timeout=2.0)
    assert seen and seen[0] <= 2.0, seen
    client.close()


def test_the_close_counts_only_its_own_ops_and_parses_each_once(app, tmp_path, monkeypatch):
    """The loop used to re-parse the whole machine-wide queue after every
    pass (plan 1.9 side note). A neighbour's 200 stuck ops are parsed once."""
    import pathlib

    neighbour_id = seeded_run(app, tmp_path)
    mine_id = seeded_run(app, tmp_path)
    client = make_client(app, tmp_spool=tmp_path / "outbox", async_writes=True)
    for step in range(200):
        _log(client, neighbour_id, step=step)
    _log(client, mine_id)

    counter = client.journal.run_ops(mine_id)
    reads: list[str] = []
    real_read_text = pathlib.Path.read_text

    def counting(self, *a, **kw):
        if self.parent == client.journal.ops_dir:
            reads.append(self.name)
        return real_read_text(self, *a, **kw)

    monkeypatch.setattr(pathlib.Path, "read_text", counting)
    assert len(counter.pending()) == 1
    first = len(reads)
    for _ in range(5):
        assert len(counter.pending()) == 1
    assert first == 201 and len(reads) == first, "later counts are listings only"
    client.close()


class _SlowMetricsServer:
    """A real HTTP server: run reads and PATCHes answer at once, a metric POST
    stalls for `stall` seconds. The fake app's MockTransport cannot show a
    request timeout; a socket can."""

    def __init__(self, stall: float, trickle: float = 0.0):
        self.stall = stall
        self.trickle = trickle
        self.run_id = str(uuid.uuid4())
        self.row = {"id": self.run_id, "status": "running", "tags": [], "summary": None}
        self.metric_posts = 0
        outer = self

        class Handler(http.server.BaseHTTPRequestHandler):
            def log_message(self, *a):
                pass

            def _send(self, code, body):
                data = json.dumps(body).encode()
                self.send_response(code)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                try:
                    self.wfile.write(data)
                except OSError:
                    pass

            def _body(self):
                length = int(self.headers.get("Content-Length") or 0)
                return json.loads(self.rfile.read(length) or b"{}")

            def do_GET(self):
                self._send(200, outer.row)

            def do_PATCH(self):
                outer.row.update({k: v for k, v in self._body().items() if k in ("status", "tags", "summary")})
                self._send(200, outer.row)

            def do_POST(self):
                self._body()
                if re.search(r"/metrics$", self.path):
                    outer.metric_posts += 1
                    time.sleep(outer.stall)
                    if outer.trickle:
                        data = b'{"inserted": 1}' + b" " * 40
                        self.send_response(200)
                        self.send_header("Content-Type", "application/json")
                        self.send_header("Content-Length", str(len(data)))
                        self.end_headers()
                        try:
                            for byte in data:  # one byte per `trickle` seconds
                                self.wfile.write(bytes([byte]))
                                self.wfile.flush()
                                time.sleep(outer.trickle)
                        except OSError:
                            pass
                        return
                    self._send(200, {"inserted": 1})
                    return
                self._send(200, {})

        self.server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.server.daemon_threads = True
        self.url = f"http://127.0.0.1:{self.server.server_address[1]}"
        threading.Thread(target=self.server.serve_forever, daemon=True).start()

    def close(self):
        self.server.shutdown()
        self.server.server_close()


def test_a_stalled_request_cannot_hold_the_close_past_its_deadline(tmp_path, monkeypatch):
    """Codex round 1: the timeout was checked only after a whole flush returned,
    so ONE stalled request held `finish(flush_timeout=10)` for 170 s live. Each
    request's timeout is now `min(remaining, transport timeout)`."""
    import httpx

    from probe.sdk.client import Client
    from probe.sdk.config import Settings
    from probe.sdk.journal import Journal
    from probe.sdk.transport import Transport

    monkeypatch.setenv("PROBE_AUTO_SNAPSHOT", "0")
    server = _SlowMetricsServer(stall=20.0)
    try:
        settings = Settings(base_url=server.url, token="ros_pat_deadbeef")
        transport = Transport(settings, client=httpx.Client(base_url=server.url, timeout=30.0))
        journal = Journal(tmp_path / "outbox", context={"name": None, "base_url": server.url})
        client = Client(settings=settings, transport=transport, journal=journal, async_writes=True)
        run = Run(client, dict(server.row))
        _log(client, server.run_id)

        started = time.monotonic()
        report = run.finish(flush_timeout=1.5)
        elapsed = time.monotonic() - started

        assert server.metric_posts >= 1, "the request was really in flight"
        assert elapsed < 4, f"a stalled request held the close for {elapsed:.1f}s"
        assert report["finish_queued"] is True
        ops = [op for _, op in client.journal.pending()]
        assert [op["method"] for op in ops] == ["POST", "PATCH"]
        # Cut short by OUR deadline after the request left: the attempt is
        # recorded (the server may have applied it), the failure is not.
        assert ops[0]["attempts"] == 1
        assert "first_failed_at" not in ops[0] and not ops[0].get("last_error")
        client.close()
    finally:
        server.close()


# --------------------------------------------------------------------------
# Review of #2011: the repros, flipped into permanent tests. Each passed while
# its defect was present; each now asserts the fixed behaviour.
# --------------------------------------------------------------------------


@pytest.mark.parametrize("patch_recovers", [True, False])
def test_a_data_dead_letter_is_not_read_as_a_rejected_close(
    app, tmp_path, monkeypatch, patch_recovers
):
    """MED 2. A default close proceeds past DATA dead letters, so the settle
    step must judge the TERMINAL PATCH, not every dead letter of the run."""
    import warnings

    run_id, client, run = _setup(app, tmp_path)
    original = client.transport.request
    state = {"patch_fails": 1 if patch_recovers else 10_000}

    def selective(method, path, *a, **kw):
        if method == "POST" and path.endswith("/metrics"):
            raise errors.ValidationError("bad point", status=422)  # dead letter
        if method == "PATCH" and path == f"/v1/runs/{run_id}" and state["patch_fails"] > 0:
            state["patch_fails"] -= 1
            raise errors.TransportError("blip on the close PATCH")
        return original(method, path, *a, **kw)

    monkeypatch.setattr(client.transport, "request", selective)
    handoffs = []
    monkeypatch.setattr(client, "hand_off_delivery", lambda: handoffs.append(1))
    _log(client, run_id)

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        result = run.finish(flush_timeout=2.0)
    messages = [str(w.message) for w in caught]

    assert not any("terminal status was rejected" in m for m in messages), messages
    if patch_recovers:
        assert app.runs[run_id]["status"] == "completed"
        assert _finish_block(app.runs[run_id])["dead_lettered"] == 1
        assert result["finish_queued"] is False and result["remaining"] == 0
    else:
        (close,) = [op for _, op in client.journal.pending()]
        assert close["method"] == "PATCH"
        assert close["body"]["summary"]["probe_finish"]["dead_lettered"] == 1
        assert handoffs, "the queued close is handed to the worker"
        assert result["finish_queued"] is True and result["remaining"] == 1
    client.close()


def test_an_auth_block_defers_the_close_at_once(app, tmp_path, monkeypatch):
    """MED 1. A refused credential on this run's own pass returns immediately:
    only a login fixes it (main raised in 0.01 s; the PR waited the deadline)."""
    run_id, client, run = _setup(app, tmp_path)
    original = client.transport.request
    calls = {"n": 0}

    def selective(method, path, *a, **kw):
        if method == "POST" and path.endswith("/metrics"):
            calls["n"] += 1
            raise errors.AuthError("token revoked", status=401)
        return original(method, path, *a, **kw)

    monkeypatch.setattr(client.transport, "request", selective)
    _log(client, run_id)
    started = time.monotonic()
    with pytest.warns(UserWarning, match=re.escape(WIZARD_HINT)):
        report = run.finish(flush_timeout=30.0)
    elapsed = time.monotonic() - started

    assert elapsed < 3, f"an auth block held the close {elapsed:.1f}s"
    assert calls["n"] == 1
    assert report["finish_queued"] is True
    assert [op["method"] for _, op in client.journal.pending()] == ["POST", "PATCH"]
    client.close()


def test_an_auth_block_under_strict_raises_at_once(app, tmp_path, monkeypatch):
    run_id, client, run = _setup(app, tmp_path)
    _fail_metrics(client, monkeypatch, exc=errors.AuthError("revoked", status=401))
    _log(client, run_id)
    started = time.monotonic()
    with pytest.raises(errors.RosError, match=re.escape(WIZARD_HINT)):
        run.finish(strict=True, flush_timeout=30.0)
    assert time.monotonic() - started < 3
    client.close()


def test_the_hardware_monitors_final_emit_is_inside_the_deadline(app, tmp_path):
    """LOW 1. The deadline is taken first, so the finalizers that run before
    the drain (hardware, lineage) run inside it."""
    from probe.sdk import transport as transport_module

    run_id, client, run = _setup(app, tmp_path)
    seen = {}

    class FakeMonitor:
        def finish(self, timeout=None):
            seen["deadline"] = transport_module._request_deadline.get()
            seen["timeout"] = timeout

    run._hw_monitor = FakeMonitor()
    started = time.monotonic()
    run.finish(flush_timeout=5.0)
    assert seen["deadline"] is not None
    assert started < seen["deadline"] <= started + 5.5
    assert 0 < seen["timeout"] <= 5.0, "its thread joins are bounded by what is left"
    client.close()


def test_the_close_finalizers_waits_fit_inside_a_short_deadline(app, tmp_path, monkeypatch):
    """Follow-up to #2011: the hardware join (5 s) and the lineage hashing wait
    (30 s) were fixed waits, so `finish(flush_timeout=1)` could take 35 s. Both
    now get a share of what is left of the close's deadline (#2016's design:
    at most half each); this pins that the close passes it to both."""
    from probe.sdk import inputs

    run_id, client, run = _setup(app, tmp_path)
    seen = {}
    monkeypatch.setattr(inputs, "is_recording", lambda run_id: True)
    monkeypatch.setattr(
        inputs, "finalize", lambda client, run_id, wait_s=None: seen.setdefault("wait_s", wait_s)
    )

    class SlowMonitor:
        def finish(self, timeout=None):
            seen["timeout"] = timeout

    run._hw_monitor = SlowMonitor()
    run.finish(flush_timeout=1.0)
    assert seen["wait_s"] <= 1.0 and seen["timeout"] <= 1.0, seen
    client.close()


def test_ctrl_c_during_the_close_still_queues_the_verdict(app, tmp_path, monkeypatch):
    """MED 3. A Ctrl-C inside the (up to 600 s) close used to leave no terminal
    status queued and nothing handed off: the reaper called the run crashed."""
    run_id, client, run = _setup(app, tmp_path)
    _fail_metrics(client, monkeypatch)
    _log(client, run_id)
    handoffs = []
    real_handoff = client.hand_off_delivery
    monkeypatch.setattr(client, "hand_off_delivery", lambda: (handoffs.append(1), real_handoff())[1])
    real_sleep = time.sleep
    n = {"i": 0}

    def interrupting_sleep(s):
        n["i"] += 1
        if n["i"] == 2:
            raise KeyboardInterrupt
        real_sleep(min(s, 0.01))

    monkeypatch.setattr("probe.sdk.run.time.sleep", interrupting_sleep)
    with pytest.raises(KeyboardInterrupt):
        run.finish(flush_timeout=30.0)

    ops = [op for _, op in client.journal.pending()]
    assert [op["method"] for op in ops] == ["POST", "PATCH"], "the verdict waits behind the data"
    assert ops[-1]["body"]["status"] == "completed"
    assert ops[-1]["body"]["summary"]["probe_finish"]["deferred"] is True
    assert handoffs, "something will deliver it"
    assert run.finish() == run._finish_result, "a repeat close returns the first answer"
    client.close()


class _InterruptingMonitor:
    """A hardware collector whose final join is interrupted."""

    def __init__(self, interrupt: BaseException):
        self.interrupt = interrupt

    def finish(self, timeout=None):
        raise self.interrupt


@pytest.mark.parametrize(
    ("interrupt", "verdict"),
    [(KeyboardInterrupt(), "canceled"), (SystemExit(2), "failed")],
    ids=["ctrl-c", "sys-exit-2"],
)
def test_an_interrupt_before_the_drain_still_queues_a_verdict(
    app, tmp_path, monkeypatch, interrupt, verdict
):
    """Lane E, building #2016 on #2011: a Ctrl-C EARLY in an explicit
    finish() -- in the finalizers that run before the drain (the lineage hash,
    the hardware join) -- queued no status at all, so the run sat `running`
    until the reaper called it crashed. It now queues the interrupt's own
    verdict behind the data, hands the queue to the worker, and re-raises."""
    run_id, client, run = _setup(app, tmp_path)
    _fail_metrics(client, monkeypatch)
    _log(client, run_id)
    handoffs = []
    real_handoff = client.hand_off_delivery
    monkeypatch.setattr(client, "hand_off_delivery", lambda: (handoffs.append(1), real_handoff())[1])
    run._hw_monitor = _InterruptingMonitor(interrupt)

    with pytest.raises(type(interrupt)):
        run.finish(flush_timeout=30.0)

    ops = [op for _, op in client.journal.pending()]
    assert [op["method"] for op in ops] == ["POST", "PATCH"], "the verdict waits behind the data"
    assert ops[-1]["body"]["status"] == verdict
    assert handoffs, "something will deliver it"
    assert run.finish() == run._finish_result, "a repeat close returns the first answer"
    client.close()


def test_a_strict_close_interrupted_before_the_drain_queues_no_verdict(
    app, tmp_path, monkeypatch
):
    """The control: a strict close promises not to close over undelivered
    data, so an early interrupt still queues no status -- but hands the data
    it has to the worker."""
    run_id, client, run = _setup(app, tmp_path)
    _fail_metrics(client, monkeypatch)
    _log(client, run_id)
    handoffs = []
    real_handoff = client.hand_off_delivery
    monkeypatch.setattr(client, "hand_off_delivery", lambda: (handoffs.append(1), real_handoff())[1])
    run._hw_monitor = _InterruptingMonitor(KeyboardInterrupt())

    with pytest.raises(KeyboardInterrupt):
        run.finish(flush_timeout=30.0, strict=True)

    assert [op["method"] for _, op in client.journal.pending()] == ["POST"]
    assert handoffs
    client.close()


def test_a_with_block_then_the_exit_hook_closes_once(app, tmp_path, monkeypatch):
    """HIGH. `with probe.init()` closed the run in `Run.__exit__`, then the
    atexit hook closed it again: two full deadlines at exit during an outage
    and two terminal PATCHes queued."""
    from probe.sdk import fluent

    fluent._current.set(None)
    fluent._process_default = None
    # `probe.integrations.miles` exports PROBE_RUN_ID into os.environ and a Miles
    # test on the same worker can leave it; init(experiment=...) then refuses.
    for var in ("PROBE_RUN_ID", "PROBE_RUN_EPOCH"):
        monkeypatch.delenv(var, raising=False)
    monkeypatch.setattr(fluent, "_install_exit_hooks", lambda: None)
    monkeypatch.setattr(run_module, "FINISH_TIMEOUT_DEFAULT_SECONDS", 1.0)
    client = make_client(app, tmp_spool=tmp_path / "outbox", async_writes=True)
    seeded_run(app, tmp_path)  # makes experiment "e" exist
    _fail_metrics(client, monkeypatch)
    closes = []
    real_close = Run._close

    def counting(self, *a, **kw):
        closes.append(1)
        return real_close(self, *a, **kw)

    monkeypatch.setattr(Run, "_close", counting)
    started = time.monotonic()
    try:
        with fluent.init(client=client, experiment="e", name="r2") as run:
            run.log({"loss": 1.0})
        fluent._finish_at_exit()
        run.finish()  # and an explicit close after it all: still one
    finally:
        fluent._current.set(None)
        fluent._process_default = None
    elapsed = time.monotonic() - started

    patches = [op for _, op in client.journal.pending() if op["method"] == "PATCH"]
    assert len(closes) == 1 and len(patches) == 1
    assert elapsed < 1.9, f"two drain windows ({elapsed:.1f}s)"
    client.close()


def test_a_strict_close_that_raised_can_be_retried(app, tmp_path, monkeypatch):
    """Idempotency covers a close that SENT a verdict; a strict refusal sent
    none, so the caller may fix things and close again."""
    run_id, client, run = _setup(app, tmp_path)
    mp = pytest.MonkeyPatch()
    _fail_metrics(client, mp)
    _log(client, run_id)
    with pytest.raises(errors.RosError, match="not closed"):
        run.finish(strict=True, flush_timeout=0.3)
    mp.undo()
    row = run.finish(strict=True, flush_timeout=5)
    assert row["status"] == "completed" and app.runs[run_id]["status"] == "completed"
    client.close()


def test_a_trickling_response_cannot_hold_the_close_past_its_deadline(tmp_path, monkeypatch):
    """MED 4. httpx's timeouts bound each socket operation, not the request: a
    response that trickles a byte every 0.25 s never trips one (review: 9.8 s
    for `flush_timeout=2`). The body is read chunk by chunk against the
    deadline."""
    import httpx

    from probe.sdk.client import Client
    from probe.sdk.config import Settings
    from probe.sdk.journal import Journal
    from probe.sdk.transport import Transport

    monkeypatch.setenv("PROBE_AUTO_SNAPSHOT", "0")
    server = _SlowMetricsServer(stall=0.0, trickle=0.25)
    try:
        settings = Settings(base_url=server.url, token="ros_pat_deadbeef")
        transport = Transport(settings, client=httpx.Client(base_url=server.url, timeout=30.0))
        journal = Journal(tmp_path / "outbox", context={"name": None, "base_url": server.url})
        client = Client(settings=settings, transport=transport, journal=journal, async_writes=True)
        run = Run(client, dict(server.row))
        _log(client, server.run_id)

        started = time.monotonic()
        report = run.finish(flush_timeout=2.0)
        elapsed = time.monotonic() - started

        assert server.metric_posts >= 1
        assert elapsed < 4, f"a trickling response held the close {elapsed:.1f}s"
        assert report["finish_queued"] is True
        client.close()
    finally:
        server.close()


def test_the_drains_own_promotion_is_inside_the_deadline(app, tmp_path, monkeypatch):
    """MED 5. Every drain pass promotes waiting uploads; with no bound, 5 slow
    scans ran past `flush_timeout=1` (5.1 s)."""
    from probe.sdk.journal import Journal

    run_id, client, run = _setup(app, tmp_path)
    client._auto_drain = False
    for i in range(5):
        p = tmp_path / f"f{i}.jsonl"
        p.write_text('{"a": 1}\n' * 10)
        run.log_artifact(p.name, path=str(p))
    assert len(client.journal.waiting_positions()) == 1
    real = Journal._promote_locked

    def slow(self, op_id):
        time.sleep(1.0)  # a large file's credential scan
        return real(self, op_id)

    monkeypatch.setattr(Journal, "_promote_locked", slow)
    started = time.monotonic()
    report = run.finish(flush_timeout=1.0)
    elapsed = time.monotonic() - started
    assert elapsed < 3.0, f"promotion ran the close to {elapsed:.1f}s"
    assert report["finish_queued"] is True
    client.close()


def test_set_status_promotion_inside_a_close_shares_its_deadline(app, tmp_path, monkeypatch):
    """LOW 4. The terminal `set_status` promotes waiting uploads again; inside
    finish() that wait is bounded by what is left of the close, not 300 s."""
    run_id, client, run = _setup(app, tmp_path)
    seen: list[float] = []

    def promote(run_ref, *, timeout):
        seen.append(timeout)
        return []

    monkeypatch.setattr(client.journal, "promote_for_close", promote)
    run.finish(flush_timeout=2.0)
    assert len(seen) >= 2, "finish's own promotion and set_status's"
    assert max(seen) <= 2.0, seen
    client.close()


def test_a_malformed_timeout_does_not_raise_under_W_error(monkeypatch):
    import warnings

    monkeypatch.setattr(run_module, "FINISH_TIMEOUT_DEFAULT_SECONDS", 600.0)
    monkeypatch.setenv("PROBE_FINISH_TIMEOUT_SEC", "soon")
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        assert Run._resolve_finish_timeout(None) == 600.0


# --------------------------------------------------------------------------
# Re-review of #2011: a close already running.
# --------------------------------------------------------------------------


def _owned_client_run(app, tmp_path, monkeypatch):
    """`probe.init()` building its OWN client (the one fluent.finish closes)."""
    from probe.sdk import fluent

    for var in ("PROBE_RUN_ID", "PROBE_RUN_EPOCH"):
        monkeypatch.delenv(var, raising=False)
    fluent._current.set(None)
    fluent._process_default = None
    monkeypatch.setattr(fluent, "_install_exit_hooks", lambda: None)
    built = []

    def factory(*_a, **_kw):
        client = make_client(app, tmp_spool=tmp_path / "outbox", async_writes=True)
        built.append(client)
        return client

    monkeypatch.setattr(fluent, "Client", factory)
    seeded_run(app, tmp_path)  # experiment "e"
    run = fluent.init(experiment="e", name="two-closers")
    return fluent, built[0], run


def test_a_second_close_from_another_thread_waits_for_the_first(app, tmp_path, monkeypatch):
    """H2b. Thread A is mid-close (the server answers 503 for a while); a
    watchdog thread calls `probe.finish()`. It used to get None at once and
    `fluent.finish` closed the client A was still sending through, so A's
    terminal write raised "the client has been closed" and the run stayed
    running with nothing queued. B now waits for A and returns A's answer."""
    import threading

    fluent, client, run = _owned_client_run(app, tmp_path, monkeypatch)
    try:
        run.log({"loss": 1.0}, step=1)
        app.metrics_busy_next = 3  # A retries through ~3.5 s of 503s
        results: dict = {}

        def first():
            try:
                results["a"] = run.finish(flush_timeout=20)
            except BaseException as exc:  # noqa: BLE001 -- the assertion below reads it
                results["a_error"] = exc

        a = threading.Thread(target=first)
        a.start()
        time.sleep(0.3)  # A is inside its close
        results["b"] = fluent.finish()
        a.join(30)

        assert "a_error" not in results, results.get("a_error")
        assert app.runs[run.id]["status"] == "completed"
        assert results["b"] == results["a"], "B returns A's answer"
        assert client.transport._client.is_closed, "released once, after A finished"
    finally:
        fluent._current.set(None)
        fluent._process_default = None


def test_a_close_re_entered_on_the_same_thread_does_not_release_the_client(
    app, tmp_path, monkeypatch
):
    """A signal handler calling `probe.finish()` while this thread is already
    inside finish() cannot wait on itself: it gets an in-progress marker, and
    `fluent.finish` leaves the client for the running close."""
    fluent, client, run = _owned_client_run(app, tmp_path, monkeypatch)
    try:
        run.log({"loss": 1.0}, step=1)
        seen = {}
        real_drain = Run._drain_until

        def drain_then_reenter(self, *a, **k):
            seen["inner"] = fluent.finish()  # the "signal handler"
            seen["closed_inside"] = client.transport._client.is_closed
            return real_drain(self, *a, **k)

        monkeypatch.setattr(Run, "_drain_until", drain_then_reenter)
        row = run.finish(flush_timeout=5)

        assert seen["inner"] == {"finish_in_progress": True}
        assert seen["closed_inside"] is False
        assert row["status"] == "completed" and app.runs[run.id]["status"] == "completed"
    finally:
        fluent._current.set(None)
        fluent._process_default = None


def test_a_code_less_system_exit_during_the_close_still_queues_the_verdict(
    app, tmp_path, monkeypatch
):
    """L1. Lightning turns SIGTERM into a code-less SystemExit; a preempted
    job's close must still queue its verdict behind the data."""
    run_id, client, run = _setup(app, tmp_path)
    _fail_metrics(client, monkeypatch)
    _log(client, run_id)
    n = {"i": 0}
    real_sleep = time.sleep

    def preempting_sleep(s):
        n["i"] += 1
        if n["i"] == 2:
            raise SystemExit
        real_sleep(min(s, 0.01))

    monkeypatch.setattr("probe.sdk.run.time.sleep", preempting_sleep)
    with pytest.raises(SystemExit):
        run.finish(flush_timeout=30.0)
    ops = [op for _, op in client.journal.pending()]
    assert [op["method"] for op in ops] == ["POST", "PATCH"]
    client.close()


def test_a_closed_client_is_a_transport_failure_not_a_runtime_error(app, tmp_path):
    """httpx raises a bare RuntimeError on a closed client. Through `write()`
    that must fail open like any transport failure."""
    run_id, client, run = _setup(app, tmp_path)
    client.transport._client.close()
    with pytest.raises(errors.TransportError):
        client.transport.request("GET", f"/v1/runs/{run_id}")
    assert client.write("PATCH", f"/v1/runs/{run_id}", {"tags": ["x"]}, sync=True) is None
    assert [op["method"] for _, op in client.journal.pending()] == ["PATCH"], "journaled"


# --------------------------------------------------------------------------
# Plan 0.1: dropped writes are reported on the run.
# --------------------------------------------------------------------------


def test_dropped_writes_warn_and_are_marked_on_the_run(app, tmp_path, monkeypatch):
    run_id, client, run = _setup(app, tmp_path)
    _log(client, run_id, step=1)
    real_append = client.journal.append_http
    calls = {"n": 0}

    def full_after_one(*a, **k):
        calls["n"] += 1
        if calls["n"] <= 2:  # two writes find the outbox full
            from probe.sdk.journal import OutboxFull

            raise OutboxFull("outbox full: test")
        return real_append(*a, **k)

    monkeypatch.setattr(client.journal, "append_http", full_after_one)
    _log(client, run_id, step=2)
    _log(client, run_id, step=3)
    monkeypatch.setattr(client.journal, "append_http", real_append)
    assert client.dropped_writes == 2

    with pytest.warns(UserWarning, match="dropped"):
        run.finish(flush_timeout=5)

    row = app.runs[run_id]
    assert row["status"] == "completed"
    assert _finish_block(row)["dropped_writes"] == 2
    client.close()


def test_drops_before_the_handle_existed_are_not_this_runs(app, tmp_path):
    run_id = seeded_run(app, tmp_path)
    client = make_client(app, tmp_spool=tmp_path / "outbox", async_writes=True)
    client.dropped_writes = 3  # an earlier run on this client lost writes
    run = Run(client, {"id": run_id})
    _log(client, run_id)

    run.finish(flush_timeout=5)

    assert "probe_finish" not in (app.runs[run_id].get("summary") or {})
    client.close()


def test_a_run_whose_writes_hit_the_cap_still_gets_its_close_and_marker(app, tmp_path, monkeypatch):
    """Review of #2014 (HIGH). The drops came from the cap, so at finish() the
    queue is still at the cap and the cap refused the terminal close: the
    verdict and the `dropped_writes` marker were both lost, after a warning
    had said "marked". The close is admitted past the cap."""
    from probe.sdk import journal as journal_module

    monkeypatch.setattr(journal_module, "MAX_PENDING_OPS", 5)
    run_id, client, run = _setup(app, tmp_path)
    mp = pytest.MonkeyPatch()
    _fail_metrics(client, mp)
    for step in range(8):  # 5 queued, 3 dropped at the cap
        _log(client, run_id, step=step)
    assert client.dropped_writes == 3

    with pytest.warns(UserWarning, match="marked probe_finish.dropped_writes=3"):
        report = run.finish(flush_timeout=0.5)

    assert report["finish_queued"] is True and not report.get("close_unrecorded")
    close = [op for _, op in client.journal.pending()][-1]
    assert close["method"] == "PATCH" and close["body"]["status"] == "completed"
    assert close["body"]["summary"]["probe_finish"]["dropped_writes"] == 3
    mp.undo()
    client.flush()
    assert app.runs[run_id]["status"] == "completed"
    assert _finish_block(app.runs[run_id])["dropped_writes"] == 3
    client.close()


def test_the_drop_warning_does_not_claim_a_marker_it_could_not_record(app, tmp_path, monkeypatch):
    import errno

    from probe.sdk import journal as journal_module

    run_id, client, run = _setup(app, tmp_path)
    _log(client, run_id)
    _fail_metrics(client, monkeypatch)
    client.dropped_writes += 2  # two writes this run lost earlier
    root = str(client.journal.dir)
    real_write = journal_module.write_text_atomic

    def read_only(path, *a, **k):
        if str(path).startswith(root):
            raise OSError(errno.EROFS, "Read-only file system", str(path))
        return real_write(path, *a, **k)

    monkeypatch.setattr(journal_module, "write_text_atomic", read_only)
    with pytest.warns(UserWarning, match="could NOT be marked"):
        report = run.finish(flush_timeout=0.5)
    assert report.get("close_unrecorded") is True
    client.close()


def _fail_status_patch(client, monkeypatch, run_id):
    """The close's own PATCH fails (a blip on the last request); data lands."""
    original = client.transport.request

    def selective(method, path, *a, **kw):
        if method == "PATCH" and path == f"/v1/runs/{run_id}":
            raise errors.TransportError("net down")
        return original(method, path, *a, **kw)

    monkeypatch.setattr(client.transport, "request", selective)


def test_a_close_that_fails_open_is_queued_even_at_the_cap(app, tmp_path, monkeypatch):
    """Review of #2014, H5b: when the close's own PATCH fails, its fail-open
    copy went through the queue-length cap, and a queue full of OTHER runs'
    writes refused it -- the close was lost while finish() reported it
    delivered. It is `admitted` now, like the deferred close."""
    from probe.sdk import journal as journal_mod

    run_id, client, run = _setup(app, tmp_path)
    monkeypatch.setattr(journal_mod, "MAX_PENDING_OPS", 3)
    for n in range(3):
        client.journal.append_http("POST", "/v1/runs/other/metrics", {"points": [{"i": n}]})
    _fail_status_patch(client, monkeypatch, run_id)

    report = run.finish(flush_timeout=2.0)

    queued = [op for _, op in client.journal.pending() if op.get("run_ref") == run_id]
    assert [op["method"] for op in queued] == ["PATCH"], "the close is queued, not dropped"
    assert report.get("finish_queued") is True, report
    client.close()


def test_a_close_the_outbox_cannot_take_says_so(app, tmp_path, monkeypatch):
    """And when the outbox cannot take the close at all, finish() reports it
    unrecorded instead of delivered."""
    run_id, client, run = _setup(app, tmp_path)
    _fail_status_patch(client, monkeypatch, run_id)
    real_append = client.journal.append_http

    def read_only(method, path, *a, **kw):
        if method == "PATCH":
            raise OSError(30, "Read-only file system")
        return real_append(method, path, *a, **kw)

    monkeypatch.setattr(client.journal, "append_http", read_only)

    report = run.finish(flush_timeout=2.0)

    assert report.get("close_unrecorded") is True and report.get("delivered") == 0, report
    client.close()
