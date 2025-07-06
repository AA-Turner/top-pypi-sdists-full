"""
Type annotations for cognito-identity service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_identity/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_cognito_identity.client import CognitoIdentityClient
    from types_aiobotocore_cognito_identity.paginator import (
        ListIdentityPoolsPaginator,
    )

    session = get_session()
    with session.create_client("cognito-identity") as client:
        client: CognitoIdentityClient

        list_identity_pools_paginator: ListIdentityPoolsPaginator = client.get_paginator("list_identity_pools")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import ListIdentityPoolsInputPaginateTypeDef, ListIdentityPoolsResponseTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ListIdentityPoolsPaginator",)

if TYPE_CHECKING:
    _ListIdentityPoolsPaginatorBase = AioPaginator[ListIdentityPoolsResponseTypeDef]
else:
    _ListIdentityPoolsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListIdentityPoolsPaginator(_ListIdentityPoolsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-identity/paginator/ListIdentityPools.html#CognitoIdentity.Paginator.ListIdentityPools)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_identity/paginators/#listidentitypoolspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListIdentityPoolsInputPaginateTypeDef]
    ) -> AioPageIterator[ListIdentityPoolsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-identity/paginator/ListIdentityPools.html#CognitoIdentity.Paginator.ListIdentityPools.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_identity/paginators/#listidentitypoolspaginator)
        """
