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
import shutil
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta, UTC
from pathlib import Path
from typing import Any, Protocol

logger = logging.getLogger(__name__)

STUB_MAGIC = "MATRX CLOUD FILE - not downloaded yet"
STATE_DIR_NAME = ".matrx/cloud-sync"
#: The feed the state's cursor belongs to. THE device feed (``/cloud-files/sync/changes``,
#: matrx-files ``sync_feed``): opaque ``(updated_at, id)`` keyset + relocation ledger. A state
#: written against the old ``/cloud-files/changes`` timestamp cursor re-bootstraps once.
FEED_NAME = "sync_v2"
#: Where the state keeps THE feed's opaque cursor. Never the ``cursor`` key: an older image
#: (rollback) reads ``cursor`` as an ISO ``since`` for the legacy feed; an opaque value there
#: answered 400 and stopped its pull AND its push (review 2026-11-02, defect 7). ``cursor``
#: carries an ISO watermark (the newest ``updated_at`` applied) that an older image can use.
FEED_CURSOR_KEY = "feed_cursor"
#: Files set aside by id while another cloud file took their path (``parked/``, in the state dir).
PARKED_DIR_NAME = "parked"
#: Page size asked of the feed.
FEED_PAGE = 500
#: Of the final flush's budget, at most this much is kept to count what is left and answer
#: (the rest uploads). The stop's transport waits only a small margin past the budget.
FLUSH_ANSWER_RESERVE_SECONDS = 10.0
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
#: ``BridgeError.status`` of a put the bridge answered without naming a cloud row: refused
#: for this file only (listed in ``skipped``), never recorded as synced.
UNCONFIRMED_UPLOAD = 424
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
    #: The final flush before a stop (save-before-stop, SIGTERM) waits at most this
    #: long for local changes to reach the cloud; past it the stop goes ahead and
    #: says how many were left (they upload on the next start, never lost).
    final_flush_seconds: int = 90
    #: How many changed files one pass uploads at once. One at a time, a stop's final flush
    #: spent its whole budget on round trips and left 8-27 files waiting (2026-11-20).
    upload_concurrency: int = 8

    @classmethod
    def from_mapping(cls, data: dict[str, Any] | None) -> SyncKnobs:
        base = cls()
        for key in base.__dataclass_fields__:
            value = (data or {}).get(key)
            if isinstance(value, int) and not isinstance(value, bool) and value >= 0:
                setattr(base, key, value)
        return base


class BridgeError(RuntimeError):
    def __init__(
        self, status: int, body: Any = None, retry_after: float | None = None, path: str | None = None,
    ) -> None:
        super().__init__(f"cloud-files bridge answered {status}: {str(body)[:300]}")
        self.status = status
        #: The one cloud path the failed call was about (None when it named none): lets a pass tell
        #: "this one file is gone" from "the bridge is down".
        self.path = path
        self.body = body
        self.retry_after = retry_after


class Bridge(Protocol):
    async def sync_changes(self, cursor: str | None, limit: int) -> dict[str, Any]: ...
    async def get(self, path: str) -> bytes: ...
    async def put(self, path: str, content: bytes, expected_checksum: str | None) -> dict[str, Any]: ...
    async def delete(self, path: str) -> None: ...
    async def session(self) -> dict[str, Any]: ...
    #: Optional. The file service's answer for ONE path (see ``HttpBridge.still_visible``):
    #: True = a live file its owner can open, False = no such file (trashed, moved away, never
    #: there), None = it could not say. A bridge without it answers None: nothing is removed.
    # async def still_visible(self, path: str) -> bool | None: ...


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
            named = (kw.get("params") or {}).get("path") or (kw.get("data") or {}).get("file_path")
            raise BridgeError(
                resp.status_code, body, float(retry) if retry and retry.isdigit() else None,
                path=str(named) if named else None,
            )
        return resp

    async def sync_changes(self, cursor: str | None, limit: int) -> dict[str, Any]:
        """THE device feed: ``cursor`` None = bootstrap; store ``next_cursor`` as given."""
        params: dict[str, Any] = {"limit": limit}
        if cursor:
            params["cursor"] = cursor
        return (await self._call("GET", "/cloud-files/sync/changes", params=params)).json()

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

    async def still_visible(self, path: str) -> bool | None:
        """Ask the file service whether ``path`` is a live file this machine's owner can open.

        The bridge's ``/get`` runs the canonical access gate on the path across every
        organization. Only the status line is read (the bytes are never downloaded):
        200 = visible; a plain 404 = no live file there (trashed, moved away); anything else
        (a 404 for missing storage bytes, 403, 5xx, a network error) = unknown -> None, and
        an unknown answer never removes a local file."""
        try:
            async with self._client.stream(
                "GET", f"{self._base}/cloud-files/get", params={"path": path}, headers=self._headers()
            ) as resp:
                if resp.status_code == 200:
                    return True
                if resp.status_code != 404:
                    return None
                body = (await resp.aread())[:2000]
        except Exception:  # noqa: BLE001 — unknown, never "gone"
            return None
        try:
            detail = json.loads(body).get("detail")
        except (ValueError, AttributeError):
            return None
        if isinstance(detail, dict):
            return None  # e.g. storage_object_missing: the row exists; this copy may be the last
        return False


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
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=UTC)


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
    #: The cloud file's id: identity. The same id at another path is a MOVE.
    file_id: str | None = None
    #: A local file this sync found at a path where a cloud file it does not manage lives
    #: (THE feed leaves that file out: a dot folder, a crawl capture). Recorded as found,
    #: never uploaded as found: only an edit made after this record uploads (as a conflict
    #: copy beside the cloud file). ``local_*`` is that first sight; ``remote_*`` is empty.
    unmanaged: bool = False


@dataclass
class SyncStats:
    downloaded: int = 0
    stubbed: int = 0
    hydrated: int = 0
    uploaded: int = 0
    deleted_local: int = 0
    #: Local files a feed or bootstrap did not list but the file service still shows (or could
    #: not answer for): kept, never removed for being left out of a listing.
    kept_unlisted: int = 0
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
    #: Moves that arrived by file id (renamed here, never re-downloaded).
    relocated: int = 0
    #: Pull and push fail separately (a feed outage never stops uploads).
    last_pull_error: str | None = None
    last_push_error: str | None = None
    #: Passes in a row where the pull or the push failed; 0 = healthy.
    consecutive_failures: int = 0
    #: When the current run of failures began (None = healthy): "sync paused since".
    failing_since: str | None = None


