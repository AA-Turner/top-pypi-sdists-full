"""
Type annotations for lambda service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_lambda.client import LambdaClient
    from types_aiobotocore_lambda.paginator import (
        GetDurableExecutionHistoryPaginator,
        GetDurableExecutionStatePaginator,
        ListAliasesPaginator,
        ListCapacityProvidersPaginator,
        ListCodeSigningConfigsPaginator,
        ListDurableExecutionsByFunctionPaginator,
        ListEventSourceMappingsPaginator,
        ListFunctionEventInvokeConfigsPaginator,
        ListFunctionUrlConfigsPaginator,
        ListFunctionVersionsByCapacityProviderPaginator,
        ListFunctionsByCodeSigningConfigPaginator,
        ListFunctionsPaginator,
        ListLayerVersionsPaginator,
        ListLayersPaginator,
        ListProvisionedConcurrencyConfigsPaginator,
        ListVersionsByFunctionPaginator,
    )

    session = get_session()
    with session.create_client("lambda") as client:
        client: LambdaClient

        get_durable_execution_history_paginator: GetDurableExecutionHistoryPaginator = client.get_paginator("get_durable_execution_history")
        get_durable_execution_state_paginator: GetDurableExecutionStatePaginator = client.get_paginator("get_durable_execution_state")
        list_aliases_paginator: ListAliasesPaginator = client.get_paginator("list_aliases")
        list_capacity_providers_paginator: ListCapacityProvidersPaginator = client.get_paginator("list_capacity_providers")
        list_code_signing_configs_paginator: ListCodeSigningConfigsPaginator = client.get_paginator("list_code_signing_configs")
        list_durable_executions_by_function_paginator: ListDurableExecutionsByFunctionPaginator = client.get_paginator("list_durable_executions_by_function")
        list_event_source_mappings_paginator: ListEventSourceMappingsPaginator = client.get_paginator("list_event_source_mappings")
        list_function_event_invoke_configs_paginator: ListFunctionEventInvokeConfigsPaginator = client.get_paginator("list_function_event_invoke_configs")
        list_function_url_configs_paginator: ListFunctionUrlConfigsPaginator = client.get_paginator("list_function_url_configs")
        list_function_versions_by_capacity_provider_paginator: ListFunctionVersionsByCapacityProviderPaginator = client.get_paginator("list_function_versions_by_capacity_provider")
        list_functions_by_code_signing_config_paginator: ListFunctionsByCodeSigningConfigPaginator = client.get_paginator("list_functions_by_code_signing_config")
        list_functions_paginator: ListFunctionsPaginator = client.get_paginator("list_functions")
        list_layer_versions_paginator: ListLayerVersionsPaginator = client.get_paginator("list_layer_versions")
        list_layers_paginator: ListLayersPaginator = client.get_paginator("list_layers")
        list_provisioned_concurrency_configs_paginator: ListProvisionedConcurrencyConfigsPaginator = client.get_paginator("list_provisioned_concurrency_configs")
        list_versions_by_function_paginator: ListVersionsByFunctionPaginator = client.get_paginator("list_versions_by_function")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    GetDurableExecutionHistoryRequestPaginateTypeDef,
    GetDurableExecutionHistoryResponseTypeDef,
    GetDurableExecutionStateRequestPaginateTypeDef,
    GetDurableExecutionStateResponseTypeDef,
    ListAliasesRequestPaginateTypeDef,
    ListAliasesResponseTypeDef,
    ListCapacityProvidersRequestPaginateTypeDef,
    ListCapacityProvidersResponseTypeDef,
    ListCodeSigningConfigsRequestPaginateTypeDef,
    ListCodeSigningConfigsResponseTypeDef,
    ListDurableExecutionsByFunctionRequestPaginateTypeDef,
    ListDurableExecutionsByFunctionResponseTypeDef,
    ListEventSourceMappingsRequestPaginateTypeDef,
    ListEventSourceMappingsResponseTypeDef,
    ListFunctionEventInvokeConfigsRequestPaginateTypeDef,
    ListFunctionEventInvokeConfigsResponseTypeDef,
    ListFunctionsByCodeSigningConfigRequestPaginateTypeDef,
    ListFunctionsByCodeSigningConfigResponseTypeDef,
    ListFunctionsRequestPaginateTypeDef,
    ListFunctionsResponseTypeDef,
    ListFunctionUrlConfigsRequestPaginateTypeDef,
    ListFunctionUrlConfigsResponseTypeDef,
    ListFunctionVersionsByCapacityProviderRequestPaginateTypeDef,
    ListFunctionVersionsByCapacityProviderResponseTypeDef,
    ListLayersRequestPaginateTypeDef,
    ListLayersResponseTypeDef,
    ListLayerVersionsRequestPaginateTypeDef,
    ListLayerVersionsResponseTypeDef,
    ListProvisionedConcurrencyConfigsRequestPaginateTypeDef,
    ListProvisionedConcurrencyConfigsResponseTypeDef,
    ListVersionsByFunctionRequestPaginateTypeDef,
    ListVersionsByFunctionResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "GetDurableExecutionHistoryPaginator",
    "GetDurableExecutionStatePaginator",
    "ListAliasesPaginator",
    "ListCapacityProvidersPaginator",
    "ListCodeSigningConfigsPaginator",
    "ListDurableExecutionsByFunctionPaginator",
    "ListEventSourceMappingsPaginator",
    "ListFunctionEventInvokeConfigsPaginator",
    "ListFunctionUrlConfigsPaginator",
    "ListFunctionVersionsByCapacityProviderPaginator",
    "ListFunctionsByCodeSigningConfigPaginator",
    "ListFunctionsPaginator",
    "ListLayerVersionsPaginator",
    "ListLayersPaginator",
    "ListProvisionedConcurrencyConfigsPaginator",
    "ListVersionsByFunctionPaginator",
)

if TYPE_CHECKING:
    _GetDurableExecutionHistoryPaginatorBase = AioPaginator[
        GetDurableExecutionHistoryResponseTypeDef
    ]
else:
    _GetDurableExecutionHistoryPaginatorBase = AioPaginator  # type: ignore[assignment]

class GetDurableExecutionHistoryPaginator(_GetDurableExecutionHistoryPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda/paginator/GetDurableExecutionHistory.html#Lambda.Paginator.GetDurableExecutionHistory)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/paginators/#getdurableexecutionhistorypaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetDurableExecutionHistoryRequestPaginateTypeDef]
    ) -> AioPageIterator[GetDurableExecutionHistoryResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda/paginator/GetDurableExecutionHistory.html#Lambda.Paginator.GetDurableExecutionHistory.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/paginators/#getdurableexecutionhistorypaginator)
        """

