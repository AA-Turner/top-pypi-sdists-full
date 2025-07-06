"""
Type annotations for docdb-elastic service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_docdb_elastic/client/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_docdb_elastic.client import DocDBElasticClient

    session = get_session()
    async with session.create_client("docdb-elastic") as client:
        client: DocDBElasticClient
    ```
"""

from __future__ import annotations

import sys
from types import TracebackType
from typing import Any, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .paginator import (
    ListClusterSnapshotsPaginator,
    ListClustersPaginator,
    ListPendingMaintenanceActionsPaginator,
)
from .type_defs import (
    ApplyPendingMaintenanceActionInputTypeDef,
    ApplyPendingMaintenanceActionOutputTypeDef,
    CopyClusterSnapshotInputTypeDef,
    CopyClusterSnapshotOutputTypeDef,
    CreateClusterInputTypeDef,
    CreateClusterOutputTypeDef,
    CreateClusterSnapshotInputTypeDef,
    CreateClusterSnapshotOutputTypeDef,
    DeleteClusterInputTypeDef,
    DeleteClusterOutputTypeDef,
    DeleteClusterSnapshotInputTypeDef,
    DeleteClusterSnapshotOutputTypeDef,
    GetClusterInputTypeDef,
    GetClusterOutputTypeDef,
    GetClusterSnapshotInputTypeDef,
    GetClusterSnapshotOutputTypeDef,
    GetPendingMaintenanceActionInputTypeDef,
    GetPendingMaintenanceActionOutputTypeDef,
    ListClustersInputTypeDef,
    ListClusterSnapshotsInputTypeDef,
    ListClusterSnapshotsOutputTypeDef,
    ListClustersOutputTypeDef,
    ListPendingMaintenanceActionsInputTypeDef,
    ListPendingMaintenanceActionsOutputTypeDef,
    ListTagsForResourceRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    RestoreClusterFromSnapshotInputTypeDef,
    RestoreClusterFromSnapshotOutputTypeDef,
    StartClusterInputTypeDef,
    StartClusterOutputTypeDef,
    StopClusterInputTypeDef,
    StopClusterOutputTypeDef,
    TagResourceRequestTypeDef,
    UntagResourceRequestTypeDef,
    UpdateClusterInputTypeDef,
    UpdateClusterOutputTypeDef,
)

if sys.version_info >= (3, 9):
    from builtins import dict as Dict
    from builtins import type as Type
    from collections.abc import Mapping
else:
    from typing import Dict, Mapping, Type
if sys.version_info >= (3, 12):
    from typing import Literal, Self, Unpack
else:
    from typing_extensions import Literal, Self, Unpack


__all__ = ("DocDBElasticClient",)


