"""
Type annotations for agent-registry-control service client paginators.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_agent_registry_control/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_agent_registry_control.client import AgentRegistryControlClient
    from mypy_boto3_agent_registry_control.paginator import (
        ListRegistriesPaginator,
        ListRegistryRecordsPaginator,
    )

    session = Session()
    client: AgentRegistryControlClient = session.client("agent-registry-control")

    list_registries_paginator: ListRegistriesPaginator = client.get_paginator("list_registries")
    list_registry_records_paginator: ListRegistryRecordsPaginator = client.get_paginator("list_registry_records")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from botocore.paginate import PageIterator, Paginator

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
    _ListRegistriesPaginatorBase = Paginator[ListRegistriesResponseTypeDef]
else:
    _ListRegistriesPaginatorBase = Paginator  # type: ignore[assignment]

class ListRegistriesPaginator(_ListRegistriesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/agent-registry-control/paginator/ListRegistries.html#AgentRegistryControl.Paginator.ListRegistries)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_agent_registry_control/paginators/#listregistriespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRegistriesRequestPaginateTypeDef]
    ) -> PageIterator[ListRegistriesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/agent-registry-control/paginator/ListRegistries.html#AgentRegistryControl.Paginator.ListRegistries.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_agent_registry_control/paginators/#listregistriespaginator)
        """

if TYPE_CHECKING:
    _ListRegistryRecordsPaginatorBase = Paginator[ListRegistryRecordsResponseTypeDef]
else:
    _ListRegistryRecordsPaginatorBase = Paginator  # type: ignore[assignment]

class ListRegistryRecordsPaginator(_ListRegistryRecordsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/agent-registry-control/paginator/ListRegistryRecords.html#AgentRegistryControl.Paginator.ListRegistryRecords)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_agent_registry_control/paginators/#listregistryrecordspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRegistryRecordsRequestPaginateTypeDef]
    ) -> PageIterator[ListRegistryRecordsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/agent-registry-control/paginator/ListRegistryRecords.html#AgentRegistryControl.Paginator.ListRegistryRecords.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_agent_registry_control/paginators/#listregistryrecordspaginator)
        """
