"""Queued uploads wait for their credential scan in `<journal>/waiting/`.

`log_artifact` copies the file there and returns; a promoter (the detached
worker, a barrier, `drain`, this process at exit) scans, redacts and
fingerprints the copy, and only then queues it as an op. These tests pin the
properties that make that safe: nothing unscanned ever reaches `ops/`, a crash
at any step ends in exactly one op, an older drainer never sees a waiting item,
and a run's close is never queued ahead of its uploads.
"""

from __future__ import annotations

import hashlib
import io
import json
import os
import subprocess
import sys
import tarfile
import threading
from pathlib import Path

import pytest

from probe.sdk import journal as journal_module
from probe.sdk import outbox_worker, secret_gate
from probe.sdk.journal import Journal
from probe.sdk.run import Run

from tests.conftest import make_client
from tests.test_outbox import seeded_run
from tests import test_outbox_cli

outbox_dir = test_outbox_cli.outbox_dir  # fixtures
wired_async = test_outbox_cli.wired_async

_GHP = "ghp_KKF0RDt0Xaetn6QMfStFUWSus4jowQUux6hu"
_TEXT = ('{"answer": 1}\n' + f'{{"env": "GITHUB_TOKEN={_GHP}"}}\n') * 20


@pytest.fixture(autouse=True)
def _isolated(monkeypatch, tmp_path):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(tmp_path / "config" / "probe.json"))
    monkeypatch.delenv("PROBE_TOKEN", raising=False)
    monkeypatch.delenv("PROBE_ASYNC", raising=False)
    monkeypatch.delenv("PROBE_ARTIFACT_OPAQUE_POLICY", raising=False)


def _journal(tmp_path) -> Journal:
    return Journal(tmp_path / "outbox")


def _source(tmp_path, text: str = _TEXT, name: str = "predictions.jsonl") -> str:
    path = tmp_path / name
    path.write_text(text)
    return str(path)


def _enqueue(journal: Journal, src: str, run_ref: str = "run-1") -> dict:
    return journal.append_upload(
        anchor="run", anchor_id=run_ref, name=Path(src).name, src_path=src,
        inline_hash=True, run_ref=run_ref, require_staged=True, defer_scan=True,
    )


def _only_op(journal: Journal) -> dict:
    ops = journal.pending()
    assert len(ops) == 1, [path.name for path, _ in ops]
    return ops[0][1]


def _assert_clean_blob(journal: Journal, op: dict) -> None:
    body = journal.blob_path(op).read_bytes()
    assert _GHP.encode() not in body
    assert b"<redacted:github-token>" in body
    assert op["upload"]["blob"] == hashlib.sha256(body).hexdigest()
    assert op["upload"]["size_bytes"] == len(body)


def test_enqueue_returns_before_any_scan(tmp_path, monkeypatch):
    journal = _journal(tmp_path)
    monkeypatch.setattr(journal_module, "redact_quick_bytes", lambda raw: pytest.fail("scanned on enqueue"))
    result = _enqueue(journal, _source(tmp_path))
    assert result["waiting"] is True and result["staged"] is True and result["blob"] is None
    assert journal.pending() == [], "nothing unscanned may sit in ops/"
    assert journal.waiting() == [result["op_id"]]
    assert Journal.read_status(journal.dir)["waiting"] == 1


def test_promotion_scans_redacts_and_queues(tmp_path):
    journal = _journal(tmp_path)
    result = _enqueue(journal, _source(tmp_path))
    assert journal.promote_waiting() == 1
    op = _only_op(journal)
    assert op["op_id"] == result["op_id"]
    _assert_clean_blob(journal, op)
    assert journal.waiting() == []
    assert os.listdir(journal.waiting_dir) == []


def test_the_queue_keeps_the_call_order(tmp_path):
    """The op takes the position of the CALL, reserved at enqueue: an op
    queued after the upload (a run's close) still sorts after it."""
    journal = _journal(tmp_path)
    _enqueue(journal, _source(tmp_path))
    journal.append_http("PATCH", "/v1/runs/run-1", {"status": "completed"}, run_ref="run-1")
    journal.promote_waiting()
    kinds = [op["kind"] for _, op in journal.pending()]
    assert kinds == ["upload", "http"]


def test_a_crash_before_the_record_leaves_nothing(tmp_path):
    journal = _journal(tmp_path)
    journal._ensure()
    (journal.waiting_dir / "deadbeef.bytes").write_bytes(b"half a copy")
    assert journal.promote_waiting() == 0
    assert journal.pending() == [] and os.listdir(journal.waiting_dir) == []


