"""send several uploads at once ahead of the serial pass: per-run and receipt windows, many-upload items."""

from __future__ import annotations
import json
import os
import re
import unicodedata
from concurrent.futures import ThreadPoolExecutor, as_completed
from contextvars import copy_context
from contextlib import nullcontext
from pathlib import Path
from typing import Any
# At module load, not in the drain: a module first imported while a script exits clears its
# pending KeyboardInterrupt (tests/test_ctrlc_exit_code.py).
from ....values import unstorable
from ....artifact.storage_handlers import r2 as upload_many


def _upload_workers() -> int:
    """How many upload bodies move at once. 1 restores the strictly serial drain."""
    raw = os.environ.get("PROBE_UPLOAD_WORKERS")
    if raw:
        try:
            return max(1, min(int(raw), 32))
        except ValueError:
            pass
    return 8
#: Many-file presign requests a window has in flight at once.
MANY_IN_FLIGHT = 4


def _prefetch_uploads(
    journal, entries, client_for, workers, run_ref, *, skips=None, already=frozenset(), away=None
) -> dict:
    """Do the NETWORK half of several upload operations at once.

    Every file is presign -> PUT -> confirm, three round trips, done one file after another by
    the drain: on a hundred thousand small files, hours of latency no bandwidth can fix.

    WHAT IS PARALLEL IS DELIBERATELY NARROW. Only uploads. In the backfill/receipt lane, ones
    carrying a correlation (content-addressed identity, server idempotent per correlation: order
    cannot matter). In a run's outbox, only uploads at the head of each run's queue
    (`_run_window`): an upload never moves past an op it could depend on. Plain HTTP operations
    keep strict FIFO, because their order IS their meaning.

    A run's small uploads go together (`upload_many`): one presign and one confirm request for
    the window, the PUTs in parallel. The rest, and every file of a server without those doors,
    go one op per worker.

    NOTHING IS DECIDED HERE. Workers return a result or raise. Saving the receipt, deleting the
    op file, classifying the failure, parking the queue, breaking on auth all still happen
    exactly once, in order, on the drain's own thread. A failed worker leaves its op for the
    serial pass.

    ``skips(path, op)`` names the ops the serial pass would not attempt now (a stalled or held
    run, a barrier's other ops); ``already`` the ops an earlier window delivered. ``away(lanes)``,
    when given, wraps the network half (`_DrainHold.away`: the drain lock let go, those runs'
    locks held) for a window of run uploads; one carrying a receipt correlation keeps the lock.
    """
    limit = workers * UPLOAD_WINDOW_FACTOR
    if journal.receipt_enabled:
        candidates = _receipt_window(journal, entries, client_for, limit, run_ref, already)
    else:
        candidates = _run_window(entries, client_for, limit, run_ref, skips, already)
    if len(candidates) < 2:
        return {}

    def run_one(item):
        path, op, client = item
        with _delivery_scope(op):
            # Its own run_ids map: petname resolution is a per-op cache and sharing a dict across
            # threads would race for no benefit. A window's run upload asks for a direct-to-storage
            # link (`upload_many.direct_wanted`); the serial pass never does.
            return _execute(journal, client, path, op, {}, direct=upload_many.direct_wanted(client))

    groups: dict[tuple, list] = {}
    alone = []
    for item in candidates:
        many = _many_item(journal, item[1], item[2])
        if many is None:
            alone.append(item)
        else:
            upload = item[1]["upload"]
            # One request carries one session, one date and one origin (`_delivery_scope`): ops of
            # other sessions, another 5-minute bucket, or a run's beside the agent's own, go apart.
            key = (
                id(item[2]),
                str(upload["anchor_id"]),
                item[1].get("attribution", "ambient"),
                item[1].get("agent_session", ""),
                _queued_bucket(item[1]),
                item[1].get("write_origin", ""),
            )
            groups.setdefault(key, []).append((item, many))
    for key in [k for k, members in groups.items() if len(members) < 2]:
        alone.extend(item for item, _ in groups.pop(key))

    done = {}
    if away is None or any(item[1].get("correlation") for item in candidates):
        away_from_lock = nullcontext()
    else:
        away_from_lock = away({_lane_of(item[1]) for item in candidates})
    try:
        with away_from_lock, ThreadPoolExecutor(max_workers=workers) as pool:
            _send_window(pool, alone, groups, workers, run_one, done)
    except RuntimeError:
        # "cannot schedule new futures after interpreter shutdown": the close a script's exit
        # runs. Nothing was sent; the serial pass sends it all.
        return {}
    return done


