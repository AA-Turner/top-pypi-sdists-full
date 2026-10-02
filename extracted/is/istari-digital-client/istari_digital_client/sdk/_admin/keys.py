"""Keys manager (IstariAdmin surface).

``Keys`` manages principal (USER/AGENT) keypair registration with the
Identity Service. This is a facade over the existing ``_auth/key_registration``
module.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from istari_digital_client.sdk._auth.identity_service import PrincipalKind
from istari_digital_client.sdk._auth.key_registration import (
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
from istari_digital_client.sdk._auth.keys import GeneratedClientCredentials, generate_client_keypair
from istari_digital_client.sdk._base import _Manager

if TYPE_CHECKING:
    from istari_digital_client.sdk._auth.identity_service import IdentityServiceClient


class Keys(_Manager):
    """Create and manage access keys (API keys / credentials) for users and agents.

    Aliases: access-key api-key credential key rotate


    Reached via ``admin.keys``. Manages ECDSA P-384 public keys for USER and
    AGENT principals against the identity-service's key-management endpoints.

    Note: This manager requires an authenticated IdentityServiceClient, which
    is typically obtained through the key exchange flow.

    Usage::

        # Generate and register a new keypair for a user
        result = admin.keys.generate_and_register(
            ir_client=ir_client,
            principal_id="user-uuid",
            kind=PrincipalKind.USER,
        )
        # Save credentials for later use
        result.credentials.write_to_json("credentials.json")

        # List registered keys for a principal
        principal_keys = admin.keys.list(
            ir_client=ir_client,
            principal_id="user-uuid",
        )
        for key in principal_keys.keys:
            print(f"{key.key_id}: created {key.created_at}")

        # Revoke a key
        admin.keys.revoke(
            ir_client=ir_client,
            principal_id="user-uuid",
            key_id="key-uuid",
        )
    """

    def generate_keypair(
        self,
        *,
        client_id: str,
        key_id: str | None = None,
    ) -> GeneratedClientCredentials:
        """Generate an access-key credential pair (public/private) without registering it.

        Args:
            client_id: The principal ID to bind the credentials to.
            key_id: Optional key ID; a random one is generated if not provided.

        Returns:
            The generated credentials (public/private key pair).
        """
        return generate_client_keypair(client_id=client_id, key_id=key_id)

    def register(
        self,
        ir_client: "IdentityServiceClient",
        principal_id: str,
        credentials: GeneratedClientCredentials,
        *,
        kind: PrincipalKind = PrincipalKind.USER,
        username: str | None = None,
        display_name: str | None = None,
    ) -> KeyMetadata:
        """Register a user's or agent's access key (public key) with the identity service.

        Mutates: true

        Args:
            ir_client: Authenticated identity-service client.
            principal_id: Target principal ID; "me" resolves to the caller (user routes).
            credentials: The keypair to register (only public key is sent).
            kind: Whether the principal is USER (default) or AGENT.
            username: Optional; honored when admin registers first key for new agent.
            display_name: Optional; seeds a new agent's display name.

        Returns:
            Metadata for the registered key.

        Raises:
            KeyRegistrationError: On invalid input, duplicate key, or server error.
        """
        return register_key(
            ir_client,
            principal_id,
            credentials,
            kind=kind,
            username=username,
            display_name=display_name,
        )

    def generate_and_register(
        self,
        ir_client: "IdentityServiceClient",
        principal_id: str,
        *,
        kind: PrincipalKind = PrincipalKind.USER,
        key_id: str | None = None,
    ) -> RegisterKeyResult:
        """Create (generate and register) an access key for a user or agent in one step.

        Mutates: true

        Aliases: create access-key api-key credential key


        Args:
            ir_client: Authenticated identity-service client.
            principal_id: Target principal ID (cannot be "me").
            kind: Whether the principal is USER (default) or AGENT.
            key_id: Optional key ID; a random one is generated if not provided.

        Returns:
            Result containing both credentials and key metadata.

        Raises:
            KeyRegistrationError: If principal_id is "me", or on server error.
        """
        return generate_keypair_and_register(
            ir_client,
            principal_id,
            kind=kind,
            key_id=key_id,
        )

    def list(
        self,
        ir_client: "IdentityServiceClient",
        principal_id: str,
        *,
        kind: PrincipalKind = PrincipalKind.USER,
    ) -> PrincipalKeys:
        """List a user's or agent's registered access keys (metadata only, no key material).

        Args:
            ir_client: Authenticated identity-service client.
            principal_id: Target principal ID; "me" resolves to the caller (user routes).
            kind: Whether the principal is USER (default) or AGENT.

        Returns:
            Principal info with list of key metadata.

        Raises:
            KeyRegistrationError: On client error or exhausted retry budget.
        """
        return list_keys(ir_client, principal_id, kind=kind)

    def get(
        self,
        ir_client: "IdentityServiceClient",
        principal_id: str,
        key_id: str,
        *,
        kind: PrincipalKind = PrincipalKind.USER,
    ) -> KeyMetadata:
        """Fetch metadata for a single registered key.

        Args:
            ir_client: Authenticated identity-service client.
            principal_id: Target principal ID; "me" resolves to the caller (user routes).
            key_id: The key ID to fetch.
            kind: Whether the principal is USER (default) or AGENT.

        Returns:
            Metadata for the key.

        Raises:
            KeyRegistrationError: If key not found (404) or on server error.
        """
        return get_key(ir_client, principal_id, key_id, kind=kind)

    def revoke(
        self,
        ir_client: "IdentityServiceClient",
        principal_id: str,
        key_id: str,
        *,
        kind: PrincipalKind = PrincipalKind.USER,
    ) -> None:
        """Revoke (hard-delete) a single registered access key.

        Mutates: true

        Args:
            ir_client: Authenticated identity-service client.
            principal_id: Target principal ID; "me" resolves to the caller (user routes).
            key_id: The key ID to revoke.
            kind: Whether the principal is USER (default) or AGENT.

        Raises:
            KeyRegistrationError: If key not found (404) or on server error.
        """
        revoke_key(ir_client, principal_id, key_id, kind=kind)


# Re-export types for convenience
__all__ = [
    "Keys",
    "KeyMetadata",
    "KeyRegistrationError",
    "PrincipalKeys",
    "RegisterKeyResult",
    "GeneratedClientCredentials",
    "PrincipalKind",
]
