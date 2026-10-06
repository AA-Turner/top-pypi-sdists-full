"""Identity-service principal keys (admin.identity.keys)."""

from __future__ import annotations

from typing import Any

from istari_digital_client.identity.v2.models.register_key_request import RegisterKeyRequest
from istari_digital_client.sdk._base import _Manager
from istari_digital_client.sdk._identity.auth.keys import GeneratedClientCredentials, generate_client_keypair


class IdentityKeys(_Manager):
    """Register, list, read and revoke a principal's public keys at /api/v2/principals/{id}/keys."""

    def list(self, principal_id: str = "me") -> Any:
        """List a principal's keys (``"me"`` for the caller)."""
        return self._call(self._engine.identity_v2_api.list_principal_keys, principal_id)

    def get(self, principal_id: str, key_id: str) -> Any:
        """Read one key's metadata."""
        return self._call(self._engine.identity_v2_api.get_principal_key, principal_id, key_id)

    def register(self, principal_id: str, credentials: GeneratedClientCredentials, *, name: str | None = None,
                 expires_at: str | None = None) -> Any:
        """Register a keypair's public key for a principal.

        Mutates: true
        """
        req = RegisterKeyRequest(key_id=credentials.key_id, public_key_pem=credentials.public_key_pem,
                                 name=name, expires_at=expires_at)
        return self._call(self._engine.identity_v2_api.register_principal_key, principal_id, req)

    def generate_and_register(self, principal_id: str, *, client_id: str | None = None,
                              key_id: str | None = None, name: str | None = None) -> tuple[GeneratedClientCredentials, Any]:
        """Generate a keypair, register its public half, return (credentials, key metadata).

        ``client_id`` names the principal in the credentials' client assertions,
        so it is required with the ``"me"`` alias: ``"me"`` is not a client id
        the token endpoint accepts. It defaults to ``principal_id`` otherwise.

        Mutates: true
        """
        if client_id is None and principal_id == "me":
            raise ValueError(
                "client_id is required when principal_id is 'me': the alias is not a "
                "usable client id; keys.list('me').client_id is the caller's"
            )
        creds = generate_client_keypair(client_id=client_id or principal_id, key_id=key_id)
        return creds, self.register(principal_id, creds, name=name)

    def revoke(self, principal_id: str, *, key_id: str) -> None:
        """Revoke a key.

        Mutates: true
        """
        self._call(self._engine.identity_v2_api.revoke_principal_key, principal_id, key_id)
