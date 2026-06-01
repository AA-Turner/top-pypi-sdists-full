"""
Cost tracking utilities for AutoGen/AG2 integration.

AutoGen uses various LLM providers, so we include comprehensive pricing.
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


# AutoGen typically uses these models
AUTOGEN_MODEL_PRICING: dict[str, ModelPricing] = {
    # OpenAI models (most common with AutoGen)
    "gpt-4o": ModelPricing(2.50, 10.00, "openai"),
    "gpt-4o-mini": ModelPricing(0.15, 0.60, "openai"),
    "gpt-4-turbo": ModelPricing(10.00, 30.00, "openai"),
    "gpt-4-turbo-preview": ModelPricing(10.00, 30.00, "openai"),
    "gpt-4": ModelPricing(30.00, 60.00, "openai"),
    "gpt-4-32k": ModelPricing(60.00, 120.00, "openai"),
    "gpt-3.5-turbo": ModelPricing(0.50, 1.50, "openai"),
    "gpt-3.5-turbo-16k": ModelPricing(3.00, 4.00, "openai"),
    "o1-preview": ModelPricing(15.00, 60.00, "openai"),
    "o1-mini": ModelPricing(3.00, 12.00, "openai"),
    # Azure OpenAI (same pricing as OpenAI)
    "gpt-4o-2024-05-13": ModelPricing(2.50, 10.00, "azure"),
    "gpt-4-1106-preview": ModelPricing(10.00, 30.00, "azure"),
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
    "gemini-1.0-pro": ModelPricing(0.50, 1.50, "google"),
    # Mistral models
    "mistral-large-latest": ModelPricing(4.00, 12.00, "mistral"),
    "mistral-medium-latest": ModelPricing(2.70, 8.10, "mistral"),
    "mistral-small-latest": ModelPricing(1.00, 3.00, "mistral"),
    "open-mixtral-8x22b": ModelPricing(2.00, 6.00, "mistral"),
    "open-mixtral-8x7b": ModelPricing(0.70, 0.70, "mistral"),
    # Groq (fast inference)
    "llama-3.1-70b-versatile": ModelPricing(0.59, 0.79, "groq"),
    "llama-3.1-8b-instant": ModelPricing(0.05, 0.08, "groq"),
    "llama3-70b-8192": ModelPricing(0.59, 0.79, "groq"),
    "llama3-8b-8192": ModelPricing(0.05, 0.08, "groq"),
    "mixtral-8x7b-32768": ModelPricing(0.24, 0.24, "groq"),
    # Local models (free)
    "llama3": ModelPricing(0.0, 0.0, "local"),
    "codellama": ModelPricing(0.0, 0.0, "local"),
}


def extract_tokens_from_response(response: Any) -> dict[str, int]:
    """Extract token usage from various AutoGen response formats.

    Args:
        response: The LLM response object

    Returns:
        Dictionary with input_tokens, output_tokens, total_tokens
    """
    input_tokens = 0
    output_tokens = 0

    try:
        # Method 1: OpenAI-style response with usage
        if hasattr(response, "usage"):
            usage = response.usage
            if hasattr(usage, "prompt_tokens"):
                input_tokens = usage.prompt_tokens or 0
                output_tokens = usage.completion_tokens or 0
            elif isinstance(usage, dict):
                input_tokens = usage.get("prompt_tokens") or usage.get("input_tokens") or 0
                output_tokens = usage.get("completion_tokens") or usage.get("output_tokens") or 0

        # Method 2: Dict response with usage key
        if not (input_tokens or output_tokens) and isinstance(response, dict):
            usage = response.get("usage")
            if usage:
                input_tokens = usage.get("prompt_tokens") or usage.get("input_tokens") or 0
                output_tokens = usage.get("completion_tokens") or usage.get("output_tokens") or 0

        # Method 3: AutoGen-specific cost tracking
        if not (input_tokens or output_tokens) and hasattr(response, "cost"):
            cost_info = response.cost
            if isinstance(cost_info, dict):
                # Try to extract from cost structure
                for model_cost in cost_info.values():
                    if isinstance(model_cost, dict):
                        input_tokens += model_cost.get("prompt_tokens", 0)
                        output_tokens += model_cost.get("completion_tokens", 0)

    except Exception as e:
        logger.debug(f"Error extracting tokens from response: {e}")

    return {
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": input_tokens + output_tokens,
    }


def get_autogen_cost(
    model: str,
    input_tokens: int,
    output_tokens: int,
    fallback_to_aigie: bool = True,
) -> dict[str, Any] | None:
    """Calculate cost for an AutoGen LLM call.

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
    pricing = AUTOGEN_MODEL_PRICING.get(model)

    # Try lowercase match
    if not pricing:
        pricing = AUTOGEN_MODEL_PRICING.get(model_lower)

    # Try partial match for model families
    if not pricing:
        for model_key, model_pricing in AUTOGEN_MODEL_PRICING.items():
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


def extract_model_from_agent(agent: Any) -> str | None:
    """Extract model name from an AutoGen Agent.

    Args:
        agent: The AutoGen Agent object

    Returns:
        Model name or None
    """
    try:
        # Try to get llm_config from agent
        llm_config = getattr(agent, "llm_config", None)
        if not llm_config:
            return None

        if isinstance(llm_config, dict):
            # Check config_list first
            config_list = llm_config.get("config_list", [])
            if config_list and len(config_list) > 0:
                first_config = config_list[0]
                if isinstance(first_config, dict):
                    model = first_config.get("model")
                    if model:
                        return model

            # Direct model key
            model = llm_config.get("model")
            if model:
                return model

    except Exception as e:
        logger.debug(f"Error extracting model from agent: {e}")

    return None


def aggregate_conversation_costs(message_costs: list) -> dict[str, Any]:
    """Aggregate costs from multiple messages in an AutoGen conversation.

    Args:
        message_costs: List of cost dictionaries from individual messages

    Returns:
        Aggregated cost summary
    """
    total_input_tokens = 0
    total_output_tokens = 0
    total_cost = 0.0
    by_agent: dict[str, dict[str, Any]] = {}
    by_model: dict[str, dict[str, Any]] = {}

    for cost in message_costs:
        if not cost:
            continue

        input_tokens = cost.get("input_tokens", 0)
        output_tokens = cost.get("output_tokens", 0)
        msg_cost = cost.get("total_cost", 0.0)
        model = cost.get("model", "unknown")
        agent = cost.get("agent_name", "unknown")

        total_input_tokens += input_tokens
        total_output_tokens += output_tokens
        total_cost += msg_cost

        # Track by agent
        if agent not in by_agent:
            by_agent[agent] = {
                "input_tokens": 0,
                "output_tokens": 0,
                "total_cost": 0.0,
                "message_count": 0,
            }
        by_agent[agent]["input_tokens"] += input_tokens
        by_agent[agent]["output_tokens"] += output_tokens
        by_agent[agent]["total_cost"] += msg_cost
        by_agent[agent]["message_count"] += 1

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
        by_model[model]["total_cost"] += msg_cost
        by_model[model]["call_count"] += 1

    return {
        "total_input_tokens": total_input_tokens,
        "total_output_tokens": total_output_tokens,
        "total_tokens": total_input_tokens + total_output_tokens,
        "total_cost": total_cost,
        "by_agent": by_agent,
        "by_model": by_model,
        "message_count": len(message_costs),
    }
