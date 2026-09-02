"""The authenticated streaming gateway (S4 §3.2, §4, §5.4, §6).

The gateway is the only thing that exchanges a ticket for a stream session. It
runs the ten independent claim checks, sets the scoped HttpOnly cookie, connects
outbound to the assigned worker on the private network, re-authorizes on every
renewal, and enforces the revocation ordering (input dies first).

Selkies is never the product auth boundary — it sits behind this gateway
(PLAN.md §Authentication boundary).
"""

from __future__ import annotations

import secrets
import threading
import time
from dataclasses import dataclass, field

from .config import (
    CONTROL_LEASE_RENEW_INTERVAL_SECONDS,
    STREAM_COOKIE_NAME,
    STREAM_COOKIE_MAX_AGE_SECONDS,
    StreamingConfig,
)
from .errors import (
    STREAM_ALREADY_CONNECTED,
    STREAM_SESSION_NOT_FOUND,
    STREAM_TICKET_ORIGIN_MISMATCH,
    STREAM_TICKET_USER_MISMATCH,
    CONTROL_LEASE_LOST,
    GRANT_EXPIRED,
    GRANT_REVOKED,
    HANDOFF_EXPIRED,
    HANDOFF_NOT_CLAIMABLE,
    MEMBERSHIP_LOST,
    RUN_NOT_LIVE,
    WORKER_UNAVAILABLE,
    StreamError,
)
from .plane import StreamPlane
from .ticket_store import ticket_hash
from .tickets import TicketClaims


@dataclass
class StreamSession:
    stream_session_id: str
    run_id: str
    profile_id: str
    user_id: str
    mode: str
    control_revision: int | None
    worker_id: str
    cookie_value: str
    created_at: float
    lease_expires_at: float
    grant_revision: int
    live: bool = True
    handoff_id: str | None = None


@dataclass
class ClaimResult:
    session: StreamSession
    cookie_header: str


class SessionRegistry:
    def __init__(self) -> None:
        self._by_id: dict[str, StreamSession] = {}
        self._lock = threading.Lock()

    def add(self, s: StreamSession) -> None:
        with self._lock:
            self._by_id[s.stream_session_id] = s

    def get(self, sid: str) -> StreamSession | None:
        with self._lock:
            return self._by_id.get(sid)

    def by_cookie(self, sid: str, cookie_value: str) -> StreamSession | None:
        with self._lock:
            s = self._by_id.get(sid)
            if s and s.cookie_value == cookie_value and s.live:
                return s
            return None

    def live_control_sessions_for_run(
        self, run_id: str, *, exclude: str | None = None
    ) -> list[StreamSession]:
        with self._lock:
            return [
                s
                for s in self._by_id.values()
                if s.run_id == run_id
                and s.mode == "control"
                and s.live
                and s.stream_session_id != exclude
            ]

    def sessions_for_run(self, run_id: str) -> list[StreamSession]:
        with self._lock:
            return [s for s in self._by_id.values() if s.run_id == run_id and s.live]

    def kill(self, sid: str) -> StreamSession | None:
        with self._lock:
            s = self._by_id.get(sid)
            if s:
                s.live = False
            return s


