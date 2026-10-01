"""
Type annotations for cloudwatchomni service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_cloudwatchomni.client import CloudWatchOmniClient
    from types_aiobotocore_cloudwatchomni.paginator import (
        GetContextGraphPaginator,
        GetTelemetryQueryResultsPaginator,
        ListAccessGrantsPaginator,
        ListAccessProfilesPaginator,
        ListAlertsPaginator,
        ListDomainAccessGrantsForOrganizationPaginator,
        ListDomainsPaginator,
        ListIntegrationsPaginator,
        ListOmniDashboardsPaginator,
        ListSpacesForOrganizationPaginator,
        ListSpacesPaginator,
        ListTelemetryFieldsPaginator,
        ListTelemetryQuerySessionsPaginator,
        ListViewsPaginator,
        SearchPrincipalsPaginator,
    )

    session = get_session()
    with session.create_client("cloudwatchomni") as client:
        client: CloudWatchOmniClient

        get_context_graph_paginator: GetContextGraphPaginator = client.get_paginator("get_context_graph")
        get_telemetry_query_results_paginator: GetTelemetryQueryResultsPaginator = client.get_paginator("get_telemetry_query_results")
        list_access_grants_paginator: ListAccessGrantsPaginator = client.get_paginator("list_access_grants")
        list_access_profiles_paginator: ListAccessProfilesPaginator = client.get_paginator("list_access_profiles")
        list_alerts_paginator: ListAlertsPaginator = client.get_paginator("list_alerts")
        list_domain_access_grants_for_organization_paginator: ListDomainAccessGrantsForOrganizationPaginator = client.get_paginator("list_domain_access_grants_for_organization")
        list_domains_paginator: ListDomainsPaginator = client.get_paginator("list_domains")
        list_integrations_paginator: ListIntegrationsPaginator = client.get_paginator("list_integrations")
        list_omni_dashboards_paginator: ListOmniDashboardsPaginator = client.get_paginator("list_omni_dashboards")
        list_spaces_for_organization_paginator: ListSpacesForOrganizationPaginator = client.get_paginator("list_spaces_for_organization")
        list_spaces_paginator: ListSpacesPaginator = client.get_paginator("list_spaces")
        list_telemetry_fields_paginator: ListTelemetryFieldsPaginator = client.get_paginator("list_telemetry_fields")
        list_telemetry_query_sessions_paginator: ListTelemetryQuerySessionsPaginator = client.get_paginator("list_telemetry_query_sessions")
        list_views_paginator: ListViewsPaginator = client.get_paginator("list_views")
        search_principals_paginator: SearchPrincipalsPaginator = client.get_paginator("search_principals")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    GetContextGraphInputPaginateTypeDef,
    GetContextGraphOutputTypeDef,
    GetTelemetryQueryResultsRequestPaginateTypeDef,
    GetTelemetryQueryResultsResponseTypeDef,
    ListAccessGrantsInputPaginateTypeDef,
    ListAccessGrantsOutputTypeDef,
    ListAccessProfilesInputPaginateTypeDef,
    ListAccessProfilesOutputTypeDef,
    ListAlertsInputPaginateTypeDef,
    ListAlertsOutputTypeDef,
    ListDomainAccessGrantsForOrganizationInputPaginateTypeDef,
    ListDomainAccessGrantsForOrganizationOutputTypeDef,
    ListDomainsInputPaginateTypeDef,
    ListDomainsOutputTypeDef,
    ListIntegrationsInputPaginateTypeDef,
    ListIntegrationsOutputTypeDef,
    ListOmniDashboardsInputPaginateTypeDef,
    ListOmniDashboardsOutputTypeDef,
    ListSpacesForOrganizationInputPaginateTypeDef,
    ListSpacesForOrganizationOutputTypeDef,
    ListSpacesInputPaginateTypeDef,
    ListSpacesOutputTypeDef,
    ListTelemetryFieldsRequestPaginateTypeDef,
    ListTelemetryFieldsResponsePaginatorTypeDef,
    ListTelemetryQuerySessionsRequestPaginateTypeDef,
    ListTelemetryQuerySessionsResponseTypeDef,
    ListViewsRequestPaginateTypeDef,
    ListViewsResponseTypeDef,
    SearchPrincipalsInputPaginateTypeDef,
    SearchPrincipalsOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "GetContextGraphPaginator",
    "GetTelemetryQueryResultsPaginator",
    "ListAccessGrantsPaginator",
    "ListAccessProfilesPaginator",
    "ListAlertsPaginator",
    "ListDomainAccessGrantsForOrganizationPaginator",
    "ListDomainsPaginator",
    "ListIntegrationsPaginator",
    "ListOmniDashboardsPaginator",
    "ListSpacesForOrganizationPaginator",
    "ListSpacesPaginator",
    "ListTelemetryFieldsPaginator",
    "ListTelemetryQuerySessionsPaginator",
    "ListViewsPaginator",
    "SearchPrincipalsPaginator",
)

if TYPE_CHECKING:
    _GetContextGraphPaginatorBase = AioPaginator[GetContextGraphOutputTypeDef]
else:
    _GetContextGraphPaginatorBase = AioPaginator  # type: ignore[assignment]

class GetContextGraphPaginator(_GetContextGraphPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/paginator/GetContextGraph.html#CloudWatchOmni.Paginator.GetContextGraph)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/paginators/#getcontextgraphpaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetContextGraphInputPaginateTypeDef]
    ) -> AioPageIterator[GetContextGraphOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/paginator/GetContextGraph.html#CloudWatchOmni.Paginator.GetContextGraph.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/paginators/#getcontextgraphpaginator)
        """

