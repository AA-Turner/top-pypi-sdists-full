"""The snapshot a run takes at open: no network on the caller's thread, everything local queued.

Pins: the open queues its launch PATCH, code-bytes archive and code-snapshot row before it
returns; the execution record's POST runs on its own thread with a hard deadline, retried, with
the pushed base in it; its answer queues the env_ref PATCH and the row again; a file edited
after open still uploads its open-time bytes; `finish()` delivers all of it before the
terminal status; a slow record still pins before the status; a failing or hung record is a gap
and one warning; a hung record can never queue anything behind the terminal status, in
`finish()`, a direct `set_status`, a SIGTERM close or an atexit close; an explicit `snapshot()`
after open wins; the archive is pending in `check_run` until it lands; `ls-remote` and the
verify fetch never accept a new host key.
"""

from __future__ import annotations

import gzip
import io
import json
import signal
import subprocess
import sys
import tarfile
import tempfile
import threading
import time

import pytest

from probe.sdk import errors
from probe.sdk.capture import code as _snapshot
from probe.sdk.run.files import snapshot_queue
from probe.sdk.run.files.snapshot_queue import PendingSnapshot
from tests.conftest import make_client, make_pushed_repo
from tests.served_fake_app import child_env, serve

RECORDS = "/v1/execution-records"


@pytest.fixture
def opened(app, tmp_path, monkeypatch):
    """An async, fail-open client and a pushed repo as the working folder."""
    repo = make_pushed_repo(tmp_path)
    monkeypatch.chdir(repo)
    monkeypatch.setenv("PROBE_AUTO_SNAPSHOT", "1")
    client = make_client(app, tmp_spool=tmp_path / "spool", async_writes=True)
    return client, repo


class HungRecord:
    """The record's POST hangs until `release`, ignoring its deadline: a request that
    outlives its own deadline (a hung DNS lookup does) must still queue nothing late."""

    def __init__(self, monkeypatch) -> None:
        self._monkeypatch = monkeypatch
        self._release = threading.Event()

    def hang(self, client) -> None:
        real = client.transport.request

        def request(method, path, *args, **kwargs):
            if path == RECORDS:
                self._release.wait(30)
            return real(method, path, *args, **kwargs)

        self._monkeypatch.setattr(client.transport, "request", request)

    def release(self) -> None:
        """Let the POST answer, and wait until its thread is done with the answer."""
        self._release.set()
        _join_record_threads()


@pytest.fixture
def hung_record(monkeypatch):
    """A hung record, with the record's deadlines cut to half a second."""
    monkeypatch.setattr(snapshot_queue, "EXECUTION_RECORD_TIMEOUT_SECONDS", 0.5)
    monkeypatch.setattr(snapshot_queue, "PUSHED_BASE_WAIT_SECONDS", 0.5)
    hung = HungRecord(monkeypatch)
    yield hung
    hung.release()


class HeldRecord:
    """The record's POST waits for `release()`, then `delay` seconds more: proves the open
    did not wait for it, with no wall-clock bound on the open."""

    def __init__(self, monkeypatch) -> None:
        self._monkeypatch = monkeypatch
        self._gate = threading.Event()
        self.delay = 1.0

    def hold(self, client) -> None:
        real = client.transport.request

        def request(method, path, *args, **kwargs):
            if path == RECORDS and threading.current_thread().name == "probe-execution-record":
                self._gate.wait(30)
                time.sleep(self.delay)
            return real(method, path, *args, **kwargs)

        self._monkeypatch.setattr(client.transport, "request", request)

    def release(self) -> None:
        self._gate.set()


@pytest.fixture
def held_record(monkeypatch):
    held = HeldRecord(monkeypatch)
    yield held
    held.release()
    _join_record_threads()


def _open(client):
    return client.run(project="proj-open", experiment="exp-open", question="does open block?")


def _join_record_threads() -> None:
    for thread in threading.enumerate():
        if thread.name == "probe-execution-record":
            thread.join(15)


def _is_status(request) -> bool:
    return request.method == "PATCH" and b'"status"' in request.content


def _snapshot_writes(app, run_id: str) -> list[tuple[int, str]]:
    """(index in app.requests, what) for every write the open's snapshot makes."""
    out = []
    for i, r in enumerate(app.requests):
        if r.method == "PATCH" and r.url.path == f"/v1/runs/{run_id}":
            body = json.loads(r.content or b"{}")
            if "launch" in (body.get("metadata") or {}):
                out.append((i, "launch"))
            elif "env_ref" in body and "status" not in body:
                out.append((i, "pin"))
        elif r.url.path == f"/v1/runs/{run_id}/artifacts" and b"code_snapshot" in r.content:
            out.append((i, "row"))
        elif r.url.path == f"/v1/runs/{run_id}/artifacts/uploads" and b"code-bytes" in r.content:
            out.append((i, "archive"))
    return out


def _describe(op: dict) -> str:
    path, body = op.get("path") or "", op.get("body") or {}
    if op.get("kind") == "upload":
        name = (op.get("upload") or {}).get("name") or ""
        return "archive" if name.startswith("code-bytes") else f"upload {name}"
    if body.get("status"):
        return "status"
    if op.get("method") == "PATCH" and "launch" in (body.get("metadata") or {}):
        return "launch"
    if op.get("method") == "PATCH" and "env_ref" in body:
        return "pin"
    if path.endswith("/artifacts") and body.get("kind") == "code_snapshot":
        return "row"
    if path.endswith("/release"):
        return "release"
    return f"{op.get('method')} {path.rsplit('/', 1)[-1]}"


def _queued(client) -> list[str]:
    return [_describe(op) for _, op in client.journal.pending()]


def _archive_members(app, run_id: str) -> dict[str, bytes]:
    row = next(a for a in app.artifacts[run_id] if a.get("kind") == "code_bytes")
    raw = app.blobs[row["id"]]
    with gzip.open(io.BytesIO(raw), "rb") as gz, tarfile.open(fileobj=gz, mode="r") as tar:
        return {m.name: tar.extractfile(m).read() for m in tar.getmembers() if m.isfile()}


def _gaps(client) -> list[dict]:
    return [g for p in client.journal.producer_report() for g in p.get("gaps") or []]


def _stored_snapshot_rows(app, run_id: str) -> list[dict]:
    """The code-snapshot rows the SERVER holds: it updates a reference re-logged at the same
    (run, name, uri) in place, meta replaced whole (app/files/artifacts/records/records.py).
    The fake keeps every POST (other suites count them), so the update is applied here."""
    stored: dict[tuple, dict] = {}
    for post in app.artifacts.get(run_id, []):
        if post.get("kind") == "code_snapshot":
            stored[(post["name"], post["uri"])] = post
    return list(stored.values())


def _snapshot_row(app, run_id: str) -> dict:
    (row,) = _stored_snapshot_rows(app, run_id)
    return row


# -- the open -------------------------------------------------------------------------


def test_the_open_queues_everything_local_before_it_returns(app, opened, hung_record, tmp_path, monkeypatch):
    """C4: a process killed right after `probe.init()` returns still has its launch block,
    code bytes and code-snapshot row on disk, and no temp archive behind; the record's POST
    is the only request, on its own thread."""
    client, _ = opened
    scratch = tmp_path / "tmp"
    scratch.mkdir()
    monkeypatch.setattr(tempfile, "tempdir", str(scratch))
    hung_record.hang(client)
    callers: list[str] = []
    real = client.transport.request

    def request(method, path, *args, **kwargs):
        if path == RECORDS or "/artifacts" in path:
            callers.append(f"{method} {path} on {threading.current_thread().name}")
        return real(method, path, *args, **kwargs)

    monkeypatch.setattr(client.transport, "request", request)
    run = _open(client)

    assert not run._pending_snapshot._record_done.is_set(), "the open waited for the record"
    assert _queued(client) == ["launch", "row", "archive"], _queued(client)
    archive = next(op for _, op in client.journal.pending() if op.get("kind") == "upload")
    assert archive["upload"]["staged"] and archive.get("blocking") is False
    assert list(scratch.glob("probe-code-*")) == [], "the temp archive outlived the open"
    hung_record.release()
    assert callers == [f"POST {RECORDS} on probe-execution-record"], callers
    run.finish("completed")


