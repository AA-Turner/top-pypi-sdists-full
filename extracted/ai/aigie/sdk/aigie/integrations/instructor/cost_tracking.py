"""
Cost tracking utilities for Instructor integration.

Provides model pricing and token extraction for Instructor structured output calls.
Tracks costs across extraction attempts including validation retries.
"""

import logging
from dataclasses import dataclass
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class ModelPricing:
    """Pricing information for a model."""

    input_cost_per_million: float  # Cost per 1M input tokens
    output_cost_per_million: float  # Cost per 1M output tokens
    provider: str = "unknown"


# Model pricing for commonly used models with Instructor
INSTRUCTOR_MODEL_PRICING: dict[str, ModelPricing] = {
    # OpenAI models (most common with Instructor)
    "gpt-4o": ModelPricing(2.50, 10.00, "openai"),
    "gpt-4o-mini": ModelPricing(0.15, 0.60, "openai"),
    "gpt-4o-2024-11-20": ModelPricing(2.50, 10.00, "openai"),
    "gpt-4o-2024-08-06": ModelPricing(2.50, 10.00, "openai"),
    "gpt-4-turbo": ModelPricing(10.00, 30.00, "openai"),
    "gpt-4-turbo-preview": ModelPricing(10.00, 30.00, "openai"),
    "gpt-4-1106-preview": ModelPricing(10.00, 30.00, "openai"),
    "gpt-4": ModelPricing(30.00, 60.00, "openai"),
    "gpt-4-32k": ModelPricing(60.00, 120.00, "openai"),
    "gpt-3.5-turbo": ModelPricing(0.50, 1.50, "openai"),
    "gpt-3.5-turbo-1106": ModelPricing(1.00, 2.00, "openai"),
    "gpt-3.5-turbo-16k": ModelPricing(3.00, 4.00, "openai"),
    "o1-preview": ModelPricing(15.00, 60.00, "openai"),
    "o1-mini": ModelPricing(3.00, 12.00, "openai"),
    "o1": ModelPricing(15.00, 60.00, "openai"),
    "o3-mini": ModelPricing(1.10, 4.40, "openai"),
    # Anthropic models
    "claude-3-5-sonnet-20241022": ModelPricing(3.00, 15.00, "anthropic"),
    "claude-3-5-sonnet-latest": ModelPricing(3.00, 15.00, "anthropic"),
    "claude-3-5-haiku-20241022": ModelPricing(0.80, 4.00, "anthropic"),
    "claude-3-opus-20240229": ModelPricing(15.00, 75.00, "anthropic"),
    "claude-3-sonnet-20240229": ModelPricing(3.00, 15.00, "anthropic"),
    "claude-3-haiku-20240307": ModelPricing(0.25, 1.25, "anthropic"),
    "claude-opus-4-20250514": ModelPricing(15.00, 75.00, "anthropic"),
    "claude-sonnet-4-20250514": ModelPricing(3.00, 15.00, "anthropic"),
    # Google models
    "gemini-2.0-flash": ModelPricing(0.10, 0.40, "google"),
    "gemini-1.5-pro": ModelPricing(1.25, 5.00, "google"),
    "gemini-1.5-flash": ModelPricing(0.075, 0.30, "google"),
    "gemini-1.0-pro": ModelPricing(0.50, 1.50, "google"),
    # Cohere models
    "command-r-plus": ModelPricing(3.00, 15.00, "cohere"),
    "command-r": ModelPricing(0.50, 1.50, "cohere"),
    # Mistral models
    "mistral-large-latest": ModelPricing(4.00, 12.00, "mistral"),
    "mistral-medium-latest": ModelPricing(2.70, 8.10, "mistral"),
    "mistral-small-latest": ModelPricing(1.00, 3.00, "mistral"),
    # Groq models (common for fast extraction)
    "llama-3.1-70b-versatile": ModelPricing(0.59, 0.79, "groq"),
    "llama-3.1-8b-instant": ModelPricing(0.05, 0.08, "groq"),
    "mixtral-8x7b-32768": ModelPricing(0.24, 0.24, "groq"),
    # Together AI models
    "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo": ModelPricing(0.88, 0.88, "together"),
    "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo": ModelPricing(0.18, 0.18, "together"),
}


