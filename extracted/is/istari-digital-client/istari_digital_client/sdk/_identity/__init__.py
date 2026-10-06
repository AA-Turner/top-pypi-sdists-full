"""Identity-service clients: ``auth`` (token and keypair plumbing) and the deprecated
``v1``, which is not imported here; import
``istari_digital_client.sdk._identity.v1`` explicitly. The generated v2 client the
facade calls lives outside this package, at ``istari_digital_client.identity.v2``."""

from istari_digital_client.sdk._identity import auth
from istari_digital_client.sdk._identity.auth.identity_service import IdentityApiVersion

__all__ = ["IdentityApiVersion", "auth"]
