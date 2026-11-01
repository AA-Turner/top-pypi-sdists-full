"""an offline run's queue on disk: manifest, local-to-server id mapping, find, describe and amend it."""

from __future__ import annotations
import json
import os
from pathlib import Path
from typing import Any

from ... import errors
from ....foundation.durable.durable import now_iso, write_text_atomic
from ..journal.journal import Journal
from ..journal.paths import default_root

OFFLINE_DIRNAME = "offline"
MAPPING_NAME = "local_runs.json"
#: `on_conflict` values an offline run can honour at sync.
_OFFLINE_CONFLICT = ("error", "supersede")


# -- syncing ------------------------------------------------------------------
def read_manifest(directory: str | os.PathLike) -> dict | None:
    try:
        data = json.loads((Path(directory) / MANIFEST_NAME).read_text())
    except (OSError, ValueError):
        return None
    return data if isinstance(data, dict) and data.get("schema") == MANIFEST_SCHEMA else None


def read_mapping(directory: str | os.PathLike) -> dict:
    try:
        data = json.loads((Path(directory) / MAPPING_NAME).read_text())
    except (OSError, ValueError):
        return {}
    return data if isinstance(data, dict) else {}


def _write_mapping(directory: Path, key: str, run_id: str, **extra: Any) -> None:
    """Atomic: a crash leaves the old mapping or the new one, never half."""
    mapping = read_mapping(directory)
    mapping[key] = {"id": str(run_id), "synced_at": now_iso(), **extra}
    write_text_atomic(directory / MAPPING_NAME, json.dumps(mapping, indent=2) + "\n", mode=0o600)


def search_places(root: str | os.PathLike | None = None) -> list[Path]:
    """Where :func:`find_offline_dirs` looks under ``root``, for messages."""
    base = Path(root).expanduser() if root is not None else default_root()
    return [base / OFFLINE_DIRNAME, base / "rank-*" / OFFLINE_DIRNAME, base]


def find_offline_dirs(root: str | os.PathLike | None = None) -> list[Path]:
    """Offline run directories under ``root``: one run's dir, a folder of them, or an outbox
    (its ``offline/`` and every rank's ``rank-*/offline/``: a torchrun/SLURM rank's own
    outbox, or a queue recorded by an SDK that put offline runs there). Default: this
    machine's outbox root."""
    base = Path(root).expanduser() if root is not None else default_root()
    if read_manifest(base) is not None:
        return [base]
    parents = [base / OFFLINE_DIRNAME, *sorted(base.glob(f"rank-*/{OFFLINE_DIRNAME}")), base]
    found: list[Path] = []
    for parent in parents:
        if not parent.is_dir():
            continue
        for child in sorted(parent.iterdir()):
            if child.is_dir() and child not in found and read_manifest(child) is not None:
                found.append(child)
    return found


def describe(directory: Path) -> dict:
    """One offline run's state, for `probe sync --list` (no network)."""
    manifest = read_manifest(directory) or {}
    journal = Journal(directory)
    pending = len(journal.pending()) + len(journal.waiting())
    failed = len(journal.failed())
    mapped = read_mapping(directory).get(str(manifest.get("creation_key")))
    state = "synced" if mapped and not pending and not failed else "unsynced"
    if mapped and (pending or failed):
        state = "partial"
    return {
        "key": manifest.get("creation_key"),
        "dir": str(directory),
        "state": state,
        "run_id": (mapped or {}).get("id"),
        "name": manifest.get("name"),
        "project": manifest.get("project"),
        "experiment": manifest.get("experiment"),
        "recorded_at": manifest.get("recorded_at"),
        "customer_id": manifest.get("customer_id"),
        "pending": pending,
        "failed": failed,
        # Writes refused while recording (disk floor): not in the queue, so no
        # sync delivers them (`OfflineRun.finish`).
        "dropped_writes": int(manifest.get("dropped_writes") or 0),
    }


def _create_ops(journal: Journal) -> list[tuple[Path, dict]]:
    return [
        (p, op)
        for p, op in [*journal.pending(), *journal.failed()]
        if op.get("kind") == CREATE_KIND
    ]


def amend(
    directory: Path,
    *,
    project: str | None = None,
    experiment: str | None = None,
    on_conflict: str | None = None,
    only_refused: bool = False,
) -> int:
    """`probe sync --project/--experiment/--on-conflict`: change how a still undelivered
    create is filed (somewhere that exists, or as a retry -- ``supersede`` -- of the run
    holding its ``external_id``) and put a refused one back in the queue. ``only_refused``:
    leave a create not refused alone (the flags fix what failed, not every run a folder scan
    found). Returns how many create ops changed.

    A create the fallback kept a SENT request for is re-filed too: the offline create goes to
    the new home, and the kept request is still replayed as sent (original home) if the
    server says its key already made a run."""
    if on_conflict is not None and on_conflict not in _OFFLINE_CONFLICT:
        raise errors.ValidationError(
            f"--on-conflict {on_conflict!r}: an offline run can only be delivered with "
            f"{' or '.join(_OFFLINE_CONFLICT)}"
        )
    journal = Journal(directory)
    changed = 0
    for path, op in _create_ops(journal):
        refused = path.parent == journal.failed_dir
        if only_refused and not refused:
            continue
        create = op.get("create") or {}
        if project is not None:
            create.pop("path", None)  # re-resolved from the slugs at sync
            create["project"] = project
            if experiment is None:
                create.pop("experiment", None)
                create.pop("question", None)
                create.pop("experiment_name", None)
                (create.get("body") or {}).pop("group_id", None)
        if experiment is not None:
            create.pop("path", None)
            create["experiment"] = experiment
        if on_conflict is not None:
            create["on_conflict"] = on_conflict
        op["create"] = create
        op["attempts"] = 0
        op["last_error"] = None
        write_text_atomic(path, json.dumps(op, indent=2) + "\n", mode=0o600)
        if refused:
            journal.retry_failed(op.get("op_id"))
        changed += 1
    return changed
from probe.sdk.delivery.offline.offline import CREATE_KIND, MANIFEST_NAME, MANIFEST_SCHEMA  # noqa: E402 -- pieces need each other; the front door loads this one first
