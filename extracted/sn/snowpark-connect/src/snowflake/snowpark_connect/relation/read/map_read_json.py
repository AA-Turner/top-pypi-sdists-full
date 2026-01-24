#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import concurrent.futures
import copy
import json
import os
import typing
import uuid
from contextlib import suppress
from datetime import datetime

import pyspark.sql.connect.proto.relations_pb2 as relation_proto

from snowflake import snowpark
from snowflake.snowpark._internal.analyzer.analyzer_utils import unquote_if_quoted
from snowflake.snowpark._internal.utils import is_in_stored_procedure
from snowflake.snowpark.row import Row
from snowflake.snowpark.types import (
    ArrayType,
    DataType,
    DateType,
    DecimalType,
    DoubleType,
    LongType,
    MapType,
    NullType,
    StringType,
    StructField,
    StructType,
    TimestampType,
    _FractionalType,
    _IntegralType,
)
from snowflake.snowpark_connect.dataframe_container import DataFrameContainer
from snowflake.snowpark_connect.error.error_codes import ErrorCodes
from snowflake.snowpark_connect.error.error_utils import attach_custom_error_code
from snowflake.snowpark_connect.relation.read.map_read import JsonReaderConfig
from snowflake.snowpark_connect.relation.read.metadata_utils import (
    add_filename_metadata_to_reader,
)
from snowflake.snowpark_connect.relation.read.utils import (
    apply_metadata_exclusion_pattern,
    get_spark_column_names_from_snowpark_columns,
    rename_columns_as_snowflake_standard,
)
from snowflake.snowpark_connect.relation.stage_locator import (
    separate_stage_and_file_from_path,
)
from snowflake.snowpark_connect.type_mapping import (
    cast_to_match_snowpark_type,
    map_simple_types,
    map_type_to_snowflake_type,
    merge_different_types,
)
from snowflake.snowpark_connect.type_support import (
    _integral_types_conversion_enabled,
    emulate_integral_types,
)
from snowflake.snowpark_connect.utils.bz2_file_loader import LINE_CONTENT, load_bz2_file
from snowflake.snowpark_connect.utils.snowpark_connect_logging import logger
from snowflake.snowpark_connect.utils.telemetry import (
    SnowparkConnectNotImplementedError,
)


def _append_node_in_trace_stack(trace_stack: str, node: str) -> str:
    return f"{trace_stack}:{node}"


def _get_max_workers() -> int:
    is_running_in_stored_proc = is_in_stored_procedure()
    if is_running_in_stored_proc:
        # We are having issues in which the read is not giving correct number of rows
        # in storedprocs when the number of workers are more than 1
        # as a temporary fix we will make max_workers to 1
        max_workers = 1
    else:
        # We can have more workers than CPU count, this is an IO-intensive task
        max_workers = min(16, os.cpu_count() * 2)
    return max_workers


def map_read_json(
    rel: relation_proto.Relation,
    schema: StructType | None,
    session: snowpark.Session,
    paths: list[str],
    options: JsonReaderConfig,
) -> DataFrameContainer:
    """
    Read a JSON file into a Snowpark DataFrame.

    [JSON lines](http://jsonlines.org/) file format is supported.

    We leverage the stage that is already created in the map_read function that
    calls this.
    """

    if rel.read.is_streaming is True:
        # TODO: Structured streaming implementation.
        exception = SnowparkConnectNotImplementedError(
            "Streaming is not supported for JSON files."
        )
        attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
        raise exception
    else:
        snowpark_options = options.convert_to_snowpark_args()
        raw_options = rel.read.data_source.options
        snowpark_options["infer_schema"] = True

        rows_to_infer_schema = snowpark_options.pop("rowstoinferschema", 1000)
        dropFieldIfAllNull = snowpark_options.pop("dropfieldifallnull", False)
        use_bulk = snowpark_options.pop("processinbulk", False)
        batch_size = snowpark_options.pop("batchsize", 1000)
        process_single_bz2_file = snowpark_options.pop("bz2fileparallelloading", False)
        split_size_mb = snowpark_options.pop("splitsizemb", 2)
        additional_padding_mb = snowpark_options.pop("additionalpaddingmb", 2)

        apply_metadata_exclusion_pattern(snowpark_options)

        if len(paths) <= 0:
            exception = ValueError(f"No paths provided to read JSON files: {paths}")
            attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
            raise exception
        if process_single_bz2_file:
            df = read_single_bz2_file(
                session,
                paths,
                split_size_mb,
                additional_padding_mb,
                schema,
                rows_to_infer_schema,
                dropFieldIfAllNull,
            )
        else:
            df = read_normal_json_files(
                session,
                paths,
                snowpark_options,
                raw_options,
                rows_to_infer_schema,
                dropFieldIfAllNull,
                use_bulk,
                batch_size,
                schema,
            )

        spark_column_names = get_spark_column_names_from_snowpark_columns(df.columns)

        renamed_df, snowpark_column_names = rename_columns_as_snowflake_standard(
            df, rel.common.plan_id
        )
        return DataFrameContainer.create_with_column_mapping(
            dataframe=renamed_df,
            spark_column_names=spark_column_names,
            snowpark_column_names=snowpark_column_names,
            snowpark_column_types=[
                _emulate_integral_types_for_json(f.datatype) for f in df.schema.fields
            ],
        )


