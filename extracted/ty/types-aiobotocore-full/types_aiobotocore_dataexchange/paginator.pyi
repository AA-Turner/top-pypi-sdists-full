"""
Type annotations for dataexchange service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_dataexchange.client import DataExchangeClient
    from types_aiobotocore_dataexchange.paginator import (
        ListDataGrantsPaginator,
        ListDataSetRevisionsPaginator,
        ListDataSetsPaginator,
        ListEventActionsPaginator,
        ListJobsPaginator,
        ListReceivedDataGrantsPaginator,
        ListRevisionAssetsPaginator,
    )

    session = get_session()
    with session.create_client("dataexchange") as client:
        client: DataExchangeClient

        list_data_grants_paginator: ListDataGrantsPaginator = client.get_paginator("list_data_grants")
        list_data_set_revisions_paginator: ListDataSetRevisionsPaginator = client.get_paginator("list_data_set_revisions")
        list_data_sets_paginator: ListDataSetsPaginator = client.get_paginator("list_data_sets")
        list_event_actions_paginator: ListEventActionsPaginator = client.get_paginator("list_event_actions")
        list_jobs_paginator: ListJobsPaginator = client.get_paginator("list_jobs")
        list_received_data_grants_paginator: ListReceivedDataGrantsPaginator = client.get_paginator("list_received_data_grants")
        list_revision_assets_paginator: ListRevisionAssetsPaginator = client.get_paginator("list_revision_assets")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListDataGrantsRequestPaginateTypeDef,
    ListDataGrantsResponseTypeDef,
    ListDataSetRevisionsRequestPaginateTypeDef,
    ListDataSetRevisionsResponseTypeDef,
    ListDataSetsRequestPaginateTypeDef,
    ListDataSetsResponseTypeDef,
    ListEventActionsRequestPaginateTypeDef,
    ListEventActionsResponseTypeDef,
    ListJobsRequestPaginateTypeDef,
    ListJobsResponseTypeDef,
    ListReceivedDataGrantsRequestPaginateTypeDef,
    ListReceivedDataGrantsResponseTypeDef,
    ListRevisionAssetsRequestPaginateTypeDef,
    ListRevisionAssetsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListDataGrantsPaginator",
    "ListDataSetRevisionsPaginator",
    "ListDataSetsPaginator",
    "ListEventActionsPaginator",
    "ListJobsPaginator",
    "ListReceivedDataGrantsPaginator",
    "ListRevisionAssetsPaginator",
)

if TYPE_CHECKING:
    _ListDataGrantsPaginatorBase = AioPaginator[ListDataGrantsResponseTypeDef]
else:
    _ListDataGrantsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListDataGrantsPaginator(_ListDataGrantsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange/paginator/ListDataGrants.html#DataExchange.Paginator.ListDataGrants)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/paginators/#listdatagrantspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDataGrantsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListDataGrantsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange/paginator/ListDataGrants.html#DataExchange.Paginator.ListDataGrants.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/paginators/#listdatagrantspaginator)
        """

if TYPE_CHECKING:
    _ListDataSetRevisionsPaginatorBase = AioPaginator[ListDataSetRevisionsResponseTypeDef]
else:
    _ListDataSetRevisionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListDataSetRevisionsPaginator(_ListDataSetRevisionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange/paginator/ListDataSetRevisions.html#DataExchange.Paginator.ListDataSetRevisions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/paginators/#listdatasetrevisionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDataSetRevisionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListDataSetRevisionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange/paginator/ListDataSetRevisions.html#DataExchange.Paginator.ListDataSetRevisions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/paginators/#listdatasetrevisionspaginator)
        """

if TYPE_CHECKING:
    _ListDataSetsPaginatorBase = AioPaginator[ListDataSetsResponseTypeDef]
else:
    _ListDataSetsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListDataSetsPaginator(_ListDataSetsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange/paginator/ListDataSets.html#DataExchange.Paginator.ListDataSets)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/paginators/#listdatasetspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDataSetsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListDataSetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange/paginator/ListDataSets.html#DataExchange.Paginator.ListDataSets.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/paginators/#listdatasetspaginator)
        """

if TYPE_CHECKING:
    _ListEventActionsPaginatorBase = AioPaginator[ListEventActionsResponseTypeDef]
else:
    _ListEventActionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListEventActionsPaginator(_ListEventActionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange/paginator/ListEventActions.html#DataExchange.Paginator.ListEventActions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/paginators/#listeventactionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListEventActionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListEventActionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange/paginator/ListEventActions.html#DataExchange.Paginator.ListEventActions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/paginators/#listeventactionspaginator)
        """

if TYPE_CHECKING:
    _ListJobsPaginatorBase = AioPaginator[ListJobsResponseTypeDef]
else:
    _ListJobsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListJobsPaginator(_ListJobsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange/paginator/ListJobs.html#DataExchange.Paginator.ListJobs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/paginators/#listjobspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListJobsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange/paginator/ListJobs.html#DataExchange.Paginator.ListJobs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/paginators/#listjobspaginator)
        """

if TYPE_CHECKING:
    _ListReceivedDataGrantsPaginatorBase = AioPaginator[ListReceivedDataGrantsResponseTypeDef]
else:
    _ListReceivedDataGrantsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListReceivedDataGrantsPaginator(_ListReceivedDataGrantsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange/paginator/ListReceivedDataGrants.html#DataExchange.Paginator.ListReceivedDataGrants)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/paginators/#listreceiveddatagrantspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListReceivedDataGrantsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListReceivedDataGrantsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange/paginator/ListReceivedDataGrants.html#DataExchange.Paginator.ListReceivedDataGrants.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/paginators/#listreceiveddatagrantspaginator)
        """

if TYPE_CHECKING:
    _ListRevisionAssetsPaginatorBase = AioPaginator[ListRevisionAssetsResponseTypeDef]
else:
    _ListRevisionAssetsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListRevisionAssetsPaginator(_ListRevisionAssetsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange/paginator/ListRevisionAssets.html#DataExchange.Paginator.ListRevisionAssets)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/paginators/#listrevisionassetspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRevisionAssetsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListRevisionAssetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange/paginator/ListRevisionAssets.html#DataExchange.Paginator.ListRevisionAssets.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/paginators/#listrevisionassetspaginator)
        """
