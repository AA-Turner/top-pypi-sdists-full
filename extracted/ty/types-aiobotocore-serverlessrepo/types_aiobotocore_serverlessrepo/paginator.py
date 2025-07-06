"""
Type annotations for serverlessrepo service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_serverlessrepo/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_serverlessrepo.client import ServerlessApplicationRepositoryClient
    from types_aiobotocore_serverlessrepo.paginator import (
        ListApplicationDependenciesPaginator,
        ListApplicationVersionsPaginator,
        ListApplicationsPaginator,
    )

    session = get_session()
    with session.create_client("serverlessrepo") as client:
        client: ServerlessApplicationRepositoryClient

        list_application_dependencies_paginator: ListApplicationDependenciesPaginator = client.get_paginator("list_application_dependencies")
        list_application_versions_paginator: ListApplicationVersionsPaginator = client.get_paginator("list_application_versions")
        list_applications_paginator: ListApplicationsPaginator = client.get_paginator("list_applications")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListApplicationDependenciesRequestPaginateTypeDef,
    ListApplicationDependenciesResponseTypeDef,
    ListApplicationsRequestPaginateTypeDef,
    ListApplicationsResponseTypeDef,
    ListApplicationVersionsRequestPaginateTypeDef,
    ListApplicationVersionsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListApplicationDependenciesPaginator",
    "ListApplicationVersionsPaginator",
    "ListApplicationsPaginator",
)


if TYPE_CHECKING:
    _ListApplicationDependenciesPaginatorBase = AioPaginator[
        ListApplicationDependenciesResponseTypeDef
    ]
else:
    _ListApplicationDependenciesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListApplicationDependenciesPaginator(_ListApplicationDependenciesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/serverlessrepo/paginator/ListApplicationDependencies.html#ServerlessApplicationRepository.Paginator.ListApplicationDependencies)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_serverlessrepo/paginators/#listapplicationdependenciespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListApplicationDependenciesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListApplicationDependenciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/serverlessrepo/paginator/ListApplicationDependencies.html#ServerlessApplicationRepository.Paginator.ListApplicationDependencies.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_serverlessrepo/paginators/#listapplicationdependenciespaginator)
        """


if TYPE_CHECKING:
    _ListApplicationVersionsPaginatorBase = AioPaginator[ListApplicationVersionsResponseTypeDef]
else:
    _ListApplicationVersionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListApplicationVersionsPaginator(_ListApplicationVersionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/serverlessrepo/paginator/ListApplicationVersions.html#ServerlessApplicationRepository.Paginator.ListApplicationVersions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_serverlessrepo/paginators/#listapplicationversionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListApplicationVersionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListApplicationVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/serverlessrepo/paginator/ListApplicationVersions.html#ServerlessApplicationRepository.Paginator.ListApplicationVersions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_serverlessrepo/paginators/#listapplicationversionspaginator)
        """


if TYPE_CHECKING:
    _ListApplicationsPaginatorBase = AioPaginator[ListApplicationsResponseTypeDef]
else:
    _ListApplicationsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListApplicationsPaginator(_ListApplicationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/serverlessrepo/paginator/ListApplications.html#ServerlessApplicationRepository.Paginator.ListApplications)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_serverlessrepo/paginators/#listapplicationspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListApplicationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListApplicationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/serverlessrepo/paginator/ListApplications.html#ServerlessApplicationRepository.Paginator.ListApplications.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_serverlessrepo/paginators/#listapplicationspaginator)
        """
