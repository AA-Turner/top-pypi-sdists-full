#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import re
from typing import Any

import pyspark.sql.connect.proto.relations_pb2 as relation_proto

from snowflake import snowpark
from snowflake.snowpark import DataFrame, DataFrameReader, Session
from snowflake.snowpark._internal.analyzer import analyzer_utils
from snowflake.snowpark._internal.type_utils import convert_sf_to_sp_type
from snowflake.snowpark.types import (
    ArrayType,
    DataType,
    MapType,
    StringType,
    StructField,
    StructType,
    TimestampTimeZone,
    TimestampType,
    VariantType,
)
from snowflake.snowpark_connect.config import (
    get_boolean_session_config_param,
    global_config,
)
from snowflake.snowpark_connect.dataframe_container import DataFrameContainer
from snowflake.snowpark_connect.error.error_codes import ErrorCodes
from snowflake.snowpark_connect.error.error_utils import attach_custom_error_code
from snowflake.snowpark_connect.relation.read.map_read_partitioned_file import (
    _read_file_with_partitions,
)
from snowflake.snowpark_connect.relation.read.metadata_utils import (
    add_filename_metadata_to_reader,
)
from snowflake.snowpark_connect.relation.read.reader_config import ReaderWriterConfig
from snowflake.snowpark_connect.relation.read.utils import (
    apply_metadata_exclusion_pattern,
    rename_columns_as_snowflake_standard,
)
from snowflake.snowpark_connect.type_support import emulate_integral_types
from snowflake.snowpark_connect.utils.io_utils import cached_file_format
from snowflake.snowpark_connect.utils.telemetry import (
    SnowparkConnectNotImplementedError,
)


def _parse_path_tokens(path: str) -> list[str]:
    """
    Parse a Snowflake FLATTEN path into a list of tokens for tree construction.

    This function tokenizes paths returned by Snowflake's FLATTEN function,
    handling various path formats including bracket-quoted names (for fields
    with special characters), array indices, and dot-separated identifiers.

    Args:
        path: A path string from FLATTEN output, e.g., "user.id", "[0].name",
              or "['field.with.dots']".

    Returns:
        List of path tokens. Examples:
        - "user.id" -> ["user", "id"]
        - "[0].name" -> ["[0]", "name"]
        - "['user.name']" -> ["user.name"]
        - "items[0].key" -> ["items", "[0]", "key"]
    """
    if not path:
        return []

    pattern = r"\['([^']+)'\]|\[\"([^\"]+)\"\]|(\"[^\"]+\")|(\[\d+\])|([^.\[\]]+)"
    tokens = []
    for match in re.finditer(pattern, path):
        token = (
            match.group(1)
            or match.group(2)
            or match.group(3)
            or match.group(4)
            or match.group(5)
        )
        if token:
            tokens.append(token)
    return tokens


def _merge_leaf_type(current: str | None, new_type: str) -> str | None:
    """
    Merge two leaf type strings when the same path has multiple type observations.

    This handles type conflicts that occur when different rows have different types
    for the same field (e.g., some rows have INTEGER, others have VARCHAR).

    Args:
        current: The currently observed type for this path, or None if first observation.
        new_type: The newly observed type from TYPEOF() result.

    Returns:
        The merged type string. Rules:
        - NULL_VALUE is ignored (returns current)
        - If current is None or NULL_VALUE, returns new_type
        - If types match, returns that type
        - If types conflict, returns VARCHAR as a safe fallback
    """
    if new_type == "NULL_VALUE":
        return current
    if current is None or current == "NULL_VALUE":
        return new_type
    if current == new_type:
        return current
    return "VARCHAR"


