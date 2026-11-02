from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="SetSecretRequest")


@_attrs_define
class SetSecretRequest:
    """Secret set request.

    Attributes:
        value (str): Secret value.
        cache_ttl_secs (int | Unset): Worker-side cache TTL in seconds. Default: 0.
    """

    value: str
    cache_ttl_secs: int | Unset = 0
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        value = self.value

        cache_ttl_secs = self.cache_ttl_secs

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "value": value,
            }
        )
        if cache_ttl_secs is not UNSET:
            field_dict["cache_ttl_secs"] = cache_ttl_secs

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        value = d.pop("value")

        cache_ttl_secs = d.pop("cache_ttl_secs", UNSET)

        set_secret_request = cls(
            value=value,
            cache_ttl_secs=cache_ttl_secs,
        )

        set_secret_request.additional_properties = d
        return set_secret_request

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
