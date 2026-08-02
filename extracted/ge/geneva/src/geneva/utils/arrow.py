# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

import datetime
import enum
import logging
import sys
import typing
from decimal import Decimal
from typing import Optional as OptAlias
from typing import get_args, get_origin

import attrs
import pyarrow as pa
from pyarrow import DataType

_LOG = logging.getLogger(__name__)

# Track if we've already warned about pyarrow fallback (warn once per session)
_PYARROW_FALLBACK_WARNED = False


def batch_add_column(
    batch: pa.RecordBatch,
    index: int,
    field: pa.Field,
    column: pa.Array,
) -> pa.RecordBatch:
    """Add a column to a RecordBatch at the specified index.

    PyArrow compatibility: RecordBatch.add_column was added in pyarrow 15.
    Ray 2.44 Docker image bundles pyarrow 14.0.2, so we maintain backwards
    compatibility by falling back to append_column (pyarrow 7+) or manual
    reconstruction for older versions.

    Parameters
    ----------
        batch
            The RecordBatch to add a column to
        index
            The index at which to insert the column
        field
            The field definition for the new column
        column
            The column data to add

    Returns
    -------
        A new RecordBatch with the column added
    """
    global _PYARROW_FALLBACK_WARNED

    if hasattr(batch, "add_column"):
        return batch.add_column(index, field, column)

    # Fallback for pyarrow < 15
    if not _PYARROW_FALLBACK_WARNED:
        _LOG.warning(
            "Using pyarrow fallback for RecordBatch column operations. "
            "Ray 2.44 bundles pyarrow 14.0.2 which lacks add_column (added in 15)."
        )
        _PYARROW_FALLBACK_WARNED = True

    if hasattr(batch, "append_column") and index == batch.num_columns:
        # append_column only works for adding at the end
        return batch.append_column(field, column)

    # Manual reconstruction for insert at arbitrary index or very old pyarrow
    columns = [batch.column(i) for i in range(batch.num_columns)]
    columns.insert(index, column)
    fields = list(batch.schema)
    fields.insert(index, field)
    schema = pa.schema(fields)
    return pa.RecordBatch.from_arrays(columns, schema=schema)


def datafusion_type_name(data_type: DataType) -> str:
    arrow_type_name = str(data_type)
    # see https://datafusion.apache.org/user-guide/sql/data_types.html
    # TODO: add more types. Note that we only support certain types in lance
    # https://github.com/lancedb/lance/blob/644213b9a63e2b143d62cda79e108df831bc5054/rust/lance-datafusion/src/planner.rs#L426-L441
    df_type_name = {
        "int8": "TINYINT",
        "uint8": "TINYINT UNSIGNED",
        "int16": "SMALLINT",
        "uint16": "SMALLINT UNSIGNED",
        "int32": "INT",
        "uint32": "INT UNSIGNED",
        "int64": "BIGINT",
        "uint64": "BIGINT UNSIGNED",
        "float32": "FLOAT",
        "float64": "DOUBLE",
        "string": "STRING",
        "binary": "BINARY",
        "boolean": "BOOLEAN",
    }.get(arrow_type_name)

    if df_type_name is None:
        raise ValueError(f"unsupported arrow type {arrow_type_name}")

    return df_type_name


def pa_type_from_py(py_type) -> DataType:
    """Map a Python/typing annotation to a PyArrow DataType."""
    origin = typing.get_origin(py_type)
    # Handle Optional[T]
    if origin is typing.Union and type(None) in typing.get_args(py_type):
        inner = [t for t in typing.get_args(py_type) if t is not type(None)][0]
        return pa_type_from_py(inner).with_nullable(True)  # type: ignore[attr-defined]
    # Handle List[T]
    if origin is list:
        subtype = typing.get_args(py_type)[0]
        return pa.list_(pa_type_from_py(subtype))

    if isinstance(py_type, type) and issubclass(py_type, enum.Enum):
        return pa.string()  # Enums are treated as strings

    # Primitives
    if py_type is int:
        return pa.int64()
    if py_type is float:
        return pa.float64()
    if py_type is bool:
        return pa.bool_()
    if py_type is str:
        return pa.string()
    if py_type is datetime.datetime:
        return pa.timestamp("us")
    if py_type is datetime.date:
        return pa.date32()
    # Fallback
    return pa.string()


# Simple registry for Python/typing -> pyarrow types
_SCALAR_MAP = {
    str: pa.string(),
    bytes: pa.binary(),
    bool: pa.bool_(),
    int: pa.int64(),  # choose int64 by default
    float: pa.float64(),
    datetime: pa.timestamp("us"),
    datetime.date: pa.date32(),
    Decimal: pa.decimal128(38, 9),  # adjust precision/scale to your data
}


def _is_attrs_class(tp: DataType) -> bool:
    return hasattr(tp, "__attrs_attrs__")


