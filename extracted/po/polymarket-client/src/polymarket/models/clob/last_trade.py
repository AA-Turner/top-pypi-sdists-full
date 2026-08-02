from __future__ import annotations

from polymarket.models.base import BaseModel
from polymarket.models.clob._validators import (
    _DecimalFromString,  # pyright: ignore[reportPrivateUsage]
)
from polymarket.models.types import OrderSide, TokenId


class LastTradePrice(BaseModel):
    price: _DecimalFromString
    side: OrderSide


class LastTradePriceForToken(BaseModel):
    token_id: TokenId
    price: _DecimalFromString
    side: OrderSide


__all__ = ["LastTradePrice", "LastTradePriceForToken"]