def read_single_bz2_file(
    session: snowpark.Session,
    paths: list[str],
    split_size_mb: int,
    additional_padding_mb: int,
    schema: StructType | None,
    rows_to_infer_schema: int,
    dropFieldIfAllNull: bool,
) -> snowpark.DataFrame:
    # Read the single bz2 file, not support metadata population for now
    stage_name, file_path = separate_stage_and_file_from_path(paths[0])
    df = load_bz2_file(
        session,
        stage_name,
        file_path,
        split_size_mb=split_size_mb,
        additional_padding_mb=additional_padding_mb,
    )
    if len(paths) > 1:
        for p in paths[1:]:
            stage_name, file_path = separate_stage_and_file_from_path(p)
            df = df.union_all(
                load_bz2_file(
                    session,
                    stage_name,
                    file_path,
                    split_size_mb=split_size_mb,
                    additional_padding_mb=additional_padding_mb,
                )
            )
    df = df.select(LINE_CONTENT)

    if schema is None:
        schema = StructType([StructField(LINE_CONTENT, StructType([]))])
        infer_row_counts = 0

        columns_with_valid_contents = set()
        string_nodes_finalized = set[str]()

        for row in df.to_local_iterator():
            infer_row_counts += 1
            if rows_to_infer_schema != -1 and infer_row_counts > rows_to_infer_schema:
                break
            schema = merge_row_schema(
                schema,
                row,
                columns_with_valid_contents,
                string_nodes_finalized,
                dropFieldIfAllNull,
            )

        if dropFieldIfAllNull:
            schema.fields = [
                sf
                for sf in schema.fields
                if unquote_if_quoted(sf.name) in columns_with_valid_contents
            ]

        real_schema = StructType([])
        for sf in schema.fields[0].datatype.fields:
            real_schema.add(sf)
        schema = real_schema

    schema, _ = validate_and_update_schema(schema)

    return construct_dataframe_by_schema_bulk(
        schema,
        df,
        session,
        LINE_CONTENT,
    )


def read_normal_json_files(
    session: snowpark.Session,
    paths: list[str],
    snowpark_options: dict,
    raw_options: dict,
    rows_to_infer_schema: int,
    dropFieldIfAllNull: bool,
    use_bulk: bool,
    batch_size: int,
    schema: StructType | None,
) -> snowpark.DataFrame:
    # Read the normal JSON files, support metadata population
    reader = add_filename_metadata_to_reader(
        session.read.options(snowpark_options), raw_options
    )

    df = reader.json(paths[0])
    if len(paths) > 1:
        # TODO: figure out if this is what Spark does.
        for p in paths[1:]:
            df = df.union_all(
                add_filename_metadata_to_reader(
                    session.read.options(snowpark_options), raw_options
                ).json(p)
            )

    if schema is None:
        schema = copy.deepcopy(df.schema)
        infer_row_counts = 0

        columns_with_valid_contents = set()
        string_nodes_finalized = set[str]()
        for row in df.to_local_iterator():
            infer_row_counts += 1
            if rows_to_infer_schema != -1 and infer_row_counts > rows_to_infer_schema:
                break
            schema = merge_row_schema(
                schema,
                row,
                columns_with_valid_contents,
                string_nodes_finalized,
                dropFieldIfAllNull,
            )

        if dropFieldIfAllNull:
            schema.fields = [
                sf
                for sf in schema.fields
                if unquote_if_quoted(sf.name) in columns_with_valid_contents
            ]

    new_schema, fields_changed = validate_and_update_schema(schema)
    if fields_changed:
        schema = new_schema

    if use_bulk:
        df = construct_dataframe_by_schema_bulk(
            schema,
            df,
            session,
        )
    else:
        df = construct_dataframe_by_schema(
            schema, df.to_local_iterator(), session, snowpark_options, batch_size
        )
    return df


