"""
Judges API Client for Aigie SDK

Interact with Aigie's predefined evaluation judges for assessing
LLM outputs across various quality dimensions.

Platform-provided judges:
- Response Quality: Evaluates coherence, clarity, and overall quality
- Factual Accuracy: Checks for factual correctness and consistency
- Safety: Evaluates for harmful, biased, or inappropriate content
- Relevance: Checks if response is relevant to the input
- Task Completion: Evaluates if the requested task was completed
"""

import os
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any

import httpx


class JudgeType(str, Enum):
    """Types of predefined judges."""

    RESPONSE_QUALITY = "response_quality"
    FACTUAL_ACCURACY = "factual_accuracy"
    SAFETY = "safety"
    RELEVANCE = "relevance"
    TASK_COMPLETION = "task_completion"
    CUSTOM = "custom"


@dataclass
class Judge:
    """Predefined evaluation judge."""

    id: str
    name: str
    type: JudgeType
    description: str
    criteria: str
    model: str  # LLM used for evaluation
    created_at: str
    is_builtin: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class JudgeResult:
    """Result from a judge evaluation."""

    judge_id: str
    judge_name: str
    score: float  # 0-1
    passed: bool
    reasoning: str
    created_at: str
    trace_id: str | None = None
    span_id: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class JudgeConfig:
    """Configuration for custom judges."""

    name: str
    description: str
    criteria: str
    model: str = "gemini-1.5-flash"
    threshold: float = 0.5
    metadata: dict[str, Any] = field(default_factory=dict)


