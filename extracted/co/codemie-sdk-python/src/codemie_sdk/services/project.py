# Copyright 2026 EPAM Systems, Inc. ("EPAM")
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Project management service for the CodeMie SDK."""

from typing import Literal
from uuid import UUID

from ..models.project import (
    BulkAssignmentRequest,
    BulkAssignmentResponse,
    BulkAssignmentUserItem,
    CsvImportValidationResponse,
    PaginatedProjectListResponse,
    ProjectAssignmentRequest,
    ProjectAssignmentResponse,
    ProjectAssignmentUpdateRequest,
    ProjectCreateRequest,
    ProjectCreateResponse,
    ProjectDeleteResponse,
    ProjectDetailResponse,
    ProjectUpdateRequest,
    ProjectUpdateResponse,
)
from ..utils.http import ApiRequestHandler, TokenSource


class ProjectService:
    """Service for managing projects in CodeMie."""

    def __init__(self, api_domain: str, token: TokenSource, verify_ssl: bool = True):
        """Initialize the ProjectService.

        Args:
            api_domain: Base URL for the CodeMie API
            token: Authentication token
            verify_ssl: Whether to verify SSL certificates
        """
        self._api = ApiRequestHandler(api_domain, token, verify_ssl)

    def create_project(
        self,
        name: str,
        description: str | None = None,
        cost_center_id: UUID | None = None,
        display_name: str | None = None,
    ) -> ProjectCreateResponse:
        """Create a new shared project.

        Args:
            name: Project name
            description: Project description (optional)
            cost_center_id: Optional cost center ID
            display_name: Human-friendly display name (max 150 chars)

        Returns:
            ProjectCreateResponse with project details

        Raises:
            HTTPException: If project creation fails
        """
        payload = ProjectCreateRequest(
            name=name,
            description=description,
            cost_center_id=cost_center_id,
            display_name=display_name,
        )

        return self._api.post(
            "/v1/projects",
            response_model=ProjectCreateResponse,
            json_data=payload.model_dump(mode="json", exclude_none=True),
        )

    def list_projects(
        self,
        search: str | None = None,
        page: int = 0,
        per_page: int = 20,
        include_counters: bool = True,
        include_budgets: bool = False,
        has_assigned_budgets: bool = False,
        sort_by: Literal["name", "created_at"] | None = None,
        sort_order: Literal["asc", "desc"] = "asc",
    ) -> PaginatedProjectListResponse:
        """List projects visible to current user with pagination and search.

        Args:
            search: Search by project name or description (substring match)
            page: Page number (0-indexed)
            per_page: Items per page (10-100)
            include_budgets: Include compact assigned budget summaries for project rows
            has_assigned_budgets: Return only projects with at least one active
                assigned project budget
            sort_by: Sort field (name or created_at); ignored when search is active
            sort_order: Sort direction (asc or desc)

        Returns:
            PaginatedProjectListResponse with projects and pagination info
        """
        params = {
            "page": page,
            "per_page": per_page,
            "include_counters": include_counters,
            "include_budgets": include_budgets,
            "has_assigned_budgets": has_assigned_budgets,
            "sort_order": sort_order,
        }

        if search is not None:
            params["search"] = search
        if sort_by is not None:
            params["sort_by"] = sort_by

        return self._api.get(
            "/v1/projects",
            response_model=PaginatedProjectListResponse,
            params=params,
            wrap_response=False,
        )

    def get_project_detail(
        self,
        project_name: str,
    ) -> ProjectDetailResponse:
        """Get project detail with member list.

        Args:
            project_name: Project name

        Returns:
            ProjectDetailResponse with project details and member list

        Raises:
            HTTPException: If project not found or user doesn't have access (404)
        """
        return self._api.get(
            f"/v1/projects/{project_name}",
            response_model=ProjectDetailResponse,
        )

    def update_project(
        self,
        project_name: str,
        name: str | None = None,
        description: str | None = None,
        clear_description: bool = False,
        cost_center_id: UUID | None = None,
        clear_cost_center: bool = False,
        enforce_member_spend_limits: bool | None = None,
        display_name: str | None = None,
        chargeback_attribution: str | None = None,
    ) -> ProjectUpdateResponse:
        """Update a project.

        Args:
            project_name: Current project name
            name: New project name (optional)
            description: New description (optional)
            clear_description: Set to True to remove the description (mutually
                exclusive with passing `description`)
            cost_center_id: New cost center ID (optional)
            clear_cost_center: Set to True to remove cost center
            enforce_member_spend_limits: Enable/disable per-member spend enforcement
            display_name: Human-friendly display name (max 150 chars)
            chargeback_attribution: Chargeback attribution mode ("project" or "cost_center")

        Returns:
            ProjectUpdateResponse with updated project details

        Raises:
            HTTPException: If project update fails, including a 422 when both
                `description` and `clear_description` are provided together
        """
        payload = ProjectUpdateRequest(
            name=name,
            description=description,
            clear_description=clear_description,
            cost_center_id=cost_center_id,
            clear_cost_center=clear_cost_center,
            enforce_member_spend_limits=enforce_member_spend_limits,
            display_name=display_name,
            chargeback_attribution=chargeback_attribution,
        )

        return self._api.patch(
            f"/v1/projects/{project_name}",
            response_model=ProjectUpdateResponse,
            json_data=payload.model_dump(exclude_none=True),
        )

    def delete_project(self, project_name: str) -> ProjectDeleteResponse:
        """Hard-delete a project if it has no assigned resources.

        Args:
            project_name: Project name

        Returns:
            ProjectDeleteResponse with deletion confirmation

        Raises:
            HTTPException: If project has assigned resources (409) or is personal (403)
        """
        return self._api.delete(
            f"/v1/projects/{project_name}",
            response_model=ProjectDeleteResponse,
        )

    # Assignment endpoints

    def assign_user_to_project(
        self,
        project_name: str,
        user_id: str,
        is_project_admin: bool,
    ) -> ProjectAssignmentResponse:
        """Assign a user to a project.

        Args:
            project_name: Project name
            user_id: User ID to assign
            is_project_admin: Whether user should be project admin

        Returns:
            ProjectAssignmentResponse with assignment details

        Raises:
            HTTPException: If assignment fails
        """
        payload = ProjectAssignmentRequest(
            user_id=user_id,
            is_project_admin=is_project_admin,
        )

        return self._api.post(
            f"/v1/projects/{project_name}/assignment",
            response_model=ProjectAssignmentResponse,
            json_data=payload.model_dump(exclude_none=True),
        )

    def update_user_project_assignment(
        self,
        project_name: str,
        user_id: str,
        is_project_admin: bool,
    ) -> ProjectAssignmentResponse:
        """Update a user's project-admin flag.

        Args:
            project_name: Project name
            user_id: User ID to update
            is_project_admin: New project admin flag value

        Returns:
            ProjectAssignmentResponse with updated assignment

        Raises:
            HTTPException: If user is not assigned to project (404)
        """
        payload = ProjectAssignmentUpdateRequest(is_project_admin=is_project_admin)

        return self._api.put(
            f"/v1/projects/{project_name}/assignment/{user_id}",
            response_model=ProjectAssignmentResponse,
            json_data=payload.model_dump(exclude_none=True),
        )

    def remove_user_from_project(
        self,
        project_name: str,
        user_id: str,
    ) -> ProjectAssignmentResponse:
        """Remove a user from a project.

        Args:
            project_name: Project name
            user_id: User ID to remove

        Returns:
            ProjectAssignmentResponse with removal confirmation

        Raises:
            HTTPException: If user is not assigned to project (404)
        """
        return self._api.delete(
            f"/v1/projects/{project_name}/assignment/{user_id}",
            response_model=ProjectAssignmentResponse,
        )

    def bulk_assign_users_to_project(
        self,
        project_name: str,
        users: list[BulkAssignmentUserItem],
    ) -> BulkAssignmentResponse:
        """Bulk assign/upsert users to a project.

        Assigns new users and updates roles for existing members in a single
        atomic operation.

        Args:
            project_name: Project name
            users: List of BulkAssignmentUserItem with user_id and is_project_admin (1-1000)

        Returns:
            BulkAssignmentResponse with per-user results

        Raises:
            HTTPException: If bulk assignment fails
        """
        payload = BulkAssignmentRequest(users=users)

        return self._api.post(
            f"/v1/projects/{project_name}/assignments",
            response_model=BulkAssignmentResponse,
            json_data=payload.model_dump(),
        )

    def bulk_remove_users_from_project(
        self,
        project_name: str,
        user_ids: list[str],
    ) -> BulkAssignmentResponse:
        """Bulk remove users from a project.

        Args:
            project_name: Project name
            user_ids: List of user IDs to remove (1-100)

        Returns:
            BulkAssignmentResponse with per-user results

        Raises:
            HTTPException: If bulk removal fails
        """
        params = [("user_id", user_id) for user_id in user_ids]

        return self._api.delete(
            f"/v1/projects/{project_name}/assignments",
            response_model=BulkAssignmentResponse,
            params=params,
        )

    # CSV import endpoints

    def validate_users_from_csv(
        self,
        project_name: str,
        file_content: bytes,
        filename: str = "users.csv",
    ) -> CsvImportValidationResponse:
        """Dry-run validation of a CSV file for user import.

        Validates each row (email format, role, system user existence) without
        modifying any data.

        Args:
            project_name: Project name
            file_content: CSV file content as bytes
            filename: CSV filename

        Returns:
            CsvImportValidationResponse with per-row validation results

        Raises:
            HTTPException: If file too large (413) or structural CSV error (422)
        """
        files = {"file": (filename, file_content, "text/csv")}

        return self._api.post_multipart(
            f"/v1/projects/{project_name}/import-users/validate",
            response_model=CsvImportValidationResponse,
            files=files,
        )

    def import_users_from_csv(
        self,
        project_name: str,
        file_content: bytes,
        filename: str = "users.csv",
    ) -> BulkAssignmentResponse:
        """Assign users to a project from a CSV file upload.

        CSV must include a header row with 'email' and 'role' columns.
        Allowed roles: 'administrator' (project admin), 'user' (regular member).

        Args:
            project_name: Project name
            file_content: CSV file content as bytes
            filename: CSV filename

        Returns:
            BulkAssignmentResponse with per-user results

        Raises:
            HTTPException: If file too large (413) or validation fails (422)
        """
        files = {"file": (filename, file_content, "text/csv")}

        return self._api.post_multipart(
            f"/v1/projects/{project_name}/import-users",
            response_model=BulkAssignmentResponse,
            files=files,
        )
