from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..models.unavailable_billing_usage_freshness import (
    UnavailableBillingUsageFreshness,
)

T = TypeVar("T", bound="UnavailableBillingUsage")


@_attrs_define
class UnavailableBillingUsage:
    """
    Attributes:
        freshness (UnavailableBillingUsageFreshness):
        error_code (str):
    """

    freshness: UnavailableBillingUsageFreshness
    error_code: str

    def to_dict(self) -> dict[str, Any]:
        freshness = self.freshness.value

        error_code = self.error_code

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "freshness": freshness,
                "error_code": error_code,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        freshness = UnavailableBillingUsageFreshness(d.pop("freshness"))

        error_code = d.pop("error_code")

        unavailable_billing_usage = cls(
            freshness=freshness,
            error_code=error_code,
        )

        return unavailable_billing_usage
