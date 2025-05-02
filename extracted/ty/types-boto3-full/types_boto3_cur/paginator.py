"""
Type annotations for cur service client paginators.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cur/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from types_boto3_cur.client import CostandUsageReportServiceClient
    from types_boto3_cur.paginator import (
        DescribeReportDefinitionsPaginator,
    )

    session = Session()
    client: CostandUsageReportServiceClient = session.client("cur")

    describe_report_definitions_paginator: DescribeReportDefinitionsPaginator = client.get_paginator("describe_report_definitions")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from botocore.paginate import PageIterator, Paginator

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
    _DescribeReportDefinitionsPaginatorBase = Paginator[DescribeReportDefinitionsResponseTypeDef]
else:
    _DescribeReportDefinitionsPaginatorBase = Paginator  # type: ignore[assignment]


class DescribeReportDefinitionsPaginator(_DescribeReportDefinitionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cur/paginator/DescribeReportDefinitions.html#CostandUsageReportService.Paginator.DescribeReportDefinitions)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cur/paginators/#describereportdefinitionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeReportDefinitionsRequestPaginateTypeDef]
    ) -> PageIterator[DescribeReportDefinitionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cur/paginator/DescribeReportDefinitions.html#CostandUsageReportService.Paginator.DescribeReportDefinitions.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cur/paginators/#describereportdefinitionspaginator)
        """
