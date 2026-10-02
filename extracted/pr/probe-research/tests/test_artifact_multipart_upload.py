"""Artifacts over 64 MiB, uploaded in parts (plan item (g)).

Against the fake server's multipart doors (`FakeApp._multipart`), which follow
0273's contract: the server cuts the layout, presigns part URLs, lists what it
holds, size-checks complete and settles after its verifier has hashed the
assembled parts. What these pin is the SDK's half:

  * `log_artifact` of a 200 MiB file STAGES it (a hardlink here) and returns at
    once; the outbox sends the parts later, in a lane of its own;
  * an old server (no `artifact_multipart`) keeps 0.7's warning and reference row;
  * a restarted worker resends only the parts the server does not hold;
  * a staged copy rewritten in place aborts the upload and records a reference
    row; one replaced by rename (checkpoint rotation) uploads what was logged;
  * a metric logged after the checkpoint is delivered before its next slice;
  * `finish()` says how many are still uploading instead of waiting -- when a
    detached worker on durable storage carries them; otherwise it sends them
    itself and records what did not make it;
  * an older worker holding the outbox never sees the new kind: it has a queue
    of its own that no earlier release reads.
"""

from __future__ import annotations

import errno
import hashlib
import json
import os
import time
import warnings

import pytest

from probe.sdk import errors, journal as journal_module, multipart, outbox_worker
from tests.conftest import make_client, open_run

MiB = 1024 * 1024
TWO_HUNDRED_MIB = 200 * MiB


def _sparse(path, size=TWO_HUNDRED_MIB, *, head: bytes = b""):
    with open(path, "wb") as fh:
        if head:
            fh.write(head)
        fh.truncate(size)
    return path


def _sha(path) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(8 * MiB), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _rows(app, run_id, name):
    return [a for a in app.artifacts.get(run_id, []) if a.get("name") == name]


def _multipart_ops(journal):
    return [op for _, op in multipart.pending(journal)]


def _flush_until(client, done, *, seconds: float = 30.0) -> None:
    """Flush until ``done()``: the staged copy is hashed on a background
    thread, so a pass may come back before there is anything to send."""
    deadline = time.monotonic() + seconds
    while time.monotonic() < deadline:
        client.flush()
        if done():
            return
        time.sleep(0.05)
    raise AssertionError("timed out")


def _drain_until_done(client, *, passes: int = 0):
    try:
        _flush_until(client, lambda: not _multipart_ops(client.journal))
    except AssertionError:
        raise AssertionError("the multipart op never finished") from None


@pytest.fixture
def mp_app(app):
    app.supports_artifact_multipart = True
    return app


@pytest.fixture
def mp_client(mp_app, tmp_path):
    return make_client(mp_app, tmp_spool=tmp_path / "outbox", async_writes=True)


def test_a_200_mib_file_is_staged_returns_at_once_and_lands_in_parts(mp_app, mp_client, tmp_path):
    run = open_run(mp_client, experiment="e", name="r")
    big = _sparse(tmp_path / "ckpt-4000.pt", head=b"weights!")
    started = time.monotonic()
    assert run.log_artifact("ckpt", path=str(big)) is None
    assert time.monotonic() - started < 2.0, "log_artifact must not hash or send 200 MiB"
    assert mp_app.multipart == {}, "nothing is sent from the training thread"

    [op] = _multipart_ops(mp_client.journal)
    assert op["blocking"] is False and op["lane"] == f"multipart:{op['op_id']}"
    staged = op["multipart"]["staged_path"]
    assert op["multipart"]["stage_mode"] == "hardlink"
    assert os.stat(staged).st_ino == os.stat(big).st_ino

    _drain_until_done(mp_client)
    [upload] = mp_app.multipart.values()
    assert (upload["part_size"], upload["part_count"]) == (64 * MiB, 4)
    assert sorted(n for _, n in mp_app.multipart_part_puts) == [1, 2, 3, 4]
    assert upload["state"] == "verified"
    [row] = _rows(mp_app, run.id, "ckpt.pt")
    assert row["status"] == "complete" and row["is_reference"] is False
    assert row["content_hash"] == _sha(big) and row["size_bytes"] == TWO_HUNDRED_MIB
    assert not os.path.exists(staged), "the staged copy goes once the server verified it"
    assert os.path.exists(big), "the caller's file is never touched"
    assert mp_app.puts == [], "no byte went through the single-PUT relay"


def test_an_old_server_keeps_the_warning_and_the_reference_row(app, tmp_path):
    client = make_client(app, tmp_spool=tmp_path / "outbox", async_writes=True)
    run = open_run(client, experiment="e", name="r")
    big = _sparse(tmp_path / "ckpt.pt", 70 * MiB)
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        run.log_artifact("ckpt", path=str(big))
    client.flush()
    [row] = _rows(app, run.id, "ckpt.pt")
    assert row["is_reference"] is True and row["meta"]["upload"] == "failed"
    assert "exceeds inspection size limit" in row["meta"]["upload_error"]
    assert any("ckpt" in str(w.message) for w in caught)
    assert _multipart_ops(client.journal) == []
    assert not multipart.staged_dir(client.journal).exists() or not os.listdir(
        multipart.staged_dir(client.journal)
    ), "nothing staged for a server that cannot take it"


