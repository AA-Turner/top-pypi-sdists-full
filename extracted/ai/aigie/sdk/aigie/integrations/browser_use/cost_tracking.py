"""
Cost tracking for browser-use LLM providers.

Includes pricing for ChatBrowserUse and other commonly used models.
"""

from dataclasses import dataclass
from typing import Any


@dataclass
class ModelPricing:
    """Pricing information for a model."""

    input_cost_per_million: float  # Cost per 1M input tokens
    output_cost_per_million: float  # Cost per 1M output tokens
    provider: str = "unknown"


# Browser-use specific model pricing
# ChatBrowserUse: $0.20 per 1M input tokens (from browser-use docs)
# Output pricing estimated at 4x input (common ratio)
BROWSER_USE_MODEL_PRICING: dict[str, ModelPricing] = {
    # ChatBrowserUse (browser-use's optimized model)
    "chat-browser-use": ModelPricing(
        input_cost_per_million=0.20,
        output_cost_per_million=0.80,
        provider="browser-use",
    ),
    "chatbrowseruse": ModelPricing(
        input_cost_per_million=0.20,
        output_cost_per_million=0.80,
        provider="browser-use",
    ),
    # OpenAI models commonly used with browser-use
    "gpt-4o": ModelPricing(
        input_cost_per_million=2.50,
        output_cost_per_million=10.00,
        provider="openai",
    ),
    "gpt-4o-mini": ModelPricing(
        input_cost_per_million=0.15,
        output_cost_per_million=0.60,
        provider="openai",
    ),
    "gpt-4-turbo": ModelPricing(
        input_cost_per_million=10.00,
        output_cost_per_million=30.00,
        provider="openai",
    ),
    "o3": ModelPricing(
        input_cost_per_million=10.00,
        output_cost_per_million=40.00,
        provider="openai",
    ),
    "o3-mini": ModelPricing(
        input_cost_per_million=1.10,
        output_cost_per_million=4.40,
        provider="openai",
    ),
    # Anthropic Claude models
    "claude-sonnet-4-20250514": ModelPricing(
        input_cost_per_million=3.00,
        output_cost_per_million=15.00,
        provider="anthropic",
    ),
    "claude-3-5-sonnet-20241022": ModelPricing(
        input_cost_per_million=3.00,
        output_cost_per_million=15.00,
        provider="anthropic",
    ),
    "claude-3-opus-20240229": ModelPricing(
        input_cost_per_million=15.00,
        output_cost_per_million=75.00,
        provider="anthropic",
    ),
    "claude-3-haiku-20240307": ModelPricing(
        input_cost_per_million=0.25,
        output_cost_per_million=1.25,
        provider="anthropic",
    ),
    # Google Gemini models
    "gemini-2.0-flash": ModelPricing(
        input_cost_per_million=0.10,
        output_cost_per_million=0.40,
        provider="google",
    ),
    "gemini-1.5-pro": ModelPricing(
        input_cost_per_million=1.25,
        output_cost_per_million=5.00,
        provider="google",
    ),
    "gemini-1.5-flash": ModelPricing(
        input_cost_per_million=0.075,
        output_cost_per_million=0.30,
        provider="google",
    ),
    # Groq models
    "llama-3.3-70b-versatile": ModelPricing(
        input_cost_per_million=0.59,
        output_cost_per_million=0.79,
        provider="groq",
    ),
    "llama-3.1-8b-instant": ModelPricing(
        input_cost_per_million=0.05,
        output_cost_per_million=0.08,
        provider="groq",
    ),
    # DeepSeek models
    "deepseek-chat": ModelPricing(
        input_cost_per_million=0.14,
        output_cost_per_million=0.28,
        provider="deepseek",
    ),
    "deepseek-reasoner": ModelPricing(
        input_cost_per_million=0.55,
        output_cost_per_million=2.19,
        provider="deepseek",
    ),
}


def get_browser_use_cost(
    model: str,
    input_tokens: int,
    output_tokens: int,
    fallback_to_aigie: bool = True,
) -> dict[str, float] | None:
    """Calculate cost for a browser-use LLM call.

    Args:
        model: Model name/identifier
        input_tokens: Number of input tokens
        output_tokens: Number of output tokens
        fallback_to_aigie: If True, fallback to main aigie cost tracking

    Returns:
        Dictionary with input_cost, output_cost, total_cost, or None if unknown
    """
    # Normalize model name
    model_lower = model.lower().replace("-", "").replace("_", "").replace(" ", "")

    # Try browser-use specific pricing first
    pricing = None
    for name, p in BROWSER_USE_MODEL_PRICING.items():
        if name.lower().replace("-", "").replace("_", "") == model_lower:
            pricing = p
            break

    # Fallback to main aigie cost tracking
    if pricing is None and fallback_to_aigie:
        try:
            from aigie.cost_tracking import get_model_pricing

            aigie_pricing = get_model_pricing(model)
            if aigie_pricing:
                pricing = ModelPricing(
                    input_cost_per_million=aigie_pricing.input_cost_per_million,
                    output_cost_per_million=aigie_pricing.output_cost_per_million,
                    provider=aigie_pricing.provider
                    if hasattr(aigie_pricing, "provider")
                    else "unknown",
                )
        except ImportError:
            pass

    if pricing is None:
        return None

    input_cost = (input_tokens / 1_000_000) * pricing.input_cost_per_million
    output_cost = (output_tokens / 1_000_000) * pricing.output_cost_per_million

    return {
        "input_cost": input_cost,
        "output_cost": output_cost,
        "total_cost": input_cost + output_cost,
        "provider": pricing.provider,
        "model": model,
    }


def extract_tokens_from_response(response: Any) -> dict[str, int] | None:
    """Extract token counts from a browser-use LLM response.

    Different providers return tokens in different formats. This function
    handles the common patterns.

    Args:
        response: The LLM response object

    Returns:
        Dictionary with input_tokens, output_tokens, total_tokens, or None
    """
    # Try common attribute patterns
    usage = None

    # Check for usage attribute (OpenAI style)
    if hasattr(response, "usage"):
        usage = response.usage
    # Check for response_metadata (LangChain style)
    elif hasattr(response, "response_metadata"):
        metadata = response.response_metadata
        if isinstance(metadata, dict):
            usage = metadata.get("usage") or metadata.get("token_usage")

    if usage is None:
        return None

    # Extract tokens from usage object
    input_tokens = None
    output_tokens = None

    if isinstance(usage, dict):
        input_tokens = usage.get("prompt_tokens") or usage.get("input_tokens")
        output_tokens = usage.get("completion_tokens") or usage.get("output_tokens")
    else:
        # Object with attributes
        input_tokens = getattr(usage, "prompt_tokens", None) or getattr(usage, "input_tokens", None)
        output_tokens = getattr(usage, "completion_tokens", None) or getattr(
            usage, "output_tokens", None
        )

    if input_tokens is None and output_tokens is None:
        return None

    input_tokens = input_tokens or 0
    output_tokens = output_tokens or 0

    return {
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": input_tokens + output_tokens,
    }
