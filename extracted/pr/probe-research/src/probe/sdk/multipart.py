"""Artifacts over 64 MiB: staged, then uploaded in parts (plan item (g)).

WHY. Every other upload reads the whole file through the credential gate,
which refuses anything over its 64 MiB inspection limit, and the server's
relay has the same ceiling. A checkpoint above it used to be kept only as a
local pointer (plan 0.7). A server that declares ``artifact_multipart`` in
``/v1/server/features`` takes it in parts, each PUT straight to object
storage on a presigned URL; the server's verifier proves the whole object's
sha256 before the artifact goes live (`app/artifacts/multipart.py`).

THE BYTES ARE STAGED FIRST (Codex round 2). ``log_artifact`` returns at once
and the upload runs later, so the file has to survive checkpoint rotation and
pod deletion for as long as that takes:

  * a HARDLINK into the outbox when the file is on the same filesystem: the
    inode stays exactly as it is when the trainer replaces the path by rename
    (``torch.save`` to a temp name, then ``os.replace``), and costs no space
    until the trainer deletes its own copy;
  * otherwise a reflink, or a byte copy (on the calling thread: a copy across
    filesystems is the one slow step ``log_artifact`` can take);
  * either way only while the staging filesystem's free space, less the
    outbox's own floor (#2054), covers this file AND every staged file of the
    uploads still waiting -- counted as if the trainer had deleted each source
    already, since a pinned hardlink is exactly what keeps those bytes on
    disk. Past that budget nothing is staged and the call records a reference
    row with a warning, as before.

A hardlink shares the file a trainer might instead rewrite IN PLACE, so the
staged copy's identity (device, inode, size, mtime) is checked before and after
the hash, around every slice of parts and before complete: a change aborts the
upload ("swapped inode aborts") and records a reference row. Anything the check
misses, the server's sha256 catches.

The staged copy is deleted once the server reports the upload ``verified``
(or a HAVE: those bytes were already stored), when the op dead-letters, or
after 7 days, whichever comes first; a copy whose op is gone, or a partial
copy a kill cut short, is collected at the start of every drain pass.

THE OP. ``multipart_upload`` is queued in ``<outbox>/multipart/ops/``, a queue
of its own that NO earlier release reads: an older worker sharing the outbox
never meets the op -- it can neither hold it (0.191+: holding its run's whole
lane, and never exiting) nor dead-letter it (0.190) -- and this release's
drain appends it after every other lane. The producer still asks the live
worker (`outbox_worker.ready_for`), so an older one steps aside for a current
one. The op has a lane of its own (``op["lane"]``) and is ``blocking=False``.
ONE upload moves at a time -- the oldest not waiting on the server -- so an
earlier checkpoint finishes, and frees its staged bytes, before a later one
pins more. A visit hashes the staged copy in a background thread (the pass
does not wait for 10 GB of sha256), then does one slice (`SLICE_SECONDS`)
with up to `PARALLEL_PARTS` part PUTs in flight (a slice can overrun by the
parts already in flight when it ends), saves where it got to, and raises
`OpInProgress`. A restarted worker lists the parts the server holds and sends
only the missing ones; an upload the server gave up on while this machine was
away (idle 24 h, 7 days old, never verified) is started again from the staged
copy, at most `_MAX_RESTARTS` times.

FINISH. ``finish()`` does not wait while a detached worker on durable storage
will carry the upload after the process exits; it says how many are still
uploading. When nothing would -- a client that delivers in-process (a token
passed in code, ``drain_interval``), an outbox on a disposable disk (a pod
without a volume, Modal) -- it sends them itself within its deadline, and
records whatever did not make it as a reference row before it returns.

THE CREDENTIAL GATE. These bytes reach object storage before anything scans
them: `Transport.put_part` is the one byte path with no local gate (a part
cannot be redacted without breaking the sha256, and the size limit is why it
is going this way). The server's verifier inspects a bounded prefix and
RECORDS findings on the artifact; nothing is blocked. A credential in the
PATH is still refused before anything happens (`secret_gate._check_path`).

Only an explicit ``log_artifact`` uses this (D12): output capture keeps files
over 64 MiB as pointers.
"""

