"""First-platform-user bootstrap (auth P1, PF-350, §5.0).

The very first people on the platform are **platform users**, and they exist
before the device-flow hosted page or any Supabase invite machinery is live.
They are seeded with a bootstrap CLI token — the same escape hatch CI uses —
handed out out-of-band. Setting ``INNODAY_TOKEN=idt_plat0...`` in the client
environment then makes every CLI/MCP call authenticate as that user (the CLI
sends it as ``Authorization: Bearer``), with no browser login. The token is a
PAT (``idt_``) with the cross-org ``plat0`` sentinel — platform users span all
orgs, so there is no single org to hash into the token.

``seed_platform_user`` is the operator action behind that: it creates (or
reuses) a ``users`` row with ``is_platform_member=True`` and mints one
``cli_tokens`` row, returning the raw token exactly once. No membership rows
are created — platform access is the ``is_platform_member`` bypass (rbac.py),
so a platform user reaches every org without enumeration.
"""

import logging
import os
from dataclasses import dataclass
from typing import Optional

from sqlmodel import Session, select

from src.domain.cli_token import CLIToken, generate_cli_token, hash_cli_token
from src.domain.user import User
from src.page_paths import AUTH_CALLBACK_PATH
from src.services.supabase_invite import send_supabase_invite


@dataclass
class SeededPlatformUser:
    user: User
    raw_token: str  # shown once; only the hash is persisted
    token_id: str
    created_user: bool  # True if the users row was created, False if reused


logger = logging.getLogger(__name__)


def seed_platform_user(
    session: Session,
    email: str,
    full_name: Optional[str] = None,
    token_name: str = "bootstrap",
) -> SeededPlatformUser:
    """Create/promote a platform user and mint a bootstrap CLI token.

    Idempotent on the user: if a user with ``email`` already exists it is
    promoted to platform member (rather than duplicated), and a fresh token is
    minted for it. The raw token is returned once and never stored.
    """
    user = session.exec(select(User).where(User.email == email)).first()
    created_user = False
    if user is None:
        # Best-effort Supabase invite so the seeded user gets a real auth
        # identity and can verify their address. Unlike POST /users this path
        # must keep working with no Supabase configured -- it is the break-glass
        # bootstrap, gated on DB credentials -- so a failure warns rather than
        # aborts. The user is still usable via their CLI token until
        # REQUIRE_VERIFIED_EMAIL is switched on.
        supabase_user_id = None
        invite = send_supabase_invite(
            email=email,
            redirect_to=f"{os.getenv('APP_URL', '').rstrip('/')}{AUTH_CALLBACK_PATH}",
            metadata={"full_name": full_name or email.split("@")[0]},
        )
        if invite.supabase_invite_id:
            supabase_user_id = invite.supabase_invite_id
        else:
            logger.warning(
                "Seeded %s without a Supabase auth identity (%s). They cannot "
                "sign in via the IdP and will be blocked once "
                "REQUIRE_VERIFIED_EMAIL is enabled -- invite them before then.",
                email,
                invite.error or "Supabase admin not configured",
            )

        user = User(
            email=email,
            full_name=full_name or email.split("@")[0],
            is_platform_member=True,
            supabase_user_id=supabase_user_id,
        )
        session.add(user)
        created_user = True
    elif not user.is_platform_member:
        user.promote_to_platform_member()
        session.add(user)

    session.commit()
    session.refresh(user)

    # Platform users are cross-org → PAT with the plat0 sentinel org segment.
    raw_token = generate_cli_token(kind="pat", org_alias=None)
    token = CLIToken(
        user_id=user.id,
        token_hash=hash_cli_token(raw_token),
        name=token_name,
        scopes=["cli"],
    )
    session.add(token)
    session.commit()
    session.refresh(token)

    return SeededPlatformUser(
        user=user,
        raw_token=raw_token,
        token_id=token.id,
        created_user=created_user,
    )
