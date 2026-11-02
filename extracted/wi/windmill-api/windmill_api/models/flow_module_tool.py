from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.flow_module_tool_tool_type import FlowModuleToolToolType

T = TypeVar("T", bound="FlowModuleTool")


@_attrs_define
class FlowModuleTool:
    """A tool implemented as a flow module (script, flow, etc.). The AI can call this like any other flow module

    Attributes:
        tool_type (FlowModuleToolToolType):
    """

    tool_type: FlowModuleToolToolType
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        tool_type = self.tool_type.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "tool_type": tool_type,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        tool_type = FlowModuleToolToolType(d.pop("tool_type"))

        flow_module_tool = cls(
            tool_type=tool_type,
        )

        flow_module_tool.additional_properties = d
        return flow_module_tool

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
