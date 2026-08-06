import json
from typing import Optional, Type
from copy import deepcopy

from pydantic import BaseModel, ConfigDict, Field, create_model, model_validator

from xpander_sdk.modules.tools_repository.utils.generic import (
    json_type_to_python,
    pascal_case,
)
from xpander_sdk.utils.json_parsing import parse_structured_string

from pydantic import BaseModel, create_model, ConfigDict
from typing import Optional, Type, Dict, Any


class _CoercingPayloadBase(BaseModel):
    """Base for dynamically-built tool payload schemas.

    LLMs sometimes pass the payload arg as a JSON-encoded string
    (`payload='{"body_params": {...}}'`) instead of a dict. This before-validator
    parses the string back to a dict so the first tool call doesn't fail with a
    confusing model_type validation error. Plain non-JSON strings fall through
    and still surface the regular validation error.
    """

    model_config = ConfigDict(strict=False, extra="allow")

    @model_validator(mode="before")
    @classmethod
    def _coerce_string_payload(cls, data: Any) -> Any:
        # Bounded to two layers: models sometimes JSON-encode the payload, then
        # JSON-encode that string again (arrives quote-wrapped).
        for _ in range(2):
            if not isinstance(data, str):
                break
            parsed = parse_structured_string(data)
            if isinstance(parsed, dict):
                data = parsed
                break
            try:
                peeled = json.loads(data)
            except Exception:
                break
            if isinstance(peeled, str) and peeled != data:
                data = peeled
                continue
            break
        if isinstance(data, dict):
            inner = data.get("payload")
            if isinstance(inner, str) and "payload" not in cls.model_fields:
                parsed = parse_structured_string(inner)
                if isinstance(parsed, dict):
                    data = {**data, "payload": parsed}
        if isinstance(data, dict):
            data = cls._unwrap_redundant_payload(data)
            data = cls._nest_flat_body_params(data)
            data = cls._hoist_misplaced_reasoning_headers(data)
            data = cls._fill_missing_reasoning_fields(data)
        return data

    @classmethod
    def _unwrap_redundant_payload(cls, data: dict) -> dict:
        """LLMs sometimes double-wrap the payload: because the tool's single arg is
        literally named ``payload`` AND its docs say "wrap in a payload object", a weak
        model emits ``{"payload": {"payload": {...}}}``. Agno binds the outer wrapper,
        so this validator receives ``{"payload": {body_params: …}}`` - a lone ``payload``
        key holding a payload-shaped dict. Left alone, _nest_flat_body_params buries that
        stray key inside body_params and every field reads as "Field required". Unwrap one
        redundant level so the inner payload validates. No-op when the model legitimately
        has its own ``payload`` field, or when ``payload`` isn't the lone meaningful key."""
        if "payload" not in data or "payload" in cls.model_fields:
            return data
        inner = data["payload"]
        if not isinstance(inner, dict):
            return data
        siblings = {k: v for k, v in data.items() if k != "payload"}
        # A stray outer "headers" dict rides along with the wrapped payload just like
        # bare toolcall* keys do; anything else means a genuinely different envelope.
        if any(
            k != "headers" and not str(k).lower().startswith("toolcall")
            for k in siblings
        ):
            return data
        payload_shape = {"body_params", "query_params", "path_params", "headers", "workspace_path"}
        if not (payload_shape & set(inner) or set(cls.model_fields) & set(inner)):
            return data
        # Carry the outer toolcall* reasoning headers into the unwrapped inner payload
        # (without clobbering any the inner already has) so the activity-log label survives.
        if siblings:
            inner = {**inner}
            for k, v in siblings.items():
                inner.setdefault(k, v)
        return inner

    @classmethod
    def _nest_flat_body_params(cls, data: dict) -> dict:
        """LLMs sometimes drop the ``body_params`` envelope and pass the request
        body flat at the payload top level (``{"path": …, "content": …}``
        instead of ``{"body_params": {"path": …, "content": …}}``). Those stray
        keys land as ignored ``extra`` fields and the tool runs with an empty
        body (Mercury: a silent ``xpworkspace-file-write`` no-op). Move top-level
        keys that aren't part of the payload contract into ``body_params`` so the
        call carries the arguments the model intended, merging with any partial
        body_params already present without overwriting its keys. No-op unless the
        model has a ``body_params`` field; skipped when query/path params are
        populated to avoid misrouting a genuinely different envelope — unless
        ``body_params`` is required and absent, where bailing out guarantees a
        "Field required" failure and nesting is the only viable read."""
        if "body_params" not in cls.model_fields:
            return data
        body_required_and_missing = cls.model_fields[
            "body_params"
        ].is_required() and not isinstance(data.get("body_params"), dict)
        if not body_required_and_missing:
            for envelope in ("query_params", "path_params"):
                val = data.get(envelope)
                if isinstance(val, dict) and val:
                    return data
        reserved = set(cls.model_fields) | {"headers", "workspace_path"}
        stray = {
            k: v
            for k, v in data.items()
            if k not in reserved and not str(k).lower().startswith("toolcall")
        }
        if not stray:
            return data
        existing = data.get("body_params")
        merged = dict(existing) if isinstance(existing, dict) else {}
        for k, v in stray.items():
            merged.setdefault(k, v)
        result = {k: v for k, v in data.items() if k not in stray}
        result["body_params"] = merged
        return result

    @staticmethod
    def _hoist_misplaced_reasoning_headers(data: dict) -> dict:
        """LLMs sometimes nest the reasoning ``headers`` dict (toolcall* keys)
        inside body_params/query_params/path_params instead of at the payload
        top level. Move it up so validation passes and the reasoning metadata
        reaches the activity log instead of leaking into the request body. A
        genuine body field named ``headers`` (any non-toolcall key) is left
        untouched."""
        result = data
        for container_name in ("body_params", "query_params", "path_params"):
            container = result.get(container_name)
            if not isinstance(container, dict):
                continue
            nested = container.get("headers")
            if not (
                isinstance(nested, dict)
                and nested
                and all(str(k).lower().startswith("toolcall") for k in nested)
            ):
                continue
            if result is data:
                result = dict(data)
            container = dict(container)
            container.pop("headers")
            result[container_name] = container
            top_headers = result.get("headers")
            if not (isinstance(top_headers, dict) and top_headers):
                result["headers"] = nested
        return result

    @classmethod
    def _fill_missing_reasoning_fields(cls, data: dict) -> dict:
        """toolcall* reasoning fields stay REQUIRED in the emitted JSON schema
        so LLMs fill them (a pydantic default would drop them from ``required``),
        but a weak model omitting them must never block the tool call
        (PRO-1928). Backfill absent/None required toolcall* fields with "" and
        an absent reasoning-only ``headers`` group with {}. Genuinely required
        fields (e.g. API headers) are never backfilled and keep failing loudly."""
        result = data
        for name, field in cls.model_fields.items():
            if not field.is_required():
                continue
            if name.lower().startswith("toolcall"):
                if result.get(name) is not None:
                    continue
                if result is data:
                    result = dict(data)
                result[name] = ""
            elif name == "headers" and name not in result:
                ann = field.annotation
                if not (
                    isinstance(ann, type)
                    and issubclass(ann, _CoercingPayloadBase)
                    and all(
                        n.lower().startswith("toolcall")
                        for n, f in ann.model_fields.items()
                        if f.is_required()
                    )
                ):
                    continue
                if result is data:
                    result = dict(data)
                result[name] = {}
        return result


