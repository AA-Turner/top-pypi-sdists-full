"""
Type annotations for elastic-inference service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elastic_inference/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_elastic_inference.client import ElasticInferenceClient
    from types_aiobotocore_elastic_inference.paginator import (
        DescribeAcceleratorsPaginator,
    )

    session = get_session()
    with session.create_client("elastic-inference") as client:
        client: ElasticInferenceClient

        describe_accelerators_paginator: DescribeAcceleratorsPaginator = client.get_paginator("describe_accelerators")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    DescribeAcceleratorsRequestPaginateTypeDef,
    DescribeAcceleratorsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("DescribeAcceleratorsPaginator",)


if TYPE_CHECKING:
    _DescribeAcceleratorsPaginatorBase = AioPaginator[DescribeAcceleratorsResponseTypeDef]
else:
    _DescribeAcceleratorsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeAcceleratorsPaginator(_DescribeAcceleratorsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastic-inference/paginator/DescribeAccelerators.html#ElasticInference.Paginator.DescribeAccelerators)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elastic_inference/paginators/#describeacceleratorspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeAcceleratorsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeAcceleratorsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastic-inference/paginator/DescribeAccelerators.html#ElasticInference.Paginator.DescribeAccelerators.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elastic_inference/paginators/#describeacceleratorspaginator)
        """
