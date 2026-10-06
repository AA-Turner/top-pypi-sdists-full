"""Identity-service tenant memberships (admin.identity.memberships)."""

from __future__ import annotations

from typing import Any

from istari_digital_client.identity.v2.models.grant_membership_request import GrantMembershipRequest
from istari_digital_client.sdk._admin.identity._paging import paginate_cursor
from istari_digital_client.sdk._base import Page, _Manager


class IdentityMemberships(_Manager):
    """Grant, revoke and list tenant memberships."""

    def list(self, tenant_id: str, *, limit: int | None = None) -> Page[Any]:
        """Page through a tenant's memberships (every principal kind)."""
        return paginate_cursor(lambda c: self._call(
            self._engine.identity_v2_api.list_tenant_members, tenant_id, cursor=c, limit=limit))

    def list_humans(self, tenant_id: str, *, limit: int | None = None) -> Page[Any]:
        """Page through a tenant's human members."""
        return paginate_cursor(lambda c: self._call(
            self._engine.identity_v2_api.list_tenant_human_members, tenant_id, cursor=c, limit=limit))

    def list_agents(self, tenant_id: str, *, limit: int | None = None) -> Page[Any]:
        """Page through a tenant's agent members."""
        return paginate_cursor(lambda c: self._call(
            self._engine.identity_v2_api.list_tenant_agent_members, tenant_id, cursor=c, limit=limit))

    def grant(self, tenant_id: str, *, principal_id: str | None = None, email: str | None = None) -> Any:
        """Grant a membership by principal id or email.

        Mutates: true
        """
        if (principal_id is None) == (email is None):
            raise ValueError("pass exactly one of principal_id or email")
        req = GrantMembershipRequest(principal_id=principal_id, email=email)
        return self._call(self._engine.identity_v2_api.grant_tenant_member, tenant_id, req)

    def revoke(self, tenant_id: str, principal_id: str) -> Any:
        """Revoke a membership; returns the now-ended membership record.

        Mutates: true
        """
        return self._call(self._engine.identity_v2_api.revoke_tenant_member, tenant_id, principal_id)

    def list_for_principal(self, principal_id: str = "me") -> Page[Any]:
        """List one principal's memberships (``"me"`` for the caller).

        The generated endpoint takes no cursor/limit, so this always returns a
        single, complete page.
        """
        raw = self._call(self._engine.identity_v2_api.list_principal_memberships, principal_id)
        return Page(list(raw.items or []))
