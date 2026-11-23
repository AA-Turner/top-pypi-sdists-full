from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

T = TypeVar("T", bound="CreditGrant")


@_attrs_define
class CreditGrant:
    """
    Attributes:
        id (str):
        campaign (str):
        amount_cents (int):
        remaining_cents (int):
        currency (str):
        effective_at (datetime.datetime):
        expires_at (datetime.datetime | None):
    """

    id: str
    campaign: str
    amount_cents: int
    remaining_cents: int
    currency: str
    effective_at: datetime.datetime
    expires_at: datetime.datetime | None

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        campaign = self.campaign

        amount_cents = self.amount_cents

        remaining_cents = self.remaining_cents

        currency = self.currency

        effective_at = self.effective_at.isoformat()

        expires_at: None | str
        if isinstance(self.expires_at, datetime.datetime):
            expires_at = self.expires_at.isoformat()
        else:
            expires_at = self.expires_at

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "id": id,
                "campaign": campaign,
                "amount_cents": amount_cents,
                "remaining_cents": remaining_cents,
                "currency": currency,
                "effective_at": effective_at,
                "expires_at": expires_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        campaign = d.pop("campaign")

        amount_cents = d.pop("amount_cents")

        remaining_cents = d.pop("remaining_cents")

        currency = d.pop("currency")

        effective_at = datetime.datetime.fromisoformat(
            d.pop("effective_at").replace("Z", "+00:00")
        )

        def _parse_expires_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                expires_at_type_0 = datetime.datetime.fromisoformat(
                    data.replace("Z", "+00:00")
                )

                return expires_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        expires_at = _parse_expires_at(d.pop("expires_at"))

        credit_grant = cls(
            id=id,
            campaign=campaign,
            amount_cents=amount_cents,
            remaining_cents=remaining_cents,
            currency=currency,
            effective_at=effective_at,
            expires_at=expires_at,
        )

        return credit_grant
