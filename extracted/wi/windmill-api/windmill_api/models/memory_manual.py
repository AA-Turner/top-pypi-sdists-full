from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.memory_manual_kind import MemoryManualKind

if TYPE_CHECKING:
    from ..models.memory_manual_messages_item import MemoryManualMessagesItem


T = TypeVar("T", bound="MemoryManual")


@_attrs_define
class MemoryManual:
    """Explicit message history

    Attributes:
        kind (MemoryManualKind):
        messages (List['MemoryManualMessagesItem']):
    """

    kind: MemoryManualKind
    messages: List["MemoryManualMessagesItem"]
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
        from ..models.memory_manual_messages_item import MemoryManualMessagesItem

        d = src_dict.copy()
        kind = MemoryManualKind(d.pop("kind"))

        messages = []
        _messages = d.pop("messages")
        for messages_item_data in _messages:
            messages_item = MemoryManualMessagesItem.from_dict(messages_item_data)

            messages.append(messages_item)

        memory_manual = cls(
            kind=kind,
            messages=messages,
        )

        memory_manual.additional_properties = d
        return memory_manual

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
