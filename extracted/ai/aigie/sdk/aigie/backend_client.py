"""
Backend Client - HTTP Client for Reporting to Kytte Backend

This client provides HTTP communication with the Kytte backend for:
1. Reporting remediation results (for learning system)
2. Fetching successful patterns (for autonomous mode)
3. Updating workflow status

The client is designed to be:
- Non-blocking: Uses async/await
- Fail-safe: Errors are logged but don't break agent execution
- Efficient: Uses connection pooling and retry logic
"""

import asyncio
import contextlib
import logging
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any

from .diagnostics import N002, N005, N006, format_diagnostic

logger = logging.getLogger("aigie.backend_client")


class RemediationStrategy(str, Enum):
    """Remediation strategy types (mirrors backend enum)."""

    RETRY_WITH_CONTEXT = "retry_with_context"
    MODIFY_PROMPT = "modify_prompt"
    FALLBACK_MODEL = "fallback_model"
    TRUNCATE_CONTEXT = "truncate_context"
    INJECT_INSTRUCTION = "inject_instruction"
    ROLLBACK_AND_RETRY = "rollback_and_retry"
    SKIP_STEP = "skip_step"
    ESCALATE = "escalate"


@dataclass
class RemediationResultReport:
    """Report for a remediation result to be sent to backend."""

    trace_id: str
    span_id: str | None = None
    cluster_id: str | None = None
    flow_id: str | None = None
    workflow_id: str | None = None
    strategy: str | None = None
    method: str | None = None
    success: bool = False
    confidence: float = 0.0
    error_message: str | None = None
    original_output: str | None = None
    fixed_output: str | None = None
    fix_applied: bool = False
    mode: str = "observe"  # "observe" or "autonomous"
    latency_ms: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "trace_id": self.trace_id,
            "span_id": self.span_id,
            "cluster_id": self.cluster_id,
            "flow_id": self.flow_id,
            "workflow_id": self.workflow_id,
            "strategy": self.strategy,
            "method": self.method,
            "success": self.success,
            "confidence": self.confidence,
            "error_message": self.error_message,
            "original_output": self.original_output,
            "fixed_output": self.fixed_output,
            "fix_applied": self.fix_applied,
            "mode": self.mode,
            "latency_ms": self.latency_ms,
            "metadata": self.metadata,
            "timestamp": datetime.utcnow().isoformat(),
        }


@dataclass
class RecommendationReport:
    """Report for a recommendation generated in recommendation mode."""

    span_id: str
    trace_id: str
    recommendation: str
    strategy: str | None = None
    issues: list[str] = field(default_factory=list)
    confidence: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "span_id": self.span_id,
            "trace_id": self.trace_id,
            "recommendation": self.recommendation,
            "strategy": self.strategy,
            "issues": self.issues,
            "confidence": self.confidence,
            "metadata": self.metadata,
            "timestamp": datetime.utcnow().isoformat(),
        }


@dataclass
class SuccessfulPattern:
    """A successful remediation pattern from the learning system."""

    pattern_id: str
    error_type: str
    strategy: str
    method: str
    success_rate: float
    application_count: int
    confidence: float
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SuccessfulPattern":
        """Create from dictionary."""
        return cls(
            pattern_id=data.get("pattern_id", ""),
            error_type=data.get("error_type", ""),
            strategy=data.get("strategy", ""),
            method=data.get("method", ""),
            success_rate=data.get("success_rate", 0.0),
            application_count=data.get("application_count", 0),
            confidence=data.get("confidence", 0.0),
            metadata=data.get("metadata", {}),
        )


