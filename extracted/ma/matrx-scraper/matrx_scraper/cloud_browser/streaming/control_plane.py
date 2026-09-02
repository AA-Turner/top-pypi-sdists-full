"""The mint authority + control-lease operations (the Browser Manager side).

In production these live in the matrx-scraper Browser Manager routers (WS-5) and
write ``browser.*`` rows. WS-4 ships them as a service class over the in-memory
plane so the mint→claim→renew→release/revoke flow is exercisable end to end with
the stub endpoint, against any headed Chromium.

Every user-facing call independently calls the access resolver
(``iam.has_access_for('browser_profile', …)``) — none trusts a prior check, a
cached answer, or the active organization (S4 §2 preamble).
"""

from __future__ import annotations

import secrets
import time

from .config import (
    CONTROL_LEASE_RENEW_INTERVAL_SECONDS,
    CONTROL_MEDIA_POLICY,
    VIEW_MEDIA_POLICY,
    VIEWPORT_HEIGHT,
    VIEWPORT_WIDTH,
    StreamingConfig,
)
from .errors import (
    GRANT_EXPIRED,
    GRANT_REVOKED,
    HANDOFF_NOT_CLAIMABLE,
    MEMBERSHIP_LOST,
    MULTI_VIEW_NOT_ENABLED,
    StreamError,
)
from .gateway import StreamGateway
from .models import (
    ControlBlock,
    IceBlock,
    MediaBlock,
    MintResponse,
    ViewportBlock,
)
from .plane import StreamPlane
from .ticket_store import TicketRecord, ticket_hash
from .turn_credentials import mint_turn_credential


