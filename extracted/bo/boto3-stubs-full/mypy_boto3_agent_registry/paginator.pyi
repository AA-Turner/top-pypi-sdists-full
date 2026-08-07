"""
Type annotations for agent-registry service client paginators.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_agent_registry/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_agent_registry.client import AgentRegistryClient
    from mypy_boto3_agent_registry.paginator import (
        ListDiscoverableRegistryRecordsPaginator,
    )

    session = Session()
    client: AgentRegistryClient = session.client("agent-registry")

    list_discoverable_registry_records_paginator: ListDiscoverableRegistryRecordsPaginator = client.get_paginator("list_discoverable_registry_records")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListDiscoverableRegistryRecordsRequestPaginateTypeDef,
    ListDiscoverableRegistryRecordsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ListDiscoverableRegistryRecordsPaginator",)

if TYPE_CHECKING:
    _ListDiscoverableRegistryRecordsPaginatorBase = Paginator[
        ListDiscoverableRegistryRecordsResponseTypeDef
    ]
else:
    _ListDiscoverableRegistryRecordsPaginatorBase = Paginator  # type: ignore[assignment]

class ListDiscoverableRegistryRecordsPaginator(_ListDiscoverableRegistryRecordsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/agent-registry/paginator/ListDiscoverableRegistryRecords.html#AgentRegistry.Paginator.ListDiscoverableRegistryRecords)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_agent_registry/paginators/#listdiscoverableregistryrecordspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDiscoverableRegistryRecordsRequestPaginateTypeDef]
    ) -> PageIterator[ListDiscoverableRegistryRecordsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/agent-registry/paginator/ListDiscoverableRegistryRecords.html#AgentRegistry.Paginator.ListDiscoverableRegistryRecords.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_agent_registry/paginators/#listdiscoverableregistryrecordspaginator)
        """
