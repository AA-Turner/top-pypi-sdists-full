"""
Type annotations for lambda-core service client paginators.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lambda_core/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_lambda_core.client import LambdaCoreClient
    from mypy_boto3_lambda_core.paginator import (
        ListNetworkConnectorVersionsPaginator,
        ListNetworkConnectorsPaginator,
        ListRuntimeAliasesPaginator,
        ListRuntimeVersionsPaginator,
        ListRuntimesPaginator,
    )

    session = Session()
    client: LambdaCoreClient = session.client("lambda-core")

    list_network_connector_versions_paginator: ListNetworkConnectorVersionsPaginator = client.get_paginator("list_network_connector_versions")
    list_network_connectors_paginator: ListNetworkConnectorsPaginator = client.get_paginator("list_network_connectors")
    list_runtime_aliases_paginator: ListRuntimeAliasesPaginator = client.get_paginator("list_runtime_aliases")
    list_runtime_versions_paginator: ListRuntimeVersionsPaginator = client.get_paginator("list_runtime_versions")
    list_runtimes_paginator: ListRuntimesPaginator = client.get_paginator("list_runtimes")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListNetworkConnectorsRequestPaginateTypeDef,
    ListNetworkConnectorsResponseTypeDef,
    ListNetworkConnectorVersionsRequestPaginateTypeDef,
    ListNetworkConnectorVersionsResponseTypeDef,
    ListRuntimeAliasesRequestPaginateTypeDef,
    ListRuntimeAliasesResponseTypeDef,
    ListRuntimesRequestPaginateTypeDef,
    ListRuntimesResponseTypeDef,
    ListRuntimeVersionsRequestPaginateTypeDef,
    ListRuntimeVersionsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListNetworkConnectorVersionsPaginator",
    "ListNetworkConnectorsPaginator",
    "ListRuntimeAliasesPaginator",
    "ListRuntimeVersionsPaginator",
    "ListRuntimesPaginator",
)


if TYPE_CHECKING:
    _ListNetworkConnectorVersionsPaginatorBase = Paginator[
        ListNetworkConnectorVersionsResponseTypeDef
    ]
else:
    _ListNetworkConnectorVersionsPaginatorBase = Paginator  # type: ignore[assignment]


class ListNetworkConnectorVersionsPaginator(_ListNetworkConnectorVersionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-core/paginator/ListNetworkConnectorVersions.html#LambdaCore.Paginator.ListNetworkConnectorVersions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lambda_core/paginators/#listnetworkconnectorversionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListNetworkConnectorVersionsRequestPaginateTypeDef]
    ) -> PageIterator[ListNetworkConnectorVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-core/paginator/ListNetworkConnectorVersions.html#LambdaCore.Paginator.ListNetworkConnectorVersions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lambda_core/paginators/#listnetworkconnectorversionspaginator)
        """


if TYPE_CHECKING:
    _ListNetworkConnectorsPaginatorBase = Paginator[ListNetworkConnectorsResponseTypeDef]
else:
    _ListNetworkConnectorsPaginatorBase = Paginator  # type: ignore[assignment]


class ListNetworkConnectorsPaginator(_ListNetworkConnectorsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-core/paginator/ListNetworkConnectors.html#LambdaCore.Paginator.ListNetworkConnectors)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lambda_core/paginators/#listnetworkconnectorspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListNetworkConnectorsRequestPaginateTypeDef]
    ) -> PageIterator[ListNetworkConnectorsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-core/paginator/ListNetworkConnectors.html#LambdaCore.Paginator.ListNetworkConnectors.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lambda_core/paginators/#listnetworkconnectorspaginator)
        """


if TYPE_CHECKING:
    _ListRuntimeAliasesPaginatorBase = Paginator[ListRuntimeAliasesResponseTypeDef]
else:
    _ListRuntimeAliasesPaginatorBase = Paginator  # type: ignore[assignment]


class ListRuntimeAliasesPaginator(_ListRuntimeAliasesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-core/paginator/ListRuntimeAliases.html#LambdaCore.Paginator.ListRuntimeAliases)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lambda_core/paginators/#listruntimealiasespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRuntimeAliasesRequestPaginateTypeDef]
    ) -> PageIterator[ListRuntimeAliasesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-core/paginator/ListRuntimeAliases.html#LambdaCore.Paginator.ListRuntimeAliases.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lambda_core/paginators/#listruntimealiasespaginator)
        """


if TYPE_CHECKING:
    _ListRuntimeVersionsPaginatorBase = Paginator[ListRuntimeVersionsResponseTypeDef]
else:
    _ListRuntimeVersionsPaginatorBase = Paginator  # type: ignore[assignment]


class ListRuntimeVersionsPaginator(_ListRuntimeVersionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-core/paginator/ListRuntimeVersions.html#LambdaCore.Paginator.ListRuntimeVersions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lambda_core/paginators/#listruntimeversionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRuntimeVersionsRequestPaginateTypeDef]
    ) -> PageIterator[ListRuntimeVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-core/paginator/ListRuntimeVersions.html#LambdaCore.Paginator.ListRuntimeVersions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lambda_core/paginators/#listruntimeversionspaginator)
        """


if TYPE_CHECKING:
    _ListRuntimesPaginatorBase = Paginator[ListRuntimesResponseTypeDef]
else:
    _ListRuntimesPaginatorBase = Paginator  # type: ignore[assignment]


class ListRuntimesPaginator(_ListRuntimesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-core/paginator/ListRuntimes.html#LambdaCore.Paginator.ListRuntimes)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lambda_core/paginators/#listruntimespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRuntimesRequestPaginateTypeDef]
    ) -> PageIterator[ListRuntimesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-core/paginator/ListRuntimes.html#LambdaCore.Paginator.ListRuntimes.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lambda_core/paginators/#listruntimespaginator)
        """
