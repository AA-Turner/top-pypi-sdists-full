"""Deprecated import path. Moved to ``istari_digital_client.sdk._identity.auth`` and
``istari_digital_client.sdk._identity.v1``; this shim warns and re-exports."""

import sys
import warnings

warnings.warn(
    "istari_digital_client.sdk._auth is deprecated; import from "
    "istari_digital_client.sdk._identity.auth or istari_digital_client.sdk._identity.v1",
    DeprecationWarning,
    stacklevel=2,
)

from istari_digital_client.sdk._identity.auth import (
    GeneratedClientCredentials,
    IdentityServiceClient,
    IdentityServiceError,
    RetryPolicy,
    generate_client_keypair,
    identity_service,
    keys,
    validate_credentials_file,
    validate_inline_credentials,
)
from istari_digital_client.sdk._identity.v1 import (
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
    key_exchange,
    key_registration,
    list_keys,
    register_key,
    revoke_key,
)

for _name, _module in (
    ("identity_service", identity_service),
    ("keys", keys),
    ("key_exchange", key_exchange),
    ("key_registration", key_registration),
):
    sys.modules[f"{__name__}.{_name}"] = _module

__all__ = [
    "ExchangePatError",
    "ExchangePatResult",
    "GeneratedClientCredentials",
    "IdentityServiceClient",
    "IdentityServiceError",
    "KeyMetadata",
    "KeyRegistrationError",
    "PrincipalKeys",
    "PrincipalKind",
    "RegisterKeyResult",
    "RetryPolicy",
    "exchange_pat",
    "generate_client_keypair",
    "generate_keypair_and_exchange",
    "generate_keypair_and_register",
    "get_key",
    "identity_service",
    "key_exchange",
    "key_registration",
    "keys",
    "list_keys",
    "register_key",
    "revoke_key",
    "validate_credentials_file",
    "validate_inline_credentials",
]
