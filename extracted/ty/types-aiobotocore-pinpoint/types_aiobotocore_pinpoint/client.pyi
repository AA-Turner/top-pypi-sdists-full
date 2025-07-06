"""
Type annotations for pinpoint service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_pinpoint.client import PinpointClient

    session = get_session()
    async with session.create_client("pinpoint") as client:
        client: PinpointClient
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
    CreateAppRequestTypeDef,
    CreateAppResponseTypeDef,
    CreateCampaignRequestTypeDef,
    CreateCampaignResponseTypeDef,
    CreateEmailTemplateRequestTypeDef,
    CreateEmailTemplateResponseTypeDef,
    CreateExportJobRequestTypeDef,
    CreateExportJobResponseTypeDef,
    CreateImportJobRequestTypeDef,
    CreateImportJobResponseTypeDef,
    CreateInAppTemplateRequestTypeDef,
    CreateInAppTemplateResponseTypeDef,
    CreateJourneyRequestTypeDef,
    CreateJourneyResponseTypeDef,
    CreatePushTemplateRequestTypeDef,
    CreatePushTemplateResponseTypeDef,
    CreateRecommenderConfigurationRequestTypeDef,
    CreateRecommenderConfigurationResponseTypeDef,
    CreateSegmentRequestTypeDef,
    CreateSegmentResponseTypeDef,
    CreateSmsTemplateRequestTypeDef,
    CreateSmsTemplateResponseTypeDef,
    CreateVoiceTemplateRequestTypeDef,
    CreateVoiceTemplateResponseTypeDef,
    DeleteAdmChannelRequestTypeDef,
    DeleteAdmChannelResponseTypeDef,
    DeleteApnsChannelRequestTypeDef,
    DeleteApnsChannelResponseTypeDef,
    DeleteApnsSandboxChannelRequestTypeDef,
    DeleteApnsSandboxChannelResponseTypeDef,
    DeleteApnsVoipChannelRequestTypeDef,
    DeleteApnsVoipChannelResponseTypeDef,
    DeleteApnsVoipSandboxChannelRequestTypeDef,
    DeleteApnsVoipSandboxChannelResponseTypeDef,
    DeleteAppRequestTypeDef,
    DeleteAppResponseTypeDef,
    DeleteBaiduChannelRequestTypeDef,
    DeleteBaiduChannelResponseTypeDef,
    DeleteCampaignRequestTypeDef,
    DeleteCampaignResponseTypeDef,
    DeleteEmailChannelRequestTypeDef,
    DeleteEmailChannelResponseTypeDef,
    DeleteEmailTemplateRequestTypeDef,
    DeleteEmailTemplateResponseTypeDef,
    DeleteEndpointRequestTypeDef,
    DeleteEndpointResponseTypeDef,
    DeleteEventStreamRequestTypeDef,
    DeleteEventStreamResponseTypeDef,
    DeleteGcmChannelRequestTypeDef,
    DeleteGcmChannelResponseTypeDef,
    DeleteInAppTemplateRequestTypeDef,
    DeleteInAppTemplateResponseTypeDef,
    DeleteJourneyRequestTypeDef,
    DeleteJourneyResponseTypeDef,
    DeletePushTemplateRequestTypeDef,
    DeletePushTemplateResponseTypeDef,
    DeleteRecommenderConfigurationRequestTypeDef,
    DeleteRecommenderConfigurationResponseTypeDef,
    DeleteSegmentRequestTypeDef,
    DeleteSegmentResponseTypeDef,
    DeleteSmsChannelRequestTypeDef,
    DeleteSmsChannelResponseTypeDef,
    DeleteSmsTemplateRequestTypeDef,
    DeleteSmsTemplateResponseTypeDef,
    DeleteUserEndpointsRequestTypeDef,
    DeleteUserEndpointsResponseTypeDef,
    DeleteVoiceChannelRequestTypeDef,
    DeleteVoiceChannelResponseTypeDef,
    DeleteVoiceTemplateRequestTypeDef,
    DeleteVoiceTemplateResponseTypeDef,
    EmptyResponseMetadataTypeDef,
    GetAdmChannelRequestTypeDef,
    GetAdmChannelResponseTypeDef,
    GetApnsChannelRequestTypeDef,
    GetApnsChannelResponseTypeDef,
    GetApnsSandboxChannelRequestTypeDef,
    GetApnsSandboxChannelResponseTypeDef,
    GetApnsVoipChannelRequestTypeDef,
    GetApnsVoipChannelResponseTypeDef,
    GetApnsVoipSandboxChannelRequestTypeDef,
    GetApnsVoipSandboxChannelResponseTypeDef,
    GetApplicationDateRangeKpiRequestTypeDef,
    GetApplicationDateRangeKpiResponseTypeDef,
    GetApplicationSettingsRequestTypeDef,
    GetApplicationSettingsResponseTypeDef,
    GetAppRequestTypeDef,
    GetAppResponseTypeDef,
    GetAppsRequestTypeDef,
    GetAppsResponseTypeDef,
    GetBaiduChannelRequestTypeDef,
    GetBaiduChannelResponseTypeDef,
    GetCampaignActivitiesRequestTypeDef,
    GetCampaignActivitiesResponseTypeDef,
    GetCampaignDateRangeKpiRequestTypeDef,
    GetCampaignDateRangeKpiResponseTypeDef,
    GetCampaignRequestTypeDef,
    GetCampaignResponseTypeDef,
    GetCampaignsRequestTypeDef,
    GetCampaignsResponseTypeDef,
    GetCampaignVersionRequestTypeDef,
    GetCampaignVersionResponseTypeDef,
    GetCampaignVersionsRequestTypeDef,
    GetCampaignVersionsResponseTypeDef,
    GetChannelsRequestTypeDef,
    GetChannelsResponseTypeDef,
    GetEmailChannelRequestTypeDef,
    GetEmailChannelResponseTypeDef,
    GetEmailTemplateRequestTypeDef,
    GetEmailTemplateResponseTypeDef,
    GetEndpointRequestTypeDef,
    GetEndpointResponseTypeDef,
    GetEventStreamRequestTypeDef,
    GetEventStreamResponseTypeDef,
    GetExportJobRequestTypeDef,
    GetExportJobResponseTypeDef,
    GetExportJobsRequestTypeDef,
    GetExportJobsResponseTypeDef,
    GetGcmChannelRequestTypeDef,
    GetGcmChannelResponseTypeDef,
    GetImportJobRequestTypeDef,
    GetImportJobResponseTypeDef,
    GetImportJobsRequestTypeDef,
    GetImportJobsResponseTypeDef,
    GetInAppMessagesRequestTypeDef,
    GetInAppMessagesResponseTypeDef,
    GetInAppTemplateRequestTypeDef,
    GetInAppTemplateResponseTypeDef,
    GetJourneyDateRangeKpiRequestTypeDef,
    GetJourneyDateRangeKpiResponseTypeDef,
    GetJourneyExecutionActivityMetricsRequestTypeDef,
    GetJourneyExecutionActivityMetricsResponseTypeDef,
    GetJourneyExecutionMetricsRequestTypeDef,
    GetJourneyExecutionMetricsResponseTypeDef,
    GetJourneyRequestTypeDef,
    GetJourneyResponseTypeDef,
    GetJourneyRunExecutionActivityMetricsRequestTypeDef,
    GetJourneyRunExecutionActivityMetricsResponseTypeDef,
    GetJourneyRunExecutionMetricsRequestTypeDef,
    GetJourneyRunExecutionMetricsResponseTypeDef,
    GetJourneyRunsRequestTypeDef,
    GetJourneyRunsResponseTypeDef,
    GetPushTemplateRequestTypeDef,
    GetPushTemplateResponseTypeDef,
    GetRecommenderConfigurationRequestTypeDef,
    GetRecommenderConfigurationResponseTypeDef,
    GetRecommenderConfigurationsRequestTypeDef,
    GetRecommenderConfigurationsResponseTypeDef,
    GetSegmentExportJobsRequestTypeDef,
    GetSegmentExportJobsResponseTypeDef,
    GetSegmentImportJobsRequestTypeDef,
    GetSegmentImportJobsResponseTypeDef,
    GetSegmentRequestTypeDef,
    GetSegmentResponseTypeDef,
    GetSegmentsRequestTypeDef,
    GetSegmentsResponseTypeDef,
    GetSegmentVersionRequestTypeDef,
    GetSegmentVersionResponseTypeDef,
    GetSegmentVersionsRequestTypeDef,
    GetSegmentVersionsResponseTypeDef,
    GetSmsChannelRequestTypeDef,
    GetSmsChannelResponseTypeDef,
    GetSmsTemplateRequestTypeDef,
    GetSmsTemplateResponseTypeDef,
    GetUserEndpointsRequestTypeDef,
    GetUserEndpointsResponseTypeDef,
    GetVoiceChannelRequestTypeDef,
    GetVoiceChannelResponseTypeDef,
    GetVoiceTemplateRequestTypeDef,
    GetVoiceTemplateResponseTypeDef,
    ListJourneysRequestTypeDef,
    ListJourneysResponseTypeDef,
    ListTagsForResourceRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListTemplatesRequestTypeDef,
    ListTemplatesResponseTypeDef,
    ListTemplateVersionsRequestTypeDef,
    ListTemplateVersionsResponseTypeDef,
    PhoneNumberValidateRequestTypeDef,
    PhoneNumberValidateResponseTypeDef,
    PutEventsRequestTypeDef,
    PutEventsResponseTypeDef,
    PutEventStreamRequestTypeDef,
    PutEventStreamResponseTypeDef,
    RemoveAttributesRequestTypeDef,
    RemoveAttributesResponseTypeDef,
    SendMessagesRequestTypeDef,
    SendMessagesResponseTypeDef,
    SendOTPMessageRequestTypeDef,
    SendOTPMessageResponseTypeDef,
    SendUsersMessagesRequestTypeDef,
    SendUsersMessagesResponseTypeDef,
    TagResourceRequestTypeDef,
    UntagResourceRequestTypeDef,
    UpdateAdmChannelRequestTypeDef,
    UpdateAdmChannelResponseTypeDef,
    UpdateApnsChannelRequestTypeDef,
    UpdateApnsChannelResponseTypeDef,
    UpdateApnsSandboxChannelRequestTypeDef,
    UpdateApnsSandboxChannelResponseTypeDef,
    UpdateApnsVoipChannelRequestTypeDef,
    UpdateApnsVoipChannelResponseTypeDef,
    UpdateApnsVoipSandboxChannelRequestTypeDef,
    UpdateApnsVoipSandboxChannelResponseTypeDef,
    UpdateApplicationSettingsRequestTypeDef,
    UpdateApplicationSettingsResponseTypeDef,
    UpdateBaiduChannelRequestTypeDef,
    UpdateBaiduChannelResponseTypeDef,
    UpdateCampaignRequestTypeDef,
    UpdateCampaignResponseTypeDef,
    UpdateEmailChannelRequestTypeDef,
    UpdateEmailChannelResponseTypeDef,
    UpdateEmailTemplateRequestTypeDef,
    UpdateEmailTemplateResponseTypeDef,
    UpdateEndpointRequestTypeDef,
    UpdateEndpointResponseTypeDef,
    UpdateEndpointsBatchRequestTypeDef,
    UpdateEndpointsBatchResponseTypeDef,
    UpdateGcmChannelRequestTypeDef,
    UpdateGcmChannelResponseTypeDef,
    UpdateInAppTemplateRequestTypeDef,
    UpdateInAppTemplateResponseTypeDef,
    UpdateJourneyRequestTypeDef,
    UpdateJourneyResponseTypeDef,
    UpdateJourneyStateRequestTypeDef,
    UpdateJourneyStateResponseTypeDef,
    UpdatePushTemplateRequestTypeDef,
    UpdatePushTemplateResponseTypeDef,
    UpdateRecommenderConfigurationRequestTypeDef,
    UpdateRecommenderConfigurationResponseTypeDef,
    UpdateSegmentRequestTypeDef,
    UpdateSegmentResponseTypeDef,
    UpdateSmsChannelRequestTypeDef,
    UpdateSmsChannelResponseTypeDef,
    UpdateSmsTemplateRequestTypeDef,
    UpdateSmsTemplateResponseTypeDef,
    UpdateTemplateActiveVersionRequestTypeDef,
    UpdateTemplateActiveVersionResponseTypeDef,
    UpdateVoiceChannelRequestTypeDef,
    UpdateVoiceChannelResponseTypeDef,
    UpdateVoiceTemplateRequestTypeDef,
    UpdateVoiceTemplateResponseTypeDef,
    VerifyOTPMessageRequestTypeDef,
    VerifyOTPMessageResponseTypeDef,
)

if sys.version_info >= (3, 9):
    from builtins import type as Type
    from collections.abc import Mapping
else:
    from typing import Mapping, Type
if sys.version_info >= (3, 12):
    from typing import Self, Unpack
else:
    from typing_extensions import Self, Unpack

__all__ = ("PinpointClient",)

class Exceptions(BaseClientExceptions):
    BadRequestException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    ForbiddenException: Type[BotocoreClientError]
    InternalServerErrorException: Type[BotocoreClientError]
    MethodNotAllowedException: Type[BotocoreClientError]
    NotFoundException: Type[BotocoreClientError]
    PayloadTooLargeException: Type[BotocoreClientError]
    TooManyRequestsException: Type[BotocoreClientError]

class PinpointClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint.html#Pinpoint.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        PinpointClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint.html#Pinpoint.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/can_paginate.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/generate_presigned_url.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#generate_presigned_url)
        """

    async def create_app(
        self, **kwargs: Unpack[CreateAppRequestTypeDef]
    ) -> CreateAppResponseTypeDef:
        """
        Creates an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/create_app.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#create_app)
        """

    async def create_campaign(
        self, **kwargs: Unpack[CreateCampaignRequestTypeDef]
    ) -> CreateCampaignResponseTypeDef:
        """
        Creates a new campaign for an application or updates the settings of an
        existing campaign for an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/create_campaign.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#create_campaign)
        """

    async def create_email_template(
        self, **kwargs: Unpack[CreateEmailTemplateRequestTypeDef]
    ) -> CreateEmailTemplateResponseTypeDef:
        """
        Creates a message template for messages that are sent through the email channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/create_email_template.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#create_email_template)
        """

    async def create_export_job(
        self, **kwargs: Unpack[CreateExportJobRequestTypeDef]
    ) -> CreateExportJobResponseTypeDef:
        """
        Creates an export job for an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/create_export_job.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#create_export_job)
        """

    async def create_import_job(
        self, **kwargs: Unpack[CreateImportJobRequestTypeDef]
    ) -> CreateImportJobResponseTypeDef:
        """
        Creates an import job for an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/create_import_job.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#create_import_job)
        """

    async def create_in_app_template(
        self, **kwargs: Unpack[CreateInAppTemplateRequestTypeDef]
    ) -> CreateInAppTemplateResponseTypeDef:
        """
        Creates a new message template for messages using the in-app message channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/create_in_app_template.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#create_in_app_template)
        """

    async def create_journey(
        self, **kwargs: Unpack[CreateJourneyRequestTypeDef]
    ) -> CreateJourneyResponseTypeDef:
        """
        Creates a journey for an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/create_journey.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#create_journey)
        """

    async def create_push_template(
        self, **kwargs: Unpack[CreatePushTemplateRequestTypeDef]
    ) -> CreatePushTemplateResponseTypeDef:
        """
        Creates a message template for messages that are sent through a push
        notification channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/create_push_template.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#create_push_template)
        """

    async def create_recommender_configuration(
        self, **kwargs: Unpack[CreateRecommenderConfigurationRequestTypeDef]
    ) -> CreateRecommenderConfigurationResponseTypeDef:
        """
        Creates an Amazon Pinpoint configuration for a recommender model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/create_recommender_configuration.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#create_recommender_configuration)
        """

    async def create_segment(
        self, **kwargs: Unpack[CreateSegmentRequestTypeDef]
    ) -> CreateSegmentResponseTypeDef:
        """
        Creates a new segment for an application or updates the configuration,
        dimension, and other settings for an existing segment that's associated with an
        application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/create_segment.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#create_segment)
        """

    async def create_sms_template(
        self, **kwargs: Unpack[CreateSmsTemplateRequestTypeDef]
    ) -> CreateSmsTemplateResponseTypeDef:
        """
        Creates a message template for messages that are sent through the SMS channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/create_sms_template.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#create_sms_template)
        """

    async def create_voice_template(
        self, **kwargs: Unpack[CreateVoiceTemplateRequestTypeDef]
    ) -> CreateVoiceTemplateResponseTypeDef:
        """
        Creates a message template for messages that are sent through the voice channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/create_voice_template.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#create_voice_template)
        """

    async def delete_adm_channel(
        self, **kwargs: Unpack[DeleteAdmChannelRequestTypeDef]
    ) -> DeleteAdmChannelResponseTypeDef:
        """
        Disables the ADM channel for an application and deletes any existing settings
        for the channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/delete_adm_channel.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#delete_adm_channel)
        """

    async def delete_apns_channel(
        self, **kwargs: Unpack[DeleteApnsChannelRequestTypeDef]
    ) -> DeleteApnsChannelResponseTypeDef:
        """
        Disables the APNs channel for an application and deletes any existing settings
        for the channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/delete_apns_channel.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#delete_apns_channel)
        """

    async def delete_apns_sandbox_channel(
        self, **kwargs: Unpack[DeleteApnsSandboxChannelRequestTypeDef]
    ) -> DeleteApnsSandboxChannelResponseTypeDef:
        """
        Disables the APNs sandbox channel for an application and deletes any existing
        settings for the channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/delete_apns_sandbox_channel.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#delete_apns_sandbox_channel)
        """

    async def delete_apns_voip_channel(
        self, **kwargs: Unpack[DeleteApnsVoipChannelRequestTypeDef]
    ) -> DeleteApnsVoipChannelResponseTypeDef:
        """
        Disables the APNs VoIP channel for an application and deletes any existing
        settings for the channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/delete_apns_voip_channel.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#delete_apns_voip_channel)
        """

    async def delete_apns_voip_sandbox_channel(
        self, **kwargs: Unpack[DeleteApnsVoipSandboxChannelRequestTypeDef]
    ) -> DeleteApnsVoipSandboxChannelResponseTypeDef:
        """
        Disables the APNs VoIP sandbox channel for an application and deletes any
        existing settings for the channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/delete_apns_voip_sandbox_channel.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#delete_apns_voip_sandbox_channel)
        """

    async def delete_app(
        self, **kwargs: Unpack[DeleteAppRequestTypeDef]
    ) -> DeleteAppResponseTypeDef:
        """
        Deletes an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/delete_app.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#delete_app)
        """

    async def delete_baidu_channel(
        self, **kwargs: Unpack[DeleteBaiduChannelRequestTypeDef]
    ) -> DeleteBaiduChannelResponseTypeDef:
        """
        Disables the Baidu channel for an application and deletes any existing settings
        for the channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/delete_baidu_channel.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#delete_baidu_channel)
        """

    async def delete_campaign(
        self, **kwargs: Unpack[DeleteCampaignRequestTypeDef]
    ) -> DeleteCampaignResponseTypeDef:
        """
        Deletes a campaign from an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/delete_campaign.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#delete_campaign)
        """

    async def delete_email_channel(
        self, **kwargs: Unpack[DeleteEmailChannelRequestTypeDef]
    ) -> DeleteEmailChannelResponseTypeDef:
        """
        Disables the email channel for an application and deletes any existing settings
        for the channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/delete_email_channel.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#delete_email_channel)
        """

    async def delete_email_template(
        self, **kwargs: Unpack[DeleteEmailTemplateRequestTypeDef]
    ) -> DeleteEmailTemplateResponseTypeDef:
        """
        Deletes a message template for messages that were sent through the email
        channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/delete_email_template.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#delete_email_template)
        """

    async def delete_endpoint(
        self, **kwargs: Unpack[DeleteEndpointRequestTypeDef]
    ) -> DeleteEndpointResponseTypeDef:
        """
        Deletes an endpoint from an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/delete_endpoint.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#delete_endpoint)
        """

    async def delete_event_stream(
        self, **kwargs: Unpack[DeleteEventStreamRequestTypeDef]
    ) -> DeleteEventStreamResponseTypeDef:
        """
        Deletes the event stream for an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/delete_event_stream.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#delete_event_stream)
        """

    async def delete_gcm_channel(
        self, **kwargs: Unpack[DeleteGcmChannelRequestTypeDef]
    ) -> DeleteGcmChannelResponseTypeDef:
        """
        Disables the GCM channel for an application and deletes any existing settings
        for the channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/delete_gcm_channel.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#delete_gcm_channel)
        """

    async def delete_in_app_template(
        self, **kwargs: Unpack[DeleteInAppTemplateRequestTypeDef]
    ) -> DeleteInAppTemplateResponseTypeDef:
        """
        Deletes a message template for messages sent using the in-app message channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/delete_in_app_template.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#delete_in_app_template)
        """

    async def delete_journey(
        self, **kwargs: Unpack[DeleteJourneyRequestTypeDef]
    ) -> DeleteJourneyResponseTypeDef:
        """
        Deletes a journey from an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/delete_journey.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#delete_journey)
        """

    async def delete_push_template(
        self, **kwargs: Unpack[DeletePushTemplateRequestTypeDef]
    ) -> DeletePushTemplateResponseTypeDef:
        """
        Deletes a message template for messages that were sent through a push
        notification channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/delete_push_template.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#delete_push_template)
        """

    async def delete_recommender_configuration(
        self, **kwargs: Unpack[DeleteRecommenderConfigurationRequestTypeDef]
    ) -> DeleteRecommenderConfigurationResponseTypeDef:
        """
        Deletes an Amazon Pinpoint configuration for a recommender model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/delete_recommender_configuration.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#delete_recommender_configuration)
        """

    async def delete_segment(
        self, **kwargs: Unpack[DeleteSegmentRequestTypeDef]
    ) -> DeleteSegmentResponseTypeDef:
        """
        Deletes a segment from an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/delete_segment.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#delete_segment)
        """

    async def delete_sms_channel(
        self, **kwargs: Unpack[DeleteSmsChannelRequestTypeDef]
    ) -> DeleteSmsChannelResponseTypeDef:
        """
        Disables the SMS channel for an application and deletes any existing settings
        for the channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/delete_sms_channel.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#delete_sms_channel)
        """

    async def delete_sms_template(
        self, **kwargs: Unpack[DeleteSmsTemplateRequestTypeDef]
    ) -> DeleteSmsTemplateResponseTypeDef:
        """
        Deletes a message template for messages that were sent through the SMS channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/delete_sms_template.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#delete_sms_template)
        """

    async def delete_user_endpoints(
        self, **kwargs: Unpack[DeleteUserEndpointsRequestTypeDef]
    ) -> DeleteUserEndpointsResponseTypeDef:
        """
        Deletes all the endpoints that are associated with a specific user ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/delete_user_endpoints.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#delete_user_endpoints)
        """

    async def delete_voice_channel(
        self, **kwargs: Unpack[DeleteVoiceChannelRequestTypeDef]
    ) -> DeleteVoiceChannelResponseTypeDef:
        """
        Disables the voice channel for an application and deletes any existing settings
        for the channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/delete_voice_channel.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#delete_voice_channel)
        """

    async def delete_voice_template(
        self, **kwargs: Unpack[DeleteVoiceTemplateRequestTypeDef]
    ) -> DeleteVoiceTemplateResponseTypeDef:
        """
        Deletes a message template for messages that were sent through the voice
        channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/delete_voice_template.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#delete_voice_template)
        """

    async def get_adm_channel(
        self, **kwargs: Unpack[GetAdmChannelRequestTypeDef]
    ) -> GetAdmChannelResponseTypeDef:
        """
        Retrieves information about the status and settings of the ADM channel for an
        application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/get_adm_channel.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#get_adm_channel)
        """

    async def get_apns_channel(
        self, **kwargs: Unpack[GetApnsChannelRequestTypeDef]
    ) -> GetApnsChannelResponseTypeDef:
        """
        Retrieves information about the status and settings of the APNs channel for an
        application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/get_apns_channel.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#get_apns_channel)
        """

    async def get_apns_sandbox_channel(
        self, **kwargs: Unpack[GetApnsSandboxChannelRequestTypeDef]
    ) -> GetApnsSandboxChannelResponseTypeDef:
        """
        Retrieves information about the status and settings of the APNs sandbox channel
        for an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/get_apns_sandbox_channel.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#get_apns_sandbox_channel)
        """

    async def get_apns_voip_channel(
        self, **kwargs: Unpack[GetApnsVoipChannelRequestTypeDef]
    ) -> GetApnsVoipChannelResponseTypeDef:
        """
        Retrieves information about the status and settings of the APNs VoIP channel
        for an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/get_apns_voip_channel.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#get_apns_voip_channel)
        """

    async def get_apns_voip_sandbox_channel(
        self, **kwargs: Unpack[GetApnsVoipSandboxChannelRequestTypeDef]
    ) -> GetApnsVoipSandboxChannelResponseTypeDef:
        """
        Retrieves information about the status and settings of the APNs VoIP sandbox
        channel for an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/get_apns_voip_sandbox_channel.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#get_apns_voip_sandbox_channel)
        """

    async def get_app(self, **kwargs: Unpack[GetAppRequestTypeDef]) -> GetAppResponseTypeDef:
        """
        Retrieves information about an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/get_app.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#get_app)
        """

    async def get_application_date_range_kpi(
        self, **kwargs: Unpack[GetApplicationDateRangeKpiRequestTypeDef]
    ) -> GetApplicationDateRangeKpiResponseTypeDef:
        """
        Retrieves (queries) pre-aggregated data for a standard metric that applies to
        an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/get_application_date_range_kpi.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#get_application_date_range_kpi)
        """

    async def get_application_settings(
        self, **kwargs: Unpack[GetApplicationSettingsRequestTypeDef]
    ) -> GetApplicationSettingsResponseTypeDef:
        """
        Retrieves information about the settings for an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/get_application_settings.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#get_application_settings)
        """

    async def get_apps(self, **kwargs: Unpack[GetAppsRequestTypeDef]) -> GetAppsResponseTypeDef:
        """
        Retrieves information about all the applications that are associated with your
        Amazon Pinpoint account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/get_apps.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#get_apps)
        """

    async def get_baidu_channel(
        self, **kwargs: Unpack[GetBaiduChannelRequestTypeDef]
    ) -> GetBaiduChannelResponseTypeDef:
        """
        Retrieves information about the status and settings of the Baidu channel for an
        application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/get_baidu_channel.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#get_baidu_channel)
        """

    async def get_campaign(
        self, **kwargs: Unpack[GetCampaignRequestTypeDef]
    ) -> GetCampaignResponseTypeDef:
        """
        Retrieves information about the status, configuration, and other settings for a
        campaign.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/get_campaign.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#get_campaign)
        """

    async def get_campaign_activities(
        self, **kwargs: Unpack[GetCampaignActivitiesRequestTypeDef]
    ) -> GetCampaignActivitiesResponseTypeDef:
        """
        Retrieves information about all the activities for a campaign.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/get_campaign_activities.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#get_campaign_activities)
        """

    async def get_campaign_date_range_kpi(
        self, **kwargs: Unpack[GetCampaignDateRangeKpiRequestTypeDef]
    ) -> GetCampaignDateRangeKpiResponseTypeDef:
        """
        Retrieves (queries) pre-aggregated data for a standard metric that applies to a
        campaign.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/get_campaign_date_range_kpi.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#get_campaign_date_range_kpi)
        """

    async def get_campaign_version(
        self, **kwargs: Unpack[GetCampaignVersionRequestTypeDef]
    ) -> GetCampaignVersionResponseTypeDef:
        """
        Retrieves information about the status, configuration, and other settings for a
        specific version of a campaign.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/get_campaign_version.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#get_campaign_version)
        """

    async def get_campaign_versions(
        self, **kwargs: Unpack[GetCampaignVersionsRequestTypeDef]
    ) -> GetCampaignVersionsResponseTypeDef:
        """
        Retrieves information about the status, configuration, and other settings for
        all versions of a campaign.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/get_campaign_versions.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#get_campaign_versions)
        """

    async def get_campaigns(
        self, **kwargs: Unpack[GetCampaignsRequestTypeDef]
    ) -> GetCampaignsResponseTypeDef:
        """
        Retrieves information about the status, configuration, and other settings for
        all the campaigns that are associated with an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/get_campaigns.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#get_campaigns)
        """

    async def get_channels(
        self, **kwargs: Unpack[GetChannelsRequestTypeDef]
    ) -> GetChannelsResponseTypeDef:
        """
        Retrieves information about the history and status of each channel for an
        application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/get_channels.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#get_channels)
        """

    async def get_email_channel(
        self, **kwargs: Unpack[GetEmailChannelRequestTypeDef]
    ) -> GetEmailChannelResponseTypeDef:
        """
        Retrieves information about the status and settings of the email channel for an
        application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/get_email_channel.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#get_email_channel)
        """

    async def get_email_template(
        self, **kwargs: Unpack[GetEmailTemplateRequestTypeDef]
    ) -> GetEmailTemplateResponseTypeDef:
        """
        Retrieves the content and settings of a message template for messages that are
        sent through the email channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/get_email_template.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#get_email_template)
        """

    async def get_endpoint(
        self, **kwargs: Unpack[GetEndpointRequestTypeDef]
    ) -> GetEndpointResponseTypeDef:
        """
        Retrieves information about the settings and attributes of a specific endpoint
        for an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/get_endpoint.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#get_endpoint)
        """

    async def get_event_stream(
        self, **kwargs: Unpack[GetEventStreamRequestTypeDef]
    ) -> GetEventStreamResponseTypeDef:
        """
        Retrieves information about the event stream settings for an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/get_event_stream.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#get_event_stream)
        """

    async def get_export_job(
        self, **kwargs: Unpack[GetExportJobRequestTypeDef]
    ) -> GetExportJobResponseTypeDef:
        """
        Retrieves information about the status and settings of a specific export job
        for an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/get_export_job.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#get_export_job)
        """

    async def get_export_jobs(
        self, **kwargs: Unpack[GetExportJobsRequestTypeDef]
    ) -> GetExportJobsResponseTypeDef:
        """
        Retrieves information about the status and settings of all the export jobs for
        an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/get_export_jobs.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#get_export_jobs)
        """

    async def get_gcm_channel(
        self, **kwargs: Unpack[GetGcmChannelRequestTypeDef]
    ) -> GetGcmChannelResponseTypeDef:
        """
        Retrieves information about the status and settings of the GCM channel for an
        application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/get_gcm_channel.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#get_gcm_channel)
        """

    async def get_import_job(
        self, **kwargs: Unpack[GetImportJobRequestTypeDef]
    ) -> GetImportJobResponseTypeDef:
        """
        Retrieves information about the status and settings of a specific import job
        for an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/get_import_job.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#get_import_job)
        """

    async def get_import_jobs(
        self, **kwargs: Unpack[GetImportJobsRequestTypeDef]
    ) -> GetImportJobsResponseTypeDef:
        """
        Retrieves information about the status and settings of all the import jobs for
        an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/get_import_jobs.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#get_import_jobs)
        """

    async def get_in_app_messages(
        self, **kwargs: Unpack[GetInAppMessagesRequestTypeDef]
    ) -> GetInAppMessagesResponseTypeDef:
        """
        Retrieves the in-app messages targeted for the provided endpoint ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/get_in_app_messages.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#get_in_app_messages)
        """

    async def get_in_app_template(
        self, **kwargs: Unpack[GetInAppTemplateRequestTypeDef]
    ) -> GetInAppTemplateResponseTypeDef:
        """
        Retrieves the content and settings of a message template for messages sent
        through the in-app channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/get_in_app_template.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#get_in_app_template)
        """

    async def get_journey(
        self, **kwargs: Unpack[GetJourneyRequestTypeDef]
    ) -> GetJourneyResponseTypeDef:
        """
        Retrieves information about the status, configuration, and other settings for a
        journey.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/get_journey.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#get_journey)
        """

    async def get_journey_date_range_kpi(
        self, **kwargs: Unpack[GetJourneyDateRangeKpiRequestTypeDef]
    ) -> GetJourneyDateRangeKpiResponseTypeDef:
        """
        Retrieves (queries) pre-aggregated data for a standard engagement metric that
        applies to a journey.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/get_journey_date_range_kpi.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#get_journey_date_range_kpi)
        """

    async def get_journey_execution_activity_metrics(
        self, **kwargs: Unpack[GetJourneyExecutionActivityMetricsRequestTypeDef]
    ) -> GetJourneyExecutionActivityMetricsResponseTypeDef:
        """
        Retrieves (queries) pre-aggregated data for a standard execution metric that
        applies to a journey activity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/get_journey_execution_activity_metrics.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#get_journey_execution_activity_metrics)
        """

    async def get_journey_execution_metrics(
        self, **kwargs: Unpack[GetJourneyExecutionMetricsRequestTypeDef]
    ) -> GetJourneyExecutionMetricsResponseTypeDef:
        """
        Retrieves (queries) pre-aggregated data for a standard execution metric that
        applies to a journey.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/get_journey_execution_metrics.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#get_journey_execution_metrics)
        """

    async def get_journey_run_execution_activity_metrics(
        self, **kwargs: Unpack[GetJourneyRunExecutionActivityMetricsRequestTypeDef]
    ) -> GetJourneyRunExecutionActivityMetricsResponseTypeDef:
        """
        Retrieves (queries) pre-aggregated data for a standard run execution metric
        that applies to a journey activity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/get_journey_run_execution_activity_metrics.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#get_journey_run_execution_activity_metrics)
        """

    async def get_journey_run_execution_metrics(
        self, **kwargs: Unpack[GetJourneyRunExecutionMetricsRequestTypeDef]
    ) -> GetJourneyRunExecutionMetricsResponseTypeDef:
        """
        Retrieves (queries) pre-aggregated data for a standard run execution metric
        that applies to a journey.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/get_journey_run_execution_metrics.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#get_journey_run_execution_metrics)
        """

    async def get_journey_runs(
        self, **kwargs: Unpack[GetJourneyRunsRequestTypeDef]
    ) -> GetJourneyRunsResponseTypeDef:
        """
        Provides information about the runs of a journey.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/get_journey_runs.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#get_journey_runs)
        """

    async def get_push_template(
        self, **kwargs: Unpack[GetPushTemplateRequestTypeDef]
    ) -> GetPushTemplateResponseTypeDef:
        """
        Retrieves the content and settings of a message template for messages that are
        sent through a push notification channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/get_push_template.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#get_push_template)
        """

    async def get_recommender_configuration(
        self, **kwargs: Unpack[GetRecommenderConfigurationRequestTypeDef]
    ) -> GetRecommenderConfigurationResponseTypeDef:
        """
        Retrieves information about an Amazon Pinpoint configuration for a recommender
        model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/get_recommender_configuration.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#get_recommender_configuration)
        """

    async def get_recommender_configurations(
        self, **kwargs: Unpack[GetRecommenderConfigurationsRequestTypeDef]
    ) -> GetRecommenderConfigurationsResponseTypeDef:
        """
        Retrieves information about all the recommender model configurations that are
        associated with your Amazon Pinpoint account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/get_recommender_configurations.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#get_recommender_configurations)
        """

    async def get_segment(
        self, **kwargs: Unpack[GetSegmentRequestTypeDef]
    ) -> GetSegmentResponseTypeDef:
        """
        Retrieves information about the configuration, dimension, and other settings
        for a specific segment that's associated with an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/get_segment.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#get_segment)
        """

    async def get_segment_export_jobs(
        self, **kwargs: Unpack[GetSegmentExportJobsRequestTypeDef]
    ) -> GetSegmentExportJobsResponseTypeDef:
        """
        Retrieves information about the status and settings of the export jobs for a
        segment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/get_segment_export_jobs.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#get_segment_export_jobs)
        """

    async def get_segment_import_jobs(
        self, **kwargs: Unpack[GetSegmentImportJobsRequestTypeDef]
    ) -> GetSegmentImportJobsResponseTypeDef:
        """
        Retrieves information about the status and settings of the import jobs for a
        segment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/get_segment_import_jobs.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#get_segment_import_jobs)
        """

    async def get_segment_version(
        self, **kwargs: Unpack[GetSegmentVersionRequestTypeDef]
    ) -> GetSegmentVersionResponseTypeDef:
        """
        Retrieves information about the configuration, dimension, and other settings
        for a specific version of a segment that's associated with an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/get_segment_version.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#get_segment_version)
        """

    async def get_segment_versions(
        self, **kwargs: Unpack[GetSegmentVersionsRequestTypeDef]
    ) -> GetSegmentVersionsResponseTypeDef:
        """
        Retrieves information about the configuration, dimension, and other settings
        for all the versions of a specific segment that's associated with an
        application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/get_segment_versions.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#get_segment_versions)
        """

    async def get_segments(
        self, **kwargs: Unpack[GetSegmentsRequestTypeDef]
    ) -> GetSegmentsResponseTypeDef:
        """
        Retrieves information about the configuration, dimension, and other settings
        for all the segments that are associated with an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/get_segments.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#get_segments)
        """

    async def get_sms_channel(
        self, **kwargs: Unpack[GetSmsChannelRequestTypeDef]
    ) -> GetSmsChannelResponseTypeDef:
        """
        Retrieves information about the status and settings of the SMS channel for an
        application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/get_sms_channel.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#get_sms_channel)
        """

    async def get_sms_template(
        self, **kwargs: Unpack[GetSmsTemplateRequestTypeDef]
    ) -> GetSmsTemplateResponseTypeDef:
        """
        Retrieves the content and settings of a message template for messages that are
        sent through the SMS channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/get_sms_template.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#get_sms_template)
        """

    async def get_user_endpoints(
        self, **kwargs: Unpack[GetUserEndpointsRequestTypeDef]
    ) -> GetUserEndpointsResponseTypeDef:
        """
        Retrieves information about all the endpoints that are associated with a
        specific user ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/get_user_endpoints.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#get_user_endpoints)
        """

    async def get_voice_channel(
        self, **kwargs: Unpack[GetVoiceChannelRequestTypeDef]
    ) -> GetVoiceChannelResponseTypeDef:
        """
        Retrieves information about the status and settings of the voice channel for an
        application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/get_voice_channel.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#get_voice_channel)
        """

    async def get_voice_template(
        self, **kwargs: Unpack[GetVoiceTemplateRequestTypeDef]
    ) -> GetVoiceTemplateResponseTypeDef:
        """
        Retrieves the content and settings of a message template for messages that are
        sent through the voice channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/get_voice_template.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#get_voice_template)
        """

    async def list_journeys(
        self, **kwargs: Unpack[ListJourneysRequestTypeDef]
    ) -> ListJourneysResponseTypeDef:
        """
        Retrieves information about the status, configuration, and other settings for
        all the journeys that are associated with an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/list_journeys.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#list_journeys)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Retrieves all the tags (keys and values) that are associated with an
        application, campaign, message template, or segment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/list_tags_for_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#list_tags_for_resource)
        """

    async def list_template_versions(
        self, **kwargs: Unpack[ListTemplateVersionsRequestTypeDef]
    ) -> ListTemplateVersionsResponseTypeDef:
        """
        Retrieves information about all the versions of a specific message template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/list_template_versions.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#list_template_versions)
        """

    async def list_templates(
        self, **kwargs: Unpack[ListTemplatesRequestTypeDef]
    ) -> ListTemplatesResponseTypeDef:
        """
        Retrieves information about all the message templates that are associated with
        your Amazon Pinpoint account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/list_templates.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#list_templates)
        """

    async def phone_number_validate(
        self, **kwargs: Unpack[PhoneNumberValidateRequestTypeDef]
    ) -> PhoneNumberValidateResponseTypeDef:
        """
        Retrieves information about a phone number.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/phone_number_validate.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#phone_number_validate)
        """

    async def put_event_stream(
        self, **kwargs: Unpack[PutEventStreamRequestTypeDef]
    ) -> PutEventStreamResponseTypeDef:
        """
        Creates a new event stream for an application or updates the settings of an
        existing event stream for an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/put_event_stream.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#put_event_stream)
        """

    async def put_events(
        self, **kwargs: Unpack[PutEventsRequestTypeDef]
    ) -> PutEventsResponseTypeDef:
        """
        Creates a new event to record for endpoints, or creates or updates endpoint
        data that existing events are associated with.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/put_events.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#put_events)
        """

    async def remove_attributes(
        self, **kwargs: Unpack[RemoveAttributesRequestTypeDef]
    ) -> RemoveAttributesResponseTypeDef:
        """
        Removes one or more custom attributes, of the same attribute type, from the
        application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/remove_attributes.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#remove_attributes)
        """

    async def send_messages(
        self, **kwargs: Unpack[SendMessagesRequestTypeDef]
    ) -> SendMessagesResponseTypeDef:
        """
        Creates and sends a direct message.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/send_messages.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#send_messages)
        """

    async def send_otp_message(
        self, **kwargs: Unpack[SendOTPMessageRequestTypeDef]
    ) -> SendOTPMessageResponseTypeDef:
        """
        Send an OTP message.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/send_otp_message.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#send_otp_message)
        """

    async def send_users_messages(
        self, **kwargs: Unpack[SendUsersMessagesRequestTypeDef]
    ) -> SendUsersMessagesResponseTypeDef:
        """
        Creates and sends a message to a list of users.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/send_users_messages.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#send_users_messages)
        """

    async def tag_resource(
        self, **kwargs: Unpack[TagResourceRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Adds one or more tags (keys and values) to an application, campaign, message
        template, or segment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/tag_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#tag_resource)
        """

    async def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes one or more tags (keys and values) from an application, campaign,
        message template, or segment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/untag_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#untag_resource)
        """

    async def update_adm_channel(
        self, **kwargs: Unpack[UpdateAdmChannelRequestTypeDef]
    ) -> UpdateAdmChannelResponseTypeDef:
        """
        Enables the ADM channel for an application or updates the status and settings
        of the ADM channel for an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/update_adm_channel.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#update_adm_channel)
        """

    async def update_apns_channel(
        self, **kwargs: Unpack[UpdateApnsChannelRequestTypeDef]
    ) -> UpdateApnsChannelResponseTypeDef:
        """
        Enables the APNs channel for an application or updates the status and settings
        of the APNs channel for an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/update_apns_channel.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#update_apns_channel)
        """

    async def update_apns_sandbox_channel(
        self, **kwargs: Unpack[UpdateApnsSandboxChannelRequestTypeDef]
    ) -> UpdateApnsSandboxChannelResponseTypeDef:
        """
        Enables the APNs sandbox channel for an application or updates the status and
        settings of the APNs sandbox channel for an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/update_apns_sandbox_channel.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#update_apns_sandbox_channel)
        """

    async def update_apns_voip_channel(
        self, **kwargs: Unpack[UpdateApnsVoipChannelRequestTypeDef]
    ) -> UpdateApnsVoipChannelResponseTypeDef:
        """
        Enables the APNs VoIP channel for an application or updates the status and
        settings of the APNs VoIP channel for an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/update_apns_voip_channel.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#update_apns_voip_channel)
        """

    async def update_apns_voip_sandbox_channel(
        self, **kwargs: Unpack[UpdateApnsVoipSandboxChannelRequestTypeDef]
    ) -> UpdateApnsVoipSandboxChannelResponseTypeDef:
        """
        Enables the APNs VoIP sandbox channel for an application or updates the status
        and settings of the APNs VoIP sandbox channel for an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/update_apns_voip_sandbox_channel.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#update_apns_voip_sandbox_channel)
        """

    async def update_application_settings(
        self, **kwargs: Unpack[UpdateApplicationSettingsRequestTypeDef]
    ) -> UpdateApplicationSettingsResponseTypeDef:
        """
        Updates the settings for an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/update_application_settings.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#update_application_settings)
        """

    async def update_baidu_channel(
        self, **kwargs: Unpack[UpdateBaiduChannelRequestTypeDef]
    ) -> UpdateBaiduChannelResponseTypeDef:
        """
        Enables the Baidu channel for an application or updates the status and settings
        of the Baidu channel for an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/update_baidu_channel.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#update_baidu_channel)
        """

    async def update_campaign(
        self, **kwargs: Unpack[UpdateCampaignRequestTypeDef]
    ) -> UpdateCampaignResponseTypeDef:
        """
        Updates the configuration and other settings for a campaign.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/update_campaign.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#update_campaign)
        """

    async def update_email_channel(
        self, **kwargs: Unpack[UpdateEmailChannelRequestTypeDef]
    ) -> UpdateEmailChannelResponseTypeDef:
        """
        Enables the email channel for an application or updates the status and settings
        of the email channel for an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/update_email_channel.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#update_email_channel)
        """

    async def update_email_template(
        self, **kwargs: Unpack[UpdateEmailTemplateRequestTypeDef]
    ) -> UpdateEmailTemplateResponseTypeDef:
        """
        Updates an existing message template for messages that are sent through the
        email channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/update_email_template.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#update_email_template)
        """

    async def update_endpoint(
        self, **kwargs: Unpack[UpdateEndpointRequestTypeDef]
    ) -> UpdateEndpointResponseTypeDef:
        """
        Creates a new endpoint for an application or updates the settings and
        attributes of an existing endpoint for an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/update_endpoint.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#update_endpoint)
        """

    async def update_endpoints_batch(
        self, **kwargs: Unpack[UpdateEndpointsBatchRequestTypeDef]
    ) -> UpdateEndpointsBatchResponseTypeDef:
        """
        Creates a new batch of endpoints for an application or updates the settings and
        attributes of a batch of existing endpoints for an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/update_endpoints_batch.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#update_endpoints_batch)
        """

    async def update_gcm_channel(
        self, **kwargs: Unpack[UpdateGcmChannelRequestTypeDef]
    ) -> UpdateGcmChannelResponseTypeDef:
        """
        Enables the GCM channel for an application or updates the status and settings
        of the GCM channel for an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/update_gcm_channel.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#update_gcm_channel)
        """

    async def update_in_app_template(
        self, **kwargs: Unpack[UpdateInAppTemplateRequestTypeDef]
    ) -> UpdateInAppTemplateResponseTypeDef:
        """
        Updates an existing message template for messages sent through the in-app
        message channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/update_in_app_template.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#update_in_app_template)
        """

    async def update_journey(
        self, **kwargs: Unpack[UpdateJourneyRequestTypeDef]
    ) -> UpdateJourneyResponseTypeDef:
        """
        Updates the configuration and other settings for a journey.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/update_journey.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#update_journey)
        """

    async def update_journey_state(
        self, **kwargs: Unpack[UpdateJourneyStateRequestTypeDef]
    ) -> UpdateJourneyStateResponseTypeDef:
        """
        Cancels (stops) an active journey.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/update_journey_state.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#update_journey_state)
        """

    async def update_push_template(
        self, **kwargs: Unpack[UpdatePushTemplateRequestTypeDef]
    ) -> UpdatePushTemplateResponseTypeDef:
        """
        Updates an existing message template for messages that are sent through a push
        notification channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/update_push_template.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#update_push_template)
        """

    async def update_recommender_configuration(
        self, **kwargs: Unpack[UpdateRecommenderConfigurationRequestTypeDef]
    ) -> UpdateRecommenderConfigurationResponseTypeDef:
        """
        Updates an Amazon Pinpoint configuration for a recommender model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/update_recommender_configuration.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#update_recommender_configuration)
        """

    async def update_segment(
        self, **kwargs: Unpack[UpdateSegmentRequestTypeDef]
    ) -> UpdateSegmentResponseTypeDef:
        """
        Creates a new segment for an application or updates the configuration,
        dimension, and other settings for an existing segment that's associated with an
        application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/update_segment.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#update_segment)
        """

    async def update_sms_channel(
        self, **kwargs: Unpack[UpdateSmsChannelRequestTypeDef]
    ) -> UpdateSmsChannelResponseTypeDef:
        """
        Enables the SMS channel for an application or updates the status and settings
        of the SMS channel for an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/update_sms_channel.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#update_sms_channel)
        """

    async def update_sms_template(
        self, **kwargs: Unpack[UpdateSmsTemplateRequestTypeDef]
    ) -> UpdateSmsTemplateResponseTypeDef:
        """
        Updates an existing message template for messages that are sent through the SMS
        channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/update_sms_template.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#update_sms_template)
        """

    async def update_template_active_version(
        self, **kwargs: Unpack[UpdateTemplateActiveVersionRequestTypeDef]
    ) -> UpdateTemplateActiveVersionResponseTypeDef:
        """
        Changes the status of a specific version of a message template to <i>active</i>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/update_template_active_version.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#update_template_active_version)
        """

    async def update_voice_channel(
        self, **kwargs: Unpack[UpdateVoiceChannelRequestTypeDef]
    ) -> UpdateVoiceChannelResponseTypeDef:
        """
        Enables the voice channel for an application or updates the status and settings
        of the voice channel for an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/update_voice_channel.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#update_voice_channel)
        """

    async def update_voice_template(
        self, **kwargs: Unpack[UpdateVoiceTemplateRequestTypeDef]
    ) -> UpdateVoiceTemplateResponseTypeDef:
        """
        Updates an existing message template for messages that are sent through the
        voice channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/update_voice_template.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#update_voice_template)
        """

    async def verify_otp_message(
        self, **kwargs: Unpack[VerifyOTPMessageRequestTypeDef]
    ) -> VerifyOTPMessageResponseTypeDef:
        """
        Verify an OTP.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint/client/verify_otp_message.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/#verify_otp_message)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint.html#Pinpoint.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/)
        """

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint.html#Pinpoint.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint/client/)
        """
