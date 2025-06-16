"""
Type annotations for pcs service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pcs/client/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_pcs.client import ParallelComputingServiceClient

    session = get_session()
    async with session.create_client("pcs") as client:
        client: ParallelComputingServiceClient
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

from .paginator import ListClustersPaginator, ListComputeNodeGroupsPaginator, ListQueuesPaginator
from .type_defs import (
    CreateClusterRequestTypeDef,
    CreateClusterResponseTypeDef,
    CreateComputeNodeGroupRequestTypeDef,
    CreateComputeNodeGroupResponseTypeDef,
    CreateQueueRequestTypeDef,
    CreateQueueResponseTypeDef,
    DeleteClusterRequestTypeDef,
    DeleteComputeNodeGroupRequestTypeDef,
    DeleteQueueRequestTypeDef,
    EmptyResponseMetadataTypeDef,
    GetClusterRequestTypeDef,
    GetClusterResponseTypeDef,
    GetComputeNodeGroupRequestTypeDef,
    GetComputeNodeGroupResponseTypeDef,
    GetQueueRequestTypeDef,
    GetQueueResponseTypeDef,
    ListClustersRequestTypeDef,
    ListClustersResponseTypeDef,
    ListComputeNodeGroupsRequestTypeDef,
    ListComputeNodeGroupsResponseTypeDef,
    ListQueuesRequestTypeDef,
    ListQueuesResponseTypeDef,
    ListTagsForResourceRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    RegisterComputeNodeGroupInstanceRequestTypeDef,
    RegisterComputeNodeGroupInstanceResponseTypeDef,
    TagResourceRequestTypeDef,
    UntagResourceRequestTypeDef,
    UpdateComputeNodeGroupRequestTypeDef,
    UpdateComputeNodeGroupResponseTypeDef,
    UpdateQueueRequestTypeDef,
    UpdateQueueResponseTypeDef,
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


__all__ = ("ParallelComputingServiceClient",)


class Exceptions(BaseClientExceptions):
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class ParallelComputingServiceClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pcs.html#ParallelComputingService.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pcs/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ParallelComputingServiceClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pcs.html#ParallelComputingService.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pcs/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pcs/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pcs/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pcs/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pcs/client/#generate_presigned_url)
        """

    async def create_cluster(
        self, **kwargs: Unpack[CreateClusterRequestTypeDef]
    ) -> CreateClusterResponseTypeDef:
        """
        Creates a cluster in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pcs/client/create_cluster.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pcs/client/#create_cluster)
        """

    async def create_compute_node_group(
        self, **kwargs: Unpack[CreateComputeNodeGroupRequestTypeDef]
    ) -> CreateComputeNodeGroupResponseTypeDef:
        """
        Creates a managed set of compute nodes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pcs/client/create_compute_node_group.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pcs/client/#create_compute_node_group)
        """

    async def create_queue(
        self, **kwargs: Unpack[CreateQueueRequestTypeDef]
    ) -> CreateQueueResponseTypeDef:
        """
        Creates a job queue.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pcs/client/create_queue.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pcs/client/#create_queue)
        """

    async def delete_cluster(self, **kwargs: Unpack[DeleteClusterRequestTypeDef]) -> Dict[str, Any]:
        """
        Deletes a cluster and all its linked resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pcs/client/delete_cluster.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pcs/client/#delete_cluster)
        """

    async def delete_compute_node_group(
        self, **kwargs: Unpack[DeleteComputeNodeGroupRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a compute node group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pcs/client/delete_compute_node_group.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pcs/client/#delete_compute_node_group)
        """

    async def delete_queue(self, **kwargs: Unpack[DeleteQueueRequestTypeDef]) -> Dict[str, Any]:
        """
        Deletes a job queue.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pcs/client/delete_queue.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pcs/client/#delete_queue)
        """

    async def get_cluster(
        self, **kwargs: Unpack[GetClusterRequestTypeDef]
    ) -> GetClusterResponseTypeDef:
        """
        Returns detailed information about a running cluster in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pcs/client/get_cluster.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pcs/client/#get_cluster)
        """

    async def get_compute_node_group(
        self, **kwargs: Unpack[GetComputeNodeGroupRequestTypeDef]
    ) -> GetComputeNodeGroupResponseTypeDef:
        """
        Returns detailed information about a compute node group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pcs/client/get_compute_node_group.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pcs/client/#get_compute_node_group)
        """

    async def get_queue(self, **kwargs: Unpack[GetQueueRequestTypeDef]) -> GetQueueResponseTypeDef:
        """
        Returns detailed information about a queue.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pcs/client/get_queue.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pcs/client/#get_queue)
        """

    async def list_clusters(
        self, **kwargs: Unpack[ListClustersRequestTypeDef]
    ) -> ListClustersResponseTypeDef:
        """
        Returns a list of running clusters in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pcs/client/list_clusters.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pcs/client/#list_clusters)
        """

    async def list_compute_node_groups(
        self, **kwargs: Unpack[ListComputeNodeGroupsRequestTypeDef]
    ) -> ListComputeNodeGroupsResponseTypeDef:
        """
        Returns a list of all compute node groups associated with a cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pcs/client/list_compute_node_groups.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pcs/client/#list_compute_node_groups)
        """

    async def list_queues(
        self, **kwargs: Unpack[ListQueuesRequestTypeDef]
    ) -> ListQueuesResponseTypeDef:
        """
        Returns a list of all queues associated with a cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pcs/client/list_queues.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pcs/client/#list_queues)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Returns a list of all tags on an Amazon Web Services PCS resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pcs/client/list_tags_for_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pcs/client/#list_tags_for_resource)
        """

    async def register_compute_node_group_instance(
        self, **kwargs: Unpack[RegisterComputeNodeGroupInstanceRequestTypeDef]
    ) -> RegisterComputeNodeGroupInstanceResponseTypeDef:
        """
        <important> <p>This API action isn't intended for you to use.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pcs/client/register_compute_node_group_instance.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pcs/client/#register_compute_node_group_instance)
        """

    async def tag_resource(
        self, **kwargs: Unpack[TagResourceRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Adds or edits tags on an Amazon Web Services PCS resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pcs/client/tag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pcs/client/#tag_resource)
        """

    async def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes tags from an Amazon Web Services PCS resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pcs/client/untag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pcs/client/#untag_resource)
        """

    async def update_compute_node_group(
        self, **kwargs: Unpack[UpdateComputeNodeGroupRequestTypeDef]
    ) -> UpdateComputeNodeGroupResponseTypeDef:
        """
        Updates a compute node group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pcs/client/update_compute_node_group.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pcs/client/#update_compute_node_group)
        """

    async def update_queue(
        self, **kwargs: Unpack[UpdateQueueRequestTypeDef]
    ) -> UpdateQueueResponseTypeDef:
        """
        Updates the compute node group configuration of a queue.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pcs/client/update_queue.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pcs/client/#update_queue)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_clusters"]
    ) -> ListClustersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pcs/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pcs/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_compute_node_groups"]
    ) -> ListComputeNodeGroupsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pcs/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pcs/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_queues"]
    ) -> ListQueuesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pcs/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pcs/client/#get_paginator)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pcs.html#ParallelComputingService.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pcs/client/)
        """

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pcs.html#ParallelComputingService.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pcs/client/)
        """
