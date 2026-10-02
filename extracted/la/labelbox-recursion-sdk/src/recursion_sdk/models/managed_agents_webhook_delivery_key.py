from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_webhook_delivery_key_source import ManagedAgentsWebhookDeliveryKeySource
from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_webhook_value_selector import ManagedAgentsWebhookValueSelector





T = TypeVar("T", bound="ManagedAgentsWebhookDeliveryKey")



@_attrs_define
class ManagedAgentsWebhookDeliveryKey:
    """ Selects a stable provider delivery identity, optionally composed from multiple verified values.

        Example:
            {'body_pointer': 'example', 'header': 'example', 'selectors': [{'body_pointer': 'example', 'header': 'example',
                'source': 'body'}], 'source': 'body'}

        Attributes:
            body_pointer (str | Unset): RFC 6901 JSON pointer for a single-value body key.
            header (str | Unset): Case-insensitive header name for a single-value header key.
            selectors (list[ManagedAgentsWebhookValueSelector] | Unset): Ordered values canonically hashed into a collision-
                resistant composite delivery key.
            source (ManagedAgentsWebhookDeliveryKeySource | Unset): Delivery location for a single-value key; omit when
                selectors is used.
     """

    body_pointer: str | Unset = UNSET
    header: str | Unset = UNSET
    selectors: list[ManagedAgentsWebhookValueSelector] | Unset = UNSET
    source: ManagedAgentsWebhookDeliveryKeySource | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_webhook_value_selector import ManagedAgentsWebhookValueSelector # noqa: PLC0415
        body_pointer = self.body_pointer

        header = self.header

        selectors: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.selectors, Unset):
            selectors = []
            for selectors_item_data in self.selectors:
                selectors_item = selectors_item_data.to_dict()
                selectors.append(selectors_item)



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
        if selectors is not UNSET:
            field_dict["selectors"] = selectors
        if source is not UNSET:
            field_dict["source"] = source

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_webhook_value_selector import ManagedAgentsWebhookValueSelector # noqa: PLC0415
        d = dict(src_dict)
        body_pointer = d.pop("body_pointer", UNSET)

        header = d.pop("header", UNSET)

        _selectors = d.pop("selectors", UNSET)
        selectors: list[ManagedAgentsWebhookValueSelector] | Unset = UNSET
        if _selectors is not UNSET:
            selectors = []
            for selectors_item_data in _selectors:
                selectors_item = ManagedAgentsWebhookValueSelector.from_dict(selectors_item_data)



                selectors.append(selectors_item)


        _source = d.pop("source", UNSET)
        source: ManagedAgentsWebhookDeliveryKeySource | Unset
        if isinstance(_source,  Unset):
            source = UNSET
        else:
            source = ManagedAgentsWebhookDeliveryKeySource(_source)




        managed_agents_webhook_delivery_key = cls(
            body_pointer=body_pointer,
            header=header,
            selectors=selectors,
            source=source,
        )


        managed_agents_webhook_delivery_key.additional_properties = d
        return managed_agents_webhook_delivery_key

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
