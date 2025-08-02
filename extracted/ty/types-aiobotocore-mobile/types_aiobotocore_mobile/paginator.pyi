"""
Type annotations for mobile service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mobile/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_mobile.client import MobileClient
    from types_aiobotocore_mobile.paginator import (
        ListBundlesPaginator,
        ListProjectsPaginator,
    )

    session = get_session()
    with session.create_client("mobile") as client:
        client: MobileClient

        list_bundles_paginator: ListBundlesPaginator = client.get_paginator("list_bundles")
        list_projects_paginator: ListProjectsPaginator = client.get_paginator("list_projects")
    ```
"""

from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import ListBundlesResultTypeDef, ListProjectsResultTypeDef, PaginatorConfigTypeDef

__all__ = ("ListBundlesPaginator", "ListProjectsPaginator")

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListBundlesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mobile.html#Mobile.Paginator.ListBundles)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mobile/paginators/#listbundlespaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> AsyncIterator[ListBundlesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mobile.html#Mobile.Paginator.ListBundles.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mobile/paginators/#listbundlespaginator)
        """

class ListProjectsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mobile.html#Mobile.Paginator.ListProjects)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mobile/paginators/#listprojectspaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> AsyncIterator[ListProjectsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mobile.html#Mobile.Paginator.ListProjects.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mobile/paginators/#listprojectspaginator)
        """
