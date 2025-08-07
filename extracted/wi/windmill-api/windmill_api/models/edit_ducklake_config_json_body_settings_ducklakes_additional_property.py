from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.edit_ducklake_config_json_body_settings_ducklakes_additional_property_catalog import (
        EditDucklakeConfigJsonBodySettingsDucklakesAdditionalPropertyCatalog,
    )
    from ..models.edit_ducklake_config_json_body_settings_ducklakes_additional_property_storage import (
        EditDucklakeConfigJsonBodySettingsDucklakesAdditionalPropertyStorage,
    )


T = TypeVar("T", bound="EditDucklakeConfigJsonBodySettingsDucklakesAdditionalProperty")


@_attrs_define
class EditDucklakeConfigJsonBodySettingsDucklakesAdditionalProperty:
    """
    Attributes:
        catalog (EditDucklakeConfigJsonBodySettingsDucklakesAdditionalPropertyCatalog):
        storage (EditDucklakeConfigJsonBodySettingsDucklakesAdditionalPropertyStorage):
    """

    catalog: "EditDucklakeConfigJsonBodySettingsDucklakesAdditionalPropertyCatalog"
    storage: "EditDucklakeConfigJsonBodySettingsDucklakesAdditionalPropertyStorage"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        catalog = self.catalog.to_dict()

        storage = self.storage.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "catalog": catalog,
                "storage": storage,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.edit_ducklake_config_json_body_settings_ducklakes_additional_property_catalog import (
            EditDucklakeConfigJsonBodySettingsDucklakesAdditionalPropertyCatalog,
        )
        from ..models.edit_ducklake_config_json_body_settings_ducklakes_additional_property_storage import (
            EditDucklakeConfigJsonBodySettingsDucklakesAdditionalPropertyStorage,
        )

        d = src_dict.copy()
        catalog = EditDucklakeConfigJsonBodySettingsDucklakesAdditionalPropertyCatalog.from_dict(d.pop("catalog"))

        storage = EditDucklakeConfigJsonBodySettingsDucklakesAdditionalPropertyStorage.from_dict(d.pop("storage"))

        edit_ducklake_config_json_body_settings_ducklakes_additional_property = cls(
            catalog=catalog,
            storage=storage,
        )

        edit_ducklake_config_json_body_settings_ducklakes_additional_property.additional_properties = d
        return edit_ducklake_config_json_body_settings_ducklakes_additional_property

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
