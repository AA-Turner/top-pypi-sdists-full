from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..models.fresh_provider_value_freshness import FreshProviderValueFreshness

T = TypeVar("T", bound="FreshProviderValue")


@_attrs_define
class FreshProviderValue:
    """
    Attributes:
        freshness (FreshProviderValueFreshness):
        amount_minor (int):
        as_of_unix_seconds (int):
    """

    freshness: FreshProviderValueFreshness
    amount_minor: int
    as_of_unix_seconds: int

    def to_dict(self) -> dict[str, Any]:
        freshness = self.freshness.value

        amount_minor = self.amount_minor

        as_of_unix_seconds = self.as_of_unix_seconds

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "freshness": freshness,
                "amount_minor": amount_minor,
                "as_of_unix_seconds": as_of_unix_seconds,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        freshness = FreshProviderValueFreshness(d.pop("freshness"))

        amount_minor = d.pop("amount_minor")

        as_of_unix_seconds = d.pop("as_of_unix_seconds")

        fresh_provider_value = cls(
            freshness=freshness,
            amount_minor=amount_minor,
            as_of_unix_seconds=as_of_unix_seconds,
        )

        return fresh_provider_value
