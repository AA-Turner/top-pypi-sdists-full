"""Error types raised by the transfer engine.

The hierarchy is chosen to fit the callers' existing ``except`` clauses:

* **Terminal local conditions** (``TransferError`` and subclasses) are *not*
  ``ValueError``\\ s, so a caller that retries ``ValueError`` does not retry them.
* **Verification failures** keep a ``ValueError`` base, preserving the
  ``read_contents`` contract.
* **Disk preflight** raises an ``OSError`` with ``errno.ENOSPC``.
* **Transport/HTTP failures** raise the stack's own ``ApiException`` (built by an
  injected factory); exhausted retries raise the stack's ``TransferFailedError``,
  an ``ApiException`` that also mixes in :class:`TransferFailed`.
* Inside the engine those two cases are :class:`HttpError` and
  :class:`RetriesExhausted`; the stack adapters translate them at the boundary.
"""

from __future__ import annotations

import errno
import json
import re
from collections.abc import Mapping
from typing import Any

_REQUEST_TIMEOUT_CODE = re.compile(rb"<Code>\s*RequestTimeout\s*</Code>")


class TransferError(Exception):
    """A terminal, non-retryable local transfer condition."""


class MultipartUploadRestartRequiredError(TransferError):
    """Completion consumed the session and a safe fresh attempt is not possible.

    This is terminal, not an exhausted transport retry budget. ``token`` retains
    the logical upload identity; diagnostics deliberately exclude server bodies,
    URLs and token contents.
    """

    retries_exhausted: bool = False

    def __init__(self, token: Any, cause: BaseException, reason: str) -> None:
        """Retain the original failure with one bounded, non-secret reason."""
        reasons = {
            "source not replayable",
            "callback not safely repeatable",
            "attempt limit",
            "source changed before replay",
        }
        self.reason = reason if reason in reasons else "source not replayable"
        self.token = token
        self.cause = cause
        super().__init__(f"multipart upload restart required: {self.reason}")


def is_multipart_upload_restart_required(status: object, body: object) -> bool:
    """Recognize only the registry's exact structured completion restart signal."""
    if type(status) is not int or status != 503:
        return False
    if isinstance(body, (str, bytes)):
        try:
            body = json.loads(body)
        except (ValueError, UnicodeError, RecursionError):
            return False
    if not isinstance(body, Mapping):
        return False
    detail = body.get("detail")
    return (
        isinstance(detail, Mapping)
        and detail.get("error_code") == "MULTIPART_UPLOAD_RESTART_REQUIRED"
    )


class TransferCancelledError(TransferError):
    """The caller's ``cancel`` event was set (or the interpreter was interrupted)."""


class FileChangedDuringUploadError(TransferError):
    """The source file changed (size, mtime, or short read) while it was being uploaded."""


class SourceReadError(TransferError):
    """A local source could not be opened, positioned, or read; retrying is unsafe."""

    def __init__(self, path: str, cause: OSError) -> None:
        """Record the source path and original operating-system error."""
        super().__init__(f"{path}: could not read upload source: {cause}")
        self.path = path
        self.cause = cause


class PartPlanError(TransferError):
    """No valid uniform part plan exists for the object (too large for 10,000 parts)."""


class ContentVerificationError(ValueError):
    """Downloaded bytes do not match the token's salted SHA-384 digest."""


class InsufficientDiskSpaceError(OSError):
    """The destination filesystem lacks room for the download (``errno.ENOSPC``)."""

    def __init__(self, path: Any, needed: int, available: int) -> None:
        """Record where and how much space was missing."""
        super().__init__(
            errno.ENOSPC,
            f"insufficient disk space for {needed} bytes ({available} available)",
            str(path),
        )
        self.needed = needed
        self.available = available


class TransferFailed:
    """Mixin carried by each stack's ``TransferFailedError``.

    ``retries_exhausted`` lets a retrying caller tell a spent retry budget apart
    from a definite failure; ``token`` is the upload's content token so a caller
    can retry under the same salt and resume the upload the engine left behind.
    """

    retries_exhausted: bool = True
    token: Any = None


class HttpError(Exception):
    """A non-2xx data-plane response; the body was sniffed and the connection dropped."""

    def __init__(
        self,
        method: str,
        url: str,
        status: int,
        reason: str | None,
        headers: Mapping[str, str],
        body: bytes,
    ) -> None:
        """Capture the response so a stack can build its ``ApiException`` from it."""
        super().__init__(f"{method} {status} {reason or ''}".strip())
        self.method = method
        self.url = url
        self.status = status
        self.reason = reason
        self.headers = dict(headers)
        self.body = body

    @property
    def retryable(self) -> bool:
        """5xx, 429, 408, and the S3 400 ``RequestTimeout``."""
        return is_retryable_status(self.status, self.body)

    @property
    def expired(self) -> bool:
        """A 403, which on a presigned URL usually means it expired."""
        return self.status == 403


class RetriesExhausted(Exception):
    """The retry deadline ran out; ``last`` is the final attempt's error."""

    def __init__(self, last: BaseException, attempts: int) -> None:
        """Wrap the final failure."""
        super().__init__(f"retries exhausted after {attempts} attempts: {last!r}")
        self.last = last
        self.attempts = attempts


def is_retryable_status(status: int, body: bytes = b"") -> bool:
    """Whether an HTTP status is transient (501 and 505 are terminal)."""
    if (500 <= status < 600 and status not in (501, 505)) or status in (408, 429):
        return True
    return status == 400 and bool(_REQUEST_TIMEOUT_CODE.search(body or b""))