def test_finish_delivers_the_snapshot_before_the_terminal_status(app, opened):
    client, _ = opened
    run = _open(client)
    # The pushed base rides the record only when `ls-remote` answers before the close (plan T5).
    assert run._pending_snapshot._pushed_answered.wait(10)

    run.finish("completed", flush_timeout=30)
    client.flush()

    writes = _snapshot_writes(app, run.id)
    status_at = next(i for i, r in enumerate(app.requests) if _is_status(r))
    # The close's pass sends the run's own lane first, then the archive's (convergence review).
    assert [w for _, w in writes] == ["launch", "row", "pin", "row", "archive"], writes
    assert all(i < status_at for i, _ in writes), (writes, status_at)
    bundle = client.run_bundle(run.id)
    assert bundle["run"]["env_ref"] and bundle["run"]["status"] == "completed"
    posts = [a for a in bundle["artifacts"] if a.get("kind") == "code_snapshot"]
    assert len(posts) == 2 and posts[0]["uri"] == posts[1]["uri"], "the open's row, then its rewrite"
    meta = _snapshot_row(app, run.id)["meta"]
    assert meta["env_ref"] == bundle["run"]["env_ref"]
    assert meta["base_commit"] and meta["remote"], "the pushed base rides the row"
    assert meta["storage"] == "archive" and meta["n_pending_upload"] == 0
    assert "pending_code_bytes" not in client.check_run(run.id)["missing"]


def test_a_slow_record_still_pins_before_the_status(app, opened, held_record):
    """The record answers after the script already called finish(): the close waits for it
    (within its deadline), so the env_ref PATCH lands before the status."""
    client, _ = opened
    held_record.hold(client)
    run = _open(client)
    assert not run._pending_snapshot._record_done.is_set(), "the open waited for the record"
    held_record.release()

    # The suite's close default is 2 s; a script's is 600 s. The close waits for the record
    # within half of its own budget, so give it the room a real close has.
    run.finish("completed", flush_timeout=30)

    writes = _snapshot_writes(app, run.id)
    status_at = next(i for i, r in enumerate(app.requests) if _is_status(r))
    assert "pin" in [w for _, w in writes] and all(i < status_at for i, _ in writes), writes
    assert app.runs[run.id]["env_ref"] and app.runs[run.id]["status"] == "completed"
    assert not _gaps(client)


def test_the_record_carries_the_pushed_base_like_run_snapshot(app, opened, tmp_path):
    """I4: the open's record names the pushed base, so its env_ref is the one an in-hand
    `snapshot()` of the same tree pins."""
    client, repo = opened
    run = _open(client)
    assert run._pending_snapshot._pushed_answered.wait(10), "ls-remote answered before the close"
    run.finish("completed", flush_timeout=30)
    posted = json.loads(next(r for r in app.requests if r.url.path == RECORDS).content)
    base, remote = _snapshot.pushed_base(str(repo))
    assert base and posted["code"]["manifest"]["base_commit"] == base
    assert posted["code"]["manifest"]["remote"] == remote

    in_hand = make_client(app, tmp_spool=tmp_path / "spool-sync")  # sync: `snapshot()` at open
    other = in_hand.run(project="proj-open", experiment="exp-open", question="same tree?")
    assert app.runs[run.id]["env_ref"] == app.runs[other.id]["env_ref"]


def test_a_file_edited_after_open_uploads_its_open_time_bytes(app, opened):
    client, repo = opened
    run = _open(client)
    open_time = (repo / "train.py").read_bytes()

    (repo / "train.py").write_text("print('v3 EDITED AFTER OPEN')\n")
    run.finish("completed")
    client.flush()

    members = _archive_members(app, run.id)
    assert members["train.py"] == open_time
    assert b"AFTER OPEN" not in members["train.py"]


def test_an_archive_the_outbox_cannot_stage_is_a_gap_never_an_upload_from_here(app, opened, monkeypatch):
    """I6: below the outbox's free-space floor the archive is not stored (named as pending),
    never sent synchronously on the caller's thread."""
    client, _ = opened
    monkeypatch.setattr(
        client.journal, "append_upload",
        lambda **kw: {"op_id": None, "blob": None, "staged": False, "unstaged_reason": "low disk"},
    )
    sent: list[str] = []
    real = client.transport.request

    def request(method, path, *args, **kwargs):
        if "/artifacts/uploads" in path and threading.current_thread() is threading.main_thread():
            sent.append(path)
        return real(method, path, *args, **kwargs)

    monkeypatch.setattr(client.transport, "request", request)
    with pytest.warns(UserWarning, match="code-bytes archive not stored"):
        run = _open(client)
    assert sent == [], "an upload ran on the caller's thread"
    run.finish("completed", flush_timeout=30)
    meta = _snapshot_row(app, run.id)["meta"]
    assert meta["n_pending_upload"] > 0 and "queued" not in meta["code_bytes"]
    assert "pending_code_bytes" in client.check_run(run.id)["missing"]


def test_a_queued_archive_is_pending_in_check_run_until_it_lands(app, opened):
    """C3: the row says the archive was queued; until a `code_bytes` row exists the bytes
    are only in this machine's outbox, so the capture is not complete."""
    client, _ = opened
    run = _open(client)
    run.finish("completed", flush_timeout=30)
    client.flush()
    assert "pending_code_bytes" not in client.check_run(run.id)["missing"]

    app.artifacts[run.id] = [a for a in app.artifacts[run.id] if a.get("kind") != "code_bytes"]
    assert "pending_code_bytes" in client.check_run(run.id)["missing"]


def test_an_archive_build_failure_fails_open(app, opened, monkeypatch):
    """I5: a build error other than the size cap is a gap and a warning; the run opens and
    its launch PATCH and row are still queued."""
    client, _ = opened

    def broken(*args, **kwargs):
        raise _snapshot.SnapshotError("a file changed under the stream twice")

    monkeypatch.setattr(_snapshot, "build_pending_archive", broken)
    with pytest.warns(UserWarning, match="code-bytes archive not built"):
        run = _open(client)
    assert _queued(client)[:2] == ["launch", "row"]
    run.finish("completed", flush_timeout=30)
    meta = _snapshot_row(app, run.id)["meta"]
    assert meta["n_pending_upload"] > 0 and app.runs[run.id]["env_ref"]


def test_an_archive_build_os_error_fails_open(app, opened, monkeypatch):
    """A full temp disk while building the archive is a gap too, not an aborted snapshot."""
    client, _ = opened

    def full(*args, **kwargs):
        raise OSError(28, "No space left on device")

    monkeypatch.setattr(_snapshot, "build_pending_archive", full)
    with pytest.warns(UserWarning, match="code-bytes archive not built"):
        _open(client)
    assert _queued(client)[:2] == ["launch", "row"]


@pytest.mark.parametrize("answer", ["refused", "no_multipart_door", "not_yet_known", "staged"])
def test_an_archive_over_the_inspection_limit_goes_in_parts_only_on_a_verdict_in_hand(app, opened, monkeypatch, answer):
    """Over the inspection limit the archive goes in parts only when a features answer already in
    hand declares multipart uploads (the open asks the server nothing); a refusal, no such door,
    or no answer yet means the bytes are not stored, and the row says so (a queued
    `log_artifact` returns None either way, so its answer cannot tell)."""
    from probe.sdk.artifact.storage_handlers import multipart as _multipart
    from probe.sdk.run.run import Run

    client, _ = opened
    calls: list[str] = []

    def over_the_limit(**kwargs):
        raise ValueError("over the inspection limit")

    def multipart(self, name, path, *, refused, **kwargs):
        calls.append(name)
        return refused("Artifact upload refused: no room to stage") if answer == "refused" else None

    real_supports = type(client).supports_feature

    def supports_feature(self, feature):
        found = real_supports(self, feature)
        if answer == "not_yet_known":
            self._server_features_cache = None  # nothing answered before the archive
        elif answer in ("refused", "staged"):
            self._server_features_cache = frozenset({*(self._server_features_cache or ()), _multipart.FEATURE})
        return found

    monkeypatch.setattr(client.journal, "append_upload", over_the_limit)
    monkeypatch.setattr(_multipart, "over_threshold", lambda path: True)
    monkeypatch.setattr(Run, "_maybe_multipart", multipart)
    monkeypatch.setattr(type(client), "supports_feature", supports_feature)
    if answer == "staged":
        run = _open(client)
    else:
        with pytest.warns(UserWarning, match="code-bytes archive not stored"):
            run = _open(client)
    assert bool(calls) is (answer in ("refused", "staged")), calls
    run.finish("completed", flush_timeout=30)
    meta = _snapshot_row(app, run.id)["meta"]
    if answer == "staged":
        assert meta["code_bytes"].get("queued"), "staged in parts: the row says queued"
    else:
        assert meta["n_pending_upload"] > 0 and "queued" not in meta["code_bytes"]

