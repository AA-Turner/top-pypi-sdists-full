from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="DLQQueue")


@_attrs_define
class DLQQueue:
    """
    Attributes:
        vhost (str): Virtual host name
        queue_name (str): DLQ queue name
        messages (int): Total messages in DLQ
        messages_ready (int): Messages ready for delivery
        consumers (int): Number of consumers attached
    """

    vhost: str
    queue_name: str
    messages: int
    messages_ready: int
    consumers: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        vhost = self.vhost

        queue_name = self.queue_name

        messages = self.messages

        messages_ready = self.messages_ready

        consumers = self.consumers

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "vhost": vhost,
                "queue_name": queue_name,
                "messages": messages,
                "messages_ready": messages_ready,
                "consumers": consumers,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        vhost = d.pop("vhost")

        queue_name = d.pop("queue_name")

        messages = d.pop("messages")

        messages_ready = d.pop("messages_ready")

        consumers = d.pop("consumers")

        dlq_queue = cls(
            vhost=vhost,
            queue_name=queue_name,
            messages=messages,
            messages_ready=messages_ready,
            consumers=consumers,
        )

        dlq_queue.additional_properties = d
        return dlq_queue

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
