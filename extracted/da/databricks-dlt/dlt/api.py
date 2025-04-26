import warnings
from typing import Callable, Collection, Dict, List, Optional, Union

from pyspark.sql import Column, DataFrame
from pyspark.sql.types import StructType

from .helpers import __outer

DLT_DECORATOR_RETURN = "_dlt_get_dataset"
DLT_HOOK_DECORATOR_RETURN = "_dlt_event_hook"
DLT_DECORATOR_FUNCTION_NAMES = [DLT_HOOK_DECORATOR_RETURN, DLT_DECORATOR_RETURN]

LOCAL_EXECUTION_MODE = False


def enable_local_execution():
    global LOCAL_EXECUTION_MODE
    LOCAL_EXECUTION_MODE = True


def __local_execution_disabled():
    error_msg = "This is a stub that only contains the interfaces to Delta Live Tables. \
Delta Live Tables pipelines cannot be run locally. To learn more,  see \
https://docs.databricks.com/en/delta-live-tables/develop-locally.html. \
If you would like to run your code for testing purposes, you can switch this error message off by calling \
enable_local_execution() before running your pipeline code."

    if LOCAL_EXECUTION_MODE:
        warnings.warn(error_msg)
    else:
        raise Exception(error_msg)


def append_flow(
    name: Optional[str] = None,
    target: Optional[str] = None,
    comment: Optional[str] = None,
    spark_conf: Optional[Dict[str, str]] = None,
    once: bool = False,
) -> Callable[[Callable[[], DataFrame]], None]:
    """
    Return a decorator on a query function to define a flow in a pipeline.

    :param name: The name of the flow. If unspecified, the query function's name will be used.
    :param target: The name of the dataset this flow writes to. Must be specified.
    :param comment: Description of the flow. If unspecified, the dataset's comment will be used.
    :param spark_conf: A dict where the keys are the conf names and the values are the conf values. \
        These confs will be set when the flow is executed; they can override confs set for the \
        destination, for the pipeline, or on the cluster.
    :param once: If True, indicates this flow should run only once. (It will be rerun upon a full \
        refresh operation.)
    """
    __local_execution_disabled()
    return __outer


def table(
    query_function: Optional[Callable[..., DataFrame]] = None,
    name: Optional[str] = None,
    comment: Optional[str] = None,
    spark_conf: Optional[Dict[str, str]] = None,
    table_properties: Optional[Dict[str, str]] = None,
    partition_cols: Optional[List[str]] = None,
    path: Optional[str] = None,
    schema: Optional[Union[StructType, str]] = None,
    temporary: bool = False,
    cluster_by: Optional[List[str]] = None,
    row_filter: Optional[str] = None,
) -> Callable[[Callable[[], DataFrame]], Callable[[], DataFrame]]:
    """
    (Return a) decorator to define a table in the pipeline and mark a function as the table's query
    function.

    @table can be used with or without parameters. If called without parameters, Python will
    implicitly pass the decorated query function as the query_function param. If called with
    parameters, @table will return a decorator that is applied on the decorated query function.

    :param query_function: The table's query function. This parameter should not be explicitly \
        passed by users. This is passed implicitly by Python if the decorator is called without \
        parameters.
    :param name: The name of the dataset. If unspecified, the query function's name will be used.
    :param comment: Description of the dataset.
    :param spark_conf: A dict where the keys are the conf names and the values are the conf values. \
        These confs will be set when the query for the dataset is executed and they can override \
        confs set for the pipeline or on the cluster.
    :param table_properties: A dict where the keys are the property names and the values are the \
        property values. These properties will be set on the table.
    :param partition_cols: A list containing the column names of the partition columns.
    :param path: The path to the table.
    :param schema: Explicit Spark SQL schema to materialize this table with. Supports either a \
        Pyspark StructType or a SQL DDL string, such as "a INT, b STRING".
    :param temporary Specifies that this table should be temporary. Temporary tables are excluded \
        from being added to the metastore even if a pipeline is configured to add its tables to it.
    :param cluster_by: A list containing the column names of the clustering columns.
    :param row_filter: A row filter SQL clause that filters the rows in the table.
    """
    __local_execution_disabled()
    # For a pipeline that looks like this,
    # @create_table(name="tbl")
    # def query_fn():
    #   return ...
    # Python calls create_table(name="tbl")(query_fn). However, we have to also handle the case
    # when @create_table doesn't take any arguments. If a user's pipeline looks like this,
    # @create_table
    # def query_fn():
    #   return ...
    # Python will call create_table(query_fn), so we must call outer and pass query_fn to make it
    # behave the same as the case where the user does specify args.
    if query_function is not None:
        if callable(query_function):
            return __outer(query_function)
        else:
            raise RuntimeError(
                "The first positional argument passed to @table must be callable. Either add @table"
                " with no parameters to your query function, or pass options to @table using"
                " keyword arguments (e.g. @table(name='table_a'))."
            )

    else:
        return __outer


