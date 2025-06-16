"""
Type annotations for appsync service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_appsync.client import AppSyncClient
    from types_aiobotocore_appsync.paginator import (
        ListApiKeysPaginator,
        ListApisPaginator,
        ListChannelNamespacesPaginator,
        ListDataSourcesPaginator,
        ListDomainNamesPaginator,
        ListFunctionsPaginator,
        ListGraphqlApisPaginator,
        ListResolversByFunctionPaginator,
        ListResolversPaginator,
        ListSourceApiAssociationsPaginator,
        ListTypesByAssociationPaginator,
        ListTypesPaginator,
    )

    session = get_session()
    with session.create_client("appsync") as client:
        client: AppSyncClient

        list_api_keys_paginator: ListApiKeysPaginator = client.get_paginator("list_api_keys")
        list_apis_paginator: ListApisPaginator = client.get_paginator("list_apis")
        list_channel_namespaces_paginator: ListChannelNamespacesPaginator = client.get_paginator("list_channel_namespaces")
        list_data_sources_paginator: ListDataSourcesPaginator = client.get_paginator("list_data_sources")
        list_domain_names_paginator: ListDomainNamesPaginator = client.get_paginator("list_domain_names")
        list_functions_paginator: ListFunctionsPaginator = client.get_paginator("list_functions")
        list_graphql_apis_paginator: ListGraphqlApisPaginator = client.get_paginator("list_graphql_apis")
        list_resolvers_by_function_paginator: ListResolversByFunctionPaginator = client.get_paginator("list_resolvers_by_function")
        list_resolvers_paginator: ListResolversPaginator = client.get_paginator("list_resolvers")
        list_source_api_associations_paginator: ListSourceApiAssociationsPaginator = client.get_paginator("list_source_api_associations")
        list_types_by_association_paginator: ListTypesByAssociationPaginator = client.get_paginator("list_types_by_association")
        list_types_paginator: ListTypesPaginator = client.get_paginator("list_types")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListApiKeysRequestPaginateTypeDef,
    ListApiKeysResponseTypeDef,
    ListApisRequestPaginateTypeDef,
    ListApisResponseTypeDef,
    ListChannelNamespacesRequestPaginateTypeDef,
    ListChannelNamespacesResponseTypeDef,
    ListDataSourcesRequestPaginateTypeDef,
    ListDataSourcesResponseTypeDef,
    ListDomainNamesRequestPaginateTypeDef,
    ListDomainNamesResponseTypeDef,
    ListFunctionsRequestPaginateTypeDef,
    ListFunctionsResponseTypeDef,
    ListGraphqlApisRequestPaginateTypeDef,
    ListGraphqlApisResponseTypeDef,
    ListResolversByFunctionRequestPaginateTypeDef,
    ListResolversByFunctionResponseTypeDef,
    ListResolversRequestPaginateTypeDef,
    ListResolversResponseTypeDef,
    ListSourceApiAssociationsRequestPaginateTypeDef,
    ListSourceApiAssociationsResponseTypeDef,
    ListTypesByAssociationRequestPaginateTypeDef,
    ListTypesByAssociationResponseTypeDef,
    ListTypesRequestPaginateTypeDef,
    ListTypesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListApiKeysPaginator",
    "ListApisPaginator",
    "ListChannelNamespacesPaginator",
    "ListDataSourcesPaginator",
    "ListDomainNamesPaginator",
    "ListFunctionsPaginator",
    "ListGraphqlApisPaginator",
    "ListResolversByFunctionPaginator",
    "ListResolversPaginator",
    "ListSourceApiAssociationsPaginator",
    "ListTypesByAssociationPaginator",
    "ListTypesPaginator",
)

if TYPE_CHECKING:
    _ListApiKeysPaginatorBase = AioPaginator[ListApiKeysResponseTypeDef]
else:
    _ListApiKeysPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListApiKeysPaginator(_ListApiKeysPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync/paginator/ListApiKeys.html#AppSync.Paginator.ListApiKeys)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/paginators/#listapikeyspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListApiKeysRequestPaginateTypeDef]
    ) -> AioPageIterator[ListApiKeysResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync/paginator/ListApiKeys.html#AppSync.Paginator.ListApiKeys.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/paginators/#listapikeyspaginator)
        """

if TYPE_CHECKING:
    _ListApisPaginatorBase = AioPaginator[ListApisResponseTypeDef]
