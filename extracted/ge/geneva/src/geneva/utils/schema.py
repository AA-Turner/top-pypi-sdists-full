# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

from __future__ import annotations

import logging
import re
from types import UnionType
from typing import (
    TYPE_CHECKING,
    Any,
    Union,
    cast,
    get_args,
    get_origin,
    get_type_hints,
)

import attrs
import pyarrow as pa

from geneva.utils.arrow import _field_pa_type

if TYPE_CHECKING:
    from lancedb import Connection, Table  # type: ignore[attr-defined]

_LOG = logging.getLogger(__name__)
_UNQUOTED_FIELD_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


@attrs.define(frozen=True)
class FieldPathResolution:
    """Resolved Arrow field path with Lance-compatible canonical spelling."""

    canonical_path: str
    segments: tuple[str, ...]
    field: pa.Field
    nullable: bool

    def as_projected_field(self) -> pa.Field:
        return pa.field(
            self.canonical_path,
            self.field.type,
            nullable=self.nullable,
            metadata=self.field.metadata,
        )


def parse_field_path(path: str) -> list[str]:
    """Parse a Lance field path into segments.

    Dots split unquoted segments. Backtick-quoted segments are literal and use
    doubled backticks to represent a backtick inside the field name.
    """

    if path == "":
        raise ValueError("Field path cannot be empty")

    segments: list[str] = []
    current: list[str] = []
    in_quotes = False
    quoted_segment = False
    i = 0

    while i < len(path):
        char = path[i]
        if in_quotes:
            if char == "`":
                if i + 1 < len(path) and path[i + 1] == "`":
                    current.append("`")
                    i += 2
                    continue
                in_quotes = False
                i += 1
                if i < len(path) and path[i] != ".":
                    raise ValueError(f"Invalid field path {path!r}")
                continue
            current.append(char)
            i += 1
            continue

        if char == ".":
            if not current and not quoted_segment:
                raise ValueError(f"Invalid empty field path segment in {path!r}")
            segments.append("".join(current))
            current = []
            quoted_segment = False
            i += 1
            if i == len(path):
                raise ValueError(f"Invalid trailing dot in field path {path!r}")
            continue

        if char == "`":
            if current or quoted_segment:
                raise ValueError(f"Invalid quoted segment in field path {path!r}")
            in_quotes = True
            quoted_segment = True
            i += 1
            continue

        current.append(char)
        i += 1

    if in_quotes:
        raise ValueError(f"Unclosed quoted field path segment in {path!r}")
    if not current and not quoted_segment:
        raise ValueError(f"Invalid empty field path segment in {path!r}")
    segments.append("".join(current))
    return segments


def format_field_path(segments: list[str] | tuple[str, ...]) -> str:
    """Format field path segments using Lance-compatible backtick quoting."""

    formatted: list[str] = []
    for segment in segments:
        if _UNQUOTED_FIELD_RE.match(segment):
            formatted.append(segment)
        else:
            formatted.append(f"`{segment.replace('`', '``')}`")
    return ".".join(formatted)


def _field_index_case_insensitive(
    names: list[str], segment: str, full_path: str
) -> int:
    try:
        return names.index(segment)
    except ValueError:
        pass

    lowered = segment.lower()
    matches = [idx for idx, name in enumerate(names) if name.lower() == lowered]
    if not matches:
        raise KeyError(full_path)
    if len(matches) > 1:
        raise ValueError(f"Ambiguous field path {full_path!r}")
    return matches[0]


def resolve_arrow_field_path(schema: pa.Schema, path: str) -> FieldPathResolution:
    """Resolve a user field path against an Arrow schema.

    Resolution follows the LanceDB contract: parse backtick-escaped path
    segments, resolve names case-insensitively where unambiguous, and return the
    canonical path formatted from the actual schema field names.
    """

    parsed_segments = parse_field_path(path)
    schema_names = list(schema.names)
    idx = _field_index_case_insensitive(schema_names, parsed_segments[0], path)
    field = schema.field(idx)
    canonical_segments = [field.name]
    nullable = field.nullable

    for segment in parsed_segments[1:]:
        dtype = field.type
        if not pa.types.is_struct(dtype):
            raise KeyError(path)
        struct_type = cast("pa.StructType", dtype)
        child_names = [struct_type.field(i).name for i in range(struct_type.num_fields)]
        child_idx = _field_index_case_insensitive(child_names, segment, path)
        field = struct_type.field(child_idx)
        nullable = nullable or field.nullable
        canonical_segments.append(field.name)

    return FieldPathResolution(
        canonical_path=format_field_path(canonical_segments),
        segments=tuple(canonical_segments),
        field=field,
        nullable=nullable,
    )