from __future__ import annotations

import json
import os
import shutil
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any, Callable

from . import errors
from .durable import fsync_directory, try_clone, write_text_atomic
from .hashing import fingerprint
from .journal import OpInProgress

#: The outbox op kind (registered in `journal.OP_KINDS`).
KIND = "multipart_upload"
#: What the server declares when it takes multipart uploads.
FEATURE = "artifact_multipart"
#: Part PUTs in flight at once, per upload.
PARALLEL_PARTS = 4
#: Wall clock one drain visit may spend sending parts before it saves and
#: yields, so the rest of the queue is never more than this far behind.
SLICE_SECONDS = 20.0
#: A staged copy is given up on (and deleted) this long after it was made.
STAGED_TTL_SECONDS = 7 * 86_400
#: How long the lane waits between polls while the server verifies (the
#: lane's own backoff grows from here while it keeps waiting).
VERIFY_POLL_SECONDS = 5.0
#: How long to wait when another upload of the same bytes is in progress in
#: the team (the server's unique active upload); it becomes a HAVE once done.
BUSY_RETRY_SECONDS = 30.0
#: ...and the longest the lane waits between tries while that lasts, however
#: far its backoff has grown: the server hands the bytes to the next create
#: once the other upload has been idle 10 min (its uploader gone), and a lane
#: at the 300 s ceiling would take that up minutes late.
BUSY_MAX_WAIT_SECONDS = 60.0
#: How long the lane waits between looks at a hash running in the background.
HASH_POLL_SECONDS = 2.0
#: Server-side endings after which the upload is simply started again from the
#: staged copy (the bytes were never judged wrong), at most `_MAX_RESTARTS`
#: times: this machine was away longer than the server keeps an idle upload.
_RESTARTABLE = frozenset(
    {
        "idle",
        "expired",
        "store_upload_missing",
        "verification_timed_out",
        "verification_gave_up",
        # A create of the same bytes found this upload idle and took over
        # (this machine went quiet past the server's takeover threshold):
        # starting again waits on that upload and becomes a HAVE.
        "superseded_idle",
    }
)
_MAX_RESTARTS = 3
#: Slices in a row whose part URLs the store refused (and nothing was sent)
#: before the upload is given up as permanently refused.
_MAX_REFUSED_SLICES = 3
#: An orphaned staged copy (its op gone) is kept this long before gc.
_ORPHAN_GRACE_SECONDS = 3600
#: Part URLs asked for per request (the server's own cap).
_PART_URL_BATCH = 100
#: How long a SYNCHRONOUS upload waits for another upload of the same bytes:
#: past the server's 10 min idle takeover, so a dead uploader's hold on the
#: bytes ends within the wait.
_SYNC_BUSY_WAIT_SECONDS = 720.0


def threshold_bytes() -> int:
    """Above this, ``log_artifact`` uploads in parts: the credential gate's
    whole-file inspection limit (64 MiB), which the server's relay shares."""
    from .secret_gate import ScanPolicy

    return ScanPolicy().max_bytes


def over_threshold(path: str) -> bool:
    try:
        return os.path.getsize(path) > threshold_bytes()
    except OSError:
        return False


def staged_dir(journal: Any) -> Path:
    return Path(journal.dir) / "multipart" / "staged"


def ops_dir(journal: Any) -> Path:
    """This kind's own queue: read by this release's drain, by nothing older."""
    return Path(journal.dir) / "multipart" / "ops"


def failed_dir(journal: Any) -> Path:
    return Path(journal.dir) / "multipart" / "failed"


def _private(path: Path) -> Path:
    """``path`` and ``multipart/`` above it, owner-only (0700) like the rest of
    the outbox, whatever the umask."""
    Path(path.parent.parent).mkdir(parents=True, exist_ok=True)
    for level in (path.parent, path):
        try:
            level.mkdir(mode=0o700)
        except FileExistsError:
            pass
        try:
            os.chmod(level, 0o700)
        except OSError:
            pass
    return path


