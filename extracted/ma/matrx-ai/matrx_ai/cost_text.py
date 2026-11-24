"""A cost in a sentence a PERSON reads — through the host's injected formatter.

People see points, never dollars (law 14, ``common-docs/policies/points-and-money-in-the-ui.md``).
The package has no opinion on the host's points rate or its admin dollar toggle: the host injects
its ONE formatter with ``matrx_ai.configure(cost_text=...)`` (aidream: ``ai_points.format_points``).
A bare host gets points at the platform rate (20,000 points = $1) — never dollars.

Text a MODEL reads beside a dollar parameter it sets is not this module's business; only a
sentence composed for a person (a ``user_message``, a stop a person is shown) goes through here.
Same shape as ``matrx_seo.config.person_cost_text``.
"""

from __future__ import annotations

from collections.abc import Callable
from decimal import ROUND_CEILING, Decimal

#: Renders a USD amount as the words a person reads.
CostText = Callable[[Decimal], str]

_cost_text: CostText | None = None


def configure_cost_text(formatter: CostText | None) -> None:
    """Install (or, with ``None``, remove) the host's person-facing cost formatter."""
    global _cost_text
    _cost_text = formatter


def person_cost_text(amount_usd: Decimal | float | str | None) -> str:
    """``amount_usd`` as a person reads it: the host's formatter, else points at the platform rate."""
    if amount_usd is None:
        return "—"
    amount = Decimal(str(amount_usd))
    if _cost_text is not None:
        return _cost_text(amount)
    points = max(1, int((amount * 20_000).to_integral_value(rounding=ROUND_CEILING))) if amount > 0 else 0
    return f"{points:,} points"
