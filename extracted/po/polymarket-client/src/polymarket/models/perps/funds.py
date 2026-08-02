"""Perps deposit and withdrawal models."""

from pydantic import Field

from polymarket.models.base import BaseModel
from polymarket.models.perps._validators import (
    OptionalPerpsTimestamp,
    OptionalTxHash,
    PerpsTimestamp,
    _Decimal,
)
from polymarket.models.perps.types import (
    PerpsDepositStatus,
    PerpsWithdrawalId,
    PerpsWithdrawalStatus,
)


class PerpsDeposit(BaseModel):
    """One deposit into the Perps account."""

    hash: str
    asset: str
    amount: _Decimal
    status: PerpsDepositStatus
    from_address: str = Field(validation_alias="from")
    to: str
    confirmations: int
    required_confirmations: int
    created_at: PerpsTimestamp = Field(validation_alias="created_timestamp")
    confirmed_at: OptionalPerpsTimestamp = Field(
        default=None, validation_alias="confirmed_timestamp"
    )


class PerpsDepositUpdate(BaseModel):
    """Streaming status update for one Perps deposit."""

    hash: OptionalTxHash = None
    asset: str
    amount: _Decimal
    status: PerpsDepositStatus


class PerpsWithdrawal(BaseModel):
    """One withdrawal from the Perps account."""

    withdrawal_id: PerpsWithdrawalId = Field(validation_alias="withdraw_id")
    asset: str
    amount: _Decimal
    fee: _Decimal
    status: PerpsWithdrawalStatus
    to: str
    hash: OptionalTxHash = None
    confirmations: int
    required_confirmations: int
    created_at: PerpsTimestamp = Field(validation_alias="created_timestamp")
    confirmed_at: OptionalPerpsTimestamp = Field(
        default=None, validation_alias="confirmed_timestamp"
    )


class PerpsWithdrawalUpdate(BaseModel):
    """Streaming status update for one Perps withdrawal."""

    withdrawal_id: PerpsWithdrawalId = Field(validation_alias="withdraw_id")
    asset: str
    amount: _Decimal
    fee: _Decimal
    status: PerpsWithdrawalStatus
    to: str
    hash: OptionalTxHash = None


__all__ = [
    "PerpsDeposit",
    "PerpsDepositUpdate",
    "PerpsWithdrawal",
    "PerpsWithdrawalUpdate",
]
