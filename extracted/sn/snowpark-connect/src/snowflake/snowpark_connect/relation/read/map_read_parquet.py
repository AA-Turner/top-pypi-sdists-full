#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import re
import textwrap
from typing import Any

import pyspark.sql.connect.proto.relations_pb2 as relation_proto

from snowflake import snowpark
from snowflake.snowpark import Column, DataFrame, DataFrameReader, Session
from snowflake.snowpark._internal.analyzer import analyzer_utils
from snowflake.snowpark._internal.type_utils import convert_sf_to_sp_type
from snowflake.snowpark._internal.utils import (
    TempObjectType,
    random_name_for_temp_object,
)
from snowflake.snowpark.types import (
    ArrayType,
    BinaryType,
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
    str_to_bool,
)
from snowflake.snowpark_connect.dataframe_container import DataFrameContainer
from snowflake.snowpark_connect.error.error_codes import ErrorCodes
from snowflake.snowpark_connect.error.error_utils import attach_custom_error_code
from snowflake.snowpark_connect.relation.read.map_read_partitioned_file import (
    _discover_partition_columns,
    _read_partitioned_file_with_partitions,
    use_external_table,
)
from snowflake.snowpark_connect.relation.read.metadata_utils import (
    add_filename_metadata_to_reader,
    populate_metadata,
)
from snowflake.snowpark_connect.relation.read.reader_config import ReaderWriterConfig
from snowflake.snowpark_connect.relation.read.utils import (
    _load_file_with_copy_into,
    _norm,
    apply_metadata_exclusion_pattern,
    extract_relative_file_path,
    generate_stage_path_groups,
    normalize_stage_path,
    rename_columns_as_snowflake_standard,
)
from snowflake.snowpark_connect.type_mapping import map_type_to_snowflake_type
from snowflake.snowpark_connect.type_support import emulate_integral_types
from snowflake.snowpark_connect.utils.io_utils import cached_file_format
from snowflake.snowpark_connect.utils.snowpark_connect_logging import logger
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
                # Quote with exact case so Snowpark does not uppercase the name
                # when building the OBJECT(...) cast SQL. FLATTEN preserves the
                # original JSON key case (lowercase for Parquet files).
                quoted_key = analyzer_utils.quote_name(key, keep_case=True)
                fields.append(StructField(quoted_key, child_type, nullable=True))
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