def should_drop_field(field: StructField) -> bool:
    if isinstance(field.datatype, StructType):
        # "a" : {} => drop the field
        if len(field.datatype.fields) == 0:
            return True
    elif (
        isinstance(field.datatype, ArrayType)
        and field.datatype.element_type is not None
        and isinstance(field.datatype.element_type, StructType)
    ):
        if len(field.datatype.element_type.fields) == 0:
            # "a" : [{}] => drop the field
            return True
    return False


# Validate the schema to ensure it is valid for Snowflake
# Handles these cases:
#   1. Drops StructField([])
#   2. Drops ArrayType(StructType([]))
#   3. ArrayType() -> ArrayType(StringType())
def validate_and_update_schema(schema: StructType | None) -> (StructType | None, bool):
    if not isinstance(schema, StructType):
        return schema, False
    new_fields = []
    fields_changed = False
    for sf in schema.fields:
        if should_drop_field(sf):
            fields_changed = True
            continue
        if isinstance(sf.datatype, StructType):
            # If the schema is a struct, validate the child schema
            if len(sf.datatype.fields) == 0:
                # No fields in the struct, drop the field
                fields_changed = True
                continue
            child_field = StructField(sf.name, sf.datatype, sf.nullable)
            # Recursively validate the child schema
            child_field.datatype, child_field_changes = validate_and_update_schema(
                sf.datatype
            )
            if should_drop_field(child_field):
                fields_changed = True
                continue
            new_fields.append(child_field)
            fields_changed = fields_changed or child_field_changes
        elif isinstance(sf.datatype, ArrayType):
            # If the schema is an array, validate the element schema
            if sf.datatype.element_type is not None and isinstance(
                sf.datatype.element_type, StructType
            ):
                # If the element schema is a struct, validate the element schema
                if len(sf.datatype.element_type.fields) == 0:
                    # No fields in the struct, drop the field
                    fields_changed = True
                    continue
                else:
                    # Recursively validate the element schema
                    element_schema, element_field_changes = validate_and_update_schema(
                        sf.datatype.element_type
                    )
                    if element_field_changes:
                        sf.datatype.element_type = element_schema
                        fields_changed = True
                    if should_drop_field(sf):
                        fields_changed = True
                        continue
            elif sf.datatype.element_type is None:
                fields_changed = True
                sf.datatype.element_type = StringType()
            new_fields.append(sf)
        else:
            new_fields.append(sf)
    if fields_changed:
        schema.fields = new_fields
    return schema, fields_changed


