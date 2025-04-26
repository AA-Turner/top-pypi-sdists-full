"""
Type annotations for secretsmanager service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_secretsmanager/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_secretsmanager.client import SecretsManagerClient
    from types_aiobotocore_secretsmanager.paginator import (
        ListSecretsPaginator,
    )

    session = get_session()
    with session.create_client("secretsmanager") as client:
        client: SecretsManagerClient

        list_secrets_paginator: ListSecretsPaginator = client.get_paginator("list_secrets")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import ListSecretsRequestPaginateTypeDef, ListSecretsResponseTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ListSecretsPaginator",)


if TYPE_CHECKING:
    _ListSecretsPaginatorBase = AioPaginator[ListSecretsResponseTypeDef]
else:
    _ListSecretsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListSecretsPaginator(_ListSecretsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager/paginator/ListSecrets.html#SecretsManager.Paginator.ListSecrets)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_secretsmanager/paginators/#listsecretspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSecretsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListSecretsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager/paginator/ListSecrets.html#SecretsManager.Paginator.ListSecrets.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_secretsmanager/paginators/#listsecretspaginator)
        """