def view(
    query_function: Optional[Callable[..., DataFrame]] = None,
    name: Optional[str] = None,
    comment: Optional[str] = None,
    spark_conf: Optional[Dict[str, str]] = None,
) -> Union[Callable[[Callable[[], DataFrame]], Callable[[], DataFrame]]]:
    """
    (Return a) decorator to define a view in the pipeline and mark a function as the view's query
    function.

    @view can be used with or without parameters. If called without parameters, Python will
    implicitly pass the decorated query function as the query_function param. If called with
    parameters, @view will return a decorator that is applied on the decorated query function.

    :param query_function: The view's query function. This parameter should not be explicitly \
        passed by users. This is passed implicitly by Python if the decorator is called without \
        parameters.
    :param name: The name of the dataset. If unspecified, the query function's name will be used.
    :param comment: Description of the dataset.
    :param spark_conf: A dict where the keys are the conf names and the values are the conf values. \
        These confs will be set when the query for the dataset is executed and they can override \
        confs set for the pipeline or on the cluster.
    """
    __local_execution_disabled()
    # This handles the @create_view case with no args. See similar comment above in create_table.
    if query_function is not None:
        if callable(query_function):
            return __outer(query_function)
        else:
            raise RuntimeError(
                "The first positional argument passed to @view must be callable. Either add @view"
                "with no parameters to your query function, or pass options to @view using keyword"
                "arguments (e.g. @view(name='view_a'))."
            )

    else:
        return __outer


def on_event_hook(
    user_event_hook_fn: Optional[Callable] = None,
    max_allowable_consecutive_failures: Optional[int] = None,
):
    __local_execution_disabled()
    if user_event_hook_fn is not None:
        if callable(user_event_hook_fn):
            # Case where user calls @on_event_hook, python will pass along the user event hook to us.
            # While not intended/supported, if the user directly passes in a hook it will be handled here too, which may cause undesirable behavior.
            return __outer(user_event_hook_fn)
        else:
            # Case where user doesn't use named arguments for the other parameters, ex. @on_event_hook(5).
            raise RuntimeError(
                "The first positional argument passed to @on_event_hook must be callable. Either add @on_event_hook"
                " with no parameters to your event hook, or pass options to @on_event_hook using"
                " keyword arguments (e.g. @on_event_hook(max_allowable_consecutive_failures=5))."
            )
    else:
        # Case where user calls @on_event_hook() or @on_event_hook(max_allowable_consecutive_failures = some_integer).
        return __outer


def expect_all(
    expectations: Dict[str, Union[str, Column]],
) -> Callable[[Callable[[], DataFrame]], Callable[[], DataFrame]]:
    """
    Adds multiple unenforced expectations on the contents of this dataset. Unexpected records (i.e
    those where the invariant does not evaluate to true) will be counted, but allowed into the
    dataset.

    :param expectations: Dictionary where the key is the expectation name and the value is the \
        invariant (string or Column) that will be checked on the dataset.
    """
    __local_execution_disabled()
    return __outer


def expect_all_or_fail(
    expectations: Dict[str, Union[str, Column]],
) -> Callable[[Callable[[], DataFrame]], Callable[[], DataFrame]]:
    """
    Adds multiple fail expectations on the contents of this dataset. Unexpected records (i.e those
    where the invariant does not evaluate to true) will cause processing for this and any dependent
    datasets to stop until the problem is addressed.

    :param expectations: Dictionary where the key is the expectation name and the value is the \
        invariant (string or Column) that will be checked on the dataset.
    """
    __local_execution_disabled()
    return __outer