def _build_tree_from_flatten(path_type_pairs: list[tuple[str, str]]) -> dict[str, Any]:
    """
    Build an intermediate tree structure from FLATTEN path/type pairs.

    This function processes the raw output from Snowflake's FLATTEN function
    and constructs a tree that represents the nested structure of the data.
    The tree uses special keys:
    - "__meta": Container type ("ARRAY" or "OBJECT")
    - "__children": Dict of child nodes
    - "__leaf_type": The TYPEOF result for leaf values
    - "_element": Placeholder for array elements (normalized from [0], [1], etc.)

    Args:
        path_type_pairs: List of (path, type) tuples from FLATTEN output.
            Paths like "user.id" or "[0].key", types like "VARCHAR", "INTEGER".

    Returns:
        A nested dict representing the tree structure with metadata.

    Example:
        Input: [("id", "VARCHAR"), ("items", "ARRAY"), ("[0].name", "VARCHAR")]
        Output: {
            "__meta": "OBJECT",
            "__children": {
                "id": {"__meta": "OBJECT", "__children": {}, "__leaf_type": "VARCHAR"},
                "items": {
                    "__meta": "ARRAY",
                    "__children": {
                        "_element": {"__meta": "OBJECT", "__children": {...}, ...}
                    },
                    "__leaf_type": None
                }
            },
            "__leaf_type": None
        }
    """
    containers: dict[tuple[str, ...], str] = {}
    leaves: dict[tuple[str, ...], str] = {}

    for path, dtype in path_type_pairs:
        tokens = _parse_path_tokens(path)
        normalized = tuple(
            "_element" if re.fullmatch(r"\[\d+\]", t or "") else t for t in tokens
        )

        for i, token in enumerate(normalized):
            if token == "_element":
                # Parent path before the array element; empty tuple () if array is at root
                containers.setdefault(normalized[:i] if i else (), "ARRAY")
                break

        if dtype in {"ARRAY", "OBJECT"}:
            containers.setdefault(normalized, dtype)
            continue

        leaves[normalized] = _merge_leaf_type(leaves.get(normalized), dtype)

    root: dict[str, Any] = {"__meta": "OBJECT", "__children": {}, "__leaf_type": None}

    def _ensure_node(children: dict[str, Any], token: str) -> dict[str, Any]:
        if token not in children:
            children[token] = {
                "__meta": "OBJECT",
                "__children": {},
                "__leaf_type": None,
            }
        return children[token]

    for path_tokens in sorted(set(containers) | set(leaves), key=len):
        if not path_tokens:
            if path_tokens in containers:
                root["__meta"] = containers[path_tokens]
            if path_tokens in leaves and leaves[path_tokens] is not None:
                root["__leaf_type"] = leaves[path_tokens]
            continue
        node = root
        for token in path_tokens:
            node = _ensure_node(node["__children"], token)
        if path_tokens in containers:
            node["__meta"] = containers[path_tokens]
        if path_tokens in leaves and leaves[path_tokens] is not None:
            node["__leaf_type"] = leaves[path_tokens]

    return root


def _is_key_value_map_node(node: dict[str, Any]) -> bool:
    """Check if a node represents a Parquet map encoded by the non-vectorized scanner.

    The non-vectorized scanner preserves Parquet MAP encoding as:
        key_value (ARRAY)
          _element (OBJECT)
            key   (leaf)
            value (leaf or nested)

    A node whose only non-metadata child is ``key_value`` with this structure
    is a map, not a struct.
    """
    children = node.get("__children", {})
    real_children = {k: v for k, v in children.items() if k != "_element"}
    if set(real_children.keys()) != {"key_value"}:
        return False

    kv_node = real_children["key_value"]
    kv_meta = kv_node.get("__meta", "OBJECT")
    kv_children = kv_node.get("__children", {})

    if kv_meta != "ARRAY" and "_element" not in kv_children:
        return False

    element_node = kv_children.get("_element")
    if element_node is None:
        return False

    element_children = {
        k for k in element_node.get("__children", {}) if k != "_element"
    }
    return element_children == {"key", "value"}


