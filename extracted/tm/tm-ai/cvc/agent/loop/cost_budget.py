"""Cost budget — USD spend cap analog to Claude Code's ``max_budget_usd``.

Claude Code's agent loop supports two limit dimensions:

* ``max_turns`` (iteration count) — CVC already has this via
  :class:`cvc.agent.loop.budget.IterationBudget`.
* ``max_budget_usd`` (USD spend) — THIS module fills that gap.

When the budget is hit, the loop returns ``ResultMessage`` with subtype
``error_max_budget_usd``. CVC's analog is :class:`CostBudgetExceeded`,
raised by :meth:`CostBudget.consume_usd` returning ``False``.

Design notes
------------
* Thread-safe: the parent creates one ``CostBudget``, subagents inherit.
  Same inheritance pattern as :class:`IterationBudget`.
* Refundable: a tool that *retries after fail* can refund the failed
  attempt's cost via :meth:`refund_usd`.
* Pricing source-of-truth is a function passed at construction time
  (``pricing_fn``). Defaults to :data:`DEFAULT_PRICING` (a snapshot of
  public Anthropic + OpenAI list prices as of 2026-06-21). Callers
  (CLI, dashboard, future ScheduledJob) override per their config.
* Conservative rounding: cost is rounded UP at every step so the
  budget can never be silently exceeded by a few fractional cents.
"""

from __future__ import annotations

import threading
from dataclasses import dataclass
from typing import Callable, Mapping, Optional

__all__ = [
    "CostBudget",
    "CostBudgetExceeded",
    "ModelPricing",
    "DEFAULT_PRICING",
    "estimate_turn_cost",
]


class CostBudgetExceeded(Exception):
    """Raised when :meth:`CostBudget.consume_usd` would exceed the cap.

    The exception carries ``spent_usd``, ``cap_usd``, and ``remaining_usd``
    so the loop's error path can render a precise diagnostic.
    """

    def __init__(self, spent_usd: float, cap_usd: float) -> None:
        self.spent_usd = spent_usd
        self.cap_usd = cap_usd
        self.remaining_usd = max(0.0, cap_usd - spent_usd)
        super().__init__(
            f"cost budget exceeded: spent=${spent_usd:.4f} "
            f"of cap=${cap_usd:.4f} (remaining=${self.remaining_usd:.4f})"
        )


@dataclass(frozen=True)
class ModelPricing:
    """Per-million-token pricing for one model.

    Attributes are in USD per 1M tokens. Cache pricing reflects the
    discounted rate Anthropic gives on cache hits (typically 10% of
    input price).
    """

    input_per_million: float
    output_per_million: float
    cache_read_per_million: float = 0.0
    cache_write_per_million: float = 0.0

    def estimate(
        self,
        prompt_tokens: int,
        completion_tokens: int,
        cache_read_tokens: int = 0,
        cache_write_tokens: int = 0,
    ) -> float:
        """Return the USD cost for the given token counts."""
        # Always round UP so the budget is never silently blown by
        # sub-cent fractions (especially on tiny models).
        cost = 0.0
        cost += prompt_tokens / 1_000_000.0 * self.input_per_million
        cost += completion_tokens / 1_000_000.0 * self.output_per_million
        cost += cache_read_tokens / 1_000_000.0 * self.cache_read_per_million
        cost += cache_write_tokens / 1_000_000.0 * self.cache_write_per_million
        # Round up to the nearest 1/10000 of a dollar.
        from math import ceil
        return ceil(cost * 10000) / 10000.0


# Public list-price snapshot. Re-verify before quoting in docs.
# Sources: Anthropic pricing page (claude-sonnet-4 / opus-4), OpenAI
# pricing page (gpt-5 / gpt-5-mini), Google AI Studio (gemini-2.5-pro).
DEFAULT_PRICING: Mapping[str, ModelPricing] = {
    # Anthropic
    "claude-opus-4": ModelPricing(15.0, 75.0, 1.50, 18.75),
    "claude-sonnet-4": ModelPricing(3.0, 15.0, 0.30, 3.75),
    "claude-haiku-4": ModelPricing(0.80, 4.0, 0.08, 1.0),
    # OpenAI
    "gpt-5": ModelPricing(5.0, 20.0, 0.50, 0.0),
    "gpt-5-mini": ModelPricing(0.50, 2.0, 0.05, 0.0),
    "gpt-4.1": ModelPricing(3.0, 12.0, 0.30, 0.0),
    "o3": ModelPricing(15.0, 60.0, 0.0, 0.0),
    # Google
    "gemini-2.5-pro": ModelPricing(2.5, 10.0, 0.0, 0.0),
    "gemini-2.5-flash": ModelPricing(0.30, 1.20, 0.0, 0.0),
}


