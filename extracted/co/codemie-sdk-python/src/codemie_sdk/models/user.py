"""Models for user-related data structures."""

from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class PaginationInfo(BaseModel):
    model_config = ConfigDict(extra="ignore")

    total: int
    page: int
    per_page: int


class AdminUserListItem(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: str
    username: str
    email: str
    name: Optional[str] = None
    user_type: Optional[str] = None
    is_active: bool
    is_admin: bool
    is_maintainer: bool = False
    auth_source: Optional[str] = None
    last_login_at: Optional[str] = None
    date: Optional[str] = None


class PaginatedUserListResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")

    data: List[AdminUserListItem]
    pagination: PaginationInfo


class AdminUserProjectInfo(BaseModel):
    model_config = ConfigDict(extra="ignore")

    name: str
    is_project_admin: bool = False


class CodeMieUserDetail(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: str
    username: str
    email: str
    name: Optional[str] = None
    picture: Optional[str] = None
    user_type: Optional[str] = None
    is_active: bool
    is_admin: bool
    is_maintainer: bool = False
    auth_source: Optional[str] = None
    email_verified: bool = False
    last_login_at: Optional[str] = None
    projects: List[AdminUserProjectInfo] = []
    project_limit: Optional[int] = None
    knowledge_bases: List[str] = []
    date: Optional[str] = None
    update_date: Optional[str] = None
    deleted_at: Optional[str] = None


class AdminUserProject(BaseModel):
    model_config = ConfigDict(extra="ignore")

    project_name: str
    is_project_admin: bool = False
    date: Optional[str] = None


class UserProjectsResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")

    projects: List[AdminUserProject] = []


class User(BaseModel):
    """Model representing a user profile."""

    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    user_id: str = Field(
        description="Unique identifier of the user", validation_alias="userId"
    )
    name: str = Field(description="Full name of the user")
    username: str = Field(description="Username for authentication")
    email: str = Field(description="User email")
    is_admin: bool = Field(
        description="Whether the user has admin privileges", validation_alias="isAdmin"
    )
    applications: list[str] = Field(
        default_factory=list, description="List of applications the user has access to"
    )
    applications_admin: list[str] = Field(
        default_factory=list,
        description="List of applications where user has admin rights",
        validation_alias="applicationsAdmin",
    )
    picture: str = Field(default="", description="URL to user's profile picture")
    knowledge_bases: list[str] = Field(
        default_factory=list,
        description="List of knowledge bases the user has access to",
        validation_alias="knowledgeBases",
    )


class UserData(BaseModel):
    """Model representing user data."""

    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    id: str | None = Field(
        default=None, description="Unique identifier of the user data record"
    )
    date: str | None = Field(default=None, description="Creation timestamp")
    update_date: str | None = Field(default=None, description="Last update timestamp")
    user_id: str | None = Field(default=None, description="Associated user identifier")