# Serialized into every tool's schema — keep short; full protocol lives in LARGE_PAYLOAD_AUTHORING_INSTRUCTIONS.
WORKSPACE_PATH_FIELD_DESCRIPTION = (
    "[OPTIONAL] Relative workspace file holding this tool's full JSON payload. For large "
    "payloads (>= ~4000 chars) write the JSON via xpworkspace-file-write and set this "
    "instead of inlining args (inline params are then ignored); chunk the write (first "
    "mode='w', then mode='a') only when the JSON exceeds ~8000 chars. Leave null for "
    "normal calls."
)

# Single source for the payload-wrapper contract; interpolated wherever tool docs state it.
PAYLOAD_WRAPPER_RULE = "Wrap all arguments in a single 'payload' object"


def build_model_from_schema(
    model_name: str,
    schema: dict,
    with_defaults: Optional[bool] = False,
    inject_workspace_path: bool = True,
) -> Type[BaseModel]:
    fields = {}
    properties = schema.get("properties", {})
    required = set(schema.get("required", []))

    # The backend's required-ness for toolcall* reasoning headers is preserved
    # as-is (title required, description optional) — the LLM-facing function
    # schema is generated from this model, and models only reliably fill the
    # reasoning title when the schema marks it required. Omission tolerance
    # lives in _CoercingPayloadBase._fill_missing_reasoning_fields (PRO-1928),
    # not in the schema.

    # CRITICAL FIX: Add default={} to empty parameter containers
    # This allows LLMs to omit them when they have no actual content
    for param_name in ("body_params", "query_params", "path_params", "headers"):
        if param_name in properties:
            param_schema = properties[param_name]
            if (
                param_schema.get("type") == "object"
                and "properties" in param_schema
                and len(param_schema.get("properties", {})) == 0
                and "default" not in param_schema
            ):
                param_schema["default"] = {}

    FIELD_SPECS = {
        "body_params": (
            Optional[Dict[str, Any]],
            Field(
                default={},
                description="Request body parameters (default: empty object).",
            ),
        ),
        "query_params": (
            Optional[Dict[str, Any]],
            Field(
                default={},
                description="Request query parameters (default: empty object).",
            ),
        ),
        "path_params": (
            Optional[Dict[str, Any]],
            Field(
                default={},
                description="Request path parameters (default: empty object).",
            ),
        ),
    }

    # If with_defaults is True and schema is empty, set all three params
    if with_defaults and not properties:
        fields = FIELD_SPECS.copy()
    else:
        for prop_name, prop_schema in properties.items():
            # Skip invalid field names starting with "_"
            if prop_name.startswith("_"):
                continue
            prop_type = prop_schema.get("type")
            description = prop_schema.get("description", None)
            default = prop_schema.get("default", None)

            # Nested object support
            # CRITICAL: Check if this is an empty parameter container
            is_empty_param_container = False
            if prop_type == "object" and "properties" in prop_schema:
                nested_props = prop_schema.get("properties", {})
                nested_required = prop_schema.get("required", [])
                # Empty if no properties or all properties are optional/empty
                is_empty_param_container = len(nested_props) == 0 or (
                    len(nested_required) == 0
                    and all(
                        p.get("type") == "object" and len(p.get("properties", {})) == 0
                        for p in nested_props.values()
                    )
                )

                # For empty parameter containers, use Dict instead of nested model
                if is_empty_param_container and prop_name in (
                    "body_params",
                    "query_params",
                    "path_params",
                    "headers",
                ):
                    base_type = Dict[str, Any]
                else:
                    nested_model_name = f"{model_name}{pascal_case(prop_name)}"
                    base_type = build_model_from_schema(
                        nested_model_name,
                        prop_schema,
                        inject_workspace_path=False,
                    )
            else:
                # Pass the full property schema to handle anyOf correctly
                base_type = json_type_to_python(prop_type, prop_schema)

            # Field annotation and Field() construction
            # IMPORTANT: For fields marked as required in the JSON schema, don't wrap in Optional[]
            # Even if they might be nullable, the type annotation determines Pydantic's required array
            # EXCEPTION: Empty parameter containers should always be Optional with default={}
            if is_empty_param_container:
                annotation = Optional[base_type]
            else:
                annotation = base_type if prop_name in required else Optional[base_type]

            field_args = {}

            # Marker only — the payload-wrapper rule is stated once at the model level to avoid per-field schema bloat.
            enhanced_description = description or f"Parameter: {prop_name}"

            if is_empty_param_container:
                enhanced_description = (
                    f"[OPTIONAL] {enhanced_description} (default: empty object)"
                )
            elif prop_name in required:
                if default is not None:
                    enhanced_description = (
                        f"[REQUIRED] {enhanced_description} (default: {default})"
                    )
                else:
                    enhanced_description = f"[REQUIRED] {enhanced_description}"
            else:
                if default is not None:
                    enhanced_description = (
                        f"[OPTIONAL] {enhanced_description} (default: {default})"
                    )
                else:
                    enhanced_description = f"[OPTIONAL] {enhanced_description}"

            field_args["description"] = enhanced_description

            # Set default or ... (required)
            # The key insight: Pydantic includes a field in the 'required' array of model_json_schema()
            # if and only if the field has Field(...) (no default) AND is not Optional[] in type annotation
            if is_empty_param_container:
                # Empty containers always get default={}
                field_info = Field(default={}, **field_args)
            elif prop_name in required:
                if default is not None:
                    # Has a default but still required in schema - use the default
                    field_info = Field(default, **field_args)
                else:
                    # No default and required - use ellipsis
                    field_info = Field(..., **field_args)
            else:
                # Optional fields - always provide a default to keep them out of 'required' array
                if default is not None:
                    field_info = Field(default, **field_args)
                else:
                    # Optional with no explicit default - use None
                    field_info = Field(default=None, **field_args)

            fields[prop_name] = (annotation, field_info)

        # Ensure the presence of all three params if with_defaults is True
        if with_defaults:
            for key, (annotation, field_info) in FIELD_SPECS.items():
                if key not in fields:
                    fields[key] = (annotation, field_info)

    # After building fields, relax body/query/path if present and not already optional with a default
    # CRITICAL FIX: Empty parameter containers (query_params, path_params, body_params) that are marked
    # as required but have no actual properties should default to {} so LLMs can omit them
    for param in ("body_params", "query_params", "path_params"):
        if param in fields:
            ann, fld = fields[param]
            # Check if this field is required (has Ellipsis as default) or has no useful default
            has_no_default = (
                getattr(fld, "default", ...) is ...
                or getattr(fld, "default", None) is None
            ) and getattr(fld, "default_factory", None) is None

            # Always make param containers Optional with default={} to allow LLMs to omit empty ones
            if (
                has_no_default
                or ann is dict
                or ann is Dict[str, Any]
                or (hasattr(ann, "__origin__") and ann.__origin__ in (dict, Dict))
            ):
                desc = (
                    getattr(fld, "description", None)
                    or f"Request {param.replace('_', ' ')} (default: empty object)."
                )
                fields[param] = (
                    Optional[Dict[str, Any]],
                    Field(default={}, description=desc),
                )

    if inject_workspace_path:
        fields["workspace_path"] = (
            Optional[str],
            Field(default=None, description=WORKSPACE_PATH_FIELD_DESCRIPTION),
        )

    # Concrete field names in the example (not a "<fields>" placeholder) so this
    # schema-level hint matches the tool function's docstring hint — a consistent
    # wrap-in-payload example in both places, so LLMs don't set args inline.
    example_fields = {name: "..." for name in fields if name != "workspace_path"}
    model_doc = (
        f'{PAYLOAD_WRAPPER_RULE}: {json.dumps({"payload": example_fields})}. '
        "Required fields must be provided; optional fields may be omitted or null."
    )

    model = create_model(
        model_name,
        __base__=_CoercingPayloadBase,
        __doc__=model_doc,
        **fields,
    )
    # `__config__` cannot be combined with `__base__` in pydantic v2 create_model;
    # carry the strict/extra defaults from the base class and overlay per-model title here.
    model.model_config = {**model.model_config, "title": model_name}
    return model


