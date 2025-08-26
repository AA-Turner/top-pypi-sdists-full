from _qwak_proto.qwak.feature_store.entities.entity_pb2 import EntitySpec
from _qwak_proto.qwak.feature_store.entities.entity_service_pb2 import (
    CreateEntityRequest,
    CreateEntityResponse,
    DeleteEntityRequest,
    DeleteEntityResponse,
    GetEntityByNameRequest,
    GetEntityByNameResponse,
    ListEntitiesRequest,
    ListEntitiesResponse,
    UpdateEntityRequest,
    UpdateEntityResponse,
)
from _qwak_proto.qwak.feature_store.entities.entity_service_pb2_grpc import (
    EntityServiceStub,
)
from _qwak_proto.qwak.feature_store.features.feature_set_pb2 import FeatureSetSpec
from _qwak_proto.qwak.feature_store.features.feature_set_service_pb2 import (
    CreateUploadURLRequestV1,
    DeleteFeatureSetRequest,
    DeleteFeatureSetResponse,
    DeleteFeaturesetVersionRequest,
    GetEnvToFeatureSetsMappingRequest,
    GetEnvToFeatureSetsMappingResponse,
    GetFeatureSetByNameRequest,
    GetFeatureSetByNameResponse,
    GetFeaturesetSchedulingStateRequest,
    GetFeaturesetSchedulingStateResponse,
    ListFeatureSetsRequest,
    ListFeatureSetsResponse,
    ListFeaturesetVersionsByNameRequest,
    ListFeaturesetVersionsByNameResponse,
    PauseFeaturesetRequest,
    RegisterFeatureSetRequest,
    RegisterFeatureSetResponse,
    ResumeFeaturesetRequest,
    RunBatchFeatureSetRequest,
    RunBatchFeatureSetResponse,
    RunParquetBatchFeatureSetRequest,
    SetActiveFeaturesetVersionRequest,
    UpdateFeatureSetRequest,
    UpdateFeatureSetResponse,
)
from _qwak_proto.qwak.feature_store.features.feature_set_service_pb2_grpc import (
    FeatureSetServiceStub,
)
from _qwak_proto.qwak.feature_store.features.feature_set_types_pb2 import (
    Transformation as ProtoTransformation,
)
from _qwak_proto.qwak.feature_store.sources.data_source_service_pb2 import (
    CreateDataSourceRequest,
    CreateDataSourceResponse,
    CreateDataSourceUploadURLRequest,
    DeleteDataSourceRequest,
    DeleteDataSourceResponse,
    GetDataSourceByNameRequest,
    GetDataSourceByNameResponse,
    ListDataSourcesRequest,
    ListDataSourcesResponse,
    UpdateDataSourceRequest,
    UpdateDataSourceResponse,
)
from _qwak_proto.qwak.feature_store.sources.data_source_service_pb2_grpc import (
    DataSourceServiceStub,
)
from _qwak_proto.qwak.feature_store.v1.internal.data_source.data_source_service_pb2 import (
    GetDataSourceSourceCodeUploadRequest,
    GetDataSourceSourceCodeUploadResponse,
)
from _qwak_proto.qwak.feature_store.v1.internal.data_source.data_source_service_pb2_grpc import (
    DataSourceServiceStub as InternalDataSourceServiceStub,
)
from dependency_injector.wiring import Provide
from grpc import RpcError, StatusCode
from qwak.exceptions import QwakException
from qwak.inner.di_configuration import QwakContainer
from qwak.inner.tool.grpc.grpc_try_wrapping import grpc_try_catch_wrapper


