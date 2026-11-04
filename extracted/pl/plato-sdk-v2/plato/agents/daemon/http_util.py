"""Server-side helpers for typed request parsing and structured responses.

Keeps every service handler small and uniform: parse a pydantic request body,
return a pydantic response, and turn any failure into a structured ``RpcError``
JSON body (never a bare aiohttp 500). The daemon SURVIVES bad input — an
unknown route or malformed body is a typed error, not a crashed loop (the
git_ops stdio server's fatal flaw).
"""

from __future__ import annotations

import logging
from typing import TypeVar

from aiohttp import web
from pydantic import BaseModel, ValidationError

from plato.rpc.errors import HTTP_STATUS_BY_CODE, ErrorCode, RpcError
from plato.rpc.protocol import HEADER_REQUEST_ID

logger = logging.getLogger(__name__)

_ReqT = TypeVar("_ReqT", bound=BaseModel)


def request_id_of(request: web.Request) -> str:
    return request.headers.get(HEADER_REQUEST_ID, "")


def error_response(
    request: web.Request,
    code: ErrorCode,
    message: str,
    *,
    detail: dict[str, str] | None = None,
    retryable: bool = False,
) -> web.Response:
    error = RpcError(
        code=code,
        message=message,
        detail=detail or {},
        retryable=retryable,
        request_id=request_id_of(request),
    )
    return web.json_response(
        error.model_dump(mode="json"),
        status=HTTP_STATUS_BY_CODE[code],
        headers={HEADER_REQUEST_ID: error.request_id},
    )


def ok_response(request: web.Request, model: BaseModel, *, status: int = 200) -> web.Response:
    return web.json_response(
        model.model_dump(mode="json"),
        status=status,
        headers={HEADER_REQUEST_ID: request_id_of(request)},
    )


class TypedHttpError(web.HTTPException):
    """Raisable structured error. aiohttp returns it directly, so the JSON body
    reaches the client unchanged; the error middleware recognizes it by its
    ``application/json`` content type and passes it through untouched."""

    status_code = 400

    def __init__(self, request: web.Request, code: ErrorCode, message: str) -> None:
        error = RpcError(code=code, message=message, request_id=request_id_of(request))
        super().__init__(
            text=error.model_dump_json(),
            content_type="application/json",
            headers={HEADER_REQUEST_ID: error.request_id},
        )
        self.set_status(HTTP_STATUS_BY_CODE[code])


async def parse_body(request: web.Request, model_cls: type[_ReqT]) -> _ReqT:
    """Parse+validate the JSON body into ``model_cls``.

    Raises ``TypedHttpError`` on bad input — aiohttp returns it directly with
    the structured body intact.
    """
    try:
        raw = await request.read()
    except Exception as exc:  # pragma: no cover - transport-level read failure
        raise TypedHttpError(request, "INVALID_REQUEST", f"Could not read body: {exc}") from exc
    try:
        return model_cls.model_validate_json(raw)
    except ValidationError as exc:
        raise TypedHttpError(request, "INVALID_REQUEST", f"Invalid {model_cls.__name__}: {exc}") from exc


@web.middleware
async def error_middleware(request: web.Request, handler):
    """Catch-all so an unhandled exception becomes a structured INTERNAL error
    (or NOT_FOUND for an unknown route) rather than aiohttp's HTML 500/404."""
    try:
        return await handler(request)
    except web.HTTPException as exc:
        if exc.content_type == "application/json":
            return exc  # already typed by parse_body/service
        code: ErrorCode = "NOT_FOUND" if exc.status == 404 else "INTERNAL"
        return error_response(request, code, exc.reason or exc.text or "error")
    except Exception as exc:  # noqa: BLE001 - last-resort guard keeps the daemon alive
        logger.exception("Unhandled error in %s %s", request.method, request.path)
        return error_response(request, "INTERNAL", str(exc))
