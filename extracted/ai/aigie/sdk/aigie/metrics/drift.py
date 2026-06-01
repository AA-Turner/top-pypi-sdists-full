"""
Drift Detection Metric.

Measures context drift severity using LLM-as-judge pattern.
Production-grade implementation with proper error handling, logging, and caching.
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Any

from ..evaluation import EvaluationResult, ScoreType
from .base import BaseMetric

logger = logging.getLogger(__name__)


class DriftDetectionMetric(BaseMetric):
    """
    Metric for detecting and measuring context drift severity.

    Uses LLM-as-judge to evaluate if agent context has drifted from expected patterns.
    Designed for production use with proper error handling and fallback mechanisms.

    Usage:
        metric = DriftDetectionMetric(threshold=0.7)
        result = await metric.measure(
            input="User query",
            output="Agent response",
            context={"baseline_context": "...", "current_context": "..."}
        )
    """

    def __init__(
        self,
        threshold: float = 0.7,
        name: str | None = None,
        description: str | None = None,
        use_llm_judge: bool = True,
        fallback_to_rule_based: bool = True,
    ):
        """
        Initialize drift detection metric.

        Args:
            threshold: Minimum score to consider drift acceptable (0.0-1.0)
            name: Metric name (defaults to class name)
            description: Metric description
            use_llm_judge: Whether to use LLM-as-judge (requires API access)
            fallback_to_rule_based: Fallback to rule-based if LLM fails
        """
        super().__init__(
            threshold=threshold,
            name=name or "DriftDetection",
            description=description or "Measures context drift severity",
        )
        self.use_llm_judge = use_llm_judge
        self.fallback_to_rule_based = fallback_to_rule_based
        # Thread-safe cache with size limit (LRU eviction)
        import threading
        from collections import OrderedDict

        self._cache: OrderedDict[str, EvaluationResult] = OrderedDict()
        self._cache_lock = threading.Lock()
        self._cache_max_size = 100  # Limit cache to 100 entries

    async def measure(
        self, input: Any, output: Any, context: dict[str, Any] | None = None
    ) -> EvaluationResult:
        """
        Measure context drift severity.

        Args:
            input: Function/span input
            output: Function/span output
            context: Optional context (DriftContext TypedDict) containing:
                - baseline_context: Expected/previous context
                - current_context: Current context to compare
                - drift_type: Type of drift (semantic, structural, etc.)
                - trace_id: Trace ID for reference

        Returns:
            EvaluationResult with drift score (0.0 = severe drift, 1.0 = no drift)

        Raises:
            TypeError: If context is not a dict
            ValueError: If required context fields are missing
        """
        # Validate context type
        context = self._validate_context(context)

        try:
            # Extract context data
            baseline_context = context.get("baseline_context")
            current_context = context.get("current_context")
            drift_type = context.get("drift_type", "semantic")

            # Validate inputs
            if not baseline_context and not current_context:
                # Try to extract from input/output
                baseline_context = self._extract_context(input)
                current_context = self._extract_context(output)

            if not baseline_context or not current_context:
                logger.warning(
                    f"DriftDetectionMetric: Missing context data. "
                    f"baseline={bool(baseline_context)}, current={bool(current_context)}"
                )
                return self._create_fallback_result(
                    score=0.5, explanation="Insufficient context data for drift detection"
                )

            # Check cache (thread-safe)
            cache_key = self._create_cache_key(baseline_context, current_context)
            with self._cache_lock:
                if cache_key in self._cache:
                    # Move to end (LRU)
                    result = self._cache.pop(cache_key)
                    self._cache[cache_key] = result
                    logger.debug(
                        f"DriftDetectionMetric: Using cached result for {cache_key[:20]}..."
                    )
                    return result

            # Try LLM-as-judge if enabled
            if self.use_llm_judge:
                try:
                    result = await self._evaluate_with_llm(
                        baseline_context, current_context, drift_type, context
                    )
                    # Cache result (thread-safe with LRU eviction)
                    with self._cache_lock:
                        if cache_key in self._cache:
                            # Update existing
                            self._cache.pop(cache_key)
                        elif len(self._cache) >= self._cache_max_size:
                            # Evict oldest (first item)
                            self._cache.popitem(last=False)
                        self._cache[cache_key] = result
                    return result
                except Exception as e:
                    logger.warning(
                        f"DriftDetectionMetric: LLM evaluation failed: {e}. "
                        f"Falling back to rule-based evaluation."
                    )
                    if not self.fallback_to_rule_based:
                        raise

            # Fallback to rule-based evaluation
            result = await self._evaluate_rule_based(baseline_context, current_context, drift_type)
            # Cache result (thread-safe with LRU eviction)
            with self._cache_lock:
                if cache_key in self._cache:
                    self._cache.pop(cache_key)
                elif len(self._cache) >= self._cache_max_size:
                    self._cache.popitem(last=False)
                self._cache[cache_key] = result
            return result

        except Exception as e:
            logger.error(f"DriftDetectionMetric: Error measuring drift: {e}", exc_info=True)
            return self._create_fallback_result(
                score=0.5, explanation=f"Error evaluating drift: {e!s}"
            )

    async def _evaluate_with_llm(
        self, baseline_context: str, current_context: str, drift_type: str, context: dict[str, Any]
    ) -> EvaluationResult:
        """
        Evaluate drift using LLM-as-judge.

        This would integrate with the backend's UnifiedLLMJudgeService.
        For SDK-only usage, we provide a prompt-based approach.
        """
        # Build evaluation prompt
        prompt = self._build_drift_evaluation_prompt(baseline_context, current_context, drift_type)

        # In production, this would call the backend API or use a local LLM
        # For now, we'll use a simplified approach that can be extended
        try:
            # Try to use backend API if available
            api_url = context.get("api_url")
            if api_url:
                return await self._call_backend_api(api_url, prompt, context)
        except Exception as e:
            logger.debug(f"Backend API not available: {e}")

        # Fallback to rule-based if LLM not available
        logger.info("DriftDetectionMetric: LLM judge not available, using rule-based")
        return await self._evaluate_rule_based(baseline_context, current_context, drift_type)

    def _build_drift_evaluation_prompt(
        self, baseline_context: str, current_context: str, drift_type: str
    ) -> str:
        """Build prompt for LLM drift evaluation."""
        return f"""You are an expert evaluator for AI agent context drift detection.

