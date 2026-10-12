"""Capy's sessions, pulled from Capy's API into local mirror files.

Capy (capy.ai) runs its coding agent on its own servers: no transcript of a
Capy thread ever exists on this machine, and no hook fires here when one
starts. So capture runs the other way round. `probe capy sync` reads the
researcher's own threads through Capy's public API (with the researcher's own
Capy key) and appends each one to a MIRROR file under the registry row's
transcript root; the shared upload journal then sends that file exactly as it
sends any other agent's transcript (cli/capy_cli.py drives it).

ONE FILE PER SESSION. A thread is one session and each of its subagents is
another (Capy's subagents have their own transcripts, read through their own
routes), so lines from two conversations never interleave in one file. A
subagent's header names its thread's session, so the upload records the link.

THE MIRROR IS APPEND-ONLY AND REPRODUCIBLE. The upload protocol proves every
batch against a hash of the file's bytes up to that point
(`session_journal.prefix_hash`), so bytes already written must never change,
and a mirror rebuilt from scratch (a new machine, a lost state folder) must
come out byte for byte the same or its stream could never be continued:
  - a header line first, written once (`capy_session`: who this file is), made
    only of facts fixed when the thread starts (no title: threads are renamed);
  - then one line per Capy message, in Capy's own order, each serialized
    canonically: a fixed set of keys, sorted, no spaces, ASCII escapes, and a
    lone surrogate (a reply cut mid-emoji) replaced by U+FFFD the same way on
    every machine, so its bytes depend on the message alone and every reader
    (the upload journal re-encodes lines as UTF-8) can take them;
  - each message once: Capy pages a transcript with an exclusive EVENT-ID
    cursor (26 characters; a tool entry's own id is its tool call id, which is
    not a cursor). The cursor is null once caught up, so the next read starts
    again from the last non-null one and skips the ids it already wrote. The
    resume point records the mirror's size; a mirror of any other size (a sync
    killed before its record was saved) is checked against every id it holds;
  - a write is one `os.write` of whole lines per page; a torn tail a crash
    left behind is cut back to its last newline before anything is appended
    (the upload journal only ever reads complete lines, so it was never sent).

WHOSE THREADS. Every member of a Capy organization can read every non-personal
thread in it, so a key can see teammates' work. Only threads whose author IS
the researcher are mirrored, and only in the Capy projects they chose
(`probe capy connect`), checked on every thread rather than trusting the
project filter: capturing someone else's sessions would need their consent,
which this machine cannot give. Messages others add to the researcher's own
threads are part of those threads, and the consent screen says so.

WHAT CAPY SHARES. Prompts, replies and a one-line summary per tool call
(`capy_sanitize` documents the mapping). Tool output, file diffs and the
model's reasoning are not in Capy's public transcript.

THE KEY. Sent to Capy's API only: never on a redirect (no redirect is
followed), over the CLI's own TLS trust and proxies.
"""

from __future__ import annotations

import http.client
import json
import math
import os
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from collections.abc import Callable, Iterator
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

from ..tap_core.capy_sanitize import HEADER_TYPE, MESSAGE_TYPE, SUPPORTED_VERSIONS

#: Capy's public API. PROBE_CAPY_API_BASE points it elsewhere (tests, smoke).
DEFAULT_API_BASE = "https://api.capy.ai/api/v1"
ENV_API_BASE = "PROBE_CAPY_API_BASE"

#: The id space for Probe's session ids: uuid5(NAMESPACE, "capy:<kind>:<id>").
#: Fixed forever: a rebuilt mirror must name the same session.
SESSION_NAMESPACE = uuid.UUID("6f1d9c1e-8a3b-5c7e-9d2f-4b0a1c2e3f40")
THREAD = "thread"
SUBAGENT = "subagent"
#: The mirror format version this module writes (capy_sanitize reads it).
MIRROR_VERSION = 1
assert MIRROR_VERSION in SUPPORTED_VERSIONS

#: Page sizes. Capy caps pages itself; asking for more is harmless.
THREAD_PAGE = 100
MESSAGE_PAGE = 100
SUBAGENT_PAGE = 100