if TYPE_CHECKING:
    _GetTelemetryQueryResultsPaginatorBase = AioPaginator[GetTelemetryQueryResultsResponseTypeDef]
else:
    _GetTelemetryQueryResultsPaginatorBase = AioPaginator  # type: ignore[assignment]

class GetTelemetryQueryResultsPaginator(_GetTelemetryQueryResultsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/paginator/GetTelemetryQueryResults.html#CloudWatchOmni.Paginator.GetTelemetryQueryResults)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/paginators/#gettelemetryqueryresultspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetTelemetryQueryResultsRequestPaginateTypeDef]
    ) -> AioPageIterator[GetTelemetryQueryResultsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/paginator/GetTelemetryQueryResults.html#CloudWatchOmni.Paginator.GetTelemetryQueryResults.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/paginators/#gettelemetryqueryresultspaginator)
        """

if TYPE_CHECKING:
    _ListAccessGrantsPaginatorBase = AioPaginator[ListAccessGrantsOutputTypeDef]
else:
    _ListAccessGrantsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListAccessGrantsPaginator(_ListAccessGrantsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/paginator/ListAccessGrants.html#CloudWatchOmni.Paginator.ListAccessGrants)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/paginators/#listaccessgrantspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAccessGrantsInputPaginateTypeDef]
    ) -> AioPageIterator[ListAccessGrantsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/paginator/ListAccessGrants.html#CloudWatchOmni.Paginator.ListAccessGrants.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/paginators/#listaccessgrantspaginator)
        """

if TYPE_CHECKING:
    _ListAccessProfilesPaginatorBase = AioPaginator[ListAccessProfilesOutputTypeDef]
else:
    _ListAccessProfilesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListAccessProfilesPaginator(_ListAccessProfilesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/paginator/ListAccessProfiles.html#CloudWatchOmni.Paginator.ListAccessProfiles)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/paginators/#listaccessprofilespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAccessProfilesInputPaginateTypeDef]
    ) -> AioPageIterator[ListAccessProfilesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/paginator/ListAccessProfiles.html#CloudWatchOmni.Paginator.ListAccessProfiles.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/paginators/#listaccessprofilespaginator)
        """

if TYPE_CHECKING:
    _ListAlertsPaginatorBase = AioPaginator[ListAlertsOutputTypeDef]
else:
    _ListAlertsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListAlertsPaginator(_ListAlertsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/paginator/ListAlerts.html#CloudWatchOmni.Paginator.ListAlerts)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/paginators/#listalertspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAlertsInputPaginateTypeDef]
    ) -> AioPageIterator[ListAlertsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/paginator/ListAlerts.html#CloudWatchOmni.Paginator.ListAlerts.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/paginators/#listalertspaginator)
        """

if TYPE_CHECKING:
    _ListDomainAccessGrantsForOrganizationPaginatorBase = AioPaginator[
        ListDomainAccessGrantsForOrganizationOutputTypeDef
    ]
else:
    _ListDomainAccessGrantsForOrganizationPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListDomainAccessGrantsForOrganizationPaginator(
    _ListDomainAccessGrantsForOrganizationPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/paginator/ListDomainAccessGrantsForOrganization.html#CloudWatchOmni.Paginator.ListDomainAccessGrantsForOrganization)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/paginators/#listdomainaccessgrantsfororganizationpaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDomainAccessGrantsForOrganizationInputPaginateTypeDef]
    ) -> AioPageIterator[ListDomainAccessGrantsForOrganizationOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/paginator/ListDomainAccessGrantsForOrganization.html#CloudWatchOmni.Paginator.ListDomainAccessGrantsForOrganization.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/paginators/#listdomainaccessgrantsfororganizationpaginator)
        """

if TYPE_CHECKING:
    _ListDomainsPaginatorBase = AioPaginator[ListDomainsOutputTypeDef]
else:
    _ListDomainsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListDomainsPaginator(_ListDomainsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/paginator/ListDomains.html#CloudWatchOmni.Paginator.ListDomains)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/paginators/#listdomainspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDomainsInputPaginateTypeDef]
    ) -> AioPageIterator[ListDomainsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/paginator/ListDomains.html#CloudWatchOmni.Paginator.ListDomains.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/paginators/#listdomainspaginator)
        """

if TYPE_CHECKING:
    _ListIntegrationsPaginatorBase = AioPaginator[ListIntegrationsOutputTypeDef]
else:
    _ListIntegrationsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListIntegrationsPaginator(_ListIntegrationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/paginator/ListIntegrations.html#CloudWatchOmni.Paginator.ListIntegrations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/paginators/#listintegrationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListIntegrationsInputPaginateTypeDef]
    ) -> AioPageIterator[ListIntegrationsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/paginator/ListIntegrations.html#CloudWatchOmni.Paginator.ListIntegrations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/paginators/#listintegrationspaginator)
        """

if TYPE_CHECKING:
    _ListOmniDashboardsPaginatorBase = AioPaginator[ListOmniDashboardsOutputTypeDef]
else:
    _ListOmniDashboardsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListOmniDashboardsPaginator(_ListOmniDashboardsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/paginator/ListOmniDashboards.html#CloudWatchOmni.Paginator.ListOmniDashboards)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/paginators/#listomnidashboardspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListOmniDashboardsInputPaginateTypeDef]
    ) -> AioPageIterator[ListOmniDashboardsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/paginator/ListOmniDashboards.html#CloudWatchOmni.Paginator.ListOmniDashboards.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/paginators/#listomnidashboardspaginator)
        """

if TYPE_CHECKING:
    _ListSpacesForOrganizationPaginatorBase = AioPaginator[ListSpacesForOrganizationOutputTypeDef]
else:
    _ListSpacesForOrganizationPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListSpacesForOrganizationPaginator(_ListSpacesForOrganizationPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/paginator/ListSpacesForOrganization.html#CloudWatchOmni.Paginator.ListSpacesForOrganization)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/paginators/#listspacesfororganizationpaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSpacesForOrganizationInputPaginateTypeDef]
    ) -> AioPageIterator[ListSpacesForOrganizationOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/paginator/ListSpacesForOrganization.html#CloudWatchOmni.Paginator.ListSpacesForOrganization.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/paginators/#listspacesfororganizationpaginator)
        """

if TYPE_CHECKING:
    _ListSpacesPaginatorBase = AioPaginator[ListSpacesOutputTypeDef]
else:
    _ListSpacesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListSpacesPaginator(_ListSpacesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/paginator/ListSpaces.html#CloudWatchOmni.Paginator.ListSpaces)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/paginators/#listspacespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSpacesInputPaginateTypeDef]
    ) -> AioPageIterator[ListSpacesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/paginator/ListSpaces.html#CloudWatchOmni.Paginator.ListSpaces.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/paginators/#listspacespaginator)
        """

if TYPE_CHECKING:
    _ListTelemetryFieldsPaginatorBase = AioPaginator[ListTelemetryFieldsResponsePaginatorTypeDef]
else:
    _ListTelemetryFieldsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListTelemetryFieldsPaginator(_ListTelemetryFieldsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/paginator/ListTelemetryFields.html#CloudWatchOmni.Paginator.ListTelemetryFields)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/paginators/#listtelemetryfieldspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTelemetryFieldsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListTelemetryFieldsResponsePaginatorTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/paginator/ListTelemetryFields.html#CloudWatchOmni.Paginator.ListTelemetryFields.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/paginators/#listtelemetryfieldspaginator)
        """

if TYPE_CHECKING:
    _ListTelemetryQuerySessionsPaginatorBase = AioPaginator[
        ListTelemetryQuerySessionsResponseTypeDef
    ]
else:
    _ListTelemetryQuerySessionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListTelemetryQuerySessionsPaginator(_ListTelemetryQuerySessionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/paginator/ListTelemetryQuerySessions.html#CloudWatchOmni.Paginator.ListTelemetryQuerySessions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/paginators/#listtelemetryquerysessionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTelemetryQuerySessionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListTelemetryQuerySessionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/paginator/ListTelemetryQuerySessions.html#CloudWatchOmni.Paginator.ListTelemetryQuerySessions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/paginators/#listtelemetryquerysessionspaginator)
        """

if TYPE_CHECKING:
    _ListViewsPaginatorBase = AioPaginator[ListViewsResponseTypeDef]
else:
    _ListViewsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListViewsPaginator(_ListViewsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/paginator/ListViews.html#CloudWatchOmni.Paginator.ListViews)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/paginators/#listviewspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListViewsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListViewsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/paginator/ListViews.html#CloudWatchOmni.Paginator.ListViews.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/paginators/#listviewspaginator)
        """

if TYPE_CHECKING:
    _SearchPrincipalsPaginatorBase = AioPaginator[SearchPrincipalsOutputTypeDef]
else:
    _SearchPrincipalsPaginatorBase = AioPaginator  # type: ignore[assignment]

class SearchPrincipalsPaginator(_SearchPrincipalsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/paginator/SearchPrincipals.html#CloudWatchOmni.Paginator.SearchPrincipals)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/paginators/#searchprincipalspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[SearchPrincipalsInputPaginateTypeDef]
    ) -> AioPageIterator[SearchPrincipalsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/paginator/SearchPrincipals.html#CloudWatchOmni.Paginator.SearchPrincipals.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/paginators/#searchprincipalspaginator)
        """
