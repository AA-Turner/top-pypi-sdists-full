from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.ai_agent_input_transforms_memory_type_0_value_type_2_messages_item_role import (
    AiAgentInputTransformsMemoryType0ValueType2MessagesItemRole,
)

T = TypeVar("T", bound="AiAgentInputTransformsMemoryType0ValueType2MessagesItem")


@_attrs_define
class AiAgentInputTransformsMemoryType0ValueType2MessagesItem:
    """A single message in conversation history

    Attributes:
        role (AiAgentInputTransformsMemoryType0ValueType2MessagesItemRole):
        content (str):
    """

    role: AiAgentInputTransformsMemoryType0ValueType2MessagesItemRole
    content: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        role = self.role.value

        content = self.content

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "role": role,
                "content": content,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        role = AiAgentInputTransformsMemoryType0ValueType2MessagesItemRole(d.pop("role"))

        content = d.pop("content")

        ai_agent_input_transforms_memory_type_0_value_type_2_messages_item = cls(
            role=role,
            content=content,
        )

        ai_agent_input_transforms_memory_type_0_value_type_2_messages_item.additional_properties = d
        return ai_agent_input_transforms_memory_type_0_value_type_2_messages_item

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
