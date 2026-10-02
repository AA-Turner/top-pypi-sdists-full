"""Hand-written auth helpers for the Istari Digital Python client."""

from istari_digital_client.legacy.auth.keys import (
    GeneratedClientCredentials,
    generate_client_keypair,
)
from istari_digital_client.legacy.auth.identity_service import (
    IdentityServiceClient,
    IdentityServiceError,
    RetryPolicy,
    validate_credentials_file,
    validate_inline_credentials,
)
from istari_digital_client.legacy.auth.key_exchange import (
    ExchangePatError,
    ExchangePatResult,
    PrincipalKind,
    exchange_pat,
    generate_keypair_and_exchange,
)
from istari_digital_client.legacy.auth.key_registration import (
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
    "GeneratedClientCredentials",
    "generate_client_keypair",
    "IdentityServiceClient",
    "IdentityServiceError",
    "RetryPolicy",
    "validate_credentials_file",
    "validate_inline_credentials",
    "ExchangePatError",
    "ExchangePatResult",
    "PrincipalKind",
    "exchange_pat",
    "generate_keypair_and_exchange",
    "KeyMetadata",
    "KeyRegistrationError",
    "PrincipalKeys",
    "RegisterKeyResult",
    "generate_keypair_and_register",
    "get_key",
    "list_keys",
    "register_key",
    "revoke_key",
]
