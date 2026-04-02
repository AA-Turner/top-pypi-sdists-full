from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="TableSize")


@_attrs_define
class TableSize:
    """
    Attributes:
        table_name (str): Name of the database table
        total_size (int): Total size of the table in bytes
        data_size (int): Size of the actual data in bytes
        external_size (int): Size of external data (e.g., TOAST) in bytes
    """

    table_name: str
    total_size: int
    data_size: int
    external_size: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        table_name = self.table_name

        total_size = self.total_size

        data_size = self.data_size

        external_size = self.external_size

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "table_name": table_name,
                "total_size": total_size,
                "data_size": data_size,
                "external_size": external_size,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        table_name = d.pop("table_name")

        total_size = d.pop("total_size")

        data_size = d.pop("data_size")

        external_size = d.pop("external_size")

        table_size = cls(
            table_name=table_name,
            total_size=total_size,
            data_size=data_size,
            external_size=external_size,
        )

        table_size.additional_properties = d
        return table_size

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
