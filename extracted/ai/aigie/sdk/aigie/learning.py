"""
Learning API Client for Aigie SDK.

Provides access to continuous learning services, pattern detection,
feedback submission, and eval statistics.
"""

import os
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

import httpx


@dataclass
class LearningStats:
    """Overall learning service statistics."""

    total_patterns: int
    active_patterns: int
    feedback_count: int
    eval_count: int
    accuracy_rate: float
    patterns_by_type: dict[str, int] = field(default_factory=dict)
    calculated_at: str = ""


@dataclass
class LearningPattern:
    """A learned pattern from continuous learning."""

    id: str
    pattern_type: str  # error_pattern, success_pattern, workflow_pattern
    signature: str
    confidence: float
    occurrence_count: int
    last_seen: str | None = None
    first_seen: str | None = None
    enabled: bool = True
    remediation_strategy: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class FeedbackEntry:
    """Feedback entry for a trace/remediation."""

    id: str
    trace_id: str
    remediation_id: str | None = None
    was_helpful: bool = False
    user_comment: str | None = None
    submitted_at: str = ""
    submitted_by: str | None = None


@dataclass
class EvalStats:
    """Evaluation statistics."""

    total_evals: int
    passed: int
    failed: int
    pass_rate: float
    avg_confidence: float
    evals_by_judge: dict[str, int] = field(default_factory=dict)
    evals_over_time: list[dict[str, Any]] = field(default_factory=list)


