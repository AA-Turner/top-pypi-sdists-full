from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.memory_transform_type_0_value_type_2_kind import MemoryTransformType0ValueType2Kind
from ..types import UNSET, Unset

T = TypeVar("T", bound="MemoryTransformType0ValueType2")


@_attrs_define
class MemoryTransformType0ValueType2:
    """Keeps the whole memory named by the run's memory id (or the step's `memory_id`), replacing
    its older part with a summary as the conversation approaches the model's context window.
    Without a memory id the agent runs without memory, and compaction bounds the run's own loop.

        Attributes:
            kind (MemoryTransformType0ValueType2Kind):
            context_window (Union[Unset, int]): Overrides the context window looked up from the model, in tokens. Only a
                model
                Windmill does not know needs one; those fall back to 128000.
    """

    kind: MemoryTransformType0ValueType2Kind
    context_window: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        kind = self.kind.value

        context_window = self.context_window

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "kind": kind,
            }
        )
        if context_window is not UNSET:
            field_dict["context_window"] = context_window

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        kind = MemoryTransformType0ValueType2Kind(d.pop("kind"))

        context_window = d.pop("context_window", UNSET)

        memory_transform_type_0_value_type_2 = cls(
            kind=kind,
            context_window=context_window,
        )

        memory_transform_type_0_value_type_2.additional_properties = d
        return memory_transform_type_0_value_type_2

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
