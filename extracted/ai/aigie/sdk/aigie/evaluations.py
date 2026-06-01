"""
Evaluations API Client for Aigie SDK

Interact with Aigie's backend evaluation system to run evaluations,
access predefined judges, and retrieve evaluation scores.

Based on the platform's evaluation capabilities:
- 6 evaluation types: EVAL, SPAN_EVAL, DRIFT_EVAL, RECOVERY_EVAL, CHECKPOINT_EVAL, sync
- Pre-built evaluation templates
- Async job processing
- Score aggregation and retrieval
"""

import asyncio
import os
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any

import httpx


class EvaluationType(str, Enum):
    """Types of evaluations supported by the platform."""

    EVAL = "EVAL"  # Standard evaluation
    SPAN_EVAL = "SPAN_EVAL"  # Span-level evaluation
    DRIFT_EVAL = "DRIFT_EVAL"  # Drift detection evaluation
    RECOVERY_EVAL = "RECOVERY_EVAL"  # Error recovery evaluation
    CHECKPOINT_EVAL = "CHECKPOINT_EVAL"  # Checkpoint evaluation
    SYNC = "sync"  # Synchronous evaluation


class ScoreType(str, Enum):
    """Types of evaluation scores."""

    BINARY = "binary"  # Pass/fail
    NUMERIC = "numeric"  # 0-1 continuous score
    CATEGORICAL = "categorical"  # Category labels


@dataclass
class EvaluationTemplate:
    """Pre-built evaluation template."""

    id: str
    name: str
    description: str
    criteria: str
    score_type: ScoreType
    created_at: str
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class EvaluationScore:
    """Evaluation score result."""

    id: str
    trace_id: str | None
    span_id: str | None
    evaluator_name: str
    score: float
    score_type: ScoreType
    passed: bool
    reasoning: str | None
    created_at: str
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class EvaluationJob:
    """Async evaluation job."""

    id: str
    type: EvaluationType
    status: str  # pending, processing, completed, failed
    trace_id: str | None
    span_id: str | None
    created_at: str
    completed_at: str | None = None
    result: EvaluationScore | None = None
    error: str | None = None


@dataclass
class EvaluationRequest:
    """Request to run an evaluation."""

    input: Any
    output: Any
    expected_output: Any | None = None
    context: dict[str, Any] | None = None
    trace_id: str | None = None
    span_id: str | None = None
    evaluator_name: str | None = None
    template_id: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


