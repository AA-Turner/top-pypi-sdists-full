"""
Type annotations for cloudwatchomni service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/client/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_cloudwatchomni.client import CloudWatchOmniClient

    session = get_session()
    async with session.create_client("cloudwatchomni") as client:
        client: CloudWatchOmniClient
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping
from types import TracebackType
from typing import Any, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .paginator import (
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
from .type_defs import (
    CreateAccessGrantInputTypeDef,
    CreateAccessGrantOutputTypeDef,
    CreateAccessProfileInputTypeDef,
    CreateAccessProfileOutputTypeDef,
    CreateAlertInputTypeDef,
    CreateAlertOutputTypeDef,
    CreateDomainAccessGrantForOrganizationInputTypeDef,
    CreateDomainAccessGrantForOrganizationOutputTypeDef,
    CreateDomainForOrganizationInputTypeDef,
    CreateDomainForOrganizationOutputTypeDef,
    CreateDomainInputTypeDef,
    CreateDomainOutputTypeDef,
    CreateIntegrationInputTypeDef,
    CreateIntegrationOutputTypeDef,
    CreateOmniDashboardInputTypeDef,
    CreateOmniDashboardOutputTypeDef,
    CreateOneTimeDeepLinkCodeInputTypeDef,
    CreateOneTimeDeepLinkCodeOutputTypeDef,
    CreateSpaceInputTypeDef,
    CreateSpaceOutputTypeDef,
    CreateViewRequestTypeDef,
    CreateViewResponseTypeDef,
    DeleteAccessGrantInputTypeDef,
    DeleteAccessProfileInputTypeDef,
    DeleteAlertInputTypeDef,
    DeleteDomainAccessGrantForOrganizationInputTypeDef,
    DeleteDomainForOrganizationInputTypeDef,
    DeleteDomainInputTypeDef,
    DeleteIntegrationInputTypeDef,
    DeleteOmniDashboardInputTypeDef,
    DeleteSpaceInputTypeDef,
    DeleteViewRequestTypeDef,
    GetAccessGrantInputTypeDef,
    GetAccessGrantOutputTypeDef,
    GetAccessProfileInputTypeDef,
    GetAccessProfileOutputTypeDef,
    GetAlertInputTypeDef,
    GetAlertOutputTypeDef,
    GetContextGraphInputTypeDef,
    GetContextGraphOutputTypeDef,
    GetDomainAccessGrantForOrganizationInputTypeDef,
    GetDomainAccessGrantForOrganizationOutputTypeDef,
    GetDomainForOrganizationInputTypeDef,
    GetDomainForOrganizationOutputTypeDef,
    GetDomainInputTypeDef,
    GetDomainOutputTypeDef,
    GetIntegrationInputTypeDef,
    GetIntegrationOutputTypeDef,
    GetIntelligenceConfigurationOutputTypeDef,
    GetOmniDashboardInputTypeDef,
    GetOmniDashboardOutputTypeDef,
    GetSpaceCredentialsForOrganizationInputTypeDef,
    GetSpaceCredentialsForOrganizationOutputTypeDef,
    GetSpaceInputTypeDef,
    GetSpaceOutputTypeDef,
    GetTelemetryQueryResultsRequestTypeDef,
    GetTelemetryQueryResultsResponseTypeDef,
    GetViewRequestTypeDef,
    GetViewResponseTypeDef,
    ListAccessGrantsInputTypeDef,
    ListAccessGrantsOutputTypeDef,
    ListAccessProfilesInputTypeDef,
    ListAccessProfilesOutputTypeDef,
    ListAlertsInputTypeDef,
    ListAlertsOutputTypeDef,
    ListDomainAccessGrantsForOrganizationInputTypeDef,
    ListDomainAccessGrantsForOrganizationOutputTypeDef,
    ListDomainsInputTypeDef,
    ListDomainsOutputTypeDef,
    ListIntegrationsInputTypeDef,
    ListIntegrationsOutputTypeDef,
    ListOmniDashboardsInputTypeDef,
    ListOmniDashboardsOutputTypeDef,
    ListSpacesForOrganizationInputTypeDef,
    ListSpacesForOrganizationOutputTypeDef,
    ListSpacesInputTypeDef,
    ListSpacesOutputTypeDef,
    ListTelemetryFieldsRequestTypeDef,
    ListTelemetryFieldsResponseTypeDef,
    ListTelemetryQuerySessionsRequestTypeDef,
    ListTelemetryQuerySessionsResponseTypeDef,
    ListViewsRequestTypeDef,
    ListViewsResponseTypeDef,
    PutIntelligenceConfigurationInputTypeDef,
    PutIntelligenceConfigurationOutputTypeDef,
    SearchPrincipalsInputTypeDef,
    SearchPrincipalsOutputTypeDef,
    StartTelemetryQueryRequestTypeDef,
    StartTelemetryQueryResponseTypeDef,
    StartTelemetryQuerySessionRequestTypeDef,
    StartTelemetryQuerySessionResponseTypeDef,
    StopTelemetryQueryRequestTypeDef,
    StopTelemetryQuerySessionRequestTypeDef,
    UpdateAccessProfileInputTypeDef,
    UpdateAccessProfileOutputTypeDef,
    UpdateAlertInputTypeDef,
    UpdateDomainForOrganizationInputTypeDef,
    UpdateDomainForOrganizationOutputTypeDef,
    UpdateDomainInputTypeDef,
    UpdateDomainOutputTypeDef,
    UpdateIntegrationInputTypeDef,
    UpdateIntegrationOutputTypeDef,
    UpdateOmniDashboardInputTypeDef,
    UpdateOmniDashboardOutputTypeDef,
    UpdateSpaceInputTypeDef,
    UpdateSpaceOutputTypeDef,
    UpdateViewRequestTypeDef,
    UpdateViewResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Self, Unpack
else:
    from typing_extensions import Literal, Self, Unpack


__all__ = ("CloudWatchOmniClient",)


class Exceptions(BaseClientExceptions):
    AccessDeniedException: type[BotocoreClientError]
    ClientError: type[BotocoreClientError]
    ConflictException: type[BotocoreClientError]
    InternalServerException: type[BotocoreClientError]
    ResourceNotFoundException: type[BotocoreClientError]
    ServiceQuotaExceededException: type[BotocoreClientError]
    ThrottlingException: type[BotocoreClientError]
    ValidationException: type[BotocoreClientError]


class CloudWatchOmniClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni.html#CloudWatchOmni.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        CloudWatchOmniClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni.html#CloudWatchOmni.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/client/#generate_presigned_url)
        """

    async def create_access_grant(
        self, **kwargs: Unpack[CreateAccessGrantInputTypeDef]
    ) -> CreateAccessGrantOutputTypeDef:
        """
        Creates an AccessGrant that authorizes a principal to perform a set of actions
        on resources in a space.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/client/create_access_grant.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/client/#create_access_grant)
        """

    async def create_access_profile(
        self, **kwargs: Unpack[CreateAccessProfileInputTypeDef]
    ) -> CreateAccessProfileOutputTypeDef:
        """
        Creates an access profile in a space.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/client/create_access_profile.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/client/#create_access_profile)
        """

    async def create_alert(
        self, **kwargs: Unpack[CreateAlertInputTypeDef]
    ) -> CreateAlertOutputTypeDef:
        """
        Creates a new alert within a space.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/client/create_alert.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/client/#create_alert)
        """

    async def create_domain(
        self, **kwargs: Unpack[CreateDomainInputTypeDef]
    ) -> CreateDomainOutputTypeDef:
        """
        Creates a domain with identity provider configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/client/create_domain.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/client/#create_domain)
        """

    async def create_domain_access_grant_for_organization(
        self, **kwargs: Unpack[CreateDomainAccessGrantForOrganizationInputTypeDef]
    ) -> CreateDomainAccessGrantForOrganizationOutputTypeDef:
        """
        Creates an AccessGrant that authorizes a principal to administer an
        organization domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/client/create_domain_access_grant_for_organization.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/client/#create_domain_access_grant_for_organization)
        """

    async def create_domain_for_organization(
        self, **kwargs: Unpack[CreateDomainForOrganizationInputTypeDef]
    ) -> CreateDomainForOrganizationOutputTypeDef:
        """
        Creates an organization-scoped domain for the caller's AWS Organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/client/create_domain_for_organization.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/client/#create_domain_for_organization)
        """

    async def create_integration(
        self, **kwargs: Unpack[CreateIntegrationInputTypeDef]
    ) -> CreateIntegrationOutputTypeDef:
        """
        Creates an integration with a third-party provider.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/client/create_integration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/client/#create_integration)
        """

    async def create_omni_dashboard(
        self, **kwargs: Unpack[CreateOmniDashboardInputTypeDef]
    ) -> CreateOmniDashboardOutputTypeDef:
        """
        Creates a new dashboard within a space.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/client/create_omni_dashboard.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/client/#create_omni_dashboard)
        """

    async def create_one_time_deep_link_code(
        self, **kwargs: Unpack[CreateOneTimeDeepLinkCodeInputTypeDef]
    ) -> CreateOneTimeDeepLinkCodeOutputTypeDef:
        """
        Generates a one-time code for deep-link authentication.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/client/create_one_time_deep_link_code.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/client/#create_one_time_deep_link_code)
        """

    async def create_space(
        self, **kwargs: Unpack[CreateSpaceInputTypeDef]
    ) -> CreateSpaceOutputTypeDef:
        """
        Creates a space in a domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/client/create_space.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/client/#create_space)
        """

    async def create_view(
        self, **kwargs: Unpack[CreateViewRequestTypeDef]
    ) -> CreateViewResponseTypeDef:
        """
        Creates a new SQL view.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/client/create_view.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/client/#create_view)
        """

    async def delete_access_grant(
        self, **kwargs: Unpack[DeleteAccessGrantInputTypeDef]
    ) -> dict[str, Any]:
        """
        Removes an existing AccessGrant, revoking the access it granted.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/client/delete_access_grant.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/client/#delete_access_grant)
        """

    async def delete_access_profile(
        self, **kwargs: Unpack[DeleteAccessProfileInputTypeDef]
    ) -> dict[str, Any]:
        """
        Removes an access profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/client/delete_access_profile.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/client/#delete_access_profile)
        """

    async def delete_alert(self, **kwargs: Unpack[DeleteAlertInputTypeDef]) -> dict[str, Any]:
        """
        Deletes an alert by its identifier.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/client/delete_alert.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/client/#delete_alert)
        """

    async def delete_domain(self, **kwargs: Unpack[DeleteDomainInputTypeDef]) -> dict[str, Any]:
        """
        Removes a domain and all of its resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/client/delete_domain.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/client/#delete_domain)
        """

    async def delete_domain_access_grant_for_organization(
        self, **kwargs: Unpack[DeleteDomainAccessGrantForOrganizationInputTypeDef]
    ) -> dict[str, Any]:
        """
        Removes an existing organization access grant, revoking the access it granted.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/client/delete_domain_access_grant_for_organization.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/client/#delete_domain_access_grant_for_organization)
        """

    async def delete_domain_for_organization(
        self, **kwargs: Unpack[DeleteDomainForOrganizationInputTypeDef]
    ) -> dict[str, Any]:
        """
        Removes an organization domain and all of its resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/client/delete_domain_for_organization.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/client/#delete_domain_for_organization)
        """

    async def delete_integration(
        self, **kwargs: Unpack[DeleteIntegrationInputTypeDef]
    ) -> dict[str, Any]:
        """
        Deletes an integration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/client/delete_integration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/client/#delete_integration)
        """

    async def delete_omni_dashboard(
        self, **kwargs: Unpack[DeleteOmniDashboardInputTypeDef]
    ) -> dict[str, Any]:
        """
        Removes a dashboard from a space.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/client/delete_omni_dashboard.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/client/#delete_omni_dashboard)
        """

    async def delete_space(self, **kwargs: Unpack[DeleteSpaceInputTypeDef]) -> dict[str, Any]:
        """
        Removes a space and all of its resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/client/delete_space.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/client/#delete_space)
        """

    async def delete_view(self, **kwargs: Unpack[DeleteViewRequestTypeDef]) -> dict[str, Any]:
        """
        Deletes the specified view.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/client/delete_view.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/client/#delete_view)
        """

    async def get_access_grant(
        self, **kwargs: Unpack[GetAccessGrantInputTypeDef]
    ) -> GetAccessGrantOutputTypeDef:
        """
        Retrieves the full detail of a single AccessGrant by ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/client/get_access_grant.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/client/#get_access_grant)
        """

    async def get_access_profile(
        self, **kwargs: Unpack[GetAccessProfileInputTypeDef]
    ) -> GetAccessProfileOutputTypeDef:
        """
        Retrieves an access profile by ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/client/get_access_profile.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/client/#get_access_profile)
        """

    async def get_alert(self, **kwargs: Unpack[GetAlertInputTypeDef]) -> GetAlertOutputTypeDef:
        """
        Retrieves a single alert by its identifier.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/client/get_alert.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/client/#get_alert)
        """

    async def get_context_graph(
        self, **kwargs: Unpack[GetContextGraphInputTypeDef]
    ) -> GetContextGraphOutputTypeDef:
        """
        Queries the context graph with filtering, traversal, and pagination support.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/client/get_context_graph.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/client/#get_context_graph)
        """

    async def get_domain(self, **kwargs: Unpack[GetDomainInputTypeDef]) -> GetDomainOutputTypeDef:
        """
        Retrieves the details of a domain by ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/client/get_domain.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/client/#get_domain)
        """

    async def get_domain_access_grant_for_organization(
        self, **kwargs: Unpack[GetDomainAccessGrantForOrganizationInputTypeDef]
    ) -> GetDomainAccessGrantForOrganizationOutputTypeDef:
        """
        Retrieves the full detail of a single organization access grant by ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/client/get_domain_access_grant_for_organization.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/client/#get_domain_access_grant_for_organization)
        """

    async def get_domain_for_organization(
        self, **kwargs: Unpack[GetDomainForOrganizationInputTypeDef]
    ) -> GetDomainForOrganizationOutputTypeDef:
        """
        Retrieves the details of an organization domain by ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/client/get_domain_for_organization.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/client/#get_domain_for_organization)
        """

    async def get_integration(
        self, **kwargs: Unpack[GetIntegrationInputTypeDef]
    ) -> GetIntegrationOutputTypeDef:
        """
        Returns the details of a single integration, identified by its identifier,
        Amazon Resource Name, or name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/client/get_integration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/client/#get_integration)
        """

    async def get_intelligence_configuration(self) -> GetIntelligenceConfigurationOutputTypeDef:
        """
        Retrieves the intelligence configuration for the calling account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/client/get_intelligence_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/client/#get_intelligence_configuration)
        """

    async def get_omni_dashboard(
        self, **kwargs: Unpack[GetOmniDashboardInputTypeDef]
    ) -> GetOmniDashboardOutputTypeDef:
        """
        Retrieves a dashboard by ID within a space.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/client/get_omni_dashboard.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/client/#get_omni_dashboard)
        """

    async def get_space(self, **kwargs: Unpack[GetSpaceInputTypeDef]) -> GetSpaceOutputTypeDef:
        """
        Retrieves the details of a space by ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/client/get_space.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/client/#get_space)
        """

    async def get_space_credentials_for_organization(
        self, **kwargs: Unpack[GetSpaceCredentialsForOrganizationInputTypeDef]
    ) -> GetSpaceCredentialsForOrganizationOutputTypeDef:
        """
        Returns temporary credentials for a space in an organization member account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/client/get_space_credentials_for_organization.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/client/#get_space_credentials_for_organization)
        """

    async def get_telemetry_query_results(
        self, **kwargs: Unpack[GetTelemetryQueryResultsRequestTypeDef]
    ) -> GetTelemetryQueryResultsResponseTypeDef:
        """
        Returns the results for the specified query.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/client/get_telemetry_query_results.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/client/#get_telemetry_query_results)
        """

    async def get_view(self, **kwargs: Unpack[GetViewRequestTypeDef]) -> GetViewResponseTypeDef:
        """
        Returns the definition and metadata of the specified view.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/client/get_view.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/client/#get_view)
        """

    async def list_access_grants(
        self, **kwargs: Unpack[ListAccessGrantsInputTypeDef]
    ) -> ListAccessGrantsOutputTypeDef:
        """
        Returns AccessGrants, with optional filtering by domain, space, principal, or
        permission.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/client/list_access_grants.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/client/#list_access_grants)
        """

    async def list_access_profiles(
        self, **kwargs: Unpack[ListAccessProfilesInputTypeDef]
    ) -> ListAccessProfilesOutputTypeDef:
        """
        Returns the access profiles in a space.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/client/list_access_profiles.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/client/#list_access_profiles)
        """

    async def list_alerts(
        self, **kwargs: Unpack[ListAlertsInputTypeDef]
    ) -> ListAlertsOutputTypeDef:
        """
        Lists alerts within a space, optionally filtered by exact name(s), a single
        name prefix, or exact alertId(s), with pagination.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/client/list_alerts.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/client/#list_alerts)
        """

    async def list_domain_access_grants_for_organization(
        self, **kwargs: Unpack[ListDomainAccessGrantsForOrganizationInputTypeDef]
    ) -> ListDomainAccessGrantsForOrganizationOutputTypeDef:
        """
        Returns organization-level domain access grants, with optional filtering by
        domain, principal, or permission.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/client/list_domain_access_grants_for_organization.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/client/#list_domain_access_grants_for_organization)
        """

    async def list_domains(
        self, **kwargs: Unpack[ListDomainsInputTypeDef]
    ) -> ListDomainsOutputTypeDef:
        """
        Returns the caller's domains: the account-scoped domain and the
        organization-scoped domain, if either exists.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/client/list_domains.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/client/#list_domains)
        """

    async def list_integrations(
        self, **kwargs: Unpack[ListIntegrationsInputTypeDef]
    ) -> ListIntegrationsOutputTypeDef:
        """
        Lists the integrations in the account, optionally filtered by type, status, or
        name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/client/list_integrations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/client/#list_integrations)
        """

    async def list_omni_dashboards(
        self, **kwargs: Unpack[ListOmniDashboardsInputTypeDef]
    ) -> ListOmniDashboardsOutputTypeDef:
        """
        Returns the dashboards in a space, optionally filtered by name prefix.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/client/list_omni_dashboards.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/client/#list_omni_dashboards)
        """

    async def list_spaces(
        self, **kwargs: Unpack[ListSpacesInputTypeDef]
    ) -> ListSpacesOutputTypeDef:
        """
        Returns the spaces in the account, optionally filtered by domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/client/list_spaces.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/client/#list_spaces)
        """

    async def list_spaces_for_organization(
        self, **kwargs: Unpack[ListSpacesForOrganizationInputTypeDef]
    ) -> ListSpacesForOrganizationOutputTypeDef:
        """
        Returns the spaces across all member accounts in the organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/client/list_spaces_for_organization.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/client/#list_spaces_for_organization)
        """

    async def list_telemetry_fields(
        self, **kwargs: Unpack[ListTelemetryFieldsRequestTypeDef]
    ) -> ListTelemetryFieldsResponseTypeDef:
        """
        Lists fields available for telemetry queries.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/client/list_telemetry_fields.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/client/#list_telemetry_fields)
        """

    async def list_telemetry_query_sessions(
        self, **kwargs: Unpack[ListTelemetryQuerySessionsRequestTypeDef]
    ) -> ListTelemetryQuerySessionsResponseTypeDef:
        """
        Lists telemetry query sessions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/client/list_telemetry_query_sessions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/client/#list_telemetry_query_sessions)
        """

    async def list_views(
        self, **kwargs: Unpack[ListViewsRequestTypeDef]
    ) -> ListViewsResponseTypeDef:
        """
        Lists the views in the caller's account and region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/client/list_views.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/client/#list_views)
        """

    async def put_intelligence_configuration(
        self, **kwargs: Unpack[PutIntelligenceConfigurationInputTypeDef]
    ) -> PutIntelligenceConfigurationOutputTypeDef:
        """
        Creates or updates the intelligence configuration for the calling account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/client/put_intelligence_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/client/#put_intelligence_configuration)
        """

    async def search_principals(
        self, **kwargs: Unpack[SearchPrincipalsInputTypeDef]
    ) -> SearchPrincipalsOutputTypeDef:
        """
        Searches Identity Center for users and groups in a domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/client/search_principals.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/client/#search_principals)
        """

    async def start_telemetry_query(
        self, **kwargs: Unpack[StartTelemetryQueryRequestTypeDef]
    ) -> StartTelemetryQueryResponseTypeDef:
        """
        Starts a telemetry query within a session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/client/start_telemetry_query.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/client/#start_telemetry_query)
        """

    async def start_telemetry_query_session(
        self, **kwargs: Unpack[StartTelemetryQuerySessionRequestTypeDef]
    ) -> StartTelemetryQuerySessionResponseTypeDef:
        """
        Starts a new telemetry query session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/client/start_telemetry_query_session.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/client/#start_telemetry_query_session)
        """

    async def stop_telemetry_query(
        self, **kwargs: Unpack[StopTelemetryQueryRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Stops a running telemetry query.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/client/stop_telemetry_query.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/client/#stop_telemetry_query)
        """

    async def stop_telemetry_query_session(
        self, **kwargs: Unpack[StopTelemetryQuerySessionRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Stops a telemetry query session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/client/stop_telemetry_query_session.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/client/#stop_telemetry_query_session)
        """

    async def update_access_profile(
        self, **kwargs: Unpack[UpdateAccessProfileInputTypeDef]
    ) -> UpdateAccessProfileOutputTypeDef:
        """
        Updates the name or description of an access profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/client/update_access_profile.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/client/#update_access_profile)
        """

    async def update_alert(self, **kwargs: Unpack[UpdateAlertInputTypeDef]) -> dict[str, Any]:
        """
        Updates an existing alert.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/client/update_alert.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/client/#update_alert)
        """

    async def update_domain(
        self, **kwargs: Unpack[UpdateDomainInputTypeDef]
    ) -> UpdateDomainOutputTypeDef:
        """
        Updates a domain's name or identity provider configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/client/update_domain.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/client/#update_domain)
        """

    async def update_domain_for_organization(
        self, **kwargs: Unpack[UpdateDomainForOrganizationInputTypeDef]
    ) -> UpdateDomainForOrganizationOutputTypeDef:
        """
        Updates an organization domain's name or identity provider configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/client/update_domain_for_organization.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/client/#update_domain_for_organization)
        """

    async def update_integration(
        self, **kwargs: Unpack[UpdateIntegrationInputTypeDef]
    ) -> UpdateIntegrationOutputTypeDef:
        """
        Updates an existing integration, identified by its id, ARN, or name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/client/update_integration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/client/#update_integration)
        """

    async def update_omni_dashboard(
        self, **kwargs: Unpack[UpdateOmniDashboardInputTypeDef]
    ) -> UpdateOmniDashboardOutputTypeDef:
        """
        Updates an existing dashboard within a space.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/client/update_omni_dashboard.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/client/#update_omni_dashboard)
        """

    async def update_space(
        self, **kwargs: Unpack[UpdateSpaceInputTypeDef]
    ) -> UpdateSpaceOutputTypeDef:
        """
        Updates a space.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/client/update_space.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/client/#update_space)
        """

    async def update_view(
        self, **kwargs: Unpack[UpdateViewRequestTypeDef]
    ) -> UpdateViewResponseTypeDef:
        """
        Updates an existing view's definition and/or description.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/client/update_view.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/client/#update_view)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["get_context_graph"]
    ) -> GetContextGraphPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["get_telemetry_query_results"]
    ) -> GetTelemetryQueryResultsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_access_grants"]
    ) -> ListAccessGrantsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_access_profiles"]
    ) -> ListAccessProfilesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_alerts"]
    ) -> ListAlertsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_domain_access_grants_for_organization"]
    ) -> ListDomainAccessGrantsForOrganizationPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_domains"]
    ) -> ListDomainsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_integrations"]
    ) -> ListIntegrationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_omni_dashboards"]
    ) -> ListOmniDashboardsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_spaces_for_organization"]
    ) -> ListSpacesForOrganizationPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_spaces"]
    ) -> ListSpacesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_telemetry_fields"]
    ) -> ListTelemetryFieldsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_telemetry_query_sessions"]
    ) -> ListTelemetryQuerySessionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_views"]
    ) -> ListViewsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["search_principals"]
    ) -> SearchPrincipalsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/client/#get_paginator)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni.html#CloudWatchOmni.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/client/)
        """

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatchomni.html#CloudWatchOmni.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatchomni/client/)
        """