def _identity(st: os.stat_result) -> dict:
    # Not ctime: making the hardlink itself changes it.
    return {
        "dev": st.st_dev,
        "ino": st.st_ino,
        "size": st.st_size,
        "mtime_ns": st.st_mtime_ns,
    }


def _free_bytes(directory: Path) -> int:
    return shutil.disk_usage(directory).free


def _floor(journal: Any) -> int:
    """The outbox's own free-space floor (#2054), 0 when it has none."""
    try:
        return max(0, int(journal._free_floor()))
    except Exception:  # noqa: BLE001 -- no floor known: no floor
        return 0


def _pinned(journal: Any, directory: Path) -> tuple[int, int]:
    """(bytes, count) of the staged copies of uploads still queued."""
    live = _live_op_ids(journal)
    total = count = 0
    for op_id in live:
        try:
            total += (directory / f"{op_id}.src").stat().st_size
            count += 1
        except OSError:
            continue
    return total, count


class StageRefused(Exception):
    """The file could not be staged within the budget. The caller records a
    reference row and warns."""


def stage(journal: Any, src: str, op_id: str) -> dict:
    """Make the immutable copy the upload will read. Returns the op's
    ``multipart`` staging fields; raises `StageRefused` with the reason."""
    directory = _private(staged_dir(journal))
    dest = directory / f"{op_id}.src"
    size = os.stat(src).st_size
    floor = _floor(journal)
    free = _free_bytes(directory)
    pinned, waiting = _pinned(journal, directory)
    if free - floor < pinned + size:
        mib = 1 << 20
        raise StageRefused(
            f"it could not be staged for a later upload: {free // mib} MiB free on the outbox's "
            f"disk, less its {floor // mib} MiB floor, does not cover its {size // mib} MiB"
            + (f" and the {pinned // mib} MiB of {waiting} upload(s) still waiting" if waiting else "")
        )
    mode = "hardlink"
    try:
        os.link(src, dest)
    except OSError:
        temporary = directory / f".{op_id}.tmp"
        temporary.unlink(missing_ok=True)
        try:
            if try_clone(src, str(temporary)):
                mode = "reflink"
            else:
                shutil.copyfile(src, temporary)
                mode = "copy"
            os.chmod(temporary, 0o600)
            os.replace(temporary, dest)
        finally:
            temporary.unlink(missing_ok=True)
    fsync_directory(directory)
    return {
        "staged_path": str(dest),
        "stage_mode": mode,
        "identity": _identity(os.stat(dest)),
        "staged_at": time.time(),
    }


def build_op(
    journal: Any,
    *,
    run_id: str,
    name: str,
    src: str,
    kind: str | None,
    content_type: str | None,
    meta: dict | None,
    notes: str | None,
    span_id: str | None,
    step_index: int | None,
) -> dict:
    """The queued op, staged. Its ``upload`` block has the shape every reader
    of an upload op already knows (the dead-letter reference row, output
    capture's dedupe, `probe outbox status`); ``multipart`` is its own state."""
    op = journal._base_op(KIND, run_id)
    op["blocking"] = False
    op["lane"] = f"multipart:{op['op_id']}"
    op["multipart"] = {
        **stage(journal, src, op["op_id"]),
        "upload_id": None,
        "artifact_id": None,
        "part_size": None,
        "part_count": None,
        "state": "staged",
    }
    op["upload"] = {
        "anchor": "run",
        "anchor_id": run_id,
        "name": name,
        "src_path": os.path.abspath(src),
        # Not in the outbox's blob store: `journal.gc_blobs` must leave it be.
        "staged": False,
        "blob": None,
        "size_bytes": op["multipart"]["identity"]["size"],
        "content_type": content_type,
        "kind": kind,
        "meta": meta,
        "notes": notes,
        "span_id": span_id,
        "step_index": step_index,
    }
    return op


