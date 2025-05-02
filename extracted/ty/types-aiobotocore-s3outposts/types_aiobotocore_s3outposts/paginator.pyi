"""
Type annotations for s3outposts service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3outposts/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_s3outposts.client import S3OutpostsClient
    from types_aiobotocore_s3outposts.paginator import (
        ListEndpointsPaginator,
        ListOutpostsWithS3Paginator,
        ListSharedEndpointsPaginator,
    )

    session = get_session()
    with session.create_client("s3outposts") as client:
        client: S3OutpostsClient

        list_endpoints_paginator: ListEndpointsPaginator = client.get_paginator("list_endpoints")
        list_outposts_with_s3_paginator: ListOutpostsWithS3Paginator = client.get_paginator("list_outposts_with_s3")
        list_shared_endpoints_paginator: ListSharedEndpointsPaginator = client.get_paginator("list_shared_endpoints")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListEndpointsRequestPaginateTypeDef,
    ListEndpointsResultTypeDef,
    ListOutpostsWithS3RequestPaginateTypeDef,
    ListOutpostsWithS3ResultTypeDef,
    ListSharedEndpointsRequestPaginateTypeDef,
    ListSharedEndpointsResultTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ListEndpointsPaginator", "ListOutpostsWithS3Paginator", "ListSharedEndpointsPaginator")

if TYPE_CHECKING:
    _ListEndpointsPaginatorBase = AioPaginator[ListEndpointsResultTypeDef]
else:
    _ListEndpointsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListEndpointsPaginator(_ListEndpointsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3outposts/paginator/ListEndpoints.html#S3Outposts.Paginator.ListEndpoints)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3outposts/paginators/#listendpointspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListEndpointsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListEndpointsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3outposts/paginator/ListEndpoints.html#S3Outposts.Paginator.ListEndpoints.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3outposts/paginators/#listendpointspaginator)
        """

if TYPE_CHECKING:
    _ListOutpostsWithS3PaginatorBase = AioPaginator[ListOutpostsWithS3ResultTypeDef]
else:
    _ListOutpostsWithS3PaginatorBase = AioPaginator  # type: ignore[assignment]

class ListOutpostsWithS3Paginator(_ListOutpostsWithS3PaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3outposts/paginator/ListOutpostsWithS3.html#S3Outposts.Paginator.ListOutpostsWithS3)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3outposts/paginators/#listoutpostswiths3paginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListOutpostsWithS3RequestPaginateTypeDef]
    ) -> AioPageIterator[ListOutpostsWithS3ResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3outposts/paginator/ListOutpostsWithS3.html#S3Outposts.Paginator.ListOutpostsWithS3.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3outposts/paginators/#listoutpostswiths3paginator)
        """

if TYPE_CHECKING:
    _ListSharedEndpointsPaginatorBase = AioPaginator[ListSharedEndpointsResultTypeDef]
else:
    _ListSharedEndpointsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListSharedEndpointsPaginator(_ListSharedEndpointsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3outposts/paginator/ListSharedEndpoints.html#S3Outposts.Paginator.ListSharedEndpoints)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3outposts/paginators/#listsharedendpointspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSharedEndpointsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListSharedEndpointsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3outposts/paginator/ListSharedEndpoints.html#S3Outposts.Paginator.ListSharedEndpoints.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3outposts/paginators/#listsharedendpointspaginator)
        """
