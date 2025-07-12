from datetime import datetime
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest
from google.protobuf.timestamp_pb2 import Timestamp

from tecton._internals import metadata_service
from tecton._internals.infra_operations import create_feature_server_cache
from tecton._internals.infra_operations import create_feature_server_group
from tecton._internals.infra_operations import create_ingest_server_group
from tecton._internals.infra_operations import create_transform_server_group
from tecton._internals.infra_operations import delete_feature_server_cache
from tecton._internals.infra_operations import delete_feature_server_group
from tecton._internals.infra_operations import delete_ingest_server_group
from tecton._internals.infra_operations import delete_transform_server_group
from tecton._internals.infra_operations import get_feature_server_cache
from tecton._internals.infra_operations import get_feature_server_group
from tecton._internals.infra_operations import get_ingest_server_group
from tecton._internals.infra_operations import get_transform_server_group
from tecton._internals.infra_operations import list_feature_server_caches
from tecton._internals.infra_operations import list_feature_server_groups
from tecton._internals.infra_operations import list_ingest_server_groups
from tecton._internals.infra_operations import list_transform_server_groups
from tecton._internals.infra_operations import update_feature_server_cache
from tecton._internals.infra_operations import update_feature_server_group
from tecton._internals.infra_operations import update_ingest_server_group
from tecton._internals.infra_operations import update_transform_server_group
from tecton_proto.servergroupservice.server_group_service__client_pb2 import AutoscalingConfig
from tecton_proto.servergroupservice.server_group_service__client_pb2 import CreateFeatureServerCacheRequest
from tecton_proto.servergroupservice.server_group_service__client_pb2 import CreateFeatureServerGroupRequest
from tecton_proto.servergroupservice.server_group_service__client_pb2 import CreateIngestServerGroupRequest
from tecton_proto.servergroupservice.server_group_service__client_pb2 import CreateTransformServerGroupRequest
from tecton_proto.servergroupservice.server_group_service__client_pb2 import DeleteFeatureServerCacheRequest
from tecton_proto.servergroupservice.server_group_service__client_pb2 import DeleteFeatureServerGroupRequest
from tecton_proto.servergroupservice.server_group_service__client_pb2 import DeleteIngestServerGroupRequest
from tecton_proto.servergroupservice.server_group_service__client_pb2 import DeleteTransformServerGroupRequest
from tecton_proto.servergroupservice.server_group_service__client_pb2 import FeatureServerCache
from tecton_proto.servergroupservice.server_group_service__client_pb2 import FeatureServerGroup
from tecton_proto.servergroupservice.server_group_service__client_pb2 import GetFeatureServerCacheRequest
from tecton_proto.servergroupservice.server_group_service__client_pb2 import GetFeatureServerGroupRequest
from tecton_proto.servergroupservice.server_group_service__client_pb2 import GetIngestServerGroupRequest
from tecton_proto.servergroupservice.server_group_service__client_pb2 import GetTransformServerGroupRequest
from tecton_proto.servergroupservice.server_group_service__client_pb2 import IngestServerGroup
from tecton_proto.servergroupservice.server_group_service__client_pb2 import ListFeatureServerCachesRequest
from tecton_proto.servergroupservice.server_group_service__client_pb2 import ListFeatureServerGroupsRequest
from tecton_proto.servergroupservice.server_group_service__client_pb2 import ListIngestServerGroupsRequest
from tecton_proto.servergroupservice.server_group_service__client_pb2 import ListTransformServerGroupsRequest
from tecton_proto.servergroupservice.server_group_service__client_pb2 import ProvisionedScalingCacheConfig
from tecton_proto.servergroupservice.server_group_service__client_pb2 import ProvisionedScalingConfig
from tecton_proto.servergroupservice.server_group_service__client_pb2 import ResourceMetadata
from tecton_proto.servergroupservice.server_group_service__client_pb2 import Status
from tecton_proto.servergroupservice.server_group_service__client_pb2 import TransformServerGroup
from tecton_proto.servergroupservice.server_group_service__client_pb2 import UpdateFeatureServerCacheRequest
from tecton_proto.servergroupservice.server_group_service__client_pb2 import UpdateFeatureServerGroupRequest
from tecton_proto.servergroupservice.server_group_service__client_pb2 import UpdateIngestServerGroupRequest
from tecton_proto.servergroupservice.server_group_service__client_pb2 import UpdateTransformServerGroupRequest


