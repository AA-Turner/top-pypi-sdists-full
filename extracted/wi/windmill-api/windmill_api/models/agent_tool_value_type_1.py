from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.agent_tool_value_type_1_tool_type import AgentToolValueType1ToolType
from ..types import UNSET, Unset

T = TypeVar("T", bound="AgentToolValueType1")


@_attrs_define
class AgentToolValueType1:
    """Reference to an external MCP (Model Context Protocol) tool. The AI can call tools from MCP servers

    Attributes:
        tool_type (AgentToolValueType1ToolType):
        resource_path (str): Path to the MCP resource/server configuration
        include_tools (Union[Unset, List[str]]): Whitelist of specific tools to include from this MCP server
        exclude_tools (Union[Unset, List[str]]): Blacklist of tools to exclude from this MCP server
    """

    tool_type: AgentToolValueType1ToolType
    resource_path: str
    include_tools: Union[Unset, List[str]] = UNSET
    exclude_tools: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        tool_type = self.tool_type.value

        resource_path = self.resource_path
        include_tools: Union[Unset, List[str]] = UNSET
        if not isinstance(self.include_tools, Unset):
            include_tools = self.include_tools

        exclude_tools: Union[Unset, List[str]] = UNSET
        if not isinstance(self.exclude_tools, Unset):
            exclude_tools = self.exclude_tools

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "tool_type": tool_type,
                "resource_path": resource_path,
            }
        )
        if include_tools is not UNSET:
            field_dict["include_tools"] = include_tools
        if exclude_tools is not UNSET:
            field_dict["exclude_tools"] = exclude_tools

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        tool_type = AgentToolValueType1ToolType(d.pop("tool_type"))

        resource_path = d.pop("resource_path")

        include_tools = cast(List[str], d.pop("include_tools", UNSET))

        exclude_tools = cast(List[str], d.pop("exclude_tools", UNSET))

        agent_tool_value_type_1 = cls(
            tool_type=tool_type,
            resource_path=resource_path,
            include_tools=include_tools,
            exclude_tools=exclude_tools,
        )

        agent_tool_value_type_1.additional_properties = d
        return agent_tool_value_type_1

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
