"""
Type annotations for cur service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cur/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_cur.client import CostandUsageReportServiceClient
    from types_aiobotocore_cur.paginator import (
        DescribeReportDefinitionsPaginator,
    )

    session = get_session()
    with session.create_client("cur") as client:
        client: CostandUsageReportServiceClient

        describe_report_definitions_paginator: DescribeReportDefinitionsPaginator = client.get_paginator("describe_report_definitions")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    DescribeReportDefinitionsRequestPaginateTypeDef,
    DescribeReportDefinitionsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("DescribeReportDefinitionsPaginator",)


if TYPE_CHECKING:
    _DescribeReportDefinitionsPaginatorBase = AioPaginator[DescribeReportDefinitionsResponseTypeDef]
else:
    _DescribeReportDefinitionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeReportDefinitionsPaginator(_DescribeReportDefinitionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cur/paginator/DescribeReportDefinitions.html#CostandUsageReportService.Paginator.DescribeReportDefinitions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cur/paginators/#describereportdefinitionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeReportDefinitionsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeReportDefinitionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cur/paginator/DescribeReportDefinitions.html#CostandUsageReportService.Paginator.DescribeReportDefinitions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cur/paginators/#describereportdefinitionspaginator)
        """
