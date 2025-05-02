"""
Type annotations for datapipeline service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datapipeline/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_datapipeline.client import DataPipelineClient
    from types_aiobotocore_datapipeline.paginator import (
        DescribeObjectsPaginator,
        ListPipelinesPaginator,
        QueryObjectsPaginator,
    )

    session = get_session()
    with session.create_client("datapipeline") as client:
        client: DataPipelineClient

        describe_objects_paginator: DescribeObjectsPaginator = client.get_paginator("describe_objects")
        list_pipelines_paginator: ListPipelinesPaginator = client.get_paginator("list_pipelines")
        query_objects_paginator: QueryObjectsPaginator = client.get_paginator("query_objects")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    DescribeObjectsInputPaginateTypeDef,
    DescribeObjectsOutputTypeDef,
    ListPipelinesInputPaginateTypeDef,
    ListPipelinesOutputTypeDef,
    QueryObjectsInputPaginateTypeDef,
    QueryObjectsOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("DescribeObjectsPaginator", "ListPipelinesPaginator", "QueryObjectsPaginator")

if TYPE_CHECKING:
    _DescribeObjectsPaginatorBase = AioPaginator[DescribeObjectsOutputTypeDef]
else:
    _DescribeObjectsPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeObjectsPaginator(_DescribeObjectsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datapipeline/paginator/DescribeObjects.html#DataPipeline.Paginator.DescribeObjects)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datapipeline/paginators/#describeobjectspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeObjectsInputPaginateTypeDef]
    ) -> AioPageIterator[DescribeObjectsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datapipeline/paginator/DescribeObjects.html#DataPipeline.Paginator.DescribeObjects.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datapipeline/paginators/#describeobjectspaginator)
        """

if TYPE_CHECKING:
    _ListPipelinesPaginatorBase = AioPaginator[ListPipelinesOutputTypeDef]
else:
    _ListPipelinesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListPipelinesPaginator(_ListPipelinesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datapipeline/paginator/ListPipelines.html#DataPipeline.Paginator.ListPipelines)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datapipeline/paginators/#listpipelinespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPipelinesInputPaginateTypeDef]
    ) -> AioPageIterator[ListPipelinesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datapipeline/paginator/ListPipelines.html#DataPipeline.Paginator.ListPipelines.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datapipeline/paginators/#listpipelinespaginator)
        """

if TYPE_CHECKING:
    _QueryObjectsPaginatorBase = AioPaginator[QueryObjectsOutputTypeDef]
else:
    _QueryObjectsPaginatorBase = AioPaginator  # type: ignore[assignment]

class QueryObjectsPaginator(_QueryObjectsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datapipeline/paginator/QueryObjects.html#DataPipeline.Paginator.QueryObjects)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datapipeline/paginators/#queryobjectspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[QueryObjectsInputPaginateTypeDef]
    ) -> AioPageIterator[QueryObjectsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datapipeline/paginator/QueryObjects.html#DataPipeline.Paginator.QueryObjects.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datapipeline/paginators/#queryobjectspaginator)
        """