class KytteBackendClient:
    """
    HTTP client for communicating with the Kytte backend.

    Features:
    - Async HTTP requests with connection pooling
    - Automatic retry with exponential backoff
    - Circuit breaker for fault tolerance
    - Batched reporting for efficiency
    """

    def __init__(
        self,
        api_url: str,
        api_key: str,
        timeout_seconds: float = 10.0,
        max_retries: int = 3,
        retry_delay_seconds: float = 1.0,
        batch_size: int = 10,
        batch_flush_interval_seconds: float = 5.0,
        enable_batching: bool = True,
    ):
        """
        Initialize the backend client.

        Args:
            api_url: Base URL for the API (e.g., "https://api.kytte.ai")
            api_key: API key for authentication
            timeout_seconds: Request timeout
            max_retries: Maximum retry attempts
            retry_delay_seconds: Initial delay between retries
            batch_size: Number of results to batch before sending
            batch_flush_interval_seconds: Time to wait before flushing partial batch
            enable_batching: Whether to batch results
        """
        self._api_url = api_url.rstrip("/")
        self._api_key = api_key
        self._timeout = timeout_seconds
        self._max_retries = max_retries
        self._retry_delay = retry_delay_seconds
        self._batch_size = batch_size
        self._batch_flush_interval = batch_flush_interval_seconds
        self._enable_batching = enable_batching

        # HTTP client (lazily initialized)
        self._session = None

        # Batching state
        self._result_batch: list[RemediationResultReport] = []
        self._recommendation_batch: list[RecommendationReport] = []
        self._batch_task: asyncio.Task | None = None
        self._batch_lock = asyncio.Lock()

        # Circuit breaker
        self._circuit_open = False
        self._circuit_failures = 0
        self._circuit_open_until: datetime | None = None
        self._circuit_failure_threshold = 5
        self._circuit_reset_timeout_seconds = 60

        # Statistics
        self._stats = {
            "results_reported": 0,
            "results_failed": 0,
            "recommendations_reported": 0,
            "patterns_fetched": 0,
            "retries": 0,
            "circuit_opens": 0,
        }

    async def _get_session(self):
        """Get or create HTTP session."""
        if self._session is None:
            try:
                import aiohttp

                timeout = aiohttp.ClientTimeout(total=self._timeout)
                self._session = aiohttp.ClientSession(
                    timeout=timeout,
                    headers={
                        "X-API-Key": self._api_key,
                        "Content-Type": "application/json",
                        "User-Agent": "aigie-sdk/2.0.0",
                    },
                )
            except ImportError:
                logger.warning("aiohttp not installed, using httpx fallback")
                try:
                    import httpx

                    self._session = httpx.AsyncClient(
                        timeout=self._timeout,
                        headers={
                            "X-API-Key": self._api_key,
                            "Content-Type": "application/json",
                            "User-Agent": "aigie-sdk/2.0.0",
                        },
                    )
                except ImportError:
                    logger.error("Neither aiohttp nor httpx installed")
                    return None
        return self._session

    async def close(self):
        """Close the HTTP session."""
        if self._batch_task:
            self._batch_task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await self._batch_task

        # Flush remaining batches
        await self._flush_batches()

        if self._session:
            await self._session.close()
            self._session = None

    def _is_circuit_open(self) -> bool:
        """Check if circuit breaker is open."""
        if not self._circuit_open:
            return False

        if self._circuit_open_until and datetime.utcnow() > self._circuit_open_until:
            self._circuit_open = False
            self._circuit_failures = 0
            logger.info("Circuit breaker reset")
            return False

        return True

    def _record_failure(self):
        """Record a failure for circuit breaker."""
        self._circuit_failures += 1
        if self._circuit_failures >= self._circuit_failure_threshold:
            self._circuit_open = True
            self._circuit_open_until = datetime.utcnow() + timedelta(
                seconds=self._circuit_reset_timeout_seconds
            )
            self._stats["circuit_opens"] += 1
            logger.warning(
                format_diagnostic(N005, extra=f"after {self._circuit_failures} failures")
            )

    def _record_success(self):
        """Record success for circuit breaker."""
        self._circuit_failures = 0

    async def _request(
        self,
        method: str,
        endpoint: str,
        json_data: dict[str, Any] | None = None,
    ) -> dict[str, Any] | None:
        """Make an HTTP request with retry logic."""
        if self._is_circuit_open():
            logger.debug("Circuit breaker open, skipping request")
            return None

        session = await self._get_session()
        if not session:
            return None

        url = f"{self._api_url}{endpoint}"

        for attempt in range(self._max_retries + 1):
            try:
                if hasattr(session, "request"):
                    # aiohttp
                    async with session.request(method, url, json=json_data) as response:
                        if response.status >= 500:
                            raise Exception(f"Server error: {response.status}")
                        if response.status >= 400:
                            error_text = await response.text()
                            logger.warning(
                                format_diagnostic(
                                    N002, extra=f"HTTP {response.status}: {error_text}"
                                )
                            )
                            return None
                        self._record_success()
                        return await response.json()
                else:
                    # httpx
                    response = await session.request(method, url, json=json_data)
                    if response.status_code >= 500:
                        raise Exception(f"Server error: {response.status_code}")
                    if response.status_code >= 400:
                        logger.warning(
                            format_diagnostic(
                                N002, extra=f"HTTP {response.status_code}: {response.text}"
                            )
                        )
                        return None
                    self._record_success()
                    return response.json()

            except Exception as e:
                self._stats["retries"] += 1
                if attempt < self._max_retries:
                    delay = self._retry_delay * (2**attempt)
                    logger.debug(f"Request failed, retrying in {delay}s: {e}")
                    await asyncio.sleep(delay)
                else:
                    self._record_failure()
                    logger.error(format_diagnostic(N006, extra=str(e)))
                    return None

        return None

    async def report_remediation_result(
        self, result: RemediationResultReport | dict[str, Any]
    ) -> bool:
        """
        Report a remediation result to the backend.

        Args:
            result: RemediationResultReport or dict with result data

        Returns:
            True if reported successfully
        """
        if isinstance(result, dict):
            result = RemediationResultReport(**result)

        if self._enable_batching:
            async with self._batch_lock:
                self._result_batch.append(result)
                if len(self._result_batch) >= self._batch_size:
                    await self._flush_result_batch()
                elif not self._batch_task:
                    self._batch_task = asyncio.create_task(self._batch_flush_loop())
            return True
        return await self._send_result(result)

    async def _send_result(self, result: RemediationResultReport) -> bool:
        """Send a single remediation result."""
        response = await self._request(
            "POST", "/v1/remediation/results", json_data=result.to_dict()
        )
        if response:
            self._stats["results_reported"] += 1
            return True
        self._stats["results_failed"] += 1
        return False

    async def _flush_result_batch(self):
        """Flush the result batch."""
        if not self._result_batch:
            return

        batch = self._result_batch
        self._result_batch = []

        results_data = [r.to_dict() for r in batch]
        response = await self._request(
            "POST", "/v1/remediation/results/batch", json_data={"results": results_data}
        )

        if response:
            self._stats["results_reported"] += len(batch)
            logger.debug(f"Flushed {len(batch)} remediation results")
        else:
            self._stats["results_failed"] += len(batch)
            logger.warning(f"Failed to flush {len(batch)} remediation results")

    async def report_recommendation(
        self,
        span_id: str,
        trace_id: str,
        recommendation: str,
        strategy: str | None = None,
        issues: list[str] | None = None,
        confidence: float = 0.0,
    ) -> bool:
        """
        Report a recommendation to the backend.

        Args:
            span_id: ID of the span
            trace_id: ID of the trace
            recommendation: The recommendation text
            strategy: Recommended strategy
            issues: List of issues addressed
            confidence: Confidence in the recommendation

        Returns:
            True if reported successfully
        """
        report = RecommendationReport(
            span_id=span_id,
            trace_id=trace_id,
            recommendation=recommendation,
            strategy=strategy,
            issues=issues or [],
            confidence=confidence,
        )

        if self._enable_batching:
            async with self._batch_lock:
                self._recommendation_batch.append(report)
                if len(self._recommendation_batch) >= self._batch_size:
                    await self._flush_recommendation_batch()
            return True
        return await self._send_recommendation(report)

    async def _send_recommendation(self, report: RecommendationReport) -> bool:
        """Send a single recommendation."""
        response = await self._request("POST", "/v1/recommendations", json_data=report.to_dict())
        if response:
            self._stats["recommendations_reported"] += 1
            return True
        return False

    async def _flush_recommendation_batch(self):
        """Flush the recommendation batch."""
        if not self._recommendation_batch:
            return

        batch = self._recommendation_batch
        self._recommendation_batch = []

        data = [r.to_dict() for r in batch]
        response = await self._request(
            "POST", "/v1/recommendations/batch", json_data={"recommendations": data}
        )

        if response:
            self._stats["recommendations_reported"] += len(batch)
            logger.debug(f"Flushed {len(batch)} recommendations")

    async def _flush_batches(self):
        """Flush all batches."""
        async with self._batch_lock:
            await self._flush_result_batch()
            await self._flush_recommendation_batch()

    async def _batch_flush_loop(self):
        """Background loop to flush batches periodically."""
        try:
            while True:
                await asyncio.sleep(self._batch_flush_interval)
                await self._flush_batches()
        except asyncio.CancelledError:
            pass

    async def get_successful_patterns(
        self,
        error_type: str | None = None,
        time_window_hours: int = 168,  # 1 week
        limit: int = 100,
    ) -> list[SuccessfulPattern]:
        """
        Fetch successful remediation patterns from the backend.

        Args:
            error_type: Filter by error type
            time_window_hours: Time window to look back
            limit: Maximum patterns to return

        Returns:
            List of successful patterns
        """
        params = {
            "time_window_hours": time_window_hours,
            "limit": limit,
        }
        if error_type:
            params["error_type"] = error_type

        # Build query string
        query = "&".join(f"{k}={v}" for k, v in params.items())
        endpoint = f"/v1/remediation/patterns?{query}"

        response = await self._request("GET", endpoint)
        if response:
            self._stats["patterns_fetched"] += 1
            patterns = response.get("patterns", [])
            return [SuccessfulPattern.from_dict(p) for p in patterns]

        return []

    async def get_judges(self) -> list[dict[str, Any]]:
        """
        Fetch the list of available judges from the backend.

        The SDK calls this once at startup and caches the list. Each judge
        has an id, name, description, and category that the SDK uses to
        decide which judges to trigger for each step.

        Returns:
            List of judge dicts with id, name, description, category.
        """
        response = await self._request("GET", "/v1/judges")
        if response:
            return response.get("judges", [])
        return []

    async def evaluate_step(
        self,
        trace_id: str,
        span_id: str | None = None,
        step_name: str = "",
        step_type: str = "LLM",
        input: str | None = None,
        output: str | None = None,
        error: str | None = None,
        error_type: str | None = None,
        model: str | None = None,
        judge_ids: list[str] | None = None,
    ) -> dict[str, Any] | None:
        """
        Call backend /v1/judges/evaluate-step for real-time step evaluation.

        The SDK picks which judge_ids are relevant (based on the cached judge
        list) and sends them here. The backend runs them in parallel and
        returns scored results.

        Args:
            trace_id: Current trace ID
            span_id: Current span ID
            step_name: Name of the step (e.g. tool name)
            step_type: LLM, TOOL, RETRIEVAL, AGENT
            input: Truncated input (max 2000 chars)
            output: Truncated output (max 2000 chars)
            error: Error message if step failed
            error_type: Classified error type
            model: Model used (for LLM steps)
            judge_ids: Specific judges to run

        Returns:
            Dict with evaluations, has_issues, routing_analysis — or None on failure
        """
        return await self._request(
            "POST",
            "/v1/judges/evaluate-step",
            json_data={
                "trace_id": trace_id,
                "span_id": span_id,
                "step_name": step_name,
                "step_type": step_type,
                "input": (input or "")[:2000] or None,
                "output": (output or "")[:2000] or None,
                "error": error,
                "error_type": error_type,
                "model": model,
                "judge_ids": judge_ids,
            },
        )

    async def update_workflow_mode(
        self,
        workflow_id: str,
        autonomous_enabled: bool,
    ) -> bool:
        """
        Update the autonomous mode for a workflow.

        Args:
            workflow_id: ID of the workflow
            autonomous_enabled: Whether autonomous mode is enabled

        Returns:
            True if updated successfully
        """
        response = await self._request(
            "PATCH",
            f"/v1/workflows/{workflow_id}/autonomous",
            json_data={"autonomous_enabled": autonomous_enabled},
        )
        return response is not None

    # ==================================================================
    # Full Kytte Platform API Integration
    # ==================================================================

    # --- Fix Outcome Reporting (Phase 4.3) ---

    async def report_fix_outcome(
        self,
        trace_id: str,
        span_id: str,
        pattern_id: str | None = None,
        fix_action: str = "",
        success: bool = False,
        latency_ms: float = 0.0,
        error_before: str | None = None,
        error_after: str | None = None,
        judge_scores: dict[str, float] | None = None,
    ) -> bool:
        """Report fix outcome for closed-loop learning."""
        response = await self._request(
            "POST",
            "/v1/remediation/fix-outcome",
            json_data={
                "trace_id": trace_id,
                "span_id": span_id,
                "pattern_id": pattern_id,
                "fix_action": fix_action,
                "success": success,
                "latency_ms": latency_ms,
                "error_before": error_before,
                "error_after": error_after,
                "judge_scores": judge_scores or {},
            },
        )
        return response is not None

    # --- Hallucination Detection ---

    async def detect_hallucination(
        self,
        trace_id: str,
        output_content: str,
        input_content: str,
        context: dict[str, Any] | None = None,
    ) -> dict[str, Any] | None:
        """Use platform hallucination detection API."""
        return await self._request(
            "POST",
            "/v1/remediation/hallucination/detect",
            json_data={
                "trace_id": trace_id,
                "output": output_content,
                "input": input_content,
                "context": context or {},
            },
        )

    # --- Autonomous Mode ---

    async def preview_autonomous_action(
        self,
        trace_id: str,
        error: dict[str, Any],
        context: dict[str, Any] | None = None,
    ) -> dict[str, Any] | None:
        """Preview what autonomous mode WOULD do for an error."""
        return await self._request(
            "POST",
            "/v1/remediation/autonomous/preview",
            json_data={
                "trace_id": trace_id,
                "error": error,
                "context": context or {},
            },
        )

    async def execute_autonomous_fix(
        self,
        trace_id: str,
        error_type: str,
        error_message: str,
        strategy: str | None = None,
    ) -> dict[str, Any] | None:
        """Execute an autonomous fix via the platform."""
        return await self._request(
            "POST",
            "/v1/remediation/autonomous/fix",
            json_data={
                "trace_id": trace_id,
                "error_type": error_type,
                "error_message": error_message,
                "strategy": strategy,
            },
        )

    async def generate_autonomous_fix(
        self,
        trace_id: str,
        error_type: str,
        error_message: str,
        context: dict[str, Any] | None = None,
    ) -> dict[str, Any] | None:
        """Generate a fix using platform LLM (Gemini)."""
        return await self._request(
            "POST",
            "/v1/remediation/autonomous/generate-fix",
            json_data={
                "trace_id": trace_id,
                "error_type": error_type,
                "error_message": error_message,
                "context": context or {},
            },
        )

    async def get_autonomous_patterns(self) -> dict[str, Any] | None:
        """Get all autonomous remediation patterns from platform."""
        return await self._request("GET", "/v1/remediation/autonomous/patterns")

    # --- Control Loop ---

    async def get_control_loop_status(self) -> dict[str, Any] | None:
        """Get control loop status (what-we-would-do + circuit breakers)."""
        return await self._request("GET", "/v1/remediation/control-loop/status")

    async def get_control_loop_metrics(self) -> dict[str, Any] | None:
        """Get control loop metrics."""
        return await self._request("GET", "/v1/remediation/control-loop/metrics")

    async def get_degradation_status(self) -> dict[str, Any] | None:
        """Get degradation status from control loop."""
        return await self._request("GET", "/v1/remediation/control-loop/degradation")

    async def get_what_we_would_do(self) -> dict[str, Any] | None:
        """Get 'what we would do' — previews of autonomous actions."""
        return await self._request("GET", "/v1/remediation/control-loop/what-we-would-do")

    async def get_if_autonomous_was_on(self) -> dict[str, Any] | None:
        """Get counterfactual: what would have happened if autonomous was on."""
        return await self._request("GET", "/v1/remediation/control-loop/if-autonomous-was-on")

    # --- Remediation Flows ---

    async def get_remediation_flows(self) -> list[dict[str, Any]] | None:
        """Get all remediation flows from platform."""
        result = await self._request("GET", "/v1/remediation/flows")
        if result:
            return result if isinstance(result, list) else result.get("flows", [])
        return []

    async def execute_remediation_flow(
        self,
        flow_id: str,
        trace_id: str,
        error_type: str,
        error_message: str,
    ) -> dict[str, Any] | None:
        """Execute a specific remediation flow."""
        return await self._request(
            "POST",
            "/v1/remediation/flows/execute",
            json_data={
                "flow_id": flow_id,
                "trace_id": trace_id,
                "error_type": error_type,
                "error_message": error_message,
            },
        )

    # --- Evaluation / Judges ---

    async def evaluate_strategies(
        self,
        trace_id: str,
        error_type: str,
        error_message: str,
    ) -> dict[str, Any] | None:
        """Evaluate remediation strategies for an error."""
        return await self._request(
            "POST",
            "/v1/remediation/evaluate/strategies",
            json_data={
                "trace_id": trace_id,
                "error_type": error_type,
                "error_message": error_message,
            },
        )

    async def predict_remediation(
        self,
        error_type: str,
        error_message: str,
    ) -> dict[str, Any] | None:
        """Predict best remediation for an error using platform ML."""
        return await self._request(
            "POST",
            "/v1/remediation/evaluate/predict",
            json_data={
                "error_type": error_type,
                "error_message": error_message,
            },
        )

    async def sync_evaluate(
        self,
        template_id: str,
        variables: dict[str, str],
        timeout_ms: int = 5000,
        fast_mode: bool = False,
    ) -> dict[str, Any] | None:
        """Call platform sync evaluation API (LLM judge)."""
        return await self._request(
            "POST",
            "/evals/sync-evaluate",
            json_data={
                "templateId": template_id,
                "variables": variables,
                "timeoutMs": timeout_ms,
                "fastMode": fast_mode,
            },
        )

    async def get_eval_templates(self) -> list[dict[str, Any]] | None:
        """Fetch available eval templates (judge prompts) from platform."""
        result = await self._request("GET", "/v1/judges")
        return result if isinstance(result, list) else []

    # --- Guardrails ---

    async def check_guardrails(
        self,
        content: str,
        trace_id: str | None = None,
        guardrail_types: list[str] | None = None,
    ) -> dict[str, Any] | None:
        """Check content against platform guardrails."""
        return await self._request(
            "POST",
            "/v1/guardrails/check",
            json_data={
                "content": content,
                "trace_id": trace_id,
                "guardrail_types": guardrail_types or [],
            },
        )

    # --- Learning & Training ---

    async def get_training_stats(self) -> dict[str, Any] | None:
        """Get training/learning statistics from platform."""
        return await self._request("GET", "/v1/remediation/training/stats")

    async def trigger_training(
        self,
        error_type: str | None = None,
    ) -> dict[str, Any] | None:
        """Trigger training for a specific error type."""
        return await self._request(
            "POST",
            "/v1/remediation/training/trigger",
            json_data={"error_type": error_type} if error_type else {},
        )

    async def get_learning_stats(
        self,
        cluster_id: str,
    ) -> dict[str, Any] | None:
        """Get learning stats for a specific error cluster."""
        return await self._request("GET", f"/v1/remediation/learning/stats/{cluster_id}")

    # --- Checkpoints & Rollback ---

    async def create_checkpoint(
        self,
        trace_id: str,
    ) -> dict[str, Any] | None:
        """Create a checkpoint for rollback capability."""
        return await self._request(
            "POST",
            f"/v1/remediation/control-loop/checkpoints/{trace_id}/create",
        )

    async def rollback_to_checkpoint(
        self,
        checkpoint_id: str,
    ) -> dict[str, Any] | None:
        """Rollback to a specific checkpoint."""
        return await self._request(
            "POST",
            f"/v1/remediation/control-loop/checkpoints/{checkpoint_id}/rollback",
        )

    # --- Runtime Reliability Analytics ---

    async def get_runtime_reliability(self) -> dict[str, Any] | None:
        """Get runtime reliability stats (fixes count, success rate, etc.)."""
        return await self._request("GET", "/v1/analytics/runtime-reliability")

    async def get_runtime_reliability_timeline(
        self,
        interval: str = "hour",
        days: int = 7,
    ) -> dict[str, Any] | None:
        """Get runtime reliability time series."""
        return await self._request(
            "GET",
            f"/v1/analytics/runtime-reliability/timeline?interval={interval}&days={days}",
        )

    # --- Alerting ---

    async def send_alert(
        self,
        alert_type: str,
        message: str,
        severity: str = "medium",
        trace_id: str | None = None,
    ) -> dict[str, Any] | None:
        """Send an alert to the platform (Slack, webhook, etc.)."""
        return await self._request(
            "POST",
            "/v1/alerting/alerts/send",
            json_data={
                "alert_type": alert_type,
                "message": message,
                "severity": severity,
                "trace_id": trace_id,
            },
        )

    # ==================================================================

    def get_stats(self) -> dict[str, Any]:
        """Get client statistics."""
        return {
            **self._stats,
            "circuit_open": self._circuit_open,
            "pending_results": len(self._result_batch),
            "pending_recommendations": len(self._recommendation_batch),
        }
