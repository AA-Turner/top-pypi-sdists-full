"""
Workflows API Client for Aigie SDK.

Provides access to workflow definitions, executions, statistics,
and sandbox testing capabilities.
"""

import os
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

import httpx


@dataclass
class WorkflowDefinition:
    """Workflow definition with statistics."""

    id: str
    agent_name: str
    signature: str
    node_sequence: list[str] = field(default_factory=list)
    node_sequence_str: str | None = None
    node_count: int = 0
    display_name: str | None = None
    description: str | None = None
    first_seen_at: str | None = None
    last_seen_at: str | None = None
    execution_count: int = 0
    successful_count: int = 0
    failed_count: int = 0
    success_rate: float = 0.0
    avg_duration_seconds: float = 0.0
    presented_name: str | None = None
    workflow_number: int | None = None
    autonomous_enabled: bool = False
    autonomous_reason: str | None = None


@dataclass
class WorkflowExecution:
    """Single workflow execution (trace)."""

    id: str
    name: str
    status: str
    start_time: str
    end_time: str | None = None
    duration_seconds: float = 0.0
    error_message: str | None = None
    error_type: str | None = None
    total_cost: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class WorkflowStats:
    """Aggregated workflow statistics."""

    total_definitions: int
    unique_agents: int
    total_executions: int
    successful_executions: int
    failed_executions: int
    success_rate: float
    avg_node_count: float
    max_node_count: int
    time_window_hours: int
    calculated_at: str


@dataclass
class SandboxTest:
    """Sandbox test record."""

    id: str
    workflow_definition_id: str
    original_trace_id: str
    span_id: str | None = None
    span_name: str | None = None
    error_type: str | None = None
    original_error: str | None = None
    result: str = "pending"  # pending, success, failed
    strategy_type: str | None = None
    suggestion_applied: dict[str, Any] = field(default_factory=dict)
    result_details: dict[str, Any] = field(default_factory=dict)
    created_at: str | None = None
    executed_at: str | None = None


@dataclass
class ProjectedSuccess:
    """Projected success rate analysis."""

    workflow_definition_id: str
    current_success_rate: float
    projected_success_rate: float
    confidence: str  # high, medium, low, estimated
    validated: dict[str, Any] = field(default_factory=dict)
    estimated: dict[str, Any] = field(default_factory=dict)