class FeatureRegistryClient:
    """
    Used for interacting with Feature Registry endpoints
    """

    def __init__(self, grpc_channel=Provide[QwakContainer.core_grpc_channel]):
        self._features_service = FeatureSetServiceStub(grpc_channel)
        self._entity_service = EntityServiceStub(grpc_channel)
        self._sources_service = DataSourceServiceStub(grpc_channel)
        self._internal_data_sources_service = InternalDataSourceServiceStub(
            grpc_channel
        )

    @grpc_try_catch_wrapper(
        "Failed to get a presigned url", reraise_non_grpc_error_original_exception=True
    )
    def get_datasource_source_code_presign_url(
        self, ds_name: str, repository_name: str
    ) -> GetDataSourceSourceCodeUploadResponse:
        return self._internal_data_sources_service.GetDataSourceSourceCodeUploadURL(
            GetDataSourceSourceCodeUploadRequest(
                data_source_name=ds_name, repository_name=repository_name
            )
        )

    @grpc_try_catch_wrapper(
        "Failed to list features", reraise_non_grpc_error_original_exception=True
    )
    def list_feature_sets(self) -> ListFeatureSetsResponse:
        """
        Returns:
            ListFeatureSetsResponse
        """
        return self._features_service.ListFeatureSets(ListFeatureSetsRequest())

    def get_entity_by_name(self, entity_name: str) -> GetEntityByNameResponse:
        """
        Args:
            entity_name: entity name to get
        Returns:
            GetEntityByNameResponse
        """
        return self._fetch_by_name(
            lambda name: self._entity_service.GetEntityByName(
                GetEntityByNameRequest(entity_name=name)
            ),
            entity_name,
            "entity",
        )

    @grpc_try_catch_wrapper(
        "Failed to delete feature", reraise_non_grpc_error_original_exception=True
    )
    def delete_feature_set(self, feature_set_id: str) -> DeleteFeatureSetResponse:
        """
        Args:
            feature_set_id: feature set id to delete
        Returns:
            DeleteFeatureSetResponse
        """
        return self._features_service.DeleteFeatureSet(
            DeleteFeatureSetRequest(feature_set_id=feature_set_id)
        )

    @grpc_try_catch_wrapper(
        "Failed to delete entity", reraise_non_grpc_error_original_exception=True
    )
    def delete_entity(self, entity_id: str) -> DeleteEntityResponse:
        """
        Args:
            entity_id: entity id to delete
        Returns:
            DeleteEntityResponse
        """
        return self._entity_service.DeleteEntity(
            DeleteEntityRequest(entity_id=entity_id)
        )

    @grpc_try_catch_wrapper(
        "Failed to delete data source", reraise_non_grpc_error_original_exception=True
    )
    def delete_data_source(self, data_source_id: str) -> DeleteDataSourceResponse:
        """
        Args:
            data_source_id: data source id to delete
        Returns:
            DeleteDataSourceResponse
        """
        return self._sources_service.DeleteDataSource(
            DeleteDataSourceRequest(data_source_id=data_source_id)
        )

    @grpc_try_catch_wrapper(
        "Failed to run feature", reraise_non_grpc_error_original_exception=True
    )
    def run_feature_set(self, feature_set_name: str) -> RunBatchFeatureSetResponse:
        """
        Trigger a single ETL run for that feature set name
        Args:
            feature_set_name: feature set name to run
        Returns:
            :return RunBatchFeatureSetResponse with the execution id
        """
        return self._features_service.RunBatchFeatureSet(
            RunBatchFeatureSetRequest(feature_set_name=feature_set_name)
        )

    @grpc_try_catch_wrapper(
        "Failed to run feature", reraise_non_grpc_error_original_exception=True
    )
    def run_parquet_batch_feature_set(
        self, feature_set_name: str, parquet_location: str, timestamp_column: str
    ):
        """
        Trigger a single ETL run on an explicit parquet source for that feature set name
        Args:
            feature_set_name: feature set name to run
            parquet_location: parquet location to read from
            timestamp_column: the name of the timestamp column
        Returns:
            None
        """
        self._features_service.RunParquetBatchFeatureSet(
            RunParquetBatchFeatureSetRequest(
                feature_set_name=feature_set_name,
                parquet_location=parquet_location,
                timestamp_column=timestamp_column,
            )
        )

    @grpc_try_catch_wrapper(
        "Failed to update entity", reraise_non_grpc_error_original_exception=True
    )
    def update_entity(
        self, entity_id: str, proto_entity_spec: EntitySpec
    ) -> UpdateEntityResponse:
        """
        Args:
            entity_id: entity id to update
            proto_entity_spec: entity spec proto to update
        Returns:
            UpdateEntityResponse
        """
        return self._entity_service.UpdateEntity(
            UpdateEntityRequest(entity_id=entity_id, entity_spec=proto_entity_spec)
        )

    @grpc_try_catch_wrapper(
        "Failed to create entity", reraise_non_grpc_error_original_exception=True
    )
    def create_entity(self, proto_entity_spec: EntitySpec) -> CreateEntityResponse:
        """
        Args:
            proto_entity_spec: entity spec proto to create
        Returns:
            CreateEntityResponse
        """
        return self._entity_service.CreateEntity(
            CreateEntityRequest(entity_spec=proto_entity_spec)
        )

    @grpc_try_catch_wrapper(
        "Failed to list entities", reraise_non_grpc_error_original_exception=True
    )
    def list_entities(self) -> ListEntitiesResponse:
        """
        Returns:
             ListEntitiesResponse
        """
        return self._entity_service.ListEntities(ListEntitiesRequest())

    @grpc_try_catch_wrapper(
        "Failed to list data sources", reraise_non_grpc_error_original_exception=True
    )
    def list_data_sources(self) -> ListDataSourcesResponse:
        """
        Returns:
            ListDataSourcesResponse
        """
        return self._sources_service.ListDataSources(ListDataSourcesRequest())

    def get_data_source_by_name(
        self, data_source_name: str
    ) -> GetDataSourceByNameResponse:
        """
        Args:
            data_source_name: data source name to get
        Returns:
            GetDataSourceByNameResponse
        """
        return self._fetch_by_name(
            lambda name: self._sources_service.GetDataSourceByName(
                GetDataSourceByNameRequest(data_source_name=name)
            ),
            data_source_name,
            "data source",
        )

    @grpc_try_catch_wrapper(
        "Failed to update data source", reraise_non_grpc_error_original_exception=True
    )
    def update_data_source(
        self,
        data_source_id,
        proto_data_source: FeatureSetSpec,
    ) -> UpdateDataSourceResponse:
        """
        Args:
            data_source_id: data source id to update
            proto_data_source: proto data source spec to update
        Returns:
             UpdateDataSourceResponse
        """
        return self._sources_service.UpdateDataSource(
            UpdateDataSourceRequest(
                data_source_id=data_source_id,
                data_source_spec=proto_data_source,
            )
        )

    @grpc_try_catch_wrapper(
        "Failed to create data source", reraise_non_grpc_error_original_exception=True
    )
    def create_data_source(
        self, proto_data_source: FeatureSetSpec
    ) -> CreateDataSourceResponse:
        """
        Args:
            proto_data_source: proto data source spec to create
        Returns:
            CreateDataSourceResponse
        """
        return self._sources_service.CreateDataSource(
            CreateDataSourceRequest(data_source_spec=proto_data_source)
        )

    def get_feature_set_by_name(self, feature_set_name) -> GetFeatureSetByNameResponse:
        """
        Args:
            feature_set_name: feature set name to get
        Returns:
             GetFeatureSetByNameResponse
        """
        return self._fetch_by_name(
            lambda name: self._features_service.GetFeatureSetByName(
                GetFeatureSetByNameRequest(feature_set_name=name)
            ),
            feature_set_name,
            "feature set",
        )

    @grpc_try_catch_wrapper(
        "Failed to update feature set", reraise_non_grpc_error_original_exception=True
    )
    def update_feature_set(
        self,
        feature_set_id: str,
        proto_feature_set: FeatureSetSpec,
    ) -> UpdateFeatureSetResponse:
        """
        Args:
            feature_set_id: feature set id to update
            proto_feature_set: features set to proto serialization
        Returns:
            UpdateFeatureSetResponse
        """
        return self._features_service.UpdateFeatureSet(
            UpdateFeatureSetRequest(
                feature_set_id=feature_set_id, feature_set_spec=proto_feature_set
            )
        )

    @grpc_try_catch_wrapper(
        "Failed to create feature set", reraise_non_grpc_error_original_exception=True
    )
    def create_feature_set(
        self, proto_feature_set: FeatureSetSpec
    ) -> RegisterFeatureSetResponse:
        """
        Args:
            proto_feature_set: features set to proto serialization
        Returns:
            RegisterFeatureSetResponse
        """
        return self._features_service.RegisterFeatureSet(
            RegisterFeatureSetRequest(feature_set_spec=proto_feature_set)
        )

    @staticmethod
    def _fetch_by_name(extract_function, name, fs_object_type):
        """
        Args:
            extract_function: function to run on name param
            name: name of object to fetch
            fs_object_type: fs object type for exception reporting
        Returns:
            extract_function output
        """
        try:
            return extract_function(name)
        except RpcError as e:
            if e.code() == StatusCode.NOT_FOUND:
                return None
            else:
                raise QwakException(
                    f"Failed to fetch {fs_object_type} by name [{name}], error code: [{e.details()}]"
                )

    def get_presigned_url_v1(
        self, feature_set_name: str, transformation: ProtoTransformation
    ) -> str:
        """
        Get presigned url according feature set name and transformation type
        @param feature_set_name: featureset name for which we're getting the presigned URL
        @type feature_set_name: str
        @param transformation: The proto object of the transformation for which we're getting the presigned URL
        @type transformation: ProtoTransformation
        @return:
        @rtype:
        """
        try:
            return self._features_service.CreateUploadURLV1(
                CreateUploadURLRequestV1(
                    featureset_name=feature_set_name,
                    transformation=transformation,
                )
            ).upload_url
        except RpcError as e:
            raise QwakException(
                f"Failed to get presigned url for featureset name {feature_set_name} and transformation type "
                f"{type(transformation)}, error code: [{e.details()}]"
            )

    @grpc_try_catch_wrapper(
        "Failed to get presigned url for data source: {data_source_name}, object name: {object_name}",
        reraise_non_grpc_error_original_exception=True,
    )
    def get_data_source_presigned_url_v1(
        self, data_source_name: str, object_name: str
    ) -> str:
        """
        create a pre-sign url for data source according to qwak path convention that includes a timestamp millis
        to avoid using the same path. This method is meant to be used by the new sdk, which passes the path along
        in the proto message.
        Args:
            data_source_name: str:  data source name
            object_name: str object name
        Returns:
            presigned url: str
        """
        return self._sources_service.CreateDataSourceUploadURLV1(
            CreateDataSourceUploadURLRequest(
                data_source_name=data_source_name, object_name=object_name
            )
        ).upload_url

    @grpc_try_catch_wrapper(
        "Failed to query scheduling state for Featureset {feature_set_name}",
        reraise_non_grpc_error_original_exception=True,
    )
    def get_feature_set_scheduling_state(
        self, feature_set_name: str
    ) -> GetFeaturesetSchedulingStateResponse:
        return self._features_service.GetFeaturesetSchedulingState(
            GetFeaturesetSchedulingStateRequest(featureset_name=feature_set_name)
        )

    @grpc_try_catch_wrapper(
        "Failed to pause Featureset {feature_set_name}",
        reraise_non_grpc_error_original_exception=True,
    )
    def pause_feature_set(self, feature_set_name: str):
        self._features_service.PauseFeatureset(
            PauseFeaturesetRequest(featureset_name=feature_set_name)
        )

    @grpc_try_catch_wrapper(
        "Failed to resume Featureset {feature_set_name}",
        reraise_non_grpc_error_original_exception=True,
    )
    def resume_feature_set(self, feature_set_name: str):
        self._features_service.ResumeFeatureset(
            ResumeFeaturesetRequest(featureset_name=feature_set_name)
        )

    @grpc_try_catch_wrapper(
        "Failed list Featureset versions for Featureset: {featureset_name}",
        reraise_non_grpc_error_original_exception=True,
    )
    def list_featureset_versions(
        self, featureset_name: str
    ) -> ListFeaturesetVersionsByNameResponse:
        return self._features_service.ListFeaturesetVersionsByName(
            ListFeaturesetVersionsByNameRequest(featureset_name=featureset_name)
        )

    @grpc_try_catch_wrapper(
        "Failed to set active version: {version_number} for Featureset: {featureset_name}",
        reraise_non_grpc_error_original_exception=True,
    )
    def set_active_featureset_version(self, featureset_name: str, version_number: int):
        self._features_service.SetActiveFeaturesetVersion(
            SetActiveFeaturesetVersionRequest(
                featureset_name=featureset_name,
                featureset_version_number=version_number,
            )
        )

    @grpc_try_catch_wrapper(
        "Failed to delete version: {version_number} for Featureset: {featureset_name}",
        reraise_non_grpc_error_original_exception=True,
    )
    def delete_featureset_version(self, featureset_name: str, version_number: int):
        self._features_service.DeleteFeaturesetVersion(
            DeleteFeaturesetVersionRequest(
                featureset_name=featureset_name,
                featureset_version_number=version_number,
            )
        )

    @grpc_try_catch_wrapper(
        "Failed to get env to featuresets mapping",
        reraise_non_grpc_error_original_exception=True,
    )
    def get_env_to_featuresets_mapping(self) -> GetEnvToFeatureSetsMappingResponse:
        return self._features_service.GetEnvToFeatureSetsMapping(
            GetEnvToFeatureSetsMappingRequest()
        )
