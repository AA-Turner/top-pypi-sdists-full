from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.ai_agent_input_transforms_memory_type_0_value_type_3_kind import (
    AiAgentInputTransformsMemoryType0ValueType3Kind,
)

if TYPE_CHECKING:
    from ..models.ai_agent_input_transforms_memory_type_0_value_type_3_messages_item import (
        AiAgentInputTransformsMemoryType0ValueType3MessagesItem,
    )


T = TypeVar("T", bound="AiAgentInputTransformsMemoryType0ValueType3")


@_attrs_define
class AiAgentInputTransformsMemoryType0ValueType3:
    """Deprecated, still read as it was written. Move the step to `off` with `previous_messages` instead.

    Attributes:
        kind (AiAgentInputTransformsMemoryType0ValueType3Kind):
        messages (List['AiAgentInputTransformsMemoryType0ValueType3MessagesItem']):
    """

    kind: AiAgentInputTransformsMemoryType0ValueType3Kind
    messages: List["AiAgentInputTransformsMemoryType0ValueType3MessagesItem"]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        kind = self.kind.value

        messages = []
        for messages_item_data in self.messages:
            messages_item = messages_item_data.to_dict()

            messages.append(messages_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "kind": kind,
                "messages": messages,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.ai_agent_input_transforms_memory_type_0_value_type_3_messages_item import (
            AiAgentInputTransformsMemoryType0ValueType3MessagesItem,
        )

        d = src_dict.copy()
        kind = AiAgentInputTransformsMemoryType0ValueType3Kind(d.pop("kind"))

        messages = []
        _messages = d.pop("messages")
        for messages_item_data in _messages:
            messages_item = AiAgentInputTransformsMemoryType0ValueType3MessagesItem.from_dict(messages_item_data)

            messages.append(messages_item)

        ai_agent_input_transforms_memory_type_0_value_type_3 = cls(
            kind=kind,
            messages=messages,
        )

        ai_agent_input_transforms_memory_type_0_value_type_3.additional_properties = d
        return ai_agent_input_transforms_memory_type_0_value_type_3

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
