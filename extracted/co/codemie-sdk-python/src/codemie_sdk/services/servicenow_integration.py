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

"""ServiceNow integration service for the CodeMie SDK."""

from ..models.servicenow_integration import (
    ServiceNowBudgetRequest,
    ServiceNowBudgetResponse,
    ServiceNowProject,
)
from ..utils.http import ApiRequestHandler, TokenSource


class ServiceNowIntegrationService:
    """Service for the ServiceNow integration endpoints.

    Only the ServiceNow integration service account may call these endpoints; any other
    caller is rejected with HTTP 403.
    """

    def __init__(self, api_domain: str, token: TokenSource, verify_ssl: bool = True):
        """Initialize the ServiceNowIntegrationService.

        Args:
            api_domain: Base URL for the CodeMie API
            token: Authentication token
            verify_ssl: Whether to verify SSL certificates
        """
        self._api = ApiRequestHandler(api_domain, token, verify_ssl)

    def list_projects(self, emails: list[str]) -> list[ServiceNowProject]:
        """List the shared projects that any of the given users belong to.

        The result is the distinct union across all emails, ordered by project name.
        Emails with no active CodeMie user are skipped, and an empty list is returned
        when none match. The emails are sent as given; the server rejects an empty
        list or an invalid email with HTTP 422.

        Args:
            emails: Requester and approver emails

        Returns:
            List of ServiceNowProject with the project name and display name

        Raises:
            HTTPError: If the request fails
        """
        return self._api.get(
            "/v1/integrations/servicenow/projects",
            response_model=list[ServiceNowProject],
            params={"emails": emails},
            wrap_response=False,
        )

    def submit_budget_request(
        self, request: ServiceNowBudgetRequest
    ) -> ServiceNowBudgetResponse:
        """Apply a ServiceNow budget request to a project.

        ``set`` replaces the project budget, ``adjust`` merges into it and ``cancel``
        deletes it. The project (and its cost center) is created when it does not exist,
        and every resolvable ``admin_emails`` user becomes a project admin.

        Args:
            request: The budget request

        Returns:
            ServiceNowBudgetResponse with the resolved project, cost center, the budget
            after the request (None after cancel) and the admin assignment outcome

        Raises:
            HTTPError: If the request is rejected (400, 403, 404, 409 or 422)
        """
        return self._api.post(
            "/v1/integrations/servicenow/budgets",
            response_model=ServiceNowBudgetResponse,
            data=request.model_dump_json(exclude_none=True),
            wrap_response=False,
        )
