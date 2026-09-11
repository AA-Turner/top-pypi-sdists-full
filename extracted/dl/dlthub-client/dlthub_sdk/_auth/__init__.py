"""Talking to the auth service.

Private to the SDK: the CLI drives these steps and owns everything a human sees
— the polling loop, the prompts, the browser, and where a token is stored.
"""

# Current package
from dlthub_sdk._auth.pkce import Pkce, generate_pkce
from dlthub_sdk._auth.tokens import EXPIRY_MARGIN_SECONDS, decode_token, is_expiring
from dlthub_sdk._auth.transport import AuthTransport
from dlthub_sdk._auth.types import DeviceFlowStart, Pending, TokenClaims, Tokens

__all__ = [
    "EXPIRY_MARGIN_SECONDS",
    "AuthTransport",
    "DeviceFlowStart",
    "Pending",
    "Pkce",
    "TokenClaims",
    "Tokens",
    "decode_token",
    "generate_pkce",
    "is_expiring",
]
