"""
Analytics API Client for Aigie SDK.

Provides access to dashboard analytics, time series data, error clustering,
cost tracking, and other analytics endpoints.
"""

import os
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

import httpx


@dataclass
class DashboardStats:
    """Dashboard statistics."""

    total_executions: int
    successful_executions: int
    failed_executions: int
    success_rate: float
    failure_rate: float
    avg_response_time_seconds: float
    total_cost: float
    unique_agents: int
    recent_activity: int
    total_spans: int
    time_window_hours: int
    calculated_at: str


@dataclass
class TimeSeriesPoint:
    """Single time series data point."""

    timestamp: str
    total: int
    successful: int
    failed: int
    avg_duration_seconds: float


@dataclass
class ErrorCluster:
    """Error cluster information."""

    cluster_id: str
    pattern: str
    error_type: str
    count: int
    first_seen: str
    last_seen: str
    sample_errors: list[dict[str, Any]] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class WorkflowStats:
    """Workflow statistics."""

    workflow_name: str
    total_executions: int
    successful: int
    failed: int
    success_rate: float
    avg_duration_seconds: float
    total_cost: float


@dataclass
class CostAnalytics:
    """Cost and token analytics."""

    total_cost: float
    total_input_tokens: int
    total_output_tokens: int
    total_tokens: int
    cost_by_model: dict[str, float] = field(default_factory=dict)
    cost_over_time: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class ErrorSummary:
    """Error analytics summary."""

    total_errors: int
    unique_error_types: int
    error_breakdown: list[dict[str, Any]] = field(default_factory=list)
    top_errors: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class AgentStats:
    """Agent statistics."""

    agent_name: str
    total_executions: int
    successful: int
    failed: int
    success_rate: float
    avg_duration_seconds: float
    total_cost: float
    total_tokens: int


@dataclass
class SystemHealth:
    """System health status."""

    status: str  # healthy, degraded, unhealthy
    checks: dict[str, dict[str, Any]] = field(default_factory=dict)
    timestamp: str = ""


