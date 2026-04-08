"""Plato SDK v2 - Sync Testcase operations."""

from __future__ import annotations

import httpx

from plato._generated.api.v2.testcases import list_testcases
from plato._generated.models import ListTestcasesResponse


class TestcaseManager:
    """Manager for testcase operations, accessed via plato.testcases."""

    def __init__(self, http_client: httpx.Client, api_key: str):
        self._http = http_client
        self._api_key = api_key

    def list(
        self,
        *,
        simulator_ids: str | None = None,
        name: str | None = None,
        prompt: str | None = None,
        tags: str | None = None,
        has_scoring_config: bool | None = None,
        scoring_config_type: str | None = None,
        testcase_statuses: str | None = None,
        work_order_item_id: str | None = None,
        status: str | None = None,
        page: int | None = 1,
        page_size: int | None = 250,
    ) -> ListTestcasesResponse:
        """List test cases with filtering and pagination.

        Args:
            simulator_ids: Comma-separated simulator IDs to filter by (e.g. "espocrm,gitea").
            name: Filter by testcase name.
            prompt: Filter by prompt text.
            tags: Comma-separated tags to filter by.
            has_scoring_config: If True, only return testcases with a scoring config.
            scoring_config_type: Filter by scoring config type ("MUTATION" or "OUTPUT").
            testcase_statuses: Comma-separated statuses to filter by (e.g. "ACTIVE").
            work_order_item_id: Filter by work order item ID.
            status: Filter by status.
            page: Page number (default: 1).
            page_size: Number of results per page (default: 250).

        Returns:
            ListTestcasesResponse with testcases list and pagination info.

        Examples:
            >>> from plato.v2 import Plato
            >>> plato = Plato()
            >>> response = plato.testcases.list(simulator_ids="espocrm", has_scoring_config=True)
            >>> for tc in response.testcases:
            ...     print(tc["public_id"], tc.get("name"))
        """
        return list_testcases.sync(
            client=self._http,
            simulator_ids=simulator_ids,
            name=name,
            prompt=prompt,
            tags=tags,
            has_scoring_config=has_scoring_config,
            scoring_config_type=scoring_config_type,
            testcase_statuses=testcase_statuses,
            work_order_item_id=work_order_item_id,
            status=status,
            page=page,
            page_size=page_size,
            x_api_key=self._api_key,
        )
