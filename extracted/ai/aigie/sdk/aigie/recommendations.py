"""
Recommendations API Client for Aigie SDK.

Provides access to remediation recommendations, impact analysis,
and what-if analysis for autonomous mode.
"""

import os
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

import httpx


@dataclass
class RemediationAction:
    """Suggested remediation action."""

    action_type: str  # retry, fallback, log, etc.
    description: str
    expected_outcome: str
    confidence: float = 0.0
    parameters: dict[str, Any] = field(default_factory=dict)


@dataclass
class FailureRecommendation:
    """Recommendation for a specific failure."""

    span_id: str
    span_name: str
    error_type: str
    error_message: str
    detected: bool
    actions: list[RemediationAction] = field(default_factory=list)
    historical_context: dict[str, Any] = field(default_factory=dict)


@dataclass
class TraceRecommendation:
    """Recommendations for a trace."""

    trace_id: str
    trace_name: str
    status: str
    failure_recommendations: list[FailureRecommendation] = field(default_factory=list)
    summary: str = ""
    generated_at: str = ""


@dataclass
class WorkflowRecommendation:
    """Recommendations for a workflow."""

    workflow_definition_id: str
    agent_name: str
    failure_analysis: list[dict[str, Any]] = field(default_factory=list)
    recommended_strategies: list[dict[str, Any]] = field(default_factory=list)
    estimated_impact: dict[str, Any] = field(default_factory=dict)
    summary: str = ""


@dataclass
class ImpactAnalysis:
    """Impact analysis for autonomous mode."""

    analysis_period_hours: int
    current_state: dict[str, Any] = field(default_factory=dict)
    with_autonomous_mode: dict[str, Any] = field(default_factory=dict)
    impact_summary: dict[str, Any] = field(default_factory=dict)
    failure_breakdown: list[dict[str, Any]] = field(default_factory=list)
    most_affected_workflows: list[dict[str, Any]] = field(default_factory=list)
    calculated_at: str = ""


@dataclass
class WhatIfTimeline:
    """Single step in what-if timeline."""

    span_id: str
    name: str
    type: str
    status: str
    start_time: str | None = None
    end_time: str | None = None
    duration_ms: float = 0.0
    error: str | None = None
    error_type: str | None = None
    autonomous_would_have: dict[str, Any] = field(default_factory=dict)


@dataclass
class WhatIfResult:
    """What-if analysis result."""

    trace_id: str
    trace_name: str
    original_outcome: dict[str, Any] = field(default_factory=dict)
    timeline: list[WhatIfTimeline] = field(default_factory=list)
    what_if_outcome: dict[str, Any] = field(default_factory=dict)
    summary: str = ""
    generated_at: str = ""


