"""Plan 1.7: delivery trouble is said in the training process while it happens.

The detached worker writes only to `drainer.log`; dead letters and auth blocks
surfaced at `finish()` -- hours later -- and a dropped write warned once per
call (44 lines for 50 drops). Each kind of trouble now prints one line when it
starts, then at most one per 5 minutes with the running count.
"""

from __future__ import annotations

import errno
import json
import warnings
from datetime import datetime, timedelta, timezone

import pytest

from probe.sdk import errors
from probe.sdk import journal as journal_mod
from probe.sdk.journal import Journal, drain
from probe.sdk.safe_warn import DeliveryNotices
from probe.sdk.session_marker import WIZARD_HINT

from tests.conftest import make_client, open_run


@pytest.fixture(autouse=True)
def _isolated(monkeypatch, tmp_path):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(tmp_path / "config" / "probe.json"))
    for var in (*journal_mod._GLOBAL_RANK_VARS, "LOCAL_RANK", "PROBE_OUTBOX_WORKER"):
        monkeypatch.delenv(var, raising=False)


def _notices(caught) -> list[str]:
    return [
        str(w.message)
        for w in caught
        if str(w.message).startswith("probe") and "custom transport" not in str(w.message)
    ]


class _Clock:
    def __init__(self):
        self.now = 1000.0

    def __call__(self):
        return self.now


def _client(app, tmp_path, clock):
    client = make_client(app, tmp_spool=tmp_path / "outbox", async_writes=True)
    client._notices.clock = clock  # the poller keeps time by it too
    client._notice_polled_at = clock.now
    return client


def _unwritable(client, monkeypatch):
    def refuse(*a, **kw):
        raise OSError(errno.EROFS, "Read-only file system")

    monkeypatch.setattr(client.journal, "append_http", refuse)


def test_fifty_drops_are_one_line_and_the_next_says_fifty_one(app, tmp_path, monkeypatch):
    clock = _Clock()
    client = _client(app, tmp_path, clock)
    _unwritable(client, monkeypatch)
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        for step in range(50):
            client.write("POST", "/v1/runs/r-1/metrics", {"points": [{"i": step}]})
        assert len(_notices(caught)) == 1, _notices(caught)
        assert "1 write(s) dropped" in _notices(caught)[0]
        clock.now += 301
        client.write("POST", "/v1/runs/r-1/metrics", {"points": [{"i": 50}]})
    lines = _notices(caught)
    assert len(lines) == 2 and "51 write(s) dropped" in lines[1], lines
    assert client.dropped_writes == 51
    client.close()


def _status_with(journal: Journal, **fields) -> None:
    journal._ensure()
    journal.write_status(**fields)


def test_a_dead_letter_of_this_process_is_said_and_another_runs_is_not(app, tmp_path):
    clock = _Clock()
    client = _client(app, tmp_path, clock)
    client.write("POST", "/v1/runs/mine/metrics", {"points": []})
    journal = client.journal
    for op_id in ("a1", "b1"):  # the record keeps only ops still dead-lettered
        (journal.failed_dir / f"000000000009-1-{op_id}.json").write_text("{}")
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        journal._write_status_locked(
            recount=False,
            new_dead_letters=[{"run_ref": "someone-else", "op_id": "a1", "error": "422 bad"}],
        )
        clock.now += 16
        client.write("POST", "/v1/runs/mine/metrics", {"points": []})
        assert _notices(caught) == [], "another run's dead letter is not this process's"

        journal._write_status_locked(
            recount=False,
            new_dead_letters=[{"run_ref": "mine", "op_id": "b1", "error": "422 bad point"}],
        )
        clock.now += 16
        client.write("POST", "/v1/runs/mine/metrics", {"points": []})
    lines = _notices(caught)
    assert len(lines) == 1 and "dead-lettered" in lines[0] and "422 bad point" in lines[0], lines
    client.close()