def test_a_restarted_worker_sends_only_the_missing_parts(mp_app, mp_client, tmp_path, monkeypatch):
    """The first worker dies after parts 1, 2 and 4 landed (part 3's PUT
    failed); a fresh process (new Journal, new Client, same outbox) lists what
    the server holds and sends part 3 alone."""
    run = open_run(mp_client, experiment="e", name="r")
    big = _sparse(tmp_path / "ckpt.pt", head=b"resume")
    run.log_artifact("ckpt", path=str(big))

    real_put = mp_client.transport.put_part

    def dies_on_part_3(url, path, *, offset, length, **kw):
        if url.endswith("/3"):
            raise errors.TransportError("connection reset by peer")
        return real_put(url, path, offset=offset, length=length, **kw)

    monkeypatch.setattr(mp_client.transport, "put_part", dies_on_part_3)
    _flush_until(mp_client, lambda: len(mp_app.multipart_part_puts) >= 3)
    assert sorted(n for _, n in mp_app.multipart_part_puts) == [1, 2, 4]
    [op] = _multipart_ops(mp_client.journal)
    assert op["multipart"]["upload_id"], "the upload's identity survives the failure"
    monkeypatch.setattr(mp_client.transport, "put_part", real_put)

    before = len(mp_app.multipart_part_puts)
    restarted = make_client(mp_app, tmp_spool=tmp_path / "outbox", async_writes=True)
    _drain_until_done(restarted)
    assert [n for _, n in mp_app.multipart_part_puts[before:]] == [3]
    [upload] = mp_app.multipart.values()
    assert upload["state"] == "verified"
    assert _rows(mp_app, run.id, "ckpt.pt")[0]["content_hash"] == _sha(big)


def test_a_staged_copy_rewritten_in_place_aborts_and_records_a_reference(
    mp_app, mp_client, tmp_path, monkeypatch
):
    """A hardlink shares the inode: a trainer that rewrites the SAME file in
    place changes the staged copy under the upload. That is detected (size /
    mtime of the inode), the server's upload is aborted, the staged copy
    deleted, and the file recorded as a reference with the reason."""
    run = open_run(mp_client, experiment="e", name="r")
    big = _sparse(tmp_path / "ckpt.pt", head=b"epoch-1")
    run.log_artifact("ckpt", path=str(big))
    real_put = mp_client.transport.put_part

    def stall_part_4(url, path, *, offset, length, **kw):
        if url.endswith("/4"):
            raise errors.TransportError("timed out")
        return real_put(url, path, offset=offset, length=length, **kw)

    monkeypatch.setattr(mp_client.transport, "put_part", stall_part_4)
    _flush_until(mp_client, lambda: len(mp_app.multipart_part_puts) >= 3)  # parts 1-3 land
    monkeypatch.setattr(mp_client.transport, "put_part", real_put)
    [op] = _multipart_ops(mp_client.journal)
    staged = op["multipart"]["staged_path"]
    with open(big, "r+b") as fh:  # same inode, new bytes
        fh.write(b"epoch-2")
    os.utime(big, ns=(time.time_ns(), time.time_ns() + 10**9))

    with warnings.catch_warnings(record=True):
        warnings.simplefilter("always")
        mp_client.flush()
    assert _multipart_ops(mp_client.journal) == []
    [upload] = mp_app.multipart.values()
    assert upload["state"] == "aborted", "the server's parts are discarded"
    references = [r for r in _rows(mp_app, run.id, "ckpt.pt") if r["is_reference"]]
    assert len(references) == 1
    assert "changed while it was uploading" in references[0]["meta"]["upload_error"]
    assert not os.path.exists(staged)


def test_rotation_by_rename_uploads_what_was_logged(mp_app, mp_client, tmp_path):
    """The failure mode the staging exists for: the trainer writes the next
    checkpoint under a temp name and renames it over this one (and deletes the
    old ones) while the upload waits. The hardlink kept the inode."""
    run = open_run(mp_client, experiment="e", name="r")
    big = _sparse(tmp_path / "ckpt.pt", head=b"step-1000")
    logged = _sha(big)
    run.log_artifact("ckpt", path=str(big))
    fresh = _sparse(tmp_path / ".ckpt.pt.tmp", head=b"step-2000")
    os.replace(fresh, big)
    _drain_until_done(mp_client)
    [row] = _rows(mp_app, run.id, "ckpt.pt")
    assert row["status"] == "complete" and row["content_hash"] == logged
    os.remove(big)