class EvaluationsClient:
    """
    Evaluations API client for Aigie.

    Provides methods for running evaluations using the platform's
    backend evaluation system.

    Example:
        >>> from aigie.evaluations import EvaluationsClient
        >>>
        >>> client = EvaluationsClient()
        >>>
        >>> # Run a simple evaluation
        >>> score = await client.evaluate(
        ...     input="What is 2+2?",
        ...     output="4",
        ...     expected_output="4",
        ...     evaluator_name="exact_match"
        ... )
        >>> print(f"Score: {score.score}, Passed: {score.passed}")
        >>>
        >>> # Use a predefined judge
        >>> score = await client.evaluate_with_judge(
        ...     input="Explain quantum computing",
        ...     output="Quantum computing uses qubits...",
        ...     judge_name="response_quality"
        ... )
        >>>
        >>> # Get scores for a trace
        >>> scores = await client.get_trace_scores("trace-id-123")
    """

    def __init__(
        self,
        api_url: str | None = None,
        api_key: str | None = None,
    ):
        """
        Initialize evaluations client.

        Args:
            api_url: API URL (defaults to AIGIE_API_URL env var)
            api_key: API key (defaults to AIGIE_API_KEY env var)
        """
        self.api_url = api_url or os.getenv("AIGIE_API_URL", "")
        self.api_key = api_key or os.getenv("AIGIE_API_KEY", "")
        self.client = httpx.AsyncClient(timeout=60.0)

    async def evaluate(
        self,
        input: Any,
        output: Any,
        expected_output: Any | None = None,
        context: dict[str, Any] | None = None,
        evaluator_name: str | None = None,
        template_id: str | None = None,
        trace_id: str | None = None,
        span_id: str | None = None,
        metadata: dict[str, Any] | None = None,
        async_mode: bool = False,
    ) -> EvaluationScore | EvaluationJob:
        """
        Run an evaluation.

        Args:
            input: The input that was provided
            output: The output that was generated
            expected_output: Optional expected output for comparison
            context: Additional context for evaluation
            evaluator_name: Name of evaluator to use
            template_id: ID of evaluation template to use
            trace_id: Optional trace ID to attach score to
            span_id: Optional span ID to attach score to
            metadata: Additional metadata
            async_mode: If True, returns job ID for async processing

        Returns:
            EvaluationScore or EvaluationJob depending on async_mode
        """
        data = {
            "input": input,
            "output": output,
            "expectedOutput": expected_output,
            "context": context or {},
            "evaluatorName": evaluator_name,
            "templateId": template_id,
            "traceId": trace_id,
            "spanId": span_id,
            "metadata": metadata or {},
            "async": async_mode,
        }

        response = await self._request("POST", "/v1/evaluations/run", json=data)

        if async_mode:
            return EvaluationJob(
                id=response["jobId"],
                type=EvaluationType(response.get("type", "EVAL")),
                status="pending",
                trace_id=trace_id,
                span_id=span_id,
                created_at=datetime.utcnow().isoformat(),
            )
        return self._parse_score(response)

    async def evaluate_with_judge(
        self,
        input: Any,
        output: Any,
        judge_name: str,
        expected_output: Any | None = None,
        context: dict[str, Any] | None = None,
        trace_id: str | None = None,
        span_id: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> EvaluationScore:
        """
        Run evaluation using a predefined judge.

        Available judges (from platform):
        - response_quality: Evaluates response quality and coherence
        - factual_accuracy: Checks factual correctness
        - safety: Evaluates for harmful content
        - relevance: Checks response relevance to input
        - task_completion: Evaluates if task was completed

        Args:
            input: The input that was provided
            output: The output that was generated
            judge_name: Name of the predefined judge
            expected_output: Optional expected output
            context: Additional context
            trace_id: Optional trace ID
            span_id: Optional span ID
            metadata: Additional metadata

        Returns:
            EvaluationScore with the judge's assessment
        """
        data = {
            "input": input,
            "output": output,
            "expectedOutput": expected_output,
            "context": context or {},
            "judgeName": judge_name,
            "traceId": trace_id,
            "spanId": span_id,
            "metadata": metadata or {},
        }

        response = await self._request("POST", "/v1/evaluations/judge", json=data)
        return self._parse_score(response)

    async def evaluate_batch(
        self,
        evaluations: list[EvaluationRequest],
        concurrency: int = 5,
    ) -> list[EvaluationScore]:
        """
        Run multiple evaluations in batch.

        Args:
            evaluations: List of evaluation requests
            concurrency: Maximum concurrent evaluations

        Returns:
            List of evaluation scores
        """
        semaphore = asyncio.Semaphore(concurrency)

        async def run_single(req: EvaluationRequest) -> EvaluationScore:
            async with semaphore:
                return await self.evaluate(
                    input=req.input,
                    output=req.output,
                    expected_output=req.expected_output,
                    context=req.context,
                    evaluator_name=req.evaluator_name,
                    template_id=req.template_id,
                    trace_id=req.trace_id,
                    span_id=req.span_id,
                    metadata=req.metadata,
                )

        return await asyncio.gather(*[run_single(req) for req in evaluations])

    async def get_job_status(self, job_id: str) -> EvaluationJob:
        """
        Get status of an async evaluation job.

        Args:
            job_id: Job ID from async evaluation

        Returns:
            EvaluationJob with current status
        """
        response = await self._request("GET", f"/v1/evaluations/jobs/{job_id}")

        result = None
        if response.get("result"):
            result = self._parse_score(response["result"])

        return EvaluationJob(
            id=response["id"],
            type=EvaluationType(response.get("type", "EVAL")),
            status=response["status"],
            trace_id=response.get("traceId"),
            span_id=response.get("spanId"),
            created_at=response["createdAt"],
            completed_at=response.get("completedAt"),
            result=result,
            error=response.get("error"),
        )

    async def wait_for_job(
        self,
        job_id: str,
        timeout: float = 60.0,
        poll_interval: float = 1.0,
    ) -> EvaluationScore:
        """
        Wait for an async evaluation job to complete.

        Args:
            job_id: Job ID from async evaluation
            timeout: Maximum time to wait in seconds
            poll_interval: Time between status checks

        Returns:
            EvaluationScore when job completes

        Raises:
            TimeoutError: If job doesn't complete within timeout
            RuntimeError: If job fails
        """
        start_time = asyncio.get_event_loop().time()

        while True:
            job = await self.get_job_status(job_id)

            if job.status == "completed" and job.result:
                return job.result
            if job.status == "failed":
                raise RuntimeError(f"Evaluation job failed: {job.error}")

            elapsed = asyncio.get_event_loop().time() - start_time
            if elapsed >= timeout:
                raise TimeoutError(f"Evaluation job {job_id} timed out after {timeout}s")

            await asyncio.sleep(poll_interval)

    async def get_templates(
        self,
        limit: int = 100,
        offset: int = 0,
    ) -> tuple[list[EvaluationTemplate], int]:
        """
        Get available evaluation templates.

        Args:
            limit: Maximum templates to return
            offset: Pagination offset

        Returns:
            Tuple of (templates, total_count)
        """
        params = {"limit": limit, "offset": offset}
        response = await self._request("GET", "/v1/evaluations/templates", params=params)

        templates = [
            EvaluationTemplate(
                id=t["id"],
                name=t["name"],
                description=t.get("description", ""),
                criteria=t["criteria"],
                score_type=ScoreType(t.get("scoreType", "numeric")),
                created_at=t["createdAt"],
                metadata=t.get("metadata", {}),
            )
            for t in response.get("templates", [])
        ]

        return templates, response.get("total", len(templates))

    async def get_trace_scores(
        self,
        trace_id: str,
        limit: int = 100,
    ) -> list[EvaluationScore]:
        """
        Get all evaluation scores for a trace.

        Args:
            trace_id: Trace ID
            limit: Maximum scores to return

        Returns:
            List of evaluation scores
        """
        params = {"traceId": trace_id, "limit": limit}
        response = await self._request("GET", "/v1/evaluations/scores", params=params)

        return [self._parse_score(s) for s in response.get("scores", [])]

    async def get_span_scores(
        self,
        span_id: str,
        limit: int = 100,
    ) -> list[EvaluationScore]:
        """
        Get all evaluation scores for a span.

        Args:
            span_id: Span ID
            limit: Maximum scores to return

        Returns:
            List of evaluation scores
        """
        params = {"spanId": span_id, "limit": limit}
        response = await self._request("GET", "/v1/evaluations/scores", params=params)

        return [self._parse_score(s) for s in response.get("scores", [])]

    async def create_score(
        self,
        trace_id: str,
        evaluator_name: str,
        score: float,
        score_type: ScoreType = ScoreType.NUMERIC,
        passed: bool | None = None,
        reasoning: str | None = None,
        span_id: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> EvaluationScore:
        """
        Manually create an evaluation score.

        Useful for custom evaluations or importing external scores.

        Args:
            trace_id: Trace ID to attach score to
            evaluator_name: Name of the evaluator
            score: Score value (0-1 for numeric)
            score_type: Type of score
            passed: Whether evaluation passed
            reasoning: Explanation of the score
            span_id: Optional span ID
            metadata: Additional metadata

        Returns:
            Created EvaluationScore
        """
        # Default passed for binary/numeric
        if passed is None:
            passed = score >= 0.5 if score_type == ScoreType.NUMERIC else bool(score)

        data = {
            "traceId": trace_id,
            "spanId": span_id,
            "evaluatorName": evaluator_name,
            "score": score,
            "scoreType": score_type.value,
            "passed": passed,
            "reasoning": reasoning,
            "metadata": metadata or {},
        }

        response = await self._request("POST", "/v1/evaluations/scores", json=data)
        return self._parse_score(response)

    def _parse_score(self, data: dict[str, Any]) -> EvaluationScore:
        """Parse score from API response."""
        return EvaluationScore(
            id=data.get("id", ""),
            trace_id=data.get("traceId"),
            span_id=data.get("spanId"),
            evaluator_name=data.get("evaluatorName", data.get("name", "")),
            score=float(data.get("score", 0)),
            score_type=ScoreType(data.get("scoreType", "numeric")),
            passed=data.get("passed", False),
            reasoning=data.get("reasoning"),
            created_at=data.get("createdAt", datetime.utcnow().isoformat()),
            metadata=data.get("metadata", {}),
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

            logging.getLogger(__name__).error(f"Evaluations API Error [{method} {path}]: {error}")
            raise

    async def close(self):
        """Close HTTP client."""
        await self.client.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()


# Convenience function for simple evaluations
async def evaluate(
    input: Any,
    output: Any,
    expected_output: Any | None = None,
    evaluator_name: str | None = None,
    judge_name: str | None = None,
    **kwargs,
) -> EvaluationScore:
    """
    Simple evaluation function (Laminar-style API).

    Example:
        >>> from aigie.evaluations import evaluate
        >>>
        >>> score = await evaluate(
        ...     input="What is 2+2?",
        ...     output="4",
        ...     expected_output="4",
        ...     evaluator_name="exact_match"
        ... )
        >>>
        >>> # Or use a judge
        >>> score = await evaluate(
        ...     input="Explain AI",
        ...     output="AI is...",
        ...     judge_name="response_quality"
        ... )
    """
    async with EvaluationsClient() as client:
        if judge_name:
            return await client.evaluate_with_judge(
                input=input,
                output=output,
                judge_name=judge_name,
                expected_output=expected_output,
                **kwargs,
            )
        return await client.evaluate(
            input=input,
            output=output,
            expected_output=expected_output,
            evaluator_name=evaluator_name,
            **kwargs,
        )
