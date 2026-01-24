from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_settings_response_200_ducklake_ducklakes_additional_property_catalog import (
        GetSettingsResponse200DucklakeDucklakesAdditionalPropertyCatalog,
    )
    from ..models.get_settings_response_200_ducklake_ducklakes_additional_property_storage import (
        GetSettingsResponse200DucklakeDucklakesAdditionalPropertyStorage,
    )


T = TypeVar("T", bound="GetSettingsResponse200DucklakeDucklakesAdditionalProperty")


@_attrs_define
class GetSettingsResponse200DucklakeDucklakesAdditionalProperty:
    """
    Attributes:
        catalog (GetSettingsResponse200DucklakeDucklakesAdditionalPropertyCatalog):
        storage (GetSettingsResponse200DucklakeDucklakesAdditionalPropertyStorage):
        extra_args (Union[Unset, str]):
    """

    catalog: "GetSettingsResponse200DucklakeDucklakesAdditionalPropertyCatalog"
    storage: "GetSettingsResponse200DucklakeDucklakesAdditionalPropertyStorage"
    extra_args: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        catalog = self.catalog.to_dict()

        storage = self.storage.to_dict()

        extra_args = self.extra_args

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "catalog": catalog,
                "storage": storage,
            }
        )
        if extra_args is not UNSET:
            field_dict["extra_args"] = extra_args

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_settings_response_200_ducklake_ducklakes_additional_property_catalog import (
            GetSettingsResponse200DucklakeDucklakesAdditionalPropertyCatalog,
        )
        from ..models.get_settings_response_200_ducklake_ducklakes_additional_property_storage import (
            GetSettingsResponse200DucklakeDucklakesAdditionalPropertyStorage,
        )

        d = src_dict.copy()
        catalog = GetSettingsResponse200DucklakeDucklakesAdditionalPropertyCatalog.from_dict(d.pop("catalog"))

        storage = GetSettingsResponse200DucklakeDucklakesAdditionalPropertyStorage.from_dict(d.pop("storage"))

        extra_args = d.pop("extra_args", UNSET)

        get_settings_response_200_ducklake_ducklakes_additional_property = cls(
            catalog=catalog,
            storage=storage,
            extra_args=extra_args,
        )

        get_settings_response_200_ducklake_ducklakes_additional_property.additional_properties = d
        return get_settings_response_200_ducklake_ducklakes_additional_property

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
