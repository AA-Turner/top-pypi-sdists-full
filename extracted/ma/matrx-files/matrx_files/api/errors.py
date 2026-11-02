"""ONE exception→HTTP mapper for every matrx-files router.

A 500 THAT SAYS NOTHING IS A SECOND BUG. Before 2026-08-11 each router had
its own ``_map_exc`` whose 500 branch discarded the exception outright:
nothing was logged (no traceback, no exception class, no request id) and the
body was a flat ``{"error": "internal", "message": "File operation failed"}``.
A real production failure — every finished audio recording refusing to save,
for weeks — therefore left behind exactly three ``500 Internal Server Error``
access-log lines and no way to tell WHAT failed. Diagnosing it needed a
laptop, a fresh reproduction, and a bisect of the request payload.

So this module guarantees, for every unmapped exception:

* a ``logger.exception`` line carrying the operation, the request id, the
  authenticated user, and the full traceback — greppable by request id; and
* a response body carrying ``error_class``, the real exception ``message``,
  the ``operation``, and the ``request_id``, plus a plain-language
  ``user_message``.

Returning the real exception text is deliberate. This is a first-party
service behind auth, its callers are our own clients, and the alternative
has now cost real user data-entry time twice. Anything genuinely secret
(keys, tokens, connection strings) must never be in an exception message in
the first place — that is a separate, stricter rule.
"""

from __future__ import annotations

import logging

from fastapi import HTTPException, status

logger = logging.getLogger(__name__)

# Exception → (status, error code). Everything absent is an unmapped 500.
#
# ValueError also covers matrx_orm.ParameterError (bad query params, e.g. a
# non-UUID id) — a client input error, never a 500.
_MAPPED: tuple[tuple[type[BaseException], int, str], ...] = (
    (PermissionError, status.HTTP_403_FORBIDDEN, "permission_denied"),
    (FileNotFoundError, status.HTTP_404_NOT_FOUND, "not_found"),
    (ValueError, status.HTTP_400_BAD_REQUEST, "invalid_request"),
)


def _mapped_dedup_error(exc: BaseException) -> HTTPException | None:
    """``DedupError`` carries its OWN ``status_code`` / ``error_code``.

    Without this branch a 409 the package raises deliberately
    (``FilePathConflictError`` from a rename/move ``23505``,
    ``DuplicateFileError`` from an upload) arrived at the client as an
    unmapped 500 — a real conflict dressed as a server fault. The exception
    class is the authority on its own status; this never guesses one.
    """
    try:
        from matrx_files.dedup import DedupError
    except Exception:  # pragma: no cover — import cycle / partial install
        return None
    if not isinstance(exc, DedupError):
        return None
    return HTTPException(exc.status_code, exc.to_dict())


def _mapped_device_write_error(exc: BaseException) -> HTTPException | None:
    """Refused device provenance is 400 with its own code (SPEC-SERVER §2.2).

    ``invalid_device`` / ``invalid_client_time`` / ``implausible_client_time``
    are client-input errors, not server faults: a skewed clock is a named state
    ON THE CLIENT, and a device id belonging to someone else is never stored.
    Without this branch each would arrive as an unmapped 500.
    """
    try:
        from matrx_files.cloud_sync.device_writes import DeviceWriteError
    except Exception:  # pragma: no cover
        return None
    if not isinstance(exc, DeviceWriteError):
        return None
    return HTTPException(
        status.HTTP_400_BAD_REQUEST, {"error": exc.code, "message": exc.message}
    )


def _mapped_idempotency_conflict(exc: BaseException) -> HTTPException | None:
    """Same idempotency key, a DIFFERENT request: 409, never a silent accept.

    SPEC-SERVER §3.3 rule 2. Reusing one key for two distinct writes is a client
    bug; accepting the second would make the key meaningless and could overwrite
    the first write's target.
    """
    try:
        from matrx_files.cloud_sync.idempotency import IdempotencyConflict
    except Exception:  # pragma: no cover
        return None
    if not isinstance(exc, IdempotencyConflict):
        return None
    return HTTPException(
        status.HTTP_409_CONFLICT,
        {
            "error": "idempotency_key_reuse",
            "message": str(exc),
            "idempotency_key": exc.key,
        },
    )


