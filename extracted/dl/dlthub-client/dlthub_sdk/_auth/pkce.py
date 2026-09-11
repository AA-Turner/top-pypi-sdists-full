"""PKCE material for the authorization-code flow."""

from __future__ import annotations

# Python internals
import base64
import hashlib
import secrets
from dataclasses import dataclass


@dataclass(frozen=True)
class Pkce:
    """One authorization-code attempt's proof material.

    Attributes:
        verifier: Held locally and presented at exchange.
        challenge: Sent when starting the flow, an S256 digest of the verifier.
        state: Echoed back through the callback, tying it to this attempt.
    """

    verifier: str
    challenge: str
    state: str


def generate_pkce() -> Pkce:
    """Generate a fresh verifier, its S256 challenge, and a state value.

    Returns:
        Material for one login attempt; never reuse it across attempts.
    """
    verifier = secrets.token_urlsafe(64)
    digest = hashlib.sha256(verifier.encode("ascii")).digest()
    challenge = base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")
    return Pkce(verifier=verifier, challenge=challenge, state=secrets.token_urlsafe(32))
