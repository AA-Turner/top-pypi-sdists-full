"""Browser session for the ``/ui`` pages: an HttpOnly cookie holding a CLI token.

The cookie carries a **minted InnoDay token**, not the Supabase JWT that
established the session. The JWT expires in roughly an hour and this app has no
refresh-token path (``idr_`` is reserved and nothing mints one), so a page whose
auth was the JWT would log you out mid-session. A ``CLIToken`` row is durable,
revocable, records ``last_used_at``, and is read by the same ``hash_cli_token``
lookup ``src.middleware.token_auth`` already uses for the ``Authorization``
header -- so this adds a second *carrier* for an existing credential, not a
second credential type.

Session rows are marked by ``SESSION_TOKEN_NAME`` so the dashboard's token table
can hide them: they are not CLI tokens a person chose to create, and listing them
would invite someone to revoke the session they are currently using. Revoking
*all* tokens still kills them, which is correct -- that is what it is for.
"""

from datetime import datetime, timezone
from typing import Optional

from fastapi import Request, Response
from sqlmodel import Session, select

from src.domain.cli_token import CLIToken, hash_cli_token
from src.domain.user import User
from src.page_paths import UI_PREFIX
from src.routers.auth import mint_cli_token

COOKIE_NAME = "innoday_session"

# Marks a token minted for a browser rather than chosen by a person. Also the
# filter the dashboard's token list applies -- keep the two in step.
SESSION_TOKEN_NAME = "web-session"

SESSION_DAYS = 7


def issue_session(
    response: Response,
    session: Session,
    user: User,
    *,
    secure: bool = True,
) -> str:
    """Mint a session token for ``user`` and set it as an HttpOnly cookie.

    Returns the raw token (for tests; the caller has no other use for it).
    ``secure=False`` is only for local http:// development -- a Secure cookie is
    never sent over plain http, so the session would silently never establish.
    """
    row, raw_token = mint_cli_token(
        session,
        user_id=user.id,
        name=SESSION_TOKEN_NAME,
        expires_days=SESSION_DAYS,
        kind="oauth",
    )
    response.set_cookie(
        COOKIE_NAME,
        raw_token,
        max_age=SESSION_DAYS * 24 * 60 * 60,
        httponly=True,
        secure=secure,
        samesite="lax",
        path=UI_PREFIX,
    )
    return raw_token


def clear_session(response: Response) -> None:
    """Remove the session cookie. Must repeat ``path`` or the browser keeps it."""
    response.delete_cookie(COOKIE_NAME, path=UI_PREFIX)


def revoke_session(session: Session, raw_token: str) -> None:
    """Revoke the ``cli_tokens`` row behind a raw session token, if it exists."""
    row = session.exec(
        select(CLIToken).where(CLIToken.token_hash == hash_cli_token(raw_token))
    ).first()
    if row and row.revoked_at is None:
        row.revoked_at = datetime.now(timezone.utc)
        session.add(row)
        session.commit()


def user_from_request(request: Request, session: Session) -> Optional[User]:
    """Resolve the signed-in user from the session cookie, or ``None``.

    Returns ``None`` for every failure mode -- absent, unknown, revoked or
    expired -- because the caller's response is the same in all four cases: send
    them to the sign-in page. Distinguishing them would only tell an attacker
    which guessed cookie values are real tokens.
    """
    raw_token = request.cookies.get(COOKIE_NAME)
    if not raw_token:
        return None

    row = session.exec(
        select(CLIToken).where(CLIToken.token_hash == hash_cli_token(raw_token))
    ).first()
    if not row or row.revoked_at is not None:
        return None

    if row.expires_at is not None:
        expires_at = row.expires_at
        # SQLite hands back naive datetimes; Postgres timezone-aware ones. Compare
        # in UTC either way rather than letting the naive case raise.
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)
        if expires_at <= datetime.now(timezone.utc):
            return None

    user = session.get(User, row.user_id)
    if not user:
        return None

    row.last_used_at = datetime.now(timezone.utc)
    session.add(row)
    session.commit()
    return user
