from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateSecretRequest")


@_attrs_define
class CreateSecretRequest:
    """Secret creation request.

    Attributes:
        name (str): Secret display name.
        value (str): Secret value.
        cache_ttl_secs (int | Unset): Worker-side cache TTL in seconds. Default: 0.
    """

    name: str
    value: str
    cache_ttl_secs: int | Unset = 0

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        value = self.value

        cache_ttl_secs = self.cache_ttl_secs

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "name": name,
                "value": value,
            }
        )
        if cache_ttl_secs is not UNSET:
            field_dict["cache_ttl_secs"] = cache_ttl_secs

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        value = d.pop("value")

        cache_ttl_secs = d.pop("cache_ttl_secs", UNSET)

        create_secret_request = cls(
            name=name,
            value=value,
            cache_ttl_secs=cache_ttl_secs,
        )

        return create_secret_request
