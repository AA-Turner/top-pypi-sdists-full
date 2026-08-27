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
    StringType as PyStringType,
    StructField as PyStructField,
    StructType as PyStructType,
    _parse_datatype_json_string,
)

from snowflake.snowpark import DataFrame
from snowflake.snowpark._internal.analyzer.analyzer_utils import unquote_if_quoted
from snowflake.snowpark.types import (
    ArrayType,
    DataType,
    MapType,
    StructField,
    StructType,
    TimestampType,
)
from snowflake.snowpark_connect.type_mapping import (
    TIMESTAMP_TZ_TO_SF_TYPE,
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
    "infertimestamp",
    "enabledatetimeparsingfallback",
}

# Spark CSV *read* options (lowercased) the real CSVFileFormat accepts on read.
# Excludes write-only keys, SCOS-internal keys (path), inferSchema.
_SPARK_CSV_READ_OPTIONS = {
    "encoding",
    "charset",
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
    "enabledatetimeparsingfallback",
    "preferdate",
}

_ALLOWED_READ_OPTIONS = {
    "json": _SPARK_JSON_READ_OPTIONS,
    "csv": _SPARK_CSV_READ_OPTIONS,
}

# spark.sql.* session confs that change how the sandbox Spark reader decodes files.
# Only these are forwarded as SPARK_CONF (keeps the blob small + deterministic).
#
# A key here only forwards if it is also in SESSION_CONFIG_KEY_WHITELIST; adding one
# without whitelisting it is a silent no-op (SNOW-3898459, SNOW-3919681). Enforced by
# ``test_every_forwarded_key_is_reachable``.
#
# Keys with a ``default_session_config`` entry forward that default even when the client
# never calls ``conf.set``. ``legacy.timeParserPolicy`` and ``arrow.typeMappingVersion``
# (integer column widths, V1 -> NUMBER(38,0)) have none, so they drop out when unset.
_RELEVANT_SPARK_CONF_KEYS = (
    "spark.sql.session.timeZone",
    "spark.sql.timestampType",
    "spark.sql.ansi.enabled",
    "spark.sql.caseSensitive",
    "spark.sql.legacy.timeParserPolicy",
    "spark.sql.parquet.inferTimestampNTZ.enabled",
    "spark.sql.snowflake.arrow.typeMappingVersion",
    # SNOW-3898459: carry Spark's own defaults so the sandbox is never left to guess.
    "spark.sql.datetime.java8API.enabled",
    "spark.sql.json.enablePartialResults",
    # Also a READER_OPTION; forwarded for completeness (backend gap: SNOW-3899671).
    "spark.sql.columnNameOfCorruptRecord",
    # SNOW-3957419: governs UnivocityParser.parsedSchema in the sandbox. With pruning on
    # (Spark's default) parsedSchema == requiredSchema, so the token-count check never
    # fires and a short row is never malformed -- DROPMALFORMED then keeps rows it should
    # drop whenever the query projects a subset of columns.
    "spark.sql.csv.parser.columnPruning.enabled",
    # SNOW-3968584: Spark's legacy date/time parsing-fallback confs, one per format
    # (SQLConf.scala LEGACY_JSON/CSV_ENABLE_DATE_TIME_PARSING_FALLBACK). Both must also be in
    # SESSION_CONFIG_KEY_WHITELIST -- an unwhitelisted key makes SessionConfig.set a silent
    # no-op, so there would be nothing here to forward.
    "spark.sql.legacy.json.enableDateTimeParsingFallback",
    "spark.sql.legacy.csv.enableDateTimeParsingFallback",
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


# SCOS CSV defaults (reader_config.CSV_READ_DEFAULT_CONFIG) whose value contradicts
# Spark's own CSV default. They exist for the COPY path; forwarding them to the sandbox
# Spark reader silently changes results, so they are dropped unless the caller set them
# (SNOW-3861940). The other SCOS defaults that reach READER_OPTIONS (header, quote,
# escape, multiLine, ignoreLeading/TrailingWhiteSpace, enforceSchema) all match Spark's
# defaults and are kept -- ``header`` deliberately so: INFER_STAGE_FILE_SCHEMA defaults
# it to *true* while STAGE_FILE_READER defaults it to *false*, so an absent ``header``
# makes inference and read disagree about the first line.
_CSV_DEFAULTS_CONTRADICTING_SPARK = (
    # Spark auto-detects \r\n / \n / \r; pinning "\n" breaks CRLF files.
    "linesep",
    # Spark's default is *no* comment character, so SCOS's "#" silently drops any data
    # line starting with "#".
    "comment",
)


def _reconcile_leaked_csv_defaults(
    ro: dict, user_option_keys: frozenset[str] | None
) -> None:
    """Reconcile SCOS's own CSV defaults so they do not override the sandbox Spark reader.

    ``sep`` and ``delimiter`` are aliases and Spark resolves ``sep`` first
    (``CSVOptions``: ``getOrElse("sep", getOrElse("delimiter", ","))``), so SCOS's default
    ``sep`` shadows a user-supplied ``delimiter`` and the read silently splits on ``,``.
    The V1/COPY path resolves the same alias in ``reader_config.csv_convert_to_snowpark_args``.
    """
    if user_option_keys is None:
        return
    if "delimiter" in user_option_keys and "sep" not in user_option_keys:
        ro.pop("sep", None)
    for key in _CSV_DEFAULTS_CONTRADICTING_SPARK:
        if key not in user_option_keys:
            ro.pop(key, None)


def filter_reader_options(
    fmt: str,
    reader_options: dict | None,
    user_option_keys: frozenset[str] | None = None,
) -> dict:
    """Filter a SCOS options bag to the ``fmt`` (``json``/``csv``) Spark read allow-list.

    For CSV, single-char options stored in their COPY/SQL-escaped spelling
    (``escape="\\\\"`` = the SQL literal for a lone backslash) are collapsed back to one
    character — Spark's ``CSVOptions.getChar`` rejects any >1-char char option.

    ``user_option_keys`` (lowercased, from ``ReaderWriterConfig``) tells SCOS's own CSV
    defaults apart from the caller's choices so the leaked ones can be dropped — see
    :func:`_reconcile_leaked_csv_defaults`.
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
        _reconcile_leaked_csv_defaults(ro, user_option_keys)
        # Only the ``getChar`` options are collapsed. ``sep``/``delimiter`` go through
        # Spark's ``CSVExprUtils.toDelimiterStr``, which *requires* the two-character
        # spelling for a literal backslash and rejects a lone one ("Single backslash is
        # prohibited") — so the client's value must reach the sandbox untouched
        # (SNOW-3861940).
        for k, v in list(ro.items()):
            if k.lower() in ("escape", "quote", "comment") and v == "\\\\":
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


def _nss_column_name(name: str, index: int) -> str:
    """Unquote an NSS column name, falling back to ``_c{index}`` when empty.

    Snowpark's ``unquote_if_quoted`` leaves ``""`` unchanged (``ALREADY_QUOTED`` is
    ``^(".+")$``), so treat that as empty before the ``_c{i}`` default.
    """
    unquoted = unquote_if_quoted(name)
    if unquoted == '""':
        unquoted = ""
    return unquoted or f"_c{index}"


def cache_if_corrupt_record_present(
    df: DataFrame,
    corrupt_record_column_name: str | None,
    columns: list["NssColumn"],
) -> DataFrame:
    """Materialize the NSS read when its schema carries the corrupt-record column
    *alongside* at least one data column.

    A later projection down to only that column (``.filter(c.isNotNull).select(c)``)
    otherwise trips the sandbox's raw-file corrupt-record restriction
    (``queryFromRawFilesIncludeCorruptRecordColumnError``); reading the cached result
    instead of the raw file is Spark's own prescribed workaround. Falls back to the
    ``_corrupt_record`` default so the guard also covers reads that never resolved an
    explicit name (SNOW-3899671).

    When the inferred schema is the corrupt-record column *only* — the file is
    unparseable under the requested options, so inference found no data field — caching
    is skipped (SNOW-3913953). There is no later projection to defend against, and
    ``cache_result()`` would have to execute the very ``STAGE_FILE_READER`` query the
    sandbox's guard rejects, turning the mitigation into the trigger. Skipping it also
    matches upstream Spark, which serves ``df.schema`` from inference without scanning
    and only raises ``AnalysisException`` when an action actually references the column
    (verified against Spark 3.5.3: ``.schema`` succeeds, ``collect()`` raises).
    """
    effective = corrupt_record_column_name or "_corrupt_record"
    names = [unquote_if_quoted(c.name) for c in columns]
    if effective in names and len(names) > 1:
        return df.cache_result()
    return df


def _sf_data_type(dt: DataType) -> str:
    """Render a Snowpark type as the ``SF_DATA_TYPE`` string the backend parses via
    ``DataType.sqlAsDataType()`` (SNOW-3780862 / PR #481112).

    Structured types use Snowflake ``OBJECT`` / ``ARRAY`` / ``MAP`` with **unquoted**
    field names and **no** ``NOT NULL`` — nested nullability is not expressed in
    ``SF_DATA_TYPE`` (the backend's structured-type grammar has no per-field null marker;
    top-level nullability travels in the record's ``NULLABLE`` field). This matches the
    backend UT examples exactly, e.g. ``OBJECT(id INT, addr OBJECT(city VARCHAR, zip INT))``,
    ``ARRAY(OBJECT(event_id INT, event_type VARCHAR))``, ``MAP(VARCHAR, INT)``, ``ARRAY(INT)``.
    Timestamps are rendered variant-faithfully via ``TIMESTAMP_TZ_TO_SF_TYPE`` (DEFAULT
    stays bare ``TIMESTAMP`` so the session's TIMESTAMP_TYPE_MAPPING applies —
    SNOW-3891973); other scalars delegate to the shared Snowflake type mapper
    (INT/BIGINT/NUMBER are all ``NUMBER(38,0)`` in Snowflake, so the exact integer
    keyword is immaterial).
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
            f"{unquote_if_quoted(f.name)} {_sf_data_type(f.datatype)}"
            for f in dt.fields
        )
        return f"OBJECT({fields})"
    if isinstance(dt, TimestampType):
        # Bare ``TIMESTAMP`` when no variant was expressed — session default wins.
        return TIMESTAMP_TZ_TO_SF_TYPE.get(dt.tz, "TIMESTAMP")
    # Integer widths are deliberately not narrowed: the vectorized-Arrow UDTF emits SB16
    # for every integral column (SNOW-3814066), so a sub-19 precision (e.g. NUMBER(10,0))
    # fails the read with "produced fixed_size_binary[16] but expected fixed_size_binary[8]".
    # Clients see the correct Spark type via snowpark_types_from_columns regardless.
    return map_type_to_snowflake_type(dt, structured=True)


def _sf_data_type_from_spark_json(spark_type_json: str) -> str:
    """Derive ``SF_DATA_TYPE`` from a Spark ``DataType.json()`` string.

    The backend does not derive Snowflake types from Spark types — SCOS must supply
    ``SF_DATA_TYPE`` for GS column materialization. This is the *only* transform applied to
    the column's type; ``SPARK_DATA_TYPE`` itself is carried through untouched.
    """
    return _sf_data_type(_snowpark_type_from_spark_json(spark_type_json))


def _snowpark_type_from_spark_json(spark_type_json: str) -> DataType:
    """Convert a Spark ``DataType.json()`` string to its Snowpark equivalent."""
    # Quote nested struct field names before the snowpark hop so their original case is
    # preserved (an unquoted name would be upper-cased); ``_sf_data_type`` unquotes them.
    py_dt = _quote_py(_parse_datatype_json_string(spark_type_json))
    return map_pyspark_types_to_snowpark_types(py_dt)


def _unquote_nested_field_names(dt: DataType) -> DataType:
    """Rebuild a Snowpark type with its nested struct field names unquoted.

    ``_snowpark_type_from_spark_json`` double-quotes nested struct field names so the
    pyspark -> Snowpark hop preserves their case, and ``_sf_data_type`` unquotes them
    again when it renders ``DATA_SCHEMA``. A *reported* type must carry the raw name
    instead: a nested field literally named ``"field1"`` matches no key in the column the
    reader returns, so every leaf under it reads back NULL.

    Case preservation of the unquoted name (e.g. ``MixedCase`` not ``MIXEDCASE``) requires
    both ``_is_column=False`` on each nested ``StructField`` *and* SCOS structured-type
    semantics (``context._use_structured_type_semantics``, set in ``server.py``). Under
    that contract ``StructField.name`` returns the raw ``_name``; without it Snowpark
    would uppercase via ``column_identifier``. Keep the ``structured`` flags so the result
    has the shape Snowpark's own ``describe`` produces for a structured column.
    """
    if isinstance(dt, StructType):
        return StructType(
            [
                StructField(
                    unquote_if_quoted(f.name),
                    _unquote_nested_field_names(f.datatype),
                    f.nullable,
                    _is_column=False,
                )
                for f in dt.fields
            ],
            structured=dt.structured,
        )
    if isinstance(dt, ArrayType):
        return ArrayType(
            _unquote_nested_field_names(dt.element_type),
            structured=dt.structured,
            contains_null=dt.contains_null,
        )
    if isinstance(dt, MapType):
        if dt.key_type is None or dt.value_type is None:
            return dt
        return MapType(
            _unquote_nested_field_names(dt.key_type),
            _unquote_nested_field_names(dt.value_type),
            structured=dt.structured,
            value_contains_null=dt.value_contains_null,
        )
    return dt


def snowpark_types_from_columns(columns: list[NssColumn]) -> list[DataType]:
    """Snowpark column types for ``DataFrameContainer.create_with_column_mapping``.

    Every column's type is derived from its ``spark_type`` — the Spark type
    INFER_STAGE_FILE_SCHEMA returned or the caller declared — so the schema SCOS reports
    is the one it was given, for nested (struct / array / map) columns as well as
    top-level scalars. Passing ``None`` as ``create_with_column_mapping``'s
    ``snowpark_column_types`` instead makes the container re-derive the schema from the
    reader's *Snowflake* column metadata, which cannot express the difference between
    Integer and Long (both ``NUMBER(38,0)``) or between TIMESTAMP_NTZ and TIMESTAMP
    (SNOW-3891973), and widens nested element types the same way.
    """
    return [
        _unquote_nested_field_names(_snowpark_type_from_spark_json(c.spark_type))
        for c in columns
    ]


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
        name = unquote_if_quoted(name)
        return '"' + name.replace('"', '""') + '"'

    return _map_py_field_names(dt, q)


def py_schema_as_nullable(schema: PyStructType) -> PyStructType:
    """Recursively relax a pyspark schema to all-nullable — Spark's ``StructType.asNullable``.

    SPARK-35912: file sources can always yield NULL, so Spark relaxes a non-nullable user
    schema on read. SCOS applies this to the Snowpark schema in ``map_read_csv`` /
    ``map_read_json``, but the NSS branches re-derive their columns from the raw proto
    schema, which still carries ``nullable=false``. Without this the emitted
    ``DATA_SCHEMA`` says ``NULLABLE: false``, GS materializes a genuinely NOT-NULL column
    and a legitimate NULL row fails with ``100072`` (SNOW-3891605).
    """

    def relax(dt: PyDataType) -> PyDataType:
        if isinstance(dt, PyStructType):
            return PyStructType(
                [PyStructField(f.name, relax(f.dataType), True) for f in dt.fields]
            )
        if isinstance(dt, PyArrayType):
            return PyArrayType(relax(dt.elementType), True)
        if isinstance(dt, PyMapType):
            return PyMapType(relax(dt.keyType), relax(dt.valueType), True)
        return dt

    return relax(schema)


def columns_from_spark_schema(schema: PyStructType) -> list[NssColumn]:
    """Build :class:`NssColumn` list from the caller's explicit **pyspark** schema.

    ``spark_type`` is each field's ``DataType.json()`` used verbatim — this is the client's
    schema exactly as sent (parsed by ``map_read.parse_data_source_schema_to_spark``), with
    no Snowpark round-trip, matching the JSON form ``INFER_STAGE_FILE_SCHEMA`` emits.
    """
    return [NssColumn(f.name, f.dataType.json(), f.nullable) for f in schema.fields]


# Spark ``DataType.json()`` for ``StringType`` — the JSON form ``NssColumn.spark_type`` holds.
_STRING_SPARK_TYPE_JSON = PyStringType().json()


def as_all_string_columns(columns: list[NssColumn]) -> list[NssColumn]:
    """Flatten inferred column types to ``StringType``, keeping names and order.

    Spark only widens types when ``inferSchema=true``: ``CSVInferSchema.infer`` guards the
    type aggregation on ``options.inferSchemaFlag`` and its else-branch is
    ``header.map(fieldName => StructField(fieldName, StringType, nullable = true))``
    (Spark 3.5.3 ``CSVInferSchema.scala``). ``inferSchema`` defaults to false, so a plain
    ``spark.read.option("header", "true").csv(...)`` yields all-string columns.
    ``INFER_STAGE_FILE_SCHEMA`` always types the columns, so undo that here rather than
    forwarding ``inferSchema`` to the TVF: Spark's own row parser does not consume the flag
    either (only ``CSVInferSchema`` does), so the schema is the whole of its effect.
    """
    return [
        c._replace(spark_type=_STRING_SPARK_TYPE_JSON, nullable=True) for c in columns
    ]


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
            "COLUMN_NAME": _nss_column_name(c.name, i),
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
