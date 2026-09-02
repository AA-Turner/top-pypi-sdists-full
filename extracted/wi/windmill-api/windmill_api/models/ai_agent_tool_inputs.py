from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.ai_agent_tool_inputs_additional_property import AiAgentToolInputsAdditionalProperty


T = TypeVar("T", bound="AiAgentToolInputs")


@_attrs_define
class AiAgentToolInputs:
    """Host-local wiring for an agent's tool inputs, keyed by tool id then input key. Binds the
    referenced agent's tools to this flow's context (flow_input/results) without mutating the
    shared resource; overlaid onto the tools' input_transforms at runtime — including when
    `agent` is unset, since a step forked for editing keeps these overrides until it is saved
    back or unlinked.

    """

    additional_properties: Dict[str, "AiAgentToolInputsAdditionalProperty"] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        pass

        field_dict: Dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = prop.to_dict()

        field_dict.update({})

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.ai_agent_tool_inputs_additional_property import AiAgentToolInputsAdditionalProperty

        d = src_dict.copy()
        ai_agent_tool_inputs = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = AiAgentToolInputsAdditionalProperty.from_dict(prop_dict)

            additional_properties[prop_name] = additional_property

        ai_agent_tool_inputs.additional_properties = additional_properties
        return ai_agent_tool_inputs

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> "AiAgentToolInputsAdditionalProperty":
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: "AiAgentToolInputsAdditionalProperty") -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
