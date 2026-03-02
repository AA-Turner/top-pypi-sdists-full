from typing import Any, Dict, Union, TextIO, Optional
import sys
import logging

from dlt.common.runtime.collector import LogCollector
from dlt.common.schema.typing import TTableSchema
from dlt.common.pipeline import SupportsPipeline
from dlt.common.utils import RowCounts
from dlt.pipeline.trace import PipelineTrace, PipelineStepTrace

from .trace_helpers import _has_schema_changes, get_combined_schema_updates


class PlusLogCollector(LogCollector):
    """
    A basic collector-class that users can inherit from to implement their own callbacks
    The Four callbacks from SupportsTracking-Protocol are called during the pipeline
    execution:
    - on_start_trace(trace, step, pipeline)
    - on_start_trace_step(trace, step, pipline)
    - on_end_trace_step(trace, step, pipeline, step_info, send_state)
    - on_end_trace(trace, pipeline, send_state)
    one additional callback, called after load-stage, if schema update is detected:
    - on_schema_change(pipeline, trace, schema_name, changes)
    and three methods that get called from the PipelineRunner:
    - on_retry(pipeline, trace, retry_attempt, last_attempt, exception)
    - on_before(pipeline)
    - on_after(pipeline, trace, success, summary)
    The other methods are optional.

    Example:
    class MyLogCollector(PlusLogCollector):
        def on_schema_change(
            self,
            pipeline: SupportsPipeline,
            trace: PipelineTrace,
            schema_name: str,
            changes: Dict[str, TTableSchema]
        ) -> None:
            # Custom logic for handling schema changes
            ...
    """

    def __init__(
        self,
        log_period: float = 1.0,
        logger: Union[logging.Logger, TextIO] = sys.stdout,
        log_level: int = logging.INFO,
        dump_system_stats: bool = True,
        extra_info: Optional[Dict[str, Dict[str, str]]] = None,
    ) -> None:
        super().__init__(
            log_period=log_period,
            logger=logger,
            log_level=log_level,
            dump_system_stats=dump_system_stats,
        )
        self.extra_info = extra_info or {}

    def on_end_trace_step(
        self,
        trace: PipelineTrace,
        step: PipelineStepTrace,
        pipeline: SupportsPipeline,
        step_info: Any,
        send_state: bool,
    ) -> None:
        """
        Note: If you overwrite this method, make sure to call super().on_end_trace_step() to
        maintain the functionality of the on_schema_change()-callback.
        """
        # for now we only care about schema changes during the load step
        if step.step == "load":
            if _has_schema_changes(trace):
                changes_by_schema = get_combined_schema_updates(trace)
                for schema_name, changes in changes_by_schema.items():
                    self.on_schema_change(pipeline, trace, schema_name, changes)

    # these are the methods that a user should implement for their own callbacks
    def on_schema_change(
        self,
        pipeline: SupportsPipeline,
        trace: PipelineTrace,
        schema_name: str,
        changes: Dict[str, TTableSchema],
    ) -> None:
        """
        Called whenever a schema change is detected in one of the load packages during the load
        step of the pipeline.
        Args:
            pipeline: The pipeline instance
            trace: The pipeline trace
            schema_name: The name of the schema that has changed
            changes: schema changes by table
        """
        pass

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
        Args:
            pipeline: The pipeline instance
            trace: The pipeline trace
            step: The current step in the pipeline
            retry_attempt: The current retry attempt number
            last_attempt: Whether this is the last retry attempt
            exception: The exception that triggered the retry
        """
        pass

    def on_before(
        self,
        pipeline: SupportsPipeline,
    ) -> None:
        """
        Called before the pipeline starts for the very first time.
        Will not be called on retries.
        Args:
            pipeline: The pipeline instance
        """
        pass

    def on_after(
        self,
        pipeline: SupportsPipeline,
        trace: PipelineTrace,
        success: bool,
        summary: RowCounts,
    ) -> None:
        """
        Called after the pipeline has finished running, successfully or not. Will not be called on
        retries.
        If a run produced no trace, the success parameter will be False.
        Args:
            pipeline: The pipeline instance
            trace: The pipeline trace
            success: Whether the pipeline run was successful (without errors)
            summary: A summary of the pipeline run
        """
        pass

    def set_extra_info(self, extra_info: Dict[str, Dict[str, str]]) -> None:
        """
        Sets the extra_info attribute. You can also pass extra_info directly to __init__().
        Args:
            extra_info: Dictionary with format {title: {key: value}} for rendering sections
        """
        self.extra_info = extra_info
