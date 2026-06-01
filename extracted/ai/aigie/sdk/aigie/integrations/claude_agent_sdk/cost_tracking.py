"""
Cost tracking for Claude Agent SDK.

Provides pricing information and cost calculation for Claude models.
"""


# Claude model pricing (per 1M tokens)
# Updated as of January 2025
CLAUDE_MODEL_PRICING: dict[str, dict[str, float]] = {
    # Claude 4 models
    "claude-opus-4-20250514": {
        "input": 15.00,
        "output": 75.00,
        "cache_read": 1.50,
        "cache_write": 18.75,
    },
    "claude-opus-4": {
        "input": 15.00,
        "output": 75.00,
        "cache_read": 1.50,
        "cache_write": 18.75,
    },
    "claude-sonnet-4-20250514": {
        "input": 3.00,
        "output": 15.00,
        "cache_read": 0.30,
        "cache_write": 3.75,
    },
    "claude-sonnet-4": {
        "input": 3.00,
        "output": 15.00,
        "cache_read": 0.30,
        "cache_write": 3.75,
    },
    # Claude 3.5 models
    "claude-3-5-sonnet-20241022": {
        "input": 3.00,
        "output": 15.00,
        "cache_read": 0.30,
        "cache_write": 3.75,
    },
    "claude-3-5-sonnet-latest": {
        "input": 3.00,
        "output": 15.00,
        "cache_read": 0.30,
        "cache_write": 3.75,
    },
    "claude-3-5-haiku-20241022": {
        "input": 1.00,
        "output": 5.00,
        "cache_read": 0.10,
        "cache_write": 1.25,
    },
    "claude-3-5-haiku-latest": {
        "input": 1.00,
        "output": 5.00,
        "cache_read": 0.10,
        "cache_write": 1.25,
    },
    # Claude 3 models
    "claude-3-opus-20240229": {
        "input": 15.00,
        "output": 75.00,
        "cache_read": 1.50,
        "cache_write": 18.75,
    },
    "claude-3-opus-latest": {
        "input": 15.00,
        "output": 75.00,
        "cache_read": 1.50,
        "cache_write": 18.75,
    },
    "claude-3-sonnet-20240229": {
        "input": 3.00,
        "output": 15.00,
        "cache_read": 0.30,
        "cache_write": 3.75,
    },
    "claude-3-haiku-20240307": {
        "input": 0.25,
        "output": 1.25,
        "cache_read": 0.03,
        "cache_write": 0.30,
    },
}

# Aliases for common model names
MODEL_ALIASES: dict[str, str] = {
    "claude-4-opus": "claude-opus-4-20250514",
    "claude-4-sonnet": "claude-sonnet-4-20250514",
    "claude-4": "claude-sonnet-4-20250514",
    "claude-3.5-sonnet": "claude-3-5-sonnet-20241022",
    "claude-3.5-haiku": "claude-3-5-haiku-20241022",
    "claude-3-opus": "claude-3-opus-20240229",
    "claude-3-sonnet": "claude-3-sonnet-20240229",
    "claude-3-haiku": "claude-3-haiku-20240307",
    "sonnet": "claude-sonnet-4-20250514",
    "opus": "claude-opus-4-20250514",
    "haiku": "claude-3-5-haiku-20241022",
}


def get_model_pricing(model: str) -> dict[str, float] | None:
    """
    Get pricing for a Claude model.

    Args:
        model: Model name or alias

    Returns:
        Pricing dict with input/output/cache_read/cache_write rates per 1M tokens,
        or None if model not found
    """
    # Check aliases first
    resolved_model = MODEL_ALIASES.get(model, model)

    # Direct lookup
    if resolved_model in CLAUDE_MODEL_PRICING:
        return CLAUDE_MODEL_PRICING[resolved_model]

    # Try partial matching
    for model_key in CLAUDE_MODEL_PRICING:
        if model_key in resolved_model or resolved_model in model_key:
            return CLAUDE_MODEL_PRICING[model_key]

    return None


