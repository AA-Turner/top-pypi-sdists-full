from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.subscription_preview_attributes_projected_discount_source import (
    check_subscription_preview_attributes_projected_discount_source,
)
from ..models.subscription_preview_attributes_projected_discount_source import (
    SubscriptionPreviewAttributesProjectedDiscountSource,
)

if TYPE_CHECKING:
    from ..models.next_tier_response import NextTierResponse
    from ..models.subscription_change_projection import SubscriptionChangeProjection


T = TypeVar("T", bound="SubscriptionPreviewAttributes")


@_attrs_define
class SubscriptionPreviewAttributes:
    """Projected totals and per-change breakdown for a hypothetical change.

    Attributes:
        projected_subtotal_cents (int): Projected sum of item monthly list prices after the change.
        projected_discount_pct (int): Projected discount percentage that will apply after the change.
        projected_discount_source (SubscriptionPreviewAttributesProjectedDiscountSource): `VOLUME` when the projected
            discount comes from the multi-product schedule; `OVERRIDE` when an administrator's discount applies.
        projected_discount_amount_cents (int): Projected discount amount in cents after the change.
        projected_total_cents (int): Projected final monthly total in cents after the change.
        changes (list[SubscriptionChangeProjection]): Per-product breakdown of changes the desired state would produce.
            Products that would remain unchanged are omitted.
        total_charge_today_cents (int): Total amount that would be charged at confirmation time, in cents. The sum of
            `prorated_charge_today_cents` across `IMMEDIATE` changes.
        next_invoice_total_cents (int): Projected total of the next monthly invoice in cents, after all scheduled
            changes have taken effect.
        projected_next_tier (NextTierResponse | Unset): Hint describing how the customer could unlock a better discount.
    """

    projected_subtotal_cents: int
    projected_discount_pct: int
    projected_discount_source: SubscriptionPreviewAttributesProjectedDiscountSource
    projected_discount_amount_cents: int
    projected_total_cents: int
    changes: list[SubscriptionChangeProjection]
    total_charge_today_cents: int
    next_invoice_total_cents: int
    projected_next_tier: NextTierResponse | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        projected_subtotal_cents = self.projected_subtotal_cents

        projected_discount_pct = self.projected_discount_pct

        projected_discount_source: str = self.projected_discount_source

        projected_discount_amount_cents = self.projected_discount_amount_cents

        projected_total_cents = self.projected_total_cents

        changes = []
        for changes_item_data in self.changes:
            changes_item = changes_item_data.to_dict()
            changes.append(changes_item)

        total_charge_today_cents = self.total_charge_today_cents

        next_invoice_total_cents = self.next_invoice_total_cents

        projected_next_tier: dict[str, Any] | Unset = UNSET
        if not isinstance(self.projected_next_tier, Unset):
            projected_next_tier = self.projected_next_tier.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "projected_subtotal_cents": projected_subtotal_cents,
                "projected_discount_pct": projected_discount_pct,
                "projected_discount_source": projected_discount_source,
                "projected_discount_amount_cents": projected_discount_amount_cents,
                "projected_total_cents": projected_total_cents,
                "changes": changes,
                "total_charge_today_cents": total_charge_today_cents,
                "next_invoice_total_cents": next_invoice_total_cents,
            }
        )
        if projected_next_tier is not UNSET:
            field_dict["projected_next_tier"] = projected_next_tier

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.next_tier_response import NextTierResponse
        from ..models.subscription_change_projection import SubscriptionChangeProjection

        d = dict(src_dict)
        projected_subtotal_cents = d.pop("projected_subtotal_cents")

        projected_discount_pct = d.pop("projected_discount_pct")

        projected_discount_source = check_subscription_preview_attributes_projected_discount_source(
            d.pop("projected_discount_source")
        )

        projected_discount_amount_cents = d.pop("projected_discount_amount_cents")

        projected_total_cents = d.pop("projected_total_cents")

        changes = []
        _changes = d.pop("changes")
        for changes_item_data in _changes:
            changes_item = SubscriptionChangeProjection.from_dict(changes_item_data)

            changes.append(changes_item)

        total_charge_today_cents = d.pop("total_charge_today_cents")

        next_invoice_total_cents = d.pop("next_invoice_total_cents")

        _projected_next_tier = d.pop("projected_next_tier", UNSET)
        projected_next_tier: NextTierResponse | Unset
        if isinstance(_projected_next_tier, Unset):
            projected_next_tier = UNSET
        else:
            projected_next_tier = NextTierResponse.from_dict(_projected_next_tier)

        subscription_preview_attributes = cls(
            projected_subtotal_cents=projected_subtotal_cents,
            projected_discount_pct=projected_discount_pct,
            projected_discount_source=projected_discount_source,
            projected_discount_amount_cents=projected_discount_amount_cents,
            projected_total_cents=projected_total_cents,
            changes=changes,
            total_charge_today_cents=total_charge_today_cents,
            next_invoice_total_cents=next_invoice_total_cents,
            projected_next_tier=projected_next_tier,
        )

        subscription_preview_attributes.additional_properties = d
        return subscription_preview_attributes

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
