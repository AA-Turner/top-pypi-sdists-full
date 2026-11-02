"""The description of a tool that a model can call, whatever runs it."""

from typing import Any

from pydantic import BaseModel, ConfigDict, Field, JsonValue, model_validator


class ToolAnnotations(BaseModel):
    """Hints about what a tool does, as the Model Context Protocol (MCP) defines them.

    A hint the tool does not declare takes MCP's default, which assumes the worst: the tool
    writes, may destroy data, is not safe to repeat, and reaches systems outside the agent's
    own. A policy that trusts only declared hints therefore refuses a tool that declares none.
    They are hints: rely on them only for tools from sources you trust.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    read_only_hint: bool = False
    """The tool does not change its environment."""
    destructive_hint: bool = True
    """The tool may delete or overwrite data. Meaningful only when ``read_only_hint`` is false."""
    idempotent_hint: bool = False
    """A second call with the same arguments has no further effect. Meaningful only when
    ``read_only_hint`` is false."""
    open_world_hint: bool = True
    """The tool reaches systems outside the agent's own, such as the web."""


def _no_arguments() -> dict[str, JsonValue]:
    return {"type": "object", "properties": {}}


class ToolDefinition(BaseModel):
    """The description of a tool: what the model sees of it (name, description, input schema) and
    what a policy can read about it (title, annotations, source).

    It describes any tool, whether a Python function on the worker runs it (a ``PythonTool`` holds
    one) or a connector or an MCP server does. It holds no code.

    Its fields cannot be reassigned. Two tool definitions are equal only if they are the same
    object, and they hash by identity, so a set of tools works for every kind of tool.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    # Identity, not Pydantic's field-by-field equality: a value hash fails on the input_schema dict.
    __hash__ = object.__hash__

    def __eq__(self, other: object) -> bool:
        return self is other

    @classmethod
    def __pydantic_init_subclass__(cls, **kwargs: Any) -> None:
        super().__pydantic_init_subclass__(**kwargs)
        # Pydantic gives every frozen subclass a value hash when the class is built; this hook runs
        # after that, so every tool definition keeps hashing by identity.
        cls.__hash__ = object.__hash__  # type: ignore[assignment]

    name: str
    """The name the model calls the tool by."""
    title: str | None = None
    """A name for people, for example in an approval prompt."""
    description: str = ""
    """What the tool does, as the model reads it."""
    input_schema: dict[str, JsonValue] = Field(default_factory=_no_arguments)
    """The JSON Schema of the tool's arguments."""
    output_schema: dict[str, JsonValue] | None = None
    """The JSON Schema of the tool's result. None when the tool does not declare one."""
    annotations: ToolAnnotations = ToolAnnotations()
    """Hints about what the tool does, for a policy to read. The model does not see them."""
    source: str | None = None
    """The connector or MCP server that provides the tool, by name. None for a tool the agent
    defines in its own code."""

    @model_validator(mode="before")
    @classmethod
    def _refuse_a_handler(cls, data: Any) -> Any:
        if cls is ToolDefinition and isinstance(data, dict) and "handler" in data:
            raise TypeError(
                "agents.ToolDefinition describes a tool and runs no code. "
                "Build a tool that runs a Python function with @agents.tool or agents.PythonTool(handler=...)"
            )
        return data