def test_a_snapshot_nobody_closes_is_settled_at_exit(monkeypatch):
    """`client.run()` without `finish()` (a launcher that exits): the interpreter's exit
    settles the open's snapshot, so its writes and its gap are queued, not lost silently."""
    monkeypatch.setattr(snapshot_queue, "_AT_EXIT_WAIT_SECONDS", 0.2)
    client, writes = _Client(), []
    pending = _pending(client, writes, should_wait_for_pushed=False)
    pending.start()
    assert pending in snapshot_queue._STARTED and snapshot_queue._is_at_exit_registered
    with pytest.warns(UserWarning, match="no answer before the run closed"):
        snapshot_queue._settle_at_exit()
    client.go.set()
    _join_record_threads()
    assert pending.is_settled and writes == [("pin", None), ("row", None, None, None)]


def test_a_forked_child_never_settles_the_parents_snapshot(monkeypatch):
    client, writes = _Client(), []
    client.go.set()
    pending = _pending(client, writes, should_wait_for_pushed=False)
    monkeypatch.setattr(snapshot_queue.os, "getpid", lambda: -1)  # "the child"
    pending.settle(time.monotonic())
    assert not pending.is_settled and writes == []


def test_the_row_rewrite_carries_no_unit_the_closing_thread_has_open(app, opened, hung_record):
    """The close queues the row's rewrite (the record hung) inside a caller's `run.unit`:
    the row belongs to the run, so no unit's labels ride it."""
    client, _ = opened
    hung_record.hang(client)
    with pytest.warns(UserWarning, match="no answer before the run closed"):
        run = _open(client)
        with run.unit(labels={"sample": 3}):
            run.finish("completed", flush_timeout=30)
    rows = [
        json.loads(r.content) for r in app.requests
        if r.url.path == f"/v1/runs/{run.id}/artifacts" and b"code_snapshot" in r.content
    ]
    assert rows and not any(row.get("labels") or row.get("coords") for row in rows), rows


def test_the_record_threads_writes_never_go_around_the_queue(app, opened, held_record, monkeypatch):
    """Below the outbox's free-space floor a write may be sent directly; the open's record
    thread holds the gate's lock while it writes, so its writes are queue-only (a direct
    send can hang in DNS past any deadline and hold the close)."""
    client, _ = opened
    held_record.hold(client)
    run = _open(client)
    client.flush()  # the run's lane is empty: the one case a direct send is allowed
    monkeypatch.setattr(client.journal, "below_floor", lambda: "below the floor")
    sent: list[str] = []
    real = client.transport.request

    def request(method, path, *args, **kwargs):
        if threading.current_thread().name == "probe-execution-record" and path != RECORDS:
            sent.append(f"{method} {path}")
        return real(method, path, *args, **kwargs)

    monkeypatch.setattr(client.transport, "request", request)
    held_record.delay = 0.0
    held_record.release()
    run._wait_for_open_record()
    assert sent == [], sent


def test_check_run_judges_the_queued_archive_by_its_own_hash():
    """C3, precisely: only a landed upload of THIS archive (by hash, not a failed upload's
    reference row) clears it, and a row the backfill converted to per-file is not pending."""
    from probe.sdk.client.resources.runs.check import _is_archive_still_queued

    meta = {"code_bytes": {"queued": True, "archive_sha256": "a" * 64, "storage": "archive"}}
    landed = {"kind": "code_bytes", "content_hash": "a" * 64, "status": "complete"}
    assert not _is_archive_still_queued(meta, [landed])
    assert _is_archive_still_queued(meta, [{**landed, "content_hash": "b" * 64}]), "an older archive"
    assert _is_archive_still_queued(meta, [{**landed, "is_reference": True}]), "a failed upload"
    assert _is_archive_still_queued(meta, [{**landed, "status": "pending"}])
    converted = {"storage": "artifacts", "code_bytes": {**meta["code_bytes"], "storage": "artifacts"}}
    assert not _is_archive_still_queued(converted, [])


def test_an_archive_over_the_cap_still_raises(app, opened, monkeypatch):
    client, _ = opened

    def too_large(*args, **kwargs):
        raise _snapshot.SnapshotTooLarge("over the cap")

    monkeypatch.setattr(_snapshot, "build_pending_archive", too_large)
    with pytest.warns(UserWarning, match="auto-snapshot failed"):
        _open(client)


# -- the record ---------------------------------------------------------------------


def test_a_failed_record_is_a_gap_and_one_warning_never_an_exception(app, opened, monkeypatch):
    client, _ = opened
    real_post = client.transport.post

    def post(path, *args, **kwargs):
        if path == RECORDS:
            raise errors.ValidationError("refused", status=422)
        return real_post(path, *args, **kwargs)

    monkeypatch.setattr(client.transport, "post", post)
    with pytest.warns(UserWarning, match="execution record not recorded at run open") as caught:
        run = _open(client)
        run._wait_for_open_record()
        _join_record_threads()  # the warning follows the record's outcome, said off the lock
    assert sum("execution record" in str(w.message) for w in caught) == 1
    gaps = _gaps(client)
    assert any("execution record" in g.get("reason", "") for g in gaps), gaps
    run.finish("completed")
    client.flush()
    bundle = client.run_bundle(run.id)
    assert not bundle["run"].get("env_ref")
    snap = next(a for a in bundle["artifacts"] if a.get("kind") == "code_snapshot")
    assert snap["uri"].startswith("probe-tree:")
    assert any(a.get("kind") == "code_bytes" for a in bundle["artifacts"]), "bytes still land"


class _Transport:
    def __init__(self, *answers) -> None:
        self.answers = list(answers)
        self.calls: list[tuple[str, float | None]] = []

    def post(self, path, body):
        from probe.sdk.delivery.transport.deadlines import _request_deadline

        self.calls.append((threading.current_thread().name, _request_deadline.get()))
        answer = self.answers.pop(0)
        if isinstance(answer, Exception):
            raise answer
        return answer


def test_the_record_post_retries_what_a_retry_can_fix(monkeypatch):
    """I12: a 503 or a lost connection is retried within the deadline; a 422 is not."""
    monkeypatch.setattr(snapshot_queue.time, "sleep", lambda seconds: None)
    transport = _Transport(
        errors.ServerError("busy", status=503), errors.TransportError("reset"), {"content_hash": "h"}
    )
    client = type("C", (), {"transport": transport})()
    assert snapshot_queue.post_execution_record(client, {}, deadline=time.monotonic() + 5) == "h"
    assert len(transport.calls) == 3

    refused = _Transport(errors.ValidationError("bad", status=422), {"content_hash": "h"})
    client = type("C", (), {"transport": refused})()
    with pytest.raises(errors.ValidationError):
        snapshot_queue.post_execution_record(client, {}, deadline=time.monotonic() + 5)
    assert len(refused.calls) == 1


def test_the_record_post_never_pauses_past_its_deadline(monkeypatch):
    """The retry loop gives up rather than sleep past the record's deadline, a server's
    `Retry-After` included: the close's gate assumes the thread ends by then."""
    slept: list = []
    monkeypatch.setattr(snapshot_queue.time, "sleep", slept.append)
    busy = _Transport(errors.ServerError("busy", status=503), {"content_hash": "h"})
    client = type("C", (), {"transport": busy})()
    with pytest.raises(errors.ServerError):
        snapshot_queue.post_execution_record(client, {}, deadline=time.monotonic() + 0.1)
    assert len(busy.calls) == 1 and slept == []

    later = errors.ServerError("slow down", status=429)
    later.retry_after = 30.0
    throttled = _Transport(later, {"content_hash": "h"})
    client = type("C", (), {"transport": throttled})()
    with pytest.raises(errors.ServerError):
        snapshot_queue.post_execution_record(client, {}, deadline=time.monotonic() + 5)
    assert len(throttled.calls) == 1 and slept == [], "a Retry-After past the deadline is not waited"

