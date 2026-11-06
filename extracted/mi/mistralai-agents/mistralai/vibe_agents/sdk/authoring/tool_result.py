"""Rich tool results: content blocks, structured output and metadata for the client.

A tool handler may return a ``ToolResult``, one content block, a list of content blocks, an
MCP ``CallToolResult`` or MCP content blocks, a string, or any JSON value or Pydantic model.
The blocks are the Session content blocks used for ``run_turn`` input and for history.

The model sees ``content``, without blocks whose ``audience`` excludes ``"assistant"``. It sees
``structured_content`` only when ``content`` is empty. ``meta`` is never shown to the model.
"""

import warnings
from collections.abc import Mapping, Sequence
from types import UnionType
from typing import TYPE_CHECKING, Annotated, Any, Generic, Self, TypeAliasType, Union, get_args, get_origin

from mcp import types as mcp_types
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    JsonValue,
    ModelWrapValidatorHandler,
    PrivateAttr,
    TypeAdapter,
    field_validator,
    model_validator,
)
from typing_extensions import TypeVar

from mistralai.vibe.harness.app_server.session import (
    AudioContentBlock,
    ContentAnnotations,
    ContentBlock,
    EmbeddedResourceContentBlock,
    ImageContentBlock,
    ResourceLinkContentBlock,
    TextContentBlock,
)
from mistralai.vibe.harness.app_server.session.models.content import refuse_unsupported_blocks
from mistralai.vibe.harness.runtime.content import to_session_content
from mistralai.vibe.harness.runtime.hosts.mcp_results import from_mcp_content

SESSION_CONTENT_BLOCK_TYPES = (
    TextContentBlock,
    ImageContentBlock,
    AudioContentBlock,
    ResourceLinkContentBlock,
    EmbeddedResourceContentBlock,
)
MCP_CONTENT_BLOCK_TYPES = (
    mcp_types.TextContent,
    mcp_types.ImageContent,
    mcp_types.AudioContent,
    mcp_types.ResourceLink,
    mcp_types.EmbeddedResource,
)
_CONTENT_BLOCK_ADAPTER: TypeAdapter[ContentBlock] = TypeAdapter(ContentBlock)

# The parameter of the former generic ``ToolResult``. A tool annotated ``-> ToolResult[T]`` gets
# T's JSON Schema as its output schema; ``structured_content`` itself is any JSON value.
_LegacyValueT = TypeVar("_LegacyValueT", default=Any)


class ToolResult(BaseModel, Generic[_LegacyValueT]):
    """What a tool returns: content for the model, structured output, and metadata for the client.

    A tool annotated ``-> ToolResult[T]`` gets ``T``'s JSON Schema as its output schema.
    ``ToolResult[T]`` does not type ``structured_content``: the tool's output schema checks it when
    the tool returns.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    content: list[ContentBlock] = Field(default_factory=list)
    """Blocks the model sees. Blocks with ``audience=["user"]`` are for the application's UI only."""
    structured_content: JsonValue = None
    """Machine-readable output, validated against the tool's output schema. The model sees it
    only when ``content`` is empty."""
    is_error: bool = False
    """A tool execution error (MCP ``isError``): the model sees the content and can retry."""
    meta: dict[str, JsonValue] = Field(default_factory=dict)
    """Metadata for the client, as MCP's ``_meta``. Never shown to the model."""
    # The model class of a Pydantic ``structured_content`` and the dump it gave: an instance
    # of the tool's output schema needs no check against it (its dump can carry computed
    # fields the schema forbids). A copy with other ``structured_content`` holds another dump.
    _structured_model: tuple[type[BaseModel], JsonValue] | None = PrivateAttr(default=None)

    if TYPE_CHECKING:
        # The validator below takes MCP blocks, block JSON, a Pydantic structured value and the
        # deprecated aliases; without this signature type checkers would refuse all four.
        def __init__(
            self,
            *,
            content: Sequence[ContentBlock | mcp_types.ContentBlock | Mapping[str, Any]] = ...,
            structured_content: object = ...,
            is_error: bool = ...,
            meta: Mapping[str, JsonValue] = ...,
            value: object = ...,
            annotations: Mapping[str, JsonValue] = ...,
        ) -> None: ...

    @model_validator(mode="wrap")
    @classmethod
    def _accept_aliases_and_mcp_blocks(cls, data: Any, handler: ModelWrapValidatorHandler[Self]) -> Self:
        if not isinstance(data, Mapping):
            return handler(data)
        values = dict(data)
        if "value" in values:
            warnings.warn(
                "ToolResult(value=...) is deprecated; use structured_content=",
                DeprecationWarning,
                stacklevel=3,
            )
            if "structured_content" in values:
                raise ValueError("pass structured_content or value, not both")
            values["structured_content"] = values.pop("value")
        if "annotations" in values:
            warnings.warn(
                "ToolResult(annotations=...) is deprecated; use meta=",
                DeprecationWarning,
                stacklevel=3,
            )
            if "meta" in values:
                raise ValueError("pass meta or annotations, not both")
            values["meta"] = values.pop("annotations")
        structured_model: type[BaseModel] | None = None
        if isinstance(values.get("structured_content"), BaseModel):
            structured_model = type(values["structured_content"])
            # By alias, as the output schema names the fields.
            values["structured_content"] = values["structured_content"].model_dump(mode="json", by_alias=True)
        content = values.get("content")
        if isinstance(content, Sequence) and not isinstance(content, str):
            values["content"] = to_session_blocks(content)
        result = handler(values)
        if structured_model is not None:
            result._structured_model = (structured_model, result.structured_content)
        return result

    @field_validator("content")
    @classmethod
    def _refuse_unsupported_blocks(cls, content: list[ContentBlock]) -> list[ContentBlock]:
        # The model sees this content, so it must hold only blocks a Turn can run.
        return refuse_unsupported_blocks(content)

    @property
    def value(self) -> JsonValue:
        """Deprecated: read ``structured_content``."""
        return self.structured_content

    @property
    def annotations(self) -> dict[str, JsonValue]:
        """Deprecated: read ``meta``."""
        return self.meta

    @classmethod
    def error(
        cls,
        message: str,
        *,
        structured_content: JsonValue | BaseModel = None,
        meta: Mapping[str, JsonValue] | None = None,
    ) -> Self:
        """A tool execution error the model sees as ``message`` and can act on.

        Args:
            message: What the model sees.
            structured_content: Machine-readable output that goes with the failed result.
            meta: Metadata for the client, as MCP's ``_meta``. Never shown to the model.
        """
        values: dict[str, Any] = {
            "content": [TextContentBlock(text=message)],
            "is_error": True,
            "meta": dict(meta or {}),
        }
        if structured_content is not None:
            values["structured_content"] = structured_content
        return cls.model_validate(values)