def test_a_later_metric_is_delivered_before_the_checkpoints_next_slice(mp_app, mp_client, tmp_path):
    run = open_run(mp_client, experiment="e", name="r")
    big = _sparse(tmp_path / "ckpt.pt")
    run.log_artifact("ckpt", path=str(big))
    run.log({"train/loss": 0.5}, step=7)
    first_part = None
    metrics_at = None
    _flush_until(mp_client, lambda: bool(mp_app.multipart_part_puts))
    for index, request in enumerate(mp_app.requests):
        if request.url.path.startswith("/part/") and first_part is None:
            first_part = index
        if request.url.path.endswith("/metrics") and request.method == "POST" and metrics_at is None:
            metrics_at = index
    assert metrics_at is not None and first_part is not None
    assert metrics_at < first_part, "the metric must not wait behind 200 MiB of parts"
    _drain_until_done(mp_client)


def test_finish_says_how_many_are_still_uploading_and_does_not_wait(mp_app, mp_client, tmp_path, monkeypatch):
    # A client a detached worker delivers for (the default: a login's token,
    # the default transport), on durable disk. Pin it: a CI runner's outbox
    # disk reads as ephemeral (probe.sdk.ephemeral.describe), which sends the
    # op down the disposable-machine path (a reference row) instead.
    monkeypatch.setenv("PROBE_EPHEMERAL", "0")
    mp_client._auto_drain = True
    run = open_run(mp_client, experiment="e", name="r")
    big = _sparse(tmp_path / "ckpt.pt")
    run.log_artifact("ckpt", path=str(big))
    run.log({"train/loss": 0.5}, step=1)
    # Keep the op from moving during the close's barrier: a barrier never runs
    # a multipart upload anyway, and the close must not wait on it.
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        started = time.monotonic()
        run.finish()
        took = time.monotonic() - started
    assert took < 5.0
    messages = [str(w.message) for w in caught]
    assert any("1 artifact(s) still uploading" in m for m in messages), messages
    assert _multipart_ops(mp_client.journal), "still queued for the worker"
    assert mp_app.multipart == {}, "the close sent none of it"
    _drain_until_done(mp_client)
    assert _rows(mp_app, run.id, "ckpt.pt")[0]["status"] == "complete"


