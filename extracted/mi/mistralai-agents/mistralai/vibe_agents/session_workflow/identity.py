"""Caller identity passed into a session workflow."""

from typing import Final, Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict

# The completion gateway's billing bands, in the order it prioritizes them. Mirrors Albe's
# APIKeyTier, which is where the value is resolved from; restated because this wire package
# imports nothing outside pydantic.
OrgTier = Literal["pending", "free", "t1", "t2", "t3", "t4", "t5", "t6", "t7", "godmode"]

# What Albe assumes for a customer with no tier recorded. Used whenever a tier could not be
# resolved: the lowest band is the only safe guess, because the gateway reads an absent or
# unparseable tier not as "throttle hard" but as "outranks every banded caller".
DEFAULT_ORG_TIER: Final[OrgTier] = "free"


class OrganizationTenantScope(BaseModel):
    """Organization-level tenant routing scope."""

    model_config = ConfigDict(frozen=True)

    customer_id: UUID
    organization_id: UUID

    def to_organization_tenant_scope(self) -> "OrganizationTenantScope":
        return OrganizationTenantScope(customer_id=self.customer_id, organization_id=self.organization_id)


class WorkspaceTenantScope(OrganizationTenantScope):
    """Workspace-level tenant routing scope."""

    workspace_id: UUID

    def to_workspace_tenant_scope(self) -> "WorkspaceTenantScope":
        return WorkspaceTenantScope(
            customer_id=self.customer_id,
            organization_id=self.organization_id,
            workspace_id=self.workspace_id,
        )


class Principal(WorkspaceTenantScope):
    """Workflow caller identity.

    On a start input it is caller-asserted: the Agents SDK worker never trusts it there and takes
    the caller from the execution's attested identity instead.

    `user_id` is optional because some workspace-level workflows are not tied
    to a user, for example scheduled or system-triggered runs.
    """

    user_id: UUID | None = None


__all__ = ["DEFAULT_ORG_TIER", "OrganizationTenantScope", "OrgTier", "Principal", "WorkspaceTenantScope"]