class LearningClient:
    """
    Learning API client for Aigie.

    Provides methods for accessing the continuous learning service,
    pattern management, and feedback submission.

    Example:
        >>> from aigie.learning import LearningClient
        >>>
        >>> async with LearningClient() as client:
        ...     # Get learning stats
        ...     stats = await client.get_stats()
        ...     print(f"Total patterns: {stats.total_patterns}")
        ...
        ...     # List patterns
        ...     patterns, total = await client.list_patterns()
        ...     for pattern in patterns:
        ...         print(f"{pattern.pattern_type}: {pattern.signature}")
    """

    def __init__(
        self,
        api_url: str | None = None,
        api_key: str | None = None,
    ):
        """
        Initialize learning client.

        Args:
            api_url: API URL (defaults to AIGIE_API_URL env var)
            api_key: API key (defaults to AIGIE_API_KEY env var)
        """
        self.api_url = api_url or os.getenv("AIGIE_API_URL", "")
        self.api_key = api_key or os.getenv("AIGIE_API_KEY", "")
        self.client = httpx.AsyncClient(timeout=60.0)

    async def get_stats(self) -> LearningStats:
        """
        Get overall learning service statistics.

        Returns:
            LearningStats with pattern and feedback statistics
        """
        response = await self._request("GET", "/v1/learning/stats")

        return LearningStats(
            total_patterns=response.get("total_patterns", 0),
            active_patterns=response.get("active_patterns", 0),
            feedback_count=response.get("feedback_count", 0),
            eval_count=response.get("eval_count", 0),
            accuracy_rate=response.get("accuracy_rate", 0.0),
            patterns_by_type=response.get("patterns_by_type", {}),
            calculated_at=response.get("calculated_at", datetime.utcnow().isoformat()),
        )

    async def list_patterns(
        self,
        pattern_type: str | None = None,
        enabled_only: bool = True,
        limit: int = 100,
        offset: int = 0,
    ) -> tuple[list[LearningPattern], int]:
        """
        List learned patterns.

        Args:
            pattern_type: Filter by pattern type
            enabled_only: Only return enabled patterns
            limit: Maximum results
            offset: Pagination offset

        Returns:
            Tuple of (patterns, total_count)
        """
        params = {"limit": limit, "offset": offset, "enabled_only": enabled_only}
        if pattern_type:
            params["pattern_type"] = pattern_type

        response = await self._request("GET", "/v1/learning/patterns", params=params)

        patterns = [
            LearningPattern(
                id=p.get("id", ""),
                pattern_type=p.get("pattern_type", ""),
                signature=p.get("signature", ""),
                confidence=p.get("confidence", 0.0),
                occurrence_count=p.get("occurrence_count", 0),
                last_seen=p.get("last_seen"),
                first_seen=p.get("first_seen"),
                enabled=p.get("enabled", True),
                remediation_strategy=p.get("remediation_strategy"),
                metadata=p.get("metadata", {}),
            )
            for p in response.get("patterns", [])
        ]

        return patterns, response.get("total", len(patterns))

    async def get_pattern(self, pattern_id: str) -> LearningPattern:
        """
        Get a specific pattern.

        Args:
            pattern_id: Pattern ID

        Returns:
            LearningPattern details
        """
        response = await self._request("GET", f"/v1/learning/patterns/{pattern_id}")

        return LearningPattern(
            id=response.get("id", pattern_id),
            pattern_type=response.get("pattern_type", ""),
            signature=response.get("signature", ""),
            confidence=response.get("confidence", 0.0),
            occurrence_count=response.get("occurrence_count", 0),
            last_seen=response.get("last_seen"),
            first_seen=response.get("first_seen"),
            enabled=response.get("enabled", True),
            remediation_strategy=response.get("remediation_strategy"),
            metadata=response.get("metadata", {}),
        )

    async def enable_pattern(self, pattern_id: str) -> dict[str, Any]:
        """
        Enable a pattern for autonomous remediation.

        Args:
            pattern_id: Pattern ID

        Returns:
            Update result
        """
        return await self._request("POST", f"/v1/learning/patterns/{pattern_id}/enable")

    async def disable_pattern(self, pattern_id: str) -> dict[str, Any]:
        """
        Disable a pattern.

        Args:
            pattern_id: Pattern ID

        Returns:
            Update result
        """
        return await self._request("POST", f"/v1/learning/patterns/{pattern_id}/disable")

    async def submit_feedback(
        self,
        trace_id: str,
        was_helpful: bool,
        remediation_id: str | None = None,
        comment: str | None = None,
    ) -> FeedbackEntry:
        """
        Submit feedback for a trace or remediation.

        Args:
            trace_id: Trace ID
            was_helpful: Whether the output/remediation was helpful
            remediation_id: Optional remediation ID
            comment: Optional user comment

        Returns:
            Created FeedbackEntry
        """
        data = {
            "trace_id": trace_id,
            "was_helpful": was_helpful,
        }
        if remediation_id:
            data["remediation_id"] = remediation_id
        if comment:
            data["comment"] = comment

        response = await self._request("POST", "/v1/learning/feedback", json=data)

        return FeedbackEntry(
            id=response.get("id", ""),
            trace_id=trace_id,
            remediation_id=remediation_id,
            was_helpful=was_helpful,
            user_comment=comment,
            submitted_at=response.get("submitted_at", datetime.utcnow().isoformat()),
        )

    async def get_feedback(
        self,
        trace_id: str | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> tuple[list[FeedbackEntry], int]:
        """
        Get feedback entries.

        Args:
            trace_id: Optional filter by trace ID
            limit: Maximum results
            offset: Pagination offset

        Returns:
            Tuple of (feedback_entries, total_count)
        """
        params = {"limit": limit, "offset": offset}
        if trace_id:
            params["trace_id"] = trace_id

        response = await self._request("GET", "/v1/learning/feedback", params=params)

        entries = [
            FeedbackEntry(
                id=f.get("id", ""),
                trace_id=f.get("trace_id", ""),
                remediation_id=f.get("remediation_id"),
                was_helpful=f.get("was_helpful", False),
                user_comment=f.get("comment"),
                submitted_at=f.get("submitted_at", ""),
                submitted_by=f.get("submitted_by"),
            )
            for f in response.get("feedback", [])
        ]

        return entries, response.get("total", len(entries))

    async def get_eval_stats(
        self,
        hours: int = 168,
    ) -> EvalStats:
        """
        Get evaluation statistics.

        Args:
            hours: Hours to analyze (default 7 days)

        Returns:
            EvalStats with evaluation metrics
        """
        params = {"hours": hours}
        response = await self._request("GET", "/v1/learning/eval/stats", params=params)

        return EvalStats(
            total_evals=response.get("total_evals", 0),
            passed=response.get("passed", 0),
            failed=response.get("failed", 0),
            pass_rate=response.get("pass_rate", 0.0),
            avg_confidence=response.get("avg_confidence", 0.0),
            evals_by_judge=response.get("evals_by_judge", {}),
            evals_over_time=response.get("evals_over_time", []),
        )

    async def trigger_learning(
        self,
        force: bool = False,
    ) -> dict[str, Any]:
        """
        Trigger a learning cycle.

        Args:
            force: Force learning even if recent data is cached

        Returns:
            Learning cycle result
        """
        data = {"force": force}
        return await self._request("POST", "/v1/learning/trigger", json=data)

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

            logging.getLogger(__name__).error(f"Learning API Error [{method} {path}]: {error}")
            raise

    async def close(self):
        """Close HTTP client."""
        await self.client.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