def _reconstruct_schema(node: dict[str, Any]) -> DataType:
    """
    Recursively convert a tree node into a Snowpark DataType.

    This function traverses the intermediate tree structure built by
    _build_tree_from_flatten and converts each node into the appropriate
    Snowpark type (StructType, ArrayType, MapType, or primitive types).

    MapType detection: when the non-vectorized Parquet scanner is used,
    maps appear as a ``key_value`` ARRAY with ``key``/``value`` children.
    This pattern is detected at every level of the tree so that nested
    maps (e.g. struct<tags: map<string, string>>) are handled correctly.

    Args:
        node: A tree node dict with keys:
            - "__meta": Container type ("ARRAY" or "OBJECT")
            - "__children": Dict of child nodes keyed by field name
            - "__leaf_type": TYPEOF string for leaf values (e.g., "VARCHAR")

    Returns:
        The corresponding Snowpark DataType:
        - MapType if node matches the key_value array pattern
        - ArrayType if meta is "ARRAY" or has "_element" child
        - StructType if node has children (non-array)
        - Primitive type from _map_typeof_to_snowpark_type if leaf
        - VariantType as fallback
    """
    meta = node.get("__meta", "OBJECT")
    children = node.get("__children", {})
    leaf_type = node.get("__leaf_type")

    # Detect Parquet MAP encoded as key_value array (non-vectorized scanner)
    if _is_key_value_map_node(node):
        element_node = children["key_value"]["__children"]["_element"]
        key_node = element_node["__children"]["key"]
        value_node = element_node["__children"]["value"]
        key_type = _reconstruct_schema(key_node)
        value_type = _reconstruct_schema(value_node)
        return MapType(key_type, value_type)

    if meta == "ARRAY" or "_element" in children:
        element_node = children.get("_element")
        element_type = (
            _reconstruct_schema(element_node) if element_node else VariantType()
        )
        return ArrayType(element_type, structured=True)

    if children:
        fields = []
        for key, child in sorted(children.items()):
            if key == "_element":
                continue
            child_type = _reconstruct_schema(child)
            if child_type:
                fields.append(StructField(key, child_type, nullable=True))
        return StructType(fields, structured=True)

    if leaf_type:
        return _map_typeof_to_snowpark_type(leaf_type)

    return VariantType()


def _build_struct_from_paths(
    path_type_pairs: list[tuple[str, str]]
) -> StructType | ArrayType | None:
    """
    Build a StructType from a list of (path, type) pairs from FLATTEN output.

    Handles:
    - Simple structs: ("id", "VARCHAR") -> StructType([StructField("id", StringType())])
    - Nested structs: ("user.id", "VARCHAR") -> StructType([StructField("user", StructType(...))])
    - Arrays: ("[0].key", "VARCHAR") -> ArrayType(StructType([StructField("key", StringType())]))
    - Dotted field names: ("['user.name']", "VARCHAR") -> StructType([StructField("user.name", StringType())])

    Example input:
        [("event_id", "INTEGER"),
         ("user", "OBJECT"),
         ("user.id", "VARCHAR"),
         ("user.name", "VARCHAR")]

    Output:
        StructType([
            StructField("event_id", LongType()),
            StructField("user", StructType([
                StructField("id", StringType()),
                StructField("name", StringType())
            ]))
        ])
    """
    if not path_type_pairs:
        return None

    tree = _build_tree_from_flatten(path_type_pairs)
    return _reconstruct_schema(tree)


