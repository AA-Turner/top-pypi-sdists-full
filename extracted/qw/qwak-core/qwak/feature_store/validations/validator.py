from abc import ABC, abstractmethod
from typing import Optional, Tuple

from _qwak_proto.qwak.features_operator.v3.features_operator_async_service_pb2 import (
    GetValidationResultResponse as ProtoGetValidationResultResponse,
)
from qwak.clients.feature_store import FeatureRegistryClient
from qwak.clients.feature_store.operator_client import FeaturesOperatorClient
from qwak.exceptions import QwakException
from qwak.feature_store.data_sources.base import BaseSource
from qwak.feature_store.feature_sets.base_feature_set import BaseFeatureSet
from qwak.feature_store.validations.validation_decorators import (
    silence_backend_specific_validation_exceptions,
)
from qwak.feature_store.validations.validation_options import (
    DataSourceValidationOptions,
    FeatureSetValidationOptions,
)
from qwak.feature_store.validations.validation_response import (
    ValidationResponse,
    ValidationResponseFactory,
)


class Validator(ABC):
    @abstractmethod
    def validate_featureset(
        self,
        featureset: BaseFeatureSet,
        sample_size: int = 10,
        validation_options: Optional[FeatureSetValidationOptions] = None,
    ) -> Tuple[ValidationResponse, Optional[str]]:
        pass

    @abstractmethod
    def validate_data_source(
        self,
        data_source: BaseSource,
        sample_size: int = 10,
        validation_options: Optional[DataSourceValidationOptions] = None,
    ) -> Tuple[ValidationResponse, Optional[str]]:
        pass


class FeaturesOperatorValidator(Validator):
    _operator_client: FeaturesOperatorClient
    _registry_client: FeatureRegistryClient

    def __init__(self):
        try:
            import pandas  # noqa: F401
        except ImportError:
            raise QwakException("Missing required Pandas dependency")

        self._operator_client = FeaturesOperatorClient()
        self._registry_client = FeatureRegistryClient()

    @silence_backend_specific_validation_exceptions(
        "Validating DataSource is not supported for self-hosted environments"
    )
    def validate_data_source(
        self,
        data_source: BaseSource,
        sample_size: int = 10,
        validation_options: Optional[DataSourceValidationOptions] = None,
    ) -> Tuple[ValidationResponse, Optional[str]]:
        if sample_size <= 0 or 1_000 < sample_size:
            raise ValueError(
                f"sample_size must be under 1000 and positive, got: {sample_size}"
            )
        artifact_url: Optional[str] = None
        data_source_spec, artifact_url = data_source._prepare_and_get()
        proto_response: ProtoGetValidationResultResponse = (
            self._operator_client.validate_data_source_blocking(
                data_source_spec=data_source_spec,
                num_samples=sample_size,
                validation_options=(
                    validation_options.to_proto() if validation_options else None
                ),
            )
        )

        return ValidationResponseFactory.from_proto(proto_response), artifact_url

    @silence_backend_specific_validation_exceptions(
        "Validating FeatureSet is not supported for self-hosted environments"
    )
    def validate_featureset(
        self,
        featureset: BaseFeatureSet,
        sample_size: int = 10,
        validation_options: Optional[FeatureSetValidationOptions] = None,
    ) -> Tuple[ValidationResponse, Optional[str]]:
        if sample_size <= 0 or 1_000 < sample_size:
            raise ValueError(
                f"sample_size must be under 1000 and positive, got: {sample_size}"
            )
        artifact_url: Optional[str] = None
        featureset_spec, artifact_url = featureset._to_proto(
            feature_registry=self._registry_client, features=None, git_commit=None
        )

        proto_response: ProtoGetValidationResultResponse = (
            self._operator_client.validate_featureset_blocking(
                featureset_spec=featureset_spec,
                resource_path=artifact_url,
                num_samples=sample_size,
                validation_options=(
                    validation_options.to_proto() if validation_options else None
                ),
            )
        )

        return ValidationResponseFactory.from_proto(proto_response), artifact_url
