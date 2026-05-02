from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.data_table_settings_datatables import DataTableSettingsDatatables


T = TypeVar("T", bound="DataTableSettings")


@_attrs_define
class DataTableSettings:
    """
    Attributes:
        datatables (DataTableSettingsDatatables):
    """

    datatables: "DataTableSettingsDatatables"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        datatables = self.datatables.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "datatables": datatables,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.data_table_settings_datatables import DataTableSettingsDatatables

        d = src_dict.copy()
        datatables = DataTableSettingsDatatables.from_dict(d.pop("datatables"))

        data_table_settings = cls(
            datatables=datatables,
        )

        data_table_settings.additional_properties = d
        return data_table_settings

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
