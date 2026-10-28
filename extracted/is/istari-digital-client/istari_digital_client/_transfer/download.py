"""Download engine: streaming single-stream and ranged parallel downloads with inline verification.

``download_to`` writes to a temp file beside the destination and renames only after
the salted SHA-384 verifies; ``read_into_memory`` fills one preallocated buffer.
Both probe the object with a ranged GET first, so an empty object (416), a server
that ignores ``Range`` (200) and a ranged reply (206) are all handled from one
request whose body is reused rather than re-downloaded.
"""

from __future__ import annotations

import io
import logging
import os
import re
import secrets
import shutil
import threading
import time
from collections.abc import Callable
from concurrent.futures import FIRST_COMPLETED, Future, ThreadPoolExecutor, wait
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Protocol

import urllib3
import urllib3.exceptions

from istari_digital_client import native_crypto
from istari_digital_client._transfer.errors import (
    ContentVerificationError,
    HttpError,
    InsufficientDiskSpaceError,
    RetriesExhausted,
    TransferCancelledError,
    TransferError,
)
from istari_digital_client._transfer.events import (
    EventForwarder,
    EventKind,
    ProgressCallback,
    TransferEvent,
)
from istari_digital_client._transfer.http import (
    Deadline,
    RawTransport,
    TransferSettings,
    check_cancel,
    retry_control_call,
    transfer_request,
)
from istari_digital_client._transfer.plan import clamp_part_size, split_ranges
from istari_digital_client._transfer.upload import (
    URL_REFRESH_MARGIN_SECS,
    TemporaryUrlLike,
    _is_fresh,
    refresh_margin,
)

logger = logging.getLogger("istari_digital_client.transfer")

STREAM_CHUNK = 1024 * 1024
VERIFY_CHUNK = 8 * 1024 * 1024
PROGRESS_STEP = 8 * 1024 * 1024
PARTIAL_SUFFIX = ".istari-partial"


class DownloadBackend(Protocol):
    """Registry calls and error factories the download engine needs."""

    @property
    def transport(self) -> RawTransport: ...

    def presign_download(self, sha: str) -> TemporaryUrlLike: ...

    def invalidate_auth(self) -> bool: ...

    def api_error(self, error: HttpError) -> Exception: ...

    def transfer_failed(
        self, message: str, *, token: Any, cause: BaseException | None
    ) -> Exception: ...


def _verify_error(sha: str, exc: BaseException) -> ContentVerificationError:
    return ContentVerificationError(
        f"downloaded content does not match sha {sha}: {exc}"
    )


class _CombinedCancel(threading.Event):
    """Expose caller cancellation and worker shutdown as one interruptible event."""

    def __init__(self, *events: threading.Event | None) -> None:
        super().__init__()
        self._events = tuple(event for event in events if event is not None)

    def is_set(self) -> bool:
        return super().is_set() or any(event.is_set() for event in self._events)

    def wait(self, timeout: float | None = None) -> bool:
        end = None if timeout is None else time.monotonic() + timeout
        while not self.is_set():
            remaining = None if end is None else end - time.monotonic()
            if remaining is not None and remaining <= 0:
                return self.is_set()
            # No thread or callback registration is needed to watch both events.
            super().wait(0.05 if remaining is None else min(0.05, remaining))
        return True


