"""
Type annotations for amplify service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplify/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_amplify.client import AmplifyClient
    from types_aiobotocore_amplify.paginator import (
        ListAppsPaginator,
        ListBranchesPaginator,
        ListDomainAssociationsPaginator,
        ListJobsPaginator,
    )

    session = get_session()
    with session.create_client("amplify") as client:
        client: AmplifyClient

        list_apps_paginator: ListAppsPaginator = client.get_paginator("list_apps")
        list_branches_paginator: ListBranchesPaginator = client.get_paginator("list_branches")
        list_domain_associations_paginator: ListDomainAssociationsPaginator = client.get_paginator("list_domain_associations")
        list_jobs_paginator: ListJobsPaginator = client.get_paginator("list_jobs")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListAppsRequestPaginateTypeDef,
    ListAppsResultTypeDef,
    ListBranchesRequestPaginateTypeDef,
    ListBranchesResultTypeDef,
    ListDomainAssociationsRequestPaginateTypeDef,
    ListDomainAssociationsResultTypeDef,
    ListJobsRequestPaginateTypeDef,
    ListJobsResultTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListAppsPaginator",
    "ListBranchesPaginator",
    "ListDomainAssociationsPaginator",
    "ListJobsPaginator",
)


if TYPE_CHECKING:
    _ListAppsPaginatorBase = AioPaginator[ListAppsResultTypeDef]
else:
    _ListAppsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListAppsPaginator(_ListAppsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify/paginator/ListApps.html#Amplify.Paginator.ListApps)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplify/paginators/#listappspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAppsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAppsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify/paginator/ListApps.html#Amplify.Paginator.ListApps.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplify/paginators/#listappspaginator)
        """


if TYPE_CHECKING:
    _ListBranchesPaginatorBase = AioPaginator[ListBranchesResultTypeDef]
else:
    _ListBranchesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListBranchesPaginator(_ListBranchesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify/paginator/ListBranches.html#Amplify.Paginator.ListBranches)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplify/paginators/#listbranchespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListBranchesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListBranchesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify/paginator/ListBranches.html#Amplify.Paginator.ListBranches.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplify/paginators/#listbranchespaginator)
        """


if TYPE_CHECKING:
    _ListDomainAssociationsPaginatorBase = AioPaginator[ListDomainAssociationsResultTypeDef]
else:
    _ListDomainAssociationsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListDomainAssociationsPaginator(_ListDomainAssociationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify/paginator/ListDomainAssociations.html#Amplify.Paginator.ListDomainAssociations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplify/paginators/#listdomainassociationspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDomainAssociationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListDomainAssociationsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify/paginator/ListDomainAssociations.html#Amplify.Paginator.ListDomainAssociations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplify/paginators/#listdomainassociationspaginator)
        """


if TYPE_CHECKING:
    _ListJobsPaginatorBase = AioPaginator[ListJobsResultTypeDef]
else:
    _ListJobsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListJobsPaginator(_ListJobsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify/paginator/ListJobs.html#Amplify.Paginator.ListJobs)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplify/paginators/#listjobspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListJobsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListJobsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify/paginator/ListJobs.html#Amplify.Paginator.ListJobs.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplify/paginators/#listjobspaginator)
        """