class StreamGateway:
    """Claim/renew and the session lifecycle. Revocation ordering (input first)
    is centralised in :class:`RevocationCoordinator` and called from here and the
    control plane."""

    def __init__(self, plane: StreamPlane, *, sessions: SessionRegistry | None = None) -> None:
        self.plane = plane
        self.sessions = sessions or SessionRegistry()
        self.revoker = RevocationCoordinator(plane, self.sessions)

    # --- claim (S4 §3.2 — ten independent checks) ------------------------
    def claim(
        self,
        *,
        stream_session_id: str,
        ticket: str,
        request_origin: str | None,
        authenticated_user_id: str,
    ) -> ClaimResult:
        cfg = self.plane.config

        # B1 signature/issuer/audience/expiry (raises typed).
        claims: TicketClaims = self.plane.signer.verify(ticket)

        # B5 session path match (checked early so a wrong path fails cleanly).
        if claims.stream_session_id != stream_session_id:
            raise StreamError(STREAM_SESSION_NOT_FOUND, "ticket is not for this session path")

        # B3 origin — byte-for-byte, no suffix/wildcard.
        if not request_origin or request_origin != claims.origin:
            raise StreamError(STREAM_TICKET_ORIGIN_MISMATCH, "origin does not match ticket")
        if not cfg.origin_allowed(request_origin):
            raise StreamError(STREAM_TICKET_ORIGIN_MISMATCH, "origin not allowlisted")

        # B4 user — the gateway's own authenticated user equals sub.
        if authenticated_user_id != claims.user_id:
            raise StreamError(STREAM_TICKET_USER_MISMATCH, "ticket subject is a different user")

        # B2 single use — atomic CAS on the ticket hash. Do this AFTER the cheap
        # stateless checks so a replay of an origin-mismatched ticket doesn't burn
        # a record, but BEFORE opening a session so a replay can never double-open.
        self.plane.tickets.claim(ticket_hash(ticket))

        # B6 run live + worker still assigned.
        run = self.plane.runs.get(claims.run_id)  # raises RUN_NOT_LIVE
        if run.worker_id != claims.worker_id:
            raise StreamError(WORKER_UNAVAILABLE, "assigned worker changed")

        # B7 access re-derived — the check that makes revocation real.
        required = "editor" if claims.mode == "control" else "viewer"
        answer = self.plane.access.resolve(user_id=claims.user_id, profile_id=claims.profile_id)
        if not answer.membership_ok:
            raise StreamError(MEMBERSHIP_LOST, "organization membership lost")
        if not answer.meets(required):
            raise StreamError(GRANT_REVOKED, "access revoked or insufficient")
        if answer.grant_revision != claims.grant_revision:
            raise StreamError(GRANT_REVOKED, "grant changed since the ticket was minted")

        if claims.mode == "control":
            self._verify_control_claimable(run, claims)

        # Open the session, connect to the worker, enable input (control only).
        cookie_value = secrets.token_urlsafe(16)
        now = time.time()
        session = StreamSession(
            stream_session_id=stream_session_id,
            run_id=claims.run_id,
            profile_id=claims.profile_id,
            user_id=claims.user_id,
            mode=claims.mode,
            control_revision=claims.control_revision,
            worker_id=claims.worker_id,
            cookie_value=cookie_value,
            created_at=now,
            lease_expires_at=run.control_lease_expires_at
            if claims.mode == "control"
            else now + 3600,
            grant_revision=answer.grant_revision,
            handoff_id=claims.handoff_id,
        )
        self.sessions.add(session)

        if claims.mode == "control":
            # Bind THE one input path at the worker (two-layer enforcement).
            ch = self.plane.workers.channel(claims.run_id)
            ch.enable_input(
                stream_session_id=stream_session_id,
                control_revision=claims.control_revision or 0,
                scopes=frozenset(claims.scopes),
            )

        return ClaimResult(
            session=session, cookie_header=self._cookie_header(stream_session_id, cookie_value)
        )

    def _verify_control_claimable(self, run, claims: TicketClaims) -> None:
        # B8 handoff claimable.
        if (
            run.active_handoff_id != claims.handoff_id
            or run.handoff_returned
            or run.handoff_cancelled
            or run.handoff_expires_at <= time.time()
        ):
            raise StreamError(HANDOFF_NOT_CLAIMABLE, "handoff is not claimable")
        if run.handoff_claimant_user_id not in (None, claims.user_id):
            raise StreamError(HANDOFF_NOT_CLAIMABLE, "handoff claimed by another user")
        # B9 lease held at the ticket's revision.
        if (
            run.control_revision != claims.control_revision
            or run.controller_user_id != claims.user_id
        ):
            raise StreamError(CONTROL_LEASE_LOST, "control lease no longer at ticket revision")
        if not run.lease_live():
            raise StreamError(CONTROL_LEASE_LOST, "control lease expired")
        # B10 no second control connection.
        existing = self.sessions.live_control_sessions_for_run(claims.run_id)
        if existing:
            raise StreamError(
                STREAM_ALREADY_CONNECTED, "a control session is already live on this run"
            )

    def _cookie_header(self, sid: str, value: str) -> str:
        # S4 §4.2: __Secure- (host-only, no Domain), Path-scoped, HttpOnly,
        # SameSite=Strict, Max-Age = 2x lease.
        return (
            f"{STREAM_COOKIE_NAME}={value}; Path=/stream/{sid}; Secure; HttpOnly; "
            f"SameSite=Strict; Max-Age={STREAM_COOKIE_MAX_AGE_SECONDS}"
        )

    # --- renew (S4 §5.4 — a RE-AUTHORIZATION, not a keepalive) -----------
    def renew(
        self, *, stream_session_id: str, cookie_value: str, control_revision: int | None
    ) -> dict:
        session = self.sessions.by_cookie(stream_session_id, cookie_value)
        if session is None:
            raise StreamError(STREAM_SESSION_NOT_FOUND, "no such live session")

        run = self.plane.runs.get(session.run_id)  # RUN_NOT_LIVE if gone
        required = "editor" if session.mode == "control" else "viewer"
        answer = self.plane.access.resolve(user_id=session.user_id, profile_id=session.profile_id)
        if not answer.membership_ok:
            self.revoker.revoke_session(session, reason=MEMBERSHIP_LOST)
            raise StreamError(MEMBERSHIP_LOST, "membership lost")
        if not answer.meets(required):
            self.revoker.revoke_session(session, reason=GRANT_REVOKED)
            raise StreamError(GRANT_REVOKED, "access revoked")
        if answer.grant_revision != session.grant_revision:
            self.revoker.revoke_session(session, reason=GRANT_REVOKED)
            raise StreamError(GRANT_REVOKED, "grant changed")

        if session.mode == "control":
            if control_revision is None:
                raise StreamError(
                    CONTROL_LEASE_LOST, "control_revision required to renew a control session"
                )
            try:
                run = self.plane.runs.renew_control(
                    run_id=session.run_id,
                    control_revision=control_revision,
                    user_id=session.user_id,
                )
            except StreamError:
                self.revoker.revoke_session(session, reason=CONTROL_LEASE_LOST)
                raise
            session.lease_expires_at = run.control_lease_expires_at
            # handoff still active?
            if (
                run.handoff_returned
                or run.handoff_cancelled
                or run.handoff_expires_at <= time.time()
            ):
                self.revoker.revoke_session(session, reason=HANDOFF_EXPIRED)
                raise StreamError(HANDOFF_EXPIRED, "handoff no longer active")

        return {
            "lease_expires_at": int(session.lease_expires_at),
            "control_revision": session.control_revision,
            "grant_revision": answer.grant_revision,
            "next_renew_in_seconds": CONTROL_LEASE_RENEW_INTERVAL_SECONDS,
        }


