"""BAML execution utilities for the Bitfab Python SDK.

This module provides functions to execute BAML prompts dynamically on the client side.
"""

import contextlib
import json
import logging
import re
from dataclasses import dataclass
from typing import Any, Optional

from pydantic import BaseModel, create_model

logger = logging.getLogger(__name__)

# Allowed environment variable keys for LLM providers
ALLOWED_ENV_KEYS = ["OPENAI_API_KEY"]


@dataclass
class BamlExecutionResult:
    """Result of a BAML function execution with raw collector data."""

    result: Any
    raw_collector: Optional[dict[str, Any]] = None


class ProviderDefinition:
    """Provider definition from the server."""

    def __init__(self, provider: str, api_key_env: str, models: list[dict[str, str]]):
        self.provider = provider
        self.api_key_env = api_key_env
        self.models = models


def filter_env_vars(env_vars: dict[str, str]) -> dict[str, str]:
    """Filter environment variables to only include allowed keys.

    This prevents accidentally passing sensitive environment variables to the BAML runtime.

    Args:
        env_vars: Environment variables dictionary

    Returns:
        Filtered dictionary with only allowed keys
    """
    filtered = {}
    for key in ALLOWED_ENV_KEYS:
        if key in env_vars:
            filtered[key] = env_vars[key]
    return filtered


def parse_baml_class_to_pydantic(
    baml_source: str, class_name: str
) -> Optional[type[BaseModel]]:
    """Parse a BAML class definition and create a Pydantic model.

    Args:
        baml_source: The BAML source code
        class_name: The name of the class to parse

    Returns:
        A dynamically created Pydantic model, or None if parsing fails
    """
    # Find the class definition
    class_pattern = rf"class\s+{re.escape(class_name)}\s*\{{([^}}]+)\}}"
    class_match = re.search(class_pattern, baml_source, re.DOTALL)

    if not class_match:
        return None

    class_body = class_match.group(1)

    # Parse fields: field_name type? @description("...")
    field_pattern = r"(\w+)\s+(string|int|float|bool)(\?)?"
    fields = {}

    for match in re.finditer(field_pattern, class_body):
        field_name = match.group(1)
        field_type_str = match.group(2)
        is_optional = match.group(3) == "?"

        # Map BAML types to Python types
        type_map = {
            "string": str,
            "int": int,
            "float": float,
            "bool": bool,
        }

        field_type = type_map.get(field_type_str, str)

        if is_optional:
            fields[field_name] = (Optional[field_type], None)
        else:
            fields[field_name] = (field_type, ...)

    if not fields:
        return None

    # Create Pydantic model dynamically
    try:
        return create_model(class_name, **fields)
    except Exception as e:
        logger.warning(f"Failed to create Pydantic model for {class_name}: {e}")
        return None


def extract_function_name(baml_source: str) -> Optional[str]:
    """Extract the first function name from BAML source code.

    Args:
        baml_source: BAML source code

    Returns:
        Function name or None if not found
    """
    match = re.search(r"function\s+(\w+)\s*\(", baml_source)
    return match.group(1) if match else None


@dataclass
class BamlParameterType:
    """Parameter type information extracted from BAML function signature."""

    name: str
    type: str
    is_optional: bool


def extract_function_parameters(baml_source: str) -> list[BamlParameterType]:
    """Extract function parameter names and types from BAML source code.

    Used to properly coerce inputs based on expected types.

    Args:
        baml_source: The BAML source code

    Returns:
        List of parameter info with name, type, and optionality
    """
    # Match function signature: function Name(param1: type1, param2: type2?) -> ReturnType
    function_match = re.search(r"function\s+\w+\s*\(([^)]*)\)\s*->", baml_source)
    if not function_match:
        return []

    params_string = function_match.group(1).strip()
    if not params_string:
        return []

    params: list[BamlParameterType] = []

    # Split by comma, handling potential nested types like Map<string, int>
    param_parts = _split_parameters(params_string)

    for part in param_parts:
        trimmed = part.strip()
        if not trimmed:
            continue

        # Match: paramName: type or paramName: type?
        param_match = re.match(r"^(\w+)\s*:\s*(.+)$", trimmed)
        if param_match:
            name = param_match.group(1)
            param_type = param_match.group(2).strip()
            is_optional = param_type.endswith("?")
            if is_optional:
                param_type = param_type[:-1]
            params.append(
                BamlParameterType(name=name, type=param_type, is_optional=is_optional)
            )

    return params


