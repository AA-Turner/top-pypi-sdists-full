"""Operator routes: deployment-wide actions a LangSmith admin can take on a deployment.

They are served before every other middleware, so customer middleware and custom
auth handlers can't block or filter them. Instead, host-backend checks the admin's
permission and calls them with a short-lived service token scoped to one operation on
this deployment, which LangSmith verifies. See THREAT_MODEL.md.
"""

from __future__ import annotations

import contextlib
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import TYPE_CHECKING, Any
from uuid import UUID

import httpx
import structlog
from starlette.applications import Starlette
from starlette.exceptions import HTTPException
from starlette.responses import JSONResponse, Response
from starlette.routing import Route

from langgraph_api import config
from langgraph_api.auth.langsmith.client import create_client
from langgraph_api.errors import app_exception_handlers
from langgraph_api.feature_flags import IS_POSTGRES_OR_GRPC_BACKEND
from langgraph_runtime.database import connect

if IS_POSTGRES_OR_GRPC_BACKEND:
    from langgraph_api.grpc.ops import Runs
else:
    from langgraph_runtime.ops import Runs

if TYPE_CHECKING:
    from starlette.requests import Request
    from starlette.types import ASGIApp, Message, Receive, Scope, Send

logger = structlog.stdlib.get_logger(__name__)

CANCEL_RUNS_PATH = "/operator/runs/cancel"

_OPERATOR_TOKEN_PATH = "/auth/operator-token"
_INTERRUPT = "interrupt"

# host-backend fixes the boundary at the press and mints every token after it, so a
# boundary later than the token's issue time would cancel runs accepted after the
# press. The allowance only covers clock differences between host-backend replicas.
_BOUNDARY_SKEW = timedelta(seconds=5)

# The route's refusal for each LangSmith answer other than 200. Anything not listed
# means LangSmith couldn't answer.
_LANGSMITH_REFUSALS = {
    401: (401, "invalid_token"),
    # A LangSmith release without operator tokens can't authorize this route.
    404: (503, "langsmith_upgrade_required"),
    405: (503, "langsmith_upgrade_required"),
}


@dataclass(frozen=True)
class _OperatorToken:
    """The cancellation a verified operator token authorizes."""

    operation_id: UUID
    user_id: UUID
    accepted_before: datetime


class OperatorRoutesMiddleware:
    """Serves the operator routes and passes every other request through."""

    def __init__(self, app: ASGIApp, mount_prefix: str | None = None) -> None:
        self.app = app
        self.cancel_runs_paths = {CANCEL_RUNS_PATH}
        if mount_prefix:
            self.cancel_runs_paths.add(mount_prefix + CANCEL_RUNS_PATH)
        # Its own small app with the server's error handlers, since these requests
        # never reach the main app.
        self.operator_app = Starlette(
            routes=[
                Route(path, cancel_runs, methods=["POST"])
                for path in self.cancel_runs_paths
            ],
            exception_handlers=app_exception_handlers(),
        )

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http" or scope["path"] not in self.cancel_runs_paths:
            await self.app(scope, receive, send)
            return
        status = None

        async def send_recording_status(message: Message) -> None:
            nonlocal status
            if message["type"] == "http.response.start":
                status = message["status"]
            await send(message)

        # Every operator request gets exactly one log line, including ones that fail
        # unexpectedly; customer request logging never sees them.
        try:
            await self.operator_app(scope, receive, send_recording_status)
        except Exception:
            await logger.aexception("Operator request", **_log_fields(scope, status))
            raise
        await logger.ainfo("Operator request", **_log_fields(scope, status))


def _log_fields(scope: Scope, status: int | None) -> dict[str, Any]:
    # cancel_runs records the verified operation and the progress on the request state.
    learned = scope.get("state", {}).get("operator_log_fields", {})
    return {
        "path": scope["path"],
        "method": scope["method"],
        "status": status,
    } | learned


async def cancel_runs(request: Request) -> Response:
    """Interrupt every in-flight run accepted at or before the token's boundary.

    The operation, boundary and user all come from the verified token; the request
    body is ignored. One call cancels a bounded amount of work and returns how many
    targets are still in flight, and the caller repeats it until both counts are zero.
    """
    token = await _verify_token(request)
    log_fields = {
        "operation_id": str(token.operation_id),
        "user_id": str(token.user_id),
    }
    request.state.operator_log_fields = log_fields

    # Built only from fixed text and UUIDs, never from text in the request.
    reason = (
        f"cancelled by kill switch (operation {token.operation_id}, "
        f"requested by LangSmith user {token.user_id})"
    )
    async with connect() as conn:
        progress = await Runs.cancel_accepted_before(
            conn, token.accepted_before, reason=reason
        )
    log_fields.update(progress)
    return JSONResponse(progress)


async def _verify_token(request: Request) -> _OperatorToken:
    """Return the cancellation the request's operator token authorizes here.

    LangSmith checks the token's signature, audience, subject and expiry on every
    call, with no cache. This route checks that the token names this deployment and
    an interrupt. Anything short of that is a refusal.
    """
    tenant_id = _as_uuid(config.LANGSMITH_TENANT_ID)
    deployment_id = _as_uuid(config.LANGSMITH_HOST_PROJECT_ID)
    if tenant_id is None or deployment_id is None:
        # Only a deployment LangSmith manages is sent operator tokens.
        raise HTTPException(404)
    token = request.headers.get("x-service-key")
    if not token:
        raise HTTPException(401, "missing_token")
    # A client per call, so nothing one verification leaves behind (such as a
    # cookie) reaches the next.
    auth = create_client()
    try:
        response = await auth.get(
            _OPERATOR_TOKEN_PATH, headers={"X-Service-Key": token}
        )
    except httpx.HTTPError as exc:
        raise HTTPException(503, "langsmith_unavailable") from exc
    finally:
        await auth.client.aclose()
    if response.status_code != 200:
        status, detail = _LANGSMITH_REFUSALS.get(
            response.status_code, (503, "langsmith_unavailable")
        )
        raise HTTPException(status, detail)
    try:
        claims = response.json()
    except ValueError as exc:
        raise HTTPException(503, "langsmith_unavailable") from exc
    if not isinstance(claims, dict):
        raise HTTPException(503, "langsmith_unavailable")

    operation_id = _as_uuid(claims.get("operation_id"))
    user_id = _as_uuid(claims.get("user_id"))
    accepted_before = _as_datetime(claims.get("accepted_before"))
    issued_at = _as_timestamp(claims.get("issued_at"))
    if (
        _as_uuid(claims.get("tenant_id")) != tenant_id
        or _as_uuid(claims.get("deployment_id")) != deployment_id
        or claims.get("action") != _INTERRUPT
        or operation_id is None
        or user_id is None
        or accepted_before is None
        or issued_at is None
        or accepted_before > issued_at + _BOUNDARY_SKEW
    ):
        raise HTTPException(403, "forbidden")
    return _OperatorToken(operation_id, user_id, accepted_before)


def _as_uuid(value: Any) -> UUID | None:
    if isinstance(value, str):
        with contextlib.suppress(ValueError):
            return UUID(value)
    return None


def _as_timestamp(value: Any) -> datetime | None:
    if isinstance(value, int | float) and not isinstance(value, bool):
        with contextlib.suppress(OverflowError, OSError, ValueError):
            return datetime.fromtimestamp(value, UTC)
    return None


def _as_datetime(value: Any) -> datetime | None:
    if isinstance(value, str):
        with contextlib.suppress(ValueError):
            parsed = datetime.fromisoformat(value)
            if parsed.tzinfo is not None:
                return parsed
    return None
