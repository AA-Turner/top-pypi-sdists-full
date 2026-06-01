"""
Cost tracking utilities for OpenAI Agents SDK integration.

Provides model pricing for LLM calls commonly used with OpenAI Agents SDK.
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
    provider: str = "openai"


# OpenAI Agents SDK commonly used models
OPENAI_AGENTS_MODEL_PRICING: dict[str, ModelPricing] = {
    # GPT-4o models (primary for agents)
    "gpt-4o": ModelPricing(2.50, 10.00, "openai"),
    "gpt-4o-2024-11-20": ModelPricing(2.50, 10.00, "openai"),
    "gpt-4o-2024-08-06": ModelPricing(2.50, 10.00, "openai"),
    "gpt-4o-2024-05-13": ModelPricing(5.00, 15.00, "openai"),
    "gpt-4o-mini": ModelPricing(0.15, 0.60, "openai"),
    "gpt-4o-mini-2024-07-18": ModelPricing(0.15, 0.60, "openai"),
    # GPT-4 Turbo
    "gpt-4-turbo": ModelPricing(10.00, 30.00, "openai"),
    "gpt-4-turbo-2024-04-09": ModelPricing(10.00, 30.00, "openai"),
    "gpt-4-turbo-preview": ModelPricing(10.00, 30.00, "openai"),
    # GPT-4
    "gpt-4": ModelPricing(30.00, 60.00, "openai"),
    "gpt-4-0613": ModelPricing(30.00, 60.00, "openai"),
    # GPT-3.5 Turbo
    "gpt-3.5-turbo": ModelPricing(0.50, 1.50, "openai"),
    "gpt-3.5-turbo-0125": ModelPricing(0.50, 1.50, "openai"),
    "gpt-3.5-turbo-1106": ModelPricing(1.00, 2.00, "openai"),
    # O1 models (reasoning)
    "o1": ModelPricing(15.00, 60.00, "openai"),
    "o1-2024-12-17": ModelPricing(15.00, 60.00, "openai"),
    "o1-preview": ModelPricing(15.00, 60.00, "openai"),
    "o1-preview-2024-09-12": ModelPricing(15.00, 60.00, "openai"),
    "o1-mini": ModelPricing(3.00, 12.00, "openai"),
    "o1-mini-2024-09-12": ModelPricing(3.00, 12.00, "openai"),
    # O3 models (future/experimental)
    "o3-mini": ModelPricing(1.10, 4.40, "openai"),
    # Realtime models (for voice agents)
    "gpt-4o-realtime-preview": ModelPricing(5.00, 20.00, "openai"),
    "gpt-4o-mini-realtime-preview": ModelPricing(0.60, 2.40, "openai"),
}


def extract_tokens_from_response(response: Any) -> dict[str, int]:
    """Extract token usage from various OpenAI response formats.

    Args:
        response: The LLM response object

    Returns:
        Dictionary with input_tokens, output_tokens, total_tokens
    """
    input_tokens = 0
    output_tokens = 0

    try:
        # Method 1: Standard usage object
        if hasattr(response, "usage"):
            usage = response.usage
            if hasattr(usage, "prompt_tokens"):
                input_tokens = usage.prompt_tokens or 0
                output_tokens = usage.completion_tokens or 0
            elif hasattr(usage, "input_tokens"):
                input_tokens = usage.input_tokens or 0
                output_tokens = usage.output_tokens or 0
            elif isinstance(usage, dict):
                input_tokens = usage.get("prompt_tokens") or usage.get("input_tokens") or 0
                output_tokens = usage.get("completion_tokens") or usage.get("output_tokens") or 0

        # Method 2: Response model with usage
        if not (input_tokens or output_tokens) and hasattr(response, "model_response"):
            model_response = response.model_response
            if hasattr(model_response, "usage"):
                usage = model_response.usage
                if hasattr(usage, "prompt_tokens"):
                    input_tokens = usage.prompt_tokens or 0
                    output_tokens = usage.completion_tokens or 0

        # Method 3: Raw response
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


def get_openai_agents_cost(
    model: str,
    input_tokens: int,
    output_tokens: int,
    fallback_to_aigie: bool = True,
) -> dict[str, Any] | None:
    """Calculate cost for an OpenAI Agents SDK LLM call.

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
    pricing = OPENAI_AGENTS_MODEL_PRICING.get(model)

    # Try lowercase match
    if not pricing:
        pricing = OPENAI_AGENTS_MODEL_PRICING.get(model_lower)

    # Try partial match
    if not pricing:
        for model_key, model_pricing in OPENAI_AGENTS_MODEL_PRICING.items():
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
    }


def aggregate_workflow_costs(operation_costs: list[dict[str, Any]]) -> dict[str, Any]:
    """Aggregate costs from multiple operations in an agent workflow.

    Args:
        operation_costs: List of cost dictionaries from individual operations

    Returns:
        Aggregated cost summary
    """
    total_input_tokens = 0
    total_output_tokens = 0
    total_cost = 0.0
    by_model: dict[str, dict[str, Any]] = {}
    by_agent: dict[str, dict[str, Any]] = {}

    for cost in operation_costs:
        if not cost:
            continue

        input_tokens = cost.get("input_tokens", 0)
        output_tokens = cost.get("output_tokens", 0)
        op_cost = cost.get("total_cost", 0.0)
        model = cost.get("model", "unknown")
        agent = cost.get("agent", "unknown")

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

        # Track by agent
        if agent not in by_agent:
            by_agent[agent] = {
                "input_tokens": 0,
                "output_tokens": 0,
                "total_cost": 0.0,
                "call_count": 0,
            }
        by_agent[agent]["input_tokens"] += input_tokens
        by_agent[agent]["output_tokens"] += output_tokens
        by_agent[agent]["total_cost"] += op_cost
        by_agent[agent]["call_count"] += 1

    return {
        "total_input_tokens": total_input_tokens,
        "total_output_tokens": total_output_tokens,
        "total_tokens": total_input_tokens + total_output_tokens,
        "total_cost": total_cost,
        "by_model": by_model,
        "by_agent": by_agent,
        "operation_count": len(operation_costs),
    }


def estimate_tool_cost(
    tool_name: str,
    execution_time: float,
    data_size: int = 0,
) -> dict[str, Any]:
    """Estimate cost for tool execution (external APIs, compute, etc.).

    This is a placeholder for custom tool cost tracking.

    Args:
        tool_name: Name of the tool
        execution_time: Execution time in seconds
        data_size: Size of data processed in bytes

    Returns:
        Dictionary with estimated cost
    """
    # Default: assume tools are free (or cost is tracked elsewhere)
    return {
        "tool_name": tool_name,
        "execution_time": execution_time,
        "data_size": data_size,
        "estimated_cost": 0.0,
        "note": "Tool costs should be tracked separately if applicable",
    }
