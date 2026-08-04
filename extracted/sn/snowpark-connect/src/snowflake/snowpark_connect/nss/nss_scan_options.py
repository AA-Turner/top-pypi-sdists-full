#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

"""``OPTIONS`` payload + reader-option filtering for the official ``STAGE_FILE_READER``
TVF path.

The ``OPTIONS`` blob carries three client-produced keys:

* ``DATA_SCHEMA`` — a JSON *array*, one entry per top-level column, each
  ``{COLUMN_NAME, SPARK_DATA_TYPE, SF_DATA_TYPE, NULLABLE, ORDER_ID}`` (backend contract
  SNOW-3780862 / PR #481112). The backend parses ``SF_DATA_TYPE`` via
  ``DataType.sqlAsDataType()`` to materialize the GS column; ``SPARK_DATA_TYPE`` is opaque
  to GS and passed through to the sandbox Spark reader. Nested types are rendered as
  Snowflake structured-type strings (``OBJECT(...)`` / ``ARRAY(...)`` / ``MAP(...)``) with
  unquoted field names and no ``NOT NULL`` (the grammar has no per-field null marker;
  top-level nullability is the ``NULLABLE`` field). ``ORDER_ID`` is 0-based and contiguous.
* ``READER_OPTIONS`` — the Spark ``DataFrameReader`` options, filtered to each
  format's read-only allow-list.
* ``SPARK_CONF`` — the subset of ``spark.sql.*`` session confs that affect decoding
  (timezone, timestamp type, ANSI, …), consumed by the sandbox reader.

``DATA_SCHEMA`` is the single source of truth for column resolution (it replaced
``SNOWFLAKE_TABLE_SCHEMA``); ``READ_DATA_SCHEMA`` is derived by the backend. The client
does not emit either.
"""

import json
from typing import Callable, NamedTuple

from pyspark.sql.types import (
    ArrayType as PyArrayType,
    DataType as PyDataType,
    MapType as PyMapType,
    StructField as PyStructField,
    StructType as PyStructType,
    _parse_datatype_json_string,
)

from snowflake.snowpark.types import ArrayType, DataType, MapType, StructType
from snowflake.snowpark_connect.type_mapping import (
    map_pyspark_types_to_snowpark_types,
    map_type_to_snowflake_type,
)


class NssColumn(NamedTuple):
    """One DATA_SCHEMA column as SCOS knows it, before serialization.

    ``spark_type`` is Spark's ``DataType.json()`` string — carried **verbatim** from
    ``INFER_STAGE_FILE_SCHEMA`` for a schema-less read (SCOS does not re-derive it), or
    ``field.dataType.json()`` from the caller's explicit schema. The backend reconstructs
    the sandbox read schema via ``DataType.fromJson``, so this must be the JSON form.
    """

    name: str
    spark_type: str
    nullable: bool


# Spark JSON *read* options (lowercased) the real JsonFileFormat accepts on read.
# encoding/charset excluded: they route the reader through sun.nio.cs, which the
# sandbox JVM cannot access without --add-opens.
_SPARK_JSON_READ_OPTIONS = {
    "multiline",
    "mode",
    "linesep",
    "columnnameofcorruptrecord",
    "dateformat",
    "timestampformat",
    "timestampntzformat",
    "allowcomments",
    "allowunquotedfieldnames",
    "allowsinglequotes",
    "allownumericleadingzeros",
    "allowbackslashescapinganycharacter",
    "allowunquotedcontrolchars",
    "allownonnumericnumbers",
    "primitivesasstring",
    "prefersdecimal",
    "dropfieldifallnull",
    "samplingratio",
    "locale",
    "ignorenullfields",
}

# Spark CSV *read* options (lowercased) the real CSVFileFormat accepts on read.
# Excludes write-only keys, SCOS-internal keys (path), inferSchema, encoding/charset.
_SPARK_CSV_READ_OPTIONS = {
    "sep",
    "delimiter",
    "quote",
    "escape",
    "comment",
    "header",
    "ignoreleadingwhitespace",
    "ignoretrailingwhitespace",
    "nullvalue",
    "nanvalue",
    "positiveinf",
    "negativeinf",
    "dateformat",
    "timestampformat",
    "timestampntzformat",
    "maxcolumns",
    "maxcharspercolumn",
    "mode",
    "columnnameofcorruptrecord",
    "multiline",
    "chartoescapequoteescaping",
    "samplingratio",
    "emptyvalue",
    "locale",
    "linesep",
    "unescapedquotehandling",
    "enforceschema",
}

