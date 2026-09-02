from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.flow_module_value_2_type_8_input_transforms_memory_type_0_value_type_1_kind import (
    FlowModuleValue2Type8InputTransformsMemoryType0ValueType1Kind,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="FlowModuleValue2Type8InputTransformsMemoryType0ValueType1")


@_attrs_define
class FlowModuleValue2Type8InputTransformsMemoryType0ValueType1:
    """Automatic context management

    Attributes:
        kind (FlowModuleValue2Type8InputTransformsMemoryType0ValueType1Kind):
        context_length (Union[Unset, int]): Maximum number of messages to retain in context
        memory_id (Union[Unset, str]): Identifier for persistent memory across agent invocations
    """

    kind: FlowModuleValue2Type8InputTransformsMemoryType0ValueType1Kind
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
        kind = FlowModuleValue2Type8InputTransformsMemoryType0ValueType1Kind(d.pop("kind"))

        context_length = d.pop("context_length", UNSET)

        memory_id = d.pop("memory_id", UNSET)

        flow_module_value_2_type_8_input_transforms_memory_type_0_value_type_1 = cls(
            kind=kind,
            context_length=context_length,
            memory_id=memory_id,
        )

        flow_module_value_2_type_8_input_transforms_memory_type_0_value_type_1.additional_properties = d
        return flow_module_value_2_type_8_input_transforms_memory_type_0_value_type_1

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
