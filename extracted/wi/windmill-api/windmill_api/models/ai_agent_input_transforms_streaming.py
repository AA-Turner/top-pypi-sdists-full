from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="AiAgentInputTransformsStreaming")


@_attrs_define
class AiAgentInputTransformsStreaming:
    """Boolean. If true, stream the AI response incrementally.
    Streaming events include: token_delta, reasoning_token_delta, tool_call, tool_call_arguments, tool_execution,
    tool_result

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
        ai_agent_input_transforms_streaming = cls()

        ai_agent_input_transforms_streaming.additional_properties = d
        return ai_agent_input_transforms_streaming

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
