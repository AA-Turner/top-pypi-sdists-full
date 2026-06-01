from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from uuid import UUID

if TYPE_CHECKING:
    from ..models.subscription_item_request import SubscriptionItemRequest


T = TypeVar("T", bound="AdminSubscriptionRequestAttributes")


@_attrs_define
class AdminSubscriptionRequestAttributes:
    """Same as the customer request body plus the admin-only override field.

    Attributes:
        items (list[SubscriptionItemRequest]): Desired enrollments. Products listed are scheduled to be on the specified
            plan immediately (for upgrades and new enrollments) or at the end of the current billing period (for
            downgrades). Products not listed are scheduled to be dropped at the end of the current billing period.
        payment_method (None | Unset | UUID): Optional identifier of the payment method to bill against. If omitted, the
            account's default payment method is used.
        discount_override_pct (int | None | Unset): Administrator-set discount percentage (0–100). When set, the multi-
            product discount schedule is bypassed and this value is used directly. Setting `100` skips the billing provider
            entirely — the customer pays nothing. Pass `null` to clear any existing override and revert to the multi-product
            discount schedule.
    """

    items: list[SubscriptionItemRequest]
    payment_method: None | Unset | UUID = UNSET
    discount_override_pct: int | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        items = []
        for items_item_data in self.items:
            items_item = items_item_data.to_dict()
            items.append(items_item)

        payment_method: None | str | Unset
        if isinstance(self.payment_method, Unset):
            payment_method = UNSET
        elif isinstance(self.payment_method, UUID):
            payment_method = str(self.payment_method)
        else:
            payment_method = self.payment_method

        discount_override_pct: int | None | Unset
        if isinstance(self.discount_override_pct, Unset):
            discount_override_pct = UNSET
        else:
            discount_override_pct = self.discount_override_pct

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "items": items,
            }
        )
        if payment_method is not UNSET:
            field_dict["payment_method"] = payment_method
        if discount_override_pct is not UNSET:
            field_dict["discount_override_pct"] = discount_override_pct

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.subscription_item_request import SubscriptionItemRequest

        d = dict(src_dict)
        items = []
        _items = d.pop("items")
        for items_item_data in _items:
            items_item = SubscriptionItemRequest.from_dict(items_item_data)

            items.append(items_item)

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

        def _parse_discount_override_pct(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        discount_override_pct = _parse_discount_override_pct(d.pop("discount_override_pct", UNSET))

        admin_subscription_request_attributes = cls(
            items=items,
            payment_method=payment_method,
            discount_override_pct=discount_override_pct,
        )

        admin_subscription_request_attributes.additional_properties = d
        return admin_subscription_request_attributes

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
