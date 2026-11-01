"""the op record: schema, op kinds, namespaces, and what an op says about itself (run lane, attempts, day, pinned server)."""

from __future__ import annotations
import importlib
import json
import re
import uuid
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from probe.sdk.delivery.journal.journal import Journal


SCHEMA = "probe.outbox/1"

#: Op kinds this release's drain delivers (plan 1.11). A worker advertises them in its
#: caps file (`outbox_worker`); an op of any OTHER kind (queued by a newer SDK sharing
#: this outbox) is held in its run's lane, never attempted or dead-lettered, until a
#: worker that knows it drains the queue. Older releases dead-lettered an unknown kind
#: as permanent, so a producer asks the live worker first (`outbox_worker.ready_for`).
#:
#: `create_run`: an OFFLINE run's create (plan 2.12), queued only in
#: `<outbox>/offline/<key>/`, which only `probe sync` drains, so no older worker meets
#: it and no `ready_for` handshake is needed; this drain must still list it or it holds the create
#: and every write of the run behind it forever.
#:
#: `multipart_upload`: an artifact over 64 MiB (plan item (g),
#: `sdk/artifact/storage_handlers/multipart/multipart.py`), staged then sent in parts
#: to object storage, in its own lane (`op["lane"]`) so minutes of transfer never hold
#: the run's metrics. Queued in `<outbox>/multipart/ops/`, which no earlier release
#: reads (an older worker neither holds nor dead-letters it); the producer still asks
#: `outbox_worker.ready_for` so such a worker steps aside for a current one.
#:
#: `catalog_manifest`: a folder dataset's manifest (data catalog, Q9), gzip JSON sent as
#: raw bytes, so it cannot ride `http`'s JSON body. Bytes wait in
#: `<outbox>/catalog/<op_id>.json.gz`; the op names them and rides the no-run lane AHEAD
#: of the registration that needs it. An older 1.11+ worker holds it (unknown kind).
CATALOG_MANIFEST = "catalog_manifest"
OP_KINDS = frozenset(
    {"http", "upload", "rejected_http", "create_run", "multipart_upload", CATALOG_MANIFEST}
)
DELIVERY_NAMESPACE = "delivery-v1"
#: Where a client that stamps its credential (#2035) queues, one directory per credential
#: fingerprint: `<outbox>/credential-v1/<fingerprint>/`. No earlier release looks here, so
#: none can send such a write with the wrong login or stop its pass on one (#2041 reviews).
#: Each credential has its own queue, lease and worker: a token nothing else holds never
#: waits behind another credential's busy worker.
CREDENTIAL_NAMESPACE = "credential-v1"
DELIVERY_SCHEMA = "probe.outbox.delivery/1"


_RUN_PATH = re.compile(r"^/v1/runs/([^/]+)(?:/|$)")

_SAFE_COMPONENT = re.compile(r"[^A-Za-z0-9._-]+")


def _safe_component(value: str) -> str:
    return _SAFE_COMPONENT.sub("_", value)[:120] or "producer"


def run_ref_for_path(path: str) -> str | None:
    """The run a v1 path addresses, when it addresses one. Barrier scoping key."""
    match = _RUN_PATH.match(path)
    return match.group(1) if match else None


def _is_uuid(ref: str) -> bool:
    try:
        uuid.UUID(ref)
    except (AttributeError, TypeError, ValueError):
        return False
    return True


def _meta_of(op: dict) -> tuple[int, str | None]:
    """What a status recount needs from one op: (size_bytes, enqueued_at)."""
    return int((op.get("upload") or {}).get("size_bytes") or 0), op.get("enqueued_at")


def op_meta(ops: list[tuple[Path, dict]]) -> dict[str, tuple[int, str | None]]:
    """name -> (size_bytes, enqueued_at) for ops already parsed, so a status
    recount under the append lock need not parse them again."""
    out: dict[str, tuple[int, str | None]] = {}
    for path, op in ops:
        try:
            out[path.name] = _meta_of(op)
        except AttributeError:  # not an object: let the recount skip it
            out[path.name] = (0, None)
    return out


_DAY = re.compile(r"\d{4}-\d{2}-\d{2}")


def op_day(op: Any) -> str | None:
    """The UTC day ``op`` was queued (`enqueued_at`, unlike its file's mtime a retry does
    not rewrite it), as YYYY-MM-DD, or None."""
    at = op.get("enqueued_at") if isinstance(op, dict) else None
    return at[:10] if isinstance(at, str) and _DAY.fullmatch(at[:10]) else None


def op_base_url(op: Any) -> str | None:
    """The server ``op`` is pinned to, or None (no pin, or not an op)."""
    context = op.get("context") if isinstance(op, dict) else None
    pinned = context.get("base_url") if isinstance(context, dict) else None
    return str(pinned).rstrip("/") if isinstance(pinned, str) and pinned else None


def _read_op_file(path: Path) -> Any:
    try:
        return json.loads(path.read_text())
    except (OSError, ValueError):
        return None


def queued_ops(queue: "Journal") -> list[tuple[Path, dict]]:
    """``queue``'s pending ops, multipart uploads (``multipart/ops/``) included."""
    return queue.pending() + queue._read_dir(queue.dir / "multipart" / "ops")


