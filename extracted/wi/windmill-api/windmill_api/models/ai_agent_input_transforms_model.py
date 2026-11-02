from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="AiAgentInputTransformsModel")


@_attrs_define
class AiAgentInputTransformsModel:
    """String. Only on a step linked to a saved agent (see `agent`): replaces the model
    saved on the agent for this step's runs, on the agent's own provider resource. An
    empty value keeps the saved model. Set it to an expression such as
    `flow_input.model` to choose the model per run.

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
        ai_agent_input_transforms_model = cls()

        ai_agent_input_transforms_model.additional_properties = d
        return ai_agent_input_transforms_model

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
