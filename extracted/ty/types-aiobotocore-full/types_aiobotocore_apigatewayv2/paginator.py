"""
Type annotations for apigatewayv2 service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_apigatewayv2.client import ApiGatewayV2Client
    from types_aiobotocore_apigatewayv2.paginator import (
        GetApisPaginator,
        GetAuthorizersPaginator,
        GetDeploymentsPaginator,
        GetDomainNamesPaginator,
        GetIntegrationResponsesPaginator,
        GetIntegrationsPaginator,
        GetModelsPaginator,
        GetRouteResponsesPaginator,
        GetRoutesPaginator,
        GetStagesPaginator,
        ListRoutingRulesPaginator,
    )

    session = get_session()
    with session.create_client("apigatewayv2") as client:
        client: ApiGatewayV2Client

        get_apis_paginator: GetApisPaginator = client.get_paginator("get_apis")
        get_authorizers_paginator: GetAuthorizersPaginator = client.get_paginator("get_authorizers")
        get_deployments_paginator: GetDeploymentsPaginator = client.get_paginator("get_deployments")
        get_domain_names_paginator: GetDomainNamesPaginator = client.get_paginator("get_domain_names")
        get_integration_responses_paginator: GetIntegrationResponsesPaginator = client.get_paginator("get_integration_responses")
        get_integrations_paginator: GetIntegrationsPaginator = client.get_paginator("get_integrations")
        get_models_paginator: GetModelsPaginator = client.get_paginator("get_models")
        get_route_responses_paginator: GetRouteResponsesPaginator = client.get_paginator("get_route_responses")
        get_routes_paginator: GetRoutesPaginator = client.get_paginator("get_routes")
        get_stages_paginator: GetStagesPaginator = client.get_paginator("get_stages")
        list_routing_rules_paginator: ListRoutingRulesPaginator = client.get_paginator("list_routing_rules")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    GetApisRequestPaginateTypeDef,
    GetApisResponseTypeDef,
    GetAuthorizersRequestPaginateTypeDef,
    GetAuthorizersResponseTypeDef,
    GetDeploymentsRequestPaginateTypeDef,
    GetDeploymentsResponseTypeDef,
    GetDomainNamesRequestPaginateTypeDef,
    GetDomainNamesResponseTypeDef,
    GetIntegrationResponsesRequestPaginateTypeDef,
    GetIntegrationResponsesResponseTypeDef,
    GetIntegrationsRequestPaginateTypeDef,
    GetIntegrationsResponseTypeDef,
    GetModelsRequestPaginateTypeDef,
    GetModelsResponseTypeDef,
    GetRouteResponsesRequestPaginateTypeDef,
    GetRouteResponsesResponseTypeDef,
    GetRoutesRequestPaginateTypeDef,
    GetRoutesResponseTypeDef,
    GetStagesRequestPaginateTypeDef,
    GetStagesResponseTypeDef,
    ListRoutingRulesRequestPaginateTypeDef,
    ListRoutingRulesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "GetApisPaginator",
    "GetAuthorizersPaginator",
    "GetDeploymentsPaginator",
    "GetDomainNamesPaginator",
    "GetIntegrationResponsesPaginator",
    "GetIntegrationsPaginator",
    "GetModelsPaginator",
    "GetRouteResponsesPaginator",
    "GetRoutesPaginator",
    "GetStagesPaginator",
    "ListRoutingRulesPaginator",
)


if TYPE_CHECKING:
    _GetApisPaginatorBase = AioPaginator[GetApisResponseTypeDef]
else:
    _GetApisPaginatorBase = AioPaginator  # type: ignore[assignment]


class GetApisPaginator(_GetApisPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/paginator/GetApis.html#ApiGatewayV2.Paginator.GetApis)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/paginators/#getapispaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetApisRequestPaginateTypeDef]
    ) -> AioPageIterator[GetApisResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/paginator/GetApis.html#ApiGatewayV2.Paginator.GetApis.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/paginators/#getapispaginator)
        """


if TYPE_CHECKING:
    _GetAuthorizersPaginatorBase = AioPaginator[GetAuthorizersResponseTypeDef]
else:
    _GetAuthorizersPaginatorBase = AioPaginator  # type: ignore[assignment]


