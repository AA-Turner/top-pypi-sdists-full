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

"""Cost center management models for the CodeMie SDK."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class CostCenterResponse(BaseModel):
    """Response model for a cost center."""

    model_config = ConfigDict(extra="ignore")

    id: UUID
    name: str
    description: str | None = None
    created_by: str
    created_at: datetime
    project_count: int = 0


class CreateCostCenterRequest(BaseModel):
    """Request model for creating a cost center."""

    model_config = ConfigDict(extra="ignore")

    name: str
    description: str | None = None


class PaginationInfo(BaseModel):
    """Pagination metadata for list responses."""

    model_config = ConfigDict(extra="ignore")

    total: int
    page: int
    per_page: int


class PaginatedCostCenterListResponse(BaseModel):
    """Paginated cost center list response."""

    model_config = ConfigDict(extra="ignore")

    data: list[CostCenterResponse]
    pagination: PaginationInfo
