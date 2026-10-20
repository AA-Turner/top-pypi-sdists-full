"""The person's cloud files as a real ``Cloud`` folder in their Cloud Computer home.

Owner ruling (2026-10-17/18, "mirror + stubs"): small and recent files are
copied in; big or cold files appear as STUBS — a small regular placeholder file
that says what it is — and are fetched when opened through our tools (the
agent fs/shell gate calls :meth:`CloudFilesSync.hydrate`) or ``cloud-files
fetch``. Edits upload back. No FUSE: every Linux tool sees ordinary files.

The source of truth is the platform's files system, reached ONLY through the
cloud-files bridge (``/api/cloud-files/*``) with a person-scoped machine token
(``aud=cloud_computer_files``, minted by AI Dream at launch, renewed through
``POST /cloud-files/machine-session``). The machine never sees a fleet secret.

Conflict rule — never lose either side: when the cloud copy and the local copy
both changed since the last sync, the local bytes move to
``<name> (conflict from Cloud Computer <stamp>)<ext>`` (kept locally AND
uploaded as a new cloud file) and the cloud version takes the original path.

Delete rule — a local delete reaches the cloud ONLY when it is a confirmed,
individual delete (adversarial review D6, 2026-10-18): the file was in the last
synced state, it was seen missing on two scans in a row, the walk of the folder
had no error, its nearest folder still on disk lists normally (never a folder
that suddenly reads empty while it held several files), and the pass holds no
more than ``max_deletes_per_pass`` such deletes. Anything else is HELD: nothing
is deleted, the sync says why (``status()["halt"]``, the machine's activity
reading, the person's app and an admin alert), and only the person's answer lets
exactly the held set through. Every propagated delete is written to
``deleted.jsonl`` first, and the cloud delete itself is a soft delete (trash),
so it can be restored.

Resolving a hold (review 2 N2, 2026-10-18): the person sees the hold in the app
(an assist chip and the Computer tab) and chooses "Delete these N files in the
cloud" or "Restore them to the folder". Deleting needs a short-lived worker token
AI Dream mints only for the person's own signed-in click (``mtx_op=
machine_files_resolve``); the loopback CLI can only RESTORE, so an agent on the
machine can never confirm its own mass delete. A hold nobody resolves within
``held_delete_restore_after_seconds`` resolves to RESTORE by itself: the cloud
and the folder never disagree for ever.

One bad entry never stalls the pass (N4): a symlink, a path that escapes the
folder, or a file the bridge refuses is skipped and listed in ``status()
["skipped"]`` while everything else keeps syncing. A file that changes while it
uploads or downloads is never recorded as synced (N3): the upload records the
file's state from BEFORE the read, and a download is never written over a file
that changed while the bytes were in flight.

State lives in the home (EFS), so it survives a new task and a new build.
"""

from __future__ import annotations

import asyncio
import base64
import hashlib
import json
import logging
import os
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Protocol

logger = logging.getLogger(__name__)

STUB_MAGIC = "MATRX CLOUD FILE - not downloaded yet"
STATE_DIR_NAME = ".matrx/cloud-sync"
EPOCH_CURSOR = "1970-01-01T00:00:00+00:00"
#: Bridge system roots never enter the replica (the server excludes them too).
SYSTEM_ROOTS = ("generations/", "system-files/")
#: Editor temp files and our own partial downloads are never uploaded.
SKIP_SUFFIXES = (".part", ".swp", ".swx", "~", ".tmp")
_STUB_PREFIX = STUB_MAGIC.encode()


class LocalFolderUnreadable(RuntimeError):
    """The Cloud folder could not be read completely: no delete may be inferred from it."""


class ChangedDuringTransfer(RuntimeError):
    """The local file changed while bytes were in flight: never write over it."""


class HoldChanged(RuntimeError):
    """The held set the person answered is no longer the held set on the machine."""


RESOLVE_ACTIONS = ("delete", "restore")
#: How many skipped entries (symlinks, refused files) the status lists by name.
_SKIPPED_LISTED = 20


def _sig(p: Path) -> tuple[int, int, int] | None:
    """(size, mtime_ns, inode) of what is at ``p`` now, None when nothing is there."""
    try:
        st = os.lstat(p)
    except FileNotFoundError:
        return None
    return st.st_size, st.st_mtime_ns, st.st_ino


def hold_id_for(paths: list[str]) -> str:
    """A stable id for one exact held set: the person's answer names it."""
    return hashlib.sha256("\n".join(sorted(paths)).encode()).hexdigest()[:16]


@dataclass
class LocalScan:
    """One complete walk of the Cloud folder (raises instead of returning a partial one)."""

    files: set[str]
    dirs: set[str]
    #: Symbolic links in the folder: skipped (and listed), never synced or followed.
    links: set[str] = field(default_factory=set)


@dataclass
class SyncKnobs:
    """Thresholds; AI Dream sends the live ``cloud_computer.files`` knob values."""

    mirror_max_file_bytes: int = 25 * 1024 * 1024
    mirror_recent_days: int = 90
    disk_budget_bytes: int = 2 * 1024 * 1024 * 1024
    local_scan_seconds: int = 5
    remote_poll_seconds: int = 30
    #: At most this many confirmed local deletes reach the cloud in one pass;
    #: more is a mass delete: held, never propagated without the person's answer.
    #: 0 = no local delete ever reaches the cloud without confirmation.
    max_deletes_per_pass: int = 25
    #: The ``max_deletes_per_pass`` cap also holds across this rolling window, so
    #: deletes dripped a few per pass are still a mass delete (review 2 N8).
    delete_window_seconds: int = 600
    #: A hold nobody resolves restores the held files to the folder after this
    #: long (0 = restore on the next pass): never a permanent disagreement.
    held_delete_restore_after_seconds: int = 3 * 24 * 3600

    @classmethod
    def from_mapping(cls, data: dict[str, Any] | None) -> "SyncKnobs":
        base = cls()
        for key in base.__dataclass_fields__:
            value = (data or {}).get(key)
            if isinstance(value, int) and not isinstance(value, bool) and value >= 0:
                setattr(base, key, value)
        return base


