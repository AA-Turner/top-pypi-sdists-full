"""
Main interface for lakeformation service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lakeformation/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_lakeformation import (
        Client,
        GetWorkUnitsPaginator,
        LakeFormationClient,
        ListDataCellsFilterPaginator,
        ListLFTagExpressionsPaginator,
        ListLFTagsPaginator,
        SearchDatabasesByLFTagsPaginator,
        SearchTablesByLFTagsPaginator,
    )

    session = get_session()
    async with session.create_client("lakeformation") as client:
        client: LakeFormationClient
        ...


    get_work_units_paginator: GetWorkUnitsPaginator = client.get_paginator("get_work_units")
    list_data_cells_filter_paginator: ListDataCellsFilterPaginator = client.get_paginator("list_data_cells_filter")
    list_lf_tag_expressions_paginator: ListLFTagExpressionsPaginator = client.get_paginator("list_lf_tag_expressions")
    list_lf_tags_paginator: ListLFTagsPaginator = client.get_paginator("list_lf_tags")
    search_databases_by_lf_tags_paginator: SearchDatabasesByLFTagsPaginator = client.get_paginator("search_databases_by_lf_tags")
    search_tables_by_lf_tags_paginator: SearchTablesByLFTagsPaginator = client.get_paginator("search_tables_by_lf_tags")
    ```
"""

from .client import LakeFormationClient
from .paginator import (
    GetWorkUnitsPaginator,
    ListDataCellsFilterPaginator,
    ListLFTagExpressionsPaginator,
    ListLFTagsPaginator,
    SearchDatabasesByLFTagsPaginator,
    SearchTablesByLFTagsPaginator,
)

Client = LakeFormationClient

__all__ = (
    "Client",
    "GetWorkUnitsPaginator",
    "LakeFormationClient",
    "ListDataCellsFilterPaginator",
    "ListLFTagExpressionsPaginator",
    "ListLFTagsPaginator",
    "SearchDatabasesByLFTagsPaginator",
    "SearchTablesByLFTagsPaginator",
)
