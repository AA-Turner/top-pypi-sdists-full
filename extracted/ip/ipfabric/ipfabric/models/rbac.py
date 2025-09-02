import logging
from typing import Optional, Literal

from pydantic import Field, BaseModel, computed_field

from ipfabric.models.oas import Endpoint

logger = logging.getLogger("ipfabric")


class RBAC(BaseModel):
    name: str
    description: Optional[str] = None
    system: bool = Field(None, alias="isSystem")

    def __repr__(self):
        return f"{self.name}"


class Policy(RBAC, BaseModel):
    policy_id: str = Field(None, alias="id")
    scope_type: Literal["attributeScopes", "apiScopes"] = Field(None, alias="scopeType")
    api_scope_ids: Optional[list[str]] = Field(default_factory=list, alias="apiScopeIds")
    attribute_scope_ids: Optional[list[str]] = Field(default_factory=list, alias="attributeScopeIds")
    attribute_filters: Optional[dict] = Field(default_factory=dict, alias="attributeFilters")
    api_scopes: Optional[list[Endpoint]] = Field(default_factory=list)

    @computed_field
    @property
    def api_scopes_by_id(self) -> dict[str, Endpoint]:
        return {_.api_scope_id: _ for _ in self.api_scopes}

    def __hash__(self):
        return hash(self.policy_id)


class Role(RBAC, BaseModel):
    role_id: str = Field(None, alias="id")
    role_type: str = Field(None, alias="type")
    admin: bool = Field(None, alias="isAdmin")
    policy_ids: Optional[list[str]] = Field(default_factory=list, alias="policyIds")
    policies: Optional[list[Policy]] = Field(default_factory=list)

    @computed_field
    @property
    def policies_by_name(self) -> dict[str, Policy]:
        return {_.name: _ for _ in self.policies} if self.policies else dict()

    @computed_field
    @property
    def policies_by_id(self) -> dict[str, Policy]:
        return {_.policy_id: _ for _ in self.policies} if self.policies else dict()

    def __hash__(self):
        return hash(self.role_id)
