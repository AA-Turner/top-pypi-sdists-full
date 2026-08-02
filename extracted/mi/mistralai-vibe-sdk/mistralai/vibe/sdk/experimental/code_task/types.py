"""Types for programmatic tool calling.

Mirrors the TypeScript types from typescript-sandbox/schema.ts.
"""

import uuid
from typing import Annotated, Any, Literal

from pydantic import BaseModel, Discriminator, Field, Tag


class ToolCallFunction(BaseModel):
    """A tool call's identity: name + arguments."""

    name: str
    arguments: dict[str, Any] = Field(default_factory=dict)


class PendingTool(BaseModel):
    """A tool call that has not yet been resolved."""

    type: Literal["pendingTool"] = "pendingTool"
    id: str = Field(default_factory=lambda: uuid.uuid4().hex[:8])
    function: ToolCallFunction


class ResolvedTool(BaseModel):
    """A tool call that completed successfully."""

    type: Literal["resolvedTool"] = "resolvedTool"
    id: str = ""
    function: ToolCallFunction
    result: Any = None


class RejectedTool(BaseModel):
    """A tool call that failed."""

    type: Literal["rejectedTool"] = "rejectedTool"
    id: str = ""
    function: ToolCallFunction
    error: Any = None


ToolState = Annotated[
    Annotated[PendingTool, Tag("pendingTool")]
    | Annotated[ResolvedTool, Tag("resolvedTool")]
    | Annotated[RejectedTool, Tag("rejectedTool")],
    Discriminator("type"),
]


class PartialEvaluation(BaseModel):
    """The state of a partially-executed code block."""

    code: str
    tool_state: list[ToolState] = Field(default_factory=list)
    input: dict[str, Any] = Field(default_factory=dict)


class CodeResult(BaseModel):
    """The outcome of a completed execution."""

    type: Literal["success", "error"]
    value: Any = None
    error: str | None = None


class RunCodeResult(BaseModel):
    """What run_python_code() returns."""

    type: Literal["code_result", "partial_evaluation", "error"]
    result: CodeResult | None = None
    stdout: str | None = None
    stderr: str | None = None
    partial_evaluation: PartialEvaluation | None = None
    error: str | None = None


class FunctionDef(BaseModel):
    """A tool's function definition."""

    name: str
    description: str = ""
    input_schema: dict[str, Any] = Field(default_factory=dict)
    output_schema: dict[str, Any] = Field(default_factory=dict)


class ToolDefinition(BaseModel):
    """A tool available to the sandbox."""

    type: Literal["function"] = "function"
    function: FunctionDef
