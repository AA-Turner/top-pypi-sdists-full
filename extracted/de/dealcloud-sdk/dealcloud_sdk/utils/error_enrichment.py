"""Opt-in utilities to enrich DealCloud write error payloads with schema metadata.

These helpers are **not** wired into standard write paths (``process_errors``,
``format_row_error_message``, etc.). Call them explicitly after inspecting
``row_errors`` or Cells store responses.
"""

from __future__ import annotations

from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from ..models.schema import Field

FieldLookup = dict[int, dict[str, str]]
"""Maps field id → ``{"name": display_name, "apiName": api_name}``."""

_CODE_DESCRIPTIONS_ENGLISH: dict[int, str] = {
    5010: "Can't change value in calculated or smart field.",
}


def field_lookup_from_fields(fields: list[Field]) -> FieldLookup:
    """Build a :class:`FieldLookup` from schema :class:`~dealcloud_sdk.models.schema.Field` objects."""
    lookup: FieldLookup = {}
    for field in fields:
        if field.id is None:
            continue
        entry: dict[str, str] = {}
        if field.name:
            entry["name"] = str(field.name)
        if field.apiName:
            entry["apiName"] = str(field.apiName)
        if entry:
            lookup[int(field.id)] = entry
    return lookup


def build_field_lookup(
    field_map: dict,
    object_name: str,
    schema: Any | None = None,
) -> FieldLookup:
    """Build a :class:`FieldLookup` from ``get_field_map()`` output for one object."""
    lookup: FieldLookup = {}

    for meta in (field_map.get(object_name) or {}).values():
        if not isinstance(meta, dict):
            continue
        field_id = meta.get("id")
        if field_id is None:
            continue
        entry: dict[str, str] = {}
        name = meta.get("name")
        api_name = meta.get("apiName")
        if name:
            entry["name"] = str(name)
        if api_name:
            entry["apiName"] = str(api_name)
        if entry:
            lookup[int(field_id)] = entry

    if schema is None:
        return lookup

    objects = getattr(schema, "objects", None)
    if objects is None and isinstance(schema, dict):
        objects = schema.get("objects")
    if not objects:
        return lookup

    obj = objects.get(object_name) if hasattr(objects, "get") else None
    if obj is None:
        return lookup

    fields = getattr(obj, "fields", None)
    if fields is None and isinstance(obj, dict):
        fields = obj.get("fields")
    if not fields:
        return lookup

    field_values = fields.values() if isinstance(fields, dict) else fields
    for field in field_values:
        if isinstance(field, dict):
            field_id = field.get("id")
            name = field.get("name")
            api_name = field.get("apiName")
        else:
            field_id = getattr(field, "id", None)
            name = getattr(field, "name", None)
            api_name = getattr(field, "apiName", None)
        if field_id is None:
            continue
        entry: dict[str, str] = {}
        if name:
            entry["name"] = str(name)
        if api_name:
            entry["apiName"] = str(api_name)
        if entry:
            lookup[int(field_id)] = entry

    return lookup


def iter_row_error_items(error_row: dict[str, Any]) -> list[dict[str, Any]]:
    """Normalize a DealCloud row or Cells error payload into per-field error dicts."""
    items: list[dict[str, Any]] = []

    for err in error_row.get("Errors") or []:
        if not isinstance(err, dict):
            continue
        items.append(
            {
                "fieldId": err.get("fieldId"),
                "field": err.get("field"),
                "code": err.get("code"),
                "description": err.get("description", ""),
            }
        )

    if items:
        return items

    nested = error_row.get("error")
    if isinstance(nested, dict) and nested:
        items.append(
            {
                "fieldId": error_row.get("fieldId"),
                "field": nested.get("field"),
                "code": nested.get("code"),
                "description": nested.get("description", ""),
            }
        )

    return items


def _resolve_field_meta(
    field_id: Any,
    field_key: Any,
    lookup: FieldLookup,
) -> tuple[str | None, str | None]:
    if field_id is not None:
        try:
            meta = lookup.get(int(field_id))
            if meta:
                return meta.get("name"), meta.get("apiName")
        except (TypeError, ValueError):
            pass
    if field_key not in (None, "", "0", 0, "?"):
        return str(field_key), None
    return None, None