def enqueue(journal: Any, op: dict) -> Path:
    """Queue the op in this kind's own queue (`ops_dir`). Returns its path."""
    from . import outbox_worker

    path = _private(ops_dir(journal)) / f"{time.time_ns():020d}-{op['op_id']}.json"
    write_text_atomic(path, json.dumps(op, indent=2) + "\n", mode=0o600)
    try:
        # An older worker never sees this op; asking lets a current one take
        # the outbox over sooner (it exits after its pass; the next kick spawns).
        outbox_worker.ready_for(KIND, str(journal.dir))
    except Exception:  # noqa: BLE001 -- a nudge, never a condition
        pass
    return path


def pending(journal: Any) -> list[tuple[Path, dict]]:
    """The queued multipart ops, oldest first (the drain's work list)."""
    directory = ops_dir(journal)
    try:
        names = sorted(n for n in os.listdir(directory) if n.endswith(".json"))
    except OSError:
        return []
    out: list[tuple[Path, dict]] = []
    for name in names:
        path = directory / name
        try:
            op = json.loads(path.read_text())
        except (OSError, ValueError):
            continue
        if isinstance(op, dict) and op.get("kind") == KIND:
            out.append((path, op))
    return out


def _live_op_ids(journal: Any) -> set[str]:
    try:
        names = os.listdir(ops_dir(journal))
    except OSError:
        return set()
    return {n[: -len(".json")].rsplit("-", 1)[-1] for n in names if n.endswith(".json")}


def still_uploading(journal: Any, op_ids: list[str]) -> list[str]:
    """Which of these multipart ops are still queued."""
    if not op_ids:
        return []
    live = _live_op_ids(journal)
    return [op_id for op_id in op_ids if op_id in live]


def gc_staging(journal: Any, *, now: float | None = None) -> int:
    """Delete staged files nothing will read again: a copy whose op is gone
    (finished, dead-lettered, cleared from the outbox) and a partial copy a
    kill cut short (``.<op>.tmp``), once `_ORPHAN_GRACE_SECONDS` old. A LIVE
    op's copy is never touched here: the op itself gives up after 7 days
    (`advance`). Ages by ctime, which linking or writing the copy stamps (a
    hardlink's mtime is its source's). Returns how many went."""
    directory = staged_dir(journal)
    try:
        names = os.listdir(directory)
    except FileNotFoundError:
        return 0
    now = time.time() if now is None else now
    live = _live_op_ids(journal)
    removed = 0
    for name in names:
        partial = name.startswith(".") and name.endswith(".tmp")
        if not partial and name.split(".", 1)[0] in live:
            continue
        path = directory / name
        try:
            age = now - path.stat().st_ctime
        except FileNotFoundError:
            continue
        if age > _ORPHAN_GRACE_SECONDS:
            path.unlink(missing_ok=True)
            removed += 1
    return removed


def release_staged(state: dict) -> None:
    """Delete this upload's staged copy (never the caller's own file)."""
    if state.get("stage_mode") not in ("hardlink", "reflink", "copy"):
        return
    path = state.get("staged_path")
    if path:
        Path(path).unlink(missing_ok=True)


def on_dead_letter(journal: Any, client_for: Callable[[Any], Any], op: dict) -> None:
    """A multipart op that will never finish: abort the server's upload (so
    its parts are discarded now rather than by the server's 24 h sweep) and
    delete the staged copy. Best-effort; never raises."""
    state = op.get("multipart") or {}
    upload = op.get("upload") or {}
    if state.get("upload_id") and state.get("state") not in ("verified", "have"):
        try:
            client = client_for(op.get("context"))
            client.transport.delete(
                f"/v1/runs/{upload.get('anchor_id')}/artifacts/multipart/{state['upload_id']}"
            )
        except Exception:  # noqa: BLE001 -- the server sweeps an idle upload anyway
            pass
    release_staged(state)


def _fields(op: dict) -> tuple[dict, dict]:
    upload, state = op.get("upload"), op.get("multipart")
    if (
        not isinstance(upload, dict)
        or not isinstance(state, dict)
        or not upload.get("anchor_id")
        or not upload.get("name")
        or not state.get("staged_path")
        or not isinstance(state.get("identity"), dict)
    ):
        raise errors.ValidationError(
            f"multipart op {op.get('op_id')} is missing its upload or staging fields", status=422
        )
    return upload, state


