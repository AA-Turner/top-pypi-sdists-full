"""
Type annotations for migrationhubstrategy service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migrationhubstrategy/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_migrationhubstrategy.client import MigrationHubStrategyRecommendationsClient
    from types_aiobotocore_migrationhubstrategy.paginator import (
        GetServerDetailsPaginator,
        ListAnalyzableServersPaginator,
        ListApplicationComponentsPaginator,
        ListCollectorsPaginator,
        ListImportFileTaskPaginator,
        ListServersPaginator,
    )

    session = get_session()
    with session.create_client("migrationhubstrategy") as client:
        client: MigrationHubStrategyRecommendationsClient

        get_server_details_paginator: GetServerDetailsPaginator = client.get_paginator("get_server_details")
        list_analyzable_servers_paginator: ListAnalyzableServersPaginator = client.get_paginator("list_analyzable_servers")
        list_application_components_paginator: ListApplicationComponentsPaginator = client.get_paginator("list_application_components")
        list_collectors_paginator: ListCollectorsPaginator = client.get_paginator("list_collectors")
        list_import_file_task_paginator: ListImportFileTaskPaginator = client.get_paginator("list_import_file_task")
        list_servers_paginator: ListServersPaginator = client.get_paginator("list_servers")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    GetServerDetailsRequestPaginateTypeDef,
    GetServerDetailsResponseTypeDef,
    ListAnalyzableServersRequestPaginateTypeDef,
    ListAnalyzableServersResponseTypeDef,
    ListApplicationComponentsRequestPaginateTypeDef,
    ListApplicationComponentsResponseTypeDef,
    ListCollectorsRequestPaginateTypeDef,
    ListCollectorsResponseTypeDef,
    ListImportFileTaskRequestPaginateTypeDef,
    ListImportFileTaskResponseTypeDef,
    ListServersRequestPaginateTypeDef,
    ListServersResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "GetServerDetailsPaginator",
    "ListAnalyzableServersPaginator",
    "ListApplicationComponentsPaginator",
    "ListCollectorsPaginator",
    "ListImportFileTaskPaginator",
    "ListServersPaginator",
)


if TYPE_CHECKING:
    _GetServerDetailsPaginatorBase = AioPaginator[GetServerDetailsResponseTypeDef]
else:
    _GetServerDetailsPaginatorBase = AioPaginator  # type: ignore[assignment]


class GetServerDetailsPaginator(_GetServerDetailsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy/paginator/GetServerDetails.html#MigrationHubStrategyRecommendations.Paginator.GetServerDetails)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migrationhubstrategy/paginators/#getserverdetailspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetServerDetailsRequestPaginateTypeDef]
    ) -> AioPageIterator[GetServerDetailsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy/paginator/GetServerDetails.html#MigrationHubStrategyRecommendations.Paginator.GetServerDetails.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migrationhubstrategy/paginators/#getserverdetailspaginator)
        """


if TYPE_CHECKING:
    _ListAnalyzableServersPaginatorBase = AioPaginator[ListAnalyzableServersResponseTypeDef]
else:
    _ListAnalyzableServersPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListAnalyzableServersPaginator(_ListAnalyzableServersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy/paginator/ListAnalyzableServers.html#MigrationHubStrategyRecommendations.Paginator.ListAnalyzableServers)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migrationhubstrategy/paginators/#listanalyzableserverspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAnalyzableServersRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAnalyzableServersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy/paginator/ListAnalyzableServers.html#MigrationHubStrategyRecommendations.Paginator.ListAnalyzableServers.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migrationhubstrategy/paginators/#listanalyzableserverspaginator)
        """


if TYPE_CHECKING:
    _ListApplicationComponentsPaginatorBase = AioPaginator[ListApplicationComponentsResponseTypeDef]
else:
    _ListApplicationComponentsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListApplicationComponentsPaginator(_ListApplicationComponentsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy/paginator/ListApplicationComponents.html#MigrationHubStrategyRecommendations.Paginator.ListApplicationComponents)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migrationhubstrategy/paginators/#listapplicationcomponentspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListApplicationComponentsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListApplicationComponentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy/paginator/ListApplicationComponents.html#MigrationHubStrategyRecommendations.Paginator.ListApplicationComponents.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migrationhubstrategy/paginators/#listapplicationcomponentspaginator)
        """


if TYPE_CHECKING:
    _ListCollectorsPaginatorBase = AioPaginator[ListCollectorsResponseTypeDef]
else:
    _ListCollectorsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListCollectorsPaginator(_ListCollectorsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy/paginator/ListCollectors.html#MigrationHubStrategyRecommendations.Paginator.ListCollectors)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migrationhubstrategy/paginators/#listcollectorspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCollectorsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListCollectorsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy/paginator/ListCollectors.html#MigrationHubStrategyRecommendations.Paginator.ListCollectors.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migrationhubstrategy/paginators/#listcollectorspaginator)
        """


if TYPE_CHECKING:
    _ListImportFileTaskPaginatorBase = AioPaginator[ListImportFileTaskResponseTypeDef]
else:
    _ListImportFileTaskPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListImportFileTaskPaginator(_ListImportFileTaskPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy/paginator/ListImportFileTask.html#MigrationHubStrategyRecommendations.Paginator.ListImportFileTask)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migrationhubstrategy/paginators/#listimportfiletaskpaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListImportFileTaskRequestPaginateTypeDef]
    ) -> AioPageIterator[ListImportFileTaskResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy/paginator/ListImportFileTask.html#MigrationHubStrategyRecommendations.Paginator.ListImportFileTask.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migrationhubstrategy/paginators/#listimportfiletaskpaginator)
        """


if TYPE_CHECKING:
    _ListServersPaginatorBase = AioPaginator[ListServersResponseTypeDef]
else:
    _ListServersPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListServersPaginator(_ListServersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy/paginator/ListServers.html#MigrationHubStrategyRecommendations.Paginator.ListServers)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migrationhubstrategy/paginators/#listserverspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListServersRequestPaginateTypeDef]
    ) -> AioPageIterator[ListServersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy/paginator/ListServers.html#MigrationHubStrategyRecommendations.Paginator.ListServers.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migrationhubstrategy/paginators/#listserverspaginator)
        """