def test_the_record_deadline_is_set_on_the_thread_that_posts():
    transport = _Transport({"content_hash": "h"})
    pins: list = []
    client = type("C", (), {"transport": transport})()
    pending = PendingSnapshot(
        client, {}, pin=pins.append, rewrite_row=lambda *a: None, should_wait_for_pushed=False
    )
    started = time.monotonic()
    pending.start()
    pending.wait_for_record()

    (name, deadline), = transport.calls
    assert name == "probe-execution-record" and deadline is not None
    assert deadline - started == pytest.approx(snapshot_queue.EXECUTION_RECORD_TIMEOUT_SECONDS, abs=0.5)
    assert pins == ["h"]


class _Client:
    """A client whose record POST answers when the test says so."""

    def __init__(self, answer: str | None = "h") -> None:
        self.go = threading.Event()
        self.gaps: list[str] = []
        self.bodies: list[dict] = []
        self._answer = answer
        outer = self

        class Transport:
            def post(self, path, body):
                outer.bodies.append(body)
                outer.go.wait(10)
                return {"content_hash": outer._answer}

        class Journal:
            def note_capture_gap(self, reason):
                outer.gaps.append(reason)

        self.transport, self.journal = Transport(), Journal()


def _pending(client, writes: list, *, should_wait_for_pushed: bool = True, body=None) -> PendingSnapshot:
    return PendingSnapshot(
        client,
        body if body is not None else {},
        pin=lambda h: writes.append(("pin", h)),
        rewrite_row=lambda h, base, remote: writes.append(("row", h, base, remote)),
        should_wait_for_pushed=should_wait_for_pushed,
    )


def test_with_no_thread_to_be_had_the_record_posts_inline(monkeypatch):
    def refuse(self):
        raise RuntimeError("can't start new thread")

    client, writes = _Client(), []
    client.go.set()
    pending = _pending(client, writes, should_wait_for_pushed=False)
    monkeypatch.setattr(threading.Thread, "start", refuse)
    pending.start()
    assert writes == [("pin", "h"), ("row", "h", None, None)]
    pending.settle()
    assert len(writes) == 2


def test_the_pushed_base_rides_the_record_then_the_pin_then_the_row():
    client, writes = _Client(), []
    pending = _pending(client, writes, body={"code": {"manifest": {"base_commit": None}}})
    pending.start()
    pending.answer_pushed("abc123", "origin-url")
    client.go.set()
    pending.wait_for_record()
    _join_record_threads()

    assert client.bodies[0]["code"]["manifest"] == {"base_commit": "abc123", "remote": "origin-url"}
    assert writes == [("pin", "h"), ("row", "h", "abc123", "origin-url")]
    pending.settle()
    assert len(writes) == 2, "settling twice writes nothing again"


def test_the_close_first_queues_once_and_drops_both_late_answers():
    client, writes = _Client(), []
    pending = _pending(client, writes, should_wait_for_pushed=False)
    pending.start()

    with pytest.warns(UserWarning, match="no answer before the run closed"):
        pending.settle(time.monotonic())  # the close, with no time to wait
    client.go.set()
    _join_record_threads()
    pending.answer_pushed("abc123", "origin-url")

    assert writes == [("pin", None), ("row", None, None, None)]
    assert client.gaps == ["execution record not recorded at run open: no answer before the run closed"]


def test_an_interrupt_during_the_wait_still_shuts_the_gate(monkeypatch):
    client, writes = _Client(), []
    pending = _pending(client, writes, should_wait_for_pushed=False)
    pending.start()

    def interrupted(timeout=None):
        raise KeyboardInterrupt

    monkeypatch.setattr(pending._record_done, "wait", interrupted)
    with pytest.warns(UserWarning, match="no answer before the run closed"):
        with pytest.raises(KeyboardInterrupt):
            pending.settle()
    client.go.set()
    _join_record_threads()

    assert pending.is_settled and writes == [("pin", None), ("row", None, None, None)]


def test_a_write_an_interrupt_cut_short_is_finished_by_the_next_settle():
    """A second Ctrl-C inside the gate's own queueing: the next settle (the close's
    interrupt path queues the status through one) still writes the pin and the row."""
    client, writes = _Client(), []
    interrupts = [KeyboardInterrupt()]

    def pin(h):
        if interrupts:
            raise interrupts.pop()
        writes.append(("pin", h))

    pending = PendingSnapshot(
        client, {}, pin=pin, rewrite_row=lambda h, b, r: writes.append(("row", h, b, r)),
        should_wait_for_pushed=False,
    )
    pending.start()
    with pytest.warns(UserWarning, match="no answer before the run closed"):
        with pytest.raises(KeyboardInterrupt):
            pending.settle(time.monotonic())
    pending.settle(time.monotonic())
    client.go.set()
    _join_record_threads()

    assert writes == [("pin", None), ("row", None, None, None)]


def test_a_warning_stuck_on_stderr_never_holds_the_close(monkeypatch):
    """The record thread's warnings go out after it releases the gate's lock: a stderr
    another thread holds forever (a SIGTERM close) cannot keep the close from shutting it."""
    stuck = threading.Event()
    released = threading.Event()

    def warn(message, **kwargs):
        if threading.current_thread().name == "probe-execution-record":
            stuck.set()
            released.wait(10)

    monkeypatch.setattr(snapshot_queue._diagnostics, "warn", warn)
    client, writes = _Client(), []

    def refused(path, body):
        raise errors.ValidationError("bad", status=422)

    client.transport.post = refused
    pending = _pending(client, writes, should_wait_for_pushed=False)
    pending.start()
    assert stuck.wait(5), "the record thread never warned"
    try:
        started = time.monotonic()
        pending.settle(time.monotonic())
        assert time.monotonic() - started < 0.5
        assert writes == [("pin", None), ("row", None, None, None)]
    finally:
        released.set()
        _join_record_threads()


# -- nothing after the status ---------------------------------------------------------


def test_a_hung_record_never_queues_behind_the_status(app, opened, hung_record, monkeypatch):
    """The O3 trap: the close stops waiting for the record, queues what it holds, and
    closes; the record answering later queues NOTHING, so the status stays last."""
    client, _ = opened
    hung_record.hang(client)
    with pytest.warns(UserWarning, match="execution record not recorded at run open") as caught:
        run = _open(client)
        real = client.transport.request

        def down(method, path, *args, **kwargs):
            # Nothing of the run reaches the server now: its writes stay queued, in order.
            if method != "GET" and path.startswith("/v1/runs/"):
                raise errors.TransportError("net down")
            return real(method, path, *args, **kwargs)

        monkeypatch.setattr(client.transport, "request", down)
        run.log({"loss": 1.0}, step=1)
        started = time.monotonic()
        report = run.finish("completed", flush_timeout=2.0)
    took = time.monotonic() - started

    assert report["finish_queued"] is True, report
    assert took < 4.0, f"finish() was held by the hung record: {took:.2f}s"
    kinds = _queued(client)
    status_at = kinds.index("status")
    assert kinds[:3] == ["launch", "row", "archive"], kinds
    assert "pin" not in kinds and set(kinds[status_at + 1:]) <= {"release"}, kinds

    hung_record.release()
    assert _queued(client) == kinds, "queued after the status"
    assert sum("execution record" in str(w.message) for w in caught) == 1
    assert sum("execution record" in g.get("reason", "") for g in _gaps(client)) == 1


def test_a_hung_record_delivered_close_sends_nothing_after_the_status(app, opened, hung_record):
    client, _ = opened
    hung_record.hang(client)
    with pytest.warns(UserWarning, match="no answer before the run closed"):
        run = _open(client)
        started = time.monotonic()
        run.finish("completed")
    took = time.monotonic() - started
    status_at = next(i for i, r in enumerate(app.requests) if _is_status(r))

    hung_record.release()
    client.flush()

    assert took < 3.0, f"finish() waited past the record's deadline: {took:.2f}s"
    writes = _snapshot_writes(app, run.id)
    assert {"launch", "archive", "row"} <= {w for _, w in writes}, writes
    assert all(i < status_at for i, _ in writes), (writes, status_at)
    late = [
        f"{r.method} {r.url.path}"
        for r in app.requests[status_at + 1:]
        if r.method != "GET" and run.id in r.url.path and "/release" not in r.url.path
    ]
    assert late == [], late
    assert not app.runs[run.id].get("env_ref"), "the late record must not be pinned"
    assert app.runs[run.id]["status"] == "completed"
    assert client.journal.pending() == []


