from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_webhook_value_selector_request_source import ManagedAgentsWebhookValueSelectorRequestSource
from ..types import UNSET, Unset






T = TypeVar("T", bound="ManagedAgentsWebhookValueSelectorRequest")



@_attrs_define
class ManagedAgentsWebhookValueSelectorRequest:
    """ Selects one value from a verified webhook delivery body or headers.

        Example:
            {'body_pointer': 'example', 'header': 'example', 'source': 'body'}

        Attributes:
            body_pointer (str | Unset): RFC 6901 JSON pointer evaluated against the delivery body when source is body.
            header (str | Unset): HTTP header name read case-insensitively when source is header.
            source (ManagedAgentsWebhookValueSelectorRequestSource | Unset): Delivery location to read: body for a JSON
                pointer or header for a case-insensitive header name.
     """

    body_pointer: str | Unset = UNSET
    header: str | Unset = UNSET
    source: ManagedAgentsWebhookValueSelectorRequestSource | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        body_pointer = self.body_pointer

        header = self.header

        source: str | Unset = UNSET
        if not isinstance(self.source, Unset):
            source = self.source.value



        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if body_pointer is not UNSET:
            field_dict["body_pointer"] = body_pointer
        if header is not UNSET:
            field_dict["header"] = header
        if source is not UNSET:
            field_dict["source"] = source

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        body_pointer = d.pop("body_pointer", UNSET)

        header = d.pop("header", UNSET)

        _source = d.pop("source", UNSET)
        source: ManagedAgentsWebhookValueSelectorRequestSource | Unset
        if isinstance(_source,  Unset):
            source = UNSET
        else:
            source = ManagedAgentsWebhookValueSelectorRequestSource(_source)




        managed_agents_webhook_value_selector_request = cls(
            body_pointer=body_pointer,
            header=header,
            source=source,
        )


        managed_agents_webhook_value_selector_request.additional_properties = d
        return managed_agents_webhook_value_selector_request

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
