import time
import logging
from typing import Dict, List, Union, TextIO, cast
from uuid import UUID
import traceback

from dlt.common.exceptions import MissingDependencyException
from dlt.common.schema.typing import TTableSchema
from dlt.common import logger as dlt_logger
from dlt.pipeline.trace import PipelineTrace
from dlt.pipeline.typing import TPipelineStep
from dlt.common.pipeline import SupportsPipeline
from dlt.common.runtime.exec_info import get_execution_context
from dlthub._runner.plus_log_collector import PlusLogCollector
from dlt.common.runtime.collector import LogCollector
from dlt.common.utils import RowCounts

try:
    from prefect.context import get_run_context
    from prefect.context import TaskRunContext
    from prefect.artifacts import (
        create_markdown_artifact,
        create_progress_artifact,
        update_progress_artifact,
    )
    from prefect.logging import get_run_logger
    from prefect.exceptions import MissingContextError
except ModuleNotFoundError:
    raise MissingDependencyException(
        "prefect", ["prefect>=3.4.0"], "prefect must be installed to use PrefectCollector"
    )


class PrefectCollector(PlusLogCollector):
    """A Collector that creates Prefect artifacts for pipeline progress tracking.

    This collector extends CallbackCollector to create Prefect progress artifacts
    that show pipeline progress in the Prefect UI.
    """

    def __init__(
        self,
        log_period: float = 1.0,
        logger: Union[logging.Logger, TextIO] = None,
        log_level: int = logging.INFO,
        dump_system_stats: bool = True,
        create_summary_artifacts: bool = True,
        create_progress_artifacts: bool = True,
    ) -> None:
        """Initialize the Prefect collector.
        Note: This collector should be instantiated inside a flow or task.

        Args:
            log_period (float, optional): Time period in seconds between log updates.
            logger (logging.Logger | TextIO, optional): Logger or text stream to write log messages
                to. If none is provided, it will try to get the prefect logger.
            log_level (str, optional): Log level for the logger. Defaults to INFO level
            dump_system_stats (bool, optional): Log memory and cpu usage. Defaults to True
            create_artifacts (bool, optional): Whether to create Prefect artifacts. Defaults to True

        Raises:
            MissingContextError: If the logger is not provided and the prefect context is not found.

        Example:
        from prefect import flow, task
        @task
        def my_task():
            pipeline = dlt.pipeline(
                pipeline_name="my_pipeline",
                destination="duckdb",
                progress=PrefectCollector(),
            )
        """
        if logger is None:
            try:
                logger = get_run_logger()
            except MissingContextError:
                dlt_logger.error(
                    "Could not find prefects context aware logger. Instantiate "
                    "PrefectCollector inside a flow or task"
                )
                raise

        super().__init__(log_period, logger, log_level, dump_system_stats)
        self.create_summary_artifacts = create_summary_artifacts
        self.create_progress_artifacts = create_progress_artifacts
        # Dict to store progress artifact IDs for each stage
        self.progress_artifact_ids: Dict[str, UUID] = {}
        self.pipeline_instance: SupportsPipeline = None
        # Store the pipeline instance for artifact creation

    def on_start_trace(
        self, trace: PipelineTrace, step: TPipelineStep, pipeline: SupportsPipeline
    ) -> None:
        """Called when a pipeline trace starts - store the pipeline instance."""
        self.pipeline_instance = pipeline  # liskov substitution principle violation?

    def _start(self, step: str) -> None:
        """Start tracking with Prefect task tags."""
        super()._start(step)
        # Reset progress artifact IDs for new stage
        self.progress_artifact_ids = {}

    def _stop(self) -> None:
        """Stop tracking and create stage summary markdown artifact."""
        # Create artifact before calling parent's _stop() which clears counters
        if self.create_summary_artifacts and self.counters is not None and len(self.counters) > 0:
            try:
                self._create_stage_summary_markdown_artifact()
            except Exception as e:
                self._log(logging.WARNING, f"PrefectCollector artifact creation error: {e}")

        super()._stop()

    def on_log(self) -> None:
        """Called when logging occurs - update progress artifacts."""
        if self.create_progress_artifacts and self.counters:
            self._update_progress_artifacts()
        # also print the counters
        super().on_log()

    def on_schema_change(
        self,
        pipeline: SupportsPipeline,
        trace: PipelineTrace,
        schema_name: str,
        changes: Dict[str, TTableSchema],
    ) -> None:
        self._create_schema_change_markdown_artifact(schema_name, changes)
        self.add_tag_for_schema_change()

    def on_retry(
        self,
        pipeline: SupportsPipeline,
        trace: PipelineTrace,
        retry_attempt: int,
        last_attempt: bool,
        exception: Exception,
    ) -> None:
        """
        Called when a retry is triggered during the pipeline execution.
        Creates a markdown artifact summarizing the error.
        """

        self._create_retry_error_markdown_artifact(
            pipeline, trace, retry_attempt, last_attempt, exception
        )

    def on_after(
        self,
        pipeline: SupportsPipeline,
        trace: PipelineTrace,
        success: bool,
        summary: RowCounts,
    ) -> None:
        """
        Called after pipeline execution completes. Creates a markdown artifact summarizing the run.
        """
        self._create_final_report_markdown_artifact(pipeline, trace, success, summary)

    #
    # Markdown summary artifacts
    #

    def _exception_to_markdown_lines(self, exception: Union[Exception, str]) -> List[str]:
        """
        Convert an exception to markdown lines for inclusion in artifacts.

        Args:
            exception: The exception to convert (can be Exception object or string)

        Returns:
            List of markdown lines representing the exception
        """
        lines = []

        if isinstance(exception, Exception):
            # Handle actual Exception object
            lines.append(f"**Exception Type**: {type(exception).__name__}")
            lines.append(f"**Exception Message**: {str(exception)}")
            lines.append("")

            import traceback as tb

            tb_str = tb.format_exception(type(exception), exception, exception.__traceback__)
            lines.append("**Traceback:**")
            lines.append("")
            lines.extend([f"    {line}" for line in tb_str])
        else:
            # Handle string or other types
            lines.append(f"**Exception Type**: {type(exception).__name__}")
            lines.append(f"**Exception Message**: {str(exception)}")
            lines.append("")
            lines.append(
                "**Note**: Full traceback not available (exception is not an Exception object)"
            )

        return lines

    def _counter_to_markdown_line(
        self, counter_key: str, count: int, info: LogCollector.CounterInfo, current_time: float
    ) -> str:
        """Convert a single counter to a markdown line format.

        Args:
            counter_key: The counter key
            count: Current count value
            info: CounterInfo object
            current_time: Current timestamp

        Returns:
            str: Formatted markdown line for this counter
        """
        # Reuse the log line method and add markdown formatting
        log_line = self._counter_to_log_line(counter_key, count, info, current_time)

        # Convert to markdown format: add bullet point and bold the description

        # Split on first colon to separate description from the rest
        if ": " in log_line:
            description, rest = log_line.split(": ", 1)
            # Bold the description and add bullet point
            return f"- **{description}**: {rest}"
        else:
            # Fallback if format is unexpected
            return f"- {log_line}"

    def _system_stats_to_markdown_line(self) -> str:
        """Convert system stats to a markdown line format."""
        # Reuse the log line method and add markdown formatting
        log_line = self._system_stats_to_log_line()

        # Convert to markdown format: add bullet point and bold the labels
        # The log line format is: "Memory usage: X MB (Y%) | CPU usage: Z%"
        # We want: "- **Memory**: X MB (Y%) | **CPU**: Z%"

        # Replace "Memory usage:" with "**Memory**:" and "CPU usage:" with "**CPU**:"
        markdown_line = log_line.replace("Memory usage:", "**Memory**:").replace(
            "CPU usage:", "**CPU**:"
        )

        # Add bullet point
        return f"- {markdown_line}"

    def _add_pipeline_info_to_markdown(
        self, markdown_lines: List[str], pipeline: SupportsPipeline
    ) -> None:
        """Add pipeline and execution context information to markdown lines.

        Args:
            markdown_lines: List of markdown lines to append to
            pipeline: The pipeline object to get information from
        """
        markdown_lines.append("")
        markdown_lines.append("## Pipeline Information:")

        # Pipeline basic info
        markdown_lines.append(f"- **Pipeline Name**: {pipeline.pipeline_name}")
        markdown_lines.append(f"- **Working Directory**: {pipeline.working_dir}")
        markdown_lines.append(f"- **First Run**: {pipeline.first_run}")
        markdown_lines.append(f"- **Default Schema**: {pipeline.default_schema_name}")

        # Destination info from pipeline state
        state = pipeline.state
        if state:
            markdown_lines.append(f"- **Destination Name**: {state.get('destination_name', 'N/A')}")
            markdown_lines.append(f"- **Destination Type**: {state.get('destination_type', 'N/A')}")
            markdown_lines.append(f"- **Staging Name**: {state.get('staging_name', 'N/A')}")
            markdown_lines.append(f"- **Staging Type**: {state.get('staging_type', 'N/A')}")

        # Render extra_info dictionary with proper formatting
        if self.extra_info:
            for title, content_dict in self.extra_info.items():
                markdown_lines.append("")
                markdown_lines.append(f"## {title}")
                for key, value in content_dict.items():
                    markdown_lines.append(f"- **{key}**: {value}")

        # Execution context info
        exec_context = get_execution_context()
        markdown_lines.append("")
        markdown_lines.append("## Execution Context:")
        markdown_lines.append(f"- **Python Version**: {exec_context.get('python', 'N/A')}")
        markdown_lines.append(
            "- **OS**:"
            f" {exec_context.get('os', {}).get('name', 'N/A')} {exec_context.get('os', {}).get('version', '')}"  # noqa: E501
        )
        markdown_lines.append(
            "- **Library Version**:"
            f" {exec_context.get('library', {}).get('name', 'N/A')} {exec_context.get('library', {}).get('version', '')}"  # noqa: E501
        )
        markdown_lines.append(f"- **CPU Cores**: {exec_context.get('cpu', 'N/A')}")

        # Execution environment info
        exec_info = exec_context.get("exec_info", [])
        if exec_info:
            markdown_lines.append(f"- **Execution Environment**: {', '.join(exec_info)}")

    def _create_stage_summary_markdown_artifact(self) -> None:
        """Create markdown artifact based on current stage and counters."""
        if not self.create_summary_artifacts:
            return

        try:
            # Determine stage and create appropriate markdown artifact
            step = self.step

            # Skip composite steps (run, sync) as they don't need their own artifacts
            if step.startswith("run") or step.startswith("sync"):
                return

            if step.startswith("Extract"):
                self._create_extract_stage_summary_markdown_artifact()
            elif step.startswith("Normalize"):
                self._create_normalize_stage_summary_markdown_artifact()
            elif step.startswith("Load"):
                self._create_load_stage_summary_markdown_artifact()

        except Exception as e:
            self._log(logging.WARNING, f"Failed to create markdown artifact: {e}")
            self._log(logging.WARNING, f"Traceback: {traceback.format_exc()}")

    def _create_extract_stage_summary_markdown_artifact(self) -> None:
        """Create markdown artifact for extract stage - rows added per table."""
        # Use shared formatting methods to create detailed markdown
        current_time = time.time()
        markdown_lines = []

        # Add stage header
        markdown_lines.append(f"# {self.step} Stage Summary")
        markdown_lines.append("")

        # Add counter details using shared formatting
        total_rows = 0
        table_counts = {}

        for counter_key, count in self.counters.items():
            info = self.counter_info.get(counter_key)
            if info:
                # Use shared markdown formatting
                markdown_lines.append(
                    self._counter_to_markdown_line(counter_key, count, info, current_time)
                )

                # Track table counts for summary
                if not counter_key.startswith("_") and counter_key not in [
                    "Resources",
                    "Files",
                    "Items",
                    "Jobs",
                ]:
                    total_rows += count
                    table_counts[counter_key] = count

        # Add summary section
        if total_rows > 0:
            markdown_lines.append("")
            markdown_lines.append("## Summary:")
            markdown_lines.append(f"- **Total Rows**: {total_rows:,}")
            for table, count in table_counts.items():
                markdown_lines.append(f"- Table **{table}**: {count:,} rows")

        # Add system stats if enabled
        if self.dump_system_stats:
            markdown_lines.append("")
            markdown_lines.append("## System Stats:")
            markdown_lines.append(self._system_stats_to_markdown_line())

        # Add pipeline and execution context info
        if self.pipeline_instance:
            self._add_pipeline_info_to_markdown(markdown_lines, self.pipeline_instance)

        markdown_content = "\n".join(markdown_lines)
        create_markdown_artifact(
            key="extract-summary",
            markdown=markdown_content,
            description="Extract stage summary",
        )

    def _create_normalize_stage_summary_markdown_artifact(self) -> None:
        """Create markdown artifact for normalize stage - files and items processed."""
        # Use shared formatting methods to create detailed markdown
        current_time = time.time()
        markdown_lines = []

        # Add stage header
        markdown_lines.append(f"# {self.step} Stage Summary")
        markdown_lines.append("")

        # Add counter details using shared formatting
        for counter_key, count in self.counters.items():
            info = self.counter_info.get(counter_key)
            if info:
                # Use shared markdown formatting
                markdown_lines.append(
                    self._counter_to_markdown_line(counter_key, count, info, current_time)
                )

        # Add system stats if enabled
        if self.dump_system_stats:
            markdown_lines.append("")
            markdown_lines.append("## System Stats:")
            markdown_lines.append(self._system_stats_to_markdown_line())

        # Add pipeline and execution context info
        if self.pipeline_instance:
            self._add_pipeline_info_to_markdown(markdown_lines, self.pipeline_instance)

        markdown_content = "\n".join(markdown_lines)
        create_markdown_artifact(
            key="normalize-summary",
            markdown=markdown_content,
            description="Normalize stage summary",
        )

    def _create_load_stage_summary_markdown_artifact(self) -> None:
        """Create markdown artifact for load stage - jobs processed."""
        # Use shared formatting methods to create detailed markdown
        current_time = time.time()
        markdown_lines = []

        # Add stage header
        markdown_lines.append(f"# {self.step} Stage Summary")
        markdown_lines.append("")

        # Add counter details using shared formatting
        for counter_key, count in self.counters.items():
            info = self.counter_info.get(counter_key)
            if info:
                # Use shared markdown formatting
                markdown_lines.append(
                    self._counter_to_markdown_line(counter_key, count, info, current_time)
                )

        # Add system stats if enabled
        if self.dump_system_stats:
            markdown_lines.append("")
            markdown_lines.append("## System Stats:")
            markdown_lines.append(self._system_stats_to_markdown_line())

        # Add pipeline and execution context info
        if self.pipeline_instance:
            self._add_pipeline_info_to_markdown(markdown_lines, self.pipeline_instance)

        markdown_content = "\n".join(markdown_lines)
        create_markdown_artifact(
            key="load-summary",
            markdown=markdown_content,
            description="Load stage summary",
        )

    def _create_schema_change_markdown_artifact(
        self, schema_name: str, changes: Dict[str, TTableSchema]
    ) -> None:
        """Create markdown artifact for schema change."""
        only_my_tables = _changes_without_dlt_changes(changes)
        markdown_lines = []
        markdown_lines.append(f"# Schema Changes in schema: `{schema_name}`")
        markdown_lines.append("")
        markdown_lines.append(f"**Tables changed**: {len(changes)}")
        markdown_lines.append(f"without dlt tables: {len(only_my_tables)}")
        markdown_lines.append("")
        markdown_lines.append("## Changes by table:")

        for table, schema in only_my_tables.items():
            markdown_lines.append(f"### Table: {table}")
            markdown_lines.append("")

            # Process all schema keys except 'columns' first
            for key, value in schema.items():
                if key != "columns" and value is not None:
                    markdown_lines.append(f"**{key.title()}**: {value}")

            # Special handling for columns - create a subsection
            if "columns" in schema and schema["columns"]:
                markdown_lines.append("### Updated Columns")
                markdown_lines.append("")
                for column_name, column_schema in schema["columns"].items():
                    markdown_lines.append(f"#### **{column_name}**")
                    # Display column properties
                    if isinstance(column_schema, dict):
                        # show all keys at individual rows
                        for prop_key, prop_value in column_schema.items():
                            if prop_value is not None:
                                markdown_lines.append(f"- **{prop_key}**: `{prop_value}`")

                    else:
                        # If column_schema is not a dict, just show the value
                        markdown_lines.append(f"- `{column_schema}`")
                    markdown_lines.append("")

        # Add pipeline and execution context info
        if self.pipeline_instance:
            self._add_pipeline_info_to_markdown(markdown_lines, self.pipeline_instance)

        markdown_content = "\n".join(markdown_lines)
        create_markdown_artifact(
            key="schema-change",
            markdown=markdown_content,
            description="Schema change",
        )

    def _create_retry_error_markdown_artifact(
        self,
        pipeline: SupportsPipeline,
        trace: PipelineTrace,
        retry_attempt: int,
        last_attempt: bool,
        exception: Exception,
    ) -> None:
        """
        Create a markdown artifact summarizing a retry error.
        """
        try:
            lines = [
                f"# Pipeline Retry Attempt {retry_attempt}",
                f"**Pipeline**: {getattr(pipeline, 'pipeline_name', str(pipeline))}",
                f"**Last Attempt**: {last_attempt}",
            ]
            if trace:
                lines.append(f"**Trace ID**: {getattr(trace, 'trace_id', 'N/A')}")
            lines.append("")

            # Add exception information using the helper method
            lines.extend(self._exception_to_markdown_lines(exception))

            markdown_content = "\n".join(lines)
            create_markdown_artifact(
                key="retry-error",
                markdown=markdown_content,
                description="Pipeline retry error summary",
            )
        except Exception as e:
            self._log(
                logging.WARNING, f"PrefectCollector failed to create retry error artifact: {e}"
            )

    def _create_final_report_markdown_artifact(
        self,
        pipeline: SupportsPipeline,
        trace: PipelineTrace,
        success: bool,
        summary: RowCounts,
    ) -> None:
        """
        Create a markdown artifact summarizing the complete pipeline run (final report).
        """
        try:
            from dlthub._runner.trace_helpers import (
                get_combined_schema_updates,
            )

            markdown_lines = []
            markdown_lines.append("# Pipeline Final Report")
            markdown_lines.append("")
            markdown_lines.append(
                f"**Pipeline**: {getattr(pipeline, 'pipeline_name', str(pipeline))}"
            )
            markdown_lines.append(f"**Status**: {'Success' if success else 'Failed'}")
            markdown_lines.append("")

            if not success:
                # If there was an exception, get it from the trace and include it in the report
                if trace and trace.steps:
                    last_step = trace.steps[-1]
                    if hasattr(last_step, "step_exception") and last_step.step_exception:
                        self._log(
                            logging.ERROR,
                            f"Pipeline execution failed with exception: {last_step.step_exception}",
                        )

                        markdown_lines.append("## Error Information")
                        markdown_lines.append("")
                        markdown_lines.extend(
                            self._exception_to_markdown_lines(last_step.step_exception)
                        )
                        markdown_lines.append("")
            else:
                # If successful, create summary from trace
                # Check for schema changes and include detailed schema change information
                schema_updates = get_combined_schema_updates(trace)
                has_schema_changes = any(
                    _changes_without_dlt_changes(tables) for tables in schema_updates.values()
                )
                markdown_lines.append(
                    f"**Schema Changes**: {'yes' if has_schema_changes else 'no'}"
                )
                markdown_lines.append("")

                # Print row counts dict
                markdown_lines.append("## Row Counts:")
                if summary:
                    # Convert dict to markdown format
                    for table_name, count in summary.items():
                        if not table_name.startswith("_dlt_"):
                            markdown_lines.append(f"- {table_name}: {count:,}")
                else:
                    markdown_lines.append("- No row count data available")
                markdown_lines.append("")

            markdown_content = "\n".join(markdown_lines)
            create_markdown_artifact(
                key="pipeline-final-report",
                markdown=markdown_content,
                description="Pipeline final report",
            )

        except Exception as e:
            self._log(
                logging.WARNING, f"PrefectCollector failed to create final report artifact: {e}"
            )

    #
    # Progress artifacts
    #
    def _update_progress_artifacts(self) -> None:
        """Update or create progress artifacts for each stage."""
        # Don't update progress artifacts if counters are None (already cleared)
        if not self.counters:
            return

        try:
            # Update extract progress (Resources counter)
            self._update_stage_progress("Resources", "Extract")

            # Update normalize progress (Files counter)
            self._update_stage_progress("Files", "Normalize")

            # Update load progress (Jobs counter)
            self._update_stage_progress("Jobs", "Load")

        except Exception as e:
            self._log(logging.WARNING, f"PrefectCollector progress artifact error: {e}")

    def _update_stage_progress(self, counter_name: str, stage_name: str) -> None:
        """Update progress artifact for a specific stage."""
        if counter_name not in self.counters:
            return

        progress = self._calculate_stage_progress(counter_name)
        description = self._get_stage_progress_description(counter_name, stage_name)

        if counter_name not in self.progress_artifact_ids:
            # Create new progress artifact
            self.progress_artifact_ids[counter_name] = cast(
                UUID, create_progress_artifact(progress=progress, description=description)
            )
        else:
            # Update existing progress artifact
            update_progress_artifact(
                artifact_id=self.progress_artifact_ids[counter_name], progress=progress
            )

    def _calculate_stage_progress(self, counter_name: str) -> float:
        """Calculate progress percentage for a specific counter."""
        count = self.counters.get(counter_name, 0)
        info = self.counter_info.get(counter_name)

        if info and info.total:
            # Calculate percentage based on counter with total
            return min(100.0, (count / info.total) * 100.0)
        else:
            # No total known, show 50% if processing
            return 50.0 if count > 0 else 0.0

    def _get_stage_progress_description(self, counter_name: str, stage_name: str) -> str:
        """Get description for a specific stage progress artifact."""
        # includ the total count in the description like this: `x of total Resources extracted`
        counter_info = self.counter_info.get(counter_name)
        total_count = counter_info.total if counter_info else "unknown"
        x = self.counters.get(counter_name, 0)
        if counter_name == "Resources":
            return f"{stage_name}: {x}/{total_count} Resources extracted"
        elif counter_name == "Files":
            return f"{stage_name}: {x}/{total_count} Files processed"
        elif counter_name == "Jobs":
            return f"{stage_name}: {x}/{total_count} Jobs processed"
        else:
            return f"{stage_name}: {counter_name.lower()}"

    def add_tag_for_schema_change(self) -> None:
        """Add a tag for a schema change."""
        try:
            context = get_run_context()
            if isinstance(context, TaskRunContext) and context.task_run:
                context.task_run.tags.append("schema change")
        except Exception:
            self._log(logging.WARNING, "Failed to add 'schema change' tag to Prefect task run.")
            pass


