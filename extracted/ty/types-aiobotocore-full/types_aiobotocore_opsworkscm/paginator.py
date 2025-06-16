"""
Type annotations for opsworkscm service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworkscm/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_opsworkscm.client import OpsWorksCMClient
    from types_aiobotocore_opsworkscm.paginator import (
        DescribeBackupsPaginator,
        DescribeEventsPaginator,
        DescribeServersPaginator,
        ListTagsForResourcePaginator,
    )

    session = get_session()
    with session.create_client("opsworkscm") as client:
        client: OpsWorksCMClient

        describe_backups_paginator: DescribeBackupsPaginator = client.get_paginator("describe_backups")
        describe_events_paginator: DescribeEventsPaginator = client.get_paginator("describe_events")
        describe_servers_paginator: DescribeServersPaginator = client.get_paginator("describe_servers")
        list_tags_for_resource_paginator: ListTagsForResourcePaginator = client.get_paginator("list_tags_for_resource")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    DescribeBackupsRequestPaginateTypeDef,
    DescribeBackupsResponseTypeDef,
    DescribeEventsRequestPaginateTypeDef,
    DescribeEventsResponseTypeDef,
    DescribeServersRequestPaginateTypeDef,
    DescribeServersResponseTypeDef,
    ListTagsForResourceRequestPaginateTypeDef,
    ListTagsForResourceResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "DescribeBackupsPaginator",
    "DescribeEventsPaginator",
    "DescribeServersPaginator",
    "ListTagsForResourcePaginator",
)


if TYPE_CHECKING:
    _DescribeBackupsPaginatorBase = AioPaginator[DescribeBackupsResponseTypeDef]
else:
    _DescribeBackupsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeBackupsPaginator(_DescribeBackupsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworkscm/paginator/DescribeBackups.html#OpsWorksCM.Paginator.DescribeBackups)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworkscm/paginators/#describebackupspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeBackupsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeBackupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworkscm/paginator/DescribeBackups.html#OpsWorksCM.Paginator.DescribeBackups.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworkscm/paginators/#describebackupspaginator)
        """


if TYPE_CHECKING:
    _DescribeEventsPaginatorBase = AioPaginator[DescribeEventsResponseTypeDef]
else:
    _DescribeEventsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeEventsPaginator(_DescribeEventsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworkscm/paginator/DescribeEvents.html#OpsWorksCM.Paginator.DescribeEvents)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworkscm/paginators/#describeeventspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeEventsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeEventsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworkscm/paginator/DescribeEvents.html#OpsWorksCM.Paginator.DescribeEvents.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworkscm/paginators/#describeeventspaginator)
        """


if TYPE_CHECKING:
    _DescribeServersPaginatorBase = AioPaginator[DescribeServersResponseTypeDef]
else:
    _DescribeServersPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeServersPaginator(_DescribeServersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworkscm/paginator/DescribeServers.html#OpsWorksCM.Paginator.DescribeServers)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworkscm/paginators/#describeserverspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeServersRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeServersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworkscm/paginator/DescribeServers.html#OpsWorksCM.Paginator.DescribeServers.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworkscm/paginators/#describeserverspaginator)
        """


if TYPE_CHECKING:
    _ListTagsForResourcePaginatorBase = AioPaginator[ListTagsForResourceResponseTypeDef]
else:
    _ListTagsForResourcePaginatorBase = AioPaginator  # type: ignore[assignment]


class ListTagsForResourcePaginator(_ListTagsForResourcePaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworkscm/paginator/ListTagsForResource.html#OpsWorksCM.Paginator.ListTagsForResource)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworkscm/paginators/#listtagsforresourcepaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTagsForResourceRequestPaginateTypeDef]
    ) -> AioPageIterator[ListTagsForResourceResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworkscm/paginator/ListTagsForResource.html#OpsWorksCM.Paginator.ListTagsForResource.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworkscm/paginators/#listtagsforresourcepaginator)
        """