_LEAF_TYPES = frozenset(
    {
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
)


def _infer_map_value_type(
    path_type_pairs: list[tuple[str, str]],
    top_level: list[tuple[str, str]],
    all_leaf: bool,
) -> DataType:
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
        nested_pairs = [
            (rest, t)
            for p, t in path_type_pairs
            if "." in p
            for key, rest in [p.split(".", 1)]
            if key in top_keys
        ]
        if nested_pairs:
            value_type = _build_struct_from_paths(nested_pairs)
            if value_type is None:
                value_type = VariantType()
        else:
            value_type = VariantType()
    return value_type


def _discover_all_variant_schemas(
    session: Session,
    temp_view_name: str,
    columns: list[tuple[int, str, str | None]],
) -> dict[int, DataType | None]:
    """
    Discover struct/map schemas for multiple columns in a single SQL round-trip.

    Uses UNPIVOT to rotate all target columns into rows, then a single
    recursive LATERAL FLATTEN produces ``(col_name, path, data_type)`` triples
    for every column at once.

    We cannot reliably distinguish between struct and map types, and must use
    key cardinality as a heuristic. A second non-recursive flatten CTE computes this
    for each column.

    Args:
        session: Snowpark session
        temp_view_name: Name of temp view containing the data
        columns: List of (column_index, column_name, input_expr_or_None)
            tuples.  If set, `input_expr` overrides the column name used
            as the FLATTEN input.

    Returns:
        Dict mapping column index to the discovered ``DataType``, or ``None``
        when discovery fails for that column.
    """
    if not columns:
        return {}

    # Build a CTE that normalises every target column to VARIANT and
    # aliases it to a stable name (_c0, _c1, ...) so the UNPIVOT is clean.
    alias_map: dict[str, int] = {}  # maps unpivot alias -> original column
    cte_cols: list[str] = []
    unpivot_names: list[str] = []
    for idx, col_name, input_expr in columns:
        alias = f"_C{idx}"
        alias_map[alias] = idx
        effective = input_expr or col_name
        cte_cols.append(f"{effective} AS {alias}")
        unpivot_names.append(alias)

    unpivot_list = ", ".join(unpivot_names)

    cte_col_list = ", ".join(cte_cols)
    # This query is split into a few components:
    # 1. _src: UNPIVOT rotates N columns into N rows per original row, each tagged with _col_name and
    #          holding the VARIANT value in _val.
    # 2. _paths: Recursive FLATTEN to get full paths/types of sub-fields.
    # 3. _keys: Non-recursive FLATTEN to compute number of distinct key entries across the whole column,
    #           and the max number of keys in any single row.
    # 4. Join paths with cardinality stats; LEFT JOIN so every column appears even when cardinality data
    # #         is absent for that column.
    query = textwrap.dedent(
        f"""
        WITH _src AS (
            SELECT {cte_col_list} FROM {temp_view_name}
        ),
        _unpivoted AS (
            SELECT _col_name, _val
            FROM _src UNPIVOT(_val FOR _col_name IN ({unpivot_list}))
            WHERE IS_OBJECT(_val) OR IS_ARRAY(_val)
        ),
        _paths AS (
            SELECT DISTINCT _col_name, f.path, TYPEOF(f.value) AS data_type
            FROM _unpivoted,
            LATERAL FLATTEN(input => _val, recursive => true) f
        ),
        _keys AS (
            SELECT _col_name, _val, f.key
            FROM _unpivoted,
            LATERAL FLATTEN(input => _val) f
        ),
        _distinct_keys AS (
            SELECT _col_name, COUNT(DISTINCT key) AS total_distinct
            FROM _keys GROUP BY _col_name
        ),
        _max_per_row AS (
            SELECT _col_name, MAX(key_cnt) AS max_per_row FROM (
                SELECT _col_name, _val, COUNT(key) AS key_cnt
                FROM _keys GROUP BY _col_name, _val
            ) GROUP BY _col_name
        )
        SELECT p._col_name, p.path, p.data_type,
            dk.total_distinct, mpr.max_per_row
        FROM _paths p
        LEFT JOIN _distinct_keys dk ON p._col_name = dk._col_name
        LEFT JOIN _max_per_row mpr ON p._col_name = mpr._col_name
        ORDER BY p._col_name, p.path
        """
    )

    try:
        rows = session.sql(query).collect()
    except Exception:
        # Exceptions here shouldn't be possible. If we encounter one, gracefully fail by
        # returning None for each column, indicating that discovery failed.
        return {idx: None for _, idx in alias_map.items()}

    # Group rows by column alias.
    per_col: dict[str, list] = {alias: [] for alias in alias_map}
    # Dict of aliases to a flag representing whether it may be a MAP type under the cardinality heuristic.
    column_may_be_map: dict[str, bool] = {}
    for row in rows:
        alias = row["_COL_NAME"]
        if alias in per_col:
            per_col[alias].append((row["PATH"], row["DATA_TYPE"]))
            # If there are more total distinct keys than the max number of keys in
            # any given row, then we can safely assume it's a MAP rather than a struct.
            column_may_be_map[alias] = row["TOTAL_DISTINCT"] > row["MAX_PER_ROW"]

    # Determine the final type for each column.
    result: dict[int, DataType | None] = {}
    for alias, idx in alias_map.items():
        pairs = per_col[alias]
        if not pairs:
            result[idx] = None
            continue

        if column_may_be_map.get(alias, False):
            # Top-level paths: no dots and not array indices like [0], [1].
            # Bracket-quoted keys like ['1'] or ['my_key'] ARE top-level map keys
            # (Snowflake FLATTEN uses this notation for numeric-string and special-char keys).
            top_level = [
                (p, t)
                for p, t in pairs
                if "." not in p and not re.fullmatch(r"\[\d+\]", p)
            ]
            if top_level:
                top_types = {t for _, t in top_level if t not in ("NULL_VALUE", "NULL")}
                all_leaf = top_types <= _LEAF_TYPES
                all_complex = top_types <= {"OBJECT", "ARRAY"}

                if all_leaf or all_complex:
                    result[idx] = MapType(
                        StringType(),
                        _infer_map_value_type(pairs, top_level, all_leaf),
                    )
                    continue
        # If some criteria for the column potentially being a map failed, just infer as struct.
        result[idx] = _build_struct_from_paths(pairs)
    return result


def _merge_variant_schemas(
    df: DataFrame,
    session: Session,
    sampled_df: DataFrame,
) -> list[DataType]:
    """
    For each VARIANT or JSON-string column in the DataFrame, attempt to discover
    its struct schema.  Returns a list of DataTypes with VARIANT/STRING columns
    replaced by discovered StructTypes.

    Issues a single UNPIVOT + FLATTEN query covering all candidate columns. Since
    this code path uses the non-vectorized scanner, map keys appear as individual
    JSON fields, and can only be distinguished from struct types by a heuristic
    (key cardinality).

    STRING columns are included because the write path casts structured types
    to VARIANT before COPY INTO, and Snowflake serializes VARIANT as JSON
    strings in Parquet.  On read these appear as StringType.

    Args:
        df: The original DataFrame (used to get schema info)
        session: Snowpark session
        sampled_df: Pre-sampled DataFrame to use for schema discovery
    """
    import uuid

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

    batch_columns = [
        (idx, col_name, f"TRY_PARSE_JSON({col_name})" if needs_parse else None)
        for idx, col_name, needs_parse in discovery_columns
    ]

    temp_table_name = f"_VARIANT_SCHEMA_DISCOVERY_{uuid.uuid4().hex}"
    sampled_df.write.save_as_table(temp_table_name, table_type="temporary")

    try:
        discovered_schemas = _discover_all_variant_schemas(
            session, temp_table_name, batch_columns
        )
    finally:
        session.sql(f"DROP TABLE IF EXISTS {temp_table_name}").collect()

    # Retry with full (un-sampled) data for VARIANT columns that returned None.
    missing_columns = [
        (idx, name, input_expr)
        for idx, name, input_expr in batch_columns
        if input_expr is None and discovered_schemas.get(idx) is None
    ]
    if missing_columns:
        temp_table_name_full = f"_VARIANT_SCHEMA_DISCOVERY_{uuid.uuid4().hex}_full"
        df.write.save_as_table(temp_table_name_full, table_type="temporary")
        try:
            full_results = _discover_all_variant_schemas(
                session, temp_table_name_full, missing_columns
            )
            discovered_schemas.update(full_results)
        finally:
            session.sql(f"DROP TABLE IF EXISTS {temp_table_name_full}").collect()

    # Build result types, replacing VARIANT/STRING with discovered schemas.
    return [
        discovered_schemas[idx]
        if (
            idx in discovered_schemas
            and discovered_schemas[idx]
            # Only accept complex types (StructType/ArrayType/MapType) from discovery.
            # Primitive types discovered via FLATTEN (e.g. BooleanType from "true"/"false"
            # strings) are unreliable — the Parquet column is physically STRING and may
            # contain non-castable values like \N null markers. INFER_SCHEMA's type is
            # always more trustworthy for primitives.
            and isinstance(discovered_schemas[idx], (StructType, ArrayType, MapType))
        )
        else field.datatype
        for idx, field in enumerate(df.schema.fields)
    ]


def _create_nvs_sample(
    session: Session,
    path: str,
    file_format_options: dict[str, Any],
    sample_size: int,
    snowpark_options: dict[str, Any] | None = None,
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
        reader_options: dict[str, Any] = {
            "FORMAT_NAME": nvs_format,
            "ENFORCE_EXISTING_FILE_FORMAT": True,
        }
        if snowpark_options and "PATTERN" in snowpark_options:
            reader_options["PATTERN"] = snowpark_options["PATTERN"]
        nvs_df = session.read.options(reader_options).parquet(path)
        return nvs_df.sample(n=sample_size)
    except Exception:
        return None


def _discover_parquet_column_types(
    df: DataFrame,
    session: Session,
    path: str,
    file_format_options: dict[str, Any],
    rows_to_infer: int,
    snowpark_options: dict[str, Any],
    main_uses_vs: bool,
) -> list[DataType]:
    """Discover column types for a no-schema parquet read via FLATTEN-based schema discovery.

    Uses a NVS (non-vectorized scanner) sample when the main read uses the vectorized
    scanner — NVS preserves the physical Parquet MAP encoding (key_value array pattern)
    which allows ``_reconstruct_schema`` to distinguish maps from structs. Falls back
    to a regular sample if NVS is unavailable.

    Args:
        df: Lazy DataFrame from the main parquet read (used for schema fields).
        session: Snowpark session.
        path: Stage path to the parquet file/directory (for NVS sampling).
        file_format_options: Parquet file format options.
        rows_to_infer: Number of rows to sample for schema discovery.
        snowpark_options: Reader options (FORMAT_NAME, PATTERN, etc.).
        main_uses_vs: Whether the main read uses the vectorized scanner. When True,
            a separate NVS sample is taken because the vectorized scanner flattens
            Parquet MAP columns into JSON objects (keys become field names), making
            it impossible to distinguish a MAP from a STRUCT during FLATTEN-based
            discovery. The NVS preserves the physical Parquet MAP encoding as a
            key_value array, which _reconstruct_schema uses to detect maps. When
            False, the main read is already NVS so no separate sample is needed.

    Returns:
        List of DataTypes aligned with ``df.schema.fields`` — VARIANT/STRING columns
        replaced by discovered StructType/ArrayType/MapType where possible.
    """
    sampled_df = df.sample(n=rows_to_infer)
    nvs_sampled_df = (
        _create_nvs_sample(
            session, path, file_format_options, rows_to_infer, snowpark_options
        )
        if main_uses_vs
        else None
    )
    return _merge_variant_schemas(
        df,
        session,
        nvs_sampled_df if nvs_sampled_df is not None else sampled_df,
    )


def _get_parquet_file_schema(
    session: Session,
    path: str,
    snowpark_options: dict,
) -> StructType | None:
    """Infer parquet schema from file metadata (no data loaded)."""
    try:
        return session.read.options(snowpark_options).parquet(path).schema
    except Exception:
        return None


def _infer_merged_file_schema(
    session: Session,
    stage_file_groups: list[tuple[str, list[str]]],
    snowpark_options: dict,
) -> StructType | None:
    """Infer a union schema across multiple parquet files using INFER_SCHEMA with FILES.

    For each (stage, files) group, calls INFER_SCHEMA with the FILES parameter so
    Snowflake returns the union of columns across all listed files in a single query.
    Schemas from different stage groups are then merged by column name (first-seen type
    wins for overlapping columns).

    Returns the merged StructType, or None if inference fails for all groups.
    """
    seen: dict[str, StructField] = {}
    ordered_names: list[str] = []

    for stage, files in stage_file_groups:
        if files:
            relative_files = [extract_relative_file_path(path, stage) for path in files]
            opts = {
                **snowpark_options,
                "INFER_SCHEMA_OPTIONS": {"FILES": relative_files},
            }
        else:
            opts = snowpark_options

        try:
            group_schema = session.read.options(opts).parquet(stage).schema
        except Exception:
            logger.debug(
                "INFER_SCHEMA merge: skipping stage group %r (%d files): %s",
                stage,
                len(files) if files else 0,
                files[:3] if files else [],
                exc_info=True,
            )
            continue

        for field in group_schema.fields:
            col_key = _norm(analyzer_utils.unquote_if_quoted(field.name))
            if col_key not in seen:
                seen[col_key] = field
                ordered_names.append(col_key)

    if not seen:
        return None
    return StructType([seen[n] for n in ordered_names])


def _build_parquet_stage_groups(
    paths: list[str],
) -> list[tuple[str, list[str]]]:
    """Build (stage, files) groups for parquet COPY INTO.

    COPY INTO can load from a stage prefix with ``files=[]`` — there is no need
    to expand directory paths to individual files.  This function checks each
    path:

    - **Directory path** (does NOT end with ``.parquet``): use the full path as
      ``stage`` and ``files=[]``.  COPY INTO will load every file under that
      stage prefix that matches the active PATTERN / FILE_FORMAT.
    - **Specific file** (ends with ``.parquet``): extract the stage root and
      pass the file as a relative path in ``files``.  Multiple files from the
      same stage are batched together via :func:`generate_stage_path_groups`.

    This avoids issuing a separate ``LIST`` command (which can be slow and may
    fail for stages with non-standard access patterns) and correctly handles
    the trailing-slash directory paths that the read layer produces for local
    directory reads.
    """
    dir_groups: list[tuple[str, list[str]]] = []
    file_paths: list[str] = []

    for path in paths:
        raw = normalize_stage_path(path)  # strips quotes and trailing slash
        # A trailing slash on the original (pre-normalized) path means the
        # caller identified this as a directory (e.g. local dir named
        # ``data.parquet/``).  Only classify as a single-file path when
        # there is no trailing slash AND the name ends with ``.parquet``.
        is_dir_path = path.strip("'").endswith("/")
        if not is_dir_path and raw.lower().endswith(".parquet"):
            file_paths.append(path)
        else:
            dir_groups.append((path, []))

    result: list[tuple[str, list[str]]] = dir_groups
    if file_paths:
        result = result + generate_stage_path_groups(file_paths)
    return result


def _remap_partition_columns(
    partition_columns: list[str],
    partition_types: dict[str, DataType],
    user_schema: StructType,
) -> tuple[list[str], dict[str, DataType], list[str]]:
    """Map discovered partition column names to user-schema names/types.

    Returns ``(user_names, user_types, file_names)`` where:
    - ``user_names``: partition column names as in the user schema (or discovered).
    - ``user_types``: ``{user_name: DataType}``.
    - ``file_names``: actual directory segment names from METADATA$FILENAME
      (used for SPLIT_PART matching — may differ in case from user schema names).
    """
    user_schema_lookup: dict[str, StructField] = {
        _norm(analyzer_utils.unquote_if_quoted(f.name)): f for f in user_schema.fields
    }
    user_names: list[str] = []
    user_types: dict[str, DataType] = {}
    file_names: list[str] = []

    for col_name in partition_columns:
        raw_file = analyzer_utils.unquote_if_quoted(col_name)
        file_names.append(raw_file)
        user_field = user_schema_lookup.get(_norm(raw_file))
        if user_field is not None:
            raw_user = analyzer_utils.unquote_if_quoted(user_field.name)
            user_names.append(raw_user)
            user_types[raw_user] = user_field.datatype
        else:
            user_names.append(raw_file)
            user_types[raw_file] = partition_types[col_name]

    return user_names, user_types, file_names


def _build_parquet_typed_transformations(
    schema: StructType,
    infer_ntz: bool,
    file_schema: StructType | None,
    partition_col_name_set: set[str],
    session: snowpark.Session,
) -> tuple[list[str], list[Column], StructType]:
    """Build COPY INTO transformations for a parquet schema.

    Returns ``(target_cols, transforms, loading_schema)`` where:

    - ``loading_schema``: *schema* with complex fields using their coerced cast types
      (NTZ timestamps inside complex types replaced by LTZ via ``_transform_complex_type``).

    Per-field logic:
    - Partition column → skipped (added by _load_file_with_copy_into).
    - Complex type → ``$1:"file_col"::{sf_type}`` when the file stores native
      complex types, or ``PARSE_JSON(TO_VARCHAR($1:"file_col"))::{sf_type}``
      when the file schema reports StringType (Snowflake's write path stores
      complex types as JSON strings). With structured TRY_CAST support,
      uses ``TRY_CAST(... AS {sf_type} PERMISSIVE)`` instead of direct cast.
    - StringType → ``TO_VARCHAR($1:"file_col")``.
    - NTZ timestamp + infer_ntz=False → CONVERT_TIMEZONE to LTZ.
    - Other primitives → ``$1:"file_col"::TYPE``.

    Field names from *file_schema* are looked up case-insensitively to handle
    case-differing column names (VARIANT access is case-sensitive).

    For complex columns, ``_transform_complex_type`` strips any embedded SQL
    quotes from field names (``strip_quotes=True``) and replaces TIMESTAMP_NTZ
    with TIMESTAMP_LTZ (PARSE_JSON always produces LTZ from JSON timestamps). Field names
    in the OBJECT cast are produced via ``map_type_to_snowflake_type(structured=True)``
    to match the original JSON keys in the Parquet file.
    """
    from snowflake.snowpark.functions import sql_expr

    session_tz = global_config.spark_sql_session_timeZone
    ltz_type = TimestampType(TimestampTimeZone.LTZ)

    file_type_lookup: dict[str, DataType] = {}
    if file_schema is not None:
        for f in file_schema.fields:
            raw = analyzer_utils.unquote_if_quoted(f.name)
            file_type_lookup[_norm(raw)] = f.datatype

    target_cols: list[str] = []
    transforms: list[Column] = []
    loading_fields: list[StructField] = []

    for field in schema.fields:
        raw_user = analyzer_utils.unquote_if_quoted(field.name)
        if _norm(raw_user) in partition_col_name_set:
            continue

        quoted_name = analyzer_utils.quote_name_without_upper_casing(raw_user)
        target_cols.append(quoted_name)
        dt = field.datatype

        # caseSensitive=false: GET_IGNORE_CASE handles any column casing across
        # all files. caseSensitive=true: use quoted $1:"col" for exact match.
        if not global_config.spark_sql_caseSensitive:
            source_expr = f"GET_IGNORE_CASE($1, '{raw_user}')"
        else:
            source_expr = f'$1:"{raw_user}"'

        if isinstance(dt, (StructType, ArrayType, MapType)):
            # Complex types keep the client-side permissive TRY_CAST: the
            # server-side implicit structured cast is strict and raises on any
            # shape mismatch (missing struct fields, non-vectorized MAP
            # key_value encoding, etc.). PERMISSIVE nulls out mismatches,
            # which is the behavior SCOS needs here.
            variant_dt = _transform_complex_type(
                dt, strip_quotes=True, coerce_ntz_to_ltz=True
            )
            file_dt = file_type_lookup.get(_norm(raw_user))
            if isinstance(file_dt, StringType):
                parsed = sql_expr(f"PARSE_JSON(TO_VARCHAR({source_expr}))")
            else:
                parsed = sql_expr(source_expr)

            if getattr(session, "_has_structured_try_cast", False):
                transforms.append(parsed.try_cast(variant_dt, permissive=True))
            else:
                transforms.append(parsed.cast(variant_dt))
            loading_fields.append(StructField(quoted_name, variant_dt, field.nullable))
        elif isinstance(dt, StringType):
            transforms.append(sql_expr(f"TO_VARCHAR({source_expr})"))
            loading_fields.append(StructField(quoted_name, dt, field.nullable))
        elif (
            isinstance(dt, TimestampType)
            and dt.tz == TimestampTimeZone.NTZ
            and not infer_ntz
        ):
            # Treat NTZ as UTC instant, convert to LTZ (matches Spark behavior)
            expr = (
                f"CONVERT_TIMEZONE('UTC', '{session_tz}', "
                f"{source_expr}::TIMESTAMP_NTZ)::TIMESTAMP_LTZ"
            )
            transforms.append(sql_expr(expr))
            loading_fields.append(StructField(quoted_name, ltz_type, field.nullable))
        else:
            # Parquet scalars come through as VARIANT. When the server supports
            # ENABLE_IMPLICIT_STRUCTURED_CAST_IN_COPY_TRANSFORM, COPY INTO will
            # implicit-cast VARIANT to the target scalar column type, so the
            # explicit ``::TYPE`` cast is redundant and can be skipped.
            # BinaryType is excluded: the server-side implicit cast does not
            # handle VARIANT -> BINARY and fails with a type-mismatch error.
            if getattr(session, "_enable_scos_feature", False) and not isinstance(
                dt, BinaryType
            ):
                transforms.append(sql_expr(source_expr))
            else:
                type_sql = map_type_to_snowflake_type(dt, structured=True)
                transforms.append(sql_expr(f"{source_expr}::{type_sql}"))
            loading_fields.append(StructField(quoted_name, dt, field.nullable))

    return target_cols, transforms, StructType(loading_fields)


def _copy_into_parquet_and_read(
    schema: StructType,
    infer_ntz: bool,
    file_schema: StructType | None,
    partition_col_name_set: set[str],
    reader: snowpark.DataFrameReader,
    session: snowpark.Session,
    temp_table_name: str,
    stage_file_groups: list[tuple[str, list[str]]],
    file_format_options: dict[str, Any],
    partition_columns: list[str] | None,
    partition_types: dict[str, DataType] | None,
    partition_file_col_names: list[str] | None,
    needs_metadata: bool,
) -> DataFrame:
    """Build typed COPY INTO transforms, load all stage groups, and return session.table().

    Common pattern shared by the user-schema and no-schema COPY INTO paths:
    1. ``_build_parquet_typed_transformations`` — derive per-column transforms
       (primitives: ``$1:"col"::TYPE``; complex: conditional ``PARSE_JSON``
       when file stores JSON strings, then cast or ``TRY_CAST(...PERMISSIVE)``;
       NTZ: CONVERT_TIMEZONE to LTZ)
    2. ``_load_file_with_copy_into`` loop — load each (stage, files) group into temp table
    3. ``session.table(temp_table_name)`` — return lazy DataFrame over loaded data

    The first ``_load_file_with_copy_into`` call creates the temp table; subsequent
    calls skip the creation check via ``table_already_exists=True``.
    """
    target_cols, transforms, loading_schema = _build_parquet_typed_transformations(
        schema, infer_ntz, file_schema, partition_col_name_set, session
    )

    for i, (stage, files) in enumerate(stage_file_groups):
        _load_file_with_copy_into(
            reader=reader,
            session=session,
            target=temp_table_name,
            stage_file_paths=files,
            stage=stage,
            schema=loading_schema,
            file_format_options=file_format_options,
            file_format="parquet",
            target_columns=target_cols,
            transformations=transforms,
            partition_columns=partition_columns,
            partition_types=partition_types,
            partition_file_col_names=partition_file_col_names,
            needs_metadata=needs_metadata,
            table_already_exists=(i > 0),
        )

    result_df = session.table(temp_table_name)
    return result_df


def _build_no_schema_result(
    df: DataFrame,
    discovered_types: list[DataType],
    spark_column_names: list[str],
    snowpark_column_names: list[str],
    main_uses_vs: bool,
    can_be_cached: bool,
) -> DataFrameContainer:
    """Apply post-load fixups to a no-schema DataFrame and build a DataFrameContainer.

    For columns where FLATTEN-based schema discovery resolved VARIANT or STRING to a
    complex type (StructType/ArrayType/MapType):

    - **VARIANT → complex**: kept as-is. The COPY INTO transform already cast the column
      to the correct structured type (OBJECT/ARRAY/MAP). SAS serializes structured columns
      via Arrow ``pa.string()`` and uses ``snowpark_column_types`` to declare the target
      Spark type — applying an additional ``::ARRAY/::OBJECT`` cast here would cause
      "Unsupported arrow type string" errors for structured StructType/MapType.
    - **STRING → complex**: wraps the column in ``PARSE_JSON(...)`` to convert the
      JSON-encoded string (written by the Snowflake COPY INTO write path) to VARIANT,
      which SAS can then present as the discovered complex type via ``snowpark_column_types``.
    """
    from snowflake.snowpark.functions import sql_expr

    cast_columns = []
    has_casts = False
    for col_name, field, discovered_type in zip(
        df.columns, df.schema.fields, discovered_types
    ):
        is_variant = isinstance(field.datatype, VariantType)
        is_string = isinstance(field.datatype, StringType)
        is_complex_discovered = (
            (isinstance(discovered_type, StructType) and discovered_type.structured)
            or isinstance(discovered_type, ArrayType)
            or isinstance(discovered_type, MapType)
        )
        if is_complex_discovered and is_variant:
            # Keep VARIANT as-is — PARSE_JSON in COPY INTO transforms already ensures
            # proper JSON structure. SAS serializes VARIANT via Arrow pa.string() and
            # uses snowpark_column_types to declare the target Spark type. Casting to
            # ::ARRAY/::OBJECT would cause "Unsupported arrow type string" for structured
            # StructType/MapType. MapType in VS=false key_value format also skips cast.
            cast_columns.append(df[col_name])
        elif is_complex_discovered and is_string:
            # String → complex: PARSE_JSON to produce VARIANT; no further cast needed.
            raw_name = analyzer_utils.unquote_if_quoted(col_name)
            cast_columns.append(sql_expr(f'PARSE_JSON("{raw_name}")').alias(col_name))
            has_casts = True
        else:
            cast_columns.append(df[col_name])

    result_df = df.select(cast_columns) if has_casts else df
    return DataFrameContainer.create_with_column_mapping(
        dataframe=result_df,
        spark_column_names=spark_column_names,
        snowpark_column_names=snowpark_column_names,
        snowpark_column_types=[emulate_integral_types(t) for t in discovered_types],
        can_be_cached=can_be_cached,
    )


def map_read_parquet(
    rel: relation_proto.Relation,
    schema: StructType | None,
    session: snowpark.Session,
    paths: list[str],
    options: ReaderWriterConfig,
) -> DataFrameContainer:
    """Read Parquet file into a Snowpark DataFrame."""

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
    # Use canonicalized reader config (lowercase keys) so .option("mergeSchema"|"mergeschema"|"MERGESCHEMA", ...)
    # all work; raw protobuf options keep Spark casing and miss lowercased keys.
    merge_schema = str_to_bool(str(options.config.get("mergeschema", "false")))

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

    reader = session.read.options(snowpark_options)
    infer_ntz = get_boolean_session_config_param(
        "spark.sql.parquet.inferTimestampNTZ.enabled"
    )

    # ── Branch A: External table (single path only) ──────────────────────────
    # External tables are created against a single stage path (LOCATION = @stage/prefix)
    # so multiple paths cannot use this branch. When Spark issues a read across multiple
    # partitioned directories or files, it always falls through to Branch B (COPY INTO).
    # This has always been a single-path-only path — multiple paths were never supported.
    if len(paths) == 1 and use_external_table(session, paths[0]):
        ext_reader = add_filename_metadata_to_reader(reader, raw_options)
        df, partition_columns, _ = _read_parquet_with_partitions(
            session, ext_reader, paths[0], schema, snowpark_options, raw_options
        )

        if schema is not None:
            # External table already applied the schema during DDL creation.
            schema_types = [f.datatype for f in df.schema.fields]
            spark_column_names = [
                analyzer_utils.unquote_if_quoted(c) for c in df.columns
            ]
            renamed_df, snowpark_column_names = rename_columns_as_snowflake_standard(
                df, rel.common.plan_id
            )
            return DataFrameContainer.create_with_column_mapping(
                dataframe=renamed_df,
                spark_column_names=spark_column_names,
                snowpark_column_names=snowpark_column_names,
                snowpark_column_types=[
                    emulate_integral_types(dt) for dt in schema_types
                ],
                can_be_cached=False,
            )

        # No schema: infer types via FLATTEN-based schema discovery.
        if not infer_ntz:
            df = _cast_ntz_to_ltz(df)
        spark_column_names = [analyzer_utils.unquote_if_quoted(c) for c in df.columns]
        renamed_df, snowpark_column_names = rename_columns_as_snowflake_standard(
            df, rel.common.plan_id
        )
        rows_to_infer = int(options.config.get("rowstoinferschema", 1000))
        main_uses_vs = str(
            file_format_options.get("USE_VECTORIZED_SCANNER", "true")
        ).lower() in ("true", "1")
        discovered_types = _discover_parquet_column_types(
            df,
            session,
            paths[0],
            file_format_options,
            rows_to_infer,
            snowpark_options,
            main_uses_vs,
        )
        return _build_no_schema_result(
            df=renamed_df,
            discovered_types=discovered_types,
            spark_column_names=spark_column_names,
            snowpark_column_names=snowpark_column_names,
            main_uses_vs=main_uses_vs,
            can_be_cached=False,
        )

    # ── Branch B: COPY INTO ───────────────────────────────────────────────────
    needs_metadata = populate_metadata(raw_options)
    partition_columns, partition_types = _discover_partition_columns(
        session, paths[0], "parquet"
    )
    temp_table_name = random_name_for_temp_object(TempObjectType.TABLE)
    stage_file_groups = _build_parquet_stage_groups(paths)

    if schema is not None:
        # ── User-schema path ──
        # file_schema is needed for two reasons:
        # 1. Conditional PARSE_JSON: Snowflake's Parquet write path stores
        #    complex types (struct/array/map) as JSON strings (StringType in
        #    file). When the file schema reports StringType for a column the
        #    user expects as a complex type, the COPY INTO transform must wrap
        #    the value in PARSE_JSON(TO_VARCHAR(...)) before casting to the
        #    structured type; without it the cast returns NULL.
        # We infer from only the first file (paths[0]) to avoid the overhead
        # of reading schema from every file. Files written by the same
        # Snowflake write path will have a consistent schema, and Spark
        # itself does not infer/merge schemas when a user schema is provided.
        file_schema = _get_parquet_file_schema(session, paths[0], snowpark_options)
        partition_col_name_set = {
            _norm(analyzer_utils.unquote_if_quoted(c)) for c in partition_columns
        }
        user_part_names, user_part_types, file_part_names = _remap_partition_columns(
            partition_columns, partition_types, schema
        )
        df = _copy_into_parquet_and_read(
            schema=schema,
            infer_ntz=infer_ntz,
            file_schema=file_schema,
            partition_col_name_set=partition_col_name_set,
            reader=reader,
            session=session,
            temp_table_name=temp_table_name,
            stage_file_groups=stage_file_groups,
            file_format_options=file_format_options,
            partition_columns=user_part_names if partition_columns else None,
            partition_types=user_part_types if partition_columns else None,
            partition_file_col_names=file_part_names if partition_columns else None,
            needs_metadata=needs_metadata,
        )

        # Build schema_types from the user-provided schema so the Spark client
        # sees exactly the types the user requested, not the internal Snowflake
        # table types (which may differ due to timestamp coercion, etc.).
        # Complex types need quote-stripping because user schemas arrive with
        # SQL-quoted field names (e.g. '"city"') from map_json_schema_to_snowpark,
        # but Snowflake returns unquoted keys in data. Stripping quotes ensures
        # _show_string_spark matches fields by name correctly; without it struct
        # fields display as NULL.
        schema_col_lookup = {
            _norm(analyzer_utils.unquote_if_quoted(f.name)): (
                _transform_complex_type(f.datatype, strip_quotes=True)
                if isinstance(f.datatype, (StructType, ArrayType, MapType))
                else f.datatype
            )
            for f in schema.fields
        }
        # Include discovered partition types so partition columns not in the
        # user schema report their inferred type (e.g. IntegerType) instead
        # of falling back to StringType.
        if user_part_types:
            for pname, ptype in user_part_types.items():
                norm_pname = _norm(pname)
                if norm_pname not in schema_col_lookup:
                    schema_col_lookup[norm_pname] = ptype
        spark_column_names = [analyzer_utils.unquote_if_quoted(c) for c in df.columns]
        schema_types = [
            schema_col_lookup.get(_norm(name), StringType())
            for name in spark_column_names
        ]
        renamed_df, snowpark_column_names = rename_columns_as_snowflake_standard(
            df, rel.common.plan_id
        )
        return DataFrameContainer.create_with_column_mapping(
            dataframe=renamed_df,
            spark_column_names=spark_column_names,
            snowpark_column_names=snowpark_column_names,
            snowpark_column_types=[emulate_integral_types(dt) for dt in schema_types],
            can_be_cached=True,
        )

    # ── No-schema path ──
    # Use the existing sample-based schema discovery, then load via typed COPY INTO.
    rows_to_infer = int(options.config.get("rowstoinferschema", 1000))
    main_uses_vs = str(
        file_format_options.get("USE_VECTORIZED_SCANNER", "true")
    ).lower() in ("true", "1")

    # base_df is lazy — only used for schema fields and sampling.
    base_df = session.read.options(snowpark_options).parquet(paths[0])
    discovered_types = _discover_parquet_column_types(
        base_df,
        session,
        paths[0],
        file_format_options,
        rows_to_infer,
        snowpark_options,
        main_uses_vs,
    )

    # When mergeSchema is enabled and there are multiple paths, use INFER_SCHEMA
    # with FILES to get the union schema across all files. Columns from paths[0]
    # use FLATTEN-discovered types (resolves VARIANT → ARRAY/STRUCT/MAP); columns
    # only in other files use the INFER_SCHEMA type directly (primitives are
    # correct; complex types stay as VariantType — acceptable limitation).
    if merge_schema and len(paths) > 1:
        merged_file_schema = _infer_merged_file_schema(
            session, stage_file_groups, snowpark_options
        )
        if merged_file_schema is not None:
            base_type_lookup = {
                _norm(analyzer_utils.unquote_if_quoted(f.name)): dt
                for f, dt in zip(base_df.schema.fields, discovered_types)
            }
            merged_col_names = []
            merged_types = []
            for field in merged_file_schema.fields:
                col_normed = _norm(analyzer_utils.unquote_if_quoted(field.name))
                merged_col_names.append(analyzer_utils.unquote_if_quoted(field.name))
                merged_types.append(base_type_lookup.get(col_normed, field.datatype))
            effective_file_schema = merged_file_schema
        else:
            merged_col_names = [
                analyzer_utils.unquote_if_quoted(f.name) for f in base_df.schema.fields
            ]
            merged_types = discovered_types
            effective_file_schema = base_df.schema
    else:
        merged_col_names = [
            analyzer_utils.unquote_if_quoted(f.name) for f in base_df.schema.fields
        ]
        merged_types = discovered_types
        effective_file_schema = base_df.schema

    discovered_schema = StructType(
        [
            StructField(analyzer_utils.quote_name_without_upper_casing(name), dt, True)
            for name, dt in zip(merged_col_names, merged_types)
        ]
    )

    no_schema_partition_col_name_set = (
        {_norm(analyzer_utils.unquote_if_quoted(c)) for c in partition_columns}
        if partition_columns
        else set()
    )
    # effective_file_schema is passed for the same reason as the user-schema
    # path: Snowflake writes complex types as JSON strings (StringType in
    # file), so the COPY INTO transform needs to know when to apply
    # PARSE_JSON(TO_VARCHAR(...)) before casting to the structured type.
    df = _copy_into_parquet_and_read(
        schema=discovered_schema,
        infer_ntz=infer_ntz,
        file_schema=effective_file_schema,
        partition_col_name_set=no_schema_partition_col_name_set,
        reader=reader,
        session=session,
        temp_table_name=temp_table_name,
        stage_file_groups=stage_file_groups,
        file_format_options=file_format_options,
        partition_columns=partition_columns if partition_columns else None,
        partition_types=partition_types if partition_columns else None,
        partition_file_col_names=None,
        needs_metadata=needs_metadata,
    )

    # Build type list matching the table column order produced by
    # _load_file_with_copy_into: data columns (partitions excluded) →
    # partition columns → metadata.  Uses the *discovered* types (not the
    # loading types which may differ, e.g. VariantType or LTZ coercion).
    if partition_columns:
        part_norm = {
            _norm(analyzer_utils.unquote_if_quoted(c)) for c in partition_columns
        }
        all_types = [
            dt
            for name, dt in zip(merged_col_names, merged_types)
            if _norm(name) not in part_norm
        ]
        all_types += [partition_types[c] for c in partition_columns]
    else:
        all_types = list(merged_types)
    if needs_metadata:
        all_types.append(StringType())

    spark_column_names = [analyzer_utils.unquote_if_quoted(c) for c in df.columns]
    renamed_df, snowpark_column_names = rename_columns_as_snowflake_standard(
        df, rel.common.plan_id
    )
    return _build_no_schema_result(
        df=renamed_df,
        discovered_types=all_types,
        spark_column_names=spark_column_names,
        snowpark_column_names=snowpark_column_names,
        main_uses_vs=main_uses_vs,
        can_be_cached=True,
    )


def _transform_complex_type(
    dt: DataType,
    *,
    strip_quotes: bool = False,
    coerce_ntz_to_ltz: bool = False,
) -> DataType:
    """Recursive tree walk over complex types applying optional transformations.

    Parameters
    ----------
    strip_quotes:
        Strip embedded SQL quotes from struct field names.  User-provided
        schemas arrive with quoted names (e.g. ``'"city"'``) from
        ``map_json_schema_to_snowpark``.  Stripping produces raw keys
        (e.g. ``city``) matching the dict keys Snowpark Python uses when
        formatting results.  ``_is_column=False`` prevents
        ``ColumnIdentifier`` from uppercasing the name, while
        ``case_sensitive_name`` still produces the correct double-quoted
        SQL identifier for the CAST expression.
    coerce_ntz_to_ltz:
        Replace TIMESTAMP_NTZ with TIMESTAMP_LTZ.  Snowflake's VARIANT/JSON
        path (PARSE_JSON) always produces TIMESTAMP_LTZ regardless of the
        original Parquet timestamp type.  When building the COPY INTO cast
        expression for complex columns, we must use LTZ to match what
        PARSE_JSON actually returns, otherwise the COPY INTO fails with a
        type mismatch error.
    """
    if (
        coerce_ntz_to_ltz
        and isinstance(dt, TimestampType)
        and dt.tz == TimestampTimeZone.NTZ
    ):
        return TimestampType(TimestampTimeZone.LTZ)
    if isinstance(dt, StructType):
        return StructType(
            [
                StructField(
                    analyzer_utils.unquote_if_quoted(f.name)
                    if strip_quotes
                    else f.name,
                    _transform_complex_type(
                        f.datatype,
                        strip_quotes=strip_quotes,
                        coerce_ntz_to_ltz=coerce_ntz_to_ltz,
                    ),
                    f.nullable,
                    _is_column=False,
                )
                for f in dt.fields
            ],
            structured=dt.structured,
        )
    if isinstance(dt, ArrayType):
        return ArrayType(
            _transform_complex_type(
                dt.element_type,
                strip_quotes=strip_quotes,
                coerce_ntz_to_ltz=coerce_ntz_to_ltz,
            ),
            structured=dt.structured,
        )
    if isinstance(dt, MapType):
        return MapType(
            _transform_complex_type(
                dt.key_type,
                strip_quotes=strip_quotes,
                coerce_ntz_to_ltz=coerce_ntz_to_ltz,
            ),
            _transform_complex_type(
                dt.value_type,
                strip_quotes=strip_quotes,
                coerce_ntz_to_ltz=coerce_ntz_to_ltz,
            ),
            structured=dt.structured,
        )
    return dt


def _read_parquet_with_partitions(
    session: Session,
    reader: DataFrameReader,
    path: str,
    schema: StructType | None,
    snowpark_options: dict[str, Any],
    raw_options: dict[str, Any],
) -> tuple[DataFrame, list[str], bool]:
    """
    Reads parquet files and adds partition columns from subdirectories.
    Returns a tuple of (DataFrame, partition_column_names, uses_external_table).
    """

    return _read_partitioned_file_with_partitions(
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
    ntz_fields = [
        field
        for field in df.schema.fields
        if isinstance(field.datatype, TimestampType)
        and field.datatype.tz == TimestampTimeZone.NTZ
    ]
    if ntz_fields:
        df = df.with_columns(
            [f.name for f in ntz_fields],
            [
                convert_tz(lit("UTC"), lit(session_tz), col(f.name)).cast(ltz_type)
                for f in ntz_fields
            ],
        )
    return df


_parquet_file_format_allowed_options = {
    "COMPRESSION",
    "SNAPPY_COMPRESSION",
    "BINARY_AS_TEXT",
    "TRIM_SPACE",
    "USE_LOGICAL_TYPE",
    "REPLACE_INVALID_CHARACTERS",
    "NULL_IF",
}


def _parse_parquet_snowpark_options(snowpark_options: dict[str, Any]) -> dict[str, Any]:
    # SCOS always pins USE_VECTORIZED_SCANNER = TRUE to use the more performant
    # vectorized scanner for Parquet.
    file_format_options: dict[str, Any] = {"USE_VECTORIZED_SCANNER": True}
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
