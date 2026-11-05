"""OpHandler and the registry of what the drain calls above it by name; delivers one op under its writer's
attribution scope."""

from __future__ import annotations
import importlib
import json
import os
from contextlib import ExitStack, contextmanager
from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable, Protocol
from ... import errors
from ....foundation.durable.durable import (
    fsync_directory,
    write_text_atomic)
from ...artifact.hashing import fingerprint
# The drain reaches the upload handler's refusal fallback through this interface (a leaf).
from .op_handlers.upload import _record_upload_fallback  # noqa: F401
# At module load, not in the drain: a module first imported while a script exits clears
# its pending KeyboardInterrupt (tests/test_ctrlc_exit_code.py).
from ...values import unstorable

if TYPE_CHECKING:
    from probe.sdk.delivery.journal.journal import Journal


class OpHandler(Protocol):
    """Delivers one queued op of its kind (create_run, multipart_upload); raises the transport or
    client error when it fails."""

    def __call__(self, journal: Journal, client: Any, *args: Any) -> dict | None: ...


#: What the drain calls whose code lives above it, "module:function": two op kinds'
#: handlers (an offline run's create, a multipart upload's slice) and the offline
#: create's two hooks (bind local ids -> None; hold lineage until the run exists -> bool).
#: Looked up per call so the drain never imports them.
OP_HANDLERS = {
    "create_run": "probe.sdk.delivery.ops.op_handlers.create_run:deliver_create",
    "local_run_refs": "probe.sdk.delivery.ops.op_handlers.create_run:bind_local_refs",
    "lineage_gate": "probe.sdk.delivery.offline.lineage:lineage_gate",
    "multipart_upload": "probe.sdk.delivery.ops.op_handlers.multipart_upload:execute_op",
}
#: The storage handler multipart_upload ops stage through: the drain gcs its staging,
#: lists its queue and aborts a dead-lettered upload with it.
MULTIPART_STORAGE = "probe.sdk.artifact.storage_handlers.multipart"


def op_handler(name: str) -> Callable[..., Any]:
    """What `OP_HANDLERS` names (an `OpHandler` for an op kind), looked up on every call (a patch on it is seen)."""
    module, _, attribute = OP_HANDLERS[name].partition(":")
    return getattr(importlib.import_module(module), attribute)


def multipart_storage(piece: str = "") -> Any:
    """The multipart storage handler's front door, or one of its pieces."""
    return importlib.import_module(f"{MULTIPART_STORAGE}.{piece}" if piece else MULTIPART_STORAGE)


@contextmanager
def _delivery_scope(op: dict):
    """Deliver ``op`` as its writer queued it: under its persisted attribution, as the
    agent session that queued it, dated when its work happened
    (`agent_session.EVENT_AT_HEADER`, swarm friction R2), so a write the backlog held an
    hour counts that session's effort when it happened, whichever process drains it. An
    op from an older SDK names no session: sent as before (drainer's session, at
    arrival). A run process's op goes as the run's (`X-Probe-Write-Origin`, R41); every
    other op, an older SDK's included, with no origin."""
    from ..transport.headers import attribution_scope, event_at_scope, queued_origin_scope, queued_session_scope

    with ExitStack() as scope:
        scope.enter_context(attribution_scope(op.get("attribution", "ambient")))
        scope.enter_context(queued_origin_scope(op.get("write_origin")))
        if "agent_session" in op:
            scope.enter_context(queued_session_scope(op["agent_session"]))
            scope.enter_context(event_at_scope(_queued_at(op) or None))
        yield


def _execute(
    journal: Journal,
    client,
    op_path: Path,
    op: dict,
    run_ids: dict[str, str] | None = None,
    *,
    direct: bool = False,
) -> dict | None:
    """Deliver one op; raises the transport/client error on failure. Field guards raise
    ValidationError (permanent -> dead letter): a KeyError would classify transient and
    wedge the FIFO on a malformed op forever."""
    _refuse_unsafe_body(op)
    run_ids = {} if run_ids is None else run_ids
    if op.get("kind") == "create_run":
        # An OFFLINE run's create (plan 2.12). Only `probe sync` drains the queues that
        # carry this kind (`<outbox>/offline/<key>/`); no older worker meets it.
        return op_handler("create_run")(journal, client, op)
    if str(op.get("run_ref") or "").startswith("local:"):
        # ...and every later op of that run: `local:<key>` becomes the create's id.
        # Raises OfflineRunNotCreated while it has none.
        op_handler("local_run_refs")(journal, op)
        if op_handler("lineage_gate")(journal, client, op):
            # A read/write list this server does not take (`run_inputs`/`run_outputs`):
            # dropped as delivered, never sent to 404.
            return {"dropped": "lineage feature not declared"}
    if op.get("kind") == "http":
        return _send_http(client, op, run_ids)
    if op.get("kind") == "multipart_upload":
        # Plan (g): an artifact over 64 MiB, one slice per visit (see
        # `sdk/artifact/storage_handlers/multipart/multipart.py`); raises OpInProgress until done.
        return op_handler("multipart_upload")(journal, client, op_path, op)
    if op.get("kind") == CATALOG_MANIFEST:
        # A folder dataset's manifest, ahead of its registration (Q9).
        return _send_catalog_manifest(journal, client, op)
    if op.get("kind") != "upload":
        raise errors.ValidationError(
            f"unknown journal op kind {op.get('kind')!r}", status=422
        )
    return _send_upload(journal, client, op_path, op, run_ids, direct=direct)


