import uuid
from typing import Optional

import grpc
from _qwak_proto.qwak.features_operator.v3.features_operator_async_service_pb2 import (
    ValidationResponse,
)
from _qwak_proto.qwak.features_operator.v3.features_operator_async_service_pb2_grpc import (
    FeaturesOperatorAsyncServiceServicer,
)


class FeaturesOperatorV3ServiceMock(FeaturesOperatorAsyncServiceServicer):
    def __init__(self):
        self.response: Optional[ValidationResponse] = None
        super(FeaturesOperatorV3ServiceMock, self).__init__()

    def given_next_response(self, response: ValidationResponse):
        self.response = response

    def ValidateDataSource(self, request, context) -> str:
        if request.num_samples <= 0 or 1_000 < request.num_samples:
            context.set_details(
                f"[NumberOfSamples must be between 0 and 1000, got {request.num_samples}]"
            )
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            return

        request_id = str(uuid.uuid4())
        return ValidationResponse(request_id=request_id)

    def ValidateFeatureSet(self, request, context):
        if request.num_samples <= 0 or 1_000 < request.num_samples:
            context.set_details(
                f"[NumberOfSamples must be between 0 and 1000, got {request.num_samples}]"
            )
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            return

        request_id = str(uuid.uuid4())
        return ValidationResponse(request_id=request_id)

    def GetValidationResult(self, request, context):
        if not request.request_id:
            context.set_details("Request handle id not found")
            context.set_code(grpc.StatusCode.FAILED_PRECONDITION)
            return

        return self.response
