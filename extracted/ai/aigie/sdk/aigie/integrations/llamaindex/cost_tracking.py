"""
Cost tracking utilities for LlamaIndex integration.

Provides model pricing for LLM and embedding calls commonly used with LlamaIndex.
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


@dataclass
class EmbeddingPricing:
    """Pricing information for an embedding model."""

    cost_per_million: float  # Cost per 1M tokens
    provider: str = "unknown"


# LlamaIndex commonly used LLM models
LLAMAINDEX_MODEL_PRICING: dict[str, ModelPricing] = {
    # OpenAI models
    "gpt-4o": ModelPricing(2.50, 10.00, "openai"),
    "gpt-4o-mini": ModelPricing(0.15, 0.60, "openai"),
    "gpt-4-turbo": ModelPricing(10.00, 30.00, "openai"),
    "gpt-4-turbo-preview": ModelPricing(10.00, 30.00, "openai"),
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
    # Cohere models (often used for reranking)
    "command-r-plus": ModelPricing(3.00, 15.00, "cohere"),
    "command-r": ModelPricing(0.50, 1.50, "cohere"),
    # Mistral models
    "mistral-large-latest": ModelPricing(4.00, 12.00, "mistral"),
    "open-mixtral-8x22b": ModelPricing(2.00, 6.00, "mistral"),
    # Local models (free)
    "llama3": ModelPricing(0.0, 0.0, "local"),
    "mistral": ModelPricing(0.0, 0.0, "local"),
}

# Embedding model pricing
LLAMAINDEX_EMBEDDING_PRICING: dict[str, EmbeddingPricing] = {
    # OpenAI embeddings
    "text-embedding-3-large": EmbeddingPricing(0.13, "openai"),
    "text-embedding-3-small": EmbeddingPricing(0.02, "openai"),
    "text-embedding-ada-002": EmbeddingPricing(0.10, "openai"),
    # Cohere embeddings
    "embed-english-v3.0": EmbeddingPricing(0.10, "cohere"),
    "embed-multilingual-v3.0": EmbeddingPricing(0.10, "cohere"),
    "embed-english-light-v3.0": EmbeddingPricing(0.10, "cohere"),
    # Voyage AI embeddings
    "voyage-3": EmbeddingPricing(0.06, "voyage"),
    "voyage-3-lite": EmbeddingPricing(0.02, "voyage"),
    "voyage-code-3": EmbeddingPricing(0.18, "voyage"),
    # Local embeddings (free)
    "BAAI/bge-base-en-v1.5": EmbeddingPricing(0.0, "local"),
    "BAAI/bge-large-en-v1.5": EmbeddingPricing(0.0, "local"),
    "sentence-transformers/all-MiniLM-L6-v2": EmbeddingPricing(0.0, "local"),
}


def extract_tokens_from_response(response: Any) -> dict[str, int]:
    """Extract token usage from various LlamaIndex response formats.

    Args:
        response: The LLM response object

    Returns:
        Dictionary with input_tokens, output_tokens, total_tokens
    """
    input_tokens = 0
    output_tokens = 0

    try:
        # Method 1: Direct token usage on response
        if hasattr(response, "usage"):
            usage = response.usage
            if hasattr(usage, "prompt_tokens"):
                input_tokens = usage.prompt_tokens or 0
                output_tokens = usage.completion_tokens or 0
            elif isinstance(usage, dict):
                input_tokens = usage.get("prompt_tokens") or usage.get("input_tokens") or 0
                output_tokens = usage.get("completion_tokens") or usage.get("output_tokens") or 0

        # Method 2: Raw response with usage
        if not (input_tokens or output_tokens) and hasattr(response, "raw"):
            raw = response.raw
            if hasattr(raw, "usage"):
                usage = raw.usage
                if hasattr(usage, "prompt_tokens"):
                    input_tokens = usage.prompt_tokens or 0
                    output_tokens = usage.completion_tokens or 0

        # Method 3: Additional kwargs
        if not (input_tokens or output_tokens) and hasattr(response, "additional_kwargs"):
            kwargs = response.additional_kwargs
            if isinstance(kwargs, dict):
                usage = kwargs.get("usage")
                if usage:
                    input_tokens = usage.get("prompt_tokens") or 0
                    output_tokens = usage.get("completion_tokens") or 0

    except Exception as e:
        logger.debug(f"Error extracting tokens from response: {e}")

    return {
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": input_tokens + output_tokens,
    }


def get_llamaindex_cost(
    model: str,
    input_tokens: int,
    output_tokens: int,
    fallback_to_aigie: bool = True,
) -> dict[str, Any] | None:
    """Calculate cost for a LlamaIndex LLM call.

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
    pricing = LLAMAINDEX_MODEL_PRICING.get(model)

    # Try lowercase match
    if not pricing:
        pricing = LLAMAINDEX_MODEL_PRICING.get(model_lower)

    # Try partial match
    if not pricing:
        for model_key, model_pricing in LLAMAINDEX_MODEL_PRICING.items():
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


