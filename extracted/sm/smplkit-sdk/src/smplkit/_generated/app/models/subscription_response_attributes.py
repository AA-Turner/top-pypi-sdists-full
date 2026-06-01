from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.subscription_response_attributes_discount_source import (
    check_subscription_response_attributes_discount_source,
)
from ..models.subscription_response_attributes_discount_source import SubscriptionResponseAttributesDiscountSource
from typing import cast
from uuid import UUID

if TYPE_CHECKING:
    from ..models.next_tier_response import NextTierResponse
    from ..models.subscription_item_response import SubscriptionItemResponse


T = TypeVar("T", bound="SubscriptionResponseAttributes")


@_attrs_define
class SubscriptionResponseAttributes:
    """Customer's subscription as returned by the API.

    Attributes:
        discount_pct (int): Effective discount percentage applied to the subscription's monthly invoice. This is the
            value locked at the time of the customer's last subscription change; subsequent changes to the public discount
            schedule do not affect this customer until they themselves change their subscription.
        discount_source (SubscriptionResponseAttributesDiscountSource): `VOLUME` when the discount comes from the multi-
            product discount schedule; `OVERRIDE` when an administrator has applied a custom discount.
        subtotal_cents (int): Sum of all item list prices in cents, before discount.
        discount_amount_cents (int): Amount discounted from the subtotal in cents.
        total_cents (int): Final monthly total in cents after the discount is applied.
        items (list[SubscriptionItemResponse]): One entry per product currently enrolled on the subscription.
        status (None | str | Unset): Lifecycle state of the subscription. `ACTIVE` while billing is current; `PAST_DUE`
            after a failed charge; `CANCELED` once the subscription has ended; `null` when the subscription is fully
            discounted (`discount_override_pct` of 100) and has no billing-provider object.
        current_period_start (None | str | Unset): ISO-8601 timestamp of the current billing period's start.
        current_period_end (None | str | Unset): ISO-8601 timestamp of the current billing period's end. Scheduled plan
            changes take effect at this moment.
        next_tier (NextTierResponse | Unset): Hint describing how the customer could unlock a better discount.
        payment_method (None | Unset | UUID): Identifier of the default payment method used to bill this subscription.
            `null` when the subscription has no associated payment method (e.g. fully discounted via `discount_override_pct`
            of 100).
    """

    discount_pct: int
    discount_source: SubscriptionResponseAttributesDiscountSource
    subtotal_cents: int
    discount_amount_cents: int
    total_cents: int
    items: list[SubscriptionItemResponse]
    status: None | str | Unset = UNSET
    current_period_start: None | str | Unset = UNSET
    current_period_end: None | str | Unset = UNSET
    next_tier: NextTierResponse | Unset = UNSET
    payment_method: None | Unset | UUID = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        discount_pct = self.discount_pct

        discount_source: str = self.discount_source

        subtotal_cents = self.subtotal_cents

        discount_amount_cents = self.discount_amount_cents

        total_cents = self.total_cents

        items = []
        for items_item_data in self.items:
            items_item = items_item_data.to_dict()
            items.append(items_item)

        status: None | str | Unset
        if isinstance(self.status, Unset):
            status = UNSET
        else:
            status = self.status

        current_period_start: None | str | Unset
        if isinstance(self.current_period_start, Unset):
            current_period_start = UNSET
        else:
            current_period_start = self.current_period_start

        current_period_end: None | str | Unset
        if isinstance(self.current_period_end, Unset):
            current_period_end = UNSET
        else:
            current_period_end = self.current_period_end

        next_tier: dict[str, Any] | Unset = UNSET
        if not isinstance(self.next_tier, Unset):
            next_tier = self.next_tier.to_dict()

        payment_method: None | str | Unset
        if isinstance(self.payment_method, Unset):
            payment_method = UNSET
        elif isinstance(self.payment_method, UUID):
            payment_method = str(self.payment_method)
        else:
            payment_method = self.payment_method

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "discount_pct": discount_pct,
                "discount_source": discount_source,
                "subtotal_cents": subtotal_cents,
                "discount_amount_cents": discount_amount_cents,
                "total_cents": total_cents,
                "items": items,
            }
        )
        if status is not UNSET:
            field_dict["status"] = status
        if current_period_start is not UNSET:
            field_dict["current_period_start"] = current_period_start
        if current_period_end is not UNSET:
            field_dict["current_period_end"] = current_period_end
        if next_tier is not UNSET:
            field_dict["next_tier"] = next_tier
        if payment_method is not UNSET:
            field_dict["payment_method"] = payment_method

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.next_tier_response import NextTierResponse
        from ..models.subscription_item_response import SubscriptionItemResponse

        d = dict(src_dict)
        discount_pct = d.pop("discount_pct")

        discount_source = check_subscription_response_attributes_discount_source(d.pop("discount_source"))

        subtotal_cents = d.pop("subtotal_cents")

        discount_amount_cents = d.pop("discount_amount_cents")

        total_cents = d.pop("total_cents")

        items = []
        _items = d.pop("items")
        for items_item_data in _items:
            items_item = SubscriptionItemResponse.from_dict(items_item_data)

            items.append(items_item)

        def _parse_status(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        status = _parse_status(d.pop("status", UNSET))

        def _parse_current_period_start(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        current_period_start = _parse_current_period_start(d.pop("current_period_start", UNSET))

        def _parse_current_period_end(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        current_period_end = _parse_current_period_end(d.pop("current_period_end", UNSET))

        _next_tier = d.pop("next_tier", UNSET)
        next_tier: NextTierResponse | Unset
        if isinstance(_next_tier, Unset):
            next_tier = UNSET
        else:
            next_tier = NextTierResponse.from_dict(_next_tier)

        def _parse_payment_method(data: object) -> None | Unset | UUID:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                payment_method_type_0 = UUID(data)

                return payment_method_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UUID, data)

        payment_method = _parse_payment_method(d.pop("payment_method", UNSET))

        subscription_response_attributes = cls(
            discount_pct=discount_pct,
            discount_source=discount_source,
            subtotal_cents=subtotal_cents,
            discount_amount_cents=discount_amount_cents,
            total_cents=total_cents,
            items=items,
            status=status,
            current_period_start=current_period_start,
            current_period_end=current_period_end,
            next_tier=next_tier,
            payment_method=payment_method,
        )

        subscription_response_attributes.additional_properties = d
        return subscription_response_attributes

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
