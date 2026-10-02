"""The walk, written down: what was on disk, so the next run can diff it.

ENUMERATE produced a list and threw it away. `to_jsonl(evidence)` went straight
into a prompt and nothing survived the process, so:

  * every re-run re-walked the whole tree from nothing,
  * a crash lost the walk along with everything else,
  * and "what is new since last time" had no answer at all, which is why
    re-importing a folder meant re-importing a folder.

This module is the missing half. One sorted file per imported folder, beside
the ledger under XDG state and locked the same way. It records the last walk
that led to a FINISHED import, not the last walk that happened -- writing it
during the walk made a cancelled run advance it, after which the next run
compared the folder against files that were never imported, found no
difference, and dropped everything added in between. See `Index.collect`.

WHAT IDENTIFIES A FILE is path + size + mtime, and deliberately NOT inode. A
recopied or remounted drive -- which `mtime_uninformative` already calls "the
normal state of a shared drive someone was handed" -- changes every inode while
the content is identical, so an inode in the identity turns an ordinary recopy
into a full re-import with a duplicate of every artifact. Inode rides along as
a hint for rename detection and nothing reads it yet.

SORTING IS LOAD-BEARING, not tidiness. `os.scandir` returns filesystem order,
and the sampler's smallest-first sort is stable, so ties at the sample budget
broke on whatever order the filesystem happened to give -- two runs over one
unchanged folder could sample a different 600 files. Sorted by path, they
cannot.

THE DIFF HAS THREE CLASSES AND THREE DIFFERENT ANSWERS:

    new        import it.
    changed    REPORT it, do not re-import. Same-name artifacts COEXIST in
               Probe rather than superseding, so a re-upload is a duplicate
               beside the original, not a replacement. Choosing between
               versioning and skipping is a product decision that has not been
               made; reporting is the honest thing to do until it is.
    vanished   name it in the reconcile. Nothing is retired or deleted -- an
               import has no business deleting anything on the strength of a
               file being absent from a drive that might simply not be mounted.
"""

from __future__ import annotations

import hashlib
import json
import os
from collections.abc import Iterable, Iterator
from dataclasses import dataclass, field
from pathlib import Path

from ..sdk.durable import file_lock
from .backfill_ledger import default_dir

#: Written into every index so a format change can be recognised rather than
#: mis-parsed. A file whose schema we do not know is treated as absent: the
#: cost is one re-walk, and the alternative is a diff computed against rows
#: that mean something else.
SCHEMA = "probe.backfill.index/1"

#: Files past this many rows get a warning rather than a refusal. Sorting means
#: the index holds one `Row` per file until commit, alongside the caller's own
#: record list and the full-list copies `sample`/`cluster_by_mtime` make
#: downstream, so a tree far past this is a real risk of being OOM-killed with
#: nothing to show. Naming the number beats dying to the kernel.
LARGE_WALK_FILES = 2_000_000


@dataclass(frozen=True)
class Row:
    """One file, as the index remembers it."""

    path: str
    size: int
    mtime: float
    tier: str = ""
    #: Advisory. NOT part of identity -- see the module docstring.
    inode: int = 0

    @property
    def identity(self) -> tuple[str, int, int]:
        """What "the same file" means.

        mtime to whole seconds: filesystems disagree about sub-second
        resolution, so a copy between two of them changes a float that means
        nothing has changed.
        """
        return (self.path, self.size, int(self.mtime))


@dataclass
class Diff:
    """What changed between two walks of one folder."""

    new: list[str] = field(default_factory=list)
    changed: list[str] = field(default_factory=list)
    vanished: list[str] = field(default_factory=list)
    unchanged: int = 0

    @property
    def quiet(self) -> bool:
        return not (self.new or self.changed or self.vanished)

    def describe(self) -> list[str]:
        out: list[str] = []
        if self.new:
            out.append(f"{len(self.new):,} new file(s) since the last import.")
        if self.changed:
            out.append(
                f"{len(self.changed):,} file(s) changed since the last import — "
                "reported, not re-imported: an artifact of the same name would "
                "land beside the original rather than replace it."
            )
        if self.vanished:
            out.append(
                f"{len(self.vanished):,} file(s) are gone from the folder — "
                "nothing was retired; they may simply be on an unmounted drive."
            )
        return out


def path_for(root: Path, *, directory: Path | None = None) -> Path:
    """Where this folder's index lives.

    Beside the ledger and keyed the same way, so one folder's bookkeeping is
    one place and `PROBE_BACKFILL_STATE_DIR` moves all of it at once.
    """
    root = Path(root).resolve()
    base = directory or default_dir()
    key = hashlib.sha256(str(root).encode("utf-8", "replace")).hexdigest()[:16]
    # NOT `.jsonl`. `backfill_ledger.find_resumable` globs `*.jsonl` in this
    # directory and calls `read_text()` on every hit, so an index sharing the
    # extension would be slurped whole -- ~24MB for a 200k-file tree, on every
    # resumable scan -- only to conclude it is not a ledger.
    return base / f"{key}.index.log"


