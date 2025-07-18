"""
Type annotations for aiops service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_aiops/client/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_aiops.client import AIOpsClient

    session = get_session()
    async with session.create_client("aiops") as client:
        client: AIOpsClient
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

from .paginator import ListInvestigationGroupsPaginator
from .type_defs import (
    CreateInvestigationGroupInputTypeDef,
    CreateInvestigationGroupOutputTypeDef,
    DeleteInvestigationGroupPolicyRequestTypeDef,
    DeleteInvestigationGroupRequestTypeDef,
    EmptyResponseMetadataTypeDef,
    GetInvestigationGroupPolicyRequestTypeDef,
    GetInvestigationGroupPolicyResponseTypeDef,
    GetInvestigationGroupRequestTypeDef,
    GetInvestigationGroupResponseTypeDef,
    ListInvestigationGroupsInputTypeDef,
    ListInvestigationGroupsOutputTypeDef,
    ListTagsForResourceOutputTypeDef,
    ListTagsForResourceRequestTypeDef,
    PutInvestigationGroupPolicyRequestTypeDef,
    PutInvestigationGroupPolicyResponseTypeDef,
    TagResourceRequestTypeDef,
    UntagResourceRequestTypeDef,
    UpdateInvestigationGroupRequestTypeDef,
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

__all__ = ("AIOpsClient",)

class Exceptions(BaseClientExceptions):
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    ForbiddenException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class AIOpsClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/aiops.html#AIOps.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_aiops/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        AIOpsClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/aiops.html#AIOps.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_aiops/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/aiops/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_aiops/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/aiops/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_aiops/client/#generate_presigned_url)
        """

    async def create_investigation_group(
        self, **kwargs: Unpack[CreateInvestigationGroupInputTypeDef]
    ) -> CreateInvestigationGroupOutputTypeDef:
        """
        Creates an <i>investigation group</i> in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/aiops/client/create_investigation_group.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_aiops/client/#create_investigation_group)
        """

    async def delete_investigation_group(
        self, **kwargs: Unpack[DeleteInvestigationGroupRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified investigation group from your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/aiops/client/delete_investigation_group.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_aiops/client/#delete_investigation_group)
        """

    async def delete_investigation_group_policy(
        self, **kwargs: Unpack[DeleteInvestigationGroupPolicyRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes the IAM resource policy from being associated with the investigation
        group that you specify.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/aiops/client/delete_investigation_group_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_aiops/client/#delete_investigation_group_policy)
        """

    async def get_investigation_group(
        self, **kwargs: Unpack[GetInvestigationGroupRequestTypeDef]
    ) -> GetInvestigationGroupResponseTypeDef:
        """
        Returns the configuration information for the specified investigation group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/aiops/client/get_investigation_group.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_aiops/client/#get_investigation_group)
        """

    async def get_investigation_group_policy(
        self, **kwargs: Unpack[GetInvestigationGroupPolicyRequestTypeDef]
    ) -> GetInvestigationGroupPolicyResponseTypeDef:
        """
        Returns the IAM resource policy that is associated with the specified
        investigation group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/aiops/client/get_investigation_group_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_aiops/client/#get_investigation_group_policy)
        """

    async def list_investigation_groups(
        self, **kwargs: Unpack[ListInvestigationGroupsInputTypeDef]
    ) -> ListInvestigationGroupsOutputTypeDef:
        """
        Returns the ARN and name of each investigation group in the account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/aiops/client/list_investigation_groups.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_aiops/client/#list_investigation_groups)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestTypeDef]
    ) -> ListTagsForResourceOutputTypeDef:
        """
        Displays the tags associated with a CloudWatch investigations resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/aiops/client/list_tags_for_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_aiops/client/#list_tags_for_resource)
        """

    async def put_investigation_group_policy(
        self, **kwargs: Unpack[PutInvestigationGroupPolicyRequestTypeDef]
    ) -> PutInvestigationGroupPolicyResponseTypeDef:
        """
        Creates an IAM resource policy and assigns it to the specified investigation
        group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/aiops/client/put_investigation_group_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_aiops/client/#put_investigation_group_policy)
        """

    async def tag_resource(self, **kwargs: Unpack[TagResourceRequestTypeDef]) -> Dict[str, Any]:
        """
        Assigns one or more tags (key-value pairs) to the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/aiops/client/tag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_aiops/client/#tag_resource)
        """

    async def untag_resource(self, **kwargs: Unpack[UntagResourceRequestTypeDef]) -> Dict[str, Any]:
        """
        Removes one or more tags from the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/aiops/client/untag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_aiops/client/#untag_resource)
        """

    async def update_investigation_group(
        self, **kwargs: Unpack[UpdateInvestigationGroupRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates the configuration of the specified investigation group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/aiops/client/update_investigation_group.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_aiops/client/#update_investigation_group)
        """

    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_investigation_groups"]
    ) -> ListInvestigationGroupsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/aiops/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_aiops/client/#get_paginator)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/aiops.html#AIOps.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_aiops/client/)
        """

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/aiops.html#AIOps.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_aiops/client/)
        """