def _detect_map_type(
    session: Session,
    temp_view_name: str,
    column_name: str,
    path_type_pairs: list[tuple[str, str]],
    input_expr: str | None = None,
) -> MapType | None:
    """
    Detect if a VARIANT column is actually a Parquet map (vectorized scanner fallback).

    When the non-vectorized scanner is used, maps are detected via the
    ``key_value`` array pattern in ``_reconstruct_schema`` (which handles
    nested struct/map values recursively).  This function provides a fallback
    for the vectorized scanner, where map keys appear as individual JSON
    fields and need a heuristic (key cardinality) to distinguish from structs.

    Handles maps with both leaf-type values (e.g. Map<String, Int>) and
    complex-type values (e.g. Map<String, Struct<...>>).

    Returns MapType(StringType(), value_type) if detected, else None.
    """
    effective_input = input_expr or column_name
    # Top-level paths: no dots and not array indices like [0], [1].
    # Bracket-quoted keys like ['1'] or ['my_key'] ARE top-level map keys
    # (Snowflake FLATTEN uses this notation for numeric-string and special-char keys).
    top_level = [
        (p, t)
        for p, t in path_type_pairs
        if "." not in p and not re.fullmatch(r"\[\d+\]", p)
    ]
    if not top_level:
        return None

    leaf_types = {
        "INTEGER",
        "VARCHAR",
        "DOUBLE",
        "BOOLEAN",
        "DECIMAL",
        "REAL",
        "DATE",
        "TIME",
        "TIMESTAMP_NTZ",
        "TIMESTAMP_LTZ",
        "TIMESTAMP_TZ",
        "BINARY",
        "NULL_VALUE",
        "NULL",
    }

    top_types = {t for _, t in top_level if t not in ("NULL_VALUE", "NULL")}
    all_leaf = top_types <= leaf_types
    all_complex = top_types <= {"OBJECT", "ARRAY"}

    if not all_leaf and not all_complex:
        return None

    try:
        # Count total distinct keys vs max keys in any single row.
        # GROUP BY the variant value to approximate per-row grouping.
        query = (
            f"WITH per_row AS ("
            f"  SELECT {effective_input} AS v, COUNT(f.key) AS key_cnt"
            f"  FROM {temp_view_name},"
            f"  LATERAL FLATTEN(input => {effective_input}) f"
            f"  GROUP BY {effective_input}"
            f") "
            f"SELECT"
            f"  (SELECT COUNT(DISTINCT f.key) FROM {temp_view_name},"
            f"   LATERAL FLATTEN(input => {effective_input}) f) AS total_distinct,"
            f"  (SELECT MAX(key_cnt) FROM per_row) AS max_per_row"
        )
        result = session.sql(query).collect()
        total_distinct = result[0]["TOTAL_DISTINCT"]
        max_per_row = result[0]["MAX_PER_ROW"]
    except Exception:
        return None

    if total_distinct is None or max_per_row is None:
        return None
    if total_distinct <= max_per_row:
        return None  # same keys every row → struct

    # It's a map. Infer value type from FLATTEN results.
    if all_leaf:
        value_types = {t for _, t in top_level if t != "NULL_VALUE"}
        has_nulls = any(t == "NULL_VALUE" for _, t in top_level)
        if len(value_types) == 1:
            value_type = _map_typeof_to_snowpark_type(value_types.pop())
            # Snowflake's CAST to MAP(VARCHAR, <non-string>) fails when the
            # map contains null values.  Fall back to VARIANT for the value
            # type so the CAST produces MAP(VARCHAR, VARIANT) which is null-safe.
            # MAP(VARCHAR, VARCHAR) handles nulls correctly so StringType is exempt.
            if has_nulls and not isinstance(value_type, StringType):
                value_type = VariantType()
        else:
            value_type = VariantType()
    else:
        # Complex values (OBJECT/ARRAY): infer value schema from nested paths.
        # Strip the map key prefix from nested paths and build the value type.
        top_keys = {p for p, _ in top_level}
        nested_pairs = []
        for p, t in path_type_pairs:
            if "." in p:
                key, rest = p.split(".", 1)
                if key in top_keys:
                    nested_pairs.append((rest, t))

        if nested_pairs:
            value_type = _build_struct_from_paths(nested_pairs)
            if value_type is None:
                value_type = VariantType()
        else:
            value_type = VariantType()

    return MapType(StringType(), value_type)


def discover_variant_schema(
    session: Session,
    temp_view_name: str,
    column_name: str,
    input_expr: str | None = None,
) -> DataType | None:
    """
    Discover the schema of a VARIANT column using Snowflake's FLATTEN.

    Args:
        session: Snowpark session
        temp_view_name: Name of temp view containing the data
        column_name: Column name in the view
        input_expr: Optional SQL expression to use as FLATTEN input instead of
            the raw column name. Used for STRING columns where the input needs
            to be wrapped in TRY_PARSE_JSON().

    Returns:
        - MapType if the column looks like a Parquet map (varying keys per row)
        - StructType if the column has consistent keys (struct-like)
        - None if discovery fails
    """
    effective_input = input_expr or column_name
    try:

        def run_query(flatten_input: str):
            query = (
                f"SELECT DISTINCT f.path, TYPEOF(f.value) AS data_type "
                f"FROM {temp_view_name}, "
                f"LATERAL FLATTEN(input => {flatten_input}, recursive => true) f "
                f"ORDER BY f.path"
            )
            return session.sql(query).collect()

        result = run_query(effective_input)

        # Convert results to path/type pairs
        path_type_pairs = []
        for row in result:
            path_type_pairs.append((row["PATH"], row["DATA_TYPE"]))

        # Check if this is a Parquet map before building a struct
        map_type = _detect_map_type(
            session,
            temp_view_name,
            column_name,
            path_type_pairs,
            input_expr=effective_input,
        )
        if map_type is not None:
            return map_type

        schema = _build_struct_from_paths(path_type_pairs)
        return schema

    except Exception:
        return None


