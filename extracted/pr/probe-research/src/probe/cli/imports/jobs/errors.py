"""how a job ends badly: safe user-facing errors, retryable connection failures, unit retries."""

from __future__ import annotations
import errno
import socket
from urllib.error import HTTPError, URLError


class JobError(RuntimeError):
    """A safe, user-facing failure reason; never include credentials in it."""


class RetryableJobError(JobError):
    """A known temporary connection failure while replaying approved work."""


class UnitRetryJobError(RetryableJobError):
    """Approved batches whose agent stopped before finishing, with tries left.

    Replayed by the same loop as a lost connection (agents stopped first,
    cancellation honoured), and bounded by the batches' own attempt limit
    (`backfill_ledger.MAX_UNIT_ATTEMPTS`): an exhausted batch is final.
    """


def is_retryable_error(exc: BaseException) -> bool:
    """Recognize transport failures without guessing from exception messages.

    Authored JobError refusals are final even if they wrap a network error.
    Unknown wrappers may preserve a typed transport error as their cause.
    """
    import httpx
    from ....sdk.errors import AuthError, RosError, ScopeError, TransportError

    seen = set()
    while exc is not None and id(exc) not in seen:
        seen.add(id(exc))
        if isinstance(exc, RetryableJobError):
            return True
        if isinstance(exc, (JobError, AuthError, ScopeError)):
            return False
        if isinstance(exc, RosError) and exc.status is not None:
            return exc.status in (408, 429) or 500 <= exc.status <= 599
        if isinstance(exc, HTTPError):
            return exc.code in (408, 429) or 500 <= exc.code <= 599
        if isinstance(exc, httpx.HTTPStatusError):
            status = exc.response.status_code
            return status in (408, 429) or 500 <= status <= 599
        if isinstance(exc, (
            TransportError, ConnectionError, TimeoutError, socket.gaierror,
            httpx.NetworkError, httpx.TimeoutException, httpx.RemoteProtocolError,
        )):
            return True
        if isinstance(exc, OSError) and exc.errno in {
            errno.ECONNABORTED, errno.ECONNREFUSED, errno.ECONNRESET,
            errno.EHOSTUNREACH, errno.ENETDOWN, errno.ENETUNREACH, errno.ETIMEDOUT,
        }:
            return True
        # URLError also wraps invalid URLs and local file failures; only its
        # typed connection cause qualifies. Never retry arbitrary OSError.
        exc = exc.reason if isinstance(exc, URLError) and isinstance(exc.reason, BaseException) else exc.__cause__
    return False


class _Interrupted(BaseException):
    pass
