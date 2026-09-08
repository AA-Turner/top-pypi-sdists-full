"""
Type annotations for agent-registry-control service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_agent_registry_control/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_agent_registry_control.client import AgentRegistryControlClient
    from types_aiobotocore_agent_registry_control.paginator import (
        ListRegistriesPaginator,
        ListRegistryRecordsPaginator,
    )

    session = get_session()
    with session.create_client("agent-registry-control") as client:
        client: AgentRegistryControlClient

        list_registries_paginator: ListRegistriesPaginator = client.get_paginator("list_registries")
        list_registry_records_paginator: ListRegistryRecordsPaginator = client.get_paginator("list_registry_records")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListRegistriesRequestPaginateTypeDef,
    ListRegistriesResponseTypeDef,
    ListRegistryRecordsRequestPaginateTypeDef,
    ListRegistryRecordsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ListRegistriesPaginator", "ListRegistryRecordsPaginator")

if TYPE_CHECKING:
    _ListRegistriesPaginatorBase = AioPaginator[ListRegistriesResponseTypeDef]
else:
    _ListRegistriesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListRegistriesPaginator(_ListRegistriesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/agent-registry-control/paginator/ListRegistries.html#AgentRegistryControl.Paginator.ListRegistries)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_agent_registry_control/paginators/#listregistriespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRegistriesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListRegistriesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/agent-registry-control/paginator/ListRegistries.html#AgentRegistryControl.Paginator.ListRegistries.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_agent_registry_control/paginators/#listregistriespaginator)
        """

if TYPE_CHECKING:
    _ListRegistryRecordsPaginatorBase = AioPaginator[ListRegistryRecordsResponseTypeDef]
else:
    _ListRegistryRecordsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListRegistryRecordsPaginator(_ListRegistryRecordsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/agent-registry-control/paginator/ListRegistryRecords.html#AgentRegistryControl.Paginator.ListRegistryRecords)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_agent_registry_control/paginators/#listregistryrecordspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRegistryRecordsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListRegistryRecordsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/agent-registry-control/paginator/ListRegistryRecords.html#AgentRegistryControl.Paginator.ListRegistryRecords.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_agent_registry_control/paginators/#listregistryrecordspaginator)
        """
