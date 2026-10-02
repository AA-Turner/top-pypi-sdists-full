from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_webhook_value_selector_source import ManagedAgentsWebhookValueSelectorSource
from ..types import UNSET, Unset






T = TypeVar("T", bound="ManagedAgentsWebhookValueSelector")



@_attrs_define
class ManagedAgentsWebhookValueSelector:
    """ Selects one value from a verified webhook delivery body or headers.

        Example:
            {'body_pointer': 'example', 'header': 'example', 'source': 'body'}

        Attributes:
            source (ManagedAgentsWebhookValueSelectorSource): Delivery location to read: body for a JSON pointer or header
                for a case-insensitive header name.
            body_pointer (str | Unset): RFC 6901 JSON pointer evaluated against the delivery body when source is body.
            header (str | Unset): HTTP header name read case-insensitively when source is header.
     """

    source: ManagedAgentsWebhookValueSelectorSource
    body_pointer: str | Unset = UNSET
    header: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        source = self.source.value

        body_pointer = self.body_pointer

        header = self.header


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "source": source,
        })
        if body_pointer is not UNSET:
            field_dict["body_pointer"] = body_pointer
        if header is not UNSET:
            field_dict["header"] = header

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        source = ManagedAgentsWebhookValueSelectorSource(d.pop("source"))




        body_pointer = d.pop("body_pointer", UNSET)

        header = d.pop("header", UNSET)

        managed_agents_webhook_value_selector = cls(
            source=source,
            body_pointer=body_pointer,
            header=header,
        )


        managed_agents_webhook_value_selector.additional_properties = d
        return managed_agents_webhook_value_selector

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