def _mapped_precondition_error(exc: BaseException) -> HTTPException | None:
    """A refused write precondition is **412**, never 409 and never 500.

    412 on all three write routes (SPEC-SERVER §3.2): TUS already owns 409 for
    upload-session state, so reusing it here would make "your bytes are stale"
    indistinguishable from "your upload session is wrong". The body IS the
    engine's conflict input -- it carries the current checksum, version, size,
    updated_at and origin device -- so it is returned verbatim rather than
    summarized. Without this branch a deliberate 412 would arrive as an unmapped
    500 and every daemon would treat a normal conflict as a server fault.
    """
    try:
        from matrx_files.cloud_sync.preconditions import (
            PreconditionError,
            PreconditionFailed,
        )
    except Exception:  # pragma: no cover — import cycle / partial install
        return None
    if isinstance(exc, PreconditionFailed):
        return HTTPException(status.HTTP_412_PRECONDITION_FAILED, exc.payload)
    if isinstance(exc, PreconditionError):
        return HTTPException(
            status.HTTP_400_BAD_REQUEST, {"error": exc.code, "message": exc.message}
        )
    return None


def current_request_context() -> tuple[str | None, str | None]:
    """``(request_id, user_id)`` from the ambient AppContext, or ``(None, None)``.

    The auth middleware already honors the client's ``X-Request-Id`` and
    stashes it on the context, so a 500 can name the exact id the client
    logged without any router having to thread the header through.
    """
    try:
        from matrx_connect import try_get_app_context

        ctx = try_get_app_context()
    except Exception:  # pragma: no cover - context/plumbing absent
        return None, None
    if ctx is None:
        return None, None
    return getattr(ctx, "request_id", None), getattr(ctx, "user_id", None)


def map_exception(
    exc: BaseException,
    *,
    operation: str,
    user_message: str | None = None,
) -> HTTPException:
    """Map ``exc`` to an HTTPException, screaming about anything unmapped.

    ``operation`` is the thing the caller was doing ("file upload", "share
    link resolution") and appears in both the log line and the body, so a
    reader never has to guess which of a route's steps failed.
    """
    if isinstance(exc, HTTPException):
        return exc

    dedup = _mapped_dedup_error(exc)
    if dedup is not None:
        return dedup

    precondition = _mapped_precondition_error(exc)
    if precondition is not None:
        return precondition

    idempotency = _mapped_idempotency_conflict(exc)
    if idempotency is not None:
        return idempotency

    device = _mapped_device_write_error(exc)
    if device is not None:
        return device

    # A host exception that names its own HTTP status, code and user message keeps them
    # (e.g. a host refusing a storage write), instead of becoming an unmapped 500.
    own_status = getattr(exc, "http_status", None)
    own_code = getattr(exc, "code", None)
    if isinstance(own_status, int) and isinstance(own_code, str):
        body = {"error": own_code, "message": str(exc)}
        own_user_message = getattr(exc, "user_message", None)
        if isinstance(own_user_message, str) and own_user_message:
            body["user_message"] = own_user_message
        return HTTPException(own_status, body)

    for exc_type, http_status, code in _MAPPED:
        if isinstance(exc, exc_type):
            return HTTPException(http_status, {"error": code, "message": str(exc)})

    request_id, user_id = current_request_context()
    detail = str(exc).strip() or repr(exc)
    logger.exception(
        "[matrx-files] %s FAILED — %s: %s (request_id=%s user_id=%s)",
        operation,
        type(exc).__name__,
        detail,
        request_id or "<none>",
        user_id or "<none>",
    )
    return HTTPException(
        status.HTTP_500_INTERNAL_SERVER_ERROR,
        {
            "error": "internal",
            "operation": operation,
            "error_class": type(exc).__name__,
            "message": f"{operation} failed — {type(exc).__name__}: {detail}",
            "user_message": user_message or f"Could not complete the {operation}.",
            "request_id": request_id,
        },
    )
