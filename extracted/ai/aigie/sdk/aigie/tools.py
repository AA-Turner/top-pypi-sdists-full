"""
Tools - Registration and schema generation for agent tools.

Provides a type-safe way to define tools that can be called by agents.
Uses type hints for automatic JSON schema generation and Pydantic for validation.

Example:
    ```python
    from aigie import Agent, RunContext, tool
    from pydantic import BaseModel

    class MyDeps:
        db: Database

    class SearchArgs(BaseModel):
        query: str
        limit: int = 10

    @tool(name='search', description='Search the database')
    async def search(ctx: RunContext[MyDeps], args: SearchArgs) -> str:
        return await ctx.deps.db.search(args.query, args.limit)

    agent = Agent('openai:gpt-4')
    agent.register_tool(search)
    ```
"""

from __future__ import annotations

import asyncio
import json
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import (
    Any,
    Generic,
    TypeVar,
)

from aigie.run_context import RunContext
from aigie.schemas import generate_json_schema

# Type variables
DepsT = TypeVar("DepsT")
ArgsT = TypeVar("ArgsT")
ResultT = TypeVar("ResultT")


@dataclass
class Tool(Generic[DepsT, ArgsT, ResultT]):
    """
    Tool definition with schema and function.

    Attributes:
        name: Unique name for the tool
        description: Description for the LLM
        func: The tool function
        args_type: Type for arguments (Pydantic model or dict)
        json_schema: JSON Schema for OpenAI-style tool calling
        requires_context: Whether this tool requires RunContext
        metadata: Additional metadata
    """

    name: str
    description: str
    func: Callable
    args_type: type[ArgsT] | None = None
    json_schema: dict[str, Any] = field(default_factory=dict)
    requires_context: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Generate JSON schema if not provided."""
        if not self.json_schema and self.func:
            self.json_schema = self._generate_schema()

    def _generate_schema(self) -> dict[str, Any]:
        """Generate JSON schema from function signature."""
        if self.args_type:
            # Use Pydantic model schema if available
            if hasattr(self.args_type, "model_json_schema"):
                return self.args_type.model_json_schema()
            if hasattr(self.args_type, "schema"):
                return self.args_type.schema()

        # Fall back to type hints
        return generate_json_schema(self.func, skip_context=self.requires_context)

    async def execute(self, ctx: RunContext[DepsT], args: dict[str, Any]) -> ResultT:
        """
        Execute the tool with validated arguments.

        Args:
            ctx: The run context with dependencies
            args: Arguments as a dictionary

        Returns:
            The tool result
        """
        # Validate args if we have a type
        if self.args_type:
            if hasattr(self.args_type, "model_validate"):
                validated = self.args_type.model_validate(args)
            elif hasattr(self.args_type, "parse_obj"):
                validated = self.args_type.parse_obj(args)
            else:
                validated = self.args_type(**args)
        else:
            validated = args

        # Call the function
        if self.requires_context:
            if asyncio.iscoroutinefunction(self.func):
                return await self.func(ctx, validated)
            return self.func(ctx, validated)
        if asyncio.iscoroutinefunction(self.func):
            return await self.func(validated)
        return self.func(validated)

    def to_openai_function(self) -> dict[str, Any]:
        """Convert to OpenAI function format."""
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.json_schema,
            },
        }

    def to_anthropic_tool(self) -> dict[str, Any]:
        """Convert to Anthropic tool format."""
        return {
            "name": self.name,
            "description": self.description,
            "input_schema": self.json_schema,
        }


@dataclass
class ToolCall:
    """Tool call request from the LLM."""

    id: str
    name: str
    arguments: str  # JSON string

    def parse_arguments(self) -> dict[str, Any]:
        """Parse arguments from JSON string."""
        return json.loads(self.arguments)


@dataclass
class ToolResult:
    """Result of a tool execution."""

    tool_call_id: str
    content: str
    success: bool
    error: str | None = None
    duration_ms: float | None = None


def tool(
    fn: Callable = None,
    *,
    name: str = None,
    description: str = None,
    args_type: type = None,
    requires_context: bool = True,
    metadata: dict[str, Any] = None,
) -> Tool | Callable:
    """
    Decorator to create a Tool from a function.

    Can be used with or without parentheses:

    ```python
    @tool
    async def my_tool(ctx, args):
        ...

    @tool(name='custom_name', description='My tool')
    async def my_tool(ctx, args):
        ...
    ```

    Args:
        fn: The function to wrap
        name: Override the tool name (defaults to function name)
        description: Tool description (defaults to docstring)
        args_type: Pydantic model for arguments
        requires_context: Whether the tool needs RunContext
        metadata: Additional metadata

    Returns:
        A Tool instance or a decorator function
    """

    def decorator(func: Callable) -> Tool:
        tool_name = name or func.__name__
        tool_description = description or func.__doc__ or f"Tool: {tool_name}"

        # Clean up description
        if isinstance(tool_description, str):
            tool_description = tool_description.strip()

        return Tool(
            name=tool_name,
            description=tool_description,
            func=func,
            args_type=args_type,
            requires_context=requires_context,
            metadata=metadata or {},
        )

    if fn is not None:
        # Called without parentheses: @tool
        return decorator(fn)
    # Called with parentheses: @tool(...)
    return decorator


class ToolRegistry(Generic[DepsT]):
    """
    Registry for managing multiple tools.

    Example:
        ```python
        registry = ToolRegistry()

        @registry.register
        async def search(ctx, query: str) -> str:
            return "results"

        tools = registry.to_openai_functions()
        ```
    """

    def __init__(self):
        self._tools: dict[str, Tool[DepsT, Any, Any]] = {}

    def register(
        self,
        fn: Callable = None,
        *,
        name: str = None,
        description: str = None,
        args_type: type = None,
        requires_context: bool = True,
    ) -> Tool | Callable:
        """
        Register a tool function.

        Can be used as a decorator or called directly.
        """

        def decorator(func: Callable) -> Tool:
            t = tool(
                func,
                name=name,
                description=description,
                args_type=args_type,
                requires_context=requires_context,
            )
            self.add(t)
            return t

        if fn is not None:
            return decorator(fn)
        return decorator

    def add(self, t: Tool) -> None:
        """Add a tool to the registry."""
        if t.name in self._tools:
            raise ValueError(f'Tool "{t.name}" is already registered')
        self._tools[t.name] = t

    def get(self, name: str) -> Tool | None:
        """Get a tool by name."""
        return self._tools.get(name)

    def has(self, name: str) -> bool:
        """Check if a tool exists."""
        return name in self._tools

    def all(self) -> list[Tool]:
        """Get all registered tools."""
        return list(self._tools.values())

    def names(self) -> list[str]:
        """Get all tool names."""
        return list(self._tools.keys())

    def to_openai_functions(self) -> list[dict[str, Any]]:
        """Get tools in OpenAI function format."""
        return [t.to_openai_function() for t in self._tools.values()]

    def to_anthropic_tools(self) -> list[dict[str, Any]]:
        """Get tools in Anthropic tool format."""
        return [t.to_anthropic_tool() for t in self._tools.values()]

    async def execute(self, ctx: RunContext[DepsT], tool_call: ToolCall) -> ToolResult:
        """Execute a tool call."""
        start_time = time.time()

        t = self.get(tool_call.name)
        if not t:
            return ToolResult(
                tool_call_id=tool_call.id,
                content=f'Error: Unknown tool "{tool_call.name}"',
                success=False,
                error=f'Unknown tool "{tool_call.name}"',
            )

        try:
            args = tool_call.parse_arguments()
            result = await t.execute(ctx, args)

            # Convert result to string
            content = result if isinstance(result, str) else json.dumps(result)

            return ToolResult(
                tool_call_id=tool_call.id,
                content=content,
                success=True,
                duration_ms=(time.time() - start_time) * 1000,
            )

        except Exception as e:
            return ToolResult(
                tool_call_id=tool_call.id,
                content=f"Error: {e!s}",
                success=False,
                error=str(e),
                duration_ms=(time.time() - start_time) * 1000,
            )

    def clear(self) -> None:
        """Clear all registered tools."""
        self._tools.clear()


def create_tool_registry() -> ToolRegistry:
    """Create a new tool registry."""
    return ToolRegistry()


async def execute_tool(t: Tool, ctx: RunContext, tool_call: ToolCall) -> ToolResult:
    """
    Execute a single tool call with error handling.

    Args:
        t: The tool to execute
        ctx: The run context
        tool_call: The tool call to execute

    Returns:
        A ToolResult with the execution result
    """
    start_time = time.time()

    try:
        args = tool_call.parse_arguments()
        result = await t.execute(ctx, args)

        content = result if isinstance(result, str) else json.dumps(result)

        return ToolResult(
            tool_call_id=tool_call.id,
            content=content,
            success=True,
            duration_ms=(time.time() - start_time) * 1000,
        )

    except Exception as e:
        return ToolResult(
            tool_call_id=tool_call.id,
            content=f"Error: {e!s}",
            success=False,
            error=str(e),
            duration_ms=(time.time() - start_time) * 1000,
        )


def tools_to_openai_functions(tools: list[Tool]) -> list[dict[str, Any]]:
    """Convert tools to OpenAI function format."""
    return [t.to_openai_function() for t in tools]


def tools_to_anthropic_tools(tools: list[Tool]) -> list[dict[str, Any]]:
    """Convert tools to Anthropic tool format."""
    return [t.to_anthropic_tool() for t in tools]


__all__ = [
    "Tool",
    "ToolCall",
    "ToolRegistry",
    "ToolResult",
    "create_tool_registry",
    "execute_tool",
    "tool",
    "tools_to_anthropic_tools",
    "tools_to_openai_functions",
]
