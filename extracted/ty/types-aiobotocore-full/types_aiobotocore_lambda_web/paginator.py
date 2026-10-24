"""
Type annotations for lambda-web service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_web/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_lambda_web.client import LambdaWebClient
    from types_aiobotocore_lambda_web.paginator import (
        ListWebFunctionEndpointsPaginator,
        ListWebFunctionRevisionsPaginator,
        ListWebFunctionsPaginator,
    )

    session = get_session()
    with session.create_client("lambda-web") as client:
        client: LambdaWebClient

        list_web_function_endpoints_paginator: ListWebFunctionEndpointsPaginator = client.get_paginator("list_web_function_endpoints")
        list_web_function_revisions_paginator: ListWebFunctionRevisionsPaginator = client.get_paginator("list_web_function_revisions")
        list_web_functions_paginator: ListWebFunctionsPaginator = client.get_paginator("list_web_functions")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListWebFunctionEndpointsRequestPaginateTypeDef,
    ListWebFunctionEndpointsResponseTypeDef,
    ListWebFunctionRevisionsRequestPaginateTypeDef,
    ListWebFunctionRevisionsResponseTypeDef,
    ListWebFunctionsRequestPaginateTypeDef,
    ListWebFunctionsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListWebFunctionEndpointsPaginator",
    "ListWebFunctionRevisionsPaginator",
    "ListWebFunctionsPaginator",
)


if TYPE_CHECKING:
    _ListWebFunctionEndpointsPaginatorBase = AioPaginator[ListWebFunctionEndpointsResponseTypeDef]
else:
    _ListWebFunctionEndpointsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListWebFunctionEndpointsPaginator(_ListWebFunctionEndpointsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-web/paginator/ListWebFunctionEndpoints.html#LambdaWeb.Paginator.ListWebFunctionEndpoints)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_web/paginators/#listwebfunctionendpointspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListWebFunctionEndpointsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListWebFunctionEndpointsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-web/paginator/ListWebFunctionEndpoints.html#LambdaWeb.Paginator.ListWebFunctionEndpoints.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_web/paginators/#listwebfunctionendpointspaginator)
        """


if TYPE_CHECKING:
    _ListWebFunctionRevisionsPaginatorBase = AioPaginator[ListWebFunctionRevisionsResponseTypeDef]
else:
    _ListWebFunctionRevisionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListWebFunctionRevisionsPaginator(_ListWebFunctionRevisionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-web/paginator/ListWebFunctionRevisions.html#LambdaWeb.Paginator.ListWebFunctionRevisions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_web/paginators/#listwebfunctionrevisionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListWebFunctionRevisionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListWebFunctionRevisionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-web/paginator/ListWebFunctionRevisions.html#LambdaWeb.Paginator.ListWebFunctionRevisions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_web/paginators/#listwebfunctionrevisionspaginator)
        """


if TYPE_CHECKING:
    _ListWebFunctionsPaginatorBase = AioPaginator[ListWebFunctionsResponseTypeDef]
else:
    _ListWebFunctionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListWebFunctionsPaginator(_ListWebFunctionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-web/paginator/ListWebFunctions.html#LambdaWeb.Paginator.ListWebFunctions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_web/paginators/#listwebfunctionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListWebFunctionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListWebFunctionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-web/paginator/ListWebFunctions.html#LambdaWeb.Paginator.ListWebFunctions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_web/paginators/#listwebfunctionspaginator)
        """
