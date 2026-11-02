from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.execute_component_json_body_raw_code_modules_additional_property import (
        ExecuteComponentJsonBodyRawCodeModulesAdditionalProperty,
    )


T = TypeVar("T", bound="ExecuteComponentJsonBodyRawCodeModules")


@_attrs_define
class ExecuteComponentJsonBodyRawCodeModules:
    """Additional modules keyed by relative file path. Honored in preview only: a deployed app runs the modules stored with
    its runnable.

    """

    additional_properties: Dict[str, "ExecuteComponentJsonBodyRawCodeModulesAdditionalProperty"] = _attrs_field(
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
        from ..models.execute_component_json_body_raw_code_modules_additional_property import (
            ExecuteComponentJsonBodyRawCodeModulesAdditionalProperty,
        )

        d = src_dict.copy()
        execute_component_json_body_raw_code_modules = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = ExecuteComponentJsonBodyRawCodeModulesAdditionalProperty.from_dict(prop_dict)

            additional_properties[prop_name] = additional_property

        execute_component_json_body_raw_code_modules.additional_properties = additional_properties
        return execute_component_json_body_raw_code_modules

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> "ExecuteComponentJsonBodyRawCodeModulesAdditionalProperty":
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: "ExecuteComponentJsonBodyRawCodeModulesAdditionalProperty") -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