@pytest.fixture
def mock_metadata_service():
    with patch.object(metadata_service, "instance") as mock_instance:
        mock_client = MagicMock()
        mock_instance.return_value = mock_client
        yield mock_client


class TestFeatureServerCacheOperations:
    def test_create_feature_server_cache(self, mock_metadata_service):
        now = Timestamp()
        now.FromDatetime(datetime.now())
        cache = FeatureServerCache(
            id="test-id",
            workspace="test-workspace",
            name="test-cache",
            status=Status.READY,
            provisioned_config=ProvisionedScalingCacheConfig(
                num_shards=2,
                num_replicas_per_shard=3,
            ),
            metadata=ResourceMetadata(
                description="test description",
                tags={"key": "value"},
            ),
            created_at=now,
            updated_at=now,
        )
        mock_metadata_service.CreateFeatureServerCache.return_value = cache

        result = create_feature_server_cache(
            workspace="test-workspace",
            name="test-cache",
            num_shards=2,
            num_replicas_per_shard=3,
            description="test description",
            tags={"key": "value"},
        )

        assert result == cache
        mock_metadata_service.CreateFeatureServerCache.assert_called_once()
        request = mock_metadata_service.CreateFeatureServerCache.call_args[0][0]
        expected_request = CreateFeatureServerCacheRequest(
            workspace="test-workspace",
            name="test-cache",
            provisioned_config=ProvisionedScalingCacheConfig(
                num_shards=2,
                num_replicas_per_shard=3,
            ),
            metadata=ResourceMetadata(
                description="test description",
                tags={"key": "value"},
            ),
        )
        assert request == expected_request

    def test_get_feature_server_cache(self, mock_metadata_service):
        now = Timestamp()
        now.FromDatetime(datetime.now())
        cache = FeatureServerCache(
            id="test-id",
            workspace="test-workspace",
            name="test-cache",
            status=Status.READY,
            provisioned_config=ProvisionedScalingCacheConfig(
                num_shards=1,
                num_replicas_per_shard=1,
            ),
            created_at=now,
            updated_at=now,
        )
        mock_metadata_service.GetFeatureServerCache.return_value = cache

        result = get_feature_server_cache(id="test-id")

        assert result == cache
        mock_metadata_service.GetFeatureServerCache.assert_called_once()
        request = mock_metadata_service.GetFeatureServerCache.call_args[0][0]
        expected_request = GetFeatureServerCacheRequest(id="test-id")
        assert request == expected_request

    def test_update_feature_server_cache(self, mock_metadata_service):
        now = Timestamp()
        now.FromDatetime(datetime.now())
        cache = FeatureServerCache(
            id="test-id",
            workspace="test-workspace",
            name="test-cache",
            status=Status.READY,
            provisioned_config=ProvisionedScalingCacheConfig(
                num_shards=3,
                num_replicas_per_shard=4,
            ),
            metadata=ResourceMetadata(
                description="updated description",
                tags={"key2": "value2"},
            ),
            created_at=now,
            updated_at=now,
        )
        mock_metadata_service.UpdateFeatureServerCache.return_value = cache

        result = update_feature_server_cache(
            id="test-id",
            num_shards=3,
            num_replicas_per_shard=4,
            description="updated description",
            tags={"key2": "value2"},
        )

        assert result == cache
        mock_metadata_service.UpdateFeatureServerCache.assert_called_once()
        request = mock_metadata_service.UpdateFeatureServerCache.call_args[0][0]
        expected_request = UpdateFeatureServerCacheRequest(
            id="test-id",
            provisioned_config=ProvisionedScalingCacheConfig(
                num_shards=3,
                num_replicas_per_shard=4,
            ),
            metadata=ResourceMetadata(
                description="updated description",
                tags={"key2": "value2"},
            ),
        )
        assert request == expected_request

    def test_delete_feature_server_cache(self, mock_metadata_service):
        delete_feature_server_cache(id="test-id")
        mock_metadata_service.DeleteFeatureServerCache.assert_called_once()
        request = mock_metadata_service.DeleteFeatureServerCache.call_args[0][0]
        expected_request = DeleteFeatureServerCacheRequest(id="test-id")
        assert request == expected_request

    def test_list_feature_server_caches(self, mock_metadata_service):
        now = Timestamp()
        now.FromDatetime(datetime.now())
        cache1 = FeatureServerCache(
            id="id1",
            workspace="test-workspace",
            name="cache1",
            status=Status.READY,
            provisioned_config=ProvisionedScalingCacheConfig(
                num_shards=1,
                num_replicas_per_shard=1,
            ),
            created_at=now,
            updated_at=now,
        )
        cache2 = FeatureServerCache(
            id="id2",
            workspace="test-workspace",
            name="cache2",
            status=Status.READY,
            provisioned_config=ProvisionedScalingCacheConfig(
                num_shards=1,
                num_replicas_per_shard=1,
            ),
            created_at=now,
            updated_at=now,
        )
        caches = [cache1, cache2]
        mock_metadata_service.ListFeatureServerCaches.return_value.caches = caches

        result = list_feature_server_caches(workspace="test-workspace")

        assert result.caches == caches
        mock_metadata_service.ListFeatureServerCaches.assert_called_once()
        request = mock_metadata_service.ListFeatureServerCaches.call_args[0][0]
        expected_request = ListFeatureServerCachesRequest(workspace="test-workspace")
        assert request == expected_request


