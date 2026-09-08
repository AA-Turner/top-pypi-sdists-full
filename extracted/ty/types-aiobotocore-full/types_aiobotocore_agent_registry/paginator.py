"""
Type annotations for agent-registry service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_agent_registry/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_agent_registry.client import AgentRegistryClient
    from types_aiobotocore_agent_registry.paginator import (
        ListDiscoverableRegistryRecordsPaginator,
    )

    session = get_session()
    with session.create_client("agent-registry") as client:
        client: AgentRegistryClient

        list_discoverable_registry_records_paginator: ListDiscoverableRegistryRecordsPaginator = client.get_paginator("list_discoverable_registry_records")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

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
    _ListDiscoverableRegistryRecordsPaginatorBase = AioPaginator[
        ListDiscoverableRegistryRecordsResponseTypeDef
    ]
else:
    _ListDiscoverableRegistryRecordsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListDiscoverableRegistryRecordsPaginator(_ListDiscoverableRegistryRecordsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/agent-registry/paginator/ListDiscoverableRegistryRecords.html#AgentRegistry.Paginator.ListDiscoverableRegistryRecords)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_agent_registry/paginators/#listdiscoverableregistryrecordspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDiscoverableRegistryRecordsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListDiscoverableRegistryRecordsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/agent-registry/paginator/ListDiscoverableRegistryRecords.html#AgentRegistry.Paginator.ListDiscoverableRegistryRecords.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_agent_registry/paginators/#listdiscoverableregistryrecordspaginator)
        """
