from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="AiAgentInputTransformsMemoryId")


@_attrs_define
class AiAgentInputTransformsMemoryId:
    """String. Names the memory this step reads and writes, overriding the memory id the run
    was started with (the chat conversation, an app chat session or the `memory_id` run
    parameter). Leave unset to use the run's memory id. A fixed value shares one memory
    across every run; an expression such as `flow_input.customer_id` keeps one memory per
    key. When it evaluates to an empty value the agent runs without memory. Read only
    while `memory` is `window`: it is ignored when memory is off, and an older `auto` or
    `manual` memory reads neither history input.

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
        ai_agent_input_transforms_memory_id = cls()

        ai_agent_input_transforms_memory_id.additional_properties = d
        return ai_agent_input_transforms_memory_id

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
