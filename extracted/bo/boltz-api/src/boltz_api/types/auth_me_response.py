# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Union, Optional
from typing_extensions import Literal, TypeAlias

from .._models import BaseModel

__all__ = ["AuthMeResponse", "AuthMeAPIKeyResponse", "AuthMeUserResponse", "AuthMeUserResponseOrganizationMembership"]


class AuthMeAPIKeyResponse(BaseModel):
    api_key_id: str

    key_type: Literal["admin", "workspace"]

    mode: Literal["live", "test"]

    organization_id: str

    principal_type: Literal["api_key"]

    selected_organization_id: str

    workspace_id: Optional[str] = None

    organization_name: Optional[str] = None


class AuthMeUserResponseOrganizationMembership(BaseModel):
    compute_role: Literal["admin", "member"]

    organization_id: str

    organization_name: Optional[str] = None


class AuthMeUserResponse(BaseModel):
    active_organization_id: Optional[str] = None

    organization_memberships: List[AuthMeUserResponseOrganizationMembership]

    principal_type: Literal["user"]

    selected_organization_id: Optional[str] = None

    user_id: str


AuthMeResponse: TypeAlias = Union[AuthMeAPIKeyResponse, AuthMeUserResponse]
