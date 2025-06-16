"""
Type annotations for dax service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dax/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_dax.client import DAXClient
    from types_aiobotocore_dax.paginator import (
        DescribeClustersPaginator,
        DescribeDefaultParametersPaginator,
        DescribeEventsPaginator,
        DescribeParameterGroupsPaginator,
        DescribeParametersPaginator,
        DescribeSubnetGroupsPaginator,
        ListTagsPaginator,
    )

    session = get_session()
    with session.create_client("dax") as client:
        client: DAXClient

        describe_clusters_paginator: DescribeClustersPaginator = client.get_paginator("describe_clusters")
        describe_default_parameters_paginator: DescribeDefaultParametersPaginator = client.get_paginator("describe_default_parameters")
        describe_events_paginator: DescribeEventsPaginator = client.get_paginator("describe_events")
        describe_parameter_groups_paginator: DescribeParameterGroupsPaginator = client.get_paginator("describe_parameter_groups")
        describe_parameters_paginator: DescribeParametersPaginator = client.get_paginator("describe_parameters")
        describe_subnet_groups_paginator: DescribeSubnetGroupsPaginator = client.get_paginator("describe_subnet_groups")
        list_tags_paginator: ListTagsPaginator = client.get_paginator("list_tags")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    DescribeClustersRequestPaginateTypeDef,
    DescribeClustersResponseTypeDef,
    DescribeDefaultParametersRequestPaginateTypeDef,
    DescribeDefaultParametersResponseTypeDef,
    DescribeEventsRequestPaginateTypeDef,
    DescribeEventsResponseTypeDef,
    DescribeParameterGroupsRequestPaginateTypeDef,
    DescribeParameterGroupsResponseTypeDef,
    DescribeParametersRequestPaginateTypeDef,
    DescribeParametersResponseTypeDef,
    DescribeSubnetGroupsRequestPaginateTypeDef,
    DescribeSubnetGroupsResponseTypeDef,
    ListTagsRequestPaginateTypeDef,
    ListTagsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "DescribeClustersPaginator",
    "DescribeDefaultParametersPaginator",
    "DescribeEventsPaginator",
    "DescribeParameterGroupsPaginator",
    "DescribeParametersPaginator",
    "DescribeSubnetGroupsPaginator",
    "ListTagsPaginator",
)

if TYPE_CHECKING:
    _DescribeClustersPaginatorBase = AioPaginator[DescribeClustersResponseTypeDef]
else:
    _DescribeClustersPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeClustersPaginator(_DescribeClustersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dax/paginator/DescribeClusters.html#DAX.Paginator.DescribeClusters)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dax/paginators/#describeclusterspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeClustersRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeClustersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dax/paginator/DescribeClusters.html#DAX.Paginator.DescribeClusters.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dax/paginators/#describeclusterspaginator)
        """

if TYPE_CHECKING:
    _DescribeDefaultParametersPaginatorBase = AioPaginator[DescribeDefaultParametersResponseTypeDef]
else:
    _DescribeDefaultParametersPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeDefaultParametersPaginator(_DescribeDefaultParametersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dax/paginator/DescribeDefaultParameters.html#DAX.Paginator.DescribeDefaultParameters)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dax/paginators/#describedefaultparameterspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeDefaultParametersRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeDefaultParametersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dax/paginator/DescribeDefaultParameters.html#DAX.Paginator.DescribeDefaultParameters.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dax/paginators/#describedefaultparameterspaginator)
        """

if TYPE_CHECKING:
    _DescribeEventsPaginatorBase = AioPaginator[DescribeEventsResponseTypeDef]
else:
    _DescribeEventsPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeEventsPaginator(_DescribeEventsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dax/paginator/DescribeEvents.html#DAX.Paginator.DescribeEvents)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dax/paginators/#describeeventspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeEventsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeEventsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dax/paginator/DescribeEvents.html#DAX.Paginator.DescribeEvents.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dax/paginators/#describeeventspaginator)
        """

if TYPE_CHECKING:
    _DescribeParameterGroupsPaginatorBase = AioPaginator[DescribeParameterGroupsResponseTypeDef]
else:
    _DescribeParameterGroupsPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeParameterGroupsPaginator(_DescribeParameterGroupsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dax/paginator/DescribeParameterGroups.html#DAX.Paginator.DescribeParameterGroups)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dax/paginators/#describeparametergroupspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeParameterGroupsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeParameterGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dax/paginator/DescribeParameterGroups.html#DAX.Paginator.DescribeParameterGroups.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dax/paginators/#describeparametergroupspaginator)
        """

if TYPE_CHECKING:
    _DescribeParametersPaginatorBase = AioPaginator[DescribeParametersResponseTypeDef]
else:
    _DescribeParametersPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeParametersPaginator(_DescribeParametersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dax/paginator/DescribeParameters.html#DAX.Paginator.DescribeParameters)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dax/paginators/#describeparameterspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeParametersRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeParametersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dax/paginator/DescribeParameters.html#DAX.Paginator.DescribeParameters.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dax/paginators/#describeparameterspaginator)
        """

if TYPE_CHECKING:
    _DescribeSubnetGroupsPaginatorBase = AioPaginator[DescribeSubnetGroupsResponseTypeDef]
else:
    _DescribeSubnetGroupsPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeSubnetGroupsPaginator(_DescribeSubnetGroupsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dax/paginator/DescribeSubnetGroups.html#DAX.Paginator.DescribeSubnetGroups)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dax/paginators/#describesubnetgroupspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeSubnetGroupsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeSubnetGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dax/paginator/DescribeSubnetGroups.html#DAX.Paginator.DescribeSubnetGroups.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dax/paginators/#describesubnetgroupspaginator)
        """

if TYPE_CHECKING:
    _ListTagsPaginatorBase = AioPaginator[ListTagsResponseTypeDef]
else:
    _ListTagsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListTagsPaginator(_ListTagsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dax/paginator/ListTags.html#DAX.Paginator.ListTags)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dax/paginators/#listtagspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTagsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListTagsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dax/paginator/ListTags.html#DAX.Paginator.ListTags.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dax/paginators/#listtagspaginator)
        """