def _check_staged(state: dict) -> None:
    """The staged copy is still exactly what was staged, or nothing more is
    sent (a permanent refusal: the drain records a reference row)."""
    try:
        st = os.stat(state["staged_path"])
    except FileNotFoundError:
        raise errors.ValidationError(
            "the staged copy of this artifact is gone", status=422
        ) from None
    if _identity(st) != state["identity"]:
        raise errors.ValidationError(
            "the staged copy of this artifact changed while it was uploading (a hardlink "
            "shares the file the program rewrote in place); nothing more is sent",
            status=422,
        )


def _create(client: Any, upload: dict) -> dict:
    body = {
        "name": upload["name"],
        "content_hash": upload["blob"],
        "size_bytes": upload["size_bytes"],
        "content_type": upload.get("content_type"),
        "span_id": upload.get("span_id"),
        "step_index": upload.get("step_index"),
        "kind": upload.get("kind"),
        "meta": upload.get("meta"),
        "notes": upload.get("notes"),
    }
    body = {k: v for k, v in body.items() if v is not None}
    try:
        # Idempotent server-side: the same (run, name, bytes) gets its own
        # upload back while it is active.
        return client.transport.post(
            f"/v1/runs/{upload['anchor_id']}/artifacts/multipart", body, idempotent=True
        ) or {}
    except errors.ConflictError as exc:
        detail = exc.detail if isinstance(exc.detail, dict) else {}
        if detail.get("state") in ("uploading", "verifying"):
            # Another upload of these bytes is in progress in this team; once
            # it ends (verified: this becomes a HAVE; or failed/aborted) this
            # create goes through. The server bounds the wait -- ~10 min when
            # that other upload's process died (a preempted job's new run
            # re-logging the same checkpoint): the next create after it has
            # been idle that long takes it over -- and the lane retries meanwhile.
            raise _Busy("another upload of these bytes is in progress") from None
        raise


class _Busy(Exception):
    pass


_HASHING: dict[str, dict] = {}
_HASHING_LOCK = threading.Lock()


def _hash_staged(state: dict) -> tuple[str, int]:
    """sha256 of the staged copy, which must be exactly what was staged on
    both sides of the read."""
    _check_staged(state)
    digest, size = fingerprint(state["staged_path"])
    _check_staged(state)
    return digest, size


def _hash_in_background(op_id: str, state: dict) -> tuple[str, int] | None:
    """The staged copy's (sha256, size), hashed on a daemon thread so the
    drain pass that asked does not wait ~30 s per 10 GB. None while it runs
    (the caller comes back later). A process that dies mid-hash loses it and
    the next visit starts again. Raises what the hash raised."""
    with _HASHING_LOCK:
        job = _HASHING.get(op_id)
        if job is None:
            job = {"done": threading.Event(), "result": None, "error": None}
            _HASHING[op_id] = job

            def run(job=job, state=dict(state)) -> None:
                try:
                    job["result"] = _hash_staged(state)
                except BaseException as exc:  # noqa: BLE001 -- handed to the caller
                    job["error"] = exc
                finally:
                    job["done"].set()

            threading.Thread(target=run, name="probe-multipart-hash", daemon=True).start()
            return None
        if not job["done"].is_set():
            return None
        del _HASHING[op_id]
    if job["error"] is not None:
        raise job["error"]
    return job["result"]


