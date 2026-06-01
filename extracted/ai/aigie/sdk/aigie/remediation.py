"""
Remediation API Client for Aigie SDK.

Provides access to remediation queue, autonomous fixes, hallucination detection,
and control loop management.
"""

import os
from dataclasses import dataclass, field
from typing import Any

import httpx


@dataclass
class RemediationJob:
    """Queued remediation job."""

    job_id: str
    trace_id: str
    status: str  # queued, processing, completed, failed, cancelled
    priority: str  # high, normal, low
    error: dict[str, Any] = field(default_factory=dict)
    context: dict[str, Any] = field(default_factory=dict)
    result: dict[str, Any] | None = None
    created_at: str | None = None
    completed_at: str | None = None


@dataclass
class QueueStats:
    """Remediation queue statistics."""

    total_queued: int
    processing: int
    completed_today: int
    failed_today: int
    avg_processing_time_seconds: float
    by_priority: dict[str, int] = field(default_factory=dict)


@dataclass
class AutonomousPreview:
    """Preview of what autonomous mode would do."""

    trace_id: str
    would_remediate: bool
    strategy: str | None = None
    confidence: float = 0.0
    detected_issues: list[dict[str, Any]] = field(default_factory=list)
    suggested_actions: list[dict[str, Any]] = field(default_factory=list)
    estimated_success_rate: float = 0.0


@dataclass
class HallucinationDetection:
    """Result of hallucination detection."""

    trace_id: str
    is_hallucination: bool
    confidence: float
    evidence: list[str] = field(default_factory=list)
    suggested_remediation: str | None = None


@dataclass
class ControlLoopStatus:
    """Control loop status."""

    enabled: bool
    mode: str  # recommendation, autonomous
    patterns_active: int
    circuit_breakers_open: int
    last_action: str | None = None
    last_action_time: str | None = None