else:
    _ListApisPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListApisPaginator(_ListApisPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync/paginator/ListApis.html#AppSync.Paginator.ListApis)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/paginators/#listapispaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListApisRequestPaginateTypeDef]
    ) -> AioPageIterator[ListApisResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync/paginator/ListApis.html#AppSync.Paginator.ListApis.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/paginators/#listapispaginator)
        """

if TYPE_CHECKING:
    _ListChannelNamespacesPaginatorBase = AioPaginator[ListChannelNamespacesResponseTypeDef]
else:
    _ListChannelNamespacesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListChannelNamespacesPaginator(_ListChannelNamespacesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync/paginator/ListChannelNamespaces.html#AppSync.Paginator.ListChannelNamespaces)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/paginators/#listchannelnamespacespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListChannelNamespacesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListChannelNamespacesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync/paginator/ListChannelNamespaces.html#AppSync.Paginator.ListChannelNamespaces.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/paginators/#listchannelnamespacespaginator)
        """

if TYPE_CHECKING:
    _ListDataSourcesPaginatorBase = AioPaginator[ListDataSourcesResponseTypeDef]
else:
    _ListDataSourcesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListDataSourcesPaginator(_ListDataSourcesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync/paginator/ListDataSources.html#AppSync.Paginator.ListDataSources)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/paginators/#listdatasourcespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDataSourcesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListDataSourcesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync/paginator/ListDataSources.html#AppSync.Paginator.ListDataSources.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/paginators/#listdatasourcespaginator)
        """

if TYPE_CHECKING:
    _ListDomainNamesPaginatorBase = AioPaginator[ListDomainNamesResponseTypeDef]
else:
    _ListDomainNamesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListDomainNamesPaginator(_ListDomainNamesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync/paginator/ListDomainNames.html#AppSync.Paginator.ListDomainNames)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/paginators/#listdomainnamespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDomainNamesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListDomainNamesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync/paginator/ListDomainNames.html#AppSync.Paginator.ListDomainNames.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/paginators/#listdomainnamespaginator)
        """

if TYPE_CHECKING:
    _ListFunctionsPaginatorBase = AioPaginator[ListFunctionsResponseTypeDef]
else:
    _ListFunctionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListFunctionsPaginator(_ListFunctionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync/paginator/ListFunctions.html#AppSync.Paginator.ListFunctions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/paginators/#listfunctionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListFunctionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListFunctionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync/paginator/ListFunctions.html#AppSync.Paginator.ListFunctions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/paginators/#listfunctionspaginator)
        """

if TYPE_CHECKING:
    _ListGraphqlApisPaginatorBase = AioPaginator[ListGraphqlApisResponseTypeDef]
else:
    _ListGraphqlApisPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListGraphqlApisPaginator(_ListGraphqlApisPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync/paginator/ListGraphqlApis.html#AppSync.Paginator.ListGraphqlApis)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/paginators/#listgraphqlapispaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListGraphqlApisRequestPaginateTypeDef]
    ) -> AioPageIterator[ListGraphqlApisResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync/paginator/ListGraphqlApis.html#AppSync.Paginator.ListGraphqlApis.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/paginators/#listgraphqlapispaginator)
        """

if TYPE_CHECKING:
    _ListResolversByFunctionPaginatorBase = AioPaginator[ListResolversByFunctionResponseTypeDef]
else:
    _ListResolversByFunctionPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListResolversByFunctionPaginator(_ListResolversByFunctionPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync/paginator/ListResolversByFunction.html#AppSync.Paginator.ListResolversByFunction)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/paginators/#listresolversbyfunctionpaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListResolversByFunctionRequestPaginateTypeDef]
    ) -> AioPageIterator[ListResolversByFunctionResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync/paginator/ListResolversByFunction.html#AppSync.Paginator.ListResolversByFunction.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/paginators/#listresolversbyfunctionpaginator)
        """

if TYPE_CHECKING:
    _ListResolversPaginatorBase = AioPaginator[ListResolversResponseTypeDef]
else:
    _ListResolversPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListResolversPaginator(_ListResolversPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync/paginator/ListResolvers.html#AppSync.Paginator.ListResolvers)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/paginators/#listresolverspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListResolversRequestPaginateTypeDef]
    ) -> AioPageIterator[ListResolversResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync/paginator/ListResolvers.html#AppSync.Paginator.ListResolvers.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/paginators/#listresolverspaginator)
        """

if TYPE_CHECKING:
    _ListSourceApiAssociationsPaginatorBase = AioPaginator[ListSourceApiAssociationsResponseTypeDef]
else:
    _ListSourceApiAssociationsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListSourceApiAssociationsPaginator(_ListSourceApiAssociationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync/paginator/ListSourceApiAssociations.html#AppSync.Paginator.ListSourceApiAssociations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/paginators/#listsourceapiassociationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSourceApiAssociationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListSourceApiAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync/paginator/ListSourceApiAssociations.html#AppSync.Paginator.ListSourceApiAssociations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/paginators/#listsourceapiassociationspaginator)
        """

if TYPE_CHECKING:
    _ListTypesByAssociationPaginatorBase = AioPaginator[ListTypesByAssociationResponseTypeDef]
else:
    _ListTypesByAssociationPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListTypesByAssociationPaginator(_ListTypesByAssociationPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync/paginator/ListTypesByAssociation.html#AppSync.Paginator.ListTypesByAssociation)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/paginators/#listtypesbyassociationpaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTypesByAssociationRequestPaginateTypeDef]
    ) -> AioPageIterator[ListTypesByAssociationResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync/paginator/ListTypesByAssociation.html#AppSync.Paginator.ListTypesByAssociation.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/paginators/#listtypesbyassociationpaginator)
        """

if TYPE_CHECKING:
    _ListTypesPaginatorBase = AioPaginator[ListTypesResponseTypeDef]
else:
    _ListTypesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListTypesPaginator(_ListTypesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync/paginator/ListTypes.html#AppSync.Paginator.ListTypes)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/paginators/#listtypespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTypesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListTypesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync/paginator/ListTypes.html#AppSync.Paginator.ListTypes.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/paginators/#listtypespaginator)
        """
