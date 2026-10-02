from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="GradingConfigMcpToolCallToolsItem")



@_attrs_define
class GradingConfigMcpToolCallToolsItem:
    """ A single read-only MCP tool call the grader executes against the cloned solver run.

        Attributes:
            tool_name (str): Name of the MCP tool to call, as exposed by the harness mcpTools catalog.
            tool_params (str): Arguments passed to the tool, stored as an opaque JSON string (see comment).
     """

    tool_name: str
    tool_params: str





    def to_dict(self) -> dict[str, Any]:
        tool_name = self.tool_name

        tool_params = self.tool_params


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "toolName": tool_name,
            "toolParams": tool_params,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        tool_name = d.pop("toolName")

        tool_params = d.pop("toolParams")

        grading_config_mcp_tool_call_tools_item = cls(
            tool_name=tool_name,
            tool_params=tool_params,
        )

        return grading_config_mcp_tool_call_tools_item

