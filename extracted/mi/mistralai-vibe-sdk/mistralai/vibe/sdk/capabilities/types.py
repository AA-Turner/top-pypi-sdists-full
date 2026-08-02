"""Shared capability typing helpers for the Vibe SDK."""

from collections.abc import Awaitable, Callable

from pydantic import BaseModel, Field, JsonValue


class ToolResult[ValueT](BaseModel):
    value: ValueT
    annotations: dict[str, JsonValue] = Field(default_factory=dict)


type ToolHandlerContext = BaseModel
type ToolHandler[ToolInput: BaseModel, ToolResult] = Callable[
    ..., ToolResult | Awaitable[ToolResult]
]
