"""Upload engine: a single streaming PUT and the parallel, resumable multipart uploader.

Both paths are stack-neutral: the registry calls (presign, create, part URLs,
discover, complete, cancel) and the error classes come from an injected
:class:`UploadBackend`, and the data plane goes through ``RawTransport``.
"""

from __future__ import annotations

import logging
import threading
import time
from collections.abc import Callable, Iterable, Mapping, Sequence
from concurrent.futures import FIRST_COMPLETED, Future, ThreadPoolExecutor, wait
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Protocol, cast

from istari_digital_client._transfer.errors import (
    ContentVerificationError,
    FileChangedDuringUploadError,
    MultipartUploadRestartRequiredError,
    SourceReadError,
    TransferCancelledError,
    TransferError,
    is_multipart_upload_restart_required,
)
from istari_digital_client._transfer.events import (
    EventForwarder,
    EventKind,
    ProgressCallback,
    TransferEvent,
    emit,
)
from istari_digital_client._transfer.http import (
    Deadline,
    HttpError,
    RawTransport,
    RetriesExhausted,
    TransferSettings,
    check_cancel,
    exception_causes,
    finish_response,
    is_retryable_control_error,
    retry_control_call,
    retrying,
    send,
    transfer_request,
)
from istari_digital_client._transfer.plan import PartPlan, plan_parts, resume_decision
from istari_digital_client._transfer.request_options import control_request_scope
from istari_digital_client._transfer.source import PartSource, Reader, replay_source

logger = logging.getLogger("istari_digital_client.transfer")

CONTENT_TYPE = "application/octet-stream"
AZURE_BLOB_TYPE_HEADER = ("x-ms-blob-type", "BlockBlob")
# Refresh a URL this close to its expires (clock skew allowance); see refresh_margin().
URL_REFRESH_MARGIN_SECS = 60.0
# Fallback cap on part numbers per re-presign request; the backend reports the registry's.
DEFAULT_PART_URL_BATCH = 1000


class TemporaryUrlLike(Protocol):
    """A presigned URL plus its expiry (``None`` means refresh on 403 only)."""

    @property
    def url(self) -> str: ...

    @property
    def expires(self) -> datetime | None: ...


class UploadBackend(Protocol):
    """Registry calls and error factories the engine needs; each stack adapts its ``StorageApi``.

    Control-plane methods raise the stack's ``ApiException`` (duck-typed on
    ``.status``); ``discover`` returns ``None`` for a 404.
    """

    @property
    def transport(self) -> RawTransport: ...

    def is_azure_url(self, url: str) -> bool: ...

    def presign_upload(
        self,
        sha: str,
        model_id: str | None = None,
        receiving_remote_id: str | None = None,
    ) -> TemporaryUrlLike: ...

    def presign_download(self, sha: str) -> TemporaryUrlLike: ...

    def create_multipart(
        self,
        sha: str,
        num_parts: int,
        model_id: str | None,
        receiving_remote_id: str | None = None,
    ) -> tuple[str, Mapping[int, TemporaryUrlLike]]: ...

    def part_upload_urls(
        self, sha: str, upload_id: str, part_numbers: Sequence[int]
    ) -> Mapping[int, TemporaryUrlLike]: ...

    @property
    def part_url_batch_limit(self) -> int: ...

    def discover(
        self, sha: str
    ) -> tuple[str, list[tuple[int, int, str | None]]] | None: ...

    def complete(
        self,
        sha: str,
        upload_id: str,
        parts: Sequence[tuple[int, str | None]],
        *,
        part_size: int,
        object_size: int,
        timeout: float,
    ) -> None: ...

    def cancel(
        self, sha: str, upload_id: str, *, timeout: float | None = None
    ) -> None: ...

    def invalidate_auth(self) -> bool: ...

    def api_error(self, error: HttpError) -> Exception: ...

    def transfer_failed(
        self, message: str, *, token: Any, cause: BaseException | None
    ) -> Exception: ...