def calculate_claude_cost(
    model: str,
    usage: dict[str, int],
    pricing: dict[str, float] | None = None,
) -> float:
    """
    Calculate cost for Claude API usage.

    Args:
        model: Model name or alias
        usage: Usage dict with:
            - input_tokens: Number of input tokens
            - output_tokens: Number of output tokens
            - cache_read_input_tokens: Tokens read from cache (optional)
            - cache_creation_input_tokens: Tokens written to cache (optional)
        pricing: Optional custom pricing dict (uses default if not provided)

    Returns:
        Total cost in USD
    """
    if pricing is None:
        pricing = get_model_pricing(model)

    if pricing is None:
        # Use default Claude 3.5 Sonnet pricing if model not found
        pricing = CLAUDE_MODEL_PRICING.get(
            "claude-3-5-sonnet-20241022",
            {
                "input": 3.00,
                "output": 15.00,
                "cache_read": 0.30,
                "cache_write": 3.75,
            },
        )

    # Calculate cost per million tokens
    input_tokens = usage.get("input_tokens", 0)
    output_tokens = usage.get("output_tokens", 0)
    cache_read_tokens = usage.get("cache_read_input_tokens", 0)
    cache_creation_tokens = usage.get("cache_creation_input_tokens", 0)

    cost = 0.0

    # Input tokens (excluding cache read tokens which are cheaper)
    regular_input_tokens = max(0, input_tokens - cache_read_tokens)
    cost += (regular_input_tokens / 1_000_000) * pricing.get("input", 0)

    # Output tokens
    cost += (output_tokens / 1_000_000) * pricing.get("output", 0)

    # Cache read tokens (cheaper rate)
    cost += (cache_read_tokens / 1_000_000) * pricing.get("cache_read", 0)

    # Cache creation tokens (premium rate)
    cost += (cache_creation_tokens / 1_000_000) * pricing.get("cache_write", 0)

    return cost


def estimate_cost(
    model: str,
    input_text: str,
    estimated_output_tokens: int = 500,
) -> float:
    """
    Estimate cost for a Claude API call.

    This is a rough estimate using character count / 4 for input tokens.

    Args:
        model: Model name or alias
        input_text: Input text to estimate
        estimated_output_tokens: Expected output tokens (default 500)

    Returns:
        Estimated cost in USD
    """
    # Rough estimate: ~4 characters per token
    estimated_input_tokens = len(input_text) // 4

    return calculate_claude_cost(
        model,
        {
            "input_tokens": estimated_input_tokens,
            "output_tokens": estimated_output_tokens,
        },
    )


class CostTracker:
    """
    Tracks costs across multiple Claude API calls with per-model breakdown.

    Useful for tracking costs in multi-agent workflows or sessions.
    """

    def __init__(self):
        self._total_cost: float = 0.0
        self._total_input_tokens: int = 0
        self._total_output_tokens: int = 0
        self._total_cache_read_tokens: int = 0
        self._total_cache_creation_tokens: int = 0
        self._by_model: dict[str, dict[str, float]] = {}
        self._call_count: int = 0

    def add_usage(
        self,
        model: str,
        usage: dict[str, int],
        cost: float | None = None,
    ) -> float:
        """
        Add usage from a Claude API call.

        Args:
            model: Model name
            usage: Usage dict with token counts
            cost: Pre-calculated cost (if None, will be calculated)

        Returns:
            Cost for this call in USD
        """
        if cost is None:
            cost = calculate_claude_cost(model, usage)

        input_tokens = usage.get("input_tokens", 0)
        output_tokens = usage.get("output_tokens", 0)
        cache_read_tokens = usage.get("cache_read_input_tokens", 0)
        cache_creation_tokens = usage.get("cache_creation_input_tokens", 0)

        # Update totals
        self._total_cost += cost
        self._total_input_tokens += input_tokens
        self._total_output_tokens += output_tokens
        self._total_cache_read_tokens += cache_read_tokens
        self._total_cache_creation_tokens += cache_creation_tokens
        self._call_count += 1

        # Update per-model breakdown
        if model not in self._by_model:
            self._by_model[model] = {
                "cost": 0.0,
                "input_tokens": 0,
                "output_tokens": 0,
                "cache_read_tokens": 0,
                "cache_creation_tokens": 0,
                "call_count": 0,
            }

        self._by_model[model]["cost"] += cost
        self._by_model[model]["input_tokens"] += input_tokens
        self._by_model[model]["output_tokens"] += output_tokens
        self._by_model[model]["cache_read_tokens"] += cache_read_tokens
        self._by_model[model]["cache_creation_tokens"] += cache_creation_tokens
        self._by_model[model]["call_count"] += 1

        return cost

    @property
    def total_cost(self) -> float:
        """Total cost in USD."""
        return self._total_cost

    @property
    def total_tokens(self) -> int:
        """Total tokens (input + output)."""
        return self._total_input_tokens + self._total_output_tokens

    def get_costs_by_model(self) -> dict[str, dict[str, float]]:
        """Get cost breakdown by model."""
        return self._by_model.copy()

    def get_summary(self) -> dict[str, any]:
        """Get full cost tracking summary."""
        return {
            "total_cost": self._total_cost,
            "total_input_tokens": self._total_input_tokens,
            "total_output_tokens": self._total_output_tokens,
            "total_tokens": self.total_tokens,
            "total_cache_read_tokens": self._total_cache_read_tokens,
            "total_cache_creation_tokens": self._total_cache_creation_tokens,
            "call_count": self._call_count,
            "by_model": self._by_model,
        }

    def reset(self) -> None:
        """Reset all tracked costs."""
        self._total_cost = 0.0
        self._total_input_tokens = 0
        self._total_output_tokens = 0
        self._total_cache_read_tokens = 0
        self._total_cache_creation_tokens = 0
        self._by_model = {}
        self._call_count = 0


