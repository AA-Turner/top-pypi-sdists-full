"""
Type annotations for datazone service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_datazone.client import DataZoneClient
    from types_aiobotocore_datazone.paginator import (
        ListAssetFiltersPaginator,
        ListAssetRevisionsPaginator,
        ListConnectionsPaginator,
        ListDataProductRevisionsPaginator,
        ListDataSourceRunActivitiesPaginator,
        ListDataSourceRunsPaginator,
        ListDataSourcesPaginator,
        ListDomainUnitsForParentPaginator,
        ListDomainsPaginator,
        ListEntityOwnersPaginator,
        ListEnvironmentActionsPaginator,
        ListEnvironmentBlueprintConfigurationsPaginator,
        ListEnvironmentBlueprintsPaginator,
        ListEnvironmentProfilesPaginator,
        ListEnvironmentsPaginator,
        ListJobRunsPaginator,
        ListLineageEventsPaginator,
        ListLineageNodeHistoryPaginator,
        ListMetadataGenerationRunsPaginator,
        ListNotificationsPaginator,
        ListPolicyGrantsPaginator,
        ListProjectMembershipsPaginator,
        ListProjectProfilesPaginator,
        ListProjectsPaginator,
        ListRulesPaginator,
        ListSubscriptionGrantsPaginator,
        ListSubscriptionRequestsPaginator,
        ListSubscriptionTargetsPaginator,
        ListSubscriptionsPaginator,
        ListTimeSeriesDataPointsPaginator,
        SearchGroupProfilesPaginator,
        SearchListingsPaginator,
        SearchPaginator,
        SearchTypesPaginator,
        SearchUserProfilesPaginator,
    )

    session = get_session()
    with session.create_client("datazone") as client:
        client: DataZoneClient

        list_asset_filters_paginator: ListAssetFiltersPaginator = client.get_paginator("list_asset_filters")
        list_asset_revisions_paginator: ListAssetRevisionsPaginator = client.get_paginator("list_asset_revisions")
        list_connections_paginator: ListConnectionsPaginator = client.get_paginator("list_connections")
        list_data_product_revisions_paginator: ListDataProductRevisionsPaginator = client.get_paginator("list_data_product_revisions")
        list_data_source_run_activities_paginator: ListDataSourceRunActivitiesPaginator = client.get_paginator("list_data_source_run_activities")
        list_data_source_runs_paginator: ListDataSourceRunsPaginator = client.get_paginator("list_data_source_runs")
        list_data_sources_paginator: ListDataSourcesPaginator = client.get_paginator("list_data_sources")
        list_domain_units_for_parent_paginator: ListDomainUnitsForParentPaginator = client.get_paginator("list_domain_units_for_parent")
        list_domains_paginator: ListDomainsPaginator = client.get_paginator("list_domains")
        list_entity_owners_paginator: ListEntityOwnersPaginator = client.get_paginator("list_entity_owners")
        list_environment_actions_paginator: ListEnvironmentActionsPaginator = client.get_paginator("list_environment_actions")
        list_environment_blueprint_configurations_paginator: ListEnvironmentBlueprintConfigurationsPaginator = client.get_paginator("list_environment_blueprint_configurations")
        list_environment_blueprints_paginator: ListEnvironmentBlueprintsPaginator = client.get_paginator("list_environment_blueprints")
        list_environment_profiles_paginator: ListEnvironmentProfilesPaginator = client.get_paginator("list_environment_profiles")
        list_environments_paginator: ListEnvironmentsPaginator = client.get_paginator("list_environments")
        list_job_runs_paginator: ListJobRunsPaginator = client.get_paginator("list_job_runs")
        list_lineage_events_paginator: ListLineageEventsPaginator = client.get_paginator("list_lineage_events")
        list_lineage_node_history_paginator: ListLineageNodeHistoryPaginator = client.get_paginator("list_lineage_node_history")
        list_metadata_generation_runs_paginator: ListMetadataGenerationRunsPaginator = client.get_paginator("list_metadata_generation_runs")
        list_notifications_paginator: ListNotificationsPaginator = client.get_paginator("list_notifications")
        list_policy_grants_paginator: ListPolicyGrantsPaginator = client.get_paginator("list_policy_grants")
        list_project_memberships_paginator: ListProjectMembershipsPaginator = client.get_paginator("list_project_memberships")
        list_project_profiles_paginator: ListProjectProfilesPaginator = client.get_paginator("list_project_profiles")
        list_projects_paginator: ListProjectsPaginator = client.get_paginator("list_projects")
        list_rules_paginator: ListRulesPaginator = client.get_paginator("list_rules")
        list_subscription_grants_paginator: ListSubscriptionGrantsPaginator = client.get_paginator("list_subscription_grants")
        list_subscription_requests_paginator: ListSubscriptionRequestsPaginator = client.get_paginator("list_subscription_requests")
        list_subscription_targets_paginator: ListSubscriptionTargetsPaginator = client.get_paginator("list_subscription_targets")
        list_subscriptions_paginator: ListSubscriptionsPaginator = client.get_paginator("list_subscriptions")
        list_time_series_data_points_paginator: ListTimeSeriesDataPointsPaginator = client.get_paginator("list_time_series_data_points")
        search_group_profiles_paginator: SearchGroupProfilesPaginator = client.get_paginator("search_group_profiles")
        search_listings_paginator: SearchListingsPaginator = client.get_paginator("search_listings")
        search_paginator: SearchPaginator = client.get_paginator("search")
        search_types_paginator: SearchTypesPaginator = client.get_paginator("search_types")
        search_user_profiles_paginator: SearchUserProfilesPaginator = client.get_paginator("search_user_profiles")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListAssetFiltersInputPaginateTypeDef,
    ListAssetFiltersOutputTypeDef,
    ListAssetRevisionsInputPaginateTypeDef,
    ListAssetRevisionsOutputTypeDef,
    ListConnectionsInputPaginateTypeDef,
    ListConnectionsOutputTypeDef,
    ListDataProductRevisionsInputPaginateTypeDef,
    ListDataProductRevisionsOutputTypeDef,
    ListDataSourceRunActivitiesInputPaginateTypeDef,
    ListDataSourceRunActivitiesOutputTypeDef,
    ListDataSourceRunsInputPaginateTypeDef,
    ListDataSourceRunsOutputTypeDef,
    ListDataSourcesInputPaginateTypeDef,
    ListDataSourcesOutputTypeDef,
    ListDomainsInputPaginateTypeDef,
    ListDomainsOutputTypeDef,
    ListDomainUnitsForParentInputPaginateTypeDef,
    ListDomainUnitsForParentOutputTypeDef,
    ListEntityOwnersInputPaginateTypeDef,
    ListEntityOwnersOutputTypeDef,
    ListEnvironmentActionsInputPaginateTypeDef,
    ListEnvironmentActionsOutputTypeDef,
    ListEnvironmentBlueprintConfigurationsInputPaginateTypeDef,
    ListEnvironmentBlueprintConfigurationsOutputTypeDef,
    ListEnvironmentBlueprintsInputPaginateTypeDef,
    ListEnvironmentBlueprintsOutputTypeDef,
    ListEnvironmentProfilesInputPaginateTypeDef,
    ListEnvironmentProfilesOutputTypeDef,
    ListEnvironmentsInputPaginateTypeDef,
    ListEnvironmentsOutputTypeDef,
    ListJobRunsInputPaginateTypeDef,
    ListJobRunsOutputTypeDef,
    ListLineageEventsInputPaginateTypeDef,
    ListLineageEventsOutputTypeDef,
    ListLineageNodeHistoryInputPaginateTypeDef,
    ListLineageNodeHistoryOutputTypeDef,
    ListMetadataGenerationRunsInputPaginateTypeDef,
    ListMetadataGenerationRunsOutputTypeDef,
    ListNotificationsInputPaginateTypeDef,
    ListNotificationsOutputTypeDef,
    ListPolicyGrantsInputPaginateTypeDef,
    ListPolicyGrantsOutputTypeDef,
    ListProjectMembershipsInputPaginateTypeDef,
    ListProjectMembershipsOutputTypeDef,
    ListProjectProfilesInputPaginateTypeDef,
    ListProjectProfilesOutputTypeDef,
    ListProjectsInputPaginateTypeDef,
    ListProjectsOutputTypeDef,
    ListRulesInputPaginateTypeDef,
    ListRulesOutputTypeDef,
    ListSubscriptionGrantsInputPaginateTypeDef,
    ListSubscriptionGrantsOutputTypeDef,
    ListSubscriptionRequestsInputPaginateTypeDef,
    ListSubscriptionRequestsOutputTypeDef,
    ListSubscriptionsInputPaginateTypeDef,
    ListSubscriptionsOutputTypeDef,
    ListSubscriptionTargetsInputPaginateTypeDef,
    ListSubscriptionTargetsOutputTypeDef,
    ListTimeSeriesDataPointsInputPaginateTypeDef,
    ListTimeSeriesDataPointsOutputTypeDef,
    SearchGroupProfilesInputPaginateTypeDef,
    SearchGroupProfilesOutputTypeDef,
    SearchInputPaginateTypeDef,
    SearchListingsInputPaginateTypeDef,
    SearchListingsOutputTypeDef,
    SearchOutputTypeDef,
    SearchTypesInputPaginateTypeDef,
    SearchTypesOutputTypeDef,
    SearchUserProfilesInputPaginateTypeDef,
    SearchUserProfilesOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListAssetFiltersPaginator",
    "ListAssetRevisionsPaginator",
    "ListConnectionsPaginator",
    "ListDataProductRevisionsPaginator",
    "ListDataSourceRunActivitiesPaginator",
    "ListDataSourceRunsPaginator",
    "ListDataSourcesPaginator",
    "ListDomainUnitsForParentPaginator",
    "ListDomainsPaginator",
    "ListEntityOwnersPaginator",
    "ListEnvironmentActionsPaginator",
    "ListEnvironmentBlueprintConfigurationsPaginator",
    "ListEnvironmentBlueprintsPaginator",
    "ListEnvironmentProfilesPaginator",
    "ListEnvironmentsPaginator",
    "ListJobRunsPaginator",
    "ListLineageEventsPaginator",
    "ListLineageNodeHistoryPaginator",
    "ListMetadataGenerationRunsPaginator",
    "ListNotificationsPaginator",
    "ListPolicyGrantsPaginator",
    "ListProjectMembershipsPaginator",
    "ListProjectProfilesPaginator",
    "ListProjectsPaginator",
    "ListRulesPaginator",
    "ListSubscriptionGrantsPaginator",
    "ListSubscriptionRequestsPaginator",
    "ListSubscriptionTargetsPaginator",
    "ListSubscriptionsPaginator",
    "ListTimeSeriesDataPointsPaginator",
    "SearchGroupProfilesPaginator",
    "SearchListingsPaginator",
    "SearchPaginator",
    "SearchTypesPaginator",
    "SearchUserProfilesPaginator",
)

if TYPE_CHECKING:
    _ListAssetFiltersPaginatorBase = AioPaginator[ListAssetFiltersOutputTypeDef]
else:
    _ListAssetFiltersPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListAssetFiltersPaginator(_ListAssetFiltersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListAssetFilters.html#DataZone.Paginator.ListAssetFilters)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listassetfilterspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAssetFiltersInputPaginateTypeDef]
    ) -> AioPageIterator[ListAssetFiltersOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListAssetFilters.html#DataZone.Paginator.ListAssetFilters.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listassetfilterspaginator)
        """

