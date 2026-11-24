"""WebSocket admission: the same identity + organization admission as HTTP."""

from __future__ import annotations


from matrx_utils import vcprint
from starlette.requests import HTTPConnection
from starlette.types import Receive, Scope, Send

from matrx_connect.context.app_context import clear_app_context, set_app_context
from ..session_authority import (
    CredentialAuthorityUnavailable,
)

from .types import (
    ApiKeyOrganizationMismatch,
)


class WebSocketAdmission:
    """Mixin on ``AuthMiddleware``: handshake admission and the ASGI close it answers with."""

    async def _admit_websocket(self, scope: Scope, receive: Receive, send: Send) -> None:
        """Give the WebSocket lane the SAME identity + organization admission
        as the HTTP lane, instead of the no-op early return this branch used
        to be (it built no ``AppContext`` at all — no identity check, no
        organization check, for ANY WebSocket connection, on every host).

        Admission is based on whatever the handshake itself carries: a
        ``Authorization`` bearer token, an ``mx_...`` API key, a guest
        fingerprint header, or ``X-Organization-Id`` — exactly the lanes
        ``_build_context`` already resolves for HTTP, reused here via a bare
        ``HTTPConnection`` (headers/cookies/query only; nothing here ever
        calls ``receive()`` for a message body).

        * No identity at handshake → admitted through unchanged. Several WS
          endpoints (e.g. google_specialized's realtime sockets) authenticate
          via a message sent AFTER ``websocket.accept()``, which this gate
          cannot see — that is each handler's OWN admission to make, and nothing
          here removes the need for it. This gate only closes the lane for
          identity carried at handshake time.
        * Identity present, verified organization present, or the path is
          exempt → admitted.
        * Identity present, no organization, not exempt → refused: the
          connection is closed at handshake with a clear reason, never handed
          to the app and never left to hang.
        """
        connection = HTTPConnection(scope, receive)

        try:
            ctx = await self._build_context(connection)
        except CredentialAuthorityUnavailable as error:
            await self._close_websocket_handshake(
                receive, send, code=1013, reason=error.code
            )
            return
        except ApiKeyOrganizationMismatch:
            await self._close_websocket_handshake(
                receive, send, code=4409, reason="organization_context_mismatch"
            )
            return

        reason = self._organization_admission_reason(connection, ctx)
        if reason is not None:
            vcprint(
                f"[AUTH][REJECT] WS {scope.get('path')} — {reason} (user={ctx.user_id}, "
                f"claimed={getattr(ctx, 'claimed_organization_id', None)})",
                color="yellow",
                # Same expected caller denial as the HTTP 400 above.
                log_level="WARNING",
            )
            # The close reason is the only channel a handshake refusal has, so
            # it carries the SAME code the HTTP lane returns — a socket closed
            # with "organization_required" when the truth is "you are not a
            # member" is the F1 defect wearing a different transport.
            await self._close_websocket_handshake(receive, send, code=4400, reason=reason)
            return

        scope.setdefault("state", {})
        scope["state"]["context"] = ctx

        token = set_app_context(ctx)
        try:
            async with self._request_scoped(ctx):
                await self.app(scope, receive, send)
        finally:
            clear_app_context(token)

    @staticmethod
    async def _close_websocket_handshake(
        receive: Receive, send: Send, *, code: int, reason: str
    ) -> None:
        """Refuse a WebSocket at handshake, per ASGI: the server's first
        event to the app is ``websocket.connect``; the app answers with
        either ``websocket.accept`` or ``websocket.close`` before anything
        else. This middleware never called ``self.app`` for a refused
        connection, so it must consume that ``connect`` event itself and
        answer ``close`` directly — never silently drop the socket (that
        reads as a hang, not a refusal) and never forward a refused
        connection to the app.
        """
        connect_event = await receive()
        if connect_event.get("type") != "websocket.connect":
            # Protocol violation upstream — nothing we can cleanly close.
            return
        await send({"type": "websocket.close", "code": code, "reason": reason})
