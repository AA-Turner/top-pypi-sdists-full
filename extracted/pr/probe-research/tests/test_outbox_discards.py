"""Writes set aside are kept, counted and reported; a refusal with nothing
queued blocks nothing (Bucket, 2026-10-23).

A customer's 12,193 queued writes left the outbox without delivery, most
likely through `probe outbox discard --held`, and nothing said so: no discard
sent telemetry. Their discards sat in a credential queue, which the queue's
cleanup (`prune_credential_queues`) deletes once idle -- by this release and
every older one, an older SDK in a job's own environment included. And the
refusal record those writes left behind said "auth-blocked, sign in again" on
every command and reported a stuck queue every six hours, with 0 pending.
"""

from __future__ import annotations

import json
import os
import shutil

import pytest

from probe.cli import telemetry as tm
from probe.sdk import journal as journal_module
from probe.sdk.journal import (
    CREDENTIAL_NAMESPACE,
    DELIVERY_NAMESPACE,
    DiscardCounts,
    Journal,
    auth_blocked_since,
    relocate_discards,
)

HOSTED = "https://api.research.prbe.ai"
FP = "ab" * 8
OTHER_FP = "cd" * 8


@pytest.fixture(autouse=True)
def isolate(tmp_path, monkeypatch):
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(tmp_path / "probe" / "config.json"))
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    for var in ("PROBE_BASE_URL", "PROBE_TOKEN", "PROBE_MCP_TOKEN", "PROBE_OUTBOX_DIR"):
        monkeypatch.delenv(var, raising=False)
    (tmp_path / "probe").mkdir(parents=True, exist_ok=True)


@pytest.fixture()
def captured(monkeypatch):
    """emit() records at the queue seam: no thread, no network."""
    records: list[dict] = []
    monkeypatch.setenv("PROBE_TELEMETRY", "on")
    monkeypatch.setattr(tm, "_sender", None)
    monkeypatch.setattr(tm, "_flush_registered", True)
    monkeypatch.setattr(tm._Sender, "start", lambda self: None)
    monkeypatch.setattr(tm._Sender, "put", lambda self, rec: records.append(rec))
    return records


def _discarded(records) -> list[dict]:
    return [r["properties"] for r in records if r["event"] == tm.EVENT_OUTBOX_DISCARDED]


def _queue(root, fp=FP, *, base_url=HOSTED) -> Journal:
    """A credential queue whose writes a `PROBE_TOKEN` job with ``fp`` queued."""
    return Journal(
        str(root / CREDENTIAL_NAMESPACE / fp),
        context={"name": None, "base_url": base_url, "principal": {"source": "env", "fingerprint": fp}},
    )


def _write(queue: Journal, step: int = 1) -> None:
    queue.append_http("POST", "/v1/runs/r/metrics", {"points": [{"step_index": step}]})


def _discard_all(queue: Journal) -> list[str]:
    """What an older release's `discard --held --credential` left: the
    queue's writes moved into ITS OWN `discarded/`."""
    target = queue.dir / "discarded"
    target.mkdir(parents=True, exist_ok=True)
    names = []
    for path, _op in queue.pending():
        os.replace(path, target / path.name)
        names.append(path.name)
    queue.write_status(held=0)
    return names


def _age(folder) -> None:
    for path in (folder, *folder.rglob("*")):
        os.utime(path, (1, 1))


def _old_release_prune(root) -> None:
    """0.300's cleanup, which an older SDK in a job's venv still runs: an idle
    credential queue with nothing in `ops/`, `failed/` ... is deleted, its
    `discarded/` with it."""
    for path in (root / CREDENTIAL_NAMESPACE).iterdir():
        if not any(
            (path / sub).exists() and os.listdir(path / sub)
            for sub in ("ops", "failed", "waiting", "blobs", "multipart/ops")
        ):
            shutil.rmtree(path)


# -- discards are kept --------------------------------------------------------


