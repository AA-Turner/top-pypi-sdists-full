"""
Type annotations for apigateway service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_apigateway.client import APIGatewayClient
    from types_aiobotocore_apigateway.paginator import (
        GetApiKeysPaginator,
        GetAuthorizersPaginator,
        GetBasePathMappingsPaginator,
        GetClientCertificatesPaginator,
        GetDeploymentsPaginator,
        GetDocumentationPartsPaginator,
        GetDocumentationVersionsPaginator,
        GetDomainNamesPaginator,
        GetGatewayResponsesPaginator,
        GetModelsPaginator,
        GetRequestValidatorsPaginator,
        GetResourcesPaginator,
        GetRestApisPaginator,
        GetSdkTypesPaginator,
        GetUsagePaginator,
        GetUsagePlanKeysPaginator,
        GetUsagePlansPaginator,
        GetVpcLinksPaginator,
    )

    session = get_session()
    with session.create_client("apigateway") as client:
        client: APIGatewayClient

        get_api_keys_paginator: GetApiKeysPaginator = client.get_paginator("get_api_keys")
        get_authorizers_paginator: GetAuthorizersPaginator = client.get_paginator("get_authorizers")
        get_base_path_mappings_paginator: GetBasePathMappingsPaginator = client.get_paginator("get_base_path_mappings")
        get_client_certificates_paginator: GetClientCertificatesPaginator = client.get_paginator("get_client_certificates")
        get_deployments_paginator: GetDeploymentsPaginator = client.get_paginator("get_deployments")
        get_documentation_parts_paginator: GetDocumentationPartsPaginator = client.get_paginator("get_documentation_parts")
        get_documentation_versions_paginator: GetDocumentationVersionsPaginator = client.get_paginator("get_documentation_versions")
        get_domain_names_paginator: GetDomainNamesPaginator = client.get_paginator("get_domain_names")
        get_gateway_responses_paginator: GetGatewayResponsesPaginator = client.get_paginator("get_gateway_responses")
        get_models_paginator: GetModelsPaginator = client.get_paginator("get_models")
        get_request_validators_paginator: GetRequestValidatorsPaginator = client.get_paginator("get_request_validators")
        get_resources_paginator: GetResourcesPaginator = client.get_paginator("get_resources")
        get_rest_apis_paginator: GetRestApisPaginator = client.get_paginator("get_rest_apis")
        get_sdk_types_paginator: GetSdkTypesPaginator = client.get_paginator("get_sdk_types")
        get_usage_paginator: GetUsagePaginator = client.get_paginator("get_usage")
        get_usage_plan_keys_paginator: GetUsagePlanKeysPaginator = client.get_paginator("get_usage_plan_keys")
        get_usage_plans_paginator: GetUsagePlansPaginator = client.get_paginator("get_usage_plans")
        get_vpc_links_paginator: GetVpcLinksPaginator = client.get_paginator("get_vpc_links")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ApiKeysTypeDef,
    AuthorizersTypeDef,
    BasePathMappingsTypeDef,
    ClientCertificatesTypeDef,
    DeploymentsTypeDef,
    DocumentationPartsTypeDef,
    DocumentationVersionsTypeDef,
    DomainNamesTypeDef,
    GatewayResponsesTypeDef,
    GetApiKeysRequestPaginateTypeDef,
    GetAuthorizersRequestPaginateTypeDef,
    GetBasePathMappingsRequestPaginateTypeDef,
    GetClientCertificatesRequestPaginateTypeDef,
    GetDeploymentsRequestPaginateTypeDef,
    GetDocumentationPartsRequestPaginateTypeDef,
    GetDocumentationVersionsRequestPaginateTypeDef,
    GetDomainNamesRequestPaginateTypeDef,
    GetGatewayResponsesRequestPaginateTypeDef,
    GetModelsRequestPaginateTypeDef,
    GetRequestValidatorsRequestPaginateTypeDef,
    GetResourcesRequestPaginateTypeDef,
    GetRestApisRequestPaginateTypeDef,
    GetSdkTypesRequestPaginateTypeDef,
    GetUsagePlanKeysRequestPaginateTypeDef,
    GetUsagePlansRequestPaginateTypeDef,
    GetUsageRequestPaginateTypeDef,
    GetVpcLinksRequestPaginateTypeDef,
    ModelsTypeDef,
    RequestValidatorsTypeDef,
    ResourcesTypeDef,
    RestApisTypeDef,
    SdkTypesTypeDef,
    UsagePlanKeysTypeDef,
    UsagePlansTypeDef,
    UsageTypeDef,
    VpcLinksTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "GetApiKeysPaginator",
    "GetAuthorizersPaginator",
    "GetBasePathMappingsPaginator",
    "GetClientCertificatesPaginator",
    "GetDeploymentsPaginator",
    "GetDocumentationPartsPaginator",
    "GetDocumentationVersionsPaginator",
    "GetDomainNamesPaginator",
    "GetGatewayResponsesPaginator",
    "GetModelsPaginator",
    "GetRequestValidatorsPaginator",
    "GetResourcesPaginator",
    "GetRestApisPaginator",
    "GetSdkTypesPaginator",
    "GetUsagePaginator",
    "GetUsagePlanKeysPaginator",
    "GetUsagePlansPaginator",
    "GetVpcLinksPaginator",
)


if TYPE_CHECKING:
    _GetApiKeysPaginatorBase = AioPaginator[ApiKeysTypeDef]
else:
    _GetApiKeysPaginatorBase = AioPaginator  # type: ignore[assignment]


class GetApiKeysPaginator(_GetApiKeysPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetApiKeys.html#APIGateway.Paginator.GetApiKeys)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/paginators/#getapikeyspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetApiKeysRequestPaginateTypeDef]
    ) -> AioPageIterator[ApiKeysTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetApiKeys.html#APIGateway.Paginator.GetApiKeys.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/paginators/#getapikeyspaginator)
        """


