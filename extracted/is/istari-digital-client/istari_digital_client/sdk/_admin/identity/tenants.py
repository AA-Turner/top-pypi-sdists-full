"""Identity-service tenants (admin.identity.tenants)."""

from __future__ import annotations

from typing import Any

from istari_digital_client.identity.v2.models.create_tenant_request import CreateTenantRequest
from istari_digital_client.identity.v2.models.update_tenant_request import UpdateTenantRequest
from istari_digital_client.sdk._admin.identity._requests import build_request
from istari_digital_client.sdk._base import _Manager


class IdentityTenants(_Manager):
    """Create, read, update, activate, deactivate and default identity-service tenants."""

    def list(self) -> list[Any]:
        """List every tenant the caller may see (the endpoint returns a bare array)."""
        return list(self._call(self._engine.identity_v2_api.list_tenants) or [])

    def create(self, *, slug: str, display_name: str | None = None, **fields: Any) -> Any:
        """Create a tenant.

        Mutates: true
        """
        req = build_request(CreateTenantRequest, {"slug": slug, "display_name": display_name, **fields}, verb="create")
        return self._call(self._engine.identity_v2_api.create_tenant, req)

    def get(self, tenant_id: str) -> Any:
        """Read one tenant by id."""
        return self._call(self._engine.identity_v2_api.get_tenant, tenant_id)

    def update(self, tenant_id: str, **fields: Any) -> Any:
        """Patch a tenant's mutable fields.

        Mutates: true
        """
        req = build_request(UpdateTenantRequest, fields, verb="update")
        return self._call(self._engine.identity_v2_api.update_tenant, tenant_id, req)

    def activate(self, tenant_id: str) -> Any:
        """Return a deactivated tenant to service.

        Mutates: true
        """
        return self._call(self._engine.identity_v2_api.activate_tenant, tenant_id)

    def deactivate(self, tenant_id: str) -> Any:
        """Deactivate a tenant and suspend its members.

        Mutates: true
        """
        return self._call(self._engine.identity_v2_api.deactivate_tenant, tenant_id)

    def set_default(self, tenant_id: str) -> Any:
        """Make this tenant the installation default.

        Mutates: true
        """
        return self._call(self._engine.identity_v2_api.set_default_tenant, tenant_id)
