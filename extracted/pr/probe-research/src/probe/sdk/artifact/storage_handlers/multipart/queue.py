"""The multipart op and its own queue: build, enqueue, list pending or still uploading."""

from __future__ import annotations

import json
import os
import time
from pathlib import Path
from typing import Any
from ...anchors import Anchor
from .....foundation.durable.durable import write_text_atomic

#: The outbox op kind (registered in `journal.OP_KINDS`).
KIND = "multipart_upload"


def ops_dir(journal: Any) -> Path:
    """This kind's own queue: read by this release's drain, nothing older."""
    return Path(journal.dir) / "multipart" / "ops"


def failed_dir(journal: Any) -> Path:
    return Path(journal.dir) / "multipart" / "failed"


def build_op(
    journal: Any,
    *,
    run_id: str | None = None,
    name: str,
    src: str,
    kind: str | None,
    content_type: str | None,
    meta: dict | None,
    span_id: str | None,
    step_index: int | None,
    allow_copy: bool = True,
    anchor: str = Anchor.RUN.value,
    anchor_id: str | None = None,
) -> dict:
    """The queued op, staged. Its ``upload`` block has the shape readers of an upload
    op know (dead-letter reference row, output capture dedupe, `probe outbox
    status`); ``multipart`` is its own state.

    A run's op names ``run_id``; any other anchor passes ``anchor`` and
    ``anchor_id`` (None for Shared) and rides no run's lane (``run_ref`` None; every
    op here has its own lane). ``kind``/``meta``/``span_id``/``step_index`` are run-only."""
    from probe.sdk.artifact.storage_handlers.multipart.staging import stage  # call time: staging imports this module

    anchor = Anchor(anchor).value
    if anchor == Anchor.RUN.value:
        anchor_id = run_id
    if anchor != Anchor.SHARED.value and not anchor_id:
        raise ValueError(f"a {anchor} upload needs its {anchor}'s id")
    op = journal._base_op(KIND, anchor_id if anchor == Anchor.RUN.value else None)
    op["blocking"] = False
    op["lane"] = f"multipart:{op['op_id']}"
    op["multipart"] = {
        **stage(journal, src, op["op_id"], allow_copy=allow_copy),
        "upload_id": None,
        "artifact_id": None,
        "part_size": None,
        "part_count": None,
        "state": "staged",
    }
    op["upload"] = {
        "anchor": anchor,
        "anchor_id": anchor_id,
        "name": name,
        "src_path": os.path.abspath(src),
        # Not in the blob store: `journal.gc_blobs` must leave it.
        "staged": False,
        "blob": None,
        "size_bytes": op["multipart"]["identity"]["size"],
        "content_type": content_type,
        "kind": kind,
        "meta": meta,
        "span_id": span_id,
        "step_index": step_index,
    }
    return op


def enqueue(journal: Any, op: dict) -> Path:
    """Queue the op in this kind's own queue (`ops_dir`). Returns its path."""
    from ....delivery import outbox as outbox_worker
    from probe.sdk.artifact.storage_handlers.multipart.staging import _private  # call time: staging imports this module

    path = _private(ops_dir(journal)) / f"{time.time_ns():020d}-{op['op_id']}.json"
    write_text_atomic(path, json.dumps(op, indent=2) + "\n", mode=0o600)
    try:
        # An older worker never sees this op; this lets a current one take over sooner.
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
