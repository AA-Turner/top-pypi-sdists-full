"""Direct S3 transfer support (upload and download) using boto3."""

from __future__ import annotations

import io
import logging
import os
import ssl
import threading
from collections.abc import Callable
from pathlib import Path
from typing import Any, Self

from istari_digital_client import native_crypto
from istari_digital_client._transfer.download import (
    _disk_preflight,
    open_partial,
    partial_path,
)
from istari_digital_client._transfer.errors import (
    ContentVerificationError,
    TransferCancelledError,
    TransferError,
)
from istari_digital_client._transfer.events import EventKind, TransferEvent, emit
from istari_digital_client._transfer.http import (
    Deadline,
    TransferSettings,
    is_retryable_exception,
    retrying,
)

try:
    import boto3  # type: ignore[import-not-found,import-untyped]
    from boto3.s3.transfer import (
        TransferConfig,  # type: ignore[import-not-found,import-untyped]
    )
    from botocore.config import (
        Config as BotoConfig,  # type: ignore[import-not-found,import-untyped]
    )
except ImportError:
    boto3 = None
    TransferConfig = None
    BotoConfig = None

logger = logging.getLogger("istari")

MIB = 1024 * 1024
_VERIFY_CHUNK = 8 * MIB
ProgressCallback = Callable[[TransferEvent], None]


class S3AccessError(Exception):
    """Raised when an S3 operation fails due to permissions."""


class S3ObjectNotFoundError(Exception):
    """A single object is absent; direct S3 access remains usable."""


def _is_missing(exc: BaseException) -> bool:
    status = _unwrap_status(exc)
    if status is not None:
        return status == 404
    response = getattr(exc, "response", {})
    return isinstance(response, dict) and response.get("Error", {}).get("Code") in {
        "404",
        "NoSuchKey",
        "NotFound",
    }


def _retryable_stream_error(exc: BaseException) -> bool:
    """Retry only recognized remote/transport failures, not local IO or callbacks."""
    if _wraps_cancel(exc) or _is_missing(exc) or _is_access_denied(exc):
        return False
    # Botocore stores wrapped errors in kwargs as well as exception chains.
    from istari_digital_client._transfer.http import exception_causes

    causes = exception_causes(exc)
    seen = {id(cause) for cause in causes}
    for cause in causes:
        for value in getattr(cause, "kwargs", {}).values():
            if isinstance(value, BaseException):
                for nested in exception_causes(value):
                    if id(nested) not in seen:
                        seen.add(id(nested))
                        causes.append(nested)
    for cause in causes:
        if isinstance(cause, (TransferError, ValueError, TypeError)):
            return False
        if isinstance(cause, ssl.SSLError) and not is_retryable_exception(cause):
            return False
        if (
            isinstance(cause, OSError)
            and not type(cause).__module__.startswith("botocore.")
            and not is_retryable_exception(cause)
        ):
            return False
    # botocore is optional; importing it here preserves dependency-free clients.
    try:
        from botocore import exceptions as errors
    except ImportError:
        return is_retryable_exception(exc)
    if isinstance(exc, errors.ClientError):
        return _http_status(exc) in {408, 429, 500, 502, 503, 504}
    if isinstance(exc, errors.ResponseStreamingError):
        nested = [cause for cause in causes if cause is not exc]
        if nested:
            return any(is_retryable_exception(cause) for cause in nested)
        # A wrapper without a recognized underlying transport error is not evidence
        # that retrying is safe (its error may be a stringified local exception).
        return False
    for cause in causes:
        if isinstance(cause, errors.ClientError):
            return _http_status(cause) in {408, 429, 500, 502, 503, 504}
    return any(
        isinstance(
            cause,
            (
                errors.ConnectionClosedError,
                errors.ConnectTimeoutError,
                errors.ReadTimeoutError,
                errors.EndpointConnectionError,
                errors.IncompleteReadError,
            ),
        )
        or is_retryable_exception(cause)
        for cause in causes
    )


