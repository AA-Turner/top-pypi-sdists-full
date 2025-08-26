from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Optional, Tuple

from _qwak_proto.qwak.feature_store.sources.data_source_pb2 import (
    DataSourceSpec as ProtoDataSourceSpec,
)
from _qwak_proto.qwak.feature_store.v1.internal.data_source.data_source_service_pb2 import (
    GetDataSourceSourceCodeUploadResponse,
)
from qwak.clients.feature_store import FeatureRegistryClient
from qwak.exceptions import QwakException
from qwak.feature_store._common.artifact_utils import ArtifactSpec, ArtifactsUploader
from qwak.feature_store._common.source_code_spec import SourceCodeSpec
from qwak.feature_store._common.source_code_spec_factory import SourceCodeSpecFactory
from qwak.feature_store.data_sources.attributes import DataSourceAttributes
from qwak.feature_store.validations.validation_options import (
    DataSourceValidationOptions,
)
from qwak.feature_store.validations.validation_response import SuccessValidationResponse

if TYPE_CHECKING:
    try:
        import pandas as pd
    except ImportError:
        pass


@dataclass
class BaseSource(ABC):
    name: str
    description: str
    attributes: DataSourceAttributes = field(
        init=False, default_factory=lambda: DataSourceAttributes()
    )

    @abstractmethod
    def _to_proto(self, artifact_url: Optional[str] = None) -> ProtoDataSourceSpec:
        """
        Internal qwak function, converts this BaseSource instance to its protobuf representation.
        Args:
            artifact_url: provided if this base source artifact has already been uploaded
            data_source_definition_path: path to the module instantiating this base source
        """
        pass

    def _get_artifacts(self) -> Optional["ArtifactSpec"]:
        return None

    def _upload_artifact(self) -> Optional[str]:
        artifact: Optional["ArtifactSpec"] = self._get_artifacts()
        if artifact:
            return ArtifactsUploader.upload(artifact)

    def _prepare_and_get(
        self,
        artifact_url: Optional[str] = None,
        source_definition_path: Optional[Path] = None,
    ) -> Tuple[ProtoDataSourceSpec, Optional[str]]:
        uploaded_artifact_url: Optional[str] = artifact_url

        if not artifact_url:
            uploaded_artifact_url = self._upload_artifact()

        if source_definition_path:
            code_upload_args: (
                GetDataSourceSourceCodeUploadResponse
            ) = FeatureRegistryClient().get_datasource_source_code_presign_url(
                ds_name=self.name, repository_name=getattr(self, "repository")
            )
            source_code_spec: SourceCodeSpec = (
                SourceCodeSpecFactory.get_zip_source_code_spec(
                    main_entity_path=source_definition_path,
                    url=code_upload_args.upload_url,
                    extra_headers=code_upload_args.extra_headers,
                )
            )

            self.attributes = DataSourceAttributes(source_code_spec=source_code_spec)

        proto_spec: ProtoDataSourceSpec = self._to_proto(
            artifact_url=uploaded_artifact_url
        )

        proto_spec.MergeFrom(
            ProtoDataSourceSpec(data_source_attributes=self.attributes._to_proto())
        )

        return proto_spec, uploaded_artifact_url

    @classmethod
    @abstractmethod
    def _from_proto(cls, proto):
        pass

    def get_sample(
        self,
        number_of_rows: int = 10,
        validation_options: Optional[DataSourceValidationOptions] = None,
    ) -> "pd.DataFrame":
        """
        Tries to get a sample of length `number_rows` from the data source.
        Args:
            number_of_rows: number of rows to get from data source
            validation_options: validation options
        Returns:
            A tuple containing the resulting dataframe and a tuple of the columns names and types.
            (the types are pyspark dataframe types)
        """
        from qwak.feature_store.validations.validator import FeaturesOperatorValidator

        v = FeaturesOperatorValidator()

        response, _ = v.validate_data_source(
            data_source=self,
            sample_size=number_of_rows,
            validation_options=validation_options,
            silence_specific_exceptions=False,
        )

        if isinstance(response, SuccessValidationResponse):
            return response.sample
        else:
            raise QwakException(f"Sampling failed: \n{response}")