class TestFeatureServerGroupOperations:
    def test_create_feature_server_group(self, mock_metadata_service):
        now = Timestamp()
        now.FromDatetime(datetime.now())
        group = FeatureServerGroup(
            id="test-id",
            workspace="test-workspace",
            name="test-group",
            status=Status.READY,
            autoscaling_config=AutoscalingConfig(
                min_nodes=1,
                max_nodes=3,
            ),
            node_type="test-type",
            cache_id="test-cache",
            metadata=ResourceMetadata(
                description="test description",
                tags={"key": "value"},
            ),
            created_at=now,
            updated_at=now,
        )
        mock_metadata_service.CreateFeatureServerGroup.return_value = group

        result = create_feature_server_group(
            workspace="test-workspace",
            name="test-group",
            min_nodes=1,
            max_nodes=3,
            node_type="test-type",
            cache_id="test-cache",
            description="test description",
            tags={"key": "value"},
        )

        assert result == group
        mock_metadata_service.CreateFeatureServerGroup.assert_called_once()
        request = mock_metadata_service.CreateFeatureServerGroup.call_args[0][0]
        expected_request = CreateFeatureServerGroupRequest(
            workspace="test-workspace",
            name="test-group",
            autoscaling_config=AutoscalingConfig(
                min_nodes=1,
                max_nodes=3,
            ),
            node_type="test-type",
            cache_id="test-cache",
            metadata=ResourceMetadata(
                description="test description",
                tags={"key": "value"},
            ),
        )
        assert request == expected_request

    def test_get_feature_server_group(self, mock_metadata_service):
        now = Timestamp()
        now.FromDatetime(datetime.now())
        group = FeatureServerGroup(
            id="test-id",
            workspace="test-workspace",
            name="test-group",
            status=Status.READY,
            created_at=now,
            updated_at=now,
        )
        mock_metadata_service.GetFeatureServerGroup.return_value = group

        result = get_feature_server_group(id="test-id")

        assert result == group
        mock_metadata_service.GetFeatureServerGroup.assert_called_once()
        request = mock_metadata_service.GetFeatureServerGroup.call_args[0][0]
        expected_request = GetFeatureServerGroupRequest(id="test-id")
        assert request == expected_request

    def test_update_feature_server_group(self, mock_metadata_service):
        now = Timestamp()
        now.FromDatetime(datetime.now())
        group = FeatureServerGroup(
            id="test-id",
            workspace="test-workspace",
            name="test-group",
            status=Status.READY,
            provisioned_config=ProvisionedScalingConfig(
                desired_nodes=2,
            ),
            node_type="updated-type",
            metadata=ResourceMetadata(
                description="updated description",
                tags={"key2": "value2"},
            ),
            created_at=now,
            updated_at=now,
        )
        mock_metadata_service.UpdateFeatureServerGroup.return_value = group

        result = update_feature_server_group(
            id="test-id",
            desired_nodes=2,
            node_type="updated-type",
            description="updated description",
            tags={"key2": "value2"},
        )

        assert result == group
        mock_metadata_service.UpdateFeatureServerGroup.assert_called_once()
        request = mock_metadata_service.UpdateFeatureServerGroup.call_args[0][0]
        expected_request = UpdateFeatureServerGroupRequest(
            id="test-id",
            provisioned_config=ProvisionedScalingConfig(
                desired_nodes=2,
            ),
            node_type="updated-type",
            metadata=ResourceMetadata(
                description="updated description",
                tags={"key2": "value2"},
            ),
        )
        assert request == expected_request

    def test_delete_feature_server_group(self, mock_metadata_service):
        delete_feature_server_group(id="test-id")
        mock_metadata_service.DeleteFeatureServerGroup.assert_called_once()
        request = mock_metadata_service.DeleteFeatureServerGroup.call_args[0][0]
        expected_request = DeleteFeatureServerGroupRequest(id="test-id")
        assert request == expected_request

    def test_list_feature_server_groups(self, mock_metadata_service):
        now = Timestamp()
        now.FromDatetime(datetime.now())
        group1 = FeatureServerGroup(
            id="id1",
            workspace="test-workspace",
            name="group1",
            status=Status.READY,
            created_at=now,
            updated_at=now,
        )
        group2 = FeatureServerGroup(
            id="id2",
            workspace="test-workspace",
            name="group2",
            status=Status.READY,
            created_at=now,
            updated_at=now,
        )
        groups = [group1, group2]
        mock_metadata_service.ListFeatureServerGroups.return_value.feature_server_groups = groups

        result = list_feature_server_groups(workspace="test-workspace")

        assert result.feature_server_groups == groups
        mock_metadata_service.ListFeatureServerGroups.assert_called_once()
        request = mock_metadata_service.ListFeatureServerGroups.call_args[0][0]
        expected_request = ListFeatureServerGroupsRequest(workspace="test-workspace")
        assert request == expected_request


