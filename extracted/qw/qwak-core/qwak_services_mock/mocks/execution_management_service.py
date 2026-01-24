from _qwak_proto.qwak.execution.v1.execution_service_pb2 import (TriggerBackfillResponse, TriggerStreamingAggregationBackfillResponse)
from _qwak_proto.qwak.execution.v1.execution_service_pb2_grpc import (
    FeatureStoreExecutionServiceServicer,
)

from grpc import RpcError


class ExecutionManagementServiceMock(FeatureStoreExecutionServiceServicer):
    def __init__(self):
        self._execution_id = None
        self._raise_exception_on_request = False

    def set_execution_id(self, execution_id: str) -> None:
        self._execution_id = execution_id

    def set_raise_exception(self):
        self._raise_exception_on_request = True

    def clear_raise_exception(self):
        self._raise_exception_on_request = False

    def TriggerBatchBackfill(self, request, context):
        if self._raise_exception_on_request:
            raise RpcError
        return TriggerBackfillResponse(execution_id=self._execution_id)

    def TriggerStreamingAggregationBackfill(self, request, context):
        if self._raise_exception_on_request:
            raise RpcError
        return TriggerStreamingAggregationBackfillResponse(
            execution_id=self._execution_id
        )
