from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.edit_data_table_config_json_body_settings_datatables_additional_property_database_resource_type import (
    EditDataTableConfigJsonBodySettingsDatatablesAdditionalPropertyDatabaseResourceType,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="EditDataTableConfigJsonBodySettingsDatatablesAdditionalPropertyDatabase")


@_attrs_define
class EditDataTableConfigJsonBodySettingsDatatablesAdditionalPropertyDatabase:
    """
    Attributes:
        resource_type (EditDataTableConfigJsonBodySettingsDatatablesAdditionalPropertyDatabaseResourceType):
        resource_path (Union[Unset, str]):
    """

    resource_type: EditDataTableConfigJsonBodySettingsDatatablesAdditionalPropertyDatabaseResourceType
    resource_path: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        resource_type = self.resource_type.value

        resource_path = self.resource_path

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "resource_type": resource_type,
            }
        )
        if resource_path is not UNSET:
            field_dict["resource_path"] = resource_path

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        resource_type = EditDataTableConfigJsonBodySettingsDatatablesAdditionalPropertyDatabaseResourceType(
            d.pop("resource_type")
        )

        resource_path = d.pop("resource_path", UNSET)

        edit_data_table_config_json_body_settings_datatables_additional_property_database = cls(
            resource_type=resource_type,
            resource_path=resource_path,
        )

        edit_data_table_config_json_body_settings_datatables_additional_property_database.additional_properties = d
        return edit_data_table_config_json_body_settings_datatables_additional_property_database

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
