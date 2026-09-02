"""CLI access token domain model (auth P1, PF-350).

A durable, revocable replacement for the in-memory ``api_keys_store`` that
previously lived in ``src/routers/auth.py``. Each row is a long-lived opaque
token minted for a user (via the device flow in P2, or the non-device
``POST /auth/tokens`` path). The raw token is shown to the caller exactly once;
only its SHA-256 hash is stored, so a database leak never exposes usable
credentials. Revocation is a server-side flag (``revoked_at``), so a stolen
laptop's token can be killed without rotating anything else.

Token format (GitHub-style, ``<kind><orghash>.<secret>``)::

    idt_a1b2c.<32 random bytes>   personal access token (PAT)
    ido_a1b2c.<32 random bytes>   OAuth / device-login token
    idr_a1b2c.<32 random bytes>   refresh token (prefix RESERVED — nothing mints one yet)
    innoday_<32 random bytes>     legacy (no longer minted; still accepted)

The kind prefix lets a reader tell what a token is at a glance, and keeps CLI
tokens distinguishable from a Supabase JWT (which has no such prefix) in the
``Authorization`` header. The middle segment is a 5-char hash of the owning
org's **alias** (``plat0`` sentinel for cross-org/platform tokens or when the
minting user has no default org).

IMPORTANT — the org segment and the identity behind a token are *informational
only*. Authorization always flows through the ``cli_tokens`` row found by
hashing the full presented string (``token_hash``) → ``user_id`` → the user's
memberships / platform bypass. The org segment is never parsed or trusted for
authz; editing it just yields a string whose hash isn't on file, so it fails
lookup. The whole raw string (prefix + org segment included) is what gets
SHA-256'd and stored.
"""

import hashlib
import secrets
from datetime import datetime, timezone
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import JSON
from sqlmodel import Column, Field, Relationship

from src.domain._base import TimestampMixin

if TYPE_CHECKING:
    from src.domain.user import User

# Typed raw-token prefixes (GitHub-style). The kind prefix precedes a 5-char
# org-alias hash and a "." separator; see the module docstring for the layout.
CLI_TOKEN_PREFIX_PAT = (
    "idt_"  # personal access token (POST /auth/tokens, bootstrap seed)
)
CLI_TOKEN_PREFIX_OAUTH = "ido_"  # OAuth / device-login token
CLI_TOKEN_PREFIX_REFRESH = "idr_"  # refresh token — RESERVED, nothing mints one yet
CLI_TOKEN_PREFIX_LEGACY = "innoday_"  # pre-typed tokens; accepted, never minted

# The resolver routes any Bearer value starting with one of these to the CLI
# -token path (vs. a Supabase JWT). Legacy included for backward compatibility.
CLI_TOKEN_PREFIXES = frozenset(
    {
        CLI_TOKEN_PREFIX_PAT,
        CLI_TOKEN_PREFIX_OAUTH,
        CLI_TOKEN_PREFIX_REFRESH,
        CLI_TOKEN_PREFIX_LEGACY,
    }
)

# Kind -> prefix, used by generate_cli_token. "pat" is the default.
_KIND_PREFIXES = {
    "pat": CLI_TOKEN_PREFIX_PAT,
    "oauth": CLI_TOKEN_PREFIX_OAUTH,
    "refresh": CLI_TOKEN_PREFIX_REFRESH,
}

# Sentinel org segment for cross-org/platform tokens (bootstrap-seeded platform
# users) and for a minting user with no resolvable default org.
PLAT_SENTINEL = "plat0"


def org_alias_hash(org_alias: Optional[str]) -> str:
    """Return the 5-char org segment for a token's owning org alias.

    A short, stable, slug-safe hash (first 5 hex chars of SHA-256) so the token
    string carries a hint of which org it belongs to. Collision-tolerant on
    purpose — it is a display/routing hint, never an identity check. Falsy
    alias (cross-org platform token, or no default org) → ``plat0`` sentinel.
    """
    if not org_alias:
        return PLAT_SENTINEL
    return hashlib.sha256(org_alias.encode()).hexdigest()[:5]


def generate_cli_token(kind: str = "pat", org_alias: Optional[str] = None) -> str:
    """Mint a new raw opaque CLI token. Shown to the caller once, never stored.

    ``kind`` selects the prefix ("pat" | "oauth" | "refresh"; defaults to a
    PAT). ``org_alias`` is hashed into the 5-char org segment (``plat0`` when
    absent). The secret body is 32 CSPRNG bytes — the user id is never encoded
    into it; identity is resolved via the stored hash.
    """
    prefix = _KIND_PREFIXES.get(kind)
    if prefix is None:
        raise ValueError(f"unknown CLI token kind: {kind!r}")
    return f"{prefix}{org_alias_hash(org_alias)}.{secrets.token_urlsafe(32)}"


def hash_cli_token(raw_token: str) -> str:
    """SHA-256 the raw token for at-rest storage and constant-time lookup."""
    return hashlib.sha256(raw_token.encode()).hexdigest()


class CLIToken(TimestampMixin, table=True):
    """A revocable, hashed CLI access token bound to a user."""

    __tablename__ = "cli_tokens"

    # The revocable token_id (what `innoday auth tokens --revoke <id>` targets).
    id: str = Field(default_factory=lambda: secrets.token_urlsafe(16), primary_key=True)
    user_id: str = Field(foreign_key="users.id", index=True)

    # SHA-256 of the raw token; the raw value is never persisted.
    token_hash: str = Field(index=True, max_length=64)

    # Human-friendly label, e.g. "karl's laptop", shown in `innoday auth tokens`.
    name: str = Field(default="cli", max_length=255)

    # Future-proofing for scoped tokens; defaults to full CLI access.
    # `nullable=False` is explicit because the `sa_column=` overrides SQLModel's
    # inference (see BoardCredential for the same trap): dev's column is NOT
    # NULL, so leaving it off made `create_all` accept a NULL that production
    # rejects. The default_factory means the ORM always supplies a value; this
    # closes the raw-SQL path.
    scopes: List[str] = Field(
        default_factory=lambda: ["cli"], sa_column=Column(JSON, nullable=False)
    )

    last_used_at: Optional[datetime] = Field(default=None)
    expires_at: Optional[datetime] = Field(default=None)
    revoked_at: Optional[datetime] = Field(default=None)

    # Relationship
    user: Optional["User"] = Relationship()

    def is_valid(self) -> bool:
        """True if the token is neither revoked nor expired."""
        if self.revoked_at is not None:
            return False
        if self.expires_at is not None:
            # expires_at may be naive (SQLite) or aware (Postgres); normalise.
            exp = self.expires_at
            if exp.tzinfo is None:
                exp = exp.replace(tzinfo=timezone.utc)
            if datetime.now(timezone.utc) > exp:
                return False
        return True

    def mark_used(self) -> None:
        """Stamp last_used_at (caller is responsible for committing)."""
        self.last_used_at = datetime.now(timezone.utc)

    def revoke(self) -> None:
        """Flag the token revoked (caller commits)."""
        self.revoked_at = datetime.now(timezone.utc)
