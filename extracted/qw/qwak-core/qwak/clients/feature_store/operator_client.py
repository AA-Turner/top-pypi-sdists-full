from typing import Optional

from _qwak_proto.qwak.feature_store.features.feature_set_pb2 import FeatureSetSpec
from _qwak_proto.qwak.feature_store.sources.data_source_pb2 import DataSourceSpec
from _qwak_proto.qwak.features_operator.v3.features_operator_async_service_pb2 import (
    DataSourceValidationOptions,
    FeatureSetValidationOptions,
    GetValidationResultRequest,
    GetValidationResultResponse,
    ValidateDataSourceRequest,
    ValidateFeatureSetRequest,
    ValidationResponse,
)
from _qwak_proto.qwak.features_operator.v3.features_operator_async_service_pb2_grpc import (
    FeaturesOperatorAsyncServiceStub,
)
from _qwak_proto.qwak.features_operator.v3.features_operator_pb2 import (
    ValidationNotReadyResponse,
)
from dependency_injector.wiring import Provide
from qwak.inner.di_configuration import QwakContainer
from qwak.inner.tool.grpc.grpc_try_wrapping import grpc_try_catch_wrapper
from qwak.inner.tool.retry_utils import retry


class ValidationNotReadyException(Exception):
    pass


class ValidationTimeoutException(Exception):
    pass


class FeaturesOperatorClient:
    """
    Validates and samples features store objects like: data sources and feature sets.
    """

    def __init__(self, grpc_channel=Provide[QwakContainer.core_grpc_channel]):
        self._v3_client = FeaturesOperatorAsyncServiceStub(grpc_channel)

    @grpc_try_catch_wrapper(
        "Failed to validate DataSource", reraise_non_grpc_error_original_exception=True
    )
    def validate_data_source(
        self,
        data_source_spec: DataSourceSpec,
        num_samples: int = 10,
        validation_options: Optional[DataSourceValidationOptions] = None,
    ) -> str:
        """
        Validates and fetches a sample from the data source
        :return: Request handle id to poll for result with
        """
        request: ValidateDataSourceRequest = ValidateDataSourceRequest(
            data_source_spec=data_source_spec,
            num_samples=num_samples,
            validation_options=validation_options,
        )
        response: ValidationResponse = self._v3_client.ValidateDataSource(request)
        return response.request_id

    @grpc_try_catch_wrapper(
        "Failed to validate FeatureSet", reraise_non_grpc_error_original_exception=True
    )
    def validate_featureset(
        self,
        featureset_spec: FeatureSetSpec,
        resource_path: Optional[str] = None,
        num_samples: int = 10,
        validation_options: Optional[FeatureSetValidationOptions] = None,
    ) -> str:
        """
        Validates and fetches a sample from the featureset
        :return: Request handle id to poll for result with
        """
        request: ValidateFeatureSetRequest = ValidateFeatureSetRequest(
            feature_set_spec=featureset_spec,
            num_samples=num_samples,
            zip_path=resource_path,
            validation_options=validation_options,
        )

        response: ValidationResponse = self._v3_client.ValidateFeatureSet(request)
        return response.request_id

    @grpc_try_catch_wrapper(
        "Failed to fetch validation result",
        reraise_non_grpc_error_original_exception=True,
    )
    def get_result(self, request_handle: str) -> GetValidationResultResponse:
        """
        Try to fetch the validation result using the given request handle.
        :return: the validation result
        """
        request: GetValidationResultRequest = GetValidationResultRequest(
            request_id=request_handle
        )
        response: GetValidationResultResponse = self._v3_client.GetValidationResult(
            request
        )

        return response

    def _inner_poll(self, request_handle: str) -> GetValidationResultResponse:
        response: GetValidationResultResponse = self.get_result(
            request_handle=request_handle
        )
        response_type = getattr(response, response.WhichOneof("type"))

        if isinstance(response_type, ValidationNotReadyResponse):
            raise ValidationNotReadyException()

        return response

    def poll_for_result(
        self,
        request_handle: str,
        timeout_seconds: int = 5 * 60,
        poll_interval_seconds: int = 3,
    ) -> GetValidationResultResponse:
        """
        Retry wrapper on 'get_result' method that polls for the validation result
        :return: the validation result
        """
        try:
            result = retry(
                f=self._inner_poll,
                kwargs={"request_handle": request_handle},
                exceptions=ValidationNotReadyException,
                attempts=timeout_seconds / poll_interval_seconds,
                delay=poll_interval_seconds,
            )
        except ValidationNotReadyException:
            raise ValidationTimeoutException(
                f"Validation timed out. Qwak limits validation execution time to {timeout_seconds} seconds"
            )

        return result

    def validate_data_source_blocking(
        self,
        data_source_spec: DataSourceSpec,
        num_samples: int = 10,
        timeout_seconds: int = 5 * 60,
        poll_interval_seconds: int = 3,
        validation_options: Optional[DataSourceValidationOptions] = None,
    ) -> GetValidationResultResponse:
        request_handle: str = self.validate_data_source(
            data_source_spec=data_source_spec,
            num_samples=num_samples,
            validation_options=validation_options,
        )

        return self.poll_for_result(
            request_handle=request_handle,
            timeout_seconds=timeout_seconds,
            poll_interval_seconds=poll_interval_seconds,
        )

    def validate_featureset_blocking(
        self,
        featureset_spec: FeatureSetSpec,
        resource_path: Optional[str] = None,
        num_samples: int = 10,
        timeout_seconds: int = 5 * 60,
        poll_interval_seconds: int = 3,
        validation_options: Optional[FeatureSetValidationOptions] = None,
    ) -> GetValidationResultResponse:
        request_handle: str = self.validate_featureset(
            featureset_spec=featureset_spec,
            resource_path=resource_path,
            num_samples=num_samples,
            validation_options=validation_options,
        )

        return self.poll_for_result(
            request_handle=request_handle,
            timeout_seconds=timeout_seconds,
            poll_interval_seconds=poll_interval_seconds,
        )