_ALLOWED_READ_OPTIONS = {
    "json": _SPARK_JSON_READ_OPTIONS,
    "csv": _SPARK_CSV_READ_OPTIONS,
}

# spark.sql.* session confs that change how the sandbox Spark reader decodes files.
# Only these are forwarded as SPARK_CONF (keeps the blob small + deterministic).
# ``arrow.typeMappingVersion`` decides integer column widths (V1 -> NUMBER(38,0));
# forwarded when the session sets it so an explicit client choice reaches the sandbox
# (not pinned to a value — an unset conf simply drops out via build_spark_conf).
_RELEVANT_SPARK_CONF_KEYS = (
    "spark.sql.session.timeZone",
    "spark.sql.timestampType",
    "spark.sql.ansi.enabled",
    "spark.sql.legacy.timeParserPolicy",
    "spark.sql.parquet.inferTimestampNTZ.enabled",
    "spark.sql.snowflake.arrow.typeMappingVersion",
)


def sql_quote_literal(value: str) -> str:
    """Escape single quotes in ``value`` for safe interpolation inside a single-quoted
    SQL string literal (mirrors ``map_read._list_stage_files``' ``\\'`` escaping).

    Only the quote body is escaped — the caller supplies the surrounding quotes.
    """
    return value.replace("'", "\\'")


def quote_options_literal(payload: str) -> str:
    """Wrap an OPTIONS JSON ``payload`` in a Snowflake string literal that is safe against
    SQL-break / injection from user-controlled content.

    Uses a dollar-quoted literal (``$$...$$``) in the common case — its content is taken
    verbatim, no escaping. Snowflake supports **only** the bare ``$$`` delimiter (not
    Postgres-style ``$tag$``), so if the payload itself contains ``$$`` — a user column
    name (explicit/inferred) or a reader-option value such as ``.option("nullValue", "$$")``
    can — the bare ``$$`` would be closed early. In that case fall back to a single-quoted
    literal with backslashes and single quotes escaped (where ``$$`` is harmless). The TVF
    requires ``OPTIONS`` to be a constant literal, so a bind parameter is not an option.
    """
    if "$$" not in payload:
        return f"$${payload}$$"
    return "'" + payload.replace("\\", "\\\\").replace("'", "''") + "'"


def filter_reader_options(fmt: str, reader_options: dict | None) -> dict:
    """Filter a SCOS options bag to the ``fmt`` (``json``/``csv``) Spark read allow-list.

    For CSV, single-char options stored in their COPY/SQL-escaped spelling
    (``escape="\\\\"`` = the SQL literal for a lone backslash) are collapsed back to one
    character — Spark's ``CSVOptions.getChar`` rejects any >1-char char option.
    """
    allow = _ALLOWED_READ_OPTIONS.get(fmt.lower())
    ro = {
        k: v
        for k, v in (reader_options or {}).items()
        if allow is None or k.lower() in allow
    }
    # SCOS defaults date/timestamp formats to the Snowflake keyword ``AUTO`` for the
    # COPY-INTO read path (see reader_config). ``AUTO`` is not a Spark pattern: the
    # sandbox reader hands it to Spark's DateTimeFormatter, which reads the ``u`` in
    # "auto" as the (banned since Spark 3.0) week-based-year letter and throws.
    # Drop these so the sandbox reader falls back to Spark's own default format.
    for k in list(ro.keys()):
        if (
            k.lower() in ("dateformat", "timestampformat", "timestampntzformat")
            and str(ro[k]).strip().lower() == "auto"
        ):
            del ro[k]
    if fmt.lower() == "csv":
        for k, v in list(ro.items()):
            if (
                k.lower() in ("escape", "quote", "sep", "delimiter", "comment")
                and v == "\\\\"
            ):
                ro[k] = "\\"
    return ro


def build_spark_conf() -> dict:
    """Collect the decoding-relevant ``spark.sql.*`` session confs for ``SPARK_CONF``.

    Read lazily from the current session config so an unset conf simply drops out
    (empty string). Returns ``{}`` when none are set.
    """
    from snowflake.snowpark_connect.config import get_string_session_config_param

    conf = {}
    for key in _RELEVANT_SPARK_CONF_KEYS:
        val = get_string_session_config_param(key)
        if val != "" and val != "None":
            conf[key] = val
    return conf