def test_a_queue_holding_discards_is_never_deleted_with_them(tmp_path, monkeypatch):
    root = tmp_path / "outbox"
    queue = _queue(root)
    _write(queue)
    names = _discard_all(queue)
    _age(queue.dir)
    assert not journal_module._queue_is_empty(queue.dir)
    monkeypatch.setattr(journal_module, "_last_prune", float("-inf"))
    moved = DiscardCounts()
    journal_module.prune_credential_queues(root, counts=moved)
    assert sorted(os.listdir(root / "discarded")) == names, "the prune deleted a discarded write"
    assert moved.writes == 1
    _age(queue.dir)  # empty now: the next idle prune removes it
    monkeypatch.setattr(journal_module, "_last_prune", float("-inf"))
    assert journal_module.prune_credential_queues(root) == 1
    assert sorted(os.listdir(root / "discarded")) == names


def test_discards_move_whether_or_not_the_queue_is_idle(tmp_path):
    """Codex O1: a queue still in use keeps its discards exposed to an older
    release's cleanup the moment it idles. The rescuer moves them anyway."""
    root = tmp_path / "outbox"
    queue = _queue(root)
    for step in (1, 2):
        _write(queue, step)
    (discarded,) = _discard_all(queue)[:1]
    _write(queue, 3)  # still in use
    counts = relocate_discards(root)
    assert counts.writes == 2 and counts.base_url == HOSTED
    assert discarded in os.listdir(root / "discarded")
    assert len(queue.pending()) == 1, "the queue's own writes stay"
    _old_release_prune(root)  # the queue is busy: kept; nothing to lose anyway
    _queue(root)._ensure()
    _old_release_prune(root)
    assert discarded in os.listdir(root / "discarded")


def test_an_older_release_finds_nothing_to_delete_after_one_pass(tmp_path):
    root = tmp_path / "outbox"
    queue = _queue(root)
    for step in range(1, 4):
        _write(queue, step)
    names = _discard_all(queue)
    relocate_discards(root)
    _old_release_prune(root)
    assert not queue.dir.exists()
    assert sorted(os.listdir(root / "discarded")) == names


def test_a_name_the_root_already_holds_is_never_overwritten(tmp_path):
    root = tmp_path / "outbox"
    queue = _queue(root)
    _write(queue)
    (name,) = _discard_all(queue)
    (root / "discarded").mkdir(parents=True)
    (root / "discarded" / name).write_text('{"root": true}')
    assert relocate_discards(root).writes == 1
    kept = {p.name: json.loads(p.read_text()) for p in (root / "discarded").iterdir()}
    assert kept[name] == {"root": True}
    assert any(k.endswith(name) and k != name and "points" in json.dumps(v) for k, v in kept.items())


def test_a_receipt_namespaces_discards_stay_where_its_recovery_reads_them(tmp_path):
    root = tmp_path / "outbox"
    queue = _queue(root)
    receipts = queue.dir / DELIVERY_NAMESPACE / "discarded"
    receipts.mkdir(parents=True)
    (receipts / "tombstone.json").write_text("{}")
    assert relocate_discards(root).writes == 0
    assert os.listdir(receipts) == ["tombstone.json"]


def test_a_half_pruned_queues_discards_are_moved_before_it_goes(tmp_path, monkeypatch):
    """An older prune renamed a queue holding discards away and died before
    deleting it; this release's prune deletes such leftovers."""
    root = tmp_path / "outbox"
    leftover = root / CREDENTIAL_NAMESPACE / f".pruned-{FP}-123-456" / "discarded"
    leftover.mkdir(parents=True)
    (leftover / "0001-x.json").write_text(json.dumps({"kind": "http", "context": {"base_url": HOSTED}}))
    monkeypatch.setattr(journal_module, "_last_prune", float("-inf"))
    journal_module.prune_credential_queues(root)
    assert os.listdir(root / "discarded") == ["0001-x.json"]
    assert not leftover.parent.exists()


def test_this_releases_discards_of_a_credential_queue_go_to_the_root(tmp_path):
    root = tmp_path / "outbox"
    queue = _queue(root)
    _write(queue)
    counts = Journal(str(root)).discard_held_counts(credential=FP)
    assert counts.writes == 1
    assert not (queue.dir / "discarded").exists()
    assert len(os.listdir(root / "discarded")) == 1


