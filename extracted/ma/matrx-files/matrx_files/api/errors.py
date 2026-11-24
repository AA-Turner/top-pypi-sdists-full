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

from fastapi import HTTPException, Request, status

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


# ---------------------------------------------------------------------------
# The ApiError envelope — {error, message, user_message, details, request_id}
# (file-service STATE.md § wire contract). The aidream host renders its own
# HTTPExceptions into this shape; the standalone service installs the handlers
# below so BOTH hosts answer every failure identically — never FastAPI's bare
# ``{"detail": ...}`` or a raw 422 list.
# ---------------------------------------------------------------------------

_STATUS_CODES: dict[int, str] = {
    400: "invalid_request",
    401: "authentication_required",
    403: "permission_denied",
    404: "not_found",
    405: "method_not_allowed",
    409: "conflict",
    412: "precondition_failed",
    413: "payload_too_large",
    415: "unsupported_media_type",
    416: "range_not_satisfiable",
    422: "invalid_request",
    429: "rate_limited",
}

_STATUS_USER_MESSAGES: dict[int, str] = {
    400: "That request was not valid.",
    401: "Please sign in again.",
    403: "You do not have access to this file.",
    404: "That file could not be found.",
    409: "That conflicts with something that already exists.",
    413: "That file is too large.",
    429: "Too many requests. Try again shortly.",
}


def api_error_body(
    status_code: int, detail: object, *, request_id: str | None = None
) -> dict[str, object]:
    """Render any HTTPException ``detail`` as the ONE ApiError envelope."""
    if isinstance(detail, dict):
        body = dict(detail)
        error = body.pop("error", None) or _STATUS_CODES.get(status_code, "internal" if status_code >= 500 else "error")
        message = body.pop("message", None) or str(detail)
        user_message = body.pop("user_message", None)
        details = body.pop("details", None)
        rid = body.pop("request_id", None) or request_id
        if body:  # any other keys the raiser named ride in details, never dropped
            if details is None:
                details = body
            elif isinstance(details, dict):
                details = {**details, **body}
            else:
                details = {"details": details, **body}
    else:
        error = _STATUS_CODES.get(status_code, "internal" if status_code >= 500 else "error")
        message = str(detail) if detail is not None else error
        user_message = None
        details = None
        rid = request_id
    if not user_message:
        user_message = _STATUS_USER_MESSAGES.get(
            status_code, "Something went wrong." if status_code >= 500 else message
        )
    return {
        "error": error,
        "message": message,
        "user_message": user_message,
        "details": details,
        "request_id": rid,
    }


def _request_id_for(request) -> str | None:
    rid, _ = current_request_context()
    if rid:
        return rid
    try:
        return request.headers.get("x-request-id")
    except Exception:  # pragma: no cover
        return None


def install_error_handlers(app) -> None:
    """Make every failure on ``app`` an ApiError (standalone service)."""
    from fastapi.exceptions import RequestValidationError
    from fastapi.responses import JSONResponse
    from starlette.exceptions import HTTPException as StarletteHTTPException

    @app.exception_handler(StarletteHTTPException)
    async def _http(request, exc):  # noqa: ANN001
        return JSONResponse(
            api_error_body(exc.status_code, exc.detail, request_id=_request_id_for(request)),
            status_code=exc.status_code,
            headers=getattr(exc, "headers", None),
        )

    @app.exception_handler(RequestValidationError)
    async def _validation(request, exc):  # noqa: ANN001
        errors = exc.errors()
        first = errors[0] if errors else {}
        where = ".".join(str(p) for p in first.get("loc", ()) if p != "body")
        message = f"{where}: {first.get('msg', 'invalid value')}" if where else str(first.get("msg", "invalid request"))
        body = api_error_body(
            400,
            {
                "error": "invalid_request",
                "message": message,
                "details": {"errors": [
                    {"loc": list(e.get("loc", ())), "msg": e.get("msg"), "type": e.get("type")}
                    for e in errors
                ]},
            },
            request_id=_request_id_for(request),
        )
        return JSONResponse(body, status_code=400)

    @app.exception_handler(Exception)
    async def _unhandled(request, exc):  # noqa: ANN001
        mapped = map_exception(exc, operation=f"{request.method} {request.url.path}")
        return JSONResponse(
            api_error_body(mapped.status_code, mapped.detail, request_id=_request_id_for(request)),
            status_code=mapped.status_code,
        )


# ---------------------------------------------------------------------------
# Malformed ids never reach the ORM. A non-UUID ``file_id`` used to travel into
# a query and come back as the ORM's ANSI-coloured ParameterError (SQL + args)
# on the standalone host and a 500 on the aidream host. Every ``*_id`` path
# parameter on a files router is a UUID; anything else is a 404 ApiError
# before any handler runs. Mounted as a router dependency by BOTH hosts.
# ---------------------------------------------------------------------------


def is_uuid(value: object) -> bool:
    import uuid

    if not isinstance(value, str):
        return False
    try:
        uuid.UUID(value)
    except (ValueError, AttributeError, TypeError):
        return False
    return True


async def refuse_malformed_path_ids(request: Request) -> None:
    """Router dependency: every ``*_id`` path param must be a UUID → else 404."""
    for name, value in (request.path_params or {}).items():
        if name.endswith("_id") and not is_uuid(value):
            noun = name[: -len("_id")].replace("_", " ") or "record"
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                {
                    "error": "not_found",
                    "message": f"No {noun} with id {value!r} — ids are UUIDs",
                    "user_message": f"That {noun} could not be found.",
                    "details": {"param": name},
                },
            )
