"""
Type annotations for cloudhsmv2 service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsmv2/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_cloudhsmv2.client import CloudHSMV2Client
    from types_aiobotocore_cloudhsmv2.paginator import (
        DescribeBackupsPaginator,
        DescribeClustersPaginator,
        ListTagsPaginator,
    )

    session = get_session()
    with session.create_client("cloudhsmv2") as client:
        client: CloudHSMV2Client

        describe_backups_paginator: DescribeBackupsPaginator = client.get_paginator("describe_backups")
        describe_clusters_paginator: DescribeClustersPaginator = client.get_paginator("describe_clusters")
        list_tags_paginator: ListTagsPaginator = client.get_paginator("list_tags")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    DescribeBackupsRequestPaginateTypeDef,
    DescribeBackupsResponseTypeDef,
    DescribeClustersRequestPaginateTypeDef,
    DescribeClustersResponseTypeDef,
    ListTagsRequestPaginateTypeDef,
    ListTagsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("DescribeBackupsPaginator", "DescribeClustersPaginator", "ListTagsPaginator")


if TYPE_CHECKING:
    _DescribeBackupsPaginatorBase = AioPaginator[DescribeBackupsResponseTypeDef]
else:
    _DescribeBackupsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeBackupsPaginator(_DescribeBackupsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsmv2/paginator/DescribeBackups.html#CloudHSMV2.Paginator.DescribeBackups)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsmv2/paginators/#describebackupspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeBackupsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeBackupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsmv2/paginator/DescribeBackups.html#CloudHSMV2.Paginator.DescribeBackups.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsmv2/paginators/#describebackupspaginator)
        """


if TYPE_CHECKING:
    _DescribeClustersPaginatorBase = AioPaginator[DescribeClustersResponseTypeDef]
else:
    _DescribeClustersPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeClustersPaginator(_DescribeClustersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsmv2/paginator/DescribeClusters.html#CloudHSMV2.Paginator.DescribeClusters)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsmv2/paginators/#describeclusterspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeClustersRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeClustersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsmv2/paginator/DescribeClusters.html#CloudHSMV2.Paginator.DescribeClusters.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsmv2/paginators/#describeclusterspaginator)
        """


if TYPE_CHECKING:
    _ListTagsPaginatorBase = AioPaginator[ListTagsResponseTypeDef]
else:
    _ListTagsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListTagsPaginator(_ListTagsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsmv2/paginator/ListTags.html#CloudHSMV2.Paginator.ListTags)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsmv2/paginators/#listtagspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTagsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListTagsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsmv2/paginator/ListTags.html#CloudHSMV2.Paginator.ListTags.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsmv2/paginators/#listtagspaginator)
        """
