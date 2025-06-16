"""
Type annotations for kms service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_kms.client import KMSClient
    from types_aiobotocore_kms.paginator import (
        DescribeCustomKeyStoresPaginator,
        ListAliasesPaginator,
        ListGrantsPaginator,
        ListKeyPoliciesPaginator,
        ListKeyRotationsPaginator,
        ListKeysPaginator,
        ListResourceTagsPaginator,
        ListRetirableGrantsPaginator,
    )

    session = get_session()
    with session.create_client("kms") as client:
        client: KMSClient

        describe_custom_key_stores_paginator: DescribeCustomKeyStoresPaginator = client.get_paginator("describe_custom_key_stores")
        list_aliases_paginator: ListAliasesPaginator = client.get_paginator("list_aliases")
        list_grants_paginator: ListGrantsPaginator = client.get_paginator("list_grants")
        list_key_policies_paginator: ListKeyPoliciesPaginator = client.get_paginator("list_key_policies")
        list_key_rotations_paginator: ListKeyRotationsPaginator = client.get_paginator("list_key_rotations")
        list_keys_paginator: ListKeysPaginator = client.get_paginator("list_keys")
        list_resource_tags_paginator: ListResourceTagsPaginator = client.get_paginator("list_resource_tags")
        list_retirable_grants_paginator: ListRetirableGrantsPaginator = client.get_paginator("list_retirable_grants")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    DescribeCustomKeyStoresRequestPaginateTypeDef,
    DescribeCustomKeyStoresResponseTypeDef,
    ListAliasesRequestPaginateTypeDef,
    ListAliasesResponseTypeDef,
    ListGrantsRequestPaginateTypeDef,
    ListGrantsResponseTypeDef,
    ListKeyPoliciesRequestPaginateTypeDef,
    ListKeyPoliciesResponseTypeDef,
    ListKeyRotationsRequestPaginateTypeDef,
    ListKeyRotationsResponseTypeDef,
    ListKeysRequestPaginateTypeDef,
    ListKeysResponseTypeDef,
    ListResourceTagsRequestPaginateTypeDef,
    ListResourceTagsResponseTypeDef,
    ListRetirableGrantsRequestPaginateTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "DescribeCustomKeyStoresPaginator",
    "ListAliasesPaginator",
    "ListGrantsPaginator",
    "ListKeyPoliciesPaginator",
    "ListKeyRotationsPaginator",
    "ListKeysPaginator",
    "ListResourceTagsPaginator",
    "ListRetirableGrantsPaginator",
)


if TYPE_CHECKING:
    _DescribeCustomKeyStoresPaginatorBase = AioPaginator[DescribeCustomKeyStoresResponseTypeDef]
else:
    _DescribeCustomKeyStoresPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeCustomKeyStoresPaginator(_DescribeCustomKeyStoresPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/paginator/DescribeCustomKeyStores.html#KMS.Paginator.DescribeCustomKeyStores)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/paginators/#describecustomkeystorespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeCustomKeyStoresRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeCustomKeyStoresResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/paginator/DescribeCustomKeyStores.html#KMS.Paginator.DescribeCustomKeyStores.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/paginators/#describecustomkeystorespaginator)
        """


if TYPE_CHECKING:
    _ListAliasesPaginatorBase = AioPaginator[ListAliasesResponseTypeDef]
else:
    _ListAliasesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListAliasesPaginator(_ListAliasesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/paginator/ListAliases.html#KMS.Paginator.ListAliases)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/paginators/#listaliasespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAliasesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAliasesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/paginator/ListAliases.html#KMS.Paginator.ListAliases.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/paginators/#listaliasespaginator)
        """


if TYPE_CHECKING:
    _ListGrantsPaginatorBase = AioPaginator[ListGrantsResponseTypeDef]
else:
    _ListGrantsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListGrantsPaginator(_ListGrantsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/paginator/ListGrants.html#KMS.Paginator.ListGrants)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/paginators/#listgrantspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListGrantsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListGrantsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/paginator/ListGrants.html#KMS.Paginator.ListGrants.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/paginators/#listgrantspaginator)
        """


if TYPE_CHECKING:
    _ListKeyPoliciesPaginatorBase = AioPaginator[ListKeyPoliciesResponseTypeDef]
else:
    _ListKeyPoliciesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListKeyPoliciesPaginator(_ListKeyPoliciesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/paginator/ListKeyPolicies.html#KMS.Paginator.ListKeyPolicies)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/paginators/#listkeypoliciespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListKeyPoliciesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListKeyPoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/paginator/ListKeyPolicies.html#KMS.Paginator.ListKeyPolicies.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/paginators/#listkeypoliciespaginator)
        """


if TYPE_CHECKING:
    _ListKeyRotationsPaginatorBase = AioPaginator[ListKeyRotationsResponseTypeDef]
else:
    _ListKeyRotationsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListKeyRotationsPaginator(_ListKeyRotationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/paginator/ListKeyRotations.html#KMS.Paginator.ListKeyRotations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/paginators/#listkeyrotationspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListKeyRotationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListKeyRotationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/paginator/ListKeyRotations.html#KMS.Paginator.ListKeyRotations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/paginators/#listkeyrotationspaginator)
        """


if TYPE_CHECKING:
    _ListKeysPaginatorBase = AioPaginator[ListKeysResponseTypeDef]
else:
    _ListKeysPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListKeysPaginator(_ListKeysPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/paginator/ListKeys.html#KMS.Paginator.ListKeys)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/paginators/#listkeyspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListKeysRequestPaginateTypeDef]
    ) -> AioPageIterator[ListKeysResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/paginator/ListKeys.html#KMS.Paginator.ListKeys.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/paginators/#listkeyspaginator)
        """


if TYPE_CHECKING:
    _ListResourceTagsPaginatorBase = AioPaginator[ListResourceTagsResponseTypeDef]
else:
    _ListResourceTagsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListResourceTagsPaginator(_ListResourceTagsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/paginator/ListResourceTags.html#KMS.Paginator.ListResourceTags)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/paginators/#listresourcetagspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListResourceTagsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListResourceTagsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/paginator/ListResourceTags.html#KMS.Paginator.ListResourceTags.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/paginators/#listresourcetagspaginator)
        """


if TYPE_CHECKING:
    _ListRetirableGrantsPaginatorBase = AioPaginator[ListGrantsResponseTypeDef]
else:
    _ListRetirableGrantsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListRetirableGrantsPaginator(_ListRetirableGrantsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/paginator/ListRetirableGrants.html#KMS.Paginator.ListRetirableGrants)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/paginators/#listretirablegrantspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRetirableGrantsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListGrantsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/paginator/ListRetirableGrants.html#KMS.Paginator.ListRetirableGrants.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/paginators/#listretirablegrantspaginator)
        """