if TYPE_CHECKING:
    _ListAssetRevisionsPaginatorBase = AioPaginator[ListAssetRevisionsOutputTypeDef]
else:
    _ListAssetRevisionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListAssetRevisionsPaginator(_ListAssetRevisionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListAssetRevisions.html#DataZone.Paginator.ListAssetRevisions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listassetrevisionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAssetRevisionsInputPaginateTypeDef]
    ) -> AioPageIterator[ListAssetRevisionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListAssetRevisions.html#DataZone.Paginator.ListAssetRevisions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listassetrevisionspaginator)
        """

if TYPE_CHECKING:
    _ListConnectionsPaginatorBase = AioPaginator[ListConnectionsOutputTypeDef]
else:
    _ListConnectionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListConnectionsPaginator(_ListConnectionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListConnections.html#DataZone.Paginator.ListConnections)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listconnectionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListConnectionsInputPaginateTypeDef]
    ) -> AioPageIterator[ListConnectionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListConnections.html#DataZone.Paginator.ListConnections.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listconnectionspaginator)
        """

if TYPE_CHECKING:
    _ListDataProductRevisionsPaginatorBase = AioPaginator[ListDataProductRevisionsOutputTypeDef]
else:
    _ListDataProductRevisionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListDataProductRevisionsPaginator(_ListDataProductRevisionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListDataProductRevisions.html#DataZone.Paginator.ListDataProductRevisions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listdataproductrevisionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDataProductRevisionsInputPaginateTypeDef]
    ) -> AioPageIterator[ListDataProductRevisionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListDataProductRevisions.html#DataZone.Paginator.ListDataProductRevisions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listdataproductrevisionspaginator)
        """

if TYPE_CHECKING:
    _ListDataSourceRunActivitiesPaginatorBase = AioPaginator[
        ListDataSourceRunActivitiesOutputTypeDef
    ]
else:
    _ListDataSourceRunActivitiesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListDataSourceRunActivitiesPaginator(_ListDataSourceRunActivitiesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListDataSourceRunActivities.html#DataZone.Paginator.ListDataSourceRunActivities)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listdatasourcerunactivitiespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDataSourceRunActivitiesInputPaginateTypeDef]
    ) -> AioPageIterator[ListDataSourceRunActivitiesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListDataSourceRunActivities.html#DataZone.Paginator.ListDataSourceRunActivities.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listdatasourcerunactivitiespaginator)
        """

if TYPE_CHECKING:
    _ListDataSourceRunsPaginatorBase = AioPaginator[ListDataSourceRunsOutputTypeDef]
else:
    _ListDataSourceRunsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListDataSourceRunsPaginator(_ListDataSourceRunsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListDataSourceRuns.html#DataZone.Paginator.ListDataSourceRuns)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listdatasourcerunspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDataSourceRunsInputPaginateTypeDef]
    ) -> AioPageIterator[ListDataSourceRunsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListDataSourceRuns.html#DataZone.Paginator.ListDataSourceRuns.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listdatasourcerunspaginator)
        """

if TYPE_CHECKING:
    _ListDataSourcesPaginatorBase = AioPaginator[ListDataSourcesOutputTypeDef]
else:
    _ListDataSourcesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListDataSourcesPaginator(_ListDataSourcesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListDataSources.html#DataZone.Paginator.ListDataSources)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listdatasourcespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDataSourcesInputPaginateTypeDef]
    ) -> AioPageIterator[ListDataSourcesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListDataSources.html#DataZone.Paginator.ListDataSources.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listdatasourcespaginator)
        """

if TYPE_CHECKING:
    _ListDomainUnitsForParentPaginatorBase = AioPaginator[ListDomainUnitsForParentOutputTypeDef]
else:
    _ListDomainUnitsForParentPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListDomainUnitsForParentPaginator(_ListDomainUnitsForParentPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListDomainUnitsForParent.html#DataZone.Paginator.ListDomainUnitsForParent)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listdomainunitsforparentpaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDomainUnitsForParentInputPaginateTypeDef]
    ) -> AioPageIterator[ListDomainUnitsForParentOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListDomainUnitsForParent.html#DataZone.Paginator.ListDomainUnitsForParent.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listdomainunitsforparentpaginator)
        """

if TYPE_CHECKING:
    _ListDomainsPaginatorBase = AioPaginator[ListDomainsOutputTypeDef]
else:
    _ListDomainsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListDomainsPaginator(_ListDomainsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListDomains.html#DataZone.Paginator.ListDomains)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listdomainspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDomainsInputPaginateTypeDef]
    ) -> AioPageIterator[ListDomainsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListDomains.html#DataZone.Paginator.ListDomains.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listdomainspaginator)
        """

if TYPE_CHECKING:
    _ListEntityOwnersPaginatorBase = AioPaginator[ListEntityOwnersOutputTypeDef]
else:
    _ListEntityOwnersPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListEntityOwnersPaginator(_ListEntityOwnersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListEntityOwners.html#DataZone.Paginator.ListEntityOwners)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listentityownerspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListEntityOwnersInputPaginateTypeDef]
    ) -> AioPageIterator[ListEntityOwnersOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListEntityOwners.html#DataZone.Paginator.ListEntityOwners.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listentityownerspaginator)
        """

if TYPE_CHECKING:
    _ListEnvironmentActionsPaginatorBase = AioPaginator[ListEnvironmentActionsOutputTypeDef]
else:
    _ListEnvironmentActionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListEnvironmentActionsPaginator(_ListEnvironmentActionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListEnvironmentActions.html#DataZone.Paginator.ListEnvironmentActions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listenvironmentactionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListEnvironmentActionsInputPaginateTypeDef]
    ) -> AioPageIterator[ListEnvironmentActionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListEnvironmentActions.html#DataZone.Paginator.ListEnvironmentActions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listenvironmentactionspaginator)
        """

if TYPE_CHECKING:
    _ListEnvironmentBlueprintConfigurationsPaginatorBase = AioPaginator[
        ListEnvironmentBlueprintConfigurationsOutputTypeDef
    ]
else:
    _ListEnvironmentBlueprintConfigurationsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListEnvironmentBlueprintConfigurationsPaginator(
    _ListEnvironmentBlueprintConfigurationsPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListEnvironmentBlueprintConfigurations.html#DataZone.Paginator.ListEnvironmentBlueprintConfigurations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listenvironmentblueprintconfigurationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListEnvironmentBlueprintConfigurationsInputPaginateTypeDef]
    ) -> AioPageIterator[ListEnvironmentBlueprintConfigurationsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListEnvironmentBlueprintConfigurations.html#DataZone.Paginator.ListEnvironmentBlueprintConfigurations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listenvironmentblueprintconfigurationspaginator)
        """

if TYPE_CHECKING:
    _ListEnvironmentBlueprintsPaginatorBase = AioPaginator[ListEnvironmentBlueprintsOutputTypeDef]
else:
    _ListEnvironmentBlueprintsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListEnvironmentBlueprintsPaginator(_ListEnvironmentBlueprintsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListEnvironmentBlueprints.html#DataZone.Paginator.ListEnvironmentBlueprints)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listenvironmentblueprintspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListEnvironmentBlueprintsInputPaginateTypeDef]
    ) -> AioPageIterator[ListEnvironmentBlueprintsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListEnvironmentBlueprints.html#DataZone.Paginator.ListEnvironmentBlueprints.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listenvironmentblueprintspaginator)
        """

if TYPE_CHECKING:
    _ListEnvironmentProfilesPaginatorBase = AioPaginator[ListEnvironmentProfilesOutputTypeDef]
else:
    _ListEnvironmentProfilesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListEnvironmentProfilesPaginator(_ListEnvironmentProfilesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListEnvironmentProfiles.html#DataZone.Paginator.ListEnvironmentProfiles)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listenvironmentprofilespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListEnvironmentProfilesInputPaginateTypeDef]
    ) -> AioPageIterator[ListEnvironmentProfilesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListEnvironmentProfiles.html#DataZone.Paginator.ListEnvironmentProfiles.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listenvironmentprofilespaginator)
        """

if TYPE_CHECKING:
    _ListEnvironmentsPaginatorBase = AioPaginator[ListEnvironmentsOutputTypeDef]
else:
    _ListEnvironmentsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListEnvironmentsPaginator(_ListEnvironmentsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListEnvironments.html#DataZone.Paginator.ListEnvironments)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listenvironmentspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListEnvironmentsInputPaginateTypeDef]
    ) -> AioPageIterator[ListEnvironmentsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListEnvironments.html#DataZone.Paginator.ListEnvironments.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listenvironmentspaginator)
        """

if TYPE_CHECKING:
    _ListJobRunsPaginatorBase = AioPaginator[ListJobRunsOutputTypeDef]
else:
    _ListJobRunsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListJobRunsPaginator(_ListJobRunsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListJobRuns.html#DataZone.Paginator.ListJobRuns)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listjobrunspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListJobRunsInputPaginateTypeDef]
    ) -> AioPageIterator[ListJobRunsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListJobRuns.html#DataZone.Paginator.ListJobRuns.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listjobrunspaginator)
        """

if TYPE_CHECKING:
    _ListLineageEventsPaginatorBase = AioPaginator[ListLineageEventsOutputTypeDef]
else:
    _ListLineageEventsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListLineageEventsPaginator(_ListLineageEventsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListLineageEvents.html#DataZone.Paginator.ListLineageEvents)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listlineageeventspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListLineageEventsInputPaginateTypeDef]
    ) -> AioPageIterator[ListLineageEventsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListLineageEvents.html#DataZone.Paginator.ListLineageEvents.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listlineageeventspaginator)
        """

if TYPE_CHECKING:
    _ListLineageNodeHistoryPaginatorBase = AioPaginator[ListLineageNodeHistoryOutputTypeDef]
else:
    _ListLineageNodeHistoryPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListLineageNodeHistoryPaginator(_ListLineageNodeHistoryPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListLineageNodeHistory.html#DataZone.Paginator.ListLineageNodeHistory)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listlineagenodehistorypaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListLineageNodeHistoryInputPaginateTypeDef]
    ) -> AioPageIterator[ListLineageNodeHistoryOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListLineageNodeHistory.html#DataZone.Paginator.ListLineageNodeHistory.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listlineagenodehistorypaginator)
        """

if TYPE_CHECKING:
    _ListMetadataGenerationRunsPaginatorBase = AioPaginator[ListMetadataGenerationRunsOutputTypeDef]
else:
    _ListMetadataGenerationRunsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListMetadataGenerationRunsPaginator(_ListMetadataGenerationRunsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListMetadataGenerationRuns.html#DataZone.Paginator.ListMetadataGenerationRuns)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listmetadatagenerationrunspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListMetadataGenerationRunsInputPaginateTypeDef]
    ) -> AioPageIterator[ListMetadataGenerationRunsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListMetadataGenerationRuns.html#DataZone.Paginator.ListMetadataGenerationRuns.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listmetadatagenerationrunspaginator)
        """

if TYPE_CHECKING:
    _ListNotificationsPaginatorBase = AioPaginator[ListNotificationsOutputTypeDef]
else:
    _ListNotificationsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListNotificationsPaginator(_ListNotificationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListNotifications.html#DataZone.Paginator.ListNotifications)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listnotificationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListNotificationsInputPaginateTypeDef]
    ) -> AioPageIterator[ListNotificationsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListNotifications.html#DataZone.Paginator.ListNotifications.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listnotificationspaginator)
        """

if TYPE_CHECKING:
    _ListPolicyGrantsPaginatorBase = AioPaginator[ListPolicyGrantsOutputTypeDef]
else:
    _ListPolicyGrantsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListPolicyGrantsPaginator(_ListPolicyGrantsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListPolicyGrants.html#DataZone.Paginator.ListPolicyGrants)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listpolicygrantspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPolicyGrantsInputPaginateTypeDef]
    ) -> AioPageIterator[ListPolicyGrantsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListPolicyGrants.html#DataZone.Paginator.ListPolicyGrants.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listpolicygrantspaginator)
        """

if TYPE_CHECKING:
    _ListProjectMembershipsPaginatorBase = AioPaginator[ListProjectMembershipsOutputTypeDef]
else:
    _ListProjectMembershipsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListProjectMembershipsPaginator(_ListProjectMembershipsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListProjectMemberships.html#DataZone.Paginator.ListProjectMemberships)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listprojectmembershipspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListProjectMembershipsInputPaginateTypeDef]
    ) -> AioPageIterator[ListProjectMembershipsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListProjectMemberships.html#DataZone.Paginator.ListProjectMemberships.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listprojectmembershipspaginator)
        """

if TYPE_CHECKING:
    _ListProjectProfilesPaginatorBase = AioPaginator[ListProjectProfilesOutputTypeDef]
else:
    _ListProjectProfilesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListProjectProfilesPaginator(_ListProjectProfilesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListProjectProfiles.html#DataZone.Paginator.ListProjectProfiles)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listprojectprofilespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListProjectProfilesInputPaginateTypeDef]
    ) -> AioPageIterator[ListProjectProfilesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListProjectProfiles.html#DataZone.Paginator.ListProjectProfiles.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listprojectprofilespaginator)
        """

if TYPE_CHECKING:
    _ListProjectsPaginatorBase = AioPaginator[ListProjectsOutputTypeDef]
else:
    _ListProjectsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListProjectsPaginator(_ListProjectsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListProjects.html#DataZone.Paginator.ListProjects)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listprojectspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListProjectsInputPaginateTypeDef]
    ) -> AioPageIterator[ListProjectsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListProjects.html#DataZone.Paginator.ListProjects.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listprojectspaginator)
        """

if TYPE_CHECKING:
    _ListRulesPaginatorBase = AioPaginator[ListRulesOutputTypeDef]
else:
    _ListRulesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListRulesPaginator(_ListRulesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListRules.html#DataZone.Paginator.ListRules)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listrulespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRulesInputPaginateTypeDef]
    ) -> AioPageIterator[ListRulesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListRules.html#DataZone.Paginator.ListRules.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listrulespaginator)
        """

if TYPE_CHECKING:
    _ListSubscriptionGrantsPaginatorBase = AioPaginator[ListSubscriptionGrantsOutputTypeDef]
else:
    _ListSubscriptionGrantsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListSubscriptionGrantsPaginator(_ListSubscriptionGrantsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListSubscriptionGrants.html#DataZone.Paginator.ListSubscriptionGrants)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listsubscriptiongrantspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSubscriptionGrantsInputPaginateTypeDef]
    ) -> AioPageIterator[ListSubscriptionGrantsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListSubscriptionGrants.html#DataZone.Paginator.ListSubscriptionGrants.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listsubscriptiongrantspaginator)
        """

if TYPE_CHECKING:
    _ListSubscriptionRequestsPaginatorBase = AioPaginator[ListSubscriptionRequestsOutputTypeDef]
else:
    _ListSubscriptionRequestsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListSubscriptionRequestsPaginator(_ListSubscriptionRequestsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListSubscriptionRequests.html#DataZone.Paginator.ListSubscriptionRequests)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listsubscriptionrequestspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSubscriptionRequestsInputPaginateTypeDef]
    ) -> AioPageIterator[ListSubscriptionRequestsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListSubscriptionRequests.html#DataZone.Paginator.ListSubscriptionRequests.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listsubscriptionrequestspaginator)
        """

if TYPE_CHECKING:
    _ListSubscriptionTargetsPaginatorBase = AioPaginator[ListSubscriptionTargetsOutputTypeDef]
else:
    _ListSubscriptionTargetsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListSubscriptionTargetsPaginator(_ListSubscriptionTargetsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListSubscriptionTargets.html#DataZone.Paginator.ListSubscriptionTargets)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listsubscriptiontargetspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSubscriptionTargetsInputPaginateTypeDef]
    ) -> AioPageIterator[ListSubscriptionTargetsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListSubscriptionTargets.html#DataZone.Paginator.ListSubscriptionTargets.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listsubscriptiontargetspaginator)
        """

if TYPE_CHECKING:
    _ListSubscriptionsPaginatorBase = AioPaginator[ListSubscriptionsOutputTypeDef]
else:
    _ListSubscriptionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListSubscriptionsPaginator(_ListSubscriptionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListSubscriptions.html#DataZone.Paginator.ListSubscriptions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listsubscriptionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSubscriptionsInputPaginateTypeDef]
    ) -> AioPageIterator[ListSubscriptionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListSubscriptions.html#DataZone.Paginator.ListSubscriptions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listsubscriptionspaginator)
        """

if TYPE_CHECKING:
    _ListTimeSeriesDataPointsPaginatorBase = AioPaginator[ListTimeSeriesDataPointsOutputTypeDef]
else:
    _ListTimeSeriesDataPointsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListTimeSeriesDataPointsPaginator(_ListTimeSeriesDataPointsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListTimeSeriesDataPoints.html#DataZone.Paginator.ListTimeSeriesDataPoints)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listtimeseriesdatapointspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTimeSeriesDataPointsInputPaginateTypeDef]
    ) -> AioPageIterator[ListTimeSeriesDataPointsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/ListTimeSeriesDataPoints.html#DataZone.Paginator.ListTimeSeriesDataPoints.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#listtimeseriesdatapointspaginator)
        """

if TYPE_CHECKING:
    _SearchGroupProfilesPaginatorBase = AioPaginator[SearchGroupProfilesOutputTypeDef]
else:
    _SearchGroupProfilesPaginatorBase = AioPaginator  # type: ignore[assignment]

class SearchGroupProfilesPaginator(_SearchGroupProfilesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/SearchGroupProfiles.html#DataZone.Paginator.SearchGroupProfiles)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#searchgroupprofilespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[SearchGroupProfilesInputPaginateTypeDef]
    ) -> AioPageIterator[SearchGroupProfilesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/SearchGroupProfiles.html#DataZone.Paginator.SearchGroupProfiles.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#searchgroupprofilespaginator)
        """

if TYPE_CHECKING:
    _SearchListingsPaginatorBase = AioPaginator[SearchListingsOutputTypeDef]
else:
    _SearchListingsPaginatorBase = AioPaginator  # type: ignore[assignment]

class SearchListingsPaginator(_SearchListingsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/SearchListings.html#DataZone.Paginator.SearchListings)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#searchlistingspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[SearchListingsInputPaginateTypeDef]
    ) -> AioPageIterator[SearchListingsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/SearchListings.html#DataZone.Paginator.SearchListings.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#searchlistingspaginator)
        """

if TYPE_CHECKING:
    _SearchPaginatorBase = AioPaginator[SearchOutputTypeDef]
else:
    _SearchPaginatorBase = AioPaginator  # type: ignore[assignment]

class SearchPaginator(_SearchPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/Search.html#DataZone.Paginator.Search)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#searchpaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[SearchInputPaginateTypeDef]
    ) -> AioPageIterator[SearchOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/Search.html#DataZone.Paginator.Search.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#searchpaginator)
        """

if TYPE_CHECKING:
    _SearchTypesPaginatorBase = AioPaginator[SearchTypesOutputTypeDef]
else:
    _SearchTypesPaginatorBase = AioPaginator  # type: ignore[assignment]

class SearchTypesPaginator(_SearchTypesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/SearchTypes.html#DataZone.Paginator.SearchTypes)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#searchtypespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[SearchTypesInputPaginateTypeDef]
    ) -> AioPageIterator[SearchTypesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/SearchTypes.html#DataZone.Paginator.SearchTypes.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#searchtypespaginator)
        """

if TYPE_CHECKING:
    _SearchUserProfilesPaginatorBase = AioPaginator[SearchUserProfilesOutputTypeDef]
else:
    _SearchUserProfilesPaginatorBase = AioPaginator  # type: ignore[assignment]

class SearchUserProfilesPaginator(_SearchUserProfilesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/SearchUserProfiles.html#DataZone.Paginator.SearchUserProfiles)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#searchuserprofilespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[SearchUserProfilesInputPaginateTypeDef]
    ) -> AioPageIterator[SearchUserProfilesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datazone/paginator/SearchUserProfiles.html#DataZone.Paginator.SearchUserProfiles.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/paginators/#searchuserprofilespaginator)
        """
