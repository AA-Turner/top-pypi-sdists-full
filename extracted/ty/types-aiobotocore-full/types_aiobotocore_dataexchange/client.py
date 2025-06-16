"""
Type annotations for dataexchange service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/client/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_dataexchange.client import DataExchangeClient

    session = get_session()
    async with session.create_client("dataexchange") as client:
        client: DataExchangeClient
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
    ListDataGrantsPaginator,
    ListDataSetRevisionsPaginator,
    ListDataSetsPaginator,
    ListEventActionsPaginator,
    ListJobsPaginator,
    ListReceivedDataGrantsPaginator,
    ListRevisionAssetsPaginator,
)
from .type_defs import (
    AcceptDataGrantRequestTypeDef,
    AcceptDataGrantResponseTypeDef,
    CancelJobRequestTypeDef,
    CreateDataGrantRequestTypeDef,
    CreateDataGrantResponseTypeDef,
    CreateDataSetRequestTypeDef,
    CreateDataSetResponseTypeDef,
    CreateEventActionRequestTypeDef,
    CreateEventActionResponseTypeDef,
    CreateJobRequestTypeDef,
    CreateJobResponseTypeDef,
    CreateRevisionRequestTypeDef,
    CreateRevisionResponseTypeDef,
    DeleteAssetRequestTypeDef,
    DeleteDataGrantRequestTypeDef,
    DeleteDataSetRequestTypeDef,
    DeleteEventActionRequestTypeDef,
    DeleteRevisionRequestTypeDef,
    EmptyResponseMetadataTypeDef,
    GetAssetRequestTypeDef,
    GetAssetResponseTypeDef,
    GetDataGrantRequestTypeDef,
    GetDataGrantResponseTypeDef,
    GetDataSetRequestTypeDef,
    GetDataSetResponseTypeDef,
    GetEventActionRequestTypeDef,
    GetEventActionResponseTypeDef,
    GetJobRequestTypeDef,
    GetJobResponseTypeDef,
    GetReceivedDataGrantRequestTypeDef,
    GetReceivedDataGrantResponseTypeDef,
    GetRevisionRequestTypeDef,
    GetRevisionResponseTypeDef,
    ListDataGrantsRequestTypeDef,
    ListDataGrantsResponseTypeDef,
    ListDataSetRevisionsRequestTypeDef,
    ListDataSetRevisionsResponseTypeDef,
    ListDataSetsRequestTypeDef,
    ListDataSetsResponseTypeDef,
    ListEventActionsRequestTypeDef,
    ListEventActionsResponseTypeDef,
    ListJobsRequestTypeDef,
    ListJobsResponseTypeDef,
    ListReceivedDataGrantsRequestTypeDef,
    ListReceivedDataGrantsResponseTypeDef,
    ListRevisionAssetsRequestTypeDef,
    ListRevisionAssetsResponseTypeDef,
    ListTagsForResourceRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    RevokeRevisionRequestTypeDef,
    RevokeRevisionResponseTypeDef,
    SendApiAssetRequestTypeDef,
    SendApiAssetResponseTypeDef,
    SendDataSetNotificationRequestTypeDef,
    StartJobRequestTypeDef,
    TagResourceRequestTypeDef,
    UntagResourceRequestTypeDef,
    UpdateAssetRequestTypeDef,
    UpdateAssetResponseTypeDef,
    UpdateDataSetRequestTypeDef,
    UpdateDataSetResponseTypeDef,
    UpdateEventActionRequestTypeDef,
    UpdateEventActionResponseTypeDef,
    UpdateRevisionRequestTypeDef,
    UpdateRevisionResponseTypeDef,
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


__all__ = ("DataExchangeClient",)


class Exceptions(BaseClientExceptions):
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceLimitExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class DataExchangeClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange.html#DataExchange.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        DataExchangeClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange.html#DataExchange.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/client/#generate_presigned_url)
        """

    async def accept_data_grant(
        self, **kwargs: Unpack[AcceptDataGrantRequestTypeDef]
    ) -> AcceptDataGrantResponseTypeDef:
        """
        This operation accepts a data grant.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange/client/accept_data_grant.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/client/#accept_data_grant)
        """

    async def cancel_job(
        self, **kwargs: Unpack[CancelJobRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        This operation cancels a job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange/client/cancel_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/client/#cancel_job)
        """

    async def create_data_grant(
        self, **kwargs: Unpack[CreateDataGrantRequestTypeDef]
    ) -> CreateDataGrantResponseTypeDef:
        """
        This operation creates a data grant.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange/client/create_data_grant.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/client/#create_data_grant)
        """

    async def create_data_set(
        self, **kwargs: Unpack[CreateDataSetRequestTypeDef]
    ) -> CreateDataSetResponseTypeDef:
        """
        This operation creates a data set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange/client/create_data_set.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/client/#create_data_set)
        """

    async def create_event_action(
        self, **kwargs: Unpack[CreateEventActionRequestTypeDef]
    ) -> CreateEventActionResponseTypeDef:
        """
        This operation creates an event action.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange/client/create_event_action.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/client/#create_event_action)
        """

    async def create_job(
        self, **kwargs: Unpack[CreateJobRequestTypeDef]
    ) -> CreateJobResponseTypeDef:
        """
        This operation creates a job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange/client/create_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/client/#create_job)
        """

    async def create_revision(
        self, **kwargs: Unpack[CreateRevisionRequestTypeDef]
    ) -> CreateRevisionResponseTypeDef:
        """
        This operation creates a revision for a data set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange/client/create_revision.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/client/#create_revision)
        """

    async def delete_asset(
        self, **kwargs: Unpack[DeleteAssetRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        This operation deletes an asset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange/client/delete_asset.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/client/#delete_asset)
        """

    async def delete_data_grant(
        self, **kwargs: Unpack[DeleteDataGrantRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        This operation deletes a data grant.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange/client/delete_data_grant.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/client/#delete_data_grant)
        """

    async def delete_data_set(
        self, **kwargs: Unpack[DeleteDataSetRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        This operation deletes a data set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange/client/delete_data_set.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/client/#delete_data_set)
        """

    async def delete_event_action(
        self, **kwargs: Unpack[DeleteEventActionRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        This operation deletes the event action.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange/client/delete_event_action.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/client/#delete_event_action)
        """

    async def delete_revision(
        self, **kwargs: Unpack[DeleteRevisionRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        This operation deletes a revision.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange/client/delete_revision.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/client/#delete_revision)
        """

    async def get_asset(self, **kwargs: Unpack[GetAssetRequestTypeDef]) -> GetAssetResponseTypeDef:
        """
        This operation returns information about an asset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange/client/get_asset.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/client/#get_asset)
        """

    async def get_data_grant(
        self, **kwargs: Unpack[GetDataGrantRequestTypeDef]
    ) -> GetDataGrantResponseTypeDef:
        """
        This operation returns information about a data grant.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange/client/get_data_grant.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/client/#get_data_grant)
        """

    async def get_data_set(
        self, **kwargs: Unpack[GetDataSetRequestTypeDef]
    ) -> GetDataSetResponseTypeDef:
        """
        This operation returns information about a data set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange/client/get_data_set.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/client/#get_data_set)
        """

    async def get_event_action(
        self, **kwargs: Unpack[GetEventActionRequestTypeDef]
    ) -> GetEventActionResponseTypeDef:
        """
        This operation retrieves information about an event action.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange/client/get_event_action.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/client/#get_event_action)
        """

    async def get_job(self, **kwargs: Unpack[GetJobRequestTypeDef]) -> GetJobResponseTypeDef:
        """
        This operation returns information about a job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange/client/get_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/client/#get_job)
        """

    async def get_received_data_grant(
        self, **kwargs: Unpack[GetReceivedDataGrantRequestTypeDef]
    ) -> GetReceivedDataGrantResponseTypeDef:
        """
        This operation returns information about a received data grant.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange/client/get_received_data_grant.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/client/#get_received_data_grant)
        """

    async def get_revision(
        self, **kwargs: Unpack[GetRevisionRequestTypeDef]
    ) -> GetRevisionResponseTypeDef:
        """
        This operation returns information about a revision.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange/client/get_revision.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/client/#get_revision)
        """

    async def list_data_grants(
        self, **kwargs: Unpack[ListDataGrantsRequestTypeDef]
    ) -> ListDataGrantsResponseTypeDef:
        """
        This operation returns information about all data grants.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange/client/list_data_grants.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/client/#list_data_grants)
        """

    async def list_data_set_revisions(
        self, **kwargs: Unpack[ListDataSetRevisionsRequestTypeDef]
    ) -> ListDataSetRevisionsResponseTypeDef:
        """
        This operation lists a data set's revisions sorted by CreatedAt in descending
        order.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange/client/list_data_set_revisions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/client/#list_data_set_revisions)
        """

    async def list_data_sets(
        self, **kwargs: Unpack[ListDataSetsRequestTypeDef]
    ) -> ListDataSetsResponseTypeDef:
        """
        This operation lists your data sets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange/client/list_data_sets.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/client/#list_data_sets)
        """

    async def list_event_actions(
        self, **kwargs: Unpack[ListEventActionsRequestTypeDef]
    ) -> ListEventActionsResponseTypeDef:
        """
        This operation lists your event actions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange/client/list_event_actions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/client/#list_event_actions)
        """

    async def list_jobs(self, **kwargs: Unpack[ListJobsRequestTypeDef]) -> ListJobsResponseTypeDef:
        """
        This operation lists your jobs sorted by CreatedAt in descending order.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange/client/list_jobs.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/client/#list_jobs)
        """

    async def list_received_data_grants(
        self, **kwargs: Unpack[ListReceivedDataGrantsRequestTypeDef]
    ) -> ListReceivedDataGrantsResponseTypeDef:
        """
        This operation returns information about all received data grants.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange/client/list_received_data_grants.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/client/#list_received_data_grants)
        """

    async def list_revision_assets(
        self, **kwargs: Unpack[ListRevisionAssetsRequestTypeDef]
    ) -> ListRevisionAssetsResponseTypeDef:
        """
        This operation lists a revision's assets sorted alphabetically in descending
        order.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange/client/list_revision_assets.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/client/#list_revision_assets)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        This operation lists the tags on the resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange/client/list_tags_for_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/client/#list_tags_for_resource)
        """

    async def revoke_revision(
        self, **kwargs: Unpack[RevokeRevisionRequestTypeDef]
    ) -> RevokeRevisionResponseTypeDef:
        """
        This operation revokes subscribers' access to a revision.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange/client/revoke_revision.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/client/#revoke_revision)
        """

    async def send_api_asset(
        self, **kwargs: Unpack[SendApiAssetRequestTypeDef]
    ) -> SendApiAssetResponseTypeDef:
        """
        This operation invokes an API Gateway API asset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange/client/send_api_asset.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/client/#send_api_asset)
        """

    async def send_data_set_notification(
        self, **kwargs: Unpack[SendDataSetNotificationRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        The type of event associated with the data set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange/client/send_data_set_notification.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/client/#send_data_set_notification)
        """

    async def start_job(self, **kwargs: Unpack[StartJobRequestTypeDef]) -> Dict[str, Any]:
        """
        This operation starts a job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange/client/start_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/client/#start_job)
        """

    async def tag_resource(
        self, **kwargs: Unpack[TagResourceRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        This operation tags a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange/client/tag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/client/#tag_resource)
        """

    async def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        This operation removes one or more tags from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange/client/untag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/client/#untag_resource)
        """

    async def update_asset(
        self, **kwargs: Unpack[UpdateAssetRequestTypeDef]
    ) -> UpdateAssetResponseTypeDef:
        """
        This operation updates an asset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange/client/update_asset.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/client/#update_asset)
        """

    async def update_data_set(
        self, **kwargs: Unpack[UpdateDataSetRequestTypeDef]
    ) -> UpdateDataSetResponseTypeDef:
        """
        This operation updates a data set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange/client/update_data_set.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/client/#update_data_set)
        """

    async def update_event_action(
        self, **kwargs: Unpack[UpdateEventActionRequestTypeDef]
    ) -> UpdateEventActionResponseTypeDef:
        """
        This operation updates the event action.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange/client/update_event_action.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/client/#update_event_action)
        """

    async def update_revision(
        self, **kwargs: Unpack[UpdateRevisionRequestTypeDef]
    ) -> UpdateRevisionResponseTypeDef:
        """
        This operation updates a revision.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange/client/update_revision.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/client/#update_revision)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_data_grants"]
    ) -> ListDataGrantsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_data_set_revisions"]
    ) -> ListDataSetRevisionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_data_sets"]
    ) -> ListDataSetsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_event_actions"]
    ) -> ListEventActionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_jobs"]
    ) -> ListJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_received_data_grants"]
    ) -> ListReceivedDataGrantsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_revision_assets"]
    ) -> ListRevisionAssetsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/client/#get_paginator)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange.html#DataExchange.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/client/)
        """

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange.html#DataExchange.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/client/)
        """
