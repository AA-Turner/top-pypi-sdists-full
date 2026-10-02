"""Uploads the session's trace files to Probe (`POST /v1/companion/traces`).

The trace files (`trace.py`) are the queue: the shipper reads each
`<agent>.jsonl` from a byte cursor kept beside it (`<agent>.cursor`), posts the
complete lines after it in batches of at most BATCH_BYTES, and moves the cursor
only when Probe answers 202 -- so a crash, a refusal or an outage loses nothing,
and a re-sent line is the same event on the server (its id is its offset).

NEVER IN THE BITE'S WAY. It runs as its own task beside the worker's loop, one
upload in flight, and nothing the worker does waits for it (outside voice X7).
It stops with the worker after one last bounded attempt.

A line over LINE_MAX_BYTES is trimmed HERE before it goes (a tool's result,
then the call's input, then the answer; `trace_truncated` says so), so one huge
line can never block the file (X2); the local file keeps it whole.

ORPHANS. At start it also drains other sessions' folders whose cursor is behind
their file and whose worker is gone (their lock is free) -- a session that
crashed and never came back still ships (X6) -- within DRAIN_BUDGET_S.

WHERE A FOLDER MAY GO. Each session folder is stamped (`meta.json`) with the
Probe server and daemon key it is recorded under when the worker starts
(`bind`), uploads on or off, and only while it is still empty; a folder ships
only with that same server and key, and a folder with traces but no stamp
never ships. So a machine
that switched account, team or server never uploads one team's traces as
another's -- nor a self-hosted deployment's to ours.

Answers: 202 moves on (a `dark` 202 -- tracing off for this team on the server
-- keeps the cursor and waits an hour, so the lines ship once it is on); 401,
403 and 404 (a server without the route) wait an hour; 413 and 422 are about
THIS batch (the server or the traces store refused it): it is split, and a
single line refused alone is skipped (logged) so it can never block the file;
anything else backs off from 30 s to 10 min. `PROBE_DAEMON_TRACE_UPLOAD=off`
turns it off.
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import logging
import os
import time
from pathlib import Path
from typing import Any, Awaitable, Callable

from probe.daemon import trace as trace_mod
from probe.daemon.store import state_dir

log = logging.getLogger("probe.daemon")

ENV_UPLOAD = "PROBE_DAEMON_TRACE_UPLOAD"
ROUTE = "/v1/companion/traces"
BATCH_BYTES = 1024 * 1024
#: Lines per upload (the relay takes up to 5,000; fewer keeps its forward short).
BATCH_LINES = 1_000
LINE_MAX_BYTES = 900 * 1024
INTERVAL_S = 20.0
DRAIN_BUDGET_S = 60.0
STOP_BUDGET_S = 10.0
LONG_WAIT_S = 3600.0
BACKOFF_MIN_S = 30.0
BACKOFF_MAX_S = 600.0
MAX_AGE_S = trace_mod.KEEP_S
#: Trimmed first to last (a line's own keys); each keeps its shape.
TRIM_KEYS = ("result", "error", "args", "input", "output", "head", "text", "tools")
META = "meta.json"
#: The relay's code for a batch the traces store refused (a 422 with it is about
#: THIS batch; any other 422 -- a shape the server does not know -- is not).
REJECTED_CODE = "traces_rejected"
#: Marks a folder whose lines came from more than one account: never shipped.
MIXED = "mixed"
AGENTS = ("writer", "reader")

#: `(url, json body, headers) -> (status, response json or None)`
Post = Callable[[str, dict[str, Any], dict[str, str]], Awaitable[tuple[int, Any]]]


def enabled() -> bool:
    return os.environ.get(ENV_UPLOAD, "on").strip().lower() not in ("0", "off", "false", "no")


def _size(value: Any) -> int:
    return len(json.dumps(value, default=str, ensure_ascii=False).encode("utf-8"))


def _cut(text: str, keep_bytes: int) -> str:
    data = text.encode("utf-8")
    if len(data) <= keep_bytes:
        return text
    head = data[: max(0, keep_bytes)].decode("utf-8", errors="ignore")
    return f"{head}… [cut: {len(data) - len(head.encode('utf-8')):,} more bytes]"


def _largest_string(value: Any, path: tuple = ()) -> tuple[tuple, int] | None:
    if isinstance(value, str):
        return path, len(value.encode("utf-8"))
    best: tuple[tuple, int] | None = None
    items = value.items() if isinstance(value, dict) else enumerate(value) if isinstance(value, list) else ()
    for key, child in items:
        found = _largest_string(child, (*path, key))
        if found is not None and (best is None or found[1] > best[1]):
            best = found
    return best


def fit_line(line: dict[str, Any], limit: int | None = None) -> dict[str, Any]:
    """`line` under `limit` bytes (LINE_MAX_BYTES): the largest strings inside
    TRIM_KEYS cut first, in that order, each field keeping its SHAPE (a call's
    `input` stays a list, its `output` keeps `usage` and `model_name`), then
    measured again. Numbers are never cut."""
    limit = LINE_MAX_BYTES if limit is None else limit
    if _size(line) <= limit:
        return line
    line = json.loads(json.dumps(line, default=str))  # a copy the cuts cannot leak out of
    line["trace_truncated"] = True
    for key in TRIM_KEYS:
        for _ in range(8):
            over = _size(line) - limit
            if over <= 0:
                return line
            if key not in line:
                break
            if isinstance(line[key], str):
                line[key] = _cut(line[key], len(line[key].encode("utf-8")) - over - 64)
                continue
            found = _largest_string(line[key])
            if found is None or found[1] <= 64:
                break
            path, own = found
            holder = line[key]
            for part in path[:-1]:
                holder = holder[part]
            holder[path[-1]] = _cut(holder[path[-1]], max(0, own - over - 64))
    for key in TRIM_KEYS:  # still over: whole fields go, in the same order
        if _size(line) <= limit:
            break
        line.pop(key, None)
    return line


def read_batch(path: Path, cursor: int, limit: int | None = None,
               max_lines: int | None = None) -> tuple[list[dict[str, Any]], int]:
    """The complete lines after `cursor`, up to `limit` bytes (BATCH_BYTES) and
    `max_lines` lines (BATCH_LINES), and where the next batch starts. A line
    that is not a JSON object is skipped (the cursor passes it); a partial last
    line waits for its end; NaN / Infinity become null."""
    limit = BATCH_BYTES if limit is None else limit
    max_lines = BATCH_LINES if max_lines is None else max_lines
    items: list[dict[str, Any]] = []
    total = 0
    pos = cursor
    with path.open("rb") as handle:
        handle.seek(cursor)
        while True:
            if len(items) >= max_lines:
                break
            raw = handle.readline()
            if not raw or not raw.endswith(b"\n"):
                break
            if items and total + min(len(raw), LINE_MAX_BYTES) > limit:
                break
            try:
                line = json.loads(raw)
            except ValueError:
                pos += len(raw)
                continue
            if not isinstance(line, dict):
                pos += len(raw)
                continue
            if b"NaN" in raw or b"Infinity" in raw:  # a line written before lines were strict
                line = trace_mod.finite(line)
            if len(raw) > LINE_MAX_BYTES:
                line = fit_line(line)
                size = _size(line)
            else:
                size = len(raw) - 1
            if items and total + size > limit:
                break
            items.append({"offset": pos, "line": line})
            total += size
            pos += len(raw)
    return items, pos


def cursor_path(trace_file: Path) -> Path:
    return trace_file.with_suffix(".cursor")


def read_cursor(trace_file: Path) -> int:
    try:
        return max(0, int(cursor_path(trace_file).read_text().strip() or 0))
    except (OSError, ValueError):
        return 0


def write_cursor(trace_file: Path, offset: int) -> None:
    path = cursor_path(trace_file)
    tmp = path.with_suffix(".cursor.tmp")
    fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    try:
        os.write(fd, str(offset).encode())
    finally:
        os.close(fd)
    os.replace(tmp, path)


def _key_id(key: str) -> str:
    return hashlib.sha256(key.encode("utf-8")).hexdigest()[:16]


def bind_to(folder: Path, base_url: str, key_id: str) -> bool:
    """Stamp `folder` with the server and key it is recorded under -- only if it
    has no stamp and no trace yet (a folder that already holds traces from an
    unknown server or key is never adopted). True when the folder is (now)
    this server's and key's; False when it belongs to another or to nobody."""
    path = folder / META
    if path.exists():
        try:
            meta = json.loads(path.read_text())
        except (OSError, ValueError):
            return False
        if isinstance(meta, dict) and meta.get("base_url") == base_url.rstrip("/") and meta.get("key") == key_id:
            return True
        # Resumed under another account, server or key: from now on its lines
        # mix two owners, so the folder ships under NOBODY's (it stays local).
        tmp = path.with_suffix(".tmp")
        tmp.write_text(json.dumps({"base_url": MIXED, "key": MIXED}))
        os.replace(tmp, path)
        log.warning("this session's trace folder was recorded under another account or key: it stays on this "
                    "machine and is no longer uploaded")
        return False
    folder.mkdir(parents=True, exist_ok=True)
    if any(folder.glob("*.jsonl")):
        log.warning("the trace folder %s has traces but no record of whose they are: they will not be uploaded",
                    folder)
        return False
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        os.write(fd, json.dumps({"base_url": base_url.rstrip("/"), "key": key_id}).encode())
    finally:
        os.close(fd)
    return True


def bind(session_id: str, base_url: str, key: str) -> bool:
    """At the worker's start, before anything is recorded: the session's folder
    belongs to this server and key. False when it already belongs to ANOTHER
    (the session resumed under a different account or server): the caller then
    records nothing into it, so no file ever mixes two accounts' traces.
    Never raises."""
    try:
        return bind_to(trace_mod.session_dir(session_id), base_url, _key_id(key))
    except OSError as exc:
        log.warning("the session's trace folder could not be stamped (%s): its traces stay here", exc)
        return True


def _lock_free(session: str) -> bool:
    """Is no worker running for this session (its lock is free)?"""
    import fcntl

    path = state_dir() / f"{session}.lock"
    if not path.exists():
        return True
    try:
        with path.open("a") as handle:
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            return True
    except OSError:
        return False


async def _http_post(url: str, body: dict[str, Any], headers: dict[str, str]) -> tuple[int, Any]:
    import httpx

    from probe.sdk.tls import ssl_context

    # The CLI's shared trust (a corporate proxy's CA, a private server's), as
    # every other client in the package.
    async with httpx.AsyncClient(timeout=60.0, verify=ssl_context()) as client:
        # Encoded here, as measured (UTF-8, not escaped), whatever httpx's default.
        data = json.dumps(body, ensure_ascii=False, allow_nan=False).encode("utf-8")
        response = await client.post(url, content=data, headers={**headers, "Content-Type": "application/json"})
    try:
        payload = response.json()
    except ValueError:
        payload = None
    return response.status_code, payload


class Shipper:
    def __init__(self, session_id: str, *, base_url: str, key: str, post: Post | None = None,
                 clock: Callable[[], float] = time.monotonic) -> None:
        self.session_id = session_id
        self.base_url = base_url.rstrip("/")
        self.url = self.base_url + ROUTE
        self.key_id = _key_id(key)
        self.headers = {"Authorization": f"Bearer {key}"}
        self._post = post or _http_post
        self.clock = clock
        self.wait_until = 0.0
        self.failures = 0
        self.drained_others = False
        self._stopping = asyncio.Event()
        self._task: asyncio.Task | None = None

    # -- the task -------------------------------------------------------------
    def start(self) -> None:
        self._task = asyncio.ensure_future(self._run())

    async def stop(self, budget_s: float = STOP_BUDGET_S) -> None:
        """One last bounded attempt, then the task ends."""
        self._stopping.set()
        if self._task is None:
            return
        try:
            await asyncio.wait_for(asyncio.shield(self._task), budget_s)
        except (asyncio.TimeoutError, Exception):  # noqa: BLE001 -- stopping never fails the worker
            self._task.cancel()

    async def _run(self) -> None:
        while True:
            try:
                await self.ship_once()
            except Exception as exc:  # noqa: BLE001 -- the uploader never takes the worker down
                log.warning("uploading the trace failed: %s: %s", type(exc).__name__, exc)
                self._backoff()
            if self._stopping.is_set():
                return
            try:
                await asyncio.wait_for(self._stopping.wait(), INTERVAL_S)
            except asyncio.TimeoutError:
                pass

    # -- where a folder may go ---------------------------------------------------
    def stamp(self, folder: Path) -> None:
        """`bind(folder, ...)` with this shipper's server and key."""
        bind_to(folder, self.base_url, self.key_id)

    def bound_here(self, folder: Path) -> bool:
        try:
            meta = json.loads((folder / META).read_text())
        except (OSError, ValueError):
            return False
        return isinstance(meta, dict) and meta.get("base_url") == self.base_url and meta.get("key") == self.key_id

    # -- one pass ---------------------------------------------------------------
    async def ship_once(self) -> int:
        """Ship what is new; returns the lines Probe took."""
        if self.clock() < self.wait_until:
            return 0
        sent = 0
        if not self.drained_others:
            # Done only once every orphan is caught up; an outage, a dark team
            # or the time budget leaves it to the next pass.
            drained, complete = await self.drain_others()
            sent += drained
            self.drained_others = complete
        own = trace_mod.session_dir(self.session_id)
        return sent + await self.ship_folder(own, own.name)

    async def _drain_one(self, folder: Path, deadline: float) -> tuple[int, bool]:
        try:
            sent = await self.ship_folder(folder, folder.name, deadline=deadline)
            return sent, not self._behind(folder)
        except Exception as exc:  # noqa: BLE001 -- one broken folder never stops the rest, or the session's own
            log.warning("uploading %s failed: %s: %s", folder.name, type(exc).__name__, exc)
            return 0, False

    async def drain_others(self, budget_s: float = DRAIN_BUDGET_S) -> tuple[int, bool]:
        """Other sessions' unshipped traces whose worker is gone: the lines
        sent, and whether every such folder is now caught up."""
        deadline = self.clock() + budget_s
        sent = 0
        try:
            folders = [p for p in trace_mod.sessions_dir().iterdir() if p.is_dir()]
        except OSError:
            return 0, True
        own = trace_mod.session_dir(self.session_id).name
        complete = True
        for folder in folders:
            if folder.name == own or not self.bound_here(folder) or not self._behind(folder):
                continue
            if not _lock_free(folder.name):
                continue  # its own worker ships it
            if self.clock() >= deadline or self.clock() < self.wait_until:
                complete = False
                break
            drained, done = await self._drain_one(folder, deadline)
            sent += drained
            complete = complete and done
        return sent, complete

    def _behind(self, folder: Path) -> bool:
        """Has a file here a COMPLETE line past its cursor? (A partial last
        line is still being written: nothing to catch up yet.)"""
        now = time.time()
        for agent in AGENTS:
            path = folder / f"{agent}.jsonl"
            try:
                info = path.stat()
                cursor = read_cursor(path)
                if now - info.st_mtime >= MAX_AGE_S or cursor >= info.st_size:
                    continue
                with path.open("rb") as handle:
                    handle.seek(cursor)
                    if handle.readline().endswith(b"\n"):
                        return True
            except OSError:
                continue
        return False

    async def ship_folder(self, folder: Path, session: str, *, deadline: float | None = None) -> int:
        if not self.bound_here(folder):
            return 0
        sent = 0
        for agent in AGENTS:
            path = folder / f"{agent}.jsonl"
            if path.exists():
                sent += await self.ship_file(path, session, agent, deadline=deadline)
            if self.clock() < self.wait_until:
                break
        return sent

    async def ship_file(self, path: Path, session: str, agent: str, *, deadline: float | None = None) -> int:
        sent = 0
        cursor = read_cursor(path)
        max_lines = BATCH_LINES
        while cursor < path.stat().st_size:
            if deadline is not None and self.clock() >= deadline:
                break
            # File reads and JSON off the event loop: the worker's own loop.
            items, following = await asyncio.to_thread(read_batch, path, cursor, None, max_lines)
            if not items:
                if following > cursor:  # only lines that are not objects: step past them
                    write_cursor(path, following)
                    cursor = following
                    continue
                break
            status, payload = await self._post(self.url, {"session_id": session, "agent": agent, "lines": items},
                                               self.headers)
            if status == 202 and not (isinstance(payload, dict) and payload.get("dark")):
                write_cursor(path, following)
                cursor = following
                sent += len(items)
                self.failures = 0
                max_lines = BATCH_LINES
                continue
            if status == 413 or (status == 422 and _code(payload) == REJECTED_CODE):
                if len(items) > 1:
                    max_lines = max(1, len(items) // 2)
                    continue
                # One line the server refuses on its own: skipped, so it can never block the file.
                skip_to = items[0]["offset"] + _line_length(path, items[0]["offset"])
                log.warning("trace upload: HTTP %s for the line at %s:%s; skipped", status, path.name,
                            items[0]["offset"])
                write_cursor(path, skip_to)
                cursor = skip_to
                max_lines = BATCH_LINES
                continue
            if status == 202 or status in (401, 403, 404, 422):
                self.wait_until = self.clock() + LONG_WAIT_S
                log.info("trace upload paused for an hour (%s)", "tracing is off for this team" if status == 202
                         else f"HTTP {status}")
            else:
                self._backoff()
                log.warning("trace upload failed (HTTP %s): trying again later", status)
            break
        return sent

    def _backoff(self) -> None:
        self.failures += 1
        self.wait_until = self.clock() + min(BACKOFF_MAX_S, BACKOFF_MIN_S * 2 ** (self.failures - 1))


def _code(payload: Any) -> str | None:
    detail = payload.get("detail") if isinstance(payload, dict) else None
    return detail.get("code") if isinstance(detail, dict) else None


def _line_length(path: Path, offset: int) -> int:
    with path.open("rb") as handle:
        handle.seek(offset)
        return len(handle.readline())


def start(session_id: str) -> Shipper | None:
    """The session's shipper, running; None when uploads are off or the machine
    has no daemon key (nothing could be sent)."""
    if not enabled() or not trace_mod.enabled():
        return None
    from probe.daemon import model as model_mod

    try:
        ep = model_mod.endpoint()
    except model_mod.NoKey:
        return None
    shipper = Shipper(session_id, base_url=ep.base_url, key=ep.key)
    shipper.start()
    return shipper
