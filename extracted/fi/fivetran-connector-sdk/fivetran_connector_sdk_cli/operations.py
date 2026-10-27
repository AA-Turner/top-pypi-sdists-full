"""What a connector calls to emit data: upsert, update, delete, truncate, checkpoint, warning and error."""
import json

from typing import Optional

from fivetran_connector_sdk_common.constants import FIVETRAN_FILE_PATH_COLUMN
from fivetran_connector_sdk_common.helpers import (
    _validate_table_name, _validate_message, _validate_trace, print_library_log,
    _validate_schema,
)
from fivetran_connector_sdk_common.logger import Logging
from fivetran_connector_sdk_cli import runtime
from fivetran_connector_sdk_cli.file_upload import FileUpload, file_upload_chunks, validate_file_upload_if_present
from fivetran_connector_sdk_cli.records import Checkpoint, RecordType, Task, Warning, make_record, make_truncate
from fivetran_connector_sdk_cli.schema_processing import TABLES, TABLES_COLUMNS_TYPES
from fivetran_connector_sdk_cli.type_coercion import _PFX_SCALAR, encode_row_data


class Operations:
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
        record = _build_row_data_record(schema, table, data, RecordType.UPSERT, file)
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
        record = _build_row_data_record(schema, table, modified, RecordType.UPDATE, file)
        _emit_record(schema, table, record, file)

    @staticmethod
    def truncate(table: str, *, schema: Optional[str] = None):
        """Marks all existing rows in the specified table as deleted.

        This operation performs a soft delete on all rows by setting _fivetran_deleted = TRUE.
        Unlike delete() which marks specific rows by primary keys, truncate() marks all existing rows.

        Args:
            table (str): The name of the table to truncate.
            schema (str, optional): The name of the source schema this table belongs to.

        Returns:
            None
        """
        _validate_table_name(table)
        _validate_schema(schema)
        truncate = make_truncate(table, schema)
        with runtime.producer_lock:
            runtime.current().truncate(truncate)

    @staticmethod
    def delete(table: str, keys: dict, *, schema: Optional[str] = None):
        """Performs a soft delete operation on the specified table with the given keys.

        Args:
            table (str): The name of the table.
            keys (dict): The keys to delete.
            schema (str, optional): The name of the source schema this table belongs to.
        """
        _validate_table_name(table)
        _validate_schema(schema)
        columns = _get_columns(schema, table)
        encoded_data = encode_row_data(columns, keys)
        record = make_record(table, RecordType.DELETE, encoded_data, schema)
        with runtime.producer_lock:
            runtime.current().record(record)

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
        """
        checkpoint = Checkpoint(state_json=json.dumps(state))

        # One checkpoint at a time; this call returns once the runner has committed everything up to it. Other threads' records
        # wait while it does (in production one consumer takes the stream in order): a record added during the commit
        # would be written or cleared with the rows that were waiting, and could be lost.
        with runtime.checkpoint_lock:
            with runtime.producer_lock:
                runtime.current().checkpoint(checkpoint)

    @staticmethod
    def error(message: str, trace: Optional[str] = None):
        """Reports an error that occurred during the sync. This method allows the connector to communicate
        errors to Fivetran, terminating the sync process. The error will be logged and displayed
        in the Fivetran dashboard.

        Args:
            message (str): A description of the error that occurred.
            trace (str, optional): Stack trace or additional debugging information about the error.

        Raises:
            ValueError: If message is empty or contains only whitespace.
            TypeError: If message or trace is not a string (trace may be None).
        """
        _validate_message(message)
        _validate_trace(trace)
        payload = {"message": message}
        if trace and trace.strip():
            payload["trace"] = trace
        error = Task(message=json.dumps(payload))
        with runtime.producer_lock:
            runtime.current().task(error)

    @staticmethod
    def warning(message: str):
        """Reports a warning that occurred during the sync. This method allows the connector to communicate
        non-critical issues to Fivetran without affecting the sync process. The warning will be logged and
        displayed in the Fivetran dashboard.

        Args:
            message (str): A description of the warning or non-critical issue that occurred.

        Raises:
            ValueError: If message is empty or contains only whitespace.
            TypeError: If message is not a string.
        """
        _validate_message(message)
        warning = Warning(message=json.dumps({"message": message}))
        with runtime.producer_lock:
            runtime.current().warning(warning)


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


def _build_row_data_record(schema: Optional[str], table: str, data: dict, record_type, file_upload: Optional[FileUpload]):
    validate_file_upload_if_present(file_upload)

    columns = _get_columns(schema, table)
    encoded_data = encode_row_data(columns, data)
    if file_upload is not None:
        if FIVETRAN_FILE_PATH_COLUMN in data and not Operations._file_path_override_logged:
            print_library_log(
                f"{FIVETRAN_FILE_PATH_COLUMN} was provided in the row data and will be overwritten by FileUpload.path.",
                level=Logging.Level.WARNING
            )
            Operations._file_path_override_logged = True
        encoded_data[FIVETRAN_FILE_PATH_COLUMN] = _PFX_SCALAR + file_upload.path.encode('utf-8')

    return make_record(table, record_type, encoded_data, schema)


def _emit_record(schema: Optional[str], table: str, record, file_upload: Optional[FileUpload]):
    if file_upload is None:
        with runtime.producer_lock:
            runtime.current().record(record)
        return

    # The file's chunks and the row that describes it go out together.
    with runtime.producer_lock:
        sink = runtime.current()
        for chunk in file_upload_chunks(schema, table, file_upload):
            sink.file_chunk(chunk)
        sink.record(record)
