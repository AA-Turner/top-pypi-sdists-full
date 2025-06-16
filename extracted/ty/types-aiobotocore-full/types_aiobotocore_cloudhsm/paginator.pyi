"""
Type annotations for cloudhsm service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsm/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_cloudhsm.client import CloudHSMClient
    from types_aiobotocore_cloudhsm.paginator import (
        ListHapgsPaginator,
        ListHsmsPaginator,
        ListLunaClientsPaginator,
    )

    session = get_session()
    with session.create_client("cloudhsm") as client:
        client: CloudHSMClient

        list_hapgs_paginator: ListHapgsPaginator = client.get_paginator("list_hapgs")
        list_hsms_paginator: ListHsmsPaginator = client.get_paginator("list_hsms")
        list_luna_clients_paginator: ListLunaClientsPaginator = client.get_paginator("list_luna_clients")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListHapgsRequestPaginateTypeDef,
    ListHapgsResponseTypeDef,
    ListHsmsRequestPaginateTypeDef,
    ListHsmsResponseTypeDef,
    ListLunaClientsRequestPaginateTypeDef,
    ListLunaClientsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ListHapgsPaginator", "ListHsmsPaginator", "ListLunaClientsPaginator")

if TYPE_CHECKING:
    _ListHapgsPaginatorBase = AioPaginator[ListHapgsResponseTypeDef]
else:
    _ListHapgsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListHapgsPaginator(_ListHapgsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsm/paginator/ListHapgs.html#CloudHSM.Paginator.ListHapgs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsm/paginators/#listhapgspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListHapgsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListHapgsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsm/paginator/ListHapgs.html#CloudHSM.Paginator.ListHapgs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsm/paginators/#listhapgspaginator)
        """

if TYPE_CHECKING:
    _ListHsmsPaginatorBase = AioPaginator[ListHsmsResponseTypeDef]
else:
    _ListHsmsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListHsmsPaginator(_ListHsmsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsm/paginator/ListHsms.html#CloudHSM.Paginator.ListHsms)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsm/paginators/#listhsmspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListHsmsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListHsmsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsm/paginator/ListHsms.html#CloudHSM.Paginator.ListHsms.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsm/paginators/#listhsmspaginator)
        """

if TYPE_CHECKING:
    _ListLunaClientsPaginatorBase = AioPaginator[ListLunaClientsResponseTypeDef]
else:
    _ListLunaClientsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListLunaClientsPaginator(_ListLunaClientsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsm/paginator/ListLunaClients.html#CloudHSM.Paginator.ListLunaClients)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsm/paginators/#listlunaclientspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListLunaClientsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListLunaClientsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsm/paginator/ListLunaClients.html#CloudHSM.Paginator.ListLunaClients.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsm/paginators/#listlunaclientspaginator)
        """
