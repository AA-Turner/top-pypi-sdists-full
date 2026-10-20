import json
import os
import time

from typing import Optional

from fivetran_connector_sdk_common.constants import (
    JAVA_LONG_MAX_VALUE, TABLES, TABLES_COLUMNS_TYPES, FIVETRAN_FILE_PATH_COLUMN
)
from fivetran_connector_sdk.constants import CAPTURE_PERFORMANCE_METRICS_ENABLED
from fivetran_connector_sdk.file_upload import FileUpload, file_upload_chunks, validate_file_upload_if_present
from fivetran_connector_sdk_common.helpers import (
    _validate_table_name, _validate_message, _validate_trace, print_library_log,
    _validate_schema,
)
from fivetran_connector_sdk_common.logger import Logging
from fivetran_connector_sdk.protos import connector_sdk_pb2, common_pb2
from fivetran_connector_sdk.operation_stream import _OperationStream
from fivetran_connector_sdk.type_coercion import (
    _encode_row_data, _PFX_SCALAR,
    _parse_utc_datetime_str, _parse_naive_datetime_str, _parse_naive_date_str,
)

UNSPECIFIED_COLUMNS_TYPE = common_pb2.DataType.UNSPECIFIED
UPSERT_TYPE = common_pb2.RecordType.UPSERT
UPDATE_TYPE = common_pb2.RecordType.UPDATE
TRUNCATE_TYPE = common_pb2.RecordType.TRUNCATE
DELETE_TYPE = common_pb2.RecordType.DELETE


def _use_row_data() -> bool:
    # Read lazily, not once at import -- `fivetran debug` sets this env var after this module has
    # already been imported, so a frozen module-level constant would never see it.
    return os.environ.get("ConnectorSdkRemoveValueType", "false").lower() == "true"


