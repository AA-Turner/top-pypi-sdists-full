"""The description of a tool that a model can call, whatever runs it."""

from typing import Any, Literal, cast

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    JsonValue,
    SerializationInfo,
    SerializerFunctionWrapHandler,
    TypeAdapter,
    model_serializer,
)
from pydantic.alias_generators import to_camel
from pydantic.main import IncEx

_EXTRA_FIELDS: TypeAdapter[dict[str, Any]] = TypeAdapter(dict[str, Any])


def _with_extra_fields(
    model: BaseModel, handler: SerializerFunctionWrapHandler, info: SerializationInfo
) -> dict[str, Any]:
    # Pydantic writes the fields read with extra="allow" only for a model configured to allow them.
    # They go through Pydantic with the dump's own include and exclude, nested filters included.
    dumped: dict[str, Any] = handler(model)
    extra = {
        key: value for key, value in (model.model_extra or {}).items() if not (info.exclude_none and value is None)
    }
    # pydantic-core types the filters it hands over wider than the ones it takes back: same objects.
    include, exclude = cast("IncEx | None", info.include), cast("IncEx | None", info.exclude)
    mode: Literal["json", "python"] = "json" if info.mode_is_json() else "python"
    dumped.update(_EXTRA_FIELDS.dump_python(extra, mode=mode, include=include, exclude=exclude))
    return dumped


class ToolAnnotations(BaseModel):
    """Hints about what a tool does, as the Model Context Protocol (MCP) defines them, by MCP's
    names as aliases: ``readOnlyHint`` for ``read_only_hint``.

    A hint the tool does not declare takes MCP's default, which assumes the worst: the tool
    writes, may destroy data, is not safe to repeat, and reaches systems outside the agent's
    own. A policy that trusts only declared hints therefore refuses a tool that declares none.
    They are hints: rely on them only for tools from sources you trust.
    """

    # Each field reads and writes by its MCP name, its camelCase alias, with by_alias=True; the
    # constructor takes only the snake_case names and refuses unknown fields. Written in the class,
    # where the Pydantic mypy plugin reads it.
    model_config = ConfigDict(
        frozen=True, extra="forbid", alias_generator=to_camel, validate_by_name=True, validate_by_alias=False
    )

    read_only_hint: bool = False
    """The tool does not change its environment."""
    destructive_hint: bool = True
    """The tool may delete or overwrite data. Meaningful only when ``read_only_hint`` is false."""
    idempotent_hint: bool = False
    """A second call with the same arguments has no further effect. Meaningful only when
    ``read_only_hint`` is false."""
    open_world_hint: bool = True
    """The tool reaches systems outside the agent's own, such as the web."""

    @model_serializer(mode="wrap")
    def _dump_extra_fields(self, handler: SerializerFunctionWrapHandler, info: SerializationInfo) -> dict[str, Any]:
        return _with_extra_fields(self, handler, info)


def _no_arguments() -> dict[str, JsonValue]:
    return {"type": "object", "properties": {}}


class ToolDefinition(BaseModel):
    """The description of a tool: what the model sees of it (name, description, input schema) and
    what a policy can read about it (title, annotations, source).

    It describes any tool, whether a Python function on the worker runs it (a ``PythonTool`` holds
    one) or a connector or an MCP server does. It holds no code. Its fields are those of the Model
    Context Protocol's (MCP) ``Tool``, in snake case, with MCP's names as aliases, plus ``source``.
    Pydantic reads and writes a tool as an MCP server lists it in JSON::

        definition = ToolDefinition.model_validate(tool, by_alias=True, extra="allow")
        definition.model_dump(mode="json", by_alias=True, exclude_unset=True, exclude={"source"})

    ``extra="allow"`` keeps each field it does not model, as listed, in ``model_extra``: one a later
    MCP version adds, or the annotations' ``title`` in ``annotations.model_extra``. The dump writes
    them back.

    Its fields cannot be reassigned. Two tool definitions are equal only if they are the same
    object, and they hash by identity, so a set of tools works for every kind of tool.
    """

    # Each field reads and writes by its MCP name, its camelCase alias, with by_alias=True; the
    # constructor takes only the snake_case names and refuses unknown fields. Written in the class,
    # where the Pydantic mypy plugin reads it.
    model_config = ConfigDict(
        frozen=True, extra="forbid", alias_generator=to_camel, validate_by_name=True, validate_by_alias=False
    )

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
    icons: list[dict[str, JsonValue]] | None = None
    """Icons for people to see the tool by, as MCP's ``Icon`` objects. None when it lists none."""
    meta: dict[str, JsonValue] | None = Field(default=None, validation_alias="_meta", serialization_alias="_meta")
    """MCP's ``_meta``: what the tool's server attaches to it for its clients. None when it
    attaches nothing."""
    execution: dict[str, JsonValue] | None = None
    """How the tool runs, as MCP's ``execution`` object, such as ``{"taskSupport": "optional"}``.
    None when the tool does not say."""

    @property
    def display_title(self) -> str | None:
        """The tool's name for people, for example in an approval prompt: ``title``, else the
        annotations' ``title``, which some servers list instead. None when it has neither."""
        if self.title is not None:
            return self.title
        listed = (self.annotations.model_extra or {}).get("title")
        return listed if isinstance(listed, str) else None

    @model_serializer(mode="wrap")
    def _dump_extra_fields(self, handler: SerializerFunctionWrapHandler, info: SerializationInfo) -> dict[str, Any]:
        return _with_extra_fields(self, handler, info)