def test_an_older_worker_never_sees_the_new_kind(mp_app, mp_client, tmp_path):
    """1.11 and review P2/P3: a worker of an earlier release (0.190, which
    dead-letters an unknown kind; 0.191+, which holds it in its run's lane
    and never exits) must never find the op. It has a queue of its own that
    no earlier release reads -- nothing lands in `ops/` -- and the live worker
    is still asked to step aside for a current one."""
    import fcntl

    journal = mp_client.journal
    journal._ensure()
    lease = open(outbox_worker._lease_path(journal), "a+")
    fcntl.flock(lease.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
    try:
        run = open_run(mp_client, experiment="e", name="r")
        big = _sparse(tmp_path / "ckpt.pt")
        run.log_artifact("ckpt", path=str(big))
        run.log({"train/loss": 0.5}, step=1)
        assert all(op.get("kind") != multipart.KIND for _, op in journal.pending())
        assert len(_multipart_ops(journal)) == 1
        stop = json.loads(outbox_worker._stop_path(journal).read_text())
        assert multipart.KIND in stop["kinds"]
        # What an older release's pass sees: the shared queue only.
        assert journal_module.drain(journal, long_ops=False, client_factory=mp_client._outbox_client_factory()).delivered >= 1
        assert _multipart_ops(journal), "untouched by a pass that cannot run it"
    finally:
        fcntl.flock(lease.fileno(), fcntl.LOCK_UN)
        lease.close()
    _drain_until_done(mp_client)
    assert _rows(mp_app, run.id, "ckpt.pt")[0]["status"] == "complete"
    mode = os.stat(multipart.ops_dir(journal)).st_mode & 0o777
    assert mode == 0o700 and os.stat(multipart.ops_dir(journal).parent).st_mode & 0o777 == 0o700


def test_an_in_process_sender_delivers_the_upload_and_says_what_it_delivers(mp_app, tmp_path):
    """Review P1: a client that sends its own writes (drain_interval; a token
    passed in code gets one, #2041) holds the worker lease. It now writes a
    caps file like a worker, and its own sender runs the upload."""
    client = make_client(mp_app, tmp_spool=tmp_path / "outbox", async_writes=True, drain_interval=0.1)
    try:
        run = open_run(client, experiment="e", name="r")
        big = _sparse(tmp_path / "ckpt.pt", 70 * MiB, head=b"exporter")
        run.log_artifact("ckpt", path=str(big))
        deadline = time.monotonic() + 20
        while time.monotonic() < deadline and _multipart_ops(client.journal):
            time.sleep(0.1)
        caps = outbox_worker.live_worker_kinds(str(client.journal.dir))
        assert caps is None or multipart.KIND in caps
        assert not os.path.exists(outbox_worker._stop_path(client.journal)), "no one was asked to step aside"
        assert _multipart_ops(client.journal) == [], "the in-process sender ran it"
        assert _rows(mp_app, run.id, "ckpt.pt")[0]["status"] == "complete"
    finally:
        client.close()


def test_with_nothing_to_carry_it_later_finish_sends_the_upload_itself(mp_app, mp_client, tmp_path):
    """Review P2: a client whose writes no detached worker carries after it
    exits (here: a custom transport, like a token passed in code), or an
    outbox on a disposable disk, must not close with the upload queued and
    unrecorded. finish() sends it -- done once the server has every byte."""
    assert multipart.settle_reason(mp_client) is not None
    run = open_run(mp_client, experiment="e", name="r")
    big = _sparse(tmp_path / "ckpt.pt", 70 * MiB, head=b"settle")
    run.log_artifact("ckpt", path=str(big))
    staged = _multipart_ops(mp_client.journal)[0]["multipart"]["staged_path"]
    mp_app.multipart_verify_polls = 99  # the server is still verifying when the run closes
    run.finish(flush_timeout=30)
    assert _multipart_ops(mp_client.journal) == []
    [upload] = mp_app.multipart.values()
    assert upload["state"] == "verifying", "every byte is on the server"
    assert not os.path.exists(staged)
    assert not [r for r in _rows(mp_app, run.id, "ckpt.pt") if r["is_reference"]]


def test_an_upload_finish_cannot_complete_in_time_is_recorded_before_it_returns(
    mp_app, mp_client, tmp_path, monkeypatch
):
    """...and what does not make it within the close's budget is recorded as a
    reference row before finish() returns: never a run with no record."""
    monkeypatch.setenv("PROBE_EPHEMERAL", "1")
    mp_client._auto_drain = True  # a worker would carry it -- but the disk goes with the pod
    assert "disposable" in multipart.settle_reason(mp_client) or "PROBE_EPHEMERAL" in multipart.settle_reason(mp_client)
    run = open_run(mp_client, experiment="e", name="r")
    big = _sparse(tmp_path / "ckpt.pt", 70 * MiB)
    run.log_artifact("ckpt", path=str(big))
    staged = _multipart_ops(mp_client.journal)[0]["multipart"]["staged_path"]

    def never(*_a, **_k):
        raise errors.TransportError("the link is down")

    monkeypatch.setattr(mp_client.transport, "put_part", never)
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        run.finish(flush_timeout=3)
    assert any("did not finish uploading before the run closed" in str(w.message) for w in caught)
    [row] = [r for r in _rows(mp_app, run.id, "ckpt.pt") if r["is_reference"]]
    assert "the run closed before this upload finished" in row["meta"]["upload_error"]
    assert _multipart_ops(mp_client.journal) == []
    assert not os.path.exists(staged)


def test_no_room_to_stage_records_a_reference_and_warns(mp_app, mp_client, tmp_path, monkeypatch):
    run = open_run(mp_client, experiment="e", name="r")
    big = _sparse(tmp_path / "ckpt.pt")

    def other_filesystem(src, dst):
        raise OSError(errno.EXDEV, "Invalid cross-device link")

    monkeypatch.setattr(multipart.os, "link", other_filesystem)
    # Review P2: 300 MiB free is more than twice 200 MiB, but a copy would
    # leave 100 MiB -- under the outbox's own floor (#2054), which the copy
    # must respect like every other staging.
    monkeypatch.setattr(multipart, "_free_bytes", lambda _directory: 300 * MiB)
    monkeypatch.setattr(mp_client.journal, "_free_floor", lambda: 128 * MiB)
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        run.log_artifact("ckpt", path=str(big))
    mp_client.flush()
    [row] = _rows(mp_app, run.id, "ckpt.pt")
    assert row["is_reference"] is True
    assert "128 MiB floor" in row["meta"]["upload_error"]
    assert any("ckpt" in str(w.message) for w in caught)
    assert mp_app.multipart == {}


def test_a_copy_is_staged_when_the_outbox_is_on_another_filesystem(mp_app, mp_client, tmp_path, monkeypatch):
    run = open_run(mp_client, experiment="e", name="r")
    big = _sparse(tmp_path / "ckpt.pt", 70 * MiB, head=b"copied")

    def other_filesystem(src, dst):
        raise OSError(errno.EXDEV, "Invalid cross-device link")

    monkeypatch.setattr(multipart.os, "link", other_filesystem)
    run.log_artifact("ckpt", path=str(big))
    [op] = _multipart_ops(mp_client.journal)
    assert op["multipart"]["stage_mode"] in ("copy", "reflink")
    assert os.stat(op["multipart"]["staged_path"]).st_ino != os.stat(big).st_ino
    _drain_until_done(mp_client)
    assert _rows(mp_app, run.id, "ckpt.pt")[0]["content_hash"] == _sha(big)


def test_a_verifier_mismatch_records_a_reference_and_deletes_the_staged_copy(
    mp_app, mp_client, tmp_path, monkeypatch
):
    run = open_run(mp_client, experiment="e", name="r")
    big = _sparse(tmp_path / "ckpt.pt", 70 * MiB)
    run.log_artifact("ckpt", path=str(big))
    [op] = _multipart_ops(mp_client.journal)
    staged = op["multipart"]["staged_path"]

    def mismatch(up):
        up["state"], up["failure_reason"] = "failed", "sha256_mismatch"

    monkeypatch.setattr(mp_app, "_multipart_settle", mismatch)
    with warnings.catch_warnings(record=True):
        warnings.simplefilter("always")
        _drain_until_done(mp_client)
    references = [r for r in _rows(mp_app, run.id, "ckpt.pt") if r["is_reference"]]
    assert len(references) == 1 and "sha256_mismatch" in references[0]["meta"]["upload_error"]
    assert not os.path.exists(staged)


def test_an_upload_older_than_seven_days_gives_up(mp_app, mp_client, tmp_path):
    run = open_run(mp_client, experiment="e", name="r")
    big = _sparse(tmp_path / "ckpt.pt", 70 * MiB)
    run.log_artifact("ckpt", path=str(big))
    [(path, op)] = multipart.pending(mp_client.journal)
    op["multipart"]["staged_at"] -= 8 * 86_400
    path.write_text(json.dumps(op))
    with warnings.catch_warnings(record=True):
        warnings.simplefilter("always")
        mp_client.flush()
    assert _multipart_ops(mp_client.journal) == []
    assert not os.path.exists(op["multipart"]["staged_path"])
    [row] = _rows(mp_app, run.id, "ckpt.pt")
    assert row["is_reference"] is True and "7 days" in row["meta"]["upload_error"]


def test_the_kind_is_registered_and_its_lane_is_its_own():
    assert multipart.KIND in journal_module.OP_KINDS
    op = {"run_ref": "r1", "lane": "multipart:abc", "kind": multipart.KIND}
    assert journal_module._lane_of(op) == "multipart:abc"
    assert journal_module._lane_of({"run_ref": "r1"}) == "r1"


def test_strict_uploads_synchronously_and_returns_the_verifying_upload(mp_app, mp_client, tmp_path):
    mp_app.multipart_verify_polls = 3  # the server's verifier is still hashing
    run = open_run(mp_client, experiment="e", name="r")
    big = _sparse(tmp_path / "ckpt.pt", 70 * MiB, head=b"strict")
    result = run.log_artifact("ckpt", path=str(big), strict=True)
    assert result["state"] == "verifying"
    assert _multipart_ops(mp_client.journal) == []
    staged = multipart.staged_dir(mp_client.journal)
    assert not staged.exists() or os.listdir(staged) == [], "the server has the bytes"
    assert os.path.exists(big)


def test_the_opaque_block_policy_keeps_the_reference_row(mp_app, mp_client, tmp_path, monkeypatch):
    """`PROBE_ARTIFACT_OPAQUE_POLICY=block` asks that nothing uninspectable
    leaves the machine; a multipart upload is stored before anything scans it."""
    monkeypatch.setenv("PROBE_ARTIFACT_OPAQUE_POLICY", "block")
    run = open_run(mp_client, experiment="e", name="r")
    big = _sparse(tmp_path / "ckpt.pt", 70 * MiB)
    with warnings.catch_warnings(record=True):
        warnings.simplefilter("always")
        run.log_artifact("ckpt", path=str(big))
    mp_client.flush()
    [row] = _rows(mp_app, run.id, "ckpt.pt")
    assert row["is_reference"] is True
    assert mp_app.multipart == {} and _multipart_ops(mp_client.journal) == []


def test_a_part_that_fails_at_the_store_is_transient_not_an_auth_block(mp_app, mp_client, tmp_path):
    """An expired or refused PART URL answers 403 from object storage (#2075's
    `UploadRefused`, never the login): the next slice asks for fresh URLs."""
    run = open_run(mp_client, experiment="e", name="r")
    big = _sparse(tmp_path / "ckpt.pt", 70 * MiB)
    run.log_artifact("ckpt", path=str(big))
    mp_app.multipart_refuse_part_puts = 2  # this slice's two part PUTs
    _flush_until(mp_client, lambda: mp_app.multipart_refuse_part_puts == 0)
    status = json.loads((mp_client.journal.dir / "status.json").read_text())
    assert not status.get("auth_blocked_since"), "a store refusal is not the credential"
    assert _multipart_ops(mp_client.journal), "kept for a retry with fresh URLs"
    _drain_until_done(mp_client)
    assert _rows(mp_app, run.id, "ckpt.pt")[0]["status"] == "complete"


def test_a_store_that_keeps_refusing_the_part_urls_gives_up_with_a_reference_row(
    mp_app, mp_client, tmp_path
):
    """...but a store that refuses every signed URL (a server pointed at the
    wrong store) is not retried for the 7 days of staging: after
    `_MAX_REFUSED_SLICES` refused slices the upload is permanent, recorded as
    a reference row, its server upload aborted and its staged copy deleted."""
    mp_app.multipart_refuse_part_puts = -1
    run = open_run(mp_client, experiment="e", name="r")
    big = _sparse(tmp_path / "ckpt.pt", 70 * MiB)
    run.log_artifact("ckpt", path=str(big))
    staged = _multipart_ops(mp_client.journal)[0]["multipart"]["staged_path"]
    with warnings.catch_warnings(record=True):
        warnings.simplefilter("always")
        _drain_until_done(mp_client)
    [row] = [r for r in _rows(mp_app, run.id, "ckpt.pt") if r["is_reference"]]
    assert "refused (403)" in row["meta"]["upload_error"]
    [upload] = mp_app.multipart.values()
    assert upload["state"] == "aborted"
    assert not os.path.exists(staged)

def test_staged_bytes_are_bounded_by_free_space_counting_every_upload_still_waiting(
    mp_app, mp_client, tmp_path, monkeypatch
):
    """Review P2: keep-last-k checkpoints, each logged. A hardlink costs no
    space until the trainer deletes its own copy, then pins those bytes; so
    staging counts every waiting upload's staged file against the free space
    left above the floor, and past it records a reference row instead."""
    monkeypatch.setattr(multipart, "_free_bytes", lambda _directory: 120 * MiB)
    monkeypatch.setattr(mp_client.journal, "_free_floor", lambda: 0)
    run = open_run(mp_client, experiment="e", name="r")
    first = _sparse(tmp_path / "ckpt-1.pt", 70 * MiB, head=b"one")
    second = _sparse(tmp_path / "ckpt-2.pt", 70 * MiB, head=b"two")
    run.log_artifact("ckpt-1", path=str(first))
    with warnings.catch_warnings(record=True):
        warnings.simplefilter("always")
        run.log_artifact("ckpt-2", path=str(second))
    assert len(_multipart_ops(mp_client.journal)) == 1
    mp_client.flush()
    [row] = [r for r in _rows(mp_app, run.id, "ckpt-2.pt") if r["is_reference"]]
    assert "70 MiB of 1 upload(s) still waiting" in row["meta"]["upload_error"]


def test_one_upload_at_a_time_the_oldest_first(mp_app, mp_client, tmp_path, monkeypatch):
    """Review P2: round-robin slices meant none finished early and every
    staged copy stayed pinned. Now the oldest upload sends until the server
    has it all; only then does the next start."""
    mp_app.multipart_verify_polls = 2
    # A slow link: each visit gets one part out before its slice runs out.
    monkeypatch.setattr(multipart, "SLICE_SECONDS", 0.05)
    real = multipart._send_parts

    def one_part(client, upload, state, numbers, deadline, save):
        real(client, upload, state, numbers[:1], deadline, save)
        time.sleep(max(0.0, deadline - time.monotonic()))

    monkeypatch.setattr(multipart, "_send_parts", one_part)
    run = open_run(mp_client, experiment="e", name="r")
    a = _sparse(tmp_path / "a.pt", 130 * MiB, head=b"a")
    b = _sparse(tmp_path / "b.pt", 130 * MiB, head=b"b")
    run.log_artifact("a", path=str(a))
    run.log_artifact("b", path=str(b))
    _drain_until_done(mp_client, passes=40)
    uploads = {u["name"]: u["upload_id"] for u in mp_app.multipart.values()}
    order = [uid for uid, _ in mp_app.multipart_part_puts]
    a_parts = [i for i, uid in enumerate(order) if uid == uploads["a.pt"]]
    b_parts = [i for i, uid in enumerate(order) if uid == uploads["b.pt"]]
    assert max(a_parts) < min(b_parts), order


@pytest.mark.parametrize("reason", ["idle", "superseded_idle"])
def test_an_upload_the_server_gave_up_on_while_away_starts_again(
    mp_app, mp_client, tmp_path, monkeypatch, reason
):
    """Review P3: offline past the server's 24 h idle abort -- or quiet past
    its 10 min takeover, while another run's create of the same bytes took
    the upload over (`superseded_idle`) -- the staged bytes are still here and
    still right: a new upload, not a reference row."""
    run = open_run(mp_client, experiment="e", name="r")
    big = _sparse(tmp_path / "ckpt.pt", 70 * MiB, head=b"away")
    run.log_artifact("ckpt", path=str(big))
    real_put = mp_client.transport.put_part

    def offline(*_a, **_k):
        raise errors.TransportError("network unreachable")

    monkeypatch.setattr(mp_client.transport, "put_part", offline)
    _flush_until(mp_client, lambda: bool(mp_app.multipart))
    [first] = mp_app.multipart.values()
    first["state"], first["failure_reason"] = "aborted", reason  # the server ended it
    monkeypatch.setattr(mp_client.transport, "put_part", real_put)
    _drain_until_done(mp_client)
    states = sorted(u["state"] for u in mp_app.multipart.values())
    assert states == ["aborted", "verified"], states
    assert [r for r in _rows(mp_app, run.id, "ckpt.pt") if r["status"] == "complete"]


def test_partial_copies_and_orphans_are_collected_at_the_start_of_a_pass(mp_app, mp_client, tmp_path, monkeypatch):
    """Review P3: a kill mid-copy left `.<op>.tmp` forever (gc only ran after
    a pass that touched a multipart op). A live op's copy is never touched."""
    run = open_run(mp_client, experiment="e", name="r")
    big = _sparse(tmp_path / "ckpt.pt", 70 * MiB)
    run.log_artifact("ckpt", path=str(big))
    staged = multipart.staged_dir(mp_client.journal)
    (staged / ".deadbeef.tmp").write_bytes(b"half a copy")
    (staged / "cafef00d.src").write_bytes(b"an orphan")
    monkeypatch.setattr(multipart, "_ORPHAN_GRACE_SECONDS", -1)
    journal_module.drain(mp_client.journal, only_ops=set(), client_factory=mp_client._outbox_client_factory())
    names = os.listdir(staged)
    assert ".deadbeef.tmp" not in names and "cafef00d.src" not in names
    assert [n for n in names if n.endswith(".src")], "the live op's staged copy stays"


def test_the_hash_runs_in_the_background_and_does_not_hold_the_pass(mp_app, mp_client, tmp_path, monkeypatch):
    """Review P3: hashing 10 GB (~30 s) inside the drain pass held every other
    lane. The pass returns at once; a later one picks the digest up."""
    import threading

    gate = threading.Event()
    real = multipart.fingerprint

    def slow(path):
        assert gate.wait(10)
        return real(path)

    monkeypatch.setattr(multipart, "fingerprint", slow)
    run = open_run(mp_client, experiment="e", name="r")
    big = _sparse(tmp_path / "ckpt.pt", 70 * MiB)
    run.log_artifact("ckpt", path=str(big))
    run.log({"train/loss": 0.25}, step=3)
    started = time.monotonic()
    mp_client.flush()
    assert time.monotonic() - started < 3.0, "the pass did not wait for the hash"
    assert mp_app.multipart == {} and _multipart_ops(mp_client.journal)
    assert mp_app.metrics_inserted >= 1, "the metric went meanwhile"
    gate.set()
    _drain_until_done(mp_client)
    assert _rows(mp_app, run.id, "ckpt.pt")[0]["status"] == "complete"


def test_a_worker_counts_a_slice_of_parts_as_progress(tmp_path, monkeypatch):
    """Review P2: after each 20 s slice the worker slept to the soonest OTHER
    lane's backoff (64 parts: 311 s instead of 75 s). A slice is progress:
    straight into the next pass."""
    from probe.sdk.journal import DrainReport, Journal, LaneStall

    journal = Journal(tmp_path / "outbox")
    journal._ensure()
    reports = iter(
        [
            DrainReport(in_progress=1, remaining=2, stalled_runs={"other-run": LaneStall("503", 120.0)}),
            DrainReport(remaining=0),
        ]
    )
    monkeypatch.setattr(journal_module, "drain", lambda *_a, **_k: next(reports))
    long_sleeps = []
    monkeypatch.setattr(
        outbox_worker, "_sleep_until_new_work", lambda *a, **k: long_sleeps.append(a[-1])
    )
    monkeypatch.setattr(outbox_worker.time, "sleep", lambda _s: None)
    assert outbox_worker._run_leased(journal) == 0
    assert long_sleeps == [], "slept to another lane's backoff after a slice"


def test_todays_prod_keeps_the_single_put_path(app, tmp_path):
    """#2071 shipped the multipart doors OFF: prod answers 501 and does not
    declare `artifact_multipart`. Against it -- or when the features probe
    fails -- the SDK must not stage, queue or ask for a multipart upload:
    a file at or under 64 MiB goes through the single-PUT door as today, and
    one over it keeps 0.7's warning and reference row."""
    assert app.supports_artifact_multipart is False  # today's prod
    client = make_client(app, tmp_spool=tmp_path / "outbox", async_writes=True)
    run = open_run(client, experiment="e", name="r")
    small = tmp_path / "metrics.bin"
    small.write_bytes(bytes(range(256)) * 4096)  # 1 MiB
    big = _sparse(tmp_path / "ckpt.pt", 70 * MiB)
    with warnings.catch_warnings(record=True):
        warnings.simplefilter("always")
        run.log_artifact("metrics", path=str(small))
        run.log_artifact("ckpt", path=str(big))
        # A features probe that fails is not an advertisement either.
        client._server_features_cache = None
        app.fail_paths = {"/v1/server/features"}
        run.log_artifact("ckpt-2", path=str(_sparse(tmp_path / "ckpt-2.pt", 70 * MiB)))
        app.fail_paths = set()
    client.flush()
    paths = [r.url.path for r in app.requests]
    assert not [p for p in paths if "/artifacts/multipart" in p], "no multipart request at all"
    assert not multipart.ops_dir(client.journal).exists() or not os.listdir(multipart.ops_dir(client.journal))
    assert not multipart.staged_dir(client.journal).exists(), "nothing staged"
    [small_row] = _rows(app, run.id, "metrics.bin")
    assert small_row["is_reference"] is False and app.puts, "the single-PUT door took it"
    for name in ("ckpt.pt", "ckpt-2.pt"):
        [row] = _rows(app, run.id, name)
        assert row["is_reference"] is True and row["meta"]["upload"] == "failed"
        assert "exceeds inspection size limit" in row["meta"]["upload_error"]


def test_a_multipart_server_still_takes_small_files_through_the_single_put(mp_app, mp_client, tmp_path):
    """Only a file over 64 MiB uses the multipart door, even on a server that
    advertises it: the relay inspects everything at or under it whole."""
    run = open_run(mp_client, experiment="e", name="r")
    small = tmp_path / "config.bin"
    small.write_bytes(b"x" * (64 * MiB))
    run.log_artifact("config", path=str(small))
    mp_client.flush()
    assert mp_app.multipart == {} and mp_app.puts
    assert _rows(mp_app, run.id, "config.bin")[0]["is_reference"] is False


def test_a_worker_waiting_on_the_verifier_says_so(tmp_path, monkeypatch, capsys):
    """Review nit: the backoff line printed `?` for a lane waiting on the
    server's verifier (a wait records a stall, not an error)."""
    from probe.sdk.journal import DrainReport, Journal, LaneStall

    journal = Journal(tmp_path / "outbox")
    journal._ensure()
    reports = iter(
        [
            DrainReport(remaining=1, stalled_runs={"multipart:x": LaneStall("the server is verifying the upload", 5.0)}),
            DrainReport(remaining=0),
        ]
    )
    monkeypatch.setattr(journal_module, "drain", lambda *_a, **_k: next(reports))
    monkeypatch.setattr(outbox_worker, "_sleep_until_new_work", lambda *a, **k: None)
    monkeypatch.setattr(outbox_worker.time, "sleep", lambda _s: None)
    assert outbox_worker._run_leased(journal) == 0
    out = capsys.readouterr().out
    assert "the server is verifying the upload" in out and ": ?" not in out


def test_a_busy_upload_tries_again_within_a_minute_however_long_it_waits(
    mp_app, mp_client, tmp_path
):
    """Another run's upload holds the same bytes (409). The server hands them
    to the next create once that upload has been idle 10 min (its uploader is
    gone), so the lane must not back off to its 300 s ceiling meanwhile: it
    tries again at least every `BUSY_MAX_WAIT_SECONDS`."""
    from probe.sdk.journal import LaneBackoff

    run = open_run(mp_client, experiment="e", name="r")
    big = _sparse(tmp_path / "ckpt.pt", 70 * MiB, head=b"busy")
    mp_app.multipart["held"] = {
        "upload_id": "held",
        "run_id": "another-run",
        "name": "ckpt",
        "content_hash": _sha(big),
        "state": "uploading",
    }
    run.log_artifact("ckpt", path=str(big))
    factory = mp_client._outbox_client_factory()
    deadline = time.monotonic() + 30
    busy = {}
    while not busy and time.monotonic() < deadline:
        report = journal_module.drain(mp_client.journal, client_factory=factory)
        busy = {k: v for k, v in report.stalled_runs.items() if "in progress" in v.error}
        time.sleep(0.05)
    [(lane, stall)] = busy.items()
    assert (stall.retry_after, stall.wake_by) == (multipart.BUSY_RETRY_SECONDS, 60.0)

    lanes = LaneBackoff(ceiling=outbox_worker._BACKOFF_CAP_SECONDS)
    waits = []
    for i in range(12):  # ~an hour of 409s at the uncapped backoff
        report = journal_module.DrainReport(stalled_runs={lane: stall})
        lanes.record(report, now=float(i))
        waits.append(round(lanes.next_wake(now=float(i)), 3))
    assert waits[:4] == [30.0] * 4, waits
    assert max(waits) == 60.0, waits
    assert [op for op in _multipart_ops(mp_client.journal)], "still queued, never dead-lettered"


def test_a_synchronous_upload_waits_past_the_servers_idle_takeover(
    mp_app, mp_client, tmp_path, monkeypatch
):
    """`strict=True` blocks on another upload of the same bytes. The server
    hands the bytes over once that upload has been idle 10 min, so the wait
    outlasts that before it gives up with the 409."""
    run = open_run(mp_client, experiment="e", name="r")
    big = _sparse(tmp_path / "ckpt.pt", 70 * MiB, head=b"sync-busy")
    mp_app.multipart["held"] = {
        "upload_id": "held",
        "run_id": "another-run",
        "name": "ckpt",
        "content_hash": _sha(big),
        "state": "uploading",
    }
    slept = []
    monkeypatch.setattr(multipart.time, "sleep", slept.append)
    with pytest.raises(errors.ConflictError):
        run.log_artifact("ckpt", path=str(big), strict=True)
    assert sum(slept) > 600, slept