class RecommendationsClient:
    """
    Recommendations API client for Aigie.

    Provides methods for getting remediation recommendations, analyzing
    autonomous mode impact, and performing what-if analysis.

    Example:
        >>> from aigie.recommendations import RecommendationsClient
        >>>
        >>> async with RecommendationsClient() as client:
        ...     # Get recommendations for a failed trace
        ...     rec = await client.get_trace_recommendations("trace-123")
        ...     for failure in rec.failure_recommendations:
        ...         print(f"{failure.span_name}: {failure.actions[0].description}")
        ...
        ...     # Get impact analysis
        ...     impact = await client.get_impact_analysis(hours=168)
        ...     print(f"Potential improvement: {impact.impact_summary['success_rate_lift']}")
    """

    def __init__(
        self,
        api_url: str | None = None,
        api_key: str | None = None,
    ):
        """
        Initialize recommendations client.

        Args:
            api_url: API URL (defaults to AIGIE_API_URL env var)
            api_key: API key (defaults to AIGIE_API_KEY env var)
        """
        self.api_url = api_url or os.getenv("AIGIE_API_URL", "")
        self.api_key = api_key or os.getenv("AIGIE_API_KEY", "")
        self.client = httpx.AsyncClient(timeout=60.0)

    async def get_trace_recommendations(
        self,
        trace_id: str,
    ) -> TraceRecommendation:
        """
        Get recommendations for a specific trace.

        Shows exactly what autonomous mode would have done:
        - Which failures would have been caught
        - What actions would have been taken
        - Expected success rate for each action
        - Historical context from similar errors

        Args:
            trace_id: Trace ID to analyze

        Returns:
            TraceRecommendation with detailed recommendations
        """
        response = await self._request("GET", f"/v1/recommendations/trace/{trace_id}")

        failure_recs = []
        for f in response.get("failure_recommendations", response.get("recommendations", [])):
            actions = [
                RemediationAction(
                    action_type=a.get("action_type", a.get("action", "")),
                    description=a.get("description", ""),
                    expected_outcome=a.get("expected_outcome", ""),
                    confidence=a.get("confidence", 0.0),
                    parameters=a.get("parameters", {}),
                )
                for a in f.get("actions", f.get("suggested_actions", []))
            ]

            failure_recs.append(
                FailureRecommendation(
                    span_id=f.get("span_id", ""),
                    span_name=f.get("span_name", f.get("name", "")),
                    error_type=f.get("error_type", ""),
                    error_message=f.get("error_message", f.get("error", "")),
                    detected=f.get("detected", True),
                    actions=actions,
                    historical_context=f.get("historical_context", {}),
                )
            )

        return TraceRecommendation(
            trace_id=trace_id,
            trace_name=response.get("trace_name", ""),
            status=response.get("status", ""),
            failure_recommendations=failure_recs,
            summary=response.get("summary", ""),
            generated_at=response.get("generated_at", datetime.utcnow().isoformat()),
        )

    async def get_workflow_recommendations(
        self,
        workflow_id: str,
    ) -> WorkflowRecommendation:
        """
        Get recommendations for a workflow definition.

        Analyzes:
        - Most common failure points in the workflow
        - Recommended strategies for each failure type
        - Estimated impact of enabling autonomous mode

        Args:
            workflow_id: Workflow definition ID

        Returns:
            WorkflowRecommendation with analysis
        """
        response = await self._request("GET", f"/v1/recommendations/workflow/{workflow_id}")

        return WorkflowRecommendation(
            workflow_definition_id=workflow_id,
            agent_name=response.get("agent_name", ""),
            failure_analysis=response.get("failure_analysis", []),
            recommended_strategies=response.get("recommended_strategies", []),
            estimated_impact=response.get("estimated_impact", {}),
            summary=response.get("summary", ""),
        )

    async def get_dashboard(
        self,
        hours: int = 24,
        limit: int = 20,
    ) -> dict[str, Any]:
        """
        Get recommendations dashboard overview.

        Shows:
        - Summary of recent failures
        - What autonomous mode could have prevented
        - High-impact improvement opportunities
        - Estimated success rate improvement

        Args:
            hours: Hours to analyze (default 24)
            limit: Max recent failures to show

        Returns:
            Dashboard data with recommendations
        """
        params = {"hours": hours, "limit": limit}
        return await self._request("GET", "/v1/recommendations/dashboard", params=params)

    async def get_impact_analysis(
        self,
        hours: int = 168,
    ) -> ImpactAnalysis:
        """
        Calculate the potential impact of enabling autonomous mode.

        This is the key metric showing users what they would gain:
        - How many failures could have been prevented
        - What the new success rate would be
        - Cost savings from avoided failures
        - Time savings from automatic remediation

        Args:
            hours: Hours to analyze (default 168 = 7 days)

        Returns:
            ImpactAnalysis with detailed impact metrics
        """
        params = {"hours": hours}
        response = await self._request("GET", "/v1/recommendations/impact", params=params)

        return ImpactAnalysis(
            analysis_period_hours=response.get("analysis_period", {}).get("hours", hours),
            current_state=response.get("current_state", {}),
            with_autonomous_mode=response.get("with_autonomous_mode", {}),
            impact_summary=response.get("impact_summary", {}),
            failure_breakdown=response.get("failure_breakdown", []),
            most_affected_workflows=response.get("most_affected_workflows", []),
            calculated_at=response.get("calculated_at", datetime.utcnow().isoformat()),
        )

    async def get_whatif_analysis(
        self,
        trace_id: str,
    ) -> WhatIfResult:
        """
        Detailed what-if analysis for a specific trace.

        Shows step-by-step:
        1. Original execution flow
        2. Where failures occurred
        3. What autonomous mode would have detected
        4. What actions would have been taken
        5. Expected outcome

        Args:
            trace_id: Trace ID to analyze

        Returns:
            WhatIfResult with detailed timeline
        """
        response = await self._request("GET", f"/v1/recommendations/what-if/{trace_id}")

        timeline = [
            WhatIfTimeline(
                span_id=t.get("span_id", ""),
                name=t.get("name", ""),
                type=t.get("type", ""),
                status=t.get("status", ""),
                start_time=t.get("start_time"),
                end_time=t.get("end_time"),
                duration_ms=t.get("duration_ms", 0.0),
                error=t.get("error"),
                error_type=t.get("error_type"),
                autonomous_would_have=t.get("autonomous_would_have", {}),
            )
            for t in response.get("timeline", [])
        ]

        return WhatIfResult(
            trace_id=trace_id,
            trace_name=response.get("trace_name", ""),
            original_outcome=response.get("original_outcome", {}),
            timeline=timeline,
            what_if_outcome=response.get("what_if_outcome", {}),
            summary=response.get("summary", ""),
            generated_at=response.get("generated_at", datetime.utcnow().isoformat()),
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

            logging.getLogger(__name__).error(
                f"Recommendations API Error [{method} {path}]: {error}"
            )
            raise

    async def close(self):
        """Close HTTP client."""
        await self.client.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
