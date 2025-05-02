"""
Type annotations for applicationcostprofiler service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_applicationcostprofiler/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_applicationcostprofiler.client import ApplicationCostProfilerClient
    from types_aiobotocore_applicationcostprofiler.paginator import (
        ListReportDefinitionsPaginator,
    )

    session = get_session()
    with session.create_client("applicationcostprofiler") as client:
        client: ApplicationCostProfilerClient

        list_report_definitions_paginator: ListReportDefinitionsPaginator = client.get_paginator("list_report_definitions")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListReportDefinitionsRequestPaginateTypeDef,
    ListReportDefinitionsResultTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ListReportDefinitionsPaginator",)

if TYPE_CHECKING:
    _ListReportDefinitionsPaginatorBase = AioPaginator[ListReportDefinitionsResultTypeDef]
else:
    _ListReportDefinitionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListReportDefinitionsPaginator(_ListReportDefinitionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/applicationcostprofiler/paginator/ListReportDefinitions.html#ApplicationCostProfiler.Paginator.ListReportDefinitions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_applicationcostprofiler/paginators/#listreportdefinitionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListReportDefinitionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListReportDefinitionsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/applicationcostprofiler/paginator/ListReportDefinitions.html#ApplicationCostProfiler.Paginator.ListReportDefinitions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_applicationcostprofiler/paginators/#listreportdefinitionspaginator)
        """
