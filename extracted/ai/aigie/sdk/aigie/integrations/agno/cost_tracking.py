"""
Cost tracking for Agno agents.

Provides pricing information and cost calculation for various model providers
supported by Agno (Anthropic, OpenAI, Gemini, Bedrock, Mistral, etc.).
"""


# Model pricing per 1M tokens (input/output)
# Prices are approximate and may vary by region/provider
AGNO_MODEL_PRICING: dict[str, dict[str, float]] = {
    # Anthropic Claude (direct)
    "claude-3-5-sonnet-20241022": {
        "input": 3.00,
        "output": 15.00,
    },
    "claude-3-5-haiku-20241022": {
        "input": 1.00,
        "output": 5.00,
    },
    "claude-3-opus-20240229": {
        "input": 15.00,
        "output": 75.00,
    },
    "claude-3-sonnet-20240229": {
        "input": 3.00,
        "output": 15.00,
    },
    "claude-3-haiku-20240307": {
        "input": 0.25,
        "output": 1.25,
    },
    # Claude shorthand aliases
    "claude-3-5-sonnet": {
        "input": 3.00,
        "output": 15.00,
    },
    "claude-3-haiku": {
        "input": 0.25,
        "output": 1.25,
    },
    "claude-3-opus": {
        "input": 15.00,
        "output": 75.00,
    },
    # Amazon Bedrock - Claude models
    "anthropic.claude-3-5-sonnet-20241022-v2:0": {
        "input": 3.00,
        "output": 15.00,
    },
    "anthropic.claude-3-5-haiku-20241022-v1:0": {
        "input": 1.00,
        "output": 5.00,
    },
    "anthropic.claude-3-opus-20240229-v1:0": {
        "input": 15.00,
        "output": 75.00,
    },
    "anthropic.claude-3-sonnet-20240229-v1:0": {
        "input": 3.00,
        "output": 15.00,
    },
    # Amazon Nova
    "us.amazon.nova-pro-v1:0": {
        "input": 3.00,
        "output": 15.00,
    },
    "us.amazon.nova-lite-v1:0": {
        "input": 0.10,
        "output": 0.40,
    },
    "us.amazon.nova-micro-v1:0": {
        "input": 0.05,
        "output": 0.20,
    },
    # OpenAI
    "gpt-4o": {
        "input": 2.50,
        "output": 10.00,
    },
    "gpt-4o-mini": {
        "input": 0.15,
        "output": 0.60,
    },
    "gpt-4-turbo": {
        "input": 10.00,
        "output": 30.00,
    },
    "gpt-4": {
        "input": 30.00,
        "output": 60.00,
    },
    "gpt-3.5-turbo": {
        "input": 0.50,
        "output": 1.50,
    },
    "o1": {
        "input": 15.00,
        "output": 60.00,
    },
    "o1-mini": {
        "input": 3.00,
        "output": 12.00,
    },
    "o3-mini": {
        "input": 1.10,
        "output": 4.40,
    },
    # Google Gemini
    "gemini-2.0-flash": {
        "input": 0.10,
        "output": 0.40,
    },
    "gemini-2.0-flash-exp": {
        "input": 0.075,
        "output": 0.30,
    },
    "gemini-2.0-flash-thinking-exp": {
        "input": 0.075,
        "output": 0.30,
    },
    "gemini-1.5-pro": {
        "input": 1.25,
        "output": 5.00,
    },
    "gemini-1.5-flash": {
        "input": 0.075,
        "output": 0.30,
    },
    "gemini-pro": {
        "input": 0.50,
        "output": 1.50,
    },
    # Mistral
    "mistral-large-latest": {
        "input": 3.00,
        "output": 9.00,
    },
    "mistral-small-latest": {
        "input": 0.20,
        "output": 0.60,
    },
    "mistral-7b-instruct": {
        "input": 0.25,
        "output": 0.25,
    },
    # Groq
    "llama-3.1-70b-versatile": {
        "input": 0.59,
        "output": 0.79,
    },
    "llama-3.1-8b-instant": {
        "input": 0.05,
        "output": 0.08,
    },
    "mixtral-8x7b-32768": {
        "input": 0.27,
        "output": 0.27,
    },
    # Default fallback (use average pricing)
    "default": {
        "input": 2.00,
        "output": 8.00,
    },
}