def _unquote_name(name: str) -> str:
    """Strip one surrounding double-quote layer from a SCOS field name (``"a"`` -> ``a``).

    SCOS field names arrive double-quoted; the sandbox reader matches the raw JSON/column
    key, so the quotes must be removed or every field reads back NULL.
    """
    if isinstance(name, str) and len(name) >= 2 and name[0] == '"' and name[-1] == '"':
        return name[1:-1]
    return name


def _sf_data_type(dt: DataType) -> str:
    """Render a Snowpark type as the ``SF_DATA_TYPE`` string the backend parses via
    ``DataType.sqlAsDataType()`` (SNOW-3780862 / PR #481112).

    Structured types use Snowflake ``OBJECT`` / ``ARRAY`` / ``MAP`` with **unquoted**
    field names and **no** ``NOT NULL`` — nested nullability is not expressed in
    ``SF_DATA_TYPE`` (the backend's structured-type grammar has no per-field null marker;
    top-level nullability travels in the record's ``NULLABLE`` field). This matches the
    backend UT examples exactly, e.g. ``OBJECT(id INT, addr OBJECT(city VARCHAR, zip INT))``,
    ``ARRAY(OBJECT(event_id INT, event_type VARCHAR))``, ``MAP(VARCHAR, INT)``, ``ARRAY(INT)``.
    Scalars delegate to the shared Snowflake type mapper (INT/BIGINT/NUMBER are all
    ``NUMBER(38,0)`` in Snowflake, so the exact integer keyword is immaterial).
    """
    if isinstance(dt, ArrayType):
        if dt.element_type is None:
            return "ARRAY"
        return f"ARRAY({_sf_data_type(dt.element_type)})"
    if isinstance(dt, MapType):
        if dt.key_type is None or dt.value_type is None:
            return "OBJECT"
        return f"MAP({_sf_data_type(dt.key_type)}, {_sf_data_type(dt.value_type)})"
    if isinstance(dt, StructType) and dt.fields:
        fields = ", ".join(
            f"{_unquote_name(f.name)} {_sf_data_type(f.datatype)}" for f in dt.fields
        )
        return f"OBJECT({fields})"
    return map_type_to_snowflake_type(dt, structured=True)


def _sf_data_type_from_spark_json(spark_type_json: str) -> str:
    """Derive ``SF_DATA_TYPE`` from a Spark ``DataType.json()`` string.

    The backend does not derive Snowflake types from Spark types — SCOS must supply
    ``SF_DATA_TYPE`` for GS column materialization. This is the *only* transform applied to
    the column's type; ``SPARK_DATA_TYPE`` itself is carried through untouched.
    """
    # Quote nested struct field names before the snowpark hop so their original case is
    # preserved (an unquoted name would be upper-cased); ``_sf_data_type`` unquotes them.
    py_dt = _quote_py(_parse_datatype_json_string(spark_type_json))
    return _sf_data_type(map_pyspark_types_to_snowpark_types(py_dt))


def _map_py_field_names(dt: PyDataType, fn: Callable[[str], str]) -> PyDataType:
    """Recursively rebuild a pyspark type, applying ``fn`` to each struct field name."""
    if isinstance(dt, PyStructType):
        return PyStructType(
            [
                PyStructField(
                    fn(f.name), _map_py_field_names(f.dataType, fn), f.nullable
                )
                for f in dt.fields
            ]
        )
    if isinstance(dt, PyArrayType):
        return PyArrayType(_map_py_field_names(dt.elementType, fn), dt.containsNull)
    if isinstance(dt, PyMapType):
        return PyMapType(
            _map_py_field_names(dt.keyType, fn),
            _map_py_field_names(dt.valueType, fn),
            dt.valueContainsNull,
        )
    return dt


def _quote_py(dt: PyDataType) -> PyDataType:
    """Recursively rebuild a pyspark type with double-quoted struct field names (so a
    downstream Snowpark conversion preserves their case)."""

    def q(name: str) -> str:
        name = _unquote_name(name)
        return '"' + name.replace('"', '""') + '"'

    return _map_py_field_names(dt, q)