class RevocationCoordinator:
    """The one place the revocation ORDER lives (S4 §5.2, §6): worker input dies
    FIRST and synchronously, then media/gateway session, then tickets/lease. The
    human's last frames are of a screen they can no longer touch."""

    def __init__(self, plane: StreamPlane, sessions: SessionRegistry) -> None:
        self.plane = plane
        self.sessions = sessions

    def revoke_session(self, session: StreamSession, *, reason: str) -> None:
        # 1. Input dies first, synchronously.
        if session.mode == "control":
            self.plane.workers.channel(session.run_id).kill_input()
        # 2. Tear down media / close the gateway session.
        self.sessions.kill(session.stream_session_id)
        # 3. Revoke this session's tickets.
        self.plane.tickets.revoke_for_session(session.stream_session_id, reason)

    def revoke_run_control(self, run_id: str, *, reason: str, to_kind: str = "agent") -> None:
        """Return/cancel/owner-revoke/stop path. Kills input first for the run,
        then all its control sessions, then releases/bumps the lease."""
        # Input off first for the whole run.
        self.plane.workers.channel(run_id).kill_input()
        for s in self.sessions.sessions_for_run(run_id):
            if s.mode == "control":
                self.sessions.kill(s.stream_session_id)
                self.plane.tickets.revoke_for_session(s.stream_session_id, reason)

    def revoke_grant(self, *, user_id: str, profile_id: str, reason: str = GRANT_REVOKED) -> None:
        """Grant revoked/lowered/expired, or membership lost. Kills THAT user's
        sessions on the profile; other authorized users are untouched
        (PLAN.md — the profile and Chromium stay alive)."""
        for s in list(self.sessions._by_id.values()):  # snapshot
            if s.live and s.user_id == user_id and s.profile_id == profile_id:
                self.revoke_session(s, reason=reason)
        self.plane.tickets.revoke_unclaimed_for_user_profile(user_id, profile_id, reason)
