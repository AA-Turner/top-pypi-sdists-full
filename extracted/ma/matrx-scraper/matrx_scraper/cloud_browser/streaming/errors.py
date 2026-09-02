"""Typed stream/control errors — literal strings, because THREE repos consume
them (matrx-scraper gateway, matrx-frontend panel, matrx-runtime/WS-6).

Authority: contracts/S4-stream-tickets.md §2.7. The HTTP mapping is the frozen
seam; do not remap a code in one repo.
"""

from __future__ import annotations

# --- Literal error codes (S4 §2.7) ----------------------------------------
STREAM_TICKET_INVALID = "stream_ticket_invalid"
STREAM_TICKET_EXPIRED = "stream_ticket_expired"
STREAM_TICKET_ALREADY_CLAIMED = "stream_ticket_already_claimed"
STREAM_TICKET_REVOKED = "stream_ticket_revoked"
STREAM_TICKET_ORIGIN_MISMATCH = "stream_ticket_origin_mismatch"
STREAM_TICKET_USER_MISMATCH = "stream_ticket_user_mismatch"
STREAM_TICKET_NOT_CONFIGURED = "stream_ticket_not_configured"
STREAM_SESSION_NOT_FOUND = "stream_session_not_found"
STREAM_ALREADY_CONNECTED = "stream_already_connected"
CONTROL_LEASE_LOST = "control_lease_lost"
CONTROL_LEASE_EXPIRED = "control_lease_expired"
BROWSER_CONTROLLED_BY_HUMAN = "browser_controlled_by_human"
HANDOFF_NOT_CLAIMABLE = "handoff_not_claimable"
HANDOFF_EXPIRED = "handoff_expired"
GRANT_REVOKED = "grant_revoked"
GRANT_EXPIRED = "grant_expired"
MEMBERSHIP_LOST = "membership_lost"
RUN_NOT_LIVE = "run_not_live"
WORKER_UNAVAILABLE = "worker_unavailable"
MULTI_VIEW_NOT_ENABLED = "multi_view_not_enabled"
INPUT_NOT_PERMITTED = "input_not_permitted"

# HTTP mapping (S4 §2.7): 401 ticket/identity, 403 access, 409 lease/state,
# 410 gone, 503 not-configured / worker-unavailable.
_HTTP_BY_CODE: dict[str, int] = {
    STREAM_TICKET_INVALID: 401,
    STREAM_TICKET_EXPIRED: 401,
    STREAM_TICKET_ALREADY_CLAIMED: 401,
    STREAM_TICKET_REVOKED: 401,
    STREAM_TICKET_ORIGIN_MISMATCH: 401,
    STREAM_TICKET_USER_MISMATCH: 401,
    STREAM_TICKET_NOT_CONFIGURED: 503,
    STREAM_SESSION_NOT_FOUND: 410,
    STREAM_ALREADY_CONNECTED: 409,
    CONTROL_LEASE_LOST: 409,
    CONTROL_LEASE_EXPIRED: 409,
    BROWSER_CONTROLLED_BY_HUMAN: 409,
    HANDOFF_NOT_CLAIMABLE: 409,
    HANDOFF_EXPIRED: 410,
    GRANT_REVOKED: 403,
    GRANT_EXPIRED: 403,
    MEMBERSHIP_LOST: 403,
    RUN_NOT_LIVE: 410,
    WORKER_UNAVAILABLE: 503,
    MULTI_VIEW_NOT_ENABLED: 403,
    INPUT_NOT_PERMITTED: 403,
}


class StreamError(Exception):
    """A typed stream/control failure. ``code`` is one of the literals above;
    ``http_status`` is the frozen mapping. ``detail`` is a safe, human-readable
    message that never carries a ticket, cookie, TURN secret, worker address, or
    page content."""

    def __init__(self, code: str, detail: str = "", **extra: object) -> None:
        self.code = code
        self.detail = detail
        self.http_status = _HTTP_BY_CODE.get(code, 400)
        # Extra safe fields (e.g. current_controller on control_lease_lost).
        self.extra: dict[str, object] = dict(extra)
        super().__init__(f"{code}: {detail}" if detail else code)

    def as_response(self) -> dict[str, object]:
        body: dict[str, object] = {"error": self.code}
        if self.detail:
            body["detail"] = self.detail
        body.update(self.extra)
        return body
