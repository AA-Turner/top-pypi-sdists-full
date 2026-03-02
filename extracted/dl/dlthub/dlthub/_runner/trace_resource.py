from typing import Any, Dict, Iterator, List
from importlib import resources
import yaml

import dlt
from dlt.common.schema import Schema
from dlt.common.json import json
from dlt.pipeline import Pipeline
from dlt.common.time import precise_time


TRACE_TABLE_SUFFIX = "trace"
TRACES_DIR = "traces"


@dlt.resource(name=lambda args: args["table_name"])
def trace_resource(pipeline: Pipeline, table_name: str) -> Iterator[List[Dict[str, Any]]]:
    """
    A resource that yields the content of all files named `*trace.json` from the pipeline's working
    directory to a table of a given name. The resource name will be set to the table name.

    Args:
        pipeline (Pipeline): The pipeline to get the trace from.
        table_name (str): The name of the table to load the trace into. Resource name will default
        to this name as well.

    Returns:
        Iterator[List[Dict[str, Any]]]: Iterator of PipelineTrace objects as dictionaries.

    Behavior:
        - Scans the pipeline's working directory for trace files.
        - Reads and validates each trace JSON file.
        - Yields trace data as dictionaries for loading to destination.

    Example:
        >>> pipeline = dlt.pipeline("my_pipeline", destination="duckdb")
        >>> # Load trace data to destination
        >>> pipeline.run(trace_resource(pipeline, table_name="my_pipeline_trace"))
    """
    storage = pipeline._pipeline_storage
    if storage.has_folder(TRACES_DIR):
        for filename in storage.list_folder_files(TRACES_DIR):
            if filename.endswith("trace.json"):
                trace_dict = json.loads(storage.open_file(filename, "r").read())
                yield [trace_dict]


def write_trace_to_pipeline_storage(pipeline: Pipeline, name_suffix: str = None) -> None:
    """
    Write the last trace of the pipeline to the pipeline storage.

    The trace is saved as a JSON file in the 'traces' directory to the pipeline's working directory.
    The filename format is: ./traces/<transaction_id>_trace[_suffix]_trace.json

    Args:
        pipeline (Pipeline): The pipeline whose trace should be written to storage.
        name_suffix (str, optional): An optional string to add to the filename for added context.
            When provided, it's included in the filename. If not provided, a 6-character hash
            based on current time and pipeline name is generated automatically.

    Example:
        >>> pipeline = dlt.pipeline("my_pipeline", destination="duckdb")
        >>> pipeline.run(data)
        >>> write_trace_to_pipeline_storage(pipeline, name_suffix="attempt_1")
    """
    if pipeline.last_trace is None:
        return
    pipeline_storage = pipeline._pipeline_storage
    trace = pipeline.last_trace

    pipeline_storage.create_folder(TRACES_DIR, exists_ok=True)

    # Determine the suffix for the filename
    if name_suffix:
        suffix_part = f"{TRACE_TABLE_SUFFIX}_{name_suffix}"
    else:
        # Generate a 6-char unique hash based on time and pipeline name
        unique_hash = hash(f"{precise_time()}_{pipeline.pipeline_name}") % 1000000
        suffix_part = f"{TRACE_TABLE_SUFFIX}_{unique_hash:06x}"

    filename = f"{TRACES_DIR}/{trace.transaction_id}_{suffix_part}_trace.json"

    pipeline_storage.save_atomic(
        pipeline_storage.storage_path,
        filename,
        data=json.dumps(trace.asdict()),
    )


def delete_trace_files(pipeline: Pipeline) -> None:
    """
    Deletes all trace files from the pipeline's storage /traces folder.

    Args:
        pipeline (Pipeline): The pipeline whose trace files should be deleted.

    Behavior:
        - Checks if the traces directory exists in pipeline storage.
        - Deletes all files in the traces directory.
        - Removes the traces directory itself recursively.
        - Does nothing if no traces directory exists.

    Example:
        >>> pipeline = dlt.pipeline("my_pipeline", destination="duckdb")
        >>> # Clean up trace files after successful processing
        >>> delete_trace_files(pipeline)
    """
    storage = pipeline._pipeline_storage
    if not storage.has_folder(TRACES_DIR):
        return
    for filename in storage.list_folder_files(TRACES_DIR):
        storage.delete(filename)
    storage.delete_folder(TRACES_DIR, recursively=True)


def has_traces(pipeline: Pipeline) -> int:
    """Check if the pipeline has any trace files stored."""
    if pipeline._pipeline_storage.has_folder(TRACES_DIR):
        return len(pipeline._pipeline_storage.list_folder_files(TRACES_DIR))
    return 0


def get_default_trace_schema_with_name(name: str) -> Schema:
    """
    Get the default schema of a pipeline trace as of dlt 1.13.0 and change its name
    table and child table names to the given name.
    """
    with resources.files(__package__).joinpath("trace.schema.yaml").open(encoding="utf-8") as f:
        imported_schema = yaml.safe_load(f)

    imported_schema = _rename_schema_and_tables(imported_schema, old_name="trace", new_name=name)

    return Schema.from_dict(imported_schema, remove_processing_hints=True)


def _rename_schema_and_tables(
    schema_dict: Dict[str, Any], old_name: str, new_name: str
) -> Dict[str, Any]:
    """
    Adjust the
    - the name of the schema
    - change all table names (and child tables)
    - changes all references to the old name to the new name (resource, parent)
    NOTE: this is a function that works for the trace schema specifically, e.g. assuming that the
    resource writing to this table has same name as the schema.
    """

    def change_to_new_name(table_name: str) -> str:
        # replace old with new prefix in table name
        return table_name.replace(old_name, new_name)

    # Create a copy to avoid modifying the original
    adjusted_schema = schema_dict.copy()

    adjusted_schema["name"] = new_name

    tables = adjusted_schema.get("tables", {})
    new_tables = {}

    for table_name, table in tables.items():
        new_table = table.copy()

        if "parent" in new_table:
            new_table["parent"] = change_to_new_name(new_table["parent"])

        # Note: this assumes that the resource writing to this table has same name as the schema
        if "resource" in new_table and old_name in new_table["resource"]:
            new_table["resource"] = change_to_new_name(new_table["resource"])

        new_table_name = change_to_new_name(table_name)
        new_tables[new_table_name] = new_table

    adjusted_schema["tables"] = new_tables

    return adjusted_schema
