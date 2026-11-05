"""Content-addressed uploads (``POST /v1/uploads``): local files to Dreamscale's storage.

Every file is named by its sha256. The control plane answers with presigned multipart URLs
only for the blobs your organization doesn't already have, so a re-run of an unchanged
folder sends nothing. Local state under ``~/.dreamscale/uploads/`` keeps each file's hash
(by size and mtime, so a re-run doesn't re-read it) and, per blob, the parts already sent:
an interrupted upload resumes where it stopped when the server hands back the same
multipart upload. A link storage refuses (it expired, or another upload of the same blob
finished it first: uploads in one organization resume each other's open ones) is renewed by
registering the upload again, which keeps the parts already sent.

A blob may also be a slice of a larger file (``Slice``): an ABC-VLA ``.pt`` checkpoint sends
only the stored members its build reads, each as its own blob, never its optimizer state.

A dataset's upload (``upload_dataset``) goes faster: files hash on every core and each is sent as
soon as it's hashed, the manifest going up in batches; a blob of one part takes one signed PUT;
parts stream from disk, eight at a time; a refused link (expired, or its blob stored meanwhile by
another upload) is renewed by asking again; and the server lists the parts already sent, so a
resume works from any machine.
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import os
import platform
import ssl
import time
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import httpx

from dreamscale import errors
from dreamscale.config import dreamscale_home

CONCURRENCY = 4
DATASET_CONCURRENCY = 8
DOWNLOAD_CONCURRENCY = 8
DOWNLOAD_RANGE = 64 << 20
BATCH_FILES = 1000
BATCH_SECONDS = 2.0
REFRESHES = 2  # fresh links asked in a row, when storage refuses one (HTTP 403 or 404)
DATASET_BACKOFF_S = (1.0, 2.0, 4.0, 8.0, 15.0, 30.0)
STALL_S = 600.0  # an upload gives up when no part has landed for this long
PART_ATTEMPTS = 5
RETRY_BACKOFF_S = (1.0, 2.0, 4.0, 8.0)
_RETRY_STATUS = frozenset({408, 429, 500, 502, 503, 504})
_READ_CHUNK = 8 << 20

Progress = Callable[[int, int], None]  # (bytes done, bytes total)


@dataclass(frozen=True)
class Slice:
    """``length`` bytes of ``file`` from ``offset``, uploaded as the blob of its own path."""

    file: Path
    offset: int
    length: int


def _state_path() -> Path:
    return dreamscale_home() / "uploads" / "state.json"


def _load() -> dict[str, Any]:
    try:
        state = json.loads(_state_path().read_text())
    except (OSError, ValueError):
        state = {}
    if not isinstance(state, dict):
        state = {}
    state.setdefault("files", {})
    state.setdefault("parts", {})
    return state


def _save(state: dict[str, Any]) -> None:
    path = _state_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(state, separators=(",", ":")))
    os.replace(temporary, path)


def _sha256(path: Path, advance: Callable[[int], None], offset: int = 0,
            length: int | None = None) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        handle.seek(offset)
        left = length
        while chunk := handle.read(_READ_CHUNK if left is None else min(_READ_CHUNK, left)):
            digest.update(chunk)
            advance(len(chunk))
            if left is not None:
                left -= len(chunk)
    return digest.hexdigest()


def manifest(
    root: Path, files: Sequence[tuple[str, int]], *, progress: Progress | None = None,
    slices: Mapping[str, Slice] | None = None,
) -> list[dict[str, Any]]:
    """``[{path, size, sha256}]`` for ``files`` under ``root`` (or, for a path in ``slices``,
    its slice of a file); unchanged files reuse their saved hash."""
    slices = slices or {}
    state = _load()
    cache = state["files"]
    total, done = sum(size for _, size in files), 0

    def advance(count: int) -> None:
        nonlocal done
        done += count
        if progress is not None:
            progress(done, total)

    out = []
    for rel, _ in files:
        part = slices.get(rel)
        path = part.file if part is not None else root / rel
        stat = path.stat()
        key = str(path.resolve())
        offset, size = 0, stat.st_size
        if part is not None:
            if part.offset < 0 or part.length < 0 or part.offset + part.length > stat.st_size:
                raise _upload_failed(path, "the file changed since it was read")
            key, offset, size = f"{key}#{part.offset}+{part.length}", part.offset, part.length
        hit = cache.get(key)
        if hit and hit.get("size") == stat.st_size and hit.get("mtime_ns") == stat.st_mtime_ns:
            sha = hit["sha256"]
            advance(size)
        else:
            sha = _sha256(path, advance, offset, size if part is not None else None)
            cache[key] = {"size": stat.st_size, "mtime_ns": stat.st_mtime_ns, "sha256": sha}
        out.append({"path": rel, "size": size, "sha256": sha})
    _save(state)
    return out


def _upload_failed(path: Path, cause: str) -> errors.DreamscaleError:
    return errors.DreamscaleError(
        errors.ErrorInfo(
            code="upload_failed",
            problem=f"couldn't upload {path.name}",
            cause=cause,
            fix="rerun the same command; the parts already sent aren't sent again",
        )
    )


def _tls_failed(error: ssl.SSLError) -> str:
    # A TLS record failing mid-transfer ("bad record mac") isn't mapped to an httpx error (anyio
    # re-raises it as is), and naming the TLS stack helps when it keeps failing.
    reason = error.reason or type(error).__name__
    return (
        f"the connection's encryption failed ({reason}) on Python "
        f"{platform.python_version()} with {ssl.OPENSSL_VERSION}"
    )


class _Expired(Exception):
    """Storage refused a link: it expired (HTTP 403), or the upload went away (HTTP 404), often
    because another upload of the same blob completed it."""


_REFUSED = frozenset({403, 404})


async def _put(http: httpx.AsyncClient, url: str, data: bytes, path: Path) -> str:
    for attempt in range(PART_ATTEMPTS):
        try:
            resp = await http.put(url, content=data)
        except httpx.TransportError as error:
            cause = f"the network failed ({type(error).__name__})"
        except ssl.SSLCertVerificationError as error:  # retrying can't make it trusted
            raise _upload_failed(
                path, f"storage's certificate couldn't be verified ({error.verify_message})"
            ) from None
        except ssl.SSLError as error:
            cause = _tls_failed(error)
        else:
            if resp.status_code < 300 and resp.headers.get("etag"):
                return resp.headers["etag"]
            cause = f"storage answered HTTP {resp.status_code}"
            if resp.status_code in _REFUSED:  # retrying the same URL can't help; a fresh one can
                raise _Expired(cause)
            if resp.status_code < 300 or resp.status_code not in _RETRY_STATUS:
                raise _upload_failed(path, cause)
        if attempt + 1 < PART_ATTEMPTS:
            await asyncio.sleep(RETRY_BACKOFF_S[min(attempt, len(RETRY_BACKOFF_S) - 1)])
    raise _upload_failed(path, cause)


def _read(path: Path, offset: int, length: int) -> bytes:
    with path.open("rb") as handle:
        handle.seek(offset)
        return handle.read(length)


async def upload(
    client: Any,
    root: Path,
    files: list[dict[str, Any]],
    *,
    progress: Progress | None = None,
    transport: httpx.AsyncBaseTransport | None = None,
    kind: str = "dataset",
    base_model: str | None = None,
    slices: Mapping[str, Slice] | None = None,
) -> dict[str, Any]:
    """Send what the server is missing, then complete the upload. Returns the completed
    upload (``{id, status, files, bytes}``) with ``sent``: the bytes this call uploaded.
    ``kind``: a dataset to train on, or a ``checkpoint`` to deploy. ``slices``: as for
    ``manifest``. A link storage refuses registers the upload again (a blob another upload
    stored meanwhile is then not missing) and the rest goes on fresh links."""
    slices = slices or {}
    paths = {
        entry["sha256"]: (slices[entry["path"]].file, slices[entry["path"]].offset)
        if entry["path"] in slices else (root / entry["path"], 0)
        for entry in files
    }
    # Read once: another upload on this machine saving its own parts doesn't lose ours.
    state = _load()
    sent = 0
    tried: set[str] = set()  # blobs of any round, whose saved parts go once complete

    async def send_round() -> tuple[dict, list[dict], tuple[Path, str] | None, int]:
        """Register the upload and send its missing parts: (the upload, its missing blobs, the
        first refused link's file and cause, how many parts landed)."""
        nonlocal sent
        created = await client.create_upload(
            files, kind=kind, **({"base_model": base_model} if base_model is not None else {})
        )
        missing = [blob for blob in created.get("missing") or [] if isinstance(blob, dict)]
        tried.update(blob["sha256"] for blob in missing)
        total = sum(int(blob["size"]) for blob in missing)
        done = landed = 0
        refused: tuple[Path, str] | None = None
        jobs = []
        for blob in missing:
            sha, part_size = blob["sha256"], int(blob["part_size"])
            saved = state["parts"].get(sha) or {}
            if saved.get("upload_id") != blob.get("upload_id"):
                saved = {"upload_id": blob.get("upload_id"), "etags": {}}
                state["parts"][sha] = saved
            for part in blob.get("parts") or []:
                number = int(part["number"])
                offset = (number - 1) * part_size
                length = max(min(part_size, int(blob["size"]) - offset), 0)
                if str(number) in saved["etags"]:
                    done += length
                else:
                    jobs.append((sha, number, part["url"], offset, length))
        if progress is not None:
            progress(done, total)
        _save(state)
        limit = asyncio.Semaphore(CONCURRENCY)

        async def send(http: httpx.AsyncClient, sha: str, number: int, url: str, offset: int,
                       length: int) -> None:
            nonlocal done, sent, landed, refused
            path, start = paths[sha]
            async with limit:
                if refused is not None:  # its link is likely refused too: renewed next round
                    return
                data = await asyncio.to_thread(_read, path, start + offset, length)
                try:
                    etag = await _put(http, url, data, path)
                except _Expired as error:
                    refused = refused or (path, str(error))
                    return
            state["parts"][sha]["etags"][str(number)] = etag
            _save(state)
            done += length
            sent += length
            landed += 1
            if progress is not None:
                progress(done, total)

        try:
            async with (
                httpx.AsyncClient(timeout=httpx.Timeout(300.0, connect=10.0),
                                  transport=transport) as http,
                asyncio.TaskGroup() as group,
            ):
                for job in jobs:
                    group.create_task(send(http, *job))
        except BaseExceptionGroup as failed:  # the first failed part says what went wrong
            raise failed.exceptions[0] from None
        return created, missing, refused, landed

    quiet = 0  # rounds in a row that were refused with nothing landing
    while True:
        created, missing, refused, landed = await send_round()
        if refused is None:
            break
        quiet = 0 if landed else quiet + 1
        if quiet > REFRESHES:
            raise _upload_failed(*refused)
    parts = {
        blob["sha256"]: [
            {"number": int(number), "etag": etag}
            for number, etag in sorted(
                state["parts"][blob["sha256"]]["etags"].items(), key=lambda item: int(item[0])
            )
        ]
        for blob in missing
    }
    completed = await client.complete_upload(created["id"], parts, kind=kind)
    state = _load()
    for sha in tried:
        state["parts"].pop(sha, None)
    _save(state)
    return {**completed, "id": completed.get("id") or created["id"], "sent": sent}


# --- a dataset's upload ---------------------------------------------------------------------


DatasetProgress = Callable[[int, int, int], None]  # (bytes checked, bytes sent, bytes total)


class _Throttle:
    """How many parts go at once: halved when the network drops one (some links reset parallel
    uploads), back up one at a time as parts land. It also knows when the last one landed: a
    part keeps retrying while others get through."""

    def __init__(self, limit: int) -> None:
        self.most = self.limit = max(limit, 1)
        self.active = self.landed = 0
        self.landed_at = time.monotonic()
        self._changed = asyncio.Condition()

    async def __aenter__(self) -> None:
        async with self._changed:
            await self._changed.wait_for(lambda: self.active < self.limit)
            self.active += 1

    async def __aexit__(self, *_exc) -> None:
        async with self._changed:
            self.active -= 1
            self._changed.notify_all()

    def dropped(self) -> None:
        self.limit, self.landed = max(self.limit // 2, 1), 0

    def stalled(self) -> bool:
        return time.monotonic() - self.landed_at > STALL_S

    def landed_one(self) -> None:
        self.landed_at = time.monotonic()
        self.landed += 1
        if self.landed >= self.limit * 2 and self.limit < self.most:
            self.limit, self.landed = self.limit + 1, 0


async def _put_stream(
    http: httpx.AsyncClient, url: str, path: Path, offset: int, length: int,
    advance: Callable[[int], None], throttle: _Throttle,
) -> str | None:
    """PUT ``length`` bytes of ``path`` from ``offset``, read as they go. The answer's ETag."""
    attempt = 0
    while True:
        sent = 0

        async def body():
            nonlocal sent
            with path.open("rb") as handle:
                handle.seek(offset)
                left = length
                while left > 0:
                    chunk = await asyncio.to_thread(handle.read, min(_READ_CHUNK, left))
                    if not chunk:
                        raise _upload_failed(path, "the file changed since it was read")
                    left -= len(chunk)
                    sent += len(chunk)
                    advance(len(chunk))
                    yield chunk

        try:
            async with throttle:
                resp = await http.put(
                    url, content=body(), headers={"Content-Length": str(length)}
                )
        except httpx.TransportError as error:
            cause = f"the network failed ({type(error).__name__})"
            throttle.dropped()
        except ssl.SSLCertVerificationError as error:  # retrying can't make it trusted
            raise _upload_failed(
                path, f"storage's certificate couldn't be verified ({error.verify_message})"
            ) from None
        except ssl.SSLError as error:
            cause = _tls_failed(error)
            throttle.dropped()
        else:
            if resp.status_code < 300:
                throttle.landed_one()
                return resp.headers.get("etag")
            cause = f"storage answered HTTP {resp.status_code}"
            if resp.status_code in _REFUSED:
                advance(-sent)
                raise _Expired(cause)
            if resp.status_code not in _RETRY_STATUS:
                raise _upload_failed(path, cause)
            throttle.dropped()
        advance(-sent)
        if throttle.stalled():
            raise _upload_failed(path, cause)
        await asyncio.sleep(DATASET_BACKOFF_S[min(attempt, len(DATASET_BACKOFF_S) - 1)])
        attempt += 1


async def upload_dataset(
    client: Any,
    ref: str,
    root: Path,
    files: Sequence[tuple[str, int]],
    *,
    progress: DatasetProgress | None = None,
    transport: httpx.AsyncBaseTransport | None = None,
    concurrency: int = DATASET_CONCURRENCY,
) -> dict[str, Any]:
    """Upload a folder's files as the dataset's next version. Returns the complete call's answer
    (``{dataset, version, unchanged}``) with ``sent``, the bytes this call uploaded."""
    total = sum(size for _, size in files)
    started = time.monotonic()
    upload = await client.create_dataset_upload(ref, size=total)
    upload_id = upload["id"]
    state = _load()
    cache = state["files"]
    checked = sent = 0
    paths: dict[str, Path] = {}
    entries: dict[str, dict[str, Any]] = {}
    manifest: list[dict[str, Any]] = []
    pending: list[dict[str, Any]] = []
    parts: dict[str, list[dict[str, Any]]] = {}
    multiparts: dict[str, str] = {}  # sha256 -> the multipart upload its parts went to
    stored: set[str] = set()  # blobs another upload stored meanwhile
    seen: set[str] = set()
    flushed_at = time.monotonic()
    flushing = asyncio.Lock()
    hashing = asyncio.Semaphore(max(os.cpu_count() or 2, 2))
    throttle = _Throttle(concurrency)

    def report() -> None:
        if progress is not None:
            progress(checked, sent, total)

    def advance(count: int) -> None:
        nonlocal sent
        sent += count
        report()

    async def renew(sha: str) -> dict[str, Any] | None:
        answer = await client.add_dataset_upload_files(ref, upload_id, [entries[sha]])
        return next((b for b in answer.get("missing") or [] if b["sha256"] == sha), None)

    async def send_one(sha: str, url: str, offset: int, length: int, number: int | None) -> None:
        path = paths[sha]
        for refresh in range(REFRESHES + 1):
            if sha in stored:
                return
            try:
                etag = await _put_stream(http, url, path, offset, length, advance, throttle)
                break
            except _Expired:
                fresh = await renew(sha) if refresh < REFRESHES else None
                if fresh is None and refresh >= REFRESHES:
                    raise _upload_failed(path, "storage refused the upload's link") from None
                if fresh is None:
                    stored.add(sha)  # meanwhile, as another upload of it finished
                    return
                if number is None:
                    url = fresh["url"]
                    continue
                if fresh.get("upload_id") != multiparts[sha]:
                    # Its multipart upload went away unfinished: the parts sent there are lost.
                    raise _upload_failed(path, "storage started this file's upload again") from None
                listed = next((p for p in fresh.get("done") or [] if int(p["number"]) == number),
                              None)
                if listed is not None:  # sent meanwhile, by another upload of the same blob
                    advance(length)
                    parts[sha].append({"number": number, "etag": listed["etag"]})
                    return
                url = next(p["url"] for p in fresh["parts"] if int(p["number"]) == number)
        if number is not None:
            if not etag:
                raise _upload_failed(path, "storage answered without an ETag")
            parts[sha].append({"number": number, "etag": etag})

    def send_blob(group: asyncio.TaskGroup, blob: dict[str, Any]) -> None:
        sha = blob["sha256"]
        if sha in seen:
            return
        seen.add(sha)
        size = int(blob["size"])
        if blob.get("url"):
            group.create_task(send_one(sha, blob["url"], 0, size, None))
            return
        part_size = int(blob["part_size"])
        multiparts[sha] = blob.get("upload_id")
        parts[sha] = [{"number": int(p["number"]), "etag": p["etag"]}
                      for p in blob.get("done") or []]
        for done in parts[sha]:  # sent before, from any machine
            advance(max(min(part_size, size - (done["number"] - 1) * part_size), 0))
        for part in blob.get("parts") or []:
            number = int(part["number"])
            offset = (number - 1) * part_size
            group.create_task(send_one(
                sha, part["url"], offset, max(min(part_size, size - offset), 0), number
            ))

    async def flush(group: asyncio.TaskGroup) -> None:
        nonlocal pending, flushed_at
        async with flushing:
            while pending:
                batch, pending = pending[:BATCH_FILES], pending[BATCH_FILES:]
                flushed_at = time.monotonic()
                answer = await client.add_dataset_upload_files(ref, upload_id, batch)
                for blob in answer.get("missing") or []:
                    send_blob(group, blob)

    async def hash_one(group: asyncio.TaskGroup, rel: str, size: int) -> None:
        nonlocal checked
        path = root / rel
        stat = path.stat()
        key = str(path.resolve())
        hit = cache.get(key)
        if hit and hit.get("size") == stat.st_size and hit.get("mtime_ns") == stat.st_mtime_ns:
            sha = hit["sha256"]
        else:
            async with hashing:
                sha = await asyncio.to_thread(_sha256, path, lambda _count: None)
            cache[key] = {"size": stat.st_size, "mtime_ns": stat.st_mtime_ns, "sha256": sha}
        entry = {"path": rel, "size": stat.st_size, "sha256": sha}
        paths.setdefault(sha, path)
        entries.setdefault(sha, entry)
        manifest.append(entry)
        pending.append(entry)
        checked += stat.st_size
        report()
        if len(pending) >= BATCH_FILES or time.monotonic() - flushed_at >= BATCH_SECONDS:
            await flush(group)

    try:
        async with (
            httpx.AsyncClient(timeout=httpx.Timeout(300.0, connect=10.0), transport=transport)
            as http,
            asyncio.TaskGroup() as group,
        ):
            await asyncio.gather(*(hash_one(group, rel, size) for rel, size in files))
            await flush(group)
    except BaseExceptionGroup as failed:  # the first failed part says what went wrong
        raise failed.exceptions[0] from None
    finally:
        _save(state)
    done = await client.complete_dataset_upload(
        ref, upload_id,
        {sha: sorted(listed, key=lambda p: p["number"]) for sha, listed in parts.items()},
        bytes_sent=sent, seconds=round(time.monotonic() - started, 1),
        parts_in_flight=concurrency,
    )
    return {**done, "sent": sent}


# --- a dataset's download -------------------------------------------------------------------


def _same_file(path: Path, size: int, sha256: str) -> bool:
    if not path.is_file() or path.stat().st_size != size:
        return False
    return _sha256(path, lambda _count: None) == sha256


async def download_dataset(
    client: Any,
    ref: str,
    version: int,
    dest: Path,
    *,
    progress: Progress | None = None,
    transport: httpx.AsyncBaseTransport | None = None,
) -> dict[str, int]:
    """A version's files into ``dest``: a file already there with the same sha256 is skipped, and
    a large one comes in ranges at once. ``{files, bytes, sent}``."""
    listed: list[dict[str, Any]] = []
    cursor: int | None = None
    while True:
        page = await client.dataset_files(ref, version, cursor=cursor, links=True)
        listed += page.get("files") or []
        cursor = page.get("next_cursor")
        if cursor is None:
            break
    total = sum(int(f["size"]) for f in listed)
    done = fetched = 0
    gate = asyncio.Semaphore(DOWNLOAD_CONCURRENCY)

    def advance(count: int) -> None:
        nonlocal done
        done += count
        if progress is not None:
            progress(done, total)

    async def get_range(http, url: str, path: Path, start: int, end: int) -> None:
        nonlocal fetched
        for attempt in range(PART_ATTEMPTS):
            wrote = 0
            try:
                async with gate:
                    headers = {"Range": f"bytes={start}-{end}"}
                    async with http.stream("GET", url, headers=headers) as resp:
                        if resp.status_code >= 400:
                            cause = f"storage answered HTTP {resp.status_code}"
                            if resp.status_code not in _RETRY_STATUS:
                                raise _download_failed(path, cause)
                            raise httpx.TransportError(cause)
                        with path.open("r+b") as handle:
                            handle.seek(start)
                            async for chunk in resp.aiter_bytes(_READ_CHUNK):
                                await asyncio.to_thread(handle.write, chunk)
                                wrote += len(chunk)
                                advance(len(chunk))
                fetched += wrote
                return
            except httpx.TransportError as error:
                advance(-wrote)
                if attempt + 1 == PART_ATTEMPTS:
                    raise _download_failed(path, str(error)) from None
                await asyncio.sleep(RETRY_BACKOFF_S[min(attempt, len(RETRY_BACKOFF_S) - 1)])

    async def get_file(http, entry: dict[str, Any]) -> None:
        path = dest / entry["path"]
        size = int(entry["size"])
        if await asyncio.to_thread(_same_file, path, size, entry["sha256"]):
            advance(size)
            return
        path.parent.mkdir(parents=True, exist_ok=True)
        partial = path.with_name(path.name + ".part")
        with partial.open("wb") as handle:
            handle.truncate(size)
        if size:
            await asyncio.gather(*(
                get_range(http, entry["url"], partial, start,
                          min(start + DOWNLOAD_RANGE, size) - 1)
                for start in range(0, size, DOWNLOAD_RANGE)
            ))
        if await asyncio.to_thread(_sha256, partial, lambda _count: None) != entry["sha256"]:
            partial.unlink(missing_ok=True)
            raise _download_failed(path, "what arrived differs from what's stored")
        os.replace(partial, path)

    try:
        async with (
            httpx.AsyncClient(timeout=httpx.Timeout(300.0, connect=10.0), transport=transport)
            as http,
            asyncio.TaskGroup() as group,
        ):
            for entry in listed:
                group.create_task(get_file(http, entry))
    except BaseExceptionGroup as failed:
        raise failed.exceptions[0] from None
    return {"files": len(listed), "bytes": total, "sent": fetched}


def _download_failed(path: Path, cause: str) -> errors.DreamscaleError:
    return errors.DreamscaleError(
        errors.ErrorInfo(
            code="download_failed",
            problem=f"couldn't download {path.name}",
            cause=cause,
            fix="rerun the same command; files already here aren't fetched again",
        )
    )
