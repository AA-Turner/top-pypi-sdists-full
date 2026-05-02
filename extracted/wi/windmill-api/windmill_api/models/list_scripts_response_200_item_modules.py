from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.list_scripts_response_200_item_modules_additional_property import (
        ListScriptsResponse200ItemModulesAdditionalProperty,
    )


T = TypeVar("T", bound="ListScriptsResponse200ItemModules")


@_attrs_define
class ListScriptsResponse200ItemModules:
    """Additional script modules keyed by relative file path"""

    additional_properties: Dict[str, "ListScriptsResponse200ItemModulesAdditionalProperty"] = _attrs_field(
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
        from ..models.list_scripts_response_200_item_modules_additional_property import (
            ListScriptsResponse200ItemModulesAdditionalProperty,
        )

        d = src_dict.copy()
        list_scripts_response_200_item_modules = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = ListScriptsResponse200ItemModulesAdditionalProperty.from_dict(prop_dict)

            additional_properties[prop_name] = additional_property

        list_scripts_response_200_item_modules.additional_properties = additional_properties
        return list_scripts_response_200_item_modules

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> "ListScriptsResponse200ItemModulesAdditionalProperty":
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: "ListScriptsResponse200ItemModulesAdditionalProperty") -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
