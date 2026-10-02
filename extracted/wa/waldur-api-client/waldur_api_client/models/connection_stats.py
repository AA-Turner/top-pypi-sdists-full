from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ConnectionStats")


@_attrs_define
class ConnectionStats:
    """
    Attributes:
        active (int): Number of active connections
        idle (int): Number of idle connections
        idle_in_transaction (int): Number of connections idle in transaction
        waiting (int): Number of connections waiting for a lock
        max_connections (int): Maximum allowed connections
        utilization_percent (float): Percentage of max connections in use
    """

    active: int
    idle: int
    idle_in_transaction: int
    waiting: int
    max_connections: int
    utilization_percent: float
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        active = self.active

        idle = self.idle

        idle_in_transaction = self.idle_in_transaction

        waiting = self.waiting

        max_connections = self.max_connections

        utilization_percent = self.utilization_percent

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "active": active,
                "idle": idle,
                "idle_in_transaction": idle_in_transaction,
                "waiting": waiting,
                "max_connections": max_connections,
                "utilization_percent": utilization_percent,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        active = d.pop("active")

        idle = d.pop("idle")

        idle_in_transaction = d.pop("idle_in_transaction")

        waiting = d.pop("waiting")

        max_connections = d.pop("max_connections")

        utilization_percent = d.pop("utilization_percent")

        connection_stats = cls(
            active=active,
            idle=idle,
            idle_in_transaction=idle_in_transaction,
            waiting=waiting,
            max_connections=max_connections,
            utilization_percent=utilization_percent,
        )

        connection_stats.additional_properties = d
        return connection_stats

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
