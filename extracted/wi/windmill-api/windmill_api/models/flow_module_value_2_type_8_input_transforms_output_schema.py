from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="FlowModuleValue2Type8InputTransformsOutputSchema")


@_attrs_define
class FlowModuleValue2Type8InputTransformsOutputSchema:
    """JSON Schema object defining structured output format. Used when you need the AI to return data in a specific shape.
    Supports standard JSON Schema properties: type, properties, required, items, enum, pattern, minLength, maxLength,
    minimum, maximum, etc.
    Example: { type: 'object', properties: { name: { type: 'string' }, age: { type: 'integer' } }, required: ['name'] }

    """

    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        flow_module_value_2_type_8_input_transforms_output_schema = cls()

        flow_module_value_2_type_8_input_transforms_output_schema.additional_properties = d
        return flow_module_value_2_type_8_input_transforms_output_schema

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
