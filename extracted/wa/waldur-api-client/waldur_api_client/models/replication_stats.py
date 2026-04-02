from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ReplicationStats")


@_attrs_define
class ReplicationStats:
    """
    Attributes:
        is_replica (bool): Whether this database is a replica
        wal_bytes (Union[None, int]): Write-ahead log size in bytes
        replication_lag_bytes (Union[None, int]): Replication lag in bytes (only for replicas)
    """

    is_replica: bool
    wal_bytes: Union[None, int]
    replication_lag_bytes: Union[None, int]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        is_replica = self.is_replica

        wal_bytes: Union[None, int]
        wal_bytes = self.wal_bytes

        replication_lag_bytes: Union[None, int]
        replication_lag_bytes = self.replication_lag_bytes

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "is_replica": is_replica,
                "wal_bytes": wal_bytes,
                "replication_lag_bytes": replication_lag_bytes,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        is_replica = d.pop("is_replica")

        def _parse_wal_bytes(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        wal_bytes = _parse_wal_bytes(d.pop("wal_bytes"))

        def _parse_replication_lag_bytes(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        replication_lag_bytes = _parse_replication_lag_bytes(d.pop("replication_lag_bytes"))

        replication_stats = cls(
            is_replica=is_replica,
            wal_bytes=wal_bytes,
            replication_lag_bytes=replication_lag_bytes,
        )

        replication_stats.additional_properties = d
        return replication_stats

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
