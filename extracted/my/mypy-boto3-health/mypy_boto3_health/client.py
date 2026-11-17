"""
Type annotations for health service Client.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_health/client/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_health.client import HealthClient

    session = Session()
    client: HealthClient = session.client("health")
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
    DescribeAffectedAccountsForOrganizationPaginator,
    DescribeAffectedEntitiesForOrganizationPaginator,
    DescribeAffectedEntitiesPaginator,
    DescribeEventAggregatesPaginator,
    DescribeEventsForOrganizationPaginator,
    DescribeEventsPaginator,
    DescribeEventTypesPaginator,
    DescribeServiceLifecyclePaginator,
    DescribeTagsForOrganizationPaginator,
    DescribeTagsPaginator,
)
from .type_defs import (
    ConfigureTagsForOrganizationRequestTypeDef,
    ConfigureTagsForOrganizationResponseTypeDef,
    ConfigureTagsRequestTypeDef,
    ConfigureTagsResponseTypeDef,
    DescribeAffectedAccountsForOrganizationRequestTypeDef,
    DescribeAffectedAccountsForOrganizationResponseTypeDef,
    DescribeAffectedEntitiesForOrganizationRequestTypeDef,
    DescribeAffectedEntitiesForOrganizationResponseTypeDef,
    DescribeAffectedEntitiesRequestTypeDef,
    DescribeAffectedEntitiesResponseTypeDef,
    DescribeEntityAggregatesForOrganizationRequestTypeDef,
    DescribeEntityAggregatesForOrganizationResponseTypeDef,
    DescribeEntityAggregatesRequestTypeDef,
    DescribeEntityAggregatesResponseTypeDef,
    DescribeEventAggregatesRequestTypeDef,
    DescribeEventAggregatesResponseTypeDef,
    DescribeEventDetailsForOrganizationRequestTypeDef,
    DescribeEventDetailsForOrganizationResponseTypeDef,
    DescribeEventDetailsRequestTypeDef,
    DescribeEventDetailsResponseTypeDef,
    DescribeEventsForOrganizationRequestTypeDef,
    DescribeEventsForOrganizationResponseTypeDef,
    DescribeEventsRequestTypeDef,
    DescribeEventsResponseTypeDef,
    DescribeEventTypesRequestTypeDef,
    DescribeEventTypesResponseTypeDef,
    DescribeHealthServiceStatusForOrganizationResponseTypeDef,
    DescribeServiceLifecycleRequestTypeDef,
    DescribeServiceLifecycleResponseTypeDef,
    DescribeTagKeysForOrganizationResponseTypeDef,
    DescribeTagKeysResponseTypeDef,
    DescribeTagsForOrganizationRequestTypeDef,
    DescribeTagsForOrganizationResponseTypeDef,
    DescribeTagsOnboardingStatusForOrganizationResponseTypeDef,
    DescribeTagsOnboardingStatusResponseTypeDef,
    DescribeTagsRequestTypeDef,
    DescribeTagsResponseTypeDef,
    EmptyResponseMetadataTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("HealthClient",)


class Exceptions(BaseClientExceptions):
    ClientError: type[BotocoreClientError]
    ConcurrentModificationException: type[BotocoreClientError]
    InvalidPaginationToken: type[BotocoreClientError]
    UnsupportedLocale: type[BotocoreClientError]


class HealthClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health.html#Health.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_health/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        HealthClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health.html#Health.Client)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_health/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health/client/can_paginate.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_health/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health/client/generate_presigned_url.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_health/client/#generate_presigned_url)
        """

    def configure_tags(
        self, **kwargs: Unpack[ConfigureTagsRequestTypeDef]
    ) -> ConfigureTagsResponseTypeDef:
        """
        Configures which resource tag keys are tracked by Health for your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health/client/configure_tags.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_health/client/#configure_tags)
        """

    def configure_tags_for_organization(
        self, **kwargs: Unpack[ConfigureTagsForOrganizationRequestTypeDef]
    ) -> ConfigureTagsForOrganizationResponseTypeDef:
        """
        Configures which tag keys are tracked by Health for all accounts in your
        organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health/client/configure_tags_for_organization.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_health/client/#configure_tags_for_organization)
        """

    def describe_affected_accounts_for_organization(
        self, **kwargs: Unpack[DescribeAffectedAccountsForOrganizationRequestTypeDef]
    ) -> DescribeAffectedAccountsForOrganizationResponseTypeDef:
        """
        Returns a list of accounts in the organization from Organizations that are
        affected by the provided event.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health/client/describe_affected_accounts_for_organization.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_health/client/#describe_affected_accounts_for_organization)
        """

    def describe_affected_entities(
        self, **kwargs: Unpack[DescribeAffectedEntitiesRequestTypeDef]
    ) -> DescribeAffectedEntitiesResponseTypeDef:
        """
        Returns a list of entities that have been affected by the specified events,
        based on the specified filter criteria.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health/client/describe_affected_entities.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_health/client/#describe_affected_entities)
        """

    def describe_affected_entities_for_organization(
        self, **kwargs: Unpack[DescribeAffectedEntitiesForOrganizationRequestTypeDef]
    ) -> DescribeAffectedEntitiesForOrganizationResponseTypeDef:
        """
        Returns a list of entities that have been affected by one or more events for
        one or more accounts in your organization in Organizations, based on the filter
        criteria.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health/client/describe_affected_entities_for_organization.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_health/client/#describe_affected_entities_for_organization)
        """

    def describe_entity_aggregates(
        self, **kwargs: Unpack[DescribeEntityAggregatesRequestTypeDef]
    ) -> DescribeEntityAggregatesResponseTypeDef:
        """
        Returns the number of entities that are affected by each of the specified
        events.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health/client/describe_entity_aggregates.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_health/client/#describe_entity_aggregates)
        """

    def describe_entity_aggregates_for_organization(
        self, **kwargs: Unpack[DescribeEntityAggregatesForOrganizationRequestTypeDef]
    ) -> DescribeEntityAggregatesForOrganizationResponseTypeDef:
        """
        Returns a list of entity aggregates for your Organizations that are affected by
        each of the specified events.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health/client/describe_entity_aggregates_for_organization.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_health/client/#describe_entity_aggregates_for_organization)
        """

    def describe_event_aggregates(
        self, **kwargs: Unpack[DescribeEventAggregatesRequestTypeDef]
    ) -> DescribeEventAggregatesResponseTypeDef:
        """
        Returns the number of events of each event type (issue, scheduled change, and
        account notification).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health/client/describe_event_aggregates.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_health/client/#describe_event_aggregates)
        """

    def describe_event_details(
        self, **kwargs: Unpack[DescribeEventDetailsRequestTypeDef]
    ) -> DescribeEventDetailsResponseTypeDef:
        """
        Returns detailed information about one or more specified events.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health/client/describe_event_details.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_health/client/#describe_event_details)
        """

    def describe_event_details_for_organization(
        self, **kwargs: Unpack[DescribeEventDetailsForOrganizationRequestTypeDef]
    ) -> DescribeEventDetailsForOrganizationResponseTypeDef:
        """
        Returns detailed information about one or more specified events for one or more
        Amazon Web Services accounts in your organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health/client/describe_event_details_for_organization.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_health/client/#describe_event_details_for_organization)
        """

    def describe_event_types(
        self, **kwargs: Unpack[DescribeEventTypesRequestTypeDef]
    ) -> DescribeEventTypesResponseTypeDef:
        """
        Returns the event types that meet the specified filter criteria.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health/client/describe_event_types.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_health/client/#describe_event_types)
        """

    def describe_events(
        self, **kwargs: Unpack[DescribeEventsRequestTypeDef]
    ) -> DescribeEventsResponseTypeDef:
        """
        Returns information about events that meet the specified filter criteria.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health/client/describe_events.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_health/client/#describe_events)
        """

    def describe_events_for_organization(
        self, **kwargs: Unpack[DescribeEventsForOrganizationRequestTypeDef]
    ) -> DescribeEventsForOrganizationResponseTypeDef:
        """
        Returns information about events across your organization in Organizations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health/client/describe_events_for_organization.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_health/client/#describe_events_for_organization)
        """

    def describe_health_service_status_for_organization(
        self,
    ) -> DescribeHealthServiceStatusForOrganizationResponseTypeDef:
        """
        This operation provides status information on enabling or disabling Health to
        work with your organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health/client/describe_health_service_status_for_organization.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_health/client/#describe_health_service_status_for_organization)
        """

    def describe_service_lifecycle(
        self, **kwargs: Unpack[DescribeServiceLifecycleRequestTypeDef]
    ) -> DescribeServiceLifecycleResponseTypeDef:
        """
        Returns lifecycle information for Amazon Web Services services, including
        end-of-life dates, version recommendations, and lifecycle events.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health/client/describe_service_lifecycle.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_health/client/#describe_service_lifecycle)
        """

    def describe_tag_keys(self) -> DescribeTagKeysResponseTypeDef:
        """
        Returns the list of resource tag keys configured for Health event tracking in
        your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health/client/describe_tag_keys.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_health/client/#describe_tag_keys)
        """

    def describe_tag_keys_for_organization(self) -> DescribeTagKeysForOrganizationResponseTypeDef:
        """
        Returns the list of tag keys configured for Health event tracking across your
        organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health/client/describe_tag_keys_for_organization.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_health/client/#describe_tag_keys_for_organization)
        """

    def describe_tags(
        self, **kwargs: Unpack[DescribeTagsRequestTypeDef]
    ) -> DescribeTagsResponseTypeDef:
        """
        Returns the resource tags associated with Health events for your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health/client/describe_tags.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_health/client/#describe_tags)
        """

    def describe_tags_for_organization(
        self, **kwargs: Unpack[DescribeTagsForOrganizationRequestTypeDef]
    ) -> DescribeTagsForOrganizationResponseTypeDef:
        """
        Returns the tags associated with Health events across all accounts in your
        organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health/client/describe_tags_for_organization.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_health/client/#describe_tags_for_organization)
        """

    def describe_tags_onboarding_status(self) -> DescribeTagsOnboardingStatusResponseTypeDef:
        """
        Returns the current onboarding status of the Health tags feature for your
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health/client/describe_tags_onboarding_status.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_health/client/#describe_tags_onboarding_status)
        """

    def describe_tags_onboarding_status_for_organization(
        self,
    ) -> DescribeTagsOnboardingStatusForOrganizationResponseTypeDef:
        """
        Returns the current onboarding status of the Health tags feature for your
        organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health/client/describe_tags_onboarding_status_for_organization.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_health/client/#describe_tags_onboarding_status_for_organization)
        """

    def disable_health_service_access_for_organization(self) -> EmptyResponseMetadataTypeDef:
        """
        Disables Health from working with Organizations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health/client/disable_health_service_access_for_organization.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_health/client/#disable_health_service_access_for_organization)
        """

    def disable_tags(self) -> EmptyResponseMetadataTypeDef:
        """
        Disables the Health tags feature for your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health/client/disable_tags.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_health/client/#disable_tags)
        """

    def disable_tags_for_organization(self) -> EmptyResponseMetadataTypeDef:
        """
        Disables the Health tags feature for all accounts in your organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health/client/disable_tags_for_organization.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_health/client/#disable_tags_for_organization)
        """

    def enable_health_service_access_for_organization(self) -> EmptyResponseMetadataTypeDef:
        """
        Enables Health to work with Organizations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health/client/enable_health_service_access_for_organization.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_health/client/#enable_health_service_access_for_organization)
        """

    def enable_tags(self) -> EmptyResponseMetadataTypeDef:
        """
        Enables the Health tags feature for your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health/client/enable_tags.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_health/client/#enable_tags)
        """

    def enable_tags_for_organization(self) -> EmptyResponseMetadataTypeDef:
        """
        Enables the Health tags feature for all accounts in your organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health/client/enable_tags_for_organization.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_health/client/#enable_tags_for_organization)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["describe_affected_accounts_for_organization"]
    ) -> DescribeAffectedAccountsForOrganizationPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_health/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["describe_affected_entities_for_organization"]
    ) -> DescribeAffectedEntitiesForOrganizationPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_health/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["describe_affected_entities"]
    ) -> DescribeAffectedEntitiesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_health/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["describe_event_aggregates"]
    ) -> DescribeEventAggregatesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_health/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["describe_event_types"]
    ) -> DescribeEventTypesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_health/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["describe_events_for_organization"]
    ) -> DescribeEventsForOrganizationPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_health/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["describe_events"]
    ) -> DescribeEventsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_health/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["describe_service_lifecycle"]
    ) -> DescribeServiceLifecyclePaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_health/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["describe_tags_for_organization"]
    ) -> DescribeTagsForOrganizationPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_health/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["describe_tags"]
    ) -> DescribeTagsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_health/client/#get_paginator)
        """
