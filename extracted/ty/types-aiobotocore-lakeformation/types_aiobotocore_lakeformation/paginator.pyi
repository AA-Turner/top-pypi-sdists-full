"""
Type annotations for lakeformation service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lakeformation/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_lakeformation.client import LakeFormationClient
    from types_aiobotocore_lakeformation.paginator import (
        GetWorkUnitsPaginator,
        ListDataCellsFilterPaginator,
        ListLFTagExpressionsPaginator,
        ListLFTagsPaginator,
        SearchDatabasesByLFTagsPaginator,
        SearchTablesByLFTagsPaginator,
    )

    session = get_session()
    with session.create_client("lakeformation") as client:
        client: LakeFormationClient

        get_work_units_paginator: GetWorkUnitsPaginator = client.get_paginator("get_work_units")
        list_data_cells_filter_paginator: ListDataCellsFilterPaginator = client.get_paginator("list_data_cells_filter")
        list_lf_tag_expressions_paginator: ListLFTagExpressionsPaginator = client.get_paginator("list_lf_tag_expressions")
        list_lf_tags_paginator: ListLFTagsPaginator = client.get_paginator("list_lf_tags")
        search_databases_by_lf_tags_paginator: SearchDatabasesByLFTagsPaginator = client.get_paginator("search_databases_by_lf_tags")
        search_tables_by_lf_tags_paginator: SearchTablesByLFTagsPaginator = client.get_paginator("search_tables_by_lf_tags")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    GetWorkUnitsRequestPaginateTypeDef,
    GetWorkUnitsResponseTypeDef,
    ListDataCellsFilterRequestPaginateTypeDef,
    ListDataCellsFilterResponseTypeDef,
    ListLFTagExpressionsRequestPaginateTypeDef,
    ListLFTagExpressionsResponseTypeDef,
    ListLFTagsRequestPaginateTypeDef,
    ListLFTagsResponseTypeDef,
    SearchDatabasesByLFTagsRequestPaginateTypeDef,
    SearchDatabasesByLFTagsResponseTypeDef,
    SearchTablesByLFTagsRequestPaginateTypeDef,
    SearchTablesByLFTagsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "GetWorkUnitsPaginator",
    "ListDataCellsFilterPaginator",
    "ListLFTagExpressionsPaginator",
    "ListLFTagsPaginator",
    "SearchDatabasesByLFTagsPaginator",
    "SearchTablesByLFTagsPaginator",
)

if TYPE_CHECKING:
    _GetWorkUnitsPaginatorBase = AioPaginator[GetWorkUnitsResponseTypeDef]
else:
    _GetWorkUnitsPaginatorBase = AioPaginator  # type: ignore[assignment]

class GetWorkUnitsPaginator(_GetWorkUnitsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lakeformation/paginator/GetWorkUnits.html#LakeFormation.Paginator.GetWorkUnits)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lakeformation/paginators/#getworkunitspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetWorkUnitsRequestPaginateTypeDef]
    ) -> AioPageIterator[GetWorkUnitsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lakeformation/paginator/GetWorkUnits.html#LakeFormation.Paginator.GetWorkUnits.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lakeformation/paginators/#getworkunitspaginator)
        """

if TYPE_CHECKING:
    _ListDataCellsFilterPaginatorBase = AioPaginator[ListDataCellsFilterResponseTypeDef]
else:
    _ListDataCellsFilterPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListDataCellsFilterPaginator(_ListDataCellsFilterPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lakeformation/paginator/ListDataCellsFilter.html#LakeFormation.Paginator.ListDataCellsFilter)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lakeformation/paginators/#listdatacellsfilterpaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDataCellsFilterRequestPaginateTypeDef]
    ) -> AioPageIterator[ListDataCellsFilterResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lakeformation/paginator/ListDataCellsFilter.html#LakeFormation.Paginator.ListDataCellsFilter.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lakeformation/paginators/#listdatacellsfilterpaginator)
        """

if TYPE_CHECKING:
    _ListLFTagExpressionsPaginatorBase = AioPaginator[ListLFTagExpressionsResponseTypeDef]
else:
    _ListLFTagExpressionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListLFTagExpressionsPaginator(_ListLFTagExpressionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lakeformation/paginator/ListLFTagExpressions.html#LakeFormation.Paginator.ListLFTagExpressions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lakeformation/paginators/#listlftagexpressionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListLFTagExpressionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListLFTagExpressionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lakeformation/paginator/ListLFTagExpressions.html#LakeFormation.Paginator.ListLFTagExpressions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lakeformation/paginators/#listlftagexpressionspaginator)
        """

if TYPE_CHECKING:
    _ListLFTagsPaginatorBase = AioPaginator[ListLFTagsResponseTypeDef]
else:
    _ListLFTagsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListLFTagsPaginator(_ListLFTagsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lakeformation/paginator/ListLFTags.html#LakeFormation.Paginator.ListLFTags)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lakeformation/paginators/#listlftagspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListLFTagsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListLFTagsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lakeformation/paginator/ListLFTags.html#LakeFormation.Paginator.ListLFTags.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lakeformation/paginators/#listlftagspaginator)
        """

if TYPE_CHECKING:
    _SearchDatabasesByLFTagsPaginatorBase = AioPaginator[SearchDatabasesByLFTagsResponseTypeDef]
else:
    _SearchDatabasesByLFTagsPaginatorBase = AioPaginator  # type: ignore[assignment]

class SearchDatabasesByLFTagsPaginator(_SearchDatabasesByLFTagsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lakeformation/paginator/SearchDatabasesByLFTags.html#LakeFormation.Paginator.SearchDatabasesByLFTags)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lakeformation/paginators/#searchdatabasesbylftagspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[SearchDatabasesByLFTagsRequestPaginateTypeDef]
    ) -> AioPageIterator[SearchDatabasesByLFTagsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lakeformation/paginator/SearchDatabasesByLFTags.html#LakeFormation.Paginator.SearchDatabasesByLFTags.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lakeformation/paginators/#searchdatabasesbylftagspaginator)
        """

if TYPE_CHECKING:
    _SearchTablesByLFTagsPaginatorBase = AioPaginator[SearchTablesByLFTagsResponseTypeDef]
else:
    _SearchTablesByLFTagsPaginatorBase = AioPaginator  # type: ignore[assignment]

class SearchTablesByLFTagsPaginator(_SearchTablesByLFTagsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lakeformation/paginator/SearchTablesByLFTags.html#LakeFormation.Paginator.SearchTablesByLFTags)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lakeformation/paginators/#searchtablesbylftagspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[SearchTablesByLFTagsRequestPaginateTypeDef]
    ) -> AioPageIterator[SearchTablesByLFTagsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lakeformation/paginator/SearchTablesByLFTags.html#LakeFormation.Paginator.SearchTablesByLFTags.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lakeformation/paginators/#searchtablesbylftagspaginator)
        """