def test_a_short_close_does_not_wait_out_the_records_deadline(app, opened, monkeypatch):
    """The close waits for the record at most half of its own local budget: a 4 s close
    with the default 7.5 s record deadline waits ~1.5 s, never its whole budget."""
    client, _ = opened
    hung = HungRecord(monkeypatch)
    hung.hang(client)
    try:
        with pytest.warns(UserWarning, match="no answer before the run closed"):
            run = _open(client)
            started = time.monotonic()
            run.finish("completed", flush_timeout=4.0)
        assert time.monotonic() - started < 3.0
    finally:
        hung.release()


def test_a_direct_terminal_set_status_queues_the_snapshot_first(app, opened, held_record):
    client, _ = opened
    held_record.hold(client)
    held_record.delay = 0.3
    run = _open(client)
    held_record.release()

    run.set_status("completed")  # queued: async writes

    kinds = _queued(client)
    assert "pin" in kinds and kinds.index("pin") < kinds.index("status"), kinds
    assert kinds.index("status") > max(i for i, k in enumerate(kinds) if k == "row"), kinds


def test_a_rank_that_sends_no_status_does_not_wait_for_the_record(app, opened, hung_record):
    client, _ = opened
    hung_record.hang(client)
    run = _open(client)
    run._sends_terminal_status = False
    started = time.monotonic()
    run.set_status("completed")
    assert time.monotonic() - started < 0.3
    assert not run._pending_snapshot.is_settled


def test_an_explicit_snapshot_after_open_wins(app, opened, held_record):
    """`run.snapshot()` soon after open (as `run.execute()` takes the child's) settles the
    open's first, so its env_ref and launch block are the ones the run ends with."""
    client, _ = opened
    held_record.hold(client)
    run = _open(client)
    held_record.release()

    # A record of its own (no GPU section), as a child's venv makes one in `run.execute()`.
    explicit = run.snapshot(argv=["python", "CHILD_SCRIPT.py"], include_gpu=False)
    run.finish("completed", flush_timeout=30)

    row = app.runs[run.id]
    assert len(app.execution_records) == 2, "the open's record and the explicit one"
    assert row["env_ref"] == explicit["content_hash"]
    assert row["metadata"]["launch"]["process"]["argv"] == ["python", "CHILD_SCRIPT.py"]


def test_a_sync_client_keeps_the_in_hand_snapshot(app, tmp_path, monkeypatch):
    repo = make_pushed_repo(tmp_path)
    monkeypatch.chdir(repo)
    monkeypatch.setenv("PROBE_AUTO_SNAPSHOT", "1")
    client = make_client(app, tmp_spool=tmp_path / "spool")  # async_writes=False
    run = _open(client)
    assert getattr(run, "_pending_snapshot", None) is None
    bundle = client.run_bundle(run.id)
    assert bundle["run"]["env_ref"], "a sync-write client gets its pin in hand, as before"


# -- git ------------------------------------------------------------------------------


def test_ls_remote_never_accepts_a_new_host_key(monkeypatch):
    monkeypatch.delenv("GIT_SSH_COMMAND", raising=False)
    env = _snapshot._ls_remote_env()
    assert "accept-new" not in env["GIT_SSH_COMMAND"]
    assert "BatchMode=yes" in env["GIT_SSH_COMMAND"] and env["GIT_TERMINAL_PROMPT"] == "0"


def test_the_verify_fetch_never_accepts_a_new_host_key(monkeypatch):
    """I17: `commit_on_remote` (check_run --verify) fetches with the same BatchMode env."""
    monkeypatch.delenv("GIT_SSH_COMMAND", raising=False)
    seen: list[dict] = []
    real_run = subprocess.run

    def run(args, **kwargs):
        if args[:2] == ["git", "fetch"]:
            seen.append(kwargs.get("env") or {})
            return subprocess.CompletedProcess(args, 0, "", "")
        return real_run(args, **kwargs)

    monkeypatch.setattr(subprocess, "run", run)
    assert _snapshot.commit_on_remote("ssh://git@example.invalid/x.git", "a" * 40)
    assert seen and "accept-new" not in seen[0]["GIT_SSH_COMMAND"]
    assert "BatchMode=yes" in seen[0]["GIT_SSH_COMMAND"]


def test_an_unreachable_remote_answers_none_within_the_cap(tmp_path):
    repo = make_pushed_repo(tmp_path)
    subprocess.run(
        ["git", "remote", "set-url", "origin", "ssh://git@10.255.255.1:22/x.git"],
        cwd=repo, check=True,
    )
    answers: list[tuple] = []
    done = threading.Event()

    def on_answer(base, remote):
        answers.append((base, remote))
        done.set()

    started = time.monotonic()
    _snapshot.start_pushed_base(str(repo), on_answer, cap=1.0)
    assert done.wait(5.0)
    assert answers == [(None, None)]
    assert time.monotonic() - started < 3.0


# -- the process ends while the record hangs: SIGTERM and atexit closes -------------------

_CHILD = """
import json, os, sys, time
import probe
from probe.sdk.run.files import snapshot_queue

snapshot_queue.EXECUTION_RECORD_TIMEOUT_SECONDS = float(sys.argv[2])
run = probe.init(experiment="e1", name="hung-record")
for step in range(5):
    probe.log({"loss": 1.0 / (step + 1)}, step=step)
os.write(1, ("CHILD " + json.dumps({"event": "ready", "run_id": run.id}) + "\\n").encode())
if sys.argv[1] == "sigterm":
    while True:
        time.sleep(0.05)
"""


@pytest.mark.parametrize("how", ["sigterm", "exit"])
def test_a_process_ending_while_the_record_hangs_queues_nothing_after_the_status(
    app, tmp_path, monkeypatch, how
):
    """The record's POST hangs (12 s at the server) while the process ends: by SIGTERM
    (`preempt`, the close on its worker) or by falling off the end (atexit). Either close
    shuts the gate before its status: the run closes with its launch PATCH, archive and
    code-snapshot row ahead of the status, no env_ref, and nothing of the snapshot after."""
    from tests.test_sigterm_flush import _stop_workers_of

    repo = make_pushed_repo(tmp_path)
    outbox = str(tmp_path / "outbox")
    app.seed_experiment("e1")
    app.latency = lambda request: 12.0 if request.url.path == RECORDS else 0.0
    env = child_env(
        "", PROBE_AUTO_SNAPSHOT="1", PROBE_HW="0", PROBE_EPHEMERAL="0",
        PROBE_SIGTERM_FLUSH_SECONDS="10", PROBE_OUTBOX_DIR=outbox,
    )
    try:
        with serve(app) as url:
            env["PROBE_BASE_URL"] = url
            app.upload_base = url  # the archive's PUT reaches the served fake too
            proc = subprocess.Popen(
                [sys.executable, "-c", _CHILD, how, "2.0"], cwd=repo, env=env,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
            )
            ready = _child_line(proc, "ready")
            if how == "sigterm":
                proc.send_signal(signal.SIGTERM)
            try:
                _, err = proc.communicate(timeout=40)
            except subprocess.TimeoutExpired:
                proc.kill()
                raise AssertionError(f"the child hung: {proc.communicate()[1][-3000:]}")
    finally:
        _stop_workers_of(outbox)

    run_id = ready["run_id"]
    assert proc.returncode == (-signal.SIGTERM if how == "sigterm" else 0), err[-3000:]
    row = app.runs[run_id]
    assert row["status"] == ("failed" if how == "sigterm" else "completed"), err[-3000:]
    assert not row.get("env_ref")
    assert "execution record not recorded at run open" in err
    status_at = next(
        i for i, r in enumerate(app.requests) if _is_status(r) and r.url.path == f"/v1/runs/{run_id}"
    )
    writes = _snapshot_writes(app, run_id)
    assert {"launch", "row", "archive"} <= {what for _, what in writes}, (writes, err[-3000:])
    assert all(i < status_at for i, _ in writes), (writes, status_at)


def _child_line(proc, event: str, timeout: float = 60.0) -> dict:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        line = proc.stdout.readline()
        if not line:
            break
        if line.startswith("CHILD "):
            got = json.loads(line[len("CHILD "):])
            if got["event"] == event:
                return got
    proc.kill()
    raise AssertionError(f"the child never said {event!r}: {proc.communicate()[1][-3000:]}")