def test_a_half_pruned_queue_whose_discards_cannot_move_is_kept(tmp_path, monkeypatch):
    """Three reviewers: the leftover was deleted whatever the move did (a full
    disk, a permission), its discards with it."""
    root = tmp_path / "outbox"
    leftover = root / CREDENTIAL_NAMESPACE / f".pruned-{FP}-123-456" / "discarded"
    leftover.mkdir(parents=True)
    (leftover / "0001-x.json").write_text("{}")

    def refuse(*args, **kwargs):
        raise OSError(28, "No space left on device")

    monkeypatch.setattr(journal_module.os, "link", refuse)
    monkeypatch.setattr(journal_module.os, "replace", refuse)
    monkeypatch.setattr(journal_module, "_last_prune", float("-inf"))
    journal_module.prune_credential_queues(root)
    assert (leftover / "0001-x.json").exists()


def test_a_move_cut_short_is_finished_not_copied(tmp_path):
    """Two movers at once, or one killed between its link and its unlink,
    left the same write under two names, counted twice."""
    root = tmp_path / "outbox"
    queue = _queue(root)
    _write(queue)
    (name,) = _discard_all(queue)
    (root / "discarded").mkdir(parents=True)
    os.link(queue.dir / "discarded" / name, root / "discarded" / name)  # the link landed, the unlink did not
    assert relocate_discards(root).writes == 0
    assert os.listdir(root / "discarded") == [name]
    assert not os.listdir(queue.dir / "discarded")


def test_two_movers_at_once_count_the_write_once(tmp_path, monkeypatch):
    """The mover whose link landed counts it, even when the other one saw the
    link and removed the source first."""
    root = tmp_path / "outbox"
    queue = _queue(root)
    _write(queue)
    _discard_all(queue)
    real_unlink = os.unlink

    def raced(path, *args, **kwargs):
        real_unlink(path)  # the other mover saw the link and removed the source
        raise FileNotFoundError(path)

    monkeypatch.setattr(journal_module.os, "unlink", raced)
    assert relocate_discards(root).writes == 1
    assert len(os.listdir(root / "discarded")) == 1


def test_probe_outbox_resume_looks_for_stranded_writes_again_at_once(tmp_path, monkeypatch):
    import importlib

    from probe.sdk import outbox_worker

    main = importlib.import_module("probe.cli.main")
    root = tmp_path / "outbox"
    journal = Journal(str(root))
    journal.pause()
    stamp = outbox_worker._rescue_stamp(journal)
    stamp.write_text("x")
    monkeypatch.setattr(main, "_journal", lambda: Journal(str(root)))
    monkeypatch.setattr(main, "_kick_drainer", lambda *a, **k: None)
    main.outbox_resume()
    assert not stamp.exists()


def test_a_receipt_only_client_reports_its_discards_as_it_closes(tmp_path):
    from probe.sdk.client import Client

    client = Client(spool_dir=tmp_path / "outbox", async_writes=True, auto_drain=False,
                    base_url=HOSTED, token="probe_pat_x_0123456789abcdef")
    calls: list = []
    client._report_delivery = lambda final=False: calls.append(final)
    client._reported = {}
    client._discarded_requests = 2
    client.close()
    assert calls == [True]


def test_a_worker_moves_a_bounded_number_and_the_rest_wait(tmp_path, monkeypatch):
    """A worker moves discards before it sends anything: an older release's
    500k-write discard must not hold delivery for minutes."""
    root = tmp_path / "outbox"
    queue = _queue(root)
    for step in range(5):
        _write(queue, step)
    _discard_all(queue)
    monkeypatch.setattr(journal_module, "_PRUNE_MOVE_LIMIT", 2)
    monkeypatch.setattr(journal_module, "_last_prune", float("-inf"))
    moved = DiscardCounts()
    journal_module.prune_credential_queues(root, counts=moved)
    assert moved.writes == 2 and len(os.listdir(root / "discarded")) == 2
    assert relocate_discards(root).writes == 3, "the rescuer moves the rest"