def get_model_pricing(model_id: str | None) -> tuple[float, float]:
    """
    Get pricing for a model (input/output per 1M tokens).

    Args:
        model_id: Model identifier (e.g., "gpt-4o", "claude-3-5-sonnet-20241022")

    Returns:
        Tuple of (input_price, output_price) per 1M tokens
    """
    if not model_id:
        pricing = AGNO_MODEL_PRICING["default"]
        return pricing["input"], pricing["output"]

    # Try exact match first
    if model_id in AGNO_MODEL_PRICING:
        pricing = AGNO_MODEL_PRICING[model_id]
        return pricing["input"], pricing["output"]

    # Try partial matches (for version variations)
    model_id_lower = model_id.lower()
    for key, pricing in AGNO_MODEL_PRICING.items():
        if key.lower() in model_id_lower or model_id_lower in key.lower():
            return pricing["input"], pricing["output"]

    # Fallback to default
    pricing = AGNO_MODEL_PRICING["default"]
    return pricing["input"], pricing["output"]


def calculate_agno_cost(
    model_id: str | None,
    input_tokens: int = 0,
    output_tokens: int = 0,
) -> float:
    """
    Calculate cost for an Agno agent invocation.

    Args:
        model_id: Model identifier
        input_tokens: Number of input tokens
        output_tokens: Number of output tokens

    Returns:
        Total cost in USD
    """
    input_price, output_price = get_model_pricing(model_id)

    input_cost = (input_tokens / 1_000_000) * input_price
    output_cost = (output_tokens / 1_000_000) * output_price

    return input_cost + output_cost


class AgnoCostTracker:
    """
    Tracks costs across multiple Agno agent invocations with per-model breakdown.

    Useful for tracking costs in multi-agent workflows.
    """

    def __init__(self):
        self._total_cost: float = 0.0
        self._total_input_tokens: int = 0
        self._total_output_tokens: int = 0
        self._by_model: dict[str, dict[str, float]] = {}
        self._call_count: int = 0

    def add_usage(
        self,
        model_id: str | None,
        input_tokens: int = 0,
        output_tokens: int = 0,
        cost: float | None = None,
    ) -> float:
        """
        Add usage from an Agno agent invocation.

        Args:
            model_id: Model identifier
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens
            cost: Pre-calculated cost (if None, will be calculated)

        Returns:
            Cost for this call in USD
        """
        if cost is None:
            cost = calculate_agno_cost(model_id, input_tokens, output_tokens)

        model_key = model_id or "unknown"

        # Update totals
        self._total_cost += cost
        self._total_input_tokens += input_tokens
        self._total_output_tokens += output_tokens
        self._call_count += 1

        # Update per-model breakdown
        if model_key not in self._by_model:
            self._by_model[model_key] = {
                "cost": 0.0,
                "input_tokens": 0,
                "output_tokens": 0,
                "call_count": 0,
            }

        self._by_model[model_key]["cost"] += cost
        self._by_model[model_key]["input_tokens"] += input_tokens
        self._by_model[model_key]["output_tokens"] += output_tokens
        self._by_model[model_key]["call_count"] += 1

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
            "call_count": self._call_count,
            "by_model": self._by_model,
        }

    def reset(self) -> None:
        """Reset all tracked costs."""
        self._total_cost = 0.0
        self._total_input_tokens = 0
        self._total_output_tokens = 0
        self._by_model = {}
        self._call_count = 0


def aggregate_workflow_costs(agent_costs: list) -> dict[str, any]:
    """
    Aggregate costs from multiple Agno agents in a workflow.

    Args:
        agent_costs: List of cost dictionaries from individual agents/calls

    Returns:
        Aggregated cost summary with per-model breakdown
    """
    total_cost = 0.0
    total_input_tokens = 0
    total_output_tokens = 0
    by_model: dict[str, dict[str, any]] = {}

    for cost_entry in agent_costs:
        if not cost_entry:
            continue

        total_cost += cost_entry.get("cost", cost_entry.get("total_cost", 0.0))
        total_input_tokens += cost_entry.get("input_tokens", 0)
        total_output_tokens += cost_entry.get("output_tokens", 0)

        model = cost_entry.get("model", cost_entry.get("model_id", "unknown"))
        if model not in by_model:
            by_model[model] = {
                "cost": 0.0,
                "input_tokens": 0,
                "output_tokens": 0,
                "call_count": 0,
            }

        by_model[model]["cost"] += cost_entry.get("cost", cost_entry.get("total_cost", 0.0))
        by_model[model]["input_tokens"] += cost_entry.get("input_tokens", 0)
        by_model[model]["output_tokens"] += cost_entry.get("output_tokens", 0)
        by_model[model]["call_count"] += 1

    return {
        "total_cost": total_cost,
        "total_input_tokens": total_input_tokens,
        "total_output_tokens": total_output_tokens,
        "total_tokens": total_input_tokens + total_output_tokens,
        "by_model": by_model,
        "call_count": len(agent_costs),
    }
