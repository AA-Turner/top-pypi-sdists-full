"""Admin service implementation."""

from ..models.admin import (
    AdminUserListItem,
    AdminUserListResponse,
    ApplicationCreateRequest,
    ApplicationCreateResponse,
    ApplicationsListResponse,
    LocalUserCreateRequest,
    LocalUserDetail,
)
from ..utils import ApiRequestHandler, TokenSource


class AdminService:
    """Service for managing CodeMie applications/projects."""

    def __init__(self, api_domain: str, token: TokenSource, verify_ssl: bool = True):
        """Initialize the admin service.

        Args:
            api_domain: Base URL for the CodeMie API
            token: Authentication token
            verify_ssl: Whether to verify SSL certificates
        """
        self._api = ApiRequestHandler(api_domain, token, verify_ssl)

    def list_applications(self, project_name: str | None = None) -> list[str]:
        """Get list of all applications/projects.

        Args:
            project_name: Optional project name to filter by

        Returns:
            List of application names
        """
        params = {}
        if project_name:
            params["search"] = project_name

        response = self._api.get(
            "/v1/admin/applications",
            ApplicationsListResponse,
            params=params if params else None,
        )
        # Return plain names for backward compatibility with callers
        return [app.name for app in response.applications]

    def create_application(self, request: ApplicationCreateRequest) -> str:
        """Create a new application/project.

        Args:
            request: Application creation request

        Returns:
            Created application name
        """
        response = self._api.post(
            "/v1/admin/application",
            ApplicationCreateResponse,
            json_data=request.model_dump(exclude_none=True),
        )
        return response.message

    def create_local_user(
        self,
        email: str,
        username: str,
        password: str,
        name: str | None = None,
        is_admin: bool = False,
        is_maintainer: bool = False,
    ) -> LocalUserDetail:
        """Create a user via the admin API (local auth mode only).

        Args:
            email: User email address
            username: Username (3-50 chars)
            password: Initial password
            name: Optional display name
            is_admin: Grant admin role
            is_maintainer: Grant maintainer role

        Returns:
            Created user details
        """
        request = LocalUserCreateRequest(
            email=email,
            username=username,
            password=password,
            name=name,
            is_admin=is_admin,
            is_maintainer=is_maintainer,
        )
        return self._api.post(
            "/v1/admin/users",
            LocalUserDetail,
            json_data=request.model_dump(exclude_none=True),
            wrap_response=False,
        )

    def list_users(
        self,
        search: str | None = None,
        page: int = 0,
        per_page: int = 20,
    ) -> list[AdminUserListItem]:
        """List users via the admin API.

        Args:
            search: Search string matched against email, username, name
            page: 0-indexed page number
            per_page: Page size

        Returns:
            List of user items
        """
        params: dict = {"page": page, "per_page": per_page}
        if search:
            params["search"] = search
        response = self._api.get(
            "/v1/admin/users",
            AdminUserListResponse,
            params=params,
            wrap_response=False,
        )
        return response.users

    def delete_user(self, user_id: str) -> None:
        """Deactivate (soft-delete) a user via the admin API.

        Args:
            user_id: ID of the user to deactivate
        """
        self._api.delete(
            f"/v1/admin/users/{user_id}",
            dict,
            wrap_response=False,
        )