class Operations:
    operation_stream = _OperationStream()
    _file_path_override_logged = False

    @staticmethod
    def upsert(table: str, data: dict, *, schema: Optional[str] = None, file: Optional[FileUpload] = None):
        """Updates records with the same primary key if already present in the destination. Inserts new records if not already present in the destination.

        Args:
            table (str): The name of the table.
            data (dict): The data to upsert.
            schema (str, optional): The name of the source schema this table belongs to.
            file (FileUpload, optional): A file upload to stream before the metadata row.
        """
        _validate_table_name(table)
        _validate_schema(schema)
        start_time = get_start_timer()
        if _use_row_data():
            record = _build_row_data_record(schema, table, data, UPSERT_TYPE, file)
        else:
            record = _build_record(schema, table, data, UPSERT_TYPE, file)
        if CAPTURE_PERFORMANCE_METRICS_ENABLED:
            Operations.operation_stream._sdk_build_ns += time.perf_counter_ns() - start_time
        _emit_record(schema, table, record, file)

    @staticmethod
    def update(table: str, modified: dict, *, schema: Optional[str] = None, file: Optional[FileUpload] = None):
        """Performs an update operation on the specified table with the given modified data.

        Args:
            table (str): The name of the table.
            modified (dict): The modified data.
            schema (str, optional): The name of the source schema this table belongs to.
            file (FileUpload, optional): A file upload to stream before the metadata row.
        """
        _validate_table_name(table)
        _validate_schema(schema)
        start_time = get_start_timer()
        if _use_row_data():
            record = _build_row_data_record(schema, table, modified, UPDATE_TYPE, file)
        else:
            record = _build_record(schema, table, modified, UPDATE_TYPE, file)
        if CAPTURE_PERFORMANCE_METRICS_ENABLED:
            Operations.operation_stream._sdk_build_ns += time.perf_counter_ns() - start_time
        _emit_record(schema, table, record, file)

    @staticmethod
    def truncate(table: str, *, schema: Optional[str] = None):
        """Marks all existing rows in the specified table as deleted.

        This operation performs a soft delete on all rows by setting _fivetran_deleted = TRUE.
        Unlike delete() which marks specific rows by primary keys, truncate() marks all existing rows.
        The operation is buffered and emitted in batches; it may be flushed on checkpoint or when batch limits are reached.

        Args:
            table (str): The name of the table to truncate.
            schema (str, optional): The name of the source schema this table belongs to.

        Returns:
            None
        """
        _validate_table_name(table)
        _validate_schema(schema)
        record = connector_sdk_pb2.StructuredRecord(
            schema_name=schema,
            table_name=table,
            type=TRUNCATE_TYPE,
            data={}
        )
        Operations.operation_stream.add_record(record)

    @staticmethod
    def delete(table: str, keys: dict, *, schema: Optional[str] = None):
        """Performs a soft delete operation on the specified table with the given keys.

        Args:
            table (str): The name of the table.
            keys (dict): The keys to delete.
            schema (str, optional): The name of the source schema this table belongs to.

        Returns:
            connector_sdk_pb2.UpdateResponse: The delete response.
        """
        _validate_table_name(table)
        _validate_schema(schema)
        columns = _get_columns(schema, table)
        start_time = get_start_timer()
        if _use_row_data():
            encoded_data = _encode_row_data(columns, keys)
            record = connector_sdk_pb2.StructuredRecord(
                schema_name=schema,
                table_name=table,
                type=DELETE_TYPE,
                row_data=encoded_data
            )
        else:
            mapped_data = _map_data_to_columns(keys, columns)
            record = connector_sdk_pb2.StructuredRecord(
                schema_name=schema,
                table_name=table,
                type=DELETE_TYPE,
                data=mapped_data
            )
        if CAPTURE_PERFORMANCE_METRICS_ENABLED:
            Operations.operation_stream._sdk_build_ns += time.perf_counter_ns() - start_time
        Operations.operation_stream.add_record(record)

    @staticmethod
    def checkpoint(state: dict):
        """Checkpoint saves the connector's state. State is a dict which stores information to continue the
        sync from where it left off in the previous sync. For example, you may choose to have a field called
        "cursor" with a timestamp value to indicate up to when the data has been synced. This makes it possible
        for the next sync to fetch data incrementally from that time forward. See below for a few example fields
        which act as parameters for use by the connector code.\n
        {
            "initialSync": true,\n
            "cursor": "1970-01-01T00:00:00.00Z",\n
            "last_resync": "1970-01-01T00:00:00.00Z",\n
            "thread_count": 5,\n
            "api_quota_left": 5000000
        }

        Args:
            state (dict): The state to checkpoint/save.

        Returns:
            connector_sdk_pb2.UpdateResponse: The checkpoint response.
        """
        checkpoint = connector_sdk_pb2.Checkpoint(state_json=json.dumps(state))

        Operations.operation_stream.add_checkpoint(checkpoint)

    @staticmethod
    def error(message: str, trace: Optional[str] = None):
        """Reports an error that occurred during the sync. This method allows the connector to communicate
        errors to Fivetran, terminating the sync process. The error will be logged and displayed
        in the Fivetran dashboard.

        Args:
            message (str): A description of the error that occurred.
            trace (str, optional): Stack trace or additional debugging information about the error.

        Returns:
            None

        Raises:
            ValueError: If message is empty or contains only whitespace.
            TypeError: If message or trace is not a string (trace may be None).
        """
        _validate_message(message)
        _validate_trace(trace)
        payload = {"message": message}
        if trace and trace.strip():
            payload["trace"] = trace
        error_json = json.dumps(payload)
        error = common_pb2.Task(message=error_json)
        Operations.operation_stream.add_task(error)

    @staticmethod
    def warning(message: str):
        """Reports a warning that occurred during the sync. This method allows the connector to communicate
        non-critical issues to Fivetran without affecting the sync process. The warning will be logged and
        displayed in the Fivetran dashboard.

        Args:
            message (str): A description of the warning or non-critical issue that occurred.

        Returns:
            None

        Raises:
            ValueError: If message is empty or contains only whitespace.
            TypeError: If message is not a string.
        """
        _validate_message(message)
        payload = {"message": message}
        warning_json = json.dumps(payload)
        warning = common_pb2.Warning(message=warning_json)
        Operations.operation_stream.add_warning(warning)