def _changes_without_dlt_changes(
    updates: Dict[str, TTableSchema],
    exclude_dlt_tables: bool = True,
    exclude_dlt_columns: bool = True,
    dlt_column_prefix: str = "_dlt_",
    dlt_tables_prefix: str = "_dlt_",
) -> Dict[str, TTableSchema]:
    """
    Convenience method to return a shallowcopy of the updates dict with all dlt-tables and/or
    columns removed.
    Args:
        updates: The updates made to all tables in the schema, e.g. from trace load packages
        exclude_dlt_tables: If True, remove tables whose name starts with _dlt_
        exclude_dlt_columns: If True, remove columns whose name starts with _dlt_
        dlt_column_prefix: as normalized in the schema, see schema._dlt_column_prefix
        dlt_tables_prefix: as normalized in the schema, see schema._dlt_tables_prefix
    Returns:
        Shallow copy of the updates dict with all dlt-tables and/or columns removed.
    """
    filtered_tables: Dict[str, TTableSchema] = {}
    for table_name, table_schema in updates.items():
        # maybe filter dlt-tables
        if exclude_dlt_tables and table_name.startswith(dlt_tables_prefix):
            continue

        # Create a shallow copy of the table schema
        filtered_table_schema = cast(
            TTableSchema, {k: v for k, v in table_schema.items() if k != "columns"}
        )

        # Handle columns separately based on filtering requirements
        if "columns" in table_schema:
            if exclude_dlt_columns:
                # Filter out dlt columns
                filtered_table_schema["columns"] = {
                    col: col_def
                    for col, col_def in table_schema["columns"].items()
                    if not col.startswith(dlt_column_prefix)
                }
            else:
                # Keep all columns but create a shallow copy
                filtered_table_schema["columns"] = table_schema["columns"].copy()
        filtered_tables[table_name] = filtered_table_schema
    return filtered_tables
