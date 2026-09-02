"""Device authorization grants for the CLI OAuth device flow (auth P2, PF-350).

Implements the pending-grant side of RFC 8628 (OAuth 2.0 Device Authorization
Grant), the machinery behind ``innoday login``:

  1. CLI calls ``POST /device/code`` → a row is created here (PENDING) with a
     ``device_code`` (polled by the CLI) and a short human ``user_code``.
  2. A human opens the verification page, enters the ``user_code``, and approves;
     ``POST /device/approve`` binds this row to their InnoDay user and flips it
     APPROVED.
  3. CLI polls ``POST /device/token`` with the ``device_code``; on APPROVAL the
     backend mints a ``cli_tokens`` row and returns the ``ido_`` (device-login)
     token.

Like CLI tokens, the ``device_code`` is stored only as its SHA-256 hash; the
raw value lives only in the CLI's memory while it polls. The ``user_code`` is
low-entropy by design (a human types it) and short-lived, so it is stored plain
for lookup on the approval page.
"""

import hashlib
import secrets
from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Optional

from sqlalchemy import Column
from sqlalchemy import Enum as SAEnum
from sqlmodel import Field

from src.domain._base import TimestampMixin

# Human-typed code alphabet: no ambiguous chars (0/O, 1/I/L).
_USER_CODE_ALPHABET = "ABCDEFGHJKMNPQRSTUVWXYZ23456789"
DEFAULT_DEVICE_CODE_TTL_SECONDS = 900  # 15 minutes
DEFAULT_POLL_INTERVAL_SECONDS = 5


class DeviceAuthStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    DENIED = "DENIED"
    EXPIRED = "EXPIRED"


def generate_device_code() -> str:
    """The high-entropy secret the CLI polls with (never shown to a human)."""
    return secrets.token_urlsafe(32)


def hash_device_code(raw: str) -> str:
    return hashlib.sha256(raw.encode()).hexdigest()


def generate_user_code() -> str:
    """A short, human-typeable code, e.g. ``WDJB-MJHT``."""
    chars = "".join(secrets.choice(_USER_CODE_ALPHABET) for _ in range(8))
    return f"{chars[:4]}-{chars[4:]}"


class DeviceAuthorization(TimestampMixin, table=True):
    """A pending/approved device-flow grant (RFC 8628)."""

    __tablename__ = "device_authorizations"

    id: str = Field(default_factory=lambda: secrets.token_urlsafe(16), primary_key=True)
    device_code_hash: str = Field(index=True, max_length=64)
    user_code: str = Field(index=True, max_length=16)

    # VARCHAR(20), not a native Postgres enum -- that is what the migration
    # built. `native_enum=False` keeps the Python-side coercion while storing
    # a plain string, so adding a status needs no `ALTER TYPE`.
    status: DeviceAuthStatus = Field(
        default=DeviceAuthStatus.PENDING,
        sa_column=Column(
            SAEnum(DeviceAuthStatus, native_enum=False, length=20),
            nullable=False,
        ),
    )
    # Set when a human approves the grant.
    user_id: Optional[str] = Field(default=None, foreign_key="users.id")

    interval_seconds: int = Field(default=DEFAULT_POLL_INTERVAL_SECONDS)
    expires_at: datetime = Field(
        default_factory=lambda: (
            datetime.now(timezone.utc)
            + timedelta(seconds=DEFAULT_DEVICE_CODE_TTL_SECONDS)
        )
    )

    def is_expired(self) -> bool:
        exp = self.expires_at
        if exp.tzinfo is None:
            exp = exp.replace(tzinfo=timezone.utc)
        return datetime.now(timezone.utc) > exp

    def approve(self, user_id: str) -> None:
        self.status = DeviceAuthStatus.APPROVED
        self.user_id = user_id
        self.touch()

    def deny(self) -> None:
        self.status = DeviceAuthStatus.DENIED
        self.touch()
