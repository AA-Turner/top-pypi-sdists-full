"""
Type annotations for workspaces-instances service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_instances/client/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_workspaces_instances.client import WorkspacesInstancesClient

    session = get_session()
    async with session.create_client("workspaces-instances") as client:
        client: WorkspacesInstancesClient
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
    ListInstanceTypesPaginator,
    ListRegionsPaginator,
    ListWorkspaceInstancesPaginator,
)
from .type_defs import (
    AssociateVolumeRequestTypeDef,
    CreateVolumeRequestTypeDef,
    CreateVolumeResponseTypeDef,
    CreateWorkspaceInstanceRequestTypeDef,
    CreateWorkspaceInstanceResponseTypeDef,
    DeleteVolumeRequestTypeDef,
    DeleteWorkspaceInstanceRequestTypeDef,
    DisassociateVolumeRequestTypeDef,
    GetWorkspaceInstanceRequestTypeDef,
    GetWorkspaceInstanceResponseTypeDef,
    ListInstanceTypesRequestTypeDef,
    ListInstanceTypesResponseTypeDef,
    ListRegionsRequestTypeDef,
    ListRegionsResponseTypeDef,
    ListTagsForResourceRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListWorkspaceInstancesRequestTypeDef,
    ListWorkspaceInstancesResponseTypeDef,
    TagResourceRequestTypeDef,
    UntagResourceRequestTypeDef,
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

__all__ = ("WorkspacesInstancesClient",)

class Exceptions(BaseClientExceptions):
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class WorkspacesInstancesClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-instances.html#WorkspacesInstances.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_instances/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        WorkspacesInstancesClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-instances.html#WorkspacesInstances.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_instances/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-instances/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_instances/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-instances/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_instances/client/#generate_presigned_url)
        """

    async def associate_volume(
        self, **kwargs: Unpack[AssociateVolumeRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Attaches a volume to a WorkSpace Instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-instances/client/associate_volume.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_instances/client/#associate_volume)
        """

    async def create_volume(
        self, **kwargs: Unpack[CreateVolumeRequestTypeDef]
    ) -> CreateVolumeResponseTypeDef:
        """
        Creates a new volume for WorkSpace Instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-instances/client/create_volume.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_instances/client/#create_volume)
        """

    async def create_workspace_instance(
        self, **kwargs: Unpack[CreateWorkspaceInstanceRequestTypeDef]
    ) -> CreateWorkspaceInstanceResponseTypeDef:
        """
        Launches a new WorkSpace Instance with specified configuration parameters,
        enabling programmatic workspace deployment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-instances/client/create_workspace_instance.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_instances/client/#create_workspace_instance)
        """

    async def delete_volume(self, **kwargs: Unpack[DeleteVolumeRequestTypeDef]) -> Dict[str, Any]:
        """
        Deletes a specified volume.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-instances/client/delete_volume.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_instances/client/#delete_volume)
        """

    async def delete_workspace_instance(
        self, **kwargs: Unpack[DeleteWorkspaceInstanceRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the specified WorkSpace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-instances/client/delete_workspace_instance.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_instances/client/#delete_workspace_instance)
        """

    async def disassociate_volume(
        self, **kwargs: Unpack[DisassociateVolumeRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Detaches a volume from a WorkSpace Instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-instances/client/disassociate_volume.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_instances/client/#disassociate_volume)
        """

    async def get_workspace_instance(
        self, **kwargs: Unpack[GetWorkspaceInstanceRequestTypeDef]
    ) -> GetWorkspaceInstanceResponseTypeDef:
        """
        Retrieves detailed information about a specific WorkSpace Instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-instances/client/get_workspace_instance.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_instances/client/#get_workspace_instance)
        """

    async def list_instance_types(
        self, **kwargs: Unpack[ListInstanceTypesRequestTypeDef]
    ) -> ListInstanceTypesResponseTypeDef:
        """
        Retrieves a list of instance types supported by Amazon WorkSpaces Instances,
        enabling precise workspace infrastructure configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-instances/client/list_instance_types.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_instances/client/#list_instance_types)
        """

    async def list_regions(
        self, **kwargs: Unpack[ListRegionsRequestTypeDef]
    ) -> ListRegionsResponseTypeDef:
        """
        Retrieves a list of AWS regions supported by Amazon WorkSpaces Instances,
        enabling region discovery for workspace deployments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-instances/client/list_regions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_instances/client/#list_regions)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Retrieves tags for a WorkSpace Instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-instances/client/list_tags_for_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_instances/client/#list_tags_for_resource)
        """

    async def list_workspace_instances(
        self, **kwargs: Unpack[ListWorkspaceInstancesRequestTypeDef]
    ) -> ListWorkspaceInstancesResponseTypeDef:
        """
        Retrieves a collection of WorkSpaces Instances based on specified filters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-instances/client/list_workspace_instances.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_instances/client/#list_workspace_instances)
        """

    async def tag_resource(self, **kwargs: Unpack[TagResourceRequestTypeDef]) -> Dict[str, Any]:
        """
        Adds tags to a WorkSpace Instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-instances/client/tag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_instances/client/#tag_resource)
        """

    async def untag_resource(self, **kwargs: Unpack[UntagResourceRequestTypeDef]) -> Dict[str, Any]:
        """
        Removes tags from a WorkSpace Instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-instances/client/untag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_instances/client/#untag_resource)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_instance_types"]
    ) -> ListInstanceTypesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-instances/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_instances/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_regions"]
    ) -> ListRegionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-instances/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_instances/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_workspace_instances"]
    ) -> ListWorkspaceInstancesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-instances/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_instances/client/#get_paginator)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-instances.html#WorkspacesInstances.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_instances/client/)
        """

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-instances.html#WorkspacesInstances.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_instances/client/)
        """