def structured_content_model(result: ToolResult) -> type[BaseModel] | None:
    """The model class ``structured_content`` was dumped from, if it was a Pydantic model."""
    source = result._structured_model
    if source is None:
        return None
    model, dump = source
    # Only while ``structured_content`` is still that dump: ``model_copy(update=...)`` keeps
    # private attributes but may replace the value.
    return model if result.structured_content is dump else None


_RICH_RESULT_TYPES = (ToolResult, mcp_types.CallToolResult, *SESSION_CONTENT_BLOCK_TYPES, *MCP_CONTENT_BLOCK_TYPES)


def is_content_block(value: object) -> bool:
    return isinstance(value, SESSION_CONTENT_BLOCK_TYPES + MCP_CONTENT_BLOCK_TYPES)


def is_rich_tool_result(value: object) -> bool:
    """Whether a handler returned a ToolResult, content blocks or an MCP result."""
    if isinstance(value, ToolResult | mcp_types.CallToolResult) or is_content_block(value):
        return True
    return isinstance(value, list) and bool(value) and all(is_content_block(item) for item in value)


def is_rich_tool_result_type(annotation: object) -> bool:
    """Whether a return annotation names a ToolResult, an MCP result or content blocks.

    Such an annotation does not describe the structured output, so it gives no output schema.
    """
    if isinstance(annotation, TypeAliasType):
        return is_rich_tool_result_type(annotation.__value__)
    if isinstance(annotation, type):
        return issubclass(annotation, _RICH_RESULT_TYPES)
    origin = get_origin(annotation)
    if origin is Annotated:
        return is_rich_tool_result_type(get_args(annotation)[0])
    if origin is Union or origin is UnionType or (isinstance(origin, type) and issubclass(origin, Sequence)):
        arguments = [argument for argument in get_args(annotation) if argument is not Ellipsis]
        return bool(arguments) and all(is_rich_tool_result_type(argument) for argument in arguments)
    return False


def to_session_blocks(blocks: Sequence[object]) -> list[ContentBlock]:
    """Accept Session blocks, MCP blocks, and their JSON forms."""

    converted: list[ContentBlock] = []
    for block in blocks:
        if isinstance(block, SESSION_CONTENT_BLOCK_TYPES):
            converted.append(block)
        elif isinstance(block, MCP_CONTENT_BLOCK_TYPES):
            converted.extend(to_session_content(from_mcp_content([block])))
        else:
            converted.append(_CONTENT_BLOCK_ADAPTER.validate_python(block))
    return converted


__all__ = [
    "ContentAnnotations",
    "ToolResult",
    "is_content_block",
    "is_rich_tool_result",
    "is_rich_tool_result_type",
    "to_session_blocks",
]
