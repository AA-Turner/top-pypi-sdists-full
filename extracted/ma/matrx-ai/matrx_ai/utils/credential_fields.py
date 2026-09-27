"""Credential-shaped FIELDS are never written into a durable record.

A request's metadata travels as one dict and is persisted wholesale — and it
carries live credentials. Measured 2026-09-26: 653 ``chat.user_request`` rows since
2026-07-25 held ``metadata.active_sandbox.access_token``, a sandbox bearer token,
in plain text. :func:`without_credential_fields` is the one filter every durable
write of such a dict goes through.

Matching is by NAME SEGMENT, deliberately narrower than a secret scanner's: a
record's metadata legitimately carries ``mandate_key``, ``setting_key``, thinking
``signature`` and ``max_output_tokens``, and stripping those corrupts the record.
"""

from __future__ import annotations

import re
from typing import Any

#: A field is a credential when one of its name segments is one of these.
_SECRET_SEGMENTS = frozenset(
    {
        "TOKEN",
        "SECRET",
        "SECRETS",
        "PASSWORD",
        "PASSWORDS",
        "PASSWD",
        "PWD",
        "BEARER",
        "CREDENTIAL",
        "CREDENTIALS",
        "COOKIE",
        "COOKIES",
    }
)

#: ...or its whole name is one of these (segments that are harmless alone).
_SECRET_NAMES = frozenset(
    {
        "APIKEY",
        "API_KEY",
        "AUTHORIZATION",
        "PRIVATE_KEY",
        "ACCESS_KEY",
        "SECRET_KEY",
        "CLIENT_SECRET",
        "X_API_KEY",
    }
)

#: A name ending in one of these DESCRIBES a credential rather than holding one
#: (``token_count``, ``token_type``, ``token_expires``, ``token_url``).
_DESCRIPTIVE_TAILS = frozenset(
    {
        "COUNT",
        "COUNTS",
        "LIMIT",
        "LIMITS",
        "BUDGET",
        "USAGE",
        "TYPE",
        "KIND",
        "EXPIRES",
        "EXPIRY",
        "TTL",
        "URL",
        "URI",
        "ENDPOINT",
        "ID",
        "PRESENT",
        "SET",
    }
)

_SPLIT = re.compile(r"[^A-Za-z0-9]+")
_CAMEL = re.compile(r"(?<=[a-z0-9])(?=[A-Z])")


def _segments(name: str) -> list[str]:
    out: list[str] = []
    for raw in _SPLIT.split(name):
        out.extend(p.upper() for p in _CAMEL.split(raw) if p)
    return out


def is_credential_field(name: str) -> bool:
    """True when a field of this name holds a credential."""
    segments = _segments(name)
    if not segments:
        return False
    if "_".join(segments) in _SECRET_NAMES or "".join(segments) in _SECRET_NAMES:
        return True
    if segments[-1] in _DESCRIPTIVE_TAILS:
        return False
    return any(segment in _SECRET_SEGMENTS for segment in segments)


#: Names that ARE credentials whatever their value looks like.
_ALWAYS_SECRET = frozenset(
    {
        "ACCESS_TOKEN",
        "REFRESH_TOKEN",
        "ID_TOKEN",
        "AUTH_TOKEN",
        "SESSION_TOKEN",
        "BEARER_TOKEN",
        "TOKEN",
        "BEARER",
        "PASSWORD",
        "PASSWD",
        "PWD",
        "SECRET",
        "COOKIE",
    }
    | _SECRET_NAMES
)


def _drop(key: str, item: Any) -> bool:
    """Drop a field that IS a credential: an unmistakable credential name, or a
    credential-shaped name holding a value the secret scanner recognizes.

    A credential-shaped name alone is not enough — ``run_claim_token`` (an
    ownership marker the claim renewal reads back), ``next_page_token`` and
    ``credential_login`` are ordinary fields a durable record must keep.
    """
    if not is_credential_field(key):
        return False
    segments = _segments(key)
    if "_".join(segments) in _ALWAYS_SECRET or "".join(segments) in _ALWAYS_SECRET:
        return True
    if isinstance(item, str) and item:
        from matrx_utils.secret_detection import find_secrets

        return bool(find_secrets(item))
    return False


def without_credential_fields(value: Any) -> Any:
    """A copy of ``value`` with every credential field removed, at any depth."""
    if isinstance(value, dict):
        return {
            key: without_credential_fields(item)
            for key, item in value.items()
            if not (isinstance(key, str) and _drop(key, item))
        }
    if isinstance(value, list):
        return [without_credential_fields(item) for item in value]
    return value


__all__ = ["is_credential_field", "without_credential_fields"]