class JudgesClient:
    """
    Judges API client for Aigie.

    Provides access to predefined evaluation judges and the ability
    to create custom judges.

    Example:
        >>> from aigie.judges import JudgesClient, JudgeType
        >>>
        >>> client = JudgesClient()
        >>>
        >>> # List available judges
        >>> judges = await client.list_judges()
        >>> for judge in judges:
        ...     print(f"{judge.name}: {judge.description}")
        >>>
        >>> # Run a judge evaluation
        >>> result = await client.run_judge(
        ...     judge_type=JudgeType.RESPONSE_QUALITY,
        ...     input="Explain quantum computing",
        ...     output="Quantum computing uses qubits...",
        ... )
        >>> print(f"Score: {result.score}, Passed: {result.passed}")
        >>> print(f"Reasoning: {result.reasoning}")
        >>>
        >>> # Create a custom judge
        >>> custom_judge = await client.create_judge(
        ...     name="code_review",
        ...     description="Reviews code quality",
        ...     criteria="Check for best practices, security, performance"
        ... )
    """

    # Built-in judge descriptions
    BUILTIN_JUDGES = {
        JudgeType.RESPONSE_QUALITY: {
            "name": "Response Quality",
            "description": "Evaluates response coherence, clarity, and overall quality",
            "criteria": "Assess the response for clarity, coherence, completeness, and professional quality.",
        },
        JudgeType.FACTUAL_ACCURACY: {
            "name": "Factual Accuracy",
            "description": "Checks for factual correctness and consistency",
            "criteria": "Verify factual claims, check for contradictions, and assess accuracy.",
        },
        JudgeType.SAFETY: {
            "name": "Safety",
            "description": "Evaluates for harmful, biased, or inappropriate content",
            "criteria": "Check for harmful content, bias, inappropriate language, and safety concerns.",
        },
        JudgeType.RELEVANCE: {
            "name": "Relevance",
            "description": "Checks if response is relevant to the input",
            "criteria": "Assess whether the response directly addresses the input query or task.",
        },
        JudgeType.TASK_COMPLETION: {
            "name": "Task Completion",
            "description": "Evaluates if the requested task was completed",
            "criteria": "Determine if the task requested was fully completed as specified.",
        },
    }

    def __init__(
        self,
        api_url: str | None = None,
        api_key: str | None = None,
    ):
        """
        Initialize judges client.

        Args:
            api_url: API URL (defaults to AIGIE_API_URL env var)
            api_key: API key (defaults to AIGIE_API_KEY env var)
        """
        self.api_url = api_url or os.getenv("AIGIE_API_URL", "")
        self.api_key = api_key or os.getenv("AIGIE_API_KEY", "")
        self.client = httpx.AsyncClient(timeout=60.0)

    async def list_judges(
        self,
        include_custom: bool = True,
        limit: int = 100,
        offset: int = 0,
    ) -> list[Judge]:
        """
        List available judges.

        Args:
            include_custom: Include custom judges (not just builtin)
            limit: Maximum judges to return
            offset: Pagination offset

        Returns:
            List of available judges
        """
        params = {
            "includeCustom": include_custom,
            "limit": limit,
            "offset": offset,
        }

        response = await self._request("GET", "/v1/judges", params=params)

        # Backend may return a flat list or a dict with "judges" key
        items = response if isinstance(response, list) else response.get("judges", [])

        judges = []
        for j in items:
            judges.append(
                Judge(
                    id=j["id"],
                    name=j["name"],
                    type=JudgeType(j.get("type", "custom")),
                    description=j.get("description", ""),
                    criteria=j.get("criteria", ""),
                    model=j.get("model", "gemini-1.5-flash"),
                    created_at=j.get("createdAt", ""),
                    is_builtin=j.get("isBuiltin", False),
                    metadata=j.get("metadata", {}),
                )
            )

        return judges

    async def get_judge(self, judge_id: str) -> Judge:
        """
        Get a specific judge by ID.

        Args:
            judge_id: Judge ID

        Returns:
            Judge details
        """
        response = await self._request("GET", f"/v1/judges/{judge_id}")

        return Judge(
            id=response["id"],
            name=response["name"],
            type=JudgeType(response.get("type", "custom")),
            description=response.get("description", ""),
            criteria=response.get("criteria", ""),
            model=response.get("model", "gemini-1.5-flash"),
            created_at=response.get("createdAt", ""),
            is_builtin=response.get("isBuiltin", False),
            metadata=response.get("metadata", {}),
        )

    async def run_judge(
        self,
        input: Any,
        output: Any,
        judge_type: JudgeType | None = None,
        judge_id: str | None = None,
        expected_output: Any | None = None,
        context: dict[str, Any] | None = None,
        trace_id: str | None = None,
        span_id: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> JudgeResult:
        """
        Run a judge evaluation.

        Args:
            input: The input that was provided
            output: The output that was generated
            judge_type: Type of builtin judge to use
            judge_id: ID of custom judge to use (alternative to judge_type)
            expected_output: Optional expected output for comparison
            context: Additional context for the judge
            trace_id: Optional trace ID to attach result to
            span_id: Optional span ID to attach result to
            metadata: Additional metadata

        Returns:
            JudgeResult with the evaluation
        """
        if not judge_type and not judge_id:
            raise ValueError("Either judge_type or judge_id must be provided")

        # Build criteria list from judge_type or judge_id
        criteria = []
        if judge_type:
            criteria.append(judge_type.value)
        if judge_id:
            criteria.append(judge_id)

        data = {
            "trace_id": trace_id or "",
            "step_index": 0,
            "step_name": "sdk_evaluation",
            "step_type": "llm_response",
            "step_content": str(output),
            "criteria": criteria,
            "metadata": {
                **(metadata or {}),
                "input": input,
                "expected_output": expected_output,
                "context": context or {},
            },
        }
        if span_id:
            data["span_id"] = span_id

        response = await self._request("POST", "/v1/judges/evaluate-step", json=data)

        # evaluate-step returns { evaluations: [...], has_issues: bool }
        evaluations = response.get("evaluations", [])
        has_issues = response.get("has_issues", False)

        if evaluations:
            ev = evaluations[0]  # Primary evaluation result
            return JudgeResult(
                judge_id=ev.get("judge_id", ev.get("judgeId", "")),
                judge_name=ev.get("judge_name", ev.get("judgeName", "")),
                score=float(ev.get("score", 0)),
                passed=not has_issues,
                reasoning=ev.get("reasoning", ""),
                created_at=ev.get("created_at", ev.get("createdAt", datetime.utcnow().isoformat())),
                trace_id=trace_id,
                span_id=span_id,
                metadata=ev.get("metadata", {}),
            )

        # Fallback if no evaluations returned
        return JudgeResult(
            judge_id="",
            judge_name="",
            score=0.0,
            passed=not has_issues,
            reasoning=response.get("reasoning", "No evaluations returned"),
            created_at=datetime.utcnow().isoformat(),
            trace_id=trace_id,
            span_id=span_id,
            metadata={},
        )

    async def run_all_judges(
        self,
        input: Any,
        output: Any,
        judge_types: list[JudgeType] | None = None,
        expected_output: Any | None = None,
        context: dict[str, Any] | None = None,
        trace_id: str | None = None,
        span_id: str | None = None,
    ) -> list[JudgeResult]:
        """
        Run multiple judges on the same input/output.

        Args:
            input: The input that was provided
            output: The output that was generated
            judge_types: List of judge types to run (defaults to all builtin)
            expected_output: Optional expected output
            context: Additional context
            trace_id: Optional trace ID
            span_id: Optional span ID

        Returns:
            List of JudgeResult from each judge
        """
        if judge_types is None:
            judge_types = list(JudgeType)
            # Remove CUSTOM as it requires a judge_id
            judge_types = [jt for jt in judge_types if jt != JudgeType.CUSTOM]

        results = []
        for judge_type in judge_types:
            try:
                result = await self.run_judge(
                    input=input,
                    output=output,
                    judge_type=judge_type,
                    expected_output=expected_output,
                    context=context,
                    trace_id=trace_id,
                    span_id=span_id,
                )
                results.append(result)
            except Exception as e:
                # Log error but continue with other judges
                import logging

                logging.getLogger(__name__).warning(f"Judge {judge_type.value} failed: {e}")

        return results

    async def create_judge(
        self,
        name: str,
        description: str,
        criteria: str,
        model: str = "gemini-1.5-flash",
        threshold: float = 0.5,
        metadata: dict[str, Any] | None = None,
    ) -> Judge:
        """
        Create a custom judge.

        Args:
            name: Judge name
            description: What this judge evaluates
            criteria: Evaluation criteria/prompt
            model: LLM model to use for evaluation
            threshold: Score threshold for passing (0-1)
            metadata: Additional metadata

        Returns:
            Created Judge
        """
        data = {
            "name": name,
            "description": description,
            "criteria": criteria,
            "model": model,
            "threshold": threshold,
            "metadata": metadata or {},
        }

        response = await self._request("POST", "/v1/judges", json=data)

        return Judge(
            id=response["id"],
            name=response["name"],
            type=JudgeType.CUSTOM,
            description=response.get("description", ""),
            criteria=response.get("criteria", ""),
            model=response.get("model", model),
            created_at=response.get("createdAt", datetime.utcnow().isoformat()),
            is_builtin=False,
            metadata=response.get("metadata", {}),
        )

    async def update_judge(
        self,
        judge_id: str,
        name: str | None = None,
        description: str | None = None,
        criteria: str | None = None,
        model: str | None = None,
        threshold: float | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> Judge:
        """
        Update a custom judge.

        Args:
            judge_id: Judge ID to update
            name: New name
            description: New description
            criteria: New criteria
            model: New model
            threshold: New threshold
            metadata: New metadata

        Returns:
            Updated Judge
        """
        data = {}
        if name is not None:
            data["name"] = name
        if description is not None:
            data["description"] = description
        if criteria is not None:
            data["criteria"] = criteria
        if model is not None:
            data["model"] = model
        if threshold is not None:
            data["threshold"] = threshold
        if metadata is not None:
            data["metadata"] = metadata

        response = await self._request("PATCH", f"/v1/judges/{judge_id}", json=data)

        return Judge(
            id=response["id"],
            name=response["name"],
            type=JudgeType(response.get("type", "custom")),
            description=response.get("description", ""),
            criteria=response.get("criteria", ""),
            model=response.get("model", ""),
            created_at=response.get("createdAt", ""),
            is_builtin=response.get("isBuiltin", False),
            metadata=response.get("metadata", {}),
        )

    async def delete_judge(self, judge_id: str) -> None:
        """
        Delete a custom judge.

        Args:
            judge_id: Judge ID to delete
        """
        await self._request("DELETE", f"/v1/judges/{judge_id}")

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

            if response.status_code == 204:
                return {}
            return response.json()

        except httpx.HTTPError as error:
            import logging

            logging.getLogger(__name__).error(f"Judges API Error [{method} {path}]: {error}")
            raise

    async def close(self):
        """Close HTTP client."""
        await self.client.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()


# Convenience functions for quick judge usage
async def judge(
    input: Any,
    output: Any,
    judge_type: JudgeType = JudgeType.RESPONSE_QUALITY,
    **kwargs,
) -> JudgeResult:
    """
    Run a quick judge evaluation.

    Example:
        >>> from aigie.judges import judge, JudgeType
        >>>
        >>> result = await judge(
        ...     input="What is AI?",
        ...     output="AI is artificial intelligence...",
        ...     judge_type=JudgeType.RESPONSE_QUALITY
        ... )
        >>> print(f"Passed: {result.passed}")
    """
    async with JudgesClient() as client:
        return await client.run_judge(
            input=input,
            output=output,
            judge_type=judge_type,
            **kwargs,
        )


async def judge_all(
    input: Any,
    output: Any,
    **kwargs,
) -> list[JudgeResult]:
    """
    Run all builtin judges on input/output.

    Example:
        >>> from aigie.judges import judge_all
        >>>
        >>> results = await judge_all(
        ...     input="What is AI?",
        ...     output="AI is artificial intelligence..."
        ... )
        >>> for r in results:
        ...     print(f"{r.judge_name}: {r.score:.2f}")
    """
    async with JudgesClient() as client:
        return await client.run_all_judges(
            input=input,
            output=output,
            **kwargs,
        )
