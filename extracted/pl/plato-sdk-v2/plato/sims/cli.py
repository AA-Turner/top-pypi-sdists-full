"""CLI for exploring and publishing simulation APIs.

Usage:
    plato sims list
    plato sims info <sim_name>
    plato sims endpoints <sim_name> [--spec SPEC_NAME] [--tag TAG] [--path PATH] [--code]
    plato sims spec <sim_name> [--spec SPEC_NAME]
    plato sims publish [--config PATH] [--repo NAME] [--dry-run]

Examples:
    # List all available simulators
    plato sims list

    # Get detailed info about a simulator
    plato sims info spree

    # Show tag-level summary (high-level overview of endpoint categories)
    plato sims endpoints spree --spec platform

    # Explore specific category with code examples (imports, signatures, response types)
    plato sims endpoints spree --spec platform --tag Products --code

    # Filter by path substring to find specific endpoints
    plato sims endpoints espocrm --path "/User/{id}/tasks" --code

    # Get the full OpenAPI spec as JSON
    plato sims spec spree --spec platform

    # Publish SDK package (run from sim repo root with plato-config.yml)
    plato sims publish
    plato sims publish --config plato-config.yml --repo sims
    plato sims publish --dry-run  # Build without uploading

Workflow:
    1. Start with tag-level summary to see available categories
    2. Use --tag to explore specific category with --code for implementation details
    3. Use --path to find specific endpoints by URL pattern
"""

import importlib
import inspect
import json
import sys
from typing import get_type_hints

from .registry import registry


def _camel_to_snake(name: str) -> str:
    """Convert camelCase to snake_case."""
    import re

    # Insert an underscore before any uppercase letter that follows a lowercase letter
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    # Insert an underscore before any uppercase letter that follows a lowercase or uppercase letter
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


def format_table(rows: list[list[str]], headers: list[str]) -> str:
    """Format data as a simple text table."""
    if not rows:
        return ""

    # Calculate column widths
    widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(str(cell)))

    # Build table
    lines = []

    # Header
    header_line = "  ".join(h.ljust(w) for h, w in zip(headers, widths))
    lines.append(header_line)
    lines.append("-" * len(header_line))

    # Rows
    for row in rows:
        line = "  ".join(str(cell).ljust(w) for cell, w in zip(row, widths))
        lines.append(line)

    return "\n".join(lines)


def cmd_list() -> None:
    """List all available sims."""
    sims = registry.list_sims()

    if not sims:
        print("No sims found. Install sim packages with: uv add <sim-name> --extra-index-url ...")
        return

    print("Available simulation APIs:\n")
    for sim in sims:
        info = registry.get_sim_info(sim)
        print(f"  {sim}")
        print(f"    {info.title} (v{info.version})")
        if info.auth:
            print(f"    Auth: {info.auth.type}")
        print()


def _get_param_type(schema: dict) -> str:
    """Get Python type hint from OpenAPI schema."""
    schema_type = schema.get("type", "Any")

    # Map OpenAPI types to Python types
    type_map = {
        "string": "str",
        "integer": "int",
        "number": "float",
        "boolean": "bool",
        "array": "list",
        "object": "dict",
    }

    base_type = type_map.get(schema_type, "Any")

    # Handle array types
    if schema_type == "array":
        items = schema.get("items", {})
        item_type = _get_param_type(items)
        return f"list[{item_type}]"

    return base_type


def _format_schema_type(schema: dict, components: dict) -> str:
    """Format schema type for display, including refs and complex types."""
    # Handle $ref
    if "$ref" in schema:
        ref = schema["$ref"]
        # Extract model name from #/components/schemas/ModelName
        if ref.startswith("#/components/schemas/"):
            model_name = ref.split("/")[-1]
            return model_name
        return "dict"

    schema_type = schema.get("type", "")

    if schema_type == "array":
        items = schema.get("items", {})
        item_type = _format_schema_type(items, components)
        return f"list[{item_type}]"
    elif schema_type == "object":
        # Check if it has properties
        properties = schema.get("properties", {})
        if properties:
            return "dict"  # Could expand to show property types
        return "dict"
    elif schema_type:
        return _get_param_type(schema)

    return "dict"