def _split_parameters(params_string: str) -> list[str]:
    """Split parameter string by commas, respecting nested angle brackets."""
    parts: list[str] = []
    current = ""
    depth = 0

    for char in params_string:
        if char == "<":
            depth += 1
            current += char
        elif char == ">":
            depth -= 1
            current += char
        elif char == "," and depth == 0:
            parts.append(current)
            current = ""
        else:
            current += char

    if current.strip():
        parts.append(current)

    return parts


def _coerce_to_type(value: str, expected_type: str) -> Any:
    """Coerce a single string value to the expected BAML type.

    Returns the coerced value, or the original string if coercion fails.
    """
    # String type - keep as is
    if expected_type == "string":
        return value

    # Integer type
    if expected_type == "int":
        try:
            return int(value)
        except ValueError:
            return value

    # Float type
    if expected_type == "float":
        try:
            return float(value)
        except ValueError:
            return value

    # Boolean type
    if expected_type == "bool":
        lower = value.lower()
        if lower == "true":
            return True
        if lower == "false":
            return False
        return value

    # Array types (e.g., string[], int[])
    if expected_type.endswith("[]"):
        try:
            parsed = json.loads(value)
            if isinstance(parsed, list):
                return parsed
        except (json.JSONDecodeError, ValueError):
            pass
        return value

    # Complex types (objects, classes, maps) - try JSON parse
    try:
        return json.loads(value)
    except (json.JSONDecodeError, ValueError):
        return value


def coerce_inputs(
    inputs: dict[str, Any], expected_types: Optional[dict[str, str]] = None
) -> dict[str, Any]:
    """Coerce input values from strings to their appropriate types based on expected BAML types.

    Actively coerces to the expected type (int, float, bool, etc.) rather than just avoiding
    unintended conversions.

    Args:
        inputs: Input dictionary from web UI (all values are strings)
        expected_types: Map of parameter names to their expected BAML types

    Returns:
        Coerced input dictionary with proper types
    """
    if expected_types is None:
        expected_types = {}

    coerced = {}

    for key, value in inputs.items():
        if isinstance(value, str):
            expected_type = expected_types.get(key)

            if expected_type:
                # Coerce to the expected type
                coerced[key] = _coerce_to_type(value, expected_type)
            else:
                # No expected type info - keep as string
                coerced[key] = value
        else:
            coerced[key] = value

    return coerced


def format_provider(provider: str) -> str:
    """Convert provider name to PascalCase.

    Args:
        provider: Provider name (e.g., "openai")

    Returns:
        Formatted provider name (e.g., "OpenAI")
    """
    provider_map = {
        "openai": "OpenAI",
        "anthropic": "Anthropic",
        "google": "Google",
    }
    return provider_map.get(provider, provider.capitalize())


def format_model(model: str) -> str:
    """Convert a model name to a valid BAML identifier part.

    Args:
        model: Model name (e.g., "gpt-5-mini")

    Returns:
        Formatted model name (e.g., "GPT5_mini")
    """
    return (
        model.replace("gpt-", "GPT")  # gpt- prefix -> GPT
        .replace(".", "_")  # dots -> underscore
        .replace("-", "_")  # hyphens -> underscore
    )


def get_client_name(provider: str, model: str) -> str:
    """Generate the BAML client name from provider and model.

    Args:
        provider: Provider name
        model: Model name

    Returns:
        BAML client name (e.g., "OpenAI_GPT4_1_mini")
    """
    return f"{format_provider(provider)}_{format_model(model)}"