class Exceptions(BaseClientExceptions):
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class DocDBElasticClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb-elastic.html#DocDBElastic.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_docdb_elastic/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        DocDBElasticClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb-elastic.html#DocDBElastic.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_docdb_elastic/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb-elastic/client/can_paginate.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_docdb_elastic/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb-elastic/client/generate_presigned_url.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_docdb_elastic/client/#generate_presigned_url)
        """

    async def apply_pending_maintenance_action(
        self, **kwargs: Unpack[ApplyPendingMaintenanceActionInputTypeDef]
    ) -> ApplyPendingMaintenanceActionOutputTypeDef:
        """
        The type of pending maintenance action to be applied to the resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb-elastic/client/apply_pending_maintenance_action.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_docdb_elastic/client/#apply_pending_maintenance_action)
        """

    async def copy_cluster_snapshot(
        self, **kwargs: Unpack[CopyClusterSnapshotInputTypeDef]
    ) -> CopyClusterSnapshotOutputTypeDef:
        """
        Copies a snapshot of an elastic cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb-elastic/client/copy_cluster_snapshot.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_docdb_elastic/client/#copy_cluster_snapshot)
        """

    async def create_cluster(
        self, **kwargs: Unpack[CreateClusterInputTypeDef]
    ) -> CreateClusterOutputTypeDef:
        """
        Creates a new Amazon DocumentDB elastic cluster and returns its cluster
        structure.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb-elastic/client/create_cluster.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_docdb_elastic/client/#create_cluster)
        """

    async def create_cluster_snapshot(
        self, **kwargs: Unpack[CreateClusterSnapshotInputTypeDef]
    ) -> CreateClusterSnapshotOutputTypeDef:
        """
        Creates a snapshot of an elastic cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb-elastic/client/create_cluster_snapshot.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_docdb_elastic/client/#create_cluster_snapshot)
        """

    async def delete_cluster(
        self, **kwargs: Unpack[DeleteClusterInputTypeDef]
    ) -> DeleteClusterOutputTypeDef:
        """
        Delete an elastic cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb-elastic/client/delete_cluster.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_docdb_elastic/client/#delete_cluster)
        """

    async def delete_cluster_snapshot(
        self, **kwargs: Unpack[DeleteClusterSnapshotInputTypeDef]
    ) -> DeleteClusterSnapshotOutputTypeDef:
        """
        Delete an elastic cluster snapshot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb-elastic/client/delete_cluster_snapshot.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_docdb_elastic/client/#delete_cluster_snapshot)
        """

    async def get_cluster(
        self, **kwargs: Unpack[GetClusterInputTypeDef]
    ) -> GetClusterOutputTypeDef:
        """
        Returns information about a specific elastic cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb-elastic/client/get_cluster.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_docdb_elastic/client/#get_cluster)
        """

    async def get_cluster_snapshot(
        self, **kwargs: Unpack[GetClusterSnapshotInputTypeDef]
    ) -> GetClusterSnapshotOutputTypeDef:
        """
        Returns information about a specific elastic cluster snapshot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb-elastic/client/get_cluster_snapshot.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_docdb_elastic/client/#get_cluster_snapshot)
        """

    async def get_pending_maintenance_action(
        self, **kwargs: Unpack[GetPendingMaintenanceActionInputTypeDef]
    ) -> GetPendingMaintenanceActionOutputTypeDef:
        """
        Retrieves all maintenance actions that are pending.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb-elastic/client/get_pending_maintenance_action.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_docdb_elastic/client/#get_pending_maintenance_action)
        """

    async def list_cluster_snapshots(
        self, **kwargs: Unpack[ListClusterSnapshotsInputTypeDef]
    ) -> ListClusterSnapshotsOutputTypeDef:
        """
        Returns information about snapshots for a specified elastic cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb-elastic/client/list_cluster_snapshots.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_docdb_elastic/client/#list_cluster_snapshots)
        """

    async def list_clusters(
        self, **kwargs: Unpack[ListClustersInputTypeDef]
    ) -> ListClustersOutputTypeDef:
        """
        Returns information about provisioned Amazon DocumentDB elastic clusters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb-elastic/client/list_clusters.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_docdb_elastic/client/#list_clusters)
        """

    async def list_pending_maintenance_actions(
        self, **kwargs: Unpack[ListPendingMaintenanceActionsInputTypeDef]
    ) -> ListPendingMaintenanceActionsOutputTypeDef:
        """
        Retrieves a list of all maintenance actions that are pending.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb-elastic/client/list_pending_maintenance_actions.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_docdb_elastic/client/#list_pending_maintenance_actions)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists all tags on a elastic cluster resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb-elastic/client/list_tags_for_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_docdb_elastic/client/#list_tags_for_resource)
        """

    async def restore_cluster_from_snapshot(
        self, **kwargs: Unpack[RestoreClusterFromSnapshotInputTypeDef]
    ) -> RestoreClusterFromSnapshotOutputTypeDef:
        """
        Restores an elastic cluster from a snapshot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb-elastic/client/restore_cluster_from_snapshot.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_docdb_elastic/client/#restore_cluster_from_snapshot)
        """

    async def start_cluster(
        self, **kwargs: Unpack[StartClusterInputTypeDef]
    ) -> StartClusterOutputTypeDef:
        """
        Restarts the stopped elastic cluster that is specified by
        <code>clusterARN</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb-elastic/client/start_cluster.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_docdb_elastic/client/#start_cluster)
        """

    async def stop_cluster(
        self, **kwargs: Unpack[StopClusterInputTypeDef]
    ) -> StopClusterOutputTypeDef:
        """
        Stops the running elastic cluster that is specified by <code>clusterArn</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb-elastic/client/stop_cluster.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_docdb_elastic/client/#stop_cluster)
        """

    async def tag_resource(self, **kwargs: Unpack[TagResourceRequestTypeDef]) -> Dict[str, Any]:
        """
        Adds metadata tags to an elastic cluster resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb-elastic/client/tag_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_docdb_elastic/client/#tag_resource)
        """

    async def untag_resource(self, **kwargs: Unpack[UntagResourceRequestTypeDef]) -> Dict[str, Any]:
        """
        Removes metadata tags from an elastic cluster resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb-elastic/client/untag_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_docdb_elastic/client/#untag_resource)
        """

    async def update_cluster(
        self, **kwargs: Unpack[UpdateClusterInputTypeDef]
    ) -> UpdateClusterOutputTypeDef:
        """
        Modifies an elastic cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb-elastic/client/update_cluster.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_docdb_elastic/client/#update_cluster)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_cluster_snapshots"]
    ) -> ListClusterSnapshotsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb-elastic/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_docdb_elastic/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_clusters"]
    ) -> ListClustersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb-elastic/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_docdb_elastic/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_pending_maintenance_actions"]
    ) -> ListPendingMaintenanceActionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb-elastic/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_docdb_elastic/client/#get_paginator)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb-elastic.html#DocDBElastic.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_docdb_elastic/client/)
        """

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb-elastic.html#DocDBElastic.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_docdb_elastic/client/)
        """