def aggregate_workflow_costs(agent_costs: list) -> dict[str, any]:
    """
    Aggregate costs from multiple agents in a workflow.

    Args:
        agent_costs: List of cost dictionaries from individual agents/calls

    Returns:
        Aggregated cost summary with per-model breakdown
    """
    total_cost = 0.0
    total_input_tokens = 0
    total_output_tokens = 0
    total_cache_read_tokens = 0
    total_cache_creation_tokens = 0
    by_model: dict[str, dict[str, any]] = {}

    for cost_entry in agent_costs:
        if not cost_entry:
            continue

        total_cost += cost_entry.get("cost", cost_entry.get("total_cost", 0.0))
        total_input_tokens += cost_entry.get("input_tokens", 0)
        total_output_tokens += cost_entry.get("output_tokens", 0)
        total_cache_read_tokens += cost_entry.get(
            "cache_read_tokens", cost_entry.get("cache_read_input_tokens", 0)
        )
        total_cache_creation_tokens += cost_entry.get(
            "cache_creation_tokens", cost_entry.get("cache_creation_input_tokens", 0)
        )

        model = cost_entry.get("model", "unknown")
        if model not in by_model:
            by_model[model] = {
                "cost": 0.0,
                "input_tokens": 0,
                "output_tokens": 0,
                "cache_read_tokens": 0,
                "cache_creation_tokens": 0,
                "call_count": 0,
            }

        by_model[model]["cost"] += cost_entry.get("cost", cost_entry.get("total_cost", 0.0))
        by_model[model]["input_tokens"] += cost_entry.get("input_tokens", 0)
        by_model[model]["output_tokens"] += cost_entry.get("output_tokens", 0)
        by_model[model]["cache_read_tokens"] += cost_entry.get(
            "cache_read_tokens", cost_entry.get("cache_read_input_tokens", 0)
        )
        by_model[model]["cache_creation_tokens"] += cost_entry.get(
            "cache_creation_tokens", cost_entry.get("cache_creation_input_tokens", 0)
        )
        by_model[model]["call_count"] += 1

    return {
        "total_cost": total_cost,
        "total_input_tokens": total_input_tokens,
        "total_output_tokens": total_output_tokens,
        "total_tokens": total_input_tokens + total_output_tokens,
        "total_cache_read_tokens": total_cache_read_tokens,
        "total_cache_creation_tokens": total_cache_creation_tokens,
        "by_model": by_model,
        "call_count": len(agent_costs),
    }