def test_a_crash_before_the_op_is_visible_promotes_once(tmp_path, monkeypatch):
    """Step (4) -- the rename into ops/ -- fails: the record is gone and the
    committed op waits beside the source. Recovery rolls it forward, once."""
    journal = _journal(tmp_path)
    _enqueue(journal, _source(tmp_path))
    real_replace = os.replace

    def crash(src, dst):
        if Path(dst).parent == journal.ops_dir:
            raise OSError("power cut")
        return real_replace(src, dst)

    monkeypatch.setattr(journal_module.os, "replace", crash)
    journal.promote_waiting()
    assert journal.pending() == []
    monkeypatch.setattr(journal_module.os, "replace", real_replace)
    assert journal.promote_waiting() == 1
    _assert_clean_blob(journal, _only_op(journal))
    assert journal.promote_waiting() == 0, "never two"


def test_a_crash_before_the_record_is_retired_starts_over(tmp_path, monkeypatch):
    journal = _journal(tmp_path)
    _enqueue(journal, _source(tmp_path))
    real_unlink = Path.unlink

    def crash(self, missing_ok=False):
        if self.suffix == ".json" and self.parent == journal.waiting_dir and not self.name.endswith(".op.json"):
            raise OSError("power cut")
        return real_unlink(self, missing_ok=missing_ok)

    monkeypatch.setattr(Path, "unlink", crash)
    journal.promote_waiting()
    monkeypatch.setattr(Path, "unlink", real_unlink)
    assert journal.pending() == [], "the op was never made visible"
    assert journal.promote_waiting() == 1
    _assert_clean_blob(journal, _only_op(journal))


def test_a_blob_collected_between_crash_and_recovery_is_derived_again(tmp_path, monkeypatch):
    """An older version's GC sees no op referencing the published blob while
    the committed op waits, and deletes it. Recovery rebuilds it from the
    source, which is deleted last."""
    journal = _journal(tmp_path)
    _enqueue(journal, _source(tmp_path))
    real_replace = os.replace
    monkeypatch.setattr(
        journal_module.os, "replace",
        lambda s, d: (_ for _ in ()).throw(OSError("cut")) if Path(d).parent == journal.ops_dir else real_replace(s, d),
    )
    journal.promote_waiting()
    monkeypatch.setattr(journal_module.os, "replace", real_replace)
    for blob in journal.blobs_dir.iterdir():
        blob.unlink()
    assert journal.promote_waiting() == 1
    _assert_clean_blob(journal, _only_op(journal))


