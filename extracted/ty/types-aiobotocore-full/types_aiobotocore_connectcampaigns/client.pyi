"""
Type annotations for connectcampaigns service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaigns/client/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_connectcampaigns.client import ConnectCampaignServiceClient

    session = get_session()
    async with session.create_client("connectcampaigns") as client:
        client: ConnectCampaignServiceClient
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

from .paginator import ListCampaignsPaginator
from .type_defs import (
    CreateCampaignRequestTypeDef,
    CreateCampaignResponseTypeDef,
    DeleteCampaignRequestTypeDef,
    DeleteConnectInstanceConfigRequestTypeDef,
    DeleteInstanceOnboardingJobRequestTypeDef,
    DescribeCampaignRequestTypeDef,
    DescribeCampaignResponseTypeDef,
    EmptyResponseMetadataTypeDef,
    GetCampaignStateBatchRequestTypeDef,
    GetCampaignStateBatchResponseTypeDef,
    GetCampaignStateRequestTypeDef,
    GetCampaignStateResponseTypeDef,
    GetConnectInstanceConfigRequestTypeDef,
    GetConnectInstanceConfigResponseTypeDef,
    GetInstanceOnboardingJobStatusRequestTypeDef,
    GetInstanceOnboardingJobStatusResponseTypeDef,
    ListCampaignsRequestTypeDef,
    ListCampaignsResponseTypeDef,
    ListTagsForResourceRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    PauseCampaignRequestTypeDef,
    PutDialRequestBatchRequestTypeDef,
    PutDialRequestBatchResponseTypeDef,
    ResumeCampaignRequestTypeDef,
    StartCampaignRequestTypeDef,
    StartInstanceOnboardingJobRequestTypeDef,
    StartInstanceOnboardingJobResponseTypeDef,
    StopCampaignRequestTypeDef,
    TagResourceRequestTypeDef,
    UntagResourceRequestTypeDef,
    UpdateCampaignDialerConfigRequestTypeDef,
    UpdateCampaignNameRequestTypeDef,
    UpdateCampaignOutboundCallConfigRequestTypeDef,
)

if sys.version_info >= (3, 9):
    from builtins import type as Type
    from collections.abc import Mapping
else:
    from typing import Mapping, Type
if sys.version_info >= (3, 12):
    from typing import Literal, Self, Unpack
else:
    from typing_extensions import Literal, Self, Unpack

__all__ = ("ConnectCampaignServiceClient",)

class Exceptions(BaseClientExceptions):
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    InvalidCampaignStateException: Type[BotocoreClientError]
    InvalidStateException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class ConnectCampaignServiceClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaigns.html#ConnectCampaignService.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaigns/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ConnectCampaignServiceClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaigns.html#ConnectCampaignService.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaigns/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaigns/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaigns/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaigns/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaigns/client/#generate_presigned_url)
        """

    async def create_campaign(
        self, **kwargs: Unpack[CreateCampaignRequestTypeDef]
    ) -> CreateCampaignResponseTypeDef:
        """
        Creates a campaign for the specified Amazon Connect account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaigns/client/create_campaign.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaigns/client/#create_campaign)
        """

    async def delete_campaign(
        self, **kwargs: Unpack[DeleteCampaignRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a campaign from the specified Amazon Connect account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaigns/client/delete_campaign.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaigns/client/#delete_campaign)
        """

    async def delete_connect_instance_config(
        self, **kwargs: Unpack[DeleteConnectInstanceConfigRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a connect instance config from the specified AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaigns/client/delete_connect_instance_config.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaigns/client/#delete_connect_instance_config)
        """

    async def delete_instance_onboarding_job(
        self, **kwargs: Unpack[DeleteInstanceOnboardingJobRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Delete the Connect Campaigns onboarding job for the specified Amazon Connect
        instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaigns/client/delete_instance_onboarding_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaigns/client/#delete_instance_onboarding_job)
        """

    async def describe_campaign(
        self, **kwargs: Unpack[DescribeCampaignRequestTypeDef]
    ) -> DescribeCampaignResponseTypeDef:
        """
        Describes the specific campaign.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaigns/client/describe_campaign.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaigns/client/#describe_campaign)
        """

    async def get_campaign_state(
        self, **kwargs: Unpack[GetCampaignStateRequestTypeDef]
    ) -> GetCampaignStateResponseTypeDef:
        """
        Get state of a campaign for the specified Amazon Connect account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaigns/client/get_campaign_state.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaigns/client/#get_campaign_state)
        """

    async def get_campaign_state_batch(
        self, **kwargs: Unpack[GetCampaignStateBatchRequestTypeDef]
    ) -> GetCampaignStateBatchResponseTypeDef:
        """
        Get state of campaigns for the specified Amazon Connect account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaigns/client/get_campaign_state_batch.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaigns/client/#get_campaign_state_batch)
        """

    async def get_connect_instance_config(
        self, **kwargs: Unpack[GetConnectInstanceConfigRequestTypeDef]
    ) -> GetConnectInstanceConfigResponseTypeDef:
        """
        Get the specific Connect instance config.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaigns/client/get_connect_instance_config.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaigns/client/#get_connect_instance_config)
        """

    async def get_instance_onboarding_job_status(
        self, **kwargs: Unpack[GetInstanceOnboardingJobStatusRequestTypeDef]
    ) -> GetInstanceOnboardingJobStatusResponseTypeDef:
        """
        Get the specific instance onboarding job status.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaigns/client/get_instance_onboarding_job_status.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaigns/client/#get_instance_onboarding_job_status)
        """

    async def list_campaigns(
        self, **kwargs: Unpack[ListCampaignsRequestTypeDef]
    ) -> ListCampaignsResponseTypeDef:
        """
        Provides summary information about the campaigns under the specified Amazon
        Connect account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaigns/client/list_campaigns.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaigns/client/#list_campaigns)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        List tags for a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaigns/client/list_tags_for_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaigns/client/#list_tags_for_resource)
        """

    async def pause_campaign(
        self, **kwargs: Unpack[PauseCampaignRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Pauses a campaign for the specified Amazon Connect account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaigns/client/pause_campaign.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaigns/client/#pause_campaign)
        """

    async def put_dial_request_batch(
        self, **kwargs: Unpack[PutDialRequestBatchRequestTypeDef]
    ) -> PutDialRequestBatchResponseTypeDef:
        """
        Creates dials requests for the specified campaign Amazon Connect account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaigns/client/put_dial_request_batch.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaigns/client/#put_dial_request_batch)
        """

    async def resume_campaign(
        self, **kwargs: Unpack[ResumeCampaignRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Stops a campaign for the specified Amazon Connect account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaigns/client/resume_campaign.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaigns/client/#resume_campaign)
        """

    async def start_campaign(
        self, **kwargs: Unpack[StartCampaignRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Starts a campaign for the specified Amazon Connect account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaigns/client/start_campaign.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaigns/client/#start_campaign)
        """

    async def start_instance_onboarding_job(
        self, **kwargs: Unpack[StartInstanceOnboardingJobRequestTypeDef]
    ) -> StartInstanceOnboardingJobResponseTypeDef:
        """
        Onboard the specific Amazon Connect instance to Connect Campaigns.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaigns/client/start_instance_onboarding_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaigns/client/#start_instance_onboarding_job)
        """

    async def stop_campaign(
        self, **kwargs: Unpack[StopCampaignRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Stops a campaign for the specified Amazon Connect account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaigns/client/stop_campaign.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaigns/client/#stop_campaign)
        """

    async def tag_resource(
        self, **kwargs: Unpack[TagResourceRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Tag a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaigns/client/tag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaigns/client/#tag_resource)
        """

    async def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Untag a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaigns/client/untag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaigns/client/#untag_resource)
        """

    async def update_campaign_dialer_config(
        self, **kwargs: Unpack[UpdateCampaignDialerConfigRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates the dialer config of a campaign.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaigns/client/update_campaign_dialer_config.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaigns/client/#update_campaign_dialer_config)
        """

    async def update_campaign_name(
        self, **kwargs: Unpack[UpdateCampaignNameRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates the name of a campaign.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaigns/client/update_campaign_name.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaigns/client/#update_campaign_name)
        """

    async def update_campaign_outbound_call_config(
        self, **kwargs: Unpack[UpdateCampaignOutboundCallConfigRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates the outbound call config of a campaign.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaigns/client/update_campaign_outbound_call_config.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaigns/client/#update_campaign_outbound_call_config)
        """

    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_campaigns"]
    ) -> ListCampaignsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaigns/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaigns/client/#get_paginator)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaigns.html#ConnectCampaignService.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaigns/client/)
        """

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaigns.html#ConnectCampaignService.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaigns/client/)
        """
