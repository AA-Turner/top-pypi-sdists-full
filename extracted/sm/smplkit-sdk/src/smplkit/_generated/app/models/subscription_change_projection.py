from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.subscription_change_projection_effect import check_subscription_change_projection_effect
from ..models.subscription_change_projection_effect import SubscriptionChangeProjectionEffect
from typing import cast


T = TypeVar("T", bound="SubscriptionChangeProjection")


@_attrs_define
class SubscriptionChangeProjection:
    """Per-item projected effect of a subscription change.

    Attributes:
        product (str): Product key affected by this change.
        from_plan (str): Current plan for this product, or `free` if it is being added.
        to_plan (str): Plan the product will be on after the change. `free` indicates the enrollment will be dropped.
        monthly_cents (int): Monthly cost in cents of this enrollment after the change. `0` when the enrollment will be
            dropped.
        effect (SubscriptionChangeProjectionEffect): `IMMEDIATE` when the change takes effect at confirmation time (and
            a prorated charge may apply today). `NEXT_PERIOD` when the change takes effect at the end of the current billing
            period.
        prorated_charge_today_cents (int | Unset): When `effect` is `IMMEDIATE`, the estimated prorated charge for the
            remainder of the current billing period in cents. Always `0` when `effect` is `NEXT_PERIOD`. Default: 0.
        starts_at (None | str | Unset): When `effect` is `NEXT_PERIOD`, the ISO-8601 timestamp at which the change takes
            effect. `null` when `effect` is `IMMEDIATE` (the change applies on confirmation).
    """

    product: str
    from_plan: str
    to_plan: str
    monthly_cents: int
    effect: SubscriptionChangeProjectionEffect
    prorated_charge_today_cents: int | Unset = 0
    starts_at: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        product = self.product

        from_plan = self.from_plan

        to_plan = self.to_plan

        monthly_cents = self.monthly_cents

        effect: str = self.effect

        prorated_charge_today_cents = self.prorated_charge_today_cents

        starts_at: None | str | Unset
        if isinstance(self.starts_at, Unset):
            starts_at = UNSET
        else:
            starts_at = self.starts_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "product": product,
                "from_plan": from_plan,
                "to_plan": to_plan,
                "monthly_cents": monthly_cents,
                "effect": effect,
            }
        )
        if prorated_charge_today_cents is not UNSET:
            field_dict["prorated_charge_today_cents"] = prorated_charge_today_cents
        if starts_at is not UNSET:
            field_dict["starts_at"] = starts_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        product = d.pop("product")

        from_plan = d.pop("from_plan")

        to_plan = d.pop("to_plan")

        monthly_cents = d.pop("monthly_cents")

        effect = check_subscription_change_projection_effect(d.pop("effect"))

        prorated_charge_today_cents = d.pop("prorated_charge_today_cents", UNSET)

        def _parse_starts_at(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        starts_at = _parse_starts_at(d.pop("starts_at", UNSET))

        subscription_change_projection = cls(
            product=product,
            from_plan=from_plan,
            to_plan=to_plan,
            monthly_cents=monthly_cents,
            effect=effect,
            prorated_charge_today_cents=prorated_charge_today_cents,
            starts_at=starts_at,
        )

        subscription_change_projection.additional_properties = d
        return subscription_change_projection

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
