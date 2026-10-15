"""A run's checkpoints: which one is ``best`` or ``latest``, whether its bytes
are stored, and getting them back (``Client.checkpoint``,
``Client.download_checkpoint``, ``probe artifact download --checkpoint``).

A checkpoint is one ``kind="checkpoint"`` row: a file the script logged, or the
index row the Hugging Face and Lightning integrations write per save. With
``checkpoints="upload"`` an index row lists the save's files in
``meta.members``, sets ``meta.upload = "requested"``, and each file is its own
``kind="file"`` row named ``<index name>/<member>`` (see
``probe.integrations._checkpoints``).

What the rows can and cannot prove:

* a row's ``status`` alone never proves bytes are stored: an upload the SDK
  refused is recorded as a reference row, ``status`` complete, with
  ``meta.upload = "failed"`` (`Run._record_refused_upload`). STORED is a row
  that is not a reference, has a ``content_hash``, is complete and was not
  refused (:func:`is_stored`);
* a reference refreshed in place keeps the ``step_index`` it was first written
  with, while its ``meta`` is replaced whole, so the step is read from
  ``meta.step`` first (:func:`step_of`);
* ``meta.deleted`` says the LOCAL copy is gone; an uploaded checkpoint stays
  recoverable from its members (:func:`recoverable`), and one whose members
  are not ALL stored -- still uploading, refused, abandoned when the trainer
  rewrote the file, lost with a preempted job's outbox -- is not, so
  ``latest`` falls back to the newest save that can actually be had;
* one name can have more than one row (a name saved again): the NEWEST row is
  the one that counts (:func:`_by_name`);
* a save from a range a later rewind abandoned carries the server-owned
  ``meta.rewound`` (data-catalog C7): it is never ``latest`` or ``best``
  (:func:`is_rewound`), though it stays listed and downloadable by id.
"""

from __future__ import annotations

import os
import shutil
import tempfile
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any

#: The index row's own meta keys.
MEMBERS_KEY = "members"
UPLOAD_KEY = "upload"
UPLOAD_REQUESTED = "requested"
#: A refused upload's marker (`Run._record_refused_upload`).
UPLOAD_FAILED = "failed"
#: A member row's meta key: the index row it belongs to.
MEMBER_OF_KEY = "checkpoint"
#: How many of the checkpoint's files a `.probe.config` kept out (never their names).
EXCLUDED_KEY = "members_excluded"
#: Server-owned: the save is from a range a rewind abandoned (``{to_step, epoch, at}``).
REWOUND_KEY = "rewound"

CHECKPOINT_KIND = "checkpoint"
LATEST = "latest"
BEST = "best"
WHICH = (LATEST, BEST)


class CheckpointNotStored(RuntimeError):
    """The checkpoint's bytes are not (all) in Probe: a location-only row, or
    an upload whose members are missing, pending, failed or refused."""

    def __init__(self, message: str, *, missing: list[str] | None = None, location: str | None = None,
                 host: str | None = None) -> None:
        super().__init__(message)
        self.missing = missing or []
        self.location = location
        self.host = host


class AmbiguousCheckpoint(ValueError):
    """More than one checkpoint callback marked its own ``best``."""

    def __init__(self, message: str, *, callbacks: list[str]) -> None:
        super().__init__(message)
        self.callbacks = callbacks


def _meta(row: dict) -> dict:
    meta = row.get("meta")
    return meta if isinstance(meta, dict) else {}


def step_of(row: dict) -> int | None:
    """``meta.step`` (kept current by a refresh), else ``step_index``."""
    step = _meta(row).get("step")
    if isinstance(step, int) and not isinstance(step, bool):
        return step
    step = row.get("step_index")
    return step if isinstance(step, int) and not isinstance(step, bool) else None


def is_rewound(row: dict) -> bool:
    """The save is from a range a later rewind abandoned (``meta.rewound``, set
    by the server when the run is reopened with ``rewind_to_step``)."""
    mark = _meta(row).get(REWOUND_KEY)
    return isinstance(mark, dict) or mark is True


def members(row: dict) -> list[str] | None:
    """The member paths an uploaded index row lists, or None for any other row."""
    meta = _meta(row)
    listed = meta.get(MEMBERS_KEY)
    if meta.get(UPLOAD_KEY) != UPLOAD_REQUESTED or not isinstance(listed, list):
        return None
    return [m for m in listed if isinstance(m, str) and m]


def is_stored(row: dict | None) -> bool:
    """True when the row's own bytes are in Probe's storage (see the module docstring)."""
    if not row or row.get("is_reference") or not row.get("content_hash"):
        return False
    if row.get("deleted_at"):
        return False
    if (row.get("status") or "complete") != "complete":
        return False
    return _meta(row).get(UPLOAD_KEY) != UPLOAD_FAILED


def _by_name(rows: list[dict]) -> dict[str, dict]:
    """Live rows by name, the NEWEST row for a name that has several."""
    out: dict[str, dict] = {}
    for row in rows:
        if row.get("deleted_at"):
            continue
        name = row.get("name")
        held = out.get(name)
        if held is None or str(row.get("created_at") or "") > str(held.get("created_at") or ""):
            out[name] = row
    return out