if TYPE_CHECKING:
    _GetDurableExecutionStatePaginatorBase = AioPaginator[GetDurableExecutionStateResponseTypeDef]
else:
    _GetDurableExecutionStatePaginatorBase = AioPaginator  # type: ignore[assignment]

class GetDurableExecutionStatePaginator(_GetDurableExecutionStatePaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda/paginator/GetDurableExecutionState.html#Lambda.Paginator.GetDurableExecutionState)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/paginators/#getdurableexecutionstatepaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetDurableExecutionStateRequestPaginateTypeDef]
    ) -> AioPageIterator[GetDurableExecutionStateResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda/paginator/GetDurableExecutionState.html#Lambda.Paginator.GetDurableExecutionState.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/paginators/#getdurableexecutionstatepaginator)
        """

if TYPE_CHECKING:
    _ListAliasesPaginatorBase = AioPaginator[ListAliasesResponseTypeDef]
else:
    _ListAliasesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListAliasesPaginator(_ListAliasesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda/paginator/ListAliases.html#Lambda.Paginator.ListAliases)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/paginators/#listaliasespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAliasesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAliasesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda/paginator/ListAliases.html#Lambda.Paginator.ListAliases.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/paginators/#listaliasespaginator)
        """

if TYPE_CHECKING:
    _ListCapacityProvidersPaginatorBase = AioPaginator[ListCapacityProvidersResponseTypeDef]
else:
    _ListCapacityProvidersPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListCapacityProvidersPaginator(_ListCapacityProvidersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda/paginator/ListCapacityProviders.html#Lambda.Paginator.ListCapacityProviders)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/paginators/#listcapacityproviderspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCapacityProvidersRequestPaginateTypeDef]
    ) -> AioPageIterator[ListCapacityProvidersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda/paginator/ListCapacityProviders.html#Lambda.Paginator.ListCapacityProviders.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/paginators/#listcapacityproviderspaginator)
        """

if TYPE_CHECKING:
    _ListCodeSigningConfigsPaginatorBase = AioPaginator[ListCodeSigningConfigsResponseTypeDef]
else:
    _ListCodeSigningConfigsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListCodeSigningConfigsPaginator(_ListCodeSigningConfigsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda/paginator/ListCodeSigningConfigs.html#Lambda.Paginator.ListCodeSigningConfigs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/paginators/#listcodesigningconfigspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCodeSigningConfigsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListCodeSigningConfigsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda/paginator/ListCodeSigningConfigs.html#Lambda.Paginator.ListCodeSigningConfigs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/paginators/#listcodesigningconfigspaginator)
        """

if TYPE_CHECKING:
    _ListDurableExecutionsByFunctionPaginatorBase = AioPaginator[
        ListDurableExecutionsByFunctionResponseTypeDef
    ]
else:
    _ListDurableExecutionsByFunctionPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListDurableExecutionsByFunctionPaginator(_ListDurableExecutionsByFunctionPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda/paginator/ListDurableExecutionsByFunction.html#Lambda.Paginator.ListDurableExecutionsByFunction)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/paginators/#listdurableexecutionsbyfunctionpaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDurableExecutionsByFunctionRequestPaginateTypeDef]
    ) -> AioPageIterator[ListDurableExecutionsByFunctionResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda/paginator/ListDurableExecutionsByFunction.html#Lambda.Paginator.ListDurableExecutionsByFunction.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/paginators/#listdurableexecutionsbyfunctionpaginator)
        """

if TYPE_CHECKING:
    _ListEventSourceMappingsPaginatorBase = AioPaginator[ListEventSourceMappingsResponseTypeDef]
else:
    _ListEventSourceMappingsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListEventSourceMappingsPaginator(_ListEventSourceMappingsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda/paginator/ListEventSourceMappings.html#Lambda.Paginator.ListEventSourceMappings)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/paginators/#listeventsourcemappingspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListEventSourceMappingsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListEventSourceMappingsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda/paginator/ListEventSourceMappings.html#Lambda.Paginator.ListEventSourceMappings.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/paginators/#listeventsourcemappingspaginator)
        """

if TYPE_CHECKING:
    _ListFunctionEventInvokeConfigsPaginatorBase = AioPaginator[
        ListFunctionEventInvokeConfigsResponseTypeDef
    ]
else:
    _ListFunctionEventInvokeConfigsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListFunctionEventInvokeConfigsPaginator(_ListFunctionEventInvokeConfigsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda/paginator/ListFunctionEventInvokeConfigs.html#Lambda.Paginator.ListFunctionEventInvokeConfigs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/paginators/#listfunctioneventinvokeconfigspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListFunctionEventInvokeConfigsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListFunctionEventInvokeConfigsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda/paginator/ListFunctionEventInvokeConfigs.html#Lambda.Paginator.ListFunctionEventInvokeConfigs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/paginators/#listfunctioneventinvokeconfigspaginator)
        """

if TYPE_CHECKING:
    _ListFunctionUrlConfigsPaginatorBase = AioPaginator[ListFunctionUrlConfigsResponseTypeDef]
else:
    _ListFunctionUrlConfigsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListFunctionUrlConfigsPaginator(_ListFunctionUrlConfigsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda/paginator/ListFunctionUrlConfigs.html#Lambda.Paginator.ListFunctionUrlConfigs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/paginators/#listfunctionurlconfigspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListFunctionUrlConfigsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListFunctionUrlConfigsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda/paginator/ListFunctionUrlConfigs.html#Lambda.Paginator.ListFunctionUrlConfigs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/paginators/#listfunctionurlconfigspaginator)
        """

if TYPE_CHECKING:
    _ListFunctionVersionsByCapacityProviderPaginatorBase = AioPaginator[
        ListFunctionVersionsByCapacityProviderResponseTypeDef
    ]
else:
    _ListFunctionVersionsByCapacityProviderPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListFunctionVersionsByCapacityProviderPaginator(
    _ListFunctionVersionsByCapacityProviderPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda/paginator/ListFunctionVersionsByCapacityProvider.html#Lambda.Paginator.ListFunctionVersionsByCapacityProvider)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/paginators/#listfunctionversionsbycapacityproviderpaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListFunctionVersionsByCapacityProviderRequestPaginateTypeDef]
    ) -> AioPageIterator[ListFunctionVersionsByCapacityProviderResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda/paginator/ListFunctionVersionsByCapacityProvider.html#Lambda.Paginator.ListFunctionVersionsByCapacityProvider.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/paginators/#listfunctionversionsbycapacityproviderpaginator)
        """

if TYPE_CHECKING:
    _ListFunctionsByCodeSigningConfigPaginatorBase = AioPaginator[
        ListFunctionsByCodeSigningConfigResponseTypeDef
    ]
else:
    _ListFunctionsByCodeSigningConfigPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListFunctionsByCodeSigningConfigPaginator(_ListFunctionsByCodeSigningConfigPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda/paginator/ListFunctionsByCodeSigningConfig.html#Lambda.Paginator.ListFunctionsByCodeSigningConfig)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/paginators/#listfunctionsbycodesigningconfigpaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListFunctionsByCodeSigningConfigRequestPaginateTypeDef]
    ) -> AioPageIterator[ListFunctionsByCodeSigningConfigResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda/paginator/ListFunctionsByCodeSigningConfig.html#Lambda.Paginator.ListFunctionsByCodeSigningConfig.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/paginators/#listfunctionsbycodesigningconfigpaginator)
        """

if TYPE_CHECKING:
    _ListFunctionsPaginatorBase = AioPaginator[ListFunctionsResponseTypeDef]
else:
    _ListFunctionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListFunctionsPaginator(_ListFunctionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda/paginator/ListFunctions.html#Lambda.Paginator.ListFunctions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/paginators/#listfunctionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListFunctionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListFunctionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda/paginator/ListFunctions.html#Lambda.Paginator.ListFunctions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/paginators/#listfunctionspaginator)
        """

if TYPE_CHECKING:
    _ListLayerVersionsPaginatorBase = AioPaginator[ListLayerVersionsResponseTypeDef]
else:
    _ListLayerVersionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListLayerVersionsPaginator(_ListLayerVersionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda/paginator/ListLayerVersions.html#Lambda.Paginator.ListLayerVersions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/paginators/#listlayerversionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListLayerVersionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListLayerVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda/paginator/ListLayerVersions.html#Lambda.Paginator.ListLayerVersions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/paginators/#listlayerversionspaginator)
        """

if TYPE_CHECKING:
    _ListLayersPaginatorBase = AioPaginator[ListLayersResponseTypeDef]
else:
    _ListLayersPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListLayersPaginator(_ListLayersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda/paginator/ListLayers.html#Lambda.Paginator.ListLayers)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/paginators/#listlayerspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListLayersRequestPaginateTypeDef]
    ) -> AioPageIterator[ListLayersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda/paginator/ListLayers.html#Lambda.Paginator.ListLayers.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/paginators/#listlayerspaginator)
        """

if TYPE_CHECKING:
    _ListProvisionedConcurrencyConfigsPaginatorBase = AioPaginator[
        ListProvisionedConcurrencyConfigsResponseTypeDef
    ]
else:
    _ListProvisionedConcurrencyConfigsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListProvisionedConcurrencyConfigsPaginator(_ListProvisionedConcurrencyConfigsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda/paginator/ListProvisionedConcurrencyConfigs.html#Lambda.Paginator.ListProvisionedConcurrencyConfigs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/paginators/#listprovisionedconcurrencyconfigspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListProvisionedConcurrencyConfigsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListProvisionedConcurrencyConfigsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda/paginator/ListProvisionedConcurrencyConfigs.html#Lambda.Paginator.ListProvisionedConcurrencyConfigs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/paginators/#listprovisionedconcurrencyconfigspaginator)
        """

if TYPE_CHECKING:
    _ListVersionsByFunctionPaginatorBase = AioPaginator[ListVersionsByFunctionResponseTypeDef]
else:
    _ListVersionsByFunctionPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListVersionsByFunctionPaginator(_ListVersionsByFunctionPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda/paginator/ListVersionsByFunction.html#Lambda.Paginator.ListVersionsByFunction)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/paginators/#listversionsbyfunctionpaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListVersionsByFunctionRequestPaginateTypeDef]
    ) -> AioPageIterator[ListVersionsByFunctionResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda/paginator/ListVersionsByFunction.html#Lambda.Paginator.ListVersionsByFunction.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/paginators/#listversionsbyfunctionpaginator)
        """
