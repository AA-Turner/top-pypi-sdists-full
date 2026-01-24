from _qwak_proto.qwak.execution.v1.backfill_pb2 import BackfillSpec
from _qwak_proto.qwak.execution.v1.streaming_aggregation_pb2 import (
    StreamingAggregationBackfillIngestion,
)
from _qwak_proto.qwak.execution.v1.batch_pb2 import BatchIngestion
from _qwak_proto.qwak.execution.v1.execution_service_pb2 import (
    GetExecutionEntryRequest,
    GetExecutionEntryResponse,
    GetExecutionStatusRequest,
    GetExecutionStatusResponse,
    TriggerBackfillRequest,
    TriggerBackfillResponse,
    TriggerBatchFeaturesetRequest,
    TriggerBatchFeaturesetResponse,
    TriggerStreamingAggregationBackfillRequest,
    TriggerStreamingAggregationBackfillResponse,
)
from _qwak_proto.qwak.execution.v1.execution_service_pb2_grpc import (
    FeatureStoreExecutionServiceStub,
)
from dependency_injector.wiring import Provide
from grpc import RpcError
from qwak.exceptions import QwakException
from qwak.inner.di_configuration import QwakContainer


class ExecutionManagementClient:
    """
    Used for interacting with the execution manager endpoints
    """

    def __init__(self, grpc_channel=Provide[QwakContainer.core_grpc_channel]):
        self._feature_store_execution_service = FeatureStoreExecutionServiceStub(
            grpc_channel
        )

    def trigger_streaming_aggregation_backfill(
        self, backfill_ingestion: StreamingAggregationBackfillIngestion
    ) -> TriggerStreamingAggregationBackfillResponse:
        """
        Receives a configured streaming aggregation backfill proto and triggers a streaming aggregation
        backfill against the execution manager

        Args:
            backfill_ingestion (StreamingAggregationBackfillIngestion): A protobuf message
                containing the backfill specification details

        Returns:
            TriggerStreamingAggregationBackfillResponse: response object from the execution manager
        """
        try:
            return self._feature_store_execution_service.TriggerStreamingAggregationBackfill(
                TriggerStreamingAggregationBackfillRequest(backfill=backfill_ingestion)
            )
        except RpcError as e:
            raise QwakException(
                f"Failed to trigger streaming aggregation backfill job, error encountered {e}"
            )

    def trigger_batch_backfill(
        self, batch_backfill_spec: BackfillSpec
    ) -> TriggerBackfillResponse:
        """
        Receives a configured batch back-fill spec proto and triggers a batch back-fill against the execution manager
        @param batch_backfill_spec: a proto message containing the backfilll specification details
        @type batch_backfill_spec: BackfillSpec
        @return: response object from the execution manager
        @rtype: TriggerBackfillResponse
        """
        try:
            return self._feature_store_execution_service.TriggerBatchBackfill(
                TriggerBackfillRequest(backfill_spec=batch_backfill_spec)
            )
        except RpcError as e:
            raise QwakException(
                f"Failed to trigger batch backfill job, error encountered {e}"
            )

    def trigger_batch_featureset(
        self, batch_ingestion: BatchIngestion
    ) -> TriggerBatchFeaturesetResponse:
        """
        Receives a configured batch ingestion proto and triggers a batch job against the execution manager. This can be
        used both for manual and scheduled batch job executions.
        @param batch_ingestion: a proto message containing the batch job specification
        @type batch_ingestion: BatchIngestion
        @return: response object from the execution manager
        @rtype: TriggerBatchFeaturesetResponse
        """
        try:
            return self._feature_store_execution_service.TriggerBatchFeatureset(
                TriggerBatchFeaturesetRequest(batch_ingestion=batch_ingestion)
            )
        except RpcError as e:
            raise QwakException(f"Failed to trigger batch job, error encountered {e}")

    def get_execution_status(self, execution_id: str) -> GetExecutionStatusResponse:
        """

        @param execution_id: the execution id for which we're querying the execution status
        @type execution_id: str
        @return: response received from the execution manager
        @rtype: GetExecutionStatusResponse
        """
        try:
            return self._feature_store_execution_service.GetExecutionStatus(
                GetExecutionStatusRequest(execution_id=execution_id)
            )
        except RpcError as e:
            raise QwakException(
                f"Failed to get execution status, error encountered {e}"
            )

    def get_execution_entry(self, execution_id: str) -> GetExecutionEntryResponse:
        """

        @param execution_id: the execution id for which we're querying the execution status
        @type execution_id: str
        @return: response received from the execution manager
        @rtype: GetExecutionStatusResponse
        """
        try:
            return self._feature_store_execution_service.GetExecutionEntry(
                GetExecutionEntryRequest(execution_id=execution_id)
            )
        except RpcError as e:
            raise QwakException(f"Failed to get execution entry, error encountered {e}")