def expect_all_or_drop(
    expectations: Dict[str, Union[str, Column]],
) -> Callable[[Callable[[], DataFrame]], Callable[[], DataFrame]]:
    """
    Adds multiple drop expectations on the contents of this dataset. Unexpected records (i.e those
    where the invariant does not evaluate to true) will be counted and dropped.

    :param expectations: Dictionary where the key is the expectation name and the value is the \
        invariant (string or Column) that will be checked on the dataset.
    """
    __local_execution_disabled()
    return __outer


def expect(
    name: str, inv: Union[str, Column]
) -> Callable[[Callable[[], DataFrame]], Callable[[], DataFrame]]:
    """
    Adds an unenforced expectation on the contents of this dataset. Unexpected records (i.e those
    where the invariant does not evaluate to true) will be counted, but allowed into the dataset.

    :param name: The name of the expectation
    :param inv: The invariant (string or Column) that will be checked on the dataset
    """
    __local_execution_disabled()

    return __outer


def expect_or_fail(
    name: str, inv: Union[str, Column]
) -> Callable[[Callable[[], DataFrame]], Callable[[], DataFrame]]:
    """
    Adds a fail expectation on the contents of this dataset. Unexpected records (i.e those where
    the invariant does not evaluate to true) will cause processing for this and any dependent
    datasets to stop until the problem is addressed.

    :param name: The name of the expectation
    :param inv: The invariant (string or Column) that will be checked on the dataset
    """
    __local_execution_disabled()
    return __outer


def expect_or_drop(
    name: str, inv: Union[str, Column]
) -> Callable[[Callable[[], DataFrame]], Callable[[], DataFrame]]:
    """
    Adds a drop expectation on the contents of this dataset. Unexpected records (i.e those where
    the invariant does not evaluate to true) will be counted and dropped.

    :param name: The name of the expectation
    :param inv: The invariant (string or Column) that will be checked on the dataset
    """
    __local_execution_disabled()
    return __outer


def read(name: str) -> DataFrame:
    """
    Reference another graph component as a complete input.

    :param name: The name of the dataset to read from.
    """
    __local_execution_disabled()


def read_stream(name: str) -> DataFrame:
    """
    Reference another graph component as an incremental input.

    :param name: The name of the dataset to read from.
    """
    __local_execution_disabled()


def create_streaming_table(
    name: str,
    comment: Optional[str] = None,
    spark_conf: Optional[Dict[str, str]] = None,
    table_properties: Optional[Dict[str, str]] = None,
    partition_cols: Optional[Collection[str]] = None,
    path: Optional[str] = None,
    schema: Optional[Union[StructType, str]] = None,
    expect_all: Optional[Dict[str, Union[str, Column]]] = None,
    expect_all_or_drop: Optional[Dict[str, Union[str, Column]]] = None,
    expect_all_or_fail: Optional[Dict[str, Union[str, Column]]] = None,
    cluster_by: Optional[List[str]] = None,
    row_filter: Optional[str] = None,
) -> None:
    """
    Creates a target table for Apply Changes (Change Data Capture ingestion). Currently,
    expectations are not supported on the target table.

    Example:
    create_streaming_table("target")

    :param name: The name of the table.
    :param comment: Description of the table.
    :param spark_conf: A dict where the keys are the conf names and the values are the conf values. \
        These confs will be set when the query for the dataset is executed and they can override \
        confs set for the pipeline or on the cluster.
    :param table_properties: A dict where the keys are the property names and the values are the \
        property values. These properties will be set on the table.
    :param partition_cols: A list containing the column names of the partition columns.
    :param path: The path to the table.
    :param schema Explicit Spark SQL schema to materialize this table with. Supports either a \
        Pyspark StructType or a SQL DDL string, such as "a INT, b STRING".
    :param expect_all: A dict where the keys are the expectation names and the values are the \
        invariants (strings or Columns) that will be checked on the dataset.
    :param expect_all_or_drop: A dict where the keys are the expectation names and the values are \
        the invariants (strings or Columns) that will be checked on the dataset. Unexpected records \
        (i.e those where the invariant does not evaluate to true) will be counted and dropped.
    :param expect_all_or_fail: A dict where the keys are the expectation names and the values are \
        the invariants (strings or Columns) that will be checked on the dataset. Unexpected records \
        (i.e those where the invariant does not evaluate to true) will cause processing for this and \
        any dependent datasets to stop until the problem is addressed.
    :param cluster_by: A list containing the column names of the clustering columns.
    :param row_filter: A row filter SQL clause that filters the rows in the table.

    """
    __local_execution_disabled()


