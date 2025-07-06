"""
Type annotations for opensearch service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_opensearch.client import OpenSearchServiceClient
    from types_aiobotocore_opensearch.paginator import (
        ListApplicationsPaginator,
    )

    session = get_session()
    with session.create_client("opensearch") as client:
        client: OpenSearchServiceClient

        list_applications_paginator: ListApplicationsPaginator = client.get_paginator("list_applications")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import ListApplicationsRequestPaginateTypeDef, ListApplicationsResponseTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ListApplicationsPaginator",)

if TYPE_CHECKING:
    _ListApplicationsPaginatorBase = AioPaginator[ListApplicationsResponseTypeDef]
else:
    _ListApplicationsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListApplicationsPaginator(_ListApplicationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch/paginator/ListApplications.html#OpenSearchService.Paginator.ListApplications)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/paginators/#listapplicationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListApplicationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListApplicationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch/paginator/ListApplications.html#OpenSearchService.Paginator.ListApplications.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/paginators/#listapplicationspaginator)
        """