class AnalyticsClient:
    """
    Analytics API client for Aigie.

    Provides methods for retrieving dashboard analytics, time series data,
    error clustering, cost tracking, and system health information.

    Example:
        >>> from aigie.analytics import AnalyticsClient
        >>>
        >>> async with AnalyticsClient() as client:
        ...     # Get dashboard stats
        ...     stats = await client.get_dashboard_stats(hours=24)
        ...     print(f"Success rate: {stats.success_rate}%")
        ...
        ...     # Get time series data
        ...     points = await client.get_time_series(hours=24)
        ...     for point in points:
        ...         print(f"{point.timestamp}: {point.total} executions")
    """

    def __init__(
        self,
        api_url: str | None = None,
        api_key: str | None = None,
    ):
        """
        Initialize analytics client.

        Args:
            api_url: API URL (defaults to AIGIE_API_URL env var)
            api_key: API key (defaults to AIGIE_API_KEY env var)
        """
        self.api_url = api_url or os.getenv("AIGIE_API_URL", "")
        self.api_key = api_key or os.getenv("AIGIE_API_KEY", "")
        self.client = httpx.AsyncClient(timeout=60.0)

    async def get_dashboard_stats(
        self,
        hours: int = 72,
    ) -> DashboardStats:
        """
        Get aggregated dashboard statistics.

        Args:
            hours: Hours to look back (default 72, max 87600)

        Returns:
            DashboardStats with aggregated metrics
        """
        params = {"hours": hours}
        response = await self._request("GET", "/v1/analytics/dashboard/stats", params=params)

        return DashboardStats(
            total_executions=response.get("total_executions", 0),
            successful_executions=response.get("successful_executions", 0),
            failed_executions=response.get("failed_executions", 0),
            success_rate=response.get("success_rate", 0.0),
            failure_rate=response.get("failure_rate", 0.0),
            avg_response_time_seconds=response.get("avg_response_time_seconds", 0.0),
            total_cost=response.get("total_cost", 0.0),
            unique_agents=response.get("unique_agents", 0),
            recent_activity=response.get("recent_activity", 0),
            total_spans=response.get("total_spans", 0),
            time_window_hours=response.get("time_window_hours", hours),
            calculated_at=response.get("calculated_at", datetime.utcnow().isoformat()),
        )

    async def get_time_series(
        self,
        hours: int = 72,
        bucket_hours: int = 1,
    ) -> list[TimeSeriesPoint]:
        """
        Get time series data for metrics.

        Args:
            hours: Hours to look back (default 72)
            bucket_hours: Bucket size in hours (default 1)

        Returns:
            List of TimeSeriesPoint objects
        """
        params = {"hours": hours, "bucket_hours": bucket_hours}
        response = await self._request("GET", "/v1/analytics/time-series", params=params)

        return [
            TimeSeriesPoint(
                timestamp=p.get("timestamp", ""),
                total=p.get("total", 0),
                successful=p.get("successful", 0),
                failed=p.get("failed", 0),
                avg_duration_seconds=p.get("avg_duration_seconds", 0.0),
            )
            for p in response.get("data_points", response.get("time_series", []))
        ]

    async def get_workflow_stats(
        self,
        hours: int = 72,
        limit: int = 20,
    ) -> list[WorkflowStats]:
        """
        Get workflow statistics by type.

        Args:
            hours: Hours to look back
            limit: Maximum workflows to return

        Returns:
            List of WorkflowStats objects
        """
        params = {"hours": hours, "limit": limit}
        response = await self._request("GET", "/v1/analytics/workflows/stats", params=params)

        return [
            WorkflowStats(
                workflow_name=w.get("workflow_name", w.get("name", "")),
                total_executions=w.get("total_executions", w.get("count", 0)),
                successful=w.get("successful", 0),
                failed=w.get("failed", 0),
                success_rate=w.get("success_rate", 0.0),
                avg_duration_seconds=w.get("avg_duration_seconds", 0.0),
                total_cost=w.get("total_cost", 0.0),
            )
            for w in response.get("workflows", [])
        ]

    async def get_error_summary(
        self,
        hours: int = 72,
        limit: int = 20,
    ) -> ErrorSummary:
        """
        Get error analytics summary.

        Args:
            hours: Hours to look back
            limit: Maximum error types to return

        Returns:
            ErrorSummary with error analytics
        """
        params = {"hours": hours, "limit": limit}
        response = await self._request("GET", "/v1/analytics/errors/summary", params=params)

        return ErrorSummary(
            total_errors=response.get("total_errors", 0),
            unique_error_types=response.get("unique_error_types", 0),
            error_breakdown=response.get("error_breakdown", []),
            top_errors=response.get("top_errors", []),
        )

    async def get_error_clusters(
        self,
        hours: int = 72,
        limit: int = 50,
    ) -> list[ErrorCluster]:
        """
        Get error clusters.

        Args:
            hours: Hours to look back
            limit: Maximum clusters to return

        Returns:
            List of ErrorCluster objects
        """
        params = {"hours": hours, "limit": limit}
        response = await self._request("GET", "/v1/analytics/errors/clusters", params=params)

        return [
            ErrorCluster(
                cluster_id=c.get("cluster_id", c.get("id", "")),
                pattern=c.get("pattern", ""),
                error_type=c.get("error_type", ""),
                count=c.get("count", 0),
                first_seen=c.get("first_seen", ""),
                last_seen=c.get("last_seen", ""),
                sample_errors=c.get("sample_errors", []),
                metadata=c.get("metadata", {}),
            )
            for c in response.get("clusters", [])
        ]

    async def cluster_errors(
        self,
        hours: int = 24,
        min_cluster_size: int = 2,
        similarity_threshold: float = 0.7,
    ) -> dict[str, Any]:
        """
        Run error clustering analysis.

        Args:
            hours: Hours to analyze
            min_cluster_size: Minimum errors per cluster
            similarity_threshold: Similarity threshold for clustering

        Returns:
            Clustering results with clusters and statistics
        """
        data = {
            "hours": hours,
            "min_cluster_size": min_cluster_size,
            "similarity_threshold": similarity_threshold,
        }
        return await self._request("POST", "/v1/analytics/errors/cluster", json=data)

    async def get_cost_analytics(
        self,
        hours: int = 72,
    ) -> CostAnalytics:
        """
        Get cost and token analytics.

        Args:
            hours: Hours to analyze

        Returns:
            CostAnalytics with cost breakdown
        """
        params = {"hours": hours}
        response = await self._request("GET", "/v1/analytics/cost/tokens", params=params)

        return CostAnalytics(
            total_cost=response.get("total_cost", 0.0),
            total_input_tokens=response.get("total_input_tokens", 0),
            total_output_tokens=response.get("total_output_tokens", 0),
            total_tokens=response.get("total_tokens", 0),
            cost_by_model=response.get("cost_by_model", {}),
            cost_over_time=response.get("cost_over_time", []),
        )

    async def get_latency_analytics(
        self,
        hours: int = 72,
    ) -> dict[str, Any]:
        """
        Get latency analytics.

        Args:
            hours: Hours to analyze

        Returns:
            Latency analytics with percentiles and breakdowns
        """
        params = {"hours": hours}
        return await self._request("GET", "/v1/analytics/latency", params=params)

    async def get_agent_stats(
        self,
        hours: int = 72,
        limit: int = 20,
    ) -> list[AgentStats]:
        """
        Get agent statistics.

        Args:
            hours: Hours to look back
            limit: Maximum agents to return

        Returns:
            List of AgentStats objects
        """
        params = {"hours": hours, "limit": limit}
        response = await self._request("GET", "/v1/analytics/agents/stats", params=params)

        return [
            AgentStats(
                agent_name=a.get("agent_name", a.get("name", "")),
                total_executions=a.get("total_executions", a.get("count", 0)),
                successful=a.get("successful", 0),
                failed=a.get("failed", 0),
                success_rate=a.get("success_rate", 0.0),
                avg_duration_seconds=a.get("avg_duration_seconds", 0.0),
                total_cost=a.get("total_cost", 0.0),
                total_tokens=a.get("total_tokens", 0),
            )
            for a in response.get("agents", [])
        ]

    async def get_tool_stats(
        self,
        hours: int = 72,
        limit: int = 20,
    ) -> list[dict[str, Any]]:
        """
        Get tool/external service statistics.

        Args:
            hours: Hours to look back
            limit: Maximum tools to return

        Returns:
            List of tool statistics
        """
        params = {"hours": hours, "limit": limit}
        response = await self._request("GET", "/v1/analytics/tools/stats", params=params)
        return response.get("tools", [])

    async def get_remediation_stats(
        self,
        hours: int = 168,
    ) -> dict[str, Any]:
        """
        Get remediation analytics.

        Args:
            hours: Hours to analyze (default 7 days)

        Returns:
            Remediation statistics
        """
        params = {"hours": hours}
        return await self._request("GET", "/v1/analytics/remediation/stats", params=params)

    async def get_system_health(self) -> SystemHealth:
        """
        Get system health status.

        Returns:
            SystemHealth with status and checks
        """
        response = await self._request("GET", "/v1/analytics/system-health")

        return SystemHealth(
            status=response.get("status", "unknown"),
            checks=response.get("checks", {}),
            timestamp=response.get("timestamp", datetime.utcnow().isoformat()),
        )

    async def get_grouped_analytics(
        self,
        hours: int = 72,
        group_by: str = "agent",
        filters: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Get grouped analytics with filters.

        Args:
            hours: Hours to analyze
            group_by: Field to group by (agent, workflow, error_type, etc.)
            filters: Additional filters

        Returns:
            Grouped analytics results
        """
        params = {"hours": hours, "group_by": group_by}
        if filters:
            params.update(filters)
        return await self._request("GET", "/v1/analytics/grouped", params=params)

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

            logging.getLogger(__name__).error(f"Analytics API Error [{method} {path}]: {error}")
            raise

    async def close(self):
        """Close HTTP client."""
        await self.client.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