def is_ingest_path(path: str | None) -> bool:
    """Whether a request goes out with the INGEST token (`Transport._auth_headers`)."""
    return bool(path) and str(path).startswith("/ingest")

_RUN_CLOSE_PATH = re.compile(r"/v1/runs/[^/]+")
_RUN_RELEASE_PATH = re.compile(r"/v1/runs/[^/]+/writers/[^/]+/release")
_TERMINAL_RUN_STATUSES = frozenset({"completed", "failed", "crashed", "canceled", "untracked"})


def _is_run_close(op: dict) -> bool:
    """Whether ``op`` closes its run: a terminal status write (`Run.set_status`,
    `Run._queue_deferred_finish`, `probe run end --async`) or, on a `leases` run (2.8), a
    writer's lease release, from which the server closes the run (#2041 round 6: a release
    went out ahead of the run's writes queued under another credential; the run read
    completed without them)."""
    if op.get("kind") != "http":
        return False
    path = str(op.get("path") or "")
    if op.get("method") == "PATCH" and _RUN_CLOSE_PATH.fullmatch(path):
        return (op.get("body") or {}).get("status") in _TERMINAL_RUN_STATUSES
    return op.get("method") == "POST" and bool(_RUN_RELEASE_PATH.fullmatch(path))


def _write_epoch_of(op: dict) -> int | None:
    """The write epoch an op carries (its body's ``write_epoch``), or None."""
    body = op.get("body") if isinstance(op, dict) else None
    value = body.get("write_epoch") if isinstance(body, dict) else None
    try:
        return int(value) if value is not None else None
    except (TypeError, ValueError):
        return None


#: Key a takeover barrier (`Client._hold_status_writes`) stamps on a status op it set
#: aside in `failed/`: `{pid, host, until, last_error, blocking}`.
TAKEOVER_HOLD_KEY = "takeover_hold"


def _attempts(op: dict) -> int:
    """An op's attempt count; a non-number (hand-edited, corrupt) reads 0 instead of
    raising out of `drain()` for the whole machine (review of #2053)."""
    value = op.get("attempts")
    if isinstance(value, bool):
        return 0
    try:
        return max(0, int(value or 0))
    except (TypeError, ValueError, OverflowError):
        return 0


def _lane_of(op: Any) -> Any:
    """An op's lane: its ``run_ref`` when a string (or None). Anything else (list, dict)
    is unhashable or not a run and gets a lane of its own, not a TypeError out of
    `drain()` (review of #2053).

    An op naming its own string ``lane`` rides that: a multipart upload (plan item (g))
    moves gigabytes over many passes, must never stand before the run's metrics, and
    nothing of the run is ordered after it (its artifact row is its own)."""
    if isinstance(op, dict) and isinstance(op.get("lane"), str) and op["lane"]:
        return op["lane"]
    ref = op.get("run_ref") if isinstance(op, dict) else None
    return ref if ref is None or isinstance(ref, str) else "<invalid run_ref>"


def _is_multipart(op: Any) -> bool:
    return isinstance(op, dict) and op.get("kind") == "multipart_upload"


def _queued_at(op: dict) -> str:
    """When ``op``'s work happened: a daemon command's `event_at`, else when it
    was queued (ISO 8601; '' for neither)."""
    return str(op.get("event_at") or op.get("enqueued_at") or "")


def _queued_bucket(op: dict) -> int | None:
    """The 5-minute effort bucket of `_queued_at` (the server's), or None."""
    from datetime import datetime

    try:
        return int(datetime.fromisoformat(_queued_at(op)).timestamp() // 300)
    except (ValueError, OverflowError, OSError):
        return None


#: The project segment of an experiment child path journaled before its project is known:
#: `/v1/projects/~/experiments/{E}/...` (light experiments X21). Children are addressed
#: under the project the experiment is filed in, which a move changes; the queue names the
#: experiment alone and the drain asks where it is (`_placed`). `~` cannot be a project
#: slug or id, so a drainer older than this sends it to a 404 and dead-letters it.
UNPLACED_PROJECT = "~"
_UUID_SEGMENT = r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}"
_PLACED_EXPERIMENT_PATH = re.compile(
    rf"/v1/projects/{_UUID_SEGMENT}/experiments/({_UUID_SEGMENT})((?:/[^?#]*)?)"
)
_UNPLACED_EXPERIMENT_PATH = re.compile(r"/v1/projects/~/experiments/([^/?#]+)((?:/[^?#]*)?)")


def unplaced_experiment_path(path: str) -> str:
    """``path`` with an experiment child route's project replaced by
    :data:`UNPLACED_PROJECT`; any other path unchanged."""
    match = _PLACED_EXPERIMENT_PATH.fullmatch(path or "")
    if match is None:
        return path
    return f"/v1/projects/{UNPLACED_PROJECT}/experiments/{match.group(1)}{match.group(2)}"

#: The client an op is delivered with, by name: the drain builds one per credential, the
#: dead-letter checks one to ask the server. Loaded on build so delivery never imports
#: the client above it.
DELIVERY_CLIENT = "probe.sdk.client.client:Client"


def delivery_client() -> Any:
    """The class `DELIVERY_CLIENT` names, looked up on every call (a patch on it is seen)."""
    module, _, name = DELIVERY_CLIENT.partition(":")
    return getattr(importlib.import_module(module), name)