def schema_enforcement_block_and_descriptions(
    target_schema: dict, reference_schema: dict
) -> dict:
    updated_schema = deepcopy(target_schema)

    def update_properties(target_props: dict, ref_props: dict):
        to_delete = []
        for key, ref_value in ref_props.items():
            if key not in target_props:
                continue

            # Remove if isBlocked or permanentValue present
            if ref_value.get("isBlocked") is True or "permanentValue" in ref_value:
                to_delete.append(key)
                continue

            target_field = target_props[key]

            # Override description if available
            if "description" in ref_value:
                target_field["description"] = ref_value["description"]

            # Recursively update nested objects
            if (
                ref_value.get("type") == "object"
                and "properties" in ref_value
                and target_field.get("type") == "object"
                and "properties" in target_field
            ):
                update_properties(target_field["properties"], ref_value["properties"])

        # Remove blocked/permanent fields
        for key in to_delete:
            del target_props[key]

    def walk(target: dict, ref: dict):
        if not isinstance(target, dict) or not isinstance(ref, dict):
            return

        if (
            target.get("type") == "object"
            and "properties" in target
            and "properties" in ref
        ):
            update_properties(target["properties"], ref["properties"])
            for key in list(target["properties"]):
                walk(target["properties"][key], ref["properties"].get(key, {}))

    walk(updated_schema, reference_schema)
    return updated_schema


