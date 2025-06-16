"""
Main interface for redshift-data service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift_data/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_redshift_data import (
        Client,
        DescribeTablePaginator,
        GetStatementResultPaginator,
        GetStatementResultV2Paginator,
        ListDatabasesPaginator,
        ListSchemasPaginator,
        ListStatementsPaginator,
        ListTablesPaginator,
        RedshiftDataAPIServiceClient,
    )

    session = get_session()
    async with session.create_client("redshift-data") as client:
        client: RedshiftDataAPIServiceClient
        ...


    describe_table_paginator: DescribeTablePaginator = client.get_paginator("describe_table")
    get_statement_result_paginator: GetStatementResultPaginator = client.get_paginator("get_statement_result")
    get_statement_result_v2_paginator: GetStatementResultV2Paginator = client.get_paginator("get_statement_result_v2")
    list_databases_paginator: ListDatabasesPaginator = client.get_paginator("list_databases")
    list_schemas_paginator: ListSchemasPaginator = client.get_paginator("list_schemas")
    list_statements_paginator: ListStatementsPaginator = client.get_paginator("list_statements")
    list_tables_paginator: ListTablesPaginator = client.get_paginator("list_tables")
    ```
"""

from .client import RedshiftDataAPIServiceClient
from .paginator import (
    DescribeTablePaginator,
    GetStatementResultPaginator,
    GetStatementResultV2Paginator,
    ListDatabasesPaginator,
    ListSchemasPaginator,
    ListStatementsPaginator,
    ListTablesPaginator,
)

Client = RedshiftDataAPIServiceClient


__all__ = (
    "Client",
    "DescribeTablePaginator",
    "GetStatementResultPaginator",
    "GetStatementResultV2Paginator",
    "ListDatabasesPaginator",
    "ListSchemasPaginator",
    "ListStatementsPaginator",
    "ListTablesPaginator",
    "RedshiftDataAPIServiceClient",
)
