"""
Type annotations for cloudwatchomni service client paginators.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudwatchomni/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from types_boto3_cloudwatchomni.client import CloudWatchOmniClient
    from types_boto3_cloudwatchomni.paginator import (
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

    session = Session()
    client: CloudWatchOmniClient = session.client("cloudwatchomni")

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

from botocore.paginate import PageIterator, Paginator

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
    _GetContextGraphPaginatorBase = Paginator[GetContextGraphOutputTypeDef]
else:
    _GetContextGraphPaginatorBase = Paginator  # type: ignore[assignment]

class GetContextGraphPaginator(_GetContextGraphPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/paginator/GetContextGraph.html#CloudWatchOmni.Paginator.GetContextGraph)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudwatchomni/paginators/#getcontextgraphpaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetContextGraphInputPaginateTypeDef]
    ) -> PageIterator[GetContextGraphOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/paginator/GetContextGraph.html#CloudWatchOmni.Paginator.GetContextGraph.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudwatchomni/paginators/#getcontextgraphpaginator)
        """

if TYPE_CHECKING:
    _GetTelemetryQueryResultsPaginatorBase = Paginator[GetTelemetryQueryResultsResponseTypeDef]
else:
    _GetTelemetryQueryResultsPaginatorBase = Paginator  # type: ignore[assignment]