def _send_window(pool, alone, groups, workers, run_one, done) -> None:
    """`_prefetch_uploads`' network half on ``pool``: every lone op on a worker, each run's small
    uploads through `upload_many`; ``done`` gets path -> result for what landed."""
    futures = {
        pool.submit(copy_context().run, run_one, item): item[0] for item in alone
    }
    # A request presigns only what goes right after it (links are short-lived) and a window's
    # requests go at once: the server presigns a request's files one after another, so 32 files
    # as four requests of 8 in flight take a quarter of the time of two of 16 in turn (prod,
    # 2026-10-29).
    chunk_size = min(upload_many.MANY_MAX, max(2, workers))
    chunks = []
    for (_client, run_id, *_), members in groups.items():
        client = members[0][0][2]
        for start in range(0, len(members), chunk_size):
            chunks.append((client, run_id, members[start : start + chunk_size]))

    def send_chunk(chunk):
        client, run_id, members = chunk
        # One request for the chunk: its ops share a session and a bucket, so
        # it goes as the oldest of them.
        with _delivery_scope(min((item[1] for item, _ in members), key=_queued_at)):
            return upload_many.send(client, run_id, [many for _, many in members], pool)

    if chunks:
        # Its own threads: each waits on its files' checks and PUTs in `pool`, so running them
        # IN `pool` could leave every worker waiting on work queued behind it.
        with ThreadPoolExecutor(max_workers=min(len(chunks), MANY_IN_FLIGHT)) as senders:
            sent = list(senders.map(lambda c: copy_context().run(send_chunk, c), chunks))
        for (_client, _run, members), landed in zip(chunks, sent):
            if landed is None:
                # The server has no such doors: these go one op per worker.
                for item, _ in members:
                    futures[pool.submit(copy_context().run, run_one, item)] = item[0]
                continue
            for index, artifact in landed.items():
                done[members[index][0][0]] = artifact
    for future in as_completed(futures):
        try:
            done[futures[future]] = future.result()
        except Exception:  # noqa: BLE001 -- left for the serial pass
            pass


def _receipt_window(journal, entries, client_for, limit, run_ref, already) -> list:
    """The backfill/receipt lane's parallel window: uploads carrying a
    correlation and no receipt yet."""
    candidates = []
    for path, op in entries:
        if len(candidates) >= limit:
            break
        if path in already:
            continue
        if op.get("kind") != "upload" or not op.get("correlation"):
            continue
        if run_ref is not None and op.get("run_ref") != run_ref:
            continue
        if op.get("schema") != DELIVERY_SCHEMA:
            continue
        try:
            if journal.receipt(op["correlation"]) is not None:
                continue
            client = client_for(op.get("context"), op=op)
        except Exception:  # noqa: BLE001 -- the serial pass will report it
            continue
        candidates.append((path, op, client))
    return candidates


def _passes_uploads(op: dict) -> bool:
    """An op an upload may go ahead of: a metric write (no file depends on a metric point and
    no point on a file)."""
    return (
        op.get("kind") == "http"
        and op.get("method") == "POST"
        and not op.get("correlation")
        and _METRICS_ROUTE.fullmatch(op.get("path") or "") is not None
    )


