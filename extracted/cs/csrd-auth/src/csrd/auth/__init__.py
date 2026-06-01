"""Pluggable authentication for FastAPI applications.

The auth system is built around two pluggable protocols:

1. :class:`Authenticator` — how to validate a token and produce claims.
2. :class:`KeyProvider` — how to resolve the cryptographic key(s) used
   for JWT verification.
"""

from ._authenticators import (
    CallbackAuthenticator,
    ChainedAuthenticator,
    JWTAuthenticator,
    RemoteAuthenticator,
    StaticAuthenticator,
    _default_claims_mapper,
)
from ._factory import (
    create_bearer_dependency,
    create_jwt_bearer,
)
from ._guards import (
    require_any_authority,
    require_authorities,
)
from ._key_providers import (
    CallbackKeyProvider,
    EnvKeyProvider,
    JWKSKeyProvider,
    MultiKeyProvider,
    StaticKeyProvider,
    _coerce_key_provider,
)
from ._key_ring import (
    SIGNING_KEYS_MIGRATION_DOWN,
    SIGNING_KEYS_MIGRATION_UP,
    KeyRingManager,
    SigningKey,
)
from ._protocols import (
    AuthCallback,
    Authenticator,
    KeyCallback,
    KeyProvider,
    KeySource,
)

__all__ = (
    "SIGNING_KEYS_MIGRATION_DOWN",
    "SIGNING_KEYS_MIGRATION_UP",
    "AuthCallback",
    "Authenticator",
    "CallbackAuthenticator",
    "CallbackKeyProvider",
    "ChainedAuthenticator",
    "EnvKeyProvider",
    "JWKSKeyProvider",
    "JWTAuthenticator",
    "KeyCallback",
    "KeyProvider",
    "KeyRingManager",
    "KeySource",
    "MultiKeyProvider",
    "RemoteAuthenticator",
    "SigningKey",
    "StaticAuthenticator",
    "StaticKeyProvider",
    "_coerce_key_provider",
    "_default_claims_mapper",
    "create_bearer_dependency",
    "create_jwt_bearer",
    "require_any_authority",
    "require_authorities",
)
