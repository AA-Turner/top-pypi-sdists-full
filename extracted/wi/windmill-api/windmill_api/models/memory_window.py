from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.memory_window_kind import MemoryWindowKind

T = TypeVar("T", bound="MemoryWindow")


@_attrs_define
class MemoryWindow:
    """Keeps the most recent messages of the memory named by the run's memory id (or the step's
    `memory_id`). Without a memory id the agent runs without memory.

        Attributes:
            kind (MemoryWindowKind):
            context_length (int): Number of most recent messages to load and store. 0 turns memory off.
    """

    kind: MemoryWindowKind
    context_length: int
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        kind = self.kind.value

        context_length = self.context_length

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "kind": kind,
                "context_length": context_length,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        kind = MemoryWindowKind(d.pop("kind"))

        context_length = d.pop("context_length")

        memory_window = cls(
            kind=kind,
            context_length=context_length,
        )

        memory_window.additional_properties = d
        return memory_window

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
