"""LangChain BaseTool adapter (FR-008).

Provides ``to_langchain_tool()`` which converts a ``ToolDefinition``
into a LangChain ``BaseTool`` subclass.  LangChain imports are lazy —
``ImportError`` is raised only when this function is called.
"""

from __future__ import annotations

from typing import Any

from .definition import ToolDefinition
from .executor import ToolExecutor


def to_langchain_tool(definition: ToolDefinition, executor: ToolExecutor, *, node_name: str = "") -> Any:
    """Convert a tool definition to a LangChain BaseTool instance.

    Args:
        definition: The tool definition to convert.
        executor: The executor to invoke when the tool is called.
        node_name: The graph node that owns this tool adapter. Passed to
            ``ToolExecutor.execute()`` so external-mutation and destructive
            tools carry the correct node context for idempotency tracking
            (FR-006). Required for tools classified as external_mutation or
            destructive; may be left empty for read-only / local-mutation tools.

    Raises:
        ImportError: If ``langchain-core`` is not installed.
    """
    try:
        from langchain_core.tools import BaseTool
    except ImportError as exc:
        raise ImportError(
            "langchain-core is required for LangChain tool adapters. Install with: pip install agentic-devtools"
        ) from exc

    try:
        from pydantic import create_model
    except ImportError as exc:  # pragma: no cover
        raise ImportError(
            "pydantic is required for LangChain tool adapters. Install with: pip install pydantic"
        ) from exc

    # Build Pydantic model from input_schema
    fields: dict[str, Any] = {}
    properties = definition.input_schema.get("properties", {})
    required = set(definition.input_schema.get("required", []))

    for field_name, field_schema in properties.items():
        field_type = _json_type_to_python(field_schema.get("type", "string"))
        allows_null = _schema_allows_null(field_schema)
        if field_name in required:
            required_type = field_type | None if allows_null else field_type
            fields[field_name] = (required_type, ...)
        else:
            # Optional field: use Optional[type] (allows null) only when the
            # JSON Schema explicitly allows null.  Otherwise keep the type
            # non-nullable but give it a default of None so callers may omit
            # the key — this keeps the Pydantic schema aligned with the JSON
            # Schema contract (explicit None still fails Pydantic validation).
            if allows_null:
                fields[field_name] = (field_type | None, None)
            else:
                fields[field_name] = (field_type, None)

    args_model = create_model(f"{definition.name}_args", **fields)

    tool_name = definition.name
    tool_desc = definition.description
    tool_executor = executor
    captured_node_name = node_name

    class _AdaptedTool(BaseTool):  # type: ignore[misc]
        name: str = tool_name  # type: ignore[assignment]
        description: str = tool_desc  # type: ignore[assignment]
        args_schema: type = args_model  # type: ignore[assignment]

        def _run(self, **kwargs: Any) -> str:
            result = tool_executor.execute(tool_name, kwargs, node_name=captured_node_name)
            return result.to_json()

    return _AdaptedTool()


def _json_type_to_python(json_type: str | list[str]) -> type:
    """Map JSON Schema type to Python type.

    Handles both a single type string (e.g. ``"string"``) and the Draft
    2020-12 list form (e.g. ``["string", "null"]``).  For list types the
    first non-``"null"`` string entry is used; non-string entries (e.g.
    nested lists) are skipped.  Returns ``str`` when no usable type is found.
    """
    _mapping: dict[str, type] = {
        "string": str,
        "integer": int,
        "number": float,
        "boolean": bool,
        "array": list,
        "object": dict,
    }
    if isinstance(json_type, list):
        # Pick first non-null string type; skip nested lists and other
        # non-string entries (not valid in Draft 2020-12, but be defensive).
        for t in json_type:
            if isinstance(t, str) and t != "null":
                return _mapping.get(t, str)
        return str
    return _mapping.get(json_type, str)


def _schema_allows_null(field_schema: dict[str, Any]) -> bool:
    """Return True when a JSON Schema field type explicitly allows ``null``."""
    schema_type = field_schema.get("type")
    if isinstance(schema_type, list):
        return "null" in schema_type
    return schema_type == "null"
