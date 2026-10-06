"""Identity-service clients: ``auth`` (token and keypair plumbing) and ``v2``
(generated from the identity-service OpenAPI document). ``v1`` is deprecated and
is not imported here; import ``istari_digital_client.identity.v1`` explicitly."""

from istari_digital_client.identity import auth, v2
from istari_digital_client.identity.auth.identity_service import IdentityApiVersion

__all__ = ["IdentityApiVersion", "auth", "v2"]