def _check_map_has_null_values(
    session: Session,
    temp_view_name: str,
    column_name: str,
) -> bool:
    """Check if a VARIANT map column contains null values using the vectorized scanner.

    The NVS scanner omits null values from FLATTEN output, so this function
    runs a FLATTEN query on a small vectorized-scanner sampled view to detect
    whether any map entry has a null value (TYPEOF = 'NULL_VALUE').
    """
    try:
        query = (
            f"SELECT COUNT(*) AS null_count "
            f"FROM {temp_view_name}, "
            f"LATERAL FLATTEN(input => {column_name}) f "
            f"WHERE TYPEOF(f.value) = 'NULL_VALUE'"
        )
        result = session.sql(query).collect()
        return result[0]["NULL_COUNT"] > 0
    except Exception:
        return False


def _merge_variant_schemas(
    df: DataFrame,
    session: Session,
    sampled_df: DataFrame,
    vs_sampled_df: DataFrame | None = None,
) -> list[DataType]:
    """
    For each VARIANT or JSON-string column in the DataFrame, attempt to discover
    its struct schema.  Returns a list of DataTypes with VARIANT/STRING columns
    replaced by discovered StructTypes.
    Uses parallel execution for better performance with multiple columns.

    STRING columns are included because the write path casts structured types
    to VARIANT before COPY INTO, and Snowflake serializes VARIANT as JSON
    strings in Parquet.  On read these appear as StringType.

    Args:
        df: The original DataFrame (used to get schema info)
        session: Snowpark session
        sampled_df: Pre-sampled DataFrame to use for schema discovery
        vs_sampled_df: Optional vectorized-scanner sample for null-value
            detection in maps.  When NVS is used for discovery, its FLATTEN
            output omits null values; the vectorized scanner preserves them.
    """
    import os
    import uuid
    from concurrent.futures import ThreadPoolExecutor, as_completed

    # Identify VARIANT and STRING columns as candidates for discovery.
    # For STRING columns, we'll use TRY_PARSE_JSON as the FLATTEN input.
    discovery_columns: list[tuple[int, str, bool]] = []
    for idx, field in enumerate(df.schema.fields):
        if isinstance(field.datatype, VariantType):
            discovery_columns.append((idx, field.name, False))
        elif isinstance(field.datatype, StringType):
            discovery_columns.append((idx, field.name, True))

    if not discovery_columns:
        return [field.datatype for field in df.schema.fields]

    discovered_schemas: dict[int, StructType | None] = {}
    max_workers = min(
        len(discovery_columns),
        int(os.environ.get("SNOWPARK_CONNECT_SCHEMA_DISCOVERY_WORKERS", "8")),
    )

    temp_view_name = f"_VARIANT_SCHEMA_DISCOVERY_{uuid.uuid4().hex}"
    sampled_df.create_or_replace_temp_view(temp_view_name)

    def discover_for_column(item):
        idx, col_name, needs_parse = item
        expr = f"TRY_PARSE_JSON({col_name})" if needs_parse else None
        return idx, discover_variant_schema(
            session, temp_view_name, col_name, input_expr=expr
        )

    try:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(discover_for_column, item): item
                for item in discovery_columns
            }
            for future in as_completed(futures):
                idx, schema = future.result()
                discovered_schemas[idx] = schema
    finally:
        session.sql(f"DROP VIEW IF EXISTS {temp_view_name}").collect()

    # Retry with full (un-sampled) data for columns that returned None
    variant_only = [
        (idx, name) for idx, name, needs_parse in discovery_columns if not needs_parse
    ]
    missing_columns = [
        (idx, name) for idx, name in variant_only if discovered_schemas.get(idx) is None
    ]
    if missing_columns:
        temp_view_name_full = f"_VARIANT_SCHEMA_DISCOVERY_{uuid.uuid4().hex}_full"
        df.create_or_replace_temp_view(temp_view_name_full)
        try:
            for idx, col_name in missing_columns:
                discovered_schemas[idx] = discover_variant_schema(
                    session, temp_view_name_full, col_name
                )
        finally:
            session.sql(f"DROP VIEW IF EXISTS {temp_view_name_full}").collect()

    # Two-pass null check: for map columns with non-string value types,
    # query the vectorized scanner data to check if null values exist.
    # NVS omits nulls from FLATTEN output, so we need the VS data for this.
    if vs_sampled_df is not None:
        map_columns_to_check = [
            (idx, name)
            for idx, name, _ in discovery_columns
            if isinstance(discovered_schemas.get(idx), MapType)
            and not isinstance(discovered_schemas[idx].value_type, StringType)
        ]
        if map_columns_to_check:
            import uuid as _uuid

            vs_view = f"_VS_NULL_CHECK_{_uuid.uuid4().hex}"
            vs_sampled_df.create_or_replace_temp_view(vs_view)
            try:
                for idx, col_name in map_columns_to_check:
                    has_nulls = _check_map_has_null_values(session, vs_view, col_name)
                    if has_nulls:
                        discovered_schemas[idx] = MapType(
                            discovered_schemas[idx].key_type, VariantType()
                        )
            finally:
                session.sql(f"DROP VIEW IF EXISTS {vs_view}").collect()

    # Build result types, replacing VARIANT/STRING with discovered schemas
    result_types = []
    for idx, field in enumerate(df.schema.fields):
        if idx in discovered_schemas:
            schema = discovered_schemas[idx]
            if schema:
                result_types.append(schema)
            else:
                result_types.append(field.datatype)
        else:
            result_types.append(field.datatype)

    return result_types


