"""
Type annotations for agent-discovery service client paginators.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_agent_discovery/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from types_boto3_agent_discovery.client import AgentDiscoveryClient
    from types_boto3_agent_discovery.paginator import (
        SearchPublicRecordsPaginator,
    )

    session = Session()
    client: AgentDiscoveryClient = session.client("agent-discovery")

    search_public_records_paginator: SearchPublicRecordsPaginator = client.get_paginator("search_public_records")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    SearchPublicRecordsRequestPaginateTypeDef,
    SearchPublicRecordsResponsePaginatorTypeDef,
    SearchPublicRecordsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("SearchPublicRecordsPaginator",)


if TYPE_CHECKING:
    _SearchPublicRecordsPaginatorBase = Paginator[SearchPublicRecordsResponseTypeDef]
else:
    _SearchPublicRecordsPaginatorBase = Paginator  # type: ignore[assignment]


class SearchPublicRecordsPaginator(_SearchPublicRecordsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/agent-discovery/paginator/SearchPublicRecords.html#AgentDiscovery.Paginator.SearchPublicRecords)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_agent_discovery/paginators/#searchpublicrecordspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[SearchPublicRecordsRequestPaginateTypeDef]
    ) -> PageIterator[SearchPublicRecordsResponsePaginatorTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/agent-discovery/paginator/SearchPublicRecords.html#AgentDiscovery.Paginator.SearchPublicRecords.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_agent_discovery/paginators/#searchpublicrecordspaginator)
        """
