"""The builtin tools a sandbox can be asked to execute.

A consumer routes exactly these tools into the sandbox; every other builtin runs on the worker.
A sandbox that has Python runs them against the SDK installed there, and one that does not
serves them itself.

Each tool carries its own name, argument model and result model, so this module holds no parallel
mapping: ``_SANDBOX_TOOLS`` only says which tools are dispatchable. The two unions exist because a
static type checker cannot read a runtime table; a test pins them to it member for member.
"""

import json
from collections.abc import Mapping
from typing import Any, Protocol, cast

from pydantic import BaseModel, JsonValue

from ..types import ToolResult
from .bash_tool import BashArgs, BashResult, bash
from .grep_tool import GrepArgs, GrepResult, grep
from .read_file_tool import ReadFileArgs, ReadFileResult, read_file
from .search_replace_tool import SearchReplaceArgs, SearchReplaceResult, search_replace
from .write_file_tool import WriteFileArgs, WriteFileResult, write_file

type SandboxToolArgs = BashArgs | GrepArgs | ReadFileArgs | SearchReplaceArgs | WriteFileArgs

type SandboxToolResult = (
    BashResult | GrepResult | ReadFileResult | SearchReplaceResult | WriteFileResult
)


class SandboxTool(Protocol):
    """What a tool must expose to be runnable by a sandbox."""

    @property
    def name(self) -> str: ...

    @property
    def input_schema(self) -> type[BaseModel]: ...

    @property
    def result_schema(self) -> type[BaseModel] | None: ...

    # Any mirrors ToolDefinition.invoke: it validates **kwargs against input_schema at runtime.
    async def invoke(self, *positional: Any, **kwargs: Any) -> Any: ...  # noqa: ANN401


# Annotating the tuple is what makes a type checker prove each tool satisfies SandboxTool.
_SANDBOX_TOOLS: tuple[SandboxTool, ...] = (bash, grep, read_file, search_replace, write_file)

SANDBOX_DISPATCHABLE_TOOLS: Mapping[str, SandboxTool] = {tool.name: tool for tool in _SANDBOX_TOOLS}

_TOOLS_BY_ARGS_SCHEMA: Mapping[type[BaseModel], SandboxTool] = {
    tool.input_schema: tool for tool in _SANDBOX_TOOLS
}


def sandbox_tool(name: str) -> SandboxTool:
    tool = SANDBOX_DISPATCHABLE_TOOLS.get(name)
    if tool is None:
        raise ValueError(f"{name!r} is not a sandbox-dispatchable tool")
    return tool


def sandbox_tool_for(tool_args: SandboxToolArgs) -> SandboxTool:
    tool = _TOOLS_BY_ARGS_SCHEMA.get(type(tool_args))
    if tool is None:
        raise ValueError(f"{type(tool_args).__name__} is not a sandbox-dispatchable tool argument")
    return tool


def parse_sandbox_tool_args(name: str, raw: object) -> SandboxToolArgs:
    # cast: TestTableAndUnionsAgree pins the table's models to the union members exactly.
    return cast(SandboxToolArgs, sandbox_tool(name).input_schema.model_validate(raw))


def parse_sandbox_tool_result(name: str, raw: object) -> SandboxToolResult:
    tool = sandbox_tool(name)
    if tool.result_schema is None:
        raise ValueError(f"{name!r} declares no result_schema")
    return cast(SandboxToolResult, tool.result_schema.model_validate(raw))


def serialize_sandbox_tool_result(name: str, result: object) -> ToolResult[JsonValue]:
    annotations: dict[str, JsonValue] = {}
    if isinstance(result, ToolResult):
        annotations = result.annotations
        result = result.value
    if isinstance(result, BaseModel):
        result = result.model_dump(mode="json")

    parsed_result = parse_sandbox_tool_result(name, result)
    return ToolResult(
        value=_json_value(parsed_result.model_dump(mode="json")),
        annotations=annotations,
    )


def parse_sandbox_tool_execution_result(name: str, raw: object) -> ToolResult[JsonValue]:
    if isinstance(raw, Mapping) and "value" in raw and set(raw) <= {"value", "annotations"}:
        result = ToolResult[JsonValue].model_validate(
            {key: value for key, value in raw.items() if value is not None}
        )
        parsed_result = parse_sandbox_tool_result(name, result.value)
        return result.model_copy(update={"value": parsed_result.model_dump(mode="json")})

    parsed_result = parse_sandbox_tool_result(name, raw)
    return ToolResult(value=_json_value(parsed_result.model_dump(mode="json")))


def _json_value(value: object) -> JsonValue:
    return cast(JsonValue, json.loads(json.dumps(value, default=str)))