def _create_nvs_sample(
    session: Session,
    path: str,
    file_format_options: dict[str, Any],
    sample_size: int,
) -> DataFrame | None:
    """Create a sampled DataFrame using the non-vectorized Parquet scanner.

    The non-vectorized scanner preserves Parquet MAP encoding as ``key_value``
    arrays, which allows ``_reconstruct_schema`` to distinguish maps from
    structs.  This sample is used only for schema discovery; the main data
    read uses whatever scanner the user configured.

    Returns None if the non-vectorized read fails for any reason, so the
    caller can fall back to the regular sample.
    """
    try:
        nvs_options = {**file_format_options, "USE_VECTORIZED_SCANNER": False}
        nvs_format = cached_file_format(session, "parquet", nvs_options)
        nvs_df = session.read.options(
            {"FORMAT_NAME": nvs_format, "ENFORCE_EXISTING_FILE_FORMAT": True}
        ).parquet(path)
        return nvs_df.sample(n=sample_size)
    except Exception:
        return None


def _create_vs_sample(
    session: Session,
    path: str,
    file_format_options: dict[str, Any],
    sample_size: int,
) -> DataFrame | None:
    """Create a sampled DataFrame using the vectorized Parquet scanner.

    The vectorized scanner preserves NULL values in its output, which is
    needed to detect null map values that the NVS scanner omits.  This
    sample is used only for the null-value check in map columns.

    Returns None if the read fails for any reason.
    """
    try:
        vs_options = {**file_format_options, "USE_VECTORIZED_SCANNER": True}
        vs_format = cached_file_format(session, "parquet", vs_options)
        vs_df = session.read.options(
            {"FORMAT_NAME": vs_format, "ENFORCE_EXISTING_FILE_FORMAT": True}
        ).parquet(path)
        return vs_df.sample(n=sample_size)
    except Exception:
        return None


