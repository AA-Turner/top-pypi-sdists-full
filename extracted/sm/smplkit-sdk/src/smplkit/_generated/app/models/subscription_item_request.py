from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define


T = TypeVar("T", bound="SubscriptionItemRequest")


@_attrs_define
class SubscriptionItemRequest:
    """One product enrollment as supplied by the caller.

    The caller supplies the *desired* (product, plan) pair for each product
    they want enrolled. Products absent from the request are interpreted as
    scheduled-for-drop at the end of the current billing period.

        Attributes:
            product (str): Product key (e.g. `audit`, `config`, `flags`, `logging`).
            plan (str): Target plan for this product. Must be a paid plan such as `standard` or `pro`; the free plan is
                implicit when a product is not listed.
    """

    product: str
    plan: str

    def to_dict(self) -> dict[str, Any]:
        product = self.product

        plan = self.plan

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "product": product,
                "plan": plan,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        product = d.pop("product")

        plan = d.pop("plan")

        subscription_item_request = cls(
            product=product,
            plan=plan,
        )

        return subscription_item_request