def get_embedding_cost(
    model: str,
    num_tokens: int,
) -> dict[str, Any] | None:
    """Calculate cost for an embedding operation.

    Args:
        model: The embedding model name
        num_tokens: Number of tokens embedded

    Returns:
        Dictionary with cost breakdown or None if pricing not found
    """
    # Normalize model name
    model_lower = model.lower() if model else ""

    # Try exact match first
    pricing = LLAMAINDEX_EMBEDDING_PRICING.get(model)

    # Try lowercase match
    if not pricing:
        pricing = LLAMAINDEX_EMBEDDING_PRICING.get(model_lower)

    # Try partial match
    if not pricing:
        for model_key, model_pricing in LLAMAINDEX_EMBEDDING_PRICING.items():
            if model_key.lower() in model_lower or model_lower in model_key.lower():
                pricing = model_pricing
                break

    if not pricing:
        return None

    # Calculate cost
    total_cost = (num_tokens / 1_000_000) * pricing.cost_per_million

    return {
        "total_cost": total_cost,
        "tokens": num_tokens,
        "model": model,
        "provider": pricing.provider,
        "cost_per_million": pricing.cost_per_million,
    }


def aggregate_query_costs(operation_costs: list) -> dict[str, Any]:
    """Aggregate costs from multiple operations in a LlamaIndex query.

    Args:
        operation_costs: List of cost dictionaries from individual operations

    Returns:
        Aggregated cost summary
    """
    total_input_tokens = 0
    total_output_tokens = 0
    total_embedding_tokens = 0
    total_cost = 0.0
    by_model: dict[str, dict[str, Any]] = {}
    by_operation: dict[str, dict[str, Any]] = {}

    for cost in operation_costs:
        if not cost:
            continue

        operation_type = cost.get("operation_type", "llm")
        model = cost.get("model", "unknown")

        if operation_type == "embedding":
            tokens = cost.get("tokens", 0)
            total_embedding_tokens += tokens
            op_cost = cost.get("total_cost", 0.0)
        else:
            input_tokens = cost.get("input_tokens", 0)
            output_tokens = cost.get("output_tokens", 0)
            total_input_tokens += input_tokens
            total_output_tokens += output_tokens
            op_cost = cost.get("total_cost", 0.0)

        total_cost += op_cost

        # Track by model
        if model not in by_model:
            by_model[model] = {
                "input_tokens": 0,
                "output_tokens": 0,
                "total_cost": 0.0,
                "call_count": 0,
            }
        by_model[model]["input_tokens"] += cost.get("input_tokens", 0)
        by_model[model]["output_tokens"] += cost.get("output_tokens", 0)
        by_model[model]["total_cost"] += op_cost
        by_model[model]["call_count"] += 1

        # Track by operation type
        if operation_type not in by_operation:
            by_operation[operation_type] = {
                "tokens": 0,
                "total_cost": 0.0,
                "count": 0,
            }
        by_operation[operation_type]["tokens"] += (
            cost.get("input_tokens", 0) + cost.get("output_tokens", 0) + cost.get("tokens", 0)
        )
        by_operation[operation_type]["total_cost"] += op_cost
        by_operation[operation_type]["count"] += 1

    return {
        "total_input_tokens": total_input_tokens,
        "total_output_tokens": total_output_tokens,
        "total_embedding_tokens": total_embedding_tokens,
        "total_tokens": total_input_tokens + total_output_tokens + total_embedding_tokens,
        "total_cost": total_cost,
        "by_model": by_model,
        "by_operation": by_operation,
        "operation_count": len(operation_costs),
    }
