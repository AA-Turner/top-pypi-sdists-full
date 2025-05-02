"""
Type annotations for sms service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sms/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_sms.client import SMSClient
    from types_aiobotocore_sms.paginator import (
        GetConnectorsPaginator,
        GetReplicationJobsPaginator,
        GetReplicationRunsPaginator,
        GetServersPaginator,
        ListAppsPaginator,
    )

    session = get_session()
    with session.create_client("sms") as client:
        client: SMSClient

        get_connectors_paginator: GetConnectorsPaginator = client.get_paginator("get_connectors")
        get_replication_jobs_paginator: GetReplicationJobsPaginator = client.get_paginator("get_replication_jobs")
        get_replication_runs_paginator: GetReplicationRunsPaginator = client.get_paginator("get_replication_runs")
        get_servers_paginator: GetServersPaginator = client.get_paginator("get_servers")
        list_apps_paginator: ListAppsPaginator = client.get_paginator("list_apps")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    GetConnectorsRequestPaginateTypeDef,
    GetConnectorsResponseTypeDef,
    GetReplicationJobsRequestPaginateTypeDef,
    GetReplicationJobsResponseTypeDef,
    GetReplicationRunsRequestPaginateTypeDef,
    GetReplicationRunsResponseTypeDef,
    GetServersRequestPaginateTypeDef,
    GetServersResponseTypeDef,
    ListAppsRequestPaginateTypeDef,
    ListAppsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "GetConnectorsPaginator",
    "GetReplicationJobsPaginator",
    "GetReplicationRunsPaginator",
    "GetServersPaginator",
    "ListAppsPaginator",
)

if TYPE_CHECKING:
    _GetConnectorsPaginatorBase = AioPaginator[GetConnectorsResponseTypeDef]
else:
    _GetConnectorsPaginatorBase = AioPaginator  # type: ignore[assignment]

class GetConnectorsPaginator(_GetConnectorsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/paginator/GetConnectors.html#SMS.Paginator.GetConnectors)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sms/paginators/#getconnectorspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetConnectorsRequestPaginateTypeDef]
    ) -> AioPageIterator[GetConnectorsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/paginator/GetConnectors.html#SMS.Paginator.GetConnectors.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sms/paginators/#getconnectorspaginator)
        """

if TYPE_CHECKING:
    _GetReplicationJobsPaginatorBase = AioPaginator[GetReplicationJobsResponseTypeDef]
else:
    _GetReplicationJobsPaginatorBase = AioPaginator  # type: ignore[assignment]

class GetReplicationJobsPaginator(_GetReplicationJobsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/paginator/GetReplicationJobs.html#SMS.Paginator.GetReplicationJobs)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sms/paginators/#getreplicationjobspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetReplicationJobsRequestPaginateTypeDef]
    ) -> AioPageIterator[GetReplicationJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/paginator/GetReplicationJobs.html#SMS.Paginator.GetReplicationJobs.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sms/paginators/#getreplicationjobspaginator)
        """

if TYPE_CHECKING:
    _GetReplicationRunsPaginatorBase = AioPaginator[GetReplicationRunsResponseTypeDef]
else:
    _GetReplicationRunsPaginatorBase = AioPaginator  # type: ignore[assignment]

class GetReplicationRunsPaginator(_GetReplicationRunsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/paginator/GetReplicationRuns.html#SMS.Paginator.GetReplicationRuns)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sms/paginators/#getreplicationrunspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetReplicationRunsRequestPaginateTypeDef]
    ) -> AioPageIterator[GetReplicationRunsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/paginator/GetReplicationRuns.html#SMS.Paginator.GetReplicationRuns.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sms/paginators/#getreplicationrunspaginator)
        """

if TYPE_CHECKING:
    _GetServersPaginatorBase = AioPaginator[GetServersResponseTypeDef]
else:
    _GetServersPaginatorBase = AioPaginator  # type: ignore[assignment]

class GetServersPaginator(_GetServersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/paginator/GetServers.html#SMS.Paginator.GetServers)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sms/paginators/#getserverspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetServersRequestPaginateTypeDef]
    ) -> AioPageIterator[GetServersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/paginator/GetServers.html#SMS.Paginator.GetServers.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sms/paginators/#getserverspaginator)
        """

if TYPE_CHECKING:
    _ListAppsPaginatorBase = AioPaginator[ListAppsResponseTypeDef]
else:
    _ListAppsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListAppsPaginator(_ListAppsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/paginator/ListApps.html#SMS.Paginator.ListApps)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sms/paginators/#listappspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAppsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAppsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/paginator/ListApps.html#SMS.Paginator.ListApps.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sms/paginators/#listappspaginator)
        """
