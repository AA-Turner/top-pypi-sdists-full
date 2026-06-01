"""
Cost tracking for Google ADK.

Provides pricing information and cost calculation for Gemini models
used by Google ADK agents.
"""


# Gemini model pricing per 1M tokens (input/output)
# Prices are based on Google AI Studio / Vertex AI pricing as of 2024
# See: https://ai.google.dev/pricing
GEMINI_MODEL_PRICING: dict[str, dict[str, float]] = {
    # Gemini 2.5 series (latest)
    "gemini-2.5-flash": {
        "input": 0.075,
        "output": 0.30,
    },
    "gemini-2.5-flash-preview": {
        "input": 0.075,
        "output": 0.30,
    },
    "gemini-2.5-flash-preview-05-20": {
        "input": 0.075,
        "output": 0.30,
    },
    "gemini-2.5-pro": {
        "input": 1.25,
        "output": 5.00,
    },
    "gemini-2.5-pro-preview": {
        "input": 1.25,
        "output": 5.00,
    },
    "gemini-2.5-pro-preview-05-06": {
        "input": 1.25,
        "output": 5.00,
    },
    # Gemini 2.0 series
    "gemini-2.0-flash": {
        "input": 0.10,
        "output": 0.40,
    },
    "gemini-2.0-flash-exp": {
        "input": 0.10,
        "output": 0.40,
    },
    "gemini-2.0-flash-lite": {
        "input": 0.075,
        "output": 0.30,
    },
    "gemini-2.0-pro": {
        "input": 1.25,
        "output": 5.00,
    },
    "gemini-2.0-pro-exp": {
        "input": 1.25,
        "output": 5.00,
    },
    # Gemini 1.5 series
    "gemini-1.5-flash": {
        "input": 0.075,
        "output": 0.30,
    },
    "gemini-1.5-flash-latest": {
        "input": 0.075,
        "output": 0.30,
    },
    "gemini-1.5-flash-001": {
        "input": 0.075,
        "output": 0.30,
    },
    "gemini-1.5-flash-002": {
        "input": 0.075,
        "output": 0.30,
    },
    "gemini-1.5-pro": {
        "input": 1.25,
        "output": 5.00,
    },
    "gemini-1.5-pro-latest": {
        "input": 1.25,
        "output": 5.00,
    },
    "gemini-1.5-pro-001": {
        "input": 1.25,
        "output": 5.00,
    },
    "gemini-1.5-pro-002": {
        "input": 1.25,
        "output": 5.00,
    },
    # Gemini 1.0 series (legacy)
    "gemini-1.0-pro": {
        "input": 0.50,
        "output": 1.50,
    },
    "gemini-1.0-pro-001": {
        "input": 0.50,
        "output": 1.50,
    },
    "gemini-1.0-pro-latest": {
        "input": 0.50,
        "output": 1.50,
    },
    "gemini-pro": {
        "input": 0.50,
        "output": 1.50,
    },
    # Vertex AI models (same pricing, different names)
    "models/gemini-2.5-flash": {
        "input": 0.075,
        "output": 0.30,
    },
    "models/gemini-2.5-pro": {
        "input": 1.25,
        "output": 5.00,
    },
    "models/gemini-2.0-flash": {
        "input": 0.10,
        "output": 0.40,
    },
    "models/gemini-1.5-flash": {
        "input": 0.075,
        "output": 0.30,
    },
    "models/gemini-1.5-pro": {
        "input": 1.25,
        "output": 5.00,
    },
    # Default fallback (use flash pricing)
    "default": {
        "input": 0.10,
        "output": 0.40,
    },
}


def get_model_pricing(model: str | None) -> tuple[float, float]:
    """
    Get pricing for a Gemini model (input/output per 1M tokens).

    Args:
        model: Model identifier (e.g., "gemini-2.5-flash")

    Returns:
        Tuple of (input_price, output_price) per 1M tokens
    """
    if not model:
        pricing = GEMINI_MODEL_PRICING["default"]
        return pricing["input"], pricing["output"]

    # Try exact match first
    if model in GEMINI_MODEL_PRICING:
        pricing = GEMINI_MODEL_PRICING[model]
        return pricing["input"], pricing["output"]

    # Normalize model name (remove prefix, lowercase)
    model_normalized = model.lower().replace("models/", "")

    if model_normalized in GEMINI_MODEL_PRICING:
        pricing = GEMINI_MODEL_PRICING[model_normalized]
        return pricing["input"], pricing["output"]

    # Try partial matches (for version variations)
    for key, pricing in GEMINI_MODEL_PRICING.items():
        if key != "default":
            key_lower = key.lower().replace("models/", "")
            if key_lower in model_normalized or model_normalized in key_lower:
                return pricing["input"], pricing["output"]

    # Match by model family
    if "flash" in model_normalized:
        if "2.5" in model_normalized:
            pricing = GEMINI_MODEL_PRICING["gemini-2.5-flash"]
        elif "2.0" in model_normalized:
            pricing = GEMINI_MODEL_PRICING["gemini-2.0-flash"]
        elif "1.5" in model_normalized:
            pricing = GEMINI_MODEL_PRICING["gemini-1.5-flash"]
        else:
            pricing = GEMINI_MODEL_PRICING["gemini-2.0-flash"]
        return pricing["input"], pricing["output"]

    if "pro" in model_normalized:
        if "2.5" in model_normalized:
            pricing = GEMINI_MODEL_PRICING["gemini-2.5-pro"]
        elif "2.0" in model_normalized:
            pricing = GEMINI_MODEL_PRICING["gemini-2.0-pro"]
        elif "1.5" in model_normalized:
            pricing = GEMINI_MODEL_PRICING["gemini-1.5-pro"]
        else:
            pricing = GEMINI_MODEL_PRICING["gemini-1.5-pro"]
        return pricing["input"], pricing["output"]

    # Fallback to default
    pricing = GEMINI_MODEL_PRICING["default"]
    return pricing["input"], pricing["output"]


def calculate_google_adk_cost(
    model: str | None,
    input_tokens: int = 0,
    output_tokens: int = 0,
) -> float:
    """
    Calculate cost for a Google ADK agent invocation.

    Args:
        model: Model identifier
        input_tokens: Number of input/prompt tokens
        output_tokens: Number of output/completion tokens

    Returns:
        Total cost in USD
    """
    input_price, output_price = get_model_pricing(model)

    input_cost = (input_tokens / 1_000_000) * input_price
    output_cost = (output_tokens / 1_000_000) * output_price

    return input_cost + output_cost


class GoogleADKCostTracker:
    """
    Tracks costs across multiple Google ADK agent invocations with per-model breakdown.

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
        model: str | None,
        input_tokens: int = 0,
        output_tokens: int = 0,
        cost: float | None = None,
    ) -> float:
        """
        Add usage from a Google ADK agent invocation.

        Args:
            model: Model identifier
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens
            cost: Pre-calculated cost (if None, will be calculated)

        Returns:
            Cost for this call in USD
        """
        if cost is None:
            cost = calculate_google_adk_cost(model, input_tokens, output_tokens)

        model_key = model or "unknown"

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
