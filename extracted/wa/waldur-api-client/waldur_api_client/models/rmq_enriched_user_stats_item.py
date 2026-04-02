from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.rmq_enriched_connection import RmqEnrichedConnection


T = TypeVar("T", bound="RmqEnrichedUserStatsItem")


@_attrs_define
class RmqEnrichedUserStatsItem:
    """
    Attributes:
        username (str): RabbitMQ username (corresponds to EventSubscription UUID)
        connections (list['RmqEnrichedConnection']): List of active connections with detailed statistics
    """

    username: str
    connections: list["RmqEnrichedConnection"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        username = self.username

        connections = []
        for connections_item_data in self.connections:
            connections_item = connections_item_data.to_dict()
            connections.append(connections_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "username": username,
                "connections": connections,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.rmq_enriched_connection import RmqEnrichedConnection

        d = dict(src_dict)
        username = d.pop("username")

        connections = []
        _connections = d.pop("connections")
        for connections_item_data in _connections:
            connections_item = RmqEnrichedConnection.from_dict(connections_item_data)

            connections.append(connections_item)

        rmq_enriched_user_stats_item = cls(
            username=username,
            connections=connections,
        )

        rmq_enriched_user_stats_item.additional_properties = d
        return rmq_enriched_user_stats_item

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
