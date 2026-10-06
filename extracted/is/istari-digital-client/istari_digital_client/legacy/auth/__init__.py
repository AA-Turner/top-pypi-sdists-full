"""Deprecated import path. Moved to ``istari_digital_client.identity.auth`` and
``istari_digital_client.identity.v1``; this shim warns and re-exports."""

import sys
import warnings

warnings.warn(
    "istari_digital_client.legacy.auth is deprecated; import from "
    "istari_digital_client.identity.auth (token client, keypairs) or "
    "istari_digital_client.identity.v1 (frozen /api/v1 operations)",
    DeprecationWarning,
    stacklevel=2,
)

from istari_digital_client.identity.auth import (  # noqa: E402
    GeneratedClientCredentials,
    IdentityServiceClient,
    IdentityServiceError,
    RetryPolicy,
    generate_client_keypair,
    validate_credentials_file,
    validate_inline_credentials,
)
from istari_digital_client.identity.auth import identity_service, keys  # noqa: E402
from istari_digital_client.identity.v1 import (  # noqa: E402
    ExchangePatError,
    ExchangePatResult,
    KeyMetadata,
    KeyRegistrationError,
    PrincipalKeys,
    PrincipalKind,
    RegisterKeyResult,
    exchange_pat,
    generate_keypair_and_exchange,
    generate_keypair_and_register,
    get_key,
    list_keys,
    register_key,
    revoke_key,
)
from istari_digital_client.identity.v1 import key_exchange, key_registration  # noqa: E402

for _name, _module in (
    ("identity_service", identity_service),
    ("keys", keys),
    ("key_exchange", key_exchange),
    ("key_registration", key_registration),
):
    sys.modules[f"{__name__}.{_name}"] = _module

__all__ = [
    "GeneratedClientCredentials", "generate_client_keypair", "IdentityServiceClient",
    "IdentityServiceError", "RetryPolicy", "validate_credentials_file",
    "validate_inline_credentials", "ExchangePatError", "ExchangePatResult",
    "PrincipalKind", "exchange_pat", "generate_keypair_and_exchange", "KeyMetadata",
    "KeyRegistrationError", "PrincipalKeys", "RegisterKeyResult",
    "generate_keypair_and_register", "get_key", "list_keys", "register_key", "revoke_key",
    "identity_service", "keys", "key_exchange", "key_registration",
]
