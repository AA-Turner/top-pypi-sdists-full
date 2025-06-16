"""
Type annotations for braket service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_braket/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_braket.client import BraketClient
    from types_aiobotocore_braket.paginator import (
        SearchDevicesPaginator,
        SearchJobsPaginator,
        SearchQuantumTasksPaginator,
    )

    session = get_session()
    with session.create_client("braket") as client:
        client: BraketClient

        search_devices_paginator: SearchDevicesPaginator = client.get_paginator("search_devices")
        search_jobs_paginator: SearchJobsPaginator = client.get_paginator("search_jobs")
        search_quantum_tasks_paginator: SearchQuantumTasksPaginator = client.get_paginator("search_quantum_tasks")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    SearchDevicesRequestPaginateTypeDef,
    SearchDevicesResponseTypeDef,
    SearchJobsRequestPaginateTypeDef,
    SearchJobsResponseTypeDef,
    SearchQuantumTasksRequestPaginateTypeDef,
    SearchQuantumTasksResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("SearchDevicesPaginator", "SearchJobsPaginator", "SearchQuantumTasksPaginator")

if TYPE_CHECKING:
    _SearchDevicesPaginatorBase = AioPaginator[SearchDevicesResponseTypeDef]
else:
    _SearchDevicesPaginatorBase = AioPaginator  # type: ignore[assignment]

class SearchDevicesPaginator(_SearchDevicesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/braket/paginator/SearchDevices.html#Braket.Paginator.SearchDevices)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_braket/paginators/#searchdevicespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[SearchDevicesRequestPaginateTypeDef]
    ) -> AioPageIterator[SearchDevicesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/braket/paginator/SearchDevices.html#Braket.Paginator.SearchDevices.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_braket/paginators/#searchdevicespaginator)
        """

if TYPE_CHECKING:
    _SearchJobsPaginatorBase = AioPaginator[SearchJobsResponseTypeDef]
else:
    _SearchJobsPaginatorBase = AioPaginator  # type: ignore[assignment]

class SearchJobsPaginator(_SearchJobsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/braket/paginator/SearchJobs.html#Braket.Paginator.SearchJobs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_braket/paginators/#searchjobspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[SearchJobsRequestPaginateTypeDef]
    ) -> AioPageIterator[SearchJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/braket/paginator/SearchJobs.html#Braket.Paginator.SearchJobs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_braket/paginators/#searchjobspaginator)
        """

if TYPE_CHECKING:
    _SearchQuantumTasksPaginatorBase = AioPaginator[SearchQuantumTasksResponseTypeDef]
else:
    _SearchQuantumTasksPaginatorBase = AioPaginator  # type: ignore[assignment]

class SearchQuantumTasksPaginator(_SearchQuantumTasksPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/braket/paginator/SearchQuantumTasks.html#Braket.Paginator.SearchQuantumTasks)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_braket/paginators/#searchquantumtaskspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[SearchQuantumTasksRequestPaginateTypeDef]
    ) -> AioPageIterator[SearchQuantumTasksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/braket/paginator/SearchQuantumTasks.html#Braket.Paginator.SearchQuantumTasks.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_braket/paginators/#searchquantumtaskspaginator)
        """
