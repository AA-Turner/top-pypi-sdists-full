"""
Cost tracking utilities for DSPy integration.

Provides model pricing for LLM calls commonly used with DSPy.
DSPy supports multiple LLM backends, so we include broad coverage.
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


# DSPy commonly used LLM models
# DSPy supports multiple backends (OpenAI, Anthropic, local, etc.)
DSPY_MODEL_PRICING: dict[str, ModelPricing] = {
    # OpenAI models
    "gpt-4o": ModelPricing(2.50, 10.00, "openai"),
    "gpt-4o-mini": ModelPricing(0.15, 0.60, "openai"),
    "gpt-4-turbo": ModelPricing(10.00, 30.00, "openai"),
    "gpt-4": ModelPricing(30.00, 60.00, "openai"),
    "gpt-3.5-turbo": ModelPricing(0.50, 1.50, "openai"),
    "o1-preview": ModelPricing(15.00, 60.00, "openai"),
    "o1-mini": ModelPricing(3.00, 12.00, "openai"),
    # Anthropic models
    "claude-3-5-sonnet-20241022": ModelPricing(3.00, 15.00, "anthropic"),
    "claude-3-5-sonnet-latest": ModelPricing(3.00, 15.00, "anthropic"),
    "claude-3-5-haiku-20241022": ModelPricing(0.80, 4.00, "anthropic"),
    "claude-3-opus-20240229": ModelPricing(15.00, 75.00, "anthropic"),
    "claude-3-sonnet-20240229": ModelPricing(3.00, 15.00, "anthropic"),
    "claude-3-haiku-20240307": ModelPricing(0.25, 1.25, "anthropic"),
    # Google models
    "gemini-2.0-flash": ModelPricing(0.10, 0.40, "google"),
    "gemini-1.5-pro": ModelPricing(1.25, 5.00, "google"),
    "gemini-1.5-flash": ModelPricing(0.075, 0.30, "google"),
    # Together AI models (common DSPy backend)
    "meta-llama/Llama-3.2-70B-Instruct-Turbo": ModelPricing(0.88, 0.88, "together"),
    "meta-llama/Llama-3.2-11B-Instruct-Turbo": ModelPricing(0.18, 0.18, "together"),
    "meta-llama/Llama-3.2-3B-Instruct-Turbo": ModelPricing(0.06, 0.06, "together"),
    "mistralai/Mixtral-8x7B-Instruct-v0.1": ModelPricing(0.60, 0.60, "together"),
    "mistralai/Mistral-7B-Instruct-v0.2": ModelPricing(0.20, 0.20, "together"),
    # Groq models
    "llama-3.3-70b-versatile": ModelPricing(0.59, 0.79, "groq"),
    "llama-3.1-70b-versatile": ModelPricing(0.59, 0.79, "groq"),
    "llama-3.1-8b-instant": ModelPricing(0.05, 0.08, "groq"),
    "mixtral-8x7b-32768": ModelPricing(0.24, 0.24, "groq"),
    "gemma2-9b-it": ModelPricing(0.20, 0.20, "groq"),
    # Local models (free)
    "llama3": ModelPricing(0.0, 0.0, "local"),
    "llama3.2": ModelPricing(0.0, 0.0, "local"),
    "mistral": ModelPricing(0.0, 0.0, "local"),
    "mixtral": ModelPricing(0.0, 0.0, "local"),
    "phi3": ModelPricing(0.0, 0.0, "local"),
    "qwen2.5": ModelPricing(0.0, 0.0, "local"),
}


def extract_tokens_from_lm_response(response: Any) -> dict[str, int]:
    """Extract token usage from various DSPy LM response formats.

    Args:
        response: The LM response object

    Returns:
        Dictionary with input_tokens, output_tokens, total_tokens
    """
    input_tokens = 0
    output_tokens = 0

    try:
        # Method 1: Direct token counts on response
        if hasattr(response, "usage"):
            usage = response.usage
            if hasattr(usage, "prompt_tokens"):
                input_tokens = usage.prompt_tokens or 0
                output_tokens = usage.completion_tokens or 0
            elif isinstance(usage, dict):
                input_tokens = usage.get("prompt_tokens") or usage.get("input_tokens") or 0
                output_tokens = usage.get("completion_tokens") or usage.get("output_tokens") or 0

        # Method 2: DSPy-specific metadata
        if not (input_tokens or output_tokens) and hasattr(response, "_metadata"):
            meta = response._metadata
            if isinstance(meta, dict):
                input_tokens = meta.get("input_tokens", 0)
                output_tokens = meta.get("output_tokens", 0)

        # Method 3: Raw response data
        if not (input_tokens or output_tokens) and hasattr(response, "raw"):
            raw = response.raw
            if isinstance(raw, dict) and "usage" in raw:
                usage = raw["usage"]
                input_tokens = usage.get("prompt_tokens", 0)
                output_tokens = usage.get("completion_tokens", 0)

    except Exception as e:
        logger.debug(f"Error extracting tokens from response: {e}")

    return {
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": input_tokens + output_tokens,
    }


def get_dspy_cost(
    model: str,
    input_tokens: int,
    output_tokens: int,
    fallback_to_aigie: bool = True,
) -> dict[str, Any] | None:
    """Calculate cost for a DSPy LLM call.

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
    pricing = DSPY_MODEL_PRICING.get(model)

    # Try lowercase match
    if not pricing:
        pricing = DSPY_MODEL_PRICING.get(model_lower)

    # Try partial match
    if not pricing:
        for model_key, model_pricing in DSPY_MODEL_PRICING.items():
            if model_key.lower() in model_lower or model_lower in model_key.lower():
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
    }


