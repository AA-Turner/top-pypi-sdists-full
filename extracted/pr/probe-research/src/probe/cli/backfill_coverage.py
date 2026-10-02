"""Scoped backfill inventory and verified delivery, independent of agent progress.

The old ledger remains the unit execution log. This versioned projection stores
approved byte versions, immutable upload intentions and their terminal receipts.
Only receipts cover files; neither a walk nor an empty queue establishes delivery.
"""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import fcntl
import hashlib
import json
import os
from pathlib import Path
import sqlite3
import stat
import time
import unicodedata
from urllib.parse import urlsplit, urlunsplit
import uuid

from .._compat import fromisoformat
from ..sdk.durable import file_lock, now_iso, read_json, write_text_atomic
from .backfill_ledger import default_dir, fingerprint

SCHEMA = "probe.backfill.coverage/3"

#: Schemas this build can open. A v2 store is migrated in place on open (one
#: ALTER plus an identity rewrite); anything else is still refused and preserved.
MIGRATABLE_SCHEMAS = ("probe.backfill.coverage/2",)

#: Files hashed per commit, and the longest a batch may stay uncommitted. The
#: census used to be ONE transaction over the whole folder, so a crash at file
#: 190,000 of 200,000 rolled back every hash it had paid for.
OBSERVE_BATCH_FILES = 1_000
OBSERVE_BATCH_SECONDS = 5.0

#: Hashing threads. `hashlib` releases the GIL on the 1 MB chunks `hash_current`
#: already reads, so these genuinely run in parallel; the ceiling is the disk,
#: not the interpreter. SQLite is never touched from them -- see `observe`.
OBSERVE_HASH_WORKERS = 4

#: A file written within this long is re-read whatever its signature says.
#: Timestamp resolution is 1-10ms on Linux and coarser through NFS/SMB, so a
#: write landing in the same tick as the stat is invisible to the cache.
SIGNATURE_SETTLE_SECONDS = 2.0


class CoverageError(ValueError):
    """Unverified scope, corrupt state, or a conflicting import owner."""


class CoverageReport(dict):
    """The bucket mapping, plus whether it was read mid-census.

    A plain dict to every existing caller -- they index fixed keys -- with one
    attribute added, because a census that has hashed half a folder reports the
    other half as `vanished`. That is correct DURING the pass and a lie
    afterwards, so a reader has to be able to tell which it is holding.
    """

    partial: bool = False


@dataclass(frozen=True)
class Scope:
    backend: str
    customer_id: str
    workspace_id: str
    project_id: str | None = None

    @property
    def key(self) -> str:
        return hashlib.sha256(json.dumps(asdict(self), sort_keys=True).encode()).hexdigest()[:24]

    @classmethod
    def resolve(
        cls, client, project: str | None = None, *, workspace_id: str | None = None,
    ) -> Scope:
        """Authenticate and resolve IDs before any completion or resume shortcut.

        A saved job supplies its approved workspace explicitly so a later default
        selection or CLI context change cannot redirect an import already queued.
        """
        from .refs import resolve

        identity = client.me()
        tenant = identity.get("customer_id")
        parsed = urlsplit(client.settings.base_url)
        if not tenant or not parsed.hostname or parsed.username or parsed.password:
            raise CoverageError("Cannot establish an authenticated backend and tenant.")
        backend = urlunsplit((parsed.scheme.lower(), parsed.netloc.lower(),
                               parsed.path.rstrip("/"), "", ""))
        selected = None
        if project:
            selected = client.get_project(resolve(client, "project", project).id)
            if selected.get("customer_id") != tenant:
                raise CoverageError("The selected project is outside the authenticated tenant.")
            if not selected.get("workspace_id"):
                raise CoverageError("The selected project has no verified workspace.")
            if workspace_id and str(selected["workspace_id"]) != str(workspace_id):
                raise CoverageError("The selected project moved from this import's approved workspace.")
        workspace = (
            selected["workspace_id"] if selected
            else workspace_id or client.settings.workspace
        )
        if workspace:
            row = client.get_workspace(str(workspace))
            if row.get("customer_id") != tenant:
                raise CoverageError("The selected workspace is outside the authenticated tenant.")
        else:
            workspace = _default_workspace(client.list_workspaces(), identity)["id"]
        return cls(backend, str(tenant), str(workspace),
                   str(selected["id"]) if selected else None)


