"""Auto-detect and inject multipart/form-data examples into OpenAPI schemas.

This module provides the schema patcher for the file upload examples plugin.
It auto-discovers routes whose endpoint parameters use
``Form(openapi_examples=...)`` and injects the examples at the media-type
level where Swagger UI can render them via the companion JS plugin.
"""

import json
import typing

from fastapi import FastAPI

from .._base import SchemaContext


def _attr(obj: object, name: str, default: object = None) -> object:
    """Read *name* from an object (attr) or dict (key).

    FastAPI's ``Example(...)`` returns a plain dict, not an object, so
    we need to handle both access patterns.
    """
    try:
        return getattr(obj, name)
    except AttributeError:
        return obj.get(name, default) if isinstance(obj, dict) else default


def _discover(app: FastAPI) -> dict[str, dict]:
    """Find routes whose endpoint params have ``Form(openapi_examples=...)``.

    Returns a dict mapping route paths to dicts with ``examples`` and
    an optional ``schema_name`` derived from the ``x-schema-name``
    marker set by :func:`file_upload_body`.
    """
    from fastapi.params import Body, Form
    from fastapi.routing import APIRoute

    result: dict[str, dict] = {}
    for route in app.routes:
        if not isinstance(route, APIRoute):
            continue
        examples: dict = {}
        schema_name: str | None = None
        try:
            hints = typing.get_type_hints(route.endpoint, include_extras=True)
        except Exception:
            continue
        for hint in hints.values():
            if not hasattr(hint, "__metadata__"):
                continue
            for meta in hint.__metadata__:
                if isinstance(meta, (Form, Body)):
                    ex = getattr(meta, "openapi_examples", None)
                    if ex:
                        examples.update(ex)
                    extra = getattr(meta, "json_schema_extra", None)
                    if isinstance(extra, dict) and "x-schema-name" in extra:
                        schema_name = extra["x-schema-name"]
        if examples:
            result[route.path] = {
                "examples": examples,
                "schema_name": schema_name,
            }
    return result


def _inject(schema: dict, path_data: dict[str, dict], prefix: str = "") -> None:
    """Mutate *schema* in-place, adding examples and renaming schemas.

    Supports POST, PUT, and PATCH methods.  Route paths discovered from
    the sub-app are un-prefixed (e.g. ``/documents``), but the OpenAPI
    schema may already have the normalised prefix applied
    (e.g. ``/api/documents``).  We check both variants.
    """
    schema_paths = schema.get("paths", {})
    renames: dict[str, str] = {}  # old_name → new_name
    for route_path, data in path_data.items():
        examples = data["examples"]
        schema_name = data.get("schema_name")
        # The sub-app route is un-prefixed; the schema may be prefixed.
        if route_path in schema_paths:
            schema_path = route_path
        elif prefix and f"{prefix}{route_path}" in schema_paths:
            schema_path = f"{prefix}{route_path}"
        else:
            continue
        for method in ("post", "put", "patch"):
            content = (
                schema_paths[schema_path].get(method, {}).get("requestBody", {}).get("content", {})
            )
            mp = content.get("multipart/form-data")
            if mp is None:
                continue
            mp["examples"] = {
                key: {
                    "summary": _attr(ex, "summary", key),
                    "description": _attr(ex, "description", ""),
                    "value": json.dumps(_attr(ex, "value"), indent=2, sort_keys=True),
                }
                for key, ex in examples.items()
            }
            # Collect rename: resolve the $ref to find the old schema key
            if schema_name:
                ref = mp.get("schema", {}).get("$ref", "")
                if ref.startswith("#/components/schemas/"):
                    old_name = ref.split("/")[-1]
                    if old_name != schema_name:
                        renames[old_name] = schema_name
    # Apply renames: update schema keys and all $ref pointers
    if renames:
        _rename_schemas(schema, renames)


def _rename_schemas(schema: dict, renames: dict[str, str]) -> None:
    """Rename schema keys in ``components/schemas`` and update all ``$ref``s.

    When multiple Body wrappers map to the same target name (e.g. two
    routes sharing the same ``file_upload_body`` type), a numeric suffix
    is appended to avoid collisions (``DocumentRequestBody2``, etc.).
    """
    schemas = schema.get("components", {}).get("schemas", {})
    used: set[str] = set()
    for old_name, desired_name in renames.items():
        if old_name not in schemas:
            continue
        new_name = desired_name
        if new_name in schemas or new_name in used:
            counter = 2
            while f"{desired_name}{counter}" in schemas or f"{desired_name}{counter}" in used:
                counter += 1
            new_name = f"{desired_name}{counter}"
        used.add(new_name)
        schemas[new_name] = schemas.pop(old_name)
        schemas[new_name]["title"] = new_name
        _update_refs(
            schema,
            f"#/components/schemas/{old_name}",
            f"#/components/schemas/{new_name}",
        )


def _update_refs(obj: object, old_ref: str, new_ref: str) -> None:
    """Recursively replace ``$ref`` values throughout the schema."""
    if isinstance(obj, dict):
        if obj.get("$ref") == old_ref:
            obj["$ref"] = new_ref
        for v in obj.values():
            _update_refs(v, old_ref, new_ref)
    elif isinstance(obj, list):
        for item in obj:
            _update_refs(item, old_ref, new_ref)


def patch_file_upload_examples(schema: dict, ctx: SchemaContext) -> dict:
    """Schema patcher: discover file-upload routes and inject examples.

    This is the transformer function passed as ``schema_patcher`` in the
    plugin's :meth:`contribute` return value.  It follows the
    ``(schema, ctx) -> schema`` transformer pattern.
    """
    path_data = _discover(ctx.app)
    if path_data:
        _inject(schema, path_data, prefix=ctx.prefix)
    return schema