def resolve_projected_field_path(schema: pa.Schema, path: str) -> str:
    """Resolve a field path against a flat projected schema.

    Lance returns nested projections as flat columns named by the canonical field
    path (for example ``MetaData.UserId``). Runtime UDFs still use the user
    declared input path, so projected batches need path-aware name matching.
    """

    if path in schema.names:
        return path

    parsed_segments = parse_field_path(path)
    matches = []
    for field_name in schema.names:
        try:
            projected_segments = parse_field_path(field_name)
        except ValueError:
            projected_segments = [field_name]
        if len(projected_segments) != len(parsed_segments):
            continue
        if all(
            projected_segment.lower() == requested_segment.lower()
            for projected_segment, requested_segment in zip(
                projected_segments, parsed_segments, strict=True
            )
        ):
            matches.append(field_name)

    if not matches:
        raise KeyError(path)
    if len(matches) > 1:
        raise ValueError(f"Ambiguous projected field path {path!r}")
    return matches[0]


def canonical_field_path(schema: pa.Schema, path: str) -> str:
    """Return canonical schema spelling for ``path`` when it resolves."""

    try:
        return resolve_arrow_field_path(schema, path).canonical_path
    except (KeyError, ValueError):
        return path


def canonical_field_paths(
    schema: pa.Schema,
    paths: list[str] | None,
) -> list[str] | None:
    """Return canonical schema spellings for every resolvable path."""

    if paths is None:
        return None
    return [canonical_field_path(schema, path) for path in paths]


def resolve_arrow_field(schema: pa.Schema, path: str) -> pa.Field | None:
    """Resolve a field path, returning ``None`` instead of raising."""

    try:
        return resolve_arrow_field_path(schema, path).field
    except (KeyError, ValueError):
        return None


# ---------- Arrow helpers from attrs ----------

_PRIMITIVE_PA: dict[Any, pa.DataType] = {
    str: pa.string(),
    int: pa.int64(),
    float: pa.float64(),
    bool: pa.bool_(),
    bytes: pa.binary(),
}


def _is_optional(ann: Any) -> bool:
    origin = get_origin(ann)
    args = get_args(ann)
    return (origin in (Union, UnionType)) and (type(None) in args)


def _base_of_optional(ann: Any) -> Any:
    if _is_optional(ann):
        return next(t for t in get_args(ann) if t is not type(None))  # noqa: E721
    return ann


def _infer_pa_from_annotation(ann: Any) -> pa.DataType | None:
    ann = _base_of_optional(ann)
    origin = get_origin(ann)
    args = get_args(ann)

    # handle list[T]
    if origin in (list, list):
        if not args:
            return pa.list_(pa.string())
        inner = _infer_pa_from_annotation(args[0])
        if inner is None:
            return None
        return pa.list_(inner)

    # primitives
    if ann in _PRIMITIVE_PA:
        return _PRIMITIVE_PA[ann]

    return None


def _infer_pa_from_value(v: Any) -> pa.DataType | None:
    if v is None:
        return None
    if isinstance(v, dict | set):
        return None
    if isinstance(v, list):
        return None
    if isinstance(v, str | int | float | bool | bytes):
        try:
            return pa.scalar(v).type
        except Exception:
            return None
    return None


def attrs_to_arrow_schema(model: Any) -> pa.Schema:
    if not attrs.has(type(model)):
        raise TypeError("alter_or_create expects an @attrs instance")

    # Resolve annotations (handles 'from __future__ import annotations')
    type_hints = get_type_hints(type(model), include_extras=True)

    fields_pa: list[pa.Field] = []
    for f in attrs.fields(type(model)):
        name = f.name
        ann = type_hints.get(name, getattr(f, "type", Any))
        default_val = getattr(model, name)

        pa_type = _field_pa_type(f)
        if pa_type is None:
            raise TypeError(
                f"Cannot infer Arrow type for field '{name}'. "
                "Add metadata={'pa_type': ...} or use a supported annotation/value."
            )

        nullable = (default_val is None) or _is_optional(ann)
        fields_pa.append(pa.field(name, pa_type, nullable=nullable))
    return pa.schema(fields_pa)