class GetAuthorizersPaginator(_GetAuthorizersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/paginator/GetAuthorizers.html#ApiGatewayV2.Paginator.GetAuthorizers)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/paginators/#getauthorizerspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetAuthorizersRequestPaginateTypeDef]
    ) -> AioPageIterator[GetAuthorizersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/paginator/GetAuthorizers.html#ApiGatewayV2.Paginator.GetAuthorizers.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/paginators/#getauthorizerspaginator)
        """


if TYPE_CHECKING:
    _GetDeploymentsPaginatorBase = AioPaginator[GetDeploymentsResponseTypeDef]
else:
    _GetDeploymentsPaginatorBase = AioPaginator  # type: ignore[assignment]


class GetDeploymentsPaginator(_GetDeploymentsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/paginator/GetDeployments.html#ApiGatewayV2.Paginator.GetDeployments)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/paginators/#getdeploymentspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetDeploymentsRequestPaginateTypeDef]
    ) -> AioPageIterator[GetDeploymentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/paginator/GetDeployments.html#ApiGatewayV2.Paginator.GetDeployments.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/paginators/#getdeploymentspaginator)
        """


if TYPE_CHECKING:
    _GetDomainNamesPaginatorBase = AioPaginator[GetDomainNamesResponseTypeDef]
else:
    _GetDomainNamesPaginatorBase = AioPaginator  # type: ignore[assignment]


class GetDomainNamesPaginator(_GetDomainNamesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/paginator/GetDomainNames.html#ApiGatewayV2.Paginator.GetDomainNames)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/paginators/#getdomainnamespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetDomainNamesRequestPaginateTypeDef]
    ) -> AioPageIterator[GetDomainNamesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/paginator/GetDomainNames.html#ApiGatewayV2.Paginator.GetDomainNames.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/paginators/#getdomainnamespaginator)
        """


if TYPE_CHECKING:
    _GetIntegrationResponsesPaginatorBase = AioPaginator[GetIntegrationResponsesResponseTypeDef]
else:
    _GetIntegrationResponsesPaginatorBase = AioPaginator  # type: ignore[assignment]


class GetIntegrationResponsesPaginator(_GetIntegrationResponsesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/paginator/GetIntegrationResponses.html#ApiGatewayV2.Paginator.GetIntegrationResponses)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/paginators/#getintegrationresponsespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetIntegrationResponsesRequestPaginateTypeDef]
    ) -> AioPageIterator[GetIntegrationResponsesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/paginator/GetIntegrationResponses.html#ApiGatewayV2.Paginator.GetIntegrationResponses.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/paginators/#getintegrationresponsespaginator)
        """


if TYPE_CHECKING:
    _GetIntegrationsPaginatorBase = AioPaginator[GetIntegrationsResponseTypeDef]
else:
    _GetIntegrationsPaginatorBase = AioPaginator  # type: ignore[assignment]


class GetIntegrationsPaginator(_GetIntegrationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/paginator/GetIntegrations.html#ApiGatewayV2.Paginator.GetIntegrations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/paginators/#getintegrationspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetIntegrationsRequestPaginateTypeDef]
    ) -> AioPageIterator[GetIntegrationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/paginator/GetIntegrations.html#ApiGatewayV2.Paginator.GetIntegrations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/paginators/#getintegrationspaginator)
        """


if TYPE_CHECKING:
    _GetModelsPaginatorBase = AioPaginator[GetModelsResponseTypeDef]
else:
    _GetModelsPaginatorBase = AioPaginator  # type: ignore[assignment]


class GetModelsPaginator(_GetModelsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/paginator/GetModels.html#ApiGatewayV2.Paginator.GetModels)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/paginators/#getmodelspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetModelsRequestPaginateTypeDef]
    ) -> AioPageIterator[GetModelsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/paginator/GetModels.html#ApiGatewayV2.Paginator.GetModels.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/paginators/#getmodelspaginator)
        """


if TYPE_CHECKING:
    _GetRouteResponsesPaginatorBase = AioPaginator[GetRouteResponsesResponseTypeDef]
else:
    _GetRouteResponsesPaginatorBase = AioPaginator  # type: ignore[assignment]


class GetRouteResponsesPaginator(_GetRouteResponsesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/paginator/GetRouteResponses.html#ApiGatewayV2.Paginator.GetRouteResponses)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/paginators/#getrouteresponsespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetRouteResponsesRequestPaginateTypeDef]
    ) -> AioPageIterator[GetRouteResponsesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/paginator/GetRouteResponses.html#ApiGatewayV2.Paginator.GetRouteResponses.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/paginators/#getrouteresponsespaginator)
        """


if TYPE_CHECKING:
    _GetRoutesPaginatorBase = AioPaginator[GetRoutesResponseTypeDef]
else:
    _GetRoutesPaginatorBase = AioPaginator  # type: ignore[assignment]


class GetRoutesPaginator(_GetRoutesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/paginator/GetRoutes.html#ApiGatewayV2.Paginator.GetRoutes)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/paginators/#getroutespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetRoutesRequestPaginateTypeDef]
    ) -> AioPageIterator[GetRoutesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/paginator/GetRoutes.html#ApiGatewayV2.Paginator.GetRoutes.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/paginators/#getroutespaginator)
        """


if TYPE_CHECKING:
    _GetStagesPaginatorBase = AioPaginator[GetStagesResponseTypeDef]
else:
    _GetStagesPaginatorBase = AioPaginator  # type: ignore[assignment]


class GetStagesPaginator(_GetStagesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/paginator/GetStages.html#ApiGatewayV2.Paginator.GetStages)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/paginators/#getstagespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetStagesRequestPaginateTypeDef]
    ) -> AioPageIterator[GetStagesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/paginator/GetStages.html#ApiGatewayV2.Paginator.GetStages.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/paginators/#getstagespaginator)
        """


if TYPE_CHECKING:
    _ListRoutingRulesPaginatorBase = AioPaginator[ListRoutingRulesResponseTypeDef]
else:
    _ListRoutingRulesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListRoutingRulesPaginator(_ListRoutingRulesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/paginator/ListRoutingRules.html#ApiGatewayV2.Paginator.ListRoutingRules)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/paginators/#listroutingrulespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRoutingRulesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListRoutingRulesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2/paginator/ListRoutingRules.html#ApiGatewayV2.Paginator.ListRoutingRules.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/paginators/#listroutingrulespaginator)
        """