class TestIngestServerGroupOperations:
    def test_create_ingest_server_group(self, mock_metadata_service):
        now = Timestamp()
        now.FromDatetime(datetime.now())
        group = IngestServerGroup(
            id="test-id",
            workspace="test-workspace",
            name="test-group",
            status=Status.READY,
            autoscaling_config=AutoscalingConfig(
                min_nodes=1,
                max_nodes=3,
            ),
            node_type="test-type",
            metadata=ResourceMetadata(
                description="test description",
                tags={"key": "value"},
            ),
            created_at=now,
            updated_at=now,
        )
        mock_metadata_service.CreateIngestServerGroup.return_value = group

        result = create_ingest_server_group(
            workspace="test-workspace",
            name="test-group",
            min_nodes=1,
            max_nodes=3,
            node_type="test-type",
            description="test description",
            tags={"key": "value"},
        )

        assert result == group
        mock_metadata_service.CreateIngestServerGroup.assert_called_once()
        request = mock_metadata_service.CreateIngestServerGroup.call_args[0][0]
        expected_request = CreateIngestServerGroupRequest(
            workspace="test-workspace",
            name="test-group",
            autoscaling_config=AutoscalingConfig(
                min_nodes=1,
                max_nodes=3,
            ),
            node_type="test-type",
            metadata=ResourceMetadata(
                description="test description",
                tags={"key": "value"},
            ),
        )
        assert request == expected_request

    def test_get_ingest_server_group(self, mock_metadata_service):
        now = Timestamp()
        now.FromDatetime(datetime.now())
        group = IngestServerGroup(
            id="test-id",
            workspace="test-workspace",
            name="test-group",
            status=Status.READY,
            created_at=now,
            updated_at=now,
        )
        mock_metadata_service.GetIngestServerGroup.return_value = group

        result = get_ingest_server_group(id="test-id")

        assert result == group
        mock_metadata_service.GetIngestServerGroup.assert_called_once()
        request = mock_metadata_service.GetIngestServerGroup.call_args[0][0]
        expected_request = GetIngestServerGroupRequest(id="test-id")
        assert request == expected_request

    def test_update_ingest_server_group(self, mock_metadata_service):
        now = Timestamp()
        now.FromDatetime(datetime.now())
        group = IngestServerGroup(
            id="test-id",
            workspace="test-workspace",
            name="test-group",
            status=Status.READY,
            provisioned_config=ProvisionedScalingConfig(
                desired_nodes=2,
            ),
            node_type="updated-type",
            metadata=ResourceMetadata(
                description="updated description",
                tags={"key2": "value2"},
            ),
            created_at=now,
            updated_at=now,
        )
        mock_metadata_service.UpdateIngestServerGroup.return_value = group

        result = update_ingest_server_group(
            id="test-id",
            desired_nodes=2,
            node_type="updated-type",
            description="updated description",
            tags={"key2": "value2"},
        )

        assert result == group
        mock_metadata_service.UpdateIngestServerGroup.assert_called_once()
        request = mock_metadata_service.UpdateIngestServerGroup.call_args[0][0]
        expected_request = UpdateIngestServerGroupRequest(
            id="test-id",
            provisioned_config=ProvisionedScalingConfig(
                desired_nodes=2,
            ),
            node_type="updated-type",
            metadata=ResourceMetadata(
                description="updated description",
                tags={"key2": "value2"},
            ),
        )
        assert request == expected_request

    def test_delete_ingest_server_group(self, mock_metadata_service):
        delete_ingest_server_group(id="test-id")
        mock_metadata_service.DeleteIngestServerGroup.assert_called_once()
        request = mock_metadata_service.DeleteIngestServerGroup.call_args[0][0]
        expected_request = DeleteIngestServerGroupRequest(id="test-id")
        assert request == expected_request

    def test_list_ingest_server_groups(self, mock_metadata_service):
        now = Timestamp()
        now.FromDatetime(datetime.now())
        group1 = IngestServerGroup(
            id="id1",
            workspace="test-workspace",
            name="group1",
            status=Status.READY,
            created_at=now,
            updated_at=now,
        )
        group2 = IngestServerGroup(
            id="id2",
            workspace="test-workspace",
            name="group2",
            status=Status.READY,
            created_at=now,
            updated_at=now,
        )
        groups = [group1, group2]
        mock_metadata_service.ListIngestServerGroups.return_value.ingest_server_groups = groups

        result = list_ingest_server_groups(workspace="test-workspace")

        assert result.ingest_server_groups == groups
        mock_metadata_service.ListIngestServerGroups.assert_called_once()
        request = mock_metadata_service.ListIngestServerGroups.call_args[0][0]
        expected_request = ListIngestServerGroupsRequest(workspace="test-workspace")
        assert request == expected_request


