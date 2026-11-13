"""
Type annotations for secretsmanager service client paginators.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_secretsmanager/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from types_boto3_secretsmanager.client import SecretsManagerClient
    from types_boto3_secretsmanager.paginator import (
        ListResourcePoliciesPaginator,
        ListSecretsPaginator,
    )

    session = Session()
    client: SecretsManagerClient = session.client("secretsmanager")

    list_resource_policies_paginator: ListResourcePoliciesPaginator = client.get_paginator("list_resource_policies")
    list_secrets_paginator: ListSecretsPaginator = client.get_paginator("list_secrets")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListResourcePoliciesRequestPaginateTypeDef,
    ListResourcePoliciesResponseTypeDef,
    ListSecretsRequestPaginateTypeDef,
    ListSecretsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ListResourcePoliciesPaginator", "ListSecretsPaginator")


if TYPE_CHECKING:
    _ListResourcePoliciesPaginatorBase = Paginator[ListResourcePoliciesResponseTypeDef]
else:
    _ListResourcePoliciesPaginatorBase = Paginator  # type: ignore[assignment]


class ListResourcePoliciesPaginator(_ListResourcePoliciesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager/paginator/ListResourcePolicies.html#SecretsManager.Paginator.ListResourcePolicies)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_secretsmanager/paginators/#listresourcepoliciespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListResourcePoliciesRequestPaginateTypeDef]
    ) -> PageIterator[ListResourcePoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager/paginator/ListResourcePolicies.html#SecretsManager.Paginator.ListResourcePolicies.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_secretsmanager/paginators/#listresourcepoliciespaginator)
        """


if TYPE_CHECKING:
    _ListSecretsPaginatorBase = Paginator[ListSecretsResponseTypeDef]
else:
    _ListSecretsPaginatorBase = Paginator  # type: ignore[assignment]


class ListSecretsPaginator(_ListSecretsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager/paginator/ListSecrets.html#SecretsManager.Paginator.ListSecrets)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_secretsmanager/paginators/#listsecretspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSecretsRequestPaginateTypeDef]
    ) -> PageIterator[ListSecretsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager/paginator/ListSecrets.html#SecretsManager.Paginator.ListSecrets.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_secretsmanager/paginators/#listsecretspaginator)
        """