def _get_columns(schema: Optional[str], table: str) -> dict:
    """Retrieves the columns and maps to their type for the specified schema-qualified table.

    Args:
        schema (str, optional): The schema the table belongs to, or None if the schema was omitted.
        table (str): The name of the table.

    Returns:
        dict: The columns for the table.
    """
    schema_table_key = (schema, table)
    columns = {}
    if schema_table_key in TABLES_COLUMNS_TYPES:
        columns = TABLES_COLUMNS_TYPES[schema_table_key]
    if not columns and schema_table_key in TABLES:
        for column in TABLES[schema_table_key].columns:
            columns[column.name] = column.type
        TABLES_COLUMNS_TYPES[schema_table_key] = columns

    return columns

def _build_record(
        schema: Optional[str], table: str, data: dict, record_type,
        file_upload: Optional[FileUpload]):
    """`schema` is put on the wire as-is: an omitted schema must never set schema_name, so that an entirely
    unqualified table stays distinguishable, on the Java side, from one explicitly qualified with a schema
    that happens to equal the connection name (see ConnectorSdkService.java's schemaRule() and its
    'legacy vs. explicit-same-name' handling).
    """
    validate_file_upload_if_present(file_upload)

    columns = _get_columns(schema, table)
    mapped_data = _map_data_to_columns(data, columns)
    if file_upload is not None:
        if FIVETRAN_FILE_PATH_COLUMN in data and not Operations._file_path_override_logged:
            print_library_log(
                f"{FIVETRAN_FILE_PATH_COLUMN} was provided in the row data and will be overwritten by FileUpload.path.",
                level=Logging.Level.WARNING
            )
            Operations._file_path_override_logged = True
        mapped_data[FIVETRAN_FILE_PATH_COLUMN] = common_pb2.ValueType(string=file_upload.path)

    return connector_sdk_pb2.StructuredRecord(
        schema_name=schema,
        table_name=table,
        type=record_type,
        data=mapped_data
    )

def _build_row_data_record(
        schema: Optional[str], table: str, data: dict, record_type,
        file_upload: Optional[FileUpload]):
    validate_file_upload_if_present(file_upload)

    columns = _get_columns(schema, table)
    encoded_data = _encode_row_data(columns, data)
    if file_upload is not None:
        if FIVETRAN_FILE_PATH_COLUMN in data and not Operations._file_path_override_logged:
            print_library_log(
                f"{FIVETRAN_FILE_PATH_COLUMN} was provided in the row data and will be overwritten by FileUpload.path.",
                level=Logging.Level.WARNING
            )
            Operations._file_path_override_logged = True
        encoded_data[FIVETRAN_FILE_PATH_COLUMN] = _PFX_SCALAR + file_upload.path.encode('utf-8')

    return connector_sdk_pb2.StructuredRecord(
        schema_name=schema,
        table_name=table,
        type=record_type,
        row_data=encoded_data
    )

def _emit_record(schema: Optional[str], table: str, record, file_upload: Optional[FileUpload]):
    if file_upload is None:
        Operations.operation_stream.add_record(record)
        return

    # Same schema as the metadata `record` above (see _build_record's docstring), so
    # the uploaded file and its metadata row land under the same destination schema.
    Operations.operation_stream.add_file_upload(file_upload_chunks(schema, table, file_upload), record)

def _map_data_to_columns(data: dict, columns: dict) -> dict:
    """Maps data to the specified columns.

    Args:
        data (dict): The data to map.
        columns (dict): The columns to map the data to.

    Returns:
        dict: The mapped data.
    """
    mapped_data = {}
    for key, v in data.items():
        if v is None:
            mapped_data[key] = common_pb2.ValueType(null=True)
        elif (key in columns) and columns[key] != UNSPECIFIED_COLUMNS_TYPE:
            map_defined_data_type(columns[key], key, mapped_data, v)
        else:
            map_inferred_data_type(key, mapped_data, v)
    return mapped_data

