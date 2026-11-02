from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="FlowModuleValue2Type9InputTransformsQuestions")


@_attrs_define
class FlowModuleValue2Type9InputTransformsQuestions:
    """Object mapping each question name to { type, instructions, criteria }, where type is:
    - 'choice': criteria maps each option to its description (up to 255); the answer
      has choice, probabilities and confidence
    - 'score': criteria is an ordered array of 2 to 10 level descriptions; the answer
      has score, legend, probabilities and confidence
    - 'noul': yes/no, criteria optionally { true, false } descriptions; the answer has
      noul, the probability of yes (0 to 1)
    Example: { intent: { type: 'choice', instructions: 'What does the customer want?',
    criteria: { refund: 'Money back', bug: 'Something is broken' } } }

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
        flow_module_value_2_type_9_input_transforms_questions = cls()

        flow_module_value_2_type_9_input_transforms_questions.additional_properties = d
        return flow_module_value_2_type_9_input_transforms_questions

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
