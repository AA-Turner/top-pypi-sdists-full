"""Identity-service authentication plumbing shared by the v1 and v2 clients.

Hand-written and kept: the RFC 7523 client-assertion token client and the keypair
helpers have no OpenAPI schema, so nothing here can be generated.
"""

from istari_digital_client.identity.auth.identity_service import (
    IdentityApiVersion,
    IdentityServiceClient,
    IdentityServiceError,
    PrincipalKind,
    RetryPolicy,
    validate_credentials_file,
    validate_inline_credentials,
)
from istari_digital_client.identity.auth.keys import (
    GeneratedClientCredentials,
    generate_client_keypair,
)

__all__ = [
    "GeneratedClientCredentials",
    "IdentityApiVersion",
    "IdentityServiceClient",
    "IdentityServiceError",
    "PrincipalKind",
    "RetryPolicy",
    "generate_client_keypair",
    "validate_credentials_file",
    "validate_inline_credentials",
]
