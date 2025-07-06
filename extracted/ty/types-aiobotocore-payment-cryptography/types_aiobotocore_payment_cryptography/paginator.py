"""
Type annotations for payment-cryptography service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_payment_cryptography/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_payment_cryptography.client import PaymentCryptographyControlPlaneClient
    from types_aiobotocore_payment_cryptography.paginator import (
        ListAliasesPaginator,
        ListKeysPaginator,
        ListTagsForResourcePaginator,
    )

    session = get_session()
    with session.create_client("payment-cryptography") as client:
        client: PaymentCryptographyControlPlaneClient

        list_aliases_paginator: ListAliasesPaginator = client.get_paginator("list_aliases")
        list_keys_paginator: ListKeysPaginator = client.get_paginator("list_keys")
        list_tags_for_resource_paginator: ListTagsForResourcePaginator = client.get_paginator("list_tags_for_resource")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListAliasesInputPaginateTypeDef,
    ListAliasesOutputTypeDef,
    ListKeysInputPaginateTypeDef,
    ListKeysOutputTypeDef,
    ListTagsForResourceInputPaginateTypeDef,
    ListTagsForResourceOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ListAliasesPaginator", "ListKeysPaginator", "ListTagsForResourcePaginator")


if TYPE_CHECKING:
    _ListAliasesPaginatorBase = AioPaginator[ListAliasesOutputTypeDef]
else:
    _ListAliasesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListAliasesPaginator(_ListAliasesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payment-cryptography/paginator/ListAliases.html#PaymentCryptographyControlPlane.Paginator.ListAliases)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_payment_cryptography/paginators/#listaliasespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAliasesInputPaginateTypeDef]
    ) -> AioPageIterator[ListAliasesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payment-cryptography/paginator/ListAliases.html#PaymentCryptographyControlPlane.Paginator.ListAliases.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_payment_cryptography/paginators/#listaliasespaginator)
        """


if TYPE_CHECKING:
    _ListKeysPaginatorBase = AioPaginator[ListKeysOutputTypeDef]
else:
    _ListKeysPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListKeysPaginator(_ListKeysPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payment-cryptography/paginator/ListKeys.html#PaymentCryptographyControlPlane.Paginator.ListKeys)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_payment_cryptography/paginators/#listkeyspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListKeysInputPaginateTypeDef]
    ) -> AioPageIterator[ListKeysOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payment-cryptography/paginator/ListKeys.html#PaymentCryptographyControlPlane.Paginator.ListKeys.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_payment_cryptography/paginators/#listkeyspaginator)
        """


if TYPE_CHECKING:
    _ListTagsForResourcePaginatorBase = AioPaginator[ListTagsForResourceOutputTypeDef]
else:
    _ListTagsForResourcePaginatorBase = AioPaginator  # type: ignore[assignment]


class ListTagsForResourcePaginator(_ListTagsForResourcePaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payment-cryptography/paginator/ListTagsForResource.html#PaymentCryptographyControlPlane.Paginator.ListTagsForResource)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_payment_cryptography/paginators/#listtagsforresourcepaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTagsForResourceInputPaginateTypeDef]
    ) -> AioPageIterator[ListTagsForResourceOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payment-cryptography/paginator/ListTagsForResource.html#PaymentCryptographyControlPlane.Paginator.ListTagsForResource.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_payment_cryptography/paginators/#listtagsforresourcepaginator)
        """