def aggregate_program_costs(operation_costs: list[dict[str, Any]]) -> dict[str, Any]:
    """Aggregate costs from multiple operations in a DSPy program.

    Args:
        operation_costs: List of cost dictionaries from individual operations

    Returns:
        Aggregated cost summary
    """
    total_input_tokens = 0
    total_output_tokens = 0
    total_cost = 0.0
    by_model: dict[str, dict[str, Any]] = {}
    by_module: dict[str, dict[str, Any]] = {}

    for cost in operation_costs:
        if not cost:
            continue

        input_tokens = cost.get("input_tokens", 0)
        output_tokens = cost.get("output_tokens", 0)
        op_cost = cost.get("total_cost", 0.0)
        model = cost.get("model", "unknown")
        module = cost.get("module", "unknown")

        total_input_tokens += input_tokens
        total_output_tokens += output_tokens
        total_cost += op_cost

        # Track by model
        if model not in by_model:
            by_model[model] = {
                "input_tokens": 0,
                "output_tokens": 0,
                "total_cost": 0.0,
                "call_count": 0,
            }
        by_model[model]["input_tokens"] += input_tokens
        by_model[model]["output_tokens"] += output_tokens
        by_model[model]["total_cost"] += op_cost
        by_model[model]["call_count"] += 1

        # Track by module
        if module not in by_module:
            by_module[module] = {
                "input_tokens": 0,
                "output_tokens": 0,
                "total_cost": 0.0,
                "call_count": 0,
            }
        by_module[module]["input_tokens"] += input_tokens
        by_module[module]["output_tokens"] += output_tokens
        by_module[module]["total_cost"] += op_cost
        by_module[module]["call_count"] += 1

    return {
        "total_input_tokens": total_input_tokens,
        "total_output_tokens": total_output_tokens,
        "total_tokens": total_input_tokens + total_output_tokens,
        "total_cost": total_cost,
        "by_model": by_model,
        "by_module": by_module,
        "operation_count": len(operation_costs),
    }


def estimate_optimization_cost(
    num_candidates: int,
    avg_tokens_per_call: int,
    model: str,
    iterations: int = 1,
) -> dict[str, Any]:
    """Estimate the cost of a DSPy optimization run.

    Args:
        num_candidates: Number of candidate prompts
        avg_tokens_per_call: Average tokens per LLM call
        model: Model being used
        iterations: Number of optimization iterations

    Returns:
        Dictionary with estimated cost breakdown
    """
    pricing = DSPY_MODEL_PRICING.get(model)
    if not pricing:
        return {
            "estimated_cost": None,
            "note": f"Unknown model pricing for {model}",
        }

    # Estimate total calls: candidates * iterations * evaluation samples
    estimated_calls = num_candidates * iterations * 10  # Assume ~10 evaluations per candidate
    estimated_tokens = estimated_calls * avg_tokens_per_call

    # Assume 50/50 input/output split
    input_tokens = estimated_tokens // 2
    output_tokens = estimated_tokens // 2

    input_cost = (input_tokens / 1_000_000) * pricing.input_cost_per_million
    output_cost = (output_tokens / 1_000_000) * pricing.output_cost_per_million

    return {
        "estimated_calls": estimated_calls,
        "estimated_tokens": estimated_tokens,
        "estimated_input_tokens": input_tokens,
        "estimated_output_tokens": output_tokens,
        "estimated_input_cost": input_cost,
        "estimated_output_cost": output_cost,
        "estimated_total_cost": input_cost + output_cost,
        "model": model,
        "provider": pricing.provider,
    }
