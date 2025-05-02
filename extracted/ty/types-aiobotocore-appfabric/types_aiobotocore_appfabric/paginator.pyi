"""
Type annotations for appfabric service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appfabric/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_appfabric.client import AppFabricClient
    from types_aiobotocore_appfabric.paginator import (
        ListAppAuthorizationsPaginator,
        ListAppBundlesPaginator,
        ListIngestionDestinationsPaginator,
        ListIngestionsPaginator,
    )

    session = get_session()
    with session.create_client("appfabric") as client:
        client: AppFabricClient

        list_app_authorizations_paginator: ListAppAuthorizationsPaginator = client.get_paginator("list_app_authorizations")
        list_app_bundles_paginator: ListAppBundlesPaginator = client.get_paginator("list_app_bundles")
        list_ingestion_destinations_paginator: ListIngestionDestinationsPaginator = client.get_paginator("list_ingestion_destinations")
        list_ingestions_paginator: ListIngestionsPaginator = client.get_paginator("list_ingestions")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListAppAuthorizationsRequestPaginateTypeDef,
    ListAppAuthorizationsResponseTypeDef,
    ListAppBundlesRequestPaginateTypeDef,
    ListAppBundlesResponseTypeDef,
    ListIngestionDestinationsRequestPaginateTypeDef,
    ListIngestionDestinationsResponseTypeDef,
    ListIngestionsRequestPaginateTypeDef,
    ListIngestionsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListAppAuthorizationsPaginator",
    "ListAppBundlesPaginator",
    "ListIngestionDestinationsPaginator",
    "ListIngestionsPaginator",
)

if TYPE_CHECKING:
    _ListAppAuthorizationsPaginatorBase = AioPaginator[ListAppAuthorizationsResponseTypeDef]
else:
    _ListAppAuthorizationsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListAppAuthorizationsPaginator(_ListAppAuthorizationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appfabric/paginator/ListAppAuthorizations.html#AppFabric.Paginator.ListAppAuthorizations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appfabric/paginators/#listappauthorizationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAppAuthorizationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAppAuthorizationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appfabric/paginator/ListAppAuthorizations.html#AppFabric.Paginator.ListAppAuthorizations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appfabric/paginators/#listappauthorizationspaginator)
        """

if TYPE_CHECKING:
    _ListAppBundlesPaginatorBase = AioPaginator[ListAppBundlesResponseTypeDef]
else:
    _ListAppBundlesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListAppBundlesPaginator(_ListAppBundlesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appfabric/paginator/ListAppBundles.html#AppFabric.Paginator.ListAppBundles)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appfabric/paginators/#listappbundlespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAppBundlesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAppBundlesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appfabric/paginator/ListAppBundles.html#AppFabric.Paginator.ListAppBundles.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appfabric/paginators/#listappbundlespaginator)
        """

if TYPE_CHECKING:
    _ListIngestionDestinationsPaginatorBase = AioPaginator[ListIngestionDestinationsResponseTypeDef]
else:
    _ListIngestionDestinationsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListIngestionDestinationsPaginator(_ListIngestionDestinationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appfabric/paginator/ListIngestionDestinations.html#AppFabric.Paginator.ListIngestionDestinations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appfabric/paginators/#listingestiondestinationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListIngestionDestinationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListIngestionDestinationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appfabric/paginator/ListIngestionDestinations.html#AppFabric.Paginator.ListIngestionDestinations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appfabric/paginators/#listingestiondestinationspaginator)
        """

if TYPE_CHECKING:
    _ListIngestionsPaginatorBase = AioPaginator[ListIngestionsResponseTypeDef]
else:
    _ListIngestionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListIngestionsPaginator(_ListIngestionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appfabric/paginator/ListIngestions.html#AppFabric.Paginator.ListIngestions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appfabric/paginators/#listingestionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListIngestionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListIngestionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appfabric/paginator/ListIngestions.html#AppFabric.Paginator.ListIngestions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appfabric/paginators/#listingestionspaginator)
        """