class Index:
    """One folder's walk, on disk."""

    def __init__(self, path: Path) -> None:
        self.path = Path(path)
        self.lock_path = self.path.with_suffix(".lock")
        self._pending: list[Row] = []

    @classmethod
    def for_folder(cls, root: Path, *, directory: Path | None = None) -> Index:
        return cls(path_for(root, directory=directory))

    # -- writing -------------------------------------------------------------

    def collect(self, records: Iterable, *, root: Path) -> Iterator:
        """Pass `records` through, remembering each one for a later `commit`.

        A GENERATOR that yields what it was given, so the caller's existing
        loop over the walk is unchanged and the walk is not paid for twice.

        NOTHING IS WRITTEN HERE. The index is the record of the last walk that
        led to a finished import, and writing it during the walk made it the
        record of the last walk FULL STOP -- so a run the user cancelled at the
        approval prompt still advanced it, and the next run compared a folder
        against a walk whose files were never imported, found no difference,
        and reported nothing to do. Files added between those two runs were
        silently dropped. `commit` is called only where the import succeeded.

        Rows are buffered to be sorted, which is what makes the file
        deterministic; peak cost is one `Row` per file alongside the caller's
        own record list. See `LARGE_WALK_FILES`.
        """
        root = Path(root).resolve()
        rows: list[Row] = []
        self._pending = rows
        for record in records:
            rows.append(_row_from(record, root))
            yield record

    def pending(self) -> list[Row]:
        """The rows THIS walk collected, before they are committed.

        The diff has to be computed against these and not against `read()`:
        once writing moved to `commit`, the file on disk still holds the
        PREVIOUS walk for the whole run, so `diff(previous, self.read())`
        compared a walk against itself and was quiet no matter what changed.
        """
        return list(self._pending)

    def commit(self) -> None:
        """Write the collected walk down. Call ONLY after a finished import.

        A walk that collected nothing is never committed: an unreadable root
        and an unmounted drive both yield zero records, and replacing a good
        index with an empty one destroys the record of the last real walk --
        after which every file reads as new and the change report and the
        no-op gate both go quiet.
        """
        rows = getattr(self, "_pending", None)
        if not rows:
            return
        self._flush(rows)
        self._pending = []

    def _flush(self, rows: list[Row]) -> None:
        rows.sort(key=lambda r: r.path)
        self.path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        staging = self.path.with_suffix(".partial")
        with file_lock(self.lock_path):
            with staging.open("w", encoding="utf-8") as fh:
                fh.write(json.dumps({"schema": SCHEMA, "rows": len(rows)}) + "\n")
                for row in rows:
                    fh.write(
                        json.dumps(
                            {"path": row.path, "size": row.size, "mtime": row.mtime,
                             "tier": row.tier, "inode": row.inode},
                            ensure_ascii=False,
                        )
                        + "\n"
                    )
            os.replace(staging, self.path)

    # -- reading -------------------------------------------------------------

    def read(self) -> list[Row]:
        """The rows, or an empty list when there is no usable index.

        An unreadable or unknown-schema file is absence, not an error: the cost
        is one re-walk, and diffing against rows whose meaning we cannot vouch
        for is how a folder gets re-imported wholesale.
        """
        try:
            with self.path.open(encoding="utf-8") as fh:
                header = json.loads(fh.readline() or "{}")
                if header.get("schema") != SCHEMA:
                    return []
                return [row for row in (_row_from_json(line) for line in fh) if row]
        except (OSError, ValueError):
            return []

    def walk_id(self) -> str:
        """A digest of the sorted identities. Same folder, same content, same id.

        Over IDENTITY rather than the raw file so a schema field or a
        re-serialisation cannot make an unchanged folder look changed.
        """
        return walk_id_of(self.read())

    def exists(self) -> bool:
        return self.path.exists()


def walk_id_of(rows: list[Row]) -> str:
    digest = hashlib.sha256()
    for row in sorted(rows, key=lambda r: r.path):
        digest.update(f"{row.path}\0{row.size}\0{int(row.mtime)}\n".encode())
    return digest.hexdigest()[:16]


def diff(previous: list[Row], current: list[Row]) -> Diff:
    """What changed, in the three classes the module docstring describes."""
    before = {r.path: r for r in previous}
    after = {r.path: r for r in current}
    out = Diff()
    for path, row in after.items():
        was = before.get(path)
        if was is None:
            out.new.append(path)
        elif was.identity != row.identity:
            out.changed.append(path)
        else:
            out.unchanged += 1
    out.vanished.extend(path for path in before if path not in after)
    out.new.sort()
    out.changed.sort()
    out.vanished.sort()
    return out


def _row_from(record, root: Path) -> Row:
    try:
        rel = str(Path(record.path).relative_to(root))
    except ValueError:  # pragma: no cover - the walk never leaves the root
        rel = str(record.path)
    return Row(
        path=rel,
        size=int(record.size),
        mtime=float(record.mtime),
        tier=str(getattr(record, "tier", "") or ""),
        inode=int(getattr(record, "inode", 0) or 0),
    )


def _row_from_json(line: str) -> Row | None:
    line = line.strip()
    if not line:
        return None
    try:
        data = json.loads(line)
        return Row(
            path=str(data["path"]),
            size=int(data.get("size") or 0),
            mtime=float(data.get("mtime") or 0.0),
            tier=str(data.get("tier") or ""),
            inode=int(data.get("inode") or 0),
        )
    except (ValueError, KeyError, TypeError):
        # ONE unreadable row is not an unreadable index. A truncated final line
        # from a killed process should cost that line, not the whole diff.
        return None
