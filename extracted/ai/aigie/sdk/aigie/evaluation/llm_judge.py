"""
LLM-as-Judge Evaluation Framework for Kytte Production Runtime.

Integrates with Kytte's Detect → Evaluate → Fix flow:
- Runtime agent evaluation for instant error identification
- Scoring outputs for remediation decisions
- Compatible with backend's UnifiedLLMJudgeService

This is the EVALUATE step in Kytte's autonomous remediation pipeline.
"""

import json
import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any

logger = logging.getLogger(__name__)


class EvaluationCriteria(Enum):
    """Standard evaluation criteria for LLM outputs."""

    RELEVANCE = "relevance"
    COHERENCE = "coherence"
    FACTUALITY = "factuality"
    HELPFULNESS = "helpfulness"
    SAFETY = "safety"
    ACCURACY = "accuracy"
    COMPLETENESS = "completeness"
    CONCISENESS = "conciseness"
    CREATIVITY = "creativity"
    TONE = "tone"
    GRAMMAR = "grammar"
    CUSTOM = "custom"


@dataclass
class JudgeConfig:
    """Configuration for the LLM judge.

    Attributes:
        model: Model to use for evaluation (e.g., "gpt-4o-mini", "claude-3-haiku")
        temperature: Temperature for judge responses (lower = more consistent)
        max_tokens: Maximum tokens for judge response
        provider: LLM provider ("openai", "anthropic", "google", "auto")
        api_key: Optional API key (uses environment variable if not provided)
        timeout: Request timeout in seconds
        max_retries: Maximum retries for failed evaluations
    """

    model: str = "gpt-4o-mini"
    temperature: float = 0.0  # Low temperature for consistent scoring
    max_tokens: int = 1024
    provider: str = "auto"  # auto-detect from model name
    api_key: str | None = None
    timeout: float = 30.0
    max_retries: int = 2


@dataclass
class CriterionScore:
    """Score for a single evaluation criterion."""

    criterion: str
    score: float  # 0.0 to 1.0
    reasoning: str
    confidence: float = 1.0


@dataclass
class EvaluationResult:
    """Result of an LLM-as-Judge evaluation.

    Attributes:
        overall_score: Aggregate score (0.0 to 1.0)
        criterion_scores: Individual scores for each criterion
        feedback: Human-readable feedback/summary
        raw_response: Raw judge response for debugging
        model: Model used for evaluation
        timestamp: When evaluation was performed
        duration_ms: Time taken for evaluation
        metadata: Additional metadata
    """

    overall_score: float
    criterion_scores: list[CriterionScore]
    feedback: str
    raw_response: str | None = None
    model: str | None = None
    timestamp: datetime = field(default_factory=datetime.now)
    duration_ms: float | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "overall_score": self.overall_score,
            "criterion_scores": [
                {
                    "criterion": cs.criterion,
                    "score": cs.score,
                    "reasoning": cs.reasoning,
                    "confidence": cs.confidence,
                }
                for cs in self.criterion_scores
            ],
            "feedback": self.feedback,
            "model": self.model,
            "timestamp": self.timestamp.isoformat(),
            "duration_ms": self.duration_ms,
            "metadata": self.metadata,
        }

    @property
    def passed(self) -> bool:
        """Check if evaluation passed (score >= 0.7)."""
        return self.overall_score >= 0.7

    def get_score(self, criterion: str) -> float | None:
        """Get score for a specific criterion."""
        for cs in self.criterion_scores:
            if cs.criterion.lower() == criterion.lower():
                return cs.score
        return None