def test_a_malformed_dead_letter_is_discarded_and_counted_without_stopping(tmp_path):
    root = tmp_path / "outbox"
    queue = _queue(root)
    queue.failed_dir.mkdir(parents=True, exist_ok=True)
    for i, body in enumerate(['{"context": ["bad"]}', '{"kind": "upload", "upload": [1]}', "not json"]):
        (queue.failed_dir / f"000{i}-x.json").write_text(body)
    counts = Journal(str(root)).discard_failed_counts()
    assert counts.writes == 3
    assert len(os.listdir(root / "discarded")) == 3, "a credential queue's dead letters go to the root"


def test_a_day_that_is_not_a_date_never_reaches_an_event():
    counts = DiscardCounts()
    counts.add({"enqueued_at": "../../etc/passwd"}, mtime=0)
    counts.add({"enqueued_at": "2026-10-23T17:00:00+00:00"})
    assert counts.by_enqueue_day == {"1970-01-01": 1, "2026-10-23": 1}


def test_probe_outbox_drain_reports_what_it_moved(tmp_path, monkeypatch, captured, capsys):
    import importlib

    main = importlib.import_module("probe.cli.main")
    root = tmp_path / "outbox"
    queue = _queue(root)
    _write(queue)
    _discard_all(queue)
    monkeypatch.setattr(main, "_journal", lambda: Journal(str(root)))
    monkeypatch.setattr(journal_module, "_last_prune", float("-inf"))
    monkeypatch.setattr(journal_module, "drain", lambda journal, **kw: journal_module.DrainReport())
    main._drain_foreground()
    (props,) = _discarded(captured)
    assert (props["reason"], props["writes"]) == ("relocated", 1)


def test_a_paused_outbox_moves_its_discards_and_looks_again_much_later(tmp_path, monkeypatch, captured):
    from probe.sdk import outbox_worker

    root = tmp_path / "outbox"
    queue = _queue(root)
    _write(queue)
    _discard_all(queue)
    Journal(str(root)).pause()
    monkeypatch.setattr(Journal, "discover", staticmethod(lambda: []))
    monkeypatch.setattr(journal_module, "rescue_lock_path", lambda: tmp_path / "rescue.lock")
    outbox_worker.rescue(str(root))
    assert len(os.listdir(root / "discarded")) == 1
    import time

    assert os.stat(outbox_worker._rescue_stamp(Journal(str(root)))).st_mtime > time.time() + 3600


# -- the refusal a queue with nothing in it keeps --------------------------------


def _status(folder, **fields) -> None:
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "status.json").write_text(json.dumps(fields))


def test_a_refusal_with_nothing_queued_blocks_nothing(tmp_path):
    """Bucket's banner and `outbox.stuck` after its writes went: pending 0,
    one refused credential, every six hours."""
    root = tmp_path / "outbox"
    _status(root, pending=0)
    _status(root / CREDENTIAL_NAMESPACE / FP, pending=0, held=0,
            refused_fingerprints={FP: "2026-10-23T17:23:00+00:00"})
    status = Journal.read_status(root)
    assert auth_blocked_since(status) is None
    assert tm.stuck_status(status) is False


def test_a_stale_root_refusal_beside_a_busy_queue_is_not_a_block(tmp_path):
    """Codex O3: the fold summed a healthy queue's pending into the root
    before the root's own stale refusal was judged."""
    root = tmp_path / "outbox"
    _status(root, pending=0, refused_fingerprints={FP: "2026-10-23T17:23:00+00:00"},
            auth_blocked_since="2026-10-23T17:23:00+00:00")
    _status(root / CREDENTIAL_NAMESPACE / OTHER_FP, pending=7)
    status = Journal.read_status(root)
    assert status["pending"] == 7
    assert auth_blocked_since(status) is None and not status["refused_fingerprints"]


def test_a_refused_credential_with_writes_still_reads_blocked(tmp_path):
    root = tmp_path / "outbox"
    _status(root, pending=0)
    _status(root / CREDENTIAL_NAMESPACE / FP, pending=3, held=3,
            refused_fingerprints={FP: "2026-10-23T17:23:00+00:00"})
    assert auth_blocked_since(Journal.read_status(root)) == "2026-10-23T17:23:00+00:00"


