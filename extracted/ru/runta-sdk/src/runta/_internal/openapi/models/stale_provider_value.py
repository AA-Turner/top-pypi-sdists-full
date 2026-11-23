from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..models.stale_provider_value_freshness import StaleProviderValueFreshness

T = TypeVar("T", bound="StaleProviderValue")


@_attrs_define
class StaleProviderValue:
    """
    Attributes:
        freshness (StaleProviderValueFreshness):
        amount_minor (int):
        as_of_unix_seconds (int):
        error_code (str):
    """

    freshness: StaleProviderValueFreshness
    amount_minor: int
    as_of_unix_seconds: int
    error_code: str

    def to_dict(self) -> dict[str, Any]:
        freshness = self.freshness.value

        amount_minor = self.amount_minor

        as_of_unix_seconds = self.as_of_unix_seconds

        error_code = self.error_code

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "freshness": freshness,
                "amount_minor": amount_minor,
                "as_of_unix_seconds": as_of_unix_seconds,
                "error_code": error_code,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        freshness = StaleProviderValueFreshness(d.pop("freshness"))

        amount_minor = d.pop("amount_minor")

        as_of_unix_seconds = d.pop("as_of_unix_seconds")

        error_code = d.pop("error_code")

        stale_provider_value = cls(
            freshness=freshness,
            amount_minor=amount_minor,
            as_of_unix_seconds=as_of_unix_seconds,
            error_code=error_code,
        )

        return stale_provider_value