def merge_json_schema(
    content: typing.Any,
    schema: StructType | None,
    trace_stack: str,
    string_nodes_finalized: set[str],
    dropFieldIfAllNull: bool = False,
) -> DataType:
    """
    Merge the JSON content's schema into an existing schema structure.

    This function recursively processes JSON content (dict, list, or primitive values) and merges
    its inferred schema with an existing schema if provided. It handles nested structures like
    objects (StructType) and arrays (ArrayType), and can optionally drop fields that are always null.

    Args:
        content: The JSON content to infer schema from. Can be a dict, list, primitive value, or None.
        schema: The existing schema to merge with, or None if inferring from scratch.
        trace_stack: A string representing the current position in the schema hierarchy,
                          used for tracking/debugging nested structures.
        string_nodes_finalized: A set of strings representing the nodes that have been finalized as strings.
        dropFieldIfAllNull: If True, fields that only contain null values will be excluded
                          from the resulting schema. Defaults to False.

    Returns:
        The merged schema as a DataType. Returns NullType if content is None and no existing
        schema is provided. For dicts, returns StructType; for lists, returns ArrayType;
        for primitives, returns the appropriate primitive type (StringType, IntegerType, etc.).
    """
    if content is None:
        if schema is not None:
            return schema
        return NullType()

    if trace_stack in string_nodes_finalized:
        return StringType()

    if isinstance(content, dict):
        additional_schemas = list[StructField]()

        existed_schema = {}
        if schema is not None:
            if schema.type_name() == "struct":
                for sf in schema.fields:
                    existed_schema[sf.name] = sf.datatype
            else:
                string_nodes_finalized.add(trace_stack)
                return StringType()

        for k, v in content.items():
            col_name = f'"{unquote_if_quoted(k)}"'
            existed_data_type = existed_schema.get(col_name, None)
            next_level_schema = merge_json_schema(
                v,
                existed_data_type,
                _append_node_in_trace_stack(trace_stack, col_name),
                string_nodes_finalized,
                dropFieldIfAllNull,
            )

            if not dropFieldIfAllNull or not isinstance(next_level_schema, NullType):
                # Drop field if it's always null
                if col_name in existed_schema:
                    existed_schema[col_name] = next_level_schema
                else:
                    additional_schemas.append(StructField(col_name, next_level_schema))

        current_schema = StructType()
        if schema is not None and schema.type_name() == "struct":
            # Keep the order of columns in the schema
            for sf in schema.fields:
                col_name = f'"{unquote_if_quoted(sf.name)}"'
                if (
                    not dropFieldIfAllNull
                    or existed_schema.get(col_name, NullType()) != NullType()
                ):
                    current_schema.add(
                        StructField(col_name, existed_schema.get(col_name, NullType()))
                    )

        for additional_schema in additional_schemas:
            current_schema.add(additional_schema)

    elif isinstance(content, list):
        # ArrayType(*) need to have element schema inside, it would be NullType() as placeholder and keep updating while enumerating
        inner_schema = NullType()
        next_level_trace_stack = _append_node_in_trace_stack(trace_stack, "$array")

        if schema is not None:
            if schema.type_name() in ("list", "array"):
                inner_schema = schema.element_type
            else:
                string_nodes_finalized.add(trace_stack)
                return StringType()

        if next_level_trace_stack in string_nodes_finalized:
            inner_schema = StringType()
        else:
            if len(content) > 0:
                for v in content:
                    inner_schema = merge_json_schema(
                        v,
                        inner_schema,
                        next_level_trace_stack,
                        string_nodes_finalized,
                        dropFieldIfAllNull,
                    )
                    if isinstance(inner_schema, StringType):
                        string_nodes_finalized.add(next_level_trace_stack)
                        break
            if isinstance(inner_schema, NullType) and dropFieldIfAllNull:
                return NullType()
        current_schema = ArrayType(inner_schema)
    else:
        current_schema = map_simple_types(type(content).__name__)

    if (
        schema is not None
        and schema != NullType()
        and current_schema is not None
        and current_schema != NullType()
        and schema.type_name() != current_schema.type_name()
    ):
        current_schema = merge_different_types(schema, current_schema)

    if isinstance(current_schema, StructType) or isinstance(current_schema, ArrayType):
        current_schema.structured = True

    if isinstance(current_schema, StringType):
        string_nodes_finalized.add(trace_stack)
    return current_schema


