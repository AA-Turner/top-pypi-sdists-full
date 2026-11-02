"""Turn what an authored tool handler returned into a Runtime tool result."""

from collections.abc import Sequence
from typing import TypeGuard

from mcp import types as mcp_types
from pydantic import BaseModel, JsonValue, TypeAdapter, ValidationError
from pydantic_core import to_jsonable_python

from mistralai.vibe.harness.app_server.session import TextContentBlock
from mistralai.vibe.harness.core import protocol as core_protocol
from mistralai.vibe.harness.runtime.capabilities import (
    ProvidedToolInvocationFailed,
    ProvidedToolInvocationSucceeded,
)
from mistralai.vibe.harness.runtime.content import (
    to_core_content,
    to_model_json_text,
    tool_returned_error,
)
from mistralai.vibe.harness.runtime.hosts.mcp_results import from_mcp_result
from mistralai.vibe.sdk.capabilities.types import ToolResult as LegacyToolResult
from mistralai.vibe_agents.sdk.authoring.tool_result import (
    ToolResult,
    is_content_block,
    structured_content_model,
    to_session_blocks,
)

MAX_SCHEMA_ERROR_CHARS = 500

_JSON_VALUE_ADAPTER: TypeAdapter[JsonValue] = TypeAdapter(JsonValue)

type ProvidedToolResult = ProvidedToolInvocationSucceeded | ProvidedToolInvocationFailed


def to_provided_tool_result(value: object, *, result_schema: type[BaseModel] | None) -> ProvidedToolResult:
    """Normalise a handler's return value.

    Raises ``ValueError`` for blocks that are not valid content (an image that is not a URL or
    a base64 data URI, invalid base64), and for a value that is not JSON. The caller handles it as an
    exception of the tool, by ``tool_errors``.
    """

    if isinstance(value, mcp_types.CallToolResult):
        return _from_mcp_call_tool_result(value, result_schema=result_schema)
    if result_schema is not None and _is_schema_instance(value, result_schema):
        # Already an instance of the output schema: its dump, by alias and with computed
        # fields, is what the advertised schema describes; validating it again could refuse it.
        result_schema = None
    result = _to_tool_result(value)
    content = to_core_content(result.content)
    return _provided(
        content=content,
        structured_content=result.structured_content,
        has_structured_content="structured_content" in result.model_fields_set,
        is_error=result.is_error,
        meta=result.meta,
        result_schema=result_schema,
    )


def _is_schema_instance(value: object, result_schema: type[BaseModel]) -> bool:
    if isinstance(value, ToolResult):
        model = structured_content_model(value)
        return model is not None and issubclass(model, result_schema)
    return isinstance(value, result_schema)


def _to_tool_result(value: object) -> ToolResult:
    if isinstance(value, ToolResult):
        return value
    if isinstance(value, LegacyToolResult):
        structured = to_json_value(value.value)
        return ToolResult(
            content=[
                TextContentBlock(text=value.value if isinstance(value.value, str) else to_model_json_text(structured))
            ],
            structured_content=structured,
            meta=dict(value.annotations),
        )
    if is_content_block(value):
        return ToolResult(content=to_session_blocks([value]))
    if _is_block_list(value):
        return ToolResult(content=to_session_blocks(value))
    structured = to_json_value(value)
    return ToolResult(content=[TextContentBlock(text=_visible_text(value, structured))], structured_content=structured)


def _is_block_list(value: object) -> TypeGuard[Sequence[object]]:
    return (
        isinstance(value, Sequence)
        and not isinstance(value, str | bytes)
        and bool(value)
        and all(is_content_block(item) for item in value)
    )


def _visible_text(value: object, structured: JsonValue | None = None) -> str:
    if isinstance(value, str):
        return value
    return to_model_json_text(structured if structured is not None else to_json_value(value))


def _from_mcp_call_tool_result(
    value: mcp_types.CallToolResult, *, result_schema: type[BaseModel] | None
) -> ProvidedToolResult:
    parts = from_mcp_result(value)
    return _provided(
        content=parts.content,
        structured_content=parts.structured_content,
        has_structured_content=parts.has_structured_content,
        is_error=parts.is_error,
        meta=parts.meta or {},
        result_schema=result_schema,
    )


def _provided(
    *,
    content: list[core_protocol.ContentBlock],
    structured_content: JsonValue,
    has_structured_content: bool,
    is_error: bool,
    meta: dict[str, JsonValue],
    result_schema: type[BaseModel] | None,
) -> ProvidedToolResult:
    if not content and has_structured_content and structured_content is not None:
        # MCP: a tool that returns structured content SHOULD also return it serialized as text.
        content = [core_protocol.TextContentBlock(text=_visible_text(structured_content))]
    fields: dict[str, object] = {"content": content, "metadata": meta, "annotations": meta}
    if has_structured_content:
        fields["structured_content"] = structured_content
    if is_error:
        return ProvidedToolInvocationFailed.model_validate({**fields, "error": tool_returned_error(content)})
    if result_schema is not None and has_structured_content:
        try:
            result_schema.model_validate(structured_content)
        except ValidationError as error:
            # The call fails and the structured value is dropped, so code calling the tool gets
            # the error and never an unchecked value; the model still sees what the tool returned.
            mismatch = f"structured result did not match output_schema: {_validation_summary(error)}"
            return ProvidedToolInvocationFailed.model_validate(
                {
                    "content": [core_protocol.TextContentBlock(text=mismatch), *content],
                    "metadata": meta,
                    "annotations": meta,
                    "error": core_protocol.ProtocolError(
                        code="tool_output_schema_mismatch", message=mismatch, retryable=False, details=None
                    ),
                }
            )
    return ProvidedToolInvocationSucceeded.model_validate(fields)


def _validation_summary(error: ValidationError) -> str:
    summary = "; ".join(
        f"{'.'.join(str(part) for part in item['loc']) or '<root>'}: {item['msg']}"
        for item in error.errors(include_url=False)
    )
    if len(summary) > MAX_SCHEMA_ERROR_CHARS:
        return summary[: MAX_SCHEMA_ERROR_CHARS - 1] + "…"
    return summary


def to_json_value(value: object) -> JsonValue:
    # Models, also inside lists and dicts, by alias: a tool's output schema names their fields by alias.
    return _JSON_VALUE_ADAPTER.validate_python(to_jsonable_python(value, by_alias=True))


__all__ = ["to_json_value", "to_provided_tool_result"]