def _strip_optional(tp: DataType) -> tuple[DataType, bool]:
    """
    If Optional[T] (i.e., Union[T, NoneType]), return (T, True), else (tp, False).
    """
    origin = get_origin(tp)
    if origin is None:
        return tp, False
    if origin is OptAlias or (
        origin is type(typing.Optional[int]) and sys.version_info < (3, 10)
    ):
        # Older Python trick, but modern typing always uses Union.
        ...
    if origin is getattr(__import__("typing"), "Union", None):
        args = tuple(a for a in get_args(tp) if a is not type(None))  # noqa: E721
        if len(args) == 1:
            return args[0], True
    return tp, False


def _from_annotated(tp) -> tuple[DataType, DataType | None]:
    """
    If typing.Annotated[T, "pa-expr"] is used, return (T, pa_type or None).
    We accept a simple string like "timestamp[ms]" or "decimal128(20,4)".
    """
    origin = get_origin(tp)
    if origin is getattr(__import__("typing"), "Annotated", None):
        base, *meta = get_args(tp)
        # Look for the first string metadata payload
        for m in meta:
            if isinstance(m, str):
                # Parse basic pa type strings; you can make this smarter as needed
                s = m.strip().lower()
                if s.startswith("timestamp["):
                    unit = s[len("timestamp[") : -1]
                    return base, pa.timestamp(unit)  # type: ignore[arg-type]
                if s.startswith("decimal128(") and s.endswith(")"):
                    p, s_ = s[len("decimal128(") : -1].split(",")
                    return base, pa.decimal128(int(p), int(s_))
                if s in ("string", "utf8"):
                    return base, pa.string()
                if s == "binary":
                    return base, pa.binary()
                if s == "bool":
                    return base, pa.bool_()
                if s == "int64":
                    return base, pa.int64()
                if s == "float64":
                    return base, pa.float64()
        return base, None
    return tp, None


def _infer_pa_type(py_type, name: str) -> pa.DataType:
    """
    Infer pyarrow type from a (possibly typing) type, recursing into attrs classes,
    lists, dicts, and optionals.
    """
    # Handle Annotated override
    py_type, annotated_pa = _from_annotated(py_type)
    if annotated_pa is not None:
        return annotated_pa

    # Handle Optional[T]
    core, _ = _strip_optional(py_type)

    # Nested attrs class -> struct
    if _is_attrs_class(core):
        fields = []
        for a in attrs.fields(core):  # type: ignore[arg-type]
            pa_type = _field_pa_type(a)
            fields.append(pa.field(a.name, pa_type, nullable=_is_nullable(a)))
        return pa.struct(fields)

    origin = get_origin(core)
    args = get_args(core)

    # list[T] -> list_(T)
    if origin in (list, list):
        item_type = _infer_pa_type(args[0], name) if args else pa.string()
        return pa.list_(item_type)  # elements themselves default nullable

    # dict[K, V] -> map_(K, V)
    if origin in (dict, dict):
        key_type = _infer_pa_type(args[0], name) if args else pa.string()
        val_type = _infer_pa_type(args[1], name) if args else pa.string()
        return pa.map_(key_type, val_type)

    # Scalars
    if core in _SCALAR_MAP:
        return _SCALAR_MAP[core]

    raise TypeError(
        f"Cannot infer Arrow type for field '{name}'. "
        "Add metadata={'pa_type': ...} or use a supported annotation/value."
    )


def _is_nullable(a: attrs.Attribute) -> bool:
    """
    Decide nullability:
    - If type is Optional[...] -> nullable True
    - Else allow override via metadata: {"nullable": True/False}
    - Default False for most scalars, True for containers (tunable)
    """
    # Metadata override wins
    meta = a.metadata or {}
    if "nullable" in meta:
        return bool(meta["nullable"])

    # From annotation
    _, is_opt = _strip_optional(a.type) if a.type is not None else (a.type, False)  # type: ignore[arg-type]
    if is_opt:
        return True

    # Heuristic: lists/dicts/structs often okay to be nullable
    t = a.type
    if t is not None:
        base, _ = _from_annotated(t)
        base, _ = _strip_optional(base)
        if _is_attrs_class(base) or get_origin(base) in (
            list,
            list,
            dict,
            dict,
        ):
            return True

    return False


def _field_pa_type(a: attrs.Attribute) -> pa.DataType:
    """
    Per‑field mapping, honoring metadata overrides:
      - metadata={"pa_type": pa.xxx()}
      - or metadata={"pa_type": "timestamp[ms]"} (string shorthand)
    """
    meta = a.metadata or {}
    override = meta.get("pa_type")

    if isinstance(override, pa.DataType):
        return override
    if isinstance(override, str):
        # simple parser for a couple of strings
        s = override.strip().lower()
        if s.startswith("timestamp["):
            unit = s[len("timestamp[") : -1]
            return pa.timestamp(unit)  # type: ignore[arg-type]
        if s.startswith("decimal128(") and s.endswith(")"):
            p, sc = s[len("decimal128(") : -1].split(",")
            return pa.decimal128(int(p), int(sc))
        if s in ("string", "utf8"):
            return pa.string()
        if s == "binary":
            return pa.binary()
        if s == "bool":
            return pa.bool_()
        if s == "int64":
            return pa.int64()
        if s == "float64":
            return pa.float64()

    # Fall back to annotation-based inference
    return _infer_pa_type(a.type, a.name)