class BridgeError(RuntimeError):
    def __init__(self, status: int, body: Any = None, retry_after: float | None = None) -> None:
        super().__init__(f"cloud-files bridge answered {status}: {str(body)[:300]}")
        self.status = status
        self.body = body
        self.retry_after = retry_after


class Bridge(Protocol):
    async def changes(self, since: str, limit: int) -> dict[str, Any]: ...
    async def get(self, path: str) -> bytes: ...
    async def put(self, path: str, content: bytes, expected_checksum: str | None) -> dict[str, Any]: ...
    async def delete(self, path: str) -> None: ...
    async def session(self) -> dict[str, Any]: ...


def token_claims(token: str) -> dict[str, Any]:
    """Read (never verify) a JWT's claims — the bridge verifies; we only need ``exp``/``org``."""
    try:
        part = token.split(".")[1]
        return json.loads(base64.urlsafe_b64decode(part + "=" * (-len(part) % 4)))
    except Exception:  # noqa: BLE001
        return {}


class HttpBridge:
    """The cloud-files bridge over HTTPS with the person's machine token."""

    def __init__(self, base_url: str, token: str, *, client: Any = None) -> None:
        import httpx

        self._base = base_url.rstrip("/")
        self.token = token
        self._client = client or httpx.AsyncClient(timeout=httpx.Timeout(120.0, connect=15.0))

    def _headers(self) -> dict[str, str]:
        headers = {"Authorization": f"Bearer {self.token}"}
        org = token_claims(self.token).get("org")
        if org:
            headers["X-Organization-Id"] = str(org)
        return headers

    async def _call(self, method: str, path: str, **kw: Any) -> Any:
        resp = await self._client.request(method, f"{self._base}{path}", headers=self._headers(), **kw)
        if resp.status_code >= 400:
            retry = resp.headers.get("Retry-After")
            try:
                body: Any = resp.json()
            except Exception:  # noqa: BLE001
                body = resp.text[:300]
            raise BridgeError(resp.status_code, body, float(retry) if retry and retry.isdigit() else None)
        return resp

    async def changes(self, since: str, limit: int) -> dict[str, Any]:
        return (await self._call("GET", "/cloud-files/changes", params={"since": since, "limit": limit})).json()

    async def get(self, path: str) -> bytes:
        return (await self._call("GET", "/cloud-files/get", params={"path": path})).content

    async def put(self, path: str, content: bytes, expected_checksum: str | None) -> dict[str, Any]:
        data = {"file_path": path}
        if expected_checksum:
            data["expected_checksum"] = expected_checksum
        files = {"file": (os.path.basename(path) or "file", content, "application/octet-stream")}
        return (await self._call("PUT", "/cloud-files/put", data=data, files=files)).json()

    async def delete(self, path: str) -> None:
        try:
            await self._call("DELETE", "/cloud-files/delete", params={"path": path})
        except BridgeError as exc:
            if exc.status != 404:
                raise

    async def session(self) -> dict[str, Any]:
        return (await self._call("POST", "/cloud-files/machine-session")).json()


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _human(n: int) -> str:
    size = float(n)
    for unit in ("bytes", "KB", "MB", "GB"):
        if size < 1024 or unit == "GB":
            return f"{size:.0f} {unit}" if unit == "bytes" else f"{size:.1f} {unit}"
        size /= 1024
    return f"{n} bytes"


def stub_text(rel: str, size: int, updated: str | None) -> str:
    return (
        f"{STUB_MAGIC}\n"
        f"name: {os.path.basename(rel)}\n"
        f"size: {_human(size)} ({size} bytes)\n"
        f"modified: {updated or 'unknown'}\n"
        f"cloud path: {rel}\n\n"
        "This is a placeholder. The real file is in your AI Matrx cloud files.\n"
        "An agent reading it gets the real file. To download it yourself, run:\n"
        f"  cloud-files fetch \"{rel}\"\n"
    )


def _parse_time(value: Any) -> datetime | None:
    if not value:
        return None
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)


def conflict_name(rel: str, now: datetime, taken: Any = None) -> str:
    """A conflict copy's name; ``taken(name)`` True means that name is in use, so
    two conflicts on one file in the same second never overwrite each other."""
    head, ext = os.path.splitext(rel)
    stamp = now.strftime('%Y-%m-%d %H%M%S')
    name = f"{head} (conflict from Cloud Computer {stamp}){ext}"
    n = 2
    while taken is not None and taken(name):
        name = f"{head} (conflict from Cloud Computer {stamp} {n}){ext}"
        n += 1
    return name


def is_stub_bytes(data: bytes) -> bool:
    """Our own placeholder text (never a person's content; never uploaded)."""
    return data.startswith(_STUB_PREFIX)


@dataclass
class Entry:
    remote_checksum: str | None = None
    remote_size: int = 0
    remote_updated: str | None = None
    local_sha: str | None = None
    local_size: int = -1
    local_mtime: float = -1.0
    stub: bool = False
    #: A copy-eligible file still showing as a placeholder: the first mirror
    #: writes every file as a stub at once, then fills copies newest-first.
    want_copy: bool = False


@dataclass
class SyncStats:
    downloaded: int = 0
    stubbed: int = 0
    hydrated: int = 0
    uploaded: int = 0
    deleted_local: int = 0
    deleted_remote: int = 0
    conflicts: int = 0
    evicted: int = 0
    deletes_held: int = 0
    refused_stub_uploads: int = 0
    restored: int = 0
    auto_restored: int = 0
    changed_during_transfer: int = 0
    last_error: str | None = None
    last_pull_at: str | None = None
    last_push_at: str | None = None