def apply_changes(
    target: str,
    source: str,
    keys: Union[List[str], List[Column]],
    sequence_by: Union[str, Column],
    where: Optional[Union[str, Column]] = None,
    ignore_null_updates: Optional[bool] = None,
    apply_as_deletes: Optional[Union[str, Column]] = None,
    apply_as_truncates: Optional[Union[str, Column]] = None,
    column_list: Optional[Union[List[str], List[Column]]] = None,
    except_column_list: Optional[Union[List[str], List[Column]]] = None,
    stored_as_scd_type: Union[str, int] = "1",
    track_history_column_list: Optional[Union[List[str], List[Column]]] = None,
    track_history_except_column_list: Optional[Union[List[str], List[Column]]] = None,
    flow_name: Optional[str] = None,
    once: bool = False,
    ignore_null_updates_column_list: Optional[Union[List[str], List[Column]]] = None,
    ignore_null_updates_except_column_list: Optional[Union[List[str], List[Column]]] = None,
    columns_to_update: Optional[Union[str, Column]] = None,
) -> None:
    """
    Apply changes into the target table from the Change Data Capture (CDC) source. Target table must
    have already been created using create_target_table function. Only one of column_list and
    except_column_list can be specified. Also only one of track_history_column_list and
    track_history_except_column_list can be specified.

    Example:
    apply_changes(
      target = "target",
      source = "source",
      keys = ["key"],
      sequence_by = "sequence_expr",
      ignore_null_updates = True,
      column_list = ["key", "value"],
      stored_as_scd_type = "1",
      track_history_column_list = ["value"]
    )

    Note that for keys, sequence_by, column_list, except_column_list, track_history_column_list,
    track_history_except_column_list the arguments have to be column identifiers without qualifiers,
    e.g. they cannot be col("sourceTable.keyId").

    :param target: The name of the target table that receives the Apply Changes.
    :param source: The name of the CDC source to stream from.
    :param keys: The column or combination of columns that uniquely identify a row in the source \
        data. This is used to identify which CDC events apply to specific records in the target \
        table. These keys also identify records in the target table, e.g., if there exists a record \
        for given keys and the CDC source has an UPSERT operation for the same keys, we will update \
        the existing record. At least one key must be provided. This should be a list of column \
        identifiers without qualifiers, expressed as either Python strings or Pyspark Columns.
    :param sequence_by: An expression that we use to order the source data. This can be expressed \
        as either a Python string or Pyspark Expression.
    :param where: An optional condition applied to both source and target during the execution \
        process to trigger optimizations such as partition pruning. This condition cannot be used to \
        drop source rows; that is, all CDC rows in the source must satisfy this condition, or an \
        error is thrown.
    :param ignore_null_updates: Whether to ignore the null value in the source data. For example, \
        consider the case where we have an UPSERT in the source data with null value for a column, \
        and this same column has non-null value in the target. If ignore_null_updates is true, \
        merging this UPSERT will not override the existing value for this column; If false, \
        merging will override the value for this column to null.
    :param apply_as_deletes: Delete condition for the merged operation. This should be a string of \
        expression e.g. "operation = 'DELETE'"
    :param apply_as_truncates: Truncate condition for the merged operation. This should be a string \
        expression e.g. "operation = 'TRUNCATE'"
    :param column_list: Columns that will be included in the output table. This should be a list \
        of column identifiers without qualifiers, expressed as either Python strings or Pyspark \
        Column. Only one of column_list and except_column_list can be specified.
    :param except_column_list: Columns that will be excluded in the output table. This should be a \
        list of column identifiers without qualifiers, expressed as either Python strings or Pyspark \
        Column. Only one of column_list and except_column_list can be specified. When this is \
        specified, all columns in the dataframe of the target table except those in this list will \
        be in the output table.
    :param stored_as_scd_type: Specify the SCD Type for output format. 1 for SCD Type 1 and 2 for \
        SCD Type 2. This parameter can either be an integer or string. Default value is 1.
    :param track_history_column_list: Columns that will be tracked for change history. \
        This should be a list of column identifiers without qualifiers, expressed as either Python \
        strings or Pyspark Column. Only one of track_history_column_list and \
        track_history_except_column_list can be specified.
    :param track_history_except_column_list: Columns that will not be tracked for change history. \
        Those columns will reflect the values that were seen before the next update to any of the \
        tracked columns. \
        This should be a list of column identifiers without qualifiers, expressed as either Python \
        strings or Pyspark Column. Only one of track_history_column_list and \
        track_history_except_column_list can be specified.
    :param flow_name: The name of the flow for this apply_changes command. When unspecified this will build a \
           "default flow" with name equal to the target name.
    :param ignore_null_updates_column_list: subset of columns to ignore null in updates.
    :param ignore_null_updates_except_column_list: subset of columns excluded from ignoring null in updates.
    :param columns_to_update: Column indicating which user columns to update or ignore.
    """
    __local_execution_disabled()


