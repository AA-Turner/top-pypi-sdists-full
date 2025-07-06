"""
Type annotations for synthetics service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_synthetics/client/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_synthetics.client import SyntheticsClient

    session = get_session()
    async with session.create_client("synthetics") as client:
        client: SyntheticsClient
    ```
"""

from __future__ import annotations

import sys
from types import TracebackType
from typing import Any

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .type_defs import (
    AssociateResourceRequestTypeDef,
    CreateCanaryRequestTypeDef,
    CreateCanaryResponseTypeDef,
    CreateGroupRequestTypeDef,
    CreateGroupResponseTypeDef,
    DeleteCanaryRequestTypeDef,
    DeleteGroupRequestTypeDef,
    DescribeCanariesLastRunRequestTypeDef,
    DescribeCanariesLastRunResponseTypeDef,
    DescribeCanariesRequestTypeDef,
    DescribeCanariesResponseTypeDef,
    DescribeRuntimeVersionsRequestTypeDef,
    DescribeRuntimeVersionsResponseTypeDef,
    DisassociateResourceRequestTypeDef,
    GetCanaryRequestTypeDef,
    GetCanaryResponseTypeDef,
    GetCanaryRunsRequestTypeDef,
    GetCanaryRunsResponseTypeDef,
    GetGroupRequestTypeDef,
    GetGroupResponseTypeDef,
    ListAssociatedGroupsRequestTypeDef,
    ListAssociatedGroupsResponseTypeDef,
    ListGroupResourcesRequestTypeDef,
    ListGroupResourcesResponseTypeDef,
    ListGroupsRequestTypeDef,
    ListGroupsResponseTypeDef,
    ListTagsForResourceRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    StartCanaryDryRunRequestTypeDef,
    StartCanaryDryRunResponseTypeDef,
    StartCanaryRequestTypeDef,
    StopCanaryRequestTypeDef,
    TagResourceRequestTypeDef,
    UntagResourceRequestTypeDef,
    UpdateCanaryRequestTypeDef,
)

if sys.version_info >= (3, 9):
    from builtins import dict as Dict
    from builtins import type as Type
    from collections.abc import Mapping
else:
    from typing import Dict, Mapping, Type
if sys.version_info >= (3, 12):
    from typing import Self, Unpack
else:
    from typing_extensions import Self, Unpack

__all__ = ("SyntheticsClient",)

