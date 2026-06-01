from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field


if TYPE_CHECKING:
    from ..models.plan_definition_limits import PlanDefinitionLimits


T = TypeVar("T", bound="PlanDefinition")


@_attrs_define
class PlanDefinition:
    """Per-plan pricing and limits for a product.

    Attributes:
        price_monthly_cents (int): Monthly list price in cents. `0` for free plans.
        limits (PlanDefinitionLimits): Map of limit key to the cap that applies on this plan. `-1` indicates an
            unlimited cap.
    """

    price_monthly_cents: int
    limits: PlanDefinitionLimits
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        price_monthly_cents = self.price_monthly_cents

        limits = self.limits.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "price_monthly_cents": price_monthly_cents,
                "limits": limits,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.plan_definition_limits import PlanDefinitionLimits

        d = dict(src_dict)
        price_monthly_cents = d.pop("price_monthly_cents")

        limits = PlanDefinitionLimits.from_dict(d.pop("limits"))

        plan_definition = cls(
            price_monthly_cents=price_monthly_cents,
            limits=limits,
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
