"""
Cost tracking utilities for Semantic Kernel integration.

Provides model pricing and token extraction for Semantic Kernel function
invocations, particularly Azure OpenAI and OpenAI models.
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


# Model pricing for commonly used models with Semantic Kernel
# Includes both Azure OpenAI deployment names and OpenAI model names
SEMANTIC_KERNEL_MODEL_PRICING: dict[str, ModelPricing] = {
    # OpenAI models (common deployments)
    "gpt-4o": ModelPricing(2.50, 10.00, "openai"),
    "gpt-4o-mini": ModelPricing(0.15, 0.60, "openai"),
    "gpt-4o-2024-11-20": ModelPricing(2.50, 10.00, "openai"),
    "gpt-4o-2024-08-06": ModelPricing(2.50, 10.00, "openai"),
    "gpt-4-turbo": ModelPricing(10.00, 30.00, "openai"),
    "gpt-4-turbo-preview": ModelPricing(10.00, 30.00, "openai"),
    "gpt-4-1106-preview": ModelPricing(10.00, 30.00, "openai"),
    "gpt-4": ModelPricing(30.00, 60.00, "openai"),
    "gpt-4-32k": ModelPricing(60.00, 120.00, "openai"),
    "gpt-35-turbo": ModelPricing(0.50, 1.50, "azure"),  # Azure naming
    "gpt-3.5-turbo": ModelPricing(0.50, 1.50, "openai"),
    "gpt-35-turbo-16k": ModelPricing(3.00, 4.00, "azure"),  # Azure naming
    "gpt-3.5-turbo-16k": ModelPricing(3.00, 4.00, "openai"),
    "o1-preview": ModelPricing(15.00, 60.00, "openai"),
    "o1-mini": ModelPricing(3.00, 12.00, "openai"),
    "o1": ModelPricing(15.00, 60.00, "openai"),
    "o3-mini": ModelPricing(1.10, 4.40, "openai"),
    # Azure OpenAI deployments (common names)
    "gpt4": ModelPricing(30.00, 60.00, "azure"),
    "gpt4-turbo": ModelPricing(10.00, 30.00, "azure"),
    "gpt4o": ModelPricing(2.50, 10.00, "azure"),
    "gpt4o-mini": ModelPricing(0.15, 0.60, "azure"),
    "gpt35": ModelPricing(0.50, 1.50, "azure"),
    # Embedding models
    "text-embedding-ada-002": ModelPricing(0.10, 0.00, "openai"),
    "text-embedding-3-small": ModelPricing(0.02, 0.00, "openai"),
    "text-embedding-3-large": ModelPricing(0.13, 0.00, "openai"),
    # Anthropic models (via SK connectors)
    "claude-3-5-sonnet-20241022": ModelPricing(3.00, 15.00, "anthropic"),
    "claude-3-5-sonnet-latest": ModelPricing(3.00, 15.00, "anthropic"),
    "claude-3-opus-20240229": ModelPricing(15.00, 75.00, "anthropic"),
    "claude-3-sonnet-20240229": ModelPricing(3.00, 15.00, "anthropic"),
    "claude-3-haiku-20240307": ModelPricing(0.25, 1.25, "anthropic"),
    # Google models (via SK connectors)
    "gemini-2.0-flash": ModelPricing(0.10, 0.40, "google"),
    "gemini-1.5-pro": ModelPricing(1.25, 5.00, "google"),
    "gemini-1.5-flash": ModelPricing(0.075, 0.30, "google"),
    # Hugging Face models (various pricing)
    "mistral-7b": ModelPricing(0.20, 0.20, "huggingface"),
    "llama-2-70b": ModelPricing(0.90, 0.90, "huggingface"),
}


def extract_tokens_from_result(result: Any) -> dict[str, int]:
    """Extract token usage from Semantic Kernel function results.

    Args:
        result: The function result object

    Returns:
        Dictionary with input_tokens, output_tokens, total_tokens
    """
    input_tokens = 0
    output_tokens = 0
    cache_read_tokens = 0
    cache_creation_tokens = 0

    try:
        # Method 1: FunctionResult with metadata
        if hasattr(result, "metadata"):
            metadata = result.metadata
            if isinstance(metadata, dict):
                usage = metadata.get("usage") or metadata.get("token_usage")
                if usage:
                    input_tokens = usage.get("prompt_tokens") or usage.get("input_tokens") or 0
                    output_tokens = (
                        usage.get("completion_tokens") or usage.get("output_tokens") or 0
                    )
                    cache_read_tokens = usage.get("cache_read_input_tokens", 0) or 0
                    cache_creation_tokens = usage.get("cache_creation_input_tokens", 0) or 0

        # Method 2: Direct usage attribute
        if not (input_tokens or output_tokens) and hasattr(result, "usage"):
            usage = result.usage
            if hasattr(usage, "prompt_tokens"):
                input_tokens = usage.prompt_tokens or 0
                output_tokens = getattr(usage, "completion_tokens", 0) or 0
            elif isinstance(usage, dict):
                input_tokens = usage.get("prompt_tokens") or usage.get("input_tokens") or 0
                output_tokens = usage.get("completion_tokens") or usage.get("output_tokens") or 0

        # Method 3: Inner result (for ChatMessageContent)
        if not (input_tokens or output_tokens) and hasattr(result, "inner_content"):
            inner = result.inner_content
            if hasattr(inner, "usage"):
                usage = inner.usage
                if hasattr(usage, "prompt_tokens"):
                    input_tokens = usage.prompt_tokens or 0
                    output_tokens = getattr(usage, "completion_tokens", 0) or 0
                elif isinstance(usage, dict):
                    input_tokens = usage.get("prompt_tokens", 0)
                    output_tokens = usage.get("completion_tokens", 0)

        # Method 4: Response metadata (Azure OpenAI style)
        if not (input_tokens or output_tokens) and hasattr(result, "response_metadata"):
            metadata = result.response_metadata
            if isinstance(metadata, dict):
                usage = metadata.get("usage", {})
                input_tokens = usage.get("prompt_tokens", 0)
                output_tokens = usage.get("completion_tokens", 0)

    except Exception as e:
        logger.debug(f"Error extracting tokens from result: {e}")

    return {
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": input_tokens + output_tokens,
        "cache_read_input_tokens": cache_read_tokens,
        "cache_creation_input_tokens": cache_creation_tokens,
    }


def get_semantic_kernel_cost(
    model: str,
    input_tokens: int,
    output_tokens: int,
    fallback_to_aigie: bool = True,
) -> dict[str, Any] | None:
    """Calculate cost for a Semantic Kernel function invocation.

    Args:
        model: The model name/deployment name
        input_tokens: Number of input tokens
        output_tokens: Number of output tokens
        fallback_to_aigie: Whether to fallback to main aigie cost tracking

    Returns:
        Dictionary with cost breakdown or None if pricing not found
    """
    # Normalize model name
    model_lower = model.lower() if model else ""

    # Try exact match first
    pricing = SEMANTIC_KERNEL_MODEL_PRICING.get(model)

    # Try lowercase match
    if not pricing:
        pricing = SEMANTIC_KERNEL_MODEL_PRICING.get(model_lower)

    # Try partial match for model families
    if not pricing:
        for model_key, model_pricing in SEMANTIC_KERNEL_MODEL_PRICING.items():
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


def extract_model_from_service(service: Any) -> str | None:
    """Extract model name from a Semantic Kernel AI service.

    Args:
        service: The SK AI service object

    Returns:
        Model name/deployment name or None
    """
    # Common attribute names for model
    model_attrs = [
        "ai_model_id",
        "model_id",
        "model",
        "deployment_name",  # Azure
        "_model",
        "model_name",
    ]

    for attr in model_attrs:
        if hasattr(service, attr):
            value = getattr(service, attr)
            if isinstance(value, str) and value:
                return value

    # Check settings object
    if hasattr(service, "settings"):
        settings = service.settings
        for attr in ["ai_model_id", "deployment_name", "model"]:
            if hasattr(settings, attr):
                value = getattr(settings, attr)
                if isinstance(value, str) and value:
                    return value

    return None


@dataclass
class FunctionCost:
    """Records cost for a single function invocation."""

    function_name: str
    plugin_name: str | None = None
    model: str | None = None
    input_tokens: int = 0
    output_tokens: int = 0
    cost: float = 0.0
    duration_ms: float = 0.0


class SemanticKernelCostTracker:
    """
    Tracks costs across multiple Semantic Kernel function invocations.

    Useful for tracking costs in planner workflows and multi-function executions.
    """

    def __init__(self):
        self._total_cost: float = 0.0
        self._total_input_tokens: int = 0
        self._total_output_tokens: int = 0
        self._by_model: dict[str, dict[str, Any]] = {}
        self._by_function: dict[str, dict[str, Any]] = {}
        self._by_plugin: dict[str, dict[str, Any]] = {}
        self._function_count: int = 0
        self._function_costs: list[FunctionCost] = []

    def add_usage(
        self,
        function_name: str,
        plugin_name: str | None = None,
        model: str | None = None,
        input_tokens: int = 0,
        output_tokens: int = 0,
        cost: float | None = None,
        duration_ms: float = 0.0,
    ) -> float:
        """
        Add usage from a Semantic Kernel function invocation.

        Args:
            function_name: Name of the function
            plugin_name: Name of the plugin
            model: Model name/deployment
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens
            cost: Pre-calculated cost (if None, will be calculated)
            duration_ms: Duration in milliseconds

        Returns:
            Cost for this call in USD
        """
        if cost is None and model:
            cost_info = get_semantic_kernel_cost(model, input_tokens, output_tokens)
            cost = cost_info.get("total_cost", 0.0) if cost_info else 0.0
        elif cost is None:
            cost = 0.0

        # Update totals
        self._total_cost += cost
        self._total_input_tokens += input_tokens
        self._total_output_tokens += output_tokens
        self._function_count += 1

        # Record function cost
        func_cost = FunctionCost(
            function_name=function_name,
            plugin_name=plugin_name,
            model=model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cost=cost,
            duration_ms=duration_ms,
        )
        self._function_costs.append(func_cost)

        # Update per-model breakdown
        if model:
            if model not in self._by_model:
                self._by_model[model] = {
                    "cost": 0.0,
                    "input_tokens": 0,
                    "output_tokens": 0,
                    "call_count": 0,
                }
            self._by_model[model]["cost"] += cost
            self._by_model[model]["input_tokens"] += input_tokens
            self._by_model[model]["output_tokens"] += output_tokens
            self._by_model[model]["call_count"] += 1

        # Update per-function breakdown
        full_func = f"{plugin_name}.{function_name}" if plugin_name else function_name
        if full_func not in self._by_function:
            self._by_function[full_func] = {
                "cost": 0.0,
                "input_tokens": 0,
                "output_tokens": 0,
                "call_count": 0,
            }
        self._by_function[full_func]["cost"] += cost
        self._by_function[full_func]["input_tokens"] += input_tokens
        self._by_function[full_func]["output_tokens"] += output_tokens
        self._by_function[full_func]["call_count"] += 1

        # Update per-plugin breakdown
        if plugin_name:
            if plugin_name not in self._by_plugin:
                self._by_plugin[plugin_name] = {
                    "cost": 0.0,
                    "input_tokens": 0,
                    "output_tokens": 0,
                    "call_count": 0,
                    "functions": set(),
                }
            self._by_plugin[plugin_name]["cost"] += cost
            self._by_plugin[plugin_name]["input_tokens"] += input_tokens
            self._by_plugin[plugin_name]["output_tokens"] += output_tokens
            self._by_plugin[plugin_name]["call_count"] += 1
            self._by_plugin[plugin_name]["functions"].add(function_name)

        return cost

    @property
    def total_cost(self) -> float:
        """Total cost in USD."""
        return self._total_cost

    @property
    def total_tokens(self) -> int:
        """Total tokens (input + output)."""
        return self._total_input_tokens + self._total_output_tokens

    def get_costs_by_model(self) -> dict[str, dict[str, Any]]:
        """Get cost breakdown by model."""
        return self._by_model.copy()

    def get_costs_by_function(self) -> dict[str, dict[str, Any]]:
        """Get cost breakdown by function."""
        return self._by_function.copy()

    def get_costs_by_plugin(self) -> dict[str, dict[str, Any]]:
        """Get cost breakdown by plugin."""
        result = {}
        for plugin_name, data in self._by_plugin.items():
            result[plugin_name] = {
                "cost": data["cost"],
                "input_tokens": data["input_tokens"],
                "output_tokens": data["output_tokens"],
                "call_count": data["call_count"],
                "functions": list(data["functions"]),
            }
        return result

    def get_summary(self) -> dict[str, Any]:
        """Get full cost tracking summary."""
        return {
            "total_cost": self._total_cost,
            "total_input_tokens": self._total_input_tokens,
            "total_output_tokens": self._total_output_tokens,
            "total_tokens": self.total_tokens,
            "function_count": self._function_count,
            "by_model": self._by_model,
            "by_function": self._by_function,
            "by_plugin": self.get_costs_by_plugin(),
        }

    def reset(self) -> None:
        """Reset all tracked costs."""
        self._total_cost = 0.0
        self._total_input_tokens = 0
        self._total_output_tokens = 0
        self._by_model = {}
        self._by_function = {}
        self._by_plugin = {}
        self._function_count = 0
        self._function_costs = []


def aggregate_workflow_costs(function_costs: list[dict[str, Any]]) -> dict[str, Any]:
    """
    Aggregate costs from multiple function invocations in a workflow.

    Args:
        function_costs: List of cost dictionaries from individual function calls

    Returns:
        Aggregated cost summary with per-model and per-plugin breakdown
    """
    total_cost = 0.0
    total_input_tokens = 0
    total_output_tokens = 0
    by_model: dict[str, dict[str, Any]] = {}
    by_plugin: dict[str, dict[str, Any]] = {}

    for cost_entry in function_costs:
        if not cost_entry:
            continue

        total_cost += cost_entry.get("total_cost", cost_entry.get("cost", 0.0))
        total_input_tokens += cost_entry.get("input_tokens", 0)
        total_output_tokens += cost_entry.get("output_tokens", 0)

        model = cost_entry.get("model", "unknown")
        if model and model != "unknown":
            if model not in by_model:
                by_model[model] = {
                    "cost": 0.0,
                    "input_tokens": 0,
                    "output_tokens": 0,
                    "call_count": 0,
                }
            by_model[model]["cost"] += cost_entry.get("total_cost", cost_entry.get("cost", 0.0))
            by_model[model]["input_tokens"] += cost_entry.get("input_tokens", 0)
            by_model[model]["output_tokens"] += cost_entry.get("output_tokens", 0)
            by_model[model]["call_count"] += 1

        plugin = cost_entry.get("plugin_name")
        if plugin:
            if plugin not in by_plugin:
                by_plugin[plugin] = {
                    "cost": 0.0,
                    "input_tokens": 0,
                    "output_tokens": 0,
                    "call_count": 0,
                }
            by_plugin[plugin]["cost"] += cost_entry.get("total_cost", cost_entry.get("cost", 0.0))
            by_plugin[plugin]["input_tokens"] += cost_entry.get("input_tokens", 0)
            by_plugin[plugin]["output_tokens"] += cost_entry.get("output_tokens", 0)
            by_plugin[plugin]["call_count"] += 1

    return {
        "total_cost": total_cost,
        "total_input_tokens": total_input_tokens,
        "total_output_tokens": total_output_tokens,
        "total_tokens": total_input_tokens + total_output_tokens,
        "by_model": by_model,
        "by_plugin": by_plugin,
        "function_count": len(function_costs),
    }