def merge_row_schema(
    schema: StructType | None,
    row: Row,
    columns_with_valid_contents: set[str],
    string_nodes_finalized: set[str],
    dropFieldIfAllNull: bool = False,
) -> StructType | NullType:
    """
    Merge the schema inferred from a single row with the existing schema.

    This function updates the schema by examining each row of data and merging
    type information. It handles nested structures (StructType, MapType, ArrayType)
    and attempts to parse JSON strings to infer deeper schema structures.

    Args:
        schema: The current schema to merge with
        row: A single row of data to examine
        columns_with_valid_contents: Set to track columns that have non-null values
        string_nodes_finalized: Set to track nodes that have been finalized as strings
        dropFieldIfAllNull: If True, fields that are always null will be dropped

    Returns:
        The merged schema as a StructType, or NullType if the row is None and no schema exists
    """

    if row is None:
        if schema is not None:
            return schema
        return NullType()

    new_schema = StructType()
    for sf in schema.fields:
        col_name = unquote_if_quoted(sf.name)
        if col_name in string_nodes_finalized:
            columns_with_valid_contents.add(col_name)
        elif isinstance(sf.datatype, (StructType, MapType, StringType)):
            next_level_content = row[col_name]
            next_level_trace_stack = _append_node_in_trace_stack(col_name, col_name)
            if next_level_content is not None:
                with suppress(json.JSONDecodeError):
                    if isinstance(next_level_content, datetime):
                        next_level_content = str(next_level_content)
                    next_level_content = json.loads(next_level_content)
                if isinstance(next_level_content, dict):
                    sf.datatype = merge_json_schema(
                        next_level_content,
                        None
                        if not isinstance(sf.datatype, StructType)
                        else sf.datatype,
                        next_level_trace_stack,
                        string_nodes_finalized,
                        dropFieldIfAllNull,
                    )
                else:
                    sf.datatype = StringType()
                    string_nodes_finalized.add(col_name)
                columns_with_valid_contents.add(col_name)

        elif isinstance(sf.datatype, ArrayType):
            content = row[col_name]
            if content is not None:
                with suppress(Exception):
                    decoded_content = json.loads(content)
                    if isinstance(decoded_content, list):
                        content = decoded_content
                if not isinstance(content, list) or col_name in string_nodes_finalized:
                    sf.datatype = StringType()
                    string_nodes_finalized.add(col_name)
                else:
                    next_level_trace_stack = _append_node_in_trace_stack(
                        col_name, "array"
                    )
                    if next_level_trace_stack in string_nodes_finalized:
                        sf.datatype.element_type = StringType()
                    else:
                        inner_schema = sf.datatype.element_type
                        for v in content:
                            if v is not None:
                                columns_with_valid_contents.add(col_name)
                            inner_schema = merge_json_schema(
                                v,
                                inner_schema,
                                next_level_trace_stack,
                                string_nodes_finalized,
                                dropFieldIfAllNull,
                            )
                            if isinstance(inner_schema, StringType):
                                string_nodes_finalized.add(next_level_trace_stack)
                                break
                        sf.datatype.element_type = inner_schema
        elif isinstance(sf.datatype, TimestampType):
            sf.datatype = StringType()
            columns_with_valid_contents.add(col_name)
            string_nodes_finalized.add(col_name)
        elif row[col_name] is not None:
            columns_with_valid_contents.add(col_name)

        if isinstance(sf.datatype, StructType) or isinstance(sf.datatype, ArrayType):
            sf.datatype.structured = True
        new_schema.add(sf)

    return new_schema


def insert_data_chunk(
    session: snowpark.Session,
    data: list[Row],
    schema: StructType,
    table_name: str,
) -> None:
    df = session.create_dataframe(
        data=data,
        schema=schema,
    )

    df.write.mode("append").save_as_table(
        table_name, table_type="temp", table_exists=True
    )


def construct_dataframe_by_schema_bulk(
    schema: StructType,
    df_source: snowpark.DataFrame,
    session: snowpark.Session,
    root_column_name: str = None,
) -> snowpark.DataFrame:
    """
    Bulk process JSON data.
    """
    # Step 1: Create temporary view from source DataFrame
    source_view = f"__sas_json_source_view_{uuid.uuid4().hex}"
    df_source.create_or_replace_temp_view(source_view)

    # Step 2: Create target table with correct schema
    target_table = f"__sas_json_target_{uuid.uuid4().hex}"

    create_ddl = _generate_create_table_ddl(target_table, schema)
    session.sql(create_ddl).collect()

    # Step 3: Generate SELECT with CAST expressions
    select_exprs = []
    for field in schema.fields:
        # Generate Snowflake type signature for casting
        sf_type_sig = _generate_snowflake_type_signature(field.datatype)

        # Use _generate_json_path_reference to handle NULL values for missing/empty fields
        if root_column_name is not None:
            json_path_expr = _generate_json_path_reference(
                f"{root_column_name}:{field.name}", field.datatype
            )
        else:
            json_path_expr = _generate_json_path_reference(
                field.name, field.datatype, is_root=True
            )
        if isinstance(field.datatype, StringType):
            select_exprs.append(f"TO_VARCHAR({json_path_expr}) AS {field.name}")
        elif not isinstance(field.datatype, (StructType, ArrayType, MapType)):
            select_exprs.append(
                f"TRY_CAST(TO_VARCHAR({json_path_expr}) AS {sf_type_sig}) AS {field.name}"
            )
        else:
            select_exprs.append(f"{json_path_expr}::{sf_type_sig} AS {field.name}")

    # Step 4: Apply select expression and copy into target table
    sql_query = f"""
        INSERT INTO {target_table}
        (
            SELECT {', '.join(select_exprs)}
            FROM {source_view}
        )
    """

    session.sql(sql_query).collect()

    return session.table(target_table)


