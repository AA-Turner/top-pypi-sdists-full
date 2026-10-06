"""Hand-written client for the identity-service key operations, born on the frozen /api/v1 routes. Deprecated.

The key-management functions use the v2 key routes when they can and v1 otherwise;
the PAT exchange has only v1. A call that reaches v1 warns once and names its
replacement under ``istari_digital_client.sdk._identity.v2`` or ``IstariAdmin.identity``.
"""

from istari_digital_client.sdk._identity.auth.identity_service import PrincipalKind
from istari_digital_client.sdk._identity.v1.key_exchange import (
    ExchangePatError,
    ExchangePatResult,
    exchange_pat,
    generate_keypair_and_exchange,
)
from istari_digital_client.sdk._identity.v1.key_registration import (
    KeyMetadata,
    KeyRegistrationError,
    PrincipalKeys,
    RegisterKeyResult,
    generate_keypair_and_register,
    get_key,
    list_keys,
    register_key,
    revoke_key,
)

__all__ = [
    "ExchangePatError",
    "ExchangePatResult",
    "KeyMetadata",
    "KeyRegistrationError",
    "PrincipalKeys",
    "PrincipalKind",
    "RegisterKeyResult",
    "exchange_pat",
    "generate_keypair_and_exchange",
    "generate_keypair_and_register",
    "get_key",
    "list_keys",
    "register_key",
    "revoke_key",
]