def extract_tokens_from_response(response: Any) -> dict[str, int]:
    """Extract token usage from various Instructor/LLM response formats.

    Args:
        response: The LLM response object

    Returns:
        Dictionary with input_tokens, output_tokens, total_tokens
    """
    input_tokens = 0
    output_tokens = 0
    cache_read_tokens = 0
    cache_creation_tokens = 0

    try:
        # Method 1: OpenAI response format (most common with Instructor)
        if hasattr(response, "usage"):
            usage = response.usage
            if hasattr(usage, "prompt_tokens"):
                input_tokens = usage.prompt_tokens or 0
                output_tokens = getattr(usage, "completion_tokens", 0) or 0
                cache_read_tokens = getattr(usage, "cache_read_input_tokens", 0) or 0
                cache_creation_tokens = getattr(usage, "cache_creation_input_tokens", 0) or 0
            elif isinstance(usage, dict):
                input_tokens = usage.get("prompt_tokens") or usage.get("input_tokens") or 0
                output_tokens = usage.get("completion_tokens") or usage.get("output_tokens") or 0
                cache_read_tokens = usage.get("cache_read_input_tokens", 0) or 0
                cache_creation_tokens = usage.get("cache_creation_input_tokens", 0) or 0

        # Method 2: Anthropic response format
        if not (input_tokens or output_tokens) and hasattr(response, "usage"):
            usage = response.usage
            if hasattr(usage, "input_tokens"):
                input_tokens = usage.input_tokens or 0
                output_tokens = getattr(usage, "output_tokens", 0) or 0
                cache_read_tokens = getattr(usage, "cache_read_input_tokens", 0) or 0
                cache_creation_tokens = getattr(usage, "cache_creation_input_tokens", 0) or 0

        # Method 3: Dict-based response (litellm, etc.)
        if not (input_tokens or output_tokens) and isinstance(response, dict):
            usage = response.get("usage", {})
            if usage:
                input_tokens = usage.get("prompt_tokens") or usage.get("input_tokens") or 0
                output_tokens = usage.get("completion_tokens") or usage.get("output_tokens") or 0
                cache_read_tokens = usage.get("cache_read_input_tokens", 0) or 0
                cache_creation_tokens = usage.get("cache_creation_input_tokens", 0) or 0

        # Method 4: Response metadata (some providers)
        if not (input_tokens or output_tokens) and hasattr(response, "response_metadata"):
            metadata = response.response_metadata
            if isinstance(metadata, dict):
                usage = metadata.get("usage", {})
                input_tokens = usage.get("prompt_tokens") or usage.get("input_tokens") or 0
                output_tokens = usage.get("completion_tokens") or usage.get("output_tokens") or 0
                cache_read_tokens = usage.get("cache_read_input_tokens", 0) or 0
                cache_creation_tokens = usage.get("cache_creation_input_tokens", 0) or 0

        # Method 5: _raw_response attribute (instructor internal)
        if not (input_tokens or output_tokens) and hasattr(response, "_raw_response"):
            raw = response._raw_response
            if hasattr(raw, "usage"):
                usage = raw.usage
                if hasattr(usage, "prompt_tokens"):
                    input_tokens = usage.prompt_tokens or 0
                    output_tokens = getattr(usage, "completion_tokens", 0) or 0

    except Exception as e:
        logger.debug(f"Error extracting tokens from response: {e}")

    return {
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": input_tokens + output_tokens,
        "cache_read_input_tokens": cache_read_tokens,
        "cache_creation_input_tokens": cache_creation_tokens,
    }