# -- final review of #3792 ----------------------------------------------------------------


def test_a_pushed_base_thread_that_cannot_start_still_posts_the_record(app, opened, monkeypatch):
    """`start_pushed_base` raising (a thread limit) left the open before `pending.start()`: no
    record, no env_ref, and nothing for a close or exit to settle. The record goes without a
    pushed base instead."""
    client, _ = opened

    def refuse(cwd, on_answer, **kwargs):
        raise RuntimeError("can't start new thread")

    monkeypatch.setattr(_snapshot, "start_pushed_base", refuse)
    run = _open(client)
    assert getattr(run, "_pending_snapshot", None) is not None, "the record was never started"
    run.finish("completed", flush_timeout=30)
    assert app.runs[run.id]["env_ref"]


@pytest.mark.parametrize("left", [0.0, 0.1], ids=["no-time", "a-sliver"])
def test_a_record_the_close_already_gave_up_on_is_never_posted(monkeypatch, left):
    """A run closed while the record still waited for its pushed base: the gate was shut, yet
    the thread went on to POST a record nobody pins (an orphan on the server). Convergence
    review: `settle()` woke the record before it shut the gate, with no time left to wait for
    its answer (testing specialist) or less than a POST takes (red team, native adversarial);
    every wake must find the gate shut."""
    monkeypatch.setattr(snapshot_queue, "PUSHED_BASE_WAIT_SECONDS", 5.0)
    client, writes = _Client(), []
    client.go.set()
    pending = _pending(client, writes, should_wait_for_pushed=True)
    pending.start()
    gate_shut_at_each_wake: list[bool] = []
    real_set = pending._pushed_answered.set

    def set_() -> None:
        gate_shut_at_each_wake.append(pending.is_settled)
        real_set()

    monkeypatch.setattr(pending._pushed_answered, "set", set_)
    with pytest.warns(UserWarning, match="no answer before the run closed"):
        pending.settle(time.monotonic() + left)
    _join_record_threads()
    assert gate_shut_at_each_wake and all(gate_shut_at_each_wake), gate_shut_at_each_wake
    assert client.bodies == [], "the record was posted after the gate shut"
    assert writes == [("pin", None), ("row", None, None, None)]


def test_a_warning_stuck_on_stderr_never_holds_a_reader_of_the_pin(monkeypatch):
    """The record thread said its notices before it marked the record done: a stderr that
    blocks (a pipe nobody reads) held `wait_for_record()` (the hardware rail, a close) until the
    record's deadline although the pin was queued."""
    stuck = threading.Event()
    released = threading.Event()

    def warn(message, **kwargs):
        if threading.current_thread().name == "probe-execution-record":
            stuck.set()
            released.wait(10)

    monkeypatch.setattr(snapshot_queue._diagnostics, "warn", warn)
    client, writes = _Client(), []
    client.go.set()
    pending = PendingSnapshot(
        client, {}, pin=lambda h: writes.append(("pin", h)) or "probe: env_ref was queued, not confirmed",
        rewrite_row=lambda h, b, r: writes.append(("row", h, b, r)), should_wait_for_pushed=False,
    )
    pending.start()
    try:
        assert stuck.wait(5), "the record thread never warned"
        started = time.monotonic()
        pending.wait_for_record()
        assert time.monotonic() - started < 0.5
        assert writes == [("pin", "h"), ("row", "h", None, None)]
    finally:
        released.set()
        _join_record_threads()


def test_an_archive_over_the_inspection_limit_asks_the_server_nothing_from_the_open(app, opened, monkeypatch):
    """An archive the outbox would not stage (over the inspection limit) fell back to
    `_maybe_multipart`, which asks `GET /v1/server/features` whenever no verdict is cached
    (the open's own lease ask failed, say): a network wait back on `probe.init()`'s thread.
    Only a verdict already in hand is used."""
    from probe.sdk.artifact.storage_handlers import multipart as _multipart

    client, _ = opened

    def over_the_limit(**kwargs):
        raise ValueError("over the inspection limit")

    monkeypatch.setattr(client.journal, "append_upload", over_the_limit)
    monkeypatch.setattr(_multipart, "over_threshold", lambda path: True)
    real_supports = type(client).supports_feature
    asking = threading.Event()
    asked: list[str] = []

    def supports_feature(self, name):
        if name == _multipart.FEATURE:
            self._server_features_cache = None  # as if nothing had answered yet
            asking.set()
        try:
            return real_supports(self, name)
        finally:
            asking.clear()

    real = client.transport.request

    def request(method, path, *args, **kwargs):
        if asking.is_set() and threading.current_thread() is threading.main_thread():
            asked.append(f"{method} {path}")
        return real(method, path, *args, **kwargs)

    monkeypatch.setattr(type(client), "supports_feature", supports_feature)
    monkeypatch.setattr(client.transport, "request", request)
    with pytest.warns(UserWarning, match="code-bytes archive not stored"):
        run = _open(client)
    assert asked == [], asked
    run.finish("completed", flush_timeout=30)


def test_check_run_finds_the_open_rows_a_long_run_pushed_out_of_its_bundle(app, opened, monkeypatch):
    """The run bundle holds the newest 50 artifacts; the open's code-snapshot row and archive are
    a run's oldest, so a run that logged 50 more read `code_snapshot_artifact` and
    `pending_code_bytes` for good. Past a cut bundle `check_run` asks for those kinds by name."""
    client, _ = opened
    run = _open(client)
    run.finish("completed", flush_timeout=30)
    client.flush()
    real_bundle = client.run_bundle

    def cut_bundle(run_id, *args, **kwargs):
        bundle = real_bundle(run_id, *args, **kwargs)
        kept = [a for a in bundle["artifacts"] if a.get("kind") not in ("code_snapshot", "code_bytes")]
        return {**bundle, "artifacts": kept, "artifact_total": len(kept) + 60}

    monkeypatch.setattr(client, "run_bundle", cut_bundle)
    missing = client.check_run(run.id)["missing"]
    assert "code_snapshot_artifact" not in missing and "pending_code_bytes" not in missing, missing



def test_a_close_does_not_wait_out_ls_remote(monkeypatch):
    """Plan T5: the pushed base rides the record only if `ls-remote` answered before the close.
    A close waited out the pushed-base wait (up to 2.5 s) before the record's POST even began,
    so a short run, or one behind a firewall, paid it on every `finish()`."""
    client, writes = _Client(), []
    client.go.set()
    pending = _pending(client, writes, should_wait_for_pushed=True)  # ls-remote never answers
    pending.start()
    started = time.monotonic()
    pending.settle(time.monotonic() + 10)
    took = time.monotonic() - started
    _join_record_threads()
    assert took < 1.0, f"the close waited {took:.2f}s for ls-remote"
    assert writes == [("pin", "h"), ("row", "h", None, None)]


def test_a_failed_record_never_holds_a_reader_on_a_stuck_stderr(monkeypatch):
    """The failure branch said its gap warning before it marked the record done: a stderr that
    blocks held `wait_for_record()` (the hardware rail, a close) to the record's deadline."""
    stuck = threading.Event()
    released = threading.Event()

    def warn(message, **kwargs):
        if threading.current_thread().name == "probe-execution-record":
            stuck.set()
            released.wait(10)

    monkeypatch.setattr(snapshot_queue._diagnostics, "warn", warn)
    client, writes = _Client(), []

    def refused(path, body):
        raise errors.ValidationError("bad", status=422)

    client.transport.post = refused
    pending = _pending(client, writes, should_wait_for_pushed=False)
    pending.start()
    try:
        assert stuck.wait(5), "the record thread never warned"
        started = time.monotonic()
        pending.wait_for_record()
        assert time.monotonic() - started < 0.5
        assert client.gaps and writes == [("pin", None), ("row", None, None, None)]
    finally:
        released.set()
        _join_record_threads()