class MintService:
    """Mints handoff-scoped (control) and run-scoped (view) tickets."""

    def __init__(
        self, plane: StreamPlane, gateway: StreamGateway, *, multi_view_low_latency: bool = False
    ) -> None:
        self.plane = plane
        self.gateway = gateway
        # OPEN(multi-view-floor): low-latency multi-view ships only on a passing
        # P5. Until then a `view` low-latency mint is refused. The redacted
        # periodic observation channel (WS-2/WS-8) is the v1 view path and does
        # not use this mint.
        self.multi_view_low_latency = multi_view_low_latency

    # --- control (handoff-scoped) mint -----------------------------------
    def mint_control(
        self, *, handoff_id: str, user_id: str, origin: str | None, takeover: bool
    ) -> MintResponse:
        cfg = self.plane.config
        cfg.require_signing_key()
        if not cfg.origin_allowed(origin):
            raise StreamError("stream_ticket_origin_mismatch", "origin not allowlisted")

        run = self.plane.runs_by_handoff(handoff_id)
        # Access: editor required for control.
        answer = self._require(user_id=user_id, profile_id=run.profile_id, required="editor")

        # The handoff must be claimable and claimed by this user (or unclaimed).
        if (
            run.active_handoff_id != handoff_id
            or run.handoff_returned
            or run.handoff_cancelled
            or run.handoff_expires_at <= time.time()
        ):
            raise StreamError(HANDOFF_NOT_CLAIMABLE, "handoff is not claimable")

        # Claim (or reconnect within grace to) the control lease for this user.
        # A second live control tab is rejected unless takeover was requested.
        existing = self.gateway.sessions.live_control_sessions_for_run(run.run_id)
        if existing and not takeover:
            raise StreamError("stream_already_connected", "a control session is already live")
        if existing and takeover:
            for s in existing:
                self.gateway.revoker.revoke_session(s, reason="superseded_by_new_connection")

        run = self.plane.runs.claim_control(
            run_id=run.run_id,
            new_kind="human",
            user_id=user_id,
            expected_revision=(
                run.control_revision if run.controller_user_id == user_id else run.control_revision
            ),
        )
        run.handoff_claimant_user_id = user_id

        # New mint revokes this user's prior unclaimed tickets for the run+mode.
        self.plane.tickets.revoke_unclaimed_for_user_run_mode(
            user_id, run.run_id, "control", "superseded_by_new_ticket"
        )

        stream_session_id = secrets.token_urlsafe(12)
        ticket, expires_at = self.plane.signer.mint(
            user_id=user_id,
            origin=origin,  # already allowlisted + non-None
            profile_id=run.profile_id,
            run_id=run.run_id,
            handoff_id=handoff_id,
            control_revision=run.control_revision,
            grant_revision=answer.grant_revision,
            access_level=answer.level,
            mode="control",
            worker_id=run.worker_id,
            stream_session_id=stream_session_id,
            audio_allowed=CONTROL_MEDIA_POLICY.audio,
        )
        self._record_ticket(
            ticket,
            run,
            user_id,
            "control",
            stream_session_id,
            run.control_revision,
            answer.grant_revision,
            expires_at,
            handoff_id,
        )

        return self._build_response(
            ticket=ticket,
            expires_at=expires_at,
            stream_session_id=stream_session_id,
            mode="control",
            control=ControlBlock(
                control_revision=run.control_revision,
                lease_expires_at=int(run.control_lease_expires_at),
                renew_interval_seconds=CONTROL_LEASE_RENEW_INTERVAL_SECONDS,
            ),
            media=CONTROL_MEDIA_POLICY.as_dict(),
        )

    # --- view (run-scoped) mint (S4 §9) ----------------------------------
    def mint_view(self, *, run_id: str, user_id: str, origin: str | None) -> MintResponse:
        cfg = self.plane.config
        cfg.require_signing_key()
        if not cfg.origin_allowed(origin):
            raise StreamError("stream_ticket_origin_mismatch", "origin not allowlisted")
        if not self.multi_view_low_latency:
            # v1: honest refusal rather than a degraded surprise. The redacted
            # observation channel is a separate, non-encoder path.
            raise StreamError(MULTI_VIEW_NOT_ENABLED, "low-latency multi-view is not enabled in v1")

        run = self.plane.runs.get(run_id)
        answer = self._require(user_id=user_id, profile_id=run.profile_id, required="viewer")

        stream_session_id = secrets.token_urlsafe(12)
        ticket, expires_at = self.plane.signer.mint(
            user_id=user_id,
            origin=origin,
            profile_id=run.profile_id,
            run_id=run.run_id,
            handoff_id=None,
            control_revision=None,
            grant_revision=answer.grant_revision,
            access_level=answer.level,
            mode="view",
            worker_id=run.worker_id,
            stream_session_id=stream_session_id,
            audio_allowed=False,  # view forces audio off (S4 §9)
        )
        self._record_ticket(
            ticket,
            run,
            user_id,
            "view",
            stream_session_id,
            None,
            answer.grant_revision,
            expires_at,
            None,
        )
        return self._build_response(
            ticket=ticket,
            expires_at=expires_at,
            stream_session_id=stream_session_id,
            mode="view",
            control=None,
            media=VIEW_MEDIA_POLICY.as_dict(),
        )

    # --- control-lease ops ------------------------------------------------
    def release_control(
        self, *, run_id: str, user_id: str, control_revision: int, reason: str
    ) -> dict:
        released = self.plane.runs.release_control(run_id=run_id, control_revision=control_revision)
        # Input dies first regardless (idempotent).
        self.gateway.revoker.revoke_run_control(run_id, reason=reason)
        return {"status": "released" if released else "already_released"}

    def revoke_control(
        self, *, run_id: str, user_id: str, control_revision: int, reason: str, confirm: bool
    ) -> dict:
        if not confirm:
            raise StreamError("control_lease_lost", "owner revoke requires confirm=true")
        # Owner/Full authorization (item-level admin).
        self._require(
            user_id=user_id, profile_id=self.plane.runs.get(run_id).profile_id, required="admin"
        )
        self.gateway.revoker.revoke_run_control(run_id, reason=reason)
        self.plane.runs.force_revoke(run_id=run_id)
        return {"status": "revoked"}

    # --- helpers ----------------------------------------------------------
    def _require(self, *, user_id: str, profile_id: str, required: str):
        answer = self.plane.access.resolve(user_id=user_id, profile_id=profile_id)
        if not answer.membership_ok:
            raise StreamError(MEMBERSHIP_LOST, "membership lost")
        if not answer.meets(required):
            raise StreamError(GRANT_REVOKED, "insufficient access")
        return answer

    def _record_ticket(
        self,
        ticket,
        run,
        user_id,
        mode,
        sid,
        control_revision,
        grant_revision,
        expires_at,
        handoff_id,
    ):
        self.plane.tickets.record(
            TicketRecord(
                ticket_hash=ticket_hash(ticket),
                run_id=run.run_id,
                profile_id=run.profile_id,
                user_id=user_id,
                mode=mode,
                stream_session_id=sid,
                handoff_id=handoff_id,
                control_revision=control_revision,
                grant_revision=grant_revision,
                minted_at=time.time(),
                expires_at=float(expires_at),
            )
        )

    def _build_response(
        self, *, ticket, expires_at, stream_session_id, mode, control, media
    ) -> MintResponse:
        cfg = self.plane.config
        turn = mint_turn_credential(cfg, stream_session_id=stream_session_id)
        endpoint = f"{cfg.gateway_ws_base}/stream/{stream_session_id}/signal"
        return MintResponse(
            ticket=ticket,
            expires_at=int(expires_at),
            endpoint=endpoint,
            stream_session_id=stream_session_id,
            mode=mode,
            control=control,
            media=MediaBlock(**media),
            ice=IceBlock(
                stun_urls=list(turn.stun_urls),
                turn_urls=list(turn.turn_urls),
                turn_username=turn.username,
                turn_credential=turn.credential,
                turn_expires_at=turn.expires_at,
            ),
            viewport=ViewportBlock(width=VIEWPORT_WIDTH, height=VIEWPORT_HEIGHT),
        )