class _UrlSource:
    """Single-flight supply of the download URL, refreshed near expiry and on 403."""

    def __init__(
        self,
        backend: DownloadBackend,
        settings: TransferSettings,
        sha: str,
        cancel: threading.Event | None,
    ) -> None:
        self._backend = backend
        self._settings = settings
        self._sha = sha
        self._cancel = cancel
        self._lock = threading.Lock()
        self._current: TemporaryUrlLike | None = None
        self._margin = URL_REFRESH_MARGIN_SECS
        self.refreshes = 0

    def _mint(self, cancel: threading.Event) -> TemporaryUrlLike:
        def mint() -> TemporaryUrlLike:
            check_cancel(cancel)
            return self._backend.presign_download(self._sha)

        presigned = retry_control_call(
            mint,
            settings=self._settings,
            invalidate_auth=self._backend.invalidate_auth,
            cancel=cancel,
        )
        self.refreshes += 1
        self._margin = refresh_margin([presigned], datetime.now(timezone.utc))
        return presigned

    def _fresh(self, entry: TemporaryUrlLike) -> bool:
        return _is_fresh(entry, datetime.now(timezone.utc), self._margin)

    def _acquire(self, cancel: threading.Event) -> None:
        while True:
            check_cancel(cancel)
            if self._lock.acquire(timeout=0.05):
                break

    def get(self, stop: threading.Event | None = None) -> str:
        """The current URL, minting or refreshing it under one cancellable lock."""
        cancel = _CombinedCancel(self._cancel, stop)
        self._acquire(cancel)
        try:
            check_cancel(cancel)
            if self._current is None or not self._fresh(self._current):
                self._current = self._mint(cancel)
            return self._current.url
        finally:
            self._lock.release()

    def refresh(self, failed_url: str, stop: threading.Event | None = None) -> str:
        """Replace ``failed_url`` after a 403; another thread's replacement is reused.

        A re-minted URL that is already expired (a registry cache handing back an
        old signature) is reported as ``failed_url`` so the caller backs off and
        asks again instead of spending its one fresh-URL attempt on it.
        """
        cancel = _CombinedCancel(self._cancel, stop)
        self._acquire(cancel)
        try:
            check_cancel(cancel)
            if self._current is not None and self._current.url != failed_url:
                return self._current.url
            minted = self._mint(cancel)
            if minted.url != failed_url and not _is_fresh(
                minted, datetime.now(timezone.utc), 0.0
            ):
                logger.debug(
                    "refreshed download URL for %s is already expired; backing off",
                    self._sha,
                )
                return failed_url
            self._current = minted
            return minted.url
        finally:
            self._lock.release()


def _content_range_total(response: Any) -> int:
    header = response.headers.get("Content-Range", "")
    match = re.fullmatch(r"bytes (\d+)-(\d+)/(\d+)", header)
    if match is not None:
        start, end, total = map(int, match.groups())
        if start <= end < total:
            return total
    raise TransferError(
        f"206 response has unknown or malformed Content-Range: {header!r}"
    )


def _content_range_start(response: Any) -> int | None:
    header = response.headers.get("Content-Range", "")
    if header.startswith("bytes ") and "-" in header:
        start = header[6:].split("-", 1)[0].strip()
        if start.isdigit():
            return int(start)
    return None


def _content_length(response: Any) -> int | None:
    value = response.headers.get("Content-Length")
    return int(value) if value and value.isdigit() else None


@dataclass
class _Probe:
    response: (
        Any | None
    )  # open response positioned at byte 0, or None for an empty object
    total: int | None  # None when the server sent no length at all
    ranged: bool  # the server honoured Range (206)


def _probe(
    backend: DownloadBackend,
    settings: TransferSettings,
    urls: _UrlSource,
    range_len: int,
    cancel: threading.Event | None,
    progress: _Progress,
) -> _Probe:
    """``GET Range: bytes=0-(range_len-1)``; 416 means empty, 200 means Range ignored."""
    try:
        response = transfer_request(
            backend.transport,
            "GET",
            url=urls.get,
            refresh_url=urls.refresh,
            headers={"Range": f"bytes=0-{range_len - 1}"},
            settings=settings,
            deadline=Deadline(settings.retry.deadline, lazy=True),
            cancel=cancel,
            on_retry=lambda n, _w: progress.event(EventKind.RETRY, attempt=n),
            on_represign=lambda n: progress.event(EventKind.REPRESIGN, attempt=n),
            decode_content=False,
        )
    except HttpError as exc:
        if exc.status == 416:
            return _Probe(None, 0, True)
        raise backend.api_error(exc) from exc
    except RetriesExhausted as exc:
        raise backend.transfer_failed(
            f"download probe failed after {exc.attempts} attempts: {exc.last!r}",
            token=None,
            cause=exc.last,
        ) from exc.last
    if response.status == 206:
        try:
            total = _content_range_total(response)
            if _content_range_start(response) != 0:
                raise TransferError("206 probe response does not begin at byte zero")
        except BaseException:
            response.close()
            raise
        return _Probe(response, total, True)
    return _Probe(response, _content_length(response), False)