Evaluate if the agent's context has drifted from the expected baseline.

**Baseline Context (Expected):**
{baseline_context[:1000]}

**Current Context (Actual):**
{current_context[:1000]}

**Drift Type:** {drift_type}

**Evaluation Criteria:**
1. Semantic similarity (0.0-1.0): How similar is the meaning?
2. Structural consistency (0.0-1.0): How similar is the structure?
3. Intent alignment (0.0-1.0): Are the intents aligned?
4. Overall drift score (0.0-1.0): 0.0 = severe drift, 1.0 = no drift

**Output Format (JSON only, no markdown):**
{{
    "score": 0.85,
    "reasoning": "Detailed explanation of drift assessment",
    "confidence": 0.90,
    "drift_severity": "low|medium|high",
    "drift_areas": ["semantic", "structural"]
}}"""

    async def _evaluate_rule_based(
        self, baseline_context: str, current_context: str, drift_type: str
    ) -> EvaluationResult:
        """
        Rule-based drift evaluation as fallback.

        Uses simple heuristics when LLM is not available.
        """
        # Simple similarity check (can be enhanced with embeddings)
        baseline_words = set(baseline_context.lower().split())
        current_words = set(current_context.lower().split())

        if not baseline_words:
            return self._create_fallback_result(score=0.5, explanation="Empty baseline context")

        # Jaccard similarity
        intersection = len(baseline_words & current_words)
        union = len(baseline_words | current_words)
        similarity = intersection / union if union > 0 else 0.0

        # Length difference penalty
        length_diff = abs(len(baseline_context) - len(current_context))
        max_length = max(len(baseline_context), len(current_context))
        length_penalty = 1.0 - (length_diff / max_length) if max_length > 0 else 1.0

        # Combined score
        score = similarity * 0.7 + length_penalty * 0.3

        # Determine severity
        if score < 0.5:
            severity = "high"
        elif score < 0.7:
            severity = "medium"
        else:
            severity = "low"

        return EvaluationResult(
            score=score,
            score_type=ScoreType.CUSTOM,
            explanation=(
                f"Rule-based drift detection: {severity} drift detected. "
                f"Similarity: {similarity:.2f}, Length penalty: {length_penalty:.2f}"
            ),
            metadata={
                "drift_severity": severity,
                "similarity": similarity,
                "length_penalty": length_penalty,
                "evaluation_method": "rule_based",
                "timestamp": datetime.utcnow().isoformat(),
            },
        )

    def _extract_context(self, data: Any) -> str:
        """Extract context string from various data types."""
        if isinstance(data, str):
            return data
        if isinstance(data, dict):
            # Try common context fields
            for field in ["context", "input", "query", "prompt", "message"]:
                if field in data:
                    return str(data[field])
            # Fallback to JSON string
            return json.dumps(data, default=str)
        if isinstance(data, (list, tuple)):
            return " ".join(str(item) for item in data)
        return str(data)

    def _create_cache_key(self, baseline: str, current: str) -> str:
        """Create cache key for evaluation results."""
        import hashlib

        combined = f"{baseline[:100]}{current[:100]}"
        return hashlib.md5(combined.encode()).hexdigest()

    async def _call_backend_api(
        self, api_url: str, prompt: str, context: dict[str, Any]
    ) -> EvaluationResult:
        """
        Call backend API for LLM evaluation with retry logic.

        Integrates with backend's EvalsClient.evaluate_drift() if available.
        Uses exponential backoff retry for transient failures.
        """
        import httpx
        from httpx import HTTPStatusError, RequestError, TimeoutException

        # Retry configuration
        max_retries = 3
        base_delay = 1.0  # seconds
        max_delay = 30.0  # seconds

        # Extract drift data from context
        trace_id = context.get("trace_id")
        baseline_context = context.get("baseline_context")
        current_context = context.get("current_context")
        drift_type = context.get("drift_type", "semantic")

        if not trace_id or not baseline_context or not current_context:
            raise ValueError("Missing required context for drift evaluation")

        # Retry loop with exponential backoff
        last_exception = None
        for attempt in range(max_retries):
            try:
                async with httpx.AsyncClient(timeout=30.0) as client:
                    response = await client.post(
                        f"{api_url}/evals/drift",
                        json={
                            "trace_id": trace_id,
                            "drift_type": drift_type,
                            "current_context": current_context,
                            "baseline_context": baseline_context,
                            "baseline_trace_id": context.get("baseline_trace_id"),
                            "similarity_score": context.get("similarity_score"),
                        },
                    )
                    response.raise_for_status()
                    data = response.json()

                    # Success - return result
                    return EvaluationResult(
                        score=0.5,  # Placeholder until job completes
                        score_type=ScoreType.CUSTOM,
                        explanation="Drift evaluation job created, awaiting results",
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
                        f"Backend API timeout for drift evaluation (trace_id={trace_id}, "
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
                        f"Backend API client error for drift evaluation (trace_id={trace_id}): "
                        f"{e.response.status_code} - {e}"
                    )
                    raise  # Don't retry client errors
                # Server error (5xx) - retry
                last_exception = e
                if attempt < max_retries - 1:
                    delay = min(base_delay * (2**attempt), max_delay)
                    logger.warning(
                        f"Backend API server error for drift evaluation (trace_id={trace_id}, "
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
                        f"Backend API request error for drift evaluation (trace_id={trace_id}, "
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
