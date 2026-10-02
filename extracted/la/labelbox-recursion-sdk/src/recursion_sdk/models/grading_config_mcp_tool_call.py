from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.grading_config_mcp_tool_call_comparator import GradingConfigMcpToolCallComparator
from ..models.grading_config_mcp_tool_call_type import GradingConfigMcpToolCallType
from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.grading_config_mcp_tool_call_tools_item import GradingConfigMcpToolCallToolsItem





T = TypeVar("T", bound="GradingConfigMcpToolCall")



@_attrs_define
class GradingConfigMcpToolCall:
    """ Grading config leaf that calls author-fixed read-only MCP tools against the solver end-state and scores their
    captured outputs with a deterministic comparator.

        Attributes:
            type_ (GradingConfigMcpToolCallType): Discriminator: grade by calling fixed read-only MCP tools and comparing
                outputs.
            tools (list[GradingConfigMcpToolCallToolsItem]): Read-only MCP tool calls to execute against the solver end-
                state (at least one).
            comparator (GradingConfigMcpToolCallComparator): Deterministic comparator applied to the (optionally response-
                path-extracted) MCP tool output against the expected value.
            expected (str): Expected value the (response-path-extracted) tool output is compared against.
            response_path (str | Unset): Optional JSONPath into the captured tool output; the result is what gets compared.
            grader_image (None | str | Unset): MCP-verify grader image; required for grading (pre-filled from the solver run
                config grader image). No platform default — grading fails fast if unset.
     """

    type_: GradingConfigMcpToolCallType
    tools: list[GradingConfigMcpToolCallToolsItem]
    comparator: GradingConfigMcpToolCallComparator
    expected: str
    response_path: str | Unset = UNSET
    grader_image: None | str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.grading_config_mcp_tool_call_tools_item import GradingConfigMcpToolCallToolsItem # noqa: PLC0415
        type_ = self.type_.value

        tools = []
        for tools_item_data in self.tools:
            tools_item = tools_item_data.to_dict()
            tools.append(tools_item)



        comparator = self.comparator.value

        expected = self.expected

        response_path = self.response_path

        grader_image: None | str | Unset
        if isinstance(self.grader_image, Unset):
            grader_image = UNSET
        else:
            grader_image = self.grader_image


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "type": type_,
            "tools": tools,
            "comparator": comparator,
            "expected": expected,
        })
        if response_path is not UNSET:
            field_dict["responsePath"] = response_path
        if grader_image is not UNSET:
            field_dict["graderImage"] = grader_image

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.grading_config_mcp_tool_call_tools_item import GradingConfigMcpToolCallToolsItem # noqa: PLC0415
        d = dict(src_dict)
        type_ = GradingConfigMcpToolCallType(d.pop("type"))




        tools = []
        _tools = d.pop("tools")
        for tools_item_data in (_tools):
            tools_item = GradingConfigMcpToolCallToolsItem.from_dict(tools_item_data)



            tools.append(tools_item)


        comparator = GradingConfigMcpToolCallComparator(d.pop("comparator"))




        expected = d.pop("expected")

        response_path = d.pop("responsePath", UNSET)

        def _parse_grader_image(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        grader_image = _parse_grader_image(d.pop("graderImage", UNSET))


        grading_config_mcp_tool_call = cls(
            type_=type_,
            tools=tools,
            comparator=comparator,
            expected=expected,
            response_path=response_path,
            grader_image=grader_image,
        )

        return grading_config_mcp_tool_call