class Exceptions(BaseClientExceptions):
    AccessDeniedException: Type[BotocoreClientError]
    BadRequestException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalFailureException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    NotFoundException: Type[BotocoreClientError]
    RequestEntityTooLargeException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    TooManyRequestsException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class SyntheticsClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/synthetics.html#Synthetics.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_synthetics/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        SyntheticsClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/synthetics.html#Synthetics.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_synthetics/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/synthetics/client/can_paginate.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_synthetics/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/synthetics/client/generate_presigned_url.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_synthetics/client/#generate_presigned_url)
        """

    async def associate_resource(
        self, **kwargs: Unpack[AssociateResourceRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Associates a canary with a group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/synthetics/client/associate_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_synthetics/client/#associate_resource)
        """

    async def create_canary(
        self, **kwargs: Unpack[CreateCanaryRequestTypeDef]
    ) -> CreateCanaryResponseTypeDef:
        """
        Creates a canary.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/synthetics/client/create_canary.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_synthetics/client/#create_canary)
        """

    async def create_group(
        self, **kwargs: Unpack[CreateGroupRequestTypeDef]
    ) -> CreateGroupResponseTypeDef:
        """
        Creates a group which you can use to associate canaries with each other,
        including cross-Region canaries.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/synthetics/client/create_group.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_synthetics/client/#create_group)
        """

    async def delete_canary(self, **kwargs: Unpack[DeleteCanaryRequestTypeDef]) -> Dict[str, Any]:
        """
        Permanently deletes the specified canary.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/synthetics/client/delete_canary.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_synthetics/client/#delete_canary)
        """

    async def delete_group(self, **kwargs: Unpack[DeleteGroupRequestTypeDef]) -> Dict[str, Any]:
        """
        Deletes a group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/synthetics/client/delete_group.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_synthetics/client/#delete_group)
        """

    async def describe_canaries(
        self, **kwargs: Unpack[DescribeCanariesRequestTypeDef]
    ) -> DescribeCanariesResponseTypeDef:
        """
        This operation returns a list of the canaries in your account, along with full
        details about each canary.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/synthetics/client/describe_canaries.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_synthetics/client/#describe_canaries)
        """

    async def describe_canaries_last_run(
        self, **kwargs: Unpack[DescribeCanariesLastRunRequestTypeDef]
    ) -> DescribeCanariesLastRunResponseTypeDef:
        """
        Use this operation to see information from the most recent run of each canary
        that you have created.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/synthetics/client/describe_canaries_last_run.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_synthetics/client/#describe_canaries_last_run)
        """

    async def describe_runtime_versions(
        self, **kwargs: Unpack[DescribeRuntimeVersionsRequestTypeDef]
    ) -> DescribeRuntimeVersionsResponseTypeDef:
        """
        Returns a list of Synthetics canary runtime versions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/synthetics/client/describe_runtime_versions.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_synthetics/client/#describe_runtime_versions)
        """

    async def disassociate_resource(
        self, **kwargs: Unpack[DisassociateResourceRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes a canary from a group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/synthetics/client/disassociate_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_synthetics/client/#disassociate_resource)
        """

    async def get_canary(
        self, **kwargs: Unpack[GetCanaryRequestTypeDef]
    ) -> GetCanaryResponseTypeDef:
        """
        Retrieves complete information about one canary.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/synthetics/client/get_canary.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_synthetics/client/#get_canary)
        """

    async def get_canary_runs(
        self, **kwargs: Unpack[GetCanaryRunsRequestTypeDef]
    ) -> GetCanaryRunsResponseTypeDef:
        """
        Retrieves a list of runs for a specified canary.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/synthetics/client/get_canary_runs.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_synthetics/client/#get_canary_runs)
        """

    async def get_group(self, **kwargs: Unpack[GetGroupRequestTypeDef]) -> GetGroupResponseTypeDef:
        """
        Returns information about one group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/synthetics/client/get_group.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_synthetics/client/#get_group)
        """

    async def list_associated_groups(
        self, **kwargs: Unpack[ListAssociatedGroupsRequestTypeDef]
    ) -> ListAssociatedGroupsResponseTypeDef:
        """
        Returns a list of the groups that the specified canary is associated with.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/synthetics/client/list_associated_groups.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_synthetics/client/#list_associated_groups)
        """

    async def list_group_resources(
        self, **kwargs: Unpack[ListGroupResourcesRequestTypeDef]
    ) -> ListGroupResourcesResponseTypeDef:
        """
        This operation returns a list of the ARNs of the canaries that are associated
        with the specified group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/synthetics/client/list_group_resources.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_synthetics/client/#list_group_resources)
        """

    async def list_groups(
        self, **kwargs: Unpack[ListGroupsRequestTypeDef]
    ) -> ListGroupsResponseTypeDef:
        """
        Returns a list of all groups in the account, displaying their names, unique
        IDs, and ARNs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/synthetics/client/list_groups.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_synthetics/client/#list_groups)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Displays the tags associated with a canary or group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/synthetics/client/list_tags_for_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_synthetics/client/#list_tags_for_resource)
        """

    async def start_canary(self, **kwargs: Unpack[StartCanaryRequestTypeDef]) -> Dict[str, Any]:
        """
        Use this operation to run a canary that has already been created.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/synthetics/client/start_canary.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_synthetics/client/#start_canary)
        """

    async def start_canary_dry_run(
        self, **kwargs: Unpack[StartCanaryDryRunRequestTypeDef]
    ) -> StartCanaryDryRunResponseTypeDef:
        """
        Use this operation to start a dry run for a canary that has already been
        created.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/synthetics/client/start_canary_dry_run.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_synthetics/client/#start_canary_dry_run)
        """

    async def stop_canary(self, **kwargs: Unpack[StopCanaryRequestTypeDef]) -> Dict[str, Any]:
        """
        Stops the canary to prevent all future runs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/synthetics/client/stop_canary.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_synthetics/client/#stop_canary)
        """

    async def tag_resource(self, **kwargs: Unpack[TagResourceRequestTypeDef]) -> Dict[str, Any]:
        """
        Assigns one or more tags (key-value pairs) to the specified canary or group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/synthetics/client/tag_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_synthetics/client/#tag_resource)
        """

    async def untag_resource(self, **kwargs: Unpack[UntagResourceRequestTypeDef]) -> Dict[str, Any]:
        """
        Removes one or more tags from the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/synthetics/client/untag_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_synthetics/client/#untag_resource)
        """

    async def update_canary(self, **kwargs: Unpack[UpdateCanaryRequestTypeDef]) -> Dict[str, Any]:
        """
        Updates the configuration of a canary that has already been created.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/synthetics/client/update_canary.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_synthetics/client/#update_canary)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/synthetics.html#Synthetics.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_synthetics/client/)
        """

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/synthetics.html#Synthetics.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_synthetics/client/)
        """