def _raise_terminal_cause(exc: BaseException) -> None:
    """Preserve local transfer errors hidden inside transport wrappers."""
    for cause in exception_causes(exc):
        if isinstance(cause, TransferError):
            raise cause


def _status(exc: BaseException) -> int | None:
    status = getattr(exc, "status", None)
    return status if isinstance(status, int) else None


class _AlreadyExists(Exception):
    """Internal: a presign returned 409, so the object is already in the store."""


def _control(
    backend: UploadBackend,
    settings: TransferSettings,
    fn: Callable[[], Any],
    cancel: threading.Event | None,
) -> Any:
    return retry_control_call(
        fn, settings=settings, invalidate_auth=backend.invalidate_auth, cancel=cancel
    )


def _total_from_probe(response: Any) -> int | None:
    content_range = response.headers.get("Content-Range")
    if content_range and "/" in content_range:
        total = content_range.rsplit("/", 1)[1].strip()
        if total.isdigit():
            return int(total)
    if response.status == 200:
        length = response.headers.get("Content-Length")
        return int(length) if length and length.isdigit() else None
    return None


def confirm_existing(
    backend: UploadBackend,
    settings: TransferSettings,
    sha: str,
    expected_size: int,
    *,
    cancel: threading.Event | None = None,
) -> None:
    """Best-effort size check of an object the registry reported as already present (409).

    The 409 itself is proof of existence (the registry HEAD-checks first). When a
    download URL can be minted, a ``Range: bytes=0-0`` probe compares the object's
    size with ours and raises ``ContentVerificationError`` only on a definite
    mismatch. A URL that cannot be minted (no revision yet, 403, 404) is accepted:
    that is the stable-salt retry whose bytes landed but whose revision did not.
    """
    # One attempt, deliberately outside the control-plane retry loop: the usual
    # failure here is the registry's deterministic "has no revisions" 500 for a sha
    # that has bytes but no revision yet, and retrying that for the whole deadline
    # would stall every stable-salt retry for minutes.
    try:
        check_cancel(cancel)
        with control_request_scope():
            presigned = backend.presign_download(sha)
    except TransferCancelledError:
        raise
    except Exception as exc:  # noqa: BLE001 - any failure here means "cannot confirm"
        logger.debug("accepting 409 for %s without a size check: %r", sha, exc)
        return
    try:
        response = send(
            backend.transport,
            "GET",
            presigned.url,
            headers={"Range": "bytes=0-0"},
            timeout=settings.timeout(),
        )
    except HttpError as exc:
        if exc.status == 416:
            remote: int | None = 0
        else:
            logger.debug("accepting 409 for %s; probe failed with %s", sha, exc.status)
            return
    except TransferCancelledError:
        raise
    except Exception as exc:  # noqa: BLE001
        logger.debug("accepting 409 for %s; probe failed: %r", sha, exc)
        return
    else:
        remote = _total_from_probe(response)
        response.close()
    if remote is not None and remote != expected_size:
        raise ContentVerificationError(
            f"object {sha} already exists with size {remote}, but the local content is {expected_size} bytes"
        )


def upload_single(
    backend: UploadBackend,
    settings: TransferSettings,
    *,
    sha: str | None,
    size: int,
    open_reader: Callable[[], Reader],
    token: Any = None,
    presigned: TemporaryUrlLike | None = None,
    model_id: str | None = None,
    receiving_remote_id: str | None = None,
    progress: ProgressCallback | None = None,
    cancel: threading.Event | None = None,
) -> None:
    """Upload one object, reporting exactly one success or cancellation event."""
    forward = EventForwarder(progress, size)
    try:
        check_cancel(cancel)
        _upload_single(
            backend,
            settings,
            sha=sha,
            size=size,
            open_reader=open_reader,
            token=token,
            presigned=presigned,
            model_id=model_id,
            receiving_remote_id=receiving_remote_id,
            progress=forward,
            cancel=cancel,
        )
        check_cancel(cancel)
    except BaseException as exc:
        if isinstance(exc, TransferCancelledError) or not isinstance(exc, Exception):
            forward(TransferEvent(EventKind.CANCELLED, 0, size))
        raise
    forward(TransferEvent(EventKind.COMPLETE, size, size))


