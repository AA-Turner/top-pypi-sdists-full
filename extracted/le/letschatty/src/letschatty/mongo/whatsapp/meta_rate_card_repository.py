"""`RateCardRepository` on `meta_tarifas` (api-chatty `docs/meta-gastos/tdd.md`). One document per currency and date:
`{_id: "<currency>:<YYYY-MM-DD>", currency, effective_from: "YYYY-MM-DD", rates: {market: {category: "0.0618"}},
market_of_country: {ISO2: market}}`. Prices are stored as text so no float ever touches them."""
from __future__ import annotations

from datetime import date
from typing import Any, List, Mapping

from ...domain.whatsapp.meta_rate_cards import RateCard, rates_from_rows

META_RATE_CARDS = "meta_tarifas"


def card_of(document: Mapping[str, Any]) -> RateCard:
    return RateCard(currency=document["currency"], effective_from=date.fromisoformat(document["effective_from"]),
                    rates=rates_from_rows(document.get("rates") or {}),
                    market_of_country=dict(document.get("market_of_country") or {}))


class MongoRateCardRepository:
    """On a Motor collection, resolved by whoever wires it."""

    def __init__(self, collection):
        self.collection = collection

    async def of(self, currency: str) -> List[RateCard]:
        cursor = self.collection.find({"currency": currency}).sort("effective_from", 1)
        return [card_of(document) async for document in cursor]

    async def all(self) -> List[RateCard]:
        cursor = self.collection.find({}).sort([("effective_from", 1), ("currency", 1)])
        return [card_of(document) async for document in cursor]

    async def save(self, card: RateCard) -> None:
        day = card.effective_from.isoformat()
        await self.collection.replace_one(
            {"_id": f"{card.currency}:{day}"},
            {"currency": card.currency, "effective_from": day,
             "rates": {market: {category: str(price) for category, price in by_category.items()}
                       for market, by_category in card.rates.items()},
             "market_of_country": dict(card.market_of_country)},
            upsert=True)