def test_check_run_never_calls_an_unanswered_kind_read_missing(app, opened, monkeypatch):
    """Past a cut bundle `check_run` asks for the open's code rows by kind; a read that fails
    (a 503, the network) said nothing, yet it was taken for "none there", so the run read
    `code_snapshot_artifact` and `pending_code_bytes` missing on a blip."""
    client, _ = opened
    run = _open(client)
    run.finish("completed", flush_timeout=30)
    client.flush()
    real_bundle = client.run_bundle

    def cut_bundle(run_id, *args, **kwargs):
        bundle = real_bundle(run_id, *args, **kwargs)
        kept = [a for a in bundle["artifacts"] if a.get("kind") not in ("code_snapshot", "code_bytes")]
        return {**bundle, "artifacts": kept, "artifact_total": len(kept) + 60}

    def unanswered(*args, **kwargs):
        raise errors.ServerError("unavailable", status=503)

    monkeypatch.setattr(client, "run_bundle", cut_bundle)
    monkeypatch.setattr(client, "list_run_artifacts", unanswered)
    missing = client.check_run(run.id)["missing"]
    assert "code_snapshot_artifact" not in missing and "pending_code_bytes" not in missing, missing


def test_check_run_past_a_cut_bundle_still_reports_an_archive_that_never_landed(app, opened, monkeypatch):
    """The other side of asking by kind: a read that answers with no `code_bytes` row of the
    queued archive's hash leaves it pending."""
    client, _ = opened
    run = _open(client)
    run.finish("completed", flush_timeout=30)
    client.flush()
    app.artifacts[run.id] = [a for a in app.artifacts[run.id] if a.get("kind") != "code_bytes"]
    real_bundle = client.run_bundle

    def cut_bundle(run_id, *args, **kwargs):
        bundle = real_bundle(run_id, *args, **kwargs)
        kept = [a for a in bundle["artifacts"] if a.get("kind") not in ("code_snapshot", "code_bytes")]
        return {**bundle, "artifacts": kept, "artifact_total": len(kept) + 60}

    monkeypatch.setattr(client, "run_bundle", cut_bundle)
    assert "pending_code_bytes" in client.check_run(run.id)["missing"]


def test_a_storage_outage_on_the_open_archive_never_holds_the_close(app, opened, held_record):
    """The open queues its archive (non-blocking) before the record answers, so the env_ref
    PATCH and the row's rewrite (blocking) queue behind it. A storage outage parked the archive
    at the head of the run's lane and held them, and `finish()` deferred the run's status
    (Codex structured review, final pass). The archive rides a lane of its own."""
    from probe.sdk.artifact.filetype import name_with_extension

    client, _ = opened
    held_record.hold(client)
    held_record.delay = 0.0
    app.fail_put_names = {name_with_extension(_snapshot.CODE_BYTES_ARTIFACT, "code.tar.gz")}
    run = _open(client)
    held_record.release()  # answers now: its pin and row queue behind the archive
    run._wait_for_open_record()
    report = run.finish("completed", flush_timeout=10)
    assert app.runs[run.id]["status"] == "completed", report
    assert app.runs[run.id]["env_ref"]
    queued = _queued(client)
    assert queued == ["archive"], queued


def test_a_store_that_never_answers_the_open_archive_never_holds_the_close(app, opened, held_record, monkeypatch):
    """As the outage above, but a store that takes the bytes and never answers: a run's close
    walked its ops in queue order, the archive (queued at open) first, and its PUT spent the
    whole drain budget before the record's PATCH and the row went, so the status was deferred
    (red team, pass 3). A run's own pass sends the run's own lane first."""
    from probe.sdk.delivery.transport import transport as transport_module
    from probe.sdk.delivery.transport.deadlines import deadline_remaining

    client, _ = opened
    held_record.hold(client)
    held_record.delay = 0.0

    def hung(self, url, path, **kwargs):
        time.sleep(max(0.0, deadline_remaining(30.0)))  # a request ends at its deadline
        raise errors.TransportError("PUT: the store took the bytes and never answered")

    monkeypatch.setattr(transport_module.Transport, "put_file", hung)
    run = _open(client)
    held_record.release()  # answers now: its pin and row queue behind the archive
    run._wait_for_open_record()
    report = run.finish("completed", flush_timeout=4)
    assert app.runs[run.id]["status"] == "completed", report
    assert app.runs[run.id]["env_ref"]


def test_a_runs_own_pass_never_takes_the_open_archive_into_its_upload_window(app, tmp_path, monkeypatch):
    """A run's own pass sends the run's lane first, but its parallel upload window took the head
    of every lane in reach: the open's archive (a lane of its own) beside the run's own upload,
    waiting for both. A store that never answers spent the whole pass there, and the run's PATCH
    behind its upload never went (review of #3804's last five commits)."""
    from probe.sdk.delivery.outbox.drain.drain import drain
    from probe.sdk.delivery.transport import transport as transport_module
    from probe.sdk.delivery.transport.deadlines import deadline_remaining, deadline_scope

    client = make_client(app, tmp_spool=tmp_path / "spool", async_writes=True)
    client.create_project("lab", "Lab", kind="general")
    run = client.run(project="lab", name="window", heartbeat=False)
    client.flush()
    archive = tmp_path / "code.tar.gz"
    archive.write_bytes(b"\x1f\x8b" + b"x" * 64)
    client.journal.append_upload(
        anchor="run", anchor_id=run.id, name="code-bytes.gz", src_path=str(archive),
        content_type="application/gzip", kind="code_bytes", run_ref=run.id,
        require_staged=True, blocking=False, lane=f"code-bytes:{run.id}",
    )
    notes = tmp_path / "notes.txt"
    notes.write_text("notes\n")
    client.journal.append_upload(
        anchor="run", anchor_id=run.id, name="notes.txt", src_path=str(notes),
        content_type="text/plain", run_ref=run.id, require_staged=True,
    )
    client.journal.append_http("PATCH", f"/v1/runs/{run.id}", {"tags": ["window"]}, run_ref=run.id)
    real_put = transport_module.Transport.put_file

    def put_file(self, url, path, **kwargs):
        with open(path, "rb") as handle:
            is_archive = handle.read(2) == b"\x1f\x8b"
        if is_archive:  # the store takes the bytes and never answers: the request ends at its deadline
            time.sleep(max(0.0, deadline_remaining(30.0)))
            raise errors.TransportError("PUT: the store took the bytes and never answered")
        return real_put(self, url, path, **kwargs)

    monkeypatch.setattr(transport_module.Transport, "put_file", put_file)
    with deadline_scope(time.monotonic() + 2.0):
        drain(client.journal, run_ref=run.id, client_factory=client._outbox_client_factory())
    assert app.runs[run.id].get("tags") == ["window"]
    assert [op.get("lane") for _, op in client.journal.pending()] == [f"code-bytes:{run.id}"]


def test_one_503_on_the_runs_lane_never_hands_the_close_to_a_hung_archive(app, opened, held_record, monkeypatch):
    """A run's own pass sends its lane first, but one 503 left that lane for the next pass and
    the pass went on to the open's archive, whose hung PUT spent the rest of the close's
    deadline: the status was deferred (red team, review of #3804's last five commits). What
    rides a lane of its own goes only once the run's lane is through."""
    import httpx

    from probe.sdk.delivery.transport import transport as transport_module
    from probe.sdk.delivery.transport.deadlines import deadline_remaining

    client, _ = opened
    held_record.hold(client)
    held_record.delay = 0.0

    def hung(self, url, path, **kwargs):
        time.sleep(max(0.0, deadline_remaining(30.0)))
        raise errors.TransportError("PUT: the store took the bytes and never answered")

    monkeypatch.setattr(transport_module.Transport, "put_file", hung)
    run = _open(client)
    held_record.release()
    run._wait_for_open_record()
    real = httpx.MockTransport.handle_request
    blip = {"armed": True}

    def handle_request(self, request):
        if blip["armed"] and request.url.path.startswith(f"/v1/runs/{run.id}") and request.method in ("PATCH", "POST"):
            blip["armed"] = False
            return httpx.Response(503, headers={"Retry-After": "0.1"}, json={"detail": "blip"}, request=request)
        return real(self, request)

    monkeypatch.setattr(httpx.MockTransport, "handle_request", handle_request)
    report = run.finish("completed", flush_timeout=4)
    assert not blip["armed"], "the run's lane never saw its 503"
    assert app.runs[run.id]["status"] == "completed", report
    assert app.runs[run.id]["env_ref"]


