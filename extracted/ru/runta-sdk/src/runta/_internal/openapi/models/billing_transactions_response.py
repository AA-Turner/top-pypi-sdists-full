from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.fresh_billing_transactions import FreshBillingTransactions
    from ..models.stale_billing_transactions import StaleBillingTransactions
    from ..models.unavailable_billing_transactions import UnavailableBillingTransactions


T = TypeVar("T", bound="BillingTransactionsResponse")


@_attrs_define
class BillingTransactionsResponse:
    """
    Attributes:
        data (FreshBillingTransactions | StaleBillingTransactions | UnavailableBillingTransactions):
    """

    data: (
        FreshBillingTransactions
        | StaleBillingTransactions
        | UnavailableBillingTransactions
    )
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.fresh_billing_transactions import FreshBillingTransactions
        from ..models.stale_billing_transactions import StaleBillingTransactions

        data: dict[str, Any]
        if isinstance(self.data, FreshBillingTransactions):
            data = self.data.to_dict()
        elif isinstance(self.data, StaleBillingTransactions):
            data = self.data.to_dict()
        else:
            data = self.data.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "data": data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.fresh_billing_transactions import FreshBillingTransactions
        from ..models.stale_billing_transactions import StaleBillingTransactions
        from ..models.unavailable_billing_transactions import (
            UnavailableBillingTransactions,
        )

        d = dict(src_dict)

        def _parse_data(
            data: object,
        ) -> (
            FreshBillingTransactions
            | StaleBillingTransactions
            | UnavailableBillingTransactions
        ):
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_billing_transactions_type_0 = (
                    FreshBillingTransactions.from_dict(data)
                )

                return componentsschemas_billing_transactions_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_billing_transactions_type_1 = (
                    StaleBillingTransactions.from_dict(data)
                )

                return componentsschemas_billing_transactions_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            componentsschemas_billing_transactions_type_2 = (
                UnavailableBillingTransactions.from_dict(data)
            )

            return componentsschemas_billing_transactions_type_2

        data = _parse_data(d.pop("data"))

        billing_transactions_response = cls(
            data=data,
        )

        billing_transactions_response.additional_properties = d
        return billing_transactions_response

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