def _default_workspace(rows: list[dict], identity: dict) -> dict:
    """Choose from the full in-tenant list, independent of alphabetical API order.

    New workspaces are shared team rows. Legacy kind/owner metadata does not
    identify their creator; only the recorded actor does. When this user has
    created none, retain the server's oldest-workspace fallback.
    """
    candidates = [row for row in rows
                  if row.get("customer_id") == identity["customer_id"] and row.get("id")]
    if not candidates:
        raise CoverageError(
            "No workspace is available for this account. "
            "Create a workspace in the dashboard, then retry the folder import."
        )
    if len(candidates) == 1:
        return candidates[0]
    actor = f"user:{identity['user_id']}" if identity.get("user_id") else None
    created = [row for row in candidates if actor and row.get("created_by") == actor]

    def created_order(row: dict) -> tuple[datetime, str]:
        try:
            when = row["created_at"]
            if not isinstance(when, datetime):
                when = fromisoformat(when)
            if when.tzinfo is None:
                when = when.replace(tzinfo=timezone.utc)
            return when, str(row["id"])
        except (KeyError, TypeError, ValueError) as exc:
            raise CoverageError(
                "Cannot determine the default workspace from its creation date. "
                "Select a workspace with `probe workspace use`, then retry."
            ) from exc

    return max(created, key=created_order) if created else min(candidates, key=created_order)


def _signature_tuple(value) -> tuple[int, int, int, int, int]:
    return (value.st_dev, value.st_ino, value.st_size, value.st_mtime_ns, value.st_ctime_ns)


def signature_of(value) -> str | None:
    """The inode fingerprint of a stat result, or None when it cannot be trusted.

    WHAT THIS IS FOR. Re-reading a terabyte to learn that nothing changed is the
    single largest cost in a repeat import, and every backup tool solves it the
    same way: remember the inode facts, and only read again when one of them
    moved. `st_ctime_ns` is the load-bearing field -- userspace has no API to
    set it, so any write, rename or permission change bumps it, which is what
    makes this stronger than the size+mtime pair `hash_current` rightly refuses
    to accept on its own. `st_dev`/`st_ino` catch a replace-by-rename that
    restored every other field.

    WHEN IT RETURNS NONE. A whole-second `ctime_ns` means the filesystem is not
    recording sub-second resolution (exFAT, some NFS/SMB mounts, a translating
    NAS). There the timestamps cannot distinguish two writes in the same second,
    so there is no signature worth storing and the file is hashed every time --
    exactly today's behaviour, kept for the filesystems that need it.
    """
    if not value.st_ctime_ns or value.st_ctime_ns % 1_000_000_000 == 0:
        return None
    return ":".join(str(part) for part in _signature_tuple(value))


def hash_current(root: Path, relative: str) -> tuple[str, int]:
    """Hash one confined, stable open file. Same size/mtime is never enough."""
    digest, size, _ = hash_current_signed(root, relative)
    return digest, size


def hash_current_signed(root: Path, relative: str) -> tuple[str, int, str | None]:
    """`hash_current`, also returning the inode signature it verified against.

    Split out rather than changing `hash_current`'s shape: the signature is
    meaningful only NEXT to the digest it was taken with, and callers that just
    want bytes should not have to carry a third value to ignore it.
    """
    target = (root / relative).resolve(strict=True)
    if not target.is_relative_to(root.resolve()) or Path(relative).is_absolute():
        raise CoverageError(f"Source escapes the folder: {relative}")
    digest = hashlib.sha256()
    with target.open("rb") as handle:
        before = os.fstat(handle.fileno())
        if not stat.S_ISREG(before.st_mode):
            raise CoverageError(f"Source is not a regular file: {relative}")
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)
        after = os.fstat(handle.fileno())
    current = (root / relative).stat()
    if (_signature_tuple(before) != _signature_tuple(after)
            or _signature_tuple(after) != _signature_tuple(current)):
        raise CoverageError(f"Source changed while it was being verified: {relative}")
    return digest.hexdigest(), after.st_size, signature_of(current)


