"""
Type annotations for lambda-web service client paginators.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lambda_web/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from types_boto3_lambda_web.client import LambdaWebClient
    from types_boto3_lambda_web.paginator import (
        ListWebFunctionEndpointsPaginator,
        ListWebFunctionRevisionsPaginator,
        ListWebFunctionsPaginator,
    )

    session = Session()
    client: LambdaWebClient = session.client("lambda-web")

    list_web_function_endpoints_paginator: ListWebFunctionEndpointsPaginator = client.get_paginator("list_web_function_endpoints")
    list_web_function_revisions_paginator: ListWebFunctionRevisionsPaginator = client.get_paginator("list_web_function_revisions")
    list_web_functions_paginator: ListWebFunctionsPaginator = client.get_paginator("list_web_functions")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from botocore.paginate import PageIterator, Paginator

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
    _ListWebFunctionEndpointsPaginatorBase = Paginator[ListWebFunctionEndpointsResponseTypeDef]
else:
    _ListWebFunctionEndpointsPaginatorBase = Paginator  # type: ignore[assignment]

class ListWebFunctionEndpointsPaginator(_ListWebFunctionEndpointsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-web/paginator/ListWebFunctionEndpoints.html#LambdaWeb.Paginator.ListWebFunctionEndpoints)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lambda_web/paginators/#listwebfunctionendpointspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListWebFunctionEndpointsRequestPaginateTypeDef]
    ) -> PageIterator[ListWebFunctionEndpointsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-web/paginator/ListWebFunctionEndpoints.html#LambdaWeb.Paginator.ListWebFunctionEndpoints.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lambda_web/paginators/#listwebfunctionendpointspaginator)
        """

if TYPE_CHECKING:
    _ListWebFunctionRevisionsPaginatorBase = Paginator[ListWebFunctionRevisionsResponseTypeDef]
else:
    _ListWebFunctionRevisionsPaginatorBase = Paginator  # type: ignore[assignment]

class ListWebFunctionRevisionsPaginator(_ListWebFunctionRevisionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-web/paginator/ListWebFunctionRevisions.html#LambdaWeb.Paginator.ListWebFunctionRevisions)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lambda_web/paginators/#listwebfunctionrevisionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListWebFunctionRevisionsRequestPaginateTypeDef]
    ) -> PageIterator[ListWebFunctionRevisionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-web/paginator/ListWebFunctionRevisions.html#LambdaWeb.Paginator.ListWebFunctionRevisions.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lambda_web/paginators/#listwebfunctionrevisionspaginator)
        """

if TYPE_CHECKING:
    _ListWebFunctionsPaginatorBase = Paginator[ListWebFunctionsResponseTypeDef]
else:
    _ListWebFunctionsPaginatorBase = Paginator  # type: ignore[assignment]

class ListWebFunctionsPaginator(_ListWebFunctionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-web/paginator/ListWebFunctions.html#LambdaWeb.Paginator.ListWebFunctions)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lambda_web/paginators/#listwebfunctionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListWebFunctionsRequestPaginateTypeDef]
    ) -> PageIterator[ListWebFunctionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-web/paginator/ListWebFunctions.html#LambdaWeb.Paginator.ListWebFunctions.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lambda_web/paginators/#listwebfunctionspaginator)
        """
