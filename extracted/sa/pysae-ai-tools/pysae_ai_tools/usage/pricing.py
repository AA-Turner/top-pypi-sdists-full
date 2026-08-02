"""Claude per-token pricing and per-message cost computation.

Rates are USD per million tokens, sourced live from the official pricing doc and
cached on disk by ``pricing_source`` — there is no embedded table. Used to
estimate the cost of a Claude Code session in API-key mode, where there is no
plan window and every token is billed.
"""

from dataclasses import dataclass

# Fallback multipliers for the rare case a cached row lacks explicit cache rates
# (the live doc carries all of them). Standard published ratios.
CACHE_READ_MULT = 0.1
CACHE_WRITE_5M_MULT = 1.25
CACHE_WRITE_1H_MULT = 2.0


@dataclass(frozen=True)
class ModelPricing:
    """USD per million tokens. Cache rates fall back to input × standard multipliers."""

    input: float
    output: float
    cache_read: float | None = None
    cache_write_5m: float | None = None
    cache_write_1h: float | None = None

    @property
    def read_rate(self) -> float:
        return self.cache_read if self.cache_read is not None else self.input * CACHE_READ_MULT

    @property
    def write_5m_rate(self) -> float:
        return self.cache_write_5m if self.cache_write_5m is not None else self.input * CACHE_WRITE_5M_MULT

    @property
    def write_1h_rate(self) -> float:
        return self.cache_write_1h if self.cache_write_1h is not None else self.input * CACHE_WRITE_1H_MULT


def pricing_for(model: str, table: dict[str, ModelPricing]) -> ModelPricing | None:
    """Resolve a model id (possibly date-suffixed) against ``table``, longest prefix first."""
    if model in table:
        return table[model]
    for key in sorted(table, key=len, reverse=True):
        if model.startswith(key):
            return table[key]
    return None


def cost_of_usage(model: str, usage: dict[str, object], table: dict[str, ModelPricing]) -> float:
    """USD cost of one assistant turn from its `message.usage` block. 0.0 if model unknown."""
    p = pricing_for(model, table)
    if p is None:
        return 0.0

    def _int(key: str, src: dict[str, object]) -> int:
        v = src.get(key)
        return int(v) if isinstance(v, (int, float)) else 0

    inp = _int("input_tokens", usage)
    out = _int("output_tokens", usage)
    cache_read = _int("cache_read_input_tokens", usage)

    cache_creation = usage.get("cache_creation")
    if isinstance(cache_creation, dict):
        write_5m = _int("ephemeral_5m_input_tokens", cache_creation)
        write_1h = _int("ephemeral_1h_input_tokens", cache_creation)
    else:
        write_5m, write_1h = _int("cache_creation_input_tokens", usage), 0

    millions = (
        inp * p.input
        + out * p.output
        + cache_read * p.read_rate
        + write_5m * p.write_5m_rate
        + write_1h * p.write_1h_rate
    )
    return millions / 1_000_000