def test_writes_in_ops_keep_their_refusal_whatever_the_count_says(tmp_path):
    """A status write that failed leaves a stale 0 beside writes still queued."""
    root = tmp_path / "outbox"
    queue = _queue(root)
    _write(queue)
    status = json.loads(queue.status_file.read_text())
    status.update(pending=0, refused_fingerprints={FP: "2026-10-23T17:23:00+00:00"})
    queue.status_file.write_text(json.dumps(status))
    assert auth_blocked_since(Journal.read_status(queue.dir)) == "2026-10-23T17:23:00+00:00"


def test_a_multipart_upload_keeps_its_refusal(tmp_path):
    """status.json counts `ops/` alone; an upload waits in `multipart/ops`."""
    queue = tmp_path / "outbox" / CREDENTIAL_NAMESPACE / FP
    _status(queue, pending=0, refused_fingerprints={FP: "2026-10-23T17:23:00+00:00"})
    (queue / "multipart" / "ops").mkdir(parents=True)
    (queue / "multipart" / "ops" / "u.json").write_text("{}")
    assert auth_blocked_since(Journal.read_status(queue)) == "2026-10-23T17:23:00+00:00"


def test_the_drain_still_reads_the_refusals_it_wrote(tmp_path):
    """Its cooldowns count from those stamps (`_cooling_refusals`)."""
    queue = tmp_path / "outbox" / CREDENTIAL_NAMESPACE / FP
    _status(queue, pending=0, refused_fingerprints={FP: "2026-10-23T17:23:00+00:00"})
    raw = Journal.read_status(queue, include_receipts=False, keep_idle_refusals=True)
    assert raw["refused_fingerprints"] == {FP: "2026-10-23T17:23:00+00:00"}


def test_a_stale_refusal_starts_no_rescuer(tmp_path, monkeypatch):
    from probe.sdk import outbox_worker

    root = tmp_path / "outbox"
    _status(root, pending=0)
    _status(root / CREDENTIAL_NAMESPACE / FP, pending=0, refused_fingerprints={FP: "2026-10-23T17:23:00+00:00"})
    monkeypatch.setattr(Journal, "discover", staticmethod(lambda: []))
    status = Journal.read_status(root)
    assert outbox_worker._writes_held_back(Journal(str(root)), status) is False


def test_a_discard_of_every_write_forgets_their_credentials_refusal(tmp_path):
    root = tmp_path / "outbox"
    queue = _queue(root)
    _write(queue)
    queue.write_status(refused_fingerprints={FP: "2026-10-23T17:23:00+00:00", OTHER_FP: "2026-10-23T17:00:00+00:00"})
    Journal(str(root)).discard_held(credential=FP)
    written = json.loads(queue.status_file.read_text())["refused_fingerprints"]
    assert written == {OTHER_FP: "2026-10-23T17:00:00+00:00"}


# -- telemetry -------------------------------------------------------------------


def test_probe_outbox_discard_held_reports_what_it_threw_away(tmp_path, monkeypatch, captured, capsys):
    import importlib

    main = importlib.import_module("probe.cli.main")
    root = tmp_path / "outbox"
    queue = _queue(root)
    for step in (1, 2, 3):
        _write(queue, step)
    queue.append_http("PATCH", "/v1/runs/r", {"status": "completed"})
    monkeypatch.setattr(main, "_journal", lambda: Journal(str(root)))
    main.outbox_discard(op_id=None, held=True, credential=FP)
    assert "discarded 4 held write(s)" in capsys.readouterr().out
    (props,) = _discarded(captured)
    assert props["reason"] == "credential"
    assert (props["writes"], props["run_closes"], props["credentials"]) == (4, 1, 1)
    assert list(props["by_enqueue_day"].values()) == [4]
    assert FP not in json.dumps(props) and str(tmp_path) not in json.dumps(props)


def test_discarding_dead_letters_is_reported_too(tmp_path, monkeypatch, captured, capsys):
    import importlib

    main = importlib.import_module("probe.cli.main")
    root = tmp_path / "outbox"
    journal = Journal(str(root), context={"name": None, "base_url": HOSTED})
    journal.append_http("POST", "/v1/runs/r/metrics", {"points": []})
    (path, _op), = journal.pending()
    journal.failed_dir.mkdir(parents=True, exist_ok=True)
    os.replace(path, journal.failed_dir / path.name)
    monkeypatch.setattr(main, "_journal", lambda: Journal(str(root)))
    main.outbox_discard(op_id=None, held=False, credential=None)
    (props,) = _discarded(captured)
    assert (props["reason"], props["writes"]) == ("dead_letters", 1)