def _generate_create_table_ddl(table_name: str, schema: StructType) -> str:
    """
    Generate CREATE TABLE DDL with typed columns for bulk JSON processing.

    Example output:
      CREATE TEMP TABLE my_table (
        "id" INT,
        "metadata" OBJECT(field1 INT, field2 VARCHAR),
        "items" ARRAY(INT)
      )
    """
    columns_ddl = []
    for field in schema.fields:
        col_type_sig = _generate_snowflake_type_signature(field.datatype)
        columns_ddl.append(f"{field.name} {col_type_sig}")

    return f"CREATE TEMP TABLE {table_name} ({', '.join(columns_ddl)})"


def _generate_snowflake_type_signature(data_type: DataType) -> str:
    """
    Generate Snowflake type signature for CAST.

    Examples:
      IntegerType() → "INT"
      StructType([...]) → "OBJECT(field1 INT, field2 VARCHAR, ...)"
      ArrayType(IntegerType()) → "ARRAY(INT)"

    Args:
        data_type: The DataType to convert
    """
    if isinstance(data_type, StructType):
        # OBJECT(field1 type1, field2 type2, ...)
        field_sigs = []
        for field in data_type.fields:
            field_type_sig = _generate_snowflake_type_signature(
                field.datatype,
            )
            field_sigs.append(f"{field.name} {field_type_sig}")
        return f"OBJECT({', '.join(field_sigs)})"

    elif isinstance(data_type, ArrayType):
        # ARRAY(element_type)
        element_sig = _generate_snowflake_type_signature(
            data_type.element_type,
        )
        return f"ARRAY({element_sig})"

    elif isinstance(data_type, MapType):
        # MAP(key_type, value_type)
        key_sig = _generate_snowflake_type_signature(
            data_type.key_type,
        )
        value_sig = _generate_snowflake_type_signature(
            data_type.value_type,
        )
        return f"MAP({key_sig}, {value_sig})"

    else:
        # Simple types - use existing mapping
        return map_type_to_snowflake_type(data_type)


def _generate_json_path_reference(
    json_path: str, data_type: DataType, is_root: bool = False
) -> str:
    """
    Generate a JSON path reference with appropriate casting for nested fields.

    This function recursively builds OBJECT_CONSTRUCT_KEEP_NULL expressions for
    nested structures, with proper casting for arrays and maps.

    Examples:
        Simple field: "field_name:a.b.field"
        Integer field: "field_name:a.b.field::INT"
        Array field: "field_name:a.b.tags::ARRAY(TEXT)"
        Map field: "field_name:a.b.metadata::MAP(TEXT, TEXT)"
        Nested struct: "OBJECT_CONSTRUCT_KEEP_NULL('field1', field_name:a.b.field1, ...)"

    Args:
        json_path: The JSON path to the field (e.g., "field_name:a.b.field")
        data_type: The DataType of the field
    """

    variant_suffix = "::VARIANT" if not is_root else ""
    if isinstance(data_type, StructType):
        # Build OBJECT_CONSTRUCT_KEEP_NULL for nested structures
        field_exprs = []
        for field in data_type.fields:
            field_name = unquote_if_quoted(field.name)
            nested_col_name = json_path + (":" if is_root else ".") + field.name
            nested_expr = _generate_json_path_reference(nested_col_name, field.datatype)
            field_exprs.append(f"'{field_name}', {nested_expr}")

        return f"OBJECT_CONSTRUCT_KEEP_NULL({', '.join(field_exprs)}){variant_suffix}"

    elif isinstance(data_type, ArrayType):
        # Cast to typed array
        element_type_sig = _generate_snowflake_type_signature(data_type.element_type)
        return f"{json_path}::ARRAY({element_type_sig}){variant_suffix}"

    elif isinstance(data_type, MapType):
        # Cast to typed map
        key_type_sig = _generate_snowflake_type_signature(data_type.key_type)
        value_type_sig = _generate_snowflake_type_signature(data_type.value_type)
        return f"{json_path}::MAP({key_type_sig}, {value_type_sig}){variant_suffix}"

    elif isinstance(data_type, StringType):
        return f"TO_VARCHAR({json_path})"

    else:
        return (
            json_path
            if is_root
            else f"TRY_CAST(TO_VARCHAR({json_path}) AS {_generate_snowflake_type_signature(data_type)})"
        )


