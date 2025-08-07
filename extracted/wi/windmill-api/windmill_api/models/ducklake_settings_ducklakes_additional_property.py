from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.ducklake_settings_ducklakes_additional_property_catalog import (
        DucklakeSettingsDucklakesAdditionalPropertyCatalog,
    )
    from ..models.ducklake_settings_ducklakes_additional_property_storage import (
        DucklakeSettingsDucklakesAdditionalPropertyStorage,
    )


T = TypeVar("T", bound="DucklakeSettingsDucklakesAdditionalProperty")


@_attrs_define
class DucklakeSettingsDucklakesAdditionalProperty:
    """
    Attributes:
        catalog (DucklakeSettingsDucklakesAdditionalPropertyCatalog):
        storage (DucklakeSettingsDucklakesAdditionalPropertyStorage):
    """

    catalog: "DucklakeSettingsDucklakesAdditionalPropertyCatalog"
    storage: "DucklakeSettingsDucklakesAdditionalPropertyStorage"
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
        from ..models.ducklake_settings_ducklakes_additional_property_catalog import (
            DucklakeSettingsDucklakesAdditionalPropertyCatalog,
        )
        from ..models.ducklake_settings_ducklakes_additional_property_storage import (
            DucklakeSettingsDucklakesAdditionalPropertyStorage,
        )

        d = src_dict.copy()
        catalog = DucklakeSettingsDucklakesAdditionalPropertyCatalog.from_dict(d.pop("catalog"))

        storage = DucklakeSettingsDucklakesAdditionalPropertyStorage.from_dict(d.pop("storage"))

        ducklake_settings_ducklakes_additional_property = cls(
            catalog=catalog,
            storage=storage,
        )

        ducklake_settings_ducklakes_additional_property.additional_properties = d
        return ducklake_settings_ducklakes_additional_property

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
