"""What the front end hands to the core: plain values, one per operation a connector emits. They are the core's own types,
and this module builds them, checking the values as Fivetran does."""
from fivetran_connector_sdk_core.model import Checkpoint, FileChunk, Record, RecordType, Task, Truncate, Warning

from fivetran_connector_sdk_cli import wire

__all__ = ["Checkpoint", "FileChunk", "Record", "RecordType", "Task", "Truncate", "Warning", "make_file_chunk", "make_record",
           "make_truncate"]


def make_record(table, record_type, row_data, schema=None):
    """Builds a `Record` and fails as it does on Fivetran for names and values it rejects."""
    schema_name = wire.optional_text(schema)  # the schema is set before the table name
    table_name = wire.text(table)
    checked = {}
    for key, value in row_data.items():
        key = wire.map_key(key)  # a map's key is checked before its value
        checked[key] = wire.byte_string(value, unset_if_none=False)
    return Record(table_name, record_type, checked, schema_name)


def make_truncate(table, schema=None, deferred=False):
    """Builds a `Truncate`, checking the values in the order Fivetran does (the schema is set before the table name)."""
    schema_name = wire.optional_text(schema)
    return Truncate(wire.text(table), schema_name, bool(wire.boolean(deferred)))


def make_file_chunk(storage_name, file_path, chunk_data, is_last, expected_bytes=None, schema=None):
    """Builds a `FileChunk`, checking the values in the order Fivetran does."""
    name = wire.text(storage_name)
    path = wire.text(file_path)
    data = wire.byte_string(chunk_data)
    schema_name = wire.optional_text(schema)
    size = None if expected_bytes is None else wire.integer(expected_bytes, bits=64, signed=True)
    return FileChunk(name, path, data, bool(is_last), size, schema_name)