class GetTelemetryQueryResultsPaginator(_GetTelemetryQueryResultsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/paginator/GetTelemetryQueryResults.html#CloudWatchOmni.Paginator.GetTelemetryQueryResults)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudwatchomni/paginators/#gettelemetryqueryresultspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetTelemetryQueryResultsRequestPaginateTypeDef]
    ) -> PageIterator[GetTelemetryQueryResultsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/paginator/GetTelemetryQueryResults.html#CloudWatchOmni.Paginator.GetTelemetryQueryResults.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudwatchomni/paginators/#gettelemetryqueryresultspaginator)
        """

if TYPE_CHECKING:
    _ListAccessGrantsPaginatorBase = Paginator[ListAccessGrantsOutputTypeDef]
else:
    _ListAccessGrantsPaginatorBase = Paginator  # type: ignore[assignment]

class ListAccessGrantsPaginator(_ListAccessGrantsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/paginator/ListAccessGrants.html#CloudWatchOmni.Paginator.ListAccessGrants)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudwatchomni/paginators/#listaccessgrantspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAccessGrantsInputPaginateTypeDef]
    ) -> PageIterator[ListAccessGrantsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/paginator/ListAccessGrants.html#CloudWatchOmni.Paginator.ListAccessGrants.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudwatchomni/paginators/#listaccessgrantspaginator)
        """

if TYPE_CHECKING:
    _ListAccessProfilesPaginatorBase = Paginator[ListAccessProfilesOutputTypeDef]
else:
    _ListAccessProfilesPaginatorBase = Paginator  # type: ignore[assignment]

class ListAccessProfilesPaginator(_ListAccessProfilesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/paginator/ListAccessProfiles.html#CloudWatchOmni.Paginator.ListAccessProfiles)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudwatchomni/paginators/#listaccessprofilespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAccessProfilesInputPaginateTypeDef]
    ) -> PageIterator[ListAccessProfilesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/paginator/ListAccessProfiles.html#CloudWatchOmni.Paginator.ListAccessProfiles.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudwatchomni/paginators/#listaccessprofilespaginator)
        """

if TYPE_CHECKING:
    _ListAlertsPaginatorBase = Paginator[ListAlertsOutputTypeDef]
else:
    _ListAlertsPaginatorBase = Paginator  # type: ignore[assignment]

class ListAlertsPaginator(_ListAlertsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/paginator/ListAlerts.html#CloudWatchOmni.Paginator.ListAlerts)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudwatchomni/paginators/#listalertspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAlertsInputPaginateTypeDef]
    ) -> PageIterator[ListAlertsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/paginator/ListAlerts.html#CloudWatchOmni.Paginator.ListAlerts.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudwatchomni/paginators/#listalertspaginator)
        """

if TYPE_CHECKING:
    _ListDomainAccessGrantsForOrganizationPaginatorBase = Paginator[
        ListDomainAccessGrantsForOrganizationOutputTypeDef
    ]
else:
    _ListDomainAccessGrantsForOrganizationPaginatorBase = Paginator  # type: ignore[assignment]

class ListDomainAccessGrantsForOrganizationPaginator(
    _ListDomainAccessGrantsForOrganizationPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/paginator/ListDomainAccessGrantsForOrganization.html#CloudWatchOmni.Paginator.ListDomainAccessGrantsForOrganization)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudwatchomni/paginators/#listdomainaccessgrantsfororganizationpaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDomainAccessGrantsForOrganizationInputPaginateTypeDef]
    ) -> PageIterator[ListDomainAccessGrantsForOrganizationOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/paginator/ListDomainAccessGrantsForOrganization.html#CloudWatchOmni.Paginator.ListDomainAccessGrantsForOrganization.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudwatchomni/paginators/#listdomainaccessgrantsfororganizationpaginator)
        """

if TYPE_CHECKING:
    _ListDomainsPaginatorBase = Paginator[ListDomainsOutputTypeDef]
else:
    _ListDomainsPaginatorBase = Paginator  # type: ignore[assignment]

class ListDomainsPaginator(_ListDomainsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/paginator/ListDomains.html#CloudWatchOmni.Paginator.ListDomains)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudwatchomni/paginators/#listdomainspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDomainsInputPaginateTypeDef]
    ) -> PageIterator[ListDomainsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/paginator/ListDomains.html#CloudWatchOmni.Paginator.ListDomains.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudwatchomni/paginators/#listdomainspaginator)
        """

if TYPE_CHECKING:
    _ListIntegrationsPaginatorBase = Paginator[ListIntegrationsOutputTypeDef]
else:
    _ListIntegrationsPaginatorBase = Paginator  # type: ignore[assignment]

class ListIntegrationsPaginator(_ListIntegrationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/paginator/ListIntegrations.html#CloudWatchOmni.Paginator.ListIntegrations)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudwatchomni/paginators/#listintegrationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListIntegrationsInputPaginateTypeDef]
    ) -> PageIterator[ListIntegrationsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/paginator/ListIntegrations.html#CloudWatchOmni.Paginator.ListIntegrations.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudwatchomni/paginators/#listintegrationspaginator)
        """

if TYPE_CHECKING:
    _ListOmniDashboardsPaginatorBase = Paginator[ListOmniDashboardsOutputTypeDef]
else:
    _ListOmniDashboardsPaginatorBase = Paginator  # type: ignore[assignment]

class ListOmniDashboardsPaginator(_ListOmniDashboardsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/paginator/ListOmniDashboards.html#CloudWatchOmni.Paginator.ListOmniDashboards)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudwatchomni/paginators/#listomnidashboardspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListOmniDashboardsInputPaginateTypeDef]
    ) -> PageIterator[ListOmniDashboardsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/paginator/ListOmniDashboards.html#CloudWatchOmni.Paginator.ListOmniDashboards.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudwatchomni/paginators/#listomnidashboardspaginator)
        """

if TYPE_CHECKING:
    _ListSpacesForOrganizationPaginatorBase = Paginator[ListSpacesForOrganizationOutputTypeDef]
else:
    _ListSpacesForOrganizationPaginatorBase = Paginator  # type: ignore[assignment]

class ListSpacesForOrganizationPaginator(_ListSpacesForOrganizationPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/paginator/ListSpacesForOrganization.html#CloudWatchOmni.Paginator.ListSpacesForOrganization)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudwatchomni/paginators/#listspacesfororganizationpaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSpacesForOrganizationInputPaginateTypeDef]
    ) -> PageIterator[ListSpacesForOrganizationOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/paginator/ListSpacesForOrganization.html#CloudWatchOmni.Paginator.ListSpacesForOrganization.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudwatchomni/paginators/#listspacesfororganizationpaginator)
        """

if TYPE_CHECKING:
    _ListSpacesPaginatorBase = Paginator[ListSpacesOutputTypeDef]
else:
    _ListSpacesPaginatorBase = Paginator  # type: ignore[assignment]

class ListSpacesPaginator(_ListSpacesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/paginator/ListSpaces.html#CloudWatchOmni.Paginator.ListSpaces)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudwatchomni/paginators/#listspacespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSpacesInputPaginateTypeDef]
    ) -> PageIterator[ListSpacesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/paginator/ListSpaces.html#CloudWatchOmni.Paginator.ListSpaces.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudwatchomni/paginators/#listspacespaginator)
        """

if TYPE_CHECKING:
    _ListTelemetryFieldsPaginatorBase = Paginator[ListTelemetryFieldsResponsePaginatorTypeDef]
else:
    _ListTelemetryFieldsPaginatorBase = Paginator  # type: ignore[assignment]

class ListTelemetryFieldsPaginator(_ListTelemetryFieldsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/paginator/ListTelemetryFields.html#CloudWatchOmni.Paginator.ListTelemetryFields)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudwatchomni/paginators/#listtelemetryfieldspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTelemetryFieldsRequestPaginateTypeDef]
    ) -> PageIterator[ListTelemetryFieldsResponsePaginatorTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/paginator/ListTelemetryFields.html#CloudWatchOmni.Paginator.ListTelemetryFields.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudwatchomni/paginators/#listtelemetryfieldspaginator)
        """

if TYPE_CHECKING:
    _ListTelemetryQuerySessionsPaginatorBase = Paginator[ListTelemetryQuerySessionsResponseTypeDef]
else:
    _ListTelemetryQuerySessionsPaginatorBase = Paginator  # type: ignore[assignment]

class ListTelemetryQuerySessionsPaginator(_ListTelemetryQuerySessionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/paginator/ListTelemetryQuerySessions.html#CloudWatchOmni.Paginator.ListTelemetryQuerySessions)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudwatchomni/paginators/#listtelemetryquerysessionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTelemetryQuerySessionsRequestPaginateTypeDef]
    ) -> PageIterator[ListTelemetryQuerySessionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/paginator/ListTelemetryQuerySessions.html#CloudWatchOmni.Paginator.ListTelemetryQuerySessions.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudwatchomni/paginators/#listtelemetryquerysessionspaginator)
        """

if TYPE_CHECKING:
    _ListViewsPaginatorBase = Paginator[ListViewsResponseTypeDef]
else:
    _ListViewsPaginatorBase = Paginator  # type: ignore[assignment]

class ListViewsPaginator(_ListViewsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/paginator/ListViews.html#CloudWatchOmni.Paginator.ListViews)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudwatchomni/paginators/#listviewspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListViewsRequestPaginateTypeDef]
    ) -> PageIterator[ListViewsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/paginator/ListViews.html#CloudWatchOmni.Paginator.ListViews.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudwatchomni/paginators/#listviewspaginator)
        """

if TYPE_CHECKING:
    _SearchPrincipalsPaginatorBase = Paginator[SearchPrincipalsOutputTypeDef]
else:
    _SearchPrincipalsPaginatorBase = Paginator  # type: ignore[assignment]

class SearchPrincipalsPaginator(_SearchPrincipalsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/paginator/SearchPrincipals.html#CloudWatchOmni.Paginator.SearchPrincipals)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudwatchomni/paginators/#searchprincipalspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[SearchPrincipalsInputPaginateTypeDef]
    ) -> PageIterator[SearchPrincipalsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/paginator/SearchPrincipals.html#CloudWatchOmni.Paginator.SearchPrincipals.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudwatchomni/paginators/#searchprincipalspaginator)
        """