def _wraps_cancel(exc: BaseException) -> bool:
    """Whether a boto3/CRT wrapper hides a ``TransferCancelledError`` raised from our callback."""
    pending = [exc]
    seen: set[int] = set()
    while pending:
        current = pending.pop()
        if id(current) in seen:
            continue
        seen.add(id(current))
        if isinstance(current, TransferCancelledError):
            return True
        pending.extend(
            link
            for link in (current.__cause__, current.__context__)
            if link is not None
        )
    return False


def _http_status(exc: Any) -> Any:
    """HTTP status code of a botocore ClientError.

    Real ``PutObject``/``GetObject`` denials report ``Error.Code == "AccessDenied"``
    (not ``"403"``), so permission handling must key off the HTTP status here — not
    the string error code — or the presigned-URL fallback never fires.
    """
    response = getattr(exc, "response", None)
    if isinstance(response, dict):
        return response.get("ResponseMetadata", {}).get("HTTPStatusCode")
    return None


def _unwrap_status(exc: BaseException, depth: int = 6) -> Any:
    """HTTP status of ``exc`` or of the ClientError it wraps.

    ``upload_file`` raises ``S3UploadFailedError`` around the ``ClientError``; the CRT
    transfer client raises its own ``S3ResponseError`` (``status_code``). Walk
    ``__cause__``/``__context__`` so a 403 is recognised whichever wrapper is on top.
    """
    seen = 0
    current: BaseException | None = exc
    while current is not None and seen < depth:
        status = _http_status(current)
        if status is None:
            status = getattr(current, "status_code", None)
        if isinstance(status, int):
            return status
        current = current.__cause__ or current.__context__
        seen += 1
    return None


def _is_access_denied(exc: BaseException) -> bool:
    status = _unwrap_status(exc)
    if status is not None:
        return (
            status == 403
        )  # a known status is authoritative; the text match is for status-less wrappers
    text = str(exc)
    return "AccessDenied" in text or "(403)" in text


class _Callback:
    """Serialize signed boto3 deltas and bounded, nondecreasing progress delivery.

    Unknown-size transfers retain signed accounting but report no provisional byte
    counts: concurrent retries can overstate the final size. Only successful
    finalization establishes that size. A byte counter never establishes success.
    """

    def __init__(
        self,
        progress: ProgressCallback | None,
        cancel: threading.Event | None,
        total: int | None,
    ) -> None:
        self._progress = progress
        self._cancel = cancel
        self._total = total
        self._done = 0
        self._highwater = 0
        self._reported = 0
        self._terminal = False
        self._lock = threading.Lock()
        self._deadline: Deadline | None = None
        self._retry_highwater = 0

    def check_cancel(self) -> None:
        """Check cancellation even when progress delivery is coalesced or suppressed."""
        if self._cancel is not None and self._cancel.is_set():
            raise TransferCancelledError("transfer cancelled")

    def __call__(self, bytes_transferred: int) -> None:
        with self._lock:
            self.check_cancel()
            if self._terminal:
                return
            self._done += bytes_transferred
            if self._done > self._retry_highwater:
                self._retry_highwater = self._done
                if self._deadline is not None:
                    self._deadline.reset()
            if self._total is None:
                self._highwater = max(self._highwater, self._done)
                return
            self._highwater = max(self._highwater, min(self._total, max(0, self._done)))
            if self._highwater - self._reported >= _VERIFY_CHUNK:
                self._reported = self._highwater
                emit(
                    self._progress,
                    TransferEvent(EventKind.PART_DONE, self._reported, self._total),
                )

    def complete(self, size: int, publish: Callable[[], None] | None = None) -> None:
        """Flush actual final progress and success after all required checks pass."""
        with self._lock:
            self.check_cancel()
            if self._terminal:
                return
            if self._total is not None and size != self._total:
                raise ValueError("final size does not match known transfer total")
            if size < self._reported:
                raise ValueError(
                    "final size is smaller than reported transfer progress"
                )
            self._total = size
            self._highwater = size
            self._reported = size
            emit(self._progress, TransferEvent(EventKind.PART_DONE, size, size))
            self.check_cancel()
            if publish is not None:
                publish()
            self._terminal = True
            emit(self._progress, TransferEvent(EventKind.COMPLETE, size, size))

    def cancelled(self) -> None:
        """Report cancellation once, using zero until an unknown size is established."""
        with self._lock:
            if self._terminal:
                return
            self._terminal = True
            done = self._highwater if self._total is not None else 0
            emit(self._progress, TransferEvent(EventKind.CANCELLED, done, self._total))


