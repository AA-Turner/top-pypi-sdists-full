"""Artifacts over 64 MiB: staged within the outbox's disk budget, then uploaded in parts straight
to object storage (plan item (g)); rationale, callers and failure handling in DESIGN.md."""

from __future__ import annotations

import json
import os
import time
from typing import Any, Callable

from .... import errors
from ...anchors import Anchor
from .....foundation.durable.durable import write_text_atomic
from ....delivery.outbox.drain.report import OpInProgress
from probe.sdk.artifact.storage_handlers.multipart.doors import _Busy, _abort, _create, _fields, _finish, _status
from probe.sdk.artifact.storage_handlers.multipart import parts  # parts._send_parts: one binding for tests to patch
from probe.sdk.artifact.storage_handlers.multipart.parts import _hash_in_background, _hash_staged
from probe.sdk.artifact.storage_handlers.multipart.queue import failed_dir, pending, still_uploading
from probe.sdk.artifact.storage_handlers.multipart.staging import _check_staged, _identity, _private, release_staged
#: Server feature: multipart uploads.
FEATURE = "artifact_multipart"
#: Server feature: multipart at a project, experiment, workspace or Shared too.
ANCHORED_FEATURE = "artifact_multipart_anchored"
#: A staged copy is deleted this long after it was made.
STAGED_TTL_SECONDS = 7 * 86_400
#: Wait between polls while the server verifies (the lane's backoff grows from here).
VERIFY_POLL_SECONDS = 5.0
#: Wait while another upload of the same bytes is active in the team; it becomes a HAVE once done.
BUSY_RETRY_SECONDS = 30.0
#: Longest wait between tries meanwhile, however far backoff has grown: the server
#: hands the bytes to the next create once the other upload is idle 10 min, and a
#: 300 s backoff would take that up minutes late.
BUSY_MAX_WAIT_SECONDS = 60.0
#: Wait between looks at the background hash.
HASH_POLL_SECONDS = 2.0
#: Server-side endings after which the upload restarts from the staged copy (bytes
#: never judged wrong), at most `_MAX_RESTARTS` times: this machine was away longer
#: than the server keeps an idle upload.
_RESTARTABLE = frozenset(
    {
        "idle",
        "expired",
        "store_upload_missing",
        "verification_timed_out",
        "verification_gave_up",
        # Another create of the same bytes took over this idle upload; restarting waits on it and becomes a HAVE.
        "superseded_idle",
    }
)
_MAX_RESTARTS = 3
#: How long a SYNCHRONOUS upload waits for another of the same bytes: past the
#: server's 10 min idle takeover, so a dead uploader's hold ends within it.
_SYNC_BUSY_WAIT_SECONDS = 720.0


def threshold_bytes() -> int:
    """Above this, ``log_artifact`` uploads in parts: the credential gate's 64 MiB whole-file limit, shared by the server relay."""
    from ....secret_gate import ScanPolicy

    return ScanPolicy().max_bytes


def over_threshold(path: str) -> bool:
    try:
        return os.path.getsize(path) > threshold_bytes()
    except OSError:
        return False


def on_dead_letter(journal: Any, client_for: Callable[[Any], Any], op: dict) -> None:
    """A multipart op that will never finish: abort the server's upload (parts go now,
    not at its 24 h sweep) and delete the staged copy. Best-effort; never raises."""
    state = op.get("multipart") or {}
    upload = op.get("upload") or {}
    if state.get("upload_id") and state.get("state") not in ("verified", "have"):
        try:
            _abort(client_for(op.get("context")), upload, state["upload_id"])
        except Exception:  # noqa: BLE001 -- the server sweeps an idle upload anyway
            pass
    release_staged(state)