def columns_from_spark_schema(schema: PyStructType) -> list[NssColumn]:
    """Build :class:`NssColumn` list from the caller's explicit **pyspark** schema.

    ``spark_type`` is each field's ``DataType.json()`` used verbatim — this is the client's
    schema exactly as sent (parsed by ``map_read.parse_data_source_schema_to_spark``), with
    no Snowpark round-trip, matching the JSON form ``INFER_STAGE_FILE_SCHEMA`` emits.
    """
    return [NssColumn(f.name, f.dataType.json(), f.nullable) for f in schema.fields]


def build_data_schema(columns: list[NssColumn]) -> list[dict]:
    """Build ``DATA_SCHEMA`` — one entry per top-level column — per the backend contract
    (SNOW-3780862 / PR #481112).

    Each record is ``{COLUMN_NAME, SPARK_DATA_TYPE, SF_DATA_TYPE, NULLABLE, ORDER_ID}``:
    ``SPARK_DATA_TYPE`` is the column's Spark ``DataType.json()`` **parsed** (a bare type
    name for scalars, a nested object for containers) — opaque to GS; the sandbox
    ColumnDescriptor (``ScanReadOptions``) rebuilds the read schema via ``DataType.fromJson``,
    re-quoting scalars and re-serializing containers, so the raw json() *string* would
    double-encode. ``SF_DATA_TYPE`` is the Snowflake structured-type string SCOS derives for GS column
    materialization; ``NULLABLE`` is a JSON boolean; ``ORDER_ID`` is **0-based** and
    contiguous (``0..N-1``; the backend rejects out-of-range, duplicate, or non-integral
    values). The backend adopted 0-based ORDER_ID in SNOW-3859348
    (``ENABLE_FIX_3859348_DATA_SCHEMA_ZERO_BASED_ORDER_ID``, default on): "clients send
    0-based ORDER_ID; this is the correct behaviour."
    """
    return [
        {
            "COLUMN_NAME": _unquote_name(c.name),
            # Emit the *parsed* DataType.json() value, not the raw json() string. The
            # sandbox ColumnDescriptor (ScanReadOptions, PR #23) expects a scalar as a
            # bare type name ("long") — which it re-quotes before DataType.fromJson —
            # and a complex type as a nested JSON object (Jackson Map/List). Sending the
            # raw json() string double-encodes a scalar ("long" -> ""long"" -> parses as
            # the empty string) and stringifies a complex type, both of which the sandbox
            # rejects. json.loads gives a bare str for scalars and a dict for containers.
            "SPARK_DATA_TYPE": json.loads(c.spark_type),
            "SF_DATA_TYPE": _sf_data_type_from_spark_json(c.spark_type),
            "NULLABLE": bool(c.nullable),
            # 0-based column position (SNOW-3859348): the STAGE_FILE_READER backend now
            # interprets DATA_SCHEMA ORDER_ID as 0-based (first column = 0). Emitting the
            # legacy 1-based value makes the last column's ORDER_ID out-of-range and the
            # TVF rejects it ("invalid value 'OPTIONS.DATA_SCHEMA.ORDER_ID'").
            "ORDER_ID": i,
        }
        for i, c in enumerate(columns)
    ]


def _stringify_reader_option(value: bool | str | int | float) -> str:
    """Stringify a reader-option value for the JSON OPTIONS payload.

    Python ``bool`` values render as lowercase ``"true"``/``"false"`` — Spark's option
    parsing (``CaseInsensitiveMap`` + ``.toBoolean``) expects the lowercase spelling, so
    ``str(True)`` (``"True"``) would not be recognized. All other values use ``str()``.
    """
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


def build_stage_file_reader_options(
    columns: list[NssColumn],
    reader_options: dict | None = None,
    spark_conf: dict | None = None,
) -> str:
    """Build the ``OPTIONS`` JSON for ``STAGE_FILE_READER``.

    Emits ``DATA_SCHEMA`` (per-column array), ``READER_OPTIONS`` (already format-filtered by
    the caller), and ``SPARK_CONF``. The backend derives ``READ_DATA_SCHEMA``, so it is not
    emitted here (``DATA_SCHEMA`` is the single source of truth for column resolution).
    """
    reader = {k: _stringify_reader_option(v) for k, v in (reader_options or {}).items()}
    return json.dumps(
        {
            "DATA_SCHEMA": build_data_schema(columns),
            "READER_OPTIONS": reader,
            "SPARK_CONF": spark_conf if spark_conf is not None else build_spark_conf(),
        }
    )
