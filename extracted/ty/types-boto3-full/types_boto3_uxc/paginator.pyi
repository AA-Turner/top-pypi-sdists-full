"""
Type annotations for uxc service client paginators.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_uxc/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from types_boto3_uxc.client import UserExperienceCustomizationClient
    from types_boto3_uxc.paginator import (
        ListServicesPaginator,
    )

    session = Session()
    client: UserExperienceCustomizationClient = session.client("uxc")

    list_services_paginator: ListServicesPaginator = client.get_paginator("list_services")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from botocore.paginate import PageIterator, Paginator

from .type_defs import ListServicesInputPaginateTypeDef, ListServicesOutputTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ListServicesPaginator",)

if TYPE_CHECKING:
    _ListServicesPaginatorBase = Paginator[ListServicesOutputTypeDef]
else:
    _ListServicesPaginatorBase = Paginator  # type: ignore[assignment]

class ListServicesPaginator(_ListServicesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/uxc/paginator/ListServices.html#UserExperienceCustomization.Paginator.ListServices)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_uxc/paginators/#listservicespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListServicesInputPaginateTypeDef]
    ) -> PageIterator[ListServicesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/uxc/paginator/ListServices.html#UserExperienceCustomization.Paginator.ListServices.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_uxc/paginators/#listservicespaginator)
        """
