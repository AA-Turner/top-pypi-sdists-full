from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="TopQueue")


@_attrs_define
class TopQueue:
    """
    Attributes:
        vhost (str): Virtual host name
        name (str): Queue name
        messages (int): Number of messages in queue
        consumers (int): Number of consumers attached
    """

    vhost: str
    name: str
    messages: int
    consumers: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        vhost = self.vhost

        name = self.name

        messages = self.messages

        consumers = self.consumers

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "vhost": vhost,
                "name": name,
                "messages": messages,
                "consumers": consumers,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        vhost = d.pop("vhost")

        name = d.pop("name")

        messages = d.pop("messages")

        consumers = d.pop("consumers")

        top_queue = cls(
            vhost=vhost,
            name=name,
            messages=messages,
            consumers=consumers,
        )

        top_queue.additional_properties = d
        return top_queue

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