def construct_dataframe_by_schema(
    schema: StructType,
    rows: typing.Iterator[Row],
    session: snowpark.Session,
    snowpark_options: dict,
    batch_size: int = 1000,
) -> snowpark.DataFrame:
    table_name = "__sas_json_read_temp_" + uuid.uuid4().hex

    current_data = []
    progress = 0

    # Initialize the temp table
    session.create_dataframe([], schema=schema).write.mode("append").save_as_table(
        table_name, table_type="temp", table_exists=False
    )

    with concurrent.futures.ThreadPoolExecutor(max_workers=_get_max_workers()) as exc:
        for row in rows:
            current_data.append(construct_row_by_schema(row, schema, snowpark_options))
            if len(current_data) >= batch_size:
                progress += len(current_data)
                exc.submit(
                    insert_data_chunk,
                    session,
                    copy.deepcopy(current_data),
                    schema,
                    table_name,
                )

                logger.info(f"JSON reader: finished processing {progress} rows")
                current_data.clear()

        if len(current_data) > 0:
            progress += len(current_data)
            exc.submit(
                insert_data_chunk,
                session,
                copy.deepcopy(current_data),
                schema,
                table_name,
            )
            logger.info(f"JSON reader: finished processing {progress} rows")

    return session.table(table_name)


def construct_row_by_schema(
    content: typing.Any, schema: DataType, snowpark_options: dict
) -> None | DataType:
    if content is None:
        return None
    elif isinstance(schema, StructType):
        result = {}
        if isinstance(content, (dict, Row)):
            for sf in schema.fields:
                col_name = unquote_if_quoted(sf.name)
                quoted_col_name = (
                    f'"{col_name}"' if isinstance(content, Row) else col_name
                )
                result[quoted_col_name] = construct_row_by_schema(
                    (content.as_dict() if isinstance(content, Row) else content).get(
                        col_name, None
                    ),
                    sf.datatype,
                    snowpark_options,
                )
        elif isinstance(content, str):
            with suppress(json.JSONDecodeError):
                decoded_content = json.loads(content)
                if isinstance(decoded_content, dict):
                    content = decoded_content
            for sf in schema.fields:
                col_name = unquote_if_quoted(sf.name)
                result[col_name] = construct_row_by_schema(
                    content.get(col_name, None), sf.datatype, snowpark_options
                )
        else:
            exception = SnowparkConnectNotImplementedError(
                f"JSON construct {str(content)} to StructType failed"
            )
            attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
            raise exception
        return result
    elif isinstance(schema, ArrayType):
        result = []
        inner_schema = schema.element_type
        if isinstance(content, str):
            content = json.loads(content)
        if inner_schema is not None:
            for ele in content:
                result.append(
                    construct_row_by_schema(ele, inner_schema, snowpark_options)
                )
        return result
    elif isinstance(schema, DateType):
        return cast_to_match_snowpark_type(
            schema, content, snowpark_options.get("DATE_FORMAT")
        )

    return cast_to_match_snowpark_type(schema, content)


def _emulate_integral_types_for_json(t: DataType) -> DataType:
    """
    JSON type handling to match OSS Spark JSON schema inference.

    After applying emulate_integral_types, converts to Spark JSON types:
    - All integral types (ByteType, ShortType, IntegerType, LongType) -> LongType
    - DecimalType with scale > 0 -> DoubleType
    - DecimalType with scale = 0 -> LongType (if precision <= 18) or DecimalType
    - FloatType, DoubleType -> DoubleType
    """
    if not _integral_types_conversion_enabled:
        return t

    # First apply standard integral type conversion
    t = emulate_integral_types(t)

    if isinstance(t, _IntegralType):
        # All integral types -> LongType for JSON
        return LongType()

    elif isinstance(t, DecimalType):
        # DecimalType with scale > 0 means it has decimal places -> DoubleType
        if t.scale > 0:
            return DoubleType()
        # DecimalType with scale = 0 is integral
        if t.precision > 18:
            # Too big for long, keep as DecimalType
            return DecimalType(t.precision, 0)
        else:
            return LongType()

    elif isinstance(t, _FractionalType):
        # FloatType, DoubleType -> DoubleType
        return DoubleType()

    return t
