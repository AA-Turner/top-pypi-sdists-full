"""User service implementation."""

from typing import Any, Dict, List, Optional

from ..models.user import (
    AdminUserProject,
    CodeMieUserDetail,
    PaginatedUserListResponse,
    User,
    UserData,
    UserProjectsResponse,
)
from ..utils.http import ApiRequestHandler, TokenSource


class UserService:
    """Service for managing user profile and preferences."""

    def __init__(self, api_domain: str, token: TokenSource, verify_ssl: bool = True):
        """Initialize the User service.

        Args:
            api_domain: Base URL for the CodeMie API
            token: Authentication token
            verify_ssl: Whether to verify SSL certificates. Default: True
        """
        self._api = ApiRequestHandler(api_domain, token, verify_ssl)

    def about_me(self) -> User:
        """Get current user profile.

        Returns:
            User profile information
        """
        return self._api.get("/v1/user", User, wrap_response=False)

    def get_data(self) -> UserData:
        """Get user data and preferences.

        Returns:
            User data and preferences
        """
        return self._api.get("/v1/user/data", UserData, wrap_response=False)

    def list_admin_users(
        self,
        page: int = 0,
        per_page: int = 20,
        search: Optional[str] = None,
        filters: Optional[str] = None,
    ) -> PaginatedUserListResponse:
        """List all users with pagination and filtering (admin only).

        Args:
            page: Page number (0-indexed)
            per_page: Results per page (10, 20, 50, or 100)
            search: Search string matching email, username, or name
            filters: Stringified JSON with filter keys: projects, user_type, is_active, platform_role, budgets
        """
        params: Dict[str, Any] = {"page": page, "per_page": per_page}
        if search is not None:
            params["search"] = search
        if filters is not None:
            params["filters"] = filters
        return self._api.get(
            "/v1/admin/users",
            PaginatedUserListResponse,
            params=params,
            wrap_response=False,
        )

    def get_admin_user(self, user_id: str) -> CodeMieUserDetail:
        """Get full details for a specific user (admin only).

        Args:
            user_id: The user's unique identifier
        """
        return self._api.get(
            f"/v1/admin/users/{user_id}", CodeMieUserDetail, wrap_response=False
        )

    def update_admin_user(self, user_id: str, **kwargs: Any) -> CodeMieUserDetail:
        """Update editable fields of a user (SuperAdmin only).

        Args:
            user_id: The user's unique identifier
            **kwargs: Fields to update (name, picture, is_admin, is_maintainer, is_active, project_limit, etc.)
        """
        return self._api.put(
            f"/v1/admin/users/{user_id}",
            CodeMieUserDetail,
            json_data=kwargs,
            wrap_response=False,
        )

    def get_user_projects(self, user_id: str) -> List[AdminUserProject]:
        """Get a user's project memberships (admin only).

        Args:
            user_id: The user's unique identifier
        """
        response = self._api.get(
            f"/v1/admin/users/{user_id}/projects",
            UserProjectsResponse,
            wrap_response=False,
        )
        return response.projects

    def assign_user_to_project(
        self,
        user_id: str,
        project_name: str,
        is_project_admin: bool = False,
    ) -> dict:
        """Grant a user access to a project (SuperAdmin only).

        Args:
            user_id: The user's unique identifier
            project_name: Name of the project to grant access to
            is_project_admin: Whether the user should be a project admin
        """
        return self._api.post(
            f"/v1/admin/users/{user_id}/projects",
            dict,
            json_data={
                "project_name": project_name,
                "is_project_admin": is_project_admin,
            },
            wrap_response=False,
        )

    def remove_user_from_project(self, user_id: str, project_name: str) -> None:
        """Remove a user's access to a project (SuperAdmin only).

        Args:
            user_id: The user's unique identifier
            project_name: Name of the project to remove access from
        """
        self._api.delete(
            f"/v1/admin/users/{user_id}/projects/{project_name}",
            dict,
            wrap_response=False,
        )

    def update_user_project_role(
        self, user_id: str, project_name: str, is_project_admin: bool
    ) -> None:
        """Change a user's role within a project (SuperAdmin only).

        Args:
            user_id: The user's unique identifier
            project_name: Name of the project
            is_project_admin: Whether the user should be a project admin
        """
        self._api.put(
            f"/v1/admin/users/{user_id}/projects/{project_name}",
            dict,
            json_data={"is_project_admin": is_project_admin},
            wrap_response=False,
        )

    def deactivate_user(self, user_id: str) -> None:
        """Deactivate (soft-delete) a user (SuperAdmin only).

        Args:
            user_id: The user's unique identifier
        """
        self._api.delete(
            f"/v1/admin/users/{user_id}",
            dict,
            wrap_response=False,
        )

    def reactivate_user(self, user_id: str) -> CodeMieUserDetail:
        """Reactivate a previously deactivated user (SuperAdmin only).

        Args:
            user_id: The user's unique identifier

        Returns:
            Updated user details with is_active=True
        """
        return self._api.put(
            f"/v1/admin/users/{user_id}",
            CodeMieUserDetail,
            json_data={"is_active": True},
            wrap_response=False,
        )
