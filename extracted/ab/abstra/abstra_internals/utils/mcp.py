import inspect
import json
from functools import wraps
from typing import (
    Any,
    Callable,
    Dict,
    Optional,
)

from flask import Blueprint, jsonify, request

from .json_schema import (
    coerce_and_validate,
    get_function_json_schema,
    get_function_metadata,
)


def validate_and_coerce_arguments(
    arguments: Dict[str, Any],
    input_schema: Dict[str, Any],
    tool_name: str,
) -> Dict[str, Any]:
    """Validate and coerce tool arguments with instructive error messages.

    Performs staged validation:
    1. Coerce types (semantic tolerance for LLM outputs)
    2. Validate types against schema
    3. Check required fields
    4. Return coerced arguments or raise with helpful message
    """
    properties = input_schema.get("properties", {})
    required = input_schema.get("required", [])

    # Stage 1: Check required fields
    missing = [r for r in required if r not in arguments]
    if missing:
        available = list(properties.keys())
        raise TypeError(
            f"Missing required parameter(s) for '{tool_name}': {', '.join(missing)}. "
            f"Expected parameters: {', '.join(available)}"
        )

    # Stage 2: Coerce and validate each provided argument
    for prop, prop_schema in properties.items():
        if prop not in arguments:
            continue

        coerced, valid = coerce_and_validate(arguments[prop], prop_schema)
        arguments[prop] = coerced

        if not valid:
            expected = prop_schema.get("type", "unknown")
            got = type(coerced).__name__
            hint = ""
            if expected == "integer" and isinstance(coerced, str):
                hint = ' (hint: pass a number like 30, not a string like "30")'
            elif expected == "boolean" and isinstance(coerced, str):
                hint = " (hint: pass true/false, not a string)"
            elif expected == "array" and isinstance(coerced, dict):
                hint = " (hint: pass a list [...], not an object {...})"
            raise TypeError(
                f"Invalid type for '{prop}' in '{tool_name}': "
                f"expected {expected}, got {got}{hint}"
            )

    return arguments


_SERIALIZATION_METHODS = ("model_dump", "dict", "to_dict")


def _to_serializable(result: Any) -> Any:
    """Convert an object to a JSON-serializable Python type."""
    for method in _SERIALIZATION_METHODS:
        fn = getattr(result, method, None)
        if fn is not None:
            return fn()
    if hasattr(result, "__dict__") and not isinstance(
        result, (str, int, float, bool, type(None))
    ):
        return result.__dict__
    return result


def _pagination_hints(data: dict) -> list[str]:
    """Extract pagination hints from a dict result."""
    hints: list[str] = []
    if data.get("truncated"):
        total = data.get("total_matches") or data.get("total_lines") or "unknown"
        returned = data.get("matches_returned") or data.get("end_line") or "unknown"
        hints.append(f"Results truncated: showing {returned} of {total}")
    if data.get("has_more"):
        end = data.get("end_line", "?")
        next_start = end + 1 if isinstance(end, int) else "?"
        hints.append(f"More content available. Use start_line={next_start} to continue")
    return hints


def serialize_tool_result(result: Any) -> str:
    """Serialize a tool result to a JSON string with pagination hints."""
    data = _to_serializable(result)

    if data is None:
        return "null (resource not found or not accessible)"

    def _json(obj: Any) -> str:
        try:
            return json.dumps(obj, indent=2, default=str, ensure_ascii=False)
        except (TypeError, ValueError):
            return str(obj)

    if isinstance(data, dict):
        text = _json(data)
        hints = _pagination_hints(data)
        if hints:
            text += "\n\n[" + " | ".join(hints) + "]"
        return text

    if isinstance(data, list):
        text = _json(data)
        if data:
            text += f"\n\n[Returned {len(data)} items]"
        return text

    return str(data)


def requires_approval(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    wrapper._requires_approval = True  # type: ignore
    return wrapper


def register_function(
    blueprint: Blueprint,
    func: Callable,
    tools_registry: Optional[Dict[str, Dict[str, Any]]] = None,
    custom_name: Optional[str] = None,
):
    """Decorator to register a function as an MCP tool with automatic metadata generation"""

    input_schema = get_function_json_schema(func)
    tool_metadata = get_function_metadata(func)

    func_name = custom_name or func.__name__
    parameters = list(inspect.signature(func).parameters.values())

    if tools_registry is not None:
        if custom_name:
            tool_metadata = tool_metadata.copy()
            tool_metadata["name"] = custom_name
        tools_registry[func_name] = tool_metadata

    # Register the function in MCP_TOOLS
    def create_tool_endpoint():
        def tool_endpoint():
            try:
                if parameters:
                    # Function with parameters - extract from JSON and pass as keyword arguments
                    input_data = request.get_json() or {}

                    # Reuse the same staged validation as the MCP handler
                    try:
                        input_data = validate_and_coerce_arguments(
                            input_data, input_schema, func_name
                        )
                    except TypeError as e:
                        return jsonify({"error": str(e)}), 400

                    # Convert parameter names and values based on function signature
                    kwargs = {}
                    for param in parameters:
                        param_name = param.name
                        if param_name in input_data:
                            kwargs[param_name] = input_data[param_name]
                        elif param.default != inspect.Parameter.empty:
                            kwargs[param_name] = param.default

                    result = func(**kwargs)
                else:
                    # Function with no parameters - call directly
                    result = func()

                # Return the result as JSON
                if hasattr(result, "dict"):
                    return jsonify(result.dict())
                elif hasattr(result, "__dict__"):
                    return jsonify(result.__dict__)
                else:
                    return jsonify(result)

            except Exception as e:
                return jsonify({"error": str(e)}), 400

        return tool_endpoint

    # Add route with unique endpoint name
    blueprint.add_url_rule(
        f"/tools/{func_name}",
        endpoint=f"tool_{func_name}",
        view_func=create_tool_endpoint(),
        methods=["POST"],
    )


def create_mcp_tool_handler(
    tools_registry: Dict[str, Dict[str, Any]], registered_functions: Dict[str, Callable]
) -> Callable:
    """Create a dynamic tool handler that can call any registered function"""

    def handle_tool_call(tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        # Validate tool existence
        if tool_name not in registered_functions:
            raise ValueError(f"Unknown tool: {tool_name}")

        func = registered_functions[tool_name]
        func_signature = inspect.signature(func)
        parameters = list(func_signature.parameters.values())

        # Get input schema for this tool
        input_schema = tools_registry.get(tool_name, {}).get("inputSchema", {})

        # Staged validation with coercion and instructive errors
        arguments = validate_and_coerce_arguments(arguments, input_schema, tool_name)

        if parameters:
            # Function with parameters - extract from arguments dict and pass as keyword arguments
            kwargs = {}
            for param in parameters:
                param_name = param.name
                if param_name in arguments:
                    kwargs[param_name] = arguments[param_name]
                elif param.default != inspect.Parameter.empty:
                    # Use default value if provided
                    kwargs[param_name] = param.default
                # If parameter is required but not provided, let the function handle the error

            result = func(**kwargs)
        else:
            # Function with no parameters
            result = func()

        # Handle result serialization with structured metadata
        result_text = serialize_tool_result(result)

        return {"content": [{"type": "text", "text": result_text}]}

    return handle_tool_call
