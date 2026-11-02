"""OAuth token helpers for Daikin Onecta."""

import json
from base64 import urlsafe_b64decode
from binascii import Error as BinasciiError
from typing import Any

from .exceptions import OnectaAccessTokenError


def get_account_id(access_token: str) -> str:
    """Return the account ID from an unverified Daikin OAuth access token.

    The token subject is used only as a stable account identifier. Token
    validation remains the responsibility of the OAuth provider and API.
    """
    try:
        _header, payload, _signature = access_token.split(".")
        padded_payload = payload + "=" * (-len(payload) % 4)
        claims: Any = json.loads(urlsafe_b64decode(padded_payload))
        account_id = claims["sub"]
    except (
        BinasciiError,
        UnicodeDecodeError,
        ValueError,
        TypeError,
        KeyError,
        json.JSONDecodeError,
    ) as err:
        raise OnectaAccessTokenError("Daikin Onecta access token is invalid") from err

    if not isinstance(account_id, str) or not account_id:
        raise OnectaAccessTokenError("Daikin Onecta access token is missing an account ID")

    return account_id