def test_the_status_is_read_at_most_every_fifteen_seconds(app, tmp_path, monkeypatch):
    """Between reads the poller costs one monotonic check per write."""
    clock = _Clock()
    client = _client(app, tmp_path, clock)
    reads = []
    real = Journal.read_status

    def counting(d=None, **kw):
        if str(d) == str(client.journal.dir) and kw.get("include_receipts", True):
            reads.append(d)  # the poller's read; not the append's sibling check
        return real(d, **kw)

    monkeypatch.setattr(Journal, "read_status", staticmethod(counting))
    for step in range(100):
        client.write("POST", "/v1/runs/r-1/metrics", {"points": [{"i": step}]})
    assert reads == []
    clock.now += 16
    client.write("POST", "/v1/runs/r-1/metrics", {"points": [{"i": 100}]})
    assert len(reads) == 1
    client.close()


def test_an_auth_block_is_one_line_per_five_minutes(app, tmp_path, monkeypatch):
    clock = _Clock()
    client = _client(app, tmp_path, clock)
    _status_with(client.journal, auth_blocked_since="2026-09-27T10:00:00+00:00")
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        for _ in range(10):  # 10 polls over 150 s
            clock.now += 15
            client.write("POST", "/v1/runs/r-1/metrics", {"points": []})
        assert len(_notices(caught)) == 1 and WIZARD_HINT in _notices(caught)[0]
        clock.now += 300
        client.write("POST", "/v1/runs/r-1/metrics", {"points": []})
    assert len(_notices(caught)) == 2
    client.close()


def test_a_queue_stalled_for_ten_minutes_is_said(app, tmp_path, monkeypatch):
    clock = _Clock()
    client = _client(app, tmp_path, clock)
    client.write("POST", "/v1/runs/r-1/metrics", {"points": []})
    old = (datetime.now(timezone.utc) - timedelta(minutes=11)).isoformat()
    status = json.loads(client.journal.status_file.read_text())
    status["oldest_pending"] = old
    client.journal.status_file.write_text(json.dumps(status))
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        clock.now += 16
        client.write("POST", "/v1/runs/r-1/metrics", {"points": []})
    lines = _notices(caught)
    assert len(lines) == 1 and "11 min" in lines[0], lines
    client.close()


def test_an_older_workers_status_is_said_as_the_machines(app, tmp_path, monkeypatch):
    """A status.json written by a worker that predates 1.7 names no runs:
    the new dead letters are the machine's, and said so."""
    clock = _Clock()
    client = _client(app, tmp_path, clock)
    client.write("POST", "/v1/runs/r-1/metrics", {"points": []})
    status = json.loads(client.journal.status_file.read_text())
    status.pop("recent_dead_letters", None)
    status["failed"] = 3
    client.journal.status_file.write_text(json.dumps(status))
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        clock.now += 16
        client.write("POST", "/v1/runs/r-1/metrics", {"points": []})
    lines = _notices(caught)
    assert len(lines) == 1 and "this machine's outbox" in lines[0], lines
    client.close()


def test_a_credential_queues_notices_start_from_that_queue(app, tmp_path, monkeypatch):
    """A PROBE_TOKEN job writes to its credential's own queue (#2041), chosen
    in `Client.__init__`. The notices' baseline is read from THAT queue: read
    from the shared one, a process resuming a run announced the dead letters
    its queue already held for that run as its own, new ones."""
    from probe.sdk.client import Client
    from tests.served_fake_app import serve
    from tests.test_outbox_credential_stamp import ENV_A, STORED_B, _login

    with serve(app) as url:
        _login(url, STORED_B)
        monkeypatch.setenv("PROBE_TOKEN", ENV_A)
        first = Client(spool_dir=tmp_path / "outbox", async_writes=True, auto_drain=False)
        first.write("POST", "/v1/runs/r-1/metrics", {"points": []})
        queue = first.journal
        assert queue.dir.parent.parent == tmp_path / "outbox", "not a credential queue"
        first.close()
        # A dead letter of r-1 from before the next process (the record keeps
        # only ops still dead-lettered).
        queue.failed_dir.mkdir(parents=True, exist_ok=True)
        (queue.failed_dir / "000000000009-1-old1.json").write_text("{}")
        queue._write_status_locked(
            recount=False,
            new_dead_letters=[{"run_ref": "r-1", "op_id": "old1", "error": "422 bad"}],
        )
        clock = _Clock()
        client = Client(spool_dir=tmp_path / "outbox", async_writes=True, auto_drain=False)
        assert client.journal.dir == queue.dir
        client._notices.clock = clock
        client._notice_polled_at = clock.now
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            client.write("POST", "/v1/runs/r-1/metrics", {"points": []})  # resumes r-1
            clock.now += 16
            client.write("POST", "/v1/runs/r-1/metrics", {"points": []})
        client.close()
    assert [n for n in _notices(caught) if "dead-lettered" in n] == []


