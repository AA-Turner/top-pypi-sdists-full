"""
Type annotations for cloudtrail service Client.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_cloudtrail.client import CloudTrailClient

    session = Session()
    client: CloudTrailClient = session.client("cloudtrail")
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping
from typing import Any, overload

from botocore.client import BaseClient, ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .paginator import (
    ListImportFailuresPaginator,
    ListImportsPaginator,
    ListInsightsDataPaginator,
    ListPublicKeysPaginator,
    ListTagsPaginator,
    ListTrailsPaginator,
    LookupEventsPaginator,
)
from .type_defs import (
    AddTagsRequestTypeDef,
    CancelQueryRequestTypeDef,
    CancelQueryResponseTypeDef,
    CreateChannelRequestTypeDef,
    CreateChannelResponseTypeDef,
    CreateDashboardRequestTypeDef,
    CreateDashboardResponseTypeDef,
    CreateEventDataStoreRequestTypeDef,
    CreateEventDataStoreResponseTypeDef,
    CreateTrailRequestTypeDef,
    CreateTrailResponseTypeDef,
    DeleteChannelRequestTypeDef,
    DeleteDashboardRequestTypeDef,
    DeleteEventDataStoreRequestTypeDef,
    DeleteResourcePolicyRequestTypeDef,
    DeleteTrailRequestTypeDef,
    DeregisterOrganizationDelegatedAdminRequestTypeDef,
    DescribeQueryRequestTypeDef,
    DescribeQueryResponseTypeDef,
    DescribeTrailsRequestTypeDef,
    DescribeTrailsResponseTypeDef,
    DisableFederationRequestTypeDef,
    DisableFederationResponseTypeDef,
    EnableFederationRequestTypeDef,
    EnableFederationResponseTypeDef,
    GenerateQueryRequestTypeDef,
    GenerateQueryResponseTypeDef,
    GetChannelRequestTypeDef,
    GetChannelResponseTypeDef,
    GetDashboardRequestTypeDef,
    GetDashboardResponseTypeDef,
    GetEventConfigurationRequestTypeDef,
    GetEventConfigurationResponseTypeDef,
    GetEventDataStoreRequestTypeDef,
    GetEventDataStoreResponseTypeDef,
    GetEventSelectorsRequestTypeDef,
    GetEventSelectorsResponseTypeDef,
    GetImportRequestTypeDef,
    GetImportResponseTypeDef,
    GetInsightSelectorsRequestTypeDef,
    GetInsightSelectorsResponseTypeDef,
    GetQueryResultsRequestTypeDef,
    GetQueryResultsResponseTypeDef,
    GetResourcePolicyRequestTypeDef,
    GetResourcePolicyResponseTypeDef,
    GetTrailRequestTypeDef,
    GetTrailResponseTypeDef,
    GetTrailStatusRequestTypeDef,
    GetTrailStatusResponseTypeDef,
    ListChannelsRequestTypeDef,
    ListChannelsResponseTypeDef,
    ListDashboardsRequestTypeDef,
    ListDashboardsResponseTypeDef,
    ListEventDataStoresRequestTypeDef,
    ListEventDataStoresResponseTypeDef,
    ListImportFailuresRequestTypeDef,
    ListImportFailuresResponseTypeDef,
    ListImportsRequestTypeDef,
    ListImportsResponseTypeDef,
    ListInsightsDataRequestTypeDef,
    ListInsightsDataResponseTypeDef,
    ListInsightsMetricDataRequestTypeDef,
    ListInsightsMetricDataResponseTypeDef,
    ListPublicKeysRequestTypeDef,
    ListPublicKeysResponseTypeDef,
    ListQueriesRequestTypeDef,
    ListQueriesResponseTypeDef,
    ListTagsRequestTypeDef,
    ListTagsResponseTypeDef,
    ListTrailsRequestTypeDef,
    ListTrailsResponseTypeDef,
    LookupEventsRequestTypeDef,
    LookupEventsResponseTypeDef,
    PutEventConfigurationRequestTypeDef,
    PutEventConfigurationResponseTypeDef,
    PutEventSelectorsRequestTypeDef,
    PutEventSelectorsResponseTypeDef,
    PutInsightSelectorsRequestTypeDef,
    PutInsightSelectorsResponseTypeDef,
    PutResourcePolicyRequestTypeDef,
    PutResourcePolicyResponseTypeDef,
    RegisterOrganizationDelegatedAdminRequestTypeDef,
    RemoveTagsRequestTypeDef,
    RestoreEventDataStoreRequestTypeDef,
    RestoreEventDataStoreResponseTypeDef,
    SearchSampleQueriesRequestTypeDef,
    SearchSampleQueriesResponseTypeDef,
    StartDashboardRefreshRequestTypeDef,
    StartDashboardRefreshResponseTypeDef,
    StartEventDataStoreIngestionRequestTypeDef,
    StartImportRequestTypeDef,
    StartImportResponseTypeDef,
    StartLoggingRequestTypeDef,
    StartQueryRequestTypeDef,
    StartQueryResponseTypeDef,
    StopEventDataStoreIngestionRequestTypeDef,
    StopImportRequestTypeDef,
    StopImportResponseTypeDef,
    StopLoggingRequestTypeDef,
    UpdateChannelRequestTypeDef,
    UpdateChannelResponseTypeDef,
    UpdateDashboardRequestTypeDef,
    UpdateDashboardResponseTypeDef,
    UpdateEventDataStoreRequestTypeDef,
    UpdateEventDataStoreResponseTypeDef,
    UpdateTrailRequestTypeDef,
    UpdateTrailResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("CloudTrailClient",)


class Exceptions(BaseClientExceptions):
    AccessDeniedException: type[BotocoreClientError]
    AccountHasOngoingImportException: type[BotocoreClientError]
    AccountNotFoundException: type[BotocoreClientError]
    AccountNotRegisteredException: type[BotocoreClientError]
    AccountRegisteredException: type[BotocoreClientError]
    CannotDelegateManagementAccountException: type[BotocoreClientError]
    ChannelARNInvalidException: type[BotocoreClientError]
    ChannelAlreadyExistsException: type[BotocoreClientError]
    ChannelExistsForEDSException: type[BotocoreClientError]
    ChannelMaxLimitExceededException: type[BotocoreClientError]
    ChannelNotFoundException: type[BotocoreClientError]
    ClientError: type[BotocoreClientError]
    CloudTrailARNInvalidException: type[BotocoreClientError]
    CloudTrailAccessNotEnabledException: type[BotocoreClientError]
    CloudTrailInvalidClientTokenIdException: type[BotocoreClientError]
    CloudWatchLogsDeliveryUnavailableException: type[BotocoreClientError]
    ConcurrentModificationException: type[BotocoreClientError]
    ConflictException: type[BotocoreClientError]
    DelegatedAdminAccountLimitExceededException: type[BotocoreClientError]
    EventDataStoreARNInvalidException: type[BotocoreClientError]
    EventDataStoreAlreadyExistsException: type[BotocoreClientError]
    EventDataStoreFederationEnabledException: type[BotocoreClientError]
    EventDataStoreHasOngoingImportException: type[BotocoreClientError]
    EventDataStoreMaxLimitExceededException: type[BotocoreClientError]
    EventDataStoreNotFoundException: type[BotocoreClientError]
    EventDataStoreTerminationProtectedException: type[BotocoreClientError]
    GenerateResponseException: type[BotocoreClientError]
    ImportNotFoundException: type[BotocoreClientError]
    InactiveEventDataStoreException: type[BotocoreClientError]
    InactiveQueryException: type[BotocoreClientError]
    InsightNotEnabledException: type[BotocoreClientError]
    InsufficientDependencyServiceAccessPermissionException: type[BotocoreClientError]
    InsufficientEncryptionPolicyException: type[BotocoreClientError]
    InsufficientIAMAccessPermissionException: type[BotocoreClientError]
    InsufficientS3BucketPolicyException: type[BotocoreClientError]
    InsufficientSnsTopicPolicyException: type[BotocoreClientError]
    InvalidCloudWatchLogsLogGroupArnException: type[BotocoreClientError]
    InvalidCloudWatchLogsRoleArnException: type[BotocoreClientError]
    InvalidDateRangeException: type[BotocoreClientError]
    InvalidEventCategoryException: type[BotocoreClientError]
    InvalidEventDataStoreCategoryException: type[BotocoreClientError]
    InvalidEventDataStoreStatusException: type[BotocoreClientError]
    InvalidEventSelectorsException: type[BotocoreClientError]
    InvalidHomeRegionException: type[BotocoreClientError]
    InvalidImportSourceException: type[BotocoreClientError]
    InvalidInsightSelectorsException: type[BotocoreClientError]
    InvalidKmsKeyIdException: type[BotocoreClientError]
    InvalidLookupAttributesException: type[BotocoreClientError]
    InvalidMaxResultsException: type[BotocoreClientError]
    InvalidNextTokenException: type[BotocoreClientError]
    InvalidParameterCombinationException: type[BotocoreClientError]
    InvalidParameterException: type[BotocoreClientError]
    InvalidQueryStatementException: type[BotocoreClientError]
    InvalidQueryStatusException: type[BotocoreClientError]
    InvalidS3BucketNameException: type[BotocoreClientError]
    InvalidS3PrefixException: type[BotocoreClientError]
    InvalidSnsTopicNameException: type[BotocoreClientError]
    InvalidSourceException: type[BotocoreClientError]
    InvalidTagParameterException: type[BotocoreClientError]
    InvalidTimeRangeException: type[BotocoreClientError]
    InvalidTokenException: type[BotocoreClientError]
    InvalidTrailNameException: type[BotocoreClientError]
    KmsException: type[BotocoreClientError]
    KmsKeyDisabledException: type[BotocoreClientError]
    KmsKeyNotFoundException: type[BotocoreClientError]
    MaxConcurrentQueriesException: type[BotocoreClientError]
    MaximumNumberOfTrailsExceededException: type[BotocoreClientError]
    NoManagementAccountSLRExistsException: type[BotocoreClientError]
    NotOrganizationManagementAccountException: type[BotocoreClientError]
    NotOrganizationMasterAccountException: type[BotocoreClientError]
    OperationNotPermittedException: type[BotocoreClientError]
    OrganizationNotInAllFeaturesModeException: type[BotocoreClientError]
    OrganizationsNotInUseException: type[BotocoreClientError]
    QueryIdNotFoundException: type[BotocoreClientError]
    ResourceARNNotValidException: type[BotocoreClientError]
    ResourceNotFoundException: type[BotocoreClientError]
    ResourcePolicyNotFoundException: type[BotocoreClientError]
    ResourcePolicyNotValidException: type[BotocoreClientError]
    ResourceTypeNotSupportedException: type[BotocoreClientError]
    S3BucketDoesNotExistException: type[BotocoreClientError]
    ServiceQuotaExceededException: type[BotocoreClientError]
    TagsLimitExceededException: type[BotocoreClientError]
    ThrottlingException: type[BotocoreClientError]
    TrailAlreadyExistsException: type[BotocoreClientError]
    TrailNotFoundException: type[BotocoreClientError]
    TrailNotProvidedException: type[BotocoreClientError]
    UnsupportedOperationException: type[BotocoreClientError]


class CloudTrailClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail.html#CloudTrail.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        CloudTrailClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail.html#CloudTrail.Client)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/can_paginate.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/generate_presigned_url.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#generate_presigned_url)
        """

    def add_tags(self, **kwargs: Unpack[AddTagsRequestTypeDef]) -> dict[str, Any]:
        """
        Adds one or more tags to a trail, event data store, dashboard, or channel, up
        to a limit of 50.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/add_tags.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#add_tags)
        """

    def cancel_query(
        self, **kwargs: Unpack[CancelQueryRequestTypeDef]
    ) -> CancelQueryResponseTypeDef:
        """
        CloudTrail Lake will no longer be open to new customers starting May 31, 2026.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/cancel_query.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#cancel_query)
        """

    def create_channel(
        self, **kwargs: Unpack[CreateChannelRequestTypeDef]
    ) -> CreateChannelResponseTypeDef:
        """
        CloudTrail Lake will no longer be open to new customers starting May 31, 2026.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/create_channel.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#create_channel)
        """

    def create_dashboard(
        self, **kwargs: Unpack[CreateDashboardRequestTypeDef]
    ) -> CreateDashboardResponseTypeDef:
        """
        CloudTrail Lake will no longer be open to new customers starting May 31, 2026.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/create_dashboard.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#create_dashboard)
        """

    def create_event_data_store(
        self, **kwargs: Unpack[CreateEventDataStoreRequestTypeDef]
    ) -> CreateEventDataStoreResponseTypeDef:
        """
        CloudTrail Lake will no longer be open to new customers starting May 31, 2026.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/create_event_data_store.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#create_event_data_store)
        """

    def create_trail(
        self, **kwargs: Unpack[CreateTrailRequestTypeDef]
    ) -> CreateTrailResponseTypeDef:
        """
        Creates a trail that specifies the settings for delivery of log data to an
        Amazon S3 bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/create_trail.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#create_trail)
        """

    def delete_channel(self, **kwargs: Unpack[DeleteChannelRequestTypeDef]) -> dict[str, Any]:
        """
        CloudTrail Lake will no longer be open to new customers starting May 31, 2026.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/delete_channel.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#delete_channel)
        """

    def delete_dashboard(self, **kwargs: Unpack[DeleteDashboardRequestTypeDef]) -> dict[str, Any]:
        """
        CloudTrail Lake will no longer be open to new customers starting May 31, 2026.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/delete_dashboard.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#delete_dashboard)
        """

    def delete_event_data_store(
        self, **kwargs: Unpack[DeleteEventDataStoreRequestTypeDef]
    ) -> dict[str, Any]:
        """
        CloudTrail Lake will no longer be open to new customers starting May 31, 2026.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/delete_event_data_store.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#delete_event_data_store)
        """

    def delete_resource_policy(
        self, **kwargs: Unpack[DeleteResourcePolicyRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Deletes the resource-based policy attached to the CloudTrail event data store,
        dashboard, or channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/delete_resource_policy.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#delete_resource_policy)
        """

    def delete_trail(self, **kwargs: Unpack[DeleteTrailRequestTypeDef]) -> dict[str, Any]:
        """
        Deletes a trail.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/delete_trail.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#delete_trail)
        """

    def deregister_organization_delegated_admin(
        self, **kwargs: Unpack[DeregisterOrganizationDelegatedAdminRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Removes CloudTrail delegated administrator permissions from a member account in
        an organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/deregister_organization_delegated_admin.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#deregister_organization_delegated_admin)
        """

    def describe_query(
        self, **kwargs: Unpack[DescribeQueryRequestTypeDef]
    ) -> DescribeQueryResponseTypeDef:
        """
        CloudTrail Lake will no longer be open to new customers starting May 31, 2026.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/describe_query.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#describe_query)
        """

    def describe_trails(
        self, **kwargs: Unpack[DescribeTrailsRequestTypeDef]
    ) -> DescribeTrailsResponseTypeDef:
        """
        Retrieves settings for one or more trails associated with the current Region
        for your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/describe_trails.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#describe_trails)
        """

    def disable_federation(
        self, **kwargs: Unpack[DisableFederationRequestTypeDef]
    ) -> DisableFederationResponseTypeDef:
        """
        CloudTrail Lake will no longer be open to new customers starting May 31, 2026.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/disable_federation.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#disable_federation)
        """

    def enable_federation(
        self, **kwargs: Unpack[EnableFederationRequestTypeDef]
    ) -> EnableFederationResponseTypeDef:
        """
        CloudTrail Lake will no longer be open to new customers starting May 31, 2026.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/enable_federation.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#enable_federation)
        """

    def generate_query(
        self, **kwargs: Unpack[GenerateQueryRequestTypeDef]
    ) -> GenerateQueryResponseTypeDef:
        """
        CloudTrail Lake will no longer be open to new customers starting May 31, 2026.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/generate_query.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#generate_query)
        """

    def get_channel(self, **kwargs: Unpack[GetChannelRequestTypeDef]) -> GetChannelResponseTypeDef:
        """
        CloudTrail Lake will no longer be open to new customers starting May 31, 2026.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/get_channel.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#get_channel)
        """

    def get_dashboard(
        self, **kwargs: Unpack[GetDashboardRequestTypeDef]
    ) -> GetDashboardResponseTypeDef:
        """
        CloudTrail Lake will no longer be open to new customers starting May 31, 2026.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/get_dashboard.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#get_dashboard)
        """

    def get_event_configuration(
        self, **kwargs: Unpack[GetEventConfigurationRequestTypeDef]
    ) -> GetEventConfigurationResponseTypeDef:
        """
        Retrieves the current event configuration settings for the specified event data
        store or trail.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/get_event_configuration.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#get_event_configuration)
        """

    def get_event_data_store(
        self, **kwargs: Unpack[GetEventDataStoreRequestTypeDef]
    ) -> GetEventDataStoreResponseTypeDef:
        """
        CloudTrail Lake will no longer be open to new customers starting May 31, 2026.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/get_event_data_store.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#get_event_data_store)
        """

    def get_event_selectors(
        self, **kwargs: Unpack[GetEventSelectorsRequestTypeDef]
    ) -> GetEventSelectorsResponseTypeDef:
        """
        Describes the settings for the event selectors that you configured for your
        trail.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/get_event_selectors.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#get_event_selectors)
        """

    def get_import(self, **kwargs: Unpack[GetImportRequestTypeDef]) -> GetImportResponseTypeDef:
        """
        CloudTrail Lake will no longer be open to new customers starting May 31, 2026.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/get_import.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#get_import)
        """

    def get_insight_selectors(
        self, **kwargs: Unpack[GetInsightSelectorsRequestTypeDef]
    ) -> GetInsightSelectorsResponseTypeDef:
        """
        Describes the settings for the Insights event selectors that you configured for
        your trail or event data store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/get_insight_selectors.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#get_insight_selectors)
        """

    def get_query_results(
        self, **kwargs: Unpack[GetQueryResultsRequestTypeDef]
    ) -> GetQueryResultsResponseTypeDef:
        """
        CloudTrail Lake will no longer be open to new customers starting May 31, 2026.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/get_query_results.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#get_query_results)
        """

    def get_resource_policy(
        self, **kwargs: Unpack[GetResourcePolicyRequestTypeDef]
    ) -> GetResourcePolicyResponseTypeDef:
        """
        Retrieves the JSON text of the resource-based policy document attached to the
        CloudTrail event data store, dashboard, or channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/get_resource_policy.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#get_resource_policy)
        """

    def get_trail(self, **kwargs: Unpack[GetTrailRequestTypeDef]) -> GetTrailResponseTypeDef:
        """
        Returns settings information for a specified trail.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/get_trail.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#get_trail)
        """

    def get_trail_status(
        self, **kwargs: Unpack[GetTrailStatusRequestTypeDef]
    ) -> GetTrailStatusResponseTypeDef:
        """
        Returns a JSON-formatted list of information about the specified trail.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/get_trail_status.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#get_trail_status)
        """

    def list_channels(
        self, **kwargs: Unpack[ListChannelsRequestTypeDef]
    ) -> ListChannelsResponseTypeDef:
        """
        CloudTrail Lake will no longer be open to new customers starting May 31, 2026.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/list_channels.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#list_channels)
        """

    def list_dashboards(
        self, **kwargs: Unpack[ListDashboardsRequestTypeDef]
    ) -> ListDashboardsResponseTypeDef:
        """
        CloudTrail Lake will no longer be open to new customers starting May 31, 2026.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/list_dashboards.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#list_dashboards)
        """

    def list_event_data_stores(
        self, **kwargs: Unpack[ListEventDataStoresRequestTypeDef]
    ) -> ListEventDataStoresResponseTypeDef:
        """
        CloudTrail Lake will no longer be open to new customers starting May 31, 2026.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/list_event_data_stores.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#list_event_data_stores)
        """

    def list_import_failures(
        self, **kwargs: Unpack[ListImportFailuresRequestTypeDef]
    ) -> ListImportFailuresResponseTypeDef:
        """
        CloudTrail Lake will no longer be open to new customers starting May 31, 2026.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/list_import_failures.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#list_import_failures)
        """

    def list_imports(
        self, **kwargs: Unpack[ListImportsRequestTypeDef]
    ) -> ListImportsResponseTypeDef:
        """
        CloudTrail Lake will no longer be open to new customers starting May 31, 2026.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/list_imports.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#list_imports)
        """

    def list_insights_data(
        self, **kwargs: Unpack[ListInsightsDataRequestTypeDef]
    ) -> ListInsightsDataResponseTypeDef:
        """
        Returns Insights events generated on a trail that logs data events.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/list_insights_data.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#list_insights_data)
        """

    def list_insights_metric_data(
        self, **kwargs: Unpack[ListInsightsMetricDataRequestTypeDef]
    ) -> ListInsightsMetricDataResponseTypeDef:
        """
        Returns Insights metrics data for trails that have enabled Insights.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/list_insights_metric_data.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#list_insights_metric_data)
        """

    def list_public_keys(
        self, **kwargs: Unpack[ListPublicKeysRequestTypeDef]
    ) -> ListPublicKeysResponseTypeDef:
        """
        Returns all public keys whose private keys were used to sign the digest files
        within the specified time range.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/list_public_keys.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#list_public_keys)
        """

    def list_queries(
        self, **kwargs: Unpack[ListQueriesRequestTypeDef]
    ) -> ListQueriesResponseTypeDef:
        """
        CloudTrail Lake will no longer be open to new customers starting May 31, 2026.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/list_queries.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#list_queries)
        """

    def list_tags(self, **kwargs: Unpack[ListTagsRequestTypeDef]) -> ListTagsResponseTypeDef:
        """
        Lists the tags for the specified trails, event data stores, dashboards, or
        channels in the current Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/list_tags.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#list_tags)
        """

    def list_trails(self, **kwargs: Unpack[ListTrailsRequestTypeDef]) -> ListTrailsResponseTypeDef:
        """
        Lists trails that are in the current account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/list_trails.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#list_trails)
        """

    def lookup_events(
        self, **kwargs: Unpack[LookupEventsRequestTypeDef]
    ) -> LookupEventsResponseTypeDef:
        """
        Looks up <a
        href="https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-concepts.html#cloudtrail-concepts-management-events">management
        events</a> or <a
        href="https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-concepts.html#cloudtrail-concepts-insights-events">C...

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/lookup_events.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#lookup_events)
        """

    def put_event_configuration(
        self, **kwargs: Unpack[PutEventConfigurationRequestTypeDef]
    ) -> PutEventConfigurationResponseTypeDef:
        """
        Updates the event configuration settings for the specified event data store or
        trail.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/put_event_configuration.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#put_event_configuration)
        """

    def put_event_selectors(
        self, **kwargs: Unpack[PutEventSelectorsRequestTypeDef]
    ) -> PutEventSelectorsResponseTypeDef:
        """
        Configures event selectors (also referred to as <i>basic event selectors</i>)
        or advanced event selectors for your trail.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/put_event_selectors.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#put_event_selectors)
        """

    def put_insight_selectors(
        self, **kwargs: Unpack[PutInsightSelectorsRequestTypeDef]
    ) -> PutInsightSelectorsResponseTypeDef:
        """
        Lets you enable Insights event logging on specific event categories by
        specifying the Insights selectors that you want to enable on an existing trail
        or event data store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/put_insight_selectors.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#put_insight_selectors)
        """

    def put_resource_policy(
        self, **kwargs: Unpack[PutResourcePolicyRequestTypeDef]
    ) -> PutResourcePolicyResponseTypeDef:
        """
        Attaches a resource-based permission policy to a CloudTrail event data store,
        dashboard, or channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/put_resource_policy.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#put_resource_policy)
        """

    def register_organization_delegated_admin(
        self, **kwargs: Unpack[RegisterOrganizationDelegatedAdminRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Registers an organization's member account as the CloudTrail <a
        href="https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-delegated-administrator.html">delegated
        administrator</a>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/register_organization_delegated_admin.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#register_organization_delegated_admin)
        """

    def remove_tags(self, **kwargs: Unpack[RemoveTagsRequestTypeDef]) -> dict[str, Any]:
        """
        Removes the specified tags from a trail, event data store, dashboard, or
        channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/remove_tags.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#remove_tags)
        """

    def restore_event_data_store(
        self, **kwargs: Unpack[RestoreEventDataStoreRequestTypeDef]
    ) -> RestoreEventDataStoreResponseTypeDef:
        """
        CloudTrail Lake will no longer be open to new customers starting May 31, 2026.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/restore_event_data_store.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#restore_event_data_store)
        """

    def search_sample_queries(
        self, **kwargs: Unpack[SearchSampleQueriesRequestTypeDef]
    ) -> SearchSampleQueriesResponseTypeDef:
        """
        CloudTrail Lake will no longer be open to new customers starting May 31, 2026.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/search_sample_queries.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#search_sample_queries)
        """

    def start_dashboard_refresh(
        self, **kwargs: Unpack[StartDashboardRefreshRequestTypeDef]
    ) -> StartDashboardRefreshResponseTypeDef:
        """
        CloudTrail Lake will no longer be open to new customers starting May 31, 2026.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/start_dashboard_refresh.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#start_dashboard_refresh)
        """

    def start_event_data_store_ingestion(
        self, **kwargs: Unpack[StartEventDataStoreIngestionRequestTypeDef]
    ) -> dict[str, Any]:
        """
        CloudTrail Lake will no longer be open to new customers starting May 31, 2026.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/start_event_data_store_ingestion.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#start_event_data_store_ingestion)
        """

    def start_import(
        self, **kwargs: Unpack[StartImportRequestTypeDef]
    ) -> StartImportResponseTypeDef:
        """
        CloudTrail Lake will no longer be open to new customers starting May 31, 2026.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/start_import.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#start_import)
        """

    def start_logging(self, **kwargs: Unpack[StartLoggingRequestTypeDef]) -> dict[str, Any]:
        """
        Starts the recording of Amazon Web Services API calls and log file delivery for
        a trail.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/start_logging.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#start_logging)
        """

    def start_query(self, **kwargs: Unpack[StartQueryRequestTypeDef]) -> StartQueryResponseTypeDef:
        """
        CloudTrail Lake will no longer be open to new customers starting May 31, 2026.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/start_query.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#start_query)
        """

    def stop_event_data_store_ingestion(
        self, **kwargs: Unpack[StopEventDataStoreIngestionRequestTypeDef]
    ) -> dict[str, Any]:
        """
        CloudTrail Lake will no longer be open to new customers starting May 31, 2026.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/stop_event_data_store_ingestion.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#stop_event_data_store_ingestion)
        """

    def stop_import(self, **kwargs: Unpack[StopImportRequestTypeDef]) -> StopImportResponseTypeDef:
        """
        CloudTrail Lake will no longer be open to new customers starting May 31, 2026.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/stop_import.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#stop_import)
        """

    def stop_logging(self, **kwargs: Unpack[StopLoggingRequestTypeDef]) -> dict[str, Any]:
        """
        Suspends the recording of Amazon Web Services API calls and log file delivery
        for the specified trail.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/stop_logging.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#stop_logging)
        """

    def update_channel(
        self, **kwargs: Unpack[UpdateChannelRequestTypeDef]
    ) -> UpdateChannelResponseTypeDef:
        """
        CloudTrail Lake will no longer be open to new customers starting May 31, 2026.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/update_channel.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#update_channel)
        """

    def update_dashboard(
        self, **kwargs: Unpack[UpdateDashboardRequestTypeDef]
    ) -> UpdateDashboardResponseTypeDef:
        """
        CloudTrail Lake will no longer be open to new customers starting May 31, 2026.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/update_dashboard.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#update_dashboard)
        """

    def update_event_data_store(
        self, **kwargs: Unpack[UpdateEventDataStoreRequestTypeDef]
    ) -> UpdateEventDataStoreResponseTypeDef:
        """
        CloudTrail Lake will no longer be open to new customers starting May 31, 2026.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/update_event_data_store.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#update_event_data_store)
        """

    def update_trail(
        self, **kwargs: Unpack[UpdateTrailRequestTypeDef]
    ) -> UpdateTrailResponseTypeDef:
        """
        Updates trail settings that control what events you are logging, and how to
        handle log files.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/update_trail.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#update_trail)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_import_failures"]
    ) -> ListImportFailuresPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_imports"]
    ) -> ListImportsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_insights_data"]
    ) -> ListInsightsDataPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_public_keys"]
    ) -> ListPublicKeysPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_tags"]
    ) -> ListTagsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_trails"]
    ) -> ListTrailsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["lookup_events"]
    ) -> LookupEventsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#get_paginator)
        """