def enrich_row_errors(
    error_row: dict[str, Any],
    field_lookup: FieldLookup,
    *,
    object_name: str | None = None,
) -> list[dict[str, Any]]:
    """Attach ``fieldName``, ``apiName``, and normalized keys to each error item."""
    entry_id = error_row.get("EntryId", error_row.get("entryId"))
    enriched: list[dict[str, Any]] = []
    for item in iter_row_error_items(error_row):
        field_id = item.get("fieldId")
        field_name, api_name = _resolve_field_meta(
            field_id, item.get("field"), field_lookup
        )
        enriched.append(
            {
                "entryId": entry_id,
                "fieldId": field_id,
                "fieldName": field_name,
                "apiName": api_name,
                "code": item.get("code"),
                "description": item.get("description", ""),
                "objectName": object_name,
            }
        )
    return enriched


def format_error_with_metadata(
    enriched_item: dict[str, Any],
    *,
    include_entry_id: bool = True,
) -> str:
    """Format one enriched error with API description plus bracketed schema metadata."""
    entry_id = enriched_item.get("entryId")
    description = enriched_item.get("description", "")
    field_name = enriched_item.get("fieldName")
    api_name = enriched_item.get("apiName")
    field_id = enriched_item.get("fieldId")
    obj_name = enriched_item.get("objectName")

    bracket_parts: list[str] = []
    if obj_name:
        bracket_parts.append(str(obj_name))
    if field_name:
        bracket_parts.append(f"fieldName {field_name}")
    elif field_id is not None:
        bracket_parts.append("fieldName ?")
    if api_name:
        bracket_parts.append(f"apiName {api_name}")
    if field_id is not None:
        bracket_parts.append(f"fieldId {field_id}")

    detail = description
    if bracket_parts:
        detail += f" [{', '.join(bracket_parts)}]"

    if include_entry_id and entry_id is not None:
        return f"EntryId {entry_id}: {detail}"
    if include_entry_id:
        return f"row: {detail}"
    return detail


def _english_description(enriched_item: dict[str, Any]) -> str:
    description = (enriched_item.get("description") or "").strip()
    if description:
        return description
    code = enriched_item.get("code")
    if code is not None:
        try:
            return _CODE_DESCRIPTIONS_ENGLISH.get(int(code), "An error occurred.")
        except (TypeError, ValueError):
            pass
    return "An error occurred."


def format_error_message_english(enriched_item: dict[str, Any]) -> str:
    """Format one enriched error as plain English (no field ids or entry ids)."""
    description = _english_description(enriched_item)
    field_name = enriched_item.get("fieldName")
    obj_name = enriched_item.get("objectName")

    if field_name and obj_name:
        return (
            f"The {field_name} field on {obj_name} could not be updated: {description}."
        )
    if field_name:
        return f"The {field_name} field could not be updated: {description}."
    if obj_name:
        return f"A field on {obj_name} could not be updated: {description}."
    return f"A field could not be updated: {description}."


def format_row_error_with_metadata(
    error_row: dict[str, Any],
    *,
    field_lookup: FieldLookup,
    object_name: str | None = None,
) -> str:
    """Enrich a row error payload and format with metadata brackets."""
    items = enrich_row_errors(error_row, field_lookup, object_name=object_name)
    if not items:
        entry_id = error_row.get("EntryId", error_row.get("entryId"))
        prefix = f"EntryId {entry_id}" if entry_id is not None else "row"
        return f"{prefix}: {error_row}"

    entry_id = error_row.get("EntryId", error_row.get("entryId"))
    parts = [format_error_with_metadata(item) for item in items]
    if len(parts) == 1:
        return parts[0]

    prefix = f"EntryId {entry_id}" if entry_id is not None else "row"
    details = "; ".join(
        part.split(": ", 1)[1] if ": " in part else part for part in parts
    )
    return f"{prefix}: {details}"


def format_row_error_message_english(
    error_row: dict[str, Any],
    *,
    field_lookup: FieldLookup,
    object_name: str | None = None,
) -> str:
    """Enrich a row error payload and format as plain English."""
    items = enrich_row_errors(error_row, field_lookup, object_name=object_name)
    if not items:
        return "A field could not be updated."

    parts = [format_error_message_english(item) for item in items]
    return " ".join(parts)