class LLMJudge:
    """
    LLM-as-Judge for evaluating AI outputs.

    Provides structured evaluation using LLMs to score outputs
    against various quality criteria.

    Example:
        >>> judge = LLMJudge()
        >>> result = await judge.evaluate(
        ...     input="What is the capital of France?",
        ...     output="The capital of France is Paris.",
        ...     criteria=["relevance", "accuracy"],
        ... )
        >>> print(f"Score: {result.overall_score}")
        Score: 0.95
    """

    # Standard prompts for each criterion
    CRITERION_PROMPTS = {
        "relevance": "How relevant is the response to the given input/question?",
        "coherence": "How coherent and well-structured is the response?",
        "factuality": "Are the facts stated in the response accurate and verifiable?",
        "helpfulness": "How helpful is the response in addressing the user's needs?",
        "safety": "Is the response safe and free from harmful content?",
        "accuracy": "How accurate and correct is the information provided?",
        "completeness": "Does the response fully address all aspects of the query?",
        "conciseness": "Is the response appropriately concise without being too brief?",
        "creativity": "Does the response show appropriate creativity where beneficial?",
        "tone": "Is the tone appropriate for the context?",
        "grammar": "Is the response grammatically correct and well-written?",
    }

    def __init__(self, config: JudgeConfig | None = None):
        """
        Initialize the LLM judge.

        Args:
            config: Configuration for the judge. Uses defaults if not provided.
        """
        self.config = config or JudgeConfig()
        self._client = None

    async def evaluate(
        self,
        input: str,
        output: str,
        criteria: list[str] | None = None,
        reference: str | None = None,
        context: str | None = None,
        custom_prompts: dict[str, str] | None = None,
        model: str | None = None,
    ) -> EvaluationResult:
        """
        Evaluate an LLM output against specified criteria.

        Args:
            input: The original input/question/prompt
            output: The LLM's response to evaluate
            criteria: List of criteria to evaluate (default: ["relevance", "helpfulness"])
            reference: Optional reference/ground truth answer for comparison
            context: Optional additional context for evaluation
            custom_prompts: Custom prompts for specific criteria
            model: Override model for this evaluation

        Returns:
            EvaluationResult with scores and feedback
        """
        import time

        start_time = time.time()

        # Default criteria if not specified
        if not criteria:
            criteria = ["relevance", "helpfulness"]

        # Normalize criteria names
        criteria = [c.lower() for c in criteria]

        # Build evaluation prompt
        prompt = self._build_evaluation_prompt(
            input=input,
            output=output,
            criteria=criteria,
            reference=reference,
            context=context,
            custom_prompts=custom_prompts,
        )

        # Get evaluation from LLM
        model_to_use = model or self.config.model
        raw_response = await self._call_llm(prompt, model_to_use)

        # Parse response
        result = self._parse_evaluation_response(
            raw_response=raw_response,
            criteria=criteria,
            model=model_to_use,
        )

        # Add timing info
        result.duration_ms = (time.time() - start_time) * 1000
        result.metadata["input_preview"] = input[:100] + "..." if len(input) > 100 else input
        result.metadata["output_preview"] = output[:100] + "..." if len(output) > 100 else output

        return result

    async def compare(
        self,
        input: str,
        output_a: str,
        output_b: str,
        criteria: list[str] | None = None,
    ) -> dict[str, Any]:
        """
        Compare two outputs and determine which is better.

        Args:
            input: The original input/question/prompt
            output_a: First output to compare
            output_b: Second output to compare
            criteria: Criteria to use for comparison

        Returns:
            Dictionary with winner, scores, and reasoning
        """
        # Evaluate both outputs
        result_a = await self.evaluate(input, output_a, criteria)
        result_b = await self.evaluate(input, output_b, criteria)

        winner = (
            "A"
            if result_a.overall_score > result_b.overall_score
            else ("B" if result_b.overall_score > result_a.overall_score else "tie")
        )

        return {
            "winner": winner,
            "score_a": result_a.overall_score,
            "score_b": result_b.overall_score,
            "score_diff": abs(result_a.overall_score - result_b.overall_score),
            "result_a": result_a.to_dict(),
            "result_b": result_b.to_dict(),
            "reasoning": f"Output {winner} scored higher"
            if winner != "tie"
            else "Both outputs scored equally",
        }

    async def batch_evaluate(
        self,
        samples: list[dict[str, str]],
        criteria: list[str] | None = None,
    ) -> list[EvaluationResult]:
        """
        Evaluate multiple input-output pairs.

        Args:
            samples: List of {"input": str, "output": str} dictionaries
            criteria: Criteria to evaluate

        Returns:
            List of EvaluationResults
        """
        results = []
        for sample in samples:
            result = await self.evaluate(
                input=sample["input"],
                output=sample["output"],
                criteria=criteria,
                reference=sample.get("reference"),
                context=sample.get("context"),
            )
            results.append(result)
        return results

    def _build_evaluation_prompt(
        self,
        input: str,
        output: str,
        criteria: list[str],
        reference: str | None = None,
        context: str | None = None,
        custom_prompts: dict[str, str] | None = None,
    ) -> str:
        """Build the evaluation prompt for the judge LLM."""
        custom_prompts = custom_prompts or {}

        # Build criteria descriptions
        criteria_descriptions = []
        for criterion in criteria:
            if criterion in custom_prompts:
                desc = custom_prompts[criterion]
            elif criterion in self.CRITERION_PROMPTS:
                desc = self.CRITERION_PROMPTS[criterion]
            else:
                desc = f"Evaluate the {criterion} of the response."
            criteria_descriptions.append(f"- {criterion.upper()}: {desc}")

        prompt = f"""You are an expert AI evaluator. Evaluate the following response based on the specified criteria.

INPUT/QUESTION:
{input}

RESPONSE TO EVALUATE:
{output}
"""

        if reference:
            prompt += f"""
REFERENCE/EXPECTED ANSWER:
{reference}
"""

        if context:
            prompt += f"""
ADDITIONAL CONTEXT:
{context}
"""

        prompt += f"""
EVALUATION CRITERIA:
{chr(10).join(criteria_descriptions)}

INSTRUCTIONS:
1. Evaluate the response for each criterion on a scale of 0.0 to 1.0
2. Provide brief reasoning for each score
3. Calculate an overall score (weighted average)
4. Provide constructive feedback

Respond in the following JSON format:
{{
    "criterion_scores": [
        {{"criterion": "criterion_name", "score": 0.0-1.0, "reasoning": "brief explanation"}}
    ],
    "overall_score": 0.0-1.0,
    "feedback": "constructive feedback summary"
}}

Only output valid JSON, no other text."""

        return prompt

    async def _call_llm(self, prompt: str, model: str) -> str:
        """Call the LLM for evaluation."""
        provider = self._detect_provider(model)

        try:
            if provider == "openai":
                return await self._call_openai(prompt, model)
            if provider == "anthropic":
                return await self._call_anthropic(prompt, model)
            if provider == "google":
                return await self._call_google(prompt, model)
            # Default to OpenAI-compatible API
            return await self._call_openai(prompt, model)
        except Exception as e:
            logger.error(f"LLM call failed: {e}")
            # Return fallback response for parsing
            return json.dumps(
                {
                    "criterion_scores": [],
                    "overall_score": 0.0,
                    "feedback": f"Evaluation failed: {e!s}",
                }
            )

    def _detect_provider(self, model: str) -> str:
        """Detect provider from model name."""
        if self.config.provider != "auto":
            return self.config.provider

        model_lower = model.lower()
        if "gpt" in model_lower or "o1" in model_lower:
            return "openai"
        if "claude" in model_lower:
            return "anthropic"
        if "gemini" in model_lower:
            return "google"
        return "openai"  # Default

    async def _call_openai(self, prompt: str, model: str) -> str:
        """Call OpenAI API."""
        import os

        try:
            from openai import AsyncOpenAI
        except ImportError:
            raise ImportError(
                "openai package required for OpenAI evaluations. Install with: pip install openai"
            )

        api_key = self.config.api_key or os.getenv("OPENAI_API_KEY")
        client = AsyncOpenAI(api_key=api_key)

        response = await client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens,
            timeout=self.config.timeout,
        )

        return response.choices[0].message.content or ""

    async def _call_anthropic(self, prompt: str, model: str) -> str:
        """Call Anthropic API."""
        import os

        try:
            from anthropic import AsyncAnthropic
        except ImportError:
            raise ImportError(
                "anthropic package required for Anthropic evaluations. Install with: pip install anthropic"
            )

        api_key = self.config.api_key or os.getenv("ANTHROPIC_API_KEY")
        client = AsyncAnthropic(api_key=api_key)

        response = await client.messages.create(
            model=model,
            max_tokens=self.config.max_tokens,
            messages=[{"role": "user", "content": prompt}],
        )

        return response.content[0].text if response.content else ""

    async def _call_google(self, prompt: str, model: str) -> str:
        """Call Google Generative AI API."""
        import os

        try:
            import google.generativeai as genai
        except ImportError:
            raise ImportError(
                "google-generativeai package required for Google evaluations. Install with: pip install google-generativeai"
            )

        api_key = self.config.api_key or os.getenv("GOOGLE_API_KEY")
        genai.configure(api_key=api_key)

        gen_model = genai.GenerativeModel(model)
        response = await gen_model.generate_content_async(prompt)

        return response.text if response.text else ""

    def _parse_evaluation_response(
        self,
        raw_response: str,
        criteria: list[str],
        model: str,
    ) -> EvaluationResult:
        """Parse the LLM's evaluation response."""
        try:
            # Try to extract JSON from response
            json_str = raw_response
            if "```json" in raw_response:
                json_str = raw_response.split("```json")[1].split("```")[0]
            elif "```" in raw_response:
                json_str = raw_response.split("```")[1].split("```")[0]

            data = json.loads(json_str.strip())

            criterion_scores = []
            for cs in data.get("criterion_scores", []):
                criterion_scores.append(
                    CriterionScore(
                        criterion=cs.get("criterion", "unknown"),
                        score=float(cs.get("score", 0.0)),
                        reasoning=cs.get("reasoning", ""),
                        confidence=float(cs.get("confidence", 1.0)),
                    )
                )

            # Fill in missing criteria with 0 score
            found_criteria = {cs.criterion.lower() for cs in criterion_scores}
            for criterion in criteria:
                if criterion.lower() not in found_criteria:
                    criterion_scores.append(
                        CriterionScore(
                            criterion=criterion,
                            score=0.0,
                            reasoning="Not evaluated",
                            confidence=0.0,
                        )
                    )

            return EvaluationResult(
                overall_score=float(data.get("overall_score", 0.0)),
                criterion_scores=criterion_scores,
                feedback=data.get("feedback", ""),
                raw_response=raw_response,
                model=model,
            )

        except (json.JSONDecodeError, KeyError, ValueError) as e:
            logger.warning(f"Failed to parse evaluation response: {e}")
            return EvaluationResult(
                overall_score=0.0,
                criterion_scores=[],
                feedback=f"Failed to parse evaluation: {e!s}",
                raw_response=raw_response,
                model=model,
            )

    # ==================== Kytte Integration ====================

    def to_backend_format(self, result: EvaluationResult) -> dict[str, Any]:
        """
        Convert EvaluationResult to Kytte backend's JudgeEvaluation format.

        This enables seamless integration with the backend's:
        - UnifiedLLMJudgeService
        - RemediationEvaluator
        - Learning system

        Args:
            result: EvaluationResult from evaluate()

        Returns:
            Dict compatible with backend's JudgeEvaluation
        """
        return {
            "score": result.overall_score,
            "reasoning": result.feedback,
            "confidence": sum(cs.confidence for cs in result.criterion_scores)
            / max(len(result.criterion_scores), 1),
            "focus_areas": {cs.criterion: cs.score for cs in result.criterion_scores},
            "metadata": {
                "model": result.model,
                "duration_ms": result.duration_ms,
                "criterion_count": len(result.criterion_scores),
                **result.metadata,
            },
        }

    def needs_remediation(self, result: EvaluationResult, threshold: float = 0.7) -> bool:
        """
        Determine if evaluation result indicates remediation is needed.

        Part of Kytte's Detect → Evaluate → Fix flow.

        Args:
            result: EvaluationResult to check
            threshold: Score threshold below which remediation is needed

        Returns:
            True if remediation should be triggered
        """
        return result.overall_score < threshold

    def get_remediation_trigger(
        self,
        result: EvaluationResult,
        threshold: float = 0.7,
    ) -> dict[str, Any] | None:
        """
        Get remediation trigger info if evaluation indicates issues.

        Integrates with Kytte's RemediationService by providing trigger
        information for remediation plans.

        Args:
            result: EvaluationResult to analyze
            threshold: Score threshold for triggering remediation

        Returns:
            Remediation trigger dict or None if no remediation needed
        """
        if not self.needs_remediation(result, threshold):
            return None

        # Identify worst performing criteria
        failed_criteria = [cs for cs in result.criterion_scores if cs.score < threshold]

        # Map criteria to trigger types
        trigger_type = "validation_error"
        if any(cs.criterion.lower() in ["factuality", "accuracy"] for cs in failed_criteria):
            trigger_type = "context_drift"  # Hallucination/drift detected
        elif any(cs.criterion.lower() in ["relevance", "helpfulness"] for cs in failed_criteria):
            trigger_type = "api_error"  # Quality issue

        return {
            "trigger_type": trigger_type,
            "trigger_metadata": {
                "evaluation_score": result.overall_score,
                "failed_criteria": [
                    {"criterion": cs.criterion, "score": cs.score, "reasoning": cs.reasoning}
                    for cs in failed_criteria
                ],
                "model": result.model,
                "feedback": result.feedback,
            },
            "suggestions": [
                {
                    "action": "retry_with_context",
                    "description": f"Low score ({result.overall_score:.2f}) - retry with improved prompt",
                    "confidence": 1.0 - result.overall_score,
                }
            ],
        }

    async def evaluate_for_remediation(
        self,
        input: str,
        output: str,
        error: Exception | None = None,
        context: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Evaluate output specifically for remediation decision.

        Part of Kytte's Detect → Evaluate → Fix flow:
        1. DETECT: Error/issue already detected (passed as error param)
        2. EVALUATE: This method scores the output
        3. FIX: Returns remediation trigger info

        Args:
            input: Original input/prompt
            output: LLM output to evaluate
            error: Optional detected error
            context: Additional context

        Returns:
            Dict with evaluation and remediation info:
            - evaluation: Full evaluation result
            - needs_remediation: bool
            - remediation_trigger: Trigger info for RemediationService
        """
        # Choose criteria based on context
        criteria = ["relevance", "helpfulness", "accuracy"]
        if error:
            criteria.append("safety")

        # Evaluate
        result = await self.evaluate(
            input=input,
            output=output,
            criteria=criteria,
            context=str(context) if context else None,
        )

        # Determine remediation needs
        needs_fix = self.needs_remediation(result) or error is not None
        trigger = self.get_remediation_trigger(result) if needs_fix else None

        # Add error info to trigger if present
        if trigger and error:
            trigger["trigger_metadata"]["error_type"] = type(error).__name__
            trigger["trigger_metadata"]["error_message"] = str(error)

        return {
            "evaluation": result.to_dict(),
            "backend_format": self.to_backend_format(result),
            "needs_remediation": needs_fix,
            "remediation_trigger": trigger,
        }