#: Our own budget against Capy's API: at most this many calls a minute (the
#: same pace research-os keeps against W&B and Benchling), and a 429's
#: Retry-After is always honoured, up to MAX_RETRY_AFTER_S per wait.
CALLS_PER_MINUTE = 60
MAX_RETRY_AFTER_S = 120
DEFAULT_RETRY_AFTER_S = 5.0
MAX_429_RETRIES = 3
REQUEST_TIMEOUT_S = 30.0

#: A thread whose last activity is older than this is over: its session is
#: finalized (the same window the tap gives a session whose agent it cannot
#: see). New messages later simply reopen it.
QUIET_FINISH_SECONDS = 24 * 60 * 60
#: Thread / subagent statuses that end a session at once.
_THREAD_DONE = frozenset({"archived"})
_SUBAGENT_DONE = frozenset({"done", "failed"})

#: The Capy message keys a mirror line keeps, and their mirror names: the ones
#: fixed when the message is written. Anything else Capy sends (client keys,
#: file ids, upload paths, call durations, the author's display name, which can
#: be renamed) stays on Capy.
_MESSAGE_KEYS = {
    "id": "id",
    "source": "source",
    "text": "text",
    "tool": "tool",
    "editOf": "edit_of",
    "model": "model",
    "createdAt": "created_at",
}

#: At most this many Capy calls per sync: a long first history is read over
#: several syncs (each keeps what it read) instead of one that the scheduler's
#: timeout kills before anything is saved. 900 calls is 15 minutes at the pace.
MAX_CALLS_PER_SYNC = 900

#: ... and at most this long: a 429's Retry-After can be minutes, and the
#: scheduler stops a sync at SYNC_TIMEOUT_SECONDS (capy_cli).
MAX_SECONDS_PER_SYNC = 20 * 60

#: A thread of ours missing from this many complete listings in a row is
#: finished (one miss can be a listing that shifted while it was read).
UNLISTED_SYNCS = 2

#: How many trailing mirror lines a read checks for ids it already wrote, on
#: top of the ids recorded since its cursor, when the mirror is the size its
#: record says (any other size: every id is checked).
_TAIL_IDS = 2 * MESSAGE_PAGE
_CHUNK = 1024 * 1024


class CapyError(RuntimeError):
    """A Capy API call failed for a reason a later sync may not repeat."""


class CapyAuthError(CapyError):
    """Capy refused the key (401/403): revoked, expired or without access.
    Nothing more can be read until the researcher connects again."""


class CapyNotFound(CapyError):
    """A thread, subagent or project is gone (or out of the key's reach)."""


class CapyBudgetSpent(CapyError):
    """This sync made its MAX_CALLS_PER_SYNC calls: the rest waits for the next."""


def api_base() -> str:
    return (os.environ.get(ENV_API_BASE) or DEFAULT_API_BASE).rstrip("/")


def session_id_for(kind: str, capy_id: str) -> str:
    """Probe's session id for a Capy thread or subagent (a UUID, as the upload
    protocol requires; Capy's own ids are not UUIDs). Threads and subagents
    get separate id spaces, so the two can never name one session."""
    return str(uuid.uuid5(SESSION_NAMESPACE, f"capy:{kind}:{capy_id}"))


def canonical_line(record: dict) -> bytes:
    """One mirror line: sorted keys, no spaces, ASCII escapes, newline-terminated."""
    return (json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n").encode("ascii")


def project_cwd(project_id: str) -> str:
    """The folder a Capy session is filed under. Capy's checkout lives on its
    own machine, so this names the Capy project instead: absolute, stable, and
    never a path on this machine."""
    safe = urllib.parse.quote(project_id, safe="")
    return f"/capy/projects/{safe}"


def _iso(value: Any) -> str | None:
    return value if isinstance(value, str) and value else None


def _parse_time(value: Any) -> float | None:
    if not isinstance(value, str) or not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).timestamp()
    except ValueError:
        return None


