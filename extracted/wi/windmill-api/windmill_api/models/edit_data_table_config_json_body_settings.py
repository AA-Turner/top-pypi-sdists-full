from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.edit_data_table_config_json_body_settings_datatables import (
        EditDataTableConfigJsonBodySettingsDatatables,
    )


T = TypeVar("T", bound="EditDataTableConfigJsonBodySettings")


@_attrs_define
class EditDataTableConfigJsonBodySettings:
    """
    Attributes:
        datatables (EditDataTableConfigJsonBodySettingsDatatables):
    """

    datatables: "EditDataTableConfigJsonBodySettingsDatatables"
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
        from ..models.edit_data_table_config_json_body_settings_datatables import (
            EditDataTableConfigJsonBodySettingsDatatables,
        )

        d = src_dict.copy()
        datatables = EditDataTableConfigJsonBodySettingsDatatables.from_dict(d.pop("datatables"))

        edit_data_table_config_json_body_settings = cls(
            datatables=datatables,
        )

        edit_data_table_config_json_body_settings.additional_properties = d
        return edit_data_table_config_json_body_settings

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
