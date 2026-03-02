"""
Trace analysis utilities for PipelineRunner callbacks.

This module provides helper functions to analyze DLT pipeline traces and extract
meaningful insights about schema changes, row counts, and pipeline execution.
"""

from typing import Dict
from dlt.pipeline.trace import PipelineTrace
from dlt.common.storages.load_package import LoadPackageInfo
from dlt.common.schema.typing import TTableSchema
from dlt.common.utils import RowCounts


def _has_schema_changes(trace: PipelineTrace) -> bool:
    """
    Check if the trace has schema changes by looking for schema updates in all load packages.
    """
    for step in getattr(trace, "steps", []):
        step_info = getattr(step, "step_info", None)
        if not step_info or not hasattr(step_info, "load_packages"):
            continue

        for package in step_info.load_packages:
            if hasattr(package, "schema_update") and package.schema_update:
                return True

    return False


def _add_updates_from_load_package_into_schema_changes(
    package: LoadPackageInfo,
    updates: Dict[str, Dict[str, TTableSchema]],
) -> None:
    """Process a single package's schema updates and merge them into the given
    updates dict under the name of the schema that gets updated.
    """
    if not hasattr(package, "schema_update") or not package.schema_update:
        return

    schema_name = package.schema_name
    if schema_name not in updates:
        updates[schema_name] = {}
    schema_update_dict = updates[schema_name]

    for table_name, table_update in package.schema_update.items():
        if table_name in schema_update_dict:
            for column_name, column_update in table_update["columns"].items():
                schema_update_dict[table_name]["columns"][column_name] = column_update
        else:
            schema_update_dict[table_name] = table_update


def get_combined_schema_updates(trace: PipelineTrace) -> Dict[str, Dict[str, TTableSchema]]:
    """
    Analyze trace data to identify schema changes to tables and columns from all load packages,
    grouped by schema.
    Returns:
        Dict[str, Dict[str, TTableSchema]] all new table schema, grouped by schema,
            {schema_name: {table_name: TTableSchema}}
    """
    schema_updates: Dict[str, Dict[str, TTableSchema]] = {}

    for step in trace.steps:
        step_info = step.step_info if hasattr(step, "step_info") else None
        if not step_info or not hasattr(step_info, "load_packages"):
            continue

        for package in step_info.load_packages:
            _add_updates_from_load_package_into_schema_changes(package, schema_updates)

    return schema_updates


def rows_processed_per_table(trace: PipelineTrace) -> RowCounts:
    """
    Extract row counts per table from trace data.

    Args:
        trace: The PipelineTrace object from pipeline execution

    Returns:
        Dict mapping table names to row counts processed in this run
        (excluding internal tables and child tables)

    """
    if normalize_info := trace.last_normalize_info:
        return normalize_info.row_counts
    else:
        return {}