def _get_function_info(
    sim_name: str,
    spec_name: str,
    resource: str,
    operation_id: str,
) -> dict | None:
    """Import and inspect the actual generated function.

    Returns dict with:
        - module_path: full import path
        - function_name: the function name
        - signature: the function signature string
        - body_type: the body parameter type (if any)
        - body_model_source: source code of the body model class (if available)
    """
    try:
        # Build module path - for sims with only "default" spec, don't include spec in path
        if spec_name == "default":
            base_path = f"plato.sims.{sim_name}.api.{resource}"
        else:
            base_path = f"plato.sims.{sim_name}.{spec_name}.api.{resource}"

        # SDK generator converts operationIds to snake_case for Python modules
        # Try multiple variations to find the correct module name
        module = None
        module_name = operation_id
        module_path = ""

        # Variation 1: Convert camelCase to snake_case
        snake_case_name = _camel_to_snake(operation_id)

        # Variation 2: Replace double underscores with single underscores
        # Path parameters like {negotiation_id} create __ in operationIds
        # but SDK converts them to single _ in file names
        # e.g., "negotiations__negotiation_id__get" -> "negotiations_negotiation_id_get"
        no_double_underscore = snake_case_name.replace("__", "_")

        variations = [no_double_underscore, snake_case_name]

        # Variation 3: If already snake_case but has tag prefix, try stripping it
        # For example: "search_listings_search_post" becomes "listings_search_post"
        prefix = f"{resource}_"
        if no_double_underscore.startswith(prefix):
            variations.append(no_double_underscore[len(prefix) :])

        # Try each variation
        for variant in variations:
            try:
                module_path = f"{base_path}.{variant}"
                module = importlib.import_module(module_path)
                module_name = variant
                break
            except (ImportError, ModuleNotFoundError):
                continue

        if module is None:
            return None

        # Get the sync function
        if not hasattr(module, "sync"):
            return None

        sync_fn = module.sync
        sig = inspect.signature(sync_fn)

        # Get type hints
        try:
            hints = get_type_hints(sync_fn)
        except Exception:
            hints = {}

        # Get return type from hints
        return_type = hints.get("return", sig.return_annotation)

        # Build result
        result = {
            "module_path": module_path,
            "function_name": module_name,
            "params": [],
            "body_type": None,
            "body_model_source": None,
            "return_type": return_type,
            "return_type_str": _format_type_annotation(return_type, show_enum_values=False),
        }

        # Extract parameters
        params_list = result["params"]
        assert isinstance(params_list, list)  # type narrowing for ty
        for param_name, param in sig.parameters.items():
            if param_name == "client":
                params_list.append("client.httpx")
                continue

            # Get type from hints or annotation
            param_type = hints.get(param_name, param.annotation)
            type_str = _format_type_annotation(param_type)

            if param.default is inspect.Parameter.empty:
                params_list.append(f"{param_name}: {type_str}")
            else:
                default_repr = repr(param.default) if param.default is not None else "None"
                params_list.append(f"{param_name}: {type_str} = {default_repr}")

            # Check if this is the body parameter
            if param_name == "body" and param_type is not inspect.Parameter.empty:
                result["body_type"] = param_type
                # Try to get the model source
                try:
                    if hasattr(param_type, "__module__") and hasattr(param_type, "__name__"):
                        result["body_model_source"] = _get_model_source(param_type)
                except Exception:
                    pass

        return result

    except (ImportError, AttributeError):
        return None


def _format_type_annotation(annotation, show_enum_values: bool = True) -> str:
    """Format a type annotation for display."""
    if annotation is inspect.Parameter.empty:
        return "Any"

    # Handle None type
    if annotation is type(None):
        return "None"

    # Handle string annotations
    if isinstance(annotation, str):
        return annotation

    # Handle Enum types - show the values
    import enum

    if isinstance(annotation, type) and issubclass(annotation, enum.Enum) and show_enum_values:
        values = [m.value for m in annotation]
        # Show first few values
        if len(values) <= 5:
            return f"{annotation.__name__} (values: {', '.join(repr(v) for v in values)})"
        else:
            shown = ", ".join(repr(v) for v in values[:4])
            return f"{annotation.__name__} (values: {shown}, ... +{len(values) - 4} more)"

    # Handle Union types (including Optional)
    origin = getattr(annotation, "__origin__", None)
    if origin is not None:
        # Handle Union (including Optional which is Union[X, None])
        import types

        if origin is types.UnionType or str(origin) == "typing.Union":
            args = getattr(annotation, "__args__", ())
            # Check if it's Optional (Union with None)
            non_none_args = [a for a in args if a is not type(None)]
            has_none = type(None) in args
            if len(non_none_args) == 1 and has_none:
                inner = _format_type_annotation(non_none_args[0])
                # Avoid double | None
                if inner.endswith(" | None"):
                    return inner
                return f"{inner} | None"
            # Multiple non-None types
            formatted = [_format_type_annotation(a) for a in args if a is not type(None)]
            result = " | ".join(formatted)
            if has_none:
                result += " | None"
            return result
        # Handle list, dict, etc.
        args = getattr(annotation, "__args__", ())
        if args:
            args_str = ", ".join(_format_type_annotation(a) for a in args)
            origin_name = getattr(origin, "__name__", str(origin))
            return f"{origin_name}[{args_str}]"
        return getattr(origin, "__name__", str(origin))

    # Handle regular types
    if hasattr(annotation, "__name__"):
        return annotation.__name__

    # Clean up typing module references
    result = str(annotation)
    result = result.replace("typing.", "")
    return result


def _get_model_source(model_class) -> str | None:
    """Get a simplified source representation of a Pydantic model."""
    if not hasattr(model_class, "__annotations__"):
        return None

    lines = []
    module = getattr(model_class, "__module__", "")
    name = getattr(model_class, "__name__", "")

    # Import line
    if module and name:
        lines.append(f"from {module} import {name}")
        lines.append("")

    # Class definition
    lines.append(f"class {name}(BaseModel):")

    # Try to get resolved type hints (handles forward references)
    try:
        annotations = get_type_hints(model_class)
    except Exception:
        annotations = getattr(model_class, "__annotations__", {})

    if not annotations:
        lines.append("    pass")
        return "\n".join(lines)

    # Get field info for defaults
    model_fields = {}
    if hasattr(model_class, "model_fields"):
        model_fields = model_class.model_fields

    # Collect nested models to show after
    nested_models = []

    for field_name, field_type in annotations.items():
        type_str = _format_type_annotation(field_type)

        # Check if field has a default
        field_info = model_fields.get(field_name)
        is_required = True
        if field_info is not None:
            is_required = field_info.is_required()

        if is_required:
            lines.append(f"    {field_name}: {type_str}")
        else:
            # Only add | None if not already in type
            if " | None" not in type_str:
                lines.append(f"    {field_name}: {type_str} | None = None")
            else:
                lines.append(f"    {field_name}: {type_str} = None")

        # Collect nested models
        actual_type = field_type
        # Unwrap Optional/Union
        if hasattr(field_type, "__origin__"):
            args = getattr(field_type, "__args__", ())
            non_none = [a for a in args if a is not type(None)]
            if non_none:
                actual_type = non_none[0]

        if hasattr(actual_type, "__annotations__") and hasattr(actual_type, "__name__"):
            # Don't show built-in types
            if getattr(actual_type, "__module__", "builtins") not in ("builtins", "typing"):
                nested_models.append(actual_type)

    # Show nested models after the main class
    for nested_type in nested_models:
        nested_lines = _get_nested_model_source(nested_type, indent=0)
        if nested_lines:
            lines.append("")
            lines.extend(nested_lines)

    return "\n".join(lines)


