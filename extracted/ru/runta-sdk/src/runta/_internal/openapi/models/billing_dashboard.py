from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.fresh_provider_value import FreshProviderValue
    from ..models.stale_provider_value import StaleProviderValue
    from ..models.unavailable_provider_value import UnavailableProviderValue
    from ..models.usage_quantity import UsageQuantity


T = TypeVar("T", bound="BillingDashboard")


@_attrs_define
class BillingDashboard:
    """
    Attributes:
        credit_balance (FreshProviderValue | StaleProviderValue | UnavailableProviderValue): Provider-backed amount with
            typed freshness semantics.
        rated_cost (FreshProviderValue | StaleProviderValue | UnavailableProviderValue): Provider-backed amount with
            typed freshness semantics.
        quantities (list[UsageQuantity]):
        billing_revision (int):
    """

    credit_balance: FreshProviderValue | StaleProviderValue | UnavailableProviderValue
    rated_cost: FreshProviderValue | StaleProviderValue | UnavailableProviderValue
    quantities: list[UsageQuantity]
    billing_revision: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.fresh_provider_value import FreshProviderValue
        from ..models.stale_provider_value import StaleProviderValue

        credit_balance: dict[str, Any]
        if isinstance(self.credit_balance, FreshProviderValue):
            credit_balance = self.credit_balance.to_dict()
        elif isinstance(self.credit_balance, StaleProviderValue):
            credit_balance = self.credit_balance.to_dict()
        else:
            credit_balance = self.credit_balance.to_dict()

        rated_cost: dict[str, Any]
        if isinstance(self.rated_cost, FreshProviderValue):
            rated_cost = self.rated_cost.to_dict()
        elif isinstance(self.rated_cost, StaleProviderValue):
            rated_cost = self.rated_cost.to_dict()
        else:
            rated_cost = self.rated_cost.to_dict()

        quantities = []
        for quantities_item_data in self.quantities:
            quantities_item = quantities_item_data.to_dict()
            quantities.append(quantities_item)

        billing_revision = self.billing_revision

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "credit_balance": credit_balance,
                "rated_cost": rated_cost,
                "quantities": quantities,
                "billing_revision": billing_revision,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.fresh_provider_value import FreshProviderValue
        from ..models.stale_provider_value import StaleProviderValue
        from ..models.unavailable_provider_value import UnavailableProviderValue
        from ..models.usage_quantity import UsageQuantity

        d = dict(src_dict)

        def _parse_credit_balance(
            data: object,
        ) -> FreshProviderValue | StaleProviderValue | UnavailableProviderValue:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_provider_value_type_0 = FreshProviderValue.from_dict(
                    data
                )

                return componentsschemas_provider_value_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_provider_value_type_1 = StaleProviderValue.from_dict(
                    data
                )

                return componentsschemas_provider_value_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            componentsschemas_provider_value_type_2 = (
                UnavailableProviderValue.from_dict(data)
            )

            return componentsschemas_provider_value_type_2

        credit_balance = _parse_credit_balance(d.pop("credit_balance"))

        def _parse_rated_cost(
            data: object,
        ) -> FreshProviderValue | StaleProviderValue | UnavailableProviderValue:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_provider_value_type_0 = FreshProviderValue.from_dict(
                    data
                )

                return componentsschemas_provider_value_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_provider_value_type_1 = StaleProviderValue.from_dict(
                    data
                )

                return componentsschemas_provider_value_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            componentsschemas_provider_value_type_2 = (
                UnavailableProviderValue.from_dict(data)
            )

            return componentsschemas_provider_value_type_2

        rated_cost = _parse_rated_cost(d.pop("rated_cost"))

        quantities = []
        _quantities = d.pop("quantities")
        for quantities_item_data in _quantities:
            quantities_item = UsageQuantity.from_dict(quantities_item_data)

            quantities.append(quantities_item)

        billing_revision = d.pop("billing_revision")

        billing_dashboard = cls(
            credit_balance=credit_balance,
            rated_cost=rated_cost,
            quantities=quantities,
            billing_revision=billing_revision,
        )

        billing_dashboard.additional_properties = d
        return billing_dashboard

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
