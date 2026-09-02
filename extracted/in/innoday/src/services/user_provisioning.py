"""Create a user who can actually sign in.

The ordering here is the whole point, and it is not obvious: **the Supabase
identity is provisioned first, and a failure to provision refuses the whole
operation**. A ``users`` row without a matching ``auth.users`` identity looks
completely healthy -- it has an email, it can hold CLI tokens, it passes every
check -- and is permanently unable to log in. Eight users ended up in exactly
that state before anyone noticed, which is what
``scripts/backfill_supabase_identities.py`` exists to repair.

Extracted from ``POST /api/v1/users`` so the signup-approval path cannot drift
from it. Two implementations of "make a user" is how you get one that forgets
the identity.
"""

import logging
import os
from dataclasses import dataclass
from typing import Optional

from sqlmodel import Session, select

from src.domain.user import User, UserRole
from src.page_paths import AUTH_CALLBACK_PATH
from src.services.supabase_invite import send_supabase_invite

logger = logging.getLogger(__name__)


class UserProvisioningError(Exception):
    """Provisioning failed. ``reason`` distinguishes the caller's response.

    ``not_configured`` is an operator problem (503); ``upstream`` is Supabase
    refusing or unreachable (502); ``duplicate`` is a conflict (409). Callers
    map these to status codes -- this layer does not import FastAPI.
    """

    def __init__(self, reason: str, message: str):
        super().__init__(message)
        self.reason = reason


@dataclass
class ProvisionedUser:
    user: User
    supabase_user_id: Optional[str]


def invite_redirect_url() -> str:
    """Where the invite email's link should land."""
    return f"{os.getenv('APP_URL', '').rstrip('/')}{AUTH_CALLBACK_PATH}"


def provision_user(
    session: Session,
    *,
    email: str,
    full_name: str,
    role: UserRole = UserRole.MEMBER,
    is_platform_member: bool = False,
    **extra,
) -> ProvisionedUser:
    """Provision the auth identity, then create the user linked to it.

    Commits. Raises ``UserProvisioningError`` rather than leaving a half-made
    account behind: an identity-less user row is worse than no row, because it
    reads as a working account to everything that inspects it.
    """
    email = email.strip().lower()

    if session.exec(select(User).where(User.email == email)).first():
        raise UserProvisioningError("duplicate", "Email already registered")

    invite = send_supabase_invite(
        email=email,
        redirect_to=invite_redirect_url(),
        metadata={"full_name": full_name},
    )
    if not invite.configured:
        raise UserProvisioningError(
            "not_configured",
            "Supabase admin is not configured (SUPABASE_URL / "
            "SUPABASE_SERVICE_KEY), so no auth identity can be created. "
            "Refusing to create a user who could never sign in.",
        )
    if invite.error:
        raise UserProvisioningError(
            "upstream", f"Supabase invite failed: {invite.error}"
        )

    user = User(
        email=email,
        full_name=full_name,
        role=role,
        is_platform_member=is_platform_member,
        supabase_user_id=invite.supabase_invite_id,
        **extra,
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    # email_verified_at stays NULL: the invite email is what verifies the
    # address, and it has only just been sent.
    logger.info(
        "provisioned user %s (%s) with Supabase identity %s; awaiting verification",
        user.id,
        user.email,
        user.supabase_user_id,
    )
    return ProvisionedUser(user=user, supabase_user_id=invite.supabase_invite_id)


def resend_invite(email: str) -> Optional[str]:
    """Email a fresh invite to an address that already has an identity.

    This is the only path that reaches someone whose identity exists but was
    never confirmed. ``/auth/v1/otp`` -- what the sign-in page uses -- cannot:
    with ``[auth] enable_signup = false`` GoTrue routes an unconfirmed user's
    magic link through its *signup* path and answers ``422 signup_disabled``. The
    sign-in page still renders "check your email", so from the person's side the
    platform is simply broken, silently, forever. Three people sat in that state.

    Returns an error string, or ``None`` on success.
    """
    result = send_supabase_invite(email, redirect_to=invite_redirect_url())
    if not result.configured:
        return "Supabase admin is not configured"
    return result.error
