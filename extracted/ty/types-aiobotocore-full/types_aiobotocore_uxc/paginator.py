"""
Type annotations for uxc service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_uxc/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_uxc.client import UserExperienceCustomizationClient
    from types_aiobotocore_uxc.paginator import (
        ListServicesPaginator,
    )

    session = get_session()
    with session.create_client("uxc") as client:
        client: UserExperienceCustomizationClient

        list_services_paginator: ListServicesPaginator = client.get_paginator("list_services")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import ListServicesInputPaginateTypeDef, ListServicesOutputTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ListServicesPaginator",)


if TYPE_CHECKING:
    _ListServicesPaginatorBase = AioPaginator[ListServicesOutputTypeDef]
else:
    _ListServicesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListServicesPaginator(_ListServicesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/uxc/paginator/ListServices.html#UserExperienceCustomization.Paginator.ListServices)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_uxc/paginators/#listservicespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListServicesInputPaginateTypeDef]
    ) -> AioPageIterator[ListServicesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/uxc/paginator/ListServices.html#UserExperienceCustomization.Paginator.ListServices.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_uxc/paginators/#listservicespaginator)
        """