def test_check_run_past_a_cut_bundle_reports_a_snapshot_row_that_is_absent(app, opened, monkeypatch):
    """A kind read that answers with no code-snapshot row reports it missing: unread is unknown,
    but read-and-absent is absent."""
    client, _ = opened
    run = _open(client)
    run.finish("completed", flush_timeout=30)
    client.flush()
    app.artifacts[run.id] = [a for a in app.artifacts[run.id] if a.get("kind") != "code_snapshot"]
    real_bundle = client.run_bundle
    monkeypatch.setattr(client, "run_bundle", lambda run_id, *a, **k: {**real_bundle(run_id, *a, **k), "artifact_total": 999})
    assert "code_snapshot_artifact" in client.check_run(run.id)["missing"]


def test_check_run_verify_on_an_unread_archive_is_never_complete(app, opened, monkeypatch):
    """`verify=True` on a self-contained snapshot proved `complete` though the archive's kind
    read had failed: unread is unknown, so the verdict stays `unverified` (Codex, final pass)."""
    client, _ = opened
    run = _open(client)
    run.finish("completed", flush_timeout=30)
    client.flush()
    real_bundle = client.run_bundle
    real_list = client.list_run_artifacts

    def cut_bundle(run_id, *args, **kwargs):
        bundle = real_bundle(run_id, *args, **kwargs)
        kept = [a for a in bundle["artifacts"] if a.get("kind") != "code_bytes"]
        return {**bundle, "artifacts": kept, "artifact_total": len(kept) + 60}

    def list_kind(run_id, *, kind=None, **kwargs):
        if kind == "code_bytes":
            raise errors.ServerError("unavailable", status=503)
        return real_list(run_id, kind=kind, **kwargs)

    monkeypatch.setattr(client, "run_bundle", cut_bundle)
    monkeypatch.setattr(client, "list_run_artifacts", list_kind)
    verdict = client.check_run(run.id, verify=True)
    assert verdict["state"] != "complete", verdict
    assert "pending_code_bytes" not in verdict["missing"]


# -- convergence review of #3804 ------------------------------------------------------------


def _cut_without(client, monkeypatch, name: str) -> None:
    """The run bundle as a long run's: the newest 50 artifacts, here every one but ``name``."""
    real_bundle = client.run_bundle

    def cut_bundle(run_id, *args, **kwargs):
        bundle = real_bundle(run_id, *args, **kwargs)
        kept = [a for a in bundle["artifacts"] if a.get("name") != name]
        return {**bundle, "artifacts": kept, "artifact_total": len(kept) + 60}

    monkeypatch.setattr(client, "run_bundle", cut_bundle)


def _old_failed_upload(app, run_id: str) -> None:
    app.artifacts[run_id].insert(0, {
        "id": "00000000-0000-4000-8000-00000000c0de", "run_id": run_id, "kind": "checkpoint",
        "name": "ckpt-0", "is_reference": True, "status": "complete", "meta": {"upload": "failed"},
    })


def test_check_run_verify_past_a_cut_bundle_sees_an_old_failed_upload(app, opened, monkeypatch):
    """Past a cut bundle the open's rows are found by kind, so `verify=True` certified a long run
    `complete` while a failed upload older than the bundle's newest 50 went unseen (Codex). A
    complete verdict reads every failed upload."""
    client, _ = opened
    run = _open(client)
    run.finish("completed", flush_timeout=30)
    client.flush()
    _old_failed_upload(app, run.id)
    _cut_without(client, monkeypatch, "ckpt-0")
    asked_from = len(app.requests)
    verdict = client.check_run(run.id, verify=True)
    assert verdict["state"] == "incomplete" and "portable_artifact_bytes" in verdict["missing"], verdict
    # Per-file code captures (thousands on a converted snapshot) are never failed uploads: the
    # inventory read leaves them out (performance specialist).
    inventory = [
        r for r in app.requests[asked_from:]
        if r.method == "GET" and r.url.path == f"/v1/runs/{run.id}/artifacts" and "kind" not in r.url.params
    ]
    assert inventory and all(r.url.params.get("include_captured") == "false" for r in inventory), inventory


def test_check_run_verify_past_a_cut_bundle_with_the_inventory_unread_is_never_complete(app, opened, monkeypatch):
    """The other side: when the whole inventory cannot be read, the failed uploads are unknown,
    so the verdict stays `unverified`."""
    client, _ = opened
    run = _open(client)
    run.finish("completed", flush_timeout=30)
    client.flush()
    _cut_without(client, monkeypatch, "ckpt-0")
    real_request = client.transport.request

    def request(method, path, *args, params=None, **kwargs):
        if method == "GET" and path.endswith("/artifacts") and "kind" not in (params or {}):
            raise errors.ServerError("unavailable", status=503)
        return real_request(method, path, *args, params=params, **kwargs)

    monkeypatch.setattr(client.transport, "request", request)
    verdict = client.check_run(run.id, verify=True)
    assert verdict["state"] == "unverified" and verdict["missing"] == [], verdict


def test_check_run_reads_a_queued_archive_naming_no_hash_as_still_pending():
    """The SDK twin of reproduce `_has_code_archive`: a queued row naming no string
    `archive_sha256` matched a landed `code_bytes` row carrying no `content_hash` (None == None)
    and read as landed, where the server keeps it pending (red team)."""
    from probe.sdk.client.resources.runs.check import _is_archive_still_queued

    hashless = [{"kind": "code_bytes", "is_reference": False, "status": "complete"}]
    assert _is_archive_still_queued({"code_bytes": {"queued": True}}, hashless) is True
    assert _is_archive_still_queued({"code_bytes": {"queued": True, "archive_sha256": 5}}, hashless) is True
    landed = [{"kind": "code_bytes", "is_reference": False, "status": "complete", "content_hash": "a" * 64}]
    assert _is_archive_still_queued({"code_bytes": {"queued": True, "archive_sha256": "a" * 64}}, landed) is False


def test_the_record_post_stops_retrying_once_the_close_shuts_the_gate(monkeypatch):
    """The record's retries went on after the close shut the gate: a 503 or a 429, the close
    giving up meanwhile, then a retry that landed a record nobody pins (Codex adversarial, pass 3)."""
    stopped = {"now": False}
    monkeypatch.setattr(snapshot_queue.time, "sleep", lambda seconds: stopped.update(now=True))
    busy = _Transport(errors.ServerError("busy", status=503), {"content_hash": "h"})
    client = type("C", (), {"transport": busy})()
    with pytest.raises(errors.ServerError):
        snapshot_queue.post_execution_record(
            client, {}, deadline=time.monotonic() + 5, should_stop=lambda: stopped["now"]
        )
    assert len(busy.calls) == 1


def _gapless_client(transport):
    class Journal:
        def note_capture_gap(self, reason):
            pass

    return type("C", (), {"transport": transport, "journal": Journal()})()


def test_a_record_retrying_while_the_close_gives_up_posts_nothing_more(monkeypatch):
    """The wiring: the record thread's retry stops once its gate is shut."""
    busy = _Transport(errors.ServerError("busy", status=503), {"content_hash": "h"})
    writes: list = []
    pending = _pending(_gapless_client(busy), writes, should_wait_for_pushed=False)
    monkeypatch.setattr(snapshot_queue._diagnostics, "warn", lambda *a, **k: None)
    monkeypatch.setattr(snapshot_queue.time, "sleep", lambda seconds: pending._shut_gate())
    pending.start()
    _join_record_threads()
    assert len(busy.calls) == 1, "a retry went out after the gate shut"
    assert writes == [("pin", None), ("row", None, None, None)]


def test_a_record_the_close_wakes_ends_while_the_close_still_waits(monkeypatch):
    """`settle()` woke the record with time left, but its POST kept its own deadline (up to 5 s):
    the close shut the gate first and a POST still running landed a record nobody pins (native
    adversarial, pass 3). The POST it wakes ends before the close stops waiting for it."""
    monkeypatch.setattr(snapshot_queue, "PUSHED_BASE_WAIT_SECONDS", 5.0)
    answering = _Transport({"content_hash": "h"})
    writes: list = []
    pending = _pending(_gapless_client(answering), writes, should_wait_for_pushed=True)
    monkeypatch.setattr(snapshot_queue._diagnostics, "warn", lambda *a, **k: None)
    pending.start()
    wait_until = time.monotonic() + 1.0
    pending.settle(wait_until)
    _join_record_threads()
    (_, post_deadline), = answering.calls
    assert post_deadline is not None and post_deadline <= wait_until, (post_deadline, wait_until)