def _send_parts(
    client: Any,
    upload: dict,
    state: dict,
    numbers: list[int],
    deadline: float,
    save: Callable[[], None],
) -> None:
    """PUT these parts from the staged copy, `PARALLEL_PARTS` at a time, not
    starting one after ``deadline``.

    A store failure is TRANSIENT here (the store blinked; a part URL expired
    -- they live an hour -- and the next slice asks for fresh ones): it is not
    this machine's credential, so it must never read as an auth block. The one
    exception is a store that keeps refusing the signed URLs themselves
    (`UploadRefused`, #2075): `_MAX_REFUSED_SLICES` slices in a row that sent
    nothing and were refused make it permanent, and the drain records the
    reference row, rather than retrying for the 7 days of staging."""
    part_size = int(state["part_size"])
    path = state["staged_path"]
    for start in range(0, len(numbers), _PART_URL_BATCH):
        if time.monotonic() >= deadline:
            return
        grant = client.transport.post(
            f"/v1/runs/{upload['anchor_id']}/artifacts/multipart/{state['upload_id']}/parts",
            {"part_numbers": numbers[start : start + _PART_URL_BATCH]},
            idempotent=True,
        ) or {}

        def put(part: dict) -> bool:
            if time.monotonic() >= deadline:
                return False
            number = int(part["part_number"])
            client.transport.put_part(
                part["url"],
                path,
                offset=(number - 1) * part_size,
                length=int(part["size"]),
            )
            return True

        with ThreadPoolExecutor(max_workers=PARALLEL_PARTS, thread_name_prefix="probe-part") as pool:
            outcomes = [pool.submit(put, part) for part in grant.get("parts") or ()]
            failures = [f.exception() for f in outcomes if f.exception() is not None]
            sent = sum(1 for f in outcomes if f.exception() is None and f.result())
        if sent and state.get("refused_slices"):
            state["refused_slices"] = 0
            save()
        if not failures:
            continue
        deadline_hit = next((e for e in failures if isinstance(e, errors.DeadlineExceeded)), None)
        if deadline_hit is not None:
            raise deadline_hit
        refused = [e for e in failures if isinstance(e, errors.UploadRefused)]
        if refused and not sent:
            state["refused_slices"] = int(state.get("refused_slices") or 0) + 1
            save()
            if state["refused_slices"] >= _MAX_REFUSED_SLICES:
                raise refused[0]
        first = refused[0] if refused else failures[0]
        # Object storage, not the API: never an auth block, and never "the
        # server is unreachable" for every other lane either.
        raise errors.ServerError(
            f"object storage refused a part ({getattr(first, 'status', None)}): {first}", status=503
        ) from None