def map_read_parquet(
    rel: relation_proto.Relation,
    schema: StructType | None,
    session: snowpark.Session,
    paths: list[str],
    options: ReaderWriterConfig,
) -> DataFrameContainer:
    """Read a Parquet file into a Snowpark DataFrame."""

    if rel.read.is_streaming is True:
        exception = SnowparkConnectNotImplementedError(
            "Streaming is not supported for Parquet files."
        )
        attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
        raise exception

    converted_snowpark_options = options.convert_to_snowpark_args()
    file_format_options = _parse_parquet_snowpark_options(converted_snowpark_options)
    raw_options = rel.read.data_source.options
    assert len(paths) > 0, "Read PARQUET expects at least one path"

    snowpark_options = {
        # Setting these two options prevents a significant number of additional CREATE TEMPORARY
        # FILE FORMAT and DROP FILE FORMAT queries. If FORMAT_NAME is not set, the Snowpark DF reader
        # will eagerly issue a CREATE TEMPORARY FILE FORMAT when inferring the schema of the result;
        # if ENFORCE_EXISTING_FILE_FORMAT is not set, an additional CREATE ... command will be
        # issued when the lazy DF is materialized by a cache_result call.
        "FORMAT_NAME": converted_snowpark_options.get(
            "FORMAT_NAME",
            cached_file_format(session, "parquet", file_format_options),
        ),
        "ENFORCE_EXISTING_FILE_FORMAT": True,
    }

    if "PATTERN" in converted_snowpark_options:
        snowpark_options["PATTERN"] = converted_snowpark_options.get("PATTERN")

    apply_metadata_exclusion_pattern(snowpark_options)

    reader = add_filename_metadata_to_reader(
        session.read.options(snowpark_options), raw_options
    )

    if len(paths) == 1:
        df, read_using_external_table = _read_parquet_with_partitions(
            session, reader, paths[0], schema, snowpark_options, raw_options
        )
        can_be_cached = not read_using_external_table
    else:
        is_merge_schema = options.config.get("mergeschema")
        df, read_using_external_table = _read_parquet_with_partitions(
            session, reader, paths[0], schema, snowpark_options, raw_options
        )
        can_be_cached = not read_using_external_table
        schema_cols = df.columns
        for p in paths[1:]:
            reader._user_schema = None
            partition_df, read_using_external_table = _read_parquet_with_partitions(
                session, reader, p, schema, snowpark_options, raw_options
            )
            df = df.union_all_by_name(
                partition_df,
                allow_missing_columns=True,
            )
            can_be_cached = can_be_cached and not read_using_external_table

        if not is_merge_schema:
            df = df.select(*schema_cols)

    infer_ntz = get_boolean_session_config_param(
        "spark.sql.parquet.inferTimestampNTZ.enabled"
    )
    if not infer_ntz:
        df = _cast_ntz_to_ltz(df)
    spark_column_names = [analyzer_utils.unquote_if_quoted(c) for c in df.columns]
    renamed_df, snowpark_column_names = rename_columns_as_snowflake_standard(
        df, rel.common.plan_id
    )

    rows_to_infer = int(options.config.get("rowstoinferschema", 1000))
    sampled_df = df.sample(n=rows_to_infer)

    # NVS-based map discovery only works when the main df uses the vectorized
    # scanner (native map format).  When the main df uses NVS (VS=false), the
    # data is in key_value array format which can't be CAST to MAP types.
    main_uses_vs = str(
        file_format_options.get("USE_VECTORIZED_SCANNER", "true")
    ).lower() in ("true", "1")

    # Use the non-vectorized scanner so that Parquet MAP encoding is preserved
    # as key_value arrays, letting _reconstruct_schema distinguish maps from structs.
    nvs_sampled_df = (
        _create_nvs_sample(session, paths[0], file_format_options, rows_to_infer)
        if main_uses_vs
        else None
    )

    # Create a dedicated vectorized scanner sample for null-value detection.
    # The NVS omits null values; the VS preserves them.
    vs_sampled_df = (
        _create_vs_sample(session, paths[0], file_format_options, rows_to_infer)
        if nvs_sampled_df is not None
        else None
    )

    discovered_types = _merge_variant_schemas(
        df,
        session,
        nvs_sampled_df if nvs_sampled_df is not None else sampled_df,
        vs_sampled_df=vs_sampled_df,
    )

    from snowflake.snowpark.functions import builtin

    parse_json = builtin("PARSE_JSON")
    cast_columns = []
    has_casts = False
    cast_base_df = renamed_df
    for col_name, field, discovered_type in zip(
        cast_base_df.columns, cast_base_df.schema.fields, discovered_types
    ):
        is_variant = isinstance(field.datatype, VariantType)
        is_string = isinstance(field.datatype, StringType)
        is_complex_discovered = (
            (isinstance(discovered_type, StructType) and discovered_type.structured)
            or isinstance(discovered_type, ArrayType)
            or isinstance(discovered_type, MapType)
        )

        if is_complex_discovered and is_variant:
            # When VS=false, the data is in key_value format for maps.
            # CAST to MapType only works on native map format (VS=true).
            if not main_uses_vs and isinstance(discovered_type, MapType):
                cast_columns.append(cast_base_df[col_name])
                continue
            cast_columns.append(
                cast_base_df[col_name].cast(discovered_type).alias(col_name)
            )
            has_casts = True
        elif is_complex_discovered and is_string:
            cast_columns.append(
                parse_json(cast_base_df[col_name]).cast(discovered_type).alias(col_name)
            )
            has_casts = True
        else:
            cast_columns.append(cast_base_df[col_name])

    if has_casts:
        cast_base_df = cast_base_df.select(cast_columns)

    return DataFrameContainer.create_with_column_mapping(
        dataframe=cast_base_df,
        spark_column_names=spark_column_names,
        snowpark_column_names=snowpark_column_names,
        snowpark_column_types=[emulate_integral_types(t) for t in discovered_types],
        can_be_cached=can_be_cached,
    )