_INFERENCE_TYPE_HANDLERS = {
    int: lambda v: common_pb2.ValueType(float=v) if abs(v)>JAVA_LONG_MAX_VALUE else common_pb2.ValueType(long=v),
    float: lambda v: common_pb2.ValueType(float=v),
    bool: lambda v: common_pb2.ValueType(bool=v),
    bytes: lambda v: common_pb2.ValueType(binary=v),
    dict: lambda v: common_pb2.ValueType(json=json.dumps(v)),
    str: lambda v: common_pb2.ValueType(string=v)
}

def map_inferred_data_type(k, mapped_data, v):
    data_type = type(v)
    handler = _INFERENCE_TYPE_HANDLERS.get(data_type)
    if handler:
        mapped_data[k] = handler(v)
    elif isinstance(v, bool):
        mapped_data[k] = common_pb2.ValueType(bool=v)
    elif isinstance(v, int):
        if abs(v) > JAVA_LONG_MAX_VALUE:
            mapped_data[k] = common_pb2.ValueType(float=v)
        else:
            mapped_data[k] = common_pb2.ValueType(long=v)
    elif isinstance(v, float):
        mapped_data[k] = common_pb2.ValueType(float=v)
    elif isinstance(v, bytes):
        mapped_data[k] = common_pb2.ValueType(binary=v)
    elif isinstance(v, (list, dict)):
        mapped_data[k] = common_pb2.ValueType(json=json.dumps(v))
    elif isinstance(v, str):
        mapped_data[k] = common_pb2.ValueType(string=v)
    else:
        # Convert arbitrary objects to string
        mapped_data[k] = common_pb2.ValueType(string=str(v))

_TYPE_HANDLERS = {
    common_pb2.DataType.BOOLEAN: lambda val: common_pb2.ValueType(bool=val),
    common_pb2.DataType.SHORT: lambda val: common_pb2.ValueType(short=val),
    common_pb2.DataType.INT: lambda val: common_pb2.ValueType(int=val),
    common_pb2.DataType.LONG: lambda val: common_pb2.ValueType(long=val),
    common_pb2.DataType.DECIMAL: lambda val: common_pb2.ValueType(decimal=val),
    common_pb2.DataType.FLOAT: lambda val: common_pb2.ValueType(float=val),
    common_pb2.DataType.DOUBLE: lambda val: common_pb2.ValueType(double=val),
    common_pb2.DataType.NAIVE_DATE: lambda val: common_pb2.ValueType(naive_date= _parse_naive_date_str(val)),
    common_pb2.DataType.NAIVE_DATETIME: lambda val: common_pb2.ValueType(naive_datetime= _parse_naive_datetime_str(val)),
    common_pb2.DataType.UTC_DATETIME: lambda val: common_pb2.ValueType(utc_datetime= _parse_utc_datetime_str(val)),
    common_pb2.DataType.BINARY: lambda val: common_pb2.ValueType(binary=val),
    common_pb2.DataType.XML: lambda val: common_pb2.ValueType(xml=val),
    common_pb2.DataType.STRING: lambda val: common_pb2.ValueType(string=val if isinstance(val, str) else str(val)),
    common_pb2.DataType.JSON: lambda val: common_pb2.ValueType(json=json.dumps(val))
}

def map_defined_data_type(data_type, k, mapped_data, v):
    handler = _TYPE_HANDLERS.get(data_type)
    if handler:
        mapped_data[k] = handler(v)
    else:
        raise ValueError(f"Unsupported data type encountered: {data_type}. Please use valid data types.")

def get_start_timer():
    return time.perf_counter_ns() if CAPTURE_PERFORMANCE_METRICS_ENABLED else 0
