"""
Type annotations for sagemaker-featurestore-runtime service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker_featurestore_runtime/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_sagemaker_featurestore_runtime.client import SageMakerFeatureStoreRuntimeClient
    from types_aiobotocore_sagemaker_featurestore_runtime.paginator import (
        ListRecordsPaginator,
    )

    session = get_session()
    with session.create_client("sagemaker-featurestore-runtime") as client:
        client: SageMakerFeatureStoreRuntimeClient

        list_records_paginator: ListRecordsPaginator = client.get_paginator("list_records")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import ListRecordsRequestPaginateTypeDef, ListRecordsResponseTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ListRecordsPaginator",)


if TYPE_CHECKING:
    _ListRecordsPaginatorBase = AioPaginator[ListRecordsResponseTypeDef]
else:
    _ListRecordsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListRecordsPaginator(_ListRecordsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-featurestore-runtime/paginator/ListRecords.html#SageMakerFeatureStoreRuntime.Paginator.ListRecords)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker_featurestore_runtime/paginators/#listrecordspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRecordsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListRecordsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-featurestore-runtime/paginator/ListRecords.html#SageMakerFeatureStoreRuntime.Paginator.ListRecords.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker_featurestore_runtime/paginators/#listrecordspaginator)
        """