class CloudFilesSync:
    """Two-way mirror of the person's cloud files into ``root`` (``~/Cloud``)."""

    def __init__(
        self,
        root: Path,
        bridge: Bridge,
        *,
        state_dir: Path | None = None,
        knobs: SyncKnobs | None = None,
        now: Any = None,
    ) -> None:
        self.root = Path(root)
        self.bridge = bridge
        self.state_dir = state_dir or (self.root.parent / STATE_DIR_NAME)
        self.knobs = knobs or SyncKnobs()
        self._now = now or (lambda: datetime.now(timezone.utc))
        self.cursor = EPOCH_CURSOR
        self.entries: dict[str, Entry] = {}
        self.stats = SyncStats()
        self.initial_done = False
        #: True once AI Dream's live knob values arrived (the first session renewal).
        self.knobs_loaded = False
        #: Why local deletes are held right now (None = not held): reason, count,
        #: since, a few sample paths. Persisted, so a new task keeps holding.
        self.halt: dict[str, Any] | None = None
        #: Paths seen missing on the previous scan (a delete needs two in a row).
        self._missing_last: set[str] = set()
        #: The exact held set the person confirmed in the app (``resolve_held``).
        self._confirmed_deletes: set[str] = set()
        #: Entries skipped this run, never a stalled pass: path -> why (symlink,
        #: outside the folder, refused by the bridge, could not be written).
        self.skipped: dict[str, str] = {}
        #: An upload the bridge refused, by the file's signature then: never
        #: retried every 5 s until the file changes.
        self._refused: dict[str, tuple[Any, str]] = {}
        #: Cloud rows that failed to apply; retried next pull (the cursor moved on).
        self._retry_rows: dict[str, dict[str, Any]] = {}
        #: When each recent delete was sent (monotonic seconds), for the window cap.
        self._recent_deletes: list[float] = []
        self._clock = time.monotonic
        #: Work in flight, for the machine's activity reading (never stop mid-transfer).
        self.pending_uploads = 0
        self.transfers = 0
        self._lock = asyncio.Lock()
        self._load()

    # ── state ────────────────────────────────────────────────────────────
    @property
    def _state_file(self) -> Path:
        return self.state_dir / "state.json"

    def _load(self) -> None:
        try:
            data = json.loads(self._state_file.read_text())
        except (OSError, ValueError):
            return
        self.cursor = data.get("cursor") or EPOCH_CURSOR
        self.initial_done = bool(data.get("initial_done"))
        self.halt = data.get("halt") or None
        self._retry_rows = {r["file_path"]: r for r in (data.get("retry") or []) if r.get("file_path")}
        for rel, raw in (data.get("files") or {}).items():
            self.entries[rel] = Entry(**{k: v for k, v in raw.items() if k in Entry.__dataclass_fields__})

    def _payload(self) -> dict[str, Any]:
        return {
            "cursor": self.cursor,
            "initial_done": self.initial_done,
            "halt": self.halt,
            "retry": list(self._retry_rows.values()),
            "files": {rel: dict(e.__dict__) for rel, e in sorted(self.entries.items())},
        }

    def _store_state(self, payload: dict[str, Any]) -> None:
        self.state_dir.mkdir(parents=True, exist_ok=True)
        tmp = self._state_file.with_suffix(".tmp")
        tmp.write_text(json.dumps(payload, indent=1))
        os.replace(tmp, self._state_file)

    def save(self) -> None:
        self._store_state(self._payload())

    async def asave(self) -> None:
        """``save`` off the event loop: the state of a 12k-file folder is megabytes
        on a network drive, and the worker's loop also answers /health."""
        payload = self._payload()  # snapshot on the loop: no dict changes mid-write
        await asyncio.to_thread(self._store_state, payload)

    def status(self) -> dict[str, Any]:
        stubs = [r for r, e in self.entries.items() if e.stub]
        return {
            "root": str(self.root),
            "initial_done": self.initial_done,
            "cursor": self.cursor,
            "files": len(self.entries),
            "stubs": len(stubs),
            "copies_pending": self.pending_copies(),
            "mirrored_bytes": self._mirrored_bytes(),
            "knobs": self.knobs.__dict__,
            "stats": self.stats.__dict__,
            "halt": self.hold_view(),
            "skipped": self.skipped_view(),
            "work": self.work_signals(),
        }

    def hold_view(self) -> dict[str, Any] | None:
        """The hold as a person sees it: what, how many, since when, when it restores."""
        if not self.halt:
            return None
        view = {k: v for k, v in self.halt.items() if k != "paths"}
        since = _parse_time(self.halt.get("since"))
        if since is not None:
            view["restores_at"] = (
                since + timedelta(seconds=self.knobs.held_delete_restore_after_seconds)
            ).isoformat()
        return view

    def skipped_view(self) -> dict[str, Any]:
        items = sorted(self.skipped.items())
        return {"count": len(items),
                "items": [{"path": p, "reason": r} for p, r in items[:_SKIPPED_LISTED]]}

    def _skip(self, rel: str, reason: str) -> None:
        # Copy-on-write: the scan runs in a thread while /status reads this.
        if self.skipped.get(rel) != reason:
            logger.warning("cloud files: %s skipped (%s); the rest keeps syncing", rel, reason)
            self.skipped = {**self.skipped, rel: reason}

    def _unskip(self, rel: str, *prefixes: str) -> None:
        if self.skipped.get(rel, "\0").startswith(prefixes):
            self.skipped = {k: v for k, v in self.skipped.items() if k != rel}

    def work_signals(self) -> dict[str, Any]:
        """What the sync is doing right now, for ``/machine/activity``: a machine is
        never stopped (build move) while an edit waits to upload or a transfer runs.
        Copies still filling in are not work: they re-fill after any restart."""
        return {
            "pending_uploads": self.pending_uploads,
            "transfers": self.transfers,
            "deletes_held": (self.halt or {}).get("held", 0),
            "halt_reason": (self.halt or {}).get("reason"),
            "halt_since": (self.halt or {}).get("since"),
            "hold_id": (self.halt or {}).get("hold_id"),
            "hold_sample": (self.halt or {}).get("sample"),
            "skipped": len(self.skipped),
        }

    # ── helpers ──────────────────────────────────────────────────────────
    def _path(self, rel: str) -> Path:
        p = (self.root / rel).resolve()
        if self.root.resolve() not in p.parents and p != self.root.resolve():
            raise ValueError(f"path escapes the Cloud folder: {rel}")
        return p

    def _store(self, rel: str, data: bytes, entry: Entry, expect: Any = "any") -> None:
        """Write ``data`` at ``rel``. ``expect`` = the file's signature (``_sig``)
        when the decision to write was made: if it changed since (a person or an
        agent wrote it while the bytes were in flight), nothing is written and
        ``ChangedDuringTransfer`` says so. The recorded stat is the one of the
        bytes WE wrote (taken before the rename keeps it), never a later edit's."""
        p = self._path(rel)
        p.parent.mkdir(parents=True, exist_ok=True)
        tmp = p.with_name(p.name + ".part")
        tmp.write_bytes(data)
        st = tmp.stat()
        if expect != "any" and _sig(p) != expect:
            tmp.unlink(missing_ok=True)
            raise ChangedDuringTransfer(rel)
        os.replace(tmp, p)
        entry.local_sha, entry.local_size, entry.local_mtime = _sha256(data), st.st_size, st.st_mtime

    def _adopt(self, rel: str, entry: Entry, data: bytes, st: os.stat_result) -> None:
        """Record a local file that already holds the cloud bytes (no write);
        ``st`` is its stat from BEFORE the bytes were read."""
        entry.local_sha, entry.local_size, entry.local_mtime = _sha256(data), st.st_size, st.st_mtime
        entry.stub = entry.want_copy = False

    def _write(self, rel: str, data: bytes) -> Entry:
        entry = self.entries.setdefault(rel, Entry())
        self._store(rel, data, entry)
        return entry

    async def _awrite(self, rel: str, data: bytes, expect: Any = "any") -> Entry:
        """``_write`` with the file I/O off the event loop (the dict changes on the loop)."""
        entry = self.entries.get(rel) or Entry()
        await asyncio.to_thread(self._store, rel, data, entry, expect)
        self.entries[rel] = entry
        return entry

    async def _place_remote(self, rel: str) -> Entry:
        """Download the cloud file into ``rel``. A local write that lands while
        the bytes are in flight is kept as a conflict copy, never overwritten."""
        before = await asyncio.to_thread(_sig, self._path(rel))
        data = await self._get(rel)
        try:
            return await self._awrite(rel, data, before)
        except ChangedDuringTransfer:
            self.stats.changed_during_transfer += 1
            if await asyncio.to_thread(os.path.lexists, self._path(rel)):
                await self._keep_local_as_conflict(rel)
            return await self._awrite(rel, data)

    async def _get(self, rel: str) -> bytes:
        self.transfers += 1
        try:
            return await self.bridge.get(rel)
        finally:
            self.transfers -= 1

    def _unknown_local(self, rel: str) -> tuple[bytes, os.stat_result] | None:
        """Bytes (and their stat from before the read) of a file at ``rel`` the sync
        state does not know (None when absent)."""
        p = self._path(rel)
        if not p.is_file():
            return None
        st = p.stat()
        return p.read_bytes(), st

    async def _achanged(self, rel: str, entry: Entry) -> bool:
        return await asyncio.to_thread(self._local_changed, rel, entry)

    def _local_changed(self, rel: str, entry: Entry) -> bool:
        """The local file differs from what the last sync left there."""
        p = self._path(rel)
        try:
            st = p.stat()
        except FileNotFoundError:
            return entry.local_sha is not None
        if st.st_size == entry.local_size and st.st_mtime == entry.local_mtime:
            return False
        return _sha256(p.read_bytes()) != entry.local_sha

    def _mirrored_bytes(self) -> int:
        return sum(e.remote_size for e in self.entries.values() if not e.stub)

    def _wants_mirror(self, size: int, updated: str | None) -> bool:
        k = self.knobs
        if size > k.mirror_max_file_bytes:
            return False
        when = _parse_time(updated)
        if when is not None and when < self._now() - timedelta(days=k.mirror_recent_days):
            return False
        return self._mirrored_bytes() + size <= k.disk_budget_bytes

    def is_stub(self, rel: str) -> bool:
        entry = self.entries.get(rel)
        try:
            return bool(entry and entry.stub and not self._local_changed(rel, entry))
        except (OSError, ValueError):
            return False

    def rel_for(self, path: str) -> str | None:
        """``path`` (absolute or relative to the Cloud folder's parent) -> cloud path, or None."""
        p = Path(path)
        if not p.is_absolute():
            p = self.root.parent / p
        try:
            return str(p.resolve().relative_to(self.root.resolve()))
        except ValueError:
            return None

    # ── downstream ───────────────────────────────────────────────────────
    async def apply_remote(self, row: dict[str, Any]) -> None:
        rel = str(row.get("file_path") or "").lstrip("/")
        if not rel or rel.startswith(SYSTEM_ROOTS):
            return
        entry = self.entries.get(rel)
        checksum = row.get("checksum")
        size = int(row.get("size_bytes") or row.get("file_size") or 0)
        updated = row.get("updated_at")
        updated = str(updated) if updated is not None else None
        if row.get("deleted"):
            if entry is None:
                return
            if not await asyncio.to_thread(os.path.lexists, self._path(rel)):
                self.entries.pop(rel, None)  # gone on both sides
                self._missing_last.discard(rel)
                return
            if await self._achanged(rel, entry):
                # Changed here, deleted there: keep the local edit; the next push re-creates it.
                entry.remote_checksum = None
                return
            await asyncio.to_thread(self._path(rel).unlink, missing_ok=True)
            self.entries.pop(rel, None)
            self.stats.deleted_local += 1
            return
        if entry is not None and checksum and checksum == entry.remote_checksum:
            return  # our own upload echoing back, or nothing new
        if entry is not None and entry.local_sha and checksum == entry.local_sha:
            entry.remote_checksum, entry.remote_size, entry.remote_updated = checksum, size, updated
            entry.stub = False
            return
        if entry is None:
            # A file here the state does not know (state lost, or a new local
            # file racing a new cloud file of the same name): never overwrite it.
            found = await asyncio.to_thread(self._unknown_local, rel)
            local = found[0] if found else None
            if found is not None and checksum and _sha256(found[0]) == checksum:
                entry = self.entries.setdefault(rel, Entry())
                self._adopt(rel, entry, found[0], found[1])
                entry.remote_checksum, entry.remote_size, entry.remote_updated = checksum, size, updated
                return
            if local is not None and not is_stub_bytes(local):
                await self._keep_local_as_conflict(rel)
        elif not await asyncio.to_thread(os.path.lexists, self._path(rel)):
            # Deleted here, changed there: the newer cloud version wins and comes
            # back; a local delete never erases an edit it never saw.
            self._missing_last.discard(rel)
        elif await self._achanged(rel, entry):
            await self._keep_local_as_conflict(rel)
        if not self.initial_done and self._wants_mirror(size, updated):
            # First mirror: the whole tree appears at once as placeholders and
            # the copies fill in newest-first (fill_copies), so a large cloud
            # never holds the folder empty for minutes.
            entry = await self._awrite(rel, stub_text(rel, size, updated).encode())
            entry.stub, entry.want_copy = True, True
            entry.remote_checksum, entry.remote_size, entry.remote_updated = checksum, size, updated
            self.stats.stubbed += 1
            return
        if self._wants_mirror(size, updated):
            entry = await self._place_remote(rel)
            entry.stub = False
            self.stats.downloaded += 1
        else:
            entry = await self._awrite(rel, stub_text(rel, size, updated).encode())
            entry.stub = True
            self.stats.stubbed += 1
        entry.remote_checksum, entry.remote_size, entry.remote_updated = checksum, size, updated

    async def pull_once(self) -> int:
        """Apply every cloud change since the cursor. Returns the server's poll hint."""
        hint = self.knobs.remote_poll_seconds
        async with self._lock:
            for row in list(self._retry_rows.values()):
                await self._apply_one(row)
            while True:
                page = await self.bridge.changes(self.cursor, 500)
                rows = page.get("files") or []
                for row in rows:
                    await self._apply_one(row)
                nxt = page.get("next_cursor") or self.cursor
                hint = int(page.get("poll_after_seconds") or hint)
                advanced = nxt != self.cursor
                self.cursor = nxt
                await self.asave()
                if not rows or not advanced or len(rows) < 500:
                    break
            self.initial_done = True
            self.stats.last_pull_at = self._now().isoformat()
            await self.asave()
        return max(5, min(hint, 600))

    async def _apply_one(self, row: dict[str, Any]) -> None:
        """One cloud change; a failure is that row's alone. A path outside the
        folder (a symlink) is skipped and listed; any other failure keeps the row
        to retry on the next pull, because the cursor moves on without it."""
        rel = str(row.get("file_path") or "").lstrip("/")
        try:
            await self.apply_remote(row)
        except BridgeError as exc:
            if exc.status in (401, 403, 429) or exc.status >= 500:
                raise  # the bridge itself is down or refusing: the whole pass waits
            self._retry_rows[rel] = row
            self._skip(rel, f"cloud answered {exc.status}")
            return
        except ValueError as exc:
            self._retry_rows.pop(rel, None)
            self._skip(rel, str(exc))
            return
        except OSError as exc:
            self._retry_rows[rel] = row
            self._skip(rel, f"could not write: {exc.strerror or exc}")
            return
        self._retry_rows.pop(rel, None)
        self._unskip(rel, "cloud answered", "could not write", "path escapes")

    async def hydrate(self, rel: str) -> bool:
        """Fetch a stub's real bytes (fetch-on-open). True when the file is now real."""
        async with self._lock:
            entry = self.entries.get(rel)
            if entry is None or not entry.stub:
                return entry is not None
            if await self._achanged(rel, entry):
                return True  # the person wrote real content over the stub
            before = await asyncio.to_thread(_sig, self._path(rel))
            data = await self._get(rel)
            try:
                entry = await self._awrite(rel, data, before)
            except ChangedDuringTransfer:
                # Written while the bytes were in flight: theirs wins, it uploads.
                self.stats.changed_during_transfer += 1
                return True
            entry.stub = entry.want_copy = False
            entry.remote_checksum = entry.remote_checksum or entry.local_sha
            self.stats.hydrated += 1
            await self.asave()
            return True

    async def fill_copies(self, limit: int = 25) -> int:
        """Copy in up to ``limit`` copy-eligible placeholders, newest first, within the budget."""
        pending = sorted(
            ((e.remote_updated or "", rel) for rel, e in self.entries.items() if e.want_copy and e.stub),
            reverse=True,
        )
        filled = 0
        for _, rel in pending[:limit]:
            entry = self.entries[rel]
            if self._mirrored_bytes() + entry.remote_size > self.knobs.disk_budget_bytes:
                entry.want_copy = False
                continue
            if await self.hydrate(rel):
                filled += 1
        if filled:
            await self.asave()
        return filled

    def pending_copies(self) -> int:
        return sum(1 for e in self.entries.values() if e.want_copy and e.stub)

    def evict(self) -> int:
        """Over the disk budget: turn the coldest clean mirrored files back into stubs."""
        over = self._mirrored_bytes() - self.knobs.disk_budget_bytes
        if over <= 0:
            return 0
        def clean_copy(rel: str, e: Entry) -> bool:
            try:
                return not e.stub and not self._local_changed(rel, e)
            except (OSError, ValueError):
                return False  # one odd entry never stops eviction

        clean = [(e.remote_updated or "", rel) for rel, e in list(self.entries.items()) if clean_copy(rel, e)]
        evicted = 0
        for _, rel in sorted(clean):
            if over <= 0:
                break
            e = self.entries[rel]
            size = e.remote_size
            try:
                before = _sig(self._path(rel))
                if self._local_changed(rel, e):
                    continue
                self._store(rel, stub_text(rel, size, e.remote_updated).encode(), e, before)
            except (ChangedDuringTransfer, OSError, ValueError):
                continue
            new = e
            new.stub = True
            over -= size
            evicted += 1
        self.stats.evicted += evicted
        return evicted

    # ── upstream ─────────────────────────────────────────────────────────
    def _scan(self) -> LocalScan:
        """Walk the Cloud folder completely, or raise: a missing root or any
        unreadable folder is never read as "the person deleted everything"."""
        root = self.root
        if not root.is_dir():
            raise LocalFolderUnreadable(f"the Cloud folder {root} is missing")
        files: set[str] = set()
        dirs: set[str] = {""}

        def fail(err: OSError) -> None:
            raise LocalFolderUnreadable(f"could not read {err.filename}: {err.strerror or err}")

        links: set[str] = set()
        for dirpath, dirnames, filenames in os.walk(root, onerror=fail):
            dirnames[:] = [d for d in dirnames if not d.startswith(".")]
            here = Path(dirpath).relative_to(root)
            for d in list(dirnames):
                rel = str(here / d) if str(here) != "." else d
                if os.path.islink(os.path.join(dirpath, d)):
                    links.add(rel)  # never followed (os.walk), never synced
                    continue
                dirs.add(rel)
            for name in filenames:
                if name.startswith(".") or name.endswith(SKIP_SUFFIXES):
                    continue
                rel = str((Path(dirpath) / name).relative_to(root))
                if os.path.islink(os.path.join(dirpath, name)):
                    links.add(rel)
                    continue
                files.add(rel)
        return LocalScan(files=files, dirs=dirs, links=links)

    def _classify(self, scan: LocalScan, known: dict[str, Entry]) -> tuple[list[str], list[str]]:
        """(changed, missing). Known files are checked by path, never by the walk's
        name filter: a cloud file named ``.env`` or ``draft.tmp`` is not "deleted"
        just because the walk does not list such names."""
        changed: list[str] = []
        missing: list[str] = []
        for rel in scan.links:
            self._skip(rel, "symbolic link (not synced)")
        for rel in sorted(scan.files | set(known)):
            try:
                p = self._path(rel)
                if not os.path.lexists(p):
                    if rel in known:
                        missing.append(rel)
                    continue
                if p.is_symlink() or not p.is_file():
                    # A known file replaced by a link or a folder: neither
                    # changed nor deleted; listed, and the rest syncs.
                    self._skip(rel, "symbolic link (not synced)" if p.is_symlink() else "not a file")
                    continue
                if rel not in known or self._local_changed(rel, known[rel]):
                    changed.append(rel)
            except ValueError:
                # Under a folder that is now a link out of ~/Cloud: never "missing".
                self._skip(rel, "inside a symbolic link (not synced)")
            except OSError as exc:
                self._skip(rel, f"could not read: {exc.strerror or exc}")
            else:
                self._unskip(rel, "symbolic link", "inside a symbolic", "not a file", "could not read")
        for rel in [r for r, why in self.skipped.items() if why == "symbolic link (not synced)"]:
            if rel not in scan.links and rel not in known:
                self._unskip(rel, "symbolic link")  # the link is gone
        return changed, missing

    def _folder_is_healthy(self, rel: str, known: dict[str, Entry]) -> bool:
        """The nearest folder of ``rel`` still on disk lists normally and is not a
        folder that reads empty while the state says it held several files (a
        mount not ready, a network-drive hiccup, a restore in progress)."""
        parent = Path(rel).parent
        try:
            while str(parent) not in (".", "") and not self._path(str(parent)).is_dir():
                parent = parent.parent
            folder = "" if str(parent) == "." else str(parent)
            with os.scandir(self._path(folder) if folder else self.root) as it:
                empty = next(it, None) is None
        except (OSError, ValueError):
            return False
        if not empty:
            return True
        prefix = f"{folder}/" if folder else ""
        held_there = sum(1 for r in known if r.startswith(prefix))
        return held_there <= 1

    def _gate_deletes(self, missing: list[str], known: dict[str, Entry]) -> tuple[list[str], dict[str, Any] | None]:
        """Which local deletes may reach the cloud this pass, and why the rest are held."""
        now_missing = set(missing)
        seen_twice = sorted(now_missing & self._missing_last)
        self._missing_last = now_missing
        if not seen_twice and now_missing and self.halt:
            # A new process after a hold: keep holding while it re-confirms.
            return [], {k: v for k, v in self.halt.items() if k != "since"}
        confirmed = [r for r in seen_twice if r in self._confirmed_deletes]
        candidates = [r for r in seen_twice if r not in self._confirmed_deletes]
        self._confirmed_deletes &= now_missing
        def hold(reason: str, sample: list[str], **extra: Any) -> dict[str, Any]:
            return {"reason": reason, "held": len(candidates), "sample": sample[:5],
                    "paths": candidates, "hold_id": hold_id_for(candidates), **extra}

        unhealthy = [r for r in candidates if not self._folder_is_healthy(r, known)]
        if unhealthy:
            return confirmed, hold("folder_unhealthy", unhealthy)
        cap = self.knobs.max_deletes_per_pass
        if len(candidates) > cap:
            return confirmed, hold("mass_delete", candidates, cap=cap)
        if candidates and len(candidates) + self._deletes_in_window() > cap:
            # Dripped a few per pass: still more than the cap inside the window.
            return confirmed, hold("mass_delete", candidates, cap=cap,
                                   window_seconds=self.knobs.delete_window_seconds)
        return confirmed + candidates, None

    def _deletes_in_window(self) -> int:
        horizon = self._clock() - self.knobs.delete_window_seconds
        self._recent_deletes = [t for t in self._recent_deletes if t >= horizon]
        return len(self._recent_deletes)

    def _held_paths(self) -> list[str]:
        return list((self.halt or {}).get("paths") or [])

    async def resolve_held(self, hold_id: str, action: str) -> dict[str, Any]:
        """The person's answer to a hold. ``delete``: exactly the held files that
        are still missing go to the cloud trash now. ``restore``: they come back
        into the folder from the cloud. ``hold_id`` must name the hold the person
        saw, so a hold that grew since is never confirmed blind."""
        if action not in RESOLVE_ACTIONS:
            raise ValueError(f"unknown action {action!r}")
        if not self.halt:
            return {"resolved": False, "reason": "nothing_held"}
        if hold_id != self.halt.get("hold_id"):
            raise HoldChanged("the held files changed since this choice was offered")
        paths = self._held_paths()
        if action == "delete":
            self._confirmed_deletes = set(paths)
            self._missing_last |= set(paths)  # long missing: no second scan needed
            await self.push_once()
            sent = len([p for p in paths if p not in self.entries])
            return {"resolved": True, "action": "delete", "deleted": sent}
        async with self._lock:
            restored = await self._restore(paths)
        return {"resolved": True, "action": "restore", "restored": restored}

    async def _restore(self, paths: list[str], *, auto: bool = False) -> int:
        """Bring the held files back from the cloud (copy or placeholder, by the
        usual rule) and clear the hold. One file that fails is listed, not fatal."""
        restored = 0
        for rel in paths:
            entry = self.entries.get(rel)
            try:
                if entry is None or await asyncio.to_thread(os.path.lexists, self._path(rel)):
                    continue
                if entry.remote_checksum and not entry.stub and self._wants_mirror(0, entry.remote_updated):
                    placed = await self._place_remote(rel)
                    placed.stub = False
                else:
                    placed = await self._awrite(rel, stub_text(rel, entry.remote_size, entry.remote_updated).encode())
                    placed.stub = True
                placed.remote_checksum, placed.remote_size = entry.remote_checksum, entry.remote_size
                placed.remote_updated = entry.remote_updated
                restored += 1
            except (BridgeError, OSError, ValueError) as exc:
                self._skip(rel, f"could not restore: {exc}")
            self._missing_last.discard(rel)
        self.stats.restored += restored
        if auto:
            self.stats.auto_restored += restored
        logger.warning("cloud files: held deletes resolved by RESTORE (%s files%s)",
                       restored, ", automatically" if auto else "")
        self.halt = None
        self._confirmed_deletes.clear()
        await self.asave()
        return restored

    def _restore_due(self) -> bool:
        since = _parse_time((self.halt or {}).get("since"))
        if since is None:
            return False
        age = (self._now() - since).total_seconds()
        return age >= self.knobs.held_delete_restore_after_seconds

    def _tombstone(self, rel: str, entry: Entry) -> None:
        """Write the delete down BEFORE it is sent (restore from the files trash by this)."""
        self.state_dir.mkdir(parents=True, exist_ok=True)
        line = {"path": rel, "checksum": entry.remote_checksum, "size": entry.remote_size,
                "deleted_at": self._now().isoformat()}
        with open(self.state_dir / "deleted.jsonl", "a") as fh:
            fh.write(json.dumps(line) + "\n")

    async def _upload(self, rel: str, expected: str | None) -> bool:
        """Upload the local file. False (nothing sent) when it is our own placeholder:
        placeholder text never replaces a real cloud file."""
        p = self._path(rel)

        def read() -> tuple[os.stat_result, bytes]:
            # The stat BEFORE the read: an edit landing during the upload then
            # has a newer stat than the one recorded, so the next scan hashes
            # it and uploads it (review 2 N3: a stat taken after the put was
            # recorded against the old bytes and the edit was never synced).
            st = p.stat()
            return st, p.read_bytes()

        st, data = await asyncio.to_thread(read)
        if is_stub_bytes(data):
            self.stats.refused_stub_uploads += 1
            logger.warning("cloud files: %s is a placeholder; not uploaded", rel)
            return False
        self.transfers += 1
        try:
            await self.bridge.put(rel, data, expected)
        finally:
            self.transfers -= 1
        after = await asyncio.to_thread(_sig, p)
        if after != (st.st_size, st.st_mtime_ns, st.st_ino):
            self.stats.changed_during_transfer += 1
            logger.info("cloud files: %s changed during its upload; it uploads again", rel)
        sha = _sha256(data)
        entry = self.entries.get(rel) or Entry()
        entry.local_sha, entry.local_size, entry.local_mtime = sha, st.st_size, st.st_mtime
        entry.remote_checksum, entry.remote_size, entry.stub = sha, len(data), False
        entry.remote_updated = self._now().isoformat()
        self.entries[rel] = entry
        self.stats.uploaded += 1
        return True

    async def _keep_local_as_conflict(self, rel: str) -> str:
        """Move the local bytes to a conflict copy (kept here, uploaded there)."""
        target = conflict_name(rel, self._now(), lambda n: n in self.entries or self._path(n).exists())
        src, dst = self._path(rel), self._path(target)
        await asyncio.to_thread(dst.parent.mkdir, parents=True, exist_ok=True)
        await asyncio.to_thread(os.replace, src, dst)
        await self._upload(target, None)
        self.stats.conflicts += 1
        logger.warning("cloud files: %s changed on both sides; kept local copy as %s", rel, target)
        return target

    async def push_once(self) -> None:
        async with self._lock:
            # The walk and the per-file stat of a large folder on the network
            # drive take minutes cold: never on the event loop (it answers
            # /health — a 12.5k-file folder held a wake at 170 s, 2026-10-18).
            # An unreadable folder raises here: no upload, no delete this pass.
            scan = await asyncio.to_thread(self._scan)
            known = dict(self.entries)
            changed, _ = await asyncio.to_thread(self._classify, scan, known)
            self.pending_uploads = len(changed)
            for rel in changed:
                entry = self.entries.get(rel)
                expected = entry.remote_checksum if entry is not None else None
                sig = await asyncio.to_thread(_sig, self._path(rel))
                refused = self._refused.get(rel)
                if refused is not None and refused[0] == sig:
                    self.pending_uploads = max(0, self.pending_uploads - 1)
                    continue  # refused as it is; tried again once it changes
                try:
                    await self._upload(rel, expected)
                    self._refused.pop(rel, None)
                    self._unskip(rel, "cloud refused", "could not upload")
                except BridgeError as exc:
                    if exc.status in (409, 412):
                        # The cloud copy moved on since our last sync: keep both.
                        await self._keep_local_as_conflict(rel)
                        placed = await self._place_remote(rel)
                        placed.stub = False
                        placed.remote_checksum = placed.local_sha
                    elif exc.status in (401, 403, 429) or exc.status >= 500:
                        raise  # the bridge is down or refusing everything: retry the pass
                    else:
                        # This one file is refused (too big, bad name, quota):
                        # listed, and every other file keeps syncing.
                        self._refused[rel] = (sig, str(exc))
                        self._skip(rel, f"cloud refused it ({exc.status})")
                except OSError as exc:
                    self._skip(rel, f"could not upload: {exc.strerror or exc}")
                finally:
                    self.pending_uploads = max(0, self.pending_uploads - 1)
                await self.asave()
            # Re-scan: a conflict copy made above is new on disk and must never
            # be mistaken for a file the person deleted.
            scan = await asyncio.to_thread(self._scan)
            known = dict(self.entries)
            _, missing = await asyncio.to_thread(self._classify, scan, known)
            approved, held = await asyncio.to_thread(self._gate_deletes, missing, known)
            for rel in approved:
                entry = self.entries[rel]
                if entry.remote_checksum:
                    await asyncio.to_thread(self._tombstone, rel, entry)
                    await self.bridge.delete(rel)
                    self.stats.deleted_remote += 1
                    if rel not in self._confirmed_deletes:
                        self._recent_deletes.append(self._clock())
                self.entries.pop(rel, None)
                self._missing_last.discard(rel)
                await self.asave()
            before = self.halt
            self._set_halt(held)
            if self.halt != before:
                await self.asave()
            if self.halt and self._restore_due():
                # Nobody answered within the window: the folder gets the files
                # back. Never a permanent disagreement, never a silent delete.
                await self._restore(self._held_paths(), auto=True)
            self.stats.last_push_at = self._now().isoformat()

    def _set_halt(self, held: dict[str, Any] | None) -> None:
        if held is None:
            if self.halt is not None:
                logger.warning("cloud files: held deletes cleared (%s)", self.halt.get("reason"))
            self.halt = None
            return
        since = (self.halt or {}).get("since") or self._now().isoformat()
        if self.halt is None or self.halt.get("reason") != held["reason"]:
            logger.error(
                "cloud files: %s local deletes HELD (%s); nothing deleted in the cloud. "
                "The person chooses delete or restore in the app.", held["held"], held["reason"],
            )
            self.stats.deletes_held += held["held"]
        if self.halt and self.halt.get("paths") and held.get("paths") is None:
            held = {**held, "paths": self.halt["paths"], "hold_id": self.halt.get("hold_id")}
        self.halt = {**held, "since": since}

    # ── loop ─────────────────────────────────────────────────────────────
    async def run_forever(self, *, renew: Any = None) -> None:
        self.root.mkdir(parents=True, exist_ok=True)
        next_pull = 0.0
        while True:
            try:
                if renew is not None:
                    await renew()
                if time.monotonic() >= next_pull:
                    wait = await self.pull_once()
                    next_pull = time.monotonic() + wait
                    await asyncio.to_thread(self.evict)
                if self.initial_done:
                    await self.push_once()
                    await self.fill_copies()
                self.stats.last_error = None
            except BridgeError as exc:
                self.stats.last_error = str(exc)
                logger.warning("cloud files sync: %s", exc)
                if exc.retry_after:
                    next_pull = time.monotonic() + exc.retry_after
            except Exception as exc:  # noqa: BLE001 - the loop never dies; it says why
                self.stats.last_error = f"{type(exc).__name__}: {exc}"
                logger.exception("cloud files sync pass failed")
            await asyncio.sleep(max(1, self.knobs.local_scan_seconds))


