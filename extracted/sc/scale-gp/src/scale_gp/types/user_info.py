# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Optional
from typing_extensions import Literal

from .._models import BaseModel

__all__ = [
    "UserInfo",
    "AccessProfile",
    "AccessProfileAccount",
    "AccessProfileIdentity",
    "AssumedAccessProfile",
    "AssumedAccessProfileAccount",
    "AssumedAccessProfileIdentity",
]


class AccessProfileAccount(BaseModel):
    """The account in the access profile."""

    id: str

    name: str

    status: str
    """The status of the account: active, disabled, locked"""

    organization_id: Optional[str] = None


class AccessProfileIdentity(BaseModel):
    """The identity in the access profile."""

    id: str

    type: Literal["user", "service_account"]

    object: Optional[Literal["identity"]] = None


class AccessProfile(BaseModel):
    id: str
    """Access profile id."""

    account: AccessProfileAccount
    """The account in the access profile."""

    identity: AccessProfileIdentity
    """The identity in the access profile."""

    role: Literal["manager", "admin", "editor", "member", "labeler", "disabled", "invited", "viewer"]
    """The role of the user in the access profile."""


class AssumedAccessProfileAccount(BaseModel):
    """The account in the access profile."""

    id: str

    name: str

    status: str
    """The status of the account: active, disabled, locked"""

    organization_id: Optional[str] = None


class AssumedAccessProfileIdentity(BaseModel):
    """The identity in the access profile."""

    id: str

    type: Literal["user", "service_account"]

    object: Optional[Literal["identity"]] = None


class AssumedAccessProfile(BaseModel):
    """Present if the user has assumed a specific access profile via JWT token."""

    id: str
    """Access profile id."""

    account: AssumedAccessProfileAccount
    """The account in the access profile."""

    identity: AssumedAccessProfileIdentity
    """The identity in the access profile."""

    role: Literal["manager", "admin", "editor", "member", "labeler", "disabled", "invited", "viewer"]
    """The role of the user in the access profile."""


class UserInfo(BaseModel):
    id: str
    """User id"""

    access_profiles: List[AccessProfile]
    """A list of access profiles that the selected user has access to"""

    email: str
    """E-mail address"""

    assumed_access_profile: Optional[AssumedAccessProfile] = None
    """Present if the user has assumed a specific access profile via JWT token."""

    first_name: Optional[str] = None
    """First name"""

    is_deployment_admin: Optional[bool] = None
    """True if the current user is a deployment admin."""

    is_organization_admin: Optional[bool] = None
    """True if the current user is an organization admin."""

    last_name: Optional[str] = None
    """Last name"""

    organization_id: Optional[str] = None
    """The organization ID of the user."""

    preferences: Optional[Dict[str, object]] = None
    """User preferences that can be stored in the Scale GenAI Platform."""