def test_a_refused_credential_is_said_as_an_auth_block(app, tmp_path, monkeypatch):
    """Since #2041 a refused credential's writes are set aside by fingerprint
    (`refused_fingerprints` in status.json) and the queue-wide
    `auth_blocked_since` stays empty for every write a current client queues:
    a training process whose token was revoked never said so. The poller
    reads its own credential's refusal too; another credential's does not
    count."""
    from probe.sdk.client import Client
    from tests.served_fake_app import serve
    from tests.test_outbox import seeded_run
    from tests.test_outbox_credential_stamp import ENV_A, STORED_B, _login

    run_id = seeded_run(app, tmp_path)
    metric = {"points": [{"key": "loss", "kind": "model", "value": 1.0, "step_index": 1}]}
    with serve(app) as url:
        _login(url, STORED_B)
        monkeypatch.setenv("PROBE_TOKEN", ENV_A)
        clock = _Clock()
        client = Client(spool_dir=tmp_path / "outbox", async_writes=True, auto_drain=False)
        client._notices.clock = clock
        client._notice_polled_at = clock.now
        app.rejected_tokens.add(ENV_A)  # revoked while the job runs
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            client.write("POST", f"/v1/runs/{run_id}/metrics", metric)
            drain(Journal(tmp_path / "outbox"))
            status = Journal.read_status(client.journal.dir) or {}
            assert status.get("refused_fingerprints") and not status.get("auth_blocked_since")
            clock.now += 16
            client.write("POST", f"/v1/runs/{run_id}/metrics", metric)
        client.close()
    lines = [n for n in _notices(caught) if "refused" in n and "credential" in n]
    assert len(lines) == 1 and WIZARD_HINT in lines[0], _notices(caught)


def test_another_credentials_refusal_is_not_this_processs(app, tmp_path):
    """The control: a fingerprint this client never wrote with is ignored."""
    clock = _Clock()
    client = _client(app, tmp_path, clock)
    client.write("POST", "/v1/runs/r-1/metrics", {"points": []})
    _status_with(client.journal, refused_fingerprints={"someone-else": "2026-09-27T10:00:00+00:00"})
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        clock.now += 16
        client.write("POST", "/v1/runs/r-1/metrics", {"points": []})
    assert [n for n in _notices(caught) if "refused" in n] == []
    client.close()


def test_the_drain_records_its_dead_letters_in_the_status(tmp_path):
    journal = Journal(tmp_path / "outbox")
    journal.append_http("POST", "/v1/runs/r-1/metrics", {"points": []})

    class _Refusing:
        class transport:  # noqa: N801
            @staticmethod
            def request(*a, **k):
                raise errors.ValidationError("bad point", status=422)

        def close(self):
            pass

    drain(journal, client_factory=lambda ctx: _Refusing())
    (entry,) = journal.recent_dead_letters()
    assert entry["run_ref"] == "r-1" and entry["status"] == 422 and "bad point" in entry["error"]
    assert "recent_dead_letters" not in Journal.read_status(journal.dir), "not in status.json"