def _refuse_unsafe_body(op: dict) -> None:
    """Raise ValidationError (and mark the op `rejected_http`) for a body that cannot be sent."""
    try:
        # Body depth uses the same origin as enqueue/transport validation.
        for value in op.values():
            unstorable.has_nul(value)
    except errors.ValidationError:
        # A malformed legacy body cannot safely pass recursive scrubbing: retain the
        # delivery identity and the refusal, never persist raw secrets because validation
        # failed. Mark the omitted payload explicitly.
        retained = {}
        for key in ("schema", "op_id", "run_ref", "blocking", "correlation", "attempts"):
            value = op.get(key)
            if value is None or isinstance(value, (str, bool, int, float)):
                # scanning disabled: retained[key] = default_scrub(value, key=key)
                retained[key] = value
        retained.update(
            kind="rejected_http",
            validation_error="Queued payload exceeded structural validation limits",
            body={"probe.rejected_payload": "omitted: unsafe JSON structure"},
        )
        op.clear()
        op.update(retained)
        raise errors.ValidationError("Queued payload exceeded structural validation limits", status=422)
    if op.get("kind") == "http":
        # Preserve refusal through scrub and retries, including older drainers.
        try:
            unstorable.validate_nuls(
                op.get("body"), path=op.get("path", ""), method=op.get("method", "")
            )
        except errors.ValidationError:
            op["kind"] = "rejected_http"
            op["validation_error"] = "Queued HTTP payload failed local NUL validation"
    # scanning disabled: op.update(scrub_op(op))
    if op.get("kind") == "rejected_http":
        raise errors.ValidationError("Queued HTTP payload failed local NUL validation", status=422)


def _send_http(client, op: dict, run_ids: dict[str, str]) -> dict | None:
    """An http op: placed under its experiment when it is one's child write, else sent as queued
    (once more with its run's uuid when the server refused a queued petname)."""
    if not op.get("method") or not op.get("path"):
        raise errors.ValidationError(
            f"op {op.get('op_id')} is missing method/path", status=422
        )
    placed = _placed(client, op)
    if placed is not None:
        return placed["response"]
    # A queued metrics POST may be acked once durable in the server's queue (I15d).
    is_metrics = routes.classify(op["method"], op["path"]).op is routes.WriteOp.METRICS
    ack = build_async_ack_kwargs(client) if is_metrics and op["method"].upper() == "POST" else {}
    try:
        return client.transport.request(op["method"], op["path"], json_body=op.get("body"), **ack)
    except errors.ValidationError:
        resolved = _resolve_queued_run_ref(client, routes.run_ref_of(op["path"]), run_ids)
        if resolved is None:
            raise
        # Rewritten for THIS attempt only; the op file keeps the queued ref. Persisting
        # it would rewrite history, and `run_ref` is the barrier-drain scoping key: a
        # queued petname must keep matching the barrier armed on the same petname.
        return client.transport.request(
            op["method"],
            op["path"].replace(resolved[0], resolved[1], 1),
            json_body=op.get("body"),
            **ack,
        )


def _send_catalog_manifest(journal: Journal, client, op: dict) -> None:
    """PUT a queued catalog manifest's gzip bytes, then drop them."""
    digest = op.get("digest")
    body_path = journal.catalog_manifest_path(str(op.get("op_id") or ""))
    try:
        gz = body_path.read_bytes()
    except OSError:
        raise errors.ValidationError(
            f"the queued manifest {digest} is gone from {body_path}", status=422
        ) from None
    client.put_manifest(str(digest), gz)
    body_path.unlink(missing_ok=True)
    return None


