from pydantic import BaseModel, Field
from typing import List
from ....utils.types.identifier import StrObjectId
from ...assets.company_assets import CompanyAssetType
from ...CRM.funnel import Funnel
from enum import StrEnum

class Permission(StrEnum):
    VIEW = "view"    # Can only see content
    USE = "use"      # Can interact with content
    ADMIN = "admin"  # Can modify/manage content
    NONE = "none"    # No access

class AssetPermission(BaseModel):
    """
    Base model for all asset permissions.
    Determines what kind of access a user has to a specific asset type.
    """
    asset_type: CompanyAssetType
    permission: Permission = Field(default=Permission.VIEW)

    def __eq__(self, other: 'AssetPermission') -> bool:
        return self.asset_type == other.asset_type

    def __hash__(self) -> int:
        return hash(self.asset_type)


    @classmethod
    def default_for_type(cls, asset_type: CompanyAssetType, permission: Permission = Permission.VIEW):

        return cls(
            asset_type=asset_type,
            permission=permission
        )

class AgentBusinessAreaAssignmentRequest(BaseModel):
    """Assignment of a business area to a user"""
    business_area_id: StrObjectId = Field(frozen=True)
    skill_level: int = Field(ge=0, le=10, default=6, description="The skill level of the agent in the business area")

class AgentBusinessAreaAssignment(AssetPermission):
    """Assignment of an agent to a business area with a specific skill level"""
    asset_type: CompanyAssetType = Field(default=CompanyAssetType.BUSINESS_AREAS, frozen=True)
    permission: Permission = Field(default=Permission.USE, frozen=True)
    business_area_id: StrObjectId = Field(frozen=True)
    skill_level: int = Field(ge=0, le=10, default=6, description="The skill level of the agent in the business area")

    @classmethod
    def create(cls, business_area_id, skill_level=6):
        return cls(
            business_area_id=business_area_id,
            skill_level=skill_level
        )

    @classmethod
    def create_from_request(cls, business_area_assignment: AgentBusinessAreaAssignmentRequest):
        return cls(
            business_area_id=business_area_assignment.business_area_id,
            skill_level=business_area_assignment.skill_level
        )

class FunnelAssignmentRequest(BaseModel):
    funnel_id: StrObjectId = Field(frozen=True)
    skill_level: int = Field(ge=0, le=10, default=6, description="The skill level of the agent in the funnel")

class FunnelAssignment(AssetPermission):
    """Assignment of an agent to a funnel with skill levels for each stage"""
    asset_type: CompanyAssetType = Field(default=CompanyAssetType.FUNNELS, frozen=True)
    permission: Permission = Field(default=Permission.USE, frozen=True)
    funnel_id: StrObjectId = Field(frozen=True)
    skill_level: int = Field(ge=0, le=10, default=6, description="The skill level of the agent in the funnel")

    @classmethod
    def create(cls, funnel: Funnel, default_skill_level=6):
        return cls(
            funnel_id=funnel.id,
            skill_level=default_skill_level
        )

    @classmethod
    def create_from_request(cls, funnel_assignment: FunnelAssignmentRequest):
        return cls(
            funnel_id=funnel_assignment.funnel_id,
            skill_level=funnel_assignment.skill_level
        )