def member_rows(index: dict, rows: list[dict] | dict[str, dict]) -> dict[str, dict | None]:
    """Each member path of ``index`` -> its row (None when absent). ``rows`` is
    the run's rows, or :func:`_by_name` of them when asking about many indexes."""
    by_name = rows if isinstance(rows, dict) else _by_name(rows)
    prefix = f"{index.get('name')}/"
    return {rel: by_name.get(prefix + rel) for rel in members(index) or []}


def missing_members(index: dict, rows: list[dict] | dict[str, dict]) -> list[str]:
    return [rel for rel, row in member_rows(index, rows).items() if not is_stored(row)]


def recoverable(row: dict, rows: list[dict] | dict[str, dict]) -> bool:
    """Its bytes can be had: an upload whose files are ALL stored, a stored
    file, or a location-only checkpoint not known to be gone."""
    if members(row):
        return not missing_members(row, rows)
    if is_stored(row):
        return True
    return bool(row.get("is_reference")) and _meta(row).get("deleted") is not True


def _newest(row: dict) -> tuple:
    step = step_of(row)
    return (step if step is not None else -1, str(row.get("created_at") or ""))


def _candidates(rows: list[dict], which: str, callback: str | None) -> list[dict]:
    """``which``'s candidates among ``rows``, newest first."""
    if which not in WHICH:
        raise ValueError(f"which must be one of {WHICH}, not {which!r}")
    found = [
        r for r in rows if r.get("kind") == CHECKPOINT_KIND and not r.get("deleted_at") and not is_rewound(r)
    ]
    if callback is not None:
        found = [r for r in found if _meta(r).get("callback") == callback]
    if which == BEST:
        found = [r for r in found if _meta(r).get("best") is True]
        owners = sorted({str(_meta(r).get("callback")) for r in found if _meta(r).get("callback")})
        if len(owners) > 1:
            raise AmbiguousCheckpoint(
                f"{len(owners)} checkpoint callbacks each mark a best checkpoint ({', '.join(owners)})",
                callbacks=owners,
            )
    return sorted(found, key=_newest, reverse=True)


def select(rows: list[dict], which: str = LATEST, *, callback: str | None = None,
           recoverable_only: bool = True) -> dict | None:
    """The run's ``latest`` (highest step, then newest) or ``best`` checkpoint
    among ``rows`` (all of the run's artifact rows), or None. A save a rewind
    abandoned (:func:`is_rewound`) is never either.

    ``best`` is the row whose ``meta.best`` is true -- never a guess from scores.
    Two callbacks each marking a best (Lightning: top-k by ``val_loss`` and
    another by ``val_acc``) raise :class:`AmbiguousCheckpoint` unless
    ``callback=`` picks one (``meta.callback``). With ``recoverable_only`` the
    newest whose bytes can be had wins (:func:`recoverable`)."""
    by_name = _by_name(rows) if recoverable_only else {}
    for row in _candidates(rows, which, callback):
        if not recoverable_only or recoverable(row, by_name):
            return row
    return None


def find(client: Any, run_id: str, which: str = LATEST, *, callback: str | None = None,
         recoverable_only: bool = True) -> tuple[dict | None, list[dict] | None]:
    """:func:`select` over the server: the run's checkpoint rows only
    (``kind=checkpoint``), then each candidate's own files (``prefix=<name>``),
    newest first, until one can be had -- never the run's whole inventory, which
    a live run can change mid-listing. Returns the row and its files' rows."""
    rows = client.list_run_artifacts(run_id, kind=CHECKPOINT_KIND, scope="own")
    for row in _candidates(rows, which, callback):
        if not members(row):
            if not recoverable_only or recoverable(row, {}):
                return row, None
            continue
        files = client.list_run_artifacts(run_id, prefix=row["name"], scope="own")
        if not recoverable_only or recoverable(row, files):
            return row, files
    return None, None


#: Never in a member path segment: a Windows separator or NUL, anywhere.
_UNSAFE_SEGMENT_CHARS = ("\\", "\x00")


def _safe_target(dest: Path, rel: str, *, windows: bool = os.name == "nt") -> Path:
    """``dest/rel``, refusing a member path that could land outside ``dest``:
    absolute, ``..``/``.``/empty segments, a backslash or NUL, on Windows a
    drive or ``:`` (``Path(dest).joinpath("C:x")`` drops ``dest``), and --
    after joining -- anything that does not resolve under ``dest`` (a link
    already there included)."""
    posix = PurePosixPath(rel)
    parts = posix.parts
    if (
        not parts
        or posix.is_absolute()
        or any(p in ("", ".", "..") or any(c in p for c in _UNSAFE_SEGMENT_CHARS) for p in parts)
        or (windows and (":" in rel or PureWindowsPath(rel).anchor))
    ):
        raise ValueError(f"refusing member path {rel!r}: it would leave the destination folder")
    target = dest.joinpath(*parts)
    root = dest.resolve()
    resolved = target.resolve()
    if resolved != root and root not in resolved.parents:
        raise ValueError(f"refusing member path {rel!r}: it would leave the destination folder")
    return target


