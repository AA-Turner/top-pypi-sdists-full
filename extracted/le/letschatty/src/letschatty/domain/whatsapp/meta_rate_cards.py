"""The rate card of Meta («tarifas de Meta», api-chatty `docs/meta-gastos/tdd.md`): the official price of a delivered,
charged message by market and category, in one currency, from a date on. Meta changes it only on 1-Jan, 1-Apr, 1-Jul
and 1-Oct; each card is kept, so a month is priced with the card in force each day. Read-only for the app: only the
loading script writes it, from Meta's published files.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from typing import Dict, List, Mapping, Optional, Protocol

#: The market Meta uses for a country it does not list.
OTHER_MARKET = "Other"


@dataclass(frozen=True)
class RateCard:
    """`rates[market][category]`: the price of one message, `Decimal`. `market_of_country[ISO2]`: Meta's table of
    country calling codes to markets (a country of a «Rest of…» region maps to the region)."""

    currency: str
    effective_from: date
    rates: Mapping[str, Mapping[str, Decimal]]
    market_of_country: Mapping[str, str] = field(default_factory=dict)

    def rate(self, market: str, category: str) -> Optional[Decimal]:
        """The price, or None when the card has no such market or category (never a guess)."""
        return self.rates.get(market, {}).get(category)

    def market_of(self, country: Optional[str]) -> str:
        """The market of an ISO2 country; «Other» for one the card does not list or for no country."""
        if not country:
            return OTHER_MARKET
        return self.market_of_country.get(country.upper(), OTHER_MARKET)


class RateCardRepository(Protocol):
    async def of(self, currency: str) -> List[RateCard]:
        """Every card of the currency, oldest first; empty when none was loaded."""
        ...

    async def save(self, card: RateCard) -> None:
        """Stores (or replaces) the card of its currency and date (the backoffice's upload, or the script)."""
        ...

    async def all(self) -> List[RateCard]:
        """Every card of every currency, oldest first."""
        ...


def card_for(cards: List[RateCard], day: date) -> Optional[RateCard]:
    """The card in force on `day`: the latest `effective_from` not after it. None when every card is later."""
    in_force = [card for card in cards if card.effective_from <= day]
    return max(in_force, key=lambda card: card.effective_from) if in_force else None


def rates_from_rows(rows: Mapping[str, Mapping[str, str]]) -> Dict[str, Dict[str, Decimal]]:
    """`{market: {category: "0.0618"}}` as text (as stored) to `Decimal`, skipping the cells Meta marks «n/a»."""
    out: Dict[str, Dict[str, Decimal]] = {}
    for market, by_category in rows.items():
        out[market] = {category: Decimal(str(value)) for category, value in by_category.items()
                       if value not in (None, "", "n/a")}
    return out