class S3Client:
    """Direct S3 transfers (upload and download) using boto3.

    Uses boto3's managed transfer (``upload_file`` / ``download_fileobj``), which
    streams from and to disk with concurrent parts under a ``TransferConfig`` built
    from the SDK's ``multipart_threshold``, ``multipart_chunksize`` and
    ``transfer_concurrency``. On the first 403 for upload or download that
    direction is permanently disabled so callers can fall back to presigned URLs.

    When HEAD is forbidden, downloads use explicit streaming GETs without another
    managed HEAD request. Otherwise managed downloads retain concurrent ranges.

    With the ``s3-crt`` extra installed, ``preferred_transfer_client="auto"`` may
    select CRT depending on the host environment. CRT sizes parts and concurrency
    itself and can ignore transfer settings; access denials from its error types
    are still normalised into ``S3AccessError``.
    """

    def __init__(
        self,
        bucket_name: str,
        *,
        multipart_threshold: int | None = None,
        multipart_chunksize: int | None = None,
        concurrency: int | None = None,
        settings: TransferSettings | None = None,
    ) -> None:
        if boto3 is None:
            raise ImportError(
                "boto3 is required for direct S3 transfer. "
                "Install with: pip install istari-digital-client[s3]"
            )
        self._bucket = bucket_name
        self._settings = settings or TransferSettings()
        workers = max(
            1,
            min(
                int(self._settings.concurrency if concurrency is None else concurrency),
                16,
            ),
        )
        threshold = (
            self._settings.threshold
            if multipart_threshold is None
            else multipart_threshold
        )
        chunksize = (
            self._settings.part_size_floor
            if multipart_chunksize is None
            else multipart_chunksize
        )
        # A private session, not boto3's process-global default one: the default
        # session caches credentials after the first resolution, so a client built
        # later in the same process (e.g. after a credential rotation) would keep
        # using stale credentials.
        self._client = boto3.session.Session().client(
            "s3",
            config=BotoConfig(
                connect_timeout=self._settings.connect_timeout,
                read_timeout=self._settings.read_timeout,
                max_pool_connections=max(workers, 10),
                # The progress-aware transfer policy owns retries, not each request.
                retries={"mode": "standard", "total_max_attempts": 1},
                # MinIO and other non-AWS backends may reject the default flexible checksums.
                request_checksum_calculation="when_required",
                response_checksum_validation="when_required",
            ),
        )
        self._transfer_config = TransferConfig(
            multipart_threshold=max(1, int(threshold)),
            multipart_chunksize=max(1, int(chunksize)),
            max_concurrency=workers,
            use_threads=workers > 1,
            num_download_attempts=1,
            preferred_transfer_client="auto",
        )
        self._can_head = True
        self.can_upload = True
        self.can_download = True

    def close(self) -> None:
        """Release the boto3 client's connection pool. Idempotent."""
        self._client.close()

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()

    def _retry_operation(
        self,
        operation: Callable[[], Any],
        callback: _Callback | None = None,
        out: Any = None,
    ) -> Any:
        """Retry complete managed calls only after their workers and cleanup finish."""
        settings = getattr(self, "_settings", None) or TransferSettings()
        deadline = Deadline(settings.retry.deadline, lazy=True)
        if callback is not None:
            callback._deadline = deadline

        def attempt(number: int) -> Any:
            if callback is not None:
                callback.check_cancel()
                if number > 1:
                    callback._done = 0
            if number > 1 and out is not None:
                out.seek(0)
                out.truncate(0)
            return operation()

        try:
            return retrying(
                attempt,
                policy=settings.retry,
                deadline=deadline,
                retryable=_retryable_stream_error,
                cancel=callback._cancel if callback is not None else None,
                on_retry=(
                    lambda n, _exc, _wait: emit(
                        callback._progress,
                        TransferEvent(
                            EventKind.RETRY,
                            callback._reported,
                            callback._total,
                            attempt=n,
                        ),
                    )
                )
                if callback is not None
                else None,
            )
        finally:
            if callback is not None:
                callback._deadline = None

    def _exists(self, key: str, callback: _Callback | None = None) -> bool:
        if not self._can_head:
            return False
        try:
            self._retry_operation(
                lambda: self._client.head_object(Bucket=self._bucket, Key=key), callback
            )
        except Exception as exc:
            status = _http_status(exc)
            if status == 403:
                logger.debug("S3 head_object forbidden, disabling existence checks")
                self._can_head = False
                return False
            if status == 404:
                return False
            raise
        logger.debug(
            "S3 key already exists, skipping upload: bucket=%s key=%s",
            self._bucket,
            key,
        )
        return True

    def upload(
        self,
        key: str,
        data: bytes,
        *,
        progress: ProgressCallback | None = None,
        cancel: threading.Event | None = None,
    ) -> None:
        """Upload bytes with optional progress/cancellation, skipping existing keys."""
        callback = _Callback(progress, cancel, len(data))
        try:
            callback.check_cancel()
            if not self._exists(key, callback):
                callback.check_cancel()
                self._retry_operation(
                    lambda: self._client.upload_fileobj(
                        Fileobj=io.BytesIO(data),
                        Bucket=self._bucket,
                        Key=key,
                        Callback=callback,
                        Config=self._transfer_config,
                    ),
                    callback,
                )
            callback.complete(len(data))
        except (KeyboardInterrupt, SystemExit):
            callback.cancelled()
            raise
        except Exception as exc:  # boto3/CRT raise several wrapper types
            if _wraps_cancel(exc):
                callback.cancelled()
                if isinstance(exc, TransferCancelledError):
                    raise
                raise TransferCancelledError("transfer cancelled") from exc
            if _is_access_denied(exc):
                raise S3AccessError("S3 upload forbidden") from exc
            raise

    def upload_path(
        self,
        key: str,
        path: os.PathLike[str] | str,
        *,
        progress: ProgressCallback | None = None,
        cancel: threading.Event | None = None,
    ) -> None:
        """Stream a file from disk to S3 with boto3's managed transfer, skipping if the key exists.

        ``upload_file`` opens each part lazily from the filename, so memory stays at
        about ``chunksize x concurrency``; ``progress`` maps to boto3's ``Callback`` and
        ``cancel`` is checked there. Raises S3AccessError on 403 so the caller can fall back.
        """
        callback = _Callback(progress, cancel, None)
        try:
            callback.check_cancel()
            size = Path(path).stat().st_size
            callback = _Callback(progress, cancel, size)
            if not self._exists(key, callback):
                callback.check_cancel()
                # Each managed call waits for its failed multipart session to abort
                # before a new call can create another upload session.
                self._retry_operation(
                    lambda: self._client.upload_file(
                        Filename=os.fspath(path),
                        Bucket=self._bucket,
                        Key=key,
                        Callback=callback,
                        Config=self._transfer_config,
                    ),
                    callback,
                )
            callback.complete(size)
        except (KeyboardInterrupt, SystemExit):
            callback.cancelled()
            raise
        except Exception as exc:  # S3UploadFailedError / CRT wrappers
            if _wraps_cancel(exc):
                callback.cancelled()
                if isinstance(exc, TransferCancelledError):
                    raise
                raise TransferCancelledError("transfer cancelled") from exc
            if _is_access_denied(exc):
                raise S3AccessError("S3 upload forbidden") from exc
            raise

    def _download_size(self, key: str, callback: _Callback | None = None) -> int | None:
        """Probe disk requirements without treating a HEAD denial as a GET denial."""
        if not getattr(self, "_can_head", False):
            return None
        try:
            response = self._retry_operation(
                lambda: self._client.head_object(Bucket=self._bucket, Key=key), callback
            )
        except Exception as exc:
            if _is_missing(exc):
                raise S3ObjectNotFoundError(key) from exc
            if _is_access_denied(exc):
                self._can_head = False
                logger.debug("S3 head_object forbidden, disabling HEAD checks")
                return None
            raise
        return response.get("ContentLength")

    def _stream_download(
        self, key: str, out: Any, callback: _Callback, dest_dir: Path | None = None
    ) -> None:
        """Restart interrupted GETs, retaining only unique-byte public progress."""
        settings = getattr(self, "_settings", None) or TransferSettings()
        deadline = Deadline(settings.retry.deadline, lazy=True)
        highwater = 0
        remote_error = False

        def attempt(number: int) -> None:
            nonlocal highwater, remote_error
            remote_error = False
            callback.check_cancel()
            if number > 1:
                out.seek(0)
                out.truncate(0)
                callback._done = 0
            remote_error = True
            response = self._client.get_object(Bucket=self._bucket, Key=key)
            remote_error = False
            body = response["Body"]
            try:
                total = response.get("ContentLength")
                if total is not None:
                    if callback._total is not None and total != callback._total:
                        raise ContentVerificationError(
                            "S3 object size changed during download"
                        )
                    callback._total = total
                    if dest_dir is not None:
                        _disk_preflight(total, dest_dir)
                done = 0
                while True:
                    callback.check_cancel()
                    remote_error = True
                    chunk = body.read(_VERIFY_CHUNK)
                    remote_error = False
                    if not chunk:
                        break
                    out.write(chunk)
                    done += len(chunk)
                    if total is not None and done > total:
                        raise ContentVerificationError("S3 body exceeds ContentLength")
                    if done > highwater:
                        highwater = done
                        deadline.reset()
                    callback(len(chunk))
                if total is not None and done != total:
                    # StreamingBody normally raises this itself; preserve retry semantics
                    # for compatible clients that return an early EOF instead.
                    from urllib3.exceptions import IncompleteRead

                    remote_error = True
                    raise IncompleteRead(done, total - done)
            finally:
                try:
                    body.close()
                except Exception:
                    logger.warning("could not close S3 response body", exc_info=True)

        retrying(
            attempt,
            policy=settings.retry,
            deadline=deadline,
            retryable=lambda exc: remote_error and _retryable_stream_error(exc),
            cancel=callback._cancel,
            on_retry=lambda n, _exc, _wait: emit(
                callback._progress,
                TransferEvent(
                    EventKind.RETRY, callback._reported, callback._total, attempt=n
                ),
            ),
        )

    def _download_into(
        self, key: str, out: Any, callback: _Callback, dest_dir: Path | None = None
    ) -> None:
        managed = callable(getattr(self._client, "download_fileobj", None))
        if managed and (
            getattr(self, "_can_head", False)
            or not callable(getattr(self._client, "get_object", None))
        ):
            self._retry_operation(
                lambda: self._client.download_fileobj(
                    Bucket=self._bucket,
                    Key=key,
                    Fileobj=out,
                    Callback=callback,
                    Config=self._transfer_config,
                ),
                callback,
                out,
            )
        else:
            self._stream_download(key, out, callback, dest_dir)

    def download(
        self,
        key: str,
        *,
        sha: str | None = None,
        salt: str | None = None,
        progress: ProgressCallback | None = None,
        cancel: threading.Event | None = None,
    ) -> bytes:
        """Download bytes, optionally verifying paired ``sha``/``salt`` before success.

        With neither verification argument, preserve raw-byte download behavior.
        Mismatches raise ValueError-compatible ContentVerificationError.
        """
        if (sha is None) != (salt is None):
            raise ValueError("sha and salt must be supplied together")
        callback = _Callback(progress, cancel, None)
        try:
            callback.check_cancel()
            if callable(getattr(self._client, "get_object", None)):
                callback._total = self._download_size(key, callback)
            with io.BytesIO() as buf:
                self._download_into(key, buf, callback)
                callback.check_cancel()
                data = buf.getvalue()
            if sha is not None and salt is not None:
                verifier = native_crypto.VerifyingHasher(sha, salt)
                for offset in range(0, len(data), _VERIFY_CHUNK):
                    callback.check_cancel()
                    verifier.update(data[offset : offset + _VERIFY_CHUNK])
                callback.check_cancel()
                try:
                    verifier.finalize()
                except ValueError as exc:
                    raise ContentVerificationError(
                        f"downloaded content does not match sha {sha}: {exc}"
                    ) from exc
            callback.complete(len(data))
            return data
        except (KeyboardInterrupt, SystemExit):
            callback.cancelled()
            raise
        except Exception as exc:
            if _wraps_cancel(exc):
                callback.cancelled()
                if isinstance(exc, TransferCancelledError):
                    raise
                raise TransferCancelledError("transfer cancelled") from exc
            if _is_missing(exc):
                raise S3ObjectNotFoundError(key) from exc
            if _is_access_denied(exc):
                raise S3AccessError("S3 download forbidden") from exc
            raise

    def download_to(
        self,
        key: str,
        dest: os.PathLike[str] | str,
        *,
        sha: str,
        salt: str,
        progress: ProgressCallback | None = None,
        cancel: threading.Event | None = None,
    ) -> Path:
        """Stream an object to ``dest`` via a temp file beside it, verifying before the rename.

        Raises S3AccessError on 403 so the caller can fall back, and
        ContentVerificationError when the bytes do not match the token.
        """
        dest_path = Path(dest)
        callback = _Callback(progress, cancel, None)
        partial = partial_path(
            dest_path
        )  # named before it exists, so cleanup never waits on the open
        try:
            callback.check_cancel()
            total = self._download_size(key, callback)
            if total is not None:
                _disk_preflight(total, dest_path.parent)
                callback._total = total
            with open_partial(partial) as raw, io.BufferedWriter(raw) as out:
                self._download_into(key, out, callback, dest_path.parent)
            callback.check_cancel()
            verifier = native_crypto.VerifyingHasher(sha, salt)
            with partial.open("rb") as inp:
                while True:
                    callback.check_cancel()
                    chunk = inp.read(_VERIFY_CHUNK)
                    if not chunk:
                        break
                    verifier.update(chunk)
            callback.check_cancel()
            try:
                verifier.finalize()
            except ValueError as exc:
                raise ContentVerificationError(
                    f"downloaded content does not match sha {sha}: {exc}"
                ) from exc
            callback.complete(
                partial.stat().st_size, lambda: os.replace(partial, dest_path)
            )
        except BaseException as exc:
            try:
                partial.unlink()
            except FileNotFoundError:
                pass
            except OSError:
                logger.warning(
                    "could not remove partial download %s", partial, exc_info=True
                )
            if isinstance(exc, (KeyboardInterrupt, SystemExit)) or _wraps_cancel(exc):
                callback.cancelled()
                if not isinstance(
                    exc, (KeyboardInterrupt, SystemExit, TransferCancelledError)
                ):
                    raise TransferCancelledError("transfer cancelled") from exc
            elif _is_missing(exc):
                raise S3ObjectNotFoundError(key) from exc
            elif _is_access_denied(exc):
                raise S3AccessError("S3 download forbidden") from exc
            raise
        return dest_path
