"""
Type annotations for efs service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_efs/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_efs.client import EFSClient
    from types_aiobotocore_efs.paginator import (
        DescribeAccessPointsPaginator,
        DescribeFileSystemsPaginator,
        DescribeMountTargetsPaginator,
        DescribeReplicationConfigurationsPaginator,
        DescribeTagsPaginator,
    )

    session = get_session()
    with session.create_client("efs") as client:
        client: EFSClient

        describe_access_points_paginator: DescribeAccessPointsPaginator = client.get_paginator("describe_access_points")
        describe_file_systems_paginator: DescribeFileSystemsPaginator = client.get_paginator("describe_file_systems")
        describe_mount_targets_paginator: DescribeMountTargetsPaginator = client.get_paginator("describe_mount_targets")
        describe_replication_configurations_paginator: DescribeReplicationConfigurationsPaginator = client.get_paginator("describe_replication_configurations")
        describe_tags_paginator: DescribeTagsPaginator = client.get_paginator("describe_tags")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    DescribeAccessPointsRequestPaginateTypeDef,
    DescribeAccessPointsResponseTypeDef,
    DescribeFileSystemsRequestPaginateTypeDef,
    DescribeFileSystemsResponseTypeDef,
    DescribeMountTargetsRequestPaginateTypeDef,
    DescribeMountTargetsResponseTypeDef,
    DescribeReplicationConfigurationsRequestPaginateTypeDef,
    DescribeReplicationConfigurationsResponseTypeDef,
    DescribeTagsRequestPaginateTypeDef,
    DescribeTagsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "DescribeAccessPointsPaginator",
    "DescribeFileSystemsPaginator",
    "DescribeMountTargetsPaginator",
    "DescribeReplicationConfigurationsPaginator",
    "DescribeTagsPaginator",
)

if TYPE_CHECKING:
    _DescribeAccessPointsPaginatorBase = AioPaginator[DescribeAccessPointsResponseTypeDef]
else:
    _DescribeAccessPointsPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeAccessPointsPaginator(_DescribeAccessPointsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/efs/paginator/DescribeAccessPoints.html#EFS.Paginator.DescribeAccessPoints)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_efs/paginators/#describeaccesspointspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeAccessPointsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeAccessPointsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/efs/paginator/DescribeAccessPoints.html#EFS.Paginator.DescribeAccessPoints.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_efs/paginators/#describeaccesspointspaginator)
        """

if TYPE_CHECKING:
    _DescribeFileSystemsPaginatorBase = AioPaginator[DescribeFileSystemsResponseTypeDef]
else:
    _DescribeFileSystemsPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeFileSystemsPaginator(_DescribeFileSystemsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/efs/paginator/DescribeFileSystems.html#EFS.Paginator.DescribeFileSystems)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_efs/paginators/#describefilesystemspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeFileSystemsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeFileSystemsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/efs/paginator/DescribeFileSystems.html#EFS.Paginator.DescribeFileSystems.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_efs/paginators/#describefilesystemspaginator)
        """

if TYPE_CHECKING:
    _DescribeMountTargetsPaginatorBase = AioPaginator[DescribeMountTargetsResponseTypeDef]
else:
    _DescribeMountTargetsPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeMountTargetsPaginator(_DescribeMountTargetsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/efs/paginator/DescribeMountTargets.html#EFS.Paginator.DescribeMountTargets)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_efs/paginators/#describemounttargetspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeMountTargetsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeMountTargetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/efs/paginator/DescribeMountTargets.html#EFS.Paginator.DescribeMountTargets.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_efs/paginators/#describemounttargetspaginator)
        """

if TYPE_CHECKING:
    _DescribeReplicationConfigurationsPaginatorBase = AioPaginator[
        DescribeReplicationConfigurationsResponseTypeDef
    ]
else:
    _DescribeReplicationConfigurationsPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeReplicationConfigurationsPaginator(_DescribeReplicationConfigurationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/efs/paginator/DescribeReplicationConfigurations.html#EFS.Paginator.DescribeReplicationConfigurations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_efs/paginators/#describereplicationconfigurationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeReplicationConfigurationsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeReplicationConfigurationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/efs/paginator/DescribeReplicationConfigurations.html#EFS.Paginator.DescribeReplicationConfigurations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_efs/paginators/#describereplicationconfigurationspaginator)
        """

if TYPE_CHECKING:
    _DescribeTagsPaginatorBase = AioPaginator[DescribeTagsResponseTypeDef]
else:
    _DescribeTagsPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeTagsPaginator(_DescribeTagsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/efs/paginator/DescribeTags.html#EFS.Paginator.DescribeTags)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_efs/paginators/#describetagspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeTagsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeTagsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/efs/paginator/DescribeTags.html#EFS.Paginator.DescribeTags.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_efs/paginators/#describetagspaginator)
        """
