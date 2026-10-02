"""Tenants manager (IstariAdmin surface).

``Tenants`` manages tenant configuration and tenant public keys.
"""

from __future__ import annotations

from typing import Any

from istari_digital_client.sdk._base import _Manager


class Tenants(_Manager):
    """Manage tenant (organization) configuration and public keys.

    Aliases: tenant organization org


    Reached via ``admin.tenants``. Manages tenant settings and the public keys
    used for secure communication between tenants.

    Note: Public key operations apply to the current tenant (based on the
    authenticated user's tenant).

    Usage::

        # List all tenants
        for tenant in admin.tenants.list():
            print(f"{tenant.id}: {tenant.name}")

        # Get current tenant's public key
        key = admin.tenants.get_public_key()
        print(key.public_key)

        # Register a new public key for current tenant
        key = admin.tenants.create_public_key(public_key_file=b"-----BEGIN PUBLIC KEY-----...")
    """

    def list(
        self,
        *,
        page: int | None = None,
        size: int | None = None,
    ) -> Any:
        """List all tenants (organizations).

        Args:
            page: Page number (1-based).
            size: Number of items per page (max 100).

        Returns:
            A paginated result containing tenants.
        """
        # Storage API uses offset pagination (page/size), not cursor
        return self._call(
            self._engine.storage_api.list_tenants,
            page=page,
            size=size,
        )

    def get_public_key(self) -> Any:
        """Get the current tenant's public key.

        Returns:
            The tenant public key details.
        """
        return self._call(self._engine.storage_api.get_tenant_public_key)

    def create_public_key(
        self,
        *,
        public_key_file: bytes | str,
    ) -> Any:
        """Create/register a new public key for the current tenant.

        Mutates: true

        Args:
            public_key_file: The PEM-encoded public key as bytes or string.

        Returns:
            The created public key details.
        """
        return self._call(
            self._engine.storage_api.create_tenant_public_key,
            public_key_file=public_key_file,
        )

    def update_public_key(
        self,
        *,
        public_key_file: bytes | str,
    ) -> Any:
        """Update the current tenant's public key.

        Mutates: true

        Args:
            public_key_file: The new PEM-encoded public key as bytes or string.

        Returns:
            The updated public key details.
        """
        return self._call(
            self._engine.storage_api.update_tenant_public_key,
            public_key_file=public_key_file,
        )

    def delete_public_key(self) -> None:
        """Delete the current tenant's public key.

        Mutates: true
        """
        self._call(self._engine.storage_api.delete_tenant_public_key)