def _upload_single(
    backend: UploadBackend,
    settings: TransferSettings,
    *,
    sha: str | None,
    size: int,
    open_reader: Callable[[], Reader],
    token: Any = None,
    presigned: TemporaryUrlLike | None = None,
    model_id: str | None = None,
    receiving_remote_id: str | None = None,
    progress: ProgressCallback | None = None,
    cancel: threading.Event | None = None,
) -> None:
    """Upload one object with a single presigned PUT (``Content-Type`` pinned).

    ``presigned`` skips the mint (bulk callers already hold a URL); ``sha`` enables
    re-minting on a 403 and 409 handling. A 409 from the mint means the object is
    already there and is confirmed via :func:`confirm_existing`.
    """
    started = time.monotonic()
    if presigned is None:
        if sha is None:
            raise ValueError("sha is required when no presigned URL is given")
        try:
            presigned = _control(
                backend,
                settings,
                lambda: backend.presign_upload(sha, model_id, receiving_remote_id),
                cancel,
            )
        except RetriesExhausted as exc:
            raise backend.transfer_failed(
                f"presign of {sha} failed after {exc.attempts} attempts: {exc.last!r}",
                token=token,
                cause=exc.last,
            ) from exc.last
        except Exception as exc:
            if _status(exc) == 409:
                confirm_existing(backend, settings, sha, size, cancel=cancel)
                emit(
                    progress,
                    TransferEvent(EventKind.PART_DONE, size, size, part_number=1),
                )
                return
            raise
    headers = {"Content-Type": CONTENT_TYPE}
    # Azure Put Blob requires x-ms-blob-type; Put Block (multipart parts) must not send it.
    if backend.is_azure_url(presigned.url):
        headers[AZURE_BLOB_TYPE_HEADER[0]] = AZURE_BLOB_TYPE_HEADER[1]

    def refresh(_old: str) -> str:
        try:
            return _control(
                backend,
                settings,
                lambda: backend.presign_upload(
                    cast(str, sha), model_id, receiving_remote_id
                ),
                cancel,
            ).url
        except Exception as exc:
            if _status(exc) == 409:
                raise _AlreadyExists() from exc
            raise

    reader = open_reader()
    try:
        try:
            response = transfer_request(
                backend.transport,
                "PUT",
                url=presigned.url,
                refresh_url=refresh if sha is not None else None,
                body=reader,
                headers=headers,
                settings=settings,
                deadline=Deadline(settings.retry.deadline, lazy=True),
                cancel=cancel,
                on_retry=lambda n, _w: emit(
                    progress,
                    TransferEvent(EventKind.RETRY, 0, size, part_number=1, attempt=n),
                ),
                on_represign=lambda n: emit(
                    progress,
                    TransferEvent(
                        EventKind.REPRESIGN, 0, size, part_number=1, attempt=n
                    ),
                ),
            )
        except _AlreadyExists:
            if sha is not None:
                confirm_existing(backend, settings, sha, size, cancel=cancel)
        except HttpError as exc:
            _raise_terminal_cause(exc)
            raise backend.api_error(exc) from exc
        except RetriesExhausted as exc:
            _raise_terminal_cause(exc.last)
            raise backend.transfer_failed(
                f"upload of {sha or 'object'} failed after {exc.attempts} attempts: {exc.last!r}",
                token=token,
                cause=exc.last,
            ) from exc.last
        except Exception as exc:
            _raise_terminal_cause(exc)
            raise
        else:
            finish_response(response)
    finally:
        reader.close()
    emit(
        progress,
        TransferEvent(
            EventKind.PART_DONE,
            size,
            size,
            part_number=1,
            latency=time.monotonic() - started,
        ),
    )
    logger.info(
        "uploaded %s (%d bytes) in one PUT in %.1fs",
        sha,
        size,
        time.monotonic() - started,
    )


