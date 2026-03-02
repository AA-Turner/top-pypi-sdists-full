"""Parse OpenAPI spec into intermediate representation using openapi-pydantic."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from openapi_pydantic import parse_obj


class TypeKind(Enum):
    STRING = "string"
    INT = "int"
    FLOAT = "float"
    BOOL = "bool"
    DATETIME = "datetime"
    DATE = "date"
    BYTES = "bytes"
    ANY = "any"
    NONE = "none"
    LIST = "list"
    MAP = "map"
    MODEL = "model"
    OPTIONAL = "optional"
    UNION = "union"


@dataclass
class Type:
    """Language-agnostic type representation."""

    kind: TypeKind
    model_name: str | None = None  # For MODEL kind
    inner: "Type | None" = None  # For LIST, OPTIONAL
    value_type: "Type | None" = None  # For MAP
    variants: list["Type"] | None = None  # For UNION

    def to_python(self) -> str:
        """Render type as Python type annotation."""
        match self.kind:
            case TypeKind.STRING:
                return "str"
            case TypeKind.INT:
                return "int"
            case TypeKind.FLOAT:
                return "float"
            case TypeKind.BOOL:
                return "bool"
            case TypeKind.DATETIME:
                return "datetime"
            case TypeKind.DATE:
                return "date"
            case TypeKind.BYTES:
                return "bytes"
            case TypeKind.ANY:
                return "Any"
            case TypeKind.NONE:
                return "None"
            case TypeKind.LIST:
                inner = self.inner.to_python() if self.inner else "Any"
                return f"list[{inner}]"
            case TypeKind.MAP:
                value = self.value_type.to_python() if self.value_type else "Any"
                return f"dict[str, {value}]"
            case TypeKind.MODEL:
                return self.model_name or "Any"
            case TypeKind.OPTIONAL:
                if self.inner:
                    inner = self.inner.to_python()
                    if inner == "None":
                        return "None"
                    return f"{inner} | None"
                return "Any | None"
            case TypeKind.UNION:
                if self.variants:
                    parts = [v.to_python() for v in self.variants]
                    return " | ".join(parts)
                return "Any"
        return "Any"

    def to_typescript(self) -> str:
        """Render type as TypeScript type annotation."""
        match self.kind:
            case TypeKind.STRING:
                return "string"
            case TypeKind.INT | TypeKind.FLOAT:
                return "number"
            case TypeKind.BOOL:
                return "boolean"
            case TypeKind.DATETIME | TypeKind.DATE:
                return "string"  # ISO string
            case TypeKind.BYTES:
                return "Uint8Array"
            case TypeKind.ANY:
                return "unknown"
            case TypeKind.NONE:
                return "null"
            case TypeKind.LIST:
                inner = self.inner.to_typescript() if self.inner else "unknown"
                return f"{inner}[]"
            case TypeKind.MAP:
                value = self.value_type.to_typescript() if self.value_type else "unknown"
                return f"Record<string, {value}>"
            case TypeKind.MODEL:
                return self.model_name or "unknown"
            case TypeKind.OPTIONAL:
                if self.inner:
                    inner = self.inner.to_typescript()
                    return f"{inner} | null"
                return "unknown | null"
            case TypeKind.UNION:
                if self.variants:
                    parts = [v.to_typescript() for v in self.variants]
                    return " | ".join(parts)
                return "unknown"
        return "unknown"

    def to_go(self) -> str:
        """Render type as Go type."""
        match self.kind:
            case TypeKind.STRING:
                return "string"
            case TypeKind.INT:
                return "int64"
            case TypeKind.FLOAT:
                return "float64"
            case TypeKind.BOOL:
                return "bool"
            case TypeKind.DATETIME | TypeKind.DATE:
                return "time.Time"
            case TypeKind.BYTES:
                return "[]byte"
            case TypeKind.ANY:
                return "interface{}"
            case TypeKind.NONE:
                return "nil"
            case TypeKind.LIST:
                inner = self.inner.to_go() if self.inner else "interface{}"
                return f"[]{inner}"
            case TypeKind.MAP:
                value = self.value_type.to_go() if self.value_type else "interface{}"
                return f"map[string]{value}"
            case TypeKind.MODEL:
                return self.model_name or "interface{}"
            case TypeKind.OPTIONAL:
                if self.inner:
                    inner = self.inner.to_go()
                    return f"*{inner}"
                return "*interface{}"
            case TypeKind.UNION:
                return "interface{}"  # Go doesn't have union types
        return "interface{}"

    def get_model_refs(self) -> set[str]:
        """Get all model names referenced by this type."""
        refs = set()
        if self.kind == TypeKind.MODEL and self.model_name:
            refs.add(self.model_name)
        if self.inner:
            refs.update(self.inner.get_model_refs())
        if self.value_type:
            refs.update(self.value_type.get_model_refs())
        if self.variants:
            for v in self.variants:
                refs.update(v.get_model_refs())
        return refs

    def is_nullable(self) -> bool:
        """Check if this type already includes None/null."""
        if self.kind == TypeKind.NONE:
            return True
        if self.kind == TypeKind.OPTIONAL:
            return True
        if self.kind == TypeKind.UNION and self.variants:
            return any(v.kind == TypeKind.NONE for v in self.variants)
        return False


@dataclass
class Property:
    name: str
    python_name: str
    type: Type
    required: bool
    default: Any = None
    description: str | None = None


@dataclass
class Schema:
    name: str
    class_name: str
    properties: list[Property] = field(default_factory=list)
    description: str | None = None
    enum_values: list[str | int] | None = None  # For enum schemas (allow int enums)


@dataclass
class ParameterInfo:
    name: str
    python_name: str
    location: str  # path, query, header, cookie
    type: Type
    required: bool
    default: Any = None
    description: str | None = None


@dataclass
class Endpoint:
    path: str
    method: str
    operation_id: str
    function_name: str
    tag: str  # e.g., "v1.simulator" or "v2.sessions"
    summary: str | None = None
    description: str | None = None
    parameters: list[ParameterInfo] = field(default_factory=list)
    request_body: Schema | None = None
    response_type: Type | None = None
    streaming: bool = False  # Whether this endpoint supports streaming
    stream_type: Type | None = None  # Type of streamed items
    has_file_upload: bool = False  # Whether this endpoint accepts file uploads


@dataclass
class API:
    title: str
    version: str
    schemas: dict[str, Schema] = field(default_factory=dict)
    endpoints: list[Endpoint] = field(default_factory=list)
    tags: set[str] = field(default_factory=set)


_RESERVED_PARAM_NAMES = {"client", "body", "response", "request", "url", "params", "headers"}


def to_python_name(name: str) -> str:
    """Convert camelCase or kebab-case to snake_case.

    Also handles brackets: fields[address] -> fields_address
    And nested brackets: filter[options][color] -> filter_options_color
    Empty brackets are removed: accounts[] -> accounts
    Single underscore becomes 'param_': _ -> param_
    Reserved names get '_param' suffix: client -> client_param
    """
    import re

    # Handle brackets: [anything] -> _anything, [] -> empty
    # Use * instead of + to handle empty brackets like accounts[]
    while "[" in name:
        name = re.sub(r"\[([^\]]*)\]", r"_\1", name)
    name = name.replace("-", "_")
    name = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", name)
    # Clean up any double/trailing underscores
    while "__" in name:
        name = name.replace("__", "_")
    result = name.lower().strip("_")
    # Handle edge case of empty or underscore-only names
    if not result:
        return "param_"
    # Handle reserved names that would conflict with template variables
    if result in _RESERVED_PARAM_NAMES:
        return f"{result}_param"
    return result


def to_class_name(name: str) -> str:
    """Convert to PascalCase, preserving existing casing in segments.

    Examples:
        'app_api_v2_EvaluateResponse' -> 'AppApiV2EvaluateResponse'
        'app.api.v2.EvaluateResponse' -> 'AppApiV2EvaluateResponse'
    """
    import re

    # Split on dots, underscores, dashes, and spaces
    parts = re.split(r"[._\-\s]+", name)
    # Uppercase first char of each part, preserve rest
    return "".join((part[0].upper() + part[1:] if part else "") for part in parts)


def _is_reference(obj: Any) -> bool:
    """Check if obj is a Reference (has $ref)."""
    return hasattr(obj, "ref") and obj.ref is not None


def _get_ref_name(ref: Any) -> str:
    """Extract schema name from a $ref."""
    return ref.ref.split("/")[-1]


def _resolve_ref(ref: Any, components: dict[str, dict[str, Any]], ref_type: str) -> Any:
    """Resolve a $ref to its actual definition.

    Args:
        ref: The reference object with .ref attribute
        components: Dict of component types (schemas, parameters, requestBodies, responses)
        ref_type: The type of component to look in ('schemas', 'parameters', etc.)
    """
    if not _is_reference(ref):
        return ref

    ref_path = ref.ref  # e.g., "#/components/parameters/IdParam"
    parts = ref_path.split("/")

    if len(parts) >= 4 and parts[1] == "components":
        component_type = parts[2]  # 'schemas', 'parameters', 'requestBodies', 'responses'
        component_name = parts[3]

        if component_type in components and component_name in components[component_type]:
            return components[component_type][component_name]

    return None


def parse_type_from_schema(schema: Any | None, components_schemas: dict[str, Any]) -> Type:
    """Parse OpenAPI schema to Type using openapi-pydantic models."""
    if schema is None:
        return Type(kind=TypeKind.ANY)

    # Handle $ref
    if _is_reference(schema):
        type_name = _get_ref_name(schema)
        return Type(kind=TypeKind.MODEL, model_name=to_class_name(type_name))

    # Check for nullable: true (OpenAPI 3.0 style)
    is_nullable = getattr(schema, "nullable", False)

    # Handle anyOf (union or optional)
    if hasattr(schema, "anyOf") and schema.anyOf:
        types = [parse_type_from_schema(s, components_schemas) for s in schema.anyOf]
        # Simplify: if it's just T | null, make it optional
        non_none = [t for t in types if t.kind != TypeKind.NONE]
        has_none = any(t.kind == TypeKind.NONE for t in types)
        if len(non_none) == 1 and has_none:
            return Type(kind=TypeKind.OPTIONAL, inner=non_none[0])
        if len(non_none) == 0:
            return Type(kind=TypeKind.NONE)
        result = Type(kind=TypeKind.UNION, variants=types)
        if is_nullable and not result.is_nullable():
            return Type(kind=TypeKind.OPTIONAL, inner=result)
        return result

    # Handle oneOf (discriminated union)
    if hasattr(schema, "oneOf") and schema.oneOf:
        types = [parse_type_from_schema(s, components_schemas) for s in schema.oneOf]
        result = Type(kind=TypeKind.UNION, variants=types)
        if is_nullable and not result.is_nullable():
            return Type(kind=TypeKind.OPTIONAL, inner=result)
        return result

    # Handle allOf (composition/intersection)
    if hasattr(schema, "allOf") and schema.allOf:
        # Collect all referenced types - for now, return the first reference
        # A more complete solution would merge all schemas
        refs = []
        for s in schema.allOf:
            if _is_reference(s):
                refs.append(parse_type_from_schema(s, components_schemas))
        if refs:
            # If multiple refs, return as union (not perfect but better than dropping)
            if len(refs) == 1:
                result = refs[0]
            else:
                result = Type(kind=TypeKind.UNION, variants=refs)
            if is_nullable:
                return Type(kind=TypeKind.OPTIONAL, inner=result)
            return result
        return Type(kind=TypeKind.ANY)

    schema_type = getattr(schema, "type", None)

    # Handle DataType enum - extract .value if it's an enum
    schema_type = getattr(schema_type, "value", schema_type)

    # Handle OpenAPI 3.1 type arrays (e.g., ["string", "null"])
    if isinstance(schema_type, list):
        types = []
        for t in schema_type:
            if t == "null":
                types.append(Type(kind=TypeKind.NONE))
            elif t == "string":
                types.append(Type(kind=TypeKind.STRING))
            elif t == "integer":
                types.append(Type(kind=TypeKind.INT))
            elif t == "number":
                types.append(Type(kind=TypeKind.FLOAT))
            elif t == "boolean":
                types.append(Type(kind=TypeKind.BOOL))
            elif t == "array":
                items = getattr(schema, "items", None)
                item_type = parse_type_from_schema(items, components_schemas)
                types.append(Type(kind=TypeKind.LIST, inner=item_type))
            elif t == "object":
                types.append(Type(kind=TypeKind.MAP, value_type=Type(kind=TypeKind.ANY)))
            else:
                types.append(Type(kind=TypeKind.ANY))

        # Simplify: if it's just T | null, make it optional
        non_none = [t for t in types if t.kind != TypeKind.NONE]
        has_none = any(t.kind == TypeKind.NONE for t in types)
        if len(non_none) == 1 and has_none:
            return Type(kind=TypeKind.OPTIONAL, inner=non_none[0])
        if len(types) == 1:
            return types[0]
        return Type(kind=TypeKind.UNION, variants=types)

    def _make_nullable(t: Type) -> Type:
        """Wrap type in optional if nullable and not already nullable."""
        if is_nullable and not t.is_nullable():
            return Type(kind=TypeKind.OPTIONAL, inner=t)
        return t

    if schema_type == "null":
        return Type(kind=TypeKind.NONE)
    if schema_type == "string":
        fmt = getattr(schema, "schema_format", None)
        if fmt == "date-time":
            return _make_nullable(Type(kind=TypeKind.DATETIME))
        if fmt == "date":
            return _make_nullable(Type(kind=TypeKind.DATE))
        if fmt == "binary":
            return _make_nullable(Type(kind=TypeKind.BYTES))
        return _make_nullable(Type(kind=TypeKind.STRING))
    if schema_type == "integer":
        return _make_nullable(Type(kind=TypeKind.INT))
    if schema_type == "number":
        return _make_nullable(Type(kind=TypeKind.FLOAT))
    if schema_type == "boolean":
        return _make_nullable(Type(kind=TypeKind.BOOL))
    if schema_type == "array":
        items = getattr(schema, "items", None)
        item_type = parse_type_from_schema(items, components_schemas)
        return _make_nullable(Type(kind=TypeKind.LIST, inner=item_type))
    if schema_type == "object":
        additional = getattr(schema, "additionalProperties", None)
        if additional:
            if additional is True:
                return _make_nullable(Type(kind=TypeKind.MAP, value_type=Type(kind=TypeKind.ANY)))
            value_type = parse_type_from_schema(additional, components_schemas)
            return _make_nullable(Type(kind=TypeKind.MAP, value_type=value_type))
        # Check if it has properties - if so, it might be an inline model
        # For now, still return as map but this could be improved
        return _make_nullable(Type(kind=TypeKind.MAP, value_type=Type(kind=TypeKind.ANY)))

    return Type(kind=TypeKind.ANY)


def parse_schema_def(name: str, schema: Any, components_schemas: dict[str, Any]) -> Schema:
    """Parse a schema definition."""
    # Handle enum schemas - allow both string and int values
    if hasattr(schema, "enum") and schema.enum:
        enum_values = [
            v
            for v in schema.enum
            if isinstance(v, (str, int))  # Allow string and int enums
        ]
        return Schema(
            name=name,
            class_name=to_class_name(name),
            description=getattr(schema, "description", None),
            enum_values=enum_values,
        )

    properties = []
    required_props = set(getattr(schema, "required", None) or [])

    for prop_name, prop_schema in (getattr(schema, "properties", None) or {}).items():
        prop_type = parse_type_from_schema(prop_schema, components_schemas)
        is_required = prop_name in required_props

        # Wrap in optional if not required and not already nullable
        if not is_required and not prop_type.is_nullable():
            prop_type = Type(kind=TypeKind.OPTIONAL, inner=prop_type)

        # Handle default values
        default = None
        prop_default = getattr(prop_schema, "default", None)
        if prop_default is not None:
            default = prop_default
            if isinstance(default, str):
                default = f'"{default}"'
            elif isinstance(default, bool):
                default = str(default)

        description = getattr(prop_schema, "description", None)

        properties.append(
            Property(
                name=prop_name,
                python_name=to_python_name(prop_name),
                type=prop_type,
                required=is_required,
                default=default,
                description=description,
            )
        )

    return Schema(
        name=name,
        class_name=to_class_name(name),
        properties=properties,
        description=getattr(schema, "description", None),
    )


def normalize_tag(tag: str) -> str:
    """Normalize tag for use as module path.

    Tags with '/' become nested modules: 'v1/simulator' -> 'v1.simulator'
    Kebab-case is converted to snake_case: 'agent-artifacts' -> 'agent_artifacts'
    Spaces are converted to underscores: 'Digital Downloads' -> 'digital_downloads'
    """
    # Strip leading/trailing whitespace
    tag = tag.strip()
    # Replace / with . for module nesting
    tag = tag.replace("/", ".")
    # Replace - and spaces with _ for valid Python identifiers
    tag = tag.replace("-", "_")
    tag = tag.replace(" ", "_")
    # Convert to lowercase
    tag = tag.lower()
    return tag


def _collect_union_variant_names(variants: list[Any], components: dict[str, dict[str, Any]]) -> list[str]:
    """Collect class names from union variants, handling both refs and inline schemas."""
    variant_names = []
    inline_counter = 0

    for variant in variants:
        if _is_reference(variant):
            variant_names.append(to_class_name(_get_ref_name(variant)))
        else:
            # For inline schemas, try to create a meaningful name or use Any
            # In practice, inline schemas in request bodies are rare
            # We could generate inline classes but that's complex
            schema_type = getattr(variant, "type", None)
            schema_type = getattr(schema_type, "value", schema_type)

            if schema_type == "object":
                variant_names.append("dict[str, Any]")
            elif schema_type == "array":
                variant_names.append("list[Any]")
            elif schema_type == "string":
                variant_names.append("str")
            elif schema_type == "integer":
                variant_names.append("int")
            elif schema_type == "number":
                variant_names.append("float")
            elif schema_type == "boolean":
                variant_names.append("bool")
            else:
                variant_names.append("Any")
            inline_counter += 1

    return variant_names


def _generate_request_body_name(operation_id: str) -> str:
    """Generate a class name for an inline request body schema."""
    # Convert operation_id to PascalCase and add Request suffix
    # e.g., "add_item" -> "AddItemRequest", "createCart" -> "CreateCartRequest"
    return to_class_name(operation_id) + "Request"


def _parse_inline_schema_to_model(
    schema: Any,
    name: str,
    components_schemas: dict[str, Any],
) -> Schema:
    """Parse an inline schema into a Schema model with properties."""
    properties = []
    required_props = set(getattr(schema, "required", None) or [])

    for prop_name, prop_schema in (getattr(schema, "properties", None) or {}).items():
        prop_type = parse_type_from_schema(prop_schema, components_schemas)
        is_required = prop_name in required_props

        # Wrap in optional if not required and not already nullable
        if not is_required and not prop_type.is_nullable():
            prop_type = Type(kind=TypeKind.OPTIONAL, inner=prop_type)

        description = getattr(prop_schema, "description", None)

        properties.append(
            Property(
                name=prop_name,
                python_name=to_python_name(prop_name),
                type=prop_type,
                required=is_required,
                default=None,
                description=description,
            )
        )

    return Schema(
        name=name,
        class_name=to_class_name(name),
        properties=properties,
        description=getattr(schema, "description", None),
    )


def parse_endpoint_from_operation(
    path: str,
    method: str,
    operation: Any,
    components_schemas: dict[str, Any],
    all_components: dict[str, dict[str, Any]],
    inline_schemas: dict[str, Schema] | None = None,
) -> Endpoint:
    """Parse an endpoint operation using openapi-pydantic models."""
    tags = getattr(operation, "tags", None) or ["default"]
    raw_tag = tags[0] if tags else "default"
    tag = normalize_tag(raw_tag)

    operation_id = getattr(operation, "operationId", None)
    if not operation_id:
        # Generate a better operation ID from path and method
        clean_path = path.replace("/", "_").replace("{", "").replace("}", "").strip("_")
        operation_id = f"{method}_{clean_path}"

    func_name = operation_id
    if func_name.startswith(raw_tag + "_"):
        func_name = func_name[len(raw_tag) + 1 :]
    func_name = to_python_name(func_name)

    # Parse parameters (including resolving $ref)
    parameters = []
    for param in getattr(operation, "parameters", None) or []:
        # Resolve parameter reference if needed
        if _is_reference(param):
            resolved = _resolve_ref(param, all_components, "parameters")
            if resolved is None:
                continue  # Could not resolve reference
            param = resolved

        param_schema = getattr(param, "param_schema", None)
        param_type = parse_type_from_schema(param_schema, components_schemas)

        # Strip nullable wrapper from parameter types since the template handles optionality
        # based on the required field. This prevents duplicate | None in generated code.
        if param_type.kind == TypeKind.OPTIONAL and param_type.inner:
            param_type = param_type.inner
        elif param_type.kind == TypeKind.UNION and param_type.variants:
            # If it's a union with None, remove the None variant
            non_none_variants = [v for v in param_type.variants if v.kind != TypeKind.NONE]
            if len(non_none_variants) == 1:
                param_type = non_none_variants[0]
            elif len(non_none_variants) > 1:
                param_type = Type(kind=TypeKind.UNION, variants=non_none_variants)

        raw_default = getattr(param_schema, "default", None) if param_schema else None
        default = None
        if raw_default is not None:
            # Check type compatibility - if param is string but default is bool, convert to string
            is_string_type = param_type.kind == TypeKind.STRING
            if isinstance(raw_default, str):
                default = f'"{raw_default}"'  # Quote string defaults
            elif isinstance(raw_default, bool):
                if is_string_type:
                    # Spec bug: boolean default for string type - convert to string
                    default = f'"{str(raw_default).lower()}"'
                else:
                    default = str(raw_default)  # Python True/False
            elif isinstance(raw_default, (int, float)):
                if is_string_type:
                    default = f'"{raw_default}"'  # Convert to string
                else:
                    default = str(raw_default)
            # For complex objects, leave as None (not serializable as default)

        param_in = getattr(param, "param_in", None)
        if param_in is None:
            param_in = getattr(param, "in", None)  # Some parsers use 'in' directly
        # Extract .value if it's an enum, otherwise convert to string
        location = getattr(param_in, "value", None) or (str(param_in) if param_in else "query")

        param_name = getattr(param, "name", None)
        if param_name is None:
            continue  # Invalid parameter

        parameters.append(
            ParameterInfo(
                name=param_name,
                python_name=to_python_name(param_name),
                location=location,
                type=param_type,
                required=getattr(param, "required", False) or False,
                default=default,
                description=getattr(param, "description", None),
            )
        )

    # Parse request body (including resolving $ref)
    request_body = None
    has_file_upload = False
    op_request_body = getattr(operation, "requestBody", None)

    if op_request_body:
        body = op_request_body

        # Resolve request body reference if needed
        if _is_reference(body):
            resolved = _resolve_ref(body, all_components, "requestBodies")
            if resolved is not None:
                body = resolved
            else:
                body = None  # Could not resolve

        if body and hasattr(body, "content"):
            content = getattr(body, "content", None) or {}

            # Try JSON first, then multipart, then form-urlencoded
            # Also check for JSON:API content type (application/vnd.api+json)
            json_content = content.get("application/json") or content.get("application/vnd.api+json")
            multipart_content = content.get("multipart/form-data")
            form_content = content.get("application/x-www-form-urlencoded")

            # Handle JSON content
            if json_content and hasattr(json_content, "media_type_schema"):
                body_schema = getattr(json_content, "media_type_schema", None)
                if _is_reference(body_schema):
                    ref_name = _get_ref_name(body_schema)
                    request_body = Schema(
                        name=ref_name,
                        class_name=to_class_name(ref_name),
                    )
                else:
                    # Check for anyOf/oneOf unions
                    any_of = getattr(body_schema, "anyOf", None)
                    one_of = getattr(body_schema, "oneOf", None)
                    if any_of:
                        # Handle anyOf union (FastAPI generates this for Union[A, B] types)
                        variant_names = _collect_union_variant_names(any_of, all_components)
                        if variant_names:
                            union_class_name = " | ".join(variant_names)
                            first_ref = any_of[0]
                            first_name = _get_ref_name(first_ref) if _is_reference(first_ref) else "Request"
                            request_body = Schema(
                                name=first_name,
                                class_name=union_class_name,
                            )
                    elif one_of:
                        # Handle discriminated union - create union type from all variants
                        variant_names = _collect_union_variant_names(one_of, all_components)
                        if variant_names:
                            union_class_name = " | ".join(variant_names)
                            first_ref = one_of[0]
                            first_name = _get_ref_name(first_ref) if _is_reference(first_ref) else "Request"
                            request_body = Schema(
                                name=first_name,
                                class_name=union_class_name,
                            )
                    else:
                        # Handle inline object schema (not a reference)
                        # Check if it has properties or is an object type
                        schema_type = getattr(body_schema, "type", None)
                        schema_type = getattr(schema_type, "value", schema_type)
                        schema_properties = getattr(body_schema, "properties", None)
                        if schema_properties:
                            # Generate a proper typed model for inline schema
                            model_name = _generate_request_body_name(operation_id)
                            inline_model = _parse_inline_schema_to_model(body_schema, model_name, components_schemas)
                            # Add to inline_schemas dict if provided
                            if inline_schemas is not None:
                                inline_schemas[model_name] = inline_model
                            request_body = Schema(
                                name=model_name,
                                class_name=inline_model.class_name,
                            )
                        elif schema_type == "object":
                            # No properties defined, use dict[str, Any]
                            request_body = Schema(
                                name="RequestBody",
                                class_name="dict[str, Any]",
                            )

            # Handle multipart/form-data (file uploads)
            elif multipart_content and hasattr(multipart_content, "media_type_schema"):
                has_file_upload = True
                body_schema = getattr(multipart_content, "media_type_schema", None)
                if _is_reference(body_schema):
                    ref_name = _get_ref_name(body_schema)
                    request_body = Schema(
                        name=ref_name,
                        class_name=to_class_name(ref_name),
                    )
                else:
                    # Inline multipart schema - create a generic name
                    request_body = Schema(
                        name="FormData",
                        class_name="dict[str, Any]",
                    )

            # Handle form-urlencoded
            elif form_content and hasattr(form_content, "media_type_schema"):
                body_schema = getattr(form_content, "media_type_schema", None)
                if _is_reference(body_schema):
                    ref_name = _get_ref_name(body_schema)
                    request_body = Schema(
                        name=ref_name,
                        class_name=to_class_name(ref_name),
                    )

    # Parse response (including resolving $ref)
    response_type = None
    responses = getattr(operation, "responses", None) or {}

    # Try 200, 201, 204 in order
    success_response = responses.get("200") or responses.get("201") or responses.get("204")

    if success_response:
        # Resolve response reference if needed
        if _is_reference(success_response):
            resolved = _resolve_ref(success_response, all_components, "responses")
            if resolved is not None:
                success_response = resolved
            else:
                success_response = None  # Could not resolve

        if success_response and hasattr(success_response, "content"):
            content = getattr(success_response, "content", None) or {}
            json_content = content.get("application/json")
            if json_content and hasattr(json_content, "media_type_schema"):
                resp_schema = getattr(json_content, "media_type_schema", None)
                if resp_schema:
                    response_type = parse_type_from_schema(resp_schema, components_schemas)

    return Endpoint(
        path=path,
        method=method.upper(),
        operation_id=operation_id,
        function_name=func_name,
        tag=tag,
        summary=getattr(operation, "summary", None),
        description=getattr(operation, "description", None),
        parameters=parameters,
        request_body=request_body,
        response_type=response_type,
        has_file_upload=has_file_upload,
    )


def _extract_base_path_from_servers(openapi: Any) -> str:
    """Extract base path from the first server URL in the OpenAPI spec.

    OpenAPI 3.0 says that paths are appended to the server URL, so if the server
    URL is 'https://example.com/api', then a path '/v1/accounts' becomes
    'https://example.com/api/v1/accounts'.

    This function extracts the path component (e.g., '/api') from the first server URL.
    """
    from urllib.parse import urlparse

    servers = getattr(openapi, "servers", None)
    if not servers or len(servers) == 0:
        return ""

    first_server = servers[0]
    server_url = getattr(first_server, "url", None)
    if not server_url:
        return ""

    # Parse the URL and extract the path component
    parsed = urlparse(server_url)
    base_path = parsed.path.rstrip("/")

    return base_path


def parse_openapi(spec: dict) -> API:
    """Parse OpenAPI spec into API model using openapi-pydantic."""
    # Parse spec using openapi-pydantic
    openapi = parse_obj(spec)

    info = openapi.info
    api = API(
        title=info.title,
        version=info.version,
    )

    # Extract base path from server URL (e.g., '/api' from 'https://example.com/api')
    base_path = _extract_base_path_from_servers(openapi)

    # Get all components for reference resolution
    all_components: dict[str, dict[str, Any]] = {
        "schemas": {},
        "parameters": {},
        "requestBodies": {},
        "responses": {},
    }

    components = getattr(openapi, "components", None)
    if components:
        # Collect schemas
        schemas = getattr(components, "schemas", None)
        if schemas:
            for name, schema in schemas.items():
                if not _is_reference(schema):
                    all_components["schemas"][name] = schema

        # Collect parameters
        parameters = getattr(components, "parameters", None)
        if parameters:
            for name, param in parameters.items():
                if not _is_reference(param):
                    all_components["parameters"][name] = param

        # Collect request bodies
        request_bodies = getattr(components, "requestBodies", None)
        if request_bodies:
            for name, body in request_bodies.items():
                if not _is_reference(body):
                    all_components["requestBodies"][name] = body

        # Collect responses
        responses = getattr(components, "responses", None)
        if responses:
            for name, resp in responses.items():
                if not _is_reference(resp):
                    all_components["responses"][name] = resp

    components_schemas = all_components["schemas"]

    # Parse schemas
    for name, schema in components_schemas.items():
        # Parse object schemas, schemas with properties, and enum schemas
        schema_type = getattr(schema, "type", None)
        schema_type = getattr(schema_type, "value", schema_type)
        schema_properties = getattr(schema, "properties", None)
        schema_enum = getattr(schema, "enum", None)
        if schema_type == "object" or schema_properties or schema_enum:
            api.schemas[name] = parse_schema_def(name, schema, components_schemas)

    # Parse paths - collect inline schemas as we go
    inline_schemas: dict[str, Schema] = {}
    paths = getattr(openapi, "paths", None)
    if paths:
        for path, path_item in paths.items():
            if path_item is None or _is_reference(path_item):
                continue

            # Prepend base path from server URL to endpoint path
            # e.g., base_path='/api' + path='/v1/accounts' = '/api/v1/accounts'
            full_path = base_path + path if base_path else path

            # Use duck typing - check if it has the method attributes
            if hasattr(path_item, "get"):
                methods = [
                    ("get", getattr(path_item, "get", None)),
                    ("post", getattr(path_item, "post", None)),
                    ("put", getattr(path_item, "put", None)),
                    ("patch", getattr(path_item, "patch", None)),
                    ("delete", getattr(path_item, "delete", None)),
                    ("head", getattr(path_item, "head", None)),
                    ("options", getattr(path_item, "options", None)),
                ]
                for method_name, operation in methods:
                    if operation:
                        endpoint = parse_endpoint_from_operation(
                            full_path,
                            method_name,
                            operation,
                            components_schemas,
                            all_components,
                            inline_schemas,
                        )
                        api.endpoints.append(endpoint)
                        api.tags.add(endpoint.tag)

    # Add inline schemas (request body models) to the API schemas
    for name, schema in inline_schemas.items():
        if name not in api.schemas:
            api.schemas[name] = schema

    return api
