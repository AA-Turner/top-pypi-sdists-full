"""What an auth step returns, free of any generated type."""

from __future__ import annotations

# Python internals
from dataclasses import dataclass, field


@dataclass(frozen=True)
class DeviceFlowStart:
    """What the auth service hands back to begin a device-code login.

    Attributes:
        device_code: Identifies this attempt when polling, and to ``--resume``.
        user_code: The short code the human types into the browser.
        verification_uri: Where they type it.
        verification_uri_complete: The same page with the code prefilled.
        interval: Seconds the service asks callers to wait between polls.
    """

    device_code: str
    user_code: str
    verification_uri: str
    verification_uri_complete: str
    interval: int


@dataclass(frozen=True)
class Tokens:
    """A completed login.

    Attributes:
        access_token: The JWT to present to the platform.
        refresh_token: Exchanged for a new pair when the JWT expires.
    """

    access_token: str
    refresh_token: str


@dataclass(frozen=True)
class Pending:
    """Nobody has approved the device code yet; poll again.

    A protocol state rather than a failure, so it is returned rather than
    raised: only the caller knows how long to keep waiting.
    """


@dataclass(frozen=True)
class TokenClaims:
    """The claims read off an access token.

    Decoded, not verified: the platform verifies signatures, and a client that
    rejected its own token would only strand the caller. Read these to decide
    when to refresh, never to decide what the caller may do.

    Attributes:
        email: The caller's email.
        user_id: The ``sub`` claim.
        expires_at: The ``exp`` claim as a unix timestamp, or ``None``.
        feature_flags: Flags the platform enabled for this caller.
    """

    email: str
    user_id: str
    expires_at: int | None
    feature_flags: tuple[str, ...] = field(default=())
