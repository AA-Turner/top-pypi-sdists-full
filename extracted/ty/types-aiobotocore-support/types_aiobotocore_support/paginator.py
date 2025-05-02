"""
Type annotations for support service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_support/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_support.client import SupportClient
    from types_aiobotocore_support.paginator import (
        DescribeCasesPaginator,
        DescribeCommunicationsPaginator,
    )

    session = get_session()
    with session.create_client("support") as client:
        client: SupportClient

        describe_cases_paginator: DescribeCasesPaginator = client.get_paginator("describe_cases")
        describe_communications_paginator: DescribeCommunicationsPaginator = client.get_paginator("describe_communications")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    DescribeCasesRequestPaginateTypeDef,
    DescribeCasesResponseTypeDef,
    DescribeCommunicationsRequestPaginateTypeDef,
    DescribeCommunicationsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("DescribeCasesPaginator", "DescribeCommunicationsPaginator")


if TYPE_CHECKING:
    _DescribeCasesPaginatorBase = AioPaginator[DescribeCasesResponseTypeDef]
else:
    _DescribeCasesPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeCasesPaginator(_DescribeCasesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support/paginator/DescribeCases.html#Support.Paginator.DescribeCases)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_support/paginators/#describecasespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeCasesRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeCasesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support/paginator/DescribeCases.html#Support.Paginator.DescribeCases.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_support/paginators/#describecasespaginator)
        """


if TYPE_CHECKING:
    _DescribeCommunicationsPaginatorBase = AioPaginator[DescribeCommunicationsResponseTypeDef]
else:
    _DescribeCommunicationsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeCommunicationsPaginator(_DescribeCommunicationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support/paginator/DescribeCommunications.html#Support.Paginator.DescribeCommunications)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_support/paginators/#describecommunicationspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeCommunicationsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeCommunicationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support/paginator/DescribeCommunications.html#Support.Paginator.DescribeCommunications.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_support/paginators/#describecommunicationspaginator)
        """