# ---------- main one-shot API ----------


def alter_or_create_table(
    db: Connection,
    table_name: str,
    model: Any,  # attrs instance
    del_cols: bool = False,  # drop columns not present on the model
    namespace_path: list[str] | None = None,
) -> Table:
    """
    Ensure `table_name` matches the attrs model schema.
    - If table doesn't exist -> create with model schema.
    - Else:
        - Optionally drop extra columns.
        - Add any missing columns based on pyarrow Field.
        - If the table is empty -> overwrite with full model schema.
    Returns the (opened) lancedb.Table.
    """
    if not attrs.has(type(model)):
        raise TypeError("alter_or_create expects an @attrs instance")

    # Convert None to [] for LanceDB compatibility
    namespace_path = namespace_path if namespace_path is not None else []

    # Open or create
    try:
        table = db.open_table(table_name, namespace_path=namespace_path)
        try:
            table_uri = getattr(table, "uri", None) or "<unknown>"
        except Exception:
            table_uri = "<unknown>"
        _LOG.info(
            "opened system table name=%s namespace=%s uri=%s",
            table_name,
            namespace_path,
            table_uri,
        )
    except Exception:
        # lancedb conn raises ValueError,
        # but namespace impl's may raise other exception types
        schema = attrs_to_arrow_schema(model)
        _LOG.info(f"creating table '{table_name}'")
        try:
            return db.create_table(
                table_name, schema=schema, namespace_path=namespace_path
            )
        except Exception as create_err:
            try:
                _LOG.info(
                    f"create_table('{table_name}') failed; "
                    f"attempting open in case the table already exists: "
                    f"{create_err}"
                )
                table = db.open_table(table_name, namespace_path=namespace_path)
            except Exception as e:
                raise create_err from e

    # Compute deltas
    cur_cols = set(table.schema.names)
    # model columns, values, and types
    model_fields = attrs.fields(type(model))
    model_vals = {f.name: getattr(model, f.name) for f in model_fields}
    model_cols = set(model_vals.keys())

    # Drop columns not on model
    if del_cols:
        to_drop = [c for c in cur_cols if c not in model_cols]
        if to_drop:
            _LOG.info(f"dropping cols {to_drop} from {table.schema}")
            table.drop_columns(to_drop)
            table = db.open_table(table_name, namespace_path=namespace_path)  # refresh

    # Add new columns
    # note: this does not support nested struct fields
    cur_cols = set(table.schema.names)
    new_cols = [c for c in model_cols if c not in cur_cols]

    # Refresh table after modifications with namespace if provided
    def _refresh_table() -> Table:
        return db.open_table(table_name, namespace_path=namespace_path)

    _LOG.debug(f"schema diff {table.schema=} {cur_cols=} {model_cols=} {new_cols=}")

    if not new_cols:
        _LOG.debug("No new columns; schema up to date")
        return table

    _LOG.info(f"adding columns to table {table_name} schema: {new_cols}")

    # If table is empty: just overwrite schema (fastest & simplest)
    if table.count_rows() == 0:
        schema = attrs_to_arrow_schema(model)
        _LOG.info("table is empty, overwriting with updated schema")
        db.drop_table(table_name, namespace_path=namespace_path)
        return db.create_table(
            table_name,
            schema=schema,
            mode="overwrite",
            exist_ok=True,
            namespace_path=namespace_path,
        )

    # Otherwise, add columns using field definitions from the model schema
    # This ensures proper type inference, especially for nullable fields
    model_schema = attrs_to_arrow_schema(model)
    new_fields: list[pa.Field] = [
        field for field in model_schema if field.name in new_cols
    ]

    # When adding columns to existing tables, make them nullable so existing rows
    # can have NULL values (even if the model defines them as non-nullable).
    # This allows for graceful schema evolution.
    new_fields_nullable = [
        pa.field(field.name, field.type, nullable=True, metadata=field.metadata)
        for field in new_fields
    ]

    # Pass the fields directly to add_columns for proper type handling
    # Handle both Geneva Table (has ._ltbl) and LanceDB Table (used directly)
    try:
        lance_table = getattr(table, "_ltbl", table)
        lance_table.add_columns(new_fields_nullable)
    except Exception as e:
        raise RuntimeError(
            f"Failed to add columns {new_cols} to table {table_name}. "
            f"This may indicate incompatible field types. Error: {e}"
        ) from e
    return table