def reusable_signature(root: Path, relative: str, saved: str | None) -> str | None:
    """The current signature when a saved one may stand in for re-reading the file.

    None means "read it". Three ways to get there, and all three are ordinary:
    nothing saved, the file moved in some way, or the signature is too young to
    trust -- a file whose mtime is inside the settle window may still be being
    written, and the write would land in the same timestamp we just recorded.
    """
    if not saved:
        return None
    try:
        current = (root / relative).stat()
    except OSError:
        return None
    if not stat.S_ISREG(current.st_mode):
        return None
    signature = signature_of(current)
    if signature is None or signature != saved:
        return None
    if current.st_mtime_ns > (time.time() - SIGNATURE_SETTLE_SECONDS) * 1_000_000_000:
        return None
    return signature


class Coverage:
    """One active writer per source and authenticated destination scope.

    SQLite gives bounded indexed receipt joins and transactional census updates.
    FULL synchronous commits protect the intent-before-enqueue crash boundary.
    Old workers and old backfill clients never enumerate this v2 directory.
    """

    def __init__(self, directory: Path, scope: Scope, source_id: str):
        self.directory = directory
        self.scope = scope
        self.source_id = source_id
        self.path = directory / "coverage.sqlite3"
        self.conn: sqlite3.Connection | None = None

    @classmethod
    def recovery_candidates(cls, root: Path, scope: Scope, *, directory: Path | None = None) -> list[dict]:
        """Suggest moved sources within this scope; a fingerprint never adopts one."""
        registry_path = (directory or default_dir()) / "v2" / scope.key / "sources.json"
        if not registry_path.exists():
            return []
        registry = read_json(registry_path, error=CoverageError)
        root_name = str(root.resolve())
        if any(root_name in item["paths"] for item in registry.values()):
            return []
        shape = fingerprint(root)
        return [{"source_id": key, "paths": value["paths"]}
                for key, value in registry.items() if value.get("fingerprint") == shape][:10]

    @classmethod
    def for_folder(cls, root: Path, scope: Scope, *, directory: Path | None = None,
                   source_id: str | None = None) -> Coverage:
        base = (directory or default_dir()) / "v2" / scope.key
        base.mkdir(parents=True, exist_ok=True, mode=0o700)
        registry_path = base / "sources.json"
        root_name = str(root.resolve())
        with file_lock(base / "sources.lock"):
            registry = read_json(registry_path, error=CoverageError) if registry_path.exists() else {}
            if source_id:
                source_id = str(uuid.UUID(source_id))
                if source_id not in registry:
                    raise CoverageError("Source ID does not exist in this destination scope.")
                for key, value in registry.items():
                    if key != source_id and root_name in value["paths"]:
                        value["paths"].remove(root_name)
                        value.setdefault("previous_paths", []).append(root_name)
                write_text_atomic(registry_path, json.dumps(registry, sort_keys=True))
            else:
                matches = [key for key, value in registry.items() if root_name in value["paths"]]
                if len(matches) > 1:
                    raise CoverageError("Multiple sources claim this folder; select a source ID.")
                source_id = matches[0] if matches else str(uuid.uuid4())
            if source_id not in registry:
                from ..sdk.device_identity import device_instance_id
                registry[source_id] = {"paths": [], "fingerprint": fingerprint(root),
                                       "import_device_id": device_instance_id(), "created_at": now_iso()}
            entry = registry[source_id]
            if root_name not in entry["paths"]:
                entry["paths"].append(root_name)
                write_text_atomic(registry_path, json.dumps(registry, sort_keys=True))
        target = base / source_id
        target.mkdir(exist_ok=True, mode=0o700)
        return cls(target, scope, source_id)

    @contextmanager
    def writer(self):
        """Fail promptly on contention; never wait behind another long import."""
        with (self.directory / "active.lock").open("a+") as lock:
            try:
                fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError as exc:
                raise CoverageError("Another backfill is already using this source and destination.") from exc
            try:
                self._open()
                yield self
            finally:
                if self.conn is not None:
                    self.conn.close()
                    self.conn = None
                fcntl.flock(lock, fcntl.LOCK_UN)

    def _open(self) -> None:
        existed = self.path.exists()
        self.conn = sqlite3.connect(self.path)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA synchronous=FULL")
        if not existed:
            self.conn.executescript("""
                CREATE TABLE meta (key TEXT PRIMARY KEY, value TEXT NOT NULL);
                CREATE TABLE files (
                  path TEXT PRIMARY KEY, observed_hash TEXT, size INTEGER,
                  present INTEGER NOT NULL DEFAULT 1, observation_error TEXT,
                  approved_hash TEXT, project_id TEXT, project_slug TEXT,
                  manifest TEXT, exclusion TEXT, correlation TEXT,
                  signature TEXT, dead TEXT);
                CREATE TABLE versions (
                  correlation TEXT PRIMARY KEY, intent TEXT NOT NULL,
                  receipt TEXT, error TEXT, queued INTEGER NOT NULL DEFAULT 0);
                CREATE TABLE stages (key TEXT PRIMARY KEY, value TEXT NOT NULL);
            """)
            self.put_meta("identity", {"schema": SCHEMA, "scope": asdict(self.scope),
                                       "source_id": self.source_id})
            os.chmod(self.path, 0o600)
        expected = {"schema": SCHEMA, "scope": asdict(self.scope), "source_id": self.source_id}
        identity = self.meta("identity")
        if identity != expected:
            self._migrate(identity, expected)

    def _migrate(self, identity, expected) -> None:
        """Bring a store written by an older build up to `SCHEMA`, or refuse it.

        The refusal is the important half and it is unchanged: a store whose
        SCOPE differs, or whose schema this build has never heard of, is left
        exactly as it was. Migrating is only ever offered for a schema on the
        known ladder, and only when everything else about the identity already
        matches -- otherwise a foreign store could be adopted by renaming it.

        Additive and one-way. Every receipt, intent and approval survives; a
        migrated store simply has no saved signatures yet, so its next census
        hashes the folder once and caches from then on.
        """
        older = dict(identity) if isinstance(identity, dict) else {}
        rest = {key: value for key, value in older.items() if key != "schema"}
        target = {key: value for key, value in expected.items() if key != "schema"}
        if older.get("schema") not in MIGRATABLE_SCHEMAS or rest != target:
            raise CoverageError(
                "Backfill state has an incompatible schema or destination; it was preserved."
            )
        columns = {row["name"] for row in self.conn.execute("PRAGMA table_info(files)")}
        with self.conn:
            for name in ("signature", "dead"):
                if name not in columns:
                    self.conn.execute(f"ALTER TABLE files ADD COLUMN {name} TEXT")
            self.conn.execute("CREATE TABLE IF NOT EXISTS stages (key TEXT PRIMARY KEY, value TEXT NOT NULL)")
        self.put_meta("migrated_from", {"schema": older.get("schema"), "at": now_iso()})
        self.put_meta("identity", expected)

    def meta(self, key: str, default=None):
        row = self.conn.execute("SELECT value FROM meta WHERE key=?", (key,)).fetchone()
        return json.loads(row[0]) if row else default

    def put_meta(self, key: str, value) -> None:
        with self.conn:
            self.conn.execute("INSERT OR REPLACE INTO meta VALUES (?, ?)", (key, json.dumps(value)))

    def observe(self, root: Path, paths, *, workers: int | None = None, progress=None) -> None:
        """Inventory only. A successful census never creates approved or covered rows.

        THREE CHANGES FROM THE ONE-BIG-TRANSACTION VERSION, all about a census
        over a real research drive taking minutes to hours:

        A file whose inode signature is unchanged since the hash already stored
        for it is NOT re-read. That is the difference between a repeat import
        costing a full pass over the folder and costing a stat per file. The
        rule for when a signature may stand in lives in `reusable_signature`.

        Hashing that DOES happen runs on a small pool. `hashlib` releases the
        GIL on the chunks `hash_current` reads, so this is real parallelism, and
        the pool never touches SQLite -- results come back here, on the thread
        that owns the connection, exactly like every other writer in this file.

        Progress is committed in batches instead of one transaction spanning the
        whole walk. A batch boundary is a crash boundary: a kill mid-census now
        costs the current batch, not every hash since the folder was opened.
        While that is in flight `meta.observing` is set, and `report()` says
        `partial` -- because half a census reports the un-walked half as
        vanished, which is true of the moment and false of the folder.
        """
        names = {}
        collisions = set()
        paths = list(paths)
        for path in paths:
            canonical = unicodedata.normalize("NFC", path)
            if canonical in names and names[canonical] != path:
                collisions.update((path, names[canonical]))
            names[canonical] = path
        saved = {row["path"]: row["signature"]
                 for row in self.conn.execute("SELECT path, signature FROM files")}

        run_id = uuid.uuid4().hex
        self.put_meta("observing", {"run": run_id, "at": now_iso(), "total": len(paths)})

        pending: list[tuple] = []
        reused = 0
        done = 0
        last_commit = time.monotonic()

        def flush() -> None:
            nonlocal last_commit
            if not pending:
                return
            with self.conn:
                self.conn.executemany("""
                    INSERT INTO files(path, observed_hash, size, present, observation_error, signature)
                    VALUES (?, ?, ?, 1, ?, ?)
                    ON CONFLICT(path) DO UPDATE SET observed_hash=excluded.observed_hash,
                      size=excluded.size, present=1, observation_error=excluded.observation_error,
                      signature=excluded.signature
                """, pending)
            pending.clear()
            last_commit = time.monotonic()

        def record(path: str, outcome) -> None:
            nonlocal done
            pending.append((path, *outcome))
            done += 1
            if (len(pending) >= OBSERVE_BATCH_FILES
                    or time.monotonic() - last_commit >= OBSERVE_BATCH_SECONDS):
                flush()
                if progress is not None:
                    progress(completed=done, total=len(paths), reused=reused)

        def measure(path: str):
            """Runs on a worker thread. Filesystem and hashlib only, never SQLite."""
            try:
                if path in collisions:
                    raise CoverageError(
                        "Two source paths share the same normalized artifact name; review their names."
                    )
                digest, size, signature = hash_current_signed(root, path)
                return digest, size, None, signature
            except (OSError, ValueError, RuntimeError) as exc:
                return None, None, str(exc)[:1024], None

        unchanged: list[str] = []
        to_hash: list[str] = []
        for path in paths:
            if path in collisions:
                to_hash.append(path)
                continue
            signature = reusable_signature(root, path, saved.get(path))
            if signature is None:
                to_hash.append(path)
            else:
                unchanged.append(path)

        # The cheap half first, and without a pool: these rows keep the hash
        # they already had, so there is nothing to compute and nothing to wait
        # for. Doing them up front also means a census interrupted early has
        # already re-marked every unchanged file present.
        for path in unchanged:
            row = self.conn.execute(
                "SELECT observed_hash, size, signature FROM files WHERE path=?", (path,)
            ).fetchone()
            reused += 1
            record(path, (row["observed_hash"], row["size"], None, row["signature"]))
        flush()

        count = max(1, min(int(workers) if workers else OBSERVE_HASH_WORKERS, len(to_hash) or 1))
        if count == 1 or len(to_hash) <= 1:
            for path in to_hash:
                record(path, measure(path))
        else:
            with ThreadPoolExecutor(max_workers=count) as pool:
                for path, outcome in zip(to_hash, pool.map(measure, to_hash)):
                    record(path, outcome)
        flush()
        # The last partial batch never crosses a boundary, so without this the
        # bar stops short of the total it just finished counting.
        if progress is not None and paths:
            progress(completed=done, total=len(paths), reused=reused)
        # Absence is decided at the END, against what this census actually saw.
        # Clearing `present` up front was fine while the whole walk was one
        # transaction -- an interrupt rolled it back. With batched commits it
        # would survive, so a kill mid-census left every file it had not reached
        # marked absent: `report()` calls those vanished and `enqueue()` skips
        # them, until some later complete census repairs it.
        with self.conn:
            self.conn.execute("CREATE TEMP TABLE IF NOT EXISTS seen (path TEXT PRIMARY KEY)")
            self.conn.execute("DELETE FROM seen")
            self.conn.executemany("INSERT OR IGNORE INTO seen VALUES (?)",
                                  [(path,) for path in paths])
            self.conn.execute(
                "UPDATE files SET present=0 WHERE path NOT IN (SELECT path FROM seen)")
            self.conn.execute("DELETE FROM seen")
        self.put_meta("observing", None)
        self.put_meta("last_census", {"at": now_iso(), "files": len(paths),
                                      "hashed": len(to_hash), "reused": reused})

    @property
    def observing(self) -> bool:
        """Whether a census is part-way through this store right now."""
        return bool(self.meta("observing"))

    def verified_hash(self, root: Path, path: str) -> tuple[str | None, int | None, bool]:
        """This file's current digest and size, re-reading only if it must.

        Returns `(digest, size, rehashed)`. The one place outside `observe` that
        decides whether stored bytes still describe the file on disk, so that a
        caller wanting to check a source before acting on it -- the reference
        lane in delivery is the live one -- cannot quietly use a weaker rule
        than the census does.
        """
        row = self.conn.execute(
            "SELECT observed_hash, size, signature FROM files WHERE path=?", (path,)
        ).fetchone()
        if row and row["observed_hash"] and reusable_signature(root, path, row["signature"]):
            return row["observed_hash"], row["size"], False
        digest, size, signature = hash_current_signed(root, path)
        with self.conn:
            self.conn.execute(
                "UPDATE files SET observed_hash=?, size=?, signature=? WHERE path=?",
                (digest, size, signature, path),
            )
        return digest, size, True

    def rows(self) -> list[dict]:
        return [dict(row) for row in self.conn.execute("SELECT * FROM files ORDER BY path")]

    def rows_for(self, paths) -> dict[str, dict]:
        """Just these files. The per-unit path must never read the whole table.

        `rows()` materialises every row in the folder as a dict. Calling it once
        per unit -- which the resume loop did, and which per-unit delivery would
        do again -- is O(units x files): 500 units over a 200,000-file drive is
        a hundred million dict entries built to look at four hundred of them.
        """
        wanted = list(dict.fromkeys(paths))
        found: dict[str, dict] = {}
        for start in range(0, len(wanted), 500):
            chunk = wanted[start:start + 500]
            marks = ",".join("?" * len(chunk))
            for row in self.conn.execute(f"SELECT * FROM files WHERE path IN ({marks})", chunk):
                found[row["path"]] = dict(row)
        return found

    def delivered_paths(self, paths) -> set[str]:
        """Which of THESE paths already have a receipt.

        `report()` answers this for the whole folder, which is the wrong
        question once delivery runs per unit: it joins every file row against
        every version row to decide about four hundred paths.
        """
        wanted = list(dict.fromkeys(paths))
        found: set[str] = set()
        for start in range(0, len(wanted), 500):
            chunk = wanted[start:start + 500]
            marks = ",".join("?" * len(chunk))
            for row in self.conn.execute(
                f"""SELECT f.path FROM files f JOIN versions v USING(correlation)
                    WHERE f.path IN ({marks}) AND v.receipt IS NOT NULL""", chunk):
                found.add(row["path"])
        return found

    def approve(self, assignments: dict[str, dict], *, changed: bool = False) -> None:
        """Pin the reviewed current bytes and resolved project IDs in one commit."""
        with self.conn:
            for path, project in assignments.items():
                row = self.conn.execute("SELECT * FROM files WHERE path=?", (path,)).fetchone()
                if not row or not row["observed_hash"] or not row["present"]:
                    raise CoverageError(f"Cannot approve unreadable or missing source: {path}")
                if row["approved_hash"] and row["approved_hash"] != row["observed_hash"] and not changed:
                    raise CoverageError(f"Changed source requires explicit review: {path}")
                if project.get("customer_id") != self.scope.customer_id or str(project.get("workspace_id")) != self.scope.workspace_id:
                    raise CoverageError(f"Destination is outside the reviewed workspace: {path}")
                if self.scope.project_id and str(project["id"]) != self.scope.project_id:
                    raise CoverageError(f"Destination differs from the selected project: {path}")
                same = row["approved_hash"] == row["observed_hash"] and row["project_id"] == str(project["id"])
                # `dead` clears here too: re-planning a path IS the explicit
                # decision to try it again, so a give-up must not outlive the
                # review that reconsidered it.
                self.conn.execute("""UPDATE files SET approved_hash=observed_hash,
                    project_id=?, project_slug=?, manifest=?, correlation=?,
                    exclusion=NULL, dead=NULL WHERE path=?""",
                    (str(project["id"]), project["slug"], row["manifest"] if same else None,
                     row["correlation"] if same else None, path))

    def validate_destinations(self, client) -> None:
        """A deleted/recreated slug or moved project cannot inherit old completion."""
        for row in self.conn.execute("SELECT DISTINCT project_id FROM files WHERE project_id IS NOT NULL"):
            project = client.get_project(row[0])
            if project.get("customer_id") != self.scope.customer_id or str(project.get("workspace_id")) != self.scope.workspace_id:
                raise CoverageError("A saved project is no longer in the approved tenant/workspace.")

    def remember_manifest(self, path: str, manifest: dict) -> None:
        with self.conn:
            # Once intended, notes and transfer mode belong to the immutable
            # request too. A regenerated worker description cannot mutate it.
            self.conn.execute("UPDATE files SET manifest=? WHERE path=? AND correlation IS NULL",
                              (json.dumps(manifest), path))

    def intend(self, row: dict, *, reference: bool, uri: str | None = None) -> dict:
        if not row["approved_hash"] or row["approved_hash"] != row["observed_hash"]:
            raise CoverageError(f"Source version is not approved: {row['path']}")
        if row.get("correlation"):
            saved = self.conn.execute(
                "SELECT intent FROM versions WHERE correlation=?", (row["correlation"],)
            ).fetchone()
            if not saved:
                raise CoverageError("Approved file has no durable delivery intention.")
            intent = json.loads(saved[0])
            expected = {"source_id": self.source_id, "scope": asdict(self.scope),
                        "path": row["path"], "content_hash": row["approved_hash"],
                        "size_bytes": row["size"], "project_id": row["project_id"],
                        "mode": "reference" if reference else "upload"}
            if any(intent.get(key) != value for key, value in expected.items()):
                raise CoverageError("Saved intention differs from the approved source version.")
            # A remount changes a local URI, not the reviewed remote request.
            # Preserve its reference URI through the intent-before-enqueue
            # crash window as well as retries already known to the SDK.
            return {**intent, "correlation": row["correlation"]}
        intent = {"source_id": self.source_id, "scope": asdict(self.scope),
                  "path": row["path"], "content_hash": row["approved_hash"],
                  "artifact_name": unicodedata.normalize("NFC", row["path"]),
                  "size_bytes": row["size"], "project_id": row["project_id"],
                  "mode": "reference" if reference else "upload", "uri": uri}
        correlation = "backfill-v2:" + hashlib.sha256(json.dumps(intent, sort_keys=True).encode()).hexdigest()
        with self.conn:
            self.conn.execute("INSERT OR IGNORE INTO versions(correlation,intent) VALUES (?,?)",
                              (correlation, json.dumps(intent, sort_keys=True)))
            self.conn.execute("UPDATE files SET correlation=? WHERE path=?", (correlation, row["path"]))
        return {**intent, "correlation": correlation}

    def accept_receipt(self, correlation: str, receipt: dict) -> None:
        found = self.conn.execute("SELECT intent FROM versions WHERE correlation=?", (correlation,)).fetchone()
        if not found:
            raise CoverageError("Receipt has no durable local intention.")
        intent = json.loads(found[0])
        expected_ref = intent["mode"] == "reference"
        if (receipt.get("correlation") != correlation or receipt.get("state") != "delivered"
                or receipt.get("status") != "complete"
                or (not expected_ref and receipt.get("readable") is not True)
                or not receipt.get("artifact_id") or receipt.get("anchor") != "project"
                or receipt.get("anchor_id") != intent["project_id"]
                or receipt.get("name") != intent["artifact_name"]
                or receipt.get("content_hash") != intent["content_hash"]
                or receipt.get("size_bytes") != intent["size_bytes"]
                or bool(receipt.get("is_reference")) != expected_ref
                or (expected_ref and receipt.get("uri") != intent["uri"])):
            raise CoverageError("Delivery receipt does not match the approved file, bytes and destination.")
        with self.conn:
            self.conn.execute("UPDATE versions SET receipt=?, error=NULL WHERE correlation=?",
                              (json.dumps(receipt), correlation))
            # An exhausted unit can still leave valid manifest rows that land
            # afterward. Retire its failed marker with this verified receipt,
            # or --retry-dead would discard the completed file's approval too.
            # A newer approval has a different correlation and stays untouched.
            self.conn.execute("UPDATE files SET dead=NULL WHERE path=? AND correlation=?",
                              (intent["path"], correlation))

    def reconcile(self, client) -> None:
        for row in self.conn.execute("SELECT correlation FROM versions WHERE receipt IS NULL").fetchall():
            try:
                state = client.delivery_state(row[0])
                if state.get("state") == "delivered":
                    self.accept_receipt(row[0], state)
                elif state.get("state") == "queued":
                    self.enqueued(row[0])
                else:
                    self.failure(row[0], state.get("error") or f"delivery {state.get('state', 'unknown')}")
            except Exception as exc:
                self.failure(row[0], f"Receipt reconciliation failed: {str(exc)[:512]}")

    def failure(self, correlation: str, message: str) -> None:
        with self.conn:
            self.conn.execute("UPDATE versions SET error=? WHERE correlation=?", (message[:1024], correlation))

    def enqueued(self, correlation: str) -> None:
        with self.conn:
            self.conn.execute("UPDATE versions SET queued=1, error=NULL WHERE correlation=?", (correlation,))

    def mark_dead(self, paths, reason: str) -> list[str]:
        """Give up on these files, keeping anything already delivered.

        A unit that fails every time it is tried is not the same thing as a file
        someone chose to skip, and it must not be recorded as one: `exclusion`
        is checked BEFORE the receipt below, so writing it over a path that
        already landed would report a delivered file as skipped, and `_run`
        only ever re-reviews `new` and `changed`, so nothing would bring it
        back. This column is read after the receipt and is cleared by an
        explicit retry.
        """
        touched = []
        with self.conn:
            for path in paths:
                row = self.conn.execute(
                    """SELECT f.path, v.receipt FROM files f
                       LEFT JOIN versions v USING(correlation) WHERE f.path=?""", (path,)
                ).fetchone()
                if not row or row["receipt"]:
                    continue
                self.conn.execute("UPDATE files SET dead=? WHERE path=?", (reason[:1024], path))
                touched.append(path)
        return touched

    def clear_dead(self, paths=None) -> int:
        """Let given-up files be planned again. `None` clears every one of them.

        THE APPROVAL GOES TOO. Clearing only the marker leaves a row that is
        approved, unmanifested and unreceipted -- which `report()` calls
        `unresolved`, and the import only ever re-reviews `new` and `changed`.
        So the flag would clear a column, change a printed line, and plan
        nothing. Dropping the approval is what puts the file back in front of
        the review, which is the whole point of asking for a retry.
        """
        columns = ("dead=NULL, approved_hash=NULL, project_id=NULL, project_slug=NULL, "
                   "manifest=NULL, correlation=NULL")
        with self.conn:
            # Older workers could leave this marker after a valid receipt.
            # Normalize those rows before selecting retries, without clearing
            # their approved version, manifest or durable delivery identity.
            self.conn.execute("""UPDATE files SET dead=NULL WHERE dead IS NOT NULL
                AND EXISTS (SELECT 1 FROM versions v
                    WHERE v.correlation=files.correlation AND v.receipt IS NOT NULL)""")
            if paths is None:
                return self.conn.execute(
                    f"UPDATE files SET {columns} WHERE dead IS NOT NULL").rowcount
            total = 0
            for path in paths:
                total += self.conn.execute(
                    f"UPDATE files SET {columns} WHERE path=? AND dead IS NOT NULL", (path,)
                ).rowcount
            return total

    def dead_reasons(self) -> dict[str, str]:
        return {row["path"]: row["dead"]
                for row in self.conn.execute(
                    "SELECT path, dead FROM files WHERE dead IS NOT NULL ORDER BY path")}

    def report(self) -> CoverageReport:
        result = CoverageReport({key: [] for key in (
            "delivered", "references", "queued", "excluded", "dead",
            "new", "changed", "unresolved", "vanished")})
        result.partial = self.observing
        for row in self.conn.execute("""SELECT f.*, v.receipt, v.error, v.queued FROM files f
                                       LEFT JOIN versions v USING(correlation) ORDER BY f.path"""):
            if not row["present"]:
                state = "vanished"
            elif row["observation_error"]:
                state = "unresolved"
            elif row["approved_hash"] and row["approved_hash"] != row["observed_hash"]:
                state = "changed"
            elif row["exclusion"]:
                state = "excluded"
            elif row["receipt"]:
                receipt = json.loads(row["receipt"])
                state = "references" if receipt.get("is_reference") else "delivered"
            elif row["dead"]:
                # AFTER the receipt on purpose -- see `mark_dead`.
                state = "dead"
            elif row["error"]:
                state = "unresolved"
            elif row["queued"]:
                state = "queued"
            elif not row["approved_hash"]:
                state = "new"
            else:
                state = "unresolved"
            result[state].append(row["path"])
        return result

    def write_report(self) -> Path:
        if self.observing:
            raise CoverageError("A census is still running; the per-file report would be half true.")
        target = self.directory / "coverage.json"
        report = self.report()
        write_text_atomic(target, json.dumps({"schema": SCHEMA, "at": now_iso(),
                          "scope": asdict(self.scope), "source_id": self.source_id,
                          "files": report, "dead": self.dead_reasons()},
                          ensure_ascii=False, indent=2))
        return target