def _seconds_left(entry: TemporaryUrlLike, now: datetime) -> float | None:
    expires = entry.expires
    if expires is None:
        return None
    if expires.tzinfo is None:
        expires = expires.replace(tzinfo=timezone.utc)
    return (expires - now).total_seconds()


def refresh_margin(entries: Iterable[TemporaryUrlLike], now: datetime) -> float:
    """Seconds before ``expires`` at which to refresh URLs minted at ``now``.

    Normally ``URL_REFRESH_MARGIN_SECS``; a quarter of the lifetime when the store's
    TTL is short enough (the registry allows 60 s) that the fixed margin would make
    every URL stale on arrival and every request re-presign.
    """
    lifetimes = [s for e in entries if (s := _seconds_left(e, now)) is not None]
    if not lifetimes:
        return URL_REFRESH_MARGIN_SECS
    return min(URL_REFRESH_MARGIN_SECS, max(min(lifetimes), 0.0) / 4)


def _is_fresh(
    entry: TemporaryUrlLike, now: datetime, margin: float = URL_REFRESH_MARGIN_SECS
) -> bool:
    left = _seconds_left(entry, now)
    return left is None or left > margin


class _PartUrlSource:
    """Thread-safe, just-in-time, single-flight supply of presigned part URLs."""

    def __init__(
        self,
        initial: Mapping[int, TemporaryUrlLike],
        fetch: Callable[[Sequence[int]], Mapping[int, TemporaryUrlLike]],
        order: Sequence[int],
        lookahead: int,
        *,
        max_batch: int = DEFAULT_PART_URL_BATCH,
    ) -> None:
        """Seed with the URLs from create; ``order`` is the ascending list of parts to upload."""
        self._urls: dict[int, TemporaryUrlLike] = dict(initial)
        self._fetch = fetch
        self._order = list(order)
        self._index = {n: i for i, n in enumerate(self._order)}
        self._lookahead = max(1, min(lookahead, max_batch))
        self._cond = threading.Condition()
        self._fetching = False
        self._margin = refresh_margin(initial.values(), datetime.now(timezone.utc))
        self.refreshes = 0

    def _cached(self, n: int, now: datetime) -> str | None:
        entry = self._urls.get(n)
        return (
            entry.url
            if entry is not None and _is_fresh(entry, now, self._margin)
            else None
        )

    def _batch_from(self, n: int, now: datetime) -> list[int]:
        start = self._index.get(n, 0)
        batch = [n]
        for m in self._order[start + 1 :]:
            if len(batch) >= self._lookahead:
                break
            if self._cached(m, now) is None:
                batch.append(m)
        return batch

    def _fetch_single_flight(
        self, numbers_for: Callable[[datetime], list[int]], n: int
    ) -> str:
        with self._cond:
            while True:
                now = datetime.now(timezone.utc)
                url = self._cached(n, now)
                if url is not None:
                    return url
                if not self._fetching:
                    self._fetching = True
                    batch = numbers_for(now)
                    break
                self._cond.wait()
        try:
            fetched = self._fetch(batch)
        except BaseException:
            with self._cond:
                self._fetching = False
                self._cond.notify_all()
            raise
        # Publish and clear in one block, so a woken waiter finds its URL instead of
        # starting a second fetch.
        with self._cond:
            self._urls.update(fetched)
            self._margin = refresh_margin(fetched.values(), datetime.now(timezone.utc))
            self.refreshes += 1
            self._fetching = False
            self._cond.notify_all()
            entry = self._urls.get(n)
        if entry is None:
            raise TransferError(f"registry returned no upload URL for part {n}")
        return entry.url

    def get(self, n: int) -> str:
        """URL for part ``n``, fetching a lookahead batch when it is missing or near expiry."""
        return self._fetch_single_flight(lambda now: self._batch_from(n, now), n)

    def refresh(self, n: int, failed_url: str) -> str:
        """Replace the URL for ``n`` after a 403 (returns another thread's refresh if it beat us)."""
        with self._cond:
            entry = self._urls.get(n)
            if entry is not None and entry.url != failed_url:
                return entry.url
            self._urls.pop(n, None)
        return self._fetch_single_flight(lambda _now: [n], n)


