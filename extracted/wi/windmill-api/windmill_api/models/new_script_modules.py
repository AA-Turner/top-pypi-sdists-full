from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.new_script_modules_additional_property import NewScriptModulesAdditionalProperty


T = TypeVar("T", bound="NewScriptModules")


@_attrs_define
class NewScriptModules:
    """Additional script modules keyed by relative file path"""

    additional_properties: Dict[str, "NewScriptModulesAdditionalProperty"] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        pass

        field_dict: Dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = prop.to_dict()

        field_dict.update({})

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.new_script_modules_additional_property import NewScriptModulesAdditionalProperty

        d = src_dict.copy()
        new_script_modules = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = NewScriptModulesAdditionalProperty.from_dict(prop_dict)

            additional_properties[prop_name] = additional_property

        new_script_modules.additional_properties = additional_properties
        return new_script_modules

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> "NewScriptModulesAdditionalProperty":
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: "NewScriptModulesAdditionalProperty") -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