def generate_client_definitions(providers: list[ProviderDefinition]) -> str:
    """Generate BAML client definition strings.

    BamlRuntime requires clients to be defined in source for parsing.

    Args:
        providers: List of provider definitions

    Returns:
        BAML client definitions as a string
    """
    definitions = []

    for provider_def in providers:
        for model in provider_def.models:
            client_name = get_client_name(provider_def.provider, model["model"])
            definitions.append(
                f"""client<llm> {client_name} {{
  provider {provider_def.provider}
  options {{
    model "{model["model"]}"
    api_key env.{provider_def.api_key_env}
  }}
}}"""
            )

    return "\n\n".join(definitions)


def with_default_clients(baml_source: str, providers: list[ProviderDefinition]) -> str:
    """Prepend the default client definitions to a BAML source if it doesn't already define them.

    Args:
        baml_source: BAML source code
        providers: List of provider definitions

    Returns:
        BAML source with client definitions
    """
    if "client<llm> OpenAI_" in baml_source:
        return baml_source

    default_clients = generate_client_definitions(providers)
    return f"{default_clients}\n\n{baml_source}"


def _obj_to_dict(obj: Any, depth: int = 0, max_depth: int = 5) -> Any:
    """Recursively convert an object to a JSON-serializable dict."""
    if depth > max_depth:
        return f"<max depth reached: {type(obj).__name__}>"

    if obj is None or isinstance(obj, (str, int, float, bool)):
        return obj

    if isinstance(obj, (list, tuple)):
        return [_obj_to_dict(item, depth + 1, max_depth) for item in obj]

    if isinstance(obj, dict):
        return {k: _obj_to_dict(v, depth + 1, max_depth) for k, v in obj.items()}

    # For objects, try to extract their attributes
    result = {"__type__": type(obj).__name__}
    for attr in dir(obj):
        if attr.startswith("_"):
            continue
        try:
            value = getattr(obj, attr)
            if callable(value):
                continue
            result[attr] = _obj_to_dict(value, depth + 1, max_depth)
        except Exception as e:
            result[attr] = f"<error: {e}>"

    return result


