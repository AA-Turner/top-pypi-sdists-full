"""Datafold API client for making requests to the Datafold server."""

import asyncio
import logging
from typing import Any

import httpx
from pydantic import BaseModel

from datafold_mcp.auth import DatafoldAuth

logger = logging.getLogger(__name__)


class DatafoldAPIError(Exception):
    """Base exception for Datafold API errors."""

    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(message)
        self.status_code = status_code


class DataSourceNotFoundError(DatafoldAPIError):
    """Data source not found."""


class QueryExecutionError(DatafoldAPIError):
    """Query execution failed."""


class AuthenticationError(DatafoldAPIError):
    """Authentication failed."""


class QueryResult(BaseModel):
    """Result of a SQL query execution."""

    rows: list[dict[str, Any]]
    columns: list[dict[str, Any]] | None = None


class DatafoldClient:
    """HTTP client for Datafold API."""

    api_v1: str = "/api/v1"

    def __init__(self, host: str, auth: DatafoldAuth, timeout: int = 300):
        self.host = host.rstrip("/")
        self.auth = auth
        self.timeout = timeout

    def _check_response(
        self,
        response: httpx.Response,
        context: str | None = None,
    ) -> None:
        """Check response for common errors and raise appropriate exceptions."""
        status = response.status_code

        if status < 400:
            return

        # Get response body for error details
        error_body = response.text[:500] if response.text else ""
        context_prefix = f"{context}: " if context else ""

        if status == 401:
            msg = f"{context_prefix}Authentication failed. Please verify your DATAFOLD_API_KEY."
            logger.error(msg)
            raise AuthenticationError(msg, status_code=401)

        if status == 403:
            msg = f"{context_prefix}Access denied. Check your permissions."
            logger.error(msg)
            raise AuthenticationError(msg, status_code=403)

        if status >= 500:
            msg = f"{context_prefix}Server error ({status}). {error_body}"
            logger.error(msg)
            raise QueryExecutionError(msg, status_code=status)

        # Other 4xx errors
        msg = f"{context_prefix}Request failed ({status}). {error_body}"
        logger.error(msg)
        raise DatafoldAPIError(msg, status_code=status)

    async def _request(
        self,
        method: str,
        path: str,
        **kwargs: Any,
    ) -> Any:
        """Make an authenticated request to the Datafold API."""
        url = f"{self.host}{self.api_v1}{path}"

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            self.auth.apply_to_client(client)
            response = await client.request(method, url, **kwargs)
            self._check_response(response)
            return response.json()

    async def verify_connection(self) -> None:
        """Verify API key is valid; raise if not."""
        try:
            await self._request("GET", "/organization/meta")
        except Exception as exc:
            raise RuntimeError(
                "Failed to connect to Datafold API. "
                "Please verify DATAFOLD_HOST and DATAFOLD_API_KEY environment variables."
            ) from exc

    # Data Sources
    async def list_data_sources(self) -> list[dict[str, Any]]:
        """List available data sources."""
        return await self._request("GET", "/data_sources")

    async def get_table_schema(
        self,
        data_source_id: int,
        table_path: list[str],
        timeout: int = 60,
    ) -> dict[str, Any]:
        """Get schema for a specific table (launches task and polls for results)."""
        # Launch the task
        task_response = await self._request(
            "POST",
            f"/data_sources/{data_source_id}/dataset_schema",
            json={"table": table_path},
        )

        task_id = task_response.get("task_id")
        if not task_id:
            raise DatafoldAPIError(f"Failed to launch schema task: {task_response}")

        # Poll for results
        elapsed = 0
        poll_interval = 1

        while elapsed < timeout:
            result = await self._request(
                "GET",
                f"/data_sources/{data_source_id}/dataset_schema/{task_id}",
            )

            status = result.get("status", "").lower()

            if status == "done":
                schema = result.get("result")
                if not schema:
                    raise DatafoldAPIError(
                        f"Schema fetch returned empty result for table {table_path}"
                    )
                return schema

            if status == "failed":
                error = result.get("result", {}).get("error", "Unknown error")
                raise DatafoldAPIError(f"Schema fetch failed: {error}")

            await asyncio.sleep(poll_interval)
            elapsed += poll_interval

        raise DatafoldAPIError(f"Schema fetch timed out after {timeout} seconds")

    async def guess_primary_keys(
        self,
        data_source_id: int,
        table: list[str],
        sample_size: int | None = None,
        avoid_types: list[str] | None = None,
        avoid_names: list[str] | None = None,
        candidates: int = 1,
    ) -> dict[str, Any]:
        """Guess primary key columns for a table."""
        payload: dict[str, Any] = {
            "table": table,
            "candidates": candidates,
        }
        if sample_size is not None:
            payload["sample_size"] = sample_size
        if avoid_types:
            payload["avoid_types"] = avoid_types
        if avoid_names:
            payload["avoid_names"] = avoid_names

        return await self._request(
            "POST",
            f"/data_sources/{data_source_id}/guess_pk",
            json=payload,
        )

    # Queries
    async def run_query(
        self,
        data_source_id: int,
        query: str,
    ) -> QueryResult:
        """Execute a SQL query against a data source."""
        url = f"{self.host}{self.api_v1}/data_sources/{data_source_id}/query"

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            self.auth.apply_to_client(client)
            response = await client.post(url, json={"query": query})

            if response.status_code == 404:
                msg = f"Data source {data_source_id} not found."
                logger.error(msg)
                raise DataSourceNotFoundError(
                    msg,
                    status_code=404,
                )
            self._check_response(
                response, context=f"query execution for data source {data_source_id}"
            )
            return QueryResult.model_validate(response.json())

    # DataDiffs
    async def create_datadiff(
        self,
        data_source1_id: int,
        data_source2_id: int,
        pk_columns: list[str],
        table1: list[str] | None = None,
        table2: list[str] | None = None,
        query1: str | None = None,
        query2: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Create a new DataDiff comparison."""
        if (table1 is None) == (query1 is None):
            raise ValueError(
                "Exactly one of table1 or query1 must be provided, not both or neither"
            )

        if (table2 is None) == (query2 is None):
            raise ValueError(
                "Exactly one of table2 or query2 must be provided, not both or neither"
            )

        payload: dict[str, Any] = {
            "data_source1_id": data_source1_id,
            "data_source2_id": data_source2_id,
            "pk_columns": pk_columns,
        }

        if table1:
            payload["table1"] = table1
        if table2:
            payload["table2"] = table2
        if query1:
            payload["query1"] = query1
        if query2:
            payload["query2"] = query2

        payload.update(kwargs)

        return await self._request("POST", "/datadiffs", json=payload)

    async def get_datadiff(self, diff_id: int) -> dict[str, Any]:
        """Get DataDiff status and details."""
        return await self._request("GET", f"/datadiffs/{diff_id}")

    async def get_datadiff_summary(self, diff_id: int) -> dict[str, Any]:
        """Get human-readable DataDiff summary with feedback."""
        return await self._request("GET", f"/datadiffs/{diff_id}/summary")
