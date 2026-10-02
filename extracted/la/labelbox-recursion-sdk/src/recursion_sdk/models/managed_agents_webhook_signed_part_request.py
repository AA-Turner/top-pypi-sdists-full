from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_webhook_signed_part_request_kind import ManagedAgentsWebhookSignedPartRequestKind
from ..types import UNSET, Unset






T = TypeVar("T", bound="ManagedAgentsWebhookSignedPartRequest")



@_attrs_define
class ManagedAgentsWebhookSignedPartRequest:
    """ One ordered input included in the byte sequence verified by an HMAC webhook signature.

        Example:
            {'kind': 'body', 'value': 'example'}

        Attributes:
            kind (ManagedAgentsWebhookSignedPartRequestKind | Unset): Input source: the raw body, one header value, or a
                fixed literal string.
            value (str | Unset): Header name for header parts or fixed text for literal parts; omitted for the raw body.
     """

    kind: ManagedAgentsWebhookSignedPartRequestKind | Unset = UNSET
    value: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        kind: str | Unset = UNSET
        if not isinstance(self.kind, Unset):
            kind = self.kind.value


        value = self.value


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if kind is not UNSET:
            field_dict["kind"] = kind
        if value is not UNSET:
            field_dict["value"] = value

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _kind = d.pop("kind", UNSET)
        kind: ManagedAgentsWebhookSignedPartRequestKind | Unset
        if isinstance(_kind,  Unset):
            kind = UNSET
        else:
            kind = ManagedAgentsWebhookSignedPartRequestKind(_kind)




        value = d.pop("value", UNSET)

        managed_agents_webhook_signed_part_request = cls(
            kind=kind,
            value=value,
        )


        managed_agents_webhook_signed_part_request.additional_properties = d
        return managed_agents_webhook_signed_part_request

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
