"""
Cost tracking utilities for CrewAI integration.

CrewAI uses LangChain LLMs internally, so we use the same pricing models.
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


# CrewAI typically uses these models through LangChain
CREWAI_MODEL_PRICING: dict[str, ModelPricing] = {
    # OpenAI models (most common with CrewAI)
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
    # Groq models (often used with CrewAI for speed)
    "llama-3.1-70b-versatile": ModelPricing(0.59, 0.79, "groq"),
    "llama-3.1-8b-instant": ModelPricing(0.05, 0.08, "groq"),
    "llama3-70b-8192": ModelPricing(0.59, 0.79, "groq"),
    "llama3-8b-8192": ModelPricing(0.05, 0.08, "groq"),
    "mixtral-8x7b-32768": ModelPricing(0.24, 0.24, "groq"),
    # Ollama local models (free)
    "llama3": ModelPricing(0.0, 0.0, "ollama"),
    "llama3.1": ModelPricing(0.0, 0.0, "ollama"),
    "mistral": ModelPricing(0.0, 0.0, "ollama"),
    "codellama": ModelPricing(0.0, 0.0, "ollama"),
}


def extract_tokens_from_response(response: Any) -> dict[str, int]:
    """Extract token usage from various CrewAI/LangChain response formats.

    Args:
        response: The LLM response object

    Returns:
        Dictionary with input_tokens, output_tokens, total_tokens
    """
    input_tokens = 0
    output_tokens = 0

    try:
        # Method 1: LLMResult format (LangChain standard)
        if hasattr(response, "llm_output") and response.llm_output:
            llm_output = response.llm_output
            if isinstance(llm_output, dict):
                token_usage = llm_output.get("token_usage") or llm_output.get("usage")
                if token_usage:
                    input_tokens = (
                        token_usage.get("prompt_tokens") or token_usage.get("input_tokens") or 0
                    )
                    output_tokens = (
                        token_usage.get("completion_tokens")
                        or token_usage.get("output_tokens")
                        or 0
                    )

        # Method 2: response_metadata (newer LangChain format)
        if not (input_tokens or output_tokens) and hasattr(response, "response_metadata"):
            metadata = response.response_metadata
            if isinstance(metadata, dict):
                usage = metadata.get("usage") or metadata.get("token_usage")
                if usage:
                    input_tokens = usage.get("prompt_tokens") or usage.get("input_tokens") or 0
                    output_tokens = (
                        usage.get("completion_tokens") or usage.get("output_tokens") or 0
                    )

        # Method 3: usage_metadata
        if not (input_tokens or output_tokens) and hasattr(response, "usage_metadata"):
            usage = response.usage_metadata
            if usage:
                if hasattr(usage, "input_tokens"):
                    input_tokens = usage.input_tokens or 0
                if hasattr(usage, "output_tokens"):
                    output_tokens = usage.output_tokens or 0
                if isinstance(usage, dict):
                    input_tokens = usage.get("input_tokens") or usage.get("prompt_tokens") or 0
                    output_tokens = (
                        usage.get("output_tokens") or usage.get("completion_tokens") or 0
                    )

        # Method 4: Direct usage attribute
        if not (input_tokens or output_tokens) and hasattr(response, "usage"):
            usage = response.usage
            if hasattr(usage, "prompt_tokens"):
                input_tokens = usage.prompt_tokens or 0
                output_tokens = usage.completion_tokens or 0
            elif isinstance(usage, dict):
                input_tokens = usage.get("prompt_tokens") or usage.get("input_tokens") or 0
                output_tokens = usage.get("completion_tokens") or usage.get("output_tokens") or 0

        # Method 5: CrewAI-specific attributes
        if not (input_tokens or output_tokens) and hasattr(response, "token_usage"):
            usage = response.token_usage
            if isinstance(usage, dict):
                input_tokens = usage.get("input_tokens") or usage.get("prompt_tokens") or 0
                output_tokens = (
                    usage.get("output_tokens") or usage.get("completion_tokens") or 0
                )

    except Exception as e:
        logger.debug(f"Error extracting tokens from response: {e}")

    return {
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": input_tokens + output_tokens,
    }


def get_crewai_cost(
    model: str,
    input_tokens: int,
    output_tokens: int,
    fallback_to_aigie: bool = True,
) -> dict[str, Any] | None:
    """Calculate cost for a CrewAI LLM call.

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
    pricing = CREWAI_MODEL_PRICING.get(model)

    # Try lowercase match
    if not pricing:
        pricing = CREWAI_MODEL_PRICING.get(model_lower)

    # Try partial match for model families
    if not pricing:
        for model_key, model_pricing in CREWAI_MODEL_PRICING.items():
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
    """Extract model name from a CrewAI Agent.

    Args:
        agent: The CrewAI Agent object

    Returns:
        Model name or None
    """
    try:
        # Try to get LLM from agent
        llm = getattr(agent, "llm", None)
        if not llm:
            return None

        # Common attribute names for model
        model_attrs = [
            "model_name",
            "model",
            "model_id",
            "deployment_name",
            "_model",
        ]

        for attr in model_attrs:
            if hasattr(llm, attr):
                value = getattr(llm, attr)
                if isinstance(value, str) and value:
                    return value

        # Try class name as fallback
        class_name = type(llm).__name__
        if class_name and "Chat" in class_name:
            return class_name.replace("Chat", "").lower()

    except Exception as e:
        logger.debug(f"Error extracting model from agent: {e}")

    return None


def aggregate_crew_costs(task_costs: list) -> dict[str, Any]:
    """Aggregate costs from multiple tasks in a CrewAI crew.

    Args:
        task_costs: List of cost dictionaries from individual tasks

    Returns:
        Aggregated cost summary
    """
    total_input_tokens = 0
    total_output_tokens = 0
    total_cost = 0.0
    by_agent: dict[str, dict[str, Any]] = {}
    by_model: dict[str, dict[str, Any]] = {}

    for cost in task_costs:
        if not cost:
            continue

        input_tokens = cost.get("input_tokens", 0)
        output_tokens = cost.get("output_tokens", 0)
        task_cost = cost.get("total_cost", 0.0)
        model = cost.get("model", "unknown")
        agent = cost.get("agent_role", "unknown")

        total_input_tokens += input_tokens
        total_output_tokens += output_tokens
        total_cost += task_cost

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
        by_agent[agent]["total_cost"] += task_cost
        by_agent[agent]["call_count"] += 1

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
        by_model[model]["total_cost"] += task_cost
        by_model[model]["call_count"] += 1

    return {
        "total_input_tokens": total_input_tokens,
        "total_output_tokens": total_output_tokens,
        "total_tokens": total_input_tokens + total_output_tokens,
        "total_cost": total_cost,
        "by_agent": by_agent,
        "by_model": by_model,
        "task_count": len(task_costs),
    }
