"""Standalone FastAPI app wiring the stub mint endpoint + the real gateway.

This is the WS-4 standalone harness (S4 §10): a mint endpoint issuing
contract-shaped tickets signed by a locally-generated EC P-256 key, over the
in-memory plane, plus the REAL gateway/verifier/cookie/renew/revocation. It runs
against any headed Chromium worker and needs no Browser Manager and no
``browser.*`` schema.

In production these routes are split: mint + control-lease ops live in the
Browser Manager routers (WS-5) on the app host and write ``browser.*``; the
gateway lives on its own ``stream.aimatrx.com`` subdomain (OPEN(gateway-host)).
The user identity here is a stub bearer (``Authorization: Bearer <user_id>``) —
production replaces ``_user_id`` with ``verify_supabase_token``. The gateway
NEVER accepts a stream ticket as a user login.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, FastAPI, Header, Request, Response
from fastapi.responses import JSONResponse

from .config import STREAM_COOKIE_NAME, StreamingConfig
from .control_plane import MintService
from .errors import StreamError
from .gateway import StreamGateway
from .models import (
    ClaimRequest,
    MintControlRequest,
    MintViewRequest,
    ReleaseRequest,
    RenewRequest,
    RevokeRequest,
)
from .plane import StreamPlane


def _user_id(authorization: str | None) -> str:
    """STUB identity. Production: verify_supabase_token(authorization).sub."""
    if not authorization or not authorization.lower().startswith("bearer "):
        raise StreamError("stream_ticket_user_mismatch", "missing bearer identity")
    return authorization.split(None, 1)[1].strip()


def _err(exc: StreamError) -> JSONResponse:
    return JSONResponse(status_code=exc.http_status, content=exc.as_response())


def build_app(*, plane: StreamPlane, gateway: StreamGateway, mint: MintService) -> FastAPI:
    app = FastAPI(title="matrx cloud-browser streaming (WS-4 standalone)")

    bm = APIRouter(prefix="/browser-manager")
    gw = APIRouter()

    # --- Browser Manager (mint + control ops) — stub stands in for WS-5 ---
    @bm.post("/handoffs/{handoff_id}/stream-ticket")
    def mint_control(
        handoff_id: str,
        body: MintControlRequest,
        authorization: str | None = Header(default=None),
        origin: str | None = Header(default=None),
    ):
        try:
            return mint.mint_control(
                handoff_id=handoff_id,
                user_id=_user_id(authorization),
                origin=origin,
                takeover=body.takeover,
            ).model_dump()
        except StreamError as exc:
            return _err(exc)

    @bm.post("/runs/{run_id}/stream-ticket")
    def mint_view(
        run_id: str,
        body: MintViewRequest,
        authorization: str | None = Header(default=None),
        origin: str | None = Header(default=None),
    ):
        try:
            return mint.mint_view(
                run_id=run_id, user_id=_user_id(authorization), origin=origin
            ).model_dump()
        except StreamError as exc:
            return _err(exc)

    @bm.post("/runs/{run_id}/release-control")
    def release(
        run_id: str, body: ReleaseRequest, authorization: str | None = Header(default=None)
    ):
        try:
            return mint.release_control(
                run_id=run_id,
                user_id=_user_id(authorization),
                control_revision=body.control_revision,
                reason=body.reason,
            )
        except StreamError as exc:
            return _err(exc)

    @bm.post("/runs/{run_id}/revoke-control")
    def revoke(run_id: str, body: RevokeRequest, authorization: str | None = Header(default=None)):
        try:
            return mint.revoke_control(
                run_id=run_id,
                user_id=_user_id(authorization),
                control_revision=body.control_revision,
                reason=body.reason,
                confirm=body.confirm,
            )
        except StreamError as exc:
            return _err(exc)

    # --- Gateway (claim + renew) ----------------------------------------
    @gw.post("/stream/{stream_session_id}/claim")
    def claim(
        stream_session_id: str,
        body: ClaimRequest,
        response: Response,
        authorization: str | None = Header(default=None),
        origin: str | None = Header(default=None),
    ):
        try:
            result = gateway.claim(
                stream_session_id=stream_session_id,
                ticket=body.ticket,
                request_origin=origin,
                authenticated_user_id=_user_id(authorization),
            )
        except StreamError as exc:
            return _err(exc)
        r = Response(status_code=204)
        r.headers["Set-Cookie"] = result.cookie_header
        return r

    @gw.post("/stream/{stream_session_id}/renew")
    def renew(stream_session_id: str, body: RenewRequest, request: Request):
        cookie = request.cookies.get(STREAM_COOKIE_NAME, "")
        try:
            return gateway.renew(
                stream_session_id=stream_session_id,
                cookie_value=cookie,
                control_revision=body.control_revision,
            )
        except StreamError as exc:
            return _err(exc)

    app.include_router(bm)
    app.include_router(gw)
    return app


def build_standalone_app(
    config: StreamingConfig, access: Any, *, multi_view_low_latency: bool = False
) -> FastAPI:
    plane = StreamPlane.build(config=config, access=access)
    gateway = StreamGateway(plane)
    mint = MintService(plane, gateway, multi_view_low_latency=multi_view_low_latency)
    app = build_app(plane=plane, gateway=gateway, mint=mint)
    app.state.plane = plane
    app.state.gateway = gateway
    app.state.mint = mint
    return app