def get_instructor_cost(
    model: str,
    input_tokens: int,
    output_tokens: int,
    fallback_to_aigie: bool = True,
) -> dict[str, Any] | None:
    """Calculate cost for an Instructor extraction call.

    Args:
        model: The model name/identifier
        input_tokens: Number of input tokens
        output_tokens: Number of output tokens
        fallback_to_aigie: Whether to fallback to main aigie cost tracking

    Returns:
        Dictionary with cost breakdown or None if pricing not found
    """
    # Normalize model name
    model_lower = model.lower() if model else ""

    # Try exact match first
    pricing = INSTRUCTOR_MODEL_PRICING.get(model)

    # Try lowercase match
    if not pricing:
        pricing = INSTRUCTOR_MODEL_PRICING.get(model_lower)

    # Try partial match for model families
    if not pricing:
        for model_key, model_pricing in INSTRUCTOR_MODEL_PRICING.items():
            if model_key in model_lower or model_lower in model_key:
                pricing = model_pricing
                break

    # Fallback to main aigie cost tracking
    if not pricing and fallback_to_aigie:
        try:
            from ...cost_tracking import get_model_pricing

            pricing = get_model_pricing(model)
        except ImportError:
            pass

    if not pricing:
        return None

    # Calculate costs
    input_cost = (input_tokens / 1_000_000) * pricing.input_cost_per_million
    output_cost = (output_tokens / 1_000_000) * pricing.output_cost_per_million
    total_cost = input_cost + output_cost

    return {
        "input_cost": input_cost,
        "output_cost": output_cost,
        "total_cost": total_cost,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "model": model,
        "provider": pricing.provider,
        "input_cost_per_million": pricing.input_cost_per_million,
        "output_cost_per_million": pricing.output_cost_per_million,
    }


def extract_model_from_client(client: Any) -> str | None:
    """Extract model name from an Instructor-patched client.

    Args:
        client: The Instructor-patched client object

    Returns:
        Model name or None
    """
    # Common attribute names for model
    model_attrs = [
        "model",
        "model_name",
        "_model",
        "default_model",
        "model_id",
    ]

    for attr in model_attrs:
        if hasattr(client, attr):
            value = getattr(client, attr)
            if isinstance(value, str) and value:
                return value

    # Check kwargs or settings
    if hasattr(client, "kwargs"):
        kwargs = client.kwargs
        if isinstance(kwargs, dict) and "model" in kwargs:
            return kwargs["model"]

    # Check client._client for inner client model
    if hasattr(client, "_client"):
        inner = client._client
        for attr in model_attrs:
            if hasattr(inner, attr):
                value = getattr(inner, attr)
                if isinstance(value, str) and value:
                    return value

    return None


@dataclass
class ExtractionAttempt:
    """Records a single extraction attempt."""

    attempt_number: int
    success: bool
    input_tokens: int = 0
    output_tokens: int = 0
    cost: float = 0.0
    duration_ms: float = 0.0
    validation_error: str | None = None