class RemediationClient:
    """
    Remediation API client for Aigie.

    Provides methods for managing remediation jobs, autonomous fixes,
    hallucination detection, and control loop management.

    Example:
        >>> from aigie.remediation import RemediationClient
        >>>
        >>> async with RemediationClient() as client:
        ...     # Queue a remediation job
        ...     job = await client.queue_job(
        ...         trace_id="trace-123",
        ...         error={"type": "API_ERROR", "message": "Rate limit exceeded"},
        ...         priority="high"
        ...     )
        ...     print(f"Job queued: {job.job_id}")
        ...
        ...     # Check status
        ...     status = await client.get_job_status(job.job_id)
        ...     print(f"Status: {status.status}")
    """

    def __init__(
        self,
        api_url: str | None = None,
        api_key: str | None = None,
    ):
        """
        Initialize remediation client.

        Args:
            api_url: API URL (defaults to AIGIE_API_URL env var)
            api_key: API key (defaults to AIGIE_API_KEY env var)
        """
        self.api_url = api_url or os.getenv("AIGIE_API_URL", "")
        self.api_key = api_key or os.getenv("AIGIE_API_KEY", "")
        self.client = httpx.AsyncClient(timeout=60.0)

    # ========== Queue Management ==========

    async def queue_job(
        self,
        trace_id: str,
        error: dict[str, Any],
        context: dict[str, Any] | None = None,
        priority: str = "normal",
    ) -> RemediationJob:
        """
        Queue a remediation job for async processing.

        Args:
            trace_id: Trace ID with error
            error: Error information (type, message)
            context: Additional context
            priority: Job priority (high, normal, low)

        Returns:
            RemediationJob with job_id
        """
        data = {
            "trace_id": trace_id,
            "error": error,
            "context": context or {},
            "priority": priority,
        }

        response = await self._request("POST", "/v1/remediation/queue", json=data)

        return RemediationJob(
            job_id=response.get("job_id", ""),
            trace_id=trace_id,
            status=response.get("status", "queued"),
            priority=priority,
            error=error,
            context=context or {},
        )

    async def queue_batch(
        self,
        jobs: list[dict[str, Any]],
        priority: str = "normal",
    ) -> list[RemediationJob]:
        """
        Queue multiple remediation jobs.

        Args:
            jobs: List of job dicts with trace_id, error, context
            priority: Default priority for all jobs

        Returns:
            List of RemediationJob objects
        """
        data = {
            "jobs": jobs,
            "priority": priority,
        }

        response = await self._request("POST", "/v1/remediation/queue/batch", json=data)

        return [
            RemediationJob(
                job_id=j.get("job_id", ""),
                trace_id=j.get("trace_id", ""),
                status=j.get("status", "queued"),
                priority=priority,
            )
            for j in response.get("jobs", [])
        ]

    async def get_job_status(self, job_id: str) -> RemediationJob:
        """
        Get status of a remediation job.

        Args:
            job_id: Job ID

        Returns:
            RemediationJob with current status
        """
        response = await self._request("GET", f"/v1/remediation/status/{job_id}")

        return RemediationJob(
            job_id=job_id,
            trace_id=response.get("trace_id", ""),
            status=response.get("status", "unknown"),
            priority=response.get("priority", "normal"),
            error=response.get("error", {}),
            context=response.get("context", {}),
            result=response.get("result"),
            created_at=response.get("created_at"),
            completed_at=response.get("completed_at"),
        )

    async def cancel_job(self, job_id: str) -> bool:
        """
        Cancel a queued remediation job.

        Args:
            job_id: Job ID

        Returns:
            True if cancelled successfully
        """
        response = await self._request("DELETE", f"/v1/remediation/queue/{job_id}")
        return response.get("status") == "cancelled"

    async def get_queue_stats(self) -> QueueStats:
        """
        Get queue statistics.

        Returns:
            QueueStats with queue metrics
        """
        response = await self._request("GET", "/v1/remediation/queue/stats")

        return QueueStats(
            total_queued=response.get("total_queued", 0),
            processing=response.get("processing", 0),
            completed_today=response.get("completed_today", 0),
            failed_today=response.get("failed_today", 0),
            avg_processing_time_seconds=response.get("avg_processing_time_seconds", 0.0),
            by_priority=response.get("by_priority", {}),
        )

    # ========== Autonomous Remediation ==========

    async def preview_autonomous(
        self,
        trace_id: str,
    ) -> AutonomousPreview:
        """
        Preview what autonomous mode would do for a trace.

        Shows what Aigie would fix if autonomous mode was enabled.

        Args:
            trace_id: Trace ID to analyze

        Returns:
            AutonomousPreview with recommendations
        """
        data = {"trace_id": trace_id}
        response = await self._request("POST", "/v1/remediation/autonomous/preview", json=data)

        return AutonomousPreview(
            trace_id=trace_id,
            would_remediate=response.get("would_remediate", False),
            strategy=response.get("strategy"),
            confidence=response.get("confidence", 0.0),
            detected_issues=response.get("detected_issues", []),
            suggested_actions=response.get("suggested_actions", []),
            estimated_success_rate=response.get("estimated_success_rate", 0.0),
        )

    async def apply_autonomous_fix(
        self,
        trace_id: str,
        error: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Apply autonomous fix to a trace.

        Args:
            trace_id: Trace ID
            error: Error information

        Returns:
            Fix result
        """
        data = {
            "trace_id": trace_id,
            "error": error,
        }
        return await self._request("POST", "/v1/remediation/autonomous/fix", json=data)

    async def generate_fix(
        self,
        trace_id: str,
        error: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Generate a fix without applying it.

        Args:
            trace_id: Trace ID
            error: Error information

        Returns:
            Generated fix plan
        """
        data = {
            "trace_id": trace_id,
            "error": error,
        }
        return await self._request("POST", "/v1/remediation/autonomous/generate-fix", json=data)

    async def get_autonomous_patterns(self) -> list[dict[str, Any]]:
        """
        Get patterns used for autonomous remediation.

        Returns:
            List of pattern configurations
        """
        response = await self._request("GET", "/v1/remediation/autonomous/patterns")
        return response.get("patterns", [])

    async def enable_pattern(self, error_type: str) -> dict[str, Any]:
        """
        Enable autonomous remediation for an error type.

        Args:
            error_type: Error type to enable

        Returns:
            Update result
        """
        return await self._request(
            "POST", f"/v1/remediation/autonomous/patterns/{error_type}/enable"
        )

    async def disable_pattern(self, error_type: str) -> dict[str, Any]:
        """
        Disable autonomous remediation for an error type.

        Args:
            error_type: Error type to disable

        Returns:
            Update result
        """
        return await self._request(
            "POST", f"/v1/remediation/autonomous/patterns/{error_type}/disable"
        )

    # ========== Hallucination Detection ==========

    async def detect_hallucination(
        self,
        trace_id: str,
        output: str,
        context: dict[str, Any] | None = None,
    ) -> HallucinationDetection:
        """
        Detect if an output contains hallucinations.

        Args:
            trace_id: Trace ID
            output: Output text to analyze
            context: Additional context

        Returns:
            HallucinationDetection result
        """
        data = {
            "trace_id": trace_id,
            "output": output,
            "context": context or {},
        }

        response = await self._request("POST", "/v1/remediation/hallucination/detect", json=data)

        return HallucinationDetection(
            trace_id=trace_id,
            is_hallucination=response.get("is_hallucination", False),
            confidence=response.get("confidence", 0.0),
            evidence=response.get("evidence", []),
            suggested_remediation=response.get("suggested_remediation"),
        )

    async def validate_remediation(
        self,
        original_output: str,
        remediated_output: str,
        context: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Validate if a remediation fixed the hallucination.

        Args:
            original_output: Original output with hallucination
            remediated_output: Remediated output
            context: Additional context

        Returns:
            Validation result
        """
        data = {
            "original_output": original_output,
            "remediated_output": remediated_output,
            "context": context or {},
        }
        return await self._request(
            "POST", "/v1/remediation/hallucination/validate-remediation", json=data
        )

    async def get_hallucination_metrics(self) -> dict[str, Any]:
        """
        Get hallucination detection metrics.

        Returns:
            Detection metrics and statistics
        """
        return await self._request("GET", "/v1/remediation/hallucination/metrics")

    # ========== Control Loop Management ==========

    async def get_control_loop_status(self) -> ControlLoopStatus:
        """
        Get control loop status.

        Returns:
            ControlLoopStatus
        """
        response = await self._request("GET", "/v1/remediation/control-loop/status")

        return ControlLoopStatus(
            enabled=response.get("enabled", False),
            mode=response.get("mode", "recommendation"),
            patterns_active=response.get("patterns_active", 0),
            circuit_breakers_open=response.get("circuit_breakers_open", 0),
            last_action=response.get("last_action"),
            last_action_time=response.get("last_action_time"),
        )

    async def start_control_loop(self) -> dict[str, Any]:
        """Start the control loop."""
        return await self._request("POST", "/v1/remediation/control-loop/start")

    async def stop_control_loop(self) -> dict[str, Any]:
        """Stop the control loop."""
        return await self._request("POST", "/v1/remediation/control-loop/stop")

    async def update_control_loop_config(
        self,
        config: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Update control loop configuration.

        Args:
            config: Configuration updates

        Returns:
            Updated configuration
        """
        return await self._request("POST", "/v1/remediation/control-loop/config", json=config)

    async def get_control_loop_metrics(self) -> dict[str, Any]:
        """Get control loop metrics."""
        return await self._request("GET", "/v1/remediation/control-loop/metrics")

    async def get_what_we_would_do(self) -> dict[str, Any]:
        """
        Get what the control loop would do if autonomous mode was enabled.

        Returns:
            Pending actions and recommendations
        """
        return await self._request("GET", "/v1/remediation/control-loop/what-we-would-do")

    async def get_circuit_breakers(self) -> list[dict[str, Any]]:
        """Get current circuit breaker states."""
        response = await self._request("GET", "/v1/remediation/control-loop/circuit-breakers")
        return response.get("circuit_breakers", [])

    async def reset_circuit_breaker(self, pattern_id: str) -> dict[str, Any]:
        """
        Reset a circuit breaker.

        Args:
            pattern_id: Pattern ID to reset

        Returns:
            Reset result
        """
        return await self._request(
            "POST", f"/v1/remediation/control-loop/circuit-breakers/{pattern_id}/reset"
        )

    # ========== Checkpoint Management ==========

    async def create_checkpoint(
        self,
        trace_id: str,
    ) -> dict[str, Any]:
        """
        Create a checkpoint for a trace.

        Args:
            trace_id: Trace ID

        Returns:
            Checkpoint details
        """
        return await self._request(
            "POST", f"/v1/remediation/control-loop/checkpoints/{trace_id}/create"
        )

    async def rollback_checkpoint(
        self,
        checkpoint_id: str,
    ) -> dict[str, Any]:
        """
        Rollback to a checkpoint.

        Args:
            checkpoint_id: Checkpoint ID

        Returns:
            Rollback result
        """
        return await self._request(
            "POST", f"/v1/remediation/control-loop/checkpoints/{checkpoint_id}/rollback"
        )

    async def get_checkpoints(
        self,
        limit: int = 50,
    ) -> list[dict[str, Any]]:
        """
        Get recent checkpoints.

        Args:
            limit: Maximum results

        Returns:
            List of checkpoints
        """
        params = {"limit": limit}
        response = await self._request(
            "GET", "/v1/remediation/control-loop/checkpoints", params=params
        )
        return response.get("checkpoints", [])

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

            logging.getLogger(__name__).error(f"Remediation API Error [{method} {path}]: {error}")
            raise

    async def close(self):
        """Close HTTP client."""
        await self.client.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
