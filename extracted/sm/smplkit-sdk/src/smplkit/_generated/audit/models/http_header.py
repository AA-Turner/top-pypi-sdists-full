from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field


T = TypeVar("T", bound="HttpHeader")


@_attrs_define
class HttpHeader:
    """A single HTTP header attached to a forwarder delivery request.

    Header values are encrypted at the application layer before
    persistence regardless of header name; the wire representation here
    is always plaintext on both the request and the response, so a
    `GET → mutate → PUT` round-trip preserves header values without
    requiring the customer to re-enter secrets.

        Attributes:
            name (str): Header name.
            value (str): Header value. Stored encrypted at rest; returned as plaintext on `GET`.
    """

    name: str
    value: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        value = self.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "value": value,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        value = d.pop("value")

        http_header = cls(
            name=name,
            value=value,
        )

        http_header.additional_properties = d
        return http_header

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