def test_the_dead_letter_record_forgets_retried_and_discarded_ops(tmp_path):
    """Review of #2055: the record never cleared, and lived in status.json,
    which every append rewrote (32 entries: 15 KB, 179 -> 511 us). It is its
    own file now, and retry/discard prune it."""
    journal = Journal(tmp_path / "outbox")
    for n in range(3):
        journal.append_http("POST", f"/v1/runs/r-{n}/metrics", {"points": []})

    class _Refusing:
        class transport:  # noqa: N801
            @staticmethod
            def request(*a, **k):
                raise errors.ValidationError("bad point", status=422)

        def close(self):
            pass

    drain(journal, client_factory=lambda ctx: _Refusing())
    records = journal.recent_dead_letters()
    assert len(records) == 3
    journal.retry_failed(records[0]["op_id"])
    journal.discard_failed(records[1]["op_id"])
    assert [r["op_id"] for r in journal.recent_dead_letters()] == [records[2]["op_id"]]
    text = journal.status_file.read_text()
    assert "\n  " not in text, "status.json is written compact"


def test_finish_says_what_was_held_back(app, tmp_path, monkeypatch):
    clock = _Clock()
    client = _client(app, tmp_path, clock)
    run = open_run(client, experiment="notices")
    _unwritable(client, monkeypatch)
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        for step in range(5):
            run.log({"loss": float(step)}, step=step)
        run.finish(flush_timeout=0)
    lines = [line for line in _notices(caught) if "write(s) dropped before" in line]
    # The first drop is said at once; the running total once more, at the close.
    assert len(lines) == 2 and "1 write(s)" in lines[0], lines
    import re

    total = int(re.search(r"(\d+) write\(s\)", lines[1]).group(1))
    assert "(at close)" in lines[1] and total >= 5, lines  # 5 logs (+ the close's beacon)
    client.close()


def test_ranks_say_which_rank_they_are(app, tmp_path, monkeypatch):
    monkeypatch.setenv("RANK", "3")
    client = make_client(app, tmp_spool=tmp_path / "outbox", async_writes=True)
    _unwritable(client, monkeypatch)
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        client.write("POST", "/v1/runs/r-1/metrics", {"points": []})
    assert _notices(caught)[0].startswith("probe[rank-3]:")
    client.close()


def test_the_worker_says_nothing(monkeypatch):
    monkeypatch.setenv("PROBE_OUTBOX_WORKER", "1")
    notices = DeliveryNotices()
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        notices.note(notices.DROP, "{n} write(s) dropped")
        notices.summary()
    assert caught == []


def test_a_notice_cannot_raise_under_W_error():
    notices = DeliveryNotices()
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        notices.note(notices.DROP, "{n} write(s) dropped")
        notices.summary()


def _showwarning_raising(exc):
    def show(*_a, **_k):
        raise exc

    return show


@pytest.mark.parametrize("stop", [KeyboardInterrupt, SystemExit])
def test_a_signal_landing_in_a_notice_still_stops_the_process(stop):
    """A notice swallowed BaseException, so a KeyboardInterrupt raised while
    one printed (a Ctrl-C, a DDP worker's death signal re-delivered in the
    middle of its close) was lost and the process carried on. Through the REAL
    warnings path: `safe_warn.warn` itself swallowed it too."""
    notices = DeliveryNotices()
    with warnings.catch_warnings():
        warnings.simplefilter("always")
        warnings.showwarning = _showwarning_raising(stop)  # restored on exit
        with pytest.raises(stop):
            notices.note(notices.DROP, "{n} write(s) dropped")
        notices._kinds[notices.DROP].printed = 0
        with pytest.raises(stop):
            notices.summary()
        with pytest.raises(stop):
            from probe.sdk import safe_warn

            safe_warn.warn("probe: anything")
    assert notices._lock.acquire(timeout=1), "the lock was left held"
    notices._lock.release()


def test_a_broken_warning_hook_is_still_swallowed():
    """The control: anything else a warning raises stays ours to absorb."""
    from probe.sdk import safe_warn

    notices = DeliveryNotices()
    with warnings.catch_warnings():
        warnings.simplefilter("always")
        warnings.showwarning = _showwarning_raising(RuntimeError("hook broke"))
        notices.note(notices.DROP, "{n} write(s) dropped")
        notices.summary()
        safe_warn.warn("probe: anything")
    assert safe_warn.describe(_Unrepresentable()) == "<unrepresentable _Unrepresentable>"