class TestTransformServerGroupOperations:
    def test_create_transform_server_group(self, mock_metadata_service):
        now = Timestamp()
        now.FromDatetime(datetime.now())
        group = TransformServerGroup(
            id="test-id",
            workspace="test-workspace",
            name="test-group",
            environment="test-env",
            status=Status.READY,
            autoscaling_config=AutoscalingConfig(
                min_nodes=1,
                max_nodes=3,
            ),
            node_type="test-type",
            environment_variables={"key": "value"},
            metadata=ResourceMetadata(
                description="test description",
                tags={"key": "value"},
            ),
            created_at=now,
            updated_at=now,
        )
        mock_metadata_service.CreateTransformServerGroup.return_value = group

        result = create_transform_server_group(
            workspace="test-workspace",
            name="test-group",
            environment="test-env",
            min_nodes=1,
            max_nodes=3,
            node_type="test-type",
            environment_variables={"key": "value"},
            description="test description",
            tags={"key": "value"},
        )

        assert result == group
        mock_metadata_service.CreateTransformServerGroup.assert_called_once()
        request = mock_metadata_service.CreateTransformServerGroup.call_args[0][0]
        expected_request = CreateTransformServerGroupRequest(
            workspace="test-workspace",
            name="test-group",
            environment="test-env",
            autoscaling_config=AutoscalingConfig(
                min_nodes=1,
                max_nodes=3,
            ),
            node_type="test-type",
            environment_variables={"key": "value"},
            metadata=ResourceMetadata(
                description="test description",
                tags={"key": "value"},
            ),
        )
        assert request == expected_request

    def test_get_transform_server_group(self, mock_metadata_service):
        now = Timestamp()
        now.FromDatetime(datetime.now())
        group = TransformServerGroup(
            id="test-id",
            workspace="test-workspace",
            name="test-group",
            environment="test-env",
            status=Status.READY,
            created_at=now,
            updated_at=now,
        )
        mock_metadata_service.GetTransformServerGroup.return_value = group

        result = get_transform_server_group(id="test-id")

        assert result == group
        mock_metadata_service.GetTransformServerGroup.assert_called_once()
        request = mock_metadata_service.GetTransformServerGroup.call_args[0][0]
        expected_request = GetTransformServerGroupRequest(id="test-id")
        assert request == expected_request

    def test_update_transform_server_group(self, mock_metadata_service):
        now = Timestamp()
        now.FromDatetime(datetime.now())
        group = TransformServerGroup(
            id="test-id",
            workspace="test-workspace",
            name="test-group",
            environment="test-env",
            status=Status.READY,
            provisioned_config=ProvisionedScalingConfig(
                desired_nodes=2,
            ),
            node_type="updated-type",
            environment_variables={"key2": "value2"},
            metadata=ResourceMetadata(
                description="updated description",
                tags={"key2": "value2"},
            ),
            created_at=now,
            updated_at=now,
        )
        mock_metadata_service.UpdateTransformServerGroup.return_value = group

        result = update_transform_server_group(
            id="test-id",
            environment="test-env",
            desired_nodes=2,
            node_type="updated-type",
            environment_variables={"key2": "value2"},
            description="updated description",
            tags={"key2": "value2"},
        )

        assert result == group
        mock_metadata_service.UpdateTransformServerGroup.assert_called_once()
        request = mock_metadata_service.UpdateTransformServerGroup.call_args[0][0]
        expected_request = UpdateTransformServerGroupRequest(
            id="test-id",
            environment="test-env",
            provisioned_config=ProvisionedScalingConfig(
                desired_nodes=2,
            ),
            node_type="updated-type",
            environment_variables={"key2": "value2"},
            metadata=ResourceMetadata(
                description="updated description",
                tags={"key2": "value2"},
            ),
        )
        assert request == expected_request

    def test_delete_transform_server_group(self, mock_metadata_service):
        delete_transform_server_group(id="test-id")
        mock_metadata_service.DeleteTransformServerGroup.assert_called_once()
        request = mock_metadata_service.DeleteTransformServerGroup.call_args[0][0]
        expected_request = DeleteTransformServerGroupRequest(id="test-id")
        assert request == expected_request

    def test_list_transform_server_groups(self, mock_metadata_service):
        now = Timestamp()
        now.FromDatetime(datetime.now())
        group1 = TransformServerGroup(
            id="id1",
            workspace="test-workspace",
            name="group1",
            environment="env1",
            status=Status.READY,
            created_at=now,
            updated_at=now,
        )
        group2 = TransformServerGroup(
            id="id2",
            workspace="test-workspace",
            name="group2",
            environment="env2",
            status=Status.READY,
            created_at=now,
            updated_at=now,
        )
        groups = [group1, group2]
        mock_metadata_service.ListTransformServerGroups.return_value.transform_server_groups = groups

        result = list_transform_server_groups(workspace="test-workspace")

        assert result.transform_server_groups == groups
        mock_metadata_service.ListTransformServerGroups.assert_called_once()
        request = mock_metadata_service.ListTransformServerGroups.call_args[0][0]
        expected_request = ListTransformServerGroupsRequest(workspace="test-workspace")
        assert request == expected_request
