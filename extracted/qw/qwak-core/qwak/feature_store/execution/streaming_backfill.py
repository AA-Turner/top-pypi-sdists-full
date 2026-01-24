import pathlib

from qwak.clients.feature_store.execution_management_client import (
    ExecutionManagementClient,
)
from qwak.feature_store.feature_sets.streaming_backfill import StreamingBackfill


class StreamingAggregationBackfill:
    def __init__(
        self,
        streaming_backfill: StreamingBackfill,
        source_definition_path: pathlib.Path,
    ):
        """
        Initialize the streaming aggregation backfill executor.

        Args:
            streaming_backfill (StreamingBackfill): Specification containing the
                              featureset name, time range, data sources, and transformation
            source_definition_path (Path): Path to the Python file containing the backfill
                                   definition. Required for locating UDF artifacts.
        """
        self._streaming_backfill = streaming_backfill
        self._source_definition_path = source_definition_path

    def trigger(self) -> str:
        """
        Triggers the streaming aggregation backfill execution.

        Converts the backfill specification to proto format and sends it to
        the execution manager to start the backfill job.

        Returns:
            str: The execution ID for tracking the backfill job status

        Raises:
            QwakException: If the execution manager request fails
        """
        backfill_proto = self._streaming_backfill._to_proto(
            str(self._source_definition_path)
        )

        execution_client = ExecutionManagementClient()
        response = execution_client.trigger_streaming_aggregation_backfill(
            backfill_proto
        )
        return response.execution_id
