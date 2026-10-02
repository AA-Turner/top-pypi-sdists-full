from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="DatabaseSizeStats")


@_attrs_define
class DatabaseSizeStats:
    """
    Attributes:
        database_name (str): Name of the database
        total_size_bytes (int): Total database size in bytes
        data_size_bytes (int): Size of data excluding indexes in bytes
        index_size_bytes (int): Total size of all indexes in bytes
    """

    database_name: str
    total_size_bytes: int
    data_size_bytes: int
    index_size_bytes: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        database_name = self.database_name

        total_size_bytes = self.total_size_bytes

        data_size_bytes = self.data_size_bytes

        index_size_bytes = self.index_size_bytes

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "database_name": database_name,
                "total_size_bytes": total_size_bytes,
                "data_size_bytes": data_size_bytes,
                "index_size_bytes": index_size_bytes,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        database_name = d.pop("database_name")

        total_size_bytes = d.pop("total_size_bytes")

        data_size_bytes = d.pop("data_size_bytes")

        index_size_bytes = d.pop("index_size_bytes")

        database_size_stats = cls(
            database_name=database_name,
            total_size_bytes=total_size_bytes,
            data_size_bytes=data_size_bytes,
            index_size_bytes=index_size_bytes,
        )

        database_size_stats.additional_properties = d
        return database_size_stats

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
