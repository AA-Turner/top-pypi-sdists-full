from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.grading_config_input_mcp_tool_call_tools_item_tool_params_type_1 import GradingConfigInputMcpToolCallToolsItemToolParamsType1





T = TypeVar("T", bound="GradingConfigInputMcpToolCallToolsItem")



@_attrs_define
class GradingConfigInputMcpToolCallToolsItem:
    """ A single read-only MCP tool call the grader executes against the cloned solver run.

        Attributes:
            tool_name (str): Name of the MCP tool to call, as exposed by the harness mcpTools catalog.
            tool_params (GradingConfigInputMcpToolCallToolsItemToolParamsType1 | str): Arguments passed to the tool, stored
                as an opaque JSON string (see comment).
     """

    tool_name: str
    tool_params: GradingConfigInputMcpToolCallToolsItemToolParamsType1 | str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.grading_config_input_mcp_tool_call_tools_item_tool_params_type_1 import GradingConfigInputMcpToolCallToolsItemToolParamsType1 # noqa: PLC0415
        tool_name = self.tool_name

        tool_params: dict[str, Any] | str
        if isinstance(self.tool_params, GradingConfigInputMcpToolCallToolsItemToolParamsType1):
            tool_params = self.tool_params.to_dict()
        else:
            tool_params = self.tool_params


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "toolName": tool_name,
            "toolParams": tool_params,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.grading_config_input_mcp_tool_call_tools_item_tool_params_type_1 import GradingConfigInputMcpToolCallToolsItemToolParamsType1 # noqa: PLC0415
        d = dict(src_dict)
        tool_name = d.pop("toolName")

        def _parse_tool_params(data: object) -> GradingConfigInputMcpToolCallToolsItemToolParamsType1 | str:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                tool_params_type_1 = GradingConfigInputMcpToolCallToolsItemToolParamsType1.from_dict(data)



                return tool_params_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(GradingConfigInputMcpToolCallToolsItemToolParamsType1 | str, data)

        tool_params = _parse_tool_params(d.pop("toolParams"))


        grading_config_input_mcp_tool_call_tools_item = cls(
            tool_name=tool_name,
            tool_params=tool_params,
        )


        grading_config_input_mcp_tool_call_tools_item.additional_properties = d
        return grading_config_input_mcp_tool_call_tools_item

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
