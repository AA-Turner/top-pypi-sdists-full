from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="RmqObjectTotals")


@_attrs_define
class RmqObjectTotals:
    """
    Attributes:
        connections (int): Total active connections
        channels (int): Total active channels
        exchanges (int): Total exchanges
        queues (int): Total queues
        consumers (int): Total active consumers
    """

    connections: int
    channels: int
    exchanges: int
    queues: int
    consumers: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        connections = self.connections

        channels = self.channels

        exchanges = self.exchanges

        queues = self.queues

        consumers = self.consumers

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "connections": connections,
                "channels": channels,
                "exchanges": exchanges,
                "queues": queues,
                "consumers": consumers,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        connections = d.pop("connections")

        channels = d.pop("channels")

        exchanges = d.pop("exchanges")

        queues = d.pop("queues")

        consumers = d.pop("consumers")

        rmq_object_totals = cls(
            connections=connections,
            channels=channels,
            exchanges=exchanges,
            queues=queues,
            consumers=consumers,
        )

        rmq_object_totals.additional_properties = d
        return rmq_object_totals

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
