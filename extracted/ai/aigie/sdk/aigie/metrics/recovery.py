"""
Recovery Success Metric.

Measures error recovery effectiveness using LLM-as-judge pattern.
Production-grade implementation with proper error handling and logging.
"""

import asyncio
import logging
from datetime import datetime
from typing import Any

from aigie.evaluation import EvaluationResult, ScoreType
from aigie.metrics.base import BaseMetric

logger = logging.getLogger(__name__)


class RecoverySuccessMetric(BaseMetric):
    """
    Metric for measuring error recovery effectiveness.

    Evaluates if error recovery strategies were successful and effective.
    Designed for production use with comprehensive error handling.

    Usage:
        metric = RecoverySuccessMetric(threshold=0.8)
        result = await metric.measure(
            input={"error": "..."},
            output={"recovered": True},
            context={"recovery_strategy": "retry", "recovery_duration_ms": 100}
        )
    """

    def __init__(
        self,
        threshold: float = 0.8,
        name: str | None = None,
        description: str | None = None,
        use_llm_judge: bool = True,
        fallback_to_rule_based: bool = True,
    ):
        """
        Initialize recovery success metric.

        Args:
            threshold: Minimum score for successful recovery (0.0-1.0)
            name: Metric name (defaults to class name)
            description: Metric description
            use_llm_judge: Whether to use LLM-as-judge
            fallback_to_rule_based: Fallback to rule-based if LLM fails
        """
        super().__init__(
            threshold=threshold,
            name=name or "RecoverySuccess",
            description=description or "Measures error recovery effectiveness",
        )
        self.use_llm_judge = use_llm_judge
        self.fallback_to_rule_based = fallback_to_rule_based

    async def measure(
        self, input: Any, output: Any, context: dict[str, Any] | None = None
    ) -> EvaluationResult:
        """
        Measure recovery success.

        Args:
            input: Original error or input that caused error
            output: Recovery result or recovered output
            context: Optional context containing:
                - original_error: Original error information
                - recovery_strategy: Strategy used (retry, fallback, etc.)
                - recovery_duration_ms: Time taken for recovery
                - recovery_success: Boolean indicating if recovery succeeded
                - error_type: Type of error

        Returns:
            EvaluationResult with recovery score (0.0 = failed, 1.0 = perfect recovery)
        """
        # Validate context type
        context = self._validate_context(context)

        try:
            # Extract recovery data
            original_error = self._extract_error(input, context)
            recovery_result = self._extract_recovery(output, context)
            recovery_strategy = context.get("recovery_strategy", "unknown")
            recovery_duration_ms = context.get("recovery_duration_ms", 0)
            recovery_success = context.get("recovery_success")
            error_type = context.get("error_type", "unknown")

            if not original_error:
                logger.warning("RecoverySuccessMetric: Missing original error information")
                return self._create_fallback_result(
                    score=0.5, explanation="Insufficient error information for recovery evaluation"
                )

            # Try LLM-as-judge if enabled
            if self.use_llm_judge:
                try:
                    return await self._evaluate_with_llm(
                        original_error,
                        recovery_result,
                        recovery_strategy,
                        recovery_duration_ms,
                        recovery_success,
                        error_type,
                        context,
                    )
                except Exception as e:
                    logger.warning(
                        f"RecoverySuccessMetric: LLM evaluation failed: {e}. "
                        f"Falling back to rule-based evaluation."
                    )
                    if not self.fallback_to_rule_based:
                        raise

            # Fallback to rule-based evaluation
            return await self._evaluate_rule_based(
                original_error,
                recovery_result,
                recovery_strategy,
                recovery_duration_ms,
                recovery_success,
            )

        except Exception as e:
            logger.error(f"RecoverySuccessMetric: Error measuring recovery: {e}", exc_info=True)
            return self._create_fallback_result(
                score=0.5, explanation=f"Error evaluating recovery: {e!s}"
            )

    async def _evaluate_with_llm(
        self,
        original_error: str,
        recovery_result: str,
        recovery_strategy: str,
        recovery_duration_ms: int,
        recovery_success: bool | None,
        error_type: str,
        context: dict[str, Any],
    ) -> EvaluationResult:
        """Evaluate recovery using LLM-as-judge."""
        prompt = self._build_recovery_evaluation_prompt(
            original_error,
            recovery_result,
            recovery_strategy,
            recovery_duration_ms,
            recovery_success,
            error_type,
        )

        # Try backend API if available
        api_url = context.get("api_url")
        if api_url:
            try:
                return await self._call_backend_api(api_url, prompt, context)
            except Exception as e:
                logger.debug(f"Backend API not available: {e}")

        # Fallback to rule-based
        logger.info("RecoverySuccessMetric: LLM judge not available, using rule-based")
        return await self._evaluate_rule_based(
            original_error,
            recovery_result,
            recovery_strategy,
            recovery_duration_ms,
            recovery_success,
        )

    def _build_recovery_evaluation_prompt(
        self,
        original_error: str,
        recovery_result: str,
        recovery_strategy: str,
        recovery_duration_ms: int,
        recovery_success: bool | None,
        error_type: str,
    ) -> str:
        """Build prompt for LLM recovery evaluation."""
        return f"""You are an expert evaluator for AI agent error recovery effectiveness.

Evaluate if the error recovery was successful and effective.

**Original Error:**
{original_error[:500]}

**Recovery Result:**
{recovery_result[:500]}

**Recovery Strategy:** {recovery_strategy}
**Recovery Duration:** {recovery_duration_ms}ms
**Error Type:** {error_type}
**Recovery Success (Boolean):** {recovery_success}

**Evaluation Criteria:**
1. Recovery success (0.0-1.0): Was the error successfully recovered?
2. Recovery quality (0.0-1.0): How well was the error handled?
3. Recovery speed (0.0-1.0): Was recovery fast enough?
4. User impact (0.0-1.0): Was user experience maintained?
5. Overall recovery score (0.0-1.0): 0.0 = failed, 1.0 = perfect recovery

**Output Format (JSON only, no markdown):**
{{
    "score": 0.85,
    "reasoning": "Detailed explanation of recovery assessment",
    "confidence": 0.90,
    "recovery_quality": "excellent|good|adequate|poor",
    "factors": {{
        "success": 0.9,
        "quality": 0.85,
        "speed": 0.8,
        "user_impact": 0.9
    }}
}}"""

    async def _evaluate_rule_based(
        self,
        original_error: str,
        recovery_result: str,
        recovery_strategy: str,
        recovery_duration_ms: int,
        recovery_success: bool | None,
    ) -> EvaluationResult:
        """Rule-based recovery evaluation."""
        # Base score from recovery success
        if recovery_success is True:
            base_score = 0.8
        elif recovery_success is False:
            base_score = 0.2
        else:
            # Unknown - check if recovery_result exists
            base_score = 0.6 if recovery_result else 0.3

        # Speed penalty (faster is better, but not too fast)
        if recovery_duration_ms < 100:
            speed_score = 1.0
        elif recovery_duration_ms < 500:
            speed_score = 0.9
        elif recovery_duration_ms < 1000:
            speed_score = 0.7
        elif recovery_duration_ms < 5000:
            speed_score = 0.5
        else:
            speed_score = 0.3

        # Strategy bonus
        strategy_scores = {"retry": 0.8, "fallback": 0.7, "circuit_breaker": 0.6, "manual": 0.5}
        strategy_score = strategy_scores.get(recovery_strategy.lower(), 0.6)

        # Combined score
        score = base_score * 0.6 + speed_score * 0.2 + strategy_score * 0.2

        # Determine quality
        if score >= 0.8:
            quality = "excellent"
        elif score >= 0.6:
            quality = "good"
        elif score >= 0.4:
            quality = "adequate"
        else:
            quality = "poor"

        return EvaluationResult(
            score=score,
            score_type=ScoreType.CUSTOM,
            explanation=(
                f"Rule-based recovery evaluation: {quality} recovery. "
                f"Base: {base_score:.2f}, Speed: {speed_score:.2f}, Strategy: {strategy_score:.2f}"
            ),
            metadata={
                "recovery_quality": quality,
                "base_score": base_score,
                "speed_score": speed_score,
                "strategy_score": strategy_score,
                "recovery_duration_ms": recovery_duration_ms,
                "recovery_strategy": recovery_strategy,
                "evaluation_method": "rule_based",
                "timestamp": datetime.utcnow().isoformat(),
            },
        )

    def _extract_error(self, input: Any, context: dict[str, Any]) -> str:
        """Extract error information from input or context."""
        # Try context first
        if "original_error" in context:
            error = context["original_error"]
            if isinstance(error, dict):
                return error.get("error_message", str(error))
            return str(error)

        # Try input
        if isinstance(input, dict):
            for field in ["error", "error_message", "exception", "failure"]:
                if field in input:
                    return str(input[field])

        # Fallback
        if isinstance(input, Exception):
            return str(input)

        return str(input) if input else ""

    def _extract_recovery(self, output: Any, context: dict[str, Any]) -> str:
        """Extract recovery result from output or context."""
        # Try context
        if "recovery_result" in context:
            return str(context["recovery_result"])

        # Try output
        if isinstance(output, dict):
            for field in ["recovered", "result", "output", "response"]:
                if field in output:
                    return str(output[field])

        return str(output) if output else ""

    async def _call_backend_api(
        self, api_url: str, prompt: str, context: dict[str, Any]
    ) -> EvaluationResult:
        """
        Call backend API for LLM evaluation with retry logic.

        Integrates with backend's EvalsClient.evaluate_recovery() if available.
        Uses exponential backoff retry for transient failures.
        """
        import httpx
        from httpx import HTTPStatusError, RequestError, TimeoutException

        # Retry configuration
        max_retries = 3
        base_delay = 1.0  # seconds
        max_delay = 30.0  # seconds

        # Extract recovery data from context
        trace_id = context.get("trace_id")
        original_error = context.get("original_error", str(context.get("error", "")))
        error_type = context.get("error_type", "unknown")
        recovery_strategy = context.get("recovery_strategy", "unknown")
        recovery_success = context.get("recovery_success", False)
        recovery_duration_ms = context.get("recovery_duration_ms", 0)

        if not trace_id:
            raise ValueError("Missing trace_id for recovery evaluation")

        # Retry loop with exponential backoff
        last_exception = None
        for attempt in range(max_retries):
            try:
                async with httpx.AsyncClient(timeout=30.0) as client:
                    response = await client.post(
                        f"{api_url}/evals/recovery",
                        json={
                            "trace_id": trace_id,
                            "original_error": original_error,
                            "error_type": error_type,
                            "recovery_strategy": recovery_strategy,
                            "recovery_success": recovery_success,
                            "recovery_duration_ms": recovery_duration_ms,
                            "recovery_metadata": context.get("recovery_metadata", {}),
                        },
                    )
                    response.raise_for_status()
                    data = response.json()

                    # Success - return result
                    return EvaluationResult(
                        score=0.5,  # Placeholder until job completes
                        score_type=ScoreType.CUSTOM,
                        explanation="Recovery evaluation job created, awaiting results",
                        metadata={
                            "job_execution_id": data.get("job_execution_id"),
                            "status": "pending",
                            "evaluation_method": "backend_api",
                            "retry_attempt": attempt + 1,
                            "timestamp": datetime.utcnow().isoformat(),
                        },
                    )

            except TimeoutException as e:
                last_exception = e
                if attempt < max_retries - 1:
                    delay = min(base_delay * (2**attempt), max_delay)
                    logger.warning(
                        f"Backend API timeout for recovery evaluation (trace_id={trace_id}, "
                        f"attempt {attempt + 1}/{max_retries}), retrying in {delay:.1f}s..."
                    )
                    await asyncio.sleep(delay)
                    continue
                logger.error(
                    f"Backend API timeout after {max_retries} attempts (trace_id={trace_id}): {e}"
                )
                raise  # Trigger fallback

            except HTTPStatusError as e:
                # Don't retry on client errors (4xx), only server errors (5xx)
                if 400 <= e.response.status_code < 500:
                    logger.warning(
                        f"Backend API client error for recovery evaluation (trace_id={trace_id}): "
                        f"{e.response.status_code} - {e}"
                    )
                    raise  # Don't retry client errors
                # Server error (5xx) - retry
                last_exception = e
                if attempt < max_retries - 1:
                    delay = min(base_delay * (2**attempt), max_delay)
                    logger.warning(
                        f"Backend API server error for recovery evaluation (trace_id={trace_id}, "
                        f"attempt {attempt + 1}/{max_retries}, status={e.response.status_code}), "
                        f"retrying in {delay:.1f}s..."
                    )
                    await asyncio.sleep(delay)
                    continue
                logger.error(
                    f"Backend API server error after {max_retries} attempts "
                    f"(trace_id={trace_id}): {e}"
                )
                raise  # Trigger fallback

            except RequestError as e:
                # Network errors - retry
                last_exception = e
                if attempt < max_retries - 1:
                    delay = min(base_delay * (2**attempt), max_delay)
                    logger.warning(
                        f"Backend API request error for recovery evaluation (trace_id={trace_id}, "
                        f"attempt {attempt + 1}/{max_retries}), retrying in {delay:.1f}s...: {e}"
                    )
                    await asyncio.sleep(delay)
                    continue
                logger.error(
                    f"Backend API request error after {max_retries} attempts "
                    f"(trace_id={trace_id}): {e}"
                )
                raise  # Trigger fallback

        # Should never reach here, but just in case
        if last_exception:
            raise last_exception
        raise RuntimeError(f"Failed to call backend API after {max_retries} attempts")

    def _create_fallback_result(self, score: float, explanation: str) -> EvaluationResult:
        """Create fallback result on error."""
        return EvaluationResult(
            score=score,
            score_type=ScoreType.CUSTOM,
            explanation=explanation,
            metadata={"error": True, "timestamp": datetime.utcnow().isoformat()},
        )
