"""Rank-source choices a MEMBER or AGENT sees are plain tiers, never a vendor id (R-1, R-18).

Internally a rank check still runs on ``brave`` / ``serpapi`` / ``dataforseo``; a tool schema lists ``web`` /
``google`` / ``ai_answers`` and the argument model accepts either spelling (saved workflows and old agent
runs keep working). ``ProviderWithAnswers`` is the three-way choice, ``Provider`` the two-way one.
"""

from __future__ import annotations

from typing import Annotated, Any, Literal

from pydantic import BeforeValidator, WithJsonSchema

TIER_TO_PROVIDER: dict[str, str] = {"web": "brave", "google": "serpapi", "ai_answers": "dataforseo"}

#: Two phrases the ``seo`` / ``seo_rank`` schema listed for ONE day (four stored versions, 2026-10-16/17, enum
#: ``["brave", "our search data service", "our SEO data service"]``, positionally the same three choices). A stored call
#: or agent config that picked them up still validates, mapped to today's values (BREAK-LEDGER OTH-9).
INTERMEDIATE_PHRASES: dict[str, str] = {"our search data service": "serpapi", "our SEO data service": "dataforseo"}


def accept_tier(value: Any) -> Any:
    """``web`` -> ``brave`` etc.; every other value (the legacy ids, junk) is left for the Literal to judge."""
    if not isinstance(value, str):
        return value
    return TIER_TO_PROVIDER.get(value) or INTERMEDIATE_PHRASES.get(value) or value


Provider = Annotated[
    Literal["brave", "serpapi"],
    BeforeValidator(accept_tier),
    WithJsonSchema({"type": "string", "enum": ["web", "google"]}),
]
ProviderWithAnswers = Annotated[
    Literal["brave", "serpapi", "dataforseo"],
    BeforeValidator(accept_tier),
    WithJsonSchema({"type": "string", "enum": ["web", "google", "ai_answers"]}),
]

__all__ = ["INTERMEDIATE_PHRASES", "Provider", "ProviderWithAnswers", "TIER_TO_PROVIDER", "accept_tier"]