def _get_nested_model_source(model_class, indent: int = 0) -> list[str]:
    """Get source for a nested model (without import)."""
    prefix = "    " * indent
    lines = []
    name = getattr(model_class, "__name__", "")

    lines.append(f"{prefix}class {name}(BaseModel):")

    # Try to get resolved type hints
    try:
        annotations = get_type_hints(model_class)
    except Exception:
        annotations = getattr(model_class, "__annotations__", {})

    if not annotations:
        lines.append(f"{prefix}    pass")
        return lines

    model_fields = {}
    if hasattr(model_class, "model_fields"):
        model_fields = model_class.model_fields

    for field_name, field_type in annotations.items():
        type_str = _format_type_annotation(field_type)

        field_info = model_fields.get(field_name)
        is_required = True
        if field_info is not None:
            is_required = field_info.is_required()

        if is_required:
            lines.append(f"{prefix}    {field_name}: {type_str}")
        else:
            # Only add | None if not already in type
            if " | None" not in type_str:
                lines.append(f"{prefix}    {field_name}: {type_str} | None = None")
            else:
                lines.append(f"{prefix}    {field_name}: {type_str} = None")

    return lines


def _get_response_model_source(sim_name: str, api_name: str, model_name: str) -> str | None:
    """Import and introspect a response model from the SDK."""
    try:
        # Convert snake_case model name to PascalCase
        pascal_name = _to_pascal_case(model_name)

        # Try to import from models - for sims with only "default" spec, don't include spec in path
        if api_name == "default":
            module_path = f"plato.sims.{sim_name}.models"
        else:
            module_path = f"plato.sims.{sim_name}.{api_name}.models"
        module = importlib.import_module(module_path)

        if not hasattr(module, pascal_name):
            return None

        model_class = getattr(module, pascal_name)
        return _get_model_source(model_class)

    except (ImportError, AttributeError):
        return None


def _resolve_ref(ref: str, components: dict) -> tuple[str, dict | None]:
    """Resolve a $ref to its schema definition.

    Returns (model_name, schema_dict).
    """
    if not ref.startswith("#/components/schemas/"):
        return ("dict", None)

    model_name = ref.split("/")[-1]
    schemas = components.get("schemas", {})
    return (model_name, schemas.get(model_name))


def _to_pascal_case(name: str) -> str:
    """Convert snake_case or kebab-case to PascalCase."""
    # Handle already PascalCase names
    if name and name[0].isupper() and "_" not in name and "-" not in name:
        return name
    # Convert snake_case or kebab-case
    parts = name.replace("-", "_").split("_")
    return "".join(word.capitalize() for word in parts)


def _format_model_class(
    model_name: str,
    schema: dict,
    components: dict,
    sim_name: str,
    api_name: str,
    indent: str = "         ",
) -> list[str]:
    """Format a Pydantic model class definition.

    Returns lines showing the class structure with proper types.
    """
    lines = []
    pascal_name = _to_pascal_case(model_name)

    # Import line - for sims with only "default" spec, don't include spec in path
    if api_name == "default":
        import_path = f"plato.sims.{sim_name}.models"
    else:
        import_path = f"plato.sims.{sim_name}.{api_name}.models"
    lines.append(f"{indent}from {import_path} import {pascal_name}")
    lines.append("")

    # Class definition
    lines.append(f"{indent}class {pascal_name}(BaseModel):")

    properties = schema.get("properties", {})
    required_fields = set(schema.get("required", []))

    if not properties:
        lines.append(f"{indent}    pass")
        return lines

    # Collect nested models to show after
    nested_models: list[tuple[str, dict]] = []

    for prop_name, prop_schema in properties.items():
        is_required = prop_name in required_fields

        # Determine the type
        if "$ref" in prop_schema:
            ref_name, ref_schema = _resolve_ref(prop_schema["$ref"], components)
            prop_type = _to_pascal_case(ref_name)
            if ref_schema:
                nested_models.append((ref_name, ref_schema))
        elif prop_schema.get("type") == "object" and prop_schema.get("properties"):
            # Inline object - use PascalCase of property name as type
            prop_type = _to_pascal_case(prop_name)
            nested_models.append((prop_name, prop_schema))
        elif prop_schema.get("type") == "array":
            items = prop_schema.get("items", {})
            if "$ref" in items:
                item_name, item_schema = _resolve_ref(items["$ref"], components)
                prop_type = f"list[{_to_pascal_case(item_name)}]"
                if item_schema:
                    nested_models.append((item_name, item_schema))
            elif items.get("type") == "object" and items.get("properties"):
                # Inline array item object
                item_type = _to_pascal_case(prop_name) + "Item"
                prop_type = f"list[{item_type}]"
                nested_models.append((prop_name + "_item", items))
            else:
                item_type = _get_param_type(items)
                prop_type = f"list[{item_type}]"
        else:
            prop_type = _get_param_type(prop_schema)

        # Format the field
        if is_required:
            lines.append(f"{indent}    {prop_name}: {prop_type}")
        else:
            lines.append(f"{indent}    {prop_name}: {prop_type} | None = None")

    # Show nested model definitions
    for nested_name, nested_schema in nested_models:
        lines.append("")
        nested_pascal = _to_pascal_case(nested_name)
        lines.append(f"{indent}class {nested_pascal}(BaseModel):")

        nested_props = nested_schema.get("properties", {})
        nested_required = set(nested_schema.get("required", []))

        if not nested_props:
            lines.append(f"{indent}    pass")
            continue

        for prop_name, prop_schema in nested_props.items():
            is_req = prop_name in nested_required

            if "$ref" in prop_schema:
                ref_name, _ = _resolve_ref(prop_schema["$ref"], components)
                prop_type = _to_pascal_case(ref_name)
            elif prop_schema.get("type") == "object" and prop_schema.get("properties"):
                # Nested inline object - just show as the property type
                prop_type = _to_pascal_case(prop_name)
            elif prop_schema.get("type") == "array":
                items = prop_schema.get("items", {})
                if "$ref" in items:
                    item_name, _ = _resolve_ref(items["$ref"], components)
                    prop_type = f"list[{_to_pascal_case(item_name)}]"
                else:
                    prop_type = f"list[{_get_param_type(items)}]"
            else:
                prop_type = _get_param_type(prop_schema)

            if is_req:
                lines.append(f"{indent}    {prop_name}: {prop_type}")
            else:
                lines.append(f"{indent}    {prop_name}: {prop_type} | None = None")

    return lines


