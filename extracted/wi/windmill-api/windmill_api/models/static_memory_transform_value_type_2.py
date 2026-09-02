from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.static_memory_transform_value_type_2_kind import StaticMemoryTransformValueType2Kind

if TYPE_CHECKING:
    from ..models.static_memory_transform_value_type_2_messages_item import StaticMemoryTransformValueType2MessagesItem


T = TypeVar("T", bound="StaticMemoryTransformValueType2")


@_attrs_define
class StaticMemoryTransformValueType2:
    """Explicit message history

    Attributes:
        kind (StaticMemoryTransformValueType2Kind):
        messages (List['StaticMemoryTransformValueType2MessagesItem']):
    """

    kind: StaticMemoryTransformValueType2Kind
    messages: List["StaticMemoryTransformValueType2MessagesItem"]
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
        from ..models.static_memory_transform_value_type_2_messages_item import (
            StaticMemoryTransformValueType2MessagesItem,
        )

        d = src_dict.copy()
        kind = StaticMemoryTransformValueType2Kind(d.pop("kind"))

        messages = []
        _messages = d.pop("messages")
        for messages_item_data in _messages:
            messages_item = StaticMemoryTransformValueType2MessagesItem.from_dict(messages_item_data)

            messages.append(messages_item)

        static_memory_transform_value_type_2 = cls(
            kind=kind,
            messages=messages,
        )

        static_memory_transform_value_type_2.additional_properties = d
        return static_memory_transform_value_type_2

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
