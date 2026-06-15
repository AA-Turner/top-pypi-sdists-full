from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
    from ..models.plan_definition_limits import PlanDefinitionLimits
    from ..models.plan_definition_overage_rates import PlanDefinitionOverageRates


T = TypeVar("T", bound="PlanDefinition")


@_attrs_define
class PlanDefinition:
    """Per-plan pricing and limits for a product.

    Attributes:
        price_monthly_cents (int): Monthly list price in cents. `0` for free plans.
        limits (PlanDefinitionLimits): Map of limit key to the cap that applies on this plan. `-1` indicates an
            unlimited cap.
        overage_rates (None | PlanDefinitionOverageRates | Unset): For metered products only: map of metered limit key
            to the per-unit overage price in micro-USD ($0.000001) charged for each unit beyond the plan's included
            allotment. A rate of `0` means the plan stops at its allotment with no overage. Omitted for products that are
            not metered.
    """

    price_monthly_cents: int
    limits: PlanDefinitionLimits
    overage_rates: None | PlanDefinitionOverageRates | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.plan_definition_overage_rates import PlanDefinitionOverageRates

        price_monthly_cents = self.price_monthly_cents

        limits = self.limits.to_dict()

        overage_rates: dict[str, Any] | None | Unset
        if isinstance(self.overage_rates, Unset):
            overage_rates = UNSET
        elif isinstance(self.overage_rates, PlanDefinitionOverageRates):
            overage_rates = self.overage_rates.to_dict()
        else:
            overage_rates = self.overage_rates

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "price_monthly_cents": price_monthly_cents,
                "limits": limits,
            }
        )
        if overage_rates is not UNSET:
            field_dict["overage_rates"] = overage_rates

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.plan_definition_limits import PlanDefinitionLimits
        from ..models.plan_definition_overage_rates import PlanDefinitionOverageRates

        d = dict(src_dict)
        price_monthly_cents = d.pop("price_monthly_cents")

        limits = PlanDefinitionLimits.from_dict(d.pop("limits"))

        def _parse_overage_rates(data: object) -> None | PlanDefinitionOverageRates | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                overage_rates_type_0 = PlanDefinitionOverageRates.from_dict(data)

                return overage_rates_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | PlanDefinitionOverageRates | Unset, data)

        overage_rates = _parse_overage_rates(d.pop("overage_rates", UNSET))

        plan_definition = cls(
            price_monthly_cents=price_monthly_cents,
            limits=limits,
            overage_rates=overage_rates,
        )

        plan_definition.additional_properties = d
        return plan_definition

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
