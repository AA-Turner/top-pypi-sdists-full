"""
Type annotations for amplifybackend service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifybackend/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_amplifybackend.client import AmplifyBackendClient
    from types_aiobotocore_amplifybackend.paginator import (
        ListBackendJobsPaginator,
    )

    session = get_session()
    with session.create_client("amplifybackend") as client:
        client: AmplifyBackendClient

        list_backend_jobs_paginator: ListBackendJobsPaginator = client.get_paginator("list_backend_jobs")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import ListBackendJobsRequestPaginateTypeDef, ListBackendJobsResponseTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ListBackendJobsPaginator",)

if TYPE_CHECKING:
    _ListBackendJobsPaginatorBase = AioPaginator[ListBackendJobsResponseTypeDef]
else:
    _ListBackendJobsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListBackendJobsPaginator(_ListBackendJobsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend/paginator/ListBackendJobs.html#AmplifyBackend.Paginator.ListBackendJobs)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifybackend/paginators/#listbackendjobspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListBackendJobsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListBackendJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend/paginator/ListBackendJobs.html#AmplifyBackend.Paginator.ListBackendJobs.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifybackend/paginators/#listbackendjobspaginator)
        """