def _send_upload(
    journal: Journal, client, op_path: Path, op: dict, run_ids: dict[str, str], *, direct: bool
) -> dict:
    """A byte upload: find its bytes, hash them if enqueue did not, and upload them fingerprinted
    (once more with its run's uuid when the server refused a queued petname)."""
    upload = op.get("upload") or {}
    if not upload.get("anchor") or not upload.get("name") or not upload.get("src_path"):
        raise errors.ValidationError(
            f"upload op {op.get('op_id')} is missing anchor/name/src_path", status=422
        )
    source = _find_upload_source(journal, op, upload)
    digest = upload.get("blob")
    size = upload.get("size_bytes")
    if digest is None:
        digest, size, source = _hash_deferred_upload(journal, op_path, op, upload, source)

    def _upload(anchor_id: str | None) -> dict:
        return client.upload_fingerprinted(
            upload["anchor"],
            anchor_id,
            upload["name"],
            str(source),
            digest=digest,
            size=size,
            content_type=upload.get("content_type"),
            kind=upload.get("kind"),
            meta=upload.get("meta"),
            # An older client's op may carry `notes`: dropped, not sent (files carry no
            # notes now); the op replays as usual.
            span_id=upload.get("span_id"),
            step_index=upload.get("step_index"),
            **({"direct": True} if direct and upload["anchor"] == "run" else {}),
        )

    try:
        return _upload(upload["anchor_id"])
    except errors.ValidationError:
        # `artifact add --from-manifest` rows anchored on a petname reported
        # `anchors_resolved: 0` and `failed: 0`, then dead-lettered here. Same
        # 422-then-resolve retry as the http ops, for the RUN anchor only: project and
        # experiment slugs resolve at enqueue; workspace/shared anchors have ids only.
        resolved = (
            _resolve_queued_run_ref(client, upload["anchor_id"], run_ids)
            if upload["anchor"] == "run"
            else None
        )
        if resolved is None:
            raise
        return _upload(resolved[1])


def _find_upload_source(journal: Journal, op: dict, upload: dict) -> Path:
    """The upload's bytes: its staged blob (recovering an interrupted rename) or its source file;
    ValidationError naming which is gone."""
    from ..journal.uploads import is_drain_fenced, need_staged_bytes

    staged = journal.blob_path(op)
    if staged is None and is_drain_fenced():
        raise errors.ValidationError(
            f"op {op['op_id']} names its source file, and a fenced caller's drain sends only staged bytes",
            status=422)
    source = staged or Path(upload["src_path"])
    if not source.exists() and upload.get("staged"):
        # Recover an interrupted incoming-><digest> rename from a previous drain (red team):
        # the file may exist only under the incoming staging name (or vice versa).
        incoming = journal.blobs_dir / f"incoming-{op['op_id']}"
        if incoming.exists():
            if upload.get("blob"):
                os.replace(incoming, source)
                fsync_directory(journal.blobs_dir)
            else:
                source = incoming
    if not source.exists():
        # Two different failures, two fixes: a missing STAGED blob is the outbox losing
        # bytes it owned (gc, wiped state dir); a missing SOURCE is a file the producer
        # deleted, moved or unmounted before delivery, which the outbox never copied.
        # Saying "staged bytes are gone" for both sent people hunting the blob store.
        if upload.get("staged"):
            raise errors.ValidationError(
                f"staged bytes for op {op['op_id']} are gone ({source})", status=422
            )
        reason = upload.get("unstaged_reason")
        raise errors.ValidationError(
            f"source file for op {op['op_id']} is gone ({source}) and it was "
            "never staged into the outbox, so there are no bytes to fall back "
            "on -- "
            + (reason if reason else "the op was enqueued with stage=False"),
            status=422,
        )
    return need_staged_bytes(source)


def _hash_deferred_upload(
    journal: Journal, op_path: Path, op: dict, upload: dict, source: Path
) -> tuple[str, int, Path]:
    """11A: the big-file path hashed nothing at enqueue. Hash now, persist the digest, then move a
    staged blob to its content address; returns (digest, size, where the bytes are)."""
    digest, size = fingerprint(str(source))
    upload["blob"], upload["size_bytes"] = digest, size
    # Persist the digest BEFORE the rename (red team: the reverse left a crash window
    # where the op pointed at a vanished staging name and gc reaped the blob).
    write_text_atomic(op_path, json.dumps(op, indent=2) + "\n", mode=0o600)
    if upload.get("staged"):
        hashed = journal.blobs_dir / digest
        if hashed.exists():
            source.unlink(missing_ok=True)  # dedup: identical bytes already staged
        else:
            os.replace(source, hashed)
            fsync_directory(journal.blobs_dir)
        source = hashed
    return digest, size, source
from probe.sdk.delivery.ops.classify import _resolve_queued_run_ref  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.ops.op_handlers.http import _placed  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk import routes  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.ops.ingest_queue import build_async_ack_kwargs  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.ops.ops import CATALOG_MANIFEST, _queued_at  # noqa: E402 -- pieces need each other; the front door loads this one first