def _format_dict_structure(
    schema: dict,
    components: dict,
    indent: str = "         ",
    depth: int = 0,
    max_depth: int = 2,
) -> list[str]:
    """Format response structure as dict access examples."""
    lines = []

    properties = schema.get("properties", {})
    if not properties:
        return lines

    if depth == 0:
        lines.append(f'{indent}Example: result["data"], result.get("meta"), etc.')
        lines.append(f"{indent}Structure:")

    for prop_name, prop_schema in list(properties.items())[:8]:  # Limit fields shown
        prop_indent = indent + "  " * (depth + 1)

        if "$ref" in prop_schema:
            ref_name, ref_schema = _resolve_ref(prop_schema["$ref"], components)
            if ref_schema and depth < max_depth:
                lines.append(f'{prop_indent}"{prop_name}": {{  # {ref_name}')
                nested = _format_dict_structure(ref_schema, components, indent, depth + 1, max_depth)
                lines.extend(nested)
                lines.append(f"{prop_indent}}}")
            else:
                lines.append(f'{prop_indent}"{prop_name}": {{...}}  # {ref_name}')
        elif prop_schema.get("type") == "array":
            items = prop_schema.get("items", {})
            if "$ref" in items:
                item_name, item_schema = _resolve_ref(items["$ref"], components)
                if item_schema and depth < max_depth:
                    lines.append(f'{prop_indent}"{prop_name}": [  # list of {item_name}')
                    lines.append(f"{prop_indent}  {{")
                    nested = _format_dict_structure(item_schema, components, indent, depth + 2, max_depth)
                    lines.extend(nested)
                    lines.append(f"{prop_indent}  }}, ...")
                    lines.append(f"{prop_indent}]")
                else:
                    lines.append(f'{prop_indent}"{prop_name}": [{{...}}, ...]  # list of {item_name}')
            else:
                item_type = _get_param_type(items)
                lines.append(f'{prop_indent}"{prop_name}": [...]  # list of {item_type}')
        elif prop_schema.get("type") == "object":
            lines.append(f'{prop_indent}"{prop_name}": {{...}}')
        else:
            prop_type = _get_param_type(prop_schema)
            lines.append(f'{prop_indent}"{prop_name}": ...  # {prop_type}')

    if len(properties) > 8:
        prop_indent = indent + "  " * (depth + 1)
        lines.append(f"{prop_indent}# ... and {len(properties) - 8} more fields")

    return lines


def _format_response_structure(
    schema: dict,
    components: dict,
    indent: str = "         ",
    max_fields: int = 8,
) -> list[str]:
    """Format response structure showing key fields."""
    lines = []

    # Resolve ref if present
    model_name = None
    if "$ref" in schema:
        model_name, resolved = _resolve_ref(schema["$ref"], components)
        if resolved:
            schema = resolved

    if model_name:
        lines.append(f"{indent}Response type: {_to_pascal_case(model_name)}")
    else:
        lines.append(f"{indent}Response type: dict")

    properties = schema.get("properties", {})
    if properties:
        lines.append(f"{indent}Fields:")
        field_count = 0
        for prop_name, prop_schema in properties.items():
            if field_count >= max_fields:
                remaining = len(properties) - field_count
                lines.append(f"{indent}  ... and {remaining} more fields")
                break

            if "$ref" in prop_schema:
                ref_name, _ = _resolve_ref(prop_schema["$ref"], components)
                prop_type = _to_pascal_case(ref_name)
            elif prop_schema.get("type") == "array":
                items = prop_schema.get("items", {})
                if "$ref" in items:
                    item_name, _ = _resolve_ref(items["$ref"], components)
                    prop_type = f"list[{_to_pascal_case(item_name)}]"
                else:
                    prop_type = f"list[{_get_param_type(items)}]"
            else:
                prop_type = _get_param_type(prop_schema)

            lines.append(f"{indent}  {prop_name}: {prop_type}")
            field_count += 1

    return lines


