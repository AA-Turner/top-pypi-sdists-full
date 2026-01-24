from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.edit_data_table_config_json_body_settings_datatables_additional_property import (
        EditDataTableConfigJsonBodySettingsDatatablesAdditionalProperty,
    )


T = TypeVar("T", bound="EditDataTableConfigJsonBodySettingsDatatables")


@_attrs_define
class EditDataTableConfigJsonBodySettingsDatatables:
    """ """

    additional_properties: Dict[str, "EditDataTableConfigJsonBodySettingsDatatablesAdditionalProperty"] = _attrs_field(
        init=False, factory=dict
    )

    def to_dict(self) -> Dict[str, Any]:
        pass

        field_dict: Dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = prop.to_dict()

        field_dict.update({})

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.edit_data_table_config_json_body_settings_datatables_additional_property import (
            EditDataTableConfigJsonBodySettingsDatatablesAdditionalProperty,
        )

        d = src_dict.copy()
        edit_data_table_config_json_body_settings_datatables = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = EditDataTableConfigJsonBodySettingsDatatablesAdditionalProperty.from_dict(prop_dict)

            additional_properties[prop_name] = additional_property

        edit_data_table_config_json_body_settings_datatables.additional_properties = additional_properties
        return edit_data_table_config_json_body_settings_datatables

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> "EditDataTableConfigJsonBodySettingsDatatablesAdditionalProperty":
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: "EditDataTableConfigJsonBodySettingsDatatablesAdditionalProperty") -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
