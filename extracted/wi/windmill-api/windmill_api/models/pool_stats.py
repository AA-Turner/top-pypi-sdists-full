from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="PoolStats")


@_attrs_define
class PoolStats:
    """Database connection pool statistics

    Attributes:
        size (int): Current number of connections in the pool
        idle (int): Number of idle connections
        max_connections (int): Maximum number of connections allowed
    """

    size: int
    idle: int
    max_connections: int
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        size = self.size
        idle = self.idle
        max_connections = self.max_connections

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "size": size,
                "idle": idle,
                "max_connections": max_connections,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        size = d.pop("size")

        idle = d.pop("idle")

        max_connections = d.pop("max_connections")

        pool_stats = cls(
            size=size,
            idle=idle,
            max_connections=max_connections,
        )

        pool_stats.additional_properties = d
        return pool_stats

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