def apply_changes_from_snapshot(
    target: str,
    source: str = None,
    keys: Union[List[str], List[Column]] = None,
    stored_as_scd_type: Union[str, int] = None,
    snapshot_and_version: Callable = None,
    track_history_column_list: Optional[Union[List[str], List[Column]]] = None,
    track_history_except_column_list: Optional[Union[List[str], List[Column]]] = None,
) -> None:
    """
    APPLY CHANGES into the target table from a sequence of snapshots. Target table must
    have already been created using create_target_table function. Only one of
    track_history_column_list and track_history_except_column_list can be specified with SCD TYPE 2.

    Example:
    def next_snapshot_and_version(latest_snapshot_version):
     version = latest_snapshot_version + 1
     file_name = "dir_path/filename_" + version + ".<file_format>"
     return (spark.read.load(file_name) if(exist(file_name)) else None, version)

    apply_changes_from_snapshot(
      target = "target",
      track_history_column_list = next_snapshot_and_version,
      keys = ["key"],
      stored_as_scd_type = "1",
      track_history_column_list = ["value"]
    )

    :param target: The name of the target table that receives the APPLY CHANGES.
    :param snapshot_and_version: The lambda function that takes latest process snapshot version as \
        an argument and optionally return the tuple of new snapshot DF to be processed and the \
        version of the snapshot. Each time the apply_changes_from_snapshot pipeline get triggered, \
        we will keep execute `snapshot_and_version` to get the next new snapshot DF to process until \
        there is no snapshot DF returned from the function.
    :param keys: The column or combination of columns that uniquely identify a row in the source \
        data. This is used to identify which CDC events apply to specific records in the target \
        table. These keys also identify records in the target table, e.g., if there exists a record \
        for given keys and the CDC source has an UPSERT operation for the same keys, we will update \
        the existing record. At least one key must be provided. This should be a list of column \
        identifiers without qualifiers, expressed as either Python strings or Pyspark Columns.
    :param stored_as_scd_type: Specify the SCD Type for output format. 1 for SCD Type 1 and 2 for \
        SCD Type 2. This parameter can either be an integer or string. Default value is 1.
    :param track_history_column_list: Columns that will be tracked for change history. \
        This should be a list of column identifiers without qualifiers, expressed as either Python \
        strings or Pyspark Column. Only one of track_history_column_list and \
        track_history_except_column_list can be specified.
    :param track_history_except_column_list: Columns that will not be tracked for change history. \
        Those columns will reflect the values that were seen before the next update to any of the \
        tracked columns. \
        This should be a list of column identifiers without qualifiers, expressed as either Python \
        strings or Pyspark Column. Only one of track_history_column_list and \
        track_history_except_column_list can be specified.
    """
    __local_execution_disabled()
