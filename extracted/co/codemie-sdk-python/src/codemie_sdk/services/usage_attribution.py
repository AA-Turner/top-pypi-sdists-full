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

"""Usage Attribution analytics service for the CodeMie SDK.

Wraps the read endpoints under ``/v1/analytics/usage-attribution``, available to
admins, maintainers and auditors when the ``features:usageAttribution`` flag is on.
"""

from typing import Any
from urllib.parse import quote

from ..models.usage_attribution import (
    UsageAttributionQueryParams,
    UsageAttributionResponse,
    UsageAttributionSettingsResponse,
    UsageAttributionTableResponse,
)
from ..utils import ApiRequestHandler, TokenSource

_BASE = "/v1/analytics/usage-attribution"


class UsageAttributionService:
    """Service for reading Usage Attribution analytics: who pays for Web Platform and CLI usage."""

    def __init__(self, api_domain: str, token: TokenSource, verify_ssl: bool = True):
        """Initialize the usage attribution service.

        Args:
            api_domain: Base URL for the CodeMie API
            token: Authentication token
            verify_ssl: Whether to verify SSL certificates
        """
        self._api = ApiRequestHandler(api_domain, token, verify_ssl)

    @staticmethod
    def _query(
        params: UsageAttributionQueryParams | None, **extra: Any
    ) -> dict[str, Any]:
        """Period parameters plus the extra ones that were given (None means the server default)."""
        query = params.model_dump(exclude_none=True) if params else {}
        query.update({key: value for key, value in extra.items() if value is not None})
        return query

    def _get_view(
        self,
        path: str,
        params: UsageAttributionQueryParams | None = None,
        **extra: Any,
    ) -> UsageAttributionResponse:
        return self._api.get(
            f"{_BASE}{path}",
            UsageAttributionResponse,
            params=self._query(params, **extra),
            wrap_response=False,
        )

    def _get_table(
        self,
        path: str,
        params: UsageAttributionQueryParams | None = None,
        **extra: Any,
    ) -> UsageAttributionTableResponse:
        return self._api.get(
            f"{_BASE}{path}",
            UsageAttributionTableResponse,
            params=self._query(params, **extra),
            wrap_response=False,
        )

    def get_totals(
        self, params: UsageAttributionQueryParams | None = None
    ) -> UsageAttributionResponse:
        """Get the fast totals: Total, Web Platform, CLI, Charged Back and Who Pays.

        Args:
            params: Period parameters

        Returns:
            UsageAttributionResponse whose data holds the amounts. The analysis
            block is absent for this view.

        Raises:
            requests.HTTPError: 403 without an allowed role, 404 when the feature is off
        """
        return self._get_view("/totals", params)

    def get_status(
        self, params: UsageAttributionQueryParams | None = None
    ) -> UsageAttributionResponse:
        """Get How It Works: coverage, data quality, run details and the settings in effect.

        Args:
            params: Period parameters

        Returns:
            UsageAttributionResponse with the analysis block
        """
        return self._get_view("/status", params)

    def get_cli_summary(
        self, params: UsageAttributionQueryParams | None = None
    ) -> UsageAttributionResponse:
        """Get the CLI categories: tiles, Who Pays and CLI spend by category.

        Args:
            params: Period parameters

        Returns:
            UsageAttributionResponse with tiles, who_pays, categories and the analysis block
        """
        return self._get_view("/cli-summary", params)

    def get_settings(self) -> UsageAttributionSettingsResponse:
        """Get the analysis settings: defaults, tunable schema and what the caller may do.

        Returns:
            UsageAttributionSettingsResponse, whose data carries ``can_tune`` and ``can_refresh``
        """
        return self._api.get(
            f"{_BASE}/settings",
            UsageAttributionSettingsResponse,
            wrap_response=False,
        )

    def get_shared_projects(
        self,
        params: UsageAttributionQueryParams | None = None,
        scope: str | None = None,
        search: str | None = None,
        page: int | None = None,
        per_page: int | None = None,
        sort_by: str | None = None,
        sort_order: str | None = None,
    ) -> UsageAttributionTableResponse:
        """List shared projects without a budget.

        Args:
            params: Period parameters
            scope: "threshold" (default) or "all"
            search: Case-insensitive text to find in the project name
            page: Zero-indexed page number
            per_page: Items per page
            sort_by: Column to sort by
            sort_order: "asc" or "desc"

        Returns:
            UsageAttributionTableResponse with the rows of the page and the filter counts
        """
        return self._get_table(
            "/shared-projects",
            params,
            scope=scope,
            search=search,
            page=page,
            per_page=per_page,
            sort_by=sort_by,
            sort_order=sort_order,
        )

    def get_shared_project(
        self,
        project_name: str,
        params: UsageAttributionQueryParams | None = None,
    ) -> UsageAttributionResponse:
        """Get the popup of one shared project.

        Args:
            project_name: Name of the project
            params: Period parameters

        Returns:
            UsageAttributionResponse whose data holds ``row`` and ``detail``

        Raises:
            requests.HTTPError: 404 when the project is not in the analysis of the period
        """
        return self._get_view(
            f"/shared-projects/{quote(project_name, safe='')}", params
        )

    def get_repository_groups(
        self,
        params: UsageAttributionQueryParams | None = None,
        scope: str | None = None,
        search: str | None = None,
        page: int | None = None,
        per_page: int | None = None,
        sort_by: str | None = None,
        sort_order: str | None = None,
    ) -> UsageAttributionTableResponse:
        """List repository groups in personal projects.

        Args:
            params: Period parameters
            scope: "threshold" (default) or "all"
            search: Case-insensitive text to find in the group name or its repositories
            page: Zero-indexed page number
            per_page: Items per page
            sort_by: Column to sort by
            sort_order: "asc" or "desc"

        Returns:
            UsageAttributionTableResponse with the rows of the page and the filter counts
        """
        return self._get_table(
            "/repository-groups",
            params,
            scope=scope,
            search=search,
            page=page,
            per_page=per_page,
            sort_by=sort_by,
            sort_order=sort_order,
        )

    def get_repository_group(
        self,
        group_id: str,
        params: UsageAttributionQueryParams | None = None,
    ) -> UsageAttributionResponse:
        """Get the popup of one repository group.

        Args:
            group_id: Group id as listed by get_repository_groups
            params: Period parameters

        Returns:
            UsageAttributionResponse whose data holds ``row`` and ``detail``

        Raises:
            requests.HTTPError: 404 when the group is not in the analysis of the period
        """
        return self._get_view(f"/repository-groups/{quote(group_id, safe='')}", params)

    def get_people(
        self,
        params: UsageAttributionQueryParams | None = None,
        filter: str | None = None,
        search: str | None = None,
        page: int | None = None,
        per_page: int | None = None,
        sort_by: str | None = None,
        sort_order: str | None = None,
    ) -> UsageAttributionTableResponse:
        """List people with their spend.

        Args:
            params: Period parameters
            filter: "all" (default), "cand", "prod", "exp", "shared" or "platform"
            search: Case-insensitive text to find in the name, e-mail or main repository
            page: Zero-indexed page number
            per_page: Items per page
            sort_by: Column to sort by
            sort_order: "asc" or "desc"

        Returns:
            UsageAttributionTableResponse with the rows of the page and a count per filter
        """
        return self._get_table(
            "/people",
            params,
            filter=filter,
            search=search,
            page=page,
            per_page=per_page,
            sort_by=sort_by,
            sort_order=sort_order,
        )

    def get_person(
        self,
        user_id: str,
        params: UsageAttributionQueryParams | None = None,
    ) -> UsageAttributionResponse:
        """Get the popup of one person.

        Args:
            user_id: User id as listed by get_people
            params: Period parameters

        Returns:
            UsageAttributionResponse whose data holds ``row`` and ``detail``

        Raises:
            requests.HTTPError: 404 when the person is not in the analysis of the period
        """
        return self._get_view(f"/people/{quote(user_id, safe='')}", params)

    def get_breakdown(
        self,
        params: UsageAttributionQueryParams | None = None,
        dimension: str | None = None,
        category: str | None = None,
    ) -> UsageAttributionResponse:
        """Get CLI spend paid from personal budgets, by country or job title group.

        Args:
            params: Period parameters
            dimension: "country" (default) or "job"
            category: "production" (default), "learning", "testing", "experimental",
                "pet_project" or "unclassified"

        Returns:
            UsageAttributionResponse whose data holds ``rows`` (label and spend) and ``total``

        Raises:
            requests.HTTPError: 404 when user enrichment is disabled
        """
        return self._get_view(
            "/breakdown", params, dimension=dimension, category=category
        )
