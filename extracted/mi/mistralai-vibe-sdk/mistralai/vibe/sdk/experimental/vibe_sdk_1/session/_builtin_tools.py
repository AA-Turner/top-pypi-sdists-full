"""Internal built-in tool definitions for the harness engine."""

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Literal, cast

from pydantic import Field

from ..base import JsonSchema, ProtocolModel

type BuiltinToolName = Literal["bash", "read_file", "write_file"]


class BashToolInput(ProtocolModel):
    command: str
    timeout_seconds: int = Field(default=300, ge=1)


class BashToolOutput(ProtocolModel):
    stdout: str = ""
    stderr: str = ""
    exit_code: int


class ReadFileToolInput(ProtocolModel):
    path: str
    offset: int = Field(default=0, ge=0)
    limit: int | None = Field(default=None, ge=0)


class ReadFileToolOutput(ProtocolModel):
    path: str
    content: str
    truncated: bool = False


class WriteFileToolInput(ProtocolModel):
    path: str
    content: str
    overwrite: bool = False


class WriteFileToolOutput(ProtocolModel):
    path: str
    bytes_written: int = Field(ge=0)


@dataclass(frozen=True, slots=True)
class BuiltinToolDefinition:
    """Internal model-facing definition for SDK-owned harness tools."""

    name: BuiltinToolName
    description: str
    input_model: type[ProtocolModel]
    output_model: type[ProtocolModel]

    @property
    def input_schema(self) -> JsonSchema:
        return cast(JsonSchema, self.input_model.model_json_schema())

    @property
    def output_schema(self) -> JsonSchema:
        return cast(JsonSchema, self.output_model.model_json_schema())


BUILTIN_TOOL_DEFINITIONS: Mapping[BuiltinToolName, BuiltinToolDefinition] = {
    "bash": BuiltinToolDefinition(
        name="bash",
        description="Run a shell command on the host machine and return stdout, stderr, and code.",
        input_model=BashToolInput,
        output_model=BashToolOutput,
    ),
    "read_file": BuiltinToolDefinition(
        name="read_file",
        description="Read a UTF-8 text file from the host filesystem.",
        input_model=ReadFileToolInput,
        output_model=ReadFileToolOutput,
    ),
    "write_file": BuiltinToolDefinition(
        name="write_file",
        description="Write UTF-8 text to the host filesystem.",
        input_model=WriteFileToolInput,
        output_model=WriteFileToolOutput,
    ),
}
