from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from uuid import UUID


T = TypeVar("T", bound="SubscriptionItemResponse")


@_attrs_define
class SubscriptionItemResponse:
    """One product enrollment as exposed in subscription responses.

    Attributes:
        id (UUID): Unique identifier for this enrollment.
        product (str): Product key (e.g. `audit`, `config`, `flags`, `logging`).
        plan (str): Current plan for this product (e.g. `standard`, `pro`).
        price_monthly_cents (int): Monthly list price for this enrollment, in cents. This value is locked at the time
            the enrollment was created or last had its plan changed; subsequent changes to the public price list do not
            affect this enrollment until the customer themselves changes their plan.
        pending_plan_change (None | str | Unset): When a plan change is scheduled for the end of the current billing
            period, this is the plan that will take effect. Otherwise `null`. The value `free` indicates the enrollment will
            be dropped.
        scheduled_change_effective_at (None | str | Unset): ISO-8601 timestamp at which the pending plan change takes
            effect. Matches the subscription's `current_period_end`.
    """

    id: UUID
    product: str
    plan: str
    price_monthly_cents: int
    pending_plan_change: None | str | Unset = UNSET
    scheduled_change_effective_at: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        product = self.product

        plan = self.plan

        price_monthly_cents = self.price_monthly_cents

        pending_plan_change: None | str | Unset
        if isinstance(self.pending_plan_change, Unset):
            pending_plan_change = UNSET
        else:
            pending_plan_change = self.pending_plan_change

        scheduled_change_effective_at: None | str | Unset
        if isinstance(self.scheduled_change_effective_at, Unset):
            scheduled_change_effective_at = UNSET
        else:
            scheduled_change_effective_at = self.scheduled_change_effective_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "product": product,
                "plan": plan,
                "price_monthly_cents": price_monthly_cents,
            }
        )
        if pending_plan_change is not UNSET:
            field_dict["pending_plan_change"] = pending_plan_change
        if scheduled_change_effective_at is not UNSET:
            field_dict["scheduled_change_effective_at"] = scheduled_change_effective_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))

        product = d.pop("product")

        plan = d.pop("plan")

        price_monthly_cents = d.pop("price_monthly_cents")

        def _parse_pending_plan_change(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        pending_plan_change = _parse_pending_plan_change(d.pop("pending_plan_change", UNSET))

        def _parse_scheduled_change_effective_at(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        scheduled_change_effective_at = _parse_scheduled_change_effective_at(
            d.pop("scheduled_change_effective_at", UNSET)
        )

        subscription_item_response = cls(
            id=id,
            product=product,
            plan=plan,
            price_monthly_cents=price_monthly_cents,
            pending_plan_change=pending_plan_change,
            scheduled_change_effective_at=scheduled_change_effective_at,
        )

        subscription_item_response.additional_properties = d
        return subscription_item_response

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
