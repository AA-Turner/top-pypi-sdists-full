# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

from __future__ import annotations

import os
from typing import TYPE_CHECKING

from lance_namespace.errors import ServiceUnavailableError, ThrottlingError

if TYPE_CHECKING:
    from collections.abc import Iterator

APPLIER_TRANSIENT_RETRIES = max(
    0, int(os.environ.get("GENEVA_APPLIER_TRANSIENT_RETRIES", "3"))
)
APPLIER_RETRY_BASE_BACKOFF_SECONDS = float(
    os.environ.get("GENEVA_APPLIER_RETRY_BASE_BACKOFF_SECONDS", "1.0")
)
APPLIER_RETRY_MAX_BACKOFF_SECONDS = float(
    os.environ.get("GENEVA_APPLIER_RETRY_MAX_BACKOFF_SECONDS", "8.0")
)

NON_RETRYABLE_OBJECT_STORE_STATUS_CODES = {401, 403, 404}
RETRYABLE_OBJECT_STORE_STATUS_CODES = {408, 429, 500, 502, 503, 504}
OBJECT_STORE_CONTEXT_MARKERS = (
    "aws credentials",
    "credential",
    "object store",
    "lanceerror(io)",
    "connectorerror",
    "providererror",
)
NON_RETRYABLE_OBJECT_STORE_MARKERS = (
    "unauthorized",
    "forbidden",
    "permission denied",
    "access denied",
    "invalid schema",
    "schema mismatch",
    "schema error",
    "missing column",
    "invalid input",
    "invalid argument",
)
RETRYABLE_OBJECT_STORE_MARKERS = (
    "timeout",
    "timed out",
    "temporarily unavailable",
    "temporary failure",
    "temporary redirect",
    "connection reset",
    "connection refused",
    "connection aborted",
    "connection error",
    "broken pipe",
    "unexpected eof",
    "eof while",
    "too many requests",
    "rate limit",
    "throttle",
    "service unavailable",
    "bad gateway",
    "gateway timeout",
    "error sending request",
    "error performing",
    # Azure Blob throttling: HTTP 503 already retryable, but the error often
    # surfaces with the response code "ServerBusy" and/or the body message
    # "The server is busy." (GEN-525, observed on Atlas range reads).
    "serverbusy",
    "server is busy",
    # Lance/object_store multipart upload: transient state inconsistency where
    # a previously-uploaded part is reported missing on commit. Recoverable by
    # restarting the upload (GEN-525, observed on Atlas writes).
    "missing part",
)
# Throttle-specific subset: only these (plus a retryable status code or a typed
# throttle error) may override a not-found message, so a generic transient
# marker cannot resurrect a genuine miss.
THROTTLE_OBJECT_STORE_MARKERS = (
    "too many requests",
    "rate limit",
    "throttle",
    "service unavailable",
    "serverbusy",
    "server is busy",
)


# Bare Exception subclasses with no status/marker text, so they are matched
# by type. Both exist at the lance-namespace floor pinned in pyproject.toml.
LANCE_NAMESPACE_THROTTLE_ERRORS = (ThrottlingError, ServiceUnavailableError)


def get_applier_retry_settings() -> tuple[int, float, float]:
    """Return applier retry settings shared by run/setup object store retries."""
    return (
        APPLIER_TRANSIENT_RETRIES,
        APPLIER_RETRY_BASE_BACKOFF_SECONDS,
        APPLIER_RETRY_MAX_BACKOFF_SECONDS,
    )


def iter_exception_chain(exc: BaseException) -> Iterator[BaseException]:
    """Yield exception and nested causes/contexts without looping."""
    seen: set[int] = set()
    current: BaseException | None = exc
    while current is not None and id(current) not in seen:
        seen.add(id(current))
        yield current
        current = current.__cause__ or current.__context__


def get_status_code(exc: BaseException) -> int | None:
    status_code = getattr(exc, "status_code", None)
    return status_code if isinstance(status_code, int) else None


def is_not_found_object_store_message(msg: str) -> bool:
    return (
        "no such table" in msg
        or "does not exist" in msg
        or ("table" in msg and "not found" in msg)
        or ("column" in msg and "not found" in msg)
        or "not found in schema" in msg
    )


def has_marker(msg: str, markers: tuple[str, ...]) -> bool:
    return any(marker in msg for marker in markers)


def _has_throttle_evidence(candidates: tuple[BaseException, ...]) -> bool:
    """True for a typed throttle error, retryable status, or throttle marker."""
    for candidate in candidates:
        if isinstance(candidate, LANCE_NAMESPACE_THROTTLE_ERRORS):
            return True
        if get_status_code(candidate) in RETRYABLE_OBJECT_STORE_STATUS_CODES:
            return True
        if has_marker(str(candidate).lower(), THROTTLE_OBJECT_STORE_MARKERS):
            return True
    return False


def is_retryable_object_store_error(exc: BaseException) -> bool:
    """Return True for transient object-store setup/read failures.

    Throttle-specific evidence overrides a not-found message; a not-found with
    no throttle evidence stays non-retryable. Auth/404 signals win over all.
    """
    candidates = tuple(iter_exception_chain(exc))
    has_object_store_context = False
    has_not_found = False

    for candidate in candidates:
        status_code = get_status_code(candidate)
        if status_code in NON_RETRYABLE_OBJECT_STORE_STATUS_CODES:
            return False

        msg = str(candidate).lower()
        if not msg:
            continue
        if has_marker(msg, OBJECT_STORE_CONTEXT_MARKERS):
            has_object_store_context = True
        if is_not_found_object_store_message(msg):
            has_not_found = True
        if has_marker(msg, NON_RETRYABLE_OBJECT_STORE_MARKERS):
            return False

    # Typed throttle errors are definitive alone; other throttle evidence still
    # needs object-store context (a not-found message counts as context).
    for candidate in candidates:
        if isinstance(candidate, LANCE_NAMESPACE_THROTTLE_ERRORS):
            return True
    if (has_object_store_context or has_not_found) and _has_throttle_evidence(
        candidates
    ):
        return True

    if has_not_found:
        return False

    for candidate in candidates:
        status_code = get_status_code(candidate)
        if (
            has_object_store_context
            and status_code in RETRYABLE_OBJECT_STORE_STATUS_CODES
        ):
            return True

        msg = str(candidate).lower()
        if not msg:
            continue
        if has_object_store_context and has_marker(msg, RETRYABLE_OBJECT_STORE_MARKERS):
            return True

    return False