def _run_window(entries, client_for, limit, run_ref, skips, already) -> list:
    """The uploads of a run's outbox that may move ahead of the serial pass. Per run, the
    uploads at the head of its queue, passing only metric writes (`_passes_uploads`), each file
    name once. Anything else ends that run's window: a span its upload cites, a reference row
    of the same name, another version of the same file, an op that failed before (it goes alone,
    its successors wait), an op the serial pass would not attempt now, the run's close. So an
    upload never lands before an op it could depend on and two versions of a file land in queue
    order."""
    candidates = []
    ended: set = set()
    names: dict = {}
    for path, op in entries:
        if len(candidates) >= limit:
            break
        if not isinstance(op, dict) or path in already:
            continue  # already landed: nothing behind it waits for it
        lane = _lane_of(op)
        if lane in ended:
            continue
        if op.get("kind") != "upload":
            if not _passes_uploads(op):
                ended.add(lane)
            continue
        upload = op.get("upload") if isinstance(op.get("upload"), dict) else {}
        # The anchor's KIND and the name as the server keys it (NFC), not its id: one run's file
        # can be queued under its uuid and its petname, or two encodings of one name; those must
        # not race.
        name = (upload.get("anchor"), unicodedata.normalize("NFC", str(upload.get("name") or "")))
        seen = names.setdefault(lane, set())
        if (
            name in seen
            or _attempts(op) > 0
            or str(op.get("run_ref") or "").startswith("local:")
            or (run_ref is not None and op.get("run_ref") != run_ref)
            or (skips is not None and skips(path, op))
        ):
            ended.add(lane)
            continue
        seen.add(name)
        try:
            client = client_for(op.get("context"), op_credential(op)[1], op=op)
        except Exception:  # noqa: BLE001 -- the serial pass will report it
            ended.add(lane)
            continue
        candidates.append((path, op, client))
    return candidates


def _many_item(journal, op: dict, client: Any):
    """``op`` as an `upload_many.Item` (a small, hashed upload to a run named by its id, on a
    server with the many-file doors) or None to send it alone. Its fields pass the same NUL
    check and scrub `_execute` applies first."""
    if not upload_many.enabled():
        return None
    upload = op.get("upload") if isinstance(op.get("upload"), dict) else {}
    digest, size = upload.get("blob"), upload.get("size_bytes")
    if (
        upload.get("anchor") != "run"
        or not _is_uuid(str(upload.get("anchor_id") or ""))
        or not upload.get("name")
        or not upload.get("src_path")
        or not isinstance(digest, str)
        or not isinstance(size, int)
        or size > upload_many.ITEM_MAX_BYTES
        or not upload_many.available(client)
    ):
        return None
    source = journal.blob_path(op) or Path(upload["src_path"])
    try:
        if not source.is_file():
            return None
        view = json.loads(json.dumps(op))
        for value in view.values():
            unstorable.has_nul(value)
        # scanning disabled: view.update(scrub_op(view))
        sent = view["upload"]
        # The per-row presign's `UploadRequest` body, built without importing the models: this
        # can run in a script's exit, where a first import clears a pending KeyboardInterrupt
        # (tests/test_ctrlc_exit_code.py).
        fields = {
            "name": sent["name"],
            "content_hash": digest,
            "size_bytes": size,
            "content_type": sent.get("content_type"),
            "span_id": sent.get("span_id"),
            "step_index": sent.get("step_index"),
            "kind": sent.get("kind"),
            "meta": sent.get("meta") or None,
        }
        body = {key: value for key, value in fields.items() if value is not None}
    except Exception:  # noqa: BLE001 -- alone, `_execute` meets it and decides
        return None
    return upload_many.Item(
        path=str(source),
        digest=digest,
        size=size,
        content_type=sent.get("content_type"),
        body=body,
    )
_METRICS_ROUTE = re.compile(r"/v1/runs/([^/?#]+)/metrics")
from probe.sdk.delivery.ops.op_handler import _delivery_scope, _execute  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.ops.ops import (  # noqa: E402 -- pieces need each other; the front door loads this one first
    DELIVERY_SCHEMA,
    _attempts,
    _is_uuid,
    _lane_of,
    _queued_at,
    _queued_bucket,
)
from probe.sdk.delivery.outbox.drain.credentials import op_credential  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.outbox.drain.drain import UPLOAD_WINDOW_FACTOR  # noqa: E402 -- pieces need each other; the front door loads this one first