class InstructorCostTracker:
    """
    Tracks costs across multiple Instructor extraction calls with per-model breakdown.

    Includes tracking of validation retry costs, which can be significant for
    complex structured outputs.
    """

    def __init__(self):
        self._total_cost: float = 0.0
        self._total_input_tokens: int = 0
        self._total_output_tokens: int = 0
        self._by_model: dict[str, dict[str, Any]] = {}
        self._extraction_count: int = 0
        self._retry_count: int = 0
        self._retry_cost: float = 0.0
        self._attempts: list[ExtractionAttempt] = []

    def add_usage(
        self,
        model: str,
        input_tokens: int = 0,
        output_tokens: int = 0,
        cost: float | None = None,
        is_retry: bool = False,
    ) -> float:
        """
        Add usage from an Instructor extraction call.

        Args:
            model: Model name
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens
            cost: Pre-calculated cost (if None, will be calculated)
            is_retry: Whether this is a validation retry attempt

        Returns:
            Cost for this call in USD
        """
        if cost is None:
            cost_info = get_instructor_cost(model, input_tokens, output_tokens)
            cost = cost_info.get("total_cost", 0.0) if cost_info else 0.0

        # Update totals
        self._total_cost += cost
        self._total_input_tokens += input_tokens
        self._total_output_tokens += output_tokens

        if is_retry:
            self._retry_count += 1
            self._retry_cost += cost
        else:
            self._extraction_count += 1

        # Update per-model breakdown
        if model not in self._by_model:
            self._by_model[model] = {
                "cost": 0.0,
                "input_tokens": 0,
                "output_tokens": 0,
                "call_count": 0,
                "retry_count": 0,
                "retry_cost": 0.0,
            }

        self._by_model[model]["cost"] += cost
        self._by_model[model]["input_tokens"] += input_tokens
        self._by_model[model]["output_tokens"] += output_tokens
        self._by_model[model]["call_count"] += 1

        if is_retry:
            self._by_model[model]["retry_count"] += 1
            self._by_model[model]["retry_cost"] += cost

        return cost

    def record_attempt(
        self,
        attempt_number: int,
        success: bool,
        input_tokens: int = 0,
        output_tokens: int = 0,
        cost: float = 0.0,
        duration_ms: float = 0.0,
        validation_error: str | None = None,
    ) -> None:
        """Record a detailed extraction attempt."""
        attempt = ExtractionAttempt(
            attempt_number=attempt_number,
            success=success,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cost=cost,
            duration_ms=duration_ms,
            validation_error=validation_error[:200] if validation_error else None,
        )
        self._attempts.append(attempt)

    @property
    def total_cost(self) -> float:
        """Total cost in USD (including retries)."""
        return self._total_cost

    @property
    def retry_cost(self) -> float:
        """Cost spent on validation retries."""
        return self._retry_cost

    @property
    def total_tokens(self) -> int:
        """Total tokens (input + output)."""
        return self._total_input_tokens + self._total_output_tokens

    @property
    def retry_ratio(self) -> float:
        """Ratio of retry cost to total cost."""
        if self._total_cost == 0:
            return 0.0
        return self._retry_cost / self._total_cost

    def get_costs_by_model(self) -> dict[str, dict[str, Any]]:
        """Get cost breakdown by model."""
        return self._by_model.copy()

    def get_summary(self) -> dict[str, Any]:
        """Get full cost tracking summary."""
        return {
            "total_cost": self._total_cost,
            "total_input_tokens": self._total_input_tokens,
            "total_output_tokens": self._total_output_tokens,
            "total_tokens": self.total_tokens,
            "extraction_count": self._extraction_count,
            "retry_count": self._retry_count,
            "retry_cost": self._retry_cost,
            "retry_cost_ratio": self.retry_ratio,
            "by_model": self._by_model,
            "attempts": [
                {
                    "attempt": a.attempt_number,
                    "success": a.success,
                    "tokens": a.input_tokens + a.output_tokens,
                    "cost": a.cost,
                }
                for a in self._attempts[-20:]  # Last 20 attempts
            ],
        }

    def reset(self) -> None:
        """Reset all tracked costs."""
        self._total_cost = 0.0
        self._total_input_tokens = 0
        self._total_output_tokens = 0
        self._by_model = {}
        self._extraction_count = 0
        self._retry_count = 0
        self._retry_cost = 0.0
        self._attempts = []


def aggregate_extraction_costs(extraction_costs: list[dict[str, Any]]) -> dict[str, Any]:
    """
    Aggregate costs from multiple extraction calls.

    Args:
        extraction_costs: List of cost dictionaries from individual extractions

    Returns:
        Aggregated cost summary with per-model breakdown
    """
    total_cost = 0.0
    total_input_tokens = 0
    total_output_tokens = 0
    total_retry_cost = 0.0
    by_model: dict[str, dict[str, Any]] = {}

    for cost_entry in extraction_costs:
        if not cost_entry:
            continue

        total_cost += cost_entry.get("total_cost", cost_entry.get("cost", 0.0))
        total_input_tokens += cost_entry.get("input_tokens", 0)
        total_output_tokens += cost_entry.get("output_tokens", 0)
        total_retry_cost += cost_entry.get("retry_cost", 0.0)

        model = cost_entry.get("model", "unknown")
        if model not in by_model:
            by_model[model] = {
                "cost": 0.0,
                "input_tokens": 0,
                "output_tokens": 0,
                "call_count": 0,
                "retry_count": 0,
            }

        by_model[model]["cost"] += cost_entry.get("total_cost", cost_entry.get("cost", 0.0))
        by_model[model]["input_tokens"] += cost_entry.get("input_tokens", 0)
        by_model[model]["output_tokens"] += cost_entry.get("output_tokens", 0)
        by_model[model]["call_count"] += 1
        by_model[model]["retry_count"] += cost_entry.get("retry_count", 0)

    return {
        "total_cost": total_cost,
        "total_input_tokens": total_input_tokens,
        "total_output_tokens": total_output_tokens,
        "total_tokens": total_input_tokens + total_output_tokens,
        "total_retry_cost": total_retry_cost,
        "retry_cost_ratio": total_retry_cost / total_cost if total_cost > 0 else 0.0,
        "by_model": by_model,
        "extraction_count": len(extraction_costs),
    }