if TYPE_CHECKING:
    _GetAuthorizersPaginatorBase = AioPaginator[AuthorizersTypeDef]
else:
    _GetAuthorizersPaginatorBase = AioPaginator  # type: ignore[assignment]


class GetAuthorizersPaginator(_GetAuthorizersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetAuthorizers.html#APIGateway.Paginator.GetAuthorizers)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/paginators/#getauthorizerspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetAuthorizersRequestPaginateTypeDef]
    ) -> AioPageIterator[AuthorizersTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetAuthorizers.html#APIGateway.Paginator.GetAuthorizers.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/paginators/#getauthorizerspaginator)
        """


if TYPE_CHECKING:
    _GetBasePathMappingsPaginatorBase = AioPaginator[BasePathMappingsTypeDef]
else:
    _GetBasePathMappingsPaginatorBase = AioPaginator  # type: ignore[assignment]


class GetBasePathMappingsPaginator(_GetBasePathMappingsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetBasePathMappings.html#APIGateway.Paginator.GetBasePathMappings)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/paginators/#getbasepathmappingspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetBasePathMappingsRequestPaginateTypeDef]
    ) -> AioPageIterator[BasePathMappingsTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetBasePathMappings.html#APIGateway.Paginator.GetBasePathMappings.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/paginators/#getbasepathmappingspaginator)
        """


if TYPE_CHECKING:
    _GetClientCertificatesPaginatorBase = AioPaginator[ClientCertificatesTypeDef]
else:
    _GetClientCertificatesPaginatorBase = AioPaginator  # type: ignore[assignment]


class GetClientCertificatesPaginator(_GetClientCertificatesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetClientCertificates.html#APIGateway.Paginator.GetClientCertificates)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/paginators/#getclientcertificatespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetClientCertificatesRequestPaginateTypeDef]
    ) -> AioPageIterator[ClientCertificatesTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetClientCertificates.html#APIGateway.Paginator.GetClientCertificates.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/paginators/#getclientcertificatespaginator)
        """


if TYPE_CHECKING:
    _GetDeploymentsPaginatorBase = AioPaginator[DeploymentsTypeDef]
else:
    _GetDeploymentsPaginatorBase = AioPaginator  # type: ignore[assignment]


class GetDeploymentsPaginator(_GetDeploymentsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetDeployments.html#APIGateway.Paginator.GetDeployments)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/paginators/#getdeploymentspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetDeploymentsRequestPaginateTypeDef]
    ) -> AioPageIterator[DeploymentsTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetDeployments.html#APIGateway.Paginator.GetDeployments.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/paginators/#getdeploymentspaginator)
        """


if TYPE_CHECKING:
    _GetDocumentationPartsPaginatorBase = AioPaginator[DocumentationPartsTypeDef]
else:
    _GetDocumentationPartsPaginatorBase = AioPaginator  # type: ignore[assignment]


class GetDocumentationPartsPaginator(_GetDocumentationPartsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetDocumentationParts.html#APIGateway.Paginator.GetDocumentationParts)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/paginators/#getdocumentationpartspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetDocumentationPartsRequestPaginateTypeDef]
    ) -> AioPageIterator[DocumentationPartsTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetDocumentationParts.html#APIGateway.Paginator.GetDocumentationParts.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/paginators/#getdocumentationpartspaginator)
        """


if TYPE_CHECKING:
    _GetDocumentationVersionsPaginatorBase = AioPaginator[DocumentationVersionsTypeDef]
else:
    _GetDocumentationVersionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class GetDocumentationVersionsPaginator(_GetDocumentationVersionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetDocumentationVersions.html#APIGateway.Paginator.GetDocumentationVersions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/paginators/#getdocumentationversionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetDocumentationVersionsRequestPaginateTypeDef]
    ) -> AioPageIterator[DocumentationVersionsTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetDocumentationVersions.html#APIGateway.Paginator.GetDocumentationVersions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/paginators/#getdocumentationversionspaginator)
        """


if TYPE_CHECKING:
    _GetDomainNamesPaginatorBase = AioPaginator[DomainNamesTypeDef]
else:
    _GetDomainNamesPaginatorBase = AioPaginator  # type: ignore[assignment]


class GetDomainNamesPaginator(_GetDomainNamesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetDomainNames.html#APIGateway.Paginator.GetDomainNames)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/paginators/#getdomainnamespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetDomainNamesRequestPaginateTypeDef]
    ) -> AioPageIterator[DomainNamesTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetDomainNames.html#APIGateway.Paginator.GetDomainNames.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/paginators/#getdomainnamespaginator)
        """


if TYPE_CHECKING:
    _GetGatewayResponsesPaginatorBase = AioPaginator[GatewayResponsesTypeDef]
else:
    _GetGatewayResponsesPaginatorBase = AioPaginator  # type: ignore[assignment]


class GetGatewayResponsesPaginator(_GetGatewayResponsesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetGatewayResponses.html#APIGateway.Paginator.GetGatewayResponses)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/paginators/#getgatewayresponsespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetGatewayResponsesRequestPaginateTypeDef]
    ) -> AioPageIterator[GatewayResponsesTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetGatewayResponses.html#APIGateway.Paginator.GetGatewayResponses.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/paginators/#getgatewayresponsespaginator)
        """


if TYPE_CHECKING:
    _GetModelsPaginatorBase = AioPaginator[ModelsTypeDef]
else:
    _GetModelsPaginatorBase = AioPaginator  # type: ignore[assignment]


class GetModelsPaginator(_GetModelsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetModels.html#APIGateway.Paginator.GetModels)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/paginators/#getmodelspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetModelsRequestPaginateTypeDef]
    ) -> AioPageIterator[ModelsTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetModels.html#APIGateway.Paginator.GetModels.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/paginators/#getmodelspaginator)
        """


if TYPE_CHECKING:
    _GetRequestValidatorsPaginatorBase = AioPaginator[RequestValidatorsTypeDef]
else:
    _GetRequestValidatorsPaginatorBase = AioPaginator  # type: ignore[assignment]


class GetRequestValidatorsPaginator(_GetRequestValidatorsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetRequestValidators.html#APIGateway.Paginator.GetRequestValidators)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/paginators/#getrequestvalidatorspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetRequestValidatorsRequestPaginateTypeDef]
    ) -> AioPageIterator[RequestValidatorsTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetRequestValidators.html#APIGateway.Paginator.GetRequestValidators.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/paginators/#getrequestvalidatorspaginator)
        """


if TYPE_CHECKING:
    _GetResourcesPaginatorBase = AioPaginator[ResourcesTypeDef]
else:
    _GetResourcesPaginatorBase = AioPaginator  # type: ignore[assignment]


class GetResourcesPaginator(_GetResourcesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetResources.html#APIGateway.Paginator.GetResources)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/paginators/#getresourcespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetResourcesRequestPaginateTypeDef]
    ) -> AioPageIterator[ResourcesTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetResources.html#APIGateway.Paginator.GetResources.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/paginators/#getresourcespaginator)
        """


if TYPE_CHECKING:
    _GetRestApisPaginatorBase = AioPaginator[RestApisTypeDef]
else:
    _GetRestApisPaginatorBase = AioPaginator  # type: ignore[assignment]


class GetRestApisPaginator(_GetRestApisPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetRestApis.html#APIGateway.Paginator.GetRestApis)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/paginators/#getrestapispaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetRestApisRequestPaginateTypeDef]
    ) -> AioPageIterator[RestApisTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetRestApis.html#APIGateway.Paginator.GetRestApis.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/paginators/#getrestapispaginator)
        """


if TYPE_CHECKING:
    _GetSdkTypesPaginatorBase = AioPaginator[SdkTypesTypeDef]
else:
    _GetSdkTypesPaginatorBase = AioPaginator  # type: ignore[assignment]


class GetSdkTypesPaginator(_GetSdkTypesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetSdkTypes.html#APIGateway.Paginator.GetSdkTypes)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/paginators/#getsdktypespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetSdkTypesRequestPaginateTypeDef]
    ) -> AioPageIterator[SdkTypesTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetSdkTypes.html#APIGateway.Paginator.GetSdkTypes.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/paginators/#getsdktypespaginator)
        """


if TYPE_CHECKING:
    _GetUsagePaginatorBase = AioPaginator[UsageTypeDef]
else:
    _GetUsagePaginatorBase = AioPaginator  # type: ignore[assignment]


class GetUsagePaginator(_GetUsagePaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetUsage.html#APIGateway.Paginator.GetUsage)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/paginators/#getusagepaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetUsageRequestPaginateTypeDef]
    ) -> AioPageIterator[UsageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetUsage.html#APIGateway.Paginator.GetUsage.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/paginators/#getusagepaginator)
        """


if TYPE_CHECKING:
    _GetUsagePlanKeysPaginatorBase = AioPaginator[UsagePlanKeysTypeDef]
else:
    _GetUsagePlanKeysPaginatorBase = AioPaginator  # type: ignore[assignment]


class GetUsagePlanKeysPaginator(_GetUsagePlanKeysPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetUsagePlanKeys.html#APIGateway.Paginator.GetUsagePlanKeys)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/paginators/#getusageplankeyspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetUsagePlanKeysRequestPaginateTypeDef]
    ) -> AioPageIterator[UsagePlanKeysTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetUsagePlanKeys.html#APIGateway.Paginator.GetUsagePlanKeys.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/paginators/#getusageplankeyspaginator)
        """


if TYPE_CHECKING:
    _GetUsagePlansPaginatorBase = AioPaginator[UsagePlansTypeDef]
else:
    _GetUsagePlansPaginatorBase = AioPaginator  # type: ignore[assignment]


class GetUsagePlansPaginator(_GetUsagePlansPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetUsagePlans.html#APIGateway.Paginator.GetUsagePlans)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/paginators/#getusageplanspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetUsagePlansRequestPaginateTypeDef]
    ) -> AioPageIterator[UsagePlansTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetUsagePlans.html#APIGateway.Paginator.GetUsagePlans.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/paginators/#getusageplanspaginator)
        """


if TYPE_CHECKING:
    _GetVpcLinksPaginatorBase = AioPaginator[VpcLinksTypeDef]
else:
    _GetVpcLinksPaginatorBase = AioPaginator  # type: ignore[assignment]


class GetVpcLinksPaginator(_GetVpcLinksPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetVpcLinks.html#APIGateway.Paginator.GetVpcLinks)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/paginators/#getvpclinkspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetVpcLinksRequestPaginateTypeDef]
    ) -> AioPageIterator[VpcLinksTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetVpcLinks.html#APIGateway.Paginator.GetVpcLinks.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/paginators/#getvpclinkspaginator)
        """
