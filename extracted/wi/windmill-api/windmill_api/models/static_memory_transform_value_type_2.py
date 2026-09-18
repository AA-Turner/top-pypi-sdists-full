from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.static_memory_transform_value_type_2_kind import StaticMemoryTransformValueType2Kind
from ..types import UNSET, Unset

T = TypeVar("T", bound="StaticMemoryTransformValueType2")


@_attrs_define
class StaticMemoryTransformValueType2:
    """Deprecated, still read as it was written: the run's memory id, else the `memory_id` here.
    The step's own `memory_id` is not read while this kind is set; switch the kind to `window`
    to use it. Without a `context_length`, or with 0, it is `off` and reads `previous_messages`.

        Attributes:
            kind (StaticMemoryTransformValueType2Kind):
            context_length (Union[Unset, int]): Maximum number of messages to retain in context
            memory_id (Union[Unset, str]): Identifier for persistent memory across agent invocations
    """

    kind: StaticMemoryTransformValueType2Kind
    context_length: Union[Unset, int] = UNSET
    memory_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        kind = self.kind.value

        context_length = self.context_length
        memory_id = self.memory_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "kind": kind,
            }
        )
        if context_length is not UNSET:
            field_dict["context_length"] = context_length
        if memory_id is not UNSET:
            field_dict["memory_id"] = memory_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        kind = StaticMemoryTransformValueType2Kind(d.pop("kind"))

        context_length = d.pop("context_length", UNSET)

        memory_id = d.pop("memory_id", UNSET)

        static_memory_transform_value_type_2 = cls(
            kind=kind,
            context_length=context_length,
            memory_id=memory_id,
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
