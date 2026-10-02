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

"""Cost center management service for the CodeMie SDK (admin endpoints)."""

from uuid import UUID

from ..models.cost_center import (
    CostCenterResponse,
    CreateCostCenterRequest,
    PaginatedCostCenterListResponse,
)
from ..utils.http import ApiRequestHandler, TokenSource


class CostCenterService:
    """Service for managing cost centers via the CodeMie admin API."""

    def __init__(self, api_domain: str, token: TokenSource, verify_ssl: bool = True):
        """Initialize the CostCenterService.

        Args:
            api_domain: Base URL for the CodeMie API
            token: Authentication token
            verify_ssl: Whether to verify SSL certificates
        """
        self._api = ApiRequestHandler(api_domain, token, verify_ssl)

    def create_cost_center(
        self,
        name: str,
        description: str | None = None,
    ) -> CostCenterResponse:
        """Create a new cost center (admin-only).

        Args:
            name: Cost center name
            description: Optional description

        Returns:
            CostCenterResponse with the created cost center details including id

        Raises:
            HTTPError: If cost center creation fails
        """
        payload = CreateCostCenterRequest(name=name, description=description)

        return self._api.post(
            "/v1/admin/cost-centers",
            response_model=CostCenterResponse,
            json_data=payload.model_dump(exclude_none=True),
        )

    def delete_cost_center(self, cost_center_id: UUID) -> None:
        """Soft-delete a cost center (admin-only).

        Sets deleted_at on the cost center; does not remove the row.

        Args:
            cost_center_id: UUID of the cost center to delete

        Raises:
            HTTPError: If deletion fails
        """
        self._api.delete(
            f"/v1/admin/cost-centers/{cost_center_id}",
            response_model=dict,
            wrap_response=False,
        )

    def list_cost_centers(
        self,
        page: int = 0,
        per_page: int = 20,
    ) -> PaginatedCostCenterListResponse:
        """List cost centers with pagination (admin-only).

        Args:
            page: Page number (0-indexed)
            per_page: Items per page

        Returns:
            PaginatedCostCenterListResponse with cost centers and pagination info

        Raises:
            HTTPError: If the request fails
        """
        params = {"page": page, "per_page": per_page}

        return self._api.get(
            "/v1/admin/cost-centers",
            response_model=PaginatedCostCenterListResponse,
            params=params,
            wrap_response=False,
        )