def _read_parquet_with_partitions(
    session: Session,
    reader: DataFrameReader,
    path: str,
    schema: StructType | None,
    snowpark_options: dict[str, Any],
    raw_options: dict[str, Any],
) -> tuple[DataFrame, bool]:
    """
    Reads parquet files and adds partition columns from subdirectories.
    Returns a tuple of read DataFrame and a boolean indicating if DataFrame was read from external table.

    This function delegates to the generalized _read_file_with_partitions function.
    """

    return _read_file_with_partitions(
        session=session,
        reader=reader,
        file_format="parquet",
        path=path,
        schema=schema,
        snowpark_options=snowpark_options,
        raw_options=raw_options,
    )


def _cast_ntz_to_ltz(df: DataFrame) -> DataFrame:
    """When inferTimestampNTZ.enabled is false, reinterpret TIMESTAMP_NTZ columns as UTC instants.

    A simple CAST(ntz AS TIMESTAMP_LTZ) interprets the NTZ value in the session
    timezone, which preserves the wall-clock time. We need CONVERT_TIMEZONE which
    treats NTZ as UTC, matching Spark's behavior of reading all Parquet timestamps
    as UTC-based instants regardless of isAdjustedToUTC.
    """
    from snowflake.snowpark.functions import builtin, col, lit

    convert_tz = builtin("CONVERT_TIMEZONE")
    session_tz = global_config.spark_sql_session_timeZone
    ltz_type = TimestampType(TimestampTimeZone.LTZ)
    for field in df.schema.fields:
        if (
            isinstance(field.datatype, TimestampType)
            and field.datatype.tz == TimestampTimeZone.NTZ
        ):
            df = df.with_column(
                field.name,
                convert_tz(lit("UTC"), lit(session_tz), col(field.name)).cast(ltz_type),
            )
    return df


_parquet_file_format_allowed_options = {
    "COMPRESSION",
    "SNAPPY_COMPRESSION",
    "BINARY_AS_TEXT",
    "TRIM_SPACE",
    "USE_LOGICAL_TYPE",
    "USE_VECTORIZED_SCANNER",
    "REPLACE_INVALID_CHARACTERS",
    "NULL_IF",
}


def _parse_parquet_snowpark_options(snowpark_options: dict[str, Any]) -> dict[str, Any]:
    file_format_options = dict()
    for key, value in snowpark_options.items():
        upper_key = key.upper()
        if upper_key in _parquet_file_format_allowed_options:
            file_format_options[upper_key] = value
    return file_format_options


def _map_typeof_to_snowpark_type(typeof_result: str) -> DataType:
    """
    Map a Snowflake TYPEOF() result to a Snowpark DataType.

    TYPEOF() returns strings like: VARCHAR, INTEGER, OBJECT, ARRAY, BOOLEAN, etc.
    This function delegates to Snowpark's convert_sf_to_sp_type where possible.
    """
    typeof_upper = typeof_result.upper()

    # NULL_VALUE (JSON null) and NULL (SQL NULL) can't determine type
    if typeof_upper in ("NULL_VALUE", "NULL"):
        return StringType()

    # Mapping from TYPEOF() result names to Snowflake metadata type names
    # used by convert_sf_to_sp_type.
    _TYPEOF_TO_SF_TYPE_MAP = {
        "VARCHAR": "TEXT",
        "INTEGER": "FIXED",
        "DECIMAL": "REAL",
        "DOUBLE": "REAL",
        "REAL": "REAL",
        "BOOLEAN": "BOOLEAN",
        "DATE": "DATE",
        "TIME": "TIME",
        "TIMESTAMP_NTZ": "TIMESTAMP_NTZ",
        "TIMESTAMP_LTZ": "TIMESTAMP_LTZ",
        "TIMESTAMP_TZ": "TIMESTAMP_TZ",
        "BINARY": "BINARY",
    }

    sf_type = _TYPEOF_TO_SF_TYPE_MAP.get(typeof_upper)
    if sf_type:
        try:
            return convert_sf_to_sp_type(
                sf_type,
                precision=38,
                scale=0,
                internal_size=0,
                max_string_size=0,
            )
        except NotImplementedError:
            return VariantType()

    # Default fallback for unknown types
    return VariantType()
