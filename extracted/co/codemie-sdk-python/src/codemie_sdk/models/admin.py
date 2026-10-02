"""Admin models for managing applications/projects."""

from pydantic import BaseModel, ConfigDict, Field


class ApplicationInfo(BaseModel):
    """Single application entry returned by GET /v1/admin/applications."""

    model_config = ConfigDict(extra="ignore")

    name: str
    display_name: str | None = None


class ApplicationsListResponse(BaseModel):
    """Response model for list applications endpoint."""

    model_config = ConfigDict(extra="ignore")

    applications: list[ApplicationInfo] = Field(
        ..., description="List of application info objects"
    )


class ApplicationCreateRequest(BaseModel):
    """Request model for creating an application/project."""

    model_config = ConfigDict(extra="ignore")

    name: str = Field(..., description="Application/project name")


class ApplicationCreateResponse(BaseModel):
    """Response model for create application endpoint."""

    model_config = ConfigDict(extra="ignore")

    message: str = Field(..., description="Created application name")


class LocalUserCreateRequest(BaseModel):
    """Request model for admin user creation (local auth mode only)."""

    model_config = ConfigDict(extra="ignore")

    email: str
    username: str
    password: str
    name: str | None = None
    is_admin: bool = False
    is_maintainer: bool = False


class LocalUserDetail(BaseModel):
    """Response model for created/fetched user (local auth mode)."""

    model_config = ConfigDict(extra="ignore")

    id: str
    email: str
    username: str


class AdminUserListItem(BaseModel):
    """User item returned by the admin list-users endpoint."""

    model_config = ConfigDict(extra="ignore")

    id: str
    email: str
    username: str


class AdminUserListPagination(BaseModel):
    """Pagination metadata from GET /v1/admin/users."""

    model_config = ConfigDict(extra="ignore")

    total: int
    page: int
    per_page: int


class AdminUserListResponse(BaseModel):
    """Paginated response from GET /v1/admin/users."""

    model_config = ConfigDict(extra="ignore")

    data: list[AdminUserListItem]
    pagination: AdminUserListPagination

    @property
    def users(self) -> list[AdminUserListItem]:
        return self.data

    @property
    def total(self) -> int:
        return self.pagination.total
