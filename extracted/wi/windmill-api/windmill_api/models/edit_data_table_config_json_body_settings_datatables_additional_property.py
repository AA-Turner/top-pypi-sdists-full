from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.edit_data_table_config_json_body_settings_datatables_additional_property_database import (
        EditDataTableConfigJsonBodySettingsDatatablesAdditionalPropertyDatabase,
    )


T = TypeVar("T", bound="EditDataTableConfigJsonBodySettingsDatatablesAdditionalProperty")


@_attrs_define
class EditDataTableConfigJsonBodySettingsDatatablesAdditionalProperty:
    """
    Attributes:
        database (EditDataTableConfigJsonBodySettingsDatatablesAdditionalPropertyDatabase):
    """

    database: "EditDataTableConfigJsonBodySettingsDatatablesAdditionalPropertyDatabase"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        database = self.database.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "database": database,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.edit_data_table_config_json_body_settings_datatables_additional_property_database import (
            EditDataTableConfigJsonBodySettingsDatatablesAdditionalPropertyDatabase,
        )

        d = src_dict.copy()
        database = EditDataTableConfigJsonBodySettingsDatatablesAdditionalPropertyDatabase.from_dict(d.pop("database"))

        edit_data_table_config_json_body_settings_datatables_additional_property = cls(
            database=database,
        )

        edit_data_table_config_json_body_settings_datatables_additional_property.additional_properties = d
        return edit_data_table_config_json_body_settings_datatables_additional_property

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
