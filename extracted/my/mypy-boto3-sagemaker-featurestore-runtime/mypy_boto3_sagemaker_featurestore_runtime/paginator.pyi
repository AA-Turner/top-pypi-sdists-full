"""
Type annotations for sagemaker-featurestore-runtime service client paginators.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker_featurestore_runtime/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_sagemaker_featurestore_runtime.client import SageMakerFeatureStoreRuntimeClient
    from mypy_boto3_sagemaker_featurestore_runtime.paginator import (
        ListRecordsPaginator,
    )

    session = Session()
    client: SageMakerFeatureStoreRuntimeClient = session.client("sagemaker-featurestore-runtime")

    list_records_paginator: ListRecordsPaginator = client.get_paginator("list_records")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from botocore.paginate import PageIterator, Paginator

from .type_defs import ListRecordsRequestPaginateTypeDef, ListRecordsResponseTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ListRecordsPaginator",)

if TYPE_CHECKING:
    _ListRecordsPaginatorBase = Paginator[ListRecordsResponseTypeDef]
else:
    _ListRecordsPaginatorBase = Paginator  # type: ignore[assignment]

class ListRecordsPaginator(_ListRecordsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-featurestore-runtime/paginator/ListRecords.html#SageMakerFeatureStoreRuntime.Paginator.ListRecords)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker_featurestore_runtime/paginators/#listrecordspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRecordsRequestPaginateTypeDef]
    ) -> PageIterator[ListRecordsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-featurestore-runtime/paginator/ListRecords.html#SageMakerFeatureStoreRuntime.Paginator.ListRecords.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker_featurestore_runtime/paginators/#listrecordspaginator)
        """