class _Unrepresentable:
    def __init__(self, exc=None):
        self.exc = exc

    def __repr__(self):
        raise self.exc or RuntimeError("released CUDA context")


def test_a_ctrl_c_while_describing_a_value_reaches_the_caller():
    from probe.sdk import safe_warn

    with pytest.raises(KeyboardInterrupt):
        safe_warn.describe(_Unrepresentable(KeyboardInterrupt()))


@pytest.mark.parametrize("stop", [KeyboardInterrupt, SystemExit])
def test_a_ctrl_c_mid_append_stops_the_process_and_is_no_dropped_write(
    app, tmp_path, monkeypatch, stop
):
    """`Client._enqueue` caught BaseException, so a Ctrl-C landing in a queue
    write became "1 write(s) dropped" -- a notice, `dropped_writes=1` on the
    run -- and training carried on past it (#2029's Lightning Ctrl-C test saw
    the run close `failed`, not `canceled`). It propagates now, and the write
    it cut off leaves nothing behind: the op file's temp copy existed when the
    signal landed, and is gone."""
    import os
    import threading

    from probe.sdk import durable

    clock = _Clock()
    client = _client(app, tmp_path, clock)
    client.write("POST", "/v1/runs/r-1/metrics", {"points": [{"i": 0}]})
    ops = client.journal.ops_dir
    before = sorted(os.listdir(ops))
    real_fsync, me, landed = durable.os.fsync, threading.get_ident(), []

    def interrupted(fd):
        # This thread only, and only once the op's temp file exists: the
        # signal lands in the middle of the write, not before it.
        if threading.get_ident() == me and not landed:
            temps = [n for n in os.listdir(ops) if n.endswith(".tmp")]
            if temps:
                landed.append(temps)
                raise stop
        return real_fsync(fd)

    monkeypatch.setattr(durable.os, "fsync", interrupted)
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        with pytest.raises(stop):
            client.write("POST", "/v1/runs/r-1/metrics", {"points": [{"i": 1}]})
    monkeypatch.setattr(durable.os, "fsync", real_fsync)
    assert landed, "the signal never landed mid-write"
    assert client.dropped_writes == 0
    assert [n for n in _notices(caught) if "dropped" in n] == []
    assert sorted(os.listdir(ops)) == before, "a partial write was left in the queue"
    # The append lock was released: the next write queues.
    client.write("POST", "/v1/runs/r-1/metrics", {"points": [{"i": 2}]})
    assert len(os.listdir(ops)) == len(before) + 1
    client.close()


def test_a_ctrl_c_after_the_op_landed_leaves_a_whole_op_that_delivers(app, tmp_path, monkeypatch):
    """The other side of the window: the op file is in, the status count is
    not. The op is whole and delivers; nothing is counted dropped."""
    import os

    clock = _Clock()
    client = _client(app, tmp_path, clock)
    real = client.journal._write_status_locked

    def interrupted(**kw):
        if kw.get("pending_delta") == 1:
            raise KeyboardInterrupt
        return real(**kw)

    monkeypatch.setattr(client.journal, "_write_status_locked", interrupted)
    with pytest.raises(KeyboardInterrupt):
        client.write(
            "POST", "/v1/runs/r-1/metrics", {"points": [{"key": "loss", "value": 1.0, "step": 0}]}
        )
    monkeypatch.setattr(client.journal, "_write_status_locked", real)
    assert client.dropped_writes == 0
    ops = client.journal.ops_dir
    assert [n for n in os.listdir(ops) if n.endswith(".tmp")] == []
    drain(client.journal, client_factory=lambda ctx: client)
    assert [p["key"] for p in app.metric_points_posted["r-1"]] == ["loss"]
    client.close()