@dataclass
class _Session:
    upload_id: str
    plan: PartPlan
    missing: list[int]
    urls: Mapping[int, TemporaryUrlLike]
    landed_bytes: int
    resumed: bool
    etags: dict[int, str | None] = field(default_factory=dict)


@dataclass
class MultipartUploader:
    """Parallel, resumable multipart upload of one ``PartSource``.

    Flow: discover (adopt the server's part size when its landed parts fit a
    valid uniform plan), create, bounded worker pool with just-in-time part URLs,
    ``before_complete`` veto, then an idempotent complete. The veto runs after the
    source is read to its end (see ``PartSource``), also when the object already exists. Failures stop new parts,
    drain in-flight ones, and cancel the upload only when nothing could resume it.
    """

    backend: UploadBackend
    settings: TransferSettings
    source: PartSource
    token: Any
    stable_salt: bool
    model_id: str | None = None
    receiving_remote_id: str | None = None
    before_complete: Callable[[], None] | None = None
    progress: ProgressCallback | None = None
    cancel: threading.Event | None = None
    # Adapters wrapping readers supply the underlying source explicitly. Only the
    # shared exact-built-in check decides whether it is safe to replay.
    replay_source: PartSource | None = None
    user_before_complete: bool = True
    _stop: threading.Event = field(
        default_factory=threading.Event, init=False, repr=False
    )
    _done_bytes: int = field(default=0, init=False, repr=False)
    _retries: int = field(default=0, init=False, repr=False)

    @property
    def sha(self) -> str:
        """Content sha of the object being uploaded."""
        return str(self.token.sha)

    def _control(
        self, fn: Callable[[], Any], *, cancel: threading.Event | None = None
    ) -> Any:
        return _control(
            self.backend, self.settings, fn, self._stop if cancel is None else cancel
        )

    def _check(self) -> None:
        if self.cancel is not None and self.cancel.is_set():
            self._stop.set()
        check_cancel(self.cancel, self._stop)

    # --- session ------------------------------------------------------------

    def _adopt(
        self, upload_id: str, parts: list[tuple[int, int, str | None]], plan: PartPlan
    ) -> _Session | None:
        if not parts:
            return _Session(
                upload_id, plan, list(range(1, plan.num_parts + 1)), {}, 0, True
            )
        decision = resume_decision(
            [(n, size) for n, size, _ in parts], self.source.size
        )
        if decision.plan is None:
            return None
        landed = sum(size for _, size, _ in parts)
        return _Session(
            upload_id,
            decision.plan,
            decision.missing(),
            {},
            landed,
            True,
            {n: etag for n, _, etag in parts},
        )

    def _open_session(
        self, plan: PartPlan, *, retired_id: str | None = None
    ) -> _Session | None:
        """Discover-or-create; ``None`` means the object already exists."""
        sha = self.sha
        # Watch the caller's cancel here: nothing has set the internal stop yet, so a
        # cancel during a discover/create backoff would otherwise wait out the deadline.
        discovered = (
            self._control(lambda: self.backend.discover(sha), cancel=self.cancel)
            if retired_id is None
            else None
        )
        if discovered is not None:
            upload_id, parts = discovered
            session = self._adopt(upload_id, parts, plan)
            if session is not None:
                logger.info(
                    "resuming multipart upload %s for %s: %d of %d parts landed (part_size=%d)",
                    upload_id,
                    sha,
                    len(parts),
                    session.plan.num_parts,
                    session.plan.part_size,
                )
                return session
            logger.info(
                "discovered upload %s for %s has an unusable part layout; restarting",
                upload_id,
                sha,
            )
            self._cancel_upload(upload_id, best_effort=True)

        def attempt(n: int) -> _Session | None:
            if n > 1:
                # A failed create may have created a binding; adopt it rather than orphan it.
                with control_request_scope():
                    found = self.backend.discover(sha)
                if found is not None and found[0] != retired_id:
                    session = self._adopt(found[0], found[1], plan)
                    if session is not None:
                        return session
                    self._cancel_upload(found[0], best_effort=True)
            self._check()
            try:
                with control_request_scope():
                    upload_id, urls = self.backend.create_multipart(
                        sha, plan.num_parts, self.model_id, self.receiving_remote_id
                    )
            except Exception as exc:
                if _status(exc) == 409 and retired_id is None:
                    raise _AlreadyExists() from exc
                raise
            if upload_id == retired_id:
                raise TransferError("registry returned a retired multipart upload ID")
            return _Session(
                upload_id, plan, list(range(1, plan.num_parts + 1)), urls, 0, False
            )

        try:
            return retrying(
                attempt,
                policy=self.settings.retry,
                deadline=Deadline(self.settings.retry.deadline, lazy=True),
                retryable=is_retryable_control_error,
                cancel=self.cancel,
            )
        except _AlreadyExists:
            confirm_existing(
                self.backend, self.settings, sha, self.source.size, cancel=self.cancel
            )
            return None

    # --- parts --------------------------------------------------------------

    def _send_part(
        self, n: int, length: int, reader: Reader, urls: _PartUrlSource
    ) -> tuple[str | None, int, float]:
        started = time.monotonic()
        size = self.source.size

        def on_retry(attempt: int, _wait: float) -> None:
            with urls._cond:  # the upload's shared lock; workers bump this concurrently
                self._retries += 1
            emit(
                self.progress,
                TransferEvent(
                    EventKind.RETRY,
                    self._done_bytes,
                    size,
                    part_number=n,
                    attempt=attempt,
                ),
            )

        def on_represign(attempt: int) -> None:
            emit(
                self.progress,
                TransferEvent(
                    EventKind.REPRESIGN,
                    self._done_bytes,
                    size,
                    part_number=n,
                    attempt=attempt,
                ),
            )

        try:
            url = urls.get(n)
            response = transfer_request(
                self.backend.transport,
                "PUT",
                url=url,
                refresh_url=lambda failed: urls.refresh(n, failed),
                body=reader,
                # A part PUT is Azure Put Block / S3 UploadPart: Content-Type only, no
                # x-ms-blob-type (that header is Put Blob only; real Azure rejects it here).
                headers={"Content-Type": CONTENT_TYPE},
                settings=self.settings,
                deadline=Deadline(self.settings.retry.deadline, lazy=True),
                cancel=self._stop,
                on_retry=on_retry,
                on_represign=on_represign,
            )
        except HttpError as exc:
            _raise_terminal_cause(exc)
            raise self.backend.api_error(exc) from exc
        except RetriesExhausted as exc:
            _raise_terminal_cause(exc.last)
            raise self.backend.transfer_failed(
                f"part {n} of {self.sha} failed after {exc.attempts} attempts: {exc.last!r}",
                token=self.token,
                cause=exc.last,
            ) from exc.last
        except Exception as exc:
            _raise_terminal_cause(exc)
            raise
        finally:
            reader.close()
        etag: str | None = None
        if not self.backend.is_azure_url(url):
            header = response.headers.get("ETag")
            etag = header if header else None
        finish_response(response)
        logger.debug(
            "part %d of %s uploaded (%d bytes) in %.2fs",
            n,
            self.sha,
            length,
            time.monotonic() - started,
        )
        return etag, length, time.monotonic() - started

    def _upload_parts(self, session: _Session) -> dict[int, str | None]:
        sha = self.sha
        size = self.source.size
        plan = session.plan
        lookahead = 2 * self.settings.concurrency
        urls = _PartUrlSource(
            session.urls,
            lambda numbers: self._control(
                lambda: self.backend.part_upload_urls(sha, session.upload_id, numbers)
            ),
            session.missing,
            lookahead,
            max_batch=max(1, self.backend.part_url_batch_limit),
        )
        etags: dict[int, str | None] = dict(session.etags)
        # Each entry keeps its reader: _send_part closes it once running, but a future
        # the executor cancels never runs, so the error path closes what is left here.
        in_flight: dict[Future[tuple[str | None, int, float]], tuple[int, Reader]] = {}
        unsubmitted: Reader | None = None
        pending = iter(session.missing)
        exhausted = False
        executor = ThreadPoolExecutor(
            max_workers=self.settings.concurrency, thread_name_prefix="istari-upload"
        )
        try:
            while True:
                while not exhausted and len(in_flight) < lookahead:
                    self._check()
                    n = next(pending, None)
                    if n is None:
                        exhausted = True
                        break
                    offset, length = plan.part_range(n)
                    unsubmitted = self.source.open_part(n, offset, length)
                    future = executor.submit(
                        self._send_part, n, length, unsubmitted, urls
                    )
                    in_flight[future] = (n, unsubmitted)
                    unsubmitted = None
                if not in_flight:
                    break
                done, _ = wait(in_flight, timeout=0.25, return_when=FIRST_COMPLETED)
                if not done:
                    self._check()
                    continue
                for future in done:
                    n, _ = in_flight.pop(future)
                    etag, length, latency = future.result()
                    etags[n] = etag
                    self._done_bytes += length
                    emit(
                        self.progress,
                        TransferEvent(
                            EventKind.PART_DONE,
                            self._done_bytes,
                            size,
                            part_number=n,
                            latency=latency,
                        ),
                    )
        except BaseException:
            self._stop.set()
            executor.shutdown(wait=True, cancel_futures=True)
            # No worker runs now, and close() is idempotent, so a reader a finished
            # worker already closed is safe to close again.
            if unsubmitted is not None:
                unsubmitted.close()
            for _, reader in in_flight.values():
                reader.close()
            raise
        executor.shutdown(wait=True)
        return etags

    # --- complete / cancel --------------------------------------------------

    def _complete(self, session: _Session, etags: Mapping[int, str | None]) -> None:
        plan = session.plan
        parts = [(n, etags.get(n)) for n in range(1, plan.num_parts + 1)]
        sha = self.sha

        def call() -> None:
            try:
                self.backend.complete(
                    sha,
                    session.upload_id,
                    parts,
                    part_size=plan.part_size,
                    object_size=plan.size,
                    timeout=self.settings.complete_timeout,
                )
            except Exception as exc:
                # Detect inside the retry closure: this session has been consumed,
                # so retrying complete against it would hide the restart signal.
                if is_multipart_upload_restart_required(
                    getattr(exc, "status", None), getattr(exc, "body", None)
                ):
                    raise MultipartUploadRestartRequiredError(
                        self.token, exc, "attempt limit"
                    ) from exc
                raise

        try:
            retry_control_call(
                call,
                settings=self.settings,
                invalidate_auth=self.backend.invalidate_auth,
                cancel=self.cancel,
            )
        except RetriesExhausted as exc:
            raise self.backend.transfer_failed(
                f"complete of {sha} (upload {session.upload_id}) did not confirm after {exc.attempts} attempts: {exc.last!r}",
                token=self.token,
                cause=exc.last,
            ) from exc.last

    def _cancel_upload(self, upload_id: str, *, best_effort: bool) -> None:
        sha = self.sha
        emit(
            self.progress,
            TransferEvent(EventKind.ABORT, self._done_bytes, self.source.size),
        )
        try:
            # Cleanup gets one bounded request, never a fresh retry window. The
            # scope also disables redirects and the pool's own retry policy.
            configured = self.settings.control_timeout
            timeout = (
                min(5.0, configured)
                if configured is not None and 0 < configured < 5
                else 5.0
            )
            with control_request_scope():
                self.backend.cancel(sha, upload_id, timeout=timeout)
        except Exception as exc:  # noqa: BLE001 - cancellation is best effort
            logger.warning(
                "could not cancel multipart upload %s for %s: %r", upload_id, sha, exc
            )

    def _veto(self) -> None:
        """Run ``before_complete`` once the source has been read to its end."""
        if self.before_complete is None:
            return
        drain = getattr(self.source, "drain", None)
        if drain is not None:
            drain()
        self.before_complete()

    @staticmethod
    def _keeps_upload(exc: BaseException) -> bool:
        """Only a spent retry budget on a transient failure leaves the upload for a same-salt retry."""
        return bool(getattr(exc, "retries_exhausted", False))

    # --- run ----------------------------------------------------------------

    def run(self) -> None:
        """Upload the source; returns when the object is complete in the store."""
        started = time.monotonic()
        size = self.source.size
        self.progress = EventForwarder(self.progress, size)
        session: _Session | None = None
        complete_sent = False
        try:
            self._check()
            plan = plan_parts(size, self.settings.part_size_floor)
            retired_id: str | None = None
            for attempt in range(2):
                try:
                    session = self._open_session(plan, retired_id=retired_id)
                except RetriesExhausted as exc:
                    raise self.backend.transfer_failed(
                        f"opening the multipart upload of {self.sha} failed after {exc.attempts} attempts: {exc.last!r}",
                        token=self.token,
                        cause=exc.last,
                    ) from exc.last
                if session is not None:
                    self._done_bytes = session.landed_bytes
                self._check()
                if session is None:
                    # The object exists, but the source must still pass the veto.
                    self._veto()
                    self._check()
                    emit(self.progress, TransferEvent(EventKind.COMPLETE, size, size))
                    return
                etags = self._upload_parts(session)
                self._check()
                self._veto()
                self._check()
                complete_sent = True
                try:
                    self._complete(session, etags)
                except MultipartUploadRestartRequiredError as restart:
                    # The workers have drained before complete, and the registry
                    # consumed this session. Never cancel or rediscover it.
                    retired_id = session.upload_id
                    session = None
                    self._check()
                    if attempt == 1:
                        raise
                    if self.before_complete is not None and self.user_before_complete:
                        raise MultipartUploadRestartRequiredError(
                            self.token, restart.cause, "callback not safely repeatable"
                        ) from restart.cause
                    try:
                        replay = replay_source(
                            self.replay_source
                            if self.replay_source is not None
                            else self.source,
                            self.cancel,
                        )
                    except (FileChangedDuringUploadError, SourceReadError):
                        raise MultipartUploadRestartRequiredError(
                            self.token, restart.cause, "source changed before replay"
                        ) from restart.cause
                    if replay is None:
                        raise MultipartUploadRestartRequiredError(
                            self.token, restart.cause, "source not replayable"
                        ) from restart.cause
                    # Keep any explicit reader adapter; the built-in source itself
                    # retains its cancellation events and opens fresh readers at zero.
                    self._stop = threading.Event()
                    self._done_bytes = 0
                    complete_sent = False
                    continue
                self._check()
                break
        except BaseException as exc:
            cancelled = isinstance(exc, TransferCancelledError) or not isinstance(
                exc, Exception
            )
            if cancelled:
                emit(
                    self.progress,
                    TransferEvent(EventKind.CANCELLED, self._done_bytes, size),
                )
            if session is not None:
                if complete_sent:
                    # Never cancel once complete was sent, except on a definite plan mismatch (400).
                    if _status(exc) == 400:
                        self._cancel_upload(session.upload_id, best_effort=False)
                elif cancelled:
                    self._cancel_upload(session.upload_id, best_effort=True)
                elif not (self.stable_salt and self._keeps_upload(exc)):
                    self._cancel_upload(session.upload_id, best_effort=False)
                else:
                    logger.info(
                        "leaving multipart upload %s for %s in place for a same-salt retry",
                        session.upload_id,
                        self.sha,
                    )
            raise
        assert session is not None
        emit(self.progress, TransferEvent(EventKind.COMPLETE, size, size))
        logger.info(
            "uploaded %s: %d bytes in %d parts of %d (resumed=%s, retries=%d) in %.1fs",
            self.sha,
            size,
            session.plan.num_parts,
            session.plan.part_size,
            session.resumed,
            self._retries,
            time.monotonic() - started,
        )