def apply_permanent_values_to_payload(
    schema: dict, payload: dict | list
) -> dict | list:
    payload = deepcopy(payload)

    def apply(schema_node, payload_node):
        if not isinstance(schema_node, dict):
            return

        schema_type = schema_node.get("type")

        if schema_type == "object" and "properties" in schema_node:
            if not isinstance(payload_node, dict):
                return  # skip if payload_node is not an object

            for key, sub_schema in schema_node["properties"].items():
                # If permanentValue is present, enforce it
                if "permanentValue" in sub_schema:
                    payload_node[key] = sub_schema["permanentValue"]

                # Recurse
                if sub_schema.get("type") == "object":
                    payload_node.setdefault(key, {})
                    apply(sub_schema, payload_node[key])
                elif (
                    sub_schema.get("type") == "array"
                    and sub_schema.get("items", {}).get("type") == "object"
                ):
                    payload_node.setdefault(key, [{}])  # if empty, create one
                    if isinstance(payload_node[key], list):
                        for item in payload_node[key]:
                            apply(sub_schema["items"], item)

        elif (
            schema_type == "array"
            and schema_node.get("items", {}).get("type") == "object"
        ):
            if isinstance(payload_node, list):
                for item in payload_node:
                    apply(schema_node["items"], item)

    apply(schema, payload)
    return payload


