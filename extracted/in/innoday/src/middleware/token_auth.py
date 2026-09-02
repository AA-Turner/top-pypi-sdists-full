"""Unified request authentication resolver (auth P1, PF-350).

A single function, ``resolve_user_from_request``, replaces the old
trust-the-``X-User-ID``-header behaviour. It tries identity sources in order:

  1. ``Authorization: Bearer idt_...`` / ``ido_...`` / ``idr_...`` / legacy
     ``innoday_...`` → CLI token: SHA-256 hash lookup in ``cli_tokens``;
     valid/unexpired/unrevoked → its user. Stamps ``last_used_at``. The token's
     org segment is never parsed here — identity comes only from the hashed row.
  2. ``Authorization: Bearer <JWT>``        → Supabase JWT: verify via JWKS
     (``src.services.supabase_auth``), read ``sub`` → map to
     ``users.supabase_user_id``, lazily creating the mirror ``users`` row on
     first sight.
(A third path once trusted an ``X-User-ID`` header verbatim, so any caller past
the API gate could name any user id and be treated as them. It is **removed** —
identity now comes only from a token.)

**``X-Team-Secret`` is not an identity mechanism and is not part of path 3.** It
is an API *door key* — ``TeamSecretMiddleware`` compares a header against the
``TEAM_ACCESS_SECRET`` env var and calls ``next()``; it resolves no user, no org,
and never touches the database. It can stay indefinitely. Naming path 3
"X-Team-Secret + X-User-ID" (as this docstring used to) conflated the two and led
to the mistaken belief that retiring the door key was coupled to auth or to RLS.

**Neither path is related to Postgres RLS.** Authorization is enforced here and in
``rbac.py``, in Python. Nothing in this module propagates the caller's identity to
Postgres (no ``SET LOCAL``, no ``set_config``), and the app connects as a role with
``rolbypassrls=true``, so database policies never evaluate. Making RLS real is a
separate project — see the "Who can access what" section of CLAUDE.md.

``INNODAY_TOKEN`` in the *server* env is NOT consulted here — that variable is
a *client-side* bypass (the CLI sends it as a Bearer token, so it arrives via
path 1). See ``src.services.bootstrap`` for seeding the first platform users.

``rbac.get_current_user`` delegates to this so every endpoint picks up
Bearer-token auth without per-router changes.
"""

import os
from typing import Optional

from fastapi import Request
from sqlmodel import Session, select

from src.domain.cli_token import CLI_TOKEN_PREFIXES, CLIToken, hash_cli_token
from src.domain.user import User
from src.services.supabase_auth import (
    SupabaseAuthError,
    extract_identity,
    supabase_auth_configured,
    verify_supabase_jwt,
)


class UnverifiedEmailError(Exception):
    """A valid credential whose user has never verified their email address.

    Distinct from "no/invalid credential" so callers can return an actionable
    message ("check your email") rather than a generic 401 that looks like a bad
    token.
    """


def require_verified_email() -> bool:
    """Whether an unverified email blocks authentication.

    Defaults **off**. Every user predates the invite flow (`auth.users` is empty
    and no one has `email_verified_at`), so switching this on before people are
    invited would invalidate every live CLI token at once -- including the ones
    this repo's own tooling uses. Rollout: ship the column and this flag off ->
    invite/verify everyone -> set REQUIRE_VERIFIED_EMAIL=true.
    """
    raw = os.getenv("REQUIRE_VERIFIED_EMAIL", "false").strip().lower()
    return raw in ("1", "true", "yes", "on")


def _assert_email_verified(user: User) -> None:
    """Raise if enforcement is on and this user's email was never verified."""
    if require_verified_email() and not user.email_verified:
        raise UnverifiedEmailError(
            f"The email address for {user.email} has not been verified. "
            "Accept the invite emailed to you, then retry."
        )


def _bearer_token(request: Request) -> Optional[str]:
    # Starlette's request.headers is case-insensitive, so one lookup suffices.
    header = request.headers.get("Authorization")
    if not header or not header.startswith("Bearer "):
        return None
    return header[len("Bearer ") :].strip() or None


def _user_from_cli_token(raw_token: str, session: Session) -> Optional[User]:
    """Path 1: look up a prefixed opaque CLI token by its hash.

    Prefix-agnostic: the full presented string (prefix + org segment + secret)
    is hashed and matched against ``token_hash``. The org segment is neither
    parsed nor trusted — it is informational only.
    """
    token_hash = hash_cli_token(raw_token)
    row = session.exec(
        select(CLIToken).where(CLIToken.token_hash == token_hash)
    ).first()
    if not row or not row.is_valid():
        return None
    user = session.exec(select(User).where(User.id == row.user_id)).first()
    if not user:
        return None
    _assert_email_verified(user)
    row.mark_used()
    session.add(row)
    session.commit()
    return user


def _user_from_supabase_jwt(raw_token: str, session: Session) -> Optional[User]:
    """Path 2: verify a Supabase JWT and lazily mirror the user."""
    if not supabase_auth_configured():
        return None
    try:
        claims = verify_supabase_jwt(raw_token)
    except SupabaseAuthError:
        return None

    identity = extract_identity(claims)
    sub = identity.get("supabase_user_id")
    if not sub:
        return None

    confirmed = identity.get("email_confirmed_at")

    # Already linked?
    user = session.exec(select(User).where(User.supabase_user_id == sub)).first()
    if user:
        if confirmed:
            # The IdP is the source of truth; mirror its confirmation locally so
            # the CLI-token path can gate on it without a round-trip.
            user.mark_email_verified()
            session.add(user)
            session.commit()
        _assert_email_verified(user)
        return user

    email = identity.get("email")
    # Link an existing header-era row by email, if present (lazy migration).
    if email:
        user = session.exec(select(User).where(User.email == email)).first()
        if user:
            user.supabase_user_id = sub
            if confirmed:
                user.mark_email_verified()
            user.update_last_login()
            session.add(user)
            session.commit()
            session.refresh(user)
            _assert_email_verified(user)
            return user

    # Otherwise create the mirror row (invite-accept normally does this first;
    # this covers a first login via an already-provisioned Supabase user).
    if not email:
        return None
    user = User(
        email=email,
        full_name=identity.get("full_name") or email.split("@")[0],
        supabase_user_id=sub,
    )
    if confirmed:
        user.mark_email_verified()
    user.update_last_login()
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def resolve_user_from_request(request: Request, session: Session) -> Optional[User]:
    """Resolve the authenticated user, or None if no source succeeds."""
    raw_token = _bearer_token(request)
    if raw_token:
        if any(raw_token.startswith(p) for p in CLI_TOKEN_PREFIXES):
            user = _user_from_cli_token(raw_token, session)
            if user:
                return user
        else:
            user = _user_from_supabase_jwt(raw_token, session)
            if user:
                return user

    return None
