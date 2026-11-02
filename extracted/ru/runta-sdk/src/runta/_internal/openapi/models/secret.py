from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="Secret")


@_attrs_define
class Secret:
    """Secret response object.

    Attributes:
        cache_ttl_secs (int): Worker-side cache TTL in seconds.
        display_name (str): User-chosen display name.
        id (str): Stable secret UUID.
        value_preview (str | Unset): Server-masked preview (first and last chars) of the value, for display only. Never
            the full value.
    """

    cache_ttl_secs: int
    display_name: str
    id: str
    value_preview: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        cache_ttl_secs = self.cache_ttl_secs

        display_name = self.display_name

        id = self.id

        value_preview = self.value_preview

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "cache_ttl_secs": cache_ttl_secs,
                "display_name": display_name,
                "id": id,
            }
        )
        if value_preview is not UNSET:
            field_dict["value_preview"] = value_preview

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        cache_ttl_secs = d.pop("cache_ttl_secs")

        display_name = d.pop("display_name")

        id = d.pop("id")

        value_preview = d.pop("value_preview", UNSET)

        secret = cls(
            cache_ttl_secs=cache_ttl_secs,
            display_name=display_name,
            id=id,
            value_preview=value_preview,
        )

        secret.additional_properties = d
        return secret

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
