"""
Type annotations for acm service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_acm.client import ACMClient
    from types_aiobotocore_acm.paginator import (
        ListCertificatesPaginator,
    )

    session = get_session()
    with session.create_client("acm") as client:
        client: ACMClient

        list_certificates_paginator: ListCertificatesPaginator = client.get_paginator("list_certificates")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import ListCertificatesRequestPaginateTypeDef, ListCertificatesResponseTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ListCertificatesPaginator",)

if TYPE_CHECKING:
    _ListCertificatesPaginatorBase = AioPaginator[ListCertificatesResponseTypeDef]
else:
    _ListCertificatesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListCertificatesPaginator(_ListCertificatesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/paginator/ListCertificates.html#ACM.Paginator.ListCertificates)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/paginators/#listcertificatespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCertificatesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListCertificatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/paginator/ListCertificates.html#ACM.Paginator.ListCertificates.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/paginators/#listcertificatespaginator)
        """