def advance(
    client: Any,
    op: dict,
    save: Callable[[], None],
    *,
    deadline: float,
    wait_for_verify: bool = True,
    hash_inline: bool = True,
) -> dict | None:
    """Move one upload as far as ``deadline`` allows. Returns the server's answer when
    done (verified, a HAVE, or with ``wait_for_verify=False`` verifying: the server has
    every byte); raises `OpInProgress` when more remains (``retry_after`` None: parts
    went, next pass; a number: waiting on the hash, the verifier, or another upload of
    the same bytes), a permanent error when it can never finish.
    ``hash_inline=False`` hashes on a background thread."""
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
                    state["state"] = "busy"  # the one-at-a-time turn passes on
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
        status = _status(client, upload, state["upload_id"]) or {}
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
                # The server gave up while this machine was away (e.g. past its 24 h idle
                # abort); the staged bytes are still right: start anew.
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
                # Every part listed yet complete keeps refusing: back off, don't spin.
                raise errors.ServerError("multipart complete keeps refusing", status=503)
            completes += 1
            try:
                _finish(client, upload, state["upload_id"])
            except errors.ConflictError as exc:
                detail = exc.detail if isinstance(exc.detail, dict) else {}
                if detail.get("state") != "uploading":
                    raise
            continue
        if time.monotonic() >= deadline:
            raise OpInProgress(f"{len(todo)} part(s) of this artifact still to send")
        _check_staged(state)
        parts._send_parts(client, upload, state, todo, deadline, save)
        _check_staged(state)


def settle_reason(client: Any) -> str | None:
    """Why nothing would finish this client's uploads after exit, or None if a detached worker on durable storage will."""
    if not getattr(client, "_auto_drain", False):
        return "this process sends its own writes, and nothing sends them after it exits"
    try:
        from ....run.launch import ephemeral

        where = ephemeral.describe(str(client.journal.dir))
    except Exception:  # noqa: BLE001 -- unknown: trust the worker
        return None
    if not where.get("durable", True):
        return f"the outbox is on {where.get('reason') or 'a disposable disk'} and goes with this machine"
    return None


def settle_for_close(client: Any, op_ids: list[str], deadline: float, *, why: str) -> int:
    """See this run's multipart uploads through before exit (the `settle_reason` case).
    Each is done once the server has every byte. Anything unfinished by ``deadline``
    becomes a reference row, its server upload aborted and staged copy deleted.
    Returns how many were recorded."""
    from ....delivery import journal as journal_module

    journal = client.journal
    wanted = set(op_ids)
    for path, op in pending(journal):
        if op.get("op_id") in wanted and (op.get("multipart") or {}).get("until") != "verifying":
            op["multipart"]["until"] = "verifying"
            write_text_atomic(path, json.dumps(op, indent=2) + "\n", mode=0o600)
    factory = client._outbox_client_factory()
    # Reserved for recording what fails: runs after the uploads, within the same close budget.
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
            # Queued in the run's lane like any write; the deferred close or next process carries it.
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
    run_id: str | None = None,
    name: str,
    src: str,
    kind: str | None,
    content_type: str | None,
    meta: dict | None,
    span_id: str | None,
    step_index: int | None,
    anchor: str = Anchor.RUN.value,
    anchor_id: str | None = None,
) -> dict:
    """The synchronous door (``sync=True``, ``strict``, a fail-closed or queue-less
    client; `probe artifact add --sync`): hash, send every part, complete, return once
    the server is verifying. Blocks for the whole transfer. ``anchor``/``anchor_id`` as in `build_op`.

    Reads the file in place, not a staged copy; the identity check (inode, size, mtime
    around every step) refuses the upload if another thread rewrites it."""
    anchor = Anchor(anchor).value
    if anchor == Anchor.RUN.value:
        anchor_id = run_id
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
            "anchor": anchor,
            "anchor_id": anchor_id,
            "name": name,
            "src_path": os.path.abspath(src),
            "blob": None,
            "size_bytes": st.st_size,
            "content_type": content_type,
            "kind": kind,
            "meta": meta,
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
                # Only "another upload of these bytes is in progress" gets here.
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
