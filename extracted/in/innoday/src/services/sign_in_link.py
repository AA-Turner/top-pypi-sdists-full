"""Emailing an existing user a sign-in link.

Extracted from ``src/routers/webui/routes.py`` so the API can offer it too. The
Next.js UI replacing ``/ui`` is an API client and holds no database connection,
so it cannot do any of this for itself -- and the parts it cannot do are the
parts that matter:

**The address is checked against InnoDay's own users table before Supabase is
called at all.** The admin endpoint that sends the link creates an ``auth.users``
row for an address it does not recognise rather than refusing, so handing it
unvalidated input from a public form would let a stranger provision an identity
-- and then, by following the link, a mirror InnoDay user, since
``_user_from_supabase_jwt`` creates one on first sight. Our own table is the
allowlist, and checking it costs one indexed lookup.

**Every outcome renders the same answer.** Unknown address, throttled, upstream
failure, invite fallback -- all report ``sent``. Any difference between them is
an oracle for which addresses have accounts.
"""

import logging
import time
from typing import Dict, Optional

from sqlmodel import Session, func, select

from src.domain.user import User
from src.services.supabase_invite import (
    MagicLinkResult,
    magic_link_configured,
    send_magic_link,
)
from src.services.user_provisioning import resend_invite

logger = logging.getLogger(__name__)

COOLDOWN_SECONDS = 60
TRACKING_LIMIT = 1024

# In-process, therefore per worker -- a floor, not a guarantee. It exists because
# this route sends email on an unauthenticated POST, and email is a finite,
# shared, per-project resource: an unthrottled send is a way to burn the whole
# team's front door.
_last_request: Dict[str, float] = {}


def _throttled(address: str) -> bool:
    """Whether this address asked too recently. Records the attempt if not."""
    now = time.monotonic()
    last = _last_request.get(address)
    if last is not None and now - last < COOLDOWN_SECONDS:
        return True

    # Without this the dict grows one key per distinct address forever, and the
    # route is reachable by anyone -- so "distinct addresses seen" would be
    # attacker-controlled.
    if len(_last_request) > TRACKING_LIMIT:
        for stale in [
            a for a, t in _last_request.items() if now - t >= COOLDOWN_SECONDS
        ]:
            del _last_request[stale]

    _last_request[address] = now
    return False


def looks_unconfirmed(result: MagicLinkResult) -> bool:
    """Whether a failed magic link means "never confirmed" rather than "broken".

    GoTrue reports it as ``422 signup_disabled``, which reads like a
    misconfiguration and is really "this person has an identity and never clicked
    their link". Matched on the error text as well as the status, because the
    status alone is reused for other validation failures and re-inviting on one
    of those would email somebody for no reason.
    """
    if result.configured is False:
        return False
    text = (result.error or "").lower()
    return result.status_code == 422 and "signup" in text


def request_sign_in_link(
    session: Session, *, email: str, redirect_to: str
) -> Optional[str]:
    """Email ``email`` a sign-in link if it belongs to a known user.

    Returns ``None`` when the deployment can send at all, and a reason string when
    it cannot. **The return value never distinguishes one address from another** --
    only "this deployment has no identity provider", which is true for everyone.
    """
    if not magic_link_configured():
        return "not_configured"

    address = (email or "").strip().lower()
    if not address:
        return "missing_email"

    if _throttled(address):
        return None

    known = session.exec(select(User).where(func.lower(User.email) == address)).first()
    if known is None:
        # Signing up is invite-only (src/routers/invites.py), and this route must
        # never be the thing that creates an account.
        logger.info("sign-in link requested for an unknown address")
        return None

    result = send_magic_link(address, redirect_to=redirect_to)

    # The dead end this exists to remove: `/auth/v1/otp` cannot reach someone whose
    # identity exists but was never confirmed. With `[auth] enable_signup = false`
    # GoTrue routes their magic link through its *signup* path and answers
    # `422 signup_disabled`. Without this fallback the page still said "check your
    # email" and no email ever came -- so from their side the platform was
    # silently, permanently broken. `resend_invite` is the admin path, which works
    # with signup disabled, and it only runs for an address already matched against
    # our own users table, so it cannot provision anyone.
    if not result.sent and looks_unconfirmed(result):
        logger.info("sign-in fell back to a fresh invite for a known user")
        error = resend_invite(address)
        if error:
            logger.warning("sign-in invite fallback failed: %s", error)
    elif not result.sent:
        # Logged, not shown. A silent failure here is exactly how a login page can
        # be broken for everyone while looking like it works, so it must reach the
        # operator.
        logger.warning(
            "sign-in link not sent (configured=%s status=%s error=%s)",
            result.configured,
            result.status_code,
            result.error,
        )

    return None