@pytest.mark.parametrize(("env", "base_url"), [({"PROBE_TELEMETRY": "off"}, HOSTED),
                                               ({}, "https://research.internal.example.com")])
def test_a_discard_report_honors_the_killswitch_and_self_host(tmp_path, monkeypatch, captured, env, base_url):
    for key, value in env.items():
        monkeypatch.setenv(key, value)
    queue = _queue(tmp_path / "outbox", base_url=base_url)
    _write(queue)
    counts = Journal(str(tmp_path / "outbox")).discard_held_counts(credential=FP)
    assert counts.writes == 1
    assert tm.emit_outbox_discarded(counts, reason=tm.DiscardReason.CREDENTIAL) is False
    assert _discarded(captured) == []


def test_writes_pinned_to_two_servers_are_not_reported(tmp_path, captured):
    root = tmp_path / "outbox"
    for fp, url in ((FP, HOSTED), (OTHER_FP, "https://research.internal.example.com")):
        queue = _queue(root, fp, base_url=url)
        _write(queue)
        _discard_all(queue)
    counts = relocate_discards(root)
    assert counts.writes == 2 and counts.base_url is None
    assert tm.emit_outbox_discarded(counts, reason=tm.DiscardReason.RELOCATED) is False


def test_the_rescuer_moves_discards_and_reports_them_once(tmp_path, monkeypatch, captured):
    """What answers "are Bucket's writes still on that Mac" with nothing for
    the customer to run: the every-command check starts the rescuer when a
    credential queue holds discards, and its pass reports them, by day."""
    from probe.sdk import outbox_worker

    root = tmp_path / "outbox"
    queue = _queue(root)
    for step in range(1, 6):
        _write(queue, step)
    _discard_all(queue)
    monkeypatch.setattr(Journal, "discover", staticmethod(lambda: []))
    monkeypatch.delenv("PROBE_OUTBOX_RESCUE", raising=False)
    started = []
    monkeypatch.setattr(outbox_worker, "spawn_rescuer", lambda journal: started.append(journal) or True)
    assert outbox_worker.maybe_rescue(Journal(str(root)), Journal.read_status(root) or {}) is True
    monkeypatch.setattr(journal_module, "rescue_lock_path", lambda: tmp_path / "rescue.lock")
    outbox_worker.rescue(str(root))
    (props,) = _discarded(captured)
    assert (props["reason"], props["writes"]) == ("relocated", 5)
    assert len(os.listdir(root / "discarded")) == 5
    outbox_worker.rescue(str(root))
    assert len(_discarded(captured)) == 1, "nothing left to move, nothing reported"


def test_an_sdk_discard_keeps_its_answer_and_is_counted(tmp_path, monkeypatch):
    """`cli/backfill_delivery.py` reads `discard_delivery(...)["state"]`: its
    return stays the state dict. The count rides `sdk.delivery.summary`."""
    from probe.sdk.client import Client

    client = Client(spool_dir=tmp_path / "outbox", async_writes=True, auto_drain=False,
                    base_url=HOSTED, token="probe_pat_x_0123456789abcdef")
    try:
        monkeypatch.setattr(Journal, "delivery_state", lambda self, c: {"state": "queued", "correlation": c})
        monkeypatch.setattr(Journal, "discard_request", lambda self, c: {"state": "discarded", "correlation": c})
        assert client.discard_delivery("c-1")["state"] == "discarded"
        assert client._discarded_requests == 1
        monkeypatch.setattr(Journal, "delivery_state", lambda self, c: {"state": "discarded", "correlation": c})
        client.discard_delivery("c-1")  # already set aside: not counted twice
        assert client._discarded_requests == 1
        assert "discarded" in tm.DELIVERY_SUMMARY_FIELDS
    finally:
        client.close()