async def _bounded_each(items: list[str], fn: Any, limit: int) -> None:
    """Run ``fn(item)`` for every item, at most ``limit`` at once. The first failure cancels the
    rest and is raised as itself (never wrapped in a group): the caller's ``except BridgeError``
    still decides whether the pass pauses."""
    if not items:
        return
    queue = list(reversed(items))

    async def worker() -> None:
        while queue:
            await fn(queue.pop())

    tasks = [asyncio.create_task(worker()) for _ in range(min(limit, len(items)))]
    try:
        done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_EXCEPTION)
    except BaseException:
        for t in tasks:
            t.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)
        raise
    for t in pending:
        t.cancel()
    if pending:
        await asyncio.gather(*pending, return_exceptions=True)
    for t in done:
        if not t.cancelled() and t.exception() is not None:
            raise t.exception()


def _bridge_down(exc: BridgeError) -> bool:
    """The bridge is down or refusing everything: the pass must retry, not skip one file."""
    return exc.status in (401, 429) or exc.status >= 500


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
        self._now = now or (lambda: datetime.now(UTC))
        #: The feed's opaque cursor; None = bootstrap (the whole current tree).
        self.cursor: str | None = None
        #: Paths the running bootstrap delivered (None = not bootstrapping). When it drains,
        #: a clean local copy the cloud no longer has at that path leaves (a file moved or
        #: deleted while the old feed could not say so). Persisted across restarts.
        self._bootstrap_seen: set[str] | None = None
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
        #: retried until the file changes. Persisted: a new task (every wake) used
        #: to re-send each refused file once more (319 crawl captures, 2026-11-02).
        self._refused: dict[str, tuple[Any, str]] = {}
        #: Cloud rows that failed to apply; retried next pull (the cursor moved on).
        self._retry_rows: dict[str, dict[str, Any]] = {}
        #: When each recent delete was sent (epoch seconds), for the window cap.
        #: Persisted: a worker restart never resets the window (review 3 D4).
        self._recent_deletes: list[float] = []
        self._clock = time.time
        #: Held files a restore could not bring back (review 3 D1): they stay held
        #: and are retried; they never become a cloud delete unless the person
        #: confirms that exact hold. Persisted.
        self._unrestored: set[str] = set()
        #: Work in flight, for the machine's activity reading (never stop mid-transfer).
        self.pending_uploads = 0
        self.unsent_after_push: list[str] | None = None
        #: The final flush's arrival, on THIS machine's monotonic clock, and whether a pass that
        #: STARTED after it (so its scan saw every write made before the stop) finished with nothing
        #: waiting, no failures and no held delete. Status reports it; the server never compares clocks.
        self.flush_requested_mono: float | None = None
        self.clean_since_flush_request = False
        #: Wall time (this machine) taken just before the qualifying pass's closing scan: a file
        #: changed after it was not seen by that pass.
        self._clean_scan_wall: float | None = None
        self.transfers = 0
        #: file id -> local path, a cache of ``entries`` (validated on every read).
        self._by_id: dict[str, str] = {}
        #: Files this folder holds whose path another cloud file took before their own change
        #: arrived (a swap through a temp name, a move onto a path a delete freed): set aside
        #: by file id, outside the folder, until the feed says where they went. file id ->
        #: {"rel": the path they left, "entry": their Entry, "name": the parked file}.
        #: A parked file the drained feed never re-placed is gone in the cloud: a clean copy
        #: or placeholder leaves; one edited here comes back as a conflict copy. Persisted.
        self._parked: dict[str, dict[str, Any]] = {}
        #: The newest ``updated_at`` applied: the ``cursor`` an older image reads on rollback.
        self._watermark: str | None = None
        self._lock = asyncio.Lock()
        self._save_lock = asyncio.Lock()
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
        legacy = data.get("cursor")
        if _parse_time(legacy) is not None:
            self._watermark = str(legacy)
        if data.get("feed") == FEED_NAME:
            # The first image of THE feed wrote its opaque cursor into ``cursor``: still honored.
            self.cursor = data.get(FEED_CURSOR_KEY) or (
                legacy if legacy and _parse_time(legacy) is None else None)
            seen = data.get("bootstrap_seen")
            self._bootstrap_seen = set(seen) if isinstance(seen, list) else None
        else:
            # A cursor of the old timestamp feed: it skipped rows that shared a timestamp
            # and never saw moves. Bootstrap THE feed once and reconcile against it.
            self.cursor = None
        self.initial_done = bool(data.get("initial_done"))
        self.halt = data.get("halt") or None
        self._retry_rows = {r["file_path"]: r for r in (data.get("retry") or []) if r.get("file_path")}
        self._recent_deletes = [float(t) for t in (data.get("recent_deletes") or [])]
        self._unrestored = set(data.get("unrestored") or [])
        self._parked = {str(k): v for k, v in (data.get("parked") or {}).items() if isinstance(v, dict)}
        for rel, raw in (data.get("refused") or {}).items():
            sig, why = raw.get("sig"), str(raw.get("why") or "")
            if isinstance(sig, list) and len(sig) == 3:
                self._refused[rel] = (tuple(sig), why)
                # Listed as before the restart: still refused, never "waiting to upload".
                self.skipped[rel] = why
        for rel, raw in (data.get("files") or {}).items():
            self.entries[rel] = Entry(**{k: v for k, v in raw.items() if k in Entry.__dataclass_fields__})

    def _payload(self) -> dict[str, Any]:
        return {
            "feed": FEED_NAME,
            FEED_CURSOR_KEY: self.cursor,
            # ISO only (or absent): what an older image sends as ``since`` after a rollback.
            "cursor": self._watermark,
            "bootstrap_seen": sorted(self._bootstrap_seen) if self._bootstrap_seen is not None else None,
            "initial_done": self.initial_done,
            "halt": self.halt,
            "retry": list(self._retry_rows.values()),
            "recent_deletes": list(self._recent_deletes),
            "unrestored": sorted(self._unrestored),
            "parked": self._parked,
            "refused": {rel: {"sig": list(sig) if sig else None, "why": why}
                        for rel, (sig, why) in sorted(self._refused.items())},
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
        # One writer at a time (uploads run side by side and each saves): two threads sharing
        # the one temp file would race on its rename. The snapshot is taken inside the lock, so
        # the last write holds the newest state.
        async with self._save_lock:
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
            # Sync health, for the server's status ("sync paused since …") and alerts.
            "last_pull_at": self.stats.last_pull_at,
            "last_push_at": self.stats.last_push_at,
            "last_error": self.stats.last_error,
            "consecutive_failures": self.stats.consecutive_failures,
            "failing_since": self.stats.failing_since,
            # A first mirror or a re-read of the whole tree (a bootstrap) is running: the
            # server says "syncing", never "up to date", while the folder is still filling.
            "first_sync_running": (not self.initial_done) or self.cursor is None
                                  or self._bootstrap_seen is not None,
            "parked": len(self._parked),
            "clean_since_flush_request": self.clean_since_flush_request,
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
    def _path_of(self, file_id: str) -> str | None:
        """The local path holding cloud file ``file_id`` (None when none does)."""
        rel = self._by_id.get(file_id)
        if rel is not None and (self.entries.get(rel) or Entry()).file_id == file_id:
            return rel
        for rel, entry in self.entries.items():  # index stale: one scan, then cached
            if entry.file_id == file_id:
                self._by_id[file_id] = rel
                return rel
        return None

    # ── identity: every apply decision is by file id ─────────────────────
    @property
    def _parked_dir(self) -> Path:
        return self.state_dir / PARKED_DIR_NAME

    def _local_dirty(self, p: Path, entry: Entry) -> bool:
        """The file at ``p`` holds bytes the person or an agent wrote (not what the last sync
        left, and never our own placeholder text)."""
        try:
            data = p.read_bytes()
        except FileNotFoundError:
            return False
        if is_stub_bytes(data):
            return False
        return _sha256(data) != entry.local_sha

    async def _set_aside_as_conflict(self, rel: str, src: Path | None = None) -> str:
        """Move local bytes to a conflict copy beside ``rel``, here only: the next push
        uploads it as a new file. No network in the middle of an apply, so an upload that
        fails can never leave the sync half-moved (defect 3)."""
        target = conflict_name(rel, self._now(), lambda n: n in self.entries or self._path(n).exists())
        source, dst = src or self._path(rel), self._path(target)

        def move() -> None:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(source), str(dst))

        await asyncio.to_thread(move)
        self.stats.conflicts += 1
        logger.warning("cloud files: %s was edited here and left that path in the cloud; kept as %s", rel, target)
        return target

    async def _park(self, rel: str) -> None:
        """The cloud gave ``rel`` to another file while the copy here (known by its file id)
        had not yet been told where it went: set it aside by id, never upload it as a
        conflict and never delete it yet (review defects 1 and 4)."""
        entry = self.entries[rel]
        assert entry.file_id
        src = self._path(rel)
        if not await asyncio.to_thread(os.path.lexists, src):
            self.entries.pop(rel, None)
            self._missing_last.discard(rel)
            return
        name = hashlib.sha256(entry.file_id.encode()).hexdigest()[:32]
        dst = self._parked_dir / name

        def move() -> None:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(src), str(dst))

        await asyncio.to_thread(move)
        self._parked[entry.file_id] = {"rel": rel, "entry": dict(entry.__dict__), "name": name}
        self.entries.pop(rel, None)
        self._missing_last.discard(rel)
        self._retry_rows.pop(rel, None)
        await self.asave()

    async def _unpark(self, file_id: str, rel: str) -> None:
        """A parked file's new path arrived: it goes there (local edits travel with it)."""
        info = self._parked[file_id]
        src, dst = self._parked_dir / str(info["name"]), self._path(rel)
        await self._make_room(rel, file_id)

        def move() -> bool:
            if not os.path.lexists(src):
                return False
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(src), str(dst))
            return True

        moved = await asyncio.to_thread(move)
        del self._parked[file_id]
        if moved:
            entry = Entry(**{k: v for k, v in dict(info["entry"]).items() if k in Entry.__dataclass_fields__})
            self.entries[rel] = entry
            self._by_id[file_id] = rel
            self.stats.relocated += 1
        await self.asave()

    async def _settle_parked(self, file_id: str) -> None:
        """A parked file is gone in the cloud (its own tombstone said so): a clean copy or placeholder leaves; bytes edited here come back as a
        conflict copy beside the path they left, and the next push uploads them."""
        info = self._parked[file_id]
        src = self._parked_dir / str(info["name"])
        entry = Entry(**{k: v for k, v in dict(info["entry"]).items() if k in Entry.__dataclass_fields__})
        if await asyncio.to_thread(os.path.lexists, src):
            if await asyncio.to_thread(self._local_dirty, src, entry):
                await self._set_aside_as_conflict(str(info["rel"]), src)
            else:
                await asyncio.to_thread(src.unlink, missing_ok=True)
                self.stats.deleted_local += 1
        del self._parked[file_id]
        await self.asave()

    async def _make_room(self, rel: str, incoming_id: str | None) -> None:
        """Another cloud file (``incoming_id``) now owns ``rel``: whatever is here goes aside
        first. A copy known by a DIFFERENT file id is parked (its own change says where it
        went); a placeholder or a clean copy of unknown identity leaves; local bytes the
        cloud never had become a conflict copy (never lost)."""
        entry = self.entries.get(rel)
        if entry is not None and incoming_id and entry.file_id == incoming_id:
            return
        if entry is not None and entry.file_id:
            await self._park(rel)
            return
        p = self._path(rel)
        if not await asyncio.to_thread(os.path.lexists, p):
            if entry is not None:
                self.entries.pop(rel, None)
                self._missing_last.discard(rel)
            return
        if entry is None:
            found = await asyncio.to_thread(self._unknown_local, rel)
            dirty = found is not None and not is_stub_bytes(found[0])
        else:
            dirty = await asyncio.to_thread(self._local_dirty, p, entry)
        if dirty:
            await self._set_aside_as_conflict(rel)
        else:
            await asyncio.to_thread(p.unlink, missing_ok=True)
        self.entries.pop(rel, None)
        self._missing_last.discard(rel)

    async def _relocate(self, old: str, new: str) -> None:
        """The cloud moved a file this folder holds from ``old`` to ``new``: move it here too
        (local edits travel with it), never download it again and never leave the old path.
        Transactional (defect 3): the old path's record is dropped only once the file is at
        ``new``; a failure leaves it exactly where it was, and the row is retried."""
        entry = self.entries[old]
        src, dst = self._path(old), self._path(new)
        if not await asyncio.to_thread(os.path.lexists, src):
            self.entries.pop(old, None)
            self._missing_last.discard(old)
            return  # gone here already: the cloud's file arrives at ``new`` the normal way
        await self._make_room(new, entry.file_id)

        def move() -> None:
            dst.parent.mkdir(parents=True, exist_ok=True)
            os.replace(src, dst)
            root = self.root.resolve()
            parent = src.parent
            while parent != root and root in parent.parents:
                try:
                    parent.rmdir()  # only an EMPTY folder the move left behind
                except OSError:
                    break
                parent = parent.parent

        await asyncio.to_thread(move)
        self.entries.pop(old, None)
        self._missing_last.discard(old)
        self._retry_rows.pop(old, None)
        self.entries[new] = entry
        if entry.file_id:
            self._by_id[entry.file_id] = new
        self.stats.relocated += 1
        logger.info("cloud files: %s moved to %s in the cloud; moved here too", old, new)

    async def apply_remote(self, row: dict[str, Any]) -> None:
        rel = str(row.get("file_path") or "").lstrip("/")
        file_id = str(row.get("file_id") or "") or None
        visible = bool(rel) and not rel.startswith(SYSTEM_ROOTS)
        if file_id and file_id in self._parked:
            if row.get("deleted") or not visible:
                await self._settle_parked(file_id)
                return
            await self._unpark(file_id, rel)
        if file_id:
            held = self._path_of(file_id)
            if row.get("deleted"):
                if held is not None:
                    rel = held  # the file left (moved out of view, or deleted): the copy WE hold goes
                else:
                    occupant = self.entries.get(rel)
                    if occupant is None or occupant.file_id:
                        # A tombstone only removes the copy this machine holds: a file of
                        # another id at that path (another organization's row, a file that
                        # took the path since) is never touched (defect 2).
                        return
                    if not row.get("checksum") or row.get("checksum") != occupant.remote_checksum:
                        # An entry without a file id (old feed state, an unconfirmed upload):
                        # only a tombstone for the exact bytes the cloud gave or took from
                        # this machine removes it — never another file's tombstone at the path.
                        return
            elif held is not None and held != rel:
                if visible:
                    await self._relocate(held, rel)
                else:
                    rel, row = held, {**row, "deleted": True}  # moved into a system path: gone here
            elif held is None and visible:
                occupant = self.entries.get(rel)
                if occupant is not None and occupant.file_id and occupant.file_id != file_id:
                    await self._make_room(rel, file_id)  # the copy here is another file: aside
        if not rel or rel.startswith(SYSTEM_ROOTS):
            return
        await self._apply_at(rel, row)
        if file_id and not row.get("deleted") and rel in self.entries:
            self.entries[rel].file_id = file_id
            self._by_id[file_id] = rel

    async def _apply_at(self, rel: str, row: dict[str, Any]) -> None:
        entry = self.entries.get(rel)
        if entry is not None and entry.unmanaged:
            # The feed now speaks for this path. What sits here was never the cloud's file:
            # judged like an unknown local file (same bytes adopt; other bytes become a
            # conflict copy; a tombstone never takes them), never overwritten.
            self.entries.pop(rel, None)
            self._unskip(rel, "a cloud file this sync does not manage")
            if row.get("deleted"):
                return
            entry = None
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
                if row.get("gone_reason") == "no_longer_visible":
                    # Changed here, and the cloud file is one the owner can no longer see
                    # (its organization was archived, or access was lost): a push at this
                    # path would land on that file. The edit is kept as its OWN new file
                    # (a conflict copy, saved in this machine's organization), never lost.
                    self.entries.pop(rel, None)
                    await self._keep_local_as_conflict(rel)
                    return
                # Changed here, deleted there: keep the local edit; the next push re-creates it.
                # The cloud file it was is gone, so these bytes no longer carry its id: a file
                # that takes this path next sets them aside as a conflict copy instead of
                # parking them to wait for a change of a file that will never come.
                entry.remote_checksum = None
                if entry.file_id:
                    self._by_id.pop(entry.file_id, None)
                entry.file_id = None
                return
            if row.get("gone_reason") == "no_longer_visible":
                logger.info("cloud files: %s is no longer visible to this machine's owner; removed", rel)
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
        """Apply every cloud change since the cursor (THE device feed: keyset + moves).
        Returns the server's poll hint."""
        hint = self.knobs.remote_poll_seconds
        async with self._lock:
            for row in list(self._retry_rows.values()):
                await self._apply_one(row)
            if self.cursor is None and self._bootstrap_seen is None:
                self._bootstrap_seen = set()
            while True:
                page = await self.bridge.sync_changes(self.cursor, FEED_PAGE)
                rows = page.get("files") or []
                for row in rows:
                    self._advance_watermark(row.get("updated_at"))
                    if self._bootstrap_seen is not None and not row.get("deleted"):
                        self._bootstrap_seen.add(str(row.get("file_path") or "").lstrip("/"))
                    await self._apply_one(row)
                hint = int(page.get("poll_after_seconds") or hint)
                nxt = page.get("next_cursor")
                if not nxt:
                    raise BridgeError(502, "the change feed answered without a cursor")
                advanced = nxt != self.cursor
                self.cursor = nxt
                await self.asave()
                if not page.get("has_more") or not advanced:
                    break
            # A parked file leaves only by its own tombstone (``apply_remote``); one the drained
            # feed has not placed again stays parked (its move may not be served yet), never
            # removed for being left out.
            if self._bootstrap_seen is not None:
                await self._reconcile_bootstrap(self._bootstrap_seen)
                self._bootstrap_seen = None
            self.initial_done = True
            self.stats.last_pull_at = self._now().isoformat()
            await self.asave()
        return max(5, min(hint, 600))

    def _advance_watermark(self, value: Any) -> None:
        when = _parse_time(value)
        if when is not None and (self._watermark is None or when > (_parse_time(self._watermark) or when)):
            self._watermark = when.isoformat()

    async def _reconcile_bootstrap(self, seen: set[str]) -> None:
        """The bootstrap drained without delivering some paths this folder holds (entries
        without a file id: written against the old feed, or an upload the cloud never
        confirmed). Being left out of a listing is NEVER a removal: THE feed omits rows on
        purpose (dot folders like ``.matrx-tmp/``, crawl captures, rows stamped in its last
        10 s), so a file can be alive, visible to its owner, and absent from the bootstrap
        (carry-over gate 2026-11-02: 12 such files were wiped on an upgrade). Nor is "no live
        file at this path" enough: an entry without a file id never proves the cloud HELD these
        bytes (gate 2026-11-02, third run: 20 conflict copies whose uploads made no row were
        removed on a 404). Each such file stays exactly as it is; a later tombstone for these
        exact bytes, or the person, removes it."""
        stale = [r for r, e in self.entries.items()
                 if r not in seen and r not in self._retry_rows and not e.file_id]
        for rel in stale:
            entry = self.entries[rel]
            try:
                exists = await asyncio.to_thread(os.path.lexists, self._path(rel))
                if exists and await self._achanged(rel, entry):
                    entry.remote_checksum = None  # the next push re-creates it
                    continue
            except (OSError, ValueError) as exc:
                self._skip(rel, f"could not reconcile: {exc}")
                continue
            if exists:
                self.stats.kept_unlisted += 1
                logger.info("cloud files: %s was not in the feed's listing; kept as it is", rel)
                continue
            self.entries.pop(rel, None)  # gone on both sides
            self._missing_last.discard(rel)

    async def _still_visible(self, rel: str) -> bool | None:
        """The file service's answer for one path; None when the bridge cannot say."""
        ask = getattr(self.bridge, "still_visible", None)
        if ask is None:
            return None
        try:
            return await ask(rel)
        except Exception:  # noqa: BLE001 — unknown, never "gone"
            return None

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
            try:
                hydrated = await self.hydrate(rel)
            except BridgeError as exc:
                if _bridge_down(exc):
                    raise  # the bridge is down or refusing everything: retry the pass
                # This one cloud file cannot be read right now (gone since the feed listed it,
                # its stored bytes missing, 403): it stays a placeholder, listed, and every
                # other copy keeps filling. One unreadable file used to fail the whole push
                # pass every few seconds, so the machine reported "Cloud folder sync has been
                # paused" for good (2026-11-14, a 404 on one library PDF).
                entry.want_copy = False
                self._skip(rel, f"cloud could not give it ({exc.status})")
                logger.warning("cloud files: %s could not be copied in (%s); it stays a placeholder", rel, exc.status)
                continue
            if hydrated:
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
        both = now_missing & self._missing_last
        self._missing_last = now_missing
        # A file a restore could not bring back is never a delete candidate: only
        # the person's confirmation of that exact hold lets it through (D1).
        self._unrestored -= {r for r in both if r in self._confirmed_deletes}
        # Leaves the unrestored set ONLY when verified back: a regular file on
        # disk, or no longer a known file (gone from the cloud). A path that is
        # merely "not missing" (a folder or a link where the file belongs, an
        # unreadable entry) is NOT back: it stays held, so removing the blocker
        # later never turns it into a cloud delete (live 2026-10-22, f03/f04).
        self._unrestored = {
            r for r in self._unrestored
            if r in now_missing or (r in known and not self._is_regular_file(r))
        }
        pending = sorted(self._unrestored)
        seen_twice = sorted(both - self._unrestored)
        if not seen_twice and now_missing and self.halt:
            # A new process after a hold: keep holding while it re-confirms.
            return [], {k: v for k, v in self.halt.items() if k != "since"}
        confirmed = [r for r in seen_twice if r in self._confirmed_deletes]
        candidates = [r for r in seen_twice if r not in self._confirmed_deletes]
        self._confirmed_deletes &= now_missing
        def hold(reason: str, sample: list[str], **extra: Any) -> dict[str, Any]:
            paths = candidates + pending
            return {"reason": reason, "held": len(paths), "sample": sample[:5],
                    "paths": paths, "hold_id": hold_id_for(paths), **extra}

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
        if pending:
            # The allowed ones go now; the files a restore could not bring back stay held.
            return confirmed + candidates, {
                "reason": "restore_failed", "held": len(pending), "sample": pending[:5],
                "paths": pending, "hold_id": hold_id_for(pending)}
        return confirmed + candidates, None

    def _is_regular_file(self, rel: str) -> bool:
        """A real file (not a link, folder or anything else) is at ``rel``."""
        try:
            p = self._path(rel)
            return not p.is_symlink() and p.is_file()
        except (OSError, ValueError):
            return False

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
        usual rule). One file that fails is listed, not fatal, and STAYS HELD
        (``restore_failed``): it is retried every pass and never becomes a cloud
        delete without the person (review 3 D1). The hold clears only when every
        held file is back."""
        restored = 0
        failed: list[str] = []
        for rel in paths:
            entry = self.entries.get(rel)
            try:
                if entry is None:
                    continue  # no longer a cloud file: nothing to restore, nothing to delete
                if await asyncio.to_thread(os.path.lexists, self._path(rel)):
                    if await asyncio.to_thread(self._is_regular_file, rel):
                        continue  # a regular file is there: it syncs as an edit, never a delete
                    # A folder, link or anything else sits where the file belongs:
                    # NOT restored. It stays held and is retried (never "skipped").
                    raise FileExistsError(f"{rel} is blocked by something that is not a file")
                await self._restore_one(rel, entry)
                if not await asyncio.to_thread(self._is_regular_file, rel):
                    raise FileNotFoundError(f"{rel} is not on disk after the restore")
                restored += 1
                self._unskip(rel, "could not restore")
            except Exception as exc:  # noqa: BLE001 - ANY restore that did not put the file back stays held
                self._skip(rel, f"could not restore: {exc}")
                failed.append(rel)
            self._missing_last.discard(rel)
        self.stats.restored += restored
        if auto:
            self.stats.auto_restored += restored
        logger.warning("cloud files: held deletes resolved by RESTORE (%s files%s, %s still held)",
                       restored, ", automatically" if auto else "", len(failed))
        self._unrestored = (self._unrestored - set(paths)) | set(failed)
        self._confirmed_deletes.clear()
        if failed:
            since = (self.halt or {}).get("since") or self._now().isoformat()
            self.halt = {"reason": "restore_failed", "held": len(failed), "sample": failed[:5],
                         "paths": failed, "hold_id": hold_id_for(failed), "since": since}
        else:
            self.halt = None
        await self.asave()
        return restored

    async def _restore_one(self, rel: str, entry: Entry) -> None:
        """Put one known cloud file back at ``rel`` (copy or placeholder by the usual rule)."""
        if entry.remote_checksum and not entry.stub and self._wants_mirror(0, entry.remote_updated):
            placed = await self._place_remote(rel)
            placed.stub = False
        else:
            placed = await self._awrite(rel, stub_text(rel, entry.remote_size, entry.remote_updated).encode())
            placed.stub = True
        placed.remote_checksum, placed.remote_size = entry.remote_checksum, entry.remote_size
        placed.remote_updated = entry.remote_updated

    async def _placeholder_for_unreadable(self, rel: str, entry: Entry | None, status: int) -> None:
        """The cloud file cannot be read right now (404/403...): leave a listed placeholder
        in its place, never a hole (a hole reads as "the person deleted it"), and never fail
        the pass. Same per-file rule as ``fill_copies``."""
        size = entry.remote_size if entry is not None else 0
        updated = entry.remote_updated if entry is not None else None
        placed = await self._awrite(rel, stub_text(rel, size, updated).encode())
        placed.stub, placed.want_copy = True, False
        if entry is not None:
            placed.remote_checksum = entry.remote_checksum
        placed.remote_size, placed.remote_updated = size, updated
        self._skip(rel, f"cloud could not give it ({status})")
        logger.warning("cloud files: %s could not be copied in (%s); it stays a placeholder", rel, status)

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
            answer = await self.bridge.put(rel, data, expected)
        finally:
            self.transfers -= 1
        if not (isinstance(answer, dict) and answer.get("id")):
            # No cloud row named in the answer: nothing proves the cloud holds these bytes.
            # Never recorded as synced (a synced record is what lets a later "gone there"
            # remove the local file); the file stays, listed, and is retried once it changes.
            raise BridgeError(UNCONFIRMED_UPLOAD, {"error": "upload_not_confirmed", "answer": answer})
        after = await asyncio.to_thread(_sig, p)
        if after != (st.st_size, st.st_mtime_ns, st.st_ino):
            self.stats.changed_during_transfer += 1
            logger.info("cloud files: %s changed during its upload; it uploads again", rel)
        sha = _sha256(data)
        entry = self.entries.get(rel) or Entry()
        entry.local_sha, entry.local_size, entry.local_mtime = sha, st.st_size, st.st_mtime
        entry.remote_checksum, entry.remote_size, entry.stub = sha, len(data), False
        entry.remote_updated = self._now().isoformat()
        if isinstance(answer, dict) and answer.get("id"):
            entry.file_id = str(answer["id"])
            self._by_id[entry.file_id] = rel
        self.entries[rel] = entry
        self.stats.uploaded += 1
        return True

    async def _leave_unmanaged(self, rel: str) -> bool:
        """A local file the sync state does not know, at a path where the file service shows a
        live cloud file THE feed never delivered (it does not manage it: a dot folder, a crawl
        capture). Its bytes are not known to be an edit of that file — they may be what an
        older sync or another writer left — so they are recorded as found and NOT uploaded
        (carry-over gate 2026-11-02: a wake uploaded 40 "conflict" copies of crawl captures
        nobody had edited). True = recorded and left as it is. A later edit uploads."""
        if await self._still_visible(rel) is not True:
            return False  # no cloud file there (or no answer): a new local file uploads as before
        found = await asyncio.to_thread(self._unknown_local, rel)
        if found is None:
            return True
        entry = Entry(unmanaged=True)
        self._adopt(rel, entry, found[0], found[1])
        self.entries[rel] = entry
        self.stats.kept_unlisted += 1
        self._skip(rel, "a cloud file this sync does not manage has this path; kept here as it is, not uploaded")
        return True

    async def _keep_local_as_conflict(self, rel: str) -> str:
        """Move the local bytes to a conflict copy (kept here, uploaded there)."""
        target = conflict_name(rel, self._now(), lambda n: n in self.entries or self._path(n).exists())
        src, dst = self._path(rel), self._path(target)
        await asyncio.to_thread(dst.parent.mkdir, parents=True, exist_ok=True)
        await asyncio.to_thread(os.replace, src, dst)
        self.stats.conflicts += 1
        try:
            await self._upload(target, None)
        except BridgeError as exc:
            if exc.status in (401, 429) or exc.status >= 500:
                raise
            # The copy stays here, unrecorded (a new local file): never removed, retried by
            # the next push, listed until the cloud takes it.
            self._skip(target, f"cloud refused it ({exc.status})")
            logger.warning("cloud files: %s changed on both sides; kept local copy as %s "
                           "(the cloud has not taken it: %s)", rel, target, exc.status)
            return target
        logger.warning("cloud files: %s changed on both sides; kept local copy as %s", rel, target)
        return target

    async def _push_one(self, rel: str) -> None:
        """Send one changed file (or record why not). Raises only when the bridge is down."""
        entry = self.entries.get(rel)
        sig = await asyncio.to_thread(_sig, self._path(rel))
        refused = self._refused.get(rel)
        if refused is not None and refused[0] == sig:
            # Refused as it is; tried again once it changes. Checked BEFORE the
            # file service is asked about the path: a pass used to make one GET per
            # refused file (319 crawl captures on 2026-11-02), and a new file waited
            # behind all of them (161 s machine -> cloud).
            self.pending_uploads = max(0, self.pending_uploads - 1)
            return
        if entry is None and await self._leave_unmanaged(rel):
            self.pending_uploads = max(0, self.pending_uploads - 1)
            await self.asave()
            return
        expected = entry.remote_checksum if entry is not None else None
        try:
            await self._upload(rel, expected)
            self._refused.pop(rel, None)
            self._unskip(rel, "cloud refused", "could not upload")
        except BridgeError as exc:
            if exc.status in (409, 412):
                # The cloud copy moved on since our last sync: keep both.
                await self._keep_local_as_conflict(rel)
                try:
                    placed = await self._place_remote(rel)
                except BridgeError as get_exc:
                    if _bridge_down(get_exc):
                        raise
                    await self._placeholder_for_unreadable(rel, entry, get_exc.status)
                else:
                    placed.stub = False
                    placed.remote_checksum = placed.local_sha
            elif exc.status in (401, 429) or exc.status >= 500:
                raise  # the bridge is down or refusing everything: retry the pass
            else:
                # This one file is refused (too big, bad name, quota, or
                # 403: the person may read it but not write it, e.g. a
                # server-made capture): listed, tried again only once it
                # changes, and every other file keeps syncing. A 403 used
                # to abort the whole pass, so the same refused file was
                # re-sent every few seconds for ever (~120k refused PUTs
                # a day, 2026-10-31).
                self._refused[rel] = (sig, f"cloud refused it ({exc.status})")
                self._skip(rel, f"cloud refused it ({exc.status})")
        except OSError as exc:
            self._skip(rel, f"could not upload: {exc.strerror or exc}")
        # Not in a ``finally``: a pass cut short (the final flush's budget, a bridge
        # outage) leaves the file it was sending counted as waiting, which is the truth
        # the flush reports when it cannot recount in time.
        self.pending_uploads = max(0, self.pending_uploads - 1)
        await self.asave()

    async def push_once(self, changed_hint: list[str] | None = None) -> None:
        """One upload pass: send every local change (``upload_concurrency`` at a time), then
        re-scan and send deletes. ``changed_hint``: the changed files a walk made just now
        already found (the final flush's first count); the pass sends those without walking
        the folder again first, and its closing scan still catches anything else."""
        async with self._lock:
            pass_started = time.monotonic()  # taken once the lock is ours: this pass's scan starts now
            # The walk and the per-file stat of a large folder on the network
            # drive take minutes cold: never on the event loop (it answers
            # /health — a 12.5k-file folder held a wake at 170 s, 2026-10-18).
            # An unreadable folder raises here: no upload, no delete this pass.
            if changed_hint is not None:
                changed = list(changed_hint)
            else:
                scan = await asyncio.to_thread(self._scan)
                changed, _ = await asyncio.to_thread(self._classify, scan, dict(self.entries))
            self.pending_uploads = len(changed)
            await _bounded_each(changed, self._push_one, max(1, self.knobs.upload_concurrency))
            # Re-scan: a conflict copy made above is new on disk and must never
            # be mistaken for a file the person deleted.
            closing_scan_wall = time.time()
            scan = await asyncio.to_thread(self._scan)
            known = dict(self.entries)
            still_changed, missing = await asyncio.to_thread(self._classify, scan, known)
            # What this pass leaves waiting, from the walk it just made: the final flush reads it
            # instead of walking a big EFS folder a third time (that walk is what ate the flush budget).
            self.unsent_after_push = await asyncio.to_thread(self._not_refused, still_changed)
            for rel in [r for r in missing if known[r].unmanaged]:
                # Never the cloud's file: removing it here is no cloud delete and no hold.
                self.entries.pop(rel, None)
                self._unskip(rel, "a cloud file this sync does not manage")
            missing = [r for r in missing if not known[r].unmanaged]
            approved, held = await asyncio.to_thread(self._gate_deletes, missing, known)
            for rel in approved:
                entry = self.entries[rel]
                if entry.remote_checksum:
                    await asyncio.to_thread(self._tombstone, rel, entry)
                    try:
                        await self.bridge.delete(rel)
                    except BridgeError as exc:
                        if exc.status not in (403, 409):
                            raise
                        # The server held or refused this delete (its per-machine
                        # cap, or the person chose to keep the file): the file is
                        # still in the cloud, so it comes back into the folder.
                        logger.warning("cloud files: the cloud kept %s (%s); restoring it", rel, exc.status)
                        self._missing_last.discard(rel)
                        try:
                            await self._restore_one(rel, entry)
                        except BridgeError as get_exc:
                            if _bridge_down(get_exc):
                                raise
                            await self._placeholder_for_unreadable(rel, entry, get_exc.status)
                        await self.asave()
                        continue
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
            if self.halt and (self._restore_due() or self._unrestored):
                # Nobody answered within the window: the folder gets the files
                # back. Never a permanent disagreement, never a silent delete.
                # A restore that failed for some files retries them every pass.
                await self._restore(self._held_paths(), auto=True)
            self.stats.last_push_at = self._now().isoformat()
            requested = self.flush_requested_mono
            if requested is not None and pass_started > requested:
                # Only a pass that began after the flush request can vouch for writes made before it.
                self.clean_since_flush_request = (
                    self.unsent_after_push == [] and not self.stats.consecutive_failures and not self.halt
                )
                self._clean_scan_wall = closing_scan_wall

    def _anything_newer_than(self, wall: float) -> bool:
        """Is any synced file or folder under the Cloud folder changed after ``wall`` (a bound, not a
        classification: mtime of every entry the scan would list, folders included so a new, renamed
        or removed file shows). Stops at the first newer one. An unreadable folder counts as newer."""
        limit = wall - 2.0  # network-drive timestamps may trail this clock by a moment
        try:
            for dirpath, dirnames, filenames in os.walk(self.root, onerror=lambda e: (_ for _ in ()).throw(e)):
                dirnames[:] = [d for d in dirnames if not d.startswith(".")]
                if os.lstat(dirpath).st_mtime > limit:
                    return True
                for name in filenames:
                    if name.startswith(".") or name.endswith(SKIP_SUFFIXES):
                        continue
                    if os.lstat(os.path.join(dirpath, name)).st_mtime > limit:
                        return True
        except OSError:
            return True
        return False

    async def clean_now(self, timeout_seconds: float = 6.0) -> bool:
        """``clean_since_flush_request`` AT THE MOMENT OF ASKING: the proof stands only if nothing under
        the Cloud folder changed after the qualifying pass's closing scan. The check is the mtime bound
        above, not a second classification; if it cannot finish in ``timeout_seconds`` (a cold network
        drive) the answer is not clean, never a guess."""
        wall = self._clean_scan_wall
        if not self.clean_since_flush_request or wall is None:
            return False
        try:
            newer = await asyncio.wait_for(asyncio.to_thread(self._anything_newer_than, wall), timeout_seconds)
        except TimeoutError:
            return False
        return not newer

    def _unsent(self, known: dict[str, Entry] | None = None) -> list[str]:
        """Local changes not yet in the cloud (a file the cloud refused as it is
        stays listed in ``skipped``, never counted as waiting). Run in a thread, pass
        ``known`` copied on the event loop: a pass may be changing ``entries`` meanwhile."""
        scan = self._scan()
        changed, _ = self._classify(scan, dict(self.entries) if known is None else known)
        return self._not_refused(changed)

    def _not_refused(self, changed: list[str]) -> list[str]:
        out: list[str] = []
        for rel in changed:
            refused = self._refused.get(rel)
            if refused is not None and refused[0] == _sig(self._path(rel)):
                continue
            out.append(rel)
        return out

    async def flush(self, timeout_seconds: float | None = None, *, passes: int = 3) -> dict[str, Any]:
        """The final pass before the machine stops (save-before-stop and SIGTERM):
        upload every local change (conflict copies included) and wait, bounded by
        ``final_flush_seconds``, until nothing is left. Never raises: the answer
        says whether it finished and, if not, why and how many files were left."""
        self.flush_requested_mono = time.monotonic()
        self.clean_since_flush_request = False
        limit = float(self.knobs.final_flush_seconds if timeout_seconds is None else timeout_seconds)
        before = (self.stats.uploaded, self.stats.conflicts)
        started = time.monotonic()

        def answer(flushed: bool, **extra: Any) -> dict[str, Any]:
            return {
                "flushed": flushed,
                "uploaded": self.stats.uploaded - before[0],
                "conflict_copies": self.stats.conflicts - before[1],
                "skipped": len(self.skipped),
                "deletes_held": (self.halt or {}).get("held", 0),
                "seconds": round(time.monotonic() - started, 1),
                "timeout_seconds": limit,
                **extra,
            }

        if not self.initial_done:
            # The first download never finished: pushing now could mistake a not-yet
            # downloaded file for a delete. Local files stay on the home (EFS).
            return answer(False, reason="first sync not finished", pending=None)

        # Nothing waiting answers at once: one walk, outside the pass lock (the background pass
        # may hold it for its own two walks). A flush always ran full passes first, so a clean
        # folder on a big network drive spent the whole budget proving it and the stop filed
        # "timed out ... no file known to be waiting" (26 stops in 9 h, 2026-11-10). A file the
        # background pass is sending right now still counts as waiting, so this never skips one.
        try:
            already = await asyncio.wait_for(
                asyncio.to_thread(self._unsent, dict(self.entries)), timeout=max(0.05, limit / 2)
            )
        except Exception:  # noqa: BLE001 - too slow or unreadable: the passes below decide
            already = None
        if already == []:
            return answer(True, pending=0)

        async def until_clean() -> list[str]:
            left: list[str] = []
            # The first pass sends what that walk just found, without walking the folder again
            # before its first upload (on a big network drive that walk took most of the budget).
            hint = already
            for _ in range(max(1, passes)):
                self.unsent_after_push = None
                await self.push_once(hint)
                hint = None
                # The pass's own closing walk already says what is left; the fallback walk is for a
                # pass that ended without one.
                left = self.unsent_after_push
                if left is None:
                    left = await asyncio.to_thread(self._unsent, dict(self.entries))
                if not left:
                    break
            return left

        # The ANSWER is due inside ``limit`` too: the stop waits for it with only a small
        # transport margin. A slice of the budget is kept to count what is left; the count
        # itself is a folder walk (minutes cold on a big folder over EFS), so it is bounded and
        # falls back to the last pass's count. An unbounded count after the timeout is what
        # made three stops in 24 h end on "no answer (ReadTimeout)" (2026-11-09).
        reserve = min(FLUSH_ANSWER_RESERVE_SECONDS, limit * 0.2)
        try:
            left = await asyncio.wait_for(until_clean(), timeout=max(0.1, started + limit - reserve - time.monotonic()))
        except TimeoutError:
            pending, counted = await self._count_unsent_within(started + limit - time.monotonic())
            if counted and pending == 0:
                # The passes ran long, but the closing count found every file in the cloud.
                return answer(True, pending=0, timed_out=True, pending_counted=True)
            logger.error("cloud files: final flush timed out after %ss; %s files not uploaded", limit, pending)
            return answer(False, reason="timed out", timed_out=True, pending=pending, pending_counted=counted)
        except Exception as exc:  # noqa: BLE001 - reported to the caller, never swallowed
            logger.exception("cloud files: final flush failed")
            return answer(False, reason=f"{type(exc).__name__}: {str(exc)[:200]}", pending=None)
        if left:
            return answer(False, reason="files still changing", pending=len(left), sample=left[:5])
        return answer(True, pending=0)

    async def _count_unsent_within(self, seconds: float) -> tuple[int | None, bool]:
        """How many local changes are still not in the cloud, inside ``seconds``. On time:
        ``(count, True)``. Too slow or unreadable: the last pass's count when it saw any
        (``(n, False)``: at least that many were waiting), else ``(None, False)`` (unknown,
        never a made-up zero)."""
        try:
            left = await asyncio.wait_for(
                asyncio.to_thread(self._unsent, dict(self.entries)), timeout=max(0.05, seconds)
            )
            return len(left), True
        except Exception:  # noqa: BLE001 - the count is a courtesy; the timeout is the fact
            return (self.pending_uploads or None), False

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
    def _record_pass(self, pull_error: str | None, push_error: str | None) -> None:
        """One pass's outcome: pull and push are separate failure domains, and a run of
        failures is visible (``consecutive_failures``, ``failing_since``) to the server."""
        self.stats.last_error = pull_error or push_error
        if pull_error or push_error:
            self.stats.consecutive_failures += 1
            self.stats.failing_since = self.stats.failing_since or self._now().isoformat()
        else:
            self.stats.consecutive_failures = 0
            self.stats.failing_since = None

    async def run_forever(self, *, renew: Any = None) -> None:
        self.root.mkdir(parents=True, exist_ok=True)
        next_pull = 0.0
        while True:
            pull_error = push_error = None
            # PULL domain: a renew or feed failure (401/429/5xx, a frozen server) never
            # stops uploads below — the machine's edits keep reaching the cloud.
            try:
                if renew is not None:
                    await renew()
                if time.monotonic() >= next_pull:
                    wait = await self.pull_once()
                    next_pull = time.monotonic() + wait
                    await asyncio.to_thread(self.evict)
                self.stats.last_pull_error = None
            except BridgeError as exc:
                pull_error = self.stats.last_pull_error = f"pull: {exc}"
                logger.warning("cloud files sync pull: %s", exc)
                if exc.retry_after:
                    next_pull = time.monotonic() + exc.retry_after
            except Exception as exc:  # noqa: BLE001 - the loop never dies; it says why
                pull_error = self.stats.last_pull_error = f"pull: {type(exc).__name__}: {exc}"
                logger.exception("cloud files sync pull failed")
            # PUSH domain: runs whenever the first download has finished, whatever the pull did.
            if self.initial_done:
                try:
                    await self.push_once()  # stamps last_push_at
                    self.stats.last_push_error = None
                    if pull_error is None:
                        await self.fill_copies()
                except BridgeError as exc:
                    if exc.status in (404, 410) and exc.path:
                        # ONE file the cloud no longer has (deleted there while this machine still
                        # holds or pushes it; a delete the feed will deliver): listed with its path,
                        # never a paused sync (live 2026-11-16, a 404 on one library PDF).
                        entry = self.entries.get(exc.path)
                        if entry is not None:
                            entry.want_copy = False
                        self._skip(exc.path, f"cloud could not give it ({exc.status})")
                        logger.warning("cloud files sync push: %s is gone from the cloud (%s); skipped, sync goes on",
                                       exc.path, exc.status)
                    else:
                        push_error = self.stats.last_push_error = f"push: {exc}"
                        logger.warning("cloud files sync push: %s", exc)
                except Exception as exc:  # noqa: BLE001
                    push_error = self.stats.last_push_error = f"push: {type(exc).__name__}: {exc}"
                    logger.exception("cloud files sync push failed")
            self._record_pass(pull_error, push_error)
            await asyncio.sleep(max(1, self.knobs.local_scan_seconds))


@dataclass
class MachineFilesSession:
    """The machine token, renewed at half-life through the bridge, kept ONLY in this
    process's memory: the home is the agent's home (same uid, sudo), so a token
    written there is one an agent can read and delete cloud files with (review 3
    D2). A ``session.json`` an older image left there is removed at start."""

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
        for stale in (self._file, self._file.with_suffix(".tmp")):
            try:
                stale.unlink()
            except FileNotFoundError:
                pass
            except OSError as exc:
                logger.error("cloud files: could not remove the old token file %s: %s", stale, exc)

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