def advance(
    client: Any,
    op: dict,
    save: Callable[[], None],
    *,
    deadline: float,
    wait_for_verify: bool = True,
    hash_inline: bool = True,
) -> dict | None:
    """Move one multipart upload as far as ``deadline`` allows. Returns the
    server's answer when it is done (verified, or a HAVE -- or, with
    ``wait_for_verify=False``, verifying: the server has every byte); raises
    `OpInProgress` when there is more to do (``retry_after`` None: parts
    went, come back next pass; a number: waiting -- on the hash, the server's
    verifier, another upload of the same bytes), a permanent error when it
    can never finish. ``hash_inline=False`` hashes on a background thread."""
    upload, state = _fields(op)
    if time.time() - float(state.get("staged_at") or 0) > STAGED_TTL_SECONDS:
        raise errors.ValidationError(
            "this artifact's multipart upload did not finish within 7 days of staging; "
            "its staged copy is deleted",
            status=422,
        )
    if not upload.get("blob"):
        hashed = (
            _hash_staged(state) if hash_inline else _hash_in_background(op.get("op_id") or "", state)
        )
        if hashed is None:
            raise OpInProgress("hashing the staged copy", retry_after=HASH_POLL_SECONDS)
        upload["blob"], upload["size_bytes"] = hashed
        save()
    completes = 0
    while True:
        if not state.get("upload_id"):
            try:
                created = _create(client, upload)
            except _Busy:
                if state.get("state") != "busy":
                    state["state"] = "busy"  # waiting: the one-at-a-time turn passes on
                    save()
                raise OpInProgress(
                    "another upload of these bytes is in progress",
                    retry_after=BUSY_RETRY_SECONDS,
                    wake_by=BUSY_MAX_WAIT_SECONDS,
                ) from None
            if created.get("have"):
                state["state"] = "have"
                state["artifact_id"] = created.get("artifact_id")
                release_staged(state)
                return created
            state.update(
                upload_id=created["upload_id"],
                artifact_id=created.get("artifact_id"),
                part_size=created["part_size"],
                part_count=created["part_count"],
                state=created.get("state") or "uploading",
            )
            save()
        status = client.transport.get(
            f"/v1/runs/{upload['anchor_id']}/artifacts/multipart/{state['upload_id']}"
        ) or {}
        current = status.get("state")
        if current != state.get("state"):
            state["state"] = current
            save()
        if current == "verified":
            release_staged(state)
            return status
        if current in ("failed", "aborted"):
            reason = status.get("failure_reason")
            restarts = int(state.get("restarts") or 0)
            if reason in _RESTARTABLE and restarts < _MAX_RESTARTS:
                # The server gave up on an upload this machine was away from
                # (offline past its 24 h idle abort, say). The staged bytes are
                # still here and still right: start a new upload with them.
                _check_staged(state)
                state.update(
                    upload_id=None,
                    part_size=None,
                    part_count=None,
                    state="staged",
                    restarts=restarts + 1,
                )
                save()
                continue
            raise errors.ValidationError(
                f"the server {current} this upload ({reason or 'no reason'})", status=422
            )
        if current == "verifying":
            if not wait_for_verify:
                release_staged(state)
                return status
            raise OpInProgress("the server is verifying the upload", retry_after=VERIFY_POLL_SECONDS)
        if current != "uploading":
            raise errors.ValidationError(f"unknown multipart state {current!r}", status=422)
        todo = sorted(
            set(status.get("missing_parts") or ()) | set(status.get("wrong_size_parts") or ())
        )
        if not todo:
            _check_staged(state)
            if completes >= 2:
                # The listing says every part is there and complete keeps
                # disagreeing: let the lane back off rather than spin.
                raise errors.ServerError("multipart complete keeps refusing", status=503)
            completes += 1
            try:
                client.transport.post(
                    f"/v1/runs/{upload['anchor_id']}/artifacts/multipart/{state['upload_id']}/complete",
                    idempotent=True,
                )
            except errors.ConflictError as exc:
                detail = exc.detail if isinstance(exc.detail, dict) else {}
                if detail.get("state") != "uploading":
                    raise
            continue
        if time.monotonic() >= deadline:
            raise OpInProgress(f"{len(todo)} part(s) of this artifact still to send")
        _check_staged(state)
        _send_parts(client, upload, state, todo, deadline, save)
        _check_staged(state)


def execute_op(journal: Any, client: Any, op_path: Path, op: dict) -> dict | None:
    """The drain's hook (`journal._execute`): one slice of work. An op a
    closing `finish()` is seeing through (``until: verifying``) is done once
    the server has every byte."""

    def save() -> None:
        write_text_atomic(op_path, json.dumps(op, indent=2) + "\n", mode=0o600)

    until = (op.get("multipart") or {}).get("until")
    return advance(
        client,
        op,
        save,
        deadline=time.monotonic() + SLICE_SECONDS,
        wait_for_verify=until != "verifying",
        hash_inline=False,
    )


def settle_reason(client: Any) -> str | None:
    """Why nothing on this machine would finish this client's uploads after
    the process exits, or None when a detached worker on durable storage will."""
    if not getattr(client, "_auto_drain", False):
        return "this process sends its own writes, and nothing sends them after it exits"
    try:
        from . import ephemeral

        where = ephemeral.describe(str(client.journal.dir))
    except Exception:  # noqa: BLE001 -- unknown: trust the worker
        return None
    if not where.get("durable", True):
        return f"the outbox is on {where.get('reason') or 'a disposable disk'} and goes with this machine"
    return None