def cmd_info(sim_name: str, job_id: str | None = None) -> None:
    """Show detailed information about a sim."""
    try:
        info = registry.get_sim_info(sim_name)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"{info.title} (v{info.version})")
    print("=" * 60)

    if info.description:
        print(f"\n{info.description}\n")

    print(f"Name: {info.name}")

    # Try to get generator version from the package
    try:
        sim_module = importlib.import_module(f"plato.sims.{sim_name}")
        generator_version = getattr(sim_module, "__generator_version__", None)
        if generator_version:
            print(f"Generator Version: {generator_version}")
    except ImportError:
        pass

    # Handle instruction-based sims differently
    if info.sim_type == "instruction":
        _cmd_info_instruction(info, job_id)
    else:
        _cmd_info_api(info)


def _cmd_info_api(info) -> None:
    """Show info for API-based sim."""
    if info.auth:
        print(f"Auth Type: {info.auth.type}")

        print("\nRequired Environment Variables:")
        for var, desc in info.auth.env_vars.items():
            has_default = any(v for v in info.auth.default_values.values() if v)
            default_marker = " (has default for artifacts)" if has_default else ""
            print(f"  {var}: {desc}{default_marker}")

    base_url_example = "base_url='...'"
    if info.base_url_suffix:
        base_url_example = f"base_url='...' + '{info.base_url_suffix}'"

    print("\nUsage:")
    print(f"  from plato.sims import {info.name}")
    print(f"  client = await {info.name}.AsyncClient.create({base_url_example})")


def _cmd_info_instruction(info, job_id: str | None) -> None:
    """Show info for instruction-based sim."""
    print("Type: Instruction-based (no API client)")
    print()

    # Show available services
    if info.services:
        print("Services:")
        for name, svc in info.services.items():
            port = svc.get("port", "?")
            desc = svc.get("description", "")
            if job_id:
                url = f"https://{job_id}--{port}.connect.plato.so"
                print(f"  {name}: {url}")
                if desc:
                    print(f"         {desc}")
            else:
                print(f"  {name}: port {port}")
                if desc:
                    print(f"         {desc}")
        print()

    # Show env vars
    if info.env_vars:
        print("Environment Variables:")
        for name, var_config in info.env_vars.items():
            desc = var_config.get("description", "")
            if "template" in var_config:
                print(f"  {name}: (from service URL)")
            elif "default" in var_config:
                print(f"  {name}={var_config['default']}")
            else:
                print(f"  {name}")
            if desc:
                print(f"         {desc}")
        print()

    # Show instructions
    if info.instructions:
        instructions = info.instructions
        if job_id and info.services:
            # Build service URLs from job_id and replace placeholders
            for svc_name, svc_config in info.services.items():
                port = svc_config.get("port", 80)
                svc_url = f"https://{job_id}--{port}.connect.plato.so"
                instructions = instructions.replace(f"{{service:{svc_name}}}", svc_url)

        print("Instructions:")
        print(instructions)
        print()

    # Show usage
    print("Usage:")
    print(f"  from plato.sims import {info.name}")
    print()
    print("  # Get service URLs from job ID")
    print(f"  service_urls = {info.name}.get_service_urls(job_id)")
    print()
    print("  # Get formatted instructions")
    print(f"  instructions = {info.name}.get_instructions(service_urls)")
    print()
    print("  # Get environment variables to set")
    print(f"  env_vars = {info.name}.get_env_vars(service_urls)")