def enforce_schema_on_response(schema: dict, response: dict | list) -> dict | list:
    response = deepcopy(response)

    def apply(schema_node, response_node):
        if not isinstance(schema_node, dict):
            return

        schema_type = schema_node.get("type")

        if schema_type == "object" and "properties" in schema_node:
            if not isinstance(response_node, dict):
                return

            for key in list(response_node.keys()):
                sub_schema = schema_node["properties"].get(key)

                # If key not in schema, ignore
                if not sub_schema:
                    continue

                # Remove if blocked
                if sub_schema.get("isBlocked"):
                    del response_node[key]
                    continue

                # Set permanentValue if defined
                if "permanentValue" in sub_schema:
                    response_node[key] = sub_schema["permanentValue"]

                # Recurse if it's a nested object
                if sub_schema.get("type") == "object" and isinstance(
                    response_node.get(key), dict
                ):
                    apply(sub_schema, response_node[key])

                # Recurse if it's an array of objects
                elif sub_schema.get("type") == "array" and isinstance(
                    response_node.get(key), list
                ):
                    item_schema = sub_schema.get("items")
                    if item_schema and item_schema.get("type") == "object":
                        for item in response_node[key]:
                            apply(item_schema, item)

        elif (
            schema_type == "array"
            and schema_node.get("items", {}).get("type") == "object"
        ):
            if isinstance(response_node, list):
                for item in response_node:
                    apply(schema_node["items"], item)

    apply(schema, response)
    return response