def estimate_turn_cost(
    model: str,
    prompt_tokens: int,
    completion_tokens: int,
    cache_read_tokens: int = 0,
    cache_write_tokens: int = 0,
    *,
    pricing: Optional[Mapping[str, ModelPricing]] = None,
) -> float:
    """Estimate the USD cost of one turn.

    Returns ``0.0`` for unknown models (defensive default — never raises
    during a turn). The caller is expected to log a warning if a model
    isn't in the pricing table, since the budget tracker will undercount.
    """
    table = pricing or DEFAULT_PRICING
    p = table.get(model)
    if p is None:
        return 0.0
    return p.estimate(prompt_tokens, completion_tokens, cache_read_tokens, cache_write_tokens)


PricingFn = Callable[[str, int, int, int, int], float]
"""Signature: ``(model, prompt_tokens, completion_tokens,
cache_read_tokens, cache_write_tokens) -> USD cost``."""


class CostBudget:
    """Thread-safe USD cost budget. Parent creates one, subagents inherit.

    The budget is consumed *as each turn's cost is observed* — typically
    by the loop body right after the provider returns the usage block.
    On exhaustion, the loop should call :meth:`is_exhausted` and exit
    with the same ``error_max_budget_usd`` ResultMessage shape Claude
    Code uses.
    """

    DEFAULT_PARENT_USD = 5.00
    DEFAULT_SUBAGENT_USD = 2.00

    def __init__(
        self,
        cap_usd: float = DEFAULT_PARENT_USD,
        *,
        pricing: Optional[Mapping[str, ModelPricing]] = None,
        pricing_fn: Optional[PricingFn] = None,
    ) -> None:
        self._cap = max(0.0, float(cap_usd))
        self._spent = 0.0
        self._refunded = 0.0
        self._lock = threading.Lock()
        # Pricing resolution: explicit fn > explicit table > defaults.
        if pricing_fn is not None:
            self._pricing_fn = pricing_fn
        elif pricing is not None:
            self._pricing_fn = lambda model, p, c, cr, cw: estimate_turn_cost(
                model, p, c, cr, cw, pricing=pricing,
            )
        else:
            self._pricing_fn = estimate_turn_cost

    @classmethod
    def for_parent(cls, cap_usd: Optional[float] = None) -> "CostBudget":
        return cls(cap_usd or cls.DEFAULT_PARENT_USD)

    @classmethod
    def for_subagent(cls, cap_usd: Optional[float] = None) -> "CostBudget":
        return cls(cap_usd or cls.DEFAULT_SUBAGENT_USD)

    @property
    def cap_usd(self) -> float:
        return self._cap

    @property
    def spent_usd(self) -> float:
        with self._lock:
            return self._spent - self._refunded

    def remaining_usd(self) -> float:
        with self._lock:
            return max(0.0, self._cap - (self._spent - self._refunded))

    def is_exhausted(self) -> bool:
        return self.remaining_usd() <= 0.0

    def consume_usd(
        self,
        model: str,
        prompt_tokens: int,
        completion_tokens: int,
        cache_read_tokens: int = 0,
        cache_write_tokens: int = 0,
    ) -> bool:
        """Estimate and consume the cost of one turn.

        Returns True if the turn fits within budget, False if not (and
        the turn's cost is NOT counted toward the budget on rejection
        — the caller's tool call never actually happened).

        Raises :class:`CostBudgetExceeded` only when called with
        ``raise_on_exceed=True`` (default False) so the loop can
        decide whether to surface as an exception or a soft halt.
        """
        cost = self._pricing_fn(
            model, prompt_tokens, completion_tokens, cache_read_tokens, cache_write_tokens,
        )
        with self._lock:
            effective = self._spent - self._refunded
            if effective + cost > self._cap:
                return False
            self._spent += cost
            return True

    def refund_usd(self, amount: float) -> None:
        """Refund a previously-charged amount (e.g. failed retry)."""
        with self._lock:
            self._refunded += max(0.0, float(amount))

    def reset(self) -> None:
        with self._lock:
            self._spent = 0.0
            self._refunded = 0.0

    def status(self) -> dict:
        """Snapshot for dashboards / ResultMessage."""
        with self._lock:
            spent = self._spent - self._refunded
        return {
            "cap_usd": self._cap,
            "spent_usd": round(spent, 4),
            "remaining_usd": round(max(0.0, self._cap - spent), 4),
            "exhausted": spent >= self._cap,
        }
