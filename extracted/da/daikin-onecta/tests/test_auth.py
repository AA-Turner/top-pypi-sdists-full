"""Tests for Daikin OAuth token helpers."""

import json
from base64 import urlsafe_b64encode

import pytest

from daikin_onecta import OnectaAccessTokenError, get_account_id


def _access_token(claims: object) -> str:
    """Create an unsigned JWT-shaped token for testing."""
    payload = urlsafe_b64encode(json.dumps(claims).encode()).decode().rstrip("=")
    return f"header.{payload}.signature"


def test_get_account_id() -> None:
    """Return the OAuth subject as the account ID."""
    assert get_account_id(_access_token({"sub": "account-id"})) == "account-id"


@pytest.mark.parametrize(
    "access_token",
    [
        "not-a-jwt",
        "header.not-json.signature",
        _access_token([]),
        _access_token({}),
        _access_token({"sub": ""}),
        _access_token({"sub": 1}),
    ],
)
def test_get_account_id_rejects_invalid_tokens(access_token: str) -> None:
    """Reject tokens without a valid account subject."""
    with pytest.raises(OnectaAccessTokenError):
        get_account_id(access_token)
