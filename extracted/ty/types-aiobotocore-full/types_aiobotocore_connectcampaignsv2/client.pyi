"""
Type annotations for connectcampaignsv2 service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaignsv2/client/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_connectcampaignsv2.client import ConnectCampaignServiceV2Client

    session = get_session()
    async with session.create_client("connectcampaignsv2") as client:
        client: ConnectCampaignServiceV2Client
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

from .paginator import ListCampaignsPaginator, ListConnectInstanceIntegrationsPaginator
from .type_defs import (
    CreateCampaignRequestTypeDef,
    CreateCampaignResponseTypeDef,
    DeleteCampaignChannelSubtypeConfigRequestTypeDef,
    DeleteCampaignCommunicationLimitsRequestTypeDef,
    DeleteCampaignCommunicationTimeRequestTypeDef,
    DeleteCampaignRequestTypeDef,
    DeleteConnectInstanceConfigRequestTypeDef,
    DeleteConnectInstanceIntegrationRequestTypeDef,
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
    GetInstanceCommunicationLimitsRequestTypeDef,
    GetInstanceCommunicationLimitsResponseTypeDef,
    GetInstanceOnboardingJobStatusRequestTypeDef,
    GetInstanceOnboardingJobStatusResponseTypeDef,
    ListCampaignsRequestTypeDef,
    ListCampaignsResponseTypeDef,
    ListConnectInstanceIntegrationsRequestTypeDef,
    ListConnectInstanceIntegrationsResponseTypeDef,
    ListTagsForResourceRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    PauseCampaignRequestTypeDef,
    PutConnectInstanceIntegrationRequestTypeDef,
    PutInstanceCommunicationLimitsRequestTypeDef,
    PutOutboundRequestBatchRequestTypeDef,
    PutOutboundRequestBatchResponseTypeDef,
    PutProfileOutboundRequestBatchRequestTypeDef,
    PutProfileOutboundRequestBatchResponseTypeDef,
    ResumeCampaignRequestTypeDef,
    StartCampaignRequestTypeDef,
    StartInstanceOnboardingJobRequestTypeDef,
    StartInstanceOnboardingJobResponseTypeDef,
    StopCampaignRequestTypeDef,
    TagResourceRequestTypeDef,
    UntagResourceRequestTypeDef,
    UpdateCampaignChannelSubtypeConfigRequestTypeDef,
    UpdateCampaignCommunicationLimitsRequestTypeDef,
    UpdateCampaignCommunicationTimeRequestTypeDef,
    UpdateCampaignFlowAssociationRequestTypeDef,
    UpdateCampaignNameRequestTypeDef,
    UpdateCampaignScheduleRequestTypeDef,
    UpdateCampaignSourceRequestTypeDef,
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

__all__ = ("ConnectCampaignServiceV2Client",)

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

class ConnectCampaignServiceV2Client(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaignsv2.html#ConnectCampaignServiceV2.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaignsv2/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ConnectCampaignServiceV2Client exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaignsv2.html#ConnectCampaignServiceV2.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaignsv2/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaignsv2/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaignsv2/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaignsv2/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaignsv2/client/#generate_presigned_url)
        """

    async def create_campaign(
        self, **kwargs: Unpack[CreateCampaignRequestTypeDef]
    ) -> CreateCampaignResponseTypeDef:
        """
        Creates a campaign for the specified Amazon Connect account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaignsv2/client/create_campaign.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaignsv2/client/#create_campaign)
        """

    async def delete_campaign(
        self, **kwargs: Unpack[DeleteCampaignRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a campaign from the specified Amazon Connect account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaignsv2/client/delete_campaign.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaignsv2/client/#delete_campaign)
        """

    async def delete_campaign_channel_subtype_config(
        self, **kwargs: Unpack[DeleteCampaignChannelSubtypeConfigRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the channel subtype config of a campaign.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaignsv2/client/delete_campaign_channel_subtype_config.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaignsv2/client/#delete_campaign_channel_subtype_config)
        """

    async def delete_campaign_communication_limits(
        self, **kwargs: Unpack[DeleteCampaignCommunicationLimitsRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the communication limits config for a campaign.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaignsv2/client/delete_campaign_communication_limits.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaignsv2/client/#delete_campaign_communication_limits)
        """

    async def delete_campaign_communication_time(
        self, **kwargs: Unpack[DeleteCampaignCommunicationTimeRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the communication time config for a campaign.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaignsv2/client/delete_campaign_communication_time.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaignsv2/client/#delete_campaign_communication_time)
        """

    async def delete_connect_instance_config(
        self, **kwargs: Unpack[DeleteConnectInstanceConfigRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a connect instance config from the specified AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaignsv2/client/delete_connect_instance_config.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaignsv2/client/#delete_connect_instance_config)
        """

    async def delete_connect_instance_integration(
        self, **kwargs: Unpack[DeleteConnectInstanceIntegrationRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Delete the integration for the specified Amazon Connect instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaignsv2/client/delete_connect_instance_integration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaignsv2/client/#delete_connect_instance_integration)
        """

    async def delete_instance_onboarding_job(
        self, **kwargs: Unpack[DeleteInstanceOnboardingJobRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Delete the Connect Campaigns onboarding job for the specified Amazon Connect
        instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaignsv2/client/delete_instance_onboarding_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaignsv2/client/#delete_instance_onboarding_job)
        """

    async def describe_campaign(
        self, **kwargs: Unpack[DescribeCampaignRequestTypeDef]
    ) -> DescribeCampaignResponseTypeDef:
        """
        Describes the specific campaign.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaignsv2/client/describe_campaign.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaignsv2/client/#describe_campaign)
        """

    async def get_campaign_state(
        self, **kwargs: Unpack[GetCampaignStateRequestTypeDef]
    ) -> GetCampaignStateResponseTypeDef:
        """
        Get state of a campaign for the specified Amazon Connect account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaignsv2/client/get_campaign_state.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaignsv2/client/#get_campaign_state)
        """

    async def get_campaign_state_batch(
        self, **kwargs: Unpack[GetCampaignStateBatchRequestTypeDef]
    ) -> GetCampaignStateBatchResponseTypeDef:
        """
        Get state of campaigns for the specified Amazon Connect account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaignsv2/client/get_campaign_state_batch.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaignsv2/client/#get_campaign_state_batch)
        """

    async def get_connect_instance_config(
        self, **kwargs: Unpack[GetConnectInstanceConfigRequestTypeDef]
    ) -> GetConnectInstanceConfigResponseTypeDef:
        """
        Get the specific Connect instance config.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaignsv2/client/get_connect_instance_config.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaignsv2/client/#get_connect_instance_config)
        """

    async def get_instance_communication_limits(
        self, **kwargs: Unpack[GetInstanceCommunicationLimitsRequestTypeDef]
    ) -> GetInstanceCommunicationLimitsResponseTypeDef:
        """
        Get the instance communication limits.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaignsv2/client/get_instance_communication_limits.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaignsv2/client/#get_instance_communication_limits)
        """

    async def get_instance_onboarding_job_status(
        self, **kwargs: Unpack[GetInstanceOnboardingJobStatusRequestTypeDef]
    ) -> GetInstanceOnboardingJobStatusResponseTypeDef:
        """
        Get the specific instance onboarding job status.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaignsv2/client/get_instance_onboarding_job_status.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaignsv2/client/#get_instance_onboarding_job_status)
        """

    async def list_campaigns(
        self, **kwargs: Unpack[ListCampaignsRequestTypeDef]
    ) -> ListCampaignsResponseTypeDef:
        """
        Provides summary information about the campaigns under the specified Amazon
        Connect account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaignsv2/client/list_campaigns.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaignsv2/client/#list_campaigns)
        """

    async def list_connect_instance_integrations(
        self, **kwargs: Unpack[ListConnectInstanceIntegrationsRequestTypeDef]
    ) -> ListConnectInstanceIntegrationsResponseTypeDef:
        """
        Provides summary information about the integration under the specified Connect
        instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaignsv2/client/list_connect_instance_integrations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaignsv2/client/#list_connect_instance_integrations)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        List tags for a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaignsv2/client/list_tags_for_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaignsv2/client/#list_tags_for_resource)
        """

    async def pause_campaign(
        self, **kwargs: Unpack[PauseCampaignRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Pauses a campaign for the specified Amazon Connect account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaignsv2/client/pause_campaign.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaignsv2/client/#pause_campaign)
        """

    async def put_connect_instance_integration(
        self, **kwargs: Unpack[PutConnectInstanceIntegrationRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Put or update the integration for the specified Amazon Connect instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaignsv2/client/put_connect_instance_integration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaignsv2/client/#put_connect_instance_integration)
        """

    async def put_instance_communication_limits(
        self, **kwargs: Unpack[PutInstanceCommunicationLimitsRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Put the instance communication limits.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaignsv2/client/put_instance_communication_limits.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaignsv2/client/#put_instance_communication_limits)
        """

    async def put_outbound_request_batch(
        self, **kwargs: Unpack[PutOutboundRequestBatchRequestTypeDef]
    ) -> PutOutboundRequestBatchResponseTypeDef:
        """
        Creates outbound requests for the specified campaign Amazon Connect account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaignsv2/client/put_outbound_request_batch.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaignsv2/client/#put_outbound_request_batch)
        """

    async def put_profile_outbound_request_batch(
        self, **kwargs: Unpack[PutProfileOutboundRequestBatchRequestTypeDef]
    ) -> PutProfileOutboundRequestBatchResponseTypeDef:
        """
        Takes in a list of profile outbound requests to be placed as part of an
        outbound campaign.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaignsv2/client/put_profile_outbound_request_batch.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaignsv2/client/#put_profile_outbound_request_batch)
        """

    async def resume_campaign(
        self, **kwargs: Unpack[ResumeCampaignRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Stops a campaign for the specified Amazon Connect account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaignsv2/client/resume_campaign.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaignsv2/client/#resume_campaign)
        """

    async def start_campaign(
        self, **kwargs: Unpack[StartCampaignRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Starts a campaign for the specified Amazon Connect account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaignsv2/client/start_campaign.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaignsv2/client/#start_campaign)
        """

    async def start_instance_onboarding_job(
        self, **kwargs: Unpack[StartInstanceOnboardingJobRequestTypeDef]
    ) -> StartInstanceOnboardingJobResponseTypeDef:
        """
        Onboard the specific Amazon Connect instance to Connect Campaigns.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaignsv2/client/start_instance_onboarding_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaignsv2/client/#start_instance_onboarding_job)
        """

    async def stop_campaign(
        self, **kwargs: Unpack[StopCampaignRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Stops a campaign for the specified Amazon Connect account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaignsv2/client/stop_campaign.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaignsv2/client/#stop_campaign)
        """

    async def tag_resource(
        self, **kwargs: Unpack[TagResourceRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Tag a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaignsv2/client/tag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaignsv2/client/#tag_resource)
        """

    async def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Untag a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaignsv2/client/untag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaignsv2/client/#untag_resource)
        """

    async def update_campaign_channel_subtype_config(
        self, **kwargs: Unpack[UpdateCampaignChannelSubtypeConfigRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates the channel subtype config of a campaign.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaignsv2/client/update_campaign_channel_subtype_config.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaignsv2/client/#update_campaign_channel_subtype_config)
        """

    async def update_campaign_communication_limits(
        self, **kwargs: Unpack[UpdateCampaignCommunicationLimitsRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates the communication limits config for a campaign.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaignsv2/client/update_campaign_communication_limits.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaignsv2/client/#update_campaign_communication_limits)
        """

    async def update_campaign_communication_time(
        self, **kwargs: Unpack[UpdateCampaignCommunicationTimeRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates the communication time config for a campaign.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaignsv2/client/update_campaign_communication_time.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaignsv2/client/#update_campaign_communication_time)
        """

    async def update_campaign_flow_association(
        self, **kwargs: Unpack[UpdateCampaignFlowAssociationRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates the campaign flow associated with a campaign.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaignsv2/client/update_campaign_flow_association.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaignsv2/client/#update_campaign_flow_association)
        """

    async def update_campaign_name(
        self, **kwargs: Unpack[UpdateCampaignNameRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates the name of a campaign.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaignsv2/client/update_campaign_name.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaignsv2/client/#update_campaign_name)
        """

    async def update_campaign_schedule(
        self, **kwargs: Unpack[UpdateCampaignScheduleRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates the schedule for a campaign.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaignsv2/client/update_campaign_schedule.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaignsv2/client/#update_campaign_schedule)
        """

    async def update_campaign_source(
        self, **kwargs: Unpack[UpdateCampaignSourceRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates the campaign source with a campaign.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaignsv2/client/update_campaign_source.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaignsv2/client/#update_campaign_source)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_campaigns"]
    ) -> ListCampaignsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaignsv2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaignsv2/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_connect_instance_integrations"]
    ) -> ListConnectInstanceIntegrationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaignsv2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaignsv2/client/#get_paginator)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaignsv2.html#ConnectCampaignServiceV2.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaignsv2/client/)
        """

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaignsv2.html#ConnectCampaignServiceV2.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaignsv2/client/)
        """