def test_concurrent_promoters_make_one_op(tmp_path, monkeypatch):
    """The item lock, observed directly: four promoters race, the scan runs
    once (the reserved file name would hide a second op, not a second scan)."""
    journal = _journal(tmp_path)
    _enqueue(journal, _source(tmp_path))
    barrier = threading.Barrier(4)
    scans = []
    real = journal_module.redact_quick_bytes

    def slow_scan(raw):
        scans.append(1)
        threading.Event().wait(0.2)  # hold the item while the others arrive
        return real(raw)

    monkeypatch.setattr(journal_module, "redact_quick_bytes", slow_scan)

    def promote():
        barrier.wait()
        Journal(journal.dir).promote_waiting(wait=True, timeout=10)

    threads = [threading.Thread(target=promote) for _ in range(4)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    assert len(scans) == 1
    _assert_clean_blob(journal, _only_op(journal))


def test_an_uninspectable_item_is_dead_lettered(tmp_path, monkeypatch):
    journal = _journal(tmp_path)
    _enqueue(journal, _source(tmp_path))

    def refuse(raw):
        raise secret_gate.CredentialBlocked("Artifact upload refused: credential inspection failed")

    monkeypatch.setattr(journal_module, "redact_quick_bytes", refuse)
    assert journal.promote_waiting() == 0
    assert journal.pending() == [] and journal.waiting() == []
    (_, failed), = journal.failed()
    assert "credential inspection failed" in failed["last_error"]


def test_an_older_drainer_never_sees_a_waiting_upload(tmp_path):
    """The previous release's journal module, run in its own interpreter,
    reads `ops/` only: it finds no op, does not quarantine the waiting room, and
    its status rewrite cannot hide the item from this release's discovery."""
    journal = _journal(tmp_path)
    _enqueue(journal, _source(tmp_path))
    old_src = tmp_path / "old_src"
    repo = Path(__file__).resolve().parents[2]
    # The last main commit before the waiting room: permanent history, unlike
    # a branch commit a squash drops. CI's shallow checkout does not have it.
    released = "b66f45bd1"
    if subprocess.run(["git", "-C", str(repo), "cat-file", "-e", f"{released}^{{commit}}"],
                      capture_output=True).returncode != 0:
        pytest.skip(f"{released} is not in this checkout's history (shallow clone)")
    archive = subprocess.run(
        ["git", "-C", str(repo), "archive", released, "agent/src"],
        capture_output=True, check=True,
    ).stdout
    tarfile.open(fileobj=io.BytesIO(archive)).extractall(old_src, filter="data")
    script = (
        "import json, sys; from probe.sdk.journal import Journal; "
        f"j = Journal({str(journal.dir)!r}); "
        "assert not hasattr(j, 'waiting_dir'), 'not the old module'; "
        "j.quarantine_corrupt(); j.gc_blobs(); j.write_status(); "
        "print(json.dumps({'pending': len(j.pending()), 'failed': len(j.failed())}))"
    )
    env = {**os.environ, "PYTHONPATH": str(old_src / "agent" / "src")}
    out = subprocess.run([sys.executable, "-c", script], env=env, capture_output=True, text=True, check=True)
    assert json.loads(out.stdout.strip().splitlines()[-1]) == {"pending": 0, "failed": 0}
    assert journal.waiting(), "the waiting room survives the old drainer"
    assert Journal.read_status(journal.dir)["waiting"] == 1, "found by listing, not status.json"
    assert journal.promote_waiting() == 1
    _assert_clean_blob(journal, _only_op(journal))


def test_a_worker_blocked_by_another_worker_still_promotes(tmp_path):
    """The drain lease may belong to an OLDER worker that never looks in the
    waiting room; a new worker that finds it taken promotes and leaves."""
    from probe._shared import oscompat

    journal = _journal(tmp_path)
    _enqueue(journal, _source(tmp_path))
    holder = open(journal.dir / ".worker.lock", "a+")
    oscompat.flock(holder.fileno(), oscompat.LOCK_EX | oscompat.LOCK_NB)
    try:
        assert outbox_worker.run(str(journal.dir)) == 0
    finally:
        holder.close()
    _assert_clean_blob(journal, _only_op(journal))


def test_spawn_counts_waiting_uploads_even_when_status_says_empty(tmp_path, monkeypatch):
    journal = _journal(tmp_path)
    _enqueue(journal, _source(tmp_path))
    journal.write_status()  # an older worker's recount: pending 0
    spawned = []
    monkeypatch.setattr(outbox_worker.subprocess, "Popen", lambda *a, **k: spawned.append(a) or _Alive())
    monkeypatch.setattr(outbox_worker, "_spawn_took", lambda child, journal: True)
    assert outbox_worker.maybe_spawn(str(journal.dir)) is True
    assert spawned


class _Alive:
    def poll(self):
        return None


def test_finish_promotes_before_it_closes(app, tmp_path):
    run_id = seeded_run(app, tmp_path)
    client = make_client(app, tmp_spool=tmp_path / "outbox", async_writes=True)
    run = Run(client, {"id": run_id})
    client._auto_drain = False  # no worker: finish() itself must promote
    run.log_artifact("predictions.jsonl", path=_source(tmp_path))
    assert client.journal.waiting(run_ref=run_id)
    run.finish()
    assert client.journal.waiting() == [] and client.journal.pending() == []
    assert app.runs[run_id]["status"] == "completed"
    stored = [a for rows in app.artifacts.values() for a in rows if a.get("name") == "predictions.jsonl"]
    assert stored, "the upload landed before the close"
    body = app.blobs[stored[0]["id"]]
    assert _GHP.encode() not in body and b"<redacted:github-token>" in body
    client.close()


def test_containers_and_binary_are_never_rewritten():
    tar_bytes = io.BytesIO()
    with tarfile.open(fileobj=tar_bytes, mode="w") as archive:
        data = f"token={_GHP}\n".encode()
        info = tarfile.TarInfo("secrets.env")
        info.size = len(data)
        archive.addfile(info, io.BytesIO(data))
    raw = tar_bytes.getvalue()
    raw.decode("utf-8")  # an ASCII tar IS valid UTF-8 -- the container check must win
    assert secret_gate.redact_quick_bytes(raw) == (raw, secret_gate.InspectionResult())
    binary = b"\x80\x81" + _GHP.encode()
    assert secret_gate.redact_quick_bytes(binary)[0] == binary


def test_text_is_redacted_by_the_quick_check():
    cleaned, result = secret_gate.redact_quick_bytes(_TEXT.encode())
    assert _GHP.encode() not in cleaned and result.rewritten


def test_check_upload_reads_no_content(tmp_path, monkeypatch):
    src = _source(tmp_path)
    monkeypatch.setattr(secret_gate, "inspect_bytes", lambda *a, **k: pytest.fail("content scanned"))
    monkeypatch.setattr(secret_gate, "redact_quick", lambda *a, **k: pytest.fail("content scanned"))
    secret_gate.check_upload(src)


def test_the_strict_policy_keeps_its_inline_refusal(tmp_path, monkeypatch):
    monkeypatch.setenv("PROBE_ARTIFACT_OPAQUE_POLICY", "block")
    src = tmp_path / "weights.bin"
    src.write_bytes(bytes(range(256)) * 64)
    with pytest.raises(secret_gate.CredentialBlocked):
        secret_gate.check_upload(str(src))


# -- every close lands behind the run's waiting uploads --------------------

def test_a_direct_close_queues_behind_a_waiting_upload(app, tmp_path):
    """`set_status` is the one call every close goes through (finish, both
    `probe run end` modes, a caller's own). It finishes the run's scans first,
    so the journaled close sorts after the upload for any drainer version."""
    run_id = seeded_run(app, tmp_path)
    client = make_client(app, tmp_spool=tmp_path / "outbox", async_writes=True)
    client._auto_drain = False
    run = Run(client, {"id": run_id})
    run.log_artifact("predictions.jsonl", path=_source(tmp_path))
    run.set_status("completed")  # journaled: async client, no sync
    assert client.journal.waiting() == []
    kinds = [op["kind"] for _, op in client.journal.pending()]
    assert kinds == ["upload", "http"], "the close must sit BEHIND the upload"
    client.close()


def _cli_with_waiting_upload(app, outbox_dir, tmp_path):
    from tests.test_outbox_cli import start_run

    run_id = start_run(app)
    writer = make_client(app, tmp_spool=outbox_dir, async_writes=True)
    writer._auto_drain = False
    Run(writer, {"id": run_id}).log_artifact("predictions.jsonl", path=_source(tmp_path))
    assert Journal(outbox_dir).waiting(run_ref=run_id)
    writer.close()
    return run_id


def test_run_end_prepares_waiting_uploads_before_its_barrier(wired_async, outbox_dir, tmp_path, monkeypatch):
    from probe import cli
    from probe.sdk.journal import drain

    run_id = _cli_with_waiting_upload(wired_async, outbox_dir, tmp_path)
    fake = make_client(wired_async)
    monkeypatch.setattr(  # a drain that can actually reach the fake app
        "probe.sdk.journal.drain",
        lambda j, run_ref=None, **k: drain(j, run_ref=run_ref, client_factory=lambda ctx: fake),
    )
    assert cli.main(["--spool-dir", str(outbox_dir), "run", "end", run_id]) == 0
    fake.close()
    assert wired_async.runs[run_id]["status"] == "completed"
    stored = [a for rows in wired_async.artifacts.values() for a in rows if a.get("name") == "predictions.jsonl"]
    assert stored, "the barrier delivered the upload before the close"
    assert _GHP.encode() not in wired_async.blobs[stored[0]["id"]]


def test_run_end_refuses_while_an_upload_cannot_be_prepared(wired_async, outbox_dir, tmp_path, monkeypatch, capsys):
    from probe import cli

    run_id = _cli_with_waiting_upload(wired_async, outbox_dir, tmp_path)
    monkeypatch.setattr(Journal, "promote_waiting", lambda self, **kw: 0)  # a stuck promoter
    assert cli.main(["--spool-dir", str(outbox_dir), "run", "end", run_id]) == 2
    assert "could not be prepared" in capsys.readouterr().err
    assert wired_async.runs[run_id]["status"] != "completed"


def test_run_end_waits_for_a_scan_another_process_is_running(wired_async, outbox_dir, tmp_path, monkeypatch):
    """The case the barrier exists for: the worker holds the upload's item
    while it scans. A barrier that skipped it would close the run first."""
    from probe._shared import oscompat
    import time as _time

    from probe import cli
    from probe.sdk.journal import drain

    run_id = _cli_with_waiting_upload(wired_async, outbox_dir, tmp_path)
    (op_id,) = Journal(outbox_dir).waiting(run_ref=run_id)
    lock = open(Journal(outbox_dir).waiting_dir / f"{op_id}.lock", "a+")
    oscompat.flock(lock.fileno(), oscompat.LOCK_EX)
    threading.Timer(0.5, lock.close).start()  # the "worker" finishes scanning
    fake = make_client(wired_async)
    monkeypatch.setattr(
        "probe.sdk.journal.drain",
        lambda j, run_ref=None, **k: drain(j, run_ref=run_ref, client_factory=lambda ctx: fake),
    )
    started = _time.monotonic()
    assert cli.main(["--spool-dir", str(outbox_dir), "run", "end", run_id]) == 0
    fake.close()
    assert _time.monotonic() - started >= 0.4, "it waited for the scan"
    stored = [a for rows in wired_async.artifacts.values() for a in rows if a.get("name") == "predictions.jsonl"]
    assert stored, "delivered BEFORE the run was closed"
    assert wired_async.runs[run_id]["status"] == "completed"


# -- order, failures, and limits ------------------------------------------

def _hold(journal: Journal, op_id: str):
    """Hold an item's lock the way another process's promoter would."""
    from probe._shared import oscompat

    handle = open(journal.waiting_dir / f"{op_id}.lock", "a+")
    oscompat.flock(handle.fileno(), oscompat.LOCK_EX)
    return handle


def test_a_run_never_passes_its_busy_upload(tmp_path, monkeypatch):
    """Two versions of one artifact must arrive in the order they were logged:
    while another process scans the first, the second stays waiting, and the
    run's close (already queued) is held back from delivery."""
    journal = _journal(tmp_path)
    first = _enqueue(journal, _source(tmp_path, name="ckpt-1.jsonl"))
    second = _enqueue(journal, _source(tmp_path, name="ckpt-2.jsonl"))
    other = _enqueue(journal, _source(tmp_path, name="other.jsonl"), run_ref="run-2")
    journal.append_http("PATCH", "/v1/runs/run-1", {"status": "completed"}, run_ref="run-1")
    assert journal.waiting() == [first["op_id"], second["op_id"], other["op_id"]], "queue order"
    delivered: list[dict] = []
    monkeypatch.setattr(journal_module, "_execute", lambda j, client, path, op, run_ids: delivered.append(op))
    handle = _hold(journal, first["op_id"])
    try:
        assert journal.promote_waiting() == 1, "only the other run's upload goes"
        assert journal.waiting(run_ref="run-1") == [first["op_id"], second["op_id"]]
        report = journal_module.drain(journal, client_factory=lambda ctx: object())
        assert report.held_back == 1, "the close waits behind the busy upload"
        assert [(op["kind"], op["run_ref"]) for op in delivered] == [("upload", "run-2")]
    finally:
        handle.close()
    delivered.clear()
    journal_module.drain(journal, client_factory=lambda ctx: object())
    assert [(op["kind"], (op.get("upload") or {}).get("name")) for op in delivered] == [
        ("upload", "ckpt-1.jsonl"), ("upload", "ckpt-2.jsonl"), ("http", None),
    ]


@pytest.mark.parametrize("record", ["", "{}", '{"op": {"op_id": "x"}}', "[1]"])
def test_an_unreadable_record_does_not_hold_up_the_rest(tmp_path, record):
    journal = _journal(tmp_path)
    good = _enqueue(journal, _source(tmp_path))
    (journal.waiting_dir / "0badc0de.json").write_text(record)
    (journal.waiting_dir / "0badc0de.bytes").write_bytes(b"x")
    assert journal.promote_waiting(run_ref="run-1") == 1
    assert _only_op(journal)["op_id"] == good["op_id"]
    (_, failed), = journal.failed()
    assert "unreadable" in failed["last_error"] and "nothing was sent" in failed["last_error"]
    assert os.listdir(journal.waiting_dir) == []


def test_a_missing_copy_is_dead_lettered_not_retried_forever(tmp_path):
    journal = _journal(tmp_path)
    result = _enqueue(journal, _source(tmp_path))
    (journal.waiting_dir / f"{result['op_id']}.bytes").unlink()
    assert journal.promote_waiting() == 0
    assert journal.waiting() == [] and journal.pending() == []
    (_, failed), = journal.failed()
    assert "missing" in failed["last_error"]


def test_an_admitted_upload_promotes_past_a_full_queue(tmp_path, monkeypatch):
    """The ceiling counted the upload when it was queued. Refusing it again at
    promotion deadlocks: its run's later ops fill the queue, and drain holds
    them behind this very upload."""
    journal = _journal(tmp_path)
    monkeypatch.setattr(journal_module, "MAX_PENDING_OPS", 1)
    _enqueue(journal, _source(tmp_path))
    journal.append_http("POST", "/v1/runs/run-1/metrics", {"loss": 0.1}, run_ref="run-1")
    assert journal.promote_waiting() == 1
    assert [op["kind"] for _, op in journal.pending()] == ["upload", "http"]


def test_a_missing_copy_keeps_its_run(tmp_path):
    """A close checks its run's dead letters; one filed under no run would let
    `probe run end` report success over a lost upload."""
    journal = _journal(tmp_path)
    result = _enqueue(journal, _source(tmp_path))
    (journal.waiting_dir / f"{result['op_id']}.bytes").unlink()
    journal.promote_waiting()
    (_, failed), = journal.failed()
    assert failed["run_ref"] == "run-1" and failed["op_id"] == result["op_id"]


def test_a_promotion_between_the_two_reads_cannot_release_the_close(tmp_path, monkeypatch):
    """drain reads the waiting room, then the queue. A promoter finishing in
    between leaves the upload in both views -- never in neither."""
    journal = _journal(tmp_path)
    _enqueue(journal, _source(tmp_path))
    journal.append_http("PATCH", "/v1/runs/run-1", {"status": "completed"}, run_ref="run-1")
    delivered: list[dict] = []
    monkeypatch.setattr(journal_module, "_execute", lambda j, client, path, op, run_ids: delivered.append(op))
    real_positions, real_promote = Journal.waiting_positions, Journal.promote_waiting

    def positions_then_promote(self):
        seen = real_positions(self)
        real_promote(Journal(self.dir))  # another process finishes the scan now
        return seen

    monkeypatch.setattr(Journal, "waiting_positions", positions_then_promote)
    monkeypatch.setattr(Journal, "promote_waiting", lambda self, **kw: 0)  # this drain promotes nothing
    journal_module.drain(journal, client_factory=lambda ctx: object())
    assert [op["kind"] for op in delivered] == ["upload"], "the close waits one pass, never goes first"


def test_held_back_ops_are_reported_with_a_receipts_namespace_present(tmp_path, monkeypatch):
    """The worker waits between passes only when the report says ops were held
    back; with a `delivery-v1` namespace the report is a sum of two."""
    journal = _journal(tmp_path)
    first = _enqueue(journal, _source(tmp_path))
    journal.append_http("PATCH", "/v1/runs/run-1", {"status": "completed"}, run_ref="run-1")
    Journal.for_receipts(journal.dir)._ensure()
    assert len(journal.namespaces()) == 2
    monkeypatch.setattr(journal_module, "_execute", lambda *a, **k: None)
    handle = _hold(journal, first["op_id"])
    try:
        assert journal_module.drain(journal, client_factory=lambda ctx: object()).held_back == 1
    finally:
        handle.close()


def test_an_item_caught_between_promotion_steps_is_still_waiting(tmp_path, monkeypatch):
    """The listing saw `<id>.json`; by the read, a promoter has written
    `<id>.op.json` and unlinked the record (steps 2-3) but not yet renamed it
    into ops/. The item is still waiting, not gone."""
    journal = _journal(tmp_path)
    result = _enqueue(journal, _source(tmp_path))
    stale = os.listdir(journal.waiting_dir)
    record = journal.waiting_dir / f"{result['op_id']}.json"
    op = json.loads(record.read_text())["op"]
    (journal.waiting_dir / f"{result['op_id']}.op.json").write_text(json.dumps(op))
    record.unlink()
    real_listdir = os.listdir
    monkeypatch.setattr(
        journal_module.os, "listdir",
        lambda path: stale if Path(path) == journal.waiting_dir else real_listdir(path),
    )
    assert journal.waiting_positions() == {"run-1": op["queue_filename"]}


def test_the_worker_looks_again_at_an_upload_that_arrived_during_its_grace(tmp_path, monkeypatch):
    journal = _journal(tmp_path)
    journal._ensure()
    passes, held = [], []
    real_drain = journal_module.drain
    monkeypatch.setattr(journal_module, "drain", lambda j, **k: passes.append(1) or real_drain(j, **k))

    def sleep(_seconds):
        if not held:  # an upload lands mid-grace, and another promoter is scanning it
            result = _enqueue(journal, _source(tmp_path))
            held.append(_hold(journal, result["op_id"]))

    monkeypatch.setattr(outbox_worker.time, "sleep", sleep)
    monkeypatch.setattr(outbox_worker, "_WAITING_PASSES", 3)
    try:
        assert outbox_worker.run(str(journal.dir)) == 0
    finally:
        for handle in held:
            handle.close()
    assert len(passes) > 1, "the worker left without looking at the new upload"


def test_a_non_blocking_waiting_upload_holds_no_close(tmp_path):
    """`append_upload(blocking=False)` (output capture's flag) must never keep a
    run open; waiting for its scan does not change that."""
    journal = _journal(tmp_path)
    result = journal.append_upload(
        anchor="run", anchor_id="run-1", name="out.log", src_path=_source(tmp_path),
        inline_hash=True, run_ref="run-1", require_staged=True, defer_scan=True, blocking=False,
    )
    assert journal.waiting(run_ref="run-1") == [result["op_id"]]
    assert journal.waiting_positions() == {}
    assert journal.waiting_for_close("run-1") == []
    journal.promote_waiting()
    assert _only_op(journal)["blocking"] is False


def test_waiting_uploads_count_against_the_op_ceiling(tmp_path, monkeypatch):
    journal = _journal(tmp_path)
    monkeypatch.setattr(journal_module, "MAX_PENDING_OPS", 2)
    _enqueue(journal, _source(tmp_path, name="a.jsonl"))
    _enqueue(journal, _source(tmp_path, name="b.jsonl"))
    with pytest.raises(journal_module.OutboxFull):
        _enqueue(journal, _source(tmp_path, name="c.jsonl"))


def test_the_disk_floor_prices_both_copies(tmp_path, monkeypatch):
    """Until promotion ends the upload exists twice: the waiting copy and the
    clean blob. Room for one copy is not room enough."""
    journal = _journal(tmp_path)
    src = _source(tmp_path, text="x" * 10_000)
    monkeypatch.setattr(journal_module, "MIN_FREE_BYTES", 1_000)
    usage = journal_module.shutil.disk_usage(tmp_path)._replace(free=1_000 + 15_000)
    monkeypatch.setattr(journal_module.shutil, "disk_usage", lambda _path: usage)
    result = _enqueue(journal, src)
    assert result["op_id"] is None and "low disk" in result["unstaged_reason"]
    assert journal.waiting() == []


def test_a_waiting_upload_keeps_its_producers_identity(tmp_path):
    journal = _journal(tmp_path)
    journal.register_producer("sdk-producer-1")
    result = _enqueue(journal, _source(tmp_path))
    Journal(journal.dir).promote_waiting()  # a promoter with no producer of its own
    op = _only_op(journal)
    assert op["op_id"] == result["op_id"]
    assert op["producer_id"] == "sdk-producer-1" and op["producer_sequence"] >= 1


def test_the_orphan_sweep_leaves_an_enqueue_in_progress_alone(tmp_path):
    journal = _journal(tmp_path)
    journal._ensure()
    (journal.waiting_dir / "cafef00d.bytes").write_bytes(b"being copied")
    handle = _hold(journal, "cafef00d")
    try:
        journal.promote_waiting()
        assert (journal.waiting_dir / "cafef00d.bytes").exists()
    finally:
        handle.close()


@pytest.mark.skipif(os.name == "nt", reason="Windows cannot unlink an open file, so a held lock is always the file at its path")
def test_a_lock_unlinked_under_its_opener_is_not_held(tmp_path):
    """Item locks are unlinked when an item is done. One opened just before
    that and locked just after is a lock on nothing: the next opener makes a
    new file, so both would 'hold' the item."""
    path = tmp_path / "item.lock"
    handle = open(path, "a+")
    path.unlink()
    path.touch()
    assert journal_module._same_file(handle, path) is False
    handle.close()
    with journal_module._item_lock(path):
        with journal_module._try_lock(path) as held:
            assert held is False


def test_the_strict_policy_scans_in_full_before_queueing(tmp_path, monkeypatch):
    """`PROBE_ARTIFACT_OPAQUE_POLICY=block` keeps the full inspection on the
    caller's thread, as before: nothing waits, and an ESCAPED credential --
    which the quick check leaves to the server -- is redacted here."""
    monkeypatch.setenv("PROBE_ARTIFACT_OPAQUE_POLICY", "block")
    journal = _journal(tmp_path)
    escaped = _GHP.replace("K", "%4B")
    result = _enqueue(journal, _source(tmp_path, text=f"url: https://h/x?q={escaped}\n" * 50))
    assert "waiting" not in result and journal.waiting() == []
    body = journal.blob_path(_only_op(journal)).read_bytes()
    assert escaped.encode() not in body


def test_a_strict_close_refuses_while_an_upload_waits(app, tmp_path, monkeypatch):
    run_id = seeded_run(app, tmp_path)
    client = make_client(app, tmp_spool=tmp_path / "outbox", async_writes=True)
    client._auto_drain = False
    run = Run(client, {"id": run_id})
    run.log_artifact("predictions.jsonl", path=_source(tmp_path))
    monkeypatch.setattr(Journal, "promote_waiting", lambda self, **kw: 0)  # a stuck promoter
    from probe.sdk import errors

    with pytest.raises(errors.RosError, match="not closed"):
        run.finish(strict=True)
    assert not [op for _, op in client.journal.pending() if op["kind"] == "http"], "no close queued"
    client.close()


def test_a_default_close_queues_behind_a_stuck_upload_instead_of_raising(
    app, tmp_path, monkeypatch
):
    """Plan 0.2: the default close never raises. An upload still waiting for
    its scan holds the close -- the terminal status is queued BEHIND it."""
    run_id = seeded_run(app, tmp_path)
    client = make_client(app, tmp_spool=tmp_path / "outbox", async_writes=True)
    client._auto_drain = False
    run = Run(client, {"id": run_id})
    run.log_artifact("predictions.jsonl", path=_source(tmp_path))
    monkeypatch.setattr(Journal, "promote_waiting", lambda self, **kw: 0)  # a stuck promoter

    report = run.finish(flush_timeout=0.5)

    assert report["finish_queued"] is True
    (close_path, close), = [(p, op) for p, op in client.journal.pending() if op["kind"] == "http"]
    assert close["body"]["summary"]["probe_finish"]["deferred"] is True
    assert close_path.name > client.journal.waiting_positions()[run_id], "held behind the upload"
    assert app.runs[run_id]["status"] != "completed"
    client.close()


def test_a_fail_open_close_is_queued_and_held_behind_the_upload(app, tmp_path, monkeypatch):
    """`set_status(strict=False)` never raises -- it may be closing a run that
    is failing -- so the close is queued; delivery holds it behind the upload."""
    run_id = seeded_run(app, tmp_path)
    client = make_client(app, tmp_spool=tmp_path / "outbox", async_writes=True)
    client._auto_drain = False
    run = Run(client, {"id": run_id})
    run.log_artifact("predictions.jsonl", path=_source(tmp_path))
    real = Journal.promote_waiting
    monkeypatch.setattr(Journal, "promote_waiting", lambda self, **kw: 0)
    run.set_status("failed", strict=False)
    assert [op["kind"] for _, op in client.journal.pending()] == ["http"]
    positions = client.journal.waiting_positions()
    (close_path, _), = client.journal.pending()
    assert close_path.name > positions[run_id], "held back: queued after the waiting upload"
    monkeypatch.setattr(Journal, "promote_waiting", real)
    client.close()


def test_the_exit_hook_promotes_this_processes_runs_and_respects_auto_drain(app, tmp_path, monkeypatch):
    from probe.sdk import client as client_module

    hooks, spawned = [], []
    monkeypatch.setattr(client_module, "_at_exit", hooks.append)
    monkeypatch.setattr(outbox_worker, "maybe_spawn", lambda d: spawned.append(d) or True)
    run_id = seeded_run(app, tmp_path)
    client = make_client(app, tmp_spool=tmp_path / "outbox", async_writes=True)
    client._auto_drain = False
    run = Run(client, {"id": run_id})
    run.log_artifact("a.jsonl", path=_source(tmp_path, name="a.jsonl"))
    run.log_artifact("b.jsonl", path=_source(tmp_path, name="b.jsonl"))
    foreign = _enqueue(client.journal, _source(tmp_path, name="c.jsonl"), run_ref="another-process")
    assert len(hooks) == 1, "registered once"
    hooks[0]()
    assert client.journal.waiting() == [foreign["op_id"]], "only this process's runs"
    assert spawned == [], "auto_drain off: no worker"
    client.close()


def test_outbox_status_reports_waiting_uploads(outbox_dir, tmp_path, capsys):
    from probe import cli

    _enqueue(Journal(outbox_dir), _source(tmp_path))
    assert cli.main(["--spool-dir", str(outbox_dir), "outbox", "status"]) == 2
    assert "waiting" in capsys.readouterr().out
