"""
Type annotations for opensearchserverless service client paginators.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opensearchserverless/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_opensearchserverless.client import OpenSearchServiceServerlessClient
    from mypy_boto3_opensearchserverless.paginator import (
        ListIngestionJobsPaginator,
        ListIngestionStreamsPaginator,
    )

    session = Session()
    client: OpenSearchServiceServerlessClient = session.client("opensearchserverless")

    list_ingestion_jobs_paginator: ListIngestionJobsPaginator = client.get_paginator("list_ingestion_jobs")
    list_ingestion_streams_paginator: ListIngestionStreamsPaginator = client.get_paginator("list_ingestion_streams")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListIngestionJobsRequestPaginateTypeDef,
    ListIngestionJobsResponseTypeDef,
    ListIngestionStreamsRequestPaginateTypeDef,
    ListIngestionStreamsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ListIngestionJobsPaginator", "ListIngestionStreamsPaginator")

if TYPE_CHECKING:
    _ListIngestionJobsPaginatorBase = Paginator[ListIngestionJobsResponseTypeDef]
else:
    _ListIngestionJobsPaginatorBase = Paginator  # type: ignore[assignment]

class ListIngestionJobsPaginator(_ListIngestionJobsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchserverless/paginator/ListIngestionJobs.html#OpenSearchServiceServerless.Paginator.ListIngestionJobs)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opensearchserverless/paginators/#listingestionjobspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListIngestionJobsRequestPaginateTypeDef]
    ) -> PageIterator[ListIngestionJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchserverless/paginator/ListIngestionJobs.html#OpenSearchServiceServerless.Paginator.ListIngestionJobs.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opensearchserverless/paginators/#listingestionjobspaginator)
        """

if TYPE_CHECKING:
    _ListIngestionStreamsPaginatorBase = Paginator[ListIngestionStreamsResponseTypeDef]
else:
    _ListIngestionStreamsPaginatorBase = Paginator  # type: ignore[assignment]

class ListIngestionStreamsPaginator(_ListIngestionStreamsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchserverless/paginator/ListIngestionStreams.html#OpenSearchServiceServerless.Paginator.ListIngestionStreams)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opensearchserverless/paginators/#listingestionstreamspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListIngestionStreamsRequestPaginateTypeDef]
    ) -> PageIterator[ListIngestionStreamsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchserverless/paginator/ListIngestionStreams.html#OpenSearchServiceServerless.Paginator.ListIngestionStreams.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opensearchserverless/paginators/#listingestionstreamspaginator)
        """