def test_an_offline_queue_is_not_called_stalled(app, tmp_path):
    """An offline run's queue (plan 2.12, `_drains_by_hand`) waits for `probe
    sync` by design: no stalled notice, no status polling."""
    clock = _Clock()
    client = _client(app, tmp_path, clock)
    client._drains_by_hand = True
    client.write("POST", "/v1/runs/r-1/metrics", {"points": []})
    old = (datetime.now(timezone.utc) - timedelta(hours=2)).isoformat()
    status = json.loads(client.journal.status_file.read_text())
    status["oldest_pending"] = old
    client.journal.status_file.write_text(json.dumps(status))
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        clock.now += 16
        client.write("POST", "/v1/runs/r-1/metrics", {"points": []})
    assert _notices(caught) == []
    client.close()


def test_the_auth_reminder_text_changes_so_it_repeats(app, tmp_path, monkeypatch):
    """Review of #2055: Python's default warning filter shows an identical
    message from one line only once, so the 5-minute reminder never printed
    again in a real run. Its text carries the elapsed time."""
    from probe.sdk import client as client_mod

    clock = _Clock()
    client = _client(app, tmp_path, clock)
    start = clock.now
    monkeypatch.setattr(
        client_mod, "_minutes_since", lambda stamp: 7 + int((clock.now - start) // 60)
    )
    blocked = (datetime.now(timezone.utc) - timedelta(minutes=7)).isoformat()
    _status_with(client.journal, auth_blocked_since=blocked)
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        clock.now += 16
        client.write("POST", "/v1/runs/r-1/metrics", {"points": []})
        clock.now += 301
        client.write("POST", "/v1/runs/r-1/metrics", {"points": []})
    lines = _notices(caught)
    assert len(lines) == 2 and "for 7 min" in lines[0] and lines[0] != lines[1], lines
    client.close()


def test_stopped_for_counts_from_the_first_refusal(app, tmp_path):
    """A drain rewrites the refusal stamp at every refusal (the credential
    cooldown counts from the latest), so "stopped for N min" said 0-5 min
    however long the block had lasted. It counts from the first stamp of the
    unbroken block this process saw."""
    clock = _Clock()
    client = _client(app, tmp_path, clock)
    first = (datetime.now(timezone.utc) - timedelta(minutes=20)).isoformat()
    _status_with(client.journal, auth_blocked_since=first)
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        clock.now += 16
        client.write("POST", "/v1/runs/r-1/metrics", {"points": []})
        latest = (datetime.now(timezone.utc) - timedelta(minutes=1)).isoformat()
        _status_with(client.journal, auth_blocked_since=latest)  # a later pass restamps
        clock.now += 301
        client.write("POST", "/v1/runs/r-1/metrics", {"points": []})
    lines = [n for n in _notices(caught) if "refused" in n]
    assert len(lines) == 2, lines
    assert "for 20 min" in lines[1] and f"since {first}" in lines[1], lines[1]
    client.close()


def test_a_queue_being_worked_through_is_not_called_stalled(app, tmp_path):
    """Review of #2055: a long recovery pass leaves `oldest_pending` old while
    it delivers; this client's writes landing since the last look is progress."""
    clock = _Clock()
    client = _client(app, tmp_path, clock)
    client.write("POST", "/v1/runs/r-1/metrics", {"points": []})
    old = (datetime.now(timezone.utc) - timedelta(minutes=30)).isoformat()
    status = json.loads(client.journal.status_file.read_text())
    status["oldest_pending"] = old
    client.journal.status_file.write_text(json.dumps(status))
    client._delivered_seen = 0
    client.journal.note_delivered(client.journal._producer_id, 5)  # the drain at work
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        clock.now += 16
        client.write("POST", "/v1/runs/r-1/metrics", {"points": []})
    assert [line for line in _notices(caught) if "min:" in line] == []
    client.close()


def test_notices_from_many_threads_are_counted_once_each():
    import threading

    notices = DeliveryNotices()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        threads = [
            threading.Thread(
                target=lambda: [notices.note(notices.DROP, "{n} dropped") for _ in range(200)]
            )
            for _ in range(8)
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
    assert notices._kinds[notices.DROP].total == 1600