def _whole_text(value: Any) -> Any:
    """Every string in `value` with lone surrogates replaced by U+FFFD: a
    pure function of the value, so every machine writes the same bytes, and
    always encodable as UTF-8."""
    if isinstance(value, str):
        return value.encode("utf-16", "surrogatepass").decode("utf-16", "replace")
    if isinstance(value, dict):
        return {_whole_text(k): _whole_text(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_whole_text(v) for v in value]
    return value


def _finite_size(value: Any) -> int | None:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        return None
    return max(0, int(value))


def header_record(*, session_id: str, thread: dict, subagent: dict | None = None) -> dict:
    record = {
        "type": HEADER_TYPE,
        "version": MIRROR_VERSION,
        "id": session_id,
        "thread_id": thread.get("id"),
        "project_id": thread.get("projectId"),
        "cwd": project_cwd(str(thread.get("projectId") or "none")),
        "created_at": _iso((subagent or thread).get("createdAt")),
    }
    # No title: Capy renames threads (and regenerates titles), and a header
    # whose bytes could change would make a rebuilt mirror disagree with what
    # was already uploaded. Every field here is fixed when the thread starts.
    if subagent is not None:
        record["subagent_id"] = subagent.get("id")
        record["subagent_path"] = subagent.get("subagentPath") or subagent.get("taskPath")
        # session_identity records this as the session's lineage.
        record["parent_session_id"] = session_id_for(THREAD, str(thread.get("id")))
    return _whole_text({k: v for k, v in record.items() if v is not None})


def message_record(message: dict) -> dict:
    """A Capy transcript entry as one mirror line: the kept keys under their
    mirror names, tool call names, and attachments reduced to name, media
    type and size."""
    record: dict[str, Any] = {"type": MESSAGE_TYPE}
    for source_key, mirror_key in _MESSAGE_KEYS.items():
        value = message.get(source_key)
        if isinstance(value, str) and value:
            record[mirror_key] = value
    calls = message.get("calls")
    if isinstance(calls, list):
        names = [c["tool"] for c in calls if isinstance(c, dict) and isinstance(c.get("tool"), str)]
        if names:
            record["calls"] = [{"tool": name} for name in names]
    attachments = message.get("attachments")
    if isinstance(attachments, list):
        kept = []
        for item in attachments:
            file = item.get("file") if isinstance(item, dict) else None
            if not isinstance(file, dict):
                continue
            entry: dict[str, Any] = {}
            if isinstance(file.get("name"), str):
                entry["name"] = file["name"]
            if isinstance(file.get("mediaType"), str):
                entry["media_type"] = file["mediaType"]
            size = _finite_size(file.get("sizeBytes"))
            if size is not None:
                entry["size_bytes"] = size
            if entry:
                kept.append(entry)
        if kept:
            record["attachments"] = kept
    return _whole_text(record)


# --- the API -----------------------------------------------------------------


@dataclass
class Page:
    items: list[dict]
    cursor: str | None


class CapyAPI:
    """The few read routes Probe uses, with a call budget and 429 handling.

    Read-only by construction: every request is a GET. The key rides an
    unredirected header through the CLI's credential opener (no redirects,
    the environment's proxies, the CLI's TLS trust): a 3xx is an error, never
    a second host holding the key.
    """

    def __init__(
        self,
        key: str,
        *,
        base: str | None = None,
        max_calls: int | None = None,
        max_seconds: float | None = None,
        sleep: Callable[[float], None] = time.sleep,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        self.key = key
        self.base = (base or api_base()).rstrip("/")
        self.max_calls = max_calls
        self.max_seconds = max_seconds
        self._sleep = sleep
        self._clock = clock
        self._calls: list[float] = []
        self.calls_made = 0
        self._started = clock()

    def _pace(self) -> None:
        now = self._clock()
        self._calls = [t for t in self._calls if now - t < 60.0]
        if len(self._calls) >= CALLS_PER_MINUTE:
            wait = 60.0 - (now - self._calls[0])
            if wait > 0:
                self._sleep(wait)
        self._calls.append(self._clock())

    def get(self, path: str, params: dict | None = None) -> Any:
        from .capabilities import _credential_opener

        query = {k: v for k, v in (params or {}).items() if v is not None}
        url = f"{self.base}{path}" + (f"?{urllib.parse.urlencode(query)}" if query else "")
        for attempt in range(MAX_429_RETRIES + 1):
            if self.max_calls is not None and self.calls_made >= self.max_calls:
                raise CapyBudgetSpent(f"stopped after {self.calls_made} Capy calls; the next sync goes on")
            if self.max_seconds is not None and self._clock() - self._started >= self.max_seconds:
                raise CapyBudgetSpent(f"stopped after {self.max_seconds:.0f}s; the next sync goes on")
            self._pace()
            self.calls_made += 1
            request = urllib.request.Request(
                url, headers={"Accept": "application/json", "User-Agent": "probe-capy-sync/1"}
            )
            request.add_unredirected_header("Authorization", f"Bearer {self.key}")
            try:
                with _credential_opener().open(request, timeout=REQUEST_TIMEOUT_S) as response:
                    return json.loads(response.read() or b"null")
            except urllib.error.HTTPError as exc:
                if exc.code in (401, 403):
                    raise CapyAuthError(f"Capy refused the key (http {exc.code})") from None
                if exc.code == 404:
                    raise CapyNotFound(f"not found: {path}") from None
                if 300 <= exc.code < 400:
                    raise CapyError(f"Capy redirected {path}; not followed (the key stays put)") from None
                if exc.code == 429 and attempt < MAX_429_RETRIES:
                    self._sleep(retry_after_seconds(exc.headers.get("Retry-After")))
                    continue
                raise CapyError(f"Capy answered http {exc.code} for {path}") from None
            except (urllib.error.URLError, http.client.HTTPException, OSError, ValueError) as exc:
                raise CapyError(f"Capy unreachable ({type(exc).__name__})") from None
        raise CapyError(f"Capy kept rate-limiting {path}")

    def page(self, path: str, params: dict) -> Page:
        body = self.get(path, params)
        items = body.get("items") if isinstance(body, dict) else None
        if not isinstance(items, list):
            raise CapyError(f"unexpected page shape from {path}")
        cursor = body.get("cursor")
        return Page([i for i in items if isinstance(i, dict)], cursor if isinstance(cursor, str) and cursor else None)

    def listing(self, path: str, *, limit: int, params: dict | None = None) -> Iterator[dict]:
        """Every item of a list route, page by page. Threads page with
        `cursor`, subagents with `after`; a repeated cursor is an error, never
        an endless loop and never a silently short list."""
        cursor_param = "cursor" if path == "/threads" else "after"
        cursor: str | None = None
        seen: set[str] = set()
        while True:
            page = self.page(path, {**(params or {}), "limit": limit, cursor_param: cursor})
            yield from page.items
            if page.cursor is None:
                return
            if page.cursor in seen:
                raise CapyError(f"Capy repeated a page cursor for {path}")
            seen.add(page.cursor)
            cursor = page.cursor

    def users(self) -> list[dict]:
        """Bounded list: Capy returns every member at once (no cursor)."""
        return self.page("/users", {}).items

    def projects(self) -> list[dict]:
        """Bounded list: Capy returns every project at once (no cursor)."""
        return self.page("/projects", {}).items

    def threads(self, project_id: str) -> Iterator[dict]:
        return self.listing("/threads", limit=THREAD_PAGE, params={"projectId": project_id})

    def subagents(self, thread_id: str) -> Iterator[dict]:
        return self.listing(f"/threads/{urllib.parse.quote(thread_id, safe='')}/subagents", limit=SUBAGENT_PAGE)

    def message_page(self, kind: str, capy_id: str, after: str | None) -> Page:
        route = "threads" if kind == THREAD else "subagents"
        return self.page(
            f"/{route}/{urllib.parse.quote(capy_id, safe='')}/messages",
            {"limit": MESSAGE_PAGE, "after": after},
        )


def retry_after_seconds(value: Any) -> float:
    """A 429's Retry-After in seconds: a finite positive number, capped; a
    missing or unreadable one waits the default."""
    try:
        seconds = float(value)
    except (TypeError, ValueError):
        return DEFAULT_RETRY_AFTER_S
    if not math.isfinite(seconds) or seconds <= 0:
        return DEFAULT_RETRY_AFTER_S
    return min(seconds, float(MAX_RETRY_AFTER_S))


# --- the mirror files ----------------------------------------------------------


def _last_newline(path: Path, size: int) -> int:
    """The offset just past the last newline in the file, 0 when none."""
    with path.open("rb") as handle:
        end = size
        while end > 0:
            start = max(0, end - _CHUNK)
            handle.seek(start)
            chunk = handle.read(end - start)
            cut = chunk.rfind(b"\n")
            if cut >= 0:
                return start + cut + 1
            end = start
    return 0


def _repair_torn_tail(path: Path) -> None:
    """Cut a crash's incomplete last line back to the last newline. The upload
    journal reads complete lines only, so those bytes were never sent."""
    size = path.stat().st_size
    if size == 0:
        return
    with path.open("rb") as handle:
        handle.seek(size - 1)
        if handle.read(1) == b"\n":
            return
    keep = _last_newline(path, size)
    with path.open("rb+") as handle:
        handle.truncate(keep)
        handle.flush()
        os.fsync(handle.fileno())


def _tail_lines(path: Path, count: int) -> list[bytes]:
    """The last `count` complete lines, read backwards in chunks."""
    try:
        size = path.stat().st_size
    except FileNotFoundError:
        return []
    lines: list[bytes] = []
    with path.open("rb") as handle:
        end, carry = size, b""
        while end > 0 and len(lines) <= count:
            start = max(0, end - _CHUNK)
            handle.seek(start)
            block = handle.read(end - start) + carry
            parts = block.split(b"\n")
            carry = parts[0] if start > 0 else b""
            lines[:0] = [p for p in (parts[1:] if start > 0 else parts) if p]
            end = start
    return lines[-count:]


def mirrored_ids(path: Path, *, last: int | None = None) -> set[str]:
    """Ids of the messages a mirror holds: all of them, or the last `last`."""
    if last is not None:
        raw = _tail_lines(path, last)
    else:
        try:
            raw = path.read_bytes().splitlines()
        except FileNotFoundError:
            return set()
    ids = set()
    for line in raw:
        try:
            record = json.loads(line)
        except ValueError:
            continue
        if isinstance(record, dict) and record.get("type") == MESSAGE_TYPE and isinstance(record.get("id"), str):
            ids.add(record["id"])
    return ids


def append_lines(path: Path, lines: list[bytes]) -> int:
    """Append whole lines with one write and fsync. Returns bytes written."""
    if not lines:
        return 0
    data = b"".join(lines)
    fd = os.open(path, os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o600)
    try:
        view = memoryview(data)
        while view:
            written = os.write(fd, view)
            view = view[written:]
        os.fsync(fd)
    finally:
        os.close(fd)
    return len(data)


@dataclass
class MirroredSession:
    """One mirror file after a pull: what the uploader needs to send it."""

    session_id: str
    path: Path
    cwd: str
    finished: bool
    new_bytes: int = 0


@dataclass
class PullResult:
    sessions: list[MirroredSession] = field(default_factory=list)
    threads_seen: int = 0
    threads_mine: int = 0
    errors: list[str] = field(default_factory=list)
    auth_failed: bool = False
    #: MAX_CALLS_PER_SYNC was reached: what was read is kept, the rest waits.
    budget_spent: bool = False


def mirror_session(
    api: CapyAPI,
    *,
    root: Path,
    kind: str,
    capy_id: str,
    header: dict,
    cursor_state: dict,
) -> tuple[int, bool]:
    """Bring one session's mirror up to date. Returns (bytes written, settled).

    `cursor_state` ({"after", "tail", "size"}) is this session's resume
    point, updated in place after every page: `after` the last non-null event
    cursor, `tail` the ids already written from it, `size` the mirror's bytes
    then. A mirror with no record (a new machine, lost state), or not the size
    its record says (a sync killed after appending, before its record was
    saved), is checked against every id it holds; one that is missing is
    rebuilt. `settled` is False when Capy says newer messages are still
    settling (its cursor did not move): read again next sync.
    """
    path = root / f"{header['id']}.jsonl"
    written = 0
    if path.exists():
        _repair_torn_tail(path)
    fresh = not path.exists() or path.stat().st_size == 0
    if fresh:
        cursor_state.clear()
        written += append_lines(path, [canonical_line(header)])
    after = cursor_state.get("after")
    size, recorded = path.stat().st_size, cursor_state.get("size")
    if "after" in cursor_state and recorded == size:
        seen = set(cursor_state.get("tail") or ()) | mirrored_ids(path, last=_TAIL_IDS)
    else:
        seen = mirrored_ids(path)
        if isinstance(recorded, int) and size < recorded:
            # Shorter than what the cursor was saved against: messages before
            # the cursor may be missing, so read from the start.
            after = None
    tail: list[str] = [i for i in (cursor_state.get("tail") or ()) if isinstance(i, str)]
    while True:
        page = api.message_page(kind, capy_id, after)
        lines = []
        for message in page.items:
            message_id = message.get("id")
            if not isinstance(message_id, str) or not message_id or message_id in seen:
                continue
            seen.add(message_id)
            tail.append(message_id)
            lines.append(canonical_line(message_record(message)))
        written += append_lines(path, lines)
        size = path.stat().st_size
        if page.cursor is None:
            cursor_state.update(after=after, tail=tail, size=size)
            return written, True
        if page.cursor == after:
            cursor_state.update(after=after, tail=tail, size=size)
            return written, False
        after, tail = page.cursor, []
        cursor_state.update(after=after, tail=tail, size=size)


def _thread_finished(thread: dict, now: float) -> bool:
    last = _parse_time(thread.get("lastActivityAt") or thread.get("updatedAt"))
    return (
        bool(thread.get("archived"))
        or thread.get("status") in _THREAD_DONE
        or (last is not None and now - last >= QUIET_FINISH_SECONDS)
    )


def _marker(item: dict) -> dict:
    return {
        "activity": item.get("lastActivityAt") or item.get("updatedAt"),
        "status": item.get("status"),
        "archived": bool(item.get("archived")),
    }


def pull(
    api: CapyAPI,
    *,
    root: Path,
    me: str,
    projects: list[str],
    state: dict,
    now: float | None = None,
    on_thread: Callable[[], None] | None = None,
) -> PullResult:
    """Mirror every thread (and subagent) the researcher authored in the chosen
    projects. `state` is the caller's record (`threads`: each thread's last
    seen marker, project and subagents; `cursors`: each session's resume
    point); a thread whose marker did not move is not re-read, though its
    unfinished subagents are still checked. Mutates `state` in place and calls
    `on_thread` after each thread that cost Capy calls, so the caller can keep
    what was read even if this sync is stopped later.

    Each project's thread list is read whole before any thread is, so a thread
    that moves while this sync works cannot slip between pages. A thread of
    ours that UNLISTED_SYNCS complete listings in a row no longer show
    (deleted, moved out of the chosen projects, handed to another author) is
    never read again; its session is finished at what was already mirrored."""
    now = time.time() if now is None else now
    root.mkdir(parents=True, exist_ok=True, mode=0o700)
    result = PullResult()
    known: dict = state.setdefault("threads", {})
    cursors: dict = state.setdefault("cursors", {})
    listed: set[str] = set()
    complete: set[str] = set()
    for project_id in projects:
        try:
            threads = list(api.threads(project_id))
        except CapyAuthError as exc:
            result.auth_failed = True
            result.errors.append(str(exc))
            return result
        except CapyBudgetSpent:
            result.budget_spent = True
            return result
        except CapyError as exc:
            result.errors.append(f"project {project_id}: {exc}")
            continue
        complete.add(project_id)
        for thread in threads:
            thread_id = thread.get("id")
            if not isinstance(thread_id, str) or not thread_id:
                continue
            result.threads_seen += 1
            # The filter is Capy's; consent is ours. A thread from another
            # project, or another author, is never read.
            if str(thread.get("projectId")) != project_id or thread.get("authorId") != me:
                continue
            result.threads_mine += 1
            listed.add(thread_id)
            record = known.setdefault(thread_id, {})
            record["project"] = project_id
            record.pop("unlisted", None)
            calls = api.calls_made
            try:
                _pull_thread(api, thread, root=root, record=record,
                             cursors=cursors, now=now, result=result)
            except CapyAuthError as exc:
                result.auth_failed = True
                result.errors.append(str(exc))
                return result
            except CapyBudgetSpent:
                result.budget_spent = True
                return result
            except CapyNotFound:
                # Gone between the listing and the read: finished as mirrored,
                # never read again.
                result.sessions.extend(_finished_as_mirrored(thread_id, known.pop(thread_id), root))
                result.errors.append(f"thread {thread_id}: gone from Capy (deleted, or out of reach)")
            except (CapyError, OSError, ValueError) as exc:
                # Not recorded as read: the next sync tries it again.
                record.pop("marker", None)
                result.errors.append(f"thread {thread_id}: {exc}")
            if on_thread is not None and api.calls_made != calls:
                on_thread()
    # Only once every listing is in: a thread moved between two chosen
    # projects is listed under its new one, never finished by its old one.
    for thread_id, record in list(known.items()):
        if record.get("project") not in complete or thread_id in listed:
            continue
        record["unlisted"] = record.get("unlisted", 0) + 1
        if record["unlisted"] >= UNLISTED_SYNCS:
            result.sessions.extend(_finished_as_mirrored(thread_id, record, root))
    return result


def _finished_as_mirrored(thread_id: str, record: dict, root: Path) -> list[MirroredSession]:
    """A thread's (and its subagents') sessions, finished at what the mirror
    already holds."""
    cwd = project_cwd(str(record.get("project") or "none"))
    sessions = [session_id_for(THREAD, thread_id)]
    sessions += [sub["session"] for sub in (record.get("subagents") or {}).values() if sub.get("session")]
    return [
        MirroredSession(sid, root / f"{sid}.jsonl", cwd, True)
        for sid in sessions
        if (root / f"{sid}.jsonl").exists()
    ]


def _pull_thread(
    api: CapyAPI, thread: dict, *, root: Path, record: dict, cursors: dict, now: float, result: PullResult
) -> None:
    thread_id = thread["id"]
    finished = _thread_finished(thread, now)
    cwd = project_cwd(str(thread.get("projectId") or "none"))
    session_id = session_id_for(THREAD, thread_id)
    marker = _marker(thread)
    path = root / f"{session_id}.jsonl"
    # Re-read unless the marker is unchanged, Capy reported the last read
    # settled, an activity time exists, and the mirror is still on disk.
    changed = (
        record.get("marker") != marker
        or marker["activity"] is None
        or not record.get("settled", False)
        or not path.exists()
    )
    if changed:
        written, settled = mirror_session(
            api, root=root, kind=THREAD, capy_id=thread_id,
            header=header_record(session_id=session_id, thread=thread),
            cursor_state=cursors.setdefault(session_id, {}),
        )
        result.sessions.append(MirroredSession(session_id, path, cwd, finished, written))
    else:
        settled = True
        result.sessions.append(MirroredSession(session_id, path, cwd, finished))
    subagents: dict = record.setdefault("subagents", {})
    # A finished thread's subagents are re-listed only when the thread moved;
    # an open one's every sync (a subagent can talk without moving its thread).
    if changed or not finished:
        for sub in api.subagents(thread_id):
            _pull_subagent(api, thread, sub, root=root, subagents=subagents, cursors=cursors,
                           thread_finished=finished, cwd=cwd, result=result)
    else:
        for sub_record in subagents.values():
            sub_path = root / f"{sub_record['session']}.jsonl"
            if sub_path.exists():
                result.sessions.append(MirroredSession(sub_record["session"], sub_path, cwd, True))
    record.update(marker=marker, settled=settled)


def _pull_subagent(
    api: CapyAPI, thread: dict, sub: dict, *, root: Path, subagents: dict, cursors: dict,
    thread_finished: bool, cwd: str, result: PullResult,
) -> None:
    sub_id = sub.get("id")
    if not isinstance(sub_id, str) or not sub_id:
        return
    session_id = session_id_for(SUBAGENT, sub_id)
    path = root / f"{session_id}.jsonl"
    marker = _marker(sub)
    done = thread_finished or sub.get("status") in _SUBAGENT_DONE or bool(sub.get("archived"))
    record = subagents.get(sub_id) or {}
    if record.get("marker") == marker and record.get("settled") and path.exists():
        result.sessions.append(MirroredSession(session_id, path, cwd, done))
        return
    try:
        written, settled = mirror_session(
            api, root=root, kind=SUBAGENT, capy_id=sub_id,
            header=header_record(session_id=session_id, thread=thread, subagent=sub),
            cursor_state=cursors.setdefault(session_id, {}),
        )
    except CapyNotFound:
        subagents.pop(sub_id, None)
        result.errors.append(f"subagent {sub_id}: gone from Capy (deleted, or out of reach)")
        return
    subagents[sub_id] = {"session": session_id, "marker": marker, "settled": settled}
    result.sessions.append(MirroredSession(session_id, path, cwd, done, written))


def resolve_me(users: list[dict], *, email: str) -> dict | None:
    """The Capy user whose email is `email` (case and spaces ignored)."""
    needle = email.strip().lower()
    for user in users:
        if str(user.get("email") or "").strip().lower() == needle:
            return user
    return None