def _commit(staging: Path, root: Path) -> None:
    """Move the verified files from ``staging`` into ``root``, which must still
    hold nothing else: another writer's file is never overwritten or mixed in,
    and a move that fails takes back the ones already made."""
    foreign = [p.name for p in root.iterdir() if p != staging]
    if foreign:
        raise FileExistsError(f"{root} changed during the download ({', '.join(sorted(foreign)[:3])})")
    moved: list[Path] = []
    try:
        for entry in sorted(staging.iterdir()):
            target = root / entry.name
            if os.path.lexists(target):
                raise FileExistsError(f"{target} appeared during the download")
            os.replace(entry, target)
            moved.append(target)
        staging.rmdir()
    except BaseException:
        for target in moved:
            if target.is_dir() and not target.is_symlink():
                shutil.rmtree(target, ignore_errors=True)
            else:
                target.unlink(missing_ok=True)
        raise


def download(client: Any, checkpoint: dict, dest: str | os.PathLike, *, rows: list[dict] | None = None) -> dict:
    """Write the checkpoint's files into the folder ``dest``, each checked
    against its row's ``content_hash``. An uploaded set writes every member at
    its path; a stored checkpoint FILE is written as ``dest/<its file name>``.

    Raises :class:`CheckpointNotStored` (naming what is missing, or where a
    location-only checkpoint is) before writing anything. ``dest`` must not
    exist or be an empty folder (``FileExistsError`` otherwise). The files land
    in a private folder INSIDE ``dest`` (so a mount point or a read-only parent
    works) and move into place once every one is verified; on any failure
    ``dest`` is left as it was found. ``rows`` are the checkpoint's files'
    rows when the caller has them (:func:`find`).

    The result says what a byte-exact restore cannot: ``excluded`` (files a
    ``.probe.config`` kept out, never uploaded) and ``redacted`` (text files
    whose stored copy had a credential masked)."""
    name = str(checkpoint.get("name") or "")
    listed = members(checkpoint)
    if listed:
        if rows is None:
            run_id = checkpoint.get("run_id")
            if not run_id:
                raise ValueError(f"checkpoint {name} names no run_id, so its files cannot be listed")
            rows = client.list_run_artifacts(run_id, prefix=name, scope="own")
        found = member_rows(checkpoint, rows)
        missing = [rel for rel, row in found.items() if not is_stored(row)]
        if missing:
            raise CheckpointNotStored(
                f"checkpoint {name}: {len(missing)} of {len(found)} files are not stored in Probe "
                f"({', '.join(missing[:5])}{', ...' if len(missing) > 5 else ''})",
                missing=missing,
            )
        plan = list(found.items())
    elif is_stored(checkpoint):
        plan = [(PurePosixPath(name).name or "checkpoint", checkpoint)]
    else:
        meta = _meta(checkpoint)
        location = meta.get("local_path") or checkpoint.get("uri")
        host = meta.get("host")
        raise CheckpointNotStored(
            f"checkpoint {name} is recorded as a location only: {location}"
            + (f" on {host}" if host else "")
            + "; Probe stores no bytes for it",
            location=location,
            host=host,
        )
    root = Path(os.path.abspath(dest))
    if os.path.lexists(root) and (not root.is_dir() or root.is_symlink() or any(root.iterdir())):
        raise FileExistsError(
            f"{root} exists and is not an empty folder: a checkpoint is restored into a new or "
            "empty folder, so no file of another checkpoint mixes into it"
        )
    made_root = not os.path.lexists(root)
    if made_root:
        root.mkdir(parents=True)
    staging = Path(tempfile.mkdtemp(prefix=".probe-restore-", dir=root))
    try:
        targets = [(rel, _safe_target(staging, rel), row) for rel, row in plan]
        files = []
        for rel, target, row in targets:
            target.parent.mkdir(parents=True, exist_ok=True)
            got = client.download_artifact_to(row["id"], str(target))
            if got.get("sha256") != row.get("content_hash"):
                raise CheckpointNotStored(
                    f"checkpoint {name}: {rel} arrived with sha256 {got.get('sha256')}, expected "
                    f"{row.get('content_hash')}",
                    missing=[rel],
                )
            files.append({"path": rel, "size_bytes": got.get("size_bytes"), "sha256": got.get("sha256")})
        _commit(staging, root)
    except BaseException:
        shutil.rmtree(staging, ignore_errors=True)
        if made_root:
            shutil.rmtree(root, ignore_errors=True)
        raise
    excluded = _meta(checkpoint).get(EXCLUDED_KEY)
    return {
        "checkpoint": name,
        "id": checkpoint.get("id"),
        "dest": str(root),
        "files": files,
        "excluded": excluded if isinstance(excluded, int) and not isinstance(excluded, bool) else 0,
        "redacted": [rel for rel, row in plan if row.get("redacted_spans")],
    }
