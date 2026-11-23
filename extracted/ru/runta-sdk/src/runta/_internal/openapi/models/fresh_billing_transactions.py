from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.fresh_billing_transactions_freshness import (
    FreshBillingTransactionsFreshness,
)

if TYPE_CHECKING:
    from ..models.billing_transaction import BillingTransaction


T = TypeVar("T", bound="FreshBillingTransactions")


@_attrs_define
class FreshBillingTransactions:
    """
    Attributes:
        freshness (FreshBillingTransactionsFreshness):
        transactions (list[BillingTransaction]):
        next_page_token (None | str):
        as_of_unix_seconds (int):
    """

    freshness: FreshBillingTransactionsFreshness
    transactions: list[BillingTransaction]
    next_page_token: None | str
    as_of_unix_seconds: int

    def to_dict(self) -> dict[str, Any]:
        freshness = self.freshness.value

        transactions = []
        for transactions_item_data in self.transactions:
            transactions_item = transactions_item_data.to_dict()
            transactions.append(transactions_item)

        next_page_token: None | str
        next_page_token = self.next_page_token

        as_of_unix_seconds = self.as_of_unix_seconds

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "freshness": freshness,
                "transactions": transactions,
                "next_page_token": next_page_token,
                "as_of_unix_seconds": as_of_unix_seconds,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.billing_transaction import BillingTransaction

        d = dict(src_dict)
        freshness = FreshBillingTransactionsFreshness(d.pop("freshness"))

        transactions = []
        _transactions = d.pop("transactions")
        for transactions_item_data in _transactions:
            transactions_item = BillingTransaction.from_dict(transactions_item_data)

            transactions.append(transactions_item)

        def _parse_next_page_token(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        next_page_token = _parse_next_page_token(d.pop("next_page_token"))

        as_of_unix_seconds = d.pop("as_of_unix_seconds")

        fresh_billing_transactions = cls(
            freshness=freshness,
            transactions=transactions,
            next_page_token=next_page_token,
            as_of_unix_seconds=as_of_unix_seconds,
        )

        return fresh_billing_transactions