async def run_function_with_baml(
    baml_source: str,
    inputs: dict[str, Any],
    providers: list[dict[str, Any]],
    env_vars: dict[str, str],
) -> BamlExecutionResult:
    """Run the BAML function with the given inputs using the BAML runtime directly.

    Note: This requires the baml-py package to be installed.

    Args:
        baml_source: The BAML source code containing the function
        inputs: Named arguments to pass to the function
        providers: Available provider definitions
        env_vars: Environment variables for API keys (only OPENAI_API_KEY is allowed)

    Returns:
        BamlExecutionResult containing the result and execution metadata

    Raises:
        ImportError: If baml-py is not installed
        ValueError: If no function found in BAML source
        RuntimeError: If BAML function execution failed
    """
    try:
        from baml_py import BamlRuntime, Collector
    except ImportError as err:
        raise ImportError(
            "baml-py is required for local execution. Install it with: pip install baml-py"
        ) from err

    # Extract function name from the BAML source
    function_name = extract_function_name(baml_source)
    if not function_name:
        raise ValueError("No function found in BAML source")

    # Convert provider dicts to ProviderDefinition objects
    provider_objs = [
        ProviderDefinition(p["provider"], p["apiKeyEnv"], p["models"])
        for p in providers
    ]

    # Add default client definitions (runtime needs them for parsing)
    full_source = with_default_clients(baml_source, provider_objs)

    # Filter env vars to only allowed keys
    filtered_env_vars = filter_env_vars(env_vars)

    # Create runtime from source with env vars
    runtime = BamlRuntime.from_files(
        "/tmp/baml_runtime", {"source.baml": full_source}, filtered_env_vars
    )

    # Create context manager
    ctx = runtime.create_context_manager()

    # Create collector to capture execution metadata
    collector = Collector("bitfab-collector")

    # Extract expected parameter types from BAML source
    params = extract_function_parameters(baml_source)
    expected_types = {p.name: p.type for p in params}

    # Coerce inputs from strings to proper types based on BAML signature
    args = coerce_inputs(inputs, expected_types)

    # Call the function with all required arguments
    # Signature: call_function(function_name, args, ctx, tb, cb, collectors, env_vars, tags)
    result = await runtime.call_function(
        function_name,
        args,
        ctx,
        None,  # tb (TypeBuilder)
        None,  # cb (ClientRegistry)
        [collector],  # collectors - capture execution data
        filtered_env_vars,
        {},  # tags
    )

    if not result.is_ok():
        raise RuntimeError("BAML function execution failed")

    # Serialize the collector to a dict for the server to parse
    raw_collector = None
    try:
        raw_collector = _obj_to_dict(collector)
    except Exception as e:
        logger.warning(f"Failed to serialize collector: {e}")

    # Extract the parsed result directly from the BAML result object
    # The Python BAML library uses a different API than TypeScript
    # Try different methods to get the parsed result
    parsed_result = None

    # Try method 1: .value() or .get_value()
    if hasattr(result, "value"):
        with contextlib.suppress(Exception):
            parsed_result = result.value()

    # Try method 2: Direct property access
    if parsed_result is None and hasattr(result, "value"):
        with contextlib.suppress(Exception):
            parsed_result = result.value

    # Try method 3: unstable_internal_repr() and parse it properly
    if parsed_result is None:
        try:
            internal_json = result.unstable_internal_repr()
            internal_data = json.loads(internal_json)

            # The structure should be: {"Success": {"content": <parsed_object>, ...}}
            if "Success" in internal_data:
                success_data = internal_data["Success"]

                # Check if content is already a dict/object
                if "content" in success_data:
                    content = success_data["content"]

                    # If content is a string, try to parse it as JSON
                    if isinstance(content, str):
                        # Strip markdown code fence if present
                        stripped_content = content.strip()
                        if stripped_content.startswith("```"):
                            # Remove opening fence (```json or ```)
                            lines = stripped_content.split("\n")
                            if lines[0].startswith("```"):
                                lines = lines[1:]
                            # Remove closing fence
                            if lines and lines[-1].strip() == "```":
                                lines = lines[:-1]
                            stripped_content = "\n".join(lines).strip()

                        try:
                            parsed_result = json.loads(stripped_content)
                        except json.JSONDecodeError:
                            # Content might not be JSON, use as-is
                            parsed_result = content
                    else:
                        # Content is already parsed
                        parsed_result = content
        except Exception as e:
            logger.error(f"Failed to extract result from unstable_internal_repr: {e}")

    if parsed_result is None:
        raise RuntimeError("Failed to get parsed result from BAML: no method worked")

    # Convert the parsed result to a dict if it's not already
    if isinstance(parsed_result, dict):
        result_dict = parsed_result
    else:
        # If it's a Pydantic model or other object, try to convert to dict
        try:
            if hasattr(parsed_result, "model_dump"):
                result_dict = parsed_result.model_dump()
            elif hasattr(parsed_result, "dict"):
                result_dict = parsed_result.dict()
            elif hasattr(parsed_result, "__dict__"):
                result_dict = parsed_result.__dict__
            else:
                # Fallback: just return the result as-is
                return BamlExecutionResult(
                    result=parsed_result, raw_collector=raw_collector
                )
        except Exception as e:
            logger.warning(
                f"Failed to convert parsed result to dict: {e}, returning as-is"
            )
            return BamlExecutionResult(
                result=parsed_result, raw_collector=raw_collector
            )

    # Try to extract the return type from the function definition
    # Pattern: function FunctionName(...) -> ReturnType {
    return_type_match = re.search(
        rf"function\s+{re.escape(function_name)}\s*\([^)]*\)\s*->\s*(\w+)",
        baml_source,
    )

    if return_type_match:
        return_type_name = return_type_match.group(1)

        # Try to create a Pydantic model from the BAML class definition
        pydantic_model = parse_baml_class_to_pydantic(baml_source, return_type_name)

        if pydantic_model:
            # Return a Pydantic model instance
            try:
                return BamlExecutionResult(
                    result=pydantic_model(**result_dict),
                    raw_collector=raw_collector,
                )
            except Exception as e:
                logger.warning(
                    f"Failed to instantiate Pydantic model: {e}, returning dict"
                )
                return BamlExecutionResult(
                    result=result_dict, raw_collector=raw_collector
                )

    # If we couldn't create a Pydantic model, return the dict
    return BamlExecutionResult(result=result_dict, raw_collector=raw_collector)