def cmd_endpoints(
    sim_name: str,
    spec_name: str | None = None,
    tag_filter: str | None = None,
    path_filter: str | None = None,
    show_code: bool = False,
) -> None:
    """List all endpoints in a sim's API by introspecting installed package."""
    try:
        info = registry.get_sim_info(sim_name)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    # Introspect the installed package's api modules
    try:
        import importlib
        import pkgutil

        api_module = importlib.import_module(f"plato.sims.{sim_name}.api")
        api_path = getattr(api_module, "__path__", None)

        if not api_path:
            print(f"No API modules found for {sim_name}")
            return

        print(f"{info.title} (v{info.version})")
        print("=" * 60)
        print()

        # List all resource modules (account, contact, lead, etc.)
        resources = []
        for importer, modname, ispkg in pkgutil.iter_modules(api_path):
            if ispkg:
                resources.append(modname)

        if not resources:
            print("No API resources found.")
            return

        # Filter by tag if provided
        if tag_filter:
            tag_lower = tag_filter.lower()
            resources = [r for r in resources if tag_lower in r.lower()]

        print(f"API Resources ({len(resources)}):\n")

        for resource in sorted(resources):
            try:
                resource_mod = importlib.import_module(f"plato.sims.{sim_name}.api.{resource}")

                # Get all endpoint functions in this resource
                endpoints = []
                for name in dir(resource_mod):
                    if not name.startswith("_"):
                        obj = getattr(resource_mod, name)
                        if hasattr(obj, "sync") or hasattr(obj, "asyncio"):
                            endpoints.append(name)

                # Filter by path if provided
                if path_filter:
                    path_lower = path_filter.lower()
                    endpoints = [e for e in endpoints if path_lower in e.lower()]

                if endpoints:
                    print(f"  {resource.upper()} ({len(endpoints)} endpoints)")

                    # Show endpoint list when filtering or when --code is specified
                    if show_code or path_filter or tag_filter:
                        for ep in sorted(endpoints):
                            print(f"    - {ep}")
                            if show_code:
                                print(f"        from plato.sims.{sim_name}.api.{resource} import {ep}")
                                print(f"        result = await {ep}.asyncio(client.httpx, ...)")
                        print()

            except ImportError as e:
                print(f"  {resource}: (failed to load: {e})")

        if not show_code and not path_filter and not tag_filter:
            print("\nUse --tag <resource> to filter, or --code to see import examples")
            print(f"Example: plato sims endpoints {sim_name} --tag account --code")

    except ImportError as e:
        print(f"Error: Could not import {sim_name} API: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_spec(sim_name: str, spec_name: str | None = None) -> None:
    """Output the full OpenAPI spec as JSON.

    NOTE: OpenAPI specs are no longer bundled with sim packages.
    """
    print("OpenAPI specs are no longer bundled with sim packages.", file=sys.stderr)
    print("Check the sim's source repository for the OpenAPI spec.", file=sys.stderr)
    sys.exit(1)


def _cmd_spec_legacy(sim_name: str, spec_name: str | None = None) -> None:
    """Legacy spec command."""
    try:
        spec = registry.get_spec(sim_name, spec_name)
    except (ValueError, NotImplementedError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    print(json.dumps(spec, indent=2))


def cmd_publish(
    config_path: str = "plato-config.yml",
    api_key: str | None = None,
    base_url: str = "https://plato.so/api",
    repo: str = "sims",
    dry_run: bool = False,
    output_dir: str | None = None,
) -> None:
    """
    Generate and publish a sim SDK package.

    Reads the plato-config.yml to get sim name and SDK configuration,
    generates API client code from the OpenAPI spec, builds a wheel,
    and uploads it to the Plato PyPI proxy.

    Args:
        config_path: Path to plato-config.yml
        api_key: Plato API key (or set PLATO_API_KEY env var)
        base_url: Plato API base URL
        repo: CodeArtifact repository name
        dry_run: Build but don't upload
        output_dir: Directory to copy built wheel to (for testing)
    """
    import os
    import subprocess
    import tempfile
    from pathlib import Path

    import yaml

    # Get API key from env if not provided
    if not api_key:
        api_key = os.environ.get("PLATO_API_KEY")

    if not api_key and not dry_run:
        print("Error: PLATO_API_KEY environment variable not set", file=sys.stderr)
        sys.exit(1)

    # Load plato-config.yml
    config_file = Path(config_path)
    if not config_file.exists():
        print(f"Error: {config_path} not found", file=sys.stderr)
        sys.exit(1)

    with open(config_file) as f:
        config = yaml.safe_load(f)

    service_name = config.get("service")
    if not service_name:
        print("Error: 'service' not found in plato-config.yml", file=sys.stderr)
        sys.exit(1)

    # Get SDK configuration
    sdk_config = config.get("sdk", {})
    package_name = sdk_config.get("package_name", f"plato-sim-{service_name}")
    version = sdk_config.get("version", "0.1.0")
    description = sdk_config.get("description", f"Plato SDK for {service_name}")
    specs_dir = sdk_config.get("specs_dir")
    spec_path = sdk_config.get("spec_path")  # Legacy support
    auth_config_path = sdk_config.get("auth_config")

    print(f"Publishing SDK for: {service_name}")
    print(f"Package name: {package_name}")
    print(f"Version: {version}")

    # Create temp directory for build
    with tempfile.TemporaryDirectory(prefix="plato-sim-sdk-") as tmpdir:
        build_dir = Path(tmpdir)
        # Use namespace package structure: src/plato/sims/{service_name}/
        # NO __init__.py in plato/ or plato/sims/ (implicit namespace packages)
        pkg_dir = build_dir / "src" / "plato" / "sims" / service_name
        pkg_dir.mkdir(parents=True)

        config_dir = config_file.parent

        # Check for instruction-based sim first
        instructions_file = None
        if specs_dir:
            instructions_path = config_dir / specs_dir / "instructions.yaml"
            if instructions_path.exists():
                instructions_file = instructions_path
        if not instructions_file:
            instructions_path = config_dir / "instructions.yaml"
            if instructions_path.exists():
                instructions_file = instructions_path

        if instructions_file:
            # Generate instruction-based SDK
            print(f"Using instructions config: {instructions_file}")
            print("Generating instruction-based SDK...")
            try:
                import plato
                from plato._sims_generator import InstructionConfig, InstructionGenerator

                generator_version = getattr(plato, "__version__", None)
                print(f"  Generator version: {generator_version}")

                instruction_config = InstructionConfig.from_yaml(instructions_file)
                # Override version from plato-config.yml if set
                instruction_config.version = version

                generator = InstructionGenerator(
                    config=instruction_config,
                    output_path=pkg_dir,
                    package_name=service_name,
                    generator_version=generator_version,
                )
                generator.generate()
                print(f"  Generated instruction-based SDK to: {pkg_dir}")

            except ImportError as e:
                print(f"Error: Missing dependency for SDK generation: {e}", file=sys.stderr)
                print("Install with: uv add plato-sdk-v2", file=sys.stderr)
                sys.exit(1)
            except Exception as e:
                print(f"Error generating instruction SDK: {e}", file=sys.stderr)
                sys.exit(1)

        else:
            # Generate OpenAPI-based SDK
            # Find OpenAPI spec
            spec_file = None

            # Priority 1: specs_dir (new format)
            if specs_dir:
                specs_path = config_dir / specs_dir
                for candidate in ["openapi.json", "openapi.yaml", "openapi.yml"]:
                    candidate_path = specs_path / candidate
                    if candidate_path.exists():
                        spec_file = candidate_path
                        break
            # Priority 2: spec_path (legacy format)
            elif spec_path:
                spec_file = config_dir / spec_path
            # Priority 3: Try common locations in root
            else:
                for candidate in ["openapi.yaml", "openapi.yml", "openapi.json", "spec.yaml", "spec.json"]:
                    candidate_path = config_dir / candidate
                    if candidate_path.exists():
                        spec_file = candidate_path
                        break

            if not spec_file or not spec_file.exists():
                print(
                    "Error: OpenAPI spec or instructions.yaml not found. "
                    "Set 'sdk.specs_dir' or 'sdk.spec_path' in plato-config.yml",
                    file=sys.stderr,
                )
                sys.exit(1)

            print(f"Using OpenAPI spec: {spec_file}")

            # Load auth config if provided
            auth_yaml = None
            if auth_config_path:
                auth_file = config_dir / auth_config_path
                if auth_file.exists():
                    auth_yaml = auth_file
            else:
                # Try specs_dir first, then root
                search_dirs = []
                if specs_dir:
                    search_dirs.append(config_dir / specs_dir)
                search_dirs.append(config_dir)

                for search_dir in search_dirs:
                    for candidate in ["auth.yaml", "auth.yml"]:
                        candidate_path = search_dir / candidate
                        if candidate_path.exists():
                            auth_yaml = candidate_path
                            break
                    if auth_yaml:
                        break

            # Generate SDK code
            print("Generating SDK code...")
            try:
                import plato
                from plato._sims_generator import AuthConfig, PythonGenerator, parse_openapi

                # Get current plato-sdk-v2 version
                generator_version = getattr(plato, "__version__", None)
                print(f"  Generator version: {generator_version}")

                # Check if .generator-version exists and matches
                if specs_dir:
                    generator_version_file = config_dir / specs_dir / ".generator-version"
                    if generator_version_file.exists():
                        expected_version = generator_version_file.read_text().strip()
                        if expected_version and generator_version and expected_version != generator_version:
                            print(
                                f"Error: Generator version mismatch. "
                                f"Expected {expected_version} (from .generator-version), "
                                f"but running {generator_version}",
                                file=sys.stderr,
                            )
                            print(
                                f"  Run: uvx --from 'plato-sdk-v2=={expected_version}' plato sims publish",
                                file=sys.stderr,
                            )
                            print(
                                f"  Or update .generator-version to {generator_version} to use current version",
                                file=sys.stderr,
                            )
                            sys.exit(1)

                    # Write/update .generator-version to specs dir
                    if generator_version:
                        generator_version_file.write_text(f"{generator_version}\n")
                        print(f"  Updated {generator_version_file}")

                # Load spec (spec_file is guaranteed non-None after check above)
                assert spec_file is not None
                with open(spec_file) as f:
                    if spec_file.suffix == ".json":
                        spec = json.load(f)
                    else:
                        spec = yaml.safe_load(f)

                # Load auth config
                if auth_yaml and auth_yaml.exists():
                    auth = AuthConfig.from_yaml(auth_yaml)
                else:
                    # Default auth config
                    auth = AuthConfig(
                        type="basic",
                        env_prefix=service_name.upper(),
                    )

                # Parse and generate
                api = parse_openapi(spec)
                print(f"  Parsed {len(api.endpoints)} endpoints")

                generator = PythonGenerator(
                    api=api,
                    output_path=pkg_dir,
                    spec=spec,
                    package_name=service_name,
                    auth_config=auth,
                    generator_version=generator_version,
                )
                generator.generate()
                print(f"  Generated to: {pkg_dir}")

            except ImportError as e:
                print(f"Error: Missing dependency for SDK generation: {e}", file=sys.stderr)
                print("Install with: uv add plato-sdk-v2", file=sys.stderr)
                sys.exit(1)
            except Exception as e:
                print(f"Error generating SDK: {e}", file=sys.stderr)
                sys.exit(1)

        # Create pyproject.toml with namespace package structure
        # Instruction sims need pyyaml; API sims need httpx and pydantic
        if instructions_file:
            dependencies = '["pyyaml>=6.0.0"]'
            # Include yaml file in package data
            extra_config = f"""
[tool.hatch.build.targets.wheel.force-include]
"src/plato/sims/{service_name}/instructions.yaml" = "plato/sims/{service_name}/instructions.yaml"
"""
        else:
            dependencies = '["httpx>=0.25.0", "pydantic>=2.0.0"]'
            extra_config = ""

        pyproject_content = f'''[project]
name = "{package_name}"
version = "{version}"
description = "{description}"
requires-python = ">=3.10"
dependencies = {dependencies}

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/plato"]
{extra_config}'''
        (build_dir / "pyproject.toml").write_text(pyproject_content)

        # Create README
        if instructions_file:
            readme_content = f"""# {package_name}

Auto-generated instruction-based SDK for the {service_name} simulator.

## Installation

```bash
uv add {package_name} --index-url https://plato.so/api/v2/pypi/{repo}/simple/
```

## Usage

```python
from plato.sims.{service_name} import get_instructions, get_service_urls, setup_env

# Get service URLs from job ID
service_urls = get_service_urls(job_id)

# Get formatted instructions
instructions = get_instructions(service_urls)

# Set up environment variables
setup_env(service_urls)
```
"""
        else:
            readme_content = f"""# {package_name}

Auto-generated SDK for the {service_name} simulator.

## Installation

```bash
uv add {package_name} --index-url https://plato.so/api/v2/pypi/{repo}/simple/
```

## Usage

```python
from plato.sims.{service_name} import Client

client = Client.create(base_url="...")
```
"""
        (build_dir / "README.md").write_text(readme_content)

        # Build package
        print("Building package...")
        try:
            result = subprocess.run(
                ["python", "-m", "build", "--wheel", "--sdist"],
                cwd=build_dir,
                capture_output=True,
                text=True,
            )
            if result.returncode != 0:
                # Try with uv if python -m build fails
                result = subprocess.run(
                    ["uv", "build"],
                    cwd=build_dir,
                    capture_output=True,
                    text=True,
                )
            if result.returncode != 0:
                print(f"Build failed: {result.stderr}", file=sys.stderr)
                sys.exit(1)
            print("  Build successful")
        except FileNotFoundError:
            print("Error: 'build' or 'uv' not found. Install with: pip install build", file=sys.stderr)
            sys.exit(1)

        # Find built files
        dist_dir = build_dir / "dist"
        wheel_files = list(dist_dir.glob("*.whl"))
        if not wheel_files:
            print("Error: No wheel file found after build", file=sys.stderr)
            sys.exit(1)

        wheel_file = wheel_files[0]
        print(f"  Built: {wheel_file.name}")

        # Copy wheel to output directory if specified
        if output_dir:
            import shutil

            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
            dest_file = output_path / wheel_file.name
            shutil.copy2(wheel_file, dest_file)
            print(f"  Copied to: {dest_file}")

        if dry_run:
            print("\nDry run - skipping upload")
            return

        # At this point api_key is guaranteed to be set (checked earlier)
        assert api_key is not None

        # Upload using uv publish
        upload_url = f"{base_url}/v2/pypi/{repo}/"
        print(f"\nUploading to {upload_url}...")
        try:
            result = subprocess.run(
                [
                    "uv",
                    "publish",
                    "--publish-url",
                    upload_url,
                    "--username",
                    "__token__",
                    "--password",
                    api_key,
                    str(wheel_file),
                ],
                capture_output=True,
                text=True,
            )

            if result.returncode == 0:
                print("  Upload successful!")
                print("\nInstall with:")
                print(f"  uv add {package_name} --index-url https://plato.so/api/v2/pypi/{repo}/simple/")
            else:
                print("  Upload failed:", file=sys.stderr)
                if result.stdout:
                    print(result.stdout, file=sys.stderr)
                if result.stderr:
                    print(result.stderr, file=sys.stderr)
                sys.exit(1)

        except FileNotFoundError:
            print("Error: uv not found", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Upload error: {e}", file=sys.stderr)
            sys.exit(1)


def main(args: list[str] | None = None) -> None:
    """Main CLI entry point."""
    if args is None:
        args = sys.argv[1:]

    if not args or args[0] in ["-h", "--help", "help"]:
        print(__doc__)
        return

    command = args[0]

    if command == "list":
        cmd_list()

    elif command == "info":
        if len(args) < 2:
            print("Error: sim name required", file=sys.stderr)
            print("Usage: plato sims info <sim_name> [--job-id JOB_ID]", file=sys.stderr)
            sys.exit(1)

        sim_name = args[1]
        job_id = None

        # Parse optional --job-id flag
        i = 2
        while i < len(args):
            if args[i] == "--job-id" and i + 1 < len(args):
                job_id = args[i + 1]
                i += 2
            else:
                i += 1

        cmd_info(sim_name, job_id)

    elif command == "endpoints":
        if len(args) < 2:
            print("Error: sim name required", file=sys.stderr)
            print(
                "Usage: plato sims endpoints <sim_name> [--spec SPEC] [--tag TAG] [--path PATH] [--code]",
                file=sys.stderr,
            )
            sys.exit(1)

        sim_name = args[1]
        spec_name = None
        tag_filter = None
        path_filter = None
        show_code = False

        # Parse optional flags
        i = 2
        while i < len(args):
            if args[i] == "--spec" and i + 1 < len(args):
                spec_name = args[i + 1]
                i += 2
            elif args[i] == "--tag" and i + 1 < len(args):
                tag_filter = args[i + 1]
                i += 2
            elif args[i] == "--path" and i + 1 < len(args):
                path_filter = args[i + 1]
                i += 2
            elif args[i] == "--code":
                show_code = True
                i += 1
            else:
                i += 1

        cmd_endpoints(sim_name, spec_name, tag_filter, path_filter, show_code)

    elif command == "spec":
        if len(args) < 2:
            print("Error: sim name required", file=sys.stderr)
            print("Usage: plato sims spec <sim_name> [--spec SPEC]", file=sys.stderr)
            sys.exit(1)

        sim_name = args[1]
        spec_name = None

        if len(args) > 2 and args[2] == "--spec" and len(args) > 3:
            spec_name = args[3]

        cmd_spec(sim_name, spec_name)

    elif command == "publish":
        # Parse publish options
        config_path = "plato-config.yml"
        api_key = None
        base_url = "https://plato.so/api"
        repo = "sims"
        dry_run = False
        output_dir = None

        i = 1
        while i < len(args):
            if args[i] == "--config" and i + 1 < len(args):
                config_path = args[i + 1]
                i += 2
            elif args[i] == "--api-key" and i + 1 < len(args):
                api_key = args[i + 1]
                i += 2
            elif args[i] == "--base-url" and i + 1 < len(args):
                base_url = args[i + 1]
                i += 2
            elif args[i] == "--repo" and i + 1 < len(args):
                repo = args[i + 1]
                i += 2
            elif args[i] == "--output-dir" and i + 1 < len(args):
                output_dir = args[i + 1]
                i += 2
            elif args[i] == "--dry-run":
                dry_run = True
                i += 1
            else:
                i += 1

        cmd_publish(config_path, api_key, base_url, repo, dry_run, output_dir)

    else:
        print(f"Error: Unknown command '{command}'", file=sys.stderr)
        print(__doc__, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
