from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.get_settings_response_200_dbt_warehouses_additional_property import (
        GetSettingsResponse200DbtWarehousesAdditionalProperty,
    )


T = TypeVar("T", bound="GetSettingsResponse200DbtWarehouses")


@_attrs_define
class GetSettingsResponse200DbtWarehouses:
    """Warehouses a dbt project may run against, by name. `main` is the one a project gets when its descriptor names none.
    Each entry points at a resource; it never holds credentials.

    """

    additional_properties: Dict[str, "GetSettingsResponse200DbtWarehousesAdditionalProperty"] = _attrs_field(
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
        from ..models.get_settings_response_200_dbt_warehouses_additional_property import (
            GetSettingsResponse200DbtWarehousesAdditionalProperty,
        )

        d = src_dict.copy()
        get_settings_response_200_dbt_warehouses = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = GetSettingsResponse200DbtWarehousesAdditionalProperty.from_dict(prop_dict)

            additional_properties[prop_name] = additional_property

        get_settings_response_200_dbt_warehouses.additional_properties = additional_properties
        return get_settings_response_200_dbt_warehouses

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> "GetSettingsResponse200DbtWarehousesAdditionalProperty":
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: "GetSettingsResponse200DbtWarehousesAdditionalProperty") -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
