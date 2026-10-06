"""Identity-service roles (admin.identity.roles)."""

from __future__ import annotations

from typing import Any

from istari_digital_client.identity.v2.models.grant_principal_role_request import GrantPrincipalRoleRequest
from istari_digital_client.identity.v2.models.grant_tenant_role_request import GrantTenantRoleRequest
from istari_digital_client.sdk._admin.identity._paging import paginate_cursor
from istari_digital_client.sdk._base import Page, _Manager


class IdentityRoles(_Manager):
    """The role catalog and role grants at tenant and principal scope."""

    def list(self) -> Page[Any]:
        """List the role catalog.

        The generated endpoint takes no cursor/limit, so this always returns a
        single, complete page.
        """
        raw = self._call(self._engine.identity_v2_api.list_roles)
        return Page(list(raw.items or []))

    def holders(self, role: str, *, tenant_id: str | None = None, limit: int | None = None) -> Page[Any]:
        """Page through the principals holding a role."""
        tenant_ids = [tenant_id] if tenant_id else None
        return paginate_cursor(lambda c: self._call(
            self._engine.identity_v2_api.list_role_holders, role, tenant_id=tenant_ids, cursor=c, limit=limit))

    def list_tenant_roles(self, tenant_id: str, *, limit: int | None = None) -> Page[Any]:
        """Page through the grants held in a tenant."""
        return paginate_cursor(lambda c: self._call(
            self._engine.identity_v2_api.list_tenant_roles, tenant_id, cursor=c, limit=limit))

    def grant_tenant_role(self, tenant_id: str, *, role: str, principal_id: str) -> Any:
        """Grant a tenant-scoped role.

        Mutates: true
        """
        return self._call(self._engine.identity_v2_api.grant_tenant_role, tenant_id,
                          GrantTenantRoleRequest(role_id=role, principal_id=principal_id))

    def revoke_tenant_role(self, tenant_id: str, *, role: str, principal_id: str) -> None:
        """Revoke a tenant-scoped role.

        Mutates: true
        """
        self._call(self._engine.identity_v2_api.revoke_tenant_role, tenant_id, role, principal_id=principal_id)

    def list_principal_roles(self, principal_id: str) -> Page[Any]:
        """List one principal's grants, named by id.

        The role routes take no ``"me"`` alias, unlike the key and membership
        ones; pass ``principals.me()``'s id to ask about the caller. The
        generated endpoint takes no cursor/limit, so this always returns a
        single, complete page.
        """
        raw = self._call(self._engine.identity_v2_api.list_principal_roles, principal_id)
        return Page(list(raw.items or []))

    def grant_principal_role(self, principal_id: str, *, role: str, tenant_id: str | None = None) -> Any:
        """Grant a role to a principal, platform-wide or in one tenant.

        Mutates: true
        """
        return self._call(self._engine.identity_v2_api.grant_principal_role, principal_id,
                          GrantPrincipalRoleRequest(role_id=role, tenant_id=tenant_id))

    def revoke_principal_role(self, principal_id: str, *, role: str, tenant_id: str | None = None) -> None:
        """Revoke a principal's role.

        Mutates: true
        """
        self._call(self._engine.identity_v2_api.revoke_principal_role, principal_id, role, tenant_id=tenant_id)