class WorkflowsClient:
    """
    Workflows API client for Aigie.

    Provides methods for managing workflow definitions, retrieving executions,
    and running sandbox tests.

    Example:
        >>> from aigie.workflows import WorkflowsClient
        >>>
        >>> async with WorkflowsClient() as client:
        ...     # List workflow definitions
        ...     workflows, total = await client.list_workflows(limit=10)
        ...     for wf in workflows:
        ...         print(f"{wf.display_name}: {wf.success_rate}% success rate")
        ...
        ...     # Get workflow stats
        ...     stats = await client.get_stats(hours=168)
        ...     print(f"Total workflows: {stats.total_definitions}")
    """

    def __init__(
        self,
        api_url: str | None = None,
        api_key: str | None = None,
    ):
        """
        Initialize workflows client.

        Args:
            api_url: API URL (defaults to AIGIE_API_URL env var)
            api_key: API key (defaults to AIGIE_API_KEY env var)
        """
        self.api_url = api_url or os.getenv("AIGIE_API_URL", "")
        self.api_key = api_key or os.getenv("AIGIE_API_KEY", "")
        self.client = httpx.AsyncClient(timeout=60.0)

    async def list_workflows(
        self,
        agent_name: str | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> tuple[list[WorkflowDefinition], int]:
        """
        List all workflow definitions with statistics.

        Args:
            agent_name: Filter by agent name
            limit: Maximum results (default 100, max 500)
            offset: Pagination offset

        Returns:
            Tuple of (workflow_definitions, total_count)
        """
        params = {"limit": limit, "offset": offset}
        if agent_name:
            params["agent_name"] = agent_name

        response = await self._request("GET", "/v1/workflows/definitions", params=params)

        workflows = [self._parse_workflow(w) for w in response.get("workflow_definitions", [])]

        return workflows, response.get("total", len(workflows))

    async def get_workflow(
        self,
        workflow_id: str,
    ) -> WorkflowDefinition:
        """
        Get a specific workflow definition with details.

        Args:
            workflow_id: Workflow definition ID

        Returns:
            WorkflowDefinition with statistics
        """
        response = await self._request("GET", f"/v1/workflows/definitions/{workflow_id}")

        return self._parse_workflow(response.get("workflow_definition", response))

    async def get_workflow_executions(
        self,
        workflow_id: str,
        limit: int = 50,
        offset: int = 0,
    ) -> tuple[list[WorkflowExecution], int]:
        """
        Get executions for a workflow definition.

        Args:
            workflow_id: Workflow definition ID
            limit: Maximum results (default 50, max 200)
            offset: Pagination offset

        Returns:
            Tuple of (executions, total_count)
        """
        params = {"limit": limit, "offset": offset}
        response = await self._request(
            "GET",
            f"/v1/workflows/definitions/{workflow_id}/executions",
            params=params,
        )

        executions = [
            WorkflowExecution(
                id=e.get("id", ""),
                name=e.get("name", ""),
                status=e.get("status", ""),
                start_time=e.get("start_time", ""),
                end_time=e.get("end_time"),
                duration_seconds=e.get("duration_seconds", 0.0),
                error_message=e.get("error_message"),
                error_type=e.get("error_type"),
                total_cost=e.get("total_cost", 0.0),
                metadata=e.get("metadata", {}),
            )
            for e in response.get("executions", [])
        ]

        return executions, response.get("total", len(executions))

    async def get_stats(
        self,
        hours: int = 168,
    ) -> WorkflowStats:
        """
        Get aggregated workflow statistics.

        Args:
            hours: Hours to look back (default 168 = 7 days)

        Returns:
            WorkflowStats with aggregated metrics
        """
        params = {"hours": hours}
        response = await self._request("GET", "/v1/workflows/stats", params=params)

        stats = response.get("stats", response)
        return WorkflowStats(
            total_definitions=stats.get("total_definitions", 0),
            unique_agents=stats.get("unique_agents", 0),
            total_executions=stats.get("total_executions", 0),
            successful_executions=stats.get("successful_executions", 0),
            failed_executions=stats.get("failed_executions", 0),
            success_rate=stats.get("success_rate", 0.0),
            avg_node_count=stats.get("avg_node_count", 0.0),
            max_node_count=stats.get("max_node_count", 0),
            time_window_hours=response.get("time_window_hours", hours),
            calculated_at=response.get("calculated_at", datetime.utcnow().isoformat()),
        )

    async def update_workflow(
        self,
        workflow_id: str,
        presented_name: str | None = None,
        autonomous_enabled: bool | None = None,
        autonomous_reason: str | None = None,
    ) -> dict[str, Any]:
        """
        Update workflow definition settings.

        Args:
            workflow_id: Workflow definition ID
            presented_name: User-friendly display name
            autonomous_enabled: Enable/disable autonomous remediation
            autonomous_reason: Reason for enabling/disabling

        Returns:
            Updated workflow data
        """
        data = {}
        if presented_name is not None:
            data["presented_name"] = presented_name
        if autonomous_enabled is not None:
            data["autonomous_enabled"] = autonomous_enabled
        if autonomous_reason is not None:
            data["autonomous_reason"] = autonomous_reason

        return await self._request(
            "PATCH",
            f"/v1/workflows/definitions/{workflow_id}",
            json=data,
        )

    async def generate_workflow_name(
        self,
        workflow_id: str,
    ) -> dict[str, Any]:
        """
        Generate a presented name for a workflow.

        Args:
            workflow_id: Workflow definition ID

        Returns:
            Generated name details
        """
        return await self._request(
            "POST",
            f"/v1/workflows/definitions/{workflow_id}/generate-name",
        )

    async def get_projected_success(
        self,
        workflow_id: str,
    ) -> ProjectedSuccess:
        """
        Get projected success rate with remediation.

        Args:
            workflow_id: Workflow definition ID

        Returns:
            ProjectedSuccess analysis
        """
        response = await self._request(
            "GET",
            f"/v1/workflows/definitions/{workflow_id}/projected-success",
        )

        return ProjectedSuccess(
            workflow_definition_id=workflow_id,
            current_success_rate=response.get("current_success_rate", 0.0),
            projected_success_rate=response.get("projected_success_rate", 0.0),
            confidence=response.get("confidence", "estimated"),
            validated=response.get("validated", {}),
            estimated=response.get("estimated", {}),
        )

    async def get_sandbox_tests(
        self,
        workflow_id: str,
        result_filter: str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> tuple[list[SandboxTest], dict[str, Any]]:
        """
        Get sandbox test results for a workflow.

        Args:
            workflow_id: Workflow definition ID
            result_filter: Filter by result (success, failed, pending)
            limit: Maximum results
            offset: Pagination offset

        Returns:
            Tuple of (tests, stats)
        """
        params = {"limit": limit, "offset": offset}
        if result_filter:
            params["result_filter"] = result_filter

        response = await self._request(
            "GET",
            f"/v1/workflows/definitions/{workflow_id}/sandbox-tests",
            params=params,
        )

        tests = [
            SandboxTest(
                id=t.get("id", ""),
                workflow_definition_id=t.get("workflow_definition_id", workflow_id),
                original_trace_id=t.get("original_trace_id", ""),
                span_id=t.get("span_id"),
                span_name=t.get("span_name"),
                error_type=t.get("error_type"),
                original_error=t.get("original_error"),
                result=t.get("result", "pending"),
                strategy_type=t.get("strategy_type"),
                suggestion_applied=t.get("suggestion_applied", {}),
                result_details=t.get("result_details", {}),
                created_at=t.get("created_at"),
                executed_at=t.get("executed_at"),
            )
            for t in response.get("sandbox_tests", [])
        ]

        return tests, response.get("stats", {})

    async def run_sandbox_test(
        self,
        workflow_id: str,
        trace_id: str,
        span_id: str | None = None,
        suggestion: dict[str, Any] | None = None,
        execute_immediately: bool = True,
    ) -> dict[str, Any]:
        """
        Run a sandbox test for a specific failure.

        Args:
            workflow_id: Workflow definition ID
            trace_id: Original trace ID
            span_id: Optional span ID
            suggestion: Optional remediation suggestion
            execute_immediately: Execute now vs queue (default True)

        Returns:
            Sandbox test result
        """
        data = {
            "trace_id": trace_id,
            "execute_immediately": execute_immediately,
        }
        if span_id:
            data["span_id"] = span_id
        if suggestion:
            data["suggestion"] = suggestion

        return await self._request(
            "POST",
            f"/v1/workflows/definitions/{workflow_id}/run-sandbox-test",
            json=data,
        )

    async def get_untested_failures(
        self,
        workflow_id: str,
        limit: int = 20,
    ) -> list[dict[str, Any]]:
        """
        Get failed traces without sandbox tests.

        Args:
            workflow_id: Workflow definition ID
            limit: Maximum results

        Returns:
            List of untested failures
        """
        params = {"limit": limit}
        response = await self._request(
            "GET",
            f"/v1/workflows/definitions/{workflow_id}/untested-failures",
            params=params,
        )

        return response.get("untested_failures", [])

    async def process_sandbox_tests(
        self,
        workflow_id: str,
        auto_discover: bool = True,
        max_tests: int = 20,
    ) -> dict[str, Any]:
        """
        Process pending sandbox tests.

        Args:
            workflow_id: Workflow definition ID
            auto_discover: Auto-discover new failures
            max_tests: Maximum tests to process

        Returns:
            Processing results
        """
        params = {"auto_discover": auto_discover, "max_tests": max_tests}
        return await self._request(
            "POST",
            f"/v1/workflows/definitions/{workflow_id}/process-sandbox-tests",
            params=params,
        )

    async def backfill_workflows(
        self,
        limit: int = 1000,
    ) -> dict[str, Any]:
        """
        Backfill workflow definitions from existing traces.

        Args:
            limit: Maximum traces to process

        Returns:
            Backfill results with processed/created counts
        """
        params = {"limit": limit}
        return await self._request("POST", "/v1/workflows/backfill", params=params)

    def _parse_workflow(self, data: dict[str, Any]) -> WorkflowDefinition:
        """Parse workflow definition from API response."""
        return WorkflowDefinition(
            id=data.get("id", ""),
            agent_name=data.get("agent_name", ""),
            signature=data.get("signature", ""),
            node_sequence=data.get("node_sequence", []),
            node_sequence_str=data.get("node_sequence_str"),
            node_count=data.get("node_count", 0),
            display_name=data.get("display_name"),
            description=data.get("description"),
            first_seen_at=data.get("first_seen_at"),
            last_seen_at=data.get("last_seen_at"),
            execution_count=data.get("execution_count", 0),
            successful_count=data.get("successful_count", 0),
            failed_count=data.get("failed_count", 0),
            success_rate=data.get("success_rate", 0.0),
            avg_duration_seconds=data.get("avg_duration_seconds", 0.0),
            presented_name=data.get("presented_name"),
            workflow_number=data.get("workflow_number"),
            autonomous_enabled=data.get("autonomous_enabled", False),
            autonomous_reason=data.get("autonomous_reason"),
        )

    async def _request(
        self,
        method: str,
        path: str,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
    ) -> Any:
        """Make HTTP request to API."""
        url = f"{self.api_url}{path}"

        headers = {
            "Content-Type": "application/json",
            "X-API-Key": self.api_key,
        }

        try:
            response = await self.client.request(
                method=method,
                url=url,
                params=params,
                json=json,
                headers=headers,
            )

            response.raise_for_status()
            return response.json()

        except httpx.HTTPError as error:
            import logging

            logging.getLogger(__name__).error(f"Workflows API Error [{method} {path}]: {error}")
            raise

    async def close(self):
        """Close HTTP client."""
        await self.client.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