def settle_for_close(client: Any, op_ids: list[str], deadline: float, *, why: str) -> int:
    """See this run's multipart uploads through before its process exits --
    the case `settle_reason` names. Each is done once the server has every
    byte (its verifier needs nothing more from here). Whatever is not done by
    ``deadline`` is recorded as a reference row now, its server upload
    aborted and its staged copy deleted. Returns how many were recorded."""
    from . import journal as journal_module

    journal = client.journal
    wanted = set(op_ids)
    for path, op in pending(journal):
        if op.get("op_id") in wanted and (op.get("multipart") or {}).get("until") != "verifying":
            op["multipart"]["until"] = "verifying"
            write_text_atomic(path, json.dumps(op, indent=2) + "\n", mode=0o600)
    factory = client._outbox_client_factory()
    # Kept back for recording what does not make it: those requests run after
    # the uploads have had their time, under the same close budget.
    stop_at = deadline - min(10.0, 0.25 * max(0.0, deadline - time.monotonic()))
    while time.monotonic() < stop_at and still_uploading(journal, list(wanted)):
        report = journal_module.drain(
            journal,
            only_ops=wanted,
            client_factory=factory,
            lock_timeout=max(0.0, stop_at - time.monotonic()),
        )
        if not (report.delivered or report.dead_lettered or report.in_progress):
            waits = [s.retry_after or 1.0 for s in report.stalled_runs.values()] or [1.0]
            time.sleep(max(0.0, min(min(waits), stop_at - time.monotonic())))
    left = [(p, o) for p, o in pending(journal) if o.get("op_id") in wanted]
    for path, op in left:
        op["last_error"] = f"the run closed before this upload finished: {why}"
        recorded = False
        try:
            recorded = journal_module._record_upload_fallback(journal, client, op)
        except Exception:  # noqa: BLE001 -- best-effort, like the dead-letter fallback
            recorded = False
        shaped = None if recorded else journal_module._upload_fallback_request(op)
        if shaped is not None:
            # Not delivered now: queued in the run's own lane like any write,
            # so the deferred close (or the next process) carries it.
            try:
                journal.append_http("POST", shaped[0], shaped[1], run_ref=op.get("run_ref"))
            except Exception:  # noqa: BLE001 -- nothing more to try
                pass
        on_dead_letter(journal, lambda *_a: client, op)
        target = _private(failed_dir(journal)) / path.name
        op["blocking"] = False
        write_text_atomic(path, json.dumps(op, indent=2) + "\n", mode=0o600)
        os.replace(path, target)
    return len(left)


def upload_now(
    client: Any,
    *,
    run_id: str,
    name: str,
    src: str,
    kind: str | None,
    content_type: str | None,
    meta: dict | None,
    notes: str | None,
    span_id: str | None,
    step_index: int | None,
) -> dict:
    """The synchronous door (``sync=True``, ``strict``, a fail-closed client,
    or one with no queue): hash, send every part, complete, and return once
    the server is verifying (it has every byte). Blocks the caller for the
    whole transfer, which is what those callers asked for.

    Reads the caller's file where it is, not a staged copy: the caller is
    blocked on this call, and the identity check (same inode, size and mtime
    around every step) refuses the upload if another thread rotates or
    rewrites it meanwhile."""
    st = os.stat(src)
    op = {
        "op_id": "sync",
        "multipart": {
            "staged_path": os.path.abspath(src),
            "stage_mode": "none",
            "identity": _identity(st),
            "staged_at": time.time(),
            "upload_id": None,
            "state": "staged",
        },
        "upload": {
            "anchor": "run",
            "anchor_id": run_id,
            "name": name,
            "src_path": os.path.abspath(src),
            "blob": None,
            "size_bytes": st.st_size,
            "content_type": content_type,
            "kind": kind,
            "meta": meta,
            "notes": notes,
            "span_id": span_id,
            "step_index": step_index,
        },
    }
    waited = 0.0
    try:
        while True:
            try:
                return advance(
                    client, op, lambda: None, deadline=float("inf"), wait_for_verify=False
                ) or {}
            except OpInProgress as waiting:
                # Only "another upload of these bytes is in progress" gets here
                # (the deadline is unbounded and verification is not awaited).
                pause = waiting.retry_after or 0
                if waited + pause > _SYNC_BUSY_WAIT_SECONDS:
                    raise errors.ConflictError(
                        "another upload of these bytes is still in progress in this team"
                    ) from None
                time.sleep(pause)
                waited += pause
    except BaseException:
        on_dead_letter(None, lambda _context: client, op)
        raise
