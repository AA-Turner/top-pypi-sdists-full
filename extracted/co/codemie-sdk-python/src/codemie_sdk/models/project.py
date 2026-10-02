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

"""Project management models for the CodeMie SDK."""

from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ProjectCounters(BaseModel):
    """Resource counters for a project."""

    model_config = ConfigDict(extra="ignore")

    assistants_count: int = 0
    workflows_count: int = 0
    integrations_count: int = 0
    datasources_count: int = 0
    skills_count: int = 0


class ProjectMember(BaseModel):
    """Project member with role."""

    model_config = ConfigDict(extra="ignore")

    user_id: str
    is_project_admin: bool
    date: datetime | None = None


class ProjectBudgetItem(BaseModel):
    """Budget assigned to a project (present when include_budgets=true)."""

    model_config = ConfigDict(extra="ignore")

    budget_id: str
    name: str
    budget_category: str
    soft_budget: float
    max_budget: float
    budget_duration: str
    budget_reset_at: datetime | None = None
    provider_sync_status: str | None = None
    member_count: int
    allocated_member_budget_total: float
    current_spending: float | None = None


class ProjectListItem(BaseModel):
    """Project list response item."""

    model_config = ConfigDict(extra="ignore")

    name: str
    display_name: str | None = None
    description: str | None = None
    project_type: str
    created_by: str | None = None
    user_count: int
    admin_count: int
    created_at: datetime | None = None
    counters: ProjectCounters | None = None
    cost_center_id: UUID | None = None
    cost_center_name: str | None = None
    spending: float | None = None
    budgets: list[ProjectBudgetItem] | None = []
    chargeback_enabled: bool = False
    chargeback_attribution: str = "project"


class PaginationInfo(BaseModel):
    """Pagination metadata for list responses."""

    model_config = ConfigDict(extra="ignore")

    total: int
    page: int
    per_page: int


class PaginatedProjectListResponse(BaseModel):
    """Paginated project list response."""

    model_config = ConfigDict(extra="ignore")

    data: list[ProjectListItem]
    pagination: PaginationInfo


class ProjectDetailResponse(BaseModel):
    """Project detail response with member list."""

    model_config = ConfigDict(extra="ignore")

    name: str
    display_name: str | None = None
    description: str | None = None
    project_type: str
    created_by: str | None = None
    user_count: int
    admin_count: int
    created_at: datetime | None = None
    cost_center_id: UUID | None = None
    cost_center_name: str | None = None
    members: list[ProjectMember]
    chargeback_attribution: str = "project"


class ProjectCreateRequest(BaseModel):
    """Request to create a new project."""

    model_config = ConfigDict(extra="ignore")

    name: str
    display_name: str | None = Field(
        default=None,
        max_length=150,
        description="Human-friendly display name (max 150 chars)",
    )
    description: str | None = Field(default=None, description="Project description")
    cost_center_id: UUID | None = None


class ProjectCreateResponse(BaseModel):
    """Response after creating a project."""

    model_config = ConfigDict(extra="ignore")

    name: str
    display_name: str | None = None
    description: str | None = None
    project_type: str
    created_by: str
    created_at: datetime
    cost_center_id: UUID | None = None
    cost_center_name: str | None = None
    enforce_member_spend_limits: bool = False
    chargeback_attribution: str = "project"


# PATCH /v1/projects/{name} returns the same shape as the create response
ProjectUpdateResponse = ProjectCreateResponse


class ProjectUpdateRequest(BaseModel):
    """Request to update a project."""

    model_config = ConfigDict(extra="ignore")

    name: str | None = None
    display_name: str | None = Field(
        default=None,
        max_length=150,
        description="Human-friendly display name (max 150 chars)",
    )
    description: str | None = None
    clear_description: bool = False
    cost_center_id: UUID | None = None
    clear_cost_center: bool = False
    enforce_member_spend_limits: bool | None = None
    chargeback_attribution: str | None = None


class ProjectDeleteResponse(BaseModel):
    """Response after deleting a project."""

    model_config = ConfigDict(extra="ignore")

    message: str
    name: str


class ProjectAssignmentRequest(BaseModel):
    """Request to assign a user to a project."""

    model_config = ConfigDict(extra="ignore")

    user_id: str
    is_project_admin: bool


class ProjectAssignmentUpdateRequest(BaseModel):
    """Request to update a user's project role."""

    model_config = ConfigDict(extra="ignore")

    is_project_admin: bool


class ProjectAssignmentResponse(BaseModel):
    """Response after project assignment operation."""

    model_config = ConfigDict(extra="ignore")

    message: str
    user_id: str
    project_name: str
    is_project_admin: bool | None = None


class BulkAssignmentUserItem(BaseModel):
    """Single user entry in bulk assignment request."""

    model_config = ConfigDict(extra="ignore")

    user_id: str
    is_project_admin: bool


class BulkAssignmentRequest(BaseModel):
    """Bulk assignment request body."""

    model_config = ConfigDict(extra="ignore")

    users: list[BulkAssignmentUserItem] = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="List of users to assign/update (1-1000)",
    )


class BulkAssignmentResultItem(BaseModel):
    """Per-user result in bulk assignment response."""

    model_config = ConfigDict(extra="ignore")

    user_id: str
    action: Literal["assigned", "updated", "removed"]
    is_project_admin: bool | None = None


class BulkAssignmentResponse(BaseModel):
    """Response for bulk assignment operations."""

    model_config = ConfigDict(extra="ignore")

    message: str
    project_name: str
    total: int
    results: list[BulkAssignmentResultItem]


class CsvImportRowResult(BaseModel):
    """Per-row result from a CSV import validation."""

    model_config = ConfigDict(extra="ignore")

    email: str
    role: str
    error: str | None = None


class CsvImportValidationResponse(BaseModel):
    """Response for CSV import dry-run validation."""

    model_config = ConfigDict(extra="ignore")

    users: list[CsvImportRowResult]