def _disk_preflight(total: int, dest_dir: Path) -> None:
    free = shutil.disk_usage(dest_dir).free
    if total > free:
        raise InsufficientDiskSpaceError(dest_dir, total, free)


def partial_path(dest: Path) -> Path:
    """Return a fresh ``dest.parent/.<name>.<rand>.istari-partial`` name; the file is not created."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    return dest.parent / f".{dest.name}.{secrets.token_hex(16)}{PARTIAL_SUFFIX}"


def open_partial(path: Path) -> io.FileIO:
    """Create ``path`` exclusively for writing, in binary mode, honouring the umask."""
    # The caller names the file before this creates it, so an interrupt that lands
    # before the caller holds the file object still leaves it a path to unlink, and
    # the unreferenced FileIO closes its descriptor as the interrupt unwinds. With
    # 128 random bits a name taken by another file means a broken RNG, not a retry.
    return io.FileIO(path, "xb")


def check_written(path: Path, expected: int) -> None:
    """Raise ``ContentVerificationError`` unless ``path`` holds exactly ``expected`` bytes."""
    # Inline verification hashes the bytes received, not what reached the disk.
    actual = os.stat(path).st_size
    if actual != expected:
        raise ContentVerificationError(
            f"{path} holds {actual} bytes after writing {expected}"
        )


def _unlink_quietly(path: Path | None) -> None:
    if path is not None:
        try:
            path.unlink()
        except FileNotFoundError:
            pass
        except OSError:
            logger.warning("could not remove partial download %s", path, exc_info=True)


class _Progress:
    """Cumulative byte counter that emits ``part_done`` about every 8 MiB."""

    def __init__(self, progress: ProgressCallback | None, total: int | None) -> None:
        self._progress = (
            progress
            if isinstance(progress, EventForwarder)
            else EventForwarder(progress)
        )
        self.total = total
        self.done = 0
        self._last = 0
        self._lock = threading.Lock()

    def add(
        self, n: int, *, part_number: int | None = None, force: bool = False
    ) -> None:
        # Deliver under the same lock that advanced the counter: workers finish ranges
        # concurrently, and emitting after release could hand a callback 15 MiB then 10 MiB.
        with self._lock:
            self.done += n
            if not force and self.done - self._last < PROGRESS_STEP:
                return
            self._last = self.done
            self._progress(
                TransferEvent(
                    EventKind.PART_DONE, self.done, self.total, part_number=part_number
                )
            )

    def event(
        self,
        kind: EventKind,
        *,
        part_number: int | None = None,
        attempt: int | None = None,
    ) -> None:
        """Emit a non-byte event carrying the current count, ordered with ``part_done``."""
        with self._lock:
            self._progress(
                TransferEvent(
                    kind,
                    self.done,
                    self.total,
                    part_number=part_number,
                    attempt=attempt,
                )
            )


def _stream_body(
    response: Any,
    sink: Callable[[bytes], None],
    expected: int | None,
    cancel: threading.Event | None,
    progress: _Progress | None,
) -> int:
    """Copy a response body into ``sink`` in 1 MiB chunks; a short body raises IncompleteRead."""
    got = 0
    for chunk in response.stream(STREAM_CHUNK, decode_content=False):
        check_cancel(cancel)
        if not chunk:
            continue
        sink(chunk)
        got += len(chunk)
        if progress is not None:
            progress.add(len(chunk))
    check_cancel(cancel)
    if expected is not None and got != expected:
        raise urllib3.exceptions.IncompleteRead(got, expected - got)
    return got


def _resume_stream(
    backend: DownloadBackend,
    settings: TransferSettings,
    urls: _UrlSource,
    *,
    sha: str,
    offset: int,
    total: int | None,
    sink: Callable[[bytes], None],
    cancel: threading.Event | None,
    progress: _Progress,
) -> int:
    """Fetch ``bytes=offset-`` with retries, tolerating a server that ignores Range.

    ``sink`` is append-only, so a retry after a mid-body failure asks for
    ``bytes={offset + delivered}-`` rather than re-downloading and dropping what
    already arrived. New bytes renew an active retry window; healthy initial
    streaming does not start it. The deadline bounds time without new progress,
    not the whole download. Returns the bytes delivered to ``sink``.
    """
    delivered = 0
    deadline = Deadline(settings.retry.deadline, lazy=True)

    def range_header() -> dict[str, str]:
        return {"Range": f"bytes={offset + delivered}-"}

    def consume(response: Any) -> int:
        nonlocal delivered
        start = offset + delivered
        before = delivered
        if response.status == 206:
            response_total = _content_range_total(response)
            if total is not None and response_total != total:
                raise TransferError("206 response changed the download total")
        ignored_range = response.status == 200
        if ignored_range:
            skip = start  # Range ignored: discard what we already have
        elif _content_range_start(response) not in (None, start):
            raise urllib3.exceptions.ProtocolError("unexpected Content-Range start")
        else:
            skip = 0
        state = {"skip": skip}

        def skipping_sink(chunk: bytes) -> None:
            nonlocal delivered
            if state["skip"]:
                drop = min(state["skip"], len(chunk))
                state["skip"] -= drop
                chunk = chunk[drop:]
            if chunk:
                sink(chunk)
                delivered += len(chunk)
                # Delivered bytes are append-only; discarded prefixes never renew the window.
                deadline.reset()
                progress.add(len(chunk))

        expected = None if total is None else total - (0 if ignored_range else start)
        try:
            _stream_body(response, skipping_sink, expected, cancel, None)
        except (urllib3.exceptions.HTTPError, ConnectionError) as exc:
            if delivered > before:
                logger.debug(
                    "download of %s: resuming from offset %d after delivering %d bytes (%r)",
                    sha,
                    offset + delivered,
                    delivered - before,
                    exc,
                )
            raise
        return delivered

    try:
        return int(
            transfer_request(
                backend.transport,
                "GET",
                url=urls.get,
                refresh_url=urls.refresh,
                headers=range_header,
                settings=settings,
                deadline=deadline,
                cancel=cancel,
                on_retry=lambda n, _w: progress.event(EventKind.RETRY, attempt=n),
                on_represign=lambda n: progress.event(EventKind.REPRESIGN, attempt=n),
                decode_content=False,
                consume=consume,
            )
        )
    except HttpError as exc:
        raise backend.api_error(exc) from exc
    except RetriesExhausted as exc:
        raise backend.transfer_failed(
            f"download failed after {exc.attempts} attempts: {exc.last!r}",
            token=None,
            cause=exc.last,
        ) from exc.last


def _single_stream_to(
    backend: DownloadBackend,
    settings: TransferSettings,
    urls: _UrlSource,
    probe: _Probe,
    *,
    sha: str,
    salt: str,
    fd: int,
    cancel: threading.Event | None,
    progress: _Progress,
) -> int:
    """Stream the whole object into ``fd`` while hashing inline; returns bytes written."""
    verifier = native_crypto.VerifyingHasher(sha, salt)
    written = 0

    def sink(chunk: bytes) -> None:
        nonlocal written
        view = memoryview(chunk)
        while view:  # os.write may be short on a nearly full disk
            view = view[os.write(fd, view) :]
        verifier.update(chunk)
        written += len(chunk)

    total = probe.total
    if probe.response is not None:
        try:
            expected = (
                None
                if total is None
                else min(total, _content_length(probe.response) or total)
            )
            _stream_body(probe.response, sink, expected, cancel, progress)
        except (urllib3.exceptions.HTTPError, ConnectionError) as exc:
            if total is None:
                raise
            logger.debug(
                "probe body ended early at %d bytes (%r); resuming", written, exc
            )
        finally:
            probe.response.close()
    while total is not None and written < total:
        _resume_stream(
            backend,
            settings,
            urls,
            sha=sha,
            offset=written,
            total=total,
            sink=sink,
            cancel=cancel,
            progress=progress,
        )
    check_cancel(cancel)
    try:
        verifier.finalize()
    except ValueError as exc:
        raise _verify_error(sha, exc) from exc
    check_cancel(cancel)
    return written


def _verify_file(
    path: Path, sha: str, salt: str, cancel: threading.Event | None
) -> None:
    verifier = native_crypto.VerifyingHasher(sha, salt)
    buf = bytearray(VERIFY_CHUNK)
    view = memoryview(buf)
    with open(path, "rb") as f:
        while True:
            check_cancel(cancel)
            got = f.readinto(view)
            if not got:
                break
            verifier.update(view[:got])
    try:
        verifier.finalize()
    except ValueError as exc:
        raise _verify_error(sha, exc) from exc


def _ranged_to(
    backend: DownloadBackend,
    settings: TransferSettings,
    urls: _UrlSource,
    probe: _Probe,
    *,
    total: int,
    range_size: int,
    partial: Path,
    fd: int,
    cancel: threading.Event | None,
    progress: _Progress,
) -> None:
    """Fill the preallocated ``partial`` from parallel ranged GETs; the probe body is range 0."""
    ranges = split_ranges(total, range_size)
    os.ftruncate(fd, total)
    assert probe.response is not None
    first_len = ranges[0][1]
    with open(partial, "r+b") as first:

        def write_first(chunk: bytes) -> None:
            first.write(chunk)

        try:
            # Count range 1 only once it has fully landed, like every other range;
            # per-chunk accounting here would be double-counted by the re-fetch below.
            _stream_body(probe.response, write_first, first_len, cancel, None)
            first_done = True
        except (urllib3.exceptions.HTTPError, ConnectionError) as exc:
            logger.debug(
                "probe body for range 1 failed (%r); it will be re-fetched", exc
            )
            first_done = False
        finally:
            probe.response.close()
    pending = list(enumerate(ranges, start=1))
    if first_done:
        pending = pending[1:]
        progress.add(first_len, part_number=1, force=True)
    stop = threading.Event()
    lookahead = 2 * settings.concurrency

    worker_cancel = _CombinedCancel(cancel, stop)
    failures: list[BaseException] = []
    failure_lock = threading.Lock()

    def fail(error: BaseException) -> None:
        with failure_lock:
            if not failures:
                failures.append(error)
            stop.set()

    def fetch(part_number: int, offset: int, length: int) -> int:
        check_cancel(worker_cancel)
        deadline = Deadline(settings.retry.deadline, lazy=True)
        high_water = 0

        def consume(response: Any) -> int:
            nonlocal high_water
            if response.status == 206 and _content_range_total(response) != total:
                raise TransferError("206 response changed the download total")
            if response.status != 206 or _content_range_start(response) != offset:
                raise urllib3.exceptions.ProtocolError(
                    "server ignored the Range header"
                )
            with open(partial, "r+b") as handle:
                handle.seek(offset)
                got = 0
                for chunk in response.stream(STREAM_CHUNK, decode_content=False):
                    check_cancel(worker_cancel)
                    handle.write(chunk)
                    got += len(chunk)
                    if got > high_water:
                        high_water = got
                        deadline.reset()
            check_cancel(worker_cancel)
            if got != length:
                raise urllib3.exceptions.IncompleteRead(got, length - got)
            return got

        try:
            got = int(
                transfer_request(
                    backend.transport,
                    "GET",
                    url=lambda: urls.get(worker_cancel),
                    refresh_url=lambda failed: urls.refresh(failed, worker_cancel),
                    headers={"Range": f"bytes={offset}-{offset + length - 1}"},
                    settings=settings,
                    deadline=deadline,
                    cancel=worker_cancel,
                    on_retry=lambda n, _w: progress.event(
                        EventKind.RETRY, part_number=part_number, attempt=n
                    ),
                    on_represign=lambda n: progress.event(
                        EventKind.REPRESIGN, part_number=part_number, attempt=n
                    ),
                    decode_content=False,
                    consume=consume,
                )
            )
        except HttpError as exc:
            error = backend.api_error(exc)
            fail(error)
            raise error from exc
        except RetriesExhausted as exc:
            error = backend.transfer_failed(
                f"range {part_number} failed after {exc.attempts} attempts: {exc.last!r}",
                token=None,
                cause=exc.last,
            )
            fail(error)
            raise error from exc.last
        except BaseException as exc:
            fail(exc)
            raise
        progress.add(got, part_number=part_number, force=True)
        return got

    executor = ThreadPoolExecutor(
        max_workers=settings.concurrency, thread_name_prefix="istari-download"
    )
    in_flight: dict[Future[int], int] = {}
    queue = iter(pending)
    exhausted = False
    try:
        while True:
            while not exhausted and len(in_flight) < lookahead:
                if cancel is not None and cancel.is_set():
                    stop.set()
                check_cancel(cancel, stop)
                item = next(queue, None)
                if item is None:
                    exhausted = True
                    break
                part_number, (offset, length) = item
                in_flight[executor.submit(fetch, part_number, offset, length)] = (
                    part_number
                )
            if not in_flight:
                break
            done, _ = wait(in_flight, timeout=0.25, return_when=FIRST_COMPLETED)
            if not done:
                if cancel is not None and cancel.is_set():
                    stop.set()
                check_cancel(cancel, stop)
                continue
            for future in done:
                in_flight.pop(future)
                future.result()
    except BaseException as exc:
        stop.set()
        executor.shutdown(wait=True, cancel_futures=True)
        if isinstance(exc, TransferCancelledError) and failures:
            raise failures[0]
        raise
    executor.shutdown(wait=True)


def download_to(
    backend: DownloadBackend,
    settings: TransferSettings,
    *,
    sha: str,
    salt: str,
    dest: Path,
    progress: ProgressCallback | None = None,
    cancel: threading.Event | None = None,
) -> Path:
    """Download the object behind ``sha``/``salt`` to ``dest``, verified, via a temp file.

    Objects at or below ``multipart_threshold`` stream in one pass (the probe body
    is reused, the remainder resumes from the byte reached); larger ones are fetched
    as parallel ranges of the clamped ``multipart_chunksize`` into a preallocated
    file and verified by one sequential local pass. Disk preflight reserves space
    only on the destination filesystem; callers own any later cache copy.
    """
    dest = Path(dest)
    started = time.monotonic()
    urls = _UrlSource(backend, settings, sha, cancel)
    range_size = clamp_part_size(settings.part_size_floor)
    probe: _Probe | None = None
    total: int | None = None
    tracker = _Progress(progress, total)
    partial: Path | None = None
    out: io.FileIO | None = None
    try:
        check_cancel(cancel)
        probe = _probe(backend, settings, urls, range_size, cancel, tracker)
        total = tracker.total = probe.total
        tracker.add(0, force=True)
        check_cancel(cancel)
        partial = partial_path(dest)
        out = open_partial(partial)
        try:
            fd = out.fileno()
            written = 0
            if probe.response is None or total == 0:
                if probe.response is not None:
                    probe.response.close()
                try:
                    native_crypto.VerifyingHasher(sha, salt).finalize()
                except ValueError as exc:
                    raise _verify_error(sha, exc) from exc
            elif total is None or not probe.ranged or total <= settings.threshold:
                written = _single_stream_to(
                    backend,
                    settings,
                    urls,
                    probe,
                    sha=sha,
                    salt=salt,
                    fd=fd,
                    cancel=cancel,
                    progress=tracker,
                )
            else:
                _disk_preflight(total, dest.parent)
                _ranged_to(
                    backend,
                    settings,
                    urls,
                    probe,
                    total=total,
                    range_size=range_size,
                    partial=partial,
                    fd=fd,
                    cancel=cancel,
                    progress=tracker,
                )
                written = total
        finally:
            out.close()
        check_written(partial, written)
        if total is not None and total > settings.threshold and probe.ranged:
            _verify_file(partial, sha, salt, cancel)
        # Establish an unknown response's actual size before publishing, so an
        # outer content owner can reject inconsistent metadata without replacing dest.
        tracker.total = written
        tracker.add(0, force=True)
        check_cancel(cancel)  # a cancel after the last byte must not publish dest
        os.replace(partial, dest)
        partial = None
    except BaseException as exc:
        # The probe holds a pooled connection until closed; close() is idempotent.
        if probe is not None and probe.response is not None:
            probe.response.close()
        if out is not None:
            out.close()  # Windows cannot unlink an open file
        _unlink_quietly(partial)
        if isinstance(exc, (TransferCancelledError, KeyboardInterrupt, SystemExit)):
            tracker.event(EventKind.CANCELLED)
        raise
    tracker.total = tracker.done
    tracker.event(EventKind.COMPLETE)
    logger.info(
        "downloaded %s (%d bytes) to %s in %.1fs",
        sha,
        tracker.done,
        dest,
        time.monotonic() - started,
    )
    return dest


def read_into_memory(
    backend: DownloadBackend,
    settings: TransferSettings,
    *,
    sha: str,
    salt: str,
    progress: ProgressCallback | None = None,
    cancel: threading.Event | None = None,
) -> bytes:
    """Download the object into one preallocated buffer, verifying inline, and return ``bytes``."""
    urls = _UrlSource(backend, settings, sha, cancel)
    range_size = clamp_part_size(settings.part_size_floor)
    probe: _Probe | None = None
    tracker = _Progress(progress, None)
    try:
        check_cancel(cancel)
        probe = _probe(backend, settings, urls, range_size, cancel, tracker)
        total = tracker.total = probe.total
        tracker.add(0, force=True)
        check_cancel(cancel)
        verifier = native_crypto.VerifyingHasher(sha, salt)
        if probe.response is None or total == 0:
            if probe.response is not None:
                probe.response.close()
            try:
                verifier.finalize()
            except ValueError as exc:
                raise _verify_error(sha, exc) from exc
            check_cancel(cancel)
            tracker.event(EventKind.COMPLETE)
            return b""
        buffer = bytearray(total) if total is not None else bytearray()
        view = memoryview(buffer) if total is not None else None
        written = 0

        def sink(chunk: bytes) -> None:
            nonlocal written
            if view is not None:
                view[written : written + len(chunk)] = chunk
            else:
                buffer.extend(chunk)
            verifier.update(chunk)
            written += len(chunk)

        try:
            expected = (
                None
                if total is None
                else min(total, _content_length(probe.response) or total)
            )
            _stream_body(probe.response, sink, expected, cancel, tracker)
        except (urllib3.exceptions.HTTPError, ConnectionError) as exc:
            if total is None:
                raise
            logger.debug(
                "probe body ended early at %d bytes (%r); resuming", written, exc
            )
        finally:
            probe.response.close()
        while total is not None and written < total:
            _resume_stream(
                backend,
                settings,
                urls,
                sha=sha,
                offset=written,
                total=total,
                sink=sink,
                cancel=cancel,
                progress=tracker,
            )
        tracker.add(0, force=True)
        check_cancel(cancel)
        try:
            verifier.finalize()
        except ValueError as exc:
            raise _verify_error(sha, exc) from exc
        result = bytes(buffer)
        check_cancel(cancel)
        tracker.total = written
        tracker.event(EventKind.COMPLETE)
        return result
    except BaseException as exc:
        # The probe holds a pooled connection until closed; close() is idempotent.
        if probe is not None and probe.response is not None:
            probe.response.close()
        if isinstance(exc, (TransferCancelledError, KeyboardInterrupt, SystemExit)):
            tracker.event(EventKind.CANCELLED)
        raise
