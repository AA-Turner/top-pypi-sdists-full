"""The browser file-session cookie lane (GET byte routes only) and its drift detector."""

from __future__ import annotations

import asyncio
import logging
import time

from starlette.requests import HTTPConnection, Request

from matrx_connect.context.app_context import AppContext
from ..authority_retry import call_authority
from ..file_session import classify_bound_file_session_value
from ..session_authority import (
    SessionAuthorityUnavailable,
)

from .types import (
    COOKIE_DRIFT_LOG_WINDOW_SECONDS,
)


class FileCookieLane:
    """Mixin on ``AuthMiddleware``: ``mx_files_session`` cookie -> user, and the drift alarm."""

    async def _file_cookie_user(self, value: str | None) -> str | None:
        """Authenticate a byte cookie; source decisions are fresh and never cached."""
        if value and value.startswith("v2."):
            credential, reason = classify_bound_file_session_value(value, self._guest_fp_secret)
            if reason == "signature_mismatch":
                self._report_cookie_drift(reason)
            if credential is None:
                return None
            if self._resolve_file_session is None:
                raise SessionAuthorityUnavailable("file-session authority not configured")
            try:
                resolve_file = self._resolve_file_session
                flight_key = "file:" + self._hash_token(value)
                active = await call_authority(
                    lambda: self._session_flights.do(
                        flight_key,
                        lambda: resolve_file(credential),
                        limit_seconds=self._session_resolve_timeout,
                    ),
                    attempt_timeout=self._session_resolve_timeout,
                    label="File-session authority",
                )
            except asyncio.CancelledError:
                raise
            except Exception as exc:
                logging.getLogger(__name__).warning(
                    "File-session authority unavailable (%s)", type(exc).__name__
                )
                raise SessionAuthorityUnavailable("file-session authority unavailable") from exc
            return credential.user_id if active is True else None
        if self._require_file_session_source:
            return None
        from ..session_cookie import classify_session_cookie_value

        user, reason = classify_session_cookie_value(value, self._guest_fp_secret)
        if reason == "signature_mismatch":
            self._report_cookie_drift(reason)
        return user

    def _report_cookie_drift(self, reason: str) -> None:
        """CRITICAL alarm for the mx_files_session drift detector, rate-limited
        per (process, reason) burst-window.

        First occurrence logs immediately; further occurrences within
        ``COOKIE_DRIFT_LOG_WINDOW_SECONDS`` are counted silently; the next
        occurrence after the window logs again carrying the suppressed count.
        The token ``MX_COOKIE_SIGNATURE_MISMATCH`` is machine-greppable.
        """
        import logging

        now = time.monotonic()
        last, suppressed = self._drift_log_state.get(reason, (None, 0))
        if last is not None and now - last < COOKIE_DRIFT_LOG_WINDOW_SECONDS:
            self._drift_log_state[reason] = (last, suppressed + 1)
            return
        suppressed_note = (
            f" ({suppressed} further occurrence(s) suppressed in the last burst window)"
            if suppressed
            else ""
        )
        source = "EPHEMERAL per-process fallback" if self.secret_is_ephemeral else "injected"
        logging.getLogger("matrx_connect.auth").critical(
            "MX_COOKIE_SIGNATURE_MISMATCH: a structurally valid, UNEXPIRED "
            "mx_files_session cookie failed HMAC verification%s. This is secret "
            "drift — the cookie was minted by a process holding a DIFFERENT "
            "guest_fingerprint_secret (or it was tampered with); it is never a "
            "normal anonymous request, and every private file render for this "
            "client is 401ing. This process's secret is %s. Remedy: inject ONE "
            "stable guest_fingerprint_secret into AuthMiddleware on EVERY "
            "instance/container (the 2026-08-30 private-file outage class).",
            suppressed_note,
            source,
        )
        self._drift_log_state[reason] = (now, 0)

    async def _file_cookie_lane(
        self, request: Request | HTTPConnection, ctx: AppContext
    ) -> AppContext | None:
        """Lane 6: file-session cookie, GET byte routes only. None = not claimed."""
        # ------------------------------------------------------------------
        # Browser file-session cookie — the durable private render lane.
        # Accepted ONLY on GET byte-serving routes (COOKIE_AUTH_PATH_RE):
        # an <img>/<video> tag cannot send Authorization headers, and this
        # cookie can never authorize anything but reading bytes the user
        # already has access to. Source-enabled hosts also check current
        # authority; see middleware/file_session.py.
        # ------------------------------------------------------------------
        # ``.method`` only exists on a full HTTP ``Request``; a WebSocket
        # handshake is admitted through this same builder via a bare
        # ``HTTPConnection`` (see ``_admit_websocket``), which has no
        # ``.method`` at all — the file-session cookie lane is HTTP-GET-only
        # by design, so it is simply unreachable for a WS connection.
        if getattr(request, "method", None) == "GET":
            from ..session_cookie import (
                COOKIE_AUTH_PATH_RE,
                SESSION_COOKIE_NAME,
            )

            if COOKIE_AUTH_PATH_RE.match(request.url.path):
                cookie_user = await self._file_cookie_user(
                    request.cookies.get(SESSION_COOKIE_NAME)
                )
                if cookie_user:
                    return ctx.with_overrides(
                        auth_type="cookie",
                        user_id=cookie_user,
                        is_authenticated=True,
                    )

        return None