@dataclass
class MachineFilesSession:
    """The machine token, renewed at half-life through the bridge, kept in the home."""

    bridge: HttpBridge
    state_dir: Path
    sync: CloudFilesSync | None = None
    expires_at: float = 0.0
    organization_id: str | None = None
    renew_error: str | None = None
    _file: Path = field(init=False)

    def __post_init__(self) -> None:
        self._file = self.state_dir / "session.json"
        claims = token_claims(self.bridge.token)
        self.expires_at = float(claims.get("exp") or 0)
        self.organization_id = claims.get("org")
        try:
            stored = json.loads(self._file.read_text())
            if float(stored.get("expires_at") or 0) > self.expires_at:
                self.bridge.token = stored["token"]
                self.expires_at = float(stored["expires_at"])
        except (OSError, ValueError, KeyError):
            pass

    async def renew(self, *, force: bool = False) -> None:
        claims = token_claims(self.bridge.token)
        issued = float(claims.get("iat") or 0)
        half = issued + (self.expires_at - issued) / 2
        if not force and time.time() < half and self.sync is not None and self.sync.knobs_loaded:
            return
        try:
            answer = await self.bridge.session()
        except Exception as exc:  # noqa: BLE001
            self.renew_error = str(exc)[:300]
            if time.time() > self.expires_at:
                raise
            return
        self.renew_error = None
        self.bridge.token = answer["token"]
        self.expires_at = float(answer.get("expires_at") or token_claims(answer["token"]).get("exp") or 0)
        self.organization_id = answer.get("organization_id") or self.organization_id
        self.state_dir.mkdir(parents=True, exist_ok=True)
        tmp = self._file.with_suffix(".tmp")
        tmp.write_text(json.dumps({"token": self.bridge.token, "expires_at": self.expires_at}))
        os.chmod(tmp, 0o600)
        os.replace(tmp, self._file)
        if self.sync is not None:
            self.sync.knobs = SyncKnobs.from_mapping(answer.get("knobs"))
            self.sync.knobs_loaded = True


def start_sync(*, token: str, url: str, home: Path) -> tuple[CloudFilesSync, MachineFilesSession] | None:
    """Build the sync when the launch carried a machine files token; else None (says why)."""
    if not token or not url:
        logger.warning("cloud files sync off: MATRX_CLOUD_FILES_TOKEN/MATRX_CLOUD_FILES_URL not set")
        return None
    state_dir = home / STATE_DIR_NAME
    bridge = HttpBridge(url, token)
    session = MachineFilesSession(bridge=bridge, state_dir=state_dir)
    sync = CloudFilesSync(home / "Cloud", bridge, state_dir=state_dir)
    session.sync = sync
    return sync, session
