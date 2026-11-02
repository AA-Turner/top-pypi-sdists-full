from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="FlowModuleValue2Type8InputTransformsReasoningEffort")


@_attrs_define
class FlowModuleValue2Type8InputTransformsReasoningEffort:
    """String. Only on a step linked to a saved agent (see `agent`): replaces the reasoning
    effort saved on the agent for this step's runs, as a provider-native token (e.g.
    'low', 'high', 'none'). An empty value sends no effort, so the model runs at its
    default. Leave the input out to keep the saved effort, which holds only while the
    step runs the saved model. A step that is not linked sets both inside `provider`.

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
        flow_module_value_2_type_8_input_transforms_reasoning_effort = cls()

        flow_module_value_2_type_8_input_transforms_reasoning_effort.additional_properties = d
        return flow_module_value_2_type_8_input_transforms_reasoning_effort

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
